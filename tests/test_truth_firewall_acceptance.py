"""
Acceptance Test Suite for ZMIE Truth, Claim Validation & Safety Firewall Layer (Prompt 7)
Validates:
1. Atomic claim splitting and classification.
2. Citation verification & Zero Citation Laundering (fabricated DOIs / topic mentions).
3. Numerical and percentage precision checks.
4. Causality firewall (blocking or rewriting causal overreach: association != causation).
5. Cross-system equivalence firewall (Unani Mizaj != biochemical entities).
6. Hard retraction blocking and retraction propagation impact analysis.
7. End-to-end Truth & Safety Firewall orchestrator and REST API validation.
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.models.truth_firewall import (
    ClaimType,
    ClaimStatus,
    SupportLevel,
    ClaimRiskLevel,
    FirewallVerdict,
    Citation
)
from app.firewall.claim_engine import AtomicClaimEngine
from app.firewall.citation_engine import CitationVerificationEngine
from app.firewall.causality_firewall import CausalityAndLanguageFirewall
from app.firewall.orchestrator import TruthAndSafetyFirewall


class TestTruthFirewallAcceptance(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_01_atomic_claim_splitting_and_classification(self):
        """Validates sentence splitting into atomic claims and typing."""
        text = "Berberine reduced fasting glucose by 20% in diabetic adults; whereas severe GI distress was observed in pregnant patients."
        claims = AtomicClaimEngine.split_into_atomic_claims(text)
        self.assertGreaterEqual(len(claims), 2)

        type1 = AtomicClaimEngine.classify_claim_type(claims[0])
        self.assertEqual(type1, ClaimType.NUMERICAL)

        type2 = AtomicClaimEngine.classify_claim_type(claims[1])
        self.assertEqual(type2, ClaimType.SAFETY)

        risk2 = AtomicClaimEngine.classify_risk_level(claims[1], type2)
        self.assertEqual(risk2, ClaimRiskLevel.CRITICAL_RISK)

    def test_02_citation_entailment_and_numerical_precision(self):
        """Verifies exact passage support and numerical consistency."""
        valid_cit = Citation(
            source_id="SRC-101",
            document_id="DOC-101",
            title="Randomized trial of berberine",
            identifier="PMID:18442638"
        )
        claim_match = "Berberine lowered HbA1c by 1.8% in adult cohorts with type 2 diabetes."
        passage_match = "In a randomized trial of 116 adult patients with type 2 diabetes, berberine lowered HbA1c by 1.8% after 12 weeks."

        sup_lvl, ctx_ok, reasons = CitationVerificationEngine.verify_citation_entailment(
            claim_text=claim_match,
            citation=valid_cit,
            passage_text=passage_match
        )
        self.assertEqual(sup_lvl, SupportLevel.DIRECT_SUPPORT)
        self.assertTrue(ctx_ok)

        # Discrepancy test: claim asserts 25%, passage has 1.8%
        claim_wrong_num = "Berberine lowered HbA1c by 25% in adult cohorts."
        sup_lvl2, ctx_ok2, reasons2 = CitationVerificationEngine.verify_citation_entailment(
            claim_text=claim_wrong_num,
            citation=valid_cit,
            passage_text=passage_match
        )
        self.assertEqual(sup_lvl2, SupportLevel.DOES_NOT_SUPPORT)
        self.assertIn("Numerical disparity", "; ".join(reasons2))

    def test_03_zero_citation_laundering_fabricated_doi(self):
        """Detects and rejects fabricated identifiers and topic mentions lacking assertion proof."""
        bogus_cit = Citation(
            source_id="SRC-999",
            document_id="DOC-999",
            title="Fake study",
            identifier="FABRICATED_REFERENCE_XYZ"
        )
        sup_lvl, ctx_ok, reasons = CitationVerificationEngine.verify_citation_entailment(
            claim_text="Berberine cures diabetes",
            citation=bogus_cit,
            passage_text="Something about herbs."
        )
        self.assertEqual(sup_lvl, SupportLevel.DOES_NOT_SUPPORT)
        self.assertIn("fabricated identifier", reasons[0].lower())

    def test_04_causality_firewall_and_rewrite(self):
        """Prevents causal overreach from observational or preclinical evidence."""
        claim_causal = "Compound X cures diabetic neuropathy."
        ok, reason, rewrite = CausalityAndLanguageFirewall.check_causality_and_ladder(
            claim_causal, evidence_grade="observational_human_evidence"
        )
        self.assertFalse(ok)
        self.assertIn("Causal overreach", reason)
        self.assertIsNotNone(rewrite)
        self.assertIn("is associated with", rewrite)

    def test_05_cross_system_equivalence_firewall(self):
        """Rejects direct 1:1 equation of traditional concepts with modern pathology."""
        claim_bad = "Mizaj is equivalent to acute mitochondrial dysfunction."
        ok, reason, rewrite = CausalityAndLanguageFirewall.check_cross_system_equivalence(claim_bad)
        self.assertFalse(ok)
        self.assertIn("False equivalence", reason)
        self.assertIn("parallels", rewrite)

    def test_06_retraction_blocking_and_propagation(self):
        """Blocks retracted publications and traces affected claims."""
        retracted_cit = Citation(
            source_id="SRC-RET",
            document_id="DOC-RET",
            title="Retracted claims",
            identifier="10.1000/retracted-trial",
            is_retracted=True
        )
        sup_lvl, ctx_ok, reasons = CitationVerificationEngine.verify_citation_entailment(
            claim_text="Trial proves complete reversal",
            citation=retracted_cit,
            passage_text="Trial data text."
        )
        self.assertEqual(sup_lvl, SupportLevel.DOES_NOT_SUPPORT)
        self.assertIn("retracted", reasons[0].lower())

        # Test propagation impact analysis
        impact = TruthAndSafetyFirewall.run_retraction_impact_analysis("10.1000/retracted-trial")
        self.assertEqual(impact["status"], "RETRACTED_PROPAGATED")

    def test_07_end_to_end_firewall_pipeline(self):
        """Executes full answer verification with pass, modify, and block outcomes."""
        valid_cit = Citation(
            source_id="SRC-001",
            document_id="DOC-001",
            title="Trial 1",
            identifier="PMID:18442638"
        )
        answer = "Berberine lowered fasting glucose by 1.8% in adult diabetics. Berberine cures diabetic neuropathy permanently."
        passages = {
            valid_cit.identifier: "In this trial, berberine lowered fasting glucose by 1.8% in adult diabetics."
        }
        packet = TruthAndSafetyFirewall.verify_answer(
            generated_answer=answer,
            citations=[valid_cit],
            passages_map=passages
        )
        self.assertEqual(packet.verdict, FirewallVerdict.MODIFY)
        self.assertEqual(len(packet.claims), 2)
        self.assertIn("is associated with", packet.answer)

    def test_08_verify_api_endpoints(self):
        """Tests FastAPI REST endpoints under /v1/verify."""
        # 1. POST /v1/verify/citation
        resp = self.client.post("/v1/verify/citation", json={
            "claim_text": "Berberine reduces HbA1c by 1.8%.",
            "citation": {
                "source_id": "SRC-1",
                "document_id": "DOC-1",
                "title": "Study",
                "identifier": "PMID:18442638"
            },
            "passage_text": "Study observed that berberine reduces HbA1c by 1.8% in human subjects."
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["support_level"], "DIRECT_SUPPORT")

        # 2. POST /v1/verify/answer
        resp_ans = self.client.post("/v1/verify/answer", json={
            "answer": "Mizaj is equivalent to insulin resistance.",
            "citations": [],
            "passages": {}
        })
        self.assertEqual(resp_ans.status_code, 200)
        self.assertIn("verdict", resp_ans.json())

        # 3. POST /v1/verify/retraction-alert
        resp_ret = self.client.post("/v1/verify/retraction-alert", json={
            "identifier": "PMID:99999999"
        })
        self.assertEqual(resp_ret.status_code, 200)
        self.assertEqual(resp_ret.json()["status"], "RETRACTED_PROPAGATED")


if __name__ == "__main__":
    unittest.main()
