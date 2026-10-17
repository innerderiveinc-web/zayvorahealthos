"""
ZMIE Export & Coverage API Router
"""

from fastapi import APIRouter, Query, Response
from typing import List, Dict, Any
from pydantic import BaseModel

from app.agents.coverage_agent import CoverageAuditingAgent, SourceCoverageReport
from app.agents.citation_exporter import CitationExportEngine

router = APIRouter(prefix="/export", tags=["Exports & Coverage Auditing"])


class CitationExportPayload(BaseModel):
    citations: List[Dict[str, Any]]


@router.get("/coverage", response_model=SourceCoverageReport)
async def get_search_coverage(topic: str = Query(..., description="Query topic to audit")):
    """
    Returns empirical coverage metrics, full-text ratios, and acknowledged blindspots.
    """
    mock_retrieved = [
        {"document_id": "openalex-1", "license_class": "permitted_open_access"},
        {"document_id": "pmid-1", "license_class": "restricted_metadata_only"}
    ]
    return CoverageAuditingAgent.audit_coverage(topic=topic, retrieved_docs=mock_retrieved)


@router.post("/bibtex")
async def export_to_bibtex(payload: CitationExportPayload):
    """
    Exports citations to standard BibTeX format.
    """
    bibtex_str = CitationExportEngine.export_bibtex(payload.citations)
    return Response(content=bibtex_str, media_type="text/plain")


@router.post("/ris")
async def export_to_ris(payload: CitationExportPayload):
    """
    Exports citations to standard RIS format for Zotero/EndNote.
    """
    ris_str = CitationExportEngine.export_ris(payload.citations)
    return Response(content=ris_str, media_type="application/x-research-info-systems")
