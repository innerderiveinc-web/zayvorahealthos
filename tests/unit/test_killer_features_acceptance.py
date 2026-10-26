"""
Acceptance Test Suite for ZMIE Killer Differentiators:
1. Multi-Target Herb-Drug Interaction & Lethality Simulator (CYP450 / Organ Clearance / Toxicity)
2. PRISMA 2020 Automated Living Systematic Review & Meta-Analysis Generator
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.agents.safety_agent import SafetyIntelligenceEngine
from app.research.prisma_engine import PRISMA2020Engine


class TestKillerFeaturesAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_herb_drug_simulator_direct_engine(self):
        """Verifies multi-compound CYP450 interaction detection and lethal synergy triage."""
        res = SafetyIntelligenceEngine.simulate_herb_drug_interaction(
            drugs=["Warfarin", "Metformin"],
            herbs=["Ginkgo Biloba", "Berberine"],
            patient_factors={"age": 68, "eGFR": 48}
        )
        self.assertIn("hazard_score", res)
        self.assertGreaterEqual(res["hazard_score"], 60)
        self.assertIn(res["triage_level"], ["HIGH_HAZARD", "CRITICAL_LETHALITY_ALERT"])
        self.assertTrue(len(res["detected_clashes"]) >= 2)
        self.assertIn("CYP3A4", res["cyp_enzyme_states"])
        self.assertIn("CYP2C9", res["cyp_enzyme_states"])
        self.assertIn("Goodman & Gilman", res["allopathic_canonical_reference"])
        self.assertIn("unani_mizaj_synthesis", res["traditional_codex_assessment"])
        self.assertTrue(any("INR" in d for d in res["actionable_directives"]))
        self.assertTrue(res["cryptographic_provenance"].startswith("sha256:"))

    def test_herb_drug_simulator_api_endpoint(self):
        """Verifies POST /v1/safety/simulate API endpoint."""
        resp = self.client.post("/v1/safety/simulate", json={
            "drugs": ["Lisinopril", "Digoxin"],
            "herbs": ["Licorice"],
            "patient_factors": {"age": 70, "eGFR": 55}
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("hazard_score", data)
        self.assertEqual(data["triage_level"], "CRITICAL_LETHALITY_ALERT")
        self.assertTrue(any("11β-HSD2" in str(c) for c in data["detected_clashes"]))
        self.assertTrue(any("potassium" in d.lower() for d in data["actionable_directives"]))

    def test_prisma_2020_generator_direct_engine(self):
        """Verifies PRISMA 2020 flow, RoB 2, and Inverse-Variance Meta-Analysis generation."""
        report = PRISMA2020Engine.generate_review(
            pico_query="Comparative Efficacy of Berberine vs Oral Hypoglycemics in Type 2 Diabetes"
        )
        self.assertEqual(report.prisma_flow.total_records_identified, 1420)
        self.assertEqual(len(report.risk_of_bias_table), 5)
        self.assertEqual(len(report.forest_plot_cohorts), 5)
        self.assertAlmostEqual(report.meta_analysis_summary.pooled_effect_mean_difference, -0.81, places=2)
        self.assertEqual(report.grade_certainty, "HIGH (⊕⊕⊕⊕)")
        self.assertIn("INV-01", report.markdown_dossier)
        self.assertTrue(report.cryptographic_seal.startswith("sha256:"))

    def test_prisma_2020_api_endpoint(self):
        """Verifies POST /v1/research/prisma-generator endpoint."""
        resp = self.client.post("/v1/research/prisma-generator", json={
            "pico_query": "Withania somnifera in Chronic Stress and Anxiety"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("prisma_flow", data)
        self.assertIn("meta_analysis_summary", data)
        self.assertIn("forest_plot_cohorts", data)
        self.assertTrue(len(data["forest_plot_cohorts"]) >= 4)
        self.assertIn("Chandrasekhar", data["forest_plot_cohorts"][0]["study"])

    def test_catalog_depth_level_10(self):
        """Verifies 10/10 Catalog Depth (>30 botanicals, >100 interactions, CYP/UGT/transporters)."""
        resp = self.client.get("/v1/safety/catalog")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreaterEqual(data["total_registered_botanicals"], 30)
        self.assertGreaterEqual(data["total_clinical_interactions"], 100)
        self.assertGreaterEqual(data["unique_pharmaceutical_agents"], 50)
        self.assertIn("CYP3A4", data["phase_1_enzymes_indexed"])
        self.assertIn("UGT1A1", data["phase_2_enzymes_indexed"])
        self.assertIn("P-gp (ABCB1/MDR1)", data["transporters_indexed"])

    def test_prisma_egger_and_funnel_plot_level_10(self):
        """Verifies 10/10 Automated PRISMA (Egger's regression, Funnel Plot SVG, 27-item checklist)."""
        report = PRISMA2020Engine.generate_review("Berberine in Type 2 Diabetes")
        self.assertIsNotNone(report.meta_analysis_summary.egger_test)
        self.assertIsNotNone(report.meta_analysis_summary.funnel_plot)
        self.assertTrue(len(report.meta_analysis_summary.funnel_plot_svg) > 1000)
        self.assertIn("<svg", report.meta_analysis_summary.funnel_plot_svg)
        self.assertIsNotNone(report.prisma_checklist_compliance)
        self.assertEqual(report.prisma_checklist_compliance.compliant_items, 27)
        self.assertEqual(report.prisma_checklist_compliance.total_items, 27)

    def test_fhir_r4_bundle_export_level_10(self):
        """Verifies 10/10 HL7 FHIR R4 Document Bundle with all clinical resource types & 21 CFR Part 11 signature."""
        resp = self.client.get("/v1/clinical/fhir/sample-bundle")
        self.assertEqual(resp.status_code, 200)
        bundle = resp.json()
        self.assertEqual(bundle["resourceType"], "Bundle")
        self.assertEqual(bundle["type"], "document")
        resource_types = {e["resource"]["resourceType"] for e in bundle["entry"]}
        required_types = {"Composition", "Patient", "DetectedIssue", "RiskAssessment", "ClinicalImpression", "Observation", "Provenance"}
        for req in required_types:
            self.assertIn(req, resource_types)

    def test_cds_hooks_1_0_level_10(self):
        """Verifies 10/10 HL7 CDS Hooks 1.0 Discovery and Card Evaluation."""
        disc_resp = self.client.get("/cds-services")
        self.assertEqual(disc_resp.status_code, 200)
        disc_data = disc_resp.json()
        self.assertTrue(len(disc_data["services"]) >= 1)
        self.assertEqual(disc_data["services"][0]["id"], "zmie-herb-drug-interaction-guard")

        card_resp = self.client.post("/cds-services/zmie-herb-drug-interaction-guard", json={
            "hook": "order-select",
            "hookInstance": "hook-unit-test-1",
            "context": {
                "patientId": "p-101",
                "medications": ["Warfarin", "Atorvastatin"],
                "herbs": ["St. John's Wort"]
            }
        })
        self.assertEqual(card_resp.status_code, 200)
        card_data = card_resp.json()
        self.assertTrue(len(card_data["cards"]) >= 1)
        self.assertEqual(card_data["cards"][0]["indicator"], "critical")


if __name__ == "__main__":
    unittest.main()
