"""
ZMIE Expert Review & Governance API Router
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from pydantic import BaseModel

from app.agents.review_queue import ExpertReviewQueue, ReviewTask, ReviewPoolType, TaskStatus
from app.core.security import SecurityService, AuthContext, UserRole

router = APIRouter(prefix="/governance", tags=["Expert Governance & Review Queue"])


class TaskResolutionPayload(BaseModel):
    reviewer_id: str
    verdict: TaskStatus  # 'approved_verified', 'rejected_discarded', 'qualified_amended'
    notes: str


@router.get("/queue", response_model=List[ReviewTask])
async def get_review_queue(
    pool: Optional[ReviewPoolType] = Query(None, description="Filter by expert pool type"),
    auth: AuthContext = Depends(SecurityService.require_authenticated)
):
    """
    Returns pending tasks awaiting expert human verification.
    """
    return ExpertReviewQueue.list_pending_tasks(pool=pool)


@router.post("/resolve/{task_id}", response_model=ReviewTask)
async def resolve_review_task(
    task_id: str,
    payload: TaskResolutionPayload,
    auth: AuthContext = Depends(SecurityService.require_role([UserRole.CLINICIAN, UserRole.ADMIN]))
):
    """
    Physician/Hakim/Vaidya/Pharmacologist action approving or rejecting an AI-derived claim.
    Protected: Requires CLINICIAN or ADMIN role.
    """
    updated_task = ExpertReviewQueue.resolve_task(
        task_id=task_id,
        reviewer_id=payload.reviewer_id,
        verdict=payload.verdict,
        notes=payload.notes
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task ID not found in review queue.")
    return updated_task
