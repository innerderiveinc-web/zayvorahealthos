"""
ZMIE Full-Text PDF & Clinical Table Miner Acceptance Suite (Phase 4)
Validates:
1. Extraction of Table 1: Baseline Demographics & Characteristics (N, Age, Baseline Biomarkers).
2. Extraction of Table 2: Efficacy Outcomes (Continuous endpoints Mean ± SD, p-values).
3. Extraction of Table 3: Adverse Events (Incident rates, count and percentage).
4. Zero-hallucination SHA-256 Cryptographic Provenance Anchoring per cell/datapoint.
5. REST API endpoint `POST /v1/research/meta-synthesis/mine-tables`.
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.research.pdf_table_miner import PDFClinicalTableMiner


SAMPLE_CLINICAL_PAPER_PAGES = [
    # Page 1: Abstract & Intro
    (
        "CLINICAL PHARMACOLOGY & METABOLISM\n"
        "Efficacy of Standardized Botanical Alkaloid in Adults with Type 2 Diabetes\n"
        "Abstract: A randomized double-blind trial was conducted.\n"
        "Methods: Adult patients aged 35-70 were randomized 1:1 to intervention or placebo."
    ),
    # Page 2: Table 1 Baseline Characteristics
    (
        "RESULTS\n"
        "Participant Flow and Baseline Demographics\n\n"
        "Table 1: Baseline Demographic and Clinical Characteristics of Patients\n"
        "Variable\tIntervention (N = 45)\tPlacebo (N = 44)\tP-Value\n"
        "Age (years)\t54.2 ± 6.8\t53.8 ± 7.1\t0.78\n"
        "Sex (Female)\t24 (53.3%)\t22 (50.0%)\t0.75\n"
        "BMI (kg/m2)\t28.4 ± 3.2\t28.1 ± 3.4\t0.67\n"
        "Baseline HbA1c (%)\t8.6 ± 0.9\t8.5 ± 0.8\t0.82\n"
        "Fasting Plasma Glucose (mmol/L)\t9.4 ± 1.5\t9.2 ± 1.4\t0.51"
    ),
    # Page 3: Table 2 Efficacy Outcomes & Table 3 Adverse Events
    (
        "Primary and Secondary Glycemic Outcomes at Week 12\n\n"
        "Table 2. Primary Efficacy Endpoints at 12 Weeks Follow-up\n"
        "Endpoint\tIntervention Group\tPlacebo Group\tP-Value\n"
        "HbA1c Reduction (%)\t-1.25 ± 0.35\t-0.31 ± 0.22\t<0.001\n"
        "Fasting Glucose Reduction (mmol/L)\t-2.1 ± 0.6\t-0.4 ± 0.3\t<0.001\n"
        "Insulin Sensitivity HOMA-IR\t-1.4 ± 0.5\t-0.2 ± 0.3\t0.004\n\n"
        "Safety and Tolerability\n\n"
        "Table 3: Summary of Incident Adverse Events During Study\n"
        "Adverse Event\tIntervention\tPlacebo\tP-Value\n"
        "Mild Diarrhea\t4 (8.9%)\t1 (2.3%)\t0.19\n"
        "Abdominal Discomfort\t3 (6.7%)\t2 (4.5%)\t0.66\n"
        "Hypoglycemia (blood glucose < 3.9)\t0 (0.0%)\t0 (0.0%)\t1.00\n"
        "Study Discontinuation\t1 (2.2%)\t2 (4.5%)\t0.55"
    )
]


class TestPDFTableMinerAcceptance(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_01_extract_table_1_baseline_demographics(self):
        """Identifies Table 1 and extracts sample sizes, age, and baseline HbA1c."""
        res = PDFClinicalTableMiner.parse_full_text_pages(
            pages=SAMPLE_CLINICAL_PAPER_PAGES,
            document_id="PMID:18442638"
        )
        self.assertGreater(res.tables_found, 0)

        t1 = [t for t in res.tables if t.table_type == "baseline_characteristics"][0]
        self.assertIn("Table 1", t1.table_title)
        self.assertEqual(t1.page_number, 2)

        # Sample size detection
        self.assertIn("intervention", res.extracted_sample_sizes)
        self.assertGreaterEqual(res.extracted_sample_sizes["intervention"], 45)

        # Verify Age extraction (Mean ± SD)
        age_dp = [dp for dp in t1.extracted_datapoints if "Age" in dp.variable_name and dp.group_name == "intervention"][0]
        self.assertEqual(age_dp.mean_value, 54.2)
        self.assertEqual(age_dp.sd_value, 6.8)

    def test_02_extract_table_2_efficacy_outcomes(self):
        """Identifies Table 2 and extracts quantitative continuous effect sizes."""
        res = PDFClinicalTableMiner.parse_full_text_pages(
            pages=SAMPLE_CLINICAL_PAPER_PAGES,
            document_id="PMID:18442638"
        )
        t2 = [t for t in res.tables if t.table_type == "efficacy_outcomes"][0]
        self.assertIn("Table 2", t2.table_title)
        self.assertEqual(t2.page_number, 3)

        # Verify HbA1c reduction extraction
        hba1c_dp = [dp for dp in t2.extracted_datapoints if "HbA1c" in dp.variable_name and dp.group_name == "intervention"][0]
        self.assertAlmostEqual(hba1c_dp.mean_value, 1.25, places=2)
        self.assertAlmostEqual(hba1c_dp.sd_value, 0.35, places=2)

    def test_03_extract_table_3_adverse_events(self):
        """Identifies Table 3 and extracts event frequencies and percentages."""
        res = PDFClinicalTableMiner.parse_full_text_pages(
            pages=SAMPLE_CLINICAL_PAPER_PAGES,
            document_id="PMID:18442638"
        )
        t3 = [t for t in res.tables if t.table_type == "adverse_events"][0]
        self.assertIn("Table 3", t3.table_title)

        diarrhea_dp = [dp for dp in t3.extracted_datapoints if "Diarrhea" in dp.variable_name and dp.group_name == "intervention"][0]
        self.assertEqual(diarrhea_dp.events_count, 4)
        self.assertAlmostEqual(diarrhea_dp.percentage, 8.9, places=1)

    def test_04_cryptographic_provenance_anchoring(self):
        """Every numerical datapoint is cryptographically hashed with page, table, and variable coordinates."""
        res = PDFClinicalTableMiner.parse_full_text_pages(
            pages=SAMPLE_CLINICAL_PAPER_PAGES,
            document_id="PMID:18442638"
        )
        self.assertTrue(len(res.cryptographic_audit_chain) == 64)  # Valid SHA-256

        for table in res.tables:
            self.assertTrue(len(table.provenance_hash) == 64)
            for dp in table.extracted_datapoints:
                self.assertIsNotNone(dp.provenance_anchor)
                self.assertGreater(len(dp.provenance_anchor), 8)

    def test_05_rest_api_mine_tables_endpoint(self):
        """REST API: POST /v1/research/meta-synthesis/mine-tables extracts structured tables."""
        headers = {"X-Forwarded-For": "198.51.100.99"}
        payload = {
            "document_id": "PMID:18442638",
            "pages_text": SAMPLE_CLINICAL_PAPER_PAGES
        }
        resp = self.client.post("/v1/research/meta-synthesis/mine-tables", json=payload, headers=headers)
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertEqual(data["document_id"], "PMID:18442638")
        self.assertEqual(data["total_pages"], 3)
        self.assertGreaterEqual(data["tables_found"], 3)
        self.assertIn("cryptographic_audit_chain", data)


if __name__ == "__main__":
    unittest.main()
