"""ZMIE Global Medical Ontology & Terminology Evolution Engine Models.

Defines schemas for:
- Absolute Rule: Term ≠ Concept ≠ Entity ≠ Clinical Reality ≠ Ontological Meaning ≠ Evidence
- Semantic Types (Clinical, Biological, Pharmaceutical, Research, Regulatory, Traditional)
- Mapping Types (Exact, Near, Partial, Broader, Narrower, Traditional Correspondence, False Friend, Unknown)
- Multilingual, Script, Transliteration, and Dialect Models
- Historical Terminology, Temporal States, and Deprecation
- Emerging Terminology Pipeline
- Ontology Releases, Diffing, and Downstream Impact Analysis
- Governance, Expert Review, and Double-Review Policies
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EpistemicCertainty(str, Enum):
    UNREVIEWED = "UNREVIEWED"
    CANDIDATE = "CANDIDATE"
    SUPPORTED = "SUPPORTED"
    EXPERT_REVIEWED = "EXPERT_REVIEWED"
    AUTHORITATIVE = "AUTHORITATIVE"
    CONTESTED = "CONTESTED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"


class SemanticDomain(str, Enum):
    CLINICAL = "CLINICAL"
    BIOLOGICAL = "BIOLOGICAL"
    PHARMACEUTICAL = "PHARMACEUTICAL"
    RESEARCH = "RESEARCH"
    REGULATORY = "REGULATORY"
    TRADITIONAL_UNANI = "TRADITIONAL_UNANI"
    TRADITIONAL_AYURVEDA = "TRADITIONAL_AYURVEDA"
    TRADITIONAL_TCM = "TRADITIONAL_TCM"
    HISTORICAL = "HISTORICAL"


class MappingType(str, Enum):
    EXACT_EQUIVALENCE = "EXACT_EQUIVALENCE"
    NEAR_EQUIVALENCE = "NEAR_EQUIVALENCE"
    PARTIAL_EQUIVALENCE = "PARTIAL_EQUIVALENCE"
    BROADER_MAPPING = "BROADER_MAPPING"
    NARROWER_MAPPING = "NARROWER_MAPPING"
    RELATED_MAPPING = "RELATED_MAPPING"
    OVERLAPPING_MAPPING = "OVERLAPPING_MAPPING"
    CONTEXT_DEPENDENT_MAPPING = "CONTEXT_DEPENDENT_MAPPING"
    HISTORICAL_CORRESPONDENCE = "HISTORICAL_CORRESPONDENCE"
    TRADITIONAL_CORRESPONDENCE = "TRADITIONAL_CORRESPONDENCE"
    PHENOTYPIC_CORRESPONDENCE = "PHENOTYPIC_CORRESPONDENCE"
    FUNCTIONAL_CORRESPONDENCE = "FUNCTIONAL_CORRESPONDENCE"
    FALSE_FRIEND = "FALSE_FRIEND"
    NO_VALID_MAPPING = "NO_VALID_MAPPING"
    UNKNOWN_MAPPING = "UNKNOWN_MAPPING"
    CONTESTED_MAPPING = "CONTESTED_MAPPING"


class ConceptStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EMERGING = "EMERGING"
    CANDIDATE = "CANDIDATE"
    DEPRECATED = "DEPRECATED"
    REPLACED = "REPLACED"
    MERGED = "MERGED"
    SPLIT = "SPLIT"
    HISTORICAL_PRESERVED = "HISTORICAL_PRESERVED"


class DefinitionType(str, Enum):
    SOURCE_DEFINITION = "SOURCE_DEFINITION"
    ZMIE_NORMALIZED_DESCRIPTION = "ZMIE_NORMALIZED_DESCRIPTION"
    AI_SYNTHESIS = "AI_SYNTHESIS"
    EXPERT_APPROVED_DESCRIPTION = "EXPERT_APPROVED_DESCRIPTION"
    HISTORICAL_DEFINITION = "HISTORICAL_DEFINITION"
    TRADITIONAL_DEFINITION = "TRADITIONAL_DEFINITION"


class ReviewDecision(str, Enum):
    APPROVE = "APPROVE"
    APPROVE_WITH_SCOPE = "APPROVE_WITH_SCOPE"
    PARTIAL = "PARTIAL"
    REJECT = "REJECT"
    CONTESTED = "CONTESTED"
    REQUEST_MORE_EVIDENCE = "REQUEST_MORE_EVIDENCE"


# -------------------------------------------------------------
# Core Term & Concept Models
# -------------------------------------------------------------

class LexicalVariant(BaseModel):
    """Surface form, script, transliteration, and grammatical variation."""
    variant_id: str
    surface_form: str
    normalized_form: str
    language: str = "en"  # en, ur, ar, hi, sa, fa, zh, la
    script: str = "Latin"  # Latin, Arabic, Devanagari, Han
    transliteration: Optional[str] = None
    variant_type: str = "SYNONYM"  # SPELLING, ABBREVIATION, TRANSLITERATION, HISTORICAL, REGIONAL, PLURAL
    is_preferred: bool = False


class ConceptDefinition(BaseModel):
    """Source-governed definition with immutable origin."""
    definition_id: str
    definition_text: str
    definition_type: DefinitionType
    source: str
    language: str = "en"
    historical_period: Optional[str] = None
    authority: str = "OFFICIAL"
    status: str = "ACTIVE"
    created_at: str


class MedicalConcept(BaseModel):
    """First-class semantic concept distinct from surface lexical terms."""
    concept_id: str
    canonical_label: str
    preferred_label: str
    semantic_domain: SemanticDomain
    semantic_type: str  # Disease, Drug, Target, Phenotype, ConstitutionalMizaj, Dosha, etc.
    definitions: List[ConceptDefinition] = Field(default_factory=list)
    ontology_memberships: List[str] = Field(default_factory=list)  # SNOMED, ICD-11, LOINC, MeSH, UNANI_CODEX, AYUSH
    codes: Dict[str, str] = Field(default_factory=dict)  # e.g., {"SNOMED": "195967001", "ICD11": "5B81"}
    status: ConceptStatus = ConceptStatus.ACTIVE
    current_version: str = "v1.0"
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    deprecated_replacement_concept_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: str
    updated_at: str


# -------------------------------------------------------------
# Mapping, Cross-System & False-Friends Models
# -------------------------------------------------------------

class SemanticMapping(BaseModel):
    """Explicit, contextual semantic bridge between two concepts."""
    mapping_id: str
    source_concept_id: str
    target_concept_id: str
    source_system: str
    target_system: str
    mapping_type: MappingType
    context_qualifier: Optional[str] = None  # e.g. "Cardiology setting only", "Functional analogy, not molecular identity"
    assurance_state: EpistemicCertainty = EpistemicCertainty.CANDIDATE
    lexical_similarity: float = Field(default=0.5, ge=0.0, le=1.0)
    context_similarity: float = Field(default=0.5, ge=0.0, le=1.0)
    definition_similarity: float = Field(default=0.5, ge=0.0, le=1.0)
    provenance_source: str
    expert_reviewers: List[str] = Field(default_factory=list)
    requires_double_review: bool = False
    evidence_notes: str = ""
    known_differences: List[str] = Field(default_factory=list)
    unmapped_aspects: List[str] = Field(default_factory=list)
    version: str = "v1.0"
    created_at: str
    updated_at: str


class FalseFriendAssertion(BaseModel):
    """Explicit guard declaring two terms look alike but mean distinct things."""
    assertion_id: str
    term_a: str
    system_a: str
    concept_a_id: str
    term_b: str
    system_b: str
    concept_b_id: str
    distinction_explanation: str
    evidence_source: str


# -------------------------------------------------------------
# Historical & Deprecated Terminology Models
# -------------------------------------------------------------

class HistoricalTermRecord(BaseModel):
    """Preserves historical terminology without retrofitting modern biomedical concepts."""
    historical_id: str
    term: str
    historical_period: str  # e.g. "18th Century", "Classical Greco-Arab Antiquity", "Vedic Era"
    historical_definition: str
    historical_source: str
    modern_correspondence_concept_id: Optional[str] = None
    mapping_type: MappingType = MappingType.HISTORICAL_CORRESPONDENCE
    epistemic_warning: str = (
        "STRICT HISTORICAL BOUNDARY: Historical term must not be conflated with contemporary "
        "pathophysiological diagnosis. Preserved in its original scientific and historical context."
    )


class DeprecatedTermTransition(BaseModel):
    """Tracks modern terminology deprecation and reclassification (e.g. NAFLD -> MASLD)."""
    transition_id: str
    deprecated_term: str
    deprecated_concept_id: str
    replacement_term: str
    replacement_concept_id: str
    transition_date: str
    consensus_body: str  # e.g. "AASLD / EASL Multinational Consensus"
    scientific_rationale: str
    downstream_impact_count: int = 0


# -------------------------------------------------------------
# Emerging Terminology & Candidate Models
# -------------------------------------------------------------

class EmergingTermCandidate(BaseModel):
    """Newly detected lexical candidate from literature or trials."""
    candidate_id: str
    term: str
    first_detected_date: str
    source_document_id: str
    occurrence_frequency: int = 1
    extracted_contexts: List[str] = Field(default_factory=list)
    suggested_semantic_type: str
    status: ConceptStatus = ConceptStatus.EMERGING
    reviewed_by: Optional[str] = None


# -------------------------------------------------------------
# Ontology Release, Diff & Downstream Impact Models
# -------------------------------------------------------------

class OntologyRelease(BaseModel):
    """Immutable release snapshot of an ontology system."""
    release_id: str
    ontology_name: str  # SNOMED-CT, ICD-11, LOINC, UNANI-CORE
    version_tag: str
    release_date: str
    concepts_count: int
    license_type: str
    is_authoritative: bool = True


class OntologyDiff(BaseModel):
    """Quantified diff between two ontology releases."""
    diff_id: str
    ontology_name: str
    previous_version: str
    current_version: str
    added_concepts: List[str] = Field(default_factory=list)
    removed_concepts: List[str] = Field(default_factory=list)
    renamed_concepts: List[Dict[str, str]] = Field(default_factory=list)  # [{"id": "...", "old": "...", "new": "..."}]
    deprecated_concepts: List[str] = Field(default_factory=list)
    merged_concepts: List[Dict[str, Any]] = Field(default_factory=list)
    split_concepts: List[Dict[str, Any]] = Field(default_factory=list)
    generated_at: str


class DownstreamImpactAnalysis(BaseModel):
    """Traces downstream research, clinical, and regulatory entities affected by ontology changes."""
    analysis_id: str
    concept_id: str
    concept_label: str
    change_type: str  # RENAMED, DEPRECATED, SPLIT, MERGED
    affected_claims_count: int
    affected_studies_count: int
    affected_guidelines_count: int
    affected_rwe_cohorts_count: int
    affected_apis_count: int
    impact_severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    remediation_recommendations: List[str] = Field(default_factory=list)


# -------------------------------------------------------------
# Governance, Review & Resolution Models
# -------------------------------------------------------------

class MappingReviewTask(BaseModel):
    """Human review assignment for candidate semantic mappings."""
    task_id: str
    mapping_id: str
    assigned_reviewer: str
    reviewer_role: str  # "CLINICAL_EXPERT", "TRADITIONAL_MEDICINE_EXPERT", "PHARMACOLOGIST"
    decision: ReviewDecision = ReviewDecision.REQUEST_MORE_EVIDENCE
    review_notes: str = ""
    is_second_review: bool = False
    reviewed_at: Optional[str] = None


class ConceptResolutionResponse(BaseModel):
    """Output of context-aware terminology resolution."""
    input_text: str
    language_detected: str
    script_detected: str
    normalized_surface_form: str
    domain_context: Optional[str] = None
    candidate_concepts: List[Dict[str, Any]] = Field(default_factory=list)
    selected_concept: Optional[MedicalConcept] = None
    is_ambiguous: bool = False
    ambiguity_explanation: Optional[str] = None
    is_false_friend: bool = False
    false_friend_warning: Optional[str] = None
    assurance_state: EpistemicCertainty = EpistemicCertainty.UNREVIEWED
    provenance_chain: List[str] = Field(default_factory=list)
    epistemic_disclaimer: str = (
        "STRICT SEMANTIC PRINCIPLE: Term ≠ Concept ≠ Clinical Reality. "
        "Contextual resolution applied with explicit uncertainty preservation."
    )
