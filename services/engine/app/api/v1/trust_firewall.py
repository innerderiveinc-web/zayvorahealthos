"""
ZMIE Scientific Trust Firewall FastAPI Router
PROMPT 30 Master Architecture Specification
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.trust_firewall.engine import ScientificTrustFirewallEngine
from app.trust_firewall.models import (
    SourceVerificationResult,
    FirewallEvaluationReport,
    SourceLedgerEntry,
    TrustAssessment,
    TrustDecisionReport,
    QuarantineItem,
    TrustIncident,
    ScientificTrustCertificate,
    TrustDecision
)

router = APIRouter(prefix="/trust-firewall", tags=["Scientific Trust Firewall"])

# Global singleton engine instance
_firewall_engine = ScientificTrustFirewallEngine()


def get_trust_firewall() -> ScientificTrustFirewallEngine:
    return _firewall_engine


class VerifySourceRequest(BaseModel):
    identifier: str


class EvaluateClaimTrustRequest(BaseModel):
    claim_text: str
    doi: Optional[str] = None
    claimed_passage: Optional[str] = None


class ComprehensiveTrustAssessRequest(BaseModel):
    object_id: str
    object_type: str = "claim"
    claim_text: Optional[str] = None
    source_id: Optional[str] = None
    claimed_passage: Optional[str] = None
    is_simulation: bool = False
    traditional_mapping: Optional[str] = None
    regulatory_claim: Optional[str] = None
    tenant_id: str = "system"
    is_public_release: bool = False


@router.post("/assess", response_model=TrustDecisionReport)
def assess_trust(
    req: ComprehensiveTrustAssessRequest,
    engine: ScientificTrustFirewallEngine = Depends(get_trust_firewall)
):
    """
    Core Trust Decision Engine evaluation across all multi-point firewall gates.
    """
    return engine.evaluate_trust(
        object_id=req.object_id,
        object_type=req.object_type,
        claim_text=req.claim_text,
        source_id=req.source_id,
        claimed_passage=req.claimed_passage,
        is_simulation=req.is_simulation,
        traditional_mapping=req.traditional_mapping,
        regulatory_claim=req.regulatory_claim,
        tenant_id=req.tenant_id,
        is_public_release=req.is_public_release
    )


@router.post("/verify-source", response_model=SourceVerificationResult)
def verify_source(
    req: VerifySourceRequest,
    engine: ScientificTrustFirewallEngine = Depends(get_trust_firewall)
):
    """
    Verifies that a citation/DOI exists in authentic registries, is active,
    not retracted, and not in predatory publishing venues.
    """
    return engine.verify_source(req.identifier)


@router.post("/evaluate-claim", response_model=FirewallEvaluationReport)
def evaluate_claim(
    req: EvaluateClaimTrustRequest,
    engine: ScientificTrustFirewallEngine = Depends(get_trust_firewall)
):
    """
    Runs full Scientific Trust Firewall evaluation on a claim.
    """
    return engine.evaluate_claim_trust(
        claim_text=req.claim_text,
        doi=req.doi,
        claimed_passage=req.claimed_passage
    )


@router.get("/ledger", response_model=List[SourceLedgerEntry])
def list_ledger_entries(
    engine: ScientificTrustFirewallEngine = Depends(get_trust_firewall)
):
    """
    Returns verified canonical source ledger entries with HMAC signatures.
    """
    return engine.list_ledger_entries()


@router.get("/ledger/{identifier:path}", response_model=SourceLedgerEntry)
def get_ledger_entry(
    identifier: str,
    engine: ScientificTrustFirewallEngine = Depends(get_trust_firewall)
):
    """
    Returns a specific verified canonical ledger entry.
    """
    entry = engine.get_ledger_entry(identifier)
    if not entry:
        raise HTTPException(status_code=404, detail="Source not found in verified canonical ledger")
    return entry


@router.get("/quarantine", response_model=List[QuarantineItem])
def list_quarantined_items(
    engine: ScientificTrustFirewallEngine = Depends(get_trust_firewall)
):
    """
    Section 93: Lists quarantined objects failing trust firewall checks.
    """
    return engine.list_quarantine_items()


@router.get("/incidents", response_model=List[TrustIncident])
def list_trust_incidents(
    engine: ScientificTrustFirewallEngine = Depends(get_trust_firewall)
):
    """
    Section 101: Lists recorded trust and scientific integrity incidents.
    """
    return engine.list_incidents()


@router.get("/history/{object_id}", response_model=List[TrustAssessment])
def get_trust_history(
    object_id: str,
    engine: ScientificTrustFirewallEngine = Depends(get_trust_firewall)
):
    """
    Section 74 & 109: Retrieves historical trust assessments for temporal reconstruction.
    """
    return engine.get_trust_history(object_id)


@router.get("/certificates/{object_id}", response_model=ScientificTrustCertificate)
def get_trust_certificate(
    object_id: str,
    engine: ScientificTrustFirewallEngine = Depends(get_trust_firewall)
):
    """
    Section 178: Issues/retrieves cryptographically signed Scientific Trust Certificate.
    """
    cert = engine.issue_trust_certificate(object_id)
    if not cert:
        raise HTTPException(status_code=404, detail="No verified assessment found to issue certificate")
    return cert
