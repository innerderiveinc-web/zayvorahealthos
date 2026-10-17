"""
ZMIE Living Evidence Synthesis & Evidence Update API Router
Endpoints for living systematic reviews, surveillance plans, AI-assisted screening,
reproducible DerSimonian-Laird meta-analysis, retraction handling, and versioned diffing.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.models.living_evidence import (
    ReviewType,
    ReviewStatus,
    EvidenceImpactClass,
    UpdateTriggerType,
    ScreeningDecision,
    UpdateTriggerEvent,
    LivingReviewVersion,
    LivingEvidenceSynthesis
)
from app.living_evidence.engine import LivingEvidenceEngine

router = APIRouter(prefix="/living-evidence", tags=["Living Evidence Synthesis"])

_engine_instance = LivingEvidenceEngine()

def get_engine() -> LivingEvidenceEngine:
    return _engine_instance


# -------------------------------------------------------------
# Request Schemas
# -------------------------------------------------------------

class ScreeningRequest(BaseModel):
    title: str
    abstract: str
    study_design: str = "Randomized Controlled Trial"
    reviewer_id: str = "ZMIE Screener"


class TriggerRequest(BaseModel):
    trigger_type: UpdateTriggerType
    source_reference: str
    description: str
    impact_class: EvidenceImpactClass = EvidenceImpactClass.HIGH_IMPACT


class IncorporateStudyRequest(BaseModel):
    study_name: str
    trial_registration_id: str
    point_estimate: float
    ci_lower: float
    ci_upper: float
    sample_size: int
    approver: str = "ZMIE Lead Systematic Reviewer"


class RetractionRequest(BaseModel):
    retracted_study_family_id: str
    retraction_reason: str
    approver: str = "ZMIE Scientific Integrity Lead"


# -------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------

@router.get("", response_model=List[LivingEvidenceSynthesis])
async def list_living_reviews(engine: LivingEvidenceEngine = Depends(get_engine)):
    """List all registered living evidence syntheses."""
    return engine.list_reviews()


@router.get("/{review_id}", response_model=LivingEvidenceSynthesis)
async def get_living_review(review_id: str, engine: LivingEvidenceEngine = Depends(get_engine)):
    """Retrieve full details for a specified living evidence synthesis."""
    rev = engine.get_review(review_id)
    if not rev:
        raise HTTPException(status_code=404, detail=f"Review {review_id} not found.")
    return rev


@router.post("/{review_id}/start-living", response_model=LivingEvidenceSynthesis)
async def start_living_mode(review_id: str, engine: LivingEvidenceEngine = Depends(get_engine)):
    """Activate continuous living surveillance mode."""
    try:
        return engine.start_living_mode(review_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{review_id}/pause", response_model=LivingEvidenceSynthesis)
async def pause_living_mode(review_id: str, reason: str = "Administrative pause", engine: LivingEvidenceEngine = Depends(get_engine)):
    """Temporarily pause living surveillance mode."""
    try:
        return engine.pause_living_mode(review_id, reason)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{review_id}/health")
async def check_review_health(review_id: str, engine: LivingEvidenceEngine = Depends(get_engine)):
    """Check currency, backlog, surveillance frequency, and staleness indicators."""
    try:
        return engine.check_review_health(review_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{review_id}/screening", response_model=ScreeningDecision)
async def assess_screening_record(
    review_id: str,
    req: ScreeningRequest,
    engine: LivingEvidenceEngine = Depends(get_engine)
):
    """Screen candidate record with AI assistance and explicit eligibility criteria matching."""
    try:
        return engine.assess_screening_record(
            review_id=review_id,
            title=req.title,
            abstract=req.abstract,
            study_design=req.study_design,
            reviewer_id=req.reviewer_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{review_id}/triggers", response_model=UpdateTriggerEvent)
async def detect_update_trigger(
    review_id: str,
    req: TriggerRequest,
    engine: LivingEvidenceEngine = Depends(get_engine)
):
    """Detect and register new evidence trigger, classifying operational update urgency."""
    try:
        return engine.detect_update_trigger(
            review_id=review_id,
            trigger_type=req.trigger_type,
            source_reference=req.source_reference,
            description=req.description,
            impact_class=req.impact_class
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{review_id}/incorporate", response_model=LivingReviewVersion)
async def incorporate_new_study(
    review_id: str,
    req: IncorporateStudyRequest,
    engine: LivingEvidenceEngine = Depends(get_engine)
):
    """Incorporate newly validated study, recompute DerSimonian-Laird meta-analysis, and publish new version."""
    try:
        return engine.incorporate_new_study_and_recalculate(
            review_id=review_id,
            new_study_name=req.study_name,
            trial_id=req.trial_registration_id,
            point_estimate=req.point_estimate,
            ci_lower=req.ci_lower,
            ci_upper=req.ci_upper,
            sample_size=req.sample_size,
            approver=req.approver
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{review_id}/retract", response_model=LivingReviewVersion)
async def handle_retraction(
    review_id: str,
    req: RetractionRequest,
    engine: LivingEvidenceEngine = Depends(get_engine)
):
    """Quarantine retracted study, recalculate synthesis without compromised data, and publish update."""
    try:
        return engine.handle_retraction_propagation(
            review_id=review_id,
            retracted_study_family_id=req.retracted_study_family_id,
            retraction_reason=req.retraction_reason,
            approver=req.approver
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{review_id}/diff")
async def compare_review_versions(
    review_id: str,
    version_a: str = "v1.0",
    version_b: str = "v2.0",
    engine: LivingEvidenceEngine = Depends(get_engine)
):
    """Compare two review versions: study counts, pooled estimate deltas, and conclusion evolution."""
    try:
        return engine.compare_review_versions(
            review_id=review_id,
            version_a=version_a,
            version_b=version_b
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
