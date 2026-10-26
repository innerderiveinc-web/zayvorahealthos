"""
ZMIE Search & Retrieval Intelligence Acceptance Suite
Validates Section 116 Real-Data Acceptance Criteria:
- Test A: "What is IBS?" (Concept, guidelines, symptoms)
- Test B: "Human evidence for berberine in metabolic health" (E6 clinical prioritization)
- Test C: "Safety concerns of berberine" (Safety retrieval, CYP3A4, contraindications)
- Test D: "Compare Unani Zoaf-e-Meda with biomedical dyspepsia" (Comparative lens & non-equivalence)
- Test E: "What changed in evidence since 2022?" (Temporal filtering)
- Test F: "Show contradictory evidence for berberine" (Disagreement decomposition)
Plus Adversarial Tests:
- False Premise Neutralizer
- Ambiguous Abbreviation Disambiguation ("MS")
- Retracted Article Hard Quarantine
- Search Snapshot & "What Changed?" Diff
"""

import sys
import unittest
import asyncio
from datetime import datetime

from app.search.query_engine import QueryUnderstandingEngine, QueryIntent
from app.search.search_modes import SearchModeOrchestrator
from app.search.state_manager import SearchStateManager
from app.models.graph import EvidenceLadder
from app.models.claim import MedicalSystem


