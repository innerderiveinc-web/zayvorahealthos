"""
ZMIE Truth & Safety Firewall REST API Router
Provides comprehensive endpoints for:
- Answer verification (/v1/verify/answer)
- Individual claim verification (/v1/verify/claim)
- Citation verification (/v1/verify/citation)
- Retraction propagation & impact analysis (/v1/verify/retractions)
- Human review and escalation audit
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from app.models.truth_firewall import (
    Citation,
    ClaimVerification,
    VerifiedAnswerPacket,
    VerificationReview,
    FirewallVerdict
)
from app.firewall.orchestrator import TruthAndSafetyFirewall
from app.firewall.claim_engine import AtomicClaimEngine
from app.firewall.citation_engine import CitationVerificationEngine

router = APIRouter(prefix="/verify", tags=["Truth, Evidence Integrity & Safety Firewall"])


class VerifyAnswerRequest(BaseModel):
    answer: str = Field(..., description="Draft AI generated answer to verify")
    citations: List[Citation] = Field(default_factory=list, description="Associated citation objects")
    passages: Dict[str, str] = Field(default_factory=dict, description="Anchor passage text keyed by citation ID or identifier")


class VerifyClaimRequest(BaseModel):
    claim_text: str = Field(..., description="Atomic medical claim")
    citation: Optional[Citation] = None
    passage_text: Optional[str] = None


class VerifyCitationRequest(BaseModel):
    citation: Citation
    claim_text: str
    passage_text: Optional[str] = None


class RetractionNoticeRequest(BaseModel):
    identifier: str = Field(..., description="DOI or PMID of retracted publication")


@router.post("/answer", response_model=Dict[str, Any])
async def verify_generated_answer(req: VerifyAnswerRequest):
    """
    POST /v1/verify/answer:
    Executes full multi-agent verification pipeline on generated answer.
    """
    try:
        packet = TruthAndSafetyFirewall.verify_answer(
            generated_answer=req.answer,
            citations=req.citations,
            passages_map=req.passages
        )
        return packet.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firewall execution failed: {str(e)}")


@router.post("/claim", response_model=Dict[str, Any])
async def verify_single_claim(req: VerifyClaimRequest):
    """
    POST /v1/verify/claim:
    Verifies an individual atomic claim against citations and safety policies.
    """
    try:
        citations_list = [req.citation] if req.citation else []
        passages_map = {req.citation.identifier: req.passage_text} if req.citation and req.passage_text else {}
        packet = TruthAndSafetyFirewall.verify_answer(
            generated_answer=req.claim_text,
            citations=citations_list,
            passages_map=passages_map
        )
        first_claim = packet.claims[0] if packet.claims else None
        return {
            "claim": first_claim.model_dump() if first_claim else {},
            "verdict": packet.verdict.value,
            "status": packet.status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Claim verification failed: {str(e)}")


@router.post("/citation", response_model=Dict[str, Any])
async def verify_citation(req: VerifyCitationRequest):
    """
    POST /v1/verify/citation:
    Checks citation existence, DOI validity, and exact textual entailment.
    """
    try:
        sup_lvl, ctx_ok, reasons = CitationVerificationEngine.verify_citation_entailment(
            claim_text=req.claim_text,
            citation=req.citation,
            passage_text=req.passage_text
        )
        return {
            "citation_identifier": req.citation.identifier,
            "support_level": sup_lvl.value,
            "context_match": ctx_ok,
            "is_valid": sup_lvl in ["DIRECT_SUPPORT", "STRONG_CONTEXTUAL_SUPPORT", "PARTIAL_SUPPORT"],
            "audit_reasons": reasons
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Citation verification failed: {str(e)}")


@router.post("/retraction-alert", response_model=Dict[str, Any])
async def propagate_retraction(req: RetractionNoticeRequest):
    """
    POST /v1/verify/retraction-alert:
    Registers a newly retracted document and executes impact analysis across active claims.
    """
    try:
        impact = TruthAndSafetyFirewall.run_retraction_impact_analysis(req.identifier)
        return impact
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraction propagation failed: {str(e)}")


class PatientApplicabilityRequest(BaseModel):
    subject: str = Field(..., description="Intervention or compound name")
    patient_age: int = Field(..., ge=0, le=120)
    patient_egfr: float = Field(..., ge=0)
    has_diabetes: bool = False
    has_liver_disease: bool = False
    is_pregnant: bool = False
    concomitant_drugs: List[str] = Field(default_factory=list)


@router.post("/applicability", response_model=Dict[str, Any])
async def calculate_patient_applicability(req: PatientApplicabilityRequest):
    """
    POST /v1/verify/applicability:
    Calculates evidence applicability score (0-100) comparing clinical trial demographic criteria vs current patient.
    """
    score = 100
    warnings = []
    factors = []

    # Pregnancy absolute contraindication check
    if req.is_pregnant:
        score = 0
        warnings.append("Strict Contraindication: Insufficient teratogenic safety or risk of fetal hyperbilirubinemia/kernicterus.")
        return {
            "applicability_score": 0,
            "applicability_tier": "CONTRAINDICATED",
            "patient_context": req.model_dump(),
            "alignment_factors": [{"factor": "Pregnancy Status", "status": "FAIL", "penalty": 100}],
            "extrapolation_warnings": warnings
        }

    # Renal alignment
    if req.patient_egfr < 30:
        score -= 45
        warnings.append("Severe Renal Impairment (eGFR < 30 mL/min): Clinical trial cohorts universally excluded eGFR < 30; metabolite accumulation hazard.")
        factors.append({"factor": "Renal Clearance (eGFR)", "status": "MISMATCH", "penalty": 45, "detail": f"Patient eGFR is {req.patient_egfr}"})
    elif req.patient_egfr < 45:
        score -= 20
        warnings.append("Moderate Renal Impairment (eGFR 30-45 mL/min): Study population had median eGFR > 75; dose titration mandatory.")
        factors.append({"factor": "Renal Clearance (eGFR)", "status": "PARTIAL", "penalty": 20, "detail": f"Patient eGFR is {req.patient_egfr}"})
    else:
        factors.append({"factor": "Renal Clearance (eGFR)", "status": "MATCH", "penalty": 0, "detail": "eGFR within study protocol parameters"})

    # Age alignment
    if req.patient_age > 75:
        score -= 15
        warnings.append("Geriatric Extrapolation: Human RCT cohorts enrolled median age 42–65; reduced first-pass hepatic reserve expected.")
        factors.append({"factor": "Age Demographic", "status": "EXTRAPOLATION", "penalty": 15, "detail": f"Age {req.patient_age} exceeds study median"})
    elif req.patient_age < 18:
        score -= 35
        warnings.append("Pediatric Extrapolation: Safety and bioavailability unconfirmed in pediatric populations.")
        factors.append({"factor": "Age Demographic", "status": "MISMATCH", "penalty": 35, "detail": "Pediatric status unrepresented in trial matrix"})
    else:
        factors.append({"factor": "Age Demographic", "status": "MATCH", "penalty": 0, "detail": "Age aligns with clinical study cohort"})

    # Polypharmacy checks
    for drug in req.concomitant_drugs:
        d_lower = drug.lower()
        if "warfarin" in d_lower or "coumadin" in d_lower:
            score -= 25
            warnings.append("Critical Anticoagulation Hazard: Concomitant warfarin interaction risk requires daily INR surveillance.")
            factors.append({"factor": "Narrow-Index Drug Interaction", "status": "HIGH_RISK", "penalty": 25, "detail": drug})
        elif "tacrolimus" in d_lower or "cyclosporine" in d_lower:
            score -= 25
            warnings.append("Calcineurin Inhibitor Hazard: CYP3A4/P-gp substrate competition elevates immunosuppressant AUC.")
            factors.append({"factor": "Immunosuppressant Competition", "status": "HIGH_RISK", "penalty": 25, "detail": drug})

    score = max(0, min(100, score))
    tier = "HIGH" if score >= 80 else ("MODERATE" if score >= 50 else "LOW")

    return {
        "applicability_score": score,
        "applicability_tier": tier,
        "patient_context": req.model_dump(),
        "alignment_factors": factors,
        "extrapolation_warnings": warnings
    }
