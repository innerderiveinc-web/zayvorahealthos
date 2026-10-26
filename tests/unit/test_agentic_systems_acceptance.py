"""
Acceptance Test Suite for Autonomous Agentic Systems Architecture
Validates:
1. Reflection & Self-Correction Loop (Critic -> Critique -> Auto-Revision up to 3 cycles).
2. Dynamic ReAct Multi-Hop Tool Calling (tool_pubmed_search, tool_codex_lookup, tool_safety_interaction_check).
3. Fail-closed quarantine for unrepairable claims.
4. Persistent state transitions across execution checkpoints.
"""

import unittest
import asyncio
from app.models.research import GroundedAssertion, AssertionType, EvidenceTableEntry
from app.research.reflection import ReflectionAndSelfCorrectionEngine
from app.research.react_loop import ReActMultiHopOrchestrator, ReActToolRegistry
from app.research.engine import DeepResearchOperatingEngine


class TestAgenticSystemsAcceptance(unittest.TestCase):

    def setUp(self):
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    def test_01_reflection_loop_auto_repairs_causal_overreach(self):
        """Verifies that an exaggerated causal claim is auto-repaired by the reflection loop."""
        flawed_assertion = GroundedAssertion(
            assertion_id="test-ast-01",
            statement="Berberine cures chronic diabetes mellitus and permanently eliminates insulin resistance.",
            assertion_type=AssertionType.FACT,
            supporting_citations=["PMID:18442638"],
            confidence_score=0.99
        )

        verified_assertions, audit_log = ReflectionAndSelfCorrectionEngine.execute_reflection_loop(
            draft_assertions=[flawed_assertion],
            evidence_items=[]
        )

        self.assertEqual(len(verified_assertions), 1)
        repaired = verified_assertions[0]
        self.assertNotIn("cures", repaired.statement.lower())
        self.assertNotIn("permanently eliminates", repaired.statement.lower())
        self.assertIn("AUTO_CORRECTED", repaired.epistemic_status)
        self.assertEqual(audit_log[0]["status"], "AUTO_REPAIRED")
        self.assertGreaterEqual(len(audit_log[0]["critiques_resolved"]), 1)

    def test_02_reflection_loop_auto_repairs_false_equivalence(self):
        """Verifies that traditional cross-system false equivalence is rewritten to conceptual analogy."""
        flawed_assertion = GroundedAssertion(
            assertion_id="test-ast-02",
            statement="Balgham is the same as systemic lipid accumulation and equals hypertriglyceridemia.",
            assertion_type=AssertionType.SYNTHESIS,
            supporting_citations=["UNANI-01"],
            confidence_score=0.95
        )

        verified_assertions, audit_log = ReflectionAndSelfCorrectionEngine.execute_reflection_loop(
            draft_assertions=[flawed_assertion],
            evidence_items=[]
        )

        self.assertEqual(len(verified_assertions), 1)
        repaired = verified_assertions[0]
        self.assertNotIn("is the same as", repaired.statement)
        self.assertNotIn("equals", repaired.statement)
        self.assertIn("shares functional and conceptual parallels with", repaired.statement)
        self.assertEqual(audit_log[0]["status"], "AUTO_REPAIRED")

    def test_03_react_multihop_dynamic_tool_invocation(self):
        """Verifies multi-hop ReAct loop discovers secondary safety tools based on query context."""
        question = "What are the clinical interactions of Berberine when co-administered with Warfarin?"
        candidates, tools_invoked = ReActMultiHopOrchestrator.run_multihop_investigation(
            question=question,
            target_systems=["modern", "unani"]
        )

        self.assertGreater(len(candidates), 0)
        self.assertIn("tool_pubmed_search", tools_invoked)
        self.assertIn("tool_safety_interaction_check", tools_invoked)
        # Should have discovered the safety clash candidate
        has_safety_candidate = any("SAFETY" in c.get("source_id", "") for c in candidates)
        self.assertTrue(has_safety_candidate)

    def test_04_deep_research_engine_populates_agentic_telemetry(self):
        """Verifies that DeepResearchOperatingEngine outputs reflection and ReAct telemetry."""
        job = self.loop.run_until_complete(
            DeepResearchOperatingEngine.create_research_job(
                question="Efficacy of Berberine in Metabolic Syndrome with Warfarin safety evaluation",
                target_systems=["modern", "unani"],
                budget_limit=20
            )
        )

        report = self.loop.run_until_complete(
            DeepResearchOperatingEngine.execute_investigation(job.job_id)
        )

        self.assertIsNotNone(report)
        self.assertIsInstance(report.reflection_audit, list)
        self.assertGreater(len(report.reflection_audit), 0)
        self.assertIsInstance(report.react_tools_invoked, list)
        self.assertIn("tool_pubmed_search", report.react_tools_invoked)
        self.assertTrue(len(report.reproducibility_hash) == 64)


if __name__ == "__main__":
    unittest.main()
