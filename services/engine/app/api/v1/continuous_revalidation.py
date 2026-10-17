"""
ZMIE Continuous Evidence & Knowledge Revalidation FastAPI Router
PROMPT 31 Architecture Implementation
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field

from app.continuous_revalidation.engine import ContinuousRevalidationEngine
from app.continuous_revalidation.models import (
    RevalidationEventType,
    InvalidationSeverity,
    EvidenceDeltaReport,
    SurveillanceEvent,
    RevalidationTrigger,
    RevalidationScope,
    RevalidationPriority,
    RevalidationJob,
    RevalidationCertificate,
    SourceWatch,
    TopicWatcher,
    SourceDiff,
    ImpactAnalysisReport,
    KnowledgeHealth,
    KnowledgeVersion,
    ContentChangeImpact,
)

router = APIRouter(prefix="/continuous-revalidation", tags=["Continuous Evidence Revalidation"])

# Global singleton instance
_revalidation_engine = ContinuousRevalidationEngine()


def get_revalidation_engine() -> ContinuousRevalidationEngine:
    return _revalidation_engine


class IngestSurveillanceEventRequest(BaseModel):
    study_id: str
    event_type: RevalidationEventType
    reason: str
    severity: InvalidationSeverity = InvalidationSeverity.CRITICAL
    doi: Optional[str] = None
    source_notice_url: Optional[str] = None
    tenant_id: Optional[str] = None


class RevalidationJobRequest(BaseModel):
    object_id: str
    trigger: RevalidationTrigger = RevalidationTrigger.USER_TRIGGERED
    scope: RevalidationScope = RevalidationScope.DEPENDENCIES
    priority: RevalidationPriority = RevalidationPriority.NORMAL
    reason: str = "Standard revalidation request"
    tenant_id: Optional[str] = None
    incoming_event: Optional[Dict[str, Any]] = None


class SourceDiffRequest(BaseModel):
    source_id: str
    old_content: str
    new_content: str
    old_metadata: Optional[Dict[str, Any]] = None
    new_metadata: Optional[Dict[str, Any]] = None


class ImpactAnalysisRequest(BaseModel):
    target_object_id: str
    change_type: RevalidationEventType
    impact_level: ContentChangeImpact
    trigger_event_id: str = "evt-manual"


class SourceWatchRequest(BaseModel):
    watch_id: str
    source_id: str
    provider: str = "CROSSREF"
    schedule: str = "0 0 * * *"
    owner: str = "SYSTEM"


class TopicWatcherRequest(BaseModel):
    topic: str
    terms: List[str]
    entities: Optional[List[str]] = None
    scope: str = "PUBLIC"
    tenant_id: Optional[str] = None


class ContradictionSearchRequest(BaseModel):
    claim_id: str
    disconfirming_study_doi: Optional[str] = None


class ReviewDecisionRequest(BaseModel):
    reviewer_id: str
    comment_or_reason: str = "Approved"


# =========================================================================
# SURVEILLANCE & DELTAS (Existing / Backwards Compatible)
# =========================================================================

@router.post("/surveillance-events", response_model=EvidenceDeltaReport)
def ingest_surveillance_event(
    req: IngestSurveillanceEventRequest,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    """
    Ingests a surveillance radar alert (e.g. study retraction) and computes
    downstream cascade invalidation across the living evidence graph.
    """
    return engine.process_surveillance_event(
        study_id=req.study_id,
        event_type=req.event_type,
        reason=req.reason,
        severity=req.severity,
        doi=req.doi,
        source_notice_url=req.source_notice_url,
        tenant_id=req.tenant_id
    )


@router.get("/deltas", response_model=List[EvidenceDeltaReport])
def list_delta_reports(
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    """Lists all computed evidence delta reports generated from living surveillance."""
    return engine.list_delta_reports()


@router.get("/deltas/{delta_id}", response_model=EvidenceDeltaReport)
def get_delta_report(
    delta_id: str,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    """Gets specific evidence delta report by ID."""
    report = engine.get_delta_report(delta_id)
    if not report:
        raise HTTPException(status_code=404, detail="Delta report not found")
    return report


@router.get("/dependents/{node_id}")
def get_downstream_dependents(
    node_id: str,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    """Computes all downstream dependencies relying on this study or node."""
    dependents = engine.get_downstream_dependents(node_id)
    return {
        "node_id": node_id,
        "downstream_count": len(dependents),
        "dependents": dependents
    }


@router.get("/nodes/{node_id}")
def get_node(
    node_id: str,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    """Gets graph node details."""
    node = engine.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Graph node not found")
    return node


# =========================================================================
# REVALIDATION JOBS & REQUESTS (Clauses 28-30, 76-83)
# =========================================================================

@router.post("/request", response_model=RevalidationJob)
def request_revalidation(
    req: RevalidationJobRequest,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    """Requests and orchestrates a revalidation job with idempotency and trust verification."""
    return engine.request_revalidation(
        object_id=req.object_id,
        trigger=req.trigger,
        scope=req.scope,
        priority=req.priority,
        reason=req.reason,
        tenant_id=req.tenant_id,
        incoming_event=req.incoming_event
    )


@router.get("/jobs/{job_id}", response_model=RevalidationJob)
def get_revalidation_job(
    job_id: str,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    """Retrieves revalidation job status."""
    job = engine._jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Revalidation job not found")
    return job


@router.post("/jobs/{job_id}/approve")
def approve_job(
    job_id: str,
    req: ReviewDecisionRequest,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    """Applies human review approval to revalidation job."""
    res = engine.approve_revalidation(job_id, req.reviewer_id, req.comment_or_reason)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res


@router.post("/jobs/{job_id}/reject")
def reject_job(
    job_id: str,
    req: ReviewDecisionRequest,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    """Rejects revalidation result and flags restriction."""
    res = engine.reject_revalidation(job_id, req.reviewer_id, req.comment_or_reason)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res


@router.post("/jobs/{job_id}/auto-publish")
def attempt_auto_publish(
    job_id: str,
    agent_id: str,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    """Enforces No Agent Self-Approval (Clause 173)."""
    return engine.attempt_agent_auto_publish(job_id, agent_id)


# =========================================================================
# DIFFS & IMPACT (Clauses 12-20)
# =========================================================================

@router.post("/source-diff", response_model=SourceDiff)
def compute_diff(
    req: SourceDiffRequest,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    """Computes multi-dimensional diff and impact classification."""
    return engine.compute_source_diff(
        source_id=req.source_id,
        old_content=req.old_content,
        new_content=req.new_content,
        old_metadata=req.old_metadata,
        new_metadata=req.new_metadata
    )


@router.post("/impact-analysis", response_model=ImpactAnalysisReport)
def run_impact_analysis(
    req: ImpactAnalysisRequest,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    """Runs dependency-aware impact analysis down the knowledge fabric."""
    return engine.analyze_impact(
        target_object_id=req.target_object_id,
        change_type=req.change_type,
        impact_level=req.impact_level,
        trigger_event_id=req.trigger_event_id
    )


# =========================================================================
# WATCHERS & MONITORING (Clauses 10, 57-61, 138-143)
# =========================================================================

@router.post("/source-watches", response_model=SourceWatch)
def register_watch(
    req: SourceWatchRequest,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    return engine.register_source_watch(
        watch_id=req.watch_id,
        source_id=req.source_id,
        provider=req.provider,
        schedule=req.schedule,
        owner=req.owner
    )


@router.get("/source-watches", response_model=List[SourceWatch])
def list_watches(
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    return engine.list_source_watches()


@router.post("/source-watches/{watch_id}/check")
def check_watch(
    watch_id: str,
    simulate_outage: bool = False,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    res = engine.check_source_watch(watch_id, simulate_outage=simulate_outage)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res


@router.post("/topic-watchers", response_model=TopicWatcher)
def create_topic_watcher(
    req: TopicWatcherRequest,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    return engine.register_topic_watcher(
        topic=req.topic,
        terms=req.terms,
        entities=req.entities,
        scope=req.scope,
        tenant_id=req.tenant_id
    )


@router.get("/topic-watchers", response_model=List[TopicWatcher])
def list_topic_watchers(
    tenant_id: Optional[str] = None,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    return engine.list_topic_watchers(tenant_id=tenant_id)


# =========================================================================
# CONTRADICTIONS & NEGATIVE EVIDENCE (Clauses 41, 42, 196, 284)
# =========================================================================

@router.post("/contradictions/search")
def search_contradictions(
    req: ContradictionSearchRequest,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    res = engine.find_contradictions(req.claim_id, req.disconfirming_study_doi)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res


# =========================================================================
# KNOWLEDGE HISTORY, HEALTH & CERTIFICATES (Clauses 50, 87, 119, 202)
# =========================================================================

@router.get("/knowledge/{node_id}/history", response_model=List[KnowledgeVersion])
def get_knowledge_history(
    node_id: str,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    return engine.get_knowledge_history(node_id)


@router.get("/knowledge/{node_id}/health", response_model=KnowledgeHealth)
def get_knowledge_health(
    node_id: str,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    return engine.get_knowledge_health(node_id)


@router.get("/snapshots/{snapshot_id}")
def inspect_snapshot(
    snapshot_id: str,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    res = engine.inspect_snapshot(snapshot_id)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res


@router.post("/jobs/{job_id}/certificate", response_model=RevalidationCertificate)
def issue_certificate(
    job_id: str,
    reviewer: str = "LEAD_SCIENTIFIC_REVIEWER",
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    try:
        return engine.issue_revalidation_certificate(job_id, reviewer=reviewer)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/feed/what-changed")
def get_what_changed(
    limit: int = 50,
    engine: ContinuousRevalidationEngine = Depends(get_revalidation_engine)
):
    return engine.get_what_changed_feed(limit=limit)
