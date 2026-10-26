"""
ZMIE Global Clinical & Regulatory Intelligence Acceptance Tests
Validating multi-jurisdictional product resolution, label diffing,
clinical guideline lookups, pharmacovigilance safety events, and claim compliance firewalls.
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.models.clinical_regulatory import (
    RegulatoryAuthorityCode,
    ProductClassification,
    RegulatoryMarketStatus,
    ClaimType
)
from app.clinical_regulatory.engine import ClinicalRegulatoryEngine


class TestClinicalRegulatoryAcceptance(unittest.TestCase):

    def setUp(self):
        self.engine = ClinicalRegulatoryEngine()
        self.client = TestClient(app)

    # -------------------------------------------------------------
    # 1. Product Lookups & Multi-Jurisdictional Resolution
    # -------------------------------------------------------------

    def test_product_jurisdictional_resolution(self):
        prod = self.engine.get_product("DAPAGLIFLOZIN")
        self.assertIsNotNone(prod)
        self.assertEqual(prod.canonical_name, "Dapagliflozin")
        self.assertEqual(len(prod.jurisdictional_instances), 3)

        # US instance
        us_inst = next((j for j in prod.jurisdictional_instances if j.jurisdiction_country == "United States"), None)
        self.assertIsNotNone(us_inst)
        self.assertEqual(us_inst.authority, RegulatoryAuthorityCode.US_FDA)
        self.assertEqual(us_inst.local_brand_name, "Farxiga")
        self.assertEqual(us_inst.classification, ProductClassification.DRUG)
        self.assertEqual(us_inst.marketing_status, RegulatoryMarketStatus.APPROVED)

        # India instance
        in_inst = next((j for j in prod.jurisdictional_instances if j.jurisdiction_country == "India"), None)
        self.assertIsNotNone(in_inst)
        self.assertEqual(in_inst.authority, RegulatoryAuthorityCode.IN_CDSCO)
        self.assertEqual(in_inst.marketing_status, RegulatoryMarketStatus.APPROVED)

    def test_traditional_medicine_classification_divergence(self):
        # Berberine is regulated differently in US vs India
        card = self.engine.compare_jurisdictions("BERBERINE")
        self.assertIsNotNone(card)
        self.assertIn("United States", card.jurisdictions_data)
        self.assertIn("India", card.jurisdictions_data)

        us_class = card.jurisdictions_data["United States"]["classification"]
        in_class = card.jurisdictions_data["India"]["classification"]

        self.assertEqual(us_class, ProductClassification.DIETARY_SUPPLEMENT.value)
        self.assertEqual(in_class, ProductClassification.TRADITIONAL_AYUSH_MEDICINE.value)
        self.assertGreater(len(card.divergences_identified), 0)

    # -------------------------------------------------------------
    # 2. Label Versioning & Diff Engine
    # -------------------------------------------------------------

    def test_label_diffing_new_indications_and_warnings(self):
        diff = self.engine.diff_product_labels("DAPAGLIFLOZIN", "United States")
        self.assertIsNotNone(diff)
        self.assertEqual(diff.old_version_tag, "v1.0")
        self.assertEqual(diff.new_version_tag, "v2.0")
        self.assertGreater(len(diff.indications_added), 0)
        self.assertIn("heart failure", diff.indications_added[0].lower())
        self.assertGreater(len(diff.warnings_added), 0)
        self.assertIn("gangrene", diff.change_summary.lower())

    # -------------------------------------------------------------
    # 3. Clinical Guidelines & Off-Label Separation
    # -------------------------------------------------------------

    def test_clinical_guidelines_recommendations(self):
        guidelines = self.engine.list_guidelines_for_condition("Heart Failure")
        self.assertGreater(len(guidelines), 0)
        hf_guide = guidelines[0]
        self.assertEqual(hf_guide.issuing_body, "AHA / ACC / HFSA")
        self.assertEqual(len(hf_guide.recommendations), 2)

        rec_hfref = hf_guide.recommendations[0]
        self.assertIn("Class 1", rec_hfref.strength_of_recommendation)
        self.assertIn("Level A", rec_hfref.level_of_evidence)
        self.assertFalse(rec_hfref.is_off_label_use)

    # -------------------------------------------------------------
    # 4. Pharmacovigilance & Product Recalls
    # -------------------------------------------------------------

    def test_pharmacovigilance_safety_events(self):
        events = self.engine.get_safety_events_for_product("DAPAGLIFLOZIN")
        self.assertGreater(len(events), 0)
        ev = events[0]
        self.assertEqual(ev.authority, RegulatoryAuthorityCode.US_FDA)
        self.assertIn("ketoacidosis", ev.title.lower())
        self.assertEqual(ev.causality_status, "CONFIRMED_CAUSAL_RISK")

    def test_recalls_query(self):
        recalls = self.engine.get_recalls("METFORMIN")
        self.assertGreater(len(recalls), 0)
        rec = recalls[0]
        self.assertEqual(rec.recall_class, "Class II Recall")
        self.assertIn("NDMA", rec.reason)
        self.assertIn("Apotex", rec.manufacturer)

    # -------------------------------------------------------------
    # 5. Claim Compliance Firewall Engine
    # -------------------------------------------------------------

    def test_claim_firewall_disease_claim_on_supplement_rejected(self):
        assessment = self.engine.evaluate_claim_compliance(
            product_id="BERBERINE",
            claim_statement="Berberine cures diabetes and prevents heart failure.",
            target_jurisdiction="United States",
            claim_category=ClaimType.THERAPEUTIC_CLAIM
        )
        self.assertFalse(assessment.is_supported_by_approved_label)
        self.assertFalse(assessment.is_permitted_in_jurisdiction)
        self.assertEqual(assessment.compliance_verdict, "NON_COMPLIANT_DISEASE_CLAIM_FOR_SUPPLEMENT")
        self.assertGreater(len(assessment.overstatement_flags), 0)
        self.assertIsNotNone(assessment.required_mandatory_disclaimer)
        self.assertIn("legal counsel", assessment.legal_advice_disclaimer.lower())

    def test_claim_firewall_on_label_drug_claim_permitted(self):
        assessment = self.engine.evaluate_claim_compliance(
            product_id="DAPAGLIFLOZIN",
            claim_statement="Farxiga is indicated to reduce cardiovascular death and heart failure hospitalization in adults with heart failure.",
            target_jurisdiction="United States",
            claim_category=ClaimType.THERAPEUTIC_CLAIM
        )
        self.assertTrue(assessment.is_supported_by_approved_label)
        self.assertTrue(assessment.is_permitted_in_jurisdiction)
        self.assertEqual(assessment.compliance_verdict, "ON_LABEL_THERAPEUTIC_CLAIM_PERMITTED")
        self.assertEqual(len(assessment.overstatement_flags), 0)

    # -------------------------------------------------------------
    # 6. REST API Endpoints Integration
    # -------------------------------------------------------------

    def test_api_endpoints(self):
        # 1. Product details
        res = self.client.get("/v1/clinical-regulatory/products/DAPAGLIFLOZIN")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["canonical_name"], "Dapagliflozin")

        # 2. Compare jurisdictions
        res = self.client.post("/v1/clinical-regulatory/compare", json={
            "product_id": "DAPAGLIFLOZIN"
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn("United States", res.json()["jurisdictions_data"])

        # 3. Label diff
        res = self.client.get("/v1/clinical-regulatory/labels/DAPAGLIFLOZIN/diff?jurisdiction=United%20States")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Fournier", res.json()["change_summary"])

        # 4. Guidelines query
        res = self.client.get("/v1/clinical-regulatory/guidelines?condition=Heart%20Failure")
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(res.json()), 0)

        # 5. Safety events
        res = self.client.get("/v1/clinical-regulatory/safety/DAPAGLIFLOZIN")
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(res.json()), 0)

        # 6. Recalls
        res = self.client.get("/v1/clinical-regulatory/recalls?product_id=METFORMIN")
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(res.json()), 0)

        # 7. Claim check
        res = self.client.post("/v1/clinical-regulatory/claims/check", json={
            "product_id": "BERBERINE",
            "claim_statement": "Berberine guarantees a cure for diabetes.",
            "target_jurisdiction": "United States"
        })
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.json()["is_permitted_in_jurisdiction"])


if __name__ == "__main__":
    unittest.main()
