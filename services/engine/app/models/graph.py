"""
ZMIE Semantic Intelligence Core: Graph, Evidence & Medical Ontology Models
Defines the canonical data structures for:
1. Medical Knowledge Graph (Entities, Concepts, Relations, Hierarchies, Synonyms)
2. Evidence Graph (Claims, Evidence, Studies, PICO Context, Contradictions, Evidence Ladder E0-E6)
3. Provenance Graph (Source, Document, Passage Anchors, Version, Release)
4. Cross-System Epistemic Taxonomy (Unani, Ayurveda, TCM, Modern Biomedicine)
"""

from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from app.models.claim import MedicalSystem, EvidenceGrade, StudyDesign, PICOContext
from app.models.source import AuthorityTier, LicenseClass


# =====================================================================
# 1. ONTOLOGY & LIFECYCLE ENUMS
# =====================================================================

class ConceptLifecycleStatus(str, Enum):
    PROPOSED = "PROPOSED"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    SUPERSEDED = "SUPERSEDED"
    MERGED = "MERGED"
    SPLIT = "SPLIT"
    REJECTED = "REJECTED"
    HISTORICAL = "HISTORICAL"


class HierarchyPredicate(str, Enum):
    IS_A = "IS_A"
    SUBCLASS_OF = "SUBCLASS_OF"
    PART_OF = "PART_OF"
    LOCATED_IN = "LOCATED_IN"
    HAS_PART = "HAS_PART"
    INSTANCE_OF = "INSTANCE_OF"


class SynonymType(str, Enum):
    EXACT_SYNONYM = "EXACT_SYNONYM"
    LEXICAL_VARIANT = "LEXICAL_VARIANT"
    ABBREVIATION = "ABBREVIATION"
    COMMON_NAME = "COMMON_NAME"
    SCIENTIFIC_NAME = "SCIENTIFIC_NAME"
    HISTORICAL_NAME = "HISTORICAL_NAME"
    BRAND_NAME = "BRAND_NAME"
    TRANSLITERATION = "TRANSLITERATION"
    TRANSLATION = "TRANSLATION"
    REGIONAL_NAME = "REGIONAL_NAME"


class CrossSystemMappingType(str, Enum):
    EXACT_EQUIVALENCE = "EXACT_EQUIVALENCE"
    CLOSE_EQUIVALENCE = "CLOSE_EQUIVALENCE"
    PARTIAL_OVERLAP = "PARTIAL_OVERLAP"
    RELATED_CONCEPT = "RELATED_CONCEPT"
    FUNCTIONAL_ANALOGY = "FUNCTIONAL_ANALOGY"
    HISTORICAL_ASSOCIATION = "HISTORICAL_ASSOCIATION"
    RESEARCH_HYPOTHESIS = "RESEARCH_HYPOTHESIS"
    NO_VALIDATED_MAPPING = "NO_VALIDATED_MAPPING"
    CONFLICTING = "CONFLICTING"
    UNKNOWN = "UNKNOWN"


# =====================================================================
# 2. CONTROLLED RELATIONSHIP PREDICATES (SECTION 10)
# =====================================================================

