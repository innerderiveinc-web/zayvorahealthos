"""
ZMIE Global Research Discovery Network & Continuous Knowledge Evolution Models
Prompt 14 Implementation.

Defines first-class research entities, relations, discovery lifecycles,
signals, gaps, evolution cascade impacts, and knowledge snapshots.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class ProjectStatus(str, Enum):
    KNOWN = "KNOWN"
    DISCOVERED = "DISCOVERED"
    REGISTERED = "REGISTERED"
    ONGOING = "ONGOING"
    PRELIMINARY = "PRELIMINARY"
    PUBLISHED = "PUBLISHED"
    VALIDATED = "VALIDATED"
    RETRACTED = "RETRACTED"
    SUPERSEDED = "SUPERSEDED"
    UNKNOWN = "UNKNOWN"


class InstitutionType(str, Enum):
    UNIVERSITY = "UNIVERSITY"
    HOSPITAL = "HOSPITAL"
    RESEARCH_CENTER = "RESEARCH_CENTER"
    LABORATORY = "LABORATORY"
    ACADEMY = "ACADEMY"
    TRADITIONAL_COUNCIL = "TRADITIONAL_COUNCIL"  # e.g., CCRUM, CCRAS, AYUSH
    PHARMA_BIOTECH = "PHARMA_BIOTECH"
    GOVERNMENT_AGENCY = "GOVERNMENT_AGENCY"


class LifecycleRelation(str, Enum):
    AUTHORED_BY = "AUTHORED_BY"
    AFFILIATED_WITH = "AFFILIATED_WITH"
    FUNDED_BY = "FUNDED_BY"
    CONDUCTS = "CONDUCTS"
    USES_PROTOCOL = "USES_PROTOCOL"
    GENERATES_DATASET = "GENERATES_DATASET"
    GENERATES_PREPRINT = "GENERATES_PREPRINT"
    PUBLISHED_AS = "PUBLISHED_AS"
    SUPERSEDED_BY = "SUPERSEDED_BY"
    REPLICATED_BY = "REPLICATED_BY"
    RETRACTED_BY = "RETRACTED_BY"
    DERIVED_PATENT = "DERIVED_PATENT"


class Researcher(BaseModel):
    researcher_id: str
    canonical_name: str
    aliases: List[str] = Field(default_factory=list)
    orcid: Optional[str] = None
    affiliations: List[Dict[str, Any]] = Field(default_factory=list)  # {institution_id, name, department, role, current}
    subject_areas: List[str] = Field(default_factory=list)
    traditional_systems: List[str] = Field(default_factory=list)  # modern, unani, ayurveda, siddha, tcm
    co_author_ids: List[str] = Field(default_factory=list)
    disambiguation_confidence: float = 1.0
    h_index: Optional[int] = None
    citation_count: Optional[int] = None
    publication_count: int = 0
    active_projects_count: int = 0
    is_verified: bool = True


class ResearchInstitution(BaseModel):
    institution_id: str
    name: str
    ror_id: Optional[str] = None
    institution_type: InstitutionType = InstitutionType.UNIVERSITY
    country: str
    city: Optional[str] = None
    departments: List[str] = Field(default_factory=list)
    parent_institution_id: Optional[str] = None
    traditional_systems: List[str] = Field(default_factory=list)
    active_trials_count: int = 0
    total_grant_funding_usd: float = 0.0


class GrantRecord(BaseModel):
    grant_id: str
    grant_number: str
    funding_agency: str  # NIH, Wellcome Trust, AYUSH/CCRUM, ERC, ICMR
    title: str
    abstract: Optional[str] = None
    amount_usd: Optional[float] = None
    currency: str = "USD"
    pi_ids: List[str] = Field(default_factory=list)
    institution_id: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: str = "ACTIVE"  # ACTIVE, COMPLETED, TERMINATED


class ClinicalTrialRecord(BaseModel):
    trial_id: str  # NCT04286588, CTRI/2021/09/036123
    registry: str  # ClinicalTrials.gov, CTRI, EU-CTR, WHO-ICTRP
    title: str
    phase: str = "Phase 2"
    recruitment_status: str = "RECRUITING"
    interventions: List[str] = Field(default_factory=list)
    conditions: List[str] = Field(default_factory=list)
    sponsor_id: Optional[str] = None
    investigator_ids: List[str] = Field(default_factory=list)
    canonical_study_id: Optional[str] = None
    results_published: bool = False
    publication_dois: List[str] = Field(default_factory=list)


class PreprintRecord(BaseModel):
    preprint_id: str
    doi: str
    server: str  # medRxiv, bioRxiv, Research Square
    title: str
    authors: List[str] = Field(default_factory=list)
    author_ids: List[str] = Field(default_factory=list)
    deposited_date: str
    version: int = 1
    canonical_study_id: Optional[str] = None
    peer_reviewed_doi: Optional[str] = None
    is_superseded_by_peer_review: bool = False
    evidence_gating_warning: str = "PREPRINT: Non-peer-reviewed preliminary research. Not established clinical proof."


class ThesisRecord(BaseModel):
    thesis_id: str
    title: str
    author_id: str
    advisor_ids: List[str] = Field(default_factory=list)
    degree: str  # PhD, MD, Mahir-e-Tibb, MS
    institution_id: str
    defense_year: int
    canonical_study_id: Optional[str] = None
    accession_number: Optional[str] = None
    evidence_gating_warning: str = "THESIS/DISSERTATION: Academic qualification work. Subject to subsequent peer-reviewed validation."


class DatasetRecord(BaseModel):
    dataset_id: str
    doi: Optional[str] = None
    title: str
    repository: str  # Zenodo, Dryad, GEO, PhysioNet
    creator_ids: List[str] = Field(default_factory=list)
    related_study_id: Optional[str] = None
    access_tier: str = "OPEN"  # OPEN, RESTRICTED, CONTROLLED
    sample_size: Optional[int] = None


class PatentRecord(BaseModel):
    patent_id: str
    patent_number: str
    office: str  # USPTO, EPO, WIPO, Indian Patent Office
    title: str
    inventor_ids: List[str] = Field(default_factory=list)
    assignee_institution_id: Optional[str] = None
    filing_date: str
    status: str = "GRANTED"  # FILED, PUBLISHED, GRANTED, EXPIRED
    evidence_gating_warning: str = "PATENT: Intellectual property disclosure. Does not constitute clinical efficacy or safety proof."


class ResearchProject(BaseModel):
    project_id: str
    title: str
    description: Optional[str] = None
    lead_researcher_ids: List[str] = Field(default_factory=list)
    collaborator_ids: List[str] = Field(default_factory=list)
    institution_ids: List[str] = Field(default_factory=list)
    grant_ids: List[str] = Field(default_factory=list)
    status: ProjectStatus = ProjectStatus.ONGOING
    is_private_unobservable: bool = False
    clinical_trial_ids: List[str] = Field(default_factory=list)
    canonical_study_id: Optional[str] = None
    outputs: List[Dict[str, Any]] = Field(default_factory=list)  # preprints, articles, datasets


class LifecycleEdge(BaseModel):
    source_id: str
    target_id: str
    relation_type: LifecycleRelation
    timestamp: Optional[str] = None
    provenance: str = "ZMIE_RESEARCH_GRAPH"


class ResearchSignal(BaseModel):
    signal_id: str
    topic: str
    growth_rate_3yr: float
    preprints_to_papers_ratio: float
    clinical_trial_acceleration: float
    grant_inflow_usd: float
    frontier_velocity_score: float  # 0 to 100
    status: str = "EMERGING_FRONTIER"  # EMERGING_FRONTIER, ACCELERATING, MATURING, STAGNANT
    key_breakthrough_compounds: List[str] = Field(default_factory=list)
    key_institutions: List[str] = Field(default_factory=list)


class ResearchGapAnalysis(BaseModel):
    gap_id: str
    topic: str
    gap_type: str  # METHODOLOGICAL, POPULATION_EXCLUSION, CONTRADICTION_UNRESOLVED, REPLICATION_DEFICIT, GEOGRAPHIC_BIAS, TRADITIONAL_SYSTEM_UNDERINVESTIGATED
    deficiency_description: str
    missing_evidence_type: str
    affected_claims: List[str] = Field(default_factory=list)
    priority_score: float  # 0 to 100
    suggested_investigation: str


class EvolutionImpactAnalysis(BaseModel):
    impact_id: str = Field(default_factory=lambda: f"imp-{uuid.uuid4().hex[:8]}")
    trigger_type: str  # RETRACTION, NEW_STUDY, GUIDELINE_CHANGE, TRIAL_TERMINATION, SAFETY_SIGNAL
    trigger_source_id: str
    affected_claim_ids: List[str] = Field(default_factory=list)
    previous_claim_states: Dict[str, str] = Field(default_factory=dict)
    new_claim_states: Dict[str, str] = Field(default_factory=dict)
    evidence_graph_changes: List[Dict[str, Any]] = Field(default_factory=list)
    severity_level: str = "HIGH"  # CRITICAL, HIGH, MEDIUM, LOW
    alerts_dispatched: List[Dict[str, Any]] = Field(default_factory=list)
    revalidation_timestamp: datetime = Field(default_factory=datetime.utcnow)
    summary: str = ""


class KnowledgeSnapshot(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: f"snap-evo-{uuid.uuid4().hex[:8]}")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: int
    claims_count: int
    supported_claims: int
    disputed_claims: int
    retracted_claims: int
    active_gaps_count: int
    frontier_signals_count: int
    notes: str = ""
