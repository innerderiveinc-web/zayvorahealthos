"""
ZMIE Global Medical Source Universe REST API Router
Exposes enterprise endpoints for:
- Source Registry, classes, authority levels, and licenses
- Live Source Coverage and gap analysis
- Universal Source Discovery queue and approval workflows
- Multi-System Research Source Matrix search
- Continuous Retraction & Safety Invalidation logs
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.models.source_universe import (
    SourceRecord, SourceClass, MedicalSystem, AuthorityLevel,
    DiscoveryCandidate, SourceCoverageReport, RetractionEvent
)
from app.sources.registry import SourceUniverseRegistry
from app.sources.discovery import SourceDiscoveryEngine
from app.sources.search_matrix import MultiSystemSearchMatrixEngine
from app.sources.retraction_pipeline import RetractionAndSafetyPipeline
from app.sources.pubmed_client import get_pubmed_client, PubMedArticle

router = APIRouter(prefix="/sources", tags=["Global Medical Source Universe & Universal Acquisition"])


# --- Source Registry & Filtering ---

@router.get("", response_model=List[SourceRecord])
def list_sources(
    source_class: Optional[SourceClass] = Query(None),
    medical_system: Optional[MedicalSystem] = Query(None),
    authority_level: Optional[AuthorityLevel] = Query(None),
    country: Optional[str] = Query(None)
):
    return SourceUniverseRegistry.list_sources(
        source_class=source_class,
        medical_system=medical_system,
        authority_level=authority_level,
        country=country
    )


@router.get("/coverage/report", response_model=SourceCoverageReport)
def get_source_coverage():
    return SourceUniverseRegistry.get_coverage_report()


@router.get("/{source_id}", response_model=SourceRecord)
def get_source(source_id: str):
    s = SourceUniverseRegistry.get_source(source_id)
    if not s:
        raise HTTPException(status_code=404, detail="Source not found.")
    return s


# --- Universal Discovery Queue ---

@router.get("/discovery/candidates", response_model=List[DiscoveryCandidate])
def list_discovery_candidates():
    return SourceDiscoveryEngine.list_candidates()


class DiscoverSearchRequest(BaseModel):
    query: str
    gap_reason: str = "Search yields insufficient evidence from current index"


@router.post("/discovery/search", response_model=DiscoveryCandidate)
def trigger_gap_discovery(req: DiscoverSearchRequest):
    return SourceDiscoveryEngine.discover_from_search_gap(req.query, req.gap_reason)


class ApproveCandidateRequest(BaseModel):
    candidate_id: str
    authority_tier: AuthorityLevel = AuthorityLevel.S3_PEER_REVIEWED


@router.post("/discovery/approve", response_model=SourceRecord)
def approve_candidate(req: ApproveCandidateRequest):
    source = SourceDiscoveryEngine.approve_candidate(req.candidate_id, req.authority_tier)
    if not source:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    return source


# --- Multi-System Research Search Matrix ---

class MultiSystemSearchRequest(BaseModel):
    query: str
    systems: Optional[List[MedicalSystem]] = None
    source_classes: Optional[List[SourceClass]] = None


@router.post("/search")
def multi_system_source_search(req: MultiSystemSearchRequest):
    return MultiSystemSearchMatrixEngine.execute_multi_system_search(
        query=req.query,
        systems=req.systems,
        source_classes=req.source_classes
    )


# --- Retraction & Safety Invalidation ---

class IngestRetractionRequest(BaseModel):
    identifier: str
    document_title: str
    source_id: str
    retraction_reason: str
    issuing_body: str = "Publisher COPE Investigation"


@router.post("/retractions/event", response_model=RetractionEvent)
def ingest_retraction_event(req: IngestRetractionRequest):
    return RetractionAndSafetyPipeline.ingest_retraction_event(
        identifier=req.identifier,
        document_title=req.document_title,
        source_id=req.source_id,
        retraction_reason=req.retraction_reason,
        issuing_body=req.issuing_body
    )


@router.get("/retractions/events", response_model=List[RetractionEvent])
def list_retractions():
    return RetractionAndSafetyPipeline.list_retraction_events()


# --- Authenticated NCBI PubMed Query Service ---

class PubMedQueryRequest(BaseModel):
    query: str
    max_results: int = 5


@router.post("/pubmed/query", response_model=List[PubMedArticle])
def query_pubmed_service(req: PubMedQueryRequest):
    """
    Queries NCBI PubMed / MEDLINE using the authenticated NCBI_API_KEY.
    """
    client = get_pubmed_client()
    return client.search_and_fetch(req.query, max_results=req.max_results)


@router.get("/pubmed/status")
def pubmed_service_status():
    """
    Returns the operational and authentication status of the NCBI PubMed gateway.
    """
    client = get_pubmed_client()
    return {
        "status": "ready",
        "api_key_configured": client.is_configured(),
        "rate_limit": "10 requests/second (Authenticated)" if client.is_configured() else "3 requests/second (Unauthenticated)",
        "source_id": "SRC-PUBMED",
        "registry": "National Library of Medicine (NLM / NCBI)"
    }

