"""
ZMIE Safety & Retraction API Router
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.agents.safety_agent import SafetyIntelligenceEngine, SafetyCheckResult
from app.agents.retraction_monitor import RetractionMonitor
from app.research.ddhg_engine import DeepDrugHerbGeneEngine, DDHGAnalysisReport

router = APIRouter(prefix="/safety", tags=["Clinical Safety & Retraction Watch"])


class SafetyEvaluationRequest(BaseModel):
    substance: str
    patient_conditions: Optional[List[str]] = []
    medications: Optional[List[str]] = []
    symptoms: Optional[List[str]] = []


@router.post("/evaluate", response_model=SafetyCheckResult)
async def evaluate_clinical_safety(request: SafetyEvaluationRequest):
    """
    Evaluates herb-drug interactions, emergency red-flags, and contraindications.
    """
    return SafetyIntelligenceEngine.evaluate_safety(
        entity=request.substance,
        patient_conditions=request.patient_conditions,
        concurrent_medications=request.medications,
        reported_symptoms=request.symptoms
    )


@router.get("/retraction-check")
async def check_retraction_status(doi: str = Query(..., description="DOI of the biomedical paper to verify")):
    """
    Checks paper against Crossref Retraction Watch registry.
    """
    return RetractionMonitor.check_document_status(doi=doi)


class HerbDrugSimulationRequest(BaseModel):
    drugs: List[str]
    herbs: List[str]
    patient_factors: Optional[dict] = None


@router.post("/simulate")
async def simulate_herb_drug_interactions(request: HerbDrugSimulationRequest):
    """
    Simulates multi-target pharmacokinetic & pharmacodynamic hazard matrix between Allopathic drugs and Traditional botanicals.
    """
    return SafetyIntelligenceEngine.simulate_herb_drug_interaction(
        drugs=request.drugs,
        herbs=request.herbs,
        patient_factors=request.patient_factors
    )


@router.get("/catalog")
async def get_safety_catalog():
    """
    Returns full clinical inventory of indexed botanicals, pharmaceuticals, CYP450/UGT enzymes, and transporters.
    """
    return SafetyIntelligenceEngine.get_interaction_catalog()


class DDHGCheckRequest(BaseModel):
    drugs: List[str]
    herbs: List[str]
    genetic_variants: Optional[List[dict]] = None
    patient_factors: Optional[dict] = None


@router.post("/ddhg-check", response_model=DDHGAnalysisReport)
async def deep_drug_herb_gene_check(request: DDHGCheckRequest):
    """
    Deep Drug-Herb-Gene (DDHG) Pharmacogenomic Safety Evaluation (Phase 3):
    Evaluates unified multi-target pharmacokinetic & pharmacodynamic hazard matrix
    across Allopathic Drugs, 657 Catalogued Botanicals, and CPIC Human Genetic Variants.
    """
    return DeepDrugHerbGeneEngine.evaluate_ddhg_profile(
        drugs=request.drugs,
        herbs=request.herbs,
        genetic_variants=request.genetic_variants,
        patient_factors=request.patient_factors
    )

