"""
ZMIE Production Readiness & Pre-Flight Certification Acceptance Test Suite
PROMPT 34 Certification — Independent Production Gate, 28 Domains, 9 Scopes
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.platform.gateway import APIGatewayEngine
from app.production_readiness.engine import ProductionReadinessEngine
from app.production_readiness.models import (
    AuditPillar,
    PillarStatus,
    AuditDomain,
    ProductionScope,
    ReadinessState,
)
from zmie import ZMIEClient


class TestPrompt34ProductionReadinessAcceptance(unittest.TestCase):
    def setUp(self):
        self.engine = ProductionReadinessEngine()
        raw_key, _ = APIGatewayEngine.create_api_key(
            tenant_id="tenant-readiness",
            owner="auditor@zmie.org",
            name="Readiness Audit Key",
            scopes=["knowledge:read", "rag:read", "safety:read", "search:read", "evidence:read"]
        )
        self.sdk_client = ZMIEClient(api_key=raw_key, app_instance=app)

    def test_01_preflight_audit_all_7_pillars_pass(self):
        """Preflight audit must achieve GO verdict across all 7 pillars with digital signature."""
        cert = self.engine.execute_preflight_audit()

        self.assertEqual(cert.verdict, "GO")
        self.assertTrue(cert.is_production_ready)
        self.assertEqual(cert.readiness_score, 1.0)
        self.assertEqual(len(cert.critical_blockers), 0)
        self.assertEqual(len(cert.digital_signature), 64)
        self.assertIn("cert-gxp-", cert.certificate_id)
        self.assertEqual(cert.release_candidate_id, "RC-ZMIE-2026.10-PROD-1")

    def test_02_pillar_evaluations_completeness(self):
        """All 7 production pillars must be present and verified."""
        cert = self.engine.execute_preflight_audit()
        pillar_names = {p.pillar for p in cert.evaluated_pillars}
        expected_pillars = {
            AuditPillar.INVARIANTS,
            AuditPillar.ARCHITECTURE,
            AuditPillar.CRYPTOGRAPHY,
            AuditPillar.TENANCY_ISOLATION,
            AuditPillar.RELIABILITY,
            AuditPillar.OBSERVABILITY,
            AuditPillar.COMPLIANCE_GXP
        }
        self.assertEqual(pillar_names, expected_pillars)

        for p in cert.evaluated_pillars:
            self.assertEqual(p.status, PillarStatus.PASS)
            self.assertEqual(p.score, 1.0)
            self.assertGreater(p.checks_passed, 0)
            self.assertEqual(p.checks_passed, p.checks_total)

    def test_03_certificate_retrieval(self):
        """Certificates must be stored and queryable by certificate_id."""
        cert = self.engine.execute_preflight_audit()
        fetched = self.engine.get_certificate(cert.certificate_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.certificate_id, cert.certificate_id)

        all_certs = self.engine.list_certificates()
        self.assertGreaterEqual(len(all_certs), 1)

    def test_04_28_domains_audit_matrix_completeness(self):
        """All 28 comprehensive production audit domains must be evaluated with evidence (Clause 260)."""
        cert = self.engine.execute_preflight_audit()
        self.assertEqual(len(cert.domain_matrix), 28)

        # Check all enum values present
        for domain in AuditDomain:
            self.assertIn(domain.value, cert.domain_matrix)
            domain_res = cert.domain_matrix[domain.value]
            self.assertIn(domain_res.status, ["GO", "CONDITIONAL_GO"])
            self.assertEqual(len(domain_res.blocking_issues), 0)
            self.assertTrue(len(domain_res.evidence) > 0)
            self.assertIn(domain_res.residual_risk, ["LOW", "ACCEPTABLE_WITH_CONTROLS"])

        # Check clinical domain is CONDITIONAL_GO (Human-in-the-loop review mandatory)
        clinical_res = cert.domain_matrix[AuditDomain.CLINICAL.value]
        self.assertEqual(clinical_res.status, "CONDITIONAL_GO")
        self.assertIn("Human-in-the-Loop", clinical_res.evidence)

    def test_05_9_production_scopes_profiles(self):
        """All 9 targeted production readiness scope profiles must be defined (Clause 8)."""
        cert = self.engine.execute_preflight_audit()
        self.assertEqual(len(cert.scope_profiles), 9)

        for scope in ProductionScope:
            self.assertIn(scope.value, cert.scope_profiles)

        # Verify specific scope constraints
        search_scope = cert.scope_profiles[ProductionScope.PUBLIC_SEARCH.value]
        self.assertEqual(search_scope.state, ReadinessState.PRODUCTION_READY)
        self.assertEqual(search_scope.decision, "GO")

        clinical_scope = cert.scope_profiles[ProductionScope.CLINICAL_DECISION_SUPPORT.value]
        self.assertEqual(clinical_scope.state, ReadinessState.CONDITIONAL)
        self.assertEqual(clinical_scope.decision, "CONDITIONAL_GO")
        self.assertTrue(any("Human-in-the-Loop" in c for c in clinical_scope.conditions))

        federated_scope = cert.scope_profiles[ProductionScope.FEDERATED_INTELLIGENCE.value]
        self.assertEqual(federated_scope.state, ReadinessState.READY_FOR_PILOT)

    def test_06_release_manifest_integrity(self):
        """Release candidate manifest (release.json) must be hash-verified with exact component versions."""
        manifest = self.engine.generate_release_manifest()
        self.assertEqual(manifest["release_candidate_id"], "RC-ZMIE-2026.10-PROD-1")
        self.assertEqual(manifest["code_version"], "v34.0.0")
        self.assertEqual(manifest["invariants_enforced"], 10)
        self.assertEqual(manifest["audit_domains_count"], 28)
        self.assertEqual(manifest["scope_profiles_count"], 9)
        self.assertEqual(manifest["hallucination_rate"], 0.0)
        self.assertEqual(manifest["calculation_error_rate"], 0.0)
        self.assertEqual(manifest["reproducibility_divergence_rate"], 0.0)
        self.assertEqual(len(manifest["manifest_digest"]), 64)

    def test_07_risk_register_and_residual_risks(self):
        """Production risk register must track scientific, security, operational, and clinical risks."""
        risks = self.engine.get_risk_register()
        self.assertGreaterEqual(len(risks), 4)
        categories = {r.category for r in risks}
        self.assertIn("SCIENTIFIC", categories)
        self.assertIn("SECURITY", categories)
        self.assertIn("OPERATIONAL", categories)
        self.assertIn("CLINICAL", categories)

        for r in risks:
            self.assertIn(r.residual_risk, ["LOW", "ACCEPTABLE_WITH_CONTROLS"])
            self.assertTrue(len(r.controls_in_place) > 0)
            self.assertTrue(len(r.owner) > 0)

    def test_08_blocker_registry_verification(self):
        """Blocker registry must verify all critical pre-launch blockers are verified resolved."""
        blockers = self.engine.get_blocker_registry()
        self.assertGreaterEqual(len(blockers), 3)
        for b in blockers:
            self.assertEqual(b.status, "VERIFIED")
            self.assertTrue(len(b.verification_evidence) > 0)

    def test_09_stop_conditions_and_rollback_plan(self):
        """Stop conditions and rollback procedure must be explicitly defined."""
        stop_conditions = self.engine.get_stop_conditions()
        self.assertGreaterEqual(len(stop_conditions), 5)
        self.assertTrue(any("fabricated citation" in c.lower() for c in stop_conditions))
        self.assertTrue(any("cross-tenant" in c.lower() for c in stop_conditions))

        rollback = self.engine.get_rollback_plan()
        self.assertEqual(rollback["estimated_rto_seconds"], 180)
        self.assertIn("Circuit Breaker", rollback["strategy"])

    def test_10_fastapi_and_sdk_integration(self):
        """FastAPI endpoints and SDK client methods must provide end-to-end access to audit results."""
        # Preflight audit via SDK
        cert = self.sdk_client.production_readiness.preflight_audit()
        self.assertEqual(cert["verdict"], "GO")
        self.assertTrue(cert["is_production_ready"])
        self.assertEqual(len(cert["digital_signature"]), 64)

        # Domains matrix via SDK
        domains = self.sdk_client.production_readiness.get_domains()
        self.assertEqual(len(domains), 28)
        self.assertIn("ARCHITECTURE", domains)
        self.assertIn("SCIENTIFIC_VALIDATION", domains)

        # Scopes profiles via SDK
        scopes = self.sdk_client.production_readiness.get_scopes()
        self.assertEqual(len(scopes), 9)
        self.assertIn("PUBLIC_SEARCH", scopes)

        # Release manifest via SDK
        manifest = self.sdk_client.production_readiness.get_manifest()
        self.assertEqual(manifest["release_candidate_id"], "RC-ZMIE-2026.10-PROD-1")
        self.assertEqual(len(manifest["manifest_digest"]), 64)

        # Risks and blockers via SDK
        risks = self.sdk_client.production_readiness.get_risks()
        self.assertGreaterEqual(len(risks), 4)

        blockers = self.sdk_client.production_readiness.get_blockers()
        self.assertGreaterEqual(len(blockers), 3)


if __name__ == "__main__":
    unittest.main()
