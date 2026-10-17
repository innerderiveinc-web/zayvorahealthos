"""
ZMIE Global Medical Source Universe Models
Defines contracts for:
- Source taxonomy, classes, authority levels (S0-S6), and licensing states
- Medical systems (Modern, Unani, Ayurveda, Siddha, TCM, Sowa-Rigpa, Regional, Classical)
- Canonical Study identity resolution across trial registries and publications
- Source records, discovery candidates, and quality profiles
- Source coverage matrix, research snapshots, and search attribution
- Retraction, correction, and safety invalidation events
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class SourceClass(str, Enum):
    SCHOLARLY_LITERATURE = "scholarly_literature"
    EVIDENCE_SYNTHESIS = "evidence_synthesis"
    CLINICAL_GUIDELINES = "clinical_guidelines"
    CLINICAL_TRIALS = "clinical_trials"
    REGULATORY = "regulatory"
    PHARMACOLOGY = "pharmacology"
    CHEMISTRY_MOLECULAR = "chemistry_molecular"
    GENOMICS_OMICS = "genomics_omics"
    PUBLIC_HEALTH = "public_health"
    NUTRITION = "nutrition"
    BOTANICAL_HERBAL = "botanical_herbal"
    TRADITIONAL_MEDICINE = "traditional_medicine"
    CLASSICAL_CANON = "classical_canon"


class AuthorityLevel(str, Enum):
    S0_UNKNOWN = "S0"         # Unknown / unverified candidate
    S1_COMMUNITY = "S1"       # Community / unreviewed literature
    S2_SCHOLARLY_SEC = "S2"   # Scholarly secondary / gray literature
    S3_PEER_REVIEWED = "S3"   # Peer-reviewed scholarly journal
    S4_PROFESSIONAL = "S4"    # Recognized professional society / institution
    S5_REGULATORY = "S5"      # National government / regulatory authority
    S6_INTERNATIONAL = "S6"   # International authoritative agency (WHO, etc.)


class LicenseStatus(str, Enum):
    PUBLIC_DOMAIN = "PUBLIC_DOMAIN"
    OPEN_LICENSE = "OPEN_LICENSE"
    OA_DISPLAY_ONLY = "OA_DISPLAY_ONLY"
    METADATA_ONLY = "METADATA_ONLY"
    ABSTRACT_ONLY = "ABSTRACT_ONLY"
    LICENSED_FULL_TEXT = "LICENSED_FULL_TEXT"
    USER_LICENSED = "USER_LICENSED"
    INSTITUTION_LICENSED = "INSTITUTION_LICENSED"
    RESTRICTED = "RESTRICTED"
    UNKNOWN = "UNKNOWN"
    PROHIBITED = "PROHIBITED"


class MedicalSystem(str, Enum):
    MODERN = "modern"
    UNANI = "unani"
    AYURVEDA = "ayurveda"
    SIDDHA = "siddha"
    SOWA_RIGPA = "sowa_rigpa"
    TCM = "tcm"
    KAMPO = "kampo"
    KOREAN = "korean"
    TIBETAN = "tibetan"
    PERSIAN = "persian"
    GRECO_ARAB = "greco_arab"
    AFRICAN = "african"
    LATIN_AMERICAN = "latin_american"
    INDIGENOUS = "indigenous"
    ETHNOMEDICINE = "ethnomedicine"
    INTEGRATIVE = "integrative"


class KnowledgeClass(str, Enum):
    CLASSICAL_TEXT = "CLASSICAL_TEXT"
    TRADITIONAL_CLAIM = "TRADITIONAL_CLAIM"
    HISTORICAL_REFERENCE = "HISTORICAL_REFERENCE"
    EXPERT_INTERPRETATION = "EXPERT_INTERPRETATION"
    MODERN_PRECLINICAL = "MODERN_PRECLINICAL"
    MODERN_CLINICAL = "MODERN_CLINICAL"


class InclusionStatus(str, Enum):
    DISCOVERED = "DISCOVERED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    APPROVED_METADATA_ONLY = "APPROVED_METADATA_ONLY"
    APPROVED_ABSTRACT_ONLY = "APPROVED_ABSTRACT_ONLY"
    APPROVED_FULLTEXT = "APPROVED_FULLTEXT"
    RESTRICTED = "RESTRICTED"
    SUSPENDED = "SUSPENDED"
    REJECTED = "REJECTED"
    RETIRED = "RETIRED"


class SourceRecord(BaseModel):
    source_id: str
    source_name: str
    canonical_url: str
    source_type: str
    source_class: SourceClass
    publisher: Optional[str] = None
    organization: Optional[str] = None
    country: str = "Global"
    region: Optional[str] = None
    jurisdiction: str = "International"
    languages: List[str] = Field(default_factory=lambda: ["en"])
    medical_systems: List[MedicalSystem] = Field(default_factory=lambda: [MedicalSystem.MODERN])
    specialties: List[str] = Field(default_factory=list)
    authority_level: AuthorityLevel = AuthorityLevel.S3_PEER_REVIEWED
    editorial_model: Optional[str] = "Peer-Reviewed"
    peer_review_model: Optional[str] = "Double-Blind"
    api_available: bool = True
    api_url: Optional[str] = None
    full_text_available: bool = False
    metadata_available: bool = True
    abstract_available: bool = True
    open_access: bool = True
    license_status: LicenseStatus = LicenseStatus.METADATA_ONLY
    update_frequency: str = "daily"
    retraction_monitored: bool = True
    status: str = "ACTIVE"
    health_score: float = 1.0
    coverage_score: float = 0.85
    inclusion_status: InclusionStatus = InclusionStatus.APPROVED
    exclusion_reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class StudyCanonical(BaseModel):
    """
    Canonical Study Identity linking trial registries, published papers, protocols, and outcomes.
    """
    canonical_study_id: str = Field(default_factory=lambda: f"study-{uuid.uuid4().hex[:8]}")
    title: str
    primary_trial_id: Optional[str] = None  # NCT01234567, CTRI/2021/..., ChiCTR...
    associated_trial_ids: List[str] = Field(default_factory=list)
    primary_doi: Optional[str] = None
    associated_dois: List[str] = Field(default_factory=list)
    pmids: List[str] = Field(default_factory=list)
    sponsor: Optional[str] = None
    interventions: List[str] = Field(default_factory=list)
    comparators: List[str] = Field(default_factory=list)
    sample_size: Optional[int] = None
    study_phase: Optional[str] = None
    recruitment_status: str = "COMPLETED"
    registration_date: Optional[str] = None
    has_results: bool = True
    is_retracted: bool = False
    retraction_reason: Optional[str] = None


class DiscoveryCandidate(BaseModel):
    candidate_id: str = Field(default_factory=lambda: f"cand-{uuid.uuid4().hex[:8]}")
    candidate_url: str
    candidate_name: str
    discovered_from: str  # citation, publisher_network, failed_search, research_gap
    discovery_method: str
    domain: str
    country: str = "Global"
    language: str = "en"
    suspected_publisher: Optional[str] = None
    medical_system: MedicalSystem = MedicalSystem.MODERN
    source_class: SourceClass = SourceClass.SCHOLARLY_LITERATURE
    confidence: float = 0.8
    detected_api: Optional[str] = None
    detected_license: Optional[str] = None
    review_state: str = "PENDING_REVIEW"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SourceCoverageReport(BaseModel):
    sources_discovered: int
    sources_active: int
    sources_pending_review: int
    sources_licensed: int
    modern_medicine_count: int
    unani_count: int
    ayurveda_count: int
    other_traditional_count: int
    trial_registries_count: int
    guidelines_count: int
    safety_sources_count: int
    countries_covered: List[str]
    languages_covered: List[str]
    source_classes: Dict[str, int]
    known_coverage_gaps: List[str]


class ResearchSourceMatrixRow(BaseModel):
    source_class: str
    searched: int
    retrieved: int
    included: int
    excluded: int
    unavailable: int


class ResearchSourceMatrix(BaseModel):
    query: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_universe_version: str = "SUM-2026.10"
    knowledge_release_version: str = "KREL-2026.10.04"
    matrix: List[ResearchSourceMatrixRow] = Field(default_factory=list)
    unsearched_categories: List[str] = Field(default_factory=list)
    inaccessible_sources: List[str] = Field(default_factory=list)
    epistemic_context_notes: List[str] = Field(default_factory=list)


class RetractionEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"ret-{uuid.uuid4().hex[:8]}")
    identifier: str  # DOI, PMID, trial_id
    document_title: str
    source_id: str
    retraction_date: datetime = Field(default_factory=datetime.utcnow)
    retraction_reason: str
    issuing_body: str
    affected_claims_count: int = 0
    affected_graph_edges_count: int = 0
    affected_projects_count: int = 0
    status: str = "PROPAGATED"
