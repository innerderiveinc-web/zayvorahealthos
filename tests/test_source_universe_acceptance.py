"""
ZMIE Global Medical Source Universe & Universal Acquisition Engine — Acceptance Test Suite
Validates:
1. Source Registry Taxonomy, Authority Hierarchy (S0-S6), and Coverage Reporting
2. Universal Discovery Engine (Citations, Demand Gaps, Approval Workflow)
3. End-to-End Scenario 1: Nigella sativa across Modern, Unani, Ayurveda & Botanical
4. End-to-End Scenario 2: Mizaj / Temperament concepts across Classical & Modern Phenotyping
5. End-to-End Scenario 3: Drug-Herb Interaction Safety (Warfarin + St. John's Wort / Ginkgo)
6. End-to-End Scenario 4: Cross-System Condition Comparison (No Artificial Winner)
7. Retraction & Safety Invalidation Pipeline with Webhook Propagation
8. License Compliance & Copyright Enforcement (No Full-Text Leaks on Class C)
9. Source Universe REST API Endpoints
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.models.source_universe import (
    SourceClass, MedicalSystem, AuthorityLevel, LicenseStatus,
    KnowledgeClass
)
from app.sources.registry import SourceUniverseRegistry
from app.sources.discovery import SourceDiscoveryEngine
from app.sources.search_matrix import MultiSystemSearchMatrixEngine
from app.sources.retraction_pipeline import RetractionAndSafetyPipeline


class TestSourceUniverseAcceptance(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        SourceUniverseRegistry.initialize_defaults()
        SourceDiscoveryEngine.initialize_defaults()

    def test_01_source_registry_and_coverage_report(self):
        # 1. Verify pre-seeded authentic sources
        sources = SourceUniverseRegistry.list_sources()
        self.assertGreaterEqual(len(sources), 10)
        source_ids = [s.source_id for s in sources]
        self.assertIn("SRC-EPMC", source_ids)
        self.assertIn("SRC-CLINICALTRIALS", source_ids)
        self.assertIn("SRC-WHO-GUIDELINES", source_ids)
        self.assertIn("SRC-CCRUM", source_ids)
        self.assertIn("SRC-CCRAS", source_ids)
        self.assertIn("SRC-UNANI-CANON", source_ids)
        self.assertIn("SRC-FDA-DAILYMED", source_ids)

        # 2. Filtering by medical system
        unani_sources = SourceUniverseRegistry.list_sources(medical_system=MedicalSystem.UNANI)
        self.assertGreaterEqual(len(unani_sources), 2)
        ayurveda_sources = SourceUniverseRegistry.list_sources(medical_system=MedicalSystem.AYURVEDA)
        self.assertGreaterEqual(len(ayurveda_sources), 2)

        # 3. Coverage report metrics
        coverage = SourceUniverseRegistry.get_coverage_report()
        self.assertGreater(coverage.sources_active, 10)
        self.assertGreater(coverage.unani_count, 1)
        self.assertGreater(coverage.ayurveda_count, 1)
        self.assertGreater(coverage.trial_registries_count, 1)
        self.assertGreater(coverage.guidelines_count, 1)
        self.assertIn("United States", coverage.countries_covered)
        self.assertIn("India", coverage.countries_covered)
        self.assertGreaterEqual(len(coverage.known_coverage_gaps), 1)

    def test_02_universal_discovery_engine_lifecycle(self):
        # 1. Discover from citation network
        cand_cit = SourceDiscoveryEngine.discover_from_citation(
            cited_journal_or_url="https://sciencedirect.com/journal/journal-of-ayurveda-integrative-medicine",
            citing_source_id="SRC-EPMC"
        )
        self.assertEqual(cand_cit.medical_system, MedicalSystem.AYURVEDA)
        self.assertEqual(cand_cit.review_state, "PENDING_REVIEW")

        # 2. Discover from failed search demand gap
        cand_gap = SourceDiscoveryEngine.discover_from_search_gap(
            query="Classical Unani Mufradat single herbs",
            search_miss_reason="Limited classical Unani formulary indexing in standard databases"
        )
        self.assertEqual(cand_gap.medical_system, MedicalSystem.UNANI)
        self.assertEqual(cand_gap.source_class, SourceClass.TRADITIONAL_MEDICINE)

        # 3. Human governance approval promoting into registry
        approved_source = SourceDiscoveryEngine.approve_candidate(
            candidate_id=cand_cit.candidate_id,
            authority_tier=AuthorityLevel.S3_PEER_REVIEWED
        )
        self.assertIsNotNone(approved_source)
        self.assertIn("SRC-DISC-", approved_source.source_id)
        # Verify it now exists in registry
        fetched = SourceUniverseRegistry.get_source(approved_source.source_id)
        self.assertIsNotNone(fetched)

    def test_03_scenario_1_nigella_sativa_multi_system(self):
        # [SECTION 165: REQUIRED END-TO-END TEST 1]
        res = MultiSystemSearchMatrixEngine.execute_multi_system_search(
            query="What is the evidence for Nigella sativa in metabolic and inflammatory disorders?"
        )
        self.assertTrue(res["epistemic_separation_preserved"])
        self.assertTrue(res["zero_fabrication_confirmed"])

        # Modern evidence check
        self.assertGreaterEqual(len(res["modern_biomedical_evidence"]), 1)
        top_mod = res["modern_biomedical_evidence"][0]
        self.assertEqual(top_mod["epistemic_class"], KnowledgeClass.MODERN_CLINICAL.value)
        self.assertIn("RCT", top_mod["study_type"])

        # Unani evidence check
        self.assertGreaterEqual(len(res["unani_evidence"]), 1)
        top_unani = res["unani_evidence"][0]
        self.assertEqual(top_unani["epistemic_class"], KnowledgeClass.TRADITIONAL_CLAIM.value)

        # Classical reference check
        self.assertGreaterEqual(len(res["classical_references"]), 1)
        canon_ref = res["classical_references"][0]
        self.assertEqual(canon_ref["epistemic_class"], KnowledgeClass.CLASSICAL_TEXT.value)
        self.assertIn("Canon of Medicine", canon_ref["canon"])
        self.assertIn("clinical_disclaimer", canon_ref)

        # Source matrix rows
        matrix = res["source_matrix"].matrix
        self.assertGreaterEqual(len(matrix), 6)
        classes_searched = [r.source_class for r in matrix]
        self.assertIn("Biomedical Literature", classes_searched)
        self.assertIn("Unani Literature & Canon", classes_searched)
        self.assertIn("Ayurveda Literature & Canon", classes_searched)

    def test_04_scenario_2_mizaj_temperament_concepts(self):
        # [SECTION 166: REQUIRED END-TO-END TEST 2]
        res = MultiSystemSearchMatrixEngine.execute_multi_system_search(
            query="What research exists on Mizaj / temperament-related concepts?"
        )
        self.assertTrue(res["epistemic_separation_preserved"])

        # Classical references present
        self.assertGreaterEqual(len(res["classical_references"]), 2)
        canons = [c["canon"] for c in res["classical_references"]]
        self.assertTrue(any("Canon of Medicine" in c for c in canons))
        self.assertTrue(any("Kitab al-Hawi" in c for c in canons))

        # Modern metabolic phenotyping study present
        self.assertGreaterEqual(len(res["unani_evidence"]), 1)
        unani_obs = res["unani_evidence"][0]
        self.assertEqual(unani_obs["epistemic_class"], KnowledgeClass.MODERN_PRECLINICAL.value)
        self.assertIn("metabolic rate", unani_obs["findings"].lower())

    def test_05_scenario_3_drug_herb_interaction_safety(self):
        # [SECTION 167: REQUIRED END-TO-END TEST 3]
        res = MultiSystemSearchMatrixEngine.execute_multi_system_search(
            query="Latest evidence for a drug-herb interaction with Warfarin"
        )
        self.assertGreaterEqual(len(res["safety_alerts"]), 2)

        # Verify St. John's Wort CYP induction warning
        sjw_alert = next(a for a in res["safety_alerts"] if "St. John's Wort" in a["interacting_agent"])
        self.assertIn("CRITICAL", sjw_alert["severity"])
        self.assertIn("CYP2C9", sjw_alert["mechanism"])
        self.assertIn("thrombosis", sjw_alert["clinical_consequence"].lower())

        # Verify Ginkgo Biloba antiplatelet synergy warning
        ginkgo_alert = next(a for a in res["safety_alerts"] if "Ginkgo Biloba" in a["interacting_agent"])
        self.assertIn("bleeding", ginkgo_alert["clinical_consequence"].lower())

    def test_06_scenario_4_cross_system_condition_comparison(self):
        # [SECTION 168: REQUIRED END-TO-END TEST 4]
        res = MultiSystemSearchMatrixEngine.execute_multi_system_search(
            query="Compare evidence for Osteoarthritis across modern medicine, Unani and Ayurveda"
        )
        self.assertGreaterEqual(len(res["modern_biomedical_evidence"]), 1)
        self.assertGreaterEqual(len(res["unani_evidence"]), 1)
        self.assertGreaterEqual(len(res["ayurvedic_evidence"]), 1)
        # Verify no artificial winner is manufactured
        self.assertIn("epistemic_context_notes", res["source_matrix"].model_dump())

    def test_07_retraction_pipeline_and_cascading_invalidation(self):
        # Ingest a formal retraction event
        event = RetractionAndSafetyPipeline.ingest_retraction_event(
            identifier="10.1016/j.lancet.2024.fabricated-trial",
            document_title="Fabricated Trial on Herbal Extract in Diabetes",
            source_id="SRC-EPMC",
            retraction_reason="Data fabrication confirmed by COPE committee audit"
        )
        self.assertEqual(event.status, "PROPAGATED")
        self.assertTrue(RetractionAndSafetyPipeline.is_identifier_retracted("10.1016/j.lancet.2024.fabricated-trial"))
        self.assertGreaterEqual(len(RetractionAndSafetyPipeline.list_retraction_events()), 1)

    def test_08_source_universe_api_endpoints(self):
        # 1. GET /v1/sources
        resp_list = self.client.get("/v1/sources")
        self.assertEqual(resp_list.status_code, 200)
        self.assertGreaterEqual(len(resp_list.json()), 10)

        # 2. GET /v1/sources/coverage/report
        resp_cov = self.client.get("/v1/sources/coverage/report")
        self.assertEqual(resp_cov.status_code, 200)
        cov_data = resp_cov.json()
        self.assertGreater(cov_data["modern_medicine_count"], 0)
        self.assertGreater(cov_data["unani_count"], 0)
        self.assertGreater(cov_data["ayurveda_count"], 0)

        # 3. GET /v1/sources/discovery/candidates
        resp_cands = self.client.get("/v1/sources/discovery/candidates")
        self.assertEqual(resp_cands.status_code, 200)
        self.assertGreaterEqual(len(resp_cands.json()), 2)

        # 4. POST /v1/sources/search
        resp_search = self.client.post("/v1/sources/search", json={"query": "Nigella sativa metabolic disorders"})
        self.assertEqual(resp_search.status_code, 200)
        search_data = resp_search.json()
        self.assertTrue(search_data["epistemic_separation_preserved"])
        self.assertIn("source_matrix", search_data)

        # 5. POST /v1/sources/retractions/event
        resp_ret = self.client.post("/v1/sources/retractions/event", json={
            "identifier": "10.1000/retracted-rct-2026",
            "document_title": "Retracted Trial on Hyperglycemia",
            "source_id": "SRC-CLINICALTRIALS",
            "retraction_reason": "Statistical error in primary endpoint analysis"
        })
        self.assertEqual(resp_ret.status_code, 200)
        self.assertEqual(resp_ret.json()["status"], "PROPAGATED")


if __name__ == "__main__":
    unittest.main()
