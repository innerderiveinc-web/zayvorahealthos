"""
ZMIE Atomic Claim Passport & Evidence Engine Models
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class MedicalSystem(str, Enum):
    MODERN = "modern_biomedicine"
    UNANI = "unani_tibb"
    AYURVEDA = "ayurveda"
    SIDDHA = "siddha"
    TCM = "traditional_chinese_medicine"
    SOWA_RIGPA = "sowa_rigpa"
    INTEGRATIVE = "integrative"


class EvidenceGrade(str, Enum):
    AUTHORITATIVE_GUIDELINE = "authoritative_guideline"
    SYSTEMATIC_REVIEW = "systematic_review_meta_analysis"
    CONTROLLED_HUMAN_RCT = "controlled_human_evidence"
    OBSERVATIONAL_HUMAN = "observational_human_evidence"
    PRECLINICAL_IN_VIVO = "preclinical_in_vivo"
    IN_VITRO = "in_vitro_mechanistic"
    COMPUTATIONAL = "computational_in_silico"
    CANONICAL_TRADITIONAL = "canonical_traditional_claim"
    HISTORICAL_USE = "historical_anecdotal_use"
    CONFLICTING = "conflicting_evidence"
    INSUFFICIENT = "insufficient_evidence"
    UNKNOWN = "unknown"


class StudyDesign(str, Enum):
    DOUBLE_BLIND_RCT = "double_blind_rct"
    OPEN_LABEL_RCT = "open_label_rct"
    PROSPECTIVE_COHORT = "prospective_cohort"
    RETROSPECTIVE_COHORT = "retrospective_cohort"
    CASE_CONTROL = "case_control"
    SYSTEMATIC_REVIEW = "systematic_review"
    ANIMAL_IN_VIVO = "animal_in_vivo"
    CELL_LINE_IN_VITRO = "cell_line_in_vitro"
    CLASSICAL_TEXT_CODEX = "classical_text_codex"


class PICOContext(BaseModel):
    """
    Standardized Evidence Context: Under what exact conditions was this observed?
    """
    population_species: str = Field(..., description="'human', 'rat', 'in_vitro_cell'")
    age_group: Optional[str] = None
    sex: Optional[str] = None
    condition_or_phenotype: str = Field(..., description="Target pathology or physiological state")
    condition_severity: Optional[str] = None
    intervention_agent: str = Field(..., description="Molecule, compound, extract, or procedure")
    preparation_or_formulation: Optional[str] = Field(None, description="e.g., 'standardized 97% berberine HCl', 'Majun Falasifa decoction'")
    dose: Optional[str] = None
    route: Optional[str] = None
    duration: Optional[str] = None
    comparator: Optional[str] = Field(None, description="Placebo, Metformin, standard of care, etc.")


class ClaimPassport(BaseModel):
    """
    The atomic scientific and medical truth unit in ZMIE.
    Every claim generated or retrieved carries its full audit trail.
    """
    claim_id: str = Field(..., description="Persistent UUID (e.g., CLM-2026-X9921)")
    claim_text: str = Field(..., description="Normalized, atomic medical assertion")
    source_id: str = Field(..., description="Foreign key to Source Registry")
    document_id: str = Field(..., description="Foreign key to Document Storage (DOI/PMID/Work ID)")
    
    # Precise Provenance
    section_name: Optional[str] = None
    page_number: Optional[int] = None
    paragraph_hash: Optional[str] = None
    
    # Epistemology & Medical System
    medical_system: MedicalSystem
    evidence_tier: EvidenceGrade
    study_design: Optional[StudyDesign] = None
    
    # Detailed Evidence Context (PICO)
    context: PICOContext
    
    # Outcomes and Biomarkers
    outcomes_observed: List[Dict[str, Any]] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    
    # Cross-Source Verification Network
    supporting_claim_ids: List[str] = Field(default_factory=list)
    contradicting_claim_ids: List[str] = Field(default_factory=list)
    
    # Governance & Verification Status
    is_retracted: bool = False
    is_superseded: bool = False
    human_reviewed: bool = False
    reviewer_id: Optional[str] = None
    verification_timestamp: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
