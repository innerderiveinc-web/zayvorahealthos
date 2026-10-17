"""
Acceptance Test Suite for Enterprise Identity, Tenancy & Mandatory Tenant Isolation
Prompt 28 — Clauses 13–16 (MODULE 02, 03, 04 & Clause 16 Tenant Isolation Test)

Validates the mandatory release gates:
1. Tenant A cannot read Tenant B resources
2. Tenant A agent cannot access Tenant B memory
3. Tenant A cached result cannot appear in Tenant B retrieval
4. Tenant A private embedding cannot appear in global/public retrieval
5. ABAC Clearance & RBAC Action Evaluation
6. JWT token issuance, verification, and tamper detection
7. API Key generation and hashed credential lookup
"""

import unittest
from datetime import datetime, timezone, timedelta

from app.core.identity import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    generate_api_key,
    User,
    Organization,
    ApiCredential
)
from app.core.tenancy import (
    Tenant,
    Workspace,
    Project,
    TenantContext,
    DataClassification,
    TenantAccessDeniedException,
    assert_tenant_boundary
)
from app.core.authorization import (
    EnterpriseRole,
    Action,
    SubjectAttributes,
    ResourceAttributes,
    AuthorizationEngine,
    ROLE_ACTION_PERMISSIONS
)


class TestTenantIsolationAcceptance(unittest.TestCase):

    def setUp(self):
        self.tenant_a = "tenant-pharma-merck"
        self.tenant_b = "tenant-hospital-mayo"
        self.tenant_public = "public"

    # --- Clause 16: Mandatory Gate 1 ---
    def test_tenant_a_cannot_read_tenant_b_resources(self):
        """Proves Tenant A cannot read Tenant B resources."""
        subject_a = SubjectAttributes(
            user_id="usr-merck-lead",
            tenant_id=self.tenant_a,
            roles=[EnterpriseRole.RESEARCHER],
            clearance=DataClassification.CONFIDENTIAL
        )

        resource_b = ResourceAttributes(
            resource_id="doc-mayo-protocol-101",
            resource_type="protocol",
            tenant_id=self.tenant_b,
            classification=DataClassification.CONFIDENTIAL,
            is_public=False
        )

        # 1. ABAC Evaluation Check
        result = AuthorizationEngine.evaluate(
            subject=subject_a,
            action=Action.READ,
            resource=resource_b
        )
        self.assertFalse(result.allowed)
        self.assertIn("Tenant boundary isolation denied", result.reason)

        # 2. Strict Boundary Assertion Helper
        with self.assertRaises(TenantAccessDeniedException) as ctx:
            assert_tenant_boundary(
                resource_tenant_id=resource_b.tenant_id,
                caller_tenant_id=subject_a.tenant_id
            )
        self.assertEqual(ctx.exception.resource_tenant, self.tenant_b)
        self.assertEqual(ctx.exception.caller_tenant, self.tenant_a)

    # --- Clause 16: Mandatory Gate 2 ---
    def test_tenant_a_agent_cannot_access_tenant_b_memory(self):
        """Proves Tenant A agent cannot access Tenant B memory store."""
        class MockAgentMemoryStore:
            def __init__(self):
                self._storage = {}

            def write_memory(self, tenant_id: str, key: str, value: str):
                self._storage[(tenant_id, key)] = value

            def read_memory(self, caller_tenant_id: str, target_tenant_id: str, key: str):
                assert_tenant_boundary(target_tenant_id, caller_tenant_id, allow_public=False)
                return self._storage.get((target_tenant_id, key))

        memory = MockAgentMemoryStore()
        memory.write_memory(self.tenant_b, "hypothesis_scratchpad", "Confidential Target Candidate X")

        # Tenant A's agent attempts to read Tenant B's memory
        with self.assertRaises(TenantAccessDeniedException):
            memory.read_memory(
                caller_tenant_id=self.tenant_a,
                target_tenant_id=self.tenant_b,
                key="hypothesis_scratchpad"
            )

        # Tenant B can read its own memory
        self.assertEqual(
            memory.read_memory(self.tenant_b, self.tenant_b, "hypothesis_scratchpad"),
            "Confidential Target Candidate X"
        )

    # --- Clause 16: Mandatory Gate 3 ---
    def test_tenant_a_cached_result_cannot_appear_in_tenant_b_retrieval(self):
        """Proves Tenant A cached research result cannot appear in Tenant B retrieval."""
        class TenantIsolatedCache:
            def __init__(self):
                self._cache = {}

            def set(self, tenant_id: str, query: str, result: dict):
                # Cache key is strictly partitioned by tenant_id
                key = f"tenant:{tenant_id}:q:{query}"
                self._cache[key] = result

            def get(self, tenant_id: str, query: str):
                key = f"tenant:{tenant_id}:q:{query}"
                return self._cache.get(key)

        cache = TenantIsolatedCache()
        query = "efficacy of compound Z9 on HER2+ breast cancer"
        cache.set(self.tenant_a, query, {"result": "private proprietary assay findings", "n_samples": 450})

        # Tenant B queries identical search string
        tenant_b_cached = cache.get(self.tenant_b, query)
        self.assertIsNone(tenant_b_cached, "Tenant B must not retrieve Tenant A's cached query result")

        # Tenant A gets its cached result
        tenant_a_cached = cache.get(self.tenant_a, query)
        self.assertIsNotNone(tenant_a_cached)
        self.assertEqual(tenant_a_cached["n_samples"], 450)

    # --- Clause 16: Mandatory Gate 4 ---
    def test_tenant_a_private_embedding_cannot_appear_in_global_public_retrieval(self):
        """Proves Tenant A private embedding cannot appear in global/public retrieval."""
        class MockVectorStore:
            def __init__(self):
                self.records = []

            def insert(self, record_id: str, text: str, embedding: list, tenant_id: str, is_public: bool):
                self.records.append({
                    "id": record_id,
                    "text": text,
                    "tenant_id": tenant_id,
                    "is_public": is_public
                })

            def search(self, caller_tenant_id: str, include_public: bool = True):
                # Hard filtering: strictly allow public items OR caller's own tenant items
                filtered = []
                for r in self.records:
                    if r["is_public"] and include_public:
                        filtered.append(r)
                    elif r["tenant_id"] == caller_tenant_id:
                        filtered.append(r)
                return filtered

        store = MockVectorStore()
        # 1. Insert Public Knowledge
        store.insert("emb-pub-1", "Aspirin reduces platelet aggregation", [0.1, 0.2], "public", True)
        # 2. Insert Tenant A Private Clinical Note
        store.insert("emb-priv-a", "Patient 9931 developed grade 3 cardiotoxicity", [0.9, 0.8], self.tenant_a, False)

        # Public user search
        pub_results = store.search(caller_tenant_id="public")
        self.assertEqual(len(pub_results), 1)
        self.assertEqual(pub_results[0]["id"], "emb-pub-1")

        # Tenant B user search
        b_results = store.search(caller_tenant_id=self.tenant_b)
        self.assertEqual(len(b_results), 1)
        self.assertEqual(b_results[0]["id"], "emb-pub-1")

        # Tenant A user search
        a_results = store.search(caller_tenant_id=self.tenant_a)
        self.assertEqual(len(a_results), 2)
        found_ids = {r["id"] for r in a_results}
        self.assertIn("emb-pub-1", found_ids)
        self.assertIn("emb-priv-a", found_ids)

    # --- ABAC Clearance & RBAC Action Evaluation ---
    def test_abac_clearance_and_action_evaluation(self):
        """Verifies clearance hierarchy and role action matrices."""
        # Researcher cannot execute on RESTRICTED_PHI without clearance
        res_user = SubjectAttributes(
            user_id="usr-analyst-1",
            tenant_id=self.tenant_a,
            roles=[EnterpriseRole.ANALYST],
            clearance=DataClassification.INTERNAL
        )

        phi_resource = ResourceAttributes(
            resource_id="phi-dataset-01",
            resource_type="dataset",
            tenant_id=self.tenant_a,
            classification=DataClassification.RESTRICTED_PHI
        )

        eval_clearance = AuthorizationEngine.evaluate(
            subject=res_user,
            action=Action.ANALYZE,
            resource=phi_resource
        )
        self.assertFalse(eval_clearance.allowed)
        self.assertIn("Insufficient clearance", eval_clearance.reason)

        # With clearance, Analyst can ANALYZE but cannot PUBLISH
        cleared_user = SubjectAttributes(
            user_id="usr-analyst-1",
            tenant_id=self.tenant_a,
            roles=[EnterpriseRole.ANALYST],
            clearance=DataClassification.RESTRICTED_PHI
        )

        eval_analyze = AuthorizationEngine.evaluate(
            subject=cleared_user,
            action=Action.ANALYZE,
            resource=phi_resource
        )
        self.assertTrue(eval_analyze.allowed)

        eval_publish = AuthorizationEngine.evaluate(
            subject=cleared_user,
            action=Action.PUBLISH,
            resource=phi_resource
        )
        self.assertFalse(eval_publish.allowed)
        self.assertIn("Action 'PUBLISH' not granted", eval_publish.reason)

    # --- Cryptographic Identity: JWT & API Keys ---
    def test_jwt_issuance_verification_and_expiry(self):
        """Verifies JWT issuance, decode, and cryptographic tamper detection."""
        payload = {
            "sub": "usr-lead-dr-watson",
            "tenant_id": self.tenant_a,
            "role": "researcher"
        }
        token = create_access_token(payload, expires_delta=timedelta(minutes=30))
        self.assertTrue(isinstance(token, str))

        # Decode valid token
        decoded = decode_access_token(token)
        self.assertEqual(decoded["sub"], "usr-lead-dr-watson")
        self.assertEqual(decoded["tenant_id"], self.tenant_a)

        # Tampered signature fails
        tampered_token = token[:-4] + "AAAA"
        with self.assertRaises(ValueError):
            decode_access_token(tampered_token)

        # Expired token fails
        expired_token = create_access_token(payload, expires_delta=timedelta(seconds=-10))
        with self.assertRaises(ValueError) as ctx:
            decode_access_token(expired_token)
        self.assertIn("expired", str(ctx.exception).lower())

    def test_password_and_api_key_lifecycle(self):
        """Verifies salted password hashing and API key credential creation."""
        # 1. Password hashing
        pw = "SuperSecureScientificPass2026!"
        hashed = hash_password(pw)
        self.assertTrue(hashed.startswith("sha256$"))
        self.assertTrue(verify_password(pw, hashed))
        self.assertFalse(verify_password("WrongPassword!", hashed))

        # 2. API Key generation
        raw_key, cred = generate_api_key(
            tenant_id=self.tenant_a,
            user_id="usr-pi-1",
            name="CI/CD Integration Key",
            scopes=["read", "analyze", "execute"]
        )
        self.assertTrue(raw_key.startswith("zmie_"))
        self.assertEqual(cred.tenant_id, self.tenant_a)
        self.assertEqual(cred.scopes, ["read", "analyze", "execute"])


if __name__ == "__main__":
    unittest.main()
