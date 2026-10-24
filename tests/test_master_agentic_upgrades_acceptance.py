"""
Acceptance Test Suite for ZMIE Master Agentic Upgrades:
- Adversarial Debate Engine (Advocate vs Skeptic)
- Qarabadeen Polyherbal Formulations & Interaction Decomposition
- Cryptographic Clinical Dossier & FHIR EvidenceReport Export
- ReAct Autonomous Polyherbal Tool Invocation
"""

import unittest
import asyncio
from typing import List, Dict, Any

from app.models.research import GroundedAssertion, AssertionType, EvidenceTableEntry, PICOFramework
from app.research.debate import AdversarialDebateEngine, DebateVerdict
from app.sources.qarabadeen_engine import get_qarabadeen_engine
from app.research.dossier_export import ClinicalDossierExporter
from app.research.engine import DeepResearchOperatingEngine
from app.research.react_loop import ReActMultiHopOrchestrator


class TestMasterAgenticUpgrades(unittest.TestCase):

    def setUp(self):
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    def test_01_adversarial_debate_engine_execution(self):
        """Verifies Advocate, Skeptic, and Arbiter roles in clinical debate."""
        assertions = [
            GroundedAssertion(
                assertion_id="ast-1",
                statement="Berberine administration is associated with significant reductions in fasting plasma glucose.",
                assertion_type=AssertionType.FACT,
                supporting_evidence_ids=["ev-1"],
                supporting_citations=["PMID:23112345"]
            )
        ]
        evidence = [
            EvidenceTableEntry(
                evidence_id="ev-1",
                source_id="PMID:23112345",
                document_id="doc-101",
                study_title="Randomized controlled trial of berberine in type 2 diabetes",
                study_design="Double-blind RCT",
                evidence_grade="E2_CONTROLLED_TRIAL",
                population="Adult T2D patients (N=60)",
                intervention="Berberine hydrochloride 500mg TID",
                sample_size=60,  # modest sample size to test skeptic bias flag
                primary_findings="Mean HbA1c reduced by 0.72% vs placebo (p<0.01).",
                effect_size_or_stats="HbA1c -0.72%",
                doi_or_anchor="10.1016/j.metabol.2025.101"
            )
        ]

        verdict: DebateVerdict = AdversarialDebateEngine.conduct_debate(
            topic="Berberine in Type 2 Diabetes Glycemic Control",
            assertions=assertions,
            evidence_table=evidence,
            contradictions=[]
        )

        self.assertIsInstance(verdict, DebateVerdict)
        self.assertGreater(len(verdict.advocate_arguments), 0)
        self.assertGreater(len(verdict.skeptic_arguments), 0)
        # Check Advocate argument
        advocate = verdict.advocate_arguments[0]
        self.assertEqual(advocate.agent_role, "ADVOCATE")
        self.assertIn("PMID:23112345", advocate.evidence_citations[0])

        # Check Skeptic argument (caught small sample size N=60)
        skeptic_claims = [a.claim for a in verdict.skeptic_arguments]
        self.assertTrue(any("power limitation" in c.lower() or "bias" in c.lower() for c in skeptic_claims))

        # Check Arbiter consensus
        self.assertIn(verdict.grade_certainty, ["HIGH", "MODERATE", "LOW", "VERY_LOW"])
        self.assertIn(verdict.recommended_clinical_posture, ["ENDORSED_MONITORED", "CAUTIONARY", "INSUFFICIENT_DATA"])
        self.assertTrue(len(verdict.consensus_synthesis) > 20)

    def test_02_qarabadeen_polyherbal_engine(self):
        """Verifies compound formulation search, ingredient decomposition, and safety screening."""
        engine = get_qarabadeen_engine()
        all_keys = engine.list_all_keys()
        self.assertGreaterEqual(len(all_keys), 50)

        # Search for Majun Dabeed-ul-Ward
        results = engine.search_formulations("dabeed")
        self.assertGreater(len(results), 0)
        form = results[0]
        self.assertEqual(form["compound_key"], "majun_dabeed_ul_ward")
        self.assertIn("key_ingredients", form)
        self.assertGreaterEqual(len(form["key_ingredients"]), 5)

        # Ingredient decomposition
        botanicals = engine.extract_constituent_botanicals("majun_dabeed_ul_ward")
        self.assertGreater(len(botanicals), 0)

        # Safety screening against Warfarin
        safety_screen = engine.screen_compound_safety(
            compound_key="majun_dabeed_ul_ward",
            modern_drugs=["Warfarin"]
        )
        self.assertTrue(safety_screen["found"])
        self.assertEqual(safety_screen["compound_key"], "majun_dabeed_ul_ward")
        self.assertIn("interactions", safety_screen)
        self.assertIn("total_constituents_evaluated", safety_screen)

    def test_03_react_polyherbal_tool_invocation(self):
        """Verifies ReAct orchestrator invokes compound lookup tool on polyherbal queries."""
        query = "Evaluate Majun Dabeed-ul-Ward formulation and interactions"
        candidates, tools = ReActMultiHopOrchestrator.run_multihop_investigation(
            question=query,
            target_systems=["unani", "modern"],
            max_hops=3
        )
        self.assertIn("tool_compound_formulation_lookup", tools)
        self.assertTrue(any("QARABADEEN" in c["source_id"] for c in candidates))

    def test_04_clinical_dossier_export(self):
        """Verifies cryptographic clinical markdown and FHIR EvidenceReport export."""
        report = self.loop.run_until_complete(
            DeepResearchOperatingEngine.execute_investigation(
                job_id=(self.loop.run_until_complete(
                    DeepResearchOperatingEngine.create_research_job("Berberine and Metformin Synergy")
                )).job_id
            )
        )

        # 1. Export Markdown with HMAC
        md = ClinicalDossierExporter.export_clinical_markdown(report)
        self.assertIn("# ZMIE Clinical Evidence Dossier", md)
        self.assertIn("Cryptographic Signature (HMAC SHA-256)", md)
        self.assertIn("Adversarial Clinical Debate & Consensus", md)
        self.assertIn("PICO Evidence Table", md)

        # 2. Export FHIR EvidenceReport
        fhir = ClinicalDossierExporter.export_fhir_evidence_report(report)
        self.assertEqual(fhir["resourceType"], "EvidenceReport")
        self.assertEqual(fhir["id"], report.report_id)
        self.assertIn("publisher", fhir)
        self.assertEqual(len(fhir["section"]), 2)

        # Verify signature computation
        sig = ClinicalDossierExporter.compute_dossier_signature(
            report.report_id, report.job_id, "2026-10-24T12:00:00Z", report.primary_question
        )
        self.assertEqual(len(sig), 64)  # SHA-256 hex length


if __name__ == "__main__":
    unittest.main()
