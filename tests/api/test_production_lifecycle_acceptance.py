"""
ZMIE Master Production Lifecycle Loop Acceptance Tests
Production → Monitor → Revalidate → Benchmark → Audit → Improve → Release
"""

import unittest
from app.main import app
from app.platform.gateway import APIGatewayEngine
from app.lifecycle.master_loop import ProductionLifecycleEngine
from zmie import ZMIEClient


class TestProductionLifecycleAcceptance(unittest.TestCase):
    def setUp(self):
        self.engine = ProductionLifecycleEngine()
        raw_key, _ = APIGatewayEngine.create_api_key(
            tenant_id="tenant-lifecycle-master",
            owner="lifecycle-architect@zmie.org",
            name="Master Lifecycle Key",
            scopes=["knowledge:read", "rag:read", "safety:read", "search:read", "evidence:read"]
        )
        self.sdk_client = ZMIEClient(api_key=raw_key, app_instance=app)

    def test_01_step_by_step_lifecycle_execution(self):
        """Each of the 7 stages must execute sequentially with verifiable evidence."""
        # Stage 1: Production
        s1 = self.engine.step_1_production(version="v1.0.0")
        self.assertEqual(s1.stage_name, "1. PRODUCTION")
        self.assertEqual(s1.status, "COMPLETED")
        self.assertTrue(s1.evidence["circuit_breaker_armed"])
        self.assertEqual(s1.evidence["hallucination_rate"], 0.0)

        # Stage 2: Monitor
        s2 = self.engine.step_2_monitor()
        self.assertEqual(s2.stage_name, "2. MONITOR")
        self.assertEqual(s2.status, "COMPLETED")
        self.assertEqual(s2.evidence["system_health"], "OPERATIONAL")
        self.assertIn("surveillance_trigger", s2.evidence)

        # Stage 3: Revalidate
        trigger = s2.evidence["surveillance_trigger"]
        s3 = self.engine.step_3_revalidate(trigger_event=trigger)
        self.assertEqual(s3.stage_name, "3. REVALIDATE")
        self.assertEqual(s3.status, "COMPLETED")
        self.assertTrue(s3.evidence["quarantine_active"])

        # Stage 4: Benchmark
        s4 = self.engine.step_4_benchmark()
        self.assertEqual(s4.stage_name, "4. BENCHMARK")
        self.assertEqual(s4.status, "COMPLETED")
        self.assertEqual(s4.evidence["overall_decision"], "GO")
        self.assertEqual(s4.evidence["hallucination_rate"], 0.0)

        # Stage 5: Audit
        s5 = self.engine.step_5_audit()
        self.assertEqual(s5.stage_name, "5. AUDIT")
        self.assertEqual(s5.status, "COMPLETED")
        self.assertEqual(s5.evidence["verdict"], "GO")
        self.assertEqual(s5.evidence["active_blockers"], 0)


        # Stage 6: Improve
        s6 = self.engine.step_6_improve(parent_version="v1.0.0")
        self.assertEqual(s6.stage_name, "6. IMPROVE")
        self.assertEqual(s6.status, "COMPLETED")
        self.assertIn("child_snapshot_id", s6.evidence)
        self.assertEqual(s6.evidence["new_version"], "v1.1.0")

        # Stage 7: Release
        s7 = self.engine.step_7_release(new_version=s6.evidence["new_version"])
        self.assertEqual(s7.stage_name, "7. RELEASE")
        self.assertEqual(s7.status, "COMPLETED")
        self.assertEqual(s7.evidence["released_version"], "v1.1.0")
        self.assertEqual(s7.evidence["current_ring"], "RING_3_GLOBAL_PRODUCTION")
        self.assertEqual(s7.evidence["final_decision"], "GO_LIVE_APPROVED")

    def test_02_full_atomic_lifecycle_execution(self):
        """Atomic master lifecycle loop must transition from v1.0.0 to v1.1.0 with HMAC signature."""
        report = self.engine.execute_full_lifecycle(
            initial_version="v1.0.0",
            target_version="v1.1.0"
        )
        self.assertEqual(report.overall_status, "COMPLETED")
        self.assertEqual(report.initial_version, "v1.0.0")
        self.assertEqual(report.released_version, "v1.1.0")
        self.assertEqual(len(report.stages), 7)
        self.assertTrue(len(report.digital_signature) > 10)

        expected_stages = ["PRODUCTION", "MONITOR", "REVALIDATE", "BENCHMARK", "AUDIT", "IMPROVE", "RELEASE"]
        for st in expected_stages:
            self.assertIn(st, report.stages)
            self.assertEqual(report.stages[st].status, "COMPLETED")

    def test_03_fastapi_and_sdk_lifecycle_integration(self):
        """SDK client and FastAPI endpoints must provide full execution of the master lifecycle."""
        # Test stages schema
        stages = self.sdk_client.lifecycle.get_stages()
        self.assertEqual(len(stages["sequence"]), 7)
        self.assertEqual(stages["sequence"][0], "PRODUCTION")
        self.assertEqual(stages["sequence"][-1], "RELEASE")

        # Test execute via SDK
        report = self.sdk_client.lifecycle.run(
            initial_version="v1.0.0",
            target_version="v1.1.0"
        )
        self.assertEqual(report["overall_status"], "COMPLETED")
        self.assertEqual(report["released_version"], "v1.1.0")
        self.assertIn("RELEASE", report["stages"])
        self.assertEqual(report["stages"]["RELEASE"]["status"], "COMPLETED")


if __name__ == "__main__":
    unittest.main()
