"""
ZMIE External Ingestion Connectors Acceptance Suite (Track 3)
Tests:
1. UnpaywallConnector: Open Access resolution, PDF discovery, license evaluation (Classes A/B/C).
2. PMCFullTextConnector: PubMed Central BioC XML/JSON parsing into semantic sections and tables.
3. REST API endpoints:
   - GET /v1/sources/connectors/status
   - POST /v1/sources/unpaywall/resolve
   - GET /v1/sources/pmc/{pmcid}
"""

import unittest
import asyncio
from fastapi.testclient import TestClient

from app.main import app
from app.models.source import AuthorityTier, LicenseClass
from app.ingestion.connectors.unpaywall import UnpaywallConnector
from app.ingestion.connectors.pmc_fulltext import PMCFullTextConnector


class TestExternalConnectorsAcceptance(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.unpaywall = UnpaywallConnector()
        self.pmc = PMCFullTextConnector()

    def test_01_unpaywall_connector_metadata_and_properties(self):
        """Unpaywall connector has correct source ID, authority tier, and default license class."""
        self.assertEqual(self.unpaywall.source_id, "SRC-UNPAYWALL-001")
        self.assertEqual(self.unpaywall.authority_tier, AuthorityTier.TIER_B)
        self.assertEqual(self.unpaywall.default_license_class, LicenseClass.CLASS_C)

    def test_02_unpaywall_gold_oa_resolution(self):
        """Resolving a known Gold Open Access DOI returns direct PDF URL and CC-BY license."""
        loop = asyncio.new_event_loop()
        try:
            res = loop.run_until_complete(
                self.unpaywall.identify("10.3390/molecules24081541")
            )
            self.assertIsNotNone(res)
            self.assertEqual(res["doi"], "10.3390/molecules24081541")
            self.assertTrue(res["is_oa"])
            self.assertEqual(res["oa_status"], "gold")
            self.assertIsNotNone(res["best_oa_location"])
            self.assertIn("pdf", res["best_oa_location"]["pdf_url"])
            self.assertEqual(res["license_class"], LicenseClass.CLASS_B.value)
        finally:
            loop.close()

    def test_03_unpaywall_closed_access_handling(self):
        """Closed access article is identified as non-OA with no PDF URL."""
        loop = asyncio.new_event_loop()
        try:
            res = loop.run_until_complete(
                self.unpaywall.identify("10.1056/NEJMoa022410")
            )
            self.assertIsNotNone(res)
            self.assertFalse(res["is_oa"])
            self.assertEqual(res["oa_status"], "closed")
            self.assertIsNone(res["best_oa_location"])
        finally:
            loop.close()

    def test_04_unpaywall_unknown_doi(self):
        """Unknown DOI returns None without raising uncaught exceptions."""
        loop = asyncio.new_event_loop()
        try:
            res = loop.run_until_complete(
                self.unpaywall.identify("10.9999/nonexistent.doi.12345")
            )
            self.assertIsNone(res)
        finally:
            loop.close()

    def test_05_pmc_fulltext_connector_properties(self):
        """PMC connector initializes with correct attributes."""
        self.assertEqual(self.pmc.source_id, "SRC-PMC-XML-001")
        self.assertEqual(self.pmc.authority_tier, AuthorityTier.TIER_B)

    def test_06_pmc_fulltext_retrieval_and_sectioning(self):
        """PMC connector parses structured passages into clinical sections and tables."""
        loop = asyncio.new_event_loop()
        try:
            res = loop.run_until_complete(
                self.pmc.identify("PMC3285145")
            )
            self.assertIsNotNone(res)
            self.assertEqual(res["pmcid"], "PMC3285145")
            self.assertEqual(res["pmid"], "22105432")
            self.assertIn("Berberine", res["title"])

            # Verify semantic sections
            sections = res["sections"]
            self.assertIn("abstract", sections)
            self.assertIn("results", sections)
            self.assertGreater(len(sections["abstract"]), 0)
            self.assertGreater(len(sections["results"]), 0)

            # Verify table extraction
            tables = res["extracted_tables"]
            self.assertGreater(len(tables), 0)
            self.assertIn("Table 1", tables[0]["caption"])
            self.assertIn("Berberine", tables[0]["content"])
        finally:
            loop.close()

    def test_07_pmc_metadata_fetch(self):
        """PMC fetch_metadata returns lightweight bibliographic metadata without full text passages."""
        loop = asyncio.new_event_loop()
        try:
            meta = loop.run_until_complete(
                self.pmc.fetch_metadata("PMC6612200")
            )
            self.assertIsNotNone(meta)
            self.assertEqual(meta["pmcid"], "PMC6612200")
            self.assertNotIn("sections", meta)
            self.assertIn("total_passages", meta)
            self.assertIn("table_count", meta)
        finally:
            loop.close()

    def test_08_rest_api_connectors_status(self):
        """GET /v1/sources/connectors/status reports all 6 connectors active."""
        resp = self.client.get("/v1/sources/connectors/status")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "active")
        self.assertGreaterEqual(data["total_connectors"], 6)

        source_ids = [c["source_id"] for c in data["connectors"]]
        self.assertIn("SRC-UNPAYWALL-001", source_ids)
        self.assertIn("SRC-PMC-XML-001", source_ids)
        self.assertIn("SRC-EPMC-001", source_ids)
        self.assertIn("SRC-OPENALEX-001", source_ids)

    def test_09_rest_api_unpaywall_resolve_endpoint(self):
        """POST /v1/sources/unpaywall/resolve resolves open access status."""
        resp = self.client.post(
            "/v1/sources/unpaywall/resolve",
            json={"doi": "10.3390/molecules24081541"}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["doi"], "10.3390/molecules24081541")
        self.assertTrue(data["is_oa"])
        self.assertIn("pdf", data["best_oa_location"]["pdf_url"])

    def test_10_rest_api_pmc_fetch_endpoint(self):
        """GET /v1/sources/pmc/{pmcid} fetches structured passages and tables."""
        resp = self.client.get("/v1/sources/pmc/PMC3285145")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["pmcid"], "PMC3285145")
        self.assertIn("sections", data)
        self.assertIn("extracted_tables", data)


if __name__ == "__main__":
    unittest.main()
