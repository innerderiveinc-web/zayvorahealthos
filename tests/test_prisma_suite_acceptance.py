"""
ZMIE One-Click PRISMA 2020 Systematic Review & Publication Suite Acceptance Suite (Phase 5)
Validates:
1. Autonomous PRISMA 2020 review generation with 4-phase flow metrics and RoB 2 table.
2. 27-item PRISMA 2020 compliance checklist (27/27 items = 100%).
3. Vector PRISMA Flow Diagram SVG rendering.
4. BibTeX (.bib) and RIS (.ris) bibliographic reference exports for citation managers.
5. Full styled standalone HTML publication manuscript exporter.
6. REST API endpoints for all PRISMA operations.
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.research.prisma_engine import PRISMA2020Engine


class TestPRISMASuiteAcceptance(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_01_prisma_review_generation_and_27_item_checklist(self):
        """Generates complete systematic review with 100% compliant 27-item PRISMA checklist."""
        review = PRISMA2020Engine.generate_review("ashwagandha anxiety and cortisol")
        self.assertIn("Withania somnifera", review.review_title)
        self.assertGreater(review.prisma_flow.total_records_identified, 0)
        self.assertGreater(review.prisma_flow.studies_included_meta_analysis, 0)

        # RoB 2 table
        self.assertGreater(len(review.risk_of_bias_table), 0)
        for rob in review.risk_of_bias_table:
            self.assertIn(rob.overall_bias, ["Low risk", "Some concerns", "High risk"])

        # 27-item Checklist
        chk = review.prisma_checklist_compliance
        self.assertIsNotNone(chk)
        self.assertEqual(chk.total_items, 27)
        self.assertEqual(chk.compliant_items, 27)
        self.assertEqual(chk.compliance_rate_percent, 100.0)

    def test_02_prisma_flow_diagram_svg_markup(self):
        """Validates vector SVG PRISMA flow diagram generation with 4 phases."""
        review = PRISMA2020Engine.generate_review("ashwagandha anxiety")
        svg = review.flow_diagram_svg
        self.assertIsNotNone(svg)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("1. IDENTIFICATION", svg)
        self.assertIn("2. SCREENING", svg)
        self.assertIn("3. ELIGIBILITY", svg)
        self.assertIn("4. INCLUDED", svg)

    def test_03_bibtex_and_ris_citation_exports(self):
        """Generates valid BibTeX and RIS format citations for included trials."""
        review = PRISMA2020Engine.generate_review("ashwagandha anxiety")

        # BibTeX
        bibtex = PRISMA2020Engine.export_bibtex(review.risk_of_bias_table)
        self.assertIn("@article{", bibtex)
        self.assertIn("author =", bibtex)
        self.assertIn("journal =", bibtex)

        # RIS
        ris = PRISMA2020Engine.export_ris(review.risk_of_bias_table)
        self.assertIn("TY  - JOUR", ris)
        self.assertIn("AU  -", ris)
        self.assertIn("TI  -", ris)
        self.assertIn("ER  -", ris)

    def test_04_publication_html_manuscript_export(self):
        """Generates styled standalone HTML manuscript with embedded plots and metadata."""
        review = PRISMA2020Engine.generate_review("ashwagandha anxiety")
        html = PRISMA2020Engine.export_publication_html(review)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("<title>", html)
        self.assertIn("PRISMA 2020 Flow Diagram", html)
        self.assertIn("Cochrane Risk of Bias 2.0", html)
        self.assertIn("Cryptographic Provenance Seal", html)

    def test_05_rest_api_prisma_endpoints(self):
        """REST API: Validates all PRISMA review and export routes."""
        headers = {"X-Forwarded-For": "198.51.100.105"}

        # 1. POST /prisma/generate
        res_gen = self.client.post("/v1/research/meta-synthesis/prisma/generate", json={"query": "ashwagandha stress"}, headers=headers)
        self.assertEqual(res_gen.status_code, 200)
        data = res_gen.json()
        self.assertIn("review_title", data)
        self.assertIn("flow_diagram_svg", data)

        # 2. GET /prisma/flow-diagram.svg
        res_svg = self.client.get("/v1/research/meta-synthesis/prisma/flow-diagram.svg?query=ashwagandha", headers=headers)
        self.assertEqual(res_svg.status_code, 200)
        self.assertEqual(res_svg.headers["content-type"], "image/svg+xml")

        # 3. POST /prisma/export/bibtex
        res_bib = self.client.post("/v1/research/meta-synthesis/prisma/export/bibtex", json={"query": "ashwagandha"}, headers=headers)
        self.assertEqual(res_bib.status_code, 200)
        self.assertIn("@article{", res_bib.text)

        # 4. POST /prisma/export/ris
        res_ris = self.client.post("/v1/research/meta-synthesis/prisma/export/ris", json={"query": "ashwagandha"}, headers=headers)
        self.assertEqual(res_ris.status_code, 200)
        self.assertIn("TY  - JOUR", res_ris.text)

        # 5. POST /prisma/export/html
        res_html = self.client.post("/v1/research/meta-synthesis/prisma/export/html", json={"query": "ashwagandha"}, headers=headers)
        self.assertEqual(res_html.status_code, 200)
        self.assertIn("<!DOCTYPE html>", res_html.text)


if __name__ == "__main__":
    unittest.main()
