"""
ZMIE Cross-System Ontology & Mapping Engine Models
"""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class CrossSystemMappingState(str, Enum):
    EXACT_EQUIVALENCE = "exact_equivalence"              # Direct biological/botanical match
    STRONG_RELATEDNESS = "strong_relatedness"            # Highly correlated conceptual/functional model
    PARTIAL_OVERLAP = "partial_overlap"                  # Shares characteristics but distinct scope
    FUNCTIONAL_ANALOGY = "functional_analogy"            # Analogous systemic behavior (e.g. Mizaj Damwi <-> metabolic tone)
    HISTORICAL_ASSOCIATION = "historical_association"    # Classical term referenced in early texts
    RESEARCH_HYPOTHESIS = "research_hypothesis"          # Active scientific trial investigating mapping
    CONFLICTING_PARADIGM = "conflicting_paradigm"        # Fundamentally contradictory foundational theories
    NO_VALIDATED_MAPPING = "no_validated_mapping"        # Valid concept in System A with no counterpart in System B
    UNKNOWN = "unknown"


class ConceptNode(BaseModel):
    """
    Universal concept node across Modern, Unani, Ayurveda, or TCM.
    Preserves original language transliteration and epistemological meaning.
    """
    concept_id: str = Field(..., description="e.g. CON-UNANI-MIZAJ-01, CON-AYUR-PRAKRITI-01, CON-BIOMED-HOMEOSTASIS")
    system: str = Field(..., description="'modern', 'unani', 'ayurveda', 'tcm'")
    canonical_name: str = Field(..., description="English or canonical Latin standard")
    original_script_name: Optional[str] = Field(None, description="Urdu/Arabic/Devanagari/Chinese script")
    transliteration: Optional[str] = None
    category: str = Field(..., description="'anatomy', 'pathology', 'physiology', 'pharmacology', 'constitutional'")
    definition: str
    classical_references: List[str] = Field(default_factory=list)


class CrossSystemRelation(BaseModel):
    """
    Explicit mapped edge between two distinct medical systems.
    Never flattens concepts; preserves nuances and epistemic caution.
    """
    relation_id: str
    source_concept_id: str
    target_concept_id: str
    mapping_state: CrossSystemMappingState
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    epistemic_rationale: str = Field(..., description="Explanation of why this mapping exists or why equivalence is rejected")
    supporting_literature_ids: List[str] = Field(default_factory=list)
    expert_validated: bool = False
