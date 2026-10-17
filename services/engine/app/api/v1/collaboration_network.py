"""
ZMIE Global Scientific Collaboration & Research Network Engine API Router.
Prompt 22 Implementation.

Endpoints for:
- Researcher Identity Resolution & Disambiguation
- Temporal Affiliation Chronology
- Multi-Dimensional Evidence-Backed Expertise Search
- Collaboration Topology & Recency Decay
- Cross-Disciplinary Bridge Detection
- Research Cluster Discovery
- Epistemic Research Gap Mapping
- Network Snapshotting & Diffing
- Anti-Ranking Firewall Verification
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from pydantic import BaseModel, Field

from app.models.collaboration_network import (
    ResearcherIdentity,
    InstitutionIdentity,
    TemporalAffiliation,
    CollaborationEdge,
    CrossDisciplinaryBridge,
    ResearchCluster,
    ResearchGapReport,
    NetworkSnapshot,
    NetworkDiff,
    ResearcherResolveRequest,
    ExpertiseSearchQuery,
    GapStatus,
)
from app.collaboration_network.engine import (
    ScientificCollaborationNetworkEngine,
    ForbiddenRankingException,
)

router = APIRouter(prefix="/network", tags=["Global Scientific Collaboration Network"])

_engine_instance = ScientificCollaborationNetworkEngine()


def get_network_engine() -> ScientificCollaborationNetworkEngine:
    return _engine_instance


# ---------------------------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------------------------

class CreateSnapshotRequest(BaseModel):
    label: str = Field(..., description="Label or version tag for network snapshot")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/researchers/resolve", response_model=Dict[str, Any])
def resolve_researcher(
    req: ResearcherResolveRequest,
    engine: ScientificCollaborationNetworkEngine = Depends(get_network_engine),
):
    """
    Resolve and disambiguate a researcher identity using ORCID, institution,
    co-author cues, and topic hints. Refuses false merges.
    """
    return engine.resolve_researcher_identity(req)


@router.get("/researchers/{researcher_id}", response_model=Dict[str, Any])
def get_researcher_profile(
    researcher_id: str,
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
    engine: ScientificCollaborationNetworkEngine = Depends(get_network_engine),
):
    """
    Retrieve full disambiguated researcher profile, primary disciplines,
    affiliations, and evidence-backed expertise profile.
    """
    r = engine.get_researcher(researcher_id, tenant_id=x_tenant_id)
    if not r:
        raise HTTPException(status_code=404, detail="Researcher profile not found or unauthorized.")
    return r.model_dump()


@router.get("/researchers/{researcher_id}/timeline", response_model=Dict[str, Any])
def get_researcher_timeline(
    researcher_id: str,
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
    engine: ScientificCollaborationNetworkEngine = Depends(get_network_engine),
):
    """
    Retrieve chronological affiliation history with start/end dates,
    primary/visiting status, and provenance records.
    """
    timeline = engine.get_researcher_timeline(researcher_id, tenant_id=x_tenant_id)
    if "error" in timeline:
        raise HTTPException(status_code=404, detail=timeline["error"])
    return timeline


@router.get("/researchers/{researcher_id}/collaborations", response_model=Dict[str, Any])
def get_researcher_collaborations(
    researcher_id: str,
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
    engine: ScientificCollaborationNetworkEngine = Depends(get_network_engine),
):
    """
    Retrieve direct (1st degree) and indirect (2nd degree) collaboration network
    with time-decayed recency weighting and artifact evidence.
    """
    collabs = engine.get_collaborations(researcher_id, tenant_id=x_tenant_id)
    if "error" in collabs:
        raise HTTPException(status_code=404, detail=collabs["error"])
    return collabs


@router.get("/institutions/{institution_id}", response_model=Dict[str, Any])
def get_institution_profile(
    institution_id: str,
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
    engine: ScientificCollaborationNetworkEngine = Depends(get_network_engine),
):
    """
    Retrieve institutional identity, departments, labs, and identifiers (ROR/GRID).
    """
    inst = engine.get_institution(institution_id, tenant_id=x_tenant_id)
    if not inst:
        raise HTTPException(status_code=404, detail="Institution not found or unauthorized.")
    return inst.model_dump()


@router.post("/expertise/search", response_model=Dict[str, Any])
def search_evidence_expertise(
    query: ExpertiseSearchQuery,
    engine: ScientificCollaborationNetworkEngine = Depends(get_network_engine),
):
    """
    Search for researchers by evidence-backed topic, method, or disease expertise.
    Enforces the Anti-Ranking guarantee: returns objective metrics without subjective rankings.
    """
    return engine.search_expertise(query)


@router.get("/bridges/cross-disciplinary", response_model=List[Dict[str, Any]])
def get_cross_disciplinary_bridges(
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
    engine: ScientificCollaborationNetworkEngine = Depends(get_network_engine),
):
    """
    Discover researchers actively bridging two or more distinct disciplines
    (e.g., Unani Medicine + Phytochemistry, or Oncology + AI).
    """
    bridges = engine.detect_cross_disciplinary_bridges(tenant_id=x_tenant_id)
    return [b.model_dump() for b in bridges]


@router.get("/clusters", response_model=List[Dict[str, Any]])
def get_research_clusters(
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
    engine: ScientificCollaborationNetworkEngine = Depends(get_network_engine),
):
    """
    Retrieve discovered thematic research clusters and institutional collaboratories.
    """
    clusters = engine.discover_clusters(tenant_id=x_tenant_id)
    return [c.model_dump() for c in clusters]


@router.get("/gaps", response_model=Dict[str, Any])
def evaluate_gap(
    topic: str = Query(..., description="Research topic or intersection to evaluate"),
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
    engine: ScientificCollaborationNetworkEngine = Depends(get_network_engine),
):
    """
    Evaluate public literature representation for a research topic.
    Explicitly outputs 'SPARSE_IN_INDEXED_SOURCES' rather than asserting nonexistence.
    """
    report = engine.evaluate_research_gap(topic, tenant_id=x_tenant_id)
    return report.model_dump()


@router.post("/snapshot", response_model=Dict[str, Any])
def create_snapshot(
    req: CreateSnapshotRequest,
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
    engine: ScientificCollaborationNetworkEngine = Depends(get_network_engine),
):
    """
    Capture an immutable snapshot of current collaboration network state.
    """
    snap = engine.capture_snapshot(label=req.label, tenant_id=x_tenant_id)
    return snap.model_dump()


@router.get("/diff", response_model=Dict[str, Any])
def diff_snapshots(
    from_snapshot_id: str = Query(..., description="Base snapshot ID"),
    to_snapshot_id: str = Query(..., description="Target snapshot ID"),
    engine: ScientificCollaborationNetworkEngine = Depends(get_network_engine),
):
    """
    Compute topological and membership diff between two network snapshots.
    """
    try:
        diff = engine.diff_snapshots(from_snapshot_id, to_snapshot_id)
        return diff.model_dump()
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
