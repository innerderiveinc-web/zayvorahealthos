"""
Acceptance Test Suite for Prompt 14:
ZMIE Global Research Discovery Network & Continuous Knowledge Evolution Engine.
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.research.network_engine import ResearchNetworkEngine
from app.research.evolution_engine import ContinuousKnowledgeEvolutionEngine
from app.models.research_network import ProjectStatus


class TestResearchDiscoveryAcceptance(unittest.TestCase):
    """Rigorous acceptance tests for Prompt 14 research network & evolution layer."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.network = ResearchNetworkEngine()
        cls.evolution = ContinuousKnowledgeEvolutionEngine(network_engine=cls.network)

    def test_01_researcher_disambiguation_orcid_and_affiliation(self):
        """
        Verifies that researchers with identical names are not collapsed
        and disambiguate accurately based on ORCID and affiliation.
        """
        # Exact ORCID match for Oxford Professor
        res_oxford = self.network.disambiguate_researcher(
            name="Sarah Jenkins",
            orcid="0000-0002-1825-0097"
        )
        self.assertTrue(len(res_oxford) > 0)
        self.assertEqual(res_oxford[0][0].researcher_id, "res_jenkins_s")
        self.assertEqual(res_oxford[0][1], 1.0)
        self.assertIn("Exact ORCID match", res_oxford[0][2])

        # Name match with Harvard affiliation for Junior Fellow
        res_harvard = self.network.disambiguate_researcher(
            name="Sarah Jenkins",
            institution_name="Harvard Medical School"
        )
        self.assertTrue(len(res_harvard) > 0)
        self.assertEqual(res_harvard[0][0].researcher_id, "res_jenkins_s_junior")
        self.assertIn("Affiliation match", res_harvard[0][2])

        # Ensure two distinct records remain uncollapsed
        self.assertNotEqual(res_oxford[0][0].researcher_id, res_harvard[0][0].researcher_id)

    def test_02_canonical_study_clustering_and_deduplication(self):
        """
        Verifies that trial registration, preprint, and peer-reviewed publication
        cluster under one Canonical Study ID to prevent artificial evidence inflation.
        """
        canonical = self.network.resolve_canonical_study("NCT05221199")
        self.assertTrue(canonical["found"])
        self.assertEqual(canonical["canonical_study_id"], "study_dapa_energy_canonical")
        self.assertIn("NCT05221199", canonical["clinical_trials"])
        self.assertIn("prep_medrxiv_2023_8891", canonical["preprints"])
        self.assertIn("10.1056/NEJMoa2309811", canonical["peer_reviewed_dois"])
        self.assertEqual(canonical["evidence_weight_rule"], "COUNT_AS_ONE_CANONICAL_STUDY")
        self.assertGreaterEqual(canonical["suppressed_duplicate_count"], 2)

    def test_03_lifecycle_tracing_and_unobservable_boundary(self):
        """
        Verifies full lifecycle edge traversal and strict boundary gating
        preventing fabrication of private/unobservable research.
        """
        # Observable public lifecycle
        trace_public = self.network.get_lifecycle_trace("grant_ox_sglt2_2023")
        self.assertEqual(trace_public["boundary_status"], "OBSERVABLE_PUBLIC_RECORD")
        self.assertFalse(trace_public["is_private_unobservable"])
        self.assertGreaterEqual(trace_public["nodes_count"], 3)
        self.assertTrue(len(trace_public["edges"]) > 0)

        # Private confidential project boundary gating
        trace_private = self.network.get_lifecycle_trace("proj_secret_pharma_01")
        self.assertEqual(trace_private["boundary_status"], "PRIVATE_UNOBSERVABLE")
        self.assertTrue(trace_private["is_private_unobservable"])
        self.assertEqual(len(trace_private["edges"]), 0)
        self.assertIn("confidential", trace_private["message"].lower())

    def test_04_who_is_researching_multi_system(self):
        """
        Verifies multi-system query resolution for both modern cardiology
        and traditional Unani / Ayurveda medical science.
        """
        # Modern query
        modern_res = self.network.who_is_researching("SGLT2 heart failure")
        self.assertTrue(modern_res["total_matches"] > 0)
        top_modern = modern_res["top_researchers"][0]
        self.assertEqual(top_modern["researcher_id"], "res_jenkins_s")
        self.assertIn("modern", top_modern["traditional_systems"])

        # Traditional Unani query
        unani_res = self.network.who_is_researching("Khamira Abresham Unani")
        self.assertTrue(unani_res["total_matches"] > 0)
        top_unani = unani_res["top_researchers"][0]
        self.assertEqual(top_unani["researcher_id"], "res_aslam_siddiqui")
        self.assertIn("unani", top_unani["traditional_systems"])

    def test_05_where_is_research_happening(self):
        """
        Verifies institutional and geographical distribution queries.
        """
        distribution = self.network.where_is_research_happening("Unani")
        self.assertTrue(distribution["institutions_count"] >= 2)
        inst_names = [i["name"] for i in distribution["institutions"]]
        self.assertTrue(any("National Institute of Unani Medicine" in name for name in inst_names))

    def test_06_frontier_signals_velocity(self):
        """
        Verifies frontier emerging research signal tracking and velocity scores.
        """
        signals = self.network.get_frontier_signals()
        self.assertTrue(len(signals) >= 2)
        top_sig = max(signals, key=lambda s: s.frontier_velocity_score)
        self.assertGreater(top_sig.frontier_velocity_score, 80.0)
        self.assertIn(top_sig.status, ["EMERGING_FRONTIER", "ACCELERATING"])
        self.assertTrue(len(top_sig.key_breakthrough_compounds) > 0)

    def test_07_continuous_evolution_retraction_cascade(self):
        """
        Verifies cascade impact analysis when a study is retracted:
        dependent claims transition to RETRACTED and alerts are dispatched.
        """
        impact = self.evolution.trigger_cascade_impact(
            trigger_type="RETRACTION",
            trigger_source_id="10.1016/j.fakecardio.2021.09912",
            reason="Formal publisher retraction due to data fabrications."
        )
        self.assertEqual(impact.severity_level, "CRITICAL")
        self.assertIn("claim_fictitious_molecule_z", impact.affected_claim_ids)
        self.assertEqual(impact.new_claim_states["claim_fictitious_molecule_z"], "RETRACTED")
        self.assertTrue(len(impact.alerts_dispatched) > 0)
        self.assertEqual(impact.alerts_dispatched[0]["level"], "CRITICAL")

    def test_08_revalidation_queue_priority_ordering(self):
        """
        Verifies that revalidation queue processes higher priority jobs (CRITICAL/HIGH)
        ahead of lower priority jobs (LOW).
        """
        self.evolution.enqueue_revalidation("claim_low_01", "CLAIM", "LOW", "Minor typo in abstract")
        self.evolution.enqueue_revalidation("claim_crit_01", "CLAIM", "CRITICAL", "Sudden safety black box alert")
        self.evolution.enqueue_revalidation("claim_med_01", "CLAIM", "MEDIUM", "New observational preprint")

        result = self.evolution.process_revalidation_queue(max_items=2)
        self.assertEqual(result["processed_count"], 2)
        first_processed = result["processed_items"][0]
        self.assertEqual(first_processed["item_id"], "claim_crit_01")
        self.assertEqual(first_processed["priority"], "CRITICAL")

    def test_09_research_gaps_and_blindspots(self):
        """
        Verifies 'What Am I Missing?' engine identifies population exclusion
        and traditional system underinvestigation gaps.
        """
        gaps = self.evolution.analyze_research_gaps("HFpEF")
        self.assertTrue(len(gaps) > 0)
        gap = gaps[0]
        self.assertEqual(gap.gap_type, "POPULATION_EXCLUSION")
        self.assertGreater(gap.priority_score, 80.0)

        unani_gaps = self.evolution.analyze_research_gaps("Khamira")
        self.assertTrue(len(unani_gaps) > 0)
        self.assertEqual(unani_gaps[0].gap_type, "TRADITIONAL_SYSTEM_UNDERINVESTIGATED")

    def test_10_knowledge_snapshot_and_diff(self):
        """
        Verifies creation of knowledge snapshots and differential comparison.
        """
        snap = self.evolution.create_snapshot(notes="Post-retraction test snapshot")
        self.assertIsNotNone(snap.snapshot_id)
        self.assertGreater(snap.version, 2)

        snapshots = self.evolution.get_snapshots()
        self.assertGreaterEqual(len(snapshots), 3)

        diff = self.evolution.compute_snapshot_diff(snapshots[0].snapshot_id, snapshots[1].snapshot_id)
        self.assertIn("claims_growth", diff)
        self.assertIn("summary", diff)

    def test_11_rest_api_endpoints(self):
        """
        Verifies HTTP REST API endpoints mounted on FastAPI.
        """
        # 1. Researcher profile
        resp = self.client.get("/v1/research-network/researchers/res_jenkins_s")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["canonical_name"], "Prof. Sarah E. Jenkins")

        # 2. Disambiguate endpoint
        resp = self.client.post("/v1/research-network/researchers/disambiguate", json={
            "name": "Sarah Jenkins",
            "institution_name": "Harvard Medical School"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreaterEqual(data["candidates_count"], 1)

        # 3. Canonical study
        resp = self.client.get("/v1/research-network/canonical-study/NCT05221199")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["canonical_study_id"], "study_dapa_energy_canonical")

        # 4. Who is researching
        resp = self.client.get("/v1/research-network/who-is-researching?q=Cardiology")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["total_matches"] > 0)

        # 5. Frontier signals
        resp = self.client.get("/v1/research-network/frontier")
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.json()), 2)

        # 6. Gaps
        resp = self.client.get("/v1/research-network/gaps")
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.json()), 3)

        # 7. Cascade trigger API
        resp = self.client.post("/v1/research-network/evolution/cascade", json={
            "trigger_type": "GUIDELINE_CHANGE",
            "trigger_source_id": "ESC_2024_HF_GUIDELINES",
            "reason": "European Society of Cardiology updated HFpEF recommendations"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["trigger_type"], "GUIDELINE_CHANGE")


if __name__ == "__main__":
    unittest.main()