class TestSearchAcceptance(unittest.TestCase):

    def setUp(self):
        self.orchestrator = SearchModeOrchestrator()
        self.state_mgr = SearchStateManager()

    def test_01_test_a_what_is_ibs(self):
        """Test A (Sec 116): 'What is IBS?' returns canonical concept, Rome IV guidelines & symptoms."""
        res = asyncio.run(self.orchestrator.execute("What is IBS?", mode="quick"))
        self.assertGreater(res.total_results, 0)
        self.assertIn(QueryIntent.DEFINITION, res.structured_query.intents)
        self.assertIn("Irritable Bowel Syndrome", res.structured_query.entities)

        # Check that top result is Rome IV Guidelines or IBS Concept
        top_res = res.ranked_results[0]
        self.assertTrue(
            "Rome IV" in top_res.candidate.title or "Irritable Bowel" in top_res.candidate.title
        )
        self.assertEqual(top_res.candidate.authority_tier, "tier_a_official")

    def test_02_test_b_human_evidence_prioritization(self):
        """Test B (Sec 116): Prioritizes controlled human clinical evidence (E6) over weaker studies."""
        res = asyncio.run(self.orchestrator.execute("What is the human evidence for berberine in metabolic health?", mode="evidence"))
        self.assertGreater(res.total_results, 0)
        top_res = res.ranked_results[0]

        # Top result must be double-blind human RCT (PMID:18442638)
        self.assertEqual(top_res.candidate.document_id, "PMID:18442638")
        self.assertEqual(top_res.candidate.evidence_level, EvidenceLadder.E6_CONTROLLED_CLINICAL.value)
        self.assertEqual(top_res.candidate.study_type, "double_blind_rct")
        self.assertIn("High-quality controlled clinical evidence", top_res.why_this_result)

    def test_03_test_c_safety_retrieval_and_cyp3a4(self):
        """Test C (Sec 116): Activates safety retrieval and identifies CYP3A4 inhibition & pregnancy warnings."""
        res = asyncio.run(self.orchestrator.execute("What are the safety concerns and interactions of berberine?", mode="safety"))
        self.assertGreater(res.total_results, 0)

        # Verify CYP3A4 study is elevated
        cyp_docs = [r for r in res.ranked_results if "cyp3a4" in r.candidate.title.lower()]
        self.assertGreater(len(cyp_docs), 0)
        self.assertEqual(cyp_docs[0].candidate.document_id, "PMID:22105432")

        # Verify safety packet contains warnings
        safety_summary = res.mode_specific_payload.get("safety_summary", {})
        self.assertIn("cyp_interactions", safety_summary)
        self.assertIn("CONTRAINDICATED in pregnancy/lactation", safety_summary.get("pregnancy_category", ""))

    def test_04_test_d_cross_system_comparison(self):
        """Test D (Sec 116): Compare Unani Zoaf-e-Meda with biomedical functional dyspepsia, preserving non-equivalence."""
        res = asyncio.run(self.orchestrator.execute("Compare Unani Zoaf-e-Meda and biomedical dyspepsia", mode="compare"))
        comp_lens = res.mode_specific_payload.get("comparative_lens", {})
        self.assertEqual(comp_lens.get("concordance_level"), "FUNCTIONAL_ANALOGY")
        self.assertIn("SAFEGUARD", comp_lens.get("safeguard_notice", ""))
        self.assertIn("unani_tibb", comp_lens.get("system_perspectives", {}))
        self.assertIn("modern_biomedicine", comp_lens.get("system_perspectives", {}))

    def test_05_test_e_temporal_filtering_since_2022(self):
        """Test E (Sec 116): 'What changed in the evidence since 2022?' enforces temporal window."""
        res = asyncio.run(self.orchestrator.execute("What changed in the evidence for berberine since 2022?", mode="evidence"))
        self.assertEqual(res.structured_query.date_range.get("since_year"), 2022)

        # All returned candidates must be >= 2022
        for r in res.ranked_results:
            self.assertGreaterEqual(r.candidate.publication_year, 2022)

    def test_06_test_f_contradictory_evidence_decomposition(self):
        """Test F (Sec 116): Surfaces conflicting studies and decomposes reasons for disagreement."""
        res = asyncio.run(self.orchestrator.execute("Show contradictory evidence for berberine in metabolic health", mode="evidence"))
        rag = res.rag_packet
        self.assertGreater(len(rag.supporting_evidence), 0)
        self.assertGreater(len(rag.contradicting_evidence), 0)

        # Check disagreement decomposition
        contra_item = rag.contradicting_evidence[0]
        self.assertIn("disagreement_factor", contra_item)
        self.assertIn("Dose", contra_item["disagreement_factor"])

    def test_07_false_premise_neutralizer(self):
        """Adversarial Test: 'What evidence proves X cures Y?' is neutralized to neutral empirical inquiry."""
        q_engine = QueryUnderstandingEngine()
        sq = q_engine.parse_query("What evidence proves that berberine cures diabetes?")
        self.assertTrue(sq.is_false_premise)
        self.assertEqual(sq.normalized_neutral_query, "What evidence exists regarding berberine and diabetes?")
        self.assertIn("False premise neutralized", sq.false_premise_note)

    def test_08_ambiguous_abbreviation_detection(self):
        """Adversarial Test: Ambiguous medical acronyms without context marked AMBIGUOUS."""
        q_engine = QueryUnderstandingEngine()
        sq = q_engine.parse_query("What is the protocol for MS?")
        self.assertEqual(sq.disambiguation_status, "AMBIGUOUS")
        self.assertIn("Multiple Sclerosis (Neurology)", sq.disambiguation_candidates)
        self.assertIn("Morphine Sulfate (Pharmacology)", sq.disambiguation_candidates)

    def test_09_retracted_article_quarantine(self):
        """Security Test: Fabricated retracted article PMID:99999999 strictly quarantined from evidence results."""
        res = asyncio.run(self.orchestrator.execute("What is the clinical evidence for berberine?", mode="evidence"))
        retracted_matches = [r for r in res.ranked_results if r.candidate.document_id == "PMID:99999999"]
        self.assertEqual(len(retracted_matches), 0) # Quarantined

    def test_10_search_snapshot_and_diff(self):
        """Snapshot & Diff Test: Freezes search state and computes diff between two snapshots."""
        res_a = asyncio.run(self.orchestrator.execute("Berberine metabolic health", mode="quick"))
        snap_a = self.state_mgr.create_snapshot(res_a)
        self.assertIsNotNone(snap_a.snapshot_id)

        # Create simulated later snapshot with additional document
        res_b = asyncio.run(self.orchestrator.execute("Berberine metabolic health", mode="quick"))
        snap_b = self.state_mgr.create_snapshot(res_b)
        snap_b.result_document_ids.append("PMID:39999999") # New study

        diff = self.state_mgr.diff_snapshots(snap_a.snapshot_id, snap_b.snapshot_id)
        self.assertIn("PMID:39999999", diff["new_studies_indexed"])


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSearchAcceptance)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
