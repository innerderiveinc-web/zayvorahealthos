"""
ZMIE Production Readiness & Pre-Flight Certification FastAPI Router
Production Readiness Audit REST Gateway
"""

from typing import List, Dict, Optional, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.production_readiness.engine import ProductionReadinessEngine
from app.production_readiness.models import (
    ProductionReadinessCertificate,
    DomainAuditResult,
    ScopeReadinessResult,
    RiskItem,
    BlockerItem,
)

router = APIRouter(prefix="/production-readiness", tags=["Production Readiness Certification"])

# Global singleton
_readiness_engine = ProductionReadinessEngine()


def get_readiness_engine() -> ProductionReadinessEngine:
    return _readiness_engine


@router.post("/preflight-audit", response_model=ProductionReadinessCertificate)
def run_preflight_audit(
    engine: ProductionReadinessEngine = Depends(get_readiness_engine)
):
    """
    Executes comprehensive 7-pillar and 28-domain preflight audit and issues cryptographically signed certificate.
    """
    return engine.execute_preflight_audit()


@router.get("/certificates", response_model=List[ProductionReadinessCertificate])
def list_certificates(
    engine: ProductionReadinessEngine = Depends(get_readiness_engine)
):
    """
    Lists all issued production readiness certificates.
    """
    return engine.list_certificates()


@router.get("/certificates/{cert_id}", response_model=ProductionReadinessCertificate)
def get_certificate(
    cert_id: str,
    engine: ProductionReadinessEngine = Depends(get_readiness_engine)
):
    """
    Retrieves specific production readiness certificate by ID.
    """
    cert = engine.get_certificate(cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Production readiness certificate not found")
    return cert


@router.get("/domains", response_model=Dict[str, DomainAuditResult])
def get_domains_matrix(
    engine: ProductionReadinessEngine = Depends(get_readiness_engine)
):
    """
    Returns the comprehensive 28-domain production readiness audit matrix.
    """
    return engine.audit_all_28_domains()


@router.get("/scopes", response_model=Dict[str, ScopeReadinessResult])
def get_scope_profiles(
    engine: ProductionReadinessEngine = Depends(get_readiness_engine)
):
    """
    Returns the 9 targeted production readiness scope profiles.
    """
    return engine.audit_scope_profiles()


@router.get("/manifest", response_model=Dict[str, Any])
def get_release_manifest(
    engine: ProductionReadinessEngine = Depends(get_readiness_engine)
):
    """
    Returns the release candidate manifest (release.json) with hashes and component digests.
    """
    return engine.generate_release_manifest()


@router.get("/risks", response_model=List[RiskItem])
def get_risk_register(
    engine: ProductionReadinessEngine = Depends(get_readiness_engine)
):
    """
    Returns the active production risk register with residual risk classifications.
    """
    return engine.get_risk_register()


@router.get("/blockers", response_model=List[BlockerItem])
def get_blockers_registry(
    engine: ProductionReadinessEngine = Depends(get_readiness_engine)
):
    """
    Returns the verified production blocker registry.
    """
    return engine.get_blocker_registry()
