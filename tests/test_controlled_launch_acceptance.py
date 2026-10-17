"""
ZMIE Controlled Launch & Continuous Monitoring Acceptance Test Suite
PROMPT 35 Certification — Progressive Rings, Tripwires, and Autonomous Daemons
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.platform.gateway import APIGatewayEngine
from app.controlled_launch.engine import ControlledLaunchEngine
from app.controlled_launch.models import (
    DeploymentRing,
    RolloutStatus,
    TripwireCause,
    IncidentSeverity,
    ProductionIncidentRecord,
)
from zmie import ZMIEClient


class TestPrompt35ControlledLaunchAcceptance(unittest.TestCase):
    def setUp(self):
        self.engine = ControlledLaunchEngine(target_version="v1.0.0-production")
        raw_key, _ = APIGatewayEngine.create_api_key(
            tenant_id="tenant-launch",
            owner="launch-lead@zmie.org",
            name="Launch Control Key",
            scopes=["knowledge:read", "rag:read", "safety:read", "search:read", "evidence:read"]
        )
        self.sdk_client = ZMIEClient(api_key=raw_key, app_instance=app)

    def test_01_launch_plan_initialization_ring_0(self):
        """Initial launch plan must start at Ring 0 Internal with circuit breaker armed."""
        plan = self.engine.get_launch_plan()
        self.assertEqual(plan.target_version, "v1.0.0-production")
        self.assertEqual(plan.current_ring, DeploymentRing.RING_0_INTERNAL)
        self.assertTrue(plan.circuit_breaker_armed)

        r0 = plan.rings[DeploymentRing.RING_0_INTERNAL.value]
        self.assertEqual(r0.status, RolloutStatus.ACTIVE)
        self.assertEqual(r0.traffic_percentage, 100.0)
        self.assertEqual(r0.canary_metrics.invariant_violations, 0)
        self.assertEqual(r0.canary_metrics.hallucination_rate, 0.0)

    def test_02_ring_progression_promotion(self):
        """Rollout must successfully advance through progressive delivery rings (0 -> 1 -> 2 -> 3)."""
        # Promote to Ring 1 (Pilot Academic)
        plan1 = self.engine.promote_to_next_ring()
        self.assertEqual(plan1.current_ring, DeploymentRing.RING_1_PILOT_ACADEMIC)
        self.assertEqual(plan1.rings[DeploymentRing.RING_0_INTERNAL.value].status, RolloutStatus.COMPLETED)
        self.assertEqual(plan1.rings[DeploymentRing.RING_1_PILOT_ACADEMIC.value].status, RolloutStatus.ACTIVE)

        # Promote to Ring 2 (Clinical Network)
        plan2 = self.engine.promote_to_next_ring()
        self.assertEqual(plan2.current_ring, DeploymentRing.RING_2_CLINICAL_NETWORK)
        self.assertEqual(plan2.rings[DeploymentRing.RING_2_CLINICAL_NETWORK.value].status, RolloutStatus.ACTIVE)

        # Promote to Ring 3 (Global Production)
        plan3 = self.engine.promote_to_next_ring()
        self.assertEqual(plan3.current_ring, DeploymentRing.RING_3_GLOBAL_PRODUCTION)
        self.assertEqual(plan3.rings[DeploymentRing.RING_3_GLOBAL_PRODUCTION.value].status, RolloutStatus.ACTIVE)

    def test_03_circuit_breaker_rollback(self):
        """Circuit breaker trip must instantly rollback deployment to Ring 0."""
        # Advance to Ring 1
        self.engine.promote_to_next_ring()
        self.assertEqual(self.engine.get_launch_plan().current_ring, DeploymentRing.RING_1_PILOT_ACADEMIC)

        # Trigger circuit breaker rollback
        rolled_back_plan = self.engine.trigger_circuit_breaker_rollback("Simulated telemetry spike / canary trip")
        self.assertEqual(rolled_back_plan.current_ring, DeploymentRing.RING_0_INTERNAL)
        self.assertEqual(rolled_back_plan.rings[DeploymentRing.RING_1_PILOT_ACADEMIC.value].status, RolloutStatus.ROLLED_BACK)
        self.assertEqual(rolled_back_plan.rings[DeploymentRing.RING_0_INTERNAL.value].status, RolloutStatus.ACTIVE)

    def test_04_continuous_monitoring_telemetry_sampling(self):
        """Autonomous continuous monitoring telemetry must sample live health and invariant verification."""
        telemetry = self.engine.sample_continuous_monitoring_telemetry()
        self.assertEqual(telemetry.system_health_verdict, "OPERATIONAL")
        self.assertEqual(telemetry.registry_sync_status, "HEALTHY")
        self.assertEqual(telemetry.retraction_radar_status, "ACTIVE")
        self.assertEqual(telemetry.active_invariants_count, 10)
        self.assertTrue(telemetry.audit_chain_hmac_verified)
        self.assertGreater(telemetry.living_graph_nodes_monitored, 1000)
        self.assertEqual(telemetry.tenant_isolation_status, "ENFORCED")
        self.assertGreaterEqual(len(telemetry.active_daemons), 5)

    def test_05_canary_quality_gates_verification(self):
        """Canary quality gates must enforce latency SLOs, zero invariant violations, and full error budget."""
        slos = self.engine.get_slos()
        self.assertEqual(slos["current_ring"], "RING_0_INTERNAL")
        self.assertTrue(slos["circuit_breaker_armed"])
        self.assertEqual(slos["error_budget_percent"], 100.0)
        targets = slos["slo_targets"]
        self.assertIn("max_p99_latency_ms", targets)
        self.assertIn("max_hallucination_rate", targets)
        self.assertEqual(targets["max_hallucination_rate"], 0.0)

    def test_06_automated_tripwire_circuit_breaker_instant_rollback(self):
        """Simulating a citation fabrication tripwire must instantly trigger zero-second rollback to Ring 0."""
        # Advance to Ring 2
        self.engine.promote_to_next_ring()
        self.engine.promote_to_next_ring()
        self.assertEqual(self.engine.get_launch_plan().current_ring, DeploymentRing.RING_2_CLINICAL_NETWORK)

        # Trigger simulated citation fabrication tripwire
        plan = self.engine.simulate_tripwire(
            cause=TripwireCause.CITATION_FABRICATION_DETECTED,
            details={"offending_doi": "10.9999/fabricated.doi", "source": "unauthorized-inference"}
        )

        self.assertEqual(plan.current_ring, DeploymentRing.RING_0_INTERNAL)
        self.assertEqual(plan.rings[DeploymentRing.RING_2_CLINICAL_NETWORK.value].status, RolloutStatus.ROLLED_BACK)
        self.assertEqual(plan.rings[DeploymentRing.RING_0_INTERNAL.value].status, RolloutStatus.ACTIVE)
        self.assertGreaterEqual(len(plan.recent_tripwires), 1)
        last_event = plan.recent_tripwires[-1]
        self.assertEqual(last_event.cause, TripwireCause.CITATION_FABRICATION_DETECTED)
        self.assertEqual(last_event.rollback_target, DeploymentRing.RING_0_INTERNAL)

    def test_07_promotion_blocked_on_unhealthy_canary(self):
        """Promotion to next ring MUST be blocked if canary metrics show any invariant violation."""
        # Inject synthetic violation into current Ring 0
        r0 = self.engine._plan.rings[DeploymentRing.RING_0_INTERNAL.value]
        r0.canary_metrics.invariant_violations = 1

        with self.assertRaises(RuntimeError) as ctx:
            self.engine.promote_to_next_ring()
        self.assertIn("Canary violations detected", str(ctx.exception))

    def test_08_autonomous_monitoring_daemons_operational(self):
        """All 5 autonomous surveillance daemons must be active and reporting heartbeats."""
        daemons = self.engine.get_monitoring_daemons()
        self.assertEqual(len(daemons), 5)
        names = {d.daemon_name for d in daemons}
        expected_names = {
            "CanonicalRegistrySyncDaemon",
            "RetractionRadarWatcher",
            "EpistemicDriftDetector",
            "HMACChainIntegrityScanner",
            "TenantIsolationGuard"
        }
        self.assertEqual(names, expected_names)

        for d in daemons:
            self.assertEqual(d.status, "ACTIVE")
            self.assertEqual(d.anomalies_detected, 0)
            self.assertGreater(d.items_scanned_last_hour, 0)

    def test_09_slos_and_error_budget_tracking(self):
        """SLO tracking endpoint must verify error budget availability across rings."""
        slos = self.engine.get_slos()
        self.assertEqual(slos["observed_canary_metrics"]["hallucination_rate"], 0.0)
        self.assertEqual(slos["observed_canary_metrics"]["tenant_boundary_breaches"], 0)
        self.assertEqual(slos["observed_canary_metrics"]["calculation_errors"], 0)

    def test_10_fastapi_and_sdk_integration(self):
        """FastAPI endpoints and SDK client methods must provide end-to-end access to launch controls."""
        # Test get_plan via SDK
        plan = self.sdk_client.controlled_launch.get_plan()
        self.assertEqual(plan["current_ring"], "RING_0_INTERNAL")
        self.assertTrue(plan["circuit_breaker_armed"])

        # Test promote via SDK
        promoted = self.sdk_client.controlled_launch.promote()
        self.assertEqual(promoted["current_ring"], "RING_1_PILOT_ACADEMIC")

        # Test simulate_tripwire via SDK
        rolled_back = self.sdk_client.controlled_launch.simulate_tripwire("CROSS_TENANT_LEAKAGE")
        self.assertEqual(rolled_back["current_ring"], "RING_0_INTERNAL")

        # Test telemetry via SDK
        telemetry = self.sdk_client.controlled_launch.get_telemetry()
        self.assertEqual(telemetry["system_health_verdict"], "OPERATIONAL")
        self.assertEqual(len(telemetry["active_daemons"]), 5)

        # Test daemons via SDK
        daemons = self.sdk_client.controlled_launch.get_daemons()
        self.assertEqual(len(daemons), 5)

        # Test slos via SDK
        slos = self.sdk_client.controlled_launch.get_slos()
        self.assertIn("slo_targets", slos)

    def test_11_generate_launch_report_and_cryptographic_signature(self):
        """Clause 317: Controlled Production Launch Report generation and signature verification."""
        # Test directly on engine
        report = self.engine.generate_launch_report()
        self.assertTrue(report.report_id.startswith("launch-rep-"))
        self.assertEqual(report.release_id, "REL-ZMIE-2026.10-GA-1")
        self.assertEqual(report.final_decision, "GO_LIVE_APPROVED")
        self.assertIn("PublicMedicalSearch", report.features_enabled)
        self.assertIn("AutonomousDiagnosticPrescription", report.features_blocked)
        self.assertIn("ClinicalDecisionSupport", report.features_restricted)
        self.assertTrue(len(report.digital_signature) > 10)

        # Test via SDK client
        sdk_report = self.sdk_client.controlled_launch.generate_launch_report()
        self.assertTrue(sdk_report["report_id"].startswith("launch-rep-"))
        self.assertEqual(sdk_report["final_decision"], "GO_LIVE_APPROVED")
        self.assertEqual(sdk_report["security_status"], "HARDENED")
        self.assertEqual(sdk_report["trust_status"], "FIREWALL_ACTIVE")
        self.assertIn("AutonomousDiagnosticPrescription", sdk_report["features_blocked"])
        self.assertIn("PublicMedicalSearch", sdk_report["features_enabled"])

    def test_12_issue_scope_certificate_and_cryptographic_signature(self):
        """Clause 297: Production Scope Certificate issuance and cryptographic verification."""
        # Test directly on engine
        cert = self.engine.issue_scope_certificate()
        self.assertTrue(cert.certificate_id.startswith("scope-cert-"))
        self.assertEqual(cert.release_id, "REL-ZMIE-2026.10-GA-1")
        self.assertIn("PublicMedicalSearch", cert.validated_scopes)
        self.assertIn("ClinicalDecisionSupport", cert.restricted_scopes)
        self.assertIn("Chief Launch Officer & Release Governance Authority", cert.authority)
        self.assertTrue(any("Autonomous Diagnostic Prescription strictly prohibited" in lim for lim in cert.known_limitations))
        self.assertTrue(len(cert.digital_signature) > 10)

        # Test via SDK client
        sdk_cert = self.sdk_client.controlled_launch.issue_scope_certificate()
        self.assertTrue(sdk_cert["certificate_id"].startswith("scope-cert-"))
        self.assertIn("PublicMedicalSearch", sdk_cert["validated_scopes"])
        self.assertTrue(len(sdk_cert["digital_signature"]) > 10)

    def test_13_production_incident_logging_and_p0_automatic_circuit_breaker(self):
        """Clauses 137-148: P0 incident triggers immediate zero-second circuit breaker rollback to Ring 0."""
        # Advance to Ring 1 via SDK
        self.sdk_client.controlled_launch.promote()
        plan_now = self.sdk_client.controlled_launch.get_plan()
        self.assertEqual(plan_now["current_ring"], "RING_1_PILOT_ACADEMIC")

        # Log a P2 minor incident
        p2_record = {
            "incident_id": "inc-test-p2-001",
            "severity": "P2",
            "title": "Minor latency fluctuation in PubMed sync",
            "description": "Crossref sync took 45ms instead of target 20ms",
            "affected_scope": "SOURCE_REGISTRY",
            "status": "OPEN",
            "action_taken": "Traffic maintained, alert routed to on-call SRE"
        }
        plan_after_p2 = self.sdk_client.controlled_launch.log_incident(p2_record)
        self.assertEqual(plan_after_p2["current_ring"], "RING_1_PILOT_ACADEMIC")
        self.assertGreaterEqual(len(plan_after_p2["incident_log"]), 1)

        # Log a P0 critical incident (e.g. Invariant Violation / Cross-Tenant Leakage attempt)
        p0_record = {
            "incident_id": "inc-test-p0-001",
            "severity": "P0",
            "title": "Invariant Safety Gate Breach Attempt",
            "description": "Synthetic injection attempted autonomous diagnostic prescription execution",
            "affected_scope": "CLINICAL_DECISION_SUPPORT",
            "status": "OPEN",
            "action_taken": "Automated zero-second circuit breaker trip expected"
        }
        plan_after_p0 = self.sdk_client.controlled_launch.log_incident(p0_record)
        # Must have performed instant rollback to Ring 0!
        self.assertEqual(plan_after_p0["current_ring"], "RING_0_INTERNAL")
        self.assertGreaterEqual(len(plan_after_p0["recent_tripwires"]), 1)


if __name__ == "__main__":
    unittest.main()

