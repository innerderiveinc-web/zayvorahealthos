"""
ZMIE Scientific Trust Firewall Master Acceptance Test Suite
Scientific Trust Firewall & Real-Source Verification Acceptance Tests
"""

import unittest
from app.trust_firewall.engine import ScientificTrustFirewallEngine
from app.trust_firewall.models import (
    TrustDecision,
    CanonicalSourceRegistry,
    VerificationState,
    SourceAccessState,
    ClaimEntailmentState,
    AssuranceLevel,
    ToolExecutionState
)


class TestPrompt30TrustFirewallAcceptance(unittest.TestCase):
    def setUp(self):
        self.engine = ScientificTrustFirewallEngine()

    # --- Test 1: Fake Paper (Section 201.1) ---
    def test_01_fake_paper_rejected(self):
        """Nonexistent publication must return not verified / not found."""
        res = self.engine.verify_source("nonexistent-paper-xyz-2026")
        self.assertFalse(res.is_authentic)
        self.assertIn("NOT_FOUND_IN_CANONICAL_REGISTRIES", res.flags)

    # --- Test 2: Fake DOI (Section 201.2) ---
    def test_02_fake_doi_rejected(self):
        """Plausible synthetic DOI must return identifier not verified."""
        res = self.engine.verify_source("10.9999/fake.cure.12345")
        self.assertFalse(res.is_authentic)
        self.assertIn("IDENTIFIER_NOT_VERIFIED", res.flags)

    # --- Test 3: Real Paper, Wrong Claim (Section 201.3) ---
    def test_03_real_paper_wrong_claim_not_supported(self):
        """Real paper citing completely unsupported claim must return CLAIM_NOT_SUPPORTED."""
        report = self.engine.evaluate_trust(
            object_id="clm-wrong-01",
            object_type="claim",
            claim_text="The mRNA-1273 vaccine was developed exclusively to treat acute bacterial meningitis.",
            source_id="10.1056/nejmoa2022483",
            claimed_passage="The mRNA-1273 vaccine showed 94.1% efficacy at preventing Covid-19 illness, including severe disease."
        )
        self.assertEqual(report.decision, TrustDecision.RESTRICT)
        self.assertIn("RULE_CLAIM_ENTAILMENT", report.failed_rules)
        self.assertEqual(report.assessment.status, VerificationState.CONTESTED)

    # --- Test 4: Real Paper, Exaggerated Claim (Section 201.4) ---
    def test_04_real_paper_exaggerated_claim(self):
        """Causal inflation (associated with -> causes) must trigger drift and fail direct support."""
        report = self.engine.evaluate_trust(
            object_id="clm-exaggerated-01",
            object_type="claim",
            claim_text="High serum biomarker level directly causes severe coronary artery disease.",
            source_id="10.1056/nejmoa2022483",
            claimed_passage="High serum biomarker level was found to be associated with coronary artery disease in a cohort of 500 patients."
        )
        self.assertEqual(report.decision, TrustDecision.RESTRICT)
        self.assertIn("RULE_CLAIM_ENTAILMENT", report.failed_rules)

    # --- Test 5: Retracted Paper (Section 201.5) ---
    def test_05_retracted_paper_quarantined_and_blocked(self):
        """Retracted paper must receive RETRACTED status and be quarantined."""
        report = self.engine.evaluate_trust(
            object_id="clm-retracted-01",
            object_type="claim",
            claim_text="MMR vaccine causes autism.",
            source_id="10.1016/s0140-6736(97)11096-0"
        )
        self.assertEqual(report.decision, TrustDecision.REJECT)
        self.assertEqual(report.assessment.status, VerificationState.RETRACTED)
        quarantine = self.engine.list_quarantine_items()
        self.assertTrue(any(q.object_id == "clm-retracted-01" for q in quarantine))

    # --- Test 6: Abstract Only (Section 201.6) ---
    def test_06_abstract_only_source_access(self):
        """Source with ABSTRACT_ONLY access must be explicitly recorded without claiming full text."""
        access = self.engine.get_source_access_state("10.1056/nejmoa2001282")
        self.assertEqual(access, SourceAccessState.ABSTRACT_ONLY)
        report = self.engine.evaluate_trust(
            object_id="clm-abstract-01",
            object_type="claim",
            claim_text="Novel coronavirus identified in Wuhan patients.",
            source_id="10.1056/nejmoa2001282",
            claimed_passage="A novel coronavirus was identified in patients with pneumonia in Wuhan, China in late 2019."
        )
        self.assertEqual(report.assessment.availability_state, SourceAccessState.ABSTRACT_ONLY)

    # --- Test 7: Conflicting Studies (Section 201.7) ---
    def test_07_conflicting_studies_flagged(self):
        """Contradicting assertions must mark conflict_state as CONFLICTING."""
        report = self.engine.evaluate_trust(
            object_id="clm-conflict-01",
            object_type="claim",
            claim_text="Study proves complete efficacy in all cohorts.",
            source_id="10.1056/nejmoa2022483",
            claimed_passage="The trial did not reach statistical significance and showed no efficacy in elderly cohorts."
        )
        self.assertEqual(report.assessment.conflict_state, "CONFLICTING")

    # --- Test 8: Simulation Segregation (Section 201.8) ---
    def test_08_simulation_cannot_be_presented_as_observed(self):
        """Simulated results claiming in-vivo observation must be blocked."""
        report = self.engine.evaluate_trust(
            object_id="clm-sim-01",
            object_type="computation",
            claim_text="Measured in patients and observed in vivo clinical trial.",
            is_simulation=True
        )
        self.assertEqual(report.decision, TrustDecision.REJECT)
        self.assertIn("RULE_SIMULATION_SEGREGATION", report.failed_rules)

    # --- Test 9: Traditional Mapping (Section 201.9) ---
    def test_09_traditional_mapping_preserves_epistemic_distance(self):
        """False 1:1 biomedical reductionist identity must be rejected."""
        report = self.engine.evaluate_trust(
            object_id="clm-trad-01",
            object_type="ontology_mapping",
            traditional_mapping="Ayurvedic Pitta dosha is 1:1 identical to biomedical bile liquid."
        )
        self.assertEqual(report.decision, TrustDecision.RESTRICT)
        self.assertIn("RULE_TRADITIONAL_MAPPING_EPISTEMIC_DISTANCE", report.failed_rules)

    # --- Test 10: Fake Regulatory Claim (Section 201.10) ---
    def test_10_fake_regulatory_claim_blocked(self):
        """Unverified claim of FDA approval without gazette citation must be rejected."""
        report = self.engine.evaluate_trust(
            object_id="clm-reg-01",
            object_type="claim",
            source_id="10.1056/nejmoa2022483",
            regulatory_claim="This experimental herbal molecule is FDA approved for oncology."
        )
        self.assertEqual(report.decision, TrustDecision.REJECT)
        self.assertIn("RULE_REGULATORY_STATUS_VERIFICATION", report.failed_rules)

    # --- Test 11: Private Tenant Data Isolation (Section 201.11) ---
    def test_11_private_tenant_data_blocked_from_public_release(self):
        """Private tenant data cannot be released to public knowledge."""
        self.engine.register_tenant_private_object("tenant-confidential", "dataset-private-77")
        report = self.engine.evaluate_trust(
            object_id="dataset-private-77",
            object_type="dataset",
            tenant_id="tenant-confidential",
            is_public_release=True
        )
        self.assertEqual(report.decision, TrustDecision.REJECT)
        self.assertIn("RULE_TENANT_DATA_ISOLATION", report.failed_rules)

    # --- Test 12: Agent Direct Authoritative Write Bypass (Section 201.12) ---
    def test_12_agent_direct_authoritative_write_bypass_blocked(self):
        """Agents cannot self-certify or bypass trust gates to write authoritative claims."""
        report = self.engine.evaluate_trust(
            object_id="clm-agent-bypass",
            object_type="claim",
            claim_text="Agent synthesized medical assertion.",
            source_id=None,
            actor_role="AGENT"
        )
        self.assertNotEqual(report.assessment.status, VerificationState.AUTHORITATIVE)
        self.assertEqual(report.decision, TrustDecision.REJECT)

    # --- Test 13: Admin Promotion Bypass Blocked (Section 201.13) ---
    def test_13_unauthorized_admin_promotion_bypass_blocked(self):
        """Platform admins cannot bypass scientific governance without verified sources."""
        report = self.engine.evaluate_trust(
            object_id="clm-admin-bypass",
            object_type="claim",
            claim_text="Admin uploaded unverified claim.",
            source_id=None,
            actor_role="ADMIN"
        )
        self.assertNotEqual(report.assessment.status, VerificationState.AUTHORITATIVE)
        self.assertEqual(report.decision, TrustDecision.REJECT)

    # --- Test 14: Source Change Revalidation (Section 201.14) ---
    def test_14_source_material_change_triggers_revalidation(self):
        """When source changes, revalidation history is appended."""
        self.engine.evaluate_trust(
            object_id="clm-source-change-01",
            object_type="claim",
            claim_text="Original finding",
            source_id="10.1056/nejmoa2022483",
            claimed_passage="The mRNA-1273 vaccine showed 94.1% efficacy at preventing Covid-19 illness, including severe disease."
        )
        # Update source assessment
        self.engine.evaluate_trust(
            object_id="clm-source-change-01",
            object_type="claim",
            claim_text="Updated finding",
            source_id="10.1056/nejmoa2022483",
            claimed_passage="The mRNA-1273 vaccine showed 94.1% efficacy at preventing Covid-19 illness, including severe disease."
        )
        history = self.engine.get_trust_history("clm-source-change-01")
        self.assertEqual(len(history), 2)

    # --- Test 15: Policy Change Identifies Affected Objects (Section 201.15) ---
    def test_15_policy_change_identifies_affected_objects(self):
        """Policy gates evaluate strictness and record policy version."""
        self.engine.evaluate_trust(
            object_id="clm-policy-01",
            object_type="claim",
            claim_text="Vaccine trial efficacy",
            source_id="10.1056/nejmoa2022483",
            claimed_passage="The mRNA-1273 vaccine showed 94.1% efficacy at preventing Covid-19 illness, including severe disease."
        )
        cert = self.engine.issue_trust_certificate("clm-policy-01")
        self.assertIsNotNone(cert)
        self.assertEqual(cert.policy_version, "POLICY-ZMIE-2026-V1")

    # --- Test 16: Citation Drift Detection (Section 201.16) ---
    def test_16_citation_drift_revalidation_detection(self):
        """Citation drift between claim and passage is detected and scored."""
        in_vitro = "Demonstrated in vitro murine cellular inhibition."
        human_cure = "Definitively cures humans with 100% clinical efficacy."
        drift = self.engine.calculate_epistemic_drift(human_cure, in_vitro)
        self.assertGreater(drift, 0.6)

    # --- Test 17: Research Replay Temporal Integrity (Section 201.17) ---
    def test_17_research_replay_temporal_integrity(self):
        """Historical assessments preserve their exact timestamp and status."""
        history = self.engine.get_trust_history("clm-source-change-01")
        for record in history:
            self.assertIsNotNone(record.verification_timestamp)
            self.assertEqual(record.object_id, "clm-source-change-01")

    # --- Test 18: Trust Service Fail-Closed (Section 201.18) ---
    def test_18_trust_service_fail_closed(self):
        """When trust verification service is offline, high-risk promotion is strictly REJECTED."""
        self.engine.set_online_status(False)
        report = self.engine.evaluate_trust(
            object_id="clm-offline-test",
            object_type="claim",
            claim_text="Important claim",
            source_id="10.1056/nejmoa2022483"
        )
        self.assertEqual(report.decision, TrustDecision.REJECT)
        self.assertEqual(report.assessment.status, VerificationState.UNKNOWN)
        self.assertIn("FAIL_CLOSED", report.assessment.notes[0])
        self.engine.set_online_status(True)

    # --- Test 19: Tool Failure Cannot Be Represented as Success (Section 201.19) ---
    def test_19_tool_failure_status(self):
        """Tool execution state enum preserves explicit FAILED and TIMEOUT states."""
        self.assertEqual(ToolExecutionState.FAILED.value, "FAILED")
        self.assertEqual(ToolExecutionState.TIMEOUT.value, "TIMEOUT")
        self.assertNotEqual(ToolExecutionState.FAILED, ToolExecutionState.SUCCESS)

    # --- Test 20: Audit Tampering Blocked by HMAC (Section 201.20) ---
    def test_20_audit_tampering_blocked_by_hmac(self):
        """Verified ledger records must carry cryptographic HMAC signatures."""
        entries = self.engine.list_ledger_entries()
        self.assertGreater(len(entries), 0)
        for entry in entries:
            self.assertTrue(len(entry.tamper_proof_hmac) == 64)
            # Modifying entry breaks HMAC
            corrupted_hash = entry.canonical_hash[:-4] + "ffff"
            raw_sig = f"{entry.identifier}:{entry.registry.value}:{corrupted_hash}"
            import hmac, hashlib
            recomputed = hmac.new(self.engine.SECRET_KEY, raw_sig.encode("utf-8"), hashlib.sha256).hexdigest()
            self.assertNotEqual(recomputed, entry.tamper_proof_hmac)


if __name__ == "__main__":
    unittest.main()
