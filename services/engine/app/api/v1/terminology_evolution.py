"""ZMIE Global Medical Ontology & Terminology Evolution API Router.

Endpoints for:
- Context-aware term resolution (Term ≠ Concept)
- Cross-system mapping with strict UNKNOWN-FIRST policy
- Historical terminology preservation
- Deprecated terminology transitions (NAFLD -> MASLD)
- Ontology release diffing
- Downstream impact analysis
- Terminology governance & human review workflows
- License verification
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.models.terminology_evolution import (
    ConceptResolutionResponse,
    DeprecatedTermTransition,
    DownstreamImpactAnalysis,
    HistoricalTermRecord,
    MappingReviewTask,
    OntologyDiff,
    ReviewDecision,
    SemanticMapping,
)
from app.ontology.core import GlobalTerminologyEvolutionEngine

router = APIRouter(prefix="/terminology", tags=["Global Ontology & Terminology Evolution"])

_engine_instance = GlobalTerminologyEvolutionEngine()


def get_engine() -> GlobalTerminologyEvolutionEngine:
    return _engine_instance


# -------------------------------------------------------------
# Request Schemas
# -------------------------------------------------------------

class ResolveTermRequest(BaseModel):
    text: str
    domain_context: Optional[str] = None
    language: Optional[str] = None


class MapConceptsRequest(BaseModel):
    source_concept_id: str
    target_system: str


class ImpactAnalysisRequest(BaseModel):
    concept_id: str


class ReviewDecisionRequest(BaseModel):
    task_id: str
    reviewer_name: str
    decision: ReviewDecision
    review_notes: str


# -------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------

@router.post("/resolve", response_model=ConceptResolutionResponse)
async def resolve_medical_term(
    req: ResolveTermRequest,
    engine: GlobalTerminologyEvolutionEngine = Depends(get_engine),
):
    """Contextually resolves surface medical expressions to concepts with uncertainty preservation."""
    return engine.resolve_term(
        text=req.text,
        domain_context=req.domain_context,
        language=req.language,
    )


@router.post("/map", response_model=SemanticMapping)
async def map_cross_system_concepts(
    req: MapConceptsRequest,
    engine: GlobalTerminologyEvolutionEngine = Depends(get_engine),
):
    """Retrieves explicit cross-system semantic mapping. Returns NO_VALID_MAPPING if unmapped."""
    mapping = engine.map_concepts(req.source_concept_id, req.target_system)
    if not mapping:
        raise HTTPException(status_code=404, detail=f"Source concept {req.source_concept_id} not found.")
    return mapping


@router.get("/historical/{term}", response_model=HistoricalTermRecord)
async def get_historical_term(
    term: str,
    engine: GlobalTerminologyEvolutionEngine = Depends(get_engine),
):
    """Retrieves historical medical terminology without modern diagnostic retrofitting."""
    record = engine.get_historical_term(term)
    if not record:
        raise HTTPException(status_code=404, detail=f"Historical term '{term}' not found in historical codex.")
    return record


@router.get("/deprecated/{concept_id}", response_model=DeprecatedTermTransition)
async def get_deprecated_transition(
    concept_id: str,
    engine: GlobalTerminologyEvolutionEngine = Depends(get_engine),
):
    """Retrieves deprecation and reclassification transition record (e.g. NAFLD -> MASLD)."""
    trans = engine.get_deprecated_transition(concept_id)
    if not trans:
        raise HTTPException(status_code=404, detail=f"No deprecation transition record for {concept_id}.")
    return trans


@router.get("/ontologies/diff", response_model=OntologyDiff)
async def get_ontology_diff(
    ontology_name: str = Query("SNOMED-CT", description="Name of ontology system"),
    previous_version: str = Query("2024-01", description="Baseline release version"),
    current_version: str = Query("2025-01", description="Updated release version"),
    engine: GlobalTerminologyEvolutionEngine = Depends(get_engine),
):
    """Generates comprehensive semantic diff between two external ontology releases."""
    return engine.generate_ontology_diff(ontology_name, previous_version, current_version)


@router.post("/impact-analysis", response_model=DownstreamImpactAnalysis)
async def analyze_downstream_impact(
    req: ImpactAnalysisRequest,
    engine: GlobalTerminologyEvolutionEngine = Depends(get_engine),
):
    """Traces claims, studies, guidelines, and APIs impacted by ontology evolution."""
    try:
        return engine.analyze_downstream_impact(req.concept_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/governance/submit", response_model=MappingReviewTask)
async def submit_candidate_mapping(
    mapping: SemanticMapping,
    engine: GlobalTerminologyEvolutionEngine = Depends(get_engine),
):
    """Submits candidate mapping to governance queue. AI cannot directly make mappings authoritative."""
    return engine.submit_mapping_for_review(mapping)


@router.post("/governance/decision", response_model=SemanticMapping)
async def record_review_decision(
    req: ReviewDecisionRequest,
    engine: GlobalTerminologyEvolutionEngine = Depends(get_engine),
):
    """Records human expert review decision, promoting or rejecting candidate mappings."""
    try:
        return engine.record_review_decision(
            task_id=req.task_id,
            reviewer_name=req.reviewer_name,
            decision=req.decision,
            review_notes=req.review_notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/licenses/verify-export")
async def verify_license_export(
    vocabulary_name: str = Query(..., description="Vocabulary to check export license"),
    engine: GlobalTerminologyEvolutionEngine = Depends(get_engine),
):
    """Verifies intellectual property and licensing rights before allowing vocabulary export."""
    allowed, reason = engine.verify_export_license(vocabulary_name)
    return {
        "vocabulary_name": vocabulary_name,
        "export_allowed": allowed,
        "policy_message": reason,
    }
