"""
ZMIE Meta-Synthesis & Forest Plot Acceptance Test Suite
Verifies Cochrane-grade statistical meta-analysis, DerSimonian-Laird random effects,
Higgins I² heterogeneity, vector Forest Plot SVG generation, and GRADE certainty.
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.research.meta_analysis import (
    MetaAnalysisEngine,
    StudyInput,
    OutcomeType
)
from app.research.pico_extractor import PICOExtractionEngine


class TestMetaSynthesisAcceptance(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_01_dersimonian_laird_continuous_pooling(self):
        """Validates DerSimonian-Laird random-effects pooling for continuous clinical trials."""
        cohort = [
            StudyInput(
                study_id="S1",
                study_name="Yin et al.",
                year=2008,
                outcome_type=OutcomeType.MEAN_DIFFERENCE,
                n_intervention=42,
                mean_intervention=-0.80,
                sd_intervention=0.55,
                n_control=42,
                mean_control=0.00,
                sd_control=0.50
            ),
            StudyInput(
                study_id="S2",
                study_name="Zhang et al.",
                year=2008,
                outcome_type=OutcomeType.MEAN_DIFFERENCE,
                n_intervention=58,
                mean_intervention=-0.92,
                sd_intervention=0.58,
                n_control=58,
                mean_control=0.00,
                sd_control=0.52
            ),
            StudyInput(
                study_id="S3",
                study_name="Lan et al.",
                year=2015,
                outcome_type=OutcomeType.MEAN_DIFFERENCE,
                n_intervention=70,
                mean_intervention=-0.85,
                sd_intervention=0.60,
                n_control=70,
                mean_control=0.00,
                sd_control=0.58
            ),
            StudyInput(
                study_id="S4",
                study_name="Yan et al.",
                year=2020,
                outcome_type=OutcomeType.MEAN_DIFFERENCE,
                n_intervention=48,
                mean_intervention=-0.78,
                sd_intervention=0.50,
                n_control=48,
                mean_control=0.00,
                sd_control=0.48
            )
        ]

        res = MetaAnalysisEngine.run_meta_analysis(cohort, outcome_type=OutcomeType.MEAN_DIFFERENCE)

        self.assertEqual(res.num_studies, 4)
        self.assertEqual(res.total_participants, 436)
        # Pooled effect size must reflect clinical mean reduction
        self.assertAlmostEqual(res.pooled_effect, -0.84, delta=0.05)
        self.assertLess(res.ci_lower, res.pooled_effect)
        self.assertGreater(res.ci_upper, res.pooled_effect)
        self.assertTrue(res.is_statistically_significant)
        self.assertEqual(res.favors_direction, "Favors Intervention")
        self.assertLess(res.p_value, 0.001)

        # Heterogeneity metrics
        self.assertGreaterEqual(res.cochran_q, 0.0)
        self.assertEqual(res.degrees_of_freedom, 3)
        self.assertGreaterEqual(res.i_squared_pct, 0.0)
        self.assertLessEqual(res.i_squared_pct, 100.0)

    def test_02_binary_odds_ratio_pooling(self):
        """Validates log-odds transformation and pooling for binary event trials."""
        cohort = [
            StudyInput(
                study_id="B1",
                study_name="Trial Alpha",
                year=2021,
                outcome_type=OutcomeType.ODDS_RATIO,
                n_intervention=100,
                events_intervention=12,
                n_control=100,
                events_control=28
            ),
            StudyInput(
                study_id="B2",
                study_name="Trial Beta",
                year=2022,
                outcome_type=OutcomeType.ODDS_RATIO,
                n_intervention=150,
                events_intervention=18,
                n_control=150,
                events_control=42
            ),
            StudyInput(
                study_id="B3",
                study_name="Trial Gamma",
                year=2023,
                outcome_type=OutcomeType.ODDS_RATIO,
                n_intervention=120,
                events_intervention=15,
                n_control=120,
                events_control=35
            )
        ]

        res = MetaAnalysisEngine.run_meta_analysis(cohort, outcome_type=OutcomeType.ODDS_RATIO)
        self.assertEqual(res.num_studies, 3)
        self.assertEqual(res.total_participants, 740)
        # Log OR must be negative (events less in intervention arm)
        self.assertLess(res.pooled_effect, 0.0)
        self.assertTrue(res.is_statistically_significant)
        self.assertEqual(res.favors_direction, "Favors Intervention")

    def test_03_vector_forest_plot_svg_markup(self):
        """Validates that Forest Plot SVG generates valid, styled XML with summary diamond."""
        cohort = [
            StudyInput(
                study_id="FP1",
                study_name="Study 1",
                year=2019,
                effect_size=-0.50,
                standard_error=0.15,
                n_intervention=50,
                n_control=50
            ),
            StudyInput(
                study_id="FP2",
                study_name="Study 2",
                year=2022,
                effect_size=-0.70,
                standard_error=0.12,
                n_intervention=60,
                n_control=60
            )
        ]

        res = MetaAnalysisEngine.run_meta_analysis(cohort)
        svg = res.forest_plot_svg

        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.strip().endswith("</svg>"))
        self.assertIn("Study 1 (2019)", svg)
        self.assertIn("Study 2 (2022)", svg)
        self.assertIn("Pooled Random Effects", svg)
        # Summary diamond polygon must be present
        self.assertIn("<polygon points=", svg)
        # Null line dashed
        self.assertIn('stroke="#ef4444"', svg)
        self.assertIn("Favors Intervention", svg)

    def test_04_pico_extraction_from_registry(self):
        """Validates automated PICO extraction from clinical trial record dictionary."""
        trial_record = {
            "trial_id": "NCT04385992",
            "title": "Randomized Double-Blind Trial of Berberine Formulation in Type 2 Diabetes",
            "population": "Adults aged 18-65 with HbA1c > 7.5%",
            "interventions": ["Berberine 500mg BID", "Placebo Matching Capsule"],
            "primary_outcomes": ["HbA1c absolute reduction at 12 weeks"],
            "publication_year": 2022,
            "abstract": "We randomized 120 patients (n=120) to evaluate HbA1c change. The intervention showed -0.85% reduction."
        }

        extracted = PICOExtractionEngine.extract_from_trial_record(trial_record)
        self.assertEqual(extracted.trial_id, "NCT04385992")
        self.assertEqual(extracted.pico.sample_size_total, 120)
        self.assertIn("Berberine", extracted.pico.intervention_name)
        self.assertEqual(extracted.rob2.overall_risk_of_bias, "Low risk")
        self.assertEqual(extracted.derived_study_input.n_intervention, 60)
        self.assertEqual(extracted.derived_study_input.n_control, 60)

    def test_05_rest_api_meta_synthesis_endpoint(self):
        """Validates FastAPI POST /v1/research/meta-synthesis and SVG endpoint."""
        # 1. Test full meta-synthesis JSON response
        resp = self.client.post(
            "/v1/research/meta-synthesis",
            json={
                "query": "berberine diabetes",
                "outcome_type": "mean_difference",
                "use_random_effects": True
            }
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("meta_summary", data)
        self.assertIn("clinical_interpretation", data)
        self.assertGreaterEqual(data["meta_summary"]["num_studies"], 1)
        self.assertIn("<svg", data["meta_summary"]["forest_plot_svg"])
        self.assertTrue(any(g in data["meta_summary"]["grade_certainty"] for g in ["HIGH", "MODERATE", "LOW", "VERY_LOW"]))

        # 2. Test SVG direct endpoint
        svg_resp = self.client.post(
            "/v1/research/meta-synthesis/forest-plot.svg",
            json={
                "query": "berberine diabetes",
                "outcome_type": "mean_difference"
            }
        )
        self.assertEqual(svg_resp.status_code, 200)
        self.assertIn("image/svg+xml", svg_resp.headers["content-type"])
        self.assertIn("<svg", svg_resp.text)
        self.assertIn("Pooled Random Effects", svg_resp.text)


if __name__ == "__main__":
    unittest.main()
