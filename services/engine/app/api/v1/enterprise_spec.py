"""
ZMIE Enterprise Specification & Production Build REST API Gateway (Prompt 27)
Exposes endpoints for the Master Architecture Map, Architecture Decision Records (ADRs),
Platform Invariants, Deployment Capability Matrix, and Production Readiness Reports (Clauses 1-144).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.enterprise_spec import (
    get_enterprise_spec_engine,
    ArchitectureLayerSpec,
    ArchitectureDecisionRecord,
    PlatformInvariant,
    DeploymentCapabilityRow,
    BuildMatrixRow,
    ProductionReadinessReport,
)

router = APIRouter(prefix="/spec", tags=["Enterprise Implementation & Production Build Specification"])


@router.get("/architecture/layers", response_model=List[ArchitectureLayerSpec])
def list_architecture_layers():
    """Retrieves the complete ZMIE Master Architecture Layer Reconciliation Map (Clause 3)."""
    engine = get_enterprise_spec_engine()
    return engine.list_layers()


@router.get("/architecture/layers/{layer_id}", response_model=ArchitectureLayerSpec)
def get_architecture_layer(layer_id: str):
    """Retrieves detailed architecture specification for a specific layer."""
    engine = get_enterprise_spec_engine()
    layer = engine.get_layer(layer_id)
    if not layer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Layer {layer_id} not found.")
    return layer


@router.get("/architecture/adrs", response_model=List[ArchitectureDecisionRecord])
def list_adrs():
    """Retrieves all formal Architecture Decision Records (ADR-001 through ADR-015) (Clause 3)."""
    engine = get_enterprise_spec_engine()
    return engine.list_adrs()


@router.get("/architecture/adrs/{adr_id}", response_model=ArchitectureDecisionRecord)
def get_adr(adr_id: str):
    """Retrieves a specific Architecture Decision Record."""
    engine = get_enterprise_spec_engine()
    adr = engine.get_adr(adr_id)
    if not adr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ADR {adr_id} not found.")
    return adr


@router.get("/invariants", response_model=List[PlatformInvariant])
def list_platform_invariants():
    """Retrieves all non-negotiable platform integrity invariants (Clauses 4, 97)."""
    engine = get_enterprise_spec_engine()
    return engine.list_invariants()


@router.get("/invariants/verify", response_model=Dict[str, Any])
def verify_platform_invariants():
    """Rigorously verifies active enforcement of all platform invariants (Clause 97)."""
    engine = get_enterprise_spec_engine()
    return engine.verify_all_invariants()


@router.get("/deployment/matrix", response_model=List[DeploymentCapabilityRow])
def get_deployment_capability_matrix():
    """Retrieves feature capability matrix across deployment environments (Clause 6)."""
    engine = get_enterprise_spec_engine()
    return engine.list_deployment_capabilities()


@router.get("/build-matrix", response_model=List[BuildMatrixRow])
def get_build_matrix():
    """Retrieves the Master Build Matrix across all domains (Clause 103)."""
    engine = get_enterprise_spec_engine()
    return engine.get_build_matrix()


@router.get("/readiness", response_model=ProductionReadinessReport)
def get_production_readiness_report():
    """Evaluates readiness across all 20 required production domains (Clause 144)."""
    engine = get_enterprise_spec_engine()
    return engine.get_production_readiness_report()
