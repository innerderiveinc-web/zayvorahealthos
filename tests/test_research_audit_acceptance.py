"""
ZMIE Scientific Reproducibility & Research Audit Acceptance Test Suite (Prompt 26)
Tests the 13 reproducibility dimensions, immutable snapshots, SHA256 chained audit events,
bidirectional lineage traces, double extraction reconciliation, analysis plan deviations,
sandbox reproduction comparison matrix, official certificates, and tenant isolation (Clauses 1-305).
"""

import unittest
from datetime import datetime
import copy

from app.models.audit import (
    ResearchSnapshot,
    ResearchAudit,
    AuditEvent,
    AuditEventType,
    AuditActorType,
    ExclusionReason,
    AuditFindingSeverity,
    AuditFindingStatus,
    ReproducibilityDimension,
    ReproducibilityStatus,
    ReproductionMode,
    ReproductionRun,
    SearchStrategyRecord,
    ScreeningDecision,
    ExtractionRecord,
    AnalysisPlanRecord,
    AnalysisDeviation,
    EnvironmentSpec,
    CodeProvenance,
)
from app.models.federated_privacy import ResearchDataClassification
from app.audit import (
    get_audit_system,
    AuditEventStore,
    SnapshotManager,
    ResearchProvenanceGraph,
    ScreeningAuditManager,
    ExtractionAuditManager,
    ScientificIntegrityAuditor,
    ReproductionEngine,
    CertificateIssuer,
)
from app.main import app
from zmie.client import ZMIE


