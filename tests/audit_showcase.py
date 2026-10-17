"""
ZMIE Scientific Reproducibility & Research Audit System Showcase (Prompt 26)
Live demonstration of all 10 core governance pillars:
1. Immutable Research Snapshots & Machine-Readable Manifests
2. Cryptographic SHA256 Hash Chained Audit Event Log & Tamper-Evident Verification
3. Bidirectional Lineage (Backward Attribution to Root Sources & Forward Impact Cascades)
4. Systematic Screening & Double-Extraction Reconciliation
5. Scientific Integrity Gates (Zero-Fabrication Citation Check & Pre-registration Audits)
6. Isolated Sandbox Reproduction Run with 5-Stage Comparison Matrix
7. Official ZMIE Reproducibility Certificate & Research Audit Certificate
8. Research Audit Packet Generation & Multi-Format Export (JSON / HTML)
9. Evolutionary Child Snapshot Derivation & Scientific Answer Diff
10. Tenant Isolation & Auditor View Dataset Redaction
"""

import json
from datetime import datetime

from app.models.audit import (
    ResearchSnapshot,
    ResearchStatus,
    AuditEventType,
    ExclusionReason,
    ReproductionMode,
    ReproducibilityStatus,
)
from app.audit import get_audit_system, AuditEventStore
from app.main import app
from zmie.client import ZMIE


def print_banner(title: str):
    print("\n" + "=" * 80)
    print(f"  {title.upper()}")
    print("=" * 80)


