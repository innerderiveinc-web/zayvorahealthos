"""ZMIE Scientific Data Fabric & Computational Research Engine Acceptance Tests.

Verifies:
1. Golden End-to-End Research Pipeline (Clause 219):
   Dataset Ingestion -> Quality Profiling -> Cryptographic Snapshot ->
   Analysis Plan -> Containerized Execution -> Effect Estimate (COMPUTED state) ->
   Data Lineage Graph -> Reproduce Run & Computational Certificate ->
   Candidate Claim Promotion -> Knowledge Release Gate
2. Strict Scientific State Enforcement (COMPUTED != OBSERVED)
3. Data Leakage Detection & Study Design Safeguards
4. Computation Diffing (Detects changes in data, code, or parameters)
5. Intellectual Property & License Protection
6. FastAPI REST Endpoints
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.models.scientific_compute import (
    AnalysisPlan,
    DataField,
    Dataset,
    JobStatus,
    PrivacyClassification,
    ScientificState,
)
from app.scientific_compute.engine import ScientificDataFabricEngine


class TestScientificComputeAcceptance(unittest.TestCase):
    """Rigorous acceptance tests matching Prompt 21 requirements."""

    def setUp(self):
        self.engine = ScientificDataFabricEngine()
        self.client = TestClient(app)

    def test_01_golden_end_to_end_computational_research_pipeline(self):
        """Golden End-to-End Test (Clause 219): Full traceable trajectory from raw data to knowledge release."""
        # 1. Dataset Ingestion & Quality Profiling
        fields = [
            DataField(field_name="patient_id", data_type="string", semantic_type="Identifier"),
            DataField(field_name="sglt2_treatment", data_type="categorical", semantic_type="Exposure"),
            DataField(field_name="cardiac_death", data_type="numeric", semantic_type="Outcome"),
            DataField(field_name="time_to_event", data_type="numeric", semantic_type="FollowupTime", unit="days"),
            DataField(field_name="baseline_egfr", data_type="numeric", semantic_type="Confounder", unit="mL/min"),
        ]
        raw_ds = Dataset(
            dataset_id="DS-TEST-HF-01",
            name="Test Heart Failure Trial Cohort",
            description="Double-blind randomized prospective trial cohort",
            publisher_or_institution="ZMIE Core Research Facility",
            domain="Clinical Trial",
            privacy_class=PrivacyClassification.INTERNAL,
            fields=fields,
            records_count=2000,
            created_at=self.engine._now(),
            updated_at=self.engine._now(),
        )
        ds, dqr = self.engine.ingest_dataset(raw_ds)
        self.assertIsNotNone(ds)
        self.assertGreaterEqual(dqr.completeness_score, 0.95)
        self.assertEqual(dqr.fitness_for_purpose, "HIGH")

        # 2. Immutable Cryptographic Snapshot Pinning
        snapshot = self.engine.create_snapshot(ds.dataset_id, version_tag="v1.0")
        self.assertIsNotNone(snapshot.content_sha256)
        self.assertIsNotNone(snapshot.fields_schema_hash)

        # 3. Preregistered Analysis Plan & Leakage Checks
        plan = AnalysisPlan(
            plan_id="PLAN-TEST-HF-01",
            research_question="Does SGLT2i reduce cardiac death in HF?",
            study_design="Randomized Controlled Trial",
            target_population="NYHA II-IV Heart Failure patients",
            exposure_variable="sglt2_treatment",
            comparator_variable="standard_of_care",
            outcome_variable="cardiac_death",
            covariates=["baseline_egfr"],
            statistical_method="Cox Proportional Hazards Regression",
            created_at=self.engine._now(),
        )
        registered_plan = self.engine.register_analysis_plan(plan)
        self.assertTrue(registered_plan.data_leakage_checks_passed)

        # 4. Computational Workflow Execution (Strictly COMPUTED state)
        job = self.engine.execute_analysis_workflow(
            plan_id=registered_plan.plan_id,
            snapshot_id=snapshot.snapshot_id,
        )
        self.assertEqual(job.status, JobStatus.COMPLETED)
        self.assertGreater(len(job.results), 0)

        # Strict Scientific State check: COMPUTED (never OBSERVED)
        art = job.results[0]
        self.assertEqual(art.scientific_state, ScientificState.COMPUTED)
        self.assertIsNotNone(art.effect_estimate)
        self.assertEqual(art.effect_estimate.scientific_state, ScientificState.COMPUTED)
        self.assertEqual(art.effect_estimate.measure_type, "HAZARD_RATIO")
        self.assertLess(art.effect_estimate.point_estimate, 1.0)
        self.assertLess(art.effect_estimate.p_value, 0.05)

        # 5. End-to-End Lineage Graph Tracing
        lineage = self.engine.trace_data_lineage(job.job_id)
        self.assertIsNotNone(lineage)
        self.assertGreaterEqual(len(lineage.nodes), 6)
        self.assertEqual(lineage.root_source, ds.dataset_id)
        self.assertEqual(lineage.terminal_claim, art.effect_estimate.estimate_id)

        # 6. Reproducibility Engine & Computational Certificate
        reproduced_job, cert = self.engine.reproduce_run(job.job_id)
        self.assertEqual(reproduced_job.status, JobStatus.COMPLETED)
        self.assertEqual(cert.reproducibility_verdict, "FULLY_REPRODUCIBLE")
        self.assertLess(cert.relative_divergence, 1e-6)

        # 7. Candidate Claim Generation & Human Governance Promotion
        candidate_claim = self.engine.generate_candidate_claim(art.artifact_id)
        self.assertEqual(candidate_claim.human_review_status, "PENDING_REVIEW")
        self.assertFalse(candidate_claim.promoted_to_evidence_graph)

        promoted_claim = self.engine.review_and_promote_claim(
            claim_id=candidate_claim.claim_id,
            reviewer_name="Dr. E. Vance, Principal Investigator",
            approve=True,
        )
        self.assertEqual(promoted_claim.human_review_status, "APPROVED")
        self.assertTrue(promoted_claim.promoted_to_evidence_graph)
        self.assertEqual(promoted_claim.scientific_state, ScientificState.VALIDATED)

    def test_02_data_leakage_detection(self):
        """Verifies engine detects and blocks analysis plans containing post-outcome / future variables."""
        leaky_plan = AnalysisPlan(
            plan_id="PLAN-LEAKY-01",
            research_question="Leaky analysis test",
            study_design="Cohort",
            target_population="Adults",
            exposure_variable="tx",
            comparator_variable="ctrl",
            outcome_variable="event",
            covariates=["baseline_age", "post_outcome_cardiac_arrest_marker"],  # Data Leakage!
            statistical_method="Logistic Regression",
            created_at=self.engine._now(),
        )
        reg = self.engine.register_analysis_plan(leaky_plan)
        self.assertFalse(reg.data_leakage_checks_passed)

        # Execution should be blocked
        snap = self.engine._snapshots["SNAP-SGLT2-HF-v1.0"]
        with self.assertRaises(ValueError):
            self.engine.execute_analysis_workflow(reg.plan_id, snap.snapshot_id)

    def test_03_computation_diffing(self):
        """Verifies computation diffing compares two runs and pinpoints parameter/data changes."""
        snap = self.engine._snapshots["SNAP-SGLT2-HF-v1.0"]
        plan = self.engine._plans["PLAN-SGLT2-CV-DEATH"]

        # Run 1: Standard alpha 0.05
        run_1 = self.engine.execute_analysis_workflow(plan.plan_id, snap.snapshot_id, {"alpha": 0.05})
        # Run 2: Stringent alpha 0.01
        run_2 = self.engine.execute_analysis_workflow(plan.plan_id, snap.snapshot_id, {"alpha": 0.01})

        diff = self.engine.compute_diff(run_1.job_id, run_2.job_id)
        self.assertIsNotNone(diff)
        self.assertTrue(diff.parameters_changed)
        self.assertFalse(diff.dataset_version_changed)
        self.assertTrue(diff.conclusion_concordance)

    def test_04_license_export_protection(self):
        """Verifies proprietary research dataset export is safely blocked under data use agreement."""
        allowed_prop, msg_prop = self.engine.verify_dataset_export_permission("DS-RESTRICTED-PHARMA-PROPRIETARY")
        self.assertFalse(allowed_prop)
        self.assertIn("blocked", msg_prop)

        allowed_open, _ = self.engine.verify_dataset_export_permission("DS-SGLT2-HF-TRIAL-01")
        self.assertTrue(allowed_open)

    def test_05_fastapi_rest_endpoints(self):
        """Verifies FastAPI REST endpoints for the Scientific Compute Engine."""
        # GET /v1/compute/datasets/DS-SGLT2-HF-TRIAL-01
        resp_ds = self.client.get("/v1/compute/datasets/DS-SGLT2-HF-TRIAL-01")
        self.assertEqual(resp_ds.status_code, 200)
        data_ds = resp_ds.json()
        self.assertEqual(data_ds["dataset_id"], "DS-SGLT2-HF-TRIAL-01")

        # POST /v1/compute/workflows/run
        resp_run = self.client.post(
            "/v1/compute/workflows/run",
            json={
                "plan_id": "PLAN-SGLT2-CV-DEATH",
                "snapshot_id": "SNAP-SGLT2-HF-v1.0",
            },
        )
        self.assertEqual(resp_run.status_code, 200)
        job_data = resp_run.json()
        run_id = job_data["job_id"]
        art_id = job_data["results"][0]["artifact_id"]
        self.assertEqual(job_data["status"], "COMPLETED")

        # GET /v1/compute/lineage/{run_id}
        resp_lineage = self.client.get(f"/v1/compute/lineage/{run_id}")
        self.assertEqual(resp_lineage.status_code, 200)
        lineage_data = resp_lineage.json()
        self.assertGreaterEqual(len(lineage_data["nodes"]), 5)

        # POST /v1/compute/runs/{run_id}/reproduce
        resp_repro = self.client.post(f"/v1/compute/runs/{run_id}/reproduce")
        self.assertEqual(resp_repro.status_code, 200)
        repro_data = resp_repro.json()
        self.assertEqual(repro_data["certificate"]["reproducibility_verdict"], "FULLY_REPRODUCIBLE")

        # POST /v1/compute/claims/candidate
        resp_cand = self.client.post("/v1/compute/claims/candidate", json={"artifact_id": art_id})
        self.assertEqual(resp_cand.status_code, 200)
        claim_data = resp_cand.json()
        claim_id = claim_data["claim_id"]
        self.assertEqual(claim_data["human_review_status"], "PENDING_REVIEW")

        # POST /v1/compute/claims/promote
        resp_prom = self.client.post(
            "/v1/compute/claims/promote",
            json={
                "claim_id": claim_id,
                "reviewer_name": "Dr. Sarah Chen, MD",
                "approve": True,
            },
        )
        self.assertEqual(resp_prom.status_code, 200)
        prom_data = resp_prom.json()
        self.assertEqual(prom_data["human_review_status"], "APPROVED")
        self.assertTrue(prom_data["promoted_to_evidence_graph"])


if __name__ == "__main__":
    unittest.main()
