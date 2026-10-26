"""ZMIE Scientific Closed-Loop Discovery & Autonomous Knowledge Learning Acceptance Tests.

Verifies:
1. Complete 5-stage closed loop:
   SCIENTIFIC KNOWLEDGE -> HYPOTHESIS -> EXPERIMENT -> EVIDENCE -> KNOWLEDGE LEARNING SYSTEM
2. Shannon entropy computation of hypothesis space (before vs after evidence)
3. Causal DAG edge re-weighting upon empirical validation
4. Identification of retired assumptions and newly opened research frontiers
5. FastAPI REST endpoints for the closed-loop system
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.models.simulation_hypothesis import EpistemicStatus
from app.research.closed_loop_learning import ScientificClosedLoopLearningEngine


class TestClosedLoopLearningAcceptance(unittest.TestCase):
    """Rigorous acceptance tests for the ZMIE Scientific Closed-Loop Learning System."""

    def setUp(self):
        self.engine = ScientificClosedLoopLearningEngine()
        self.client = TestClient(app)

    def test_01_capture_knowledge_snapshot_and_entropy(self):
        """Verifies capturing an immutable knowledge state snapshot with Shannon entropy."""
        snap = self.engine.capture_knowledge_snapshot("SGLT2_HF", version_suffix="t0")
        self.assertIsNotNone(snap)
        self.assertIn("SNAP-", snap.snapshot_id)
        self.assertEqual(snap.topic, "SGLT2_HF")
        self.assertGreater(snap.active_hypotheses_count, 0)
        self.assertGreater(snap.shannon_entropy, 0.0)
        self.assertIn("ALIGNED", snap.regulatory_guideline_alignment)

    def test_02_execute_full_closed_loop_cycle(self):
        """Verifies execution of the entire 5-stage closed-loop discovery and learning cycle."""
        execution = self.engine.execute_closed_loop_cycle(
            topic="SGLT2_CARDIOPROTECTION",
            target_hypothesis_id="HYP-SGLT2-NHE1",
            competing_hypothesis_id="HYP-SGLT2-HEMO",
            simulated_dose_mg=25.0,
            observed_delta_pct=-28.5,
            observed_p_value=0.0015,
        )

        self.assertIsNotNone(execution)
        self.assertEqual(len(execution.stage_progression), 5)

        # Check Stage 1: Scientific Knowledge
        self.assertEqual(execution.initial_knowledge_state.topic, "SGLT2_CARDIOPROTECTION")

        # Check Stage 2: Hypothesis
        self.assertEqual(len(execution.formulated_hypotheses), 2)
        self.assertIsNotNone(execution.competing_divergence_summary)

        # Check Stage 3: Experiment & Simulation
        self.assertIsNotNone(execution.simulation_run)
        self.assertEqual(execution.simulation_run.epistemic_status, EpistemicStatus.MODEL_PREDICTED)
        self.assertIsNotNone(execution.executed_proposal)
        self.assertTrue(execution.executed_proposal.existing_data_checked)
        self.assertTrue(execution.executed_proposal.human_approval_required)

        # Check Stage 4: Evidence
        self.assertEqual(execution.ingested_evidence.epistemic_status, EpistemicStatus.OBSERVED)
        self.assertEqual(execution.ingested_evidence.effect_on_hypothesis, "SUPPORTS")

        # Check Stage 5: Knowledge Learning
        delta = execution.epistemic_delta
        self.assertGreater(delta.posterior_credence, delta.prior_credence)
        self.assertGreater(len(delta.causal_edge_weight_updates), 0)
        self.assertGreater(len(delta.retired_assumptions), 0)
        self.assertGreater(len(delta.new_questions_opened), 0)

        # Master Verdict
        self.assertIn("CLOSED-LOOP CYCLE COMPLETED", execution.master_epistemic_verdict)

    def test_03_fastapi_closed_loop_endpoints(self):
        """Verifies FastAPI REST endpoints for the closed-loop learning system."""
        # GET /v1/closed-loop/snapshot
        resp_snap = self.client.get("/v1/closed-loop/snapshot?topic=CARDIOMETABOLIC")
        self.assertEqual(resp_snap.status_code, 200)
        snap_data = resp_snap.json()
        self.assertIn("snapshot_id", snap_data)
        self.assertIn("shannon_entropy", snap_data)

        # POST /v1/closed-loop/execute
        resp_exec = self.client.post(
            "/v1/closed-loop/execute",
            json={
                "topic": "SGLT2_HF",
                "target_hypothesis_id": "HYP-SGLT2-NHE1",
                "competing_hypothesis_id": "HYP-SGLT2-HEMO",
                "simulated_dose_mg": 25.0,
                "observed_delta_pct": -29.0,
                "observed_p_value": 0.001,
            },
        )
        self.assertEqual(resp_exec.status_code, 200)
        exec_data = resp_exec.json()
        self.assertIn("cycle_id", exec_data)
        self.assertEqual(len(exec_data["stage_progression"]), 5)
        self.assertIn("epistemic_delta", exec_data)

        cycle_id = exec_data["cycle_id"]

        # GET /v1/closed-loop/executions
        resp_list = self.client.get("/v1/closed-loop/executions")
        self.assertEqual(resp_list.status_code, 200)
        list_data = resp_list.json()
        self.assertIsInstance(list_data, list)
        self.assertGreaterEqual(len(list_data), 1)

        # GET /v1/closed-loop/executions/{id}
        resp_single = self.client.get(f"/v1/closed-loop/executions/{cycle_id}")
        self.assertEqual(resp_single.status_code, 200)
        single_data = resp_single.json()
        self.assertEqual(single_data["cycle_id"], cycle_id)


if __name__ == "__main__":
    unittest.main()