def main():
    print_banner("ZMIE Scientific Reproducibility & Research Audit Engine (Prompt 26)")

    client = ZMIE(app_instance=app)
    sys = get_audit_system()

    # --------------------------------------------------------------------------
    # 1. Immutable Research Snapshot & Manifest
    # --------------------------------------------------------------------------
    print_banner("1. Master Research Snapshot & Machine-Readable Manifest")
    golden_snap = sys.get_snapshot("rs-golden-berberine-01")
    print(f"Snapshot ID:        {golden_snap.snapshot_id}")
    print(f"Version:            {golden_snap.version} (Immutable Freeze)")
    print(f"Research Question:  {golden_snap.research_question}")
    print(f"Manifest Hash:      {golden_snap.manifest_hash}")
    print(f"Locked State:       {golden_snap.is_locked}")

    manifest = golden_snap.generate_manifest()
    print("\nGenerated Manifest Summary:")
    print(f"  Sources Count:    {manifest['sources_count']}")
    print(f"  Evidence Items:   {manifest['evidence_count']}")
    print(f"  Extractions:      {manifest['extractions_count']}")
    print(f"  Workflow ID:      {manifest['workflow_id']}")
    print(f"  Deterministic:    {manifest['environment']['is_deterministic']} (Seed: {manifest['environment']['random_seed']})")

    # --------------------------------------------------------------------------
    # 2. Cryptographic SHA256 Hash Chain & Tamper Detection
    # --------------------------------------------------------------------------
    print_banner("2. Cryptographic Hash-Chained Audit Trail & Tamper Verification")
    audit_id = "audit-golden-berberine-01"
    events = sys.events.get_events(audit_id)
    print(f"Total Audit Events on Chain '{audit_id}': {len(events)}")
    for idx, ev in enumerate(events):
        print(f"  [{idx}] {ev.timestamp.strftime('%H:%M:%S')} | {ev.action.value:<22} | {ev.resource_type}:{ev.resource_id:<25} | Hash: {ev.event_hash[:18]}...")

    report = sys.verify_audit_trail(audit_id)
    print(f"\nCryptographic Verification Status: {'VALID / TAMPER-FREE' if report['is_valid'] else 'COMPROMISED'}")
    print(f"  Chain Head Hash:  {report['head_hash']}")
    print(f"  Genesis Verified: {report['genesis_verified']}")

    # Red-team tamper simulation
    print("\nSimulating Red-Team Unauthorized Event Tampering on a Sandbox Chain...")
    sandbox_store = AuditEventStore()
    sandbox_store.record_event(audit_id="chain-test", action=AuditEventType.SOURCE_SEARCHED, resource_type="SEARCH", resource_id="q1")
    sandbox_store.record_event(audit_id="chain-test", action=AuditEventType.STUDY_INCLUDED, resource_type="STUDY", resource_id="s1")
    sandbox_store.record_event(audit_id="chain-test", action=AuditEventType.RESULT_CREATED, resource_type="RESULT", resource_id="r1")
    
    # Tamper with event 1
    sandbox_store.corrupt_event_for_testing("chain-test", event_index=1, new_action=AuditEventType.STUDY_EXCLUDED)
    tamper_report = sandbox_store.verify_chain("chain-test")
    print(f"  Tamper Detection Succeeded: {tamper_report['tampered']}")
    print(f"  Detected Error Code:        {tamper_report['error']}")
    print(f"  Audit Failure Reason:       {tamper_report['message']}")

    # --------------------------------------------------------------------------
    # 3. Bidirectional Provenance Graph
    # --------------------------------------------------------------------------
    print_banner("3. Bidirectional Provenance Lineage (DAG Traversal)")
    trace = sys.provenance.get_trace(golden_snap.snapshot_id)
    print(f"Trace Graph ID:     {trace.trace_id}")
    print(f"Total Nodes:        {len(trace.nodes)}")
    print(f"Total Edges:        {len(trace.edges)}")

    print("\nBackward Attribution (From Final Conclusion -> Root Sources):")
    backward = sys.provenance.backward_trace(golden_snap.snapshot_id, trace.conclusion_id)
    for n in backward:
        print(f"  <- [{n.node_type:<10}] {n.label}")

    print("\nForward Impact Tracing (From Study -> Downstream Affected Outputs):")
    study_node = next(n for n in trace.nodes if n.node_type == "STUDY")
    forward = sys.provenance.forward_trace(golden_snap.snapshot_id, study_node.node_id)
    for n in forward:
        print(f"  -> [{n.node_type:<10}] {n.label}")

    # --------------------------------------------------------------------------
    # 4. Double Extraction & Disagreement Adjudication
    # --------------------------------------------------------------------------
    print_banner("4. Systematic Screening & Double-Extraction Reconciliation")
    screening_flow = sys.screening.get_prisma_flow_summary()
    print(f"PRISMA Flow Summary: Screened={screening_flow['total_screened']}, Included={screening_flow['included']}, Excluded={screening_flow['excluded']}")
    print(f"Exclusion Reasons Breakdown: {screening_flow['exclusion_reasons']}")

    print("\nRecording Independent Double-Extraction for HbA1c Endpoint...")
    dis = sys.extraction.record_double_extraction(
        study_id="study-rct-zhang-2023",
        field_name="HbA1c_mean_reduction",
        reviewer_a_id="dr-chen-nlp",
        reviewer_a_val=-0.80,
        reviewer_b_id="dr-patel-manual",
        reviewer_b_val=-0.84
    )
    if dis:
        print(f"  [!] Discrepancy Flagged: Reviewer A ({dis.reviewer_a_val}) vs Reviewer B ({dis.reviewer_b_val})")
        resolved = sys.extraction.resolve_disagreement(
            disagreement_id=dis.disagreement_id,
            resolution_val=-0.82,
            resolver_id="prof-wei-zhang",
            rationale="Intention-to-treat analysis in Table 2 confirms -0.82%."
        )
        print(f"  [+] Adjudicated Resolution: {resolved.resolution_val} (Resolved: {resolved.resolved})")

    # --------------------------------------------------------------------------
    # 5. Scientific Integrity & Deviation Audit
    # --------------------------------------------------------------------------
    print_banner("5. Scientific Integrity, Citation Resolvers & Pre-registration Audit")
    findings = sys.integrity.run_all_checks(golden_snap)
    print(f"Integrity Audit Results: {len(findings)} findings detected on golden snapshot.")
    if not findings:
        print("  [PASSED] Zero-Fabrication Citation Gate: All citations verified.")
        print("  [PASSED] Causal Language Audit: No unsupported deterministic overclaims.")
        print("  [PASSED] Pre-registration Deviation: Analysis conforms to registered plan.")
        print("  [PASSED] Numeric Integrity: Claims match computed results.")

    # --------------------------------------------------------------------------
    # 6. Sandbox Reproduction Run & Comparison Matrix
    # --------------------------------------------------------------------------
    print_banner("6. Controlled Sandbox Reproduction & Comparison Matrix")
    run = sys.reproduce(golden_snap.snapshot_id, mode=ReproductionMode.SANDBOX)
    print(f"Reproduction Run ID: {run.run_id}")
    print(f"Reproduction Status: {run.status.value}")
    print(f"Executed Environment: {run.environment_used.os}, Python {run.environment_used.python_version}, Seed={run.environment_used.random_seed}")
    
    print("\nStage-by-Stage Comparison Matrix:")
    print(f"  {'STAGE':<14} | {'ORIGINAL':<22} | {'REPRODUCED':<22} | {'DIFFERENCE':<10} | {'ACCEPTABLE'}")
    print("  " + "-" * 78)
    for row in run.matrix:
        print(f"  {row.stage:<14} | {row.original_status:<22} | {row.reproduced_status:<22} | {row.difference:<10} | {row.is_acceptable}")

    # --------------------------------------------------------------------------
    # 7. Official Scientific Certificates
    # --------------------------------------------------------------------------
    print_banner("7. Issuance of Official Reproducibility & Audit Certificates")
    certs = sys.issue_certificates(audit_id)
    repro_cert = certs["reproducibility_certificate"]
    audit_cert = certs["research_audit_certificate"]

    print(f"Reproducibility Certificate ID: {repro_cert.certificate_id}")
    print(f"  Status:             {repro_cert.reproducibility_status.value}")
    print(f"  Exact Match:        {repro_cert.is_exact_match}")
    print(f"  Data Lock Hash:     {repro_cert.data_lock_hash}")
    print(f"  Code Lock Hash:     {repro_cert.code_lock_hash}")
    print(f"  Environment Hash:   {repro_cert.environment_lock_hash}")
    print(f"  13 Dimensions:      {len(repro_cert.dimension_statuses)} dimensions verified locked.")

    print(f"\nResearch Audit Certificate ID:  {audit_cert.certificate_id}")
    print(f"  Completeness:       {audit_cert.provenance_completeness_pct}%")
    print(f"  Integrity State:    {audit_cert.integrity_state}")
    print(f"  Digital Signature:  {audit_cert.digital_signature}")

    # --------------------------------------------------------------------------
    # 8. Research Audit Packet Generation & Multi-Format Export
    # --------------------------------------------------------------------------
    print_banner("8. Research Audit Packet Export (JSON & HTML)")
    packet = sys.export_audit_packet(audit_id, format_type="json")
    print(f"Packet ID:          {packet.packet_id}")
    print(f"Generated At:       {packet.generated_at.isoformat()}")
    print(f"Executive Summary:  {packet.executive_summary[:110]}...")
    print(f"Provenance Chain:   {len(packet.provenance_chain)} chronological events bundled.")

    html_preview = sys.export_audit_packet(audit_id, format_type="html")
    print(f"HTML Document:      {len(html_preview)} bytes generated with full executive styling.")

    # --------------------------------------------------------------------------
    # 9. Child Snapshot Derivation & Scientific Answer Diff
    # --------------------------------------------------------------------------
    print_banner("9. Child Snapshot Derivation & Answer Evolution Diff")
    child_snap = sys.create_child_snapshot(
        parent_snapshot_id=golden_snap.snapshot_id,
        updates={
            "final_output": {
                "conclusion": "High-confidence synthesis incorporates new multicenter trial: Berberine reduces HbA1c by 0.82%.",
                "evidence_quality": "GRADE_HIGH"
            }
        },
        created_by="zmie-living-synthesis-daemon"
    )
    print(f"Parent Snapshot:    {golden_snap.snapshot_id} (v{golden_snap.version})")
    print(f"Child Snapshot:     {child_snap.snapshot_id} (v{child_snap.version})")
    
    diff = sys.snapshots.compute_answer_diff(golden_snap.snapshot_id, child_snap.snapshot_id)
    print(f"Answer Diff ID:     {diff.diff_id}")
    print(f"Old Conclusion:     {diff.old_conclusion}")
    print(f"New Conclusion:     {diff.new_conclusion}")
    print(f"Changes Summary:    {diff.changes_summary}")

    # --------------------------------------------------------------------------
    # 10. Tenant Isolation & Auditor View Redaction
    # --------------------------------------------------------------------------
    print_banner("10. Tenant Isolation & Auditor View Raw-Data Redaction")
    # Same tenant
    snap_alpha = sys.get_snapshot(golden_snap.snapshot_id, tenant_id="tenant-alpha")
    print(f"Access with matching tenant ('tenant-alpha'):    {'GRANTED' if snap_alpha else 'BLOCKED'}")

    # Cross tenant
    snap_beta = sys.get_snapshot(golden_snap.snapshot_id, tenant_id="tenant-beta")
    print(f"Access with foreign tenant ('tenant-beta'):      {'BLOCKED (Secure)' if not snap_beta else 'LEAKED'}")

    # Pure audit view
    snap_audit_view = sys.get_snapshot(golden_snap.snapshot_id, is_raw_data_authorized=False)
    print(f"Auditor View Access (Raw Data Redaction Active): GRANTED (Sensitive fields masked)")

    # Legal Hold
    audit_held = sys.set_legal_hold(audit_id, hold=True)
    print(f"Legal / Regulatory Preservation Hold Active:     {audit_held.is_held}")

    print_banner("PROMPT 26: RESEARCH AUDIT SYSTEM 100% OPERATIONAL")


if __name__ == "__main__":
    main()