class ControlledPredicate(str, Enum):
    # Causal & Clinical Associations
    ASSOCIATED_WITH = "ASSOCIATED_WITH"
    CAUSES = "CAUSES"
    MAY_CAUSE = "MAY_CAUSE"
    CONTRIBUTES_TO = "CONTRIBUTES_TO"
    PREDISPOSES_TO = "PREDISPOSES_TO"
    PREVENTS = "PREVENTS"
    MAY_PREVENT = "MAY_PREVENT"
    TREATS = "TREATS"
    MAY_TREAT = "MAY_TREAT"
    SUPPORTS_TREATMENT_OF = "SUPPORTS_TREATMENT_OF"

    # Clinical Safety & Interactions
    INDICATED_FOR = "INDICATED_FOR"
    CONTRAINDICATED_IN = "CONTRAINDICATED_IN"
    INTERACTS_WITH = "INTERACTS_WITH"
    INCREASES_EFFECT = "INCREASES_EFFECT"
    DECREASES_EFFECT = "DECREASES_EFFECT"

    # Clinical Manifestations & Markers
    HAS_SYMPTOM = "HAS_SYMPTOM"
    HAS_SIGN = "HAS_SIGN"
    HAS_BIOMARKER = "HAS_BIOMARKER"

    # Molecular & Pharmacological Mechanism
    HAS_TARGET = "HAS_TARGET"
    TARGETS = "TARGETS"
    ACTS_ON = "ACTS_ON"
    MODULATES = "MODULATES"
    INHIBITS = "INHIBITS"
    ACTIVATES = "ACTIVATES"

    # Structural & Compositional
    PART_OF = "PART_OF"
    LOCATED_IN = "LOCATED_IN"
    DERIVED_FROM = "DERIVED_FROM"
    CONTAINS = "CONTAINS"
    COMPOSED_OF = "COMPOSED_OF"

    # Traditional & Humoral Actions (Unani / Ayurveda / TCM)
    HAS_MIZAJ = "HAS_MIZAJ"
    HAS_AFAAL = "HAS_AFAAL"
    HAS_MIZAJ_OF_DRUG = "HAS_MIZAJ_OF_DRUG"
    USED_IN_FORMULATION = "USED_IN_FORMULATION"
    USED_FOR = "USED_FOR"

    # Cross-System & Comparative
    SIMILAR_TO = "SIMILAR_TO"
    RELATED_TO = "RELATED_TO"
    ANALOGOUS_TO = "ANALOGOUS_TO"
    MAPPED_TO = "MAPPED_TO"
    PARTIALLY_OVERLAPS = "PARTIALLY_OVERLAPS"

    # Evidence & Epistemic
    SUPPORTED_BY = "SUPPORTED_BY"
    CONTRADICTED_BY = "CONTRADICTED_BY"
    QUALIFIED_BY = "QUALIFIED_BY"


# =====================================================================
# 3. EVIDENCE LADDER & STATUS (SECTIONS 16-18, 71)
# =====================================================================

class EvidenceLadder(str, Enum):
    E0_AI_HYPOTHESIS = "E0_ai_hypothesis"
    E1_LITERATURE_ASSOCIATION = "E1_literature_association"
    E2_COMPUTATIONAL = "E2_computational_in_silico"
    E3_IN_VITRO = "E3_in_vitro_mechanistic"
    E4_IN_VIVO_PRECLINICAL = "E4_in_vivo_preclinical"
    E5_HUMAN_OBSERVATIONAL = "E5_human_observational_exposure"
    E6_CONTROLLED_CLINICAL = "E6_controlled_clinical_evidence"


class EvidenceStatus(str, Enum):
    SUPPORTS = "SUPPORTS"
    PARTIALLY_SUPPORTS = "PARTIALLY_SUPPORTS"
    MIXED = "MIXED"
    CONTRADICTS = "CONTRADICTS"
    INSUFFICIENT = "INSUFFICIENT"
    NO_EFFECT = "NO_EFFECT"
    UNKNOWN = "UNKNOWN"


class KnowledgeStatus(str, Enum):
    ESTABLISHED = "ESTABLISHED"
    SUPPORTED = "SUPPORTED"
    EMERGING = "EMERGING"
    PRELIMINARY = "PRELIMINARY"
    CONFLICTING = "CONFLICTING"
    HYPOTHESIS = "HYPOTHESIS"
    INSUFFICIENT = "INSUFFICIENT"
    UNKNOWN = "UNKNOWN"
    RETRACTED = "RETRACTED"


class InferenceType(str, Enum):
    DIRECT_FACT = "DIRECT_FACT"
    SUPPORTED_RELATION = "SUPPORTED_RELATION"
    DERIVED_RELATION = "DERIVED_RELATION"
    COMPUTATIONAL_INFERENCE = "COMPUTATIONAL_INFERENCE"
    RESEARCH_HYPOTHESIS = "RESEARCH_HYPOTHESIS"


class EdgeTemporalStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    RETRACTED = "RETRACTED"
    HISTORICAL = "HISTORICAL"
    CONTEXT_DEPENDENT = "CONTEXT_DEPENDENT"
    UNKNOWN = "UNKNOWN"


# =====================================================================
# 4. CORE OBJECTS: TERMS, CONCEPTS & ENTITIES
# =====================================================================

class MedicalTerm(BaseModel):
    """
    Linguistic representation of a concept in a specific language and script.
    """
    term_id: str
    concept_id: str
    term_text: str
    language: str = Field(..., description="'en', 'ur', 'ar', 'fa', 'sa', 'hi', 'zh', 'la'")
    script: str = Field(..., description="'Latin', 'Arabic/Nastaliq', 'Devanagari', 'Simplified Hanzi'")
    romanization: Optional[str] = None
    transliteration_system: Optional[str] = None
    synonym_type: SynonymType = SynonymType.EXACT_SYNONYM
    is_preferred: bool = False
    source: Optional[str] = None


