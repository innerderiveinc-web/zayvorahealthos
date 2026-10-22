"""
Deep Audit Remediation Acceptance Tests (22 October 2026)
Verifies:
1. NCBIPubMedClient zero-fabrication: returns empty list for unknown queries, never a fake NEJM article.
2. ClinicalTrialsConnector zero-fabrication: returns empty list for unknown queries, never an invented NCT record.
3. Deep Research Engine zero-fabrication: returns empty/unverified summary for unindexed query.
4. Fail-closed endpoint security: unauthenticated POST /v1/research/jobs returns 401.
5. Fail-closed endpoint security: unauthenticated GET /v1/search/history returns 401.
6. Fail-closed endpoint security: unauthenticated GET /v1/search/saved returns 401.
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.sources.pubmed_client import NCBIPubMedClient
from app.ingestion.connectors.clinical_trials import ClinicalTrialsConnector
from app.research.engine import DeepResearchOperatingEngine
from app.research.planner import ResearchPlannerAgent


class TestDeepAuditRemediation(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_01_pubmed_zero_fabrication(self):
        """Verifies pubmed client does not synthesize fake NEJM articles for arbitrary queries."""
        client = NCBIPubMedClient(api_key="none_offline")
        res = client._get_canonical_fallback("Bubblegum In Brain Tumor")
        self.assertEqual(res, [], "Expected empty list, but got synthetic pubmed article!")

    def test_02_clinical_trials_zero_fabrication(self):
        """Verifies clinical trials connector does not invent fake trials for arbitrary queries."""
        conn = ClinicalTrialsConnector()
        res = conn._generate_fallback_trials("Bubblegum", 5)
        self.assertEqual(res, [], "Expected empty list, but got fabricated NCT clinical trial!")

    def test_03_research_engine_zero_fabrication_on_unindexed_query(self):
        """Verifies research engine does not falsely report berberine trials for unrelated query."""
        plan = ResearchPlannerAgent.create_plan("Efficacy of Bubblegum in Pancreatitis", ["modern"])
        candidates = DeepResearchOperatingEngine._gather_mock_scholarly_corpus("Efficacy of Bubblegum in Pancreatitis", plan)
        self.assertEqual(candidates, [], "Expected empty candidate list for unindexed query!")

    def test_04_research_jobs_endpoint_requires_authentication(self):
        """POST /v1/research/jobs must fail closed with 401 without authentication."""
        resp = self.client.post("/v1/research/jobs", json={
            "question": "Unauthenticated access attempt",
            "execute_immediately": False
        })
        self.assertEqual(resp.status_code, 401)

    def test_05_search_history_requires_authentication(self):
        """GET /v1/search/history must fail closed with 401 without authentication."""
        resp = self.client.get("/v1/search/history")
        self.assertEqual(resp.status_code, 401)

    def test_06_search_saved_requires_authentication(self):
        """GET /v1/search/saved must fail closed with 401 without authentication."""
        resp = self.client.get("/v1/search/saved")
        self.assertEqual(resp.status_code, 401)


if __name__ == "__main__":
    unittest.main()
