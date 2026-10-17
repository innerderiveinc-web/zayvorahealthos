"""
ZMIE Scientific Reproducibility & Research Audit REST API Gateway (Prompt 26)
Exposes endpoints for immutable snapshots, cryptographic hash verification, bidirectional lineage,
sandbox reproduction, scientific certificates, and audit packets (Clauses 270-286).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Header, Query, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.audit import (
    get_audit_system,
    ResearchSnapshot,
    ResearchAudit,
    AuditEvent,
    AuditEventType,
    AuditActorType,
    ReproductionMode,
    ReproductionRun,
    ScientificAnswerDiff,
    ScientificResearchTrace,
    TraceNode,
    ResearchStatus,
)

router = APIRouter(prefix="/audit", tags=["Scientific Reproducibility & Research Audit"])


# ==============================================================================
# Request / Response Schemas
# ==============================================================================

class CreateSnapshotRequest(BaseModel):
    snapshot: ResearchSnapshot


class CreateChildSnapshotRequest(BaseModel):
    updates: Dict[str, Any]
    created_by: str = "zmie-research-updater"


class RecordEventRequest(BaseModel):
    audit_id: str
    action: AuditEventType
    resource_type: str
    resource_id: str
    actor_type: AuditActorType = AuditActorType.AGENT
    actor_id: str = "agent-researcher-01"
    before_state: Optional[Dict[str, Any]] = None
    after_state: Optional[Dict[str, Any]] = None
    reason: str = ""


class DiffSnapshotsRequest(BaseModel):
    old_snapshot_id: str
    new_snapshot_id: str


class ReproduceRequest(BaseModel):
    mode: ReproductionMode = ReproductionMode.SANDBOX
    simulated_drift: Optional[Dict[str, Any]] = None


class CreateAuditRecordRequest(BaseModel):
    snapshot_id: str
    researcher: str
    study_name: str
    project_id: Optional[str] = None


class SetLegalHoldRequest(BaseModel):
    hold: bool


# ==============================================================================
# 1. Snapshot Endpoints (Clauses 5-9, 280)
# ==============================================================================

@router.post("/snapshots", response_model=ResearchSnapshot, status_code=status.HTTP_201_CREATED)
def create_snapshot(req: CreateSnapshotRequest):
    """Creates and cryptographically locks a new publication-grade Research Snapshot."""
    sys = get_audit_system()
    try:
        return sys.create_snapshot(req.snapshot)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/snapshots", response_model=List[ResearchSnapshot])
def list_snapshots(
    project_id: Optional[str] = None,
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")
):
    """Lists research snapshots matching project and tenant boundaries."""
    sys = get_audit_system()
    return sys.snapshots.list_snapshots(project_id=project_id, tenant_id=x_tenant_id)


@router.get("/snapshots/{snapshot_id}", response_model=ResearchSnapshot)
def get_snapshot(
    snapshot_id: str,
    include_raw_data: bool = Query(True, description="False redacts row-level data for pure audit view"),
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")
):
    """Retrieves an immutable snapshot with optional auditor view redaction."""
    sys = get_audit_system()
    snap = sys.get_snapshot(snapshot_id, tenant_id=x_tenant_id, is_raw_data_authorized=include_raw_data)
    if not snap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Snapshot {snapshot_id} not found or inaccessible.")
    return snap


@router.post("/snapshots/{parent_snapshot_id}/child", response_model=ResearchSnapshot)
def derive_child_snapshot(
    parent_snapshot_id: str,
    req: CreateChildSnapshotRequest,
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")
):
    """Derives an immutable child snapshot from a parent, preserving full provenance."""
    sys = get_audit_system()
    try:
        return sys.create_child_snapshot(
            parent_snapshot_id=parent_snapshot_id,
            updates=req.updates,
            created_by=req.created_by,
            tenant_id=x_tenant_id
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get("/snapshots/{snapshot_id}/manifest", response_model=Dict[str, Any])
def get_snapshot_manifest(snapshot_id: str, x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")):
    """Retrieves machine-readable snapshot manifest with checksums."""
    sys = get_audit_system()
    snap = sys.get_snapshot(snapshot_id, tenant_id=x_tenant_id)
    if not snap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Snapshot not found.")
    return snap.generate_manifest()


@router.get("/snapshots/{snapshot_id}/lineage", response_model=List[ResearchSnapshot])
def get_snapshot_lineage(snapshot_id: str):
    """Retrieves full parent-child ancestor lineage from root snapshot to current."""
    sys = get_audit_system()
    return sys.snapshots.get_lineage(snapshot_id)


# ==============================================================================
# 2. Answer Diff Endpoint (Clauses 94-96)
# ==============================================================================

@router.post("/diff", response_model=ScientificAnswerDiff)
def diff_snapshots(req: DiffSnapshotsRequest):
    """Explains why and how scientific answers and conclusions evolved across two snapshots."""
    sys = get_audit_system()
    try:
        return sys.snapshots.compute_answer_diff(req.old_snapshot_id, req.new_snapshot_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ==============================================================================
# 3. Cryptographic Audit Events & Chain Verification (Clauses 11-14, 225)
# ==============================================================================

@router.post("/events", response_model=AuditEvent, status_code=status.HTTP_201_CREATED)
def record_audit_event(req: RecordEventRequest, x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")):
    """Records an audit event appended to the tamper-evident cryptographic hash chain."""
    sys = get_audit_system()
    return sys.events.record_event(
        audit_id=req.audit_id,
        action=req.action,
        resource_type=req.resource_type,
        resource_id=req.resource_id,
        actor_type=req.actor_type,
        actor_id=req.actor_id,
        before_state=req.before_state,
        after_state=req.after_state,
        reason=req.reason,
        tenant_id=x_tenant_id
    )


@router.get("/events/{audit_id}", response_model=List[AuditEvent])
def list_audit_events(
    audit_id: str,
    resource_id: Optional[str] = None,
    action: Optional[AuditEventType] = None
):
    """Queries audit events recorded on a chain."""
    sys = get_audit_system()
    return sys.events.get_events(audit_id=audit_id, resource_id=resource_id, action=action)


@router.get("/events/{audit_id}/verify", response_model=Dict[str, Any])
def verify_audit_chain(audit_id: str):
    """Rigorously verifies the SHA256 cryptographic hash chain integrity of an audit stream."""
    sys = get_audit_system()
    return sys.verify_audit_trail(audit_id)


# ==============================================================================
# 4. Provenance Graph & Bidirectional Trace Endpoints (Clauses 15, 16, 122, 125)
# ==============================================================================

@router.get("/provenance/{snapshot_id}", response_model=ScientificResearchTrace)
def get_provenance_trace(snapshot_id: str):
    """Retrieves full execution graph (DAG) for a research snapshot."""
    sys = get_audit_system()
    trace = sys.provenance.get_trace(snapshot_id)
    if not trace:
        snap = sys.snapshots.get_snapshot(snapshot_id)
        if snap:
            trace = sys.provenance.build_trace(snap)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Snapshot not found.")
    return trace


@router.get("/provenance/{snapshot_id}/backward", response_model=List[TraceNode])
def trace_backward(snapshot_id: str, node_id: str):
    """Traverses backward from a conclusion, claim, or result to all upstream evidence and queries."""
    sys = get_audit_system()
    nodes = sys.provenance.backward_trace(snapshot_id, node_id)
    if not nodes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node or trace not found.")
    return nodes


@router.get("/provenance/{snapshot_id}/forward", response_model=List[TraceNode])
def trace_forward(snapshot_id: str, node_id: str):
    """Traverses forward from a modified/retracted source or data node to identify all impacted outputs."""
    sys = get_audit_system()
    nodes = sys.provenance.forward_trace(snapshot_id, node_id)
    if not nodes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node or trace not found.")
    return nodes


# ==============================================================================
# 5. Reproduction Engine Endpoints (Clauses 87-90, 252)
# ==============================================================================

@router.post("/reproduce/{snapshot_id}", response_model=ReproductionRun)
def reproduce_snapshot(
    snapshot_id: str,
    req: ReproduceRequest,
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")
):
    """Executes sandbox reproduction re-running all stages and producing a comparison matrix."""
    sys = get_audit_system()
    try:
        return sys.reproduce(
            snapshot_id=snapshot_id,
            mode=req.mode,
            simulated_drift=req.simulated_drift,
            tenant_id=x_tenant_id
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/reproduce/runs/{run_id}", response_model=ReproductionRun)
def get_reproduction_run(run_id: str):
    """Retrieves reproduction run details and comparison matrix."""
    sys = get_audit_system()
    run = sys.reproduction.get_run(run_id)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reproduction run not found.")
    return run


# ==============================================================================
# 6. Certificates & Export Endpoints (Clauses 101, 102, 215, 216)
# ==============================================================================

@router.post("/certificates/{audit_id}")
def issue_certificates(audit_id: str, x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")):
    """Issues official Reproducibility and Research Audit Certificates."""
    sys = get_audit_system()
    try:
        return sys.issue_certificates(audit_id, tenant_id=x_tenant_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/certificates/{audit_id}/packet")
def get_audit_packet(
    audit_id: str,
    format: str = Query("json", description="json or html"),
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")
):
    """Exports complete downloadable Research Audit Packet."""
    sys = get_audit_system()
    try:
        content = sys.export_audit_packet(audit_id, format_type=format, tenant_id=x_tenant_id)
        if format.lower() == "html":
            return HTMLResponse(content=content)
        return content
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ==============================================================================
# 7. Research Audit Records & Legal Hold (Clauses 10, 237)
# ==============================================================================

@router.post("/records", response_model=ResearchAudit, status_code=status.HTTP_201_CREATED)
def create_audit_record(req: CreateAuditRecordRequest, x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")):
    """Initializes a new formal research audit."""
    sys = get_audit_system()
    try:
        return sys.create_audit(
            snapshot_id=req.snapshot_id,
            researcher=req.researcher,
            study_name=req.study_name,
            project_id=req.project_id,
            tenant_id=x_tenant_id
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/records/{audit_id}", response_model=ResearchAudit)
def get_audit_record(audit_id: str, x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")):
    """Retrieves a research audit record with tenant isolation."""
    sys = get_audit_system()
    audit = sys.get_audit(audit_id, tenant_id=x_tenant_id)
    if not audit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Audit record {audit_id} not found.")
    return audit


@router.post("/records/{audit_id}/hold", response_model=ResearchAudit)
def set_legal_hold(audit_id: str, req: SetLegalHoldRequest):
    """Sets or releases a legal/regulatory preservation hold."""
    sys = get_audit_system()
    try:
        return sys.set_legal_hold(audit_id, req.hold)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/records", response_model=List[ResearchAudit])
def list_audit_records(x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")):
    """Lists all formal research audit records."""
    sys = get_audit_system()
    return list(sys._audits.values())

