"""
Acceptance Test Suite for ZMIE Prompt 22:
Global Scientific Collaboration & Research Network Engine.

Validates:
1. Identity Resolution & Disambiguation (Authoritative ORCID, Probabilistic heuristic, Ambiguity Contestation)
2. Temporal Affiliation Chronology (Primary/Visiting, Date boundaries, Provenance)
3. Multi-Dimensional Evidence-Backed Expertise Profiling & Anti-Ranking Firewall
4. Collaboration Topology, 1st & 2nd Degree Separation, and Recency Decay
5. Cross-Disciplinary Bridge Detection (Biomedicine + Traditional Systems)
6. Research Cluster & Community Discovery
7. Epistemic Research Gap Mapping (Strict 'SPARSE_IN_INDEXED_SOURCES' Boundary)
8. Network Snapshotting & Diff Tracking
9. Multi-Tenant Isolation & Privacy Firewall
10. FastAPI Endpoints via TestClient
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.models.collaboration_network import (
    IdentityConfidenceState,
    AffiliationStatus,
    CollaborationType,
    RelationshipState,
    ExpertiseDimension,
    GapStatus,
    VisibilityScope,
    TemporalAffiliation,
    ExpertiseEvidenceItem,
    ResearcherIdentity,
    CollaborationEdge,
    ResearcherResolveRequest,
    ExpertiseSearchQuery,
)
from app.collaboration_network.engine import (
    ScientificCollaborationNetworkEngine,
    ForbiddenRankingException,
)


class TestCollaborationNetworkAcceptance(unittest.TestCase):

    def setUp(self):
        self.engine = ScientificCollaborationNetworkEngine()
        self.client = TestClient(app)

    # -------------------------------------------------------------------------
    # 1. Identity Resolution & Disambiguation
    # -------------------------------------------------------------------------

    def test_orcid_exact_disambiguation(self):
        """Authoritative ORCID resolves directly to the confirmed profile."""
        req = ResearcherResolveRequest(
            raw_name="M. Rahman",
            orcid="0000-0002-1234-5678"
        )
        res = self.engine.resolve_researcher_identity(req)
        self.assertTrue(res["resolved"])
        self.assertEqual(res["match_type"], "ORCID_EXACT")
        self.assertEqual(res["researcher"].canonical_name, "Hakim M. A. Rahman")
        self.assertEqual(res["confidence"], IdentityConfidenceState.CONFIRMED)

    def test_heuristic_probabilistic_resolution(self):
        """Probabilistic resolution matches alias + institutional affiliation hint."""
        req = ResearcherResolveRequest(
            raw_name="Elena Vance",
            institution_hint="Broad Institute",
            topic_hints=["AMPK Pathway", "Metabolism"]
        )
        res = self.engine.resolve_researcher_identity(req)
        self.assertTrue(res["resolved"])
        self.assertEqual(res["researcher"].researcher_id, "res-vance-02")
        self.assertIn("res-vance-02", res["researcher"].researcher_id)
        self.assertGreaterEqual(res["score"], 0.7)

    def test_ambiguity_contestation_refuses_false_merge(self):
        """When multiple researchers share names without distinguishing ORCID, flag CONTESTED."""
        # Seed another researcher with same raw name at a different institution
        duplicate_r = ResearcherIdentity(
            researcher_id="res-rahman-02",
            canonical_name="Dr. M. A. Rahman",
            aliases=["M. A. Rahman"],
            disambiguation_confidence=IdentityConfidenceState.SUPPORTED,
            affiliations=[
                TemporalAffiliation(
                    institution_id="inst-oxford-01",
                    institution_name="University of Oxford",
                    role="Research Fellow",
                    affiliation_status=AffiliationStatus.PRIMARY,
                    start_year=2019,
                    end_year=None,
                    is_current=True
                )
            ]
        )
        self.engine.researchers[duplicate_r.researcher_id] = duplicate_r

        # Query with generic name and no ORCID or distinguishing hint
        req = ResearcherResolveRequest(raw_name="M. A. Rahman")
        res = self.engine.resolve_researcher_identity(req)
        self.assertFalse(res["resolved"])
        self.assertEqual(res["confidence"], IdentityConfidenceState.CONTESTED)
        self.assertEqual(res["match_type"], "AMBIGUOUS_CONTESTED")

    def test_new_candidate_creation_for_unindexed_researcher(self):
        """Unindexed researcher is created as a provisional CANDIDATE without false matches."""
        req = ResearcherResolveRequest(
            raw_name="Dr. Tariq Al-Balkhi",
            institution_hint="Tehran University of Medical Sciences",
            topic_hints=["Avicennian Cardiology"]
        )
        res = self.engine.resolve_researcher_identity(req)
        self.assertFalse(res["resolved"])
        self.assertEqual(res["confidence"], IdentityConfidenceState.CANDIDATE)
        self.assertEqual(res["researcher"].canonical_name, "Dr. Tariq Al-Balkhi")
        self.assertEqual(len(res["researcher"].affiliations), 1)

    # -------------------------------------------------------------------------
    # 2. Temporal Affiliation Chronology
    # -------------------------------------------------------------------------

    def test_researcher_timeline_and_boundaries(self):
        """Timeline tracks chronological history and enforces non-endorsement boundary."""
        timeline = self.engine.get_researcher_timeline("res-rahman-01")
        self.assertEqual(timeline["canonical_name"], "Hakim M. A. Rahman")
        self.assertEqual(len(timeline["chronological_affiliations"]), 2)

        # Primary current vs Visiting past
        primary = next(a for a in timeline["chronological_affiliations"] if a["status"] == "PRIMARY")
        self.assertTrue(primary["is_current"])
        self.assertEqual(primary["start_year"], 2015)

        visiting = next(a for a in timeline["chronological_affiliations"] if a["status"] == "VISITING")
        self.assertFalse(visiting["is_current"])
        self.assertEqual(visiting["start_year"], 2021)
        self.assertEqual(visiting["end_year"], 2024)

        # Epistemic boundary reminder present
        self.assertIn("Epistemic boundary", timeline["boundary_reminder"])

    # -------------------------------------------------------------------------
    # 3. Evidence-Backed Expertise Profiling & Anti-Ranking Firewall
    # -------------------------------------------------------------------------

    def test_evidence_backed_expertise_search(self):
        """Expertise search returns verified evidence outputs and active years."""
        query = ExpertiseSearchQuery(topic="Diabetes", min_evidence_count=1)
        res = self.engine.search_expertise(query)
        self.assertGreaterEqual(res["matched_researcher_count"], 1)

        researcher_entry = res["researchers"][0]
        self.assertIn("matched_evidence_count", researcher_entry)
        self.assertGreater(researcher_entry["matched_evidence_count"], 0)
        self.assertIn("active_years_window", researcher_entry)
        self.assertIn("anti_ranking_guarantee", res)

    def test_anti_ranking_firewall_blocks_forbidden_terms(self):
        """Firewall strictly rejects subjective ranking claims."""
        forbidden_phrases = [
            "Hakim Rahman is the Top Scientist in diabetes",
            "Rated as the Best Researcher in Asia",
            "Recognized as the #1 Expert in herbal chemistry",
            "Leading authority in the world on metabolomics"
        ]
        for phrase in forbidden_phrases:
            with self.assertRaises(ForbiddenRankingException):
                self.engine.verify_no_subjective_ranking(phrase)

    # -------------------------------------------------------------------------
    # 4. Collaboration Topology & Recency Decay
    # -------------------------------------------------------------------------

    def test_collaboration_topology_and_decay(self):
        """Calculates direct collaborators, recency decay weights, and 2nd degree connections."""
        collabs = self.engine.get_collaborations("res-rahman-01")
        self.assertEqual(collabs["focus_researcher_id"], "res-rahman-01")
        self.assertEqual(collabs["direct_collaborators_count"], 2)

        # Direct collaborators include Sharma and Vance
        direct_names = [c["canonical_name"] for c in collabs["direct_collaborators"]]
        self.assertIn("Prof. S. K. Sharma", direct_names)
        self.assertIn("Dr. Elena Vance", direct_names)

        # Recency weights are valid floats <= 1.0
        for c in collabs["direct_collaborators"]:
            self.assertGreater(c["recency_weight"], 0.0)
            self.assertLessEqual(c["recency_weight"], 1.0)
            self.assertTrue(len(c["evidence_artifacts"]) > 0)

        # Second degree network from Vance's perspective
        vance_collabs = self.engine.get_collaborations("res-vance-02")
        self.assertEqual(vance_collabs["direct_collaborators_count"], 1)  # Direct to Rahman
        self.assertEqual(vance_collabs["second_degree_network_count"], 1)  # Sharma via Rahman
        self.assertEqual(vance_collabs["second_degree_network"][0]["canonical_name"], "Prof. S. K. Sharma")

    # -------------------------------------------------------------------------
    # 5. Cross-Disciplinary Bridge Detection
    # -------------------------------------------------------------------------

    def test_cross_disciplinary_bridge_detection(self):
        """Detects researchers actively bridging multiple paradigms (e.g. Unani + Phytochemistry + Pharmacology)."""
        bridges = self.engine.detect_cross_disciplinary_bridges()
        self.assertGreaterEqual(len(bridges), 1)

        rahman_bridge = next((b for b in bridges if b.researcher_id == "res-rahman-01"), None)
        self.assertIsNotNone(rahman_bridge)
        self.assertIn("Unani Medicine", rahman_bridge.bridged_disciplines)
        self.assertIn("Phytochemistry", rahman_bridge.bridged_disciplines)
        self.assertIn("Metabolic Pharmacology", rahman_bridge.bridged_disciplines)
        self.assertGreaterEqual(rahman_bridge.bridging_evidence_count, 2)

    # -------------------------------------------------------------------------
    # 6. Research Clusters & Communities
    # -------------------------------------------------------------------------

    def test_research_cluster_discovery(self):
        """Identifies dense collaborative clusters across traditional and modern domains."""
        clusters = self.engine.discover_clusters()
        self.assertGreaterEqual(len(clusters), 1)

        c = clusters[0]
        self.assertIn("Polyherbal Metabolic Regulation", c.label)
        self.assertIn("Unani Medicine", c.disciplines)
        self.assertIn("Endocrinology", c.disciplines)
        self.assertGreater(len(c.member_researcher_ids), 1)
        self.assertGreater(len(c.member_institution_ids), 1)
        self.assertGreater(c.cohesion_score, 0.5)

    # -------------------------------------------------------------------------
    # 7. Epistemic Research Gap Mapping
    # -------------------------------------------------------------------------

    def test_epistemic_gap_reporting(self):
        """Identifies sparse or unindexed research topics without asserting nonexistence."""
        # Unindexed topic
        unindexed_report = self.engine.evaluate_research_gap("Tibbi Nanoparticles for Glioblastoma")
        self.assertEqual(unindexed_report.status, GapStatus.SPARSE_IN_INDEXED_SOURCES)
        self.assertEqual(unindexed_report.observed_publication_count, 0)
        self.assertIn("Non-negotiable epistemic boundary", unindexed_report.epistemic_disclaimer)
        self.assertGreater(len(unindexed_report.recommended_inquiry_path), 0)

        # Well-represented topic
        represented_report = self.engine.evaluate_research_gap("Diabetes")
        self.assertIn(represented_report.status, [GapStatus.WELL_REPRESENTED, GapStatus.EMERGING])
        self.assertGreater(represented_report.observed_publication_count, 0)

    # -------------------------------------------------------------------------
    # 8. Network Snapshotting & Diff Tracking
    # -------------------------------------------------------------------------

    def test_network_snapshots_and_diff(self):
        """Captures network state at T1, adds nodes/edges at T2, and verifies diff accuracy."""
        # T1 snapshot
        snap1 = self.engine.capture_snapshot("Baseline-2024")
        self.assertEqual(snap1.label, "Baseline-2024")
        self.assertEqual(snap1.total_researchers, 3)
        self.assertEqual(snap1.total_collaboration_edges, 2)

        # Add new researcher and new collaboration edge at T2
        new_researcher = ResearcherIdentity(
            researcher_id="res-tariq-04",
            canonical_name="Dr. Tariq Al-Balkhi",
            primary_disciplines=["Integrative Cardiology"]
        )
        self.engine.researchers[new_researcher.researcher_id] = new_researcher

        new_edge = CollaborationEdge(
            edge_id="collab-rahman-tariq-03",
            source_researcher_id="res-rahman-01",
            target_researcher_id=new_researcher.researcher_id,
            relationship_type=CollaborationType.COAUTHORED,
            first_year=2025,
            last_year=2025
        )
        self.engine.edges[new_edge.edge_id] = new_edge

        # T2 snapshot
        snap2 = self.engine.capture_snapshot("Evolution-2025")
        self.assertEqual(snap2.total_researchers, 4)
        self.assertEqual(snap2.total_collaboration_edges, 3)

        # Compute diff
        diff = self.engine.diff_snapshots(snap1.snapshot_id, snap2.snapshot_id)
        self.assertIn("res-tariq-04", diff.new_researchers)
        self.assertIn("collab-rahman-tariq-03", diff.new_edges)

    # -------------------------------------------------------------------------
    # 9. Multi-Tenant Isolation & Privacy Firewall
    # -------------------------------------------------------------------------

    def test_tenant_isolation_firewall(self):
        """Private researcher identities and edges are inaccessible across tenants or publicly."""
        # Add private tenant researcher
        private_res = ResearcherIdentity(
            researcher_id="res-pharma-classified-01",
            canonical_name="Dr. Secret Investigator",
            visibility=VisibilityScope.TENANT_PRIVATE,
            tenant_id="tenant-pharma-corp"
        )
        self.engine.researchers[private_res.researcher_id] = private_res

        # Public query: cannot find private researcher
        self.assertIsNone(self.engine.get_researcher("res-pharma-classified-01", tenant_id=None))

        # Different tenant query: cannot find private researcher
        self.assertIsNone(self.engine.get_researcher("res-pharma-classified-01", tenant_id="tenant-other-hospital"))

        # Authorized tenant query: successfully retrieves profile
        auth_res = self.engine.get_researcher("res-pharma-classified-01", tenant_id="tenant-pharma-corp")
        self.assertIsNotNone(auth_res)
        self.assertEqual(auth_res.canonical_name, "Dr. Secret Investigator")

    # -------------------------------------------------------------------------
    # 10. FastAPI Endpoints via TestClient
    # -------------------------------------------------------------------------

    def test_api_resolve_researcher(self):
        """POST /v1/network/researchers/resolve"""
        payload = {"raw_name": "Hakim M. A. Rahman", "orcid": "0000-0002-1234-5678"}
        resp = self.client.post("/v1/network/researchers/resolve", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["resolved"])
        self.assertEqual(data["match_type"], "ORCID_EXACT")

    def test_api_get_researcher_profile_and_timeline(self):
        """GET /v1/network/researchers/{id} & GET /v1/network/researchers/{id}/timeline"""
        resp = self.client.get("/v1/network/researchers/res-rahman-01")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["canonical_name"], "Hakim M. A. Rahman")

        timeline_resp = self.client.get("/v1/network/researchers/res-rahman-01/timeline")
        self.assertEqual(timeline_resp.status_code, 200)
        self.assertGreaterEqual(len(timeline_resp.json()["chronological_affiliations"]), 2)

    def test_api_get_collaborations(self):
        """GET /v1/network/researchers/{id}/collaborations"""
        resp = self.client.get("/v1/network/researchers/res-rahman-01/collaborations")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["direct_collaborators_count"], 2)

    def test_api_institution_profile(self):
        """GET /v1/network/institutions/{id}"""
        resp = self.client.get("/v1/network/institutions/inst-hamdard-01")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["institution_id"], "inst-hamdard-01")

    def test_api_search_expertise(self):
        """POST /v1/network/expertise/search"""
        payload = {"topic": "Diabetes", "min_evidence_count": 1}
        resp = self.client.post("/v1/network/expertise/search", json=payload)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(resp.json()["matched_researcher_count"], 0)

    def test_api_bridges_and_clusters(self):
        """GET /v1/network/bridges/cross-disciplinary & GET /v1/network/clusters"""
        b_resp = self.client.get("/v1/network/bridges/cross-disciplinary")
        self.assertEqual(b_resp.status_code, 200)
        self.assertGreaterEqual(len(b_resp.json()), 1)

        c_resp = self.client.get("/v1/network/clusters")
        self.assertEqual(c_resp.status_code, 200)
        self.assertGreaterEqual(len(c_resp.json()), 1)

    def test_api_gaps(self):
        """GET /v1/network/gaps"""
        resp = self.client.get("/v1/network/gaps?topic=Ayurvedic+Quantum+Epigenetics")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "SPARSE_IN_INDEXED_SOURCES")

    def test_api_snapshot_and_diff(self):
        """POST /v1/network/snapshot & GET /v1/network/diff"""
        snap1_resp = self.client.post("/v1/network/snapshot", json={"label": "T1"})
        self.assertEqual(snap1_resp.status_code, 200)
        s1_id = snap1_resp.json()["snapshot_id"]

        snap2_resp = self.client.post("/v1/network/snapshot", json={"label": "T2"})
        self.assertEqual(snap2_resp.status_code, 200)
        s2_id = snap2_resp.json()["snapshot_id"]

        diff_resp = self.client.get(f"/v1/network/diff?from_snapshot_id={s1_id}&to_snapshot_id={s2_id}")
        self.assertEqual(diff_resp.status_code, 200)
        self.assertEqual(diff_resp.json()["from_snapshot_id"], s1_id)


if __name__ == "__main__":
    unittest.main()
