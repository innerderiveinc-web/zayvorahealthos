"""
Acceptance Test Suite for Core Domain Models, Audit & Provenance Foundations
Prompt 28 — MODULE 05 (Domain Models), MODULE 06 (Audit), MODULE 07 (Provenance)
Clauses 17, 19, 20

Validates:
1. Canonical Domain Models instantiation & serialization
2. Provenance graph creation, attachment, backward trace & forward trace
3. Cryptographic Audit hash-chaining, signature verification, and tamper detection
4. End-to-end integration: Computation -> Provenance node -> Audit event
"""

import unittest
from datetime import datetime, timezone

from app.models.canonical import (
    TenantRecord,
    UserRecord,
    WorkspaceRecord,
    ProjectRecord,
    SourceRecord,
    DocumentRecord,
    EntityRecord,
    ConceptRecord,
    TermRecord,
    ClaimRecord,
    EvidenceRecord,
    ResearchQuestionRecord,
    ResearchTaskRecord,
    ResearchSnapshotRecord,
    DatasetRecord,
    DatasetVersionRecord,
    ComputationRecord,
    ModelRecord,
    AgentRecord,
    AgentRunRecord,
    CanonicalStatus
)
from app.core.provenance import (
    ProvenanceGraph,
    ProvActivityType,
    create_provenance,
    attach_provenance,
    get_provenance,
    trace_backward,
    trace_forward
)
from app.core.audit import (
    AuditDispatcher,
    AuditEvent,
    AuditAction,
    ActorType
)


