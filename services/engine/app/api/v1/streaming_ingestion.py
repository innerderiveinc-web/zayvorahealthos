"""
ZMIE Biomedical Streaming Ingestion REST Gateway
Exposes real-time SSE streaming and concurrent multi-source ingestion endpoints.
"""

from __future__ import annotations
import json
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.ingestion.streaming import BiomedicalStreamingIngestionEngine

router = APIRouter(prefix="/ingestion", tags=["Streaming Ingestion"])
streaming_engine = BiomedicalStreamingIngestionEngine()


class StreamingHarvestRequest(BaseModel):
    query: str = Field(..., description="Biomedical, botanical or clinical trial query term")
    max_records_per_source: int = Field(default=5, ge=1, le=20)


class HarvestSummaryResponse(BaseModel):
    query: str
    total_records: int
    duration_ms: float
    records: List[Dict[str, Any]]
    deduplication_ratio: float


@router.get("/stream")
async def stream_live_ingestion(
    query: str = Query(..., description="Clinical or biochemical search term"),
    max_per_source: int = Query(5, ge=1, le=20)
):
    """
    Server-Sent Events (SSE) streaming endpoint.
    Streams real-time discovery, deduplication, and verification events
    as they are processed from PubMed, Europe PMC, ClinicalTrials.gov, and OpenAlex.
    """
    async def event_generator():
        async for event in streaming_engine.stream_ingest(query, max_records_per_source=max_per_source):
            payload_str = json.dumps(event)
            yield f"data: {payload_str}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.post("/harvest", response_model=HarvestSummaryResponse)
async def harvest_biomedical_records(request: StreamingHarvestRequest):
    """
    Synchronous aggregation endpoint that queries all multi-source streaming connectors
    and returns deduplicated, authenticated clinical evidence records.
    """
    records = []
    total_raw = 0
    duration_ms = 0.0

    async for event in streaming_engine.stream_ingest(
        query=request.query,
        max_records_per_source=request.max_records_per_source
    ):
        if event["event_type"] == "RECORD_INGESTED":
            records.append(event["payload"]["record"])
            total_raw += 1
        elif event["event_type"] == "DEDUPLICATION_MATCH":
            total_raw += 1
        elif event["event_type"] == "PIPELINE_COMPLETE":
            duration_ms = event["payload"]["duration_ms"]

    dedup_ratio = round((1.0 - (len(records) / max(total_raw, 1))), 4) if total_raw > 0 else 0.0

    return HarvestSummaryResponse(
        query=request.query,
        total_records=len(records),
        duration_ms=duration_ms,
        records=records,
        deduplication_ratio=dedup_ratio
    )
