"""
Acceptance test suite for the Master Pharmacopoeia (622+ Herbs - API & UPI)
and Living Medical Encyclopedia endpoints.
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.db.pharmacopoeia_master_seed import PharmacopoeiaMasterRegistry
from app.db.classical_corpus_seed import ClassicalCorpusBulkLoader


class TestPharmacopoeiaMasterAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_master_database_scale(self):
        """Verifies that the registry contains 600+ authentic medicinal taxa."""
        total = PharmacopoeiaMasterRegistry.get_total_count()
        self.assertGreaterEqual(total, 600)
        self.assertEqual(total, 622)

    def test_02_master_herb_data_completeness(self):
        """Verifies each master herb has authentic botanical, Unani, Ayurvedic, and Pharmacopoeial metadata."""
        herbs = PharmacopoeiaMasterRegistry.get_all()
        self.assertEqual(len(herbs), 622)
        for h in herbs[:50]:  # sample check
            self.assertIn("key", h)
            self.assertIn("botanical_name", h)
            self.assertIn("family", h)
            self.assertIn("unani", h)
            self.assertIn("ayurveda", h)
            self.assertIn("official_pharmacopoeia", h)
            self.assertTrue(len(h["unani"]["name"]) > 0)
            self.assertTrue(len(h["ayurveda"]["name"]) > 0)
            self.assertTrue("API" in h["official_pharmacopoeia"] or "UPI" in h["official_pharmacopoeia"])

    def test_03_search_and_pagination_api(self):
        """Tests GET /v1/topics/pharmacopoeia listing and search."""
        # 1. Listing with limit
        resp = self.client.get("/v1/topics/pharmacopoeia?limit=10")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["total_count"], 622)
        self.assertEqual(len(data["results"]), 10)

        # 2. Search by botanical binomial
        resp_s = self.client.get("/v1/topics/pharmacopoeia?q=Adhatoda")
        self.assertEqual(resp_s.status_code, 200)
        data_s = resp_s.json()
        self.assertGreaterEqual(data_s["matched_count"], 1)
        keys = [x["key"] for x in data_s["results"]]
        self.assertIn("adhatoda_vasica", keys)

        # 3. Search by common/Urdu name
        resp_u = self.client.get("/v1/topics/pharmacopoeia?q=Mulethi")
        self.assertEqual(resp_u.status_code, 200)
        data_u = resp_u.json()
        self.assertGreaterEqual(data_u["matched_count"], 1)

    def test_04_monograph_generation_for_master_herb(self):
        """Tests that full 18-part ZAYVORA monograph is generated for any master herb."""
        resp = self.client.get("/v1/topics/monograph/crocus_sativus")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("monograph", data)
        m = data["monograph"]
        self.assertEqual(m["key"], "crocus_sativus")
        self.assertIn("arabic_persian_urdu_name", m)
        self.assertIn("botanical_identity", m)
        self.assertIn("mizaj", m)
        self.assertIn("therapeutic_actions", m)
        self.assertIn("dosage", m)
        self.assertIn("method_of_preparation", m)
        self.assertIn("compound_formulations", m)
        self.assertIn("classical_references", m)
        self.assertIn("quality_standards", m)

    def test_05_fallback_resolution_in_classical_corpus(self):
        """Verifies ClassicalCorpusBulkLoader seamlessly finds and generates monographs for master herbs."""
        herb = ClassicalCorpusBulkLoader.find_by_query("nigella_sativa")
        self.assertIsNotNone(herb)
        self.assertEqual(herb["key"], "nigella_sativa")

        monograph = ClassicalCorpusBulkLoader.get_full_monograph("nigella_sativa")
        self.assertIsNotNone(monograph)
        self.assertEqual(monograph["key"], "nigella_sativa")
        self.assertIn("Kalonji", monograph["arabic_persian_urdu_name"])

    def test_06_allopathic_drug_herb_firewall(self):
        """Verifies Allopathic Drug-Herb Interaction Firewall calculates CYP and transporter hazards."""
        # Test direct API endpoint
        resp = self.client.get("/v1/topics/safety/drug-herb/berberine")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["firewall_report"]
        self.assertEqual(data["overall_clinical_hazard_level"], "CRITICAL_CONTRAINDICATION")
        self.assertIn("Cyclosporine", data["specific_high_risk_drugs"])
        self.assertIn("Atorvastatin", data["specific_high_risk_drugs"])
        self.assertGreaterEqual(data["mandatory_washout_period_days"], 14)

        # Test inclusion inside 18-part monograph
        m_resp = self.client.get("/v1/topics/monograph/berberine")
        self.assertEqual(m_resp.status_code, 200)
        mono = m_resp.json()["monograph"]
        self.assertIn("allopathic_drug_interactions", mono)
        self.assertEqual(mono["allopathic_drug_interactions"]["overall_clinical_hazard_level"], "CRITICAL_CONTRAINDICATION")

    def test_07_qarabadeen_multi_edition_reconciliation(self):
        """Verifies multi-edition Qarabadeen variation reconciliation for classical polyherbal recipes."""
        # 1. List all reconciliations
        resp = self.client.get("/v1/topics/qarabadeen/reconciliations")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreaterEqual(data["total_compounds"], 5)
        keys = [x["compound_key"] for x in data["reconciliations"]]
        self.assertIn("majun_dabeed_ul_ward", keys)
        self.assertIn("yogaraja_guggulu", keys)

        # 2. Deep comparative variant analysis
        deep_resp = self.client.get("/v1/topics/qarabadeen/reconciliation/majun_dabeed_ul_ward")
        self.assertEqual(deep_resp.status_code, 200)
        rec = deep_resp.json()["reconciliation"]
        self.assertEqual(rec["traditional_system"], "Unani Tibb")
        self.assertGreaterEqual(len(rec["editions_evaluated"]), 3)
        self.assertGreaterEqual(len(rec["ingredient_variance_matrix"]), 2)
        # Check Rose petals variance
        rose = next((x for x in rec["ingredient_variance_matrix"] if "Gul-e-Surkh" in x["ingredient_name"]), None)
        self.assertIsNotNone(rose)
        self.assertGreater(rose["variance_percentage"], 10.0)

    def test_08_live_clinical_evidence_harvesting(self):
        """Verifies real-time live trial surveillance against PubMed & ClinicalTrials.gov."""
        resp = self.client.get("/v1/topics/monograph/ashwagandha/live-trials?limit=2")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(data["total_trials_harvested"], 1)
        trial = data["trials"][0]
        self.assertIn("trial_id", trial)
        self.assertIn("primary_endpoint_result", trial)
        self.assertIn("statistical_significance", trial)
        self.assertIn("cryptographic_sha256_audit", trial)

    def test_09_defensive_key_normalization_bug_proof(self):
        """Verifies bug-proof normalization for hyphens, spaces, and case variants."""
        variants = ["berberis_aristata", "berberis-aristata", "Berberis Aristata", "BERBERIS_ARISTATA"]
        for var in variants:
            m = ClassicalCorpusBulkLoader.get_full_monograph(var)
            self.assertIsNotNone(m, f"Monograph lookup failed for variant: {var}")
            self.assertIn("Berberis aristata", m["botanical_identity"]["botanical_name"])

            herb = PharmacopoeiaMasterRegistry.find_by_key(var)
            self.assertIsNotNone(herb, f"Pharmacopoeia lookup failed for variant: {var}")

    def test_10_workbench_javascript_syntax_guard(self):
        """Ensures that workbench.html JavaScript is 100% syntactically valid and never has unclosed blocks."""
        import subprocess
        with open("workbench.html") as f:
            text = f.read()
        s_start = text.find("<script>") + 8
        s_end = text.rfind("</script>")
        self.assertGreater(s_start, 8)
        self.assertGreater(s_end, s_start)
        full_script = text[s_start:s_end]

        wrapper = "try { new Function(" + repr(full_script) + "); print('SYNTAX_OK'); } catch(e) { print('SYNTAX_FAIL:' + e.message); }"
        with open("/tmp/syntax_guard_test.js", "w") as out:
            out.write(wrapper)

        res = subprocess.run(
            ["/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc", "/tmp/syntax_guard_test.js"],
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("SYNTAX_OK", res.stdout)


if __name__ == "__main__":
    unittest.main()
