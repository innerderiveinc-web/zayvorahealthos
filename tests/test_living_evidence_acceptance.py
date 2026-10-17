"""
ZMIE Living Evidence Synthesis & Evidence Update Acceptance Tests
Testing continuous surveillance, DerSimonian-Laird random effects meta-analysis,
AI-assisted screening, study incorporation, retraction quarantine, and version diffing.
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.models.living_evidence import (
    ReviewType,
    ReviewStatus,
    EvidenceImpactClass,
    UpdateTriggerType,
    ScreeningStage,
    ExclusionReason,
    CertaintyRating,
    ConclusionChangeClass
)
from app.living_evidence.engine import LivingEvidenceEngine


class TestLivingEvidenceAcceptance(unittest.TestCase):

    def setUp(self):
        self.engine = LivingEvidenceEngine()
        self.client = TestClient(app)

    # -------------------------------------------------------------
    # 1. Baseline Review & Structured PICO Questions
    # -------------------------------------------------------------

    def test_baseline_review_initialization(self):
        rev = self.engine.get_review("REV-SGLT2I-HF")
        self.assertIsNotNone(rev)
        self.assertEqual(rev.review_type, ReviewType.LIVING_SYSTEMATIC_REVIEW)
        self.assertEqual(rev.current_status, ReviewStatus.LIVING_ACTIVE)
        self.assertEqual(rev.current_version_tag, "v1.0")

        # PICO validation
        rq = rev.research_question
        self.assertEqual(rq.framework, "PICO")
        self.assertIn("heart failure", rq.population.lower())
        self.assertIn("SGLT2", rq.intervention_or_exposure)
        self.assertGreater(len(rq.outcomes), 1)

        # Baseline version inspection
        v1 = rev.versions[0]
        self.assertEqual(v1.version_tag, "v1.0")
        self.assertEqual(v1.included_studies_count, 2)
        self.assertGreater(len(v1.meta_analyses), 0)

        # DerSimonian-Laird random effects meta-analysis
        meta = v1.meta_analyses[0]
        self.assertEqual(meta.outcome_name, "CV Death or HF Hospitalization")
        self.assertEqual(meta.model_type, "RANDOM_EFFECTS")
        self.assertAlmostEqual(meta.pooled_estimate, 0.745, places=2)
        self.assertLess(meta.ci_lower, meta.pooled_estimate)
        self.assertGreater(meta.ci_upper, meta.pooled_estimate)
        self.assertEqual(len(meta.forest_plot_data), 2)

    # -------------------------------------------------------------
    # 2. Screening & Eligibility Gating
    # -------------------------------------------------------------

    def test_screening_decisions_and_audit(self):
        # Eligible candidate study
        dec_inc = self.engine.assess_screening_record(
            review_id="REV-SGLT2I-HF",
            title="Dapagliflozin in Heart Failure with Preserved Ejection Fraction (DELIVER Trial)",
            abstract="A randomized double-blind trial evaluating dapagliflozin vs placebo on cardiovascular death or worsening heart failure.",
            study_design="Randomized Controlled Trial",
            reviewer_id="Reviewer Alpha"
        )
        self.assertEqual(dec_inc.decision, "INCLUDE")
        self.assertIsNone(dec_inc.exclusion_reason)
        self.assertTrue(dec_inc.is_ai_assisted)
        self.assertGreater(dec_inc.ai_confidence, 0.90)

        # Ineligible study: Observational design
        dec_obs = self.engine.assess_screening_record(
            review_id="REV-SGLT2I-HF",
            title="Observational registry of SGLT2 inhibitors in a single-center cohort",
            abstract="Retrospective observational analysis of 200 patients receiving SGLT2 inhibitors.",
            study_design="Observational Cohort",
            reviewer_id="Reviewer Beta"
        )
        self.assertEqual(dec_obs.decision, "EXCLUDE")
        self.assertEqual(dec_obs.exclusion_reason, ExclusionReason.WRONG_STUDY_DESIGN)

        # Ineligible study: Wrong drug
        dec_drug = self.engine.assess_screening_record(
            review_id="REV-SGLT2I-HF",
            title="Randomized trial of Sacubitril-Valsartan in acute decompensated heart failure",
            abstract="Double blind RCT assessing ARNI vs enalapril.",
            study_design="Randomized Controlled Trial",
            reviewer_id="Reviewer Gamma"
        )
        self.assertEqual(dec_drug.decision, "EXCLUDE")
        self.assertEqual(dec_drug.exclusion_reason, ExclusionReason.WRONG_INTERVENTION)

    # -------------------------------------------------------------
    # 3. Update Triggers & Surveillance Health
    # -------------------------------------------------------------

    def test_update_trigger_detection(self):
        # Routine trigger
        trig_routine = self.engine.detect_update_trigger(
            review_id="REV-SGLT2I-HF",
            trigger_type=UpdateTriggerType.NEW_RCT,
            source_reference="NEJM-2022-DELIVER",
            description="DELIVER trial completed with primary outcome reduction.",
            impact_class=EvidenceImpactClass.MODERATE_IMPACT
        )
        self.assertEqual(trig_routine.action_decision, "ASSESS")

        # Urgent safety / retraction trigger
        trig_urgent = self.engine.detect_update_trigger(
            review_id="REV-SGLT2I-HF",
            trigger_type=UpdateTriggerType.RETRACTION,
            source_reference="RetractionWatch-1029",
            description="Data fabrication identified in small satellite heart failure study.",
            impact_class=EvidenceImpactClass.CRITICAL_IMPACT
        )
        self.assertEqual(trig_urgent.action_decision, "URGENT_UPDATE")

        # Check health and staleness
        health = self.engine.check_review_health("REV-SGLT2I-HF")
        self.assertEqual(health["status"], ReviewStatus.LIVING_ACTIVE)
        self.assertGreaterEqual(health["pending_evidence_count"], 2)

    # -------------------------------------------------------------
    # 4. Incremental Study Incorporation & Meta-Analysis Recalculation
    # -------------------------------------------------------------

    def test_incorporate_study_and_recalculate(self):
        # Incorporate DELIVER Trial
        v2 = self.engine.incorporate_new_study_and_recalculate(
            review_id="REV-SGLT2I-HF",
            new_study_name="DELIVER Trial (Solomon et al.)",
            trial_id="NCT03614377",
            point_estimate=0.82,
            ci_lower=0.73,
            ci_upper=0.92,
            sample_size=6263,
            approver="ZMIE Lead Methodologist"
        )

        self.assertEqual(v2.version_tag, "v2.0")
        self.assertEqual(v2.included_studies_count, 3)
        self.assertEqual(len(v2.meta_analyses), 1)

        new_meta = v2.meta_analyses[0]
        self.assertEqual(new_meta.studies_included_count, 3)
        self.assertLess(new_meta.pooled_estimate, 0.80)
        self.assertGreater(new_meta.pooled_estimate, 0.70)
        self.assertEqual(len(new_meta.forest_plot_data), 3)

        # PRISMA flow progression
        self.assertGreater(v2.prisma_flow.records_identified, 1420)
        self.assertEqual(v2.prisma_flow.studies_included_quantitative_meta, 3)

    # -------------------------------------------------------------
    # 5. Retraction Handling & Quarantine Protocol
    # -------------------------------------------------------------

    def test_retraction_propagation_and_quarantine(self):
        # Retract EMPEROR-Reduced for test simulation
        v_retract = self.engine.handle_retraction_propagation(
            review_id="REV-SGLT2I-HF",
            retracted_study_family_id="STUDY-EMPEROR-RED",
            retraction_reason="Publisher retraction due to unverified primary data source.",
            approver="ZMIE Scientific Integrity Lead"
        )

        self.assertEqual(v_retract.version_tag, "v2.0")
        self.assertEqual(v_retract.included_studies_count, 1)  # Only DAPA-HF remains
        self.assertIn("QUARANTINED RETRACTED STUDY", v_retract.what_changed_summary)

        # Meta-analysis recalculated without retracted study
        new_meta = v_retract.meta_analyses[0]
        self.assertEqual(new_meta.studies_included_count, 1)
        self.assertEqual(new_meta.pooled_estimate, 0.74)

    # -------------------------------------------------------------
    # 6. Version Diffing & Historical Audit
    # -------------------------------------------------------------

    def test_version_diffing(self):
        # Incorporate a study to create v2.0
        self.engine.incorporate_new_study_and_recalculate(
            review_id="REV-SGLT2I-HF",
            new_study_name="DELIVER Trial",
            trial_id="NCT03614377",
            point_estimate=0.82,
            ci_lower=0.73,
            ci_upper=0.92,
            sample_size=6263,
            approver="Methodologist"
        )

        diff = self.engine.compare_review_versions("REV-SGLT2I-HF", "v1.0", "v2.0")
        self.assertEqual(diff["version_old"], "v1.0")
        self.assertEqual(diff["version_new"], "v2.0")
        self.assertEqual(diff["studies_delta"], 1)
        self.assertTrue(diff["historical_reproducible"])

    # -------------------------------------------------------------
    # 7. REST API Endpoints Integration
    # -------------------------------------------------------------

    def test_api_endpoints(self):
        # 1. List reviews
        res = self.client.get("/v1/living-evidence")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreater(len(data), 0)

        # 2. Get review
        res = self.client.get("/v1/living-evidence/REV-SGLT2I-HF")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["review_id"], "REV-SGLT2I-HF")

        # 3. Health check
        res = self.client.get("/v1/living-evidence/REV-SGLT2I-HF/health")
        self.assertEqual(res.status_code, 200)
        self.assertIn("current_as_of", res.json())

        # 4. Screening endpoint
        res = self.client.post("/v1/living-evidence/REV-SGLT2I-HF/screening", json={
            "title": "Randomized Trial of Empagliflozin in Heart Failure",
            "abstract": "Double blind trial measuring cardiovascular death reduction.",
            "study_design": "Randomized Controlled Trial",
            "reviewer_id": "API Reviewer"
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["decision"], "INCLUDE")

        # 5. Trigger endpoint
        res = self.client.post("/v1/living-evidence/REV-SGLT2I-HF/triggers", json={
            "trigger_type": "NEW_RCT",
            "source_reference": "Trial Registry NCT04000000",
            "description": "New randomized clinical trial announced.",
            "impact_class": "MODERATE_IMPACT"
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["action_decision"], "ASSESS")

        # 6. Incorporate study endpoint
        res = self.client.post("/v1/living-evidence/REV-SGLT2I-HF/incorporate", json={
            "study_name": "EMPEROR-Preserved Trial",
            "trial_registration_id": "NCT03057951",
            "point_estimate": 0.79,
            "ci_lower": 0.69,
            "ci_upper": 0.90,
            "sample_size": 5988,
            "approver": "API Approver"
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["version_tag"], "v2.0")

        # 7. Diff endpoint
        res = self.client.get("/v1/living-evidence/REV-SGLT2I-HF/diff?version_a=v1.0&version_b=v2.0")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["studies_delta"], 1)


if __name__ == "__main__":
    unittest.main()