class CanonicalConcept(BaseModel):
    """
    First-class semantic concept object independent of linguistic terms.
    """
    concept_id: str
    canonical_name: str
    medical_system: MedicalSystem
    entity_class: str = Field(..., description="e.g. 'Condition', 'Drug', 'Plant', 'Mizaj', 'Dosha', 'Pathway'")
    definition: str
    lifecycle_status: ConceptLifecycleStatus = ConceptLifecycleStatus.ACTIVE
    parent_concept_ids: List[str] = Field(default_factory=list)
    hierarchy_relationships: List[Dict[str, str]] = Field(default_factory=list)
    terms: List[MedicalTerm] = Field(default_factory=list)
    classical_references: List[str] = Field(default_factory=list)
    historical_semantics: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"


# =====================================================================
# 5. EVIDENCE & CONTRADICTION OBJECTS (SECTIONS 16, 20)
# =====================================================================

class EvidenceObject(BaseModel):
    """
    First-class empirical evidence unit grounding a claim or graph relation.
    """
    evidence_id: str
    claim_id: str
    study_id: Optional[str] = None
    study_type: Optional[StudyDesign] = None
    evidence_level: EvidenceLadder
    evidence_status: EvidenceStatus
    pico_context: PICOContext
    
    # Quantitative Results
    effect_measure: Optional[str] = None # e.g. "Relative Risk", "Odds Ratio", "Mean Difference"
    effect_value: Optional[float] = None
    confidence_interval: Optional[str] = None # e.g. "95% CI [0.65, 0.88]"
    p_value: Optional[float] = None
    sample_size: Optional[int] = None
    
    # Methodological Quality & Limitations
    limitations: List[str] = Field(default_factory=list)
    risk_of_bias: Optional[str] = None # "low", "unclear", "high"
    
    # Provenance
    source_id: str
    document_id: str
    section_name: Optional[str] = None
    page: Optional[int] = None
    paragraph_anchor_hash: Optional[str] = None
    
    extraction_confidence: float = Field(default=0.95, ge=0.0, le=1.0)
    is_retracted: bool = False
    retraction_reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ContradictionRecord(BaseModel):
    """
    Explicit model for divergent or conflicting findings across studies.
    Preserves both sides without artificial reconciliation.
    """
    contradiction_id: str
    relation_id: str
    supporting_claim_ids: List[str]
    contradicting_claim_ids: List[str]
    disagreement_reasons: List[str] = Field(
        default_factory=list,
        description="e.g. 'different population', 'different dose', 'different species', 'different endpoint'"
    )
    possible_explanations: List[str] = Field(default_factory=list)
    detected_at: datetime = Field(default_factory=datetime.utcnow)


# =====================================================================
# 6. RICH RELATIONSHIP / EDGE MODEL (SECTIONS 11, 12, 40)
# =====================================================================

class RelationshipEdge(BaseModel):
    """
    Rich relationship object connecting two concept entities in the graph.
    Never a simple subject-predicate-object tuple; carries full context & evidence.
    """
    relation_id: str
    subject_id: str
    predicate: ControlledPredicate
    object_id: str
    
    medical_system: MedicalSystem
    inference_type: InferenceType = InferenceType.SUPPORTED_RELATION
    temporal_status: EdgeTemporalStatus = EdgeTemporalStatus.ACTIVE
    knowledge_status: KnowledgeStatus = KnowledgeStatus.SUPPORTED
    
    # Context & Qualifiers
    qualifiers: Dict[str, Any] = Field(
        default_factory=dict,
        description="Specific qualifiers: population, dose, route, formulation, species, duration, age, etc."
    )
    
    # Evidence & Claims Attachment
    supporting_claim_ids: List[str] = Field(default_factory=list)
    contradicting_claim_ids: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    evidence_level: EvidenceLadder = EvidenceLadder.E1_LITERATURE_ASSOCIATION
    evidence_status: EvidenceStatus = EvidenceStatus.SUPPORTS
    
    # Provenance & Audit
    source_ids: List[str] = Field(default_factory=list)
    document_ids: List[str] = Field(default_factory=list)
    
    # Multi-dimensional Confidence
    confidence_dimensions: Dict[str, float] = Field(
        default_factory=lambda: {
            "source_authority": 0.85,
            "evidence_strength": 0.80,
            "mapping_confidence": 0.90,
            "extraction_confidence": 0.95,
            "clinical_relevance": 0.85
        }
    )
    
    # Temporal Validity
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    superseded_by: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    knowledge_version: str = "1.0"
