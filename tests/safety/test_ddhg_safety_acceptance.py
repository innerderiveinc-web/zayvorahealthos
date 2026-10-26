"""
ZMIE Deep Drug-Herb-Gene (DDHG) Safety & Pharmacogenomics Acceptance Suite (Phase 3)
Validates:
1. Gene-Drug pharmacogenomic screening (CYP2C19 *2/*2 + Clopidogrel with FDA Boxed Warning).
2. Gene-Drug lethal toxicity screening (CYP2D6 UM + Codeine respiratory depression).
3. Drug-Herb pharmacokinetic inhibition (Cyclosporine + Berberine CYP3A4/P-gp).
4. Drug-Herb-Gene Triad compounding (Clopidogrel + Ginkgo + CYP2C19 PM).
5. Renal impairment + botanical calcineurin inhibitor exacerbation.
6. REST API endpoint `POST /v1/safety/ddhg-check`.
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.research.ddhg_engine import DeepDrugHerbGeneEngine, InteractionSeverity


class TestDDHGSafetyAcceptance(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_01_cyp2c19_pm_clopidogrel_contraindication(self):
        """Gene-Drug: CYP2C19 Poor Metabolizer with Clopidogrel triggers Black Box warning."""
        report = DeepDrugHerbGeneEngine.evaluate_ddhg_profile(
            drugs=["Clopidogrel"],
            herbs=[],
            genetic_variants=[{"gene": "CYP2C19", "diplotype": "*2/*2"}]
        )
        self.assertEqual(report.overall_status, "BLOCKED_CONTRAINDICATION")
        self.assertGreater(report.critical_alerts_count, 0)

        alert = report.alerts[0]
        self.assertEqual(alert.severity, InteractionSeverity.CRITICAL_CONTRAINDICATION)
        self.assertEqual(alert.interaction_type, "DRUG_GENE")
        self.assertIn("Prasugrel or Ticagrelor", alert.actionable_directive)
        self.assertIsNotNone(alert.fda_boxed_warning_reference)
        self.assertIn("Black Box Warning", alert.fda_boxed_warning_reference)

    def test_02_cyp2d6_um_codeine_lethal_toxicity(self):
        """Gene-Drug: CYP2D6 Ultra-rapid Metabolizer with Codeine triggers fatal toxicity alert."""
        report = DeepDrugHerbGeneEngine.evaluate_ddhg_profile(
            drugs=["Codeine"],
            herbs=[],
            genetic_variants=[{"gene": "CYP2D6", "diplotype": "UM (*1xN)"}]
        )
        self.assertEqual(report.overall_status, "BLOCKED_CONTRAINDICATION")
        alert = [a for a in report.alerts if "Codeine" in a.participating_agents][0]
        self.assertEqual(alert.severity, InteractionSeverity.CRITICAL_CONTRAINDICATION)
        self.assertIn("respiratory depression", alert.clinical_risk.lower())

    def test_03_cyclosporine_berberine_pharmacokinetic_inhibition(self):
        """Drug-Herb: Berberine competitive inhibition of CYP3A4 & P-gp with Cyclosporine."""
        report = DeepDrugHerbGeneEngine.evaluate_ddhg_profile(
            drugs=["Cyclosporine"],
            herbs=["Berberine"]
        )
        self.assertEqual(report.overall_status, "BLOCKED_CONTRAINDICATION")
        alert = [a for a in report.alerts if "Berberine" in a.participating_agents][0]
        self.assertEqual(alert.severity, InteractionSeverity.CRITICAL_CONTRAINDICATION)
        self.assertEqual(alert.washout_days, 14)
        self.assertIn("CYP3A4", alert.pathway_enzymes)

    def test_04_drug_herb_gene_triad_catastrophic_interaction(self):
        """Drug-Herb-Gene Triad: Clopidogrel + Ginkgo biloba + CYP2C19 PM."""
        report = DeepDrugHerbGeneEngine.evaluate_ddhg_profile(
            drugs=["Clopidogrel"],
            herbs=["Ginkgo biloba"],
            genetic_variants=[{"gene": "CYP2C19", "diplotype": "*2/*2"}]
        )
        triad_alerts = [a for a in report.alerts if a.interaction_type == "DRUG_HERB_GENE_TRIAD"]
        self.assertGreater(len(triad_alerts), 0)

        triad = triad_alerts[0]
        self.assertEqual(triad.severity, InteractionSeverity.CRITICAL_CONTRAINDICATION)
        self.assertIn("thrombosis", triad.clinical_risk.lower())
        self.assertIn("hemorrhage", triad.clinical_risk.lower())

    def test_05_renal_impairment_calcineurin_berberine_hazard(self):
        """Renal factor: Severe renal impairment + Berberine + Cyclosporine."""
        report = DeepDrugHerbGeneEngine.evaluate_ddhg_profile(
            drugs=["Cyclosporine"],
            herbs=["Berberine"],
            patient_factors={"egfr": 32}
        )
        renal_alerts = [a for a in report.alerts if "Renal Impairment" in str(a.participating_agents)]
        self.assertGreater(len(renal_alerts), 0)
        self.assertIn("acute renal tubular necrosis", renal_alerts[0].clinical_risk.lower())

    def test_06_rest_api_ddhg_check_endpoint(self):
        """REST API: POST /v1/safety/ddhg-check returns validated DDHG report."""
        headers = {"X-Forwarded-For": "198.51.100.88"}
        payload = {
            "drugs": ["Clopidogrel", "Atorvastatin"],
            "herbs": ["Ginkgo biloba", "Berberine"],
            "genetic_variants": [{"gene": "CYP2C19", "diplotype": "*2/*2"}],
            "patient_factors": {"egfr": 75}
        }
        resp = self.client.post("/v1/safety/ddhg-check", json=payload, headers=headers)
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertIn("overall_status", data)
        self.assertIn("alerts", data)
        self.assertGreater(data["critical_alerts_count"], 0)
        self.assertIn("physician_summary", data)


if __name__ == "__main__":
    unittest.main()
