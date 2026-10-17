"""
ZMIE Knowledge Diff & Living Memory API Router
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.agents.diff_engine import KnowledgeDiffEngine, KnowledgeCommit, ChangeType

router = APIRouter(prefix="/timeline", tags=["Scientific Memory & Knowledge Diff"])


class KnowledgeCommitPayload(BaseModel):
    topic: str
    change_type: ChangeType
    previous_state_summary: str
    new_state_summary: str
    evidence_delta_description: str
    triggering_source_id: str
    reviewer: str
    doi: Optional[str] = None


@router.get("/changes", response_model=List[KnowledgeCommit])
async def list_recent_knowledge_changes(limit: int = Query(10, ge=1, le=50)):
    """
    Returns latest global medical updates, retractions, and newly verified trials.
    """
    return KnowledgeDiffEngine.get_latest_changes(limit=limit)


@router.get("/topic", response_model=List[KnowledgeCommit])
async def get_topic_knowledge_history(topic: str = Query(..., description="E.g. 'Berberine' or 'Metabolic'")):
    """
    Returns living timeline: 'What changed' for a specific biomedical topic over time.
    """
    return KnowledgeDiffEngine.get_topic_timeline(topic=topic)


@router.post("/commit", response_model=KnowledgeCommit)
async def create_knowledge_commit(payload: KnowledgeCommitPayload):
    """
    Registers a new git-like knowledge commit when evidence updates.
    """
    return KnowledgeDiffEngine.commit_knowledge_change(
        topic=payload.topic,
        change_type=payload.change_type,
        prev_summary=payload.previous_state_summary,
        new_summary=payload.new_state_summary,
        delta=payload.evidence_delta_description,
        source_id=payload.triggering_source_id,
        reviewer=payload.reviewer,
        doi=payload.doi
    )
