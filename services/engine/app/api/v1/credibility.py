"""
ZMIE Scientific Credibility & Anti-Fabrication API Endpoints
14-Layer Verification, Evidence Chain Auditing, and State Lifecycle API
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.credibility.models import (
    VerificationState,
    EvidenceChain,
    CredibilityAuditReport,
    EpistemicSeparationLevels
)
from app.credibility.engine import get_credibility_engine

router = APIRouter(prefix="/credibility", tags=["Scientific Credibility & Verification Doctrine"])


class AuditClaimRequest(BaseModel):
    target_object_id: str
    target_object_type: str = "CLAIM"
    claim_text: str
    source_id: Optional[str] = None
    identifier: Optional[str] = None
    passage_text: Optional[str] = None
    dataset_hash: Optional[str] = None
    researcher_orcid: Optional[str] = None
    drug_name: Optional[str] = None
    traditional_mapping: Optional[Dict[str, Any]] = None
    calculation_seed: Optional[int] = None
    is_ai_generated: bool = False
    is_expert_signed: bool = False
    exact_location: Optional[str] = None


class VerifyChainRequest(BaseModel):
    chain: EvidenceChain


class TransitionStateRequest(BaseModel):
    object_id: str
    target_state: VerificationState
    proof_payload: Dict[str, Any] = Field(default_factory=dict)
    actor_id: str = "system"


@router.post("/audit", response_model=CredibilityAuditReport)
async def audit_scientific_object(req: AuditClaimRequest):
    """
    Executes the complete 14-layer Anti-Fabrication & Scientific Credibility Audit.
    Enforces that unverified objects cannot be promoted to Authoritative status.
    """
    engine = get_credibility_engine()
    return engine.run_14_layer_audit(
        target_object_id=req.target_object_id,
        target_object_type=req.target_object_type,
        claim_text=req.claim_text,
        source_id=req.source_id,
        identifier=req.identifier,
        passage_text=req.passage_text,
        dataset_hash=req.dataset_hash,
        researcher_orcid=req.researcher_orcid,
        drug_name=req.drug_name,
        traditional_mapping=req.traditional_mapping,
        calculation_seed=req.calculation_seed,
        is_ai_generated=req.is_ai_generated,
        is_expert_signed=req.is_expert_signed,
        exact_location=req.exact_location
    )


@router.post("/chain/verify", response_model=EvidenceChain)
async def verify_evidence_chain(req: VerifyChainRequest):
    """
    Verifies the complete mandatory evidence chain:
    CLAIM -> EVIDENCE -> STUDY/DATA -> SOURCE -> EXACT LOCATION -> PROVENANCE -> STATUS
    If ANY link is missing, returns status INSUFFICIENT_EVIDENCE with deficiency reasons.
    """
    engine = get_credibility_engine()
    return engine.verify_evidence_chain(req.chain)


@router.post("/transition")
async def transition_verification_state(req: TransitionStateRequest):
    """
    Strict state machine transition:
    UNVERIFIED -> CANDIDATE -> SOURCE_VERIFIED -> EVIDENCE_SUPPORTED -> EXPERT_REVIEWED -> AUTHORITATIVE
    """
    engine = get_credibility_engine()
    success, message, current_state = engine.transition_state(
        object_id=req.object_id,
        target_state=req.target_state,
        proof_payload=req.proof_payload,
        actor_id=req.actor_id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "INVALID_VERIFICATION_TRANSITION", "message": message, "current_state": current_state.value}
        )
    return {"status": "SUCCESS", "message": message, "new_state": req.target_state.value}


@router.get("/states/{object_id}")
async def get_object_state(object_id: str):
    """Returns the non-negotiable verification state for an object."""
    engine = get_credibility_engine()
    state = engine.get_object_state(object_id)
    return {"object_id": object_id, "verification_state": state.value}


@router.get("/audits/{audit_id}", response_model=CredibilityAuditReport)
async def get_audit_report(audit_id: str):
    """Retrieves an existing cryptographic credibility audit report."""
    engine = get_credibility_engine()
    report = engine.get_audit_report(audit_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Audit report '{audit_id}' not found.")
    return report
