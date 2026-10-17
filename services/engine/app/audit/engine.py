"""
ZMIE Master Research Audit System (Prompt 26)
Orchestrates Snapshots, Cryptographic Hash Chains, Provenance Lineage, Screening & Extraction Audits,
Integrity Checks, Sandbox Reproduction, Scientific Certificates, and Tenant Isolation (Clauses 1-286).
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import copy
import logging

from app.models.audit import (
    ResearchSnapshot,
    ResearchAudit,
    AuditEvent,
    AuditEventType,
    AuditActorType,
    AuditFinding,
    AuditFindingSeverity,
    AuditFindingStatus,
    ReproducibilityStatus,
    ReproductionMode,
    ReproductionRun,
    ZMIEReproducibilityCertificate,
    ZMIEResearchAuditCertificate,
    ResearchAuditPacket,
    ScientificAnswerDiff,
    ScientificResearchTrace,
    SearchStrategyRecord,
    ScreeningDecision,
    ExtractionRecord,
    ExtractionDisagreement,
    AnalysisPlanRecord,
    AnalysisDeviation,
    EnvironmentSpec,
    CodeProvenance,
    ExclusionReason,
)
from app.models.federated_privacy import ResearchDataClassification
from app.audit.event_store import AuditEventStore
from app.audit.snapshots import SnapshotManager
from app.audit.provenance_graph import ResearchProvenanceGraph
from app.audit.screening_extraction import ScreeningAuditManager, ExtractionAuditManager
from app.audit.integrity_checks import ScientificIntegrityAuditor
from app.audit.reproduction_engine import ReproductionEngine
from app.audit.certificates import CertificateIssuer

logger = logging.getLogger("zmie.audit.engine")


class ResearchAuditSystem:
    """
    Master operational engine for ZMIE Scientific Reproducibility & Research Audit System.
    """

    def __init__(self):
        self.snapshots = SnapshotManager()
        self.events = AuditEventStore()
        self.provenance = ResearchProvenanceGraph()
        self.screening = ScreeningAuditManager()
        self.extraction = ExtractionAuditManager()
        self.integrity = ScientificIntegrityAuditor()
        self.reproduction = ReproductionEngine()
        self.certificates = CertificateIssuer()

        # Key: audit_id -> ResearchAudit
        self._audits: Dict[str, ResearchAudit] = {}

        # Seed initial golden research audit for operational out-of-the-box readiness
        self._seed_golden_scenario()

    def _seed_golden_scenario(self) -> None:
        """Seeds the golden research audit scenario (Berberine T2D Glycemic Synthesis, Clauses 251, 291)."""
        snapshot_id = "rs-golden-berberine-01"
        audit_id = "audit-golden-berberine-01"

        search_strat = SearchStrategyRecord(
            query_id="qry-berberine-t2d-01",
            original_query="Berberine glycemic control type 2 diabetes HbA1c fasting glucose randomized controlled trial",
            normalized_query="berberine AND type 2 diabetes AND glycemic control AND RCT",
            terminology_expansions=["C20H18NO4+", "T2D", "HbA1c", "Huanglian", "Coptis chinensis"],
            filters={"study_type": "RCT", "min_sample_size": 30},
            source_classes=["PubMed", "TKDL", "Europe PMC", "ClinicalTrials.gov"],
            results_count=42,
            checksum="sha256:search-berberine-v1-hash"
        )

        scr1 = self.screening.record_decision(
            study_id="study-rct-zhang-2023",
            study_title="Berberine vs Metformin in Newly Diagnosed Type 2 Diabetes: A Multicenter Randomized Double-Blind Trial",
            decision="INCLUDED",
            doi="10.1016/j.metabol.2023.155432",
            screener_id="screener-agent-01"
        )
        scr2 = self.screening.record_decision(
            study_id="study-obs-li-2022",
            study_title="Retrospective Cohort of Botanical Therapeutics in Metabolic Syndrome",
            decision="EXCLUDED",
            reason=ExclusionReason.WRONG_STUDY_DESIGN,
            detailed_reason="Observational retrospective design without randomization.",
            screener_id="screener-agent-01"
        )

        ext1 = self.extraction.record_extraction(
            study_id="study-rct-zhang-2023",
            field_name="HbA1c_mean_reduction",
            original_source_value="-0.82%",
            normalized_value=-0.82,
            unit="percent",
            page_or_table="Table 2, page 14",
            extractor_id="extractor-agent-01",
            review_state="CONSENSUS_VERIFIED"
        )

        plan = AnalysisPlanRecord(
            plan_id="plan-berberine-meta-01",
            research_question="What is the comparative efficacy of Berberine on HbA1c reduction in T2D?",
            hypothesis="Berberine 500mg TID reduces HbA1c significantly more than placebo and non-inferior to Metformin.",
            estimand="AVERAGE_TREATMENT_EFFECT",
            population="Adults aged 18-70 with T2D, baseline HbA1c 7.5-9.5%",
            intervention="Berberine hydrochloride 500mg thrice daily",
            comparator="Metformin 500mg thrice daily or Placebo",
            outcome="Mean change in HbA1c at 12 weeks",
            analysis_method="Random-Effects Meta-Analysis with DerSimonian-Laird Estimator",
            is_preregistered=True,
            preregistration_url="https://osf.io/zmie-berberine-t2d-plan"
        )

        code_prov = CodeProvenance(
            repo_url="https://github.com/zayvora/zmie",
            commit_hash="7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1f",
            file_path="services/engine/app/scientific_compute/meta_analysis.py",
            checksum="sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
            version_tag="1.0.0-enterprise"
        )

        golden_snapshot = ResearchSnapshot(
            snapshot_id=snapshot_id,
            version="1.0.0",
            project_id="proj-metabolic-frontier",
            tenant_id="tenant-alpha",
            classification=ResearchDataClassification.PUBLIC,
            research_question="What is the comparative efficacy and glycemic impact of Berberine in Type 2 Diabetes?",
            question_version="1.0",
            search_strategy=search_strat,
            sources_used=[
                {"source_id": "src-pubmed", "name": "PubMed / MEDLINE", "type": "BIOMEDICAL_LITERATURE"},
                {"source_id": "src-tkdl", "name": "Traditional Knowledge Digital Library", "type": "HERBAL_FORMULARY"}
            ],
            evidence_items=[
                {"study_id": "study-rct-zhang-2023", "title": scr1.study_title, "doi": scr1.doi, "design": "RCT", "sample_size": 240}
            ],
            screening_decisions=[scr1, scr2],
            extractions=[ext1],
            analysis_plan=plan,
            code_provenance=code_prov,
            workflow_id="wf-meta-synthesis-v1",
            environment=EnvironmentSpec(random_seed=42, is_deterministic=True),
            results=[
                {"name": "HbA1c_mean_difference", "value": -0.78, "unit": "percentage_points", "ci_95": [-0.92, -0.64], "p_value": 0.001}
            ],
            claims=[
                {
                    "claim_id": "clm-berberine-01",
                    "statement": "Berberine supplementation (500mg TID) demonstrates statistically significant reduction in HbA1c (-0.78% [95% CI -0.92 to -0.64]) comparable to standard oral hypoglycemics in adult T2D cohorts.",
                    "citations": ["study-rct-zhang-2023"],
                    "metric_referenced": "HbA1c_mean_difference",
                    "numeric_value": -0.78
                }
            ],
            final_output={
                "conclusion": "High-confidence living synthesis demonstrates Berberine reduces HbA1c by 0.78 percentage points with acceptable tolerability.",
                "evidence_quality": "GRADE_MODERATE"
            },
            is_locked=True
        )

        self.snapshots.save_snapshot(golden_snapshot)
        self.provenance.build_trace(golden_snapshot)

        # Record initial audit event chain
        self.events.record_event(
            audit_id=audit_id,
            action=AuditEventType.SOURCE_SEARCHED,
            resource_type="SEARCH",
            resource_id=search_strat.query_id,
            actor_id="agent-search-orchestrator",
            reason="Initial systematic discovery sweep."
        )
        self.events.record_event(
            audit_id=audit_id,
            action=AuditEventType.STUDY_INCLUDED,
            resource_type="STUDY",
            resource_id="study-rct-zhang-2023",
            actor_id="screener-agent-01",
            reason="Met all RCT inclusion criteria."
        )
        self.events.record_event(
            audit_id=audit_id,
            action=AuditEventType.EXTRACTION_CREATED,
            resource_type="EXTRACTION",
            resource_id=ext1.record_id,
            actor_id="extractor-agent-01",
            reason="Extracted HbA1c effect size."
        )
        self.events.record_event(
            audit_id=audit_id,
            action=AuditEventType.ANALYSIS_COMPLETED,
            resource_type="ANALYSIS",
            resource_id=plan.plan_id,
            actor_id="service-meta-analyzer",
            reason="DerSimonian-Laird pooling converged."
        )
        self.events.record_event(
            audit_id=audit_id,
            action=AuditEventType.SNAPSHOT_CREATED,
            resource_type="SNAPSHOT",
            resource_id=golden_snapshot.snapshot_id,
            actor_id="zmie-orchestrator",
            reason="Master publication-grade snapshot locked."
        )

        # Create audit record
        audit = ResearchAudit(
            audit_id=audit_id,
            snapshot_id=snapshot_id,
            project_id="proj-metabolic-frontier",
            tenant_id="tenant-alpha",
            researcher="Prof. Wei Zhang, MD, PhD",
            study_name="Berberine T2D Glycemic Synthesis",
            question=golden_snapshot.research_question,
            status="VALID",
            verification_passed=True,
            reproducibility_status=ReproducibilityStatus.REPRODUCED,
            events_count=5
        )
        self._audits[audit.audit_id] = audit
        logger.info(f"Initialized Golden Research Audit scenario: {audit_id}")

    # ==========================================================================
    # Snapshot Operations (Clauses 5-9)
    # ==========================================================================

    def create_snapshot(self, snapshot: ResearchSnapshot) -> ResearchSnapshot:
        """Registers and locks a new research snapshot."""
        saved = self.snapshots.save_snapshot(snapshot)
        self.provenance.build_trace(saved)
        return saved

    def get_snapshot(
        self,
        snapshot_id: str,
        tenant_id: Optional[str] = None,
        is_raw_data_authorized: bool = True
    ) -> Optional[ResearchSnapshot]:
        """
        Retrieves snapshot enforcing tenant isolation and auditor view redaction.
        """
        snap = self.snapshots.get_snapshot(snapshot_id)
        if not snap:
            return None

        # Tenant isolation check
        if snap.tenant_id and tenant_id and snap.tenant_id != tenant_id:
            logger.warning(f"Tenant isolation mismatch: snapshot {snap.tenant_id} != caller {tenant_id}")
            return None

        if not is_raw_data_authorized:
            # Mask sensitive raw dataset records for pure audit view
            snap_copy = copy.deepcopy(snap)
            snap_copy.dataset_snapshots = [
                {"dataset_id": d.get("dataset_id", "masked"), "record_count": d.get("record_count", 0), "status": "REDACTED_FOR_AUDIT_VIEW"}
                for d in snap_copy.dataset_snapshots
            ]
            return snap_copy

        return snap

    def create_child_snapshot(
        self,
        parent_snapshot_id: str,
        updates: Dict[str, Any],
        created_by: str = "zmie-research-updater",
        tenant_id: Optional[str] = None
    ) -> ResearchSnapshot:
        """Derives a new child snapshot, enforcing immutability of parent."""
        parent = self.snapshots.get_snapshot(parent_snapshot_id)
        if not parent:
            raise KeyError(f"Parent snapshot {parent_snapshot_id} does not exist.")

        # Check tenant authorization
        if parent.tenant_id and tenant_id and parent.tenant_id != tenant_id:
            raise PermissionError("Cross-tenant modification prohibited.")

        child = self.snapshots.create_child_snapshot(parent_snapshot_id, updates, created_by=created_by)
        self.provenance.build_trace(child)
        return child

    # ==========================================================================
    # Audit & Verification Operations (Clauses 10-14, 163-165)
    # ==========================================================================

    def create_audit(
        self,
        snapshot_id: str,
        researcher: str,
        study_name: str,
        project_id: Optional[str] = None,
        tenant_id: Optional[str] = None
    ) -> ResearchAudit:
        """Initializes a new formal research audit for a snapshot."""
        snapshot = self.snapshots.get_snapshot(snapshot_id)
        if not snapshot:
            raise KeyError(f"Snapshot {snapshot_id} not found.")

        # Run integrity checks
        findings = self.integrity.run_all_checks(snapshot)
        has_critical = any(f.severity == AuditFindingSeverity.CRITICAL for f in findings)

        audit = ResearchAudit(
            snapshot_id=snapshot_id,
            project_id=project_id or snapshot.project_id,
            tenant_id=tenant_id or snapshot.tenant_id,
            researcher=researcher,
            study_name=study_name,
            question=snapshot.research_question,
            status="ISSUE_FOUND" if has_critical else "VALID",
            verification_passed=(not has_critical),
            findings=findings,
            events_count=len(self.events.get_events(f"audit-{snapshot_id}"))
        )

        self._audits[audit.audit_id] = audit

        # Record audit created event
        self.events.record_event(
            audit_id=audit.audit_id,
            action=AuditEventType.SNAPSHOT_CREATED,
            resource_type="AUDIT",
            resource_id=audit.audit_id,
            actor_id=researcher,
            reason="Research audit initialized."
        )

        return audit

    def get_audit(self, audit_id: str, tenant_id: Optional[str] = None) -> Optional[ResearchAudit]:
        """Retrieves an audit record with tenant isolation."""
        audit = self._audits.get(audit_id)
        if not audit:
            return None
        if audit.tenant_id and tenant_id and audit.tenant_id != tenant_id:
            return None
        return audit

    def verify_audit_trail(self, audit_id: str) -> Dict[str, Any]:
        """Verifies cryptographic hash chain of an audit trail."""
        return self.events.verify_chain(audit_id)

    def set_legal_hold(self, audit_id: str, hold: bool) -> ResearchAudit:
        """Sets or releases a legal/regulatory preservation hold (Clause 237)."""
        audit = self.get_audit(audit_id)
        if not audit:
            raise KeyError(f"Audit {audit_id} not found.")
        audit.is_held = hold
        audit.updated_at = datetime.utcnow()
        logger.info(f"Legal hold status on audit {audit_id} set to {hold}")
        return audit

    # ==========================================================================
    # Reproduction Operations (Clauses 87-90, 252)
    # ==========================================================================

    def reproduce(
        self,
        snapshot_id: str,
        mode: ReproductionMode = ReproductionMode.SANDBOX,
        simulated_drift: Optional[Dict[str, Any]] = None,
        tenant_id: Optional[str] = None
    ) -> ReproductionRun:
        """Executes sandbox reproduction for a research snapshot."""
        snapshot = self.get_snapshot(snapshot_id, tenant_id=tenant_id)
        if not snapshot:
            raise KeyError(f"Snapshot {snapshot_id} not found or inaccessible.")

        run = self.reproduction.run_reproduction(snapshot, mode=mode, simulated_drift=simulated_drift)

        # Log event on audit chain if exists
        audit_id = f"audit-{snapshot_id}"
        self.events.record_event(
            audit_id=audit_id,
            action=AuditEventType.SNAPSHOT_REPRODUCED,
            resource_type="REPRODUCTION_RUN",
            resource_id=run.run_id,
            actor_id="reproduction-sandbox",
            reason=f"Reproduction run completed with status {run.status.value}"
        )

        return run

    # ==========================================================================
    # Certificates & Export Operations (Clauses 101, 102, 215, 216)
    # ==========================================================================

    def issue_certificates(
        self,
        audit_id: str,
        tenant_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Issues official Reproducibility and Research Audit Certificates."""
        audit = self.get_audit(audit_id, tenant_id=tenant_id)
        if not audit:
            raise KeyError(f"Audit {audit_id} not found.")

        snapshot = self.snapshots.get_snapshot(audit.snapshot_id)
        if not snapshot:
            raise KeyError(f"Snapshot {audit.snapshot_id} not found.")

        repro_cert = self.certificates.issue_reproducibility_certificate(snapshot)
        audit_cert = self.certificates.issue_research_audit_certificate(audit, snapshot, self.events)

        return {
            "reproducibility_certificate": repro_cert,
            "research_audit_certificate": audit_cert
        }

    def export_audit_packet(
        self,
        audit_id: str,
        format_type: str = "json",
        tenant_id: Optional[str] = None
    ) -> Any:
        """Generates and exports complete Research Audit Packet."""
        audit = self.get_audit(audit_id, tenant_id=tenant_id)
        if not audit:
            raise KeyError(f"Audit {audit_id} not found.")

        snapshot = self.snapshots.get_snapshot(audit.snapshot_id)
        if not snapshot:
            raise KeyError(f"Snapshot {audit.snapshot_id} not found.")

        repro_cert = self.certificates.issue_reproducibility_certificate(snapshot)
        audit_cert = self.certificates.issue_research_audit_certificate(audit, snapshot, self.events)

        packet = self.certificates.generate_audit_packet(
            audit=audit,
            snapshot=snapshot,
            event_store=self.events,
            repro_cert=repro_cert,
            audit_cert=audit_cert
        )

        if format_type.lower() == "html":
            return self.certificates.export_packet_html(packet)
        return packet


# Global singleton instance
_audit_system_instance: Optional[ResearchAuditSystem] = None


def get_audit_system() -> ResearchAuditSystem:
    """Returns singleton instance of the ResearchAuditSystem."""
    global _audit_system_instance
    if _audit_system_instance is None:
        _audit_system_instance = ResearchAuditSystem()
    return _audit_system_instance
