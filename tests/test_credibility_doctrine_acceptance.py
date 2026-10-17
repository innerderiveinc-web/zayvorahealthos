"""
Acceptance Test Suite for ZMIE Scientific Credibility, Verification, Provenance & Anti-Fabrication Engine
PROMPT 29 — Acceptance Tests for Credibility Doctrine, Epistemic Levels & 14-Layer Audit
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.credibility.models import (
    VerificationState,
    EvidenceChain,
    EpistemicSeparationLevels
)
from app.credibility.engine import ScientificCredibilityEngine, get_credibility_engine
from zmie import ZMIEClient


class TestCredibilityDoctrineAcceptance(unittest.TestCase):

    def setUp(self):
        self.engine = ScientificCredibilityEngine()
        self.client = TestClient(app)
        self.sdk = ZMIEClient(api_key="zmie_test_key", app_instance=app)

    def test_01_golden_rule_epistemic_separation(self):
        """
        Validates the Golden Rule:
        SOURCE EXISTS ≠ SOURCE IS AUTHENTIC ≠ CLAIM IS SUPPORTED ≠ CLAIM IS TRUE ≠ CLINICALLY VALID ≠ REGULATORY APPROVED
        """
        # Case A: Document exists, but is NOT authentic (bogus identifier)
        levels_bogus = self.engine.evaluate_epistemic_separation(
            source_id="SRC-BOGUS",
            identifier="FABRICATED_DOI_XYZ",
            passage_text="Random text",
            claim_text="Berberine cures diabetes."
        )
        self.assertTrue(levels_bogus.source_exists)
        self.assertFalse(levels_bogus.source_is_authentic)
        self.assertFalse(levels_bogus.claim_is_supported)
        self.assertFalse(levels_bogus.claim_is_true)
        self.assertFalse(levels_bogus.claim_is_clinically_valid)
        self.assertFalse(levels_bogus.claim_is_regulatory_approved)

        # Case B: Document exists and is authentic, but passage does NOT support claim (Citation Laundering)
        levels_unsupported = self.engine.evaluate_epistemic_separation(
            source_id="SRC-PUBMED-01",
            identifier="PMID:18442638",
            passage_text="This paper only evaluates safety and pharmacokinetics in rat hepatic tissue.",
            claim_text="Berberine lowered fasting blood glucose by 25% in human diabetics."
        )
        self.assertTrue(levels_unsupported.source_exists)
        self.assertTrue(levels_unsupported.source_is_authentic)
        self.assertFalse(levels_unsupported.claim_is_supported)
        self.assertFalse(levels_unsupported.claim_is_true)

        # Case C: Supported and clinically valid, but NOT regulatory approved
        levels_supported = self.engine.evaluate_epistemic_separation(
            source_id="SRC-PUBMED-01",
            identifier="PMID:18442638",
            passage_text="In a randomized trial of 116 adult patients with type 2 diabetes, berberine lowered fasting blood glucose by 1.8% after 12 weeks.",
            claim_text="Berberine lowered fasting blood glucose by 1.8% in adult diabetics.",
            clinical_rct_available=True,
            regulatory_approved=False
        )
        self.assertTrue(levels_supported.source_exists)
        self.assertTrue(levels_supported.source_is_authentic)
        self.assertTrue(levels_supported.claim_is_supported)
        self.assertTrue(levels_supported.claim_is_true)
        self.assertTrue(levels_supported.claim_is_clinically_valid)
        self.assertFalse(levels_supported.claim_is_regulatory_approved)

    def test_02_mandatory_evidence_chain_enforcement(self):
        """
        Enforces that any missing link in CLAIM -> EVIDENCE -> STUDY -> SOURCE -> LOCATION -> PROVENANCE -> STATUS
        strictly marks chain as incomplete and demotes status to INSUFFICIENT_EVIDENCE.
        """
        # Case A: Missing exact location
        broken_chain = EvidenceChain(
            chain_id="chain-broken-01",
            claim_id="clm-001",
            claim_text="Berberine lowered fasting blood glucose by 1.8% in adult diabetics.",
            evidence_id="evi-001",
            study_or_dataset_id="PMID:18442638",
            source_id="SRC-PUBMED",
            exact_location=None, # Missing exact location!
            provenance_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            verification_state=VerificationState.AUTHORITATIVE
        )
        verified = self.engine.verify_evidence_chain(broken_chain)
        self.assertFalse(verified.is_complete)
        self.assertEqual(verified.verification_state, VerificationState.INSUFFICIENT_EVIDENCE)
        self.assertIn("EXACT LOCATION link missing", verified.deficiency_reasons[0])

        # Case B: Complete unbroken chain
        complete_chain = EvidenceChain(
            chain_id="chain-complete-01",
            claim_id="clm-002",
            claim_text="Berberine lowered fasting blood glucose by 1.8% in adult diabetics.",
            evidence_id="evi-001",
            study_or_dataset_id="PMID:18442638",
            source_id="SRC-PUBMED",
            exact_location="Page 112, Results Section, Table 2",
            provenance_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            verification_state=VerificationState.EVIDENCE_SUPPORTED
        )
        verified_ok = self.engine.verify_evidence_chain(complete_chain)
        self.assertTrue(verified_ok.is_complete)
        self.assertEqual(len(verified_ok.deficiency_reasons), 0)

    def test_03_strict_verification_lifecycle_ladder(self):
        """
        Enforces step-by-step ladder:
        UNVERIFIED -> CANDIDATE -> SOURCE_VERIFIED -> EVIDENCE_SUPPORTED -> EXPERT_REVIEWED -> AUTHORITATIVE
        Prevents skipping levels and demands proof for AUTHORITATIVE.
        """
        obj_id = "claim-test-lifecycle-01"

        # Step 1: UNVERIFIED -> CANDIDATE (Allowed)
        ok1, _, s1 = self.engine.transition_state(obj_id, VerificationState.CANDIDATE, {})
        self.assertTrue(ok1)
        self.assertEqual(s1, VerificationState.CANDIDATE)

        # Illegal Jump: CANDIDATE -> AUTHORITATIVE (Blocked)
        ok_bad, msg_bad, _ = self.engine.transition_state(obj_id, VerificationState.AUTHORITATIVE, {})
        self.assertFalse(ok_bad)
        self.assertIn("INVALID_LIFECYCLE_TRANSITION", msg_bad)

        # Step 2: CANDIDATE -> SOURCE_VERIFIED (Allowed)
        ok2, _, s2 = self.engine.transition_state(obj_id, VerificationState.SOURCE_VERIFIED, {})
        self.assertTrue(ok2)

        # Step 3: SOURCE_VERIFIED -> EVIDENCE_SUPPORTED (Allowed)
        ok3, _, s3 = self.engine.transition_state(obj_id, VerificationState.EVIDENCE_SUPPORTED, {})
        self.assertTrue(ok3)

        # Step 4: EVIDENCE_SUPPORTED -> EXPERT_REVIEWED (Allowed)
        ok4, _, s4 = self.engine.transition_state(obj_id, VerificationState.EXPERT_REVIEWED, {})
        self.assertTrue(ok4)

        # Step 5: EXPERT_REVIEWED -> AUTHORITATIVE without proof (Blocked)
        ok5_bad, msg5_bad, _ = self.engine.transition_state(obj_id, VerificationState.AUTHORITATIVE, {})
        self.assertFalse(ok5_bad)
        self.assertIn("AUTHORITATIVE_PROHIBITION", msg5_bad)

        # Step 5: EXPERT_REVIEWED -> AUTHORITATIVE with verified expert review and complete chain (Allowed)
        ok5, _, s5 = self.engine.transition_state(
            obj_id,
            VerificationState.AUTHORITATIVE,
            {"expert_reviewer_id": "REV-DR-SMITH", "is_chain_complete": True}
        )
        self.assertTrue(ok5)
        self.assertEqual(s5, VerificationState.AUTHORITATIVE)

    def test_04_traditional_knowledge_anti_forced_equivalence(self):
        """
        Verifies that traditional concepts cannot be equated 1:1 with modern pathology on semantic similarity.
        """
        report = self.engine.run_14_layer_audit(
            target_object_id="clm-trad-01",
            target_object_type="CLAIM",
            claim_text="Mizaj Har is the same as acute inflammation.",
            source_id="SRC-AYUSH-01",
            identifier="CCRUM-042",
            passage_text="Text regarding Mizaj Har.",
            traditional_mapping={
                "is_direct_equivalence": True, # VIOLATION!
                "canonical_codex": "CCRUM"
            }
        )
        l9 = next(l for l in report.layers_audited if l.layer_number == 9)
        self.assertEqual(l9.status, "FAIL")
        self.assertIn("FORCED EQUIVALENCE VIOLATION", l9.reasons[0])
        self.assertFalse(report.is_authoritative_permitted)

    def test_05_ai_candidate_cannot_directly_become_authoritative(self):
        """
        Enforces rule: AI candidate can NEVER bypass human/expert governance to become authoritative.
        """
        report = self.engine.run_14_layer_audit(
            target_object_id="clm-ai-01",
            target_object_type="CLAIM",
            claim_text="Berberine reduces HbA1c by 1.8% in adult diabetics.",
            source_id="SRC-PUBMED-01",
            identifier="PMID:18442638",
            passage_text="In this randomized trial of 116 adult patients with type 2 diabetes, berberine lowered fasting glucose by 1.8%.",
            is_ai_generated=True,
            is_expert_signed=False, # Not yet signed by expert
            exact_location="Table 2"
        )
        l11 = next(l for l in report.layers_audited if l.layer_number == 11)
        self.assertEqual(l11.status, "FLAGGED")
        self.assertIn("AI AUTHORITATIVE PROHIBITION", l11.reasons[0])
        self.assertFalse(report.is_authoritative_permitted)

    def test_06_complete_14_layer_anti_fabrication_audit(self):
        """
        Audits a scientific object across all 14 Anti-Fabrication Layers and validates HMAC signature.
        """
        report = self.engine.run_14_layer_audit(
            target_object_id="clm-golden-01",
            target_object_type="CLAIM",
            claim_text="Berberine lowered fasting blood glucose by 1.8% in adult diabetics.",
            source_id="SRC-PUBMED-01",
            identifier="PMID:18442638",
            passage_text="In a randomized trial of 116 adult patients with type 2 diabetes, berberine lowered fasting blood glucose by 1.8% after 12 weeks.",
            dataset_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            researcher_orcid="0000-0002-1825-0097",
            drug_name="METFORMIN",
            calculation_seed=42,
            is_ai_generated=True,
            is_expert_signed=True,
            exact_location="Page 112, Table 2"
        )
        self.assertEqual(len(report.layers_audited), 14)
        self.assertTrue(all(l.status in ["PASS", "UNKNOWN", "FLAGGED"] for l in report.layers_audited))
        self.assertTrue(len(report.tamper_evident_hmac) >= 32)
        self.assertEqual(report.overall_state, VerificationState.AUTHORITATIVE)
        self.assertTrue(report.is_authoritative_permitted)

    def test_07_rest_api_and_sdk_integration(self):
        """
        Tests REST API endpoints and SDK methods for Prompt 29.
        """
        # SDK claim audit
        sdk_res = self.sdk.credibility.audit_claim(
            target_object_id="sdk-clm-01",
            claim_text="Metformin lowers HbA1c by 1.5% in adult diabetics.",
            source_id="SRC-PUBMED-01",
            identifier="PMID:18442638",
            passage_text="Metformin lowered HbA1c by 1.5% in diabetic cohort.",
            calculation_seed=42,
            is_expert_signed=True,
            exact_location="Section 3, Para 1"
        )
        self.assertIn("audit_id", sdk_res)
        self.assertIn("layers_audited", sdk_res)
        self.assertEqual(len(sdk_res["layers_audited"]), 14)

        # SDK chain verify
        chain_res = self.sdk.credibility.verify_chain({
            "chain_id": "sdk-chain-01",
            "claim_id": "sdk-clm-01",
            "claim_text": "Metformin lowers HbA1c by 1.5%.",
            "evidence_id": "evi-01",
            "study_or_dataset_id": "PMID:18442638",
            "source_id": "SRC-PUBMED-01",
            "exact_location": "Table 1",
            "provenance_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "verification_state": "EVIDENCE_SUPPORTED"
        })
        self.assertTrue(chain_res["is_complete"])


if __name__ == "__main__":
    unittest.main()
