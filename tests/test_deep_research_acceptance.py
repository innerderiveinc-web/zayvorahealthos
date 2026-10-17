"""
Acceptance Test Suite for ZMIE Deep Research Intelligence Layer (Prompt 6)
Validates:
1. Research job creation and Plan-First generation (PICO, sub-questions, criteria, search matrix).
2. Screening and study filtering (zero tolerance for retracted/promotional sources).
3. Evidence table extraction (PICO alignment, dosage, effect sizes, risk of bias).
4. Contradiction discovery and divergence root-cause taxonomy (no forced consensus).
5. Research Gap prioritization and Next-Best-Research-Question formulation.
6. Multi-stage autonomous execution and reproducible report generation.
7. Snapshots, checkpoints, and diff computation.
8. API route validation via TestClient.
"""

import unittest
import asyncio
from fastapi.testclient import TestClient

from app.main import app
from app.models.research import ResearchJobState, AssertionType, ContradictionType
from app.research.engine import DeepResearchOperatingEngine
from app.research.planner import ResearchPlannerAgent
from app.research.screening import ScreeningAndExtractionAgent
from app.research.synthesis import SynthesisAndContradictionAgent


class TestDeepResearchLayerAcceptance(unittest.TestCase):

    def setUp(self):
        try:
            asyncio.get_event_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())
        self.client = TestClient(app)
        self.question = "What is the clinical efficacy, mechanism of action, and safety profile of Berberine compared to Metformin in Type 2 Diabetes?"
        self.systems = ["modern", "unani", "ayurveda"]

    def test_01_plan_first_generation(self):
        """Validates that a comprehensive ResearchPlan is generated before execution."""
        plan = ResearchPlannerAgent.create_plan(
            question=self.question,
            target_systems=self.systems,
            budget_limit=50
        )
        self.assertIsNotNone(plan.plan_id)
        self.assertTrue(plan.primary_question.startswith("What is the clinical efficacy"))
        self.assertIn("Berberine", plan.pico.intervention)
        self.assertIn("Diabetes", plan.pico.population)
        self.assertGreaterEqual(len(plan.sub_questions), 3)
        self.assertGreaterEqual(len(plan.criteria.inclusion), 2)
        self.assertGreaterEqual(len(plan.criteria.exclusion), 2)
        self.assertGreaterEqual(len(plan.search_matrix), 3)

    def test_02_screening_and_integrity_firewall(self):
        """Verifies screening exclusions: retracted papers and commercial ads are rejected."""
        plan = ResearchPlannerAgent.create_plan(self.question, self.systems)
        candidates = [
            {
                "source_id": "VALID-RCT-01",
                "title": "Randomized trial of berberine in type 2 diabetes",
                "abstract": "Double-blind clinical study with 120 patients.",
                "is_retracted": False
            },
            {
                "source_id": "RETRACTED-01",
                "title": "Miracle berberine reverses diabetes overnight",
                "abstract": "Dubious data.",
                "is_retracted": True
            },
            {
                "source_id": "COMMERCIAL-01",
                "title": "Buy cheap berberine online supplement free shipping",
                "abstract": "Best commercial deals.",
                "is_retracted": False
            }
        ]

        decisions = ScreeningAndExtractionAgent.screen_candidates(candidates, plan)
        self.assertEqual(len(decisions), 3)

        d_map = {d.source_id: d for d in decisions}
        self.assertEqual(d_map["VALID-RCT-01"].verdict, "INCLUDED")
        self.assertEqual(d_map["RETRACTED-01"].verdict, "EXCLUDED")
        self.assertIn("retracted", d_map["RETRACTED-01"].exclusion_reason.lower())
        self.assertEqual(d_map["COMMERCIAL-01"].verdict, "EXCLUDED")

    def test_03_evidence_table_extraction(self):
        """Ensures structured EvidenceTable entries are properly extracted and populated."""
        plan = ResearchPlannerAgent.create_plan(self.question, self.systems)
        candidates = [
            {
                "source_id": "VALID-RCT-01",
                "title": "Randomized trial of berberine in type 2 diabetes",
                "abstract": "Clinical study in n=116 patients assessing HbA1c reduction.",
                "is_retracted": False,
                "evidence_grade": "E2_CONTROLLED_TRIAL",
                "study_design": "Double-blind RCT",
                "sample_size": 116,
                "duration": "12 weeks",
                "findings": "Significant HbA1c drop of 1.5%",
                "effect_size": "p < 0.01"
            }
        ]
        decisions = ScreeningAndExtractionAgent.screen_candidates(candidates, plan)
        raw_map = {c["source_id"]: c for c in candidates}
        table = ScreeningAndExtractionAgent.extract_evidence_table(decisions, raw_map, plan.pico)

        self.assertEqual(len(table), 1)
        entry = table[0]
        self.assertEqual(entry.source_id, "VALID-RCT-01")
        self.assertEqual(entry.evidence_grade, "E2_CONTROLLED_TRIAL")
        self.assertEqual(entry.sample_size, 116)
        self.assertIn("1.5%", entry.primary_findings)

    def test_04_contradiction_clustering_and_no_forced_consensus(self):
        """Validates contradiction engine detects divergence without forcing artificial consensus."""
        plan = ResearchPlannerAgent.create_plan(self.question, self.systems)
        candidates = DeepResearchOperatingEngine._gather_mock_scholarly_corpus(self.question, plan)
        decisions = ScreeningAndExtractionAgent.screen_candidates(candidates, plan)
        raw_map = {c["source_id"]: c for c in candidates}
        table = ScreeningAndExtractionAgent.extract_evidence_table(decisions, raw_map, plan.pico)

        contradictions = SynthesisAndContradictionAgent.analyze_contradictions(table, self.question)
        self.assertGreaterEqual(len(contradictions), 1)
        cluster = contradictions[0]
        self.assertIsNotNone(cluster.divergence_summary)
        self.assertIsNotNone(cluster.probable_root_cause)
        self.assertIn(cluster.contradiction_type, list(ContradictionType))

    def test_05_research_gaps_and_next_best_questions(self):
        """Verifies identification of unaddressed clinical gaps and next-best research questions."""
        plan = ResearchPlannerAgent.create_plan(self.question, self.systems)
        gaps = SynthesisAndContradictionAgent.identify_research_gaps([], plan.pico)
        self.assertGreaterEqual(len(gaps), 2)
        next_questions = SynthesisAndContradictionAgent.formulate_next_best_questions(gaps, plan.pico)
        self.assertGreaterEqual(len(next_questions), 2)
        self.assertIn("?", next_questions[0].question_text)

    def test_06_end_to_end_investigation_lifecycle(self):
        """Executes full autonomous multi-agent pipeline and validates report structure."""
        loop = asyncio.get_event_loop()
        job = loop.run_until_complete(
            DeepResearchOperatingEngine.create_research_job(
                question=self.question,
                target_systems=self.systems,
                budget_limit=25
            )
        )
        self.assertEqual(job.state, ResearchJobState.PLANNING)

        report = loop.run_until_complete(
            DeepResearchOperatingEngine.execute_investigation(job.job_id)
        )

        self.assertEqual(job.state, ResearchJobState.COMPLETED)
        self.assertIsNotNone(report.report_id)
        self.assertGreater(report.flow_metrics["screened"], 0)
        self.assertGreater(len(report.evidence_table), 0)
        self.assertGreater(len(report.contradictions), 0)
        self.assertGreater(len(report.research_gaps), 0)
        self.assertGreater(len(report.assertions), 0)
        self.assertTrue(len(report.reproducibility_hash) == 64)

    def test_07_snapshots_and_diff_tracking(self):
        """Tests taking immutable checkpoints and computing diffs between job versions."""
        loop = asyncio.get_event_loop()
        job = loop.run_until_complete(
            DeepResearchOperatingEngine.create_research_job(self.question, self.systems)
        )
        snap1 = DeepResearchOperatingEngine.create_snapshot(job.job_id)
        self.assertEqual(snap1.snapshot_version, 1)

        loop.run_until_complete(
            DeepResearchOperatingEngine.execute_investigation(job.job_id)
        )
        snap2 = job.snapshots[-1]
        self.assertGreaterEqual(snap2.snapshot_version, 2)

        diff = DeepResearchOperatingEngine.compute_diff(job.job_id, snap1.snapshot_id, snap2.snapshot_id)
        self.assertGreaterEqual(diff.added_evidence_count, 1)
        self.assertIn("Evidence shift", diff.diff_summary)

    def test_08_api_endpoints(self):
        """Tests FastAPI /v1/research REST endpoints."""
        # 1. Create job
        resp = self.client.post("/v1/research/jobs", json={
            "question": "What is the therapeutic mechanism and safety of Curcumin in Osteoarthritis?",
            "systems": ["modern", "ayurveda"],
            "execute_immediately": True
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        job_id = data["job_id"]

        # 2. Get Plan
        plan_resp = self.client.get(f"/v1/research/{job_id}/plan")
        self.assertEqual(plan_resp.status_code, 200)
        self.assertIn("Curcumin", plan_resp.json()["pico"]["intervention"])

        # 3. Get Evidence
        evi_resp = self.client.get(f"/v1/research/{job_id}/evidence")
        self.assertEqual(evi_resp.status_code, 200)
        self.assertIsInstance(evi_resp.json(), list)

        # 4. Get Conflicts
        conf_resp = self.client.get(f"/v1/research/{job_id}/conflicts")
        self.assertEqual(conf_resp.status_code, 200)

        # 5. Get Gaps
        gaps_resp = self.client.get(f"/v1/research/{job_id}/gaps")
        self.assertEqual(gaps_resp.status_code, 200)
        self.assertIn("gaps", gaps_resp.json())

        # 6. Get Report
        rep_resp = self.client.get(f"/v1/research/{job_id}/report")
        self.assertEqual(rep_resp.status_code, 200)
        self.assertIn("reproducibility_hash", rep_resp.json())


if __name__ == "__main__":
    unittest.main()