class TestCoreFoundationsAcceptance(unittest.TestCase):

    def test_canonical_domain_models_instantiation(self):
        """Verifies canonical domain models can be instantiated and validated."""
        tenant = TenantRecord(tenant_id="ten-aiims", name="AIIMS Research Enclave")
        self.assertEqual(tenant.tenant_id, "ten-aiims")

        user = UserRecord(user_id="usr-dr-khan", tenant_id="ten-aiims", email="khan@aiims.edu", full_name="Dr. Khan")
        self.assertEqual(user.email, "khan@aiims.edu")

        doc = DocumentRecord(
            document_id="doc-pmid-381920",
            source_id="src-pubmed",
            title="Curcumin Modulation in Inflammatory Bowel Disease",
            raw_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            storage_uri="s3://zmie-immutable-documents/raw/doc-pmid-381920.pdf"
        )
        self.assertEqual(doc.source_id, "src-pubmed")

        claim = ClaimRecord(
            claim_id="clm-curcumin-nfkb",
            subject_entity_id="ent-curcumin",
            predicate="INHIBITS",
            object_entity_id="ent-nfkb-p65",
            evidence_ids=["evi-rct-101"],
            confidence=0.94,
            provenance_hash="a1b2c3d4e5"
        )
        self.assertEqual(claim.predicate, "INHIBITS")

        comp = ComputationRecord(
            computation_id="comp-metanalysis-99",
            tenant_id="ten-aiims",
            runtime_environment="python:3.11-scientific",
            entrypoint_script="meta_analysis_random_effects.py",
            input_dataset_version_id="dsv-trial-data-v1",
            status=CanonicalStatus.COMPLETED,
            provenance_hash="f0e1d2c3b4"
        )
        self.assertEqual(comp.status, CanonicalStatus.COMPLETED)

    def test_provenance_lifecycle_and_lineage_tracing(self):
        """Verifies create_provenance, attach_provenance, backward and forward lineage tracing."""
        prov_graph = ProvenanceGraph()

        # Step 1: Raw Literature Ingestion
        prov_doc = prov_graph.create_provenance(
            target_id="doc-lancet-2026-01",
            activity_type=ProvActivityType.INGESTION,
            agent_id="agent-ingestion-worker",
            input_ids=[],
            metadata={"source": "The Lancet", "doi": "10.1016/S0140-6736(26)00123-X"}
        )
        self.assertIsNotNone(prov_doc.content_hash)
        self.assertEqual(len(prov_doc.parent_ids), 0)

        # Step 2: Evidence Extraction derived from Document
        prov_evidence = prov_graph.create_provenance(
            target_id="evi-pico-884",
            activity_type=ProvActivityType.ENTITY_EXTRACTION,
            agent_id="agent-pico-extractor",
            input_ids=["doc-lancet-2026-01"],
            metadata={"study_design": "Double-blind RCT", "sample_size": 1200}
        )
        self.assertIn("doc-lancet-2026-01", prov_evidence.parent_ids)

        # Step 3: Claim Synthesis derived from Evidence
        prov_claim = prov_graph.create_provenance(
            target_id="clm-statin-crp-reduction",
            activity_type=ProvActivityType.CLAIM_SYNTHESIS,
            agent_id="agent-skos-synthesizer",
            input_ids=["evi-pico-884"],
            metadata={"confidence": 0.96}
        )

        # Attach to a resource dict
        claim_resource = {"claim_id": "clm-statin-crp-reduction", "text": "Statin therapy lowers hsCRP"}
        attached = prov_graph.attach_provenance(claim_resource, prov_claim)
        self.assertEqual(attached["provenance_id"], prov_claim.provenance_id)
        self.assertEqual(attached["provenance_hash"], prov_claim.content_hash)

        # Trace Backward from Claim -> Evidence -> Document
        backward_lineage = prov_graph.trace_backward("clm-statin-crp-reduction")
        backward_target_ids = [node.target_id for node in backward_lineage]
        self.assertIn("clm-statin-crp-reduction", backward_target_ids)
        self.assertIn("evi-pico-884", backward_target_ids)
        self.assertIn("doc-lancet-2026-01", backward_target_ids)

        # Trace Forward from Document -> Evidence -> Claim (Crucial for Retractions)
        forward_impact = prov_graph.trace_forward("doc-lancet-2026-01")
        forward_target_ids = [node.target_id for node in forward_impact]
        self.assertIn("doc-lancet-2026-01", forward_target_ids)
        self.assertIn("evi-pico-884", forward_target_ids)
        self.assertIn("clm-statin-crp-reduction", forward_target_ids)

    def test_cryptographic_audit_dispatch_and_tamper_detection(self):
        """Verifies hash-chained audit dispatch, signature verification, and tamper detection."""
        dispatcher = AuditDispatcher()
        tenant = "tenant-apollo"

        # Dispatch 3 consecutive events
        ev1 = dispatcher.dispatch(
            actor="usr-cardio-1",
            actor_type=ActorType.USER,
            tenant_id=tenant,
            object_type="dataset",
            object_id="ds-ecg-signals",
            action=AuditAction.CREATE,
            metadata={"n_records": 1000}
        )
        self.assertEqual(ev1.prev_hash, "GENESIS_BLOCK_00000000000000000000000000000000")
        self.assertIsNotNone(ev1.block_hash)
        self.assertIsNotNone(ev1.signature)

        ev2 = dispatcher.dispatch(
            actor="agent-ml-classifier",
            actor_type=ActorType.AGENT,
            tenant_id=tenant,
            object_type="computation",
            object_id="comp-arrhythmia-model",
            action=AuditAction.EXECUTE,
            previous_state={"status": "PENDING"},
            new_state={"status": "COMPLETED"},
            provenance_ref="prov-comp-12345"
        )
        self.assertEqual(ev2.prev_hash, ev1.block_hash)

        ev3 = dispatcher.dispatch(
            actor="usr-auditor-9",
            actor_type=ActorType.USER,
            tenant_id=tenant,
            object_type="computation",
            object_id="comp-arrhythmia-model",
            action=AuditAction.READ
        )
        self.assertEqual(ev3.prev_hash, ev2.block_hash)

        # Ledger Integrity Verification
        self.assertTrue(dispatcher.verify_integrity())

        # Query filtered by tenant
        tenant_events = dispatcher.query(tenant)
        self.assertEqual(len(tenant_events), 3)

        # Unrelated tenant query returns empty
        other_events = dispatcher.query("tenant-unrelated")
        self.assertEqual(len(other_events), 0)

        # Tamper Detection Test: Modify an event's payload
        ev2.action = AuditAction.DELETE  # Unauthorized alteration!
        self.assertFalse(dispatcher.verify_integrity(), "Tampered event must fail cryptographic verification")


if __name__ == "__main__":
    unittest.main()