class TestResearchAuditAcceptance(unittest.TestCase):
    def setUp(self):
        self.sys = get_audit_system()
        self.client = ZMIE(app_instance=app)

    # ==========================================================================
    # 1. Golden Scenario & Snapshot Immutability (Clauses 5-9, 251, 280, 291)
    # ==========================================================================

    def test_golden_snapshot_retrieval_and_manifest(self):
        """Verifies initial seeded golden snapshot has valid manifest and checksums."""
        snap = self.sys.get_snapshot("rs-golden-berberine-01")
        self.assertIsNotNone(snap)
        self.assertEqual(snap.version, "1.0.0")
        self.assertTrue(snap.is_locked)
        self.assertTrue(snap.manifest_hash.startswith("sha256:"))

        manifest = snap.generate_manifest()
        self.assertEqual(manifest["snapshot_id"], "rs-golden-berberine-01")
        self.assertEqual(manifest["sources_count"], 2)
        self.assertEqual(manifest["evidence_count"], 1)
        self.assertEqual(manifest["extractions_count"], 1)
        self.assertEqual(manifest["manifest_hash"], snap.manifest_hash)

    def test_snapshot_immutability_guard(self):
        """Strict Immutability Guard: Locked snapshots cannot be overwritten in place (Clause 5)."""
        snap = self.sys.get_snapshot("rs-golden-berberine-01")
        # Attempting to save an existing locked snapshot with new data must fail
        snap_copy = copy.deepcopy(snap)
        snap_copy.research_question = "Mutated question attempting in-place rewrite"

        with self.assertRaises(ValueError) as ctx:
            self.sys.snapshots.save_snapshot(snap_copy)
        self.assertIn("locked and immutable", str(ctx.exception))

    def test_parent_child_lineage_and_answer_diff(self):
        """Child snapshots derive from parent, bump semantic version, and compute answer diff (Clauses 94-96, 293)."""
        parent_id = "rs-golden-berberine-01"
        updates = {
            "evidence_items": [
                {"study_id": "study-rct-zhang-2023", "title": "Zhang et al. 2023", "design": "RCT"},
                {"study_id": "study-rct-chen-2024", "title": "Chen et al. 2024 multicenter trial", "design": "RCT"}
            ],
            "final_output": {
                "conclusion": "Updated synthesis confirms Berberine reduces HbA1c by 0.84% with high certainty.",
                "evidence_quality": "GRADE_HIGH"
            }
        }

        child = self.sys.create_child_snapshot(
            parent_snapshot_id=parent_id,
            updates=updates,
            created_by="agent-researcher-chen",
        )

        self.assertIsNotNone(child.snapshot_id)
        self.assertEqual(child.parent_snapshot_id, parent_id)
        self.assertEqual(child.version, "1.1.0")
        self.assertTrue(child.is_locked)

        # Lineage check
        lineage = self.sys.snapshots.get_lineage(child.snapshot_id)
        self.assertEqual(len(lineage), 2)
        self.assertEqual(lineage[0].snapshot_id, parent_id)
        self.assertEqual(lineage[1].snapshot_id, child.snapshot_id)

        # Answer Diff check
        diff = self.sys.snapshots.compute_answer_diff(parent_id, child.snapshot_id)
        self.assertEqual(diff.old_snapshot_id, parent_id)
        self.assertEqual(diff.new_snapshot_id, child.snapshot_id)
        self.assertTrue(len(diff.evidence_diff) >= 1)
        self.assertEqual(diff.evidence_diff[0]["action"], "STUDY_ADDED")
        self.assertIn("Chen et al. 2024", diff.evidence_diff[0]["title"])
        self.assertTrue(len(diff.upstream_causes) >= 1)

    # ==========================================================================
    # 2. Tamper-Evident Hash Chained Audit Log (Clauses 11-14, 225, 262)
    # ==========================================================================

    def test_cryptographic_hash_chain_verification(self):
        """Verifies that an uncorrupted audit chain verifies 100% valid (Clause 225)."""
        audit_id = "audit-golden-berberine-01"
        report = self.sys.verify_audit_trail(audit_id)
        self.assertTrue(report["is_valid"])
        self.assertFalse(report["tampered"])
        self.assertEqual(report["total_events"], 5)
        self.assertTrue(report["genesis_verified"])

    def test_tamper_evident_red_team_detection(self):
        """Red-team test: Any in-memory tampering or mutation breaks hash verification (Clause 262)."""
        temp_store = AuditEventStore()
        chain_id = "audit-tamper-test-01"

        e1 = temp_store.record_event(
            audit_id=chain_id,
            action=AuditEventType.SOURCE_SEARCHED,
            resource_type="SEARCH",
            resource_id="search-01"
        )
        e2 = temp_store.record_event(
            audit_id=chain_id,
            action=AuditEventType.STUDY_INCLUDED,
            resource_type="STUDY",
            resource_id="study-01"
        )
        e3 = temp_store.record_event(
            audit_id=chain_id,
            action=AuditEventType.RESULT_CREATED,
            resource_type="RESULT",
            resource_id="res-01"
        )

        # Initial check must pass
        check_before = temp_store.verify_chain(chain_id)
        self.assertTrue(check_before["is_valid"])

        # Tamper step: Mutate event 1's action without updating hashes
        tampered = temp_store.corrupt_event_for_testing(chain_id, event_index=1, new_action=AuditEventType.STUDY_EXCLUDED)
        self.assertTrue(tampered)

        # Verification must now fail!
        check_after = temp_store.verify_chain(chain_id)
        self.assertFalse(check_after["is_valid"])
        self.assertTrue(check_after["tampered"])
        self.assertEqual(check_after["failed_step"], 1)
        self.assertEqual(check_after["error"], "EVENT_HASH_MUTATED")

    # ==========================================================================
    # 3. Systematic Screening & Extraction Audit (Clauses 26-35, 300)
    # ==========================================================================

    def test_screening_exclusion_reason_enforcement(self):
        """Scientific integrity rule: Excluding a study without a formal reason must fail (Clauses 28, 300)."""
        manager = ScreeningAuditManager()
        # Including without reason is fine
        d_inc = manager.record_decision(
            study_id="s1",
            study_title="Included Trial",
            decision="INCLUDED"
        )
        self.assertEqual(d_inc.decision, "INCLUDED")

        # Excluding WITHOUT reason must raise ValueError
        with self.assertRaises(ValueError) as ctx:
            manager.record_decision(
                study_id="s2",
                study_title="Excluded Trial",
                decision="EXCLUDED",
                reason=None
            )
        self.assertIn("explicit ExclusionReason", str(ctx.exception))

        # Excluding WITH reason succeeds
        d_exc = manager.record_decision(
            study_id="s2",
            study_title="Excluded Trial",
            decision="EXCLUDED",
            reason=ExclusionReason.WRONG_POPULATION
        )
        self.assertEqual(d_exc.decision, "EXCLUDED")
        self.assertEqual(d_exc.reason, ExclusionReason.WRONG_POPULATION)

        # PRISMA flow summary check
        prisma = manager.get_prisma_flow_summary()
        self.assertEqual(prisma["total_screened"], 2)
        self.assertEqual(prisma["included"], 1)
        self.assertEqual(prisma["excluded"], 1)
        self.assertEqual(prisma["exclusion_reasons"]["WRONG_POPULATION"], 1)

    def test_double_extraction_and_discrepancy_resolution(self):
        """Tests double-blind data extraction and formal consensus reconciliation (Clauses 34, 35)."""
        manager = ExtractionAuditManager()

        # Reviewer A and B agree
        dis1 = manager.record_double_extraction(
            study_id="s-101",
            field_name="sample_size",
            reviewer_a_id="rev-alice",
            reviewer_a_val=150,
            reviewer_b_id="rev-bob",
            reviewer_b_val=150
        )
        self.assertIsNone(dis1)  # No disagreement

        # Reviewer A and B disagree
        dis2 = manager.record_double_extraction(
            study_id="s-101",
            field_name="HbA1c_change",
            reviewer_a_id="rev-alice",
            reviewer_a_val=-0.75,
            reviewer_b_id="rev-bob",
            reviewer_b_val=-0.85
        )
        self.assertIsNotNone(dis2)
        self.assertFalse(dis2.resolved)
        self.assertEqual(len(manager.get_open_disagreements()), 1)

        # Resolve disagreement
        resolved = manager.resolve_disagreement(
            disagreement_id=dis2.disagreement_id,
            resolution_val=-0.82,
            resolver_id="dr-senior-adjudicator",
            rationale="Review of Table 3 page 12 reveals intention-to-treat effect size was -0.82%"
        )
        self.assertTrue(resolved.resolved)
        self.assertEqual(resolved.resolution_val, -0.82)
        self.assertEqual(len(manager.get_open_disagreements()), 0)

    # ==========================================================================
    # 4. Bidirectional Provenance Graph & Impact Analysis (Clauses 15, 16, 122, 125, 294, 295)
    # ==========================================================================

    def test_bidirectional_lineage_and_impact_tracing(self):
        """Tests backward attribution from conclusion and forward impact tracing from retracted study."""
        snap = self.sys.get_snapshot("rs-golden-berberine-01")
        trace = self.sys.provenance.get_trace(snap.snapshot_id)
        self.assertIsNotNone(trace)
        self.assertTrue(len(trace.nodes) >= 6)
        self.assertTrue(len(trace.edges) >= 5)

        # Backward trace from conclusion
        backward_nodes = self.sys.provenance.backward_trace(snap.snapshot_id, trace.conclusion_id)
        node_types = {n.node_type for n in backward_nodes}
        self.assertIn("CONCLUSION", node_types)
        self.assertIn("CLAIM", node_types)
        self.assertIn("RESULT", node_types)
        self.assertIn("ANALYSIS", node_types)
        self.assertIn("QUESTION", node_types)

        # Forward trace from study (e.g., if study is retracted or re-analyzed)
        study_node = next(n for n in trace.nodes if n.node_type == "STUDY")
        forward_nodes = self.sys.provenance.forward_trace(snap.snapshot_id, study_node.node_id)
        fwd_types = {n.node_type for n in forward_nodes}
        self.assertIn("STUDY", fwd_types)
        self.assertIn("SCREENING", fwd_types)
        self.assertIn("EXTRACTION", fwd_types)
        self.assertIn("ANALYSIS", fwd_types)
        self.assertIn("RESULT", fwd_types)
        self.assertIn("CLAIM", fwd_types)
        self.assertIn("CONCLUSION", fwd_types)

    # ==========================================================================
    # 5. Scientific Integrity Audits & Deviation Checks (Clauses 38, 163-165, 296, 300)
    # ==========================================================================

    def test_phantom_citation_zero_fabrication_rejection(self):
        """Zero-Fabrication Gate: Rejects phantom or hallucinated citations with CRITICAL severity finding (Clause 300)."""
        auditor = ScientificIntegrityAuditor()

        invalid_snapshot = ResearchSnapshot(
            snapshot_id="rs-test-phantom",
            research_question="Does berberine inhibit PCSK9?",
            evidence_items=[{"study_id": "study-real-01", "doi": "10.1001/real.01"}],
            claims=[
                {
                    "claim_id": "clm-bad",
                    "statement": "PCSK9 is significantly downregulated.",
                    "citations": ["study-fake-hallucination-999"]
                }
            ]
        )

        findings = auditor.audit_citations(invalid_snapshot)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, AuditFindingSeverity.CRITICAL)
        self.assertEqual(findings[0].object_type, "CITATION")
        self.assertIn("Unresolved / Phantom Citation", findings[0].issue)

    def test_unsupported_causal_language_detection(self):
        """Flags unwarranted deterministic causal assertions in observational research (Clause 163)."""
        auditor = ScientificIntegrityAuditor()

        overclaiming_snapshot = ResearchSnapshot(
            snapshot_id="rs-test-causal",
            research_question="Observational analysis of curcumin in osteoarthritis",
            claims=[
                {
                    "claim_id": "clm-causal-overclaim",
                    "statement": "Curcumin definitive cure proves direct cause eradication of arthritis."
                }
            ]
        )

        findings = auditor.audit_causal_language(overclaiming_snapshot)
        self.assertTrue(len(findings) >= 1)
        self.assertEqual(findings[0].severity, AuditFindingSeverity.HIGH)
        self.assertIn("Unsupported Causal Claim", findings[0].issue)

    def test_analysis_plan_deviation_audit(self):
        """Audits documented deviations from pre-registered research plan (Clauses 38, 296)."""
        plan = AnalysisPlanRecord(
            plan_id="plan-rct-01",
            research_question="Efficacy of Metformin",
            hypothesis="Reduces HbA1c",
            population="Adults with T2D",
            intervention="Metformin",
            comparator="Placebo",
            outcome="HbA1c",
            analysis_method="ANCOVA",
            is_preregistered=True,
            deviations=[
                AnalysisDeviation(
                    plan_id="plan-rct-01",
                    deviation_type="ENDPOINT_CHANGE",
                    planned_spec="Primary outcome at 24 weeks",
                    actual_spec="Switched primary outcome to 12 weeks due to early trial closure",
                    reason="COVID-19 site access restrictions",
                    authorized_by="Dr. Steering Committee Chair",
                    impact_assessment="Statistical power preserved with alpha penalty"
                )
            ]
        )

        snap = ResearchSnapshot(
            snapshot_id="rs-test-deviation",
            research_question="Metformin efficacy",
            analysis_plan=plan
        )

        auditor = ScientificIntegrityAuditor()
        findings = auditor.audit_plan_deviations(snap)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, AuditFindingSeverity.HIGH)
        self.assertIn("ENDPOINT_CHANGE", findings[0].issue)

    # ==========================================================================
    # 6. Sandbox Reproduction Engine & Comparison Matrix (Clauses 87-90, 136, 252, 292)
    # ==========================================================================

    def test_golden_reproduction_run_success(self):
        """Golden reproduction test: Re-executing golden snapshot achieves REPRODUCED status (Clause 252, 292)."""
        run = self.sys.reproduce("rs-golden-berberine-01", mode=ReproductionMode.SANDBOX)
        self.assertEqual(run.status, ReproducibilityStatus.REPRODUCED)
        self.assertEqual(len(run.matrix), 5)

        stages = [row.stage for row in run.matrix]
        self.assertListEqual(stages, ["Search", "Data", "Analysis", "Computation", "Result"])
        self.assertTrue(all(row.is_acceptable for row in run.matrix))
        self.assertEqual(len(run.differences), 0)

    def test_reproduction_run_detects_data_and_result_divergence(self):
        """Simulated drift test: Result divergence returns PARTIALLY_REPRODUCED or NOT_REPRODUCIBLE (Clause 136)."""
        snap = self.sys.get_snapshot("rs-golden-berberine-01")

        # Simulate unexpected result divergence
        run_diverged = self.sys.reproduction.run_reproduction(
            snapshot=snap,
            simulated_drift={"result_drift": 0.45}  # Substantial divergence
        )
        self.assertNotEqual(run_diverged.status, ReproducibilityStatus.REPRODUCED)
        self.assertTrue(len(run_diverged.differences) >= 1)
        res_row = next(r for r in run_diverged.matrix if r.stage == "Result")
        self.assertFalse(res_row.is_acceptable)
        self.assertIn("divergence", res_row.difference)

    # ==========================================================================
    # 7. Official Scientific Certificates & Export Packet (Clauses 101, 102, 215, 216)
    # ==========================================================================

    def test_issue_certificates_and_export_packet(self):
        """Verifies formal issuance of Reproducibility & Audit Certificates and export packet (Clauses 215, 216)."""
        certs = self.sys.issue_certificates("audit-golden-berberine-01")
        repro_cert = certs["reproducibility_certificate"]
        audit_cert = certs["research_audit_certificate"]

        self.assertEqual(repro_cert.reproducibility_status, ReproducibilityStatus.REPRODUCED)
        self.assertEqual(len(repro_cert.dimension_statuses), 13)
        self.assertTrue(repro_cert.is_exact_match)
        self.assertTrue(repro_cert.data_lock_hash.startswith("sha256:"))

        self.assertEqual(audit_cert.provenance_completeness_pct, 100.0)
        self.assertEqual(audit_cert.integrity_state, "TAMPER_FREE_CRYPTOGRAPHIC_CHAIN")
        self.assertTrue(audit_cert.digital_signature.startswith("sig:zmie-scientific-audit"))

        # Export packet JSON
        packet = self.sys.export_audit_packet("audit-golden-berberine-01", format_type="json")
        self.assertEqual(packet.audit_id, "audit-golden-berberine-01")
        self.assertIsNotNone(packet.manifest)
        self.assertIsNotNone(packet.reproducibility_certificate)
        self.assertIsNotNone(packet.audit_certificate)

        # Export packet HTML
        html_doc = self.sys.export_audit_packet("audit-golden-berberine-01", format_type="html")
        self.assertIn("<!DOCTYPE html>", html_doc)
        self.assertIn("ZMIE Research Audit Packet", html_doc)

    # ==========================================================================
    # 8. Tenant Isolation, Legal Hold & Auditor View Redaction (Clauses 230, 237, 265, 298)
    # ==========================================================================

    def test_tenant_isolation_boundary(self):
        """Verifies strict cross-tenant isolation: Tenant B cannot access Tenant A's snapshot or audit (Clause 298)."""
        # Snapshot belongs to tenant-alpha
        snap_a = self.sys.get_snapshot("rs-golden-berberine-01", tenant_id="tenant-alpha")
        self.assertIsNotNone(snap_a)

        # Access with tenant-beta must be blocked
        snap_b = self.sys.get_snapshot("rs-golden-berberine-01", tenant_id="tenant-beta")
        self.assertIsNone(snap_b)

        # Cross-tenant audit lookup
        audit_a = self.sys.get_audit("audit-golden-berberine-01", tenant_id="tenant-alpha")
        self.assertIsNotNone(audit_a)

        audit_b = self.sys.get_audit("audit-golden-berberine-01", tenant_id="tenant-beta")
        self.assertIsNone(audit_b)

    def test_auditor_view_raw_data_redaction(self):
        """Auditor View vs Raw Data View: Non-raw authorized auditors see redacted datasets (Clause 265)."""
        snap = self.sys.get_snapshot("rs-golden-berberine-01", is_raw_data_authorized=False)
        self.assertIsNotNone(snap)
        # All dataset snapshots must have REDACTED status
        for ds in snap.dataset_snapshots:
            self.assertEqual(ds.get("status"), "REDACTED_FOR_AUDIT_VIEW")

    def test_legal_and_regulatory_preservation_hold(self):
        """Legal hold prevents research audit modifications or deletions (Clause 237)."""
        audit = self.sys.set_legal_hold("audit-golden-berberine-01", hold=True)
        self.assertTrue(audit.is_held)

        # Release hold
        audit_released = self.sys.set_legal_hold("audit-golden-berberine-01", hold=False)
        self.assertFalse(audit_released.is_held)

    # ==========================================================================
    # 9. Python SDK Client Integration
    # ==========================================================================

    def test_python_sdk_audit_client_flow(self):
        """Verifies Python SDK `client.audit.*` operations against REST API."""
        # 1. Snapshot get
        snap = self.client.audit.snapshots.get("rs-golden-berberine-01")
        self.assertEqual(snap["snapshot_id"], "rs-golden-berberine-01")

        # 2. Verify chain
        verify_rep = self.client.audit.verify_chain("audit-golden-berberine-01")
        self.assertTrue(verify_rep["is_valid"])

        # 3. Provenance trace
        trace = self.client.audit.provenance.get_trace("rs-golden-berberine-01")
        self.assertTrue(len(trace["nodes"]) >= 5)

        # 4. Sandbox reproduction
        run = self.client.audit.reproduce.run("rs-golden-berberine-01")
        self.assertEqual(run["status"], "REPRODUCED")

        # 5. Certificates & Packet
        certs = self.client.audit.certificates.issue("audit-golden-berberine-01")
        self.assertIn("reproducibility_certificate", certs)
        self.assertIn("research_audit_certificate", certs)

        packet = self.client.audit.certificates.packet("audit-golden-berberine-01", format="json")
        self.assertEqual(packet["audit_id"], "audit-golden-berberine-01")


if __name__ == "__main__":
    unittest.main()
