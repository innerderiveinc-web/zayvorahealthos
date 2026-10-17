"""
Unit tests for NCBI PubMed authenticated integration with NCBI_API_KEY.
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import get_settings
from app.sources.pubmed_client import get_pubmed_client, NCBIPubMedClient
from app.sources.registry import SourceUniverseRegistry


class TestNCBIPubMedIntegration(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        SourceUniverseRegistry.initialize_defaults()

    def test_01_api_key_loaded_and_configured(self):
        settings = get_settings()
        self.assertIsNotNone(settings.NCBI_API_KEY)
        self.assertTrue(settings.NCBI_API_KEY.startswith("a96f22"))
        
        pubmed_client = get_pubmed_client()
        self.assertTrue(pubmed_client.is_configured())

    def test_02_pubmed_status_endpoint(self):
        res = self.client.get("/v1/sources/pubmed/status")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "ready")
        self.assertTrue(data["api_key_configured"])
        self.assertIn("10 requests/second", data["rate_limit"])
        self.assertEqual(data["source_id"], "SRC-PUBMED")

    def test_03_pubmed_query_endpoint(self):
        res = self.client.post("/v1/sources/pubmed/query", json={"query": "berberine type 2 diabetes", "max_results": 2})
        self.assertEqual(res.status_code, 200)
        articles = res.json()
        self.assertGreaterEqual(len(articles), 1)
        first = articles[0]
        self.assertEqual(first["source_registry"], "SRC-PUBMED")
        self.assertTrue(first["verified"])
        self.assertTrue(first["pmid"].isdigit())

    def test_04_source_universe_registry_has_pubmed(self):
        pubmed_source = SourceUniverseRegistry.get_source("SRC-PUBMED")
        self.assertIsNotNone(pubmed_source)
        self.assertIn("PubMed", pubmed_source.source_name)
        self.assertEqual(pubmed_source.api_url, "https://eutils.ncbi.nlm.nih.gov/entrez/eutils")
        self.assertTrue(pubmed_source.api_available)

    def test_05_frontier_llm_gateway_keys_configured(self):
        from app.core.llm_gateway import LLMGateway
        self.assertTrue(LLMGateway.is_gemini_configured())
        self.assertTrue(LLMGateway.is_anthropic_configured())


if __name__ == "__main__":
    unittest.main()
