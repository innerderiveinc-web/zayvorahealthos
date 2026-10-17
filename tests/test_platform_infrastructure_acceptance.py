"""
ZMIE Medical Knowledge Infrastructure Platform — Acceptance Test Suite
Validates:
1. API Gateway, Credential Scopes, Hashing & Revocation
2. RAG Context Packet Engine & Token Accounting
3. Multi-System Medical Intelligence Queries (Modern, Unani, Ayurveda)
4. AI Model Router & Gateway (Task classification, Failover fallback, Firewall verification)
5. Webhook Dispatcher (HMAC-SHA256 signing, Tamper detection, Replay defense)
6. Official Python SDK bindings
7. Enterprise Tenant Isolation & Metered Usage Ledger
"""

import unittest
import time
from fastapi.testclient import TestClient

from app.main import app
from app.platform.gateway import APIGatewayEngine
from app.platform.webhooks import WebhookDispatcher
from zmie import ZMIE


class TestPlatformInfrastructureAcceptance(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_01_api_credential_lifecycle(self):
        # 1. Create API key
        raw_key, cred = APIGatewayEngine.create_api_key(
            tenant_id="tenant-mayo-01",
            owner="dr_chen@mayo.org",
            name="Mayo Decision Support Service",
            scopes=["knowledge:read", "rag:read", "safety:read"]
        )
        self.assertTrue(raw_key.startswith("zmie_production_"))
        self.assertEqual(cred.status, "active")
        self.assertEqual(cred.key_prefix, raw_key[:12])
        self.assertNotEqual(cred.key_hash, raw_key)  # SHA-256 hashed

        # 2. Authenticate key
        auth_cred = APIGatewayEngine.authenticate_key(raw_key, required_scope="knowledge:read")
        self.assertIsNotNone(auth_cred)
        self.assertEqual(auth_cred.tenant_id, "tenant-mayo-01")

        # 3. Unauthorized scope check
        unauthorized = APIGatewayEngine.authenticate_key(raw_key, required_scope="admin:write")
        self.assertIsNone(unauthorized)

        # 4. Revocation
        revoked = APIGatewayEngine.revoke_api_key(cred.credential_id)
        self.assertTrue(revoked)

        # 5. Verify revoked key cannot authenticate
        post_revoke_cred = APIGatewayEngine.authenticate_key(raw_key)
        self.assertIsNone(post_revoke_cred)

    def test_02_rag_context_packet_generation(self):
        # Create valid key
        raw_key, cred = APIGatewayEngine.create_api_key(
            tenant_id="tenant-cleveland-02",
            owner="ai_team@ccf.org",
            name="Cleveland Clinic RAG Integration"
        )

        response = self.client.post(
            "/v1/platform/rag/context",
            headers={"X-API-Key": raw_key},
            json={
                "query": "Metformin and Vitamin B12 deficiency",
                "evidence_minimum": "E4",
                "include_safety": True,
                "include_contradictions": True
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["query"], "Metformin and Vitamin B12 deficiency")
        self.assertEqual(data["knowledge_version"], "2026.10")
        self.assertGreaterEqual(len(data["verified_claims"]), 1)
        self.assertIn("safety_context", data)
        self.assertGreaterEqual(len(data["citations"]), 1)
        self.assertGreaterEqual(len(data["limitations"]), 1)
        self.assertGreater(data["context_token_estimate"], 0)

    def test_03_multi_system_intelligence_query(self):
        response = self.client.post(
            "/v1/platform/intelligence/query",
            json={
                "query": "Ashwagandha (Withania somnifera)",
                "systems": ["modern", "unani", "ayurveda"],
                "mode": "evidence"
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["query"], "Ashwagandha (Withania somnifera)")
        self.assertTrue(data["verified"])
        self.assertIn("cross_system_mappings", data["graph_context"])
        self.assertIn("unani", data["graph_context"]["cross_system_mappings"])
        self.assertIn("ayurveda", data["graph_context"]["cross_system_mappings"])
        self.assertGreaterEqual(len(data["citations"]), 1)

    def test_04_ai_model_router_with_failover_and_firewall(self):
        # 1. Fetch grounded context packet
        ctx_resp = self.client.post(
            "/v1/platform/rag/context",
            json={"query": "Boswellia serrata in osteoarthritis"}
        )
        self.assertEqual(ctx_resp.status_code, 200)
        ctx_packet = ctx_resp.json()

        # 2. Normal route with grounded context
        res_normal = self.client.post(
            "/v1/platform/ai/route",
            json={
                "task_type": "synthesis",
                "prompt": "Evaluate safety profile of Boswellia serrata in osteoarthritis",
                "context_packet": ctx_packet,
                "simulate_failure": False
            }
        )
        self.assertEqual(res_normal.status_code, 200)
        data_normal = res_normal.json()
        self.assertFalse(data_normal["fell_back"])
        self.assertEqual(data_normal["chosen_model"], "claude-3-5-sonnet")
        self.assertTrue(data_normal["firewall_pass"])

        # 3. Simulated failure -> Failover to fallback model
        res_failover = self.client.post(
            "/v1/platform/ai/route",
            json={
                "task_type": "synthesis",
                "prompt": "Evaluate safety profile of Boswellia serrata in osteoarthritis",
                "context_packet": ctx_packet,
                "simulate_failure": True
            }
        )
        self.assertEqual(res_failover.status_code, 200)
        data_failover = res_failover.json()
        self.assertTrue(data_failover["fell_back"])
        self.assertEqual(data_failover["chosen_model"], "gpt-4o")
        self.assertIn("Primary model", data_failover["error_msg"])
        self.assertTrue(data_failover["firewall_pass"])

    def test_05_webhook_hmac_signing_and_replay_protection(self):
        secret = "whsec_test_secret_key_12345"
        payload = b'{"event":"source.retracted","doi":"10.1000/bad-trial"}'
        ts = int(time.time())

        # 1. Correct signature verification
        sig = WebhookDispatcher.sign_payload(payload, secret, ts)
        self.assertTrue(WebhookDispatcher.verify_signature(payload, secret, sig, ts))

        # 2. Tampered payload fails
        tampered_payload = b'{"event":"source.retracted","doi":"10.1000/good-trial"}'
        self.assertFalse(WebhookDispatcher.verify_signature(tampered_payload, secret, sig, ts))

        # 3. Wrong secret fails
        wrong_sig = WebhookDispatcher.sign_payload(payload, "wrong_secret", ts)
        self.assertFalse(WebhookDispatcher.verify_signature(payload, secret, wrong_sig, ts))

        # 4. Replay attack with expired timestamp (> 300s) fails
        old_ts = ts - 400
        old_sig = WebhookDispatcher.sign_payload(payload, secret, old_ts)
        self.assertFalse(WebhookDispatcher.verify_signature(payload, secret, old_sig, old_ts, tolerance_seconds=300))

    def test_06_python_sdk_integration(self):
        raw_key, _ = APIGatewayEngine.create_api_key(
            tenant_id="tenant-biotech-42",
            owner="scientist@novartis-biotech.com",
            name="Novartis Discovery Pipeline"
        )

        sdk = ZMIE(api_key=raw_key, app_instance=app)

        # 1. SDK RAG Context
        rag = sdk.rag_context("Curcumin bioavailability and piperine co-administration")
        self.assertEqual(rag["knowledge_version"], "2026.10")
        self.assertGreaterEqual(len(rag["verified_claims"]), 1)

        # 2. SDK Intelligence Query
        intel = sdk.intelligence_query("Nigella sativa", systems=["modern", "unani"])
        self.assertTrue(intel["verified"])
        self.assertIn("unani", intel["graph_context"]["cross_system_mappings"])

        # 3. SDK AI Route
        routed = sdk.route_ai(
            task_type="classification",
            prompt="Classify drug-herb interaction risk for St. John's Wort and SSRIs"
        )
        self.assertEqual(routed["chosen_model"], "claude-3-5-haiku")

        # 4. SDK Webhook Verification static helper
        sec = "whsec_sdk_test_987"
        ts = int(time.time())
        sig = WebhookDispatcher.sign_payload(b"hello world", sec, ts)
        self.assertTrue(ZMIE.verify_webhook_signature("hello world", sec, sig, ts))
        self.assertFalse(ZMIE.verify_webhook_signature("tampered text", sec, sig, ts))

    def test_07_enterprise_metering_and_usage_ledger(self):
        raw_key, cred = APIGatewayEngine.create_api_key(
            tenant_id="tenant-enterprise-99",
            owner="billing@hospital-system.com",
            name="Regional Hospital Integration"
        )

        # Issue multiple calls with the key
        self.client.post("/v1/platform/rag/context", headers={"X-API-Key": raw_key}, json={"query": "Diabetes Type 2 guidelines"})
        self.client.post("/v1/platform/intelligence/query", headers={"X-API-Key": raw_key}, json={"query": "Insulin resistance"})

        # Check usage ledger
        usage = APIGatewayEngine.get_tenant_usage("tenant-enterprise-99")
        self.assertGreaterEqual(len(usage), 2)
        services = [u.service for u in usage]
        self.assertIn("rag_context", services)
        self.assertIn("intelligence", services)


if __name__ == "__main__":
    unittest.main()
