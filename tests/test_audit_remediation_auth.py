"""
Test Suite Verifying Phase 1 Audit Remediation:
- Elimination of 'key in token' auth bypass
- Strict 401 / 403 enforcement on /v1/admin/*, /v1/projects/*, /v1/security/audit
- Tenant isolation on project workspace queries and mutations
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import SecurityService, UserRole, API_KEYS_REGISTRY


class TestAuditRemediationAuth(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, raise_server_exceptions=False)

    def test_01_token_bypass_strictly_eliminated(self):
        """Tokens containing 'key' or 'test-key' must NOT be granted researcher access."""
        fake_tokens = [
            "fake-key",
            "bearer-key-exploit",
            "test-key",
            "my_secret_key_123",
            "invalid.jwt.token"
        ]
        for token in fake_tokens:
            resp = self.client.get(
                "/v1/projects",
                headers={"Authorization": f"Bearer {token}"}
            )
            self.assertEqual(
                resp.status_code, 401,
                f"Token '{token}' bypassed authentication! Got status {resp.status_code}"
            )

    def test_02_admin_telemetry_requires_admin(self):
        """GET /v1/admin/telemetry must fail closed without admin authentication."""
        # Unauthenticated -> 401
        resp_unauth = self.client.get("/v1/admin/telemetry")
        self.assertEqual(resp_unauth.status_code, 401)

        # Non-admin (Researcher key) -> 403
        resp_res = self.client.get(
            "/v1/admin/telemetry",
            headers={"X-ZMIE-API-KEY": "zmie-res-key-9921"}
        )
        self.assertEqual(resp_res.status_code, 403)

        # Admin key -> 200
        resp_adm = self.client.get(
            "/v1/admin/telemetry",
            headers={"X-ZMIE-API-KEY": "zmie-adm-key-0001"}
        )
        self.assertEqual(resp_adm.status_code, 200)

    def test_03_admin_audit_logs_requires_admin(self):
        """GET /v1/admin/audit-logs must fail closed without admin authentication."""
        resp_unauth = self.client.get("/v1/admin/audit-logs")
        self.assertEqual(resp_unauth.status_code, 401)

        resp_adm = self.client.get(
            "/v1/admin/audit-logs",
            headers={"X-ZMIE-API-KEY": "zmie-adm-key-0001"}
        )
        self.assertEqual(resp_adm.status_code, 200)

    def test_04_projects_list_scoped_to_tenant(self):
        """GET /v1/projects must require authentication and scope to tenant."""
        # Unauthenticated -> 401
        resp_unauth = self.client.get("/v1/projects")
        self.assertEqual(resp_unauth.status_code, 401)

        # AIIMS Delhi Researcher -> gets their own project
        resp_aiims = self.client.get(
            "/v1/projects",
            headers={"X-ZMIE-API-KEY": "zmie-res-key-9921"}
        )
        self.assertEqual(resp_aiims.status_code, 200)
        projects = resp_aiims.json()
        self.assertTrue(len(projects) >= 1)
        self.assertEqual(projects[0]["org_id"], "org-aiims-delhi")

        # Apollo Clinician -> cannot see AIIMS projects
        resp_apollo = self.client.get(
            "/v1/projects",
            headers={"X-ZMIE-API-KEY": "zmie-cli-key-4412"}
        )
        self.assertEqual(resp_apollo.status_code, 200)
        self.assertEqual(len(resp_apollo.json()), 0)

    def test_05_project_details_cross_tenant_denied(self):
        """GET /v1/projects/{id} must reject unauthenticated and cross-tenant callers."""
        # Unauthenticated -> 401
        resp_unauth = self.client.get("/v1/projects/PROJ-METABOLIC-01")
        self.assertEqual(resp_unauth.status_code, 401)

        # Cross-tenant (Apollo Hospitals trying to view AIIMS project) -> 403
        resp_cross = self.client.get(
            "/v1/projects/PROJ-METABOLIC-01",
            headers={"X-ZMIE-API-KEY": "zmie-cli-key-4412"}
        )
        self.assertEqual(resp_cross.status_code, 403)
        self.assertIn("cross-tenant", resp_cross.json()["detail"].lower())

        # Legitimate owner (AIIMS) -> 200
        resp_owner = self.client.get(
            "/v1/projects/PROJ-METABOLIC-01",
            headers={"X-ZMIE-API-KEY": "zmie-res-key-9921"}
        )
        self.assertEqual(resp_owner.status_code, 200)
        self.assertEqual(resp_owner.json()["project_id"], "PROJ-METABOLIC-01")

    def test_06_security_audit_requires_admin(self):
        """GET /v1/security/audit must require admin role."""
        resp_unauth = self.client.get("/v1/security/audit")
        self.assertEqual(resp_unauth.status_code, 401)

        resp_res = self.client.get(
            "/v1/security/audit",
            headers={"X-ZMIE-API-KEY": "zmie-res-key-9921"}
        )
        self.assertEqual(resp_res.status_code, 403)

        resp_adm = self.client.get(
            "/v1/security/audit",
            headers={"X-ZMIE-API-KEY": "zmie-adm-key-0001"}
        )
        self.assertEqual(resp_adm.status_code, 200)


if __name__ == "__main__":
    unittest.main()
