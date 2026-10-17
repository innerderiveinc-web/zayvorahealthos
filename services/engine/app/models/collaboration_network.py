"""
ZMIE Global Scientific Collaboration & Research Network Engine Models
Prompt 22 Implementation.

Defines first-class scientific collaboration entities, temporal affiliations,
multi-dimensional expertise evidence, disambiguated researcher & institutional identities,
collaboration edges with recency decay, cross-disciplinary bridges, research clusters,
objective gap mapping, network snapshots, and privacy/tenancy firewalls.
"""

from enum import Enum
from typing import List, Dict, Any, Optional, Set
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class RelationshipState(str, Enum):
    OBSERVED = "OBSERVED"
    SOURCE_REPORTED = "SOURCE_REPORTED"
    STRUCTURED = "STRUCTURED"
    DERIVED = "DERIVED"
    INFERRED = "INFERRED"
    PREDICTED = "PREDICTED"
    USER_ASSERTED = "USER_ASSERTED"
    UNKNOWN = "UNKNOWN"
    PRIVATE_UNOBSERVABLE = "PRIVATE_UNOBSERVABLE"


class IdentityConfidenceState(str, Enum):
    UNRESOLVED = "UNRESOLVED"
    CANDIDATE = "CANDIDATE"
    PROBABLE = "PROBABLE"
    SUPPORTED = "SUPPORTED"
    CONFIRMED = "CONFIRMED"
    CONTESTED = "CONTESTED"
    REJECTED = "REJECTED"


class CollaborationType(str, Enum):
    COAUTHORED = "COAUTHORED"
    COINVESTIGATED = "COINVESTIGATED"
    COFUNDED = "COFUNDED"
    CODEVELOPED = "CODEVELOPED"
    SHARED_DATASET = "SHARED_DATASET"
    SHARED_PROJECT = "SHARED_PROJECT"
    SHARED_TRIAL = "SHARED_TRIAL"
    SHARED_METHOD = "SHARED_METHOD"
    CONSORTIUM_MEMBER = "CONSORTIUM_MEMBER"
    INSTITUTIONAL_PARTNER = "INSTITUTIONAL_PARTNER"


class ExpertiseDimension(str, Enum):
    DOMAIN = "DOMAIN"
    TOPIC = "TOPIC"
    METHOD = "METHOD"
    TECHNOLOGY = "TECHNOLOGY"
    DISEASE = "DISEASE"
    POPULATION = "POPULATION"
    GEOGRAPHY = "GEOGRAPHY"


class AffiliationStatus(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    VISITING = "VISITING"
    EMERITUS = "EMERITUS"
    HISTORICAL = "HISTORICAL"
    UNKNOWN = "UNKNOWN"


class GapStatus(str, Enum):
    WELL_REPRESENTED = "WELL_REPRESENTED"
    SPARSE_IN_INDEXED_SOURCES = "SPARSE_IN_INDEXED_SOURCES"
    EMERGING = "EMERGING"
    CONTESTED = "CONTESTED"


class VisibilityScope(str, Enum):
    PUBLIC = "PUBLIC"
    TENANT_PRIVATE = "TENANT_PRIVATE"
    RESTRICTED_CONSORTIUM = "RESTRICTED_CONSORTIUM"


# --- Temporal Affiliation ---

class TemporalAffiliation(BaseModel):
    affiliation_id: str = Field(default_factory=lambda: f"aff-{uuid.uuid4().hex[:8]}")
    institution_id: str
    institution_name: str
    department_id: Optional[str] = None
    department_name: Optional[str] = None
    role: str = "Researcher"
    affiliation_status: AffiliationStatus = AffiliationStatus.PRIMARY
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    is_current: bool = True
    provenance_source: str = "SOURCE_REPORTED"
    confidence: float = 1.0


# --- Multi-Dimensional Expertise Evidence ---

class ExpertiseEvidenceItem(BaseModel):
    dimension: ExpertiseDimension
    topic_or_method: str
    evidence_type: str = "PUBLICATION"  # PUBLICATION, CLINICAL_TRIAL, GRANT, DATASET, METHOD
    source_identifiers: List[str] = Field(default_factory=list)  # DOIs, NCT IDs, Grant numbers
    years_active: List[int] = Field(default_factory=list)
    confidence_state: IdentityConfidenceState = IdentityConfidenceState.SUPPORTED
    evidence_count: int = 1
    sample_context: Optional[str] = None


# --- Disambiguated Researcher Identity ---

class ResearcherIdentity(BaseModel):
    researcher_id: str
    canonical_name: str
    aliases: List[str] = Field(default_factory=list)
    orcid: Optional[str] = None
    email_domain_hints: List[str] = Field(default_factory=list)
    disambiguation_confidence: IdentityConfidenceState = IdentityConfidenceState.SUPPORTED
    is_contested: bool = False
    contestation_reason: Optional[str] = None
    affiliations: List[TemporalAffiliation] = Field(default_factory=list)
    expertise_profile: List[ExpertiseEvidenceItem] = Field(default_factory=list)
    primary_disciplines: List[str] = Field(default_factory=list)
    visibility: VisibilityScope = VisibilityScope.PUBLIC
    tenant_id: Optional[str] = None
    provenance_records: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# --- Disambiguated Institution Identity ---

class InstitutionIdentity(BaseModel):
    institution_id: str
    canonical_name: str
    aliases: List[str] = Field(default_factory=list)
    ror_id: Optional[str] = None
    grid_id: Optional[str] = None
    country: str = "Global"
    city: Optional[str] = None
    institution_type: str = "UNIVERSITY"  # UNIVERSITY, HOSPITAL, TRADITIONAL_COUNCIL, RESEARCH_INSTITUTE
    parent_institution_id: Optional[str] = None
    departments: List[str] = Field(default_factory=list)
    labs: List[str] = Field(default_factory=list)
    visibility: VisibilityScope = VisibilityScope.PUBLIC
    tenant_id: Optional[str] = None


# --- Collaboration Edge with Recency & Evidence ---

class CollaborationEdge(BaseModel):
    edge_id: str = Field(default_factory=lambda: f"collab-{uuid.uuid4().hex[:8]}")
    source_researcher_id: str
    target_researcher_id: str
    relationship_type: CollaborationType = CollaborationType.COAUTHORED
    relationship_state: RelationshipState = RelationshipState.OBSERVED
    evidence_artifacts: List[str] = Field(default_factory=list)  # DOIs, Clinical Trial IDs, Grants
    shared_work_count: int = 1
    first_year: int
    last_year: int
    is_active_recent: bool = True  # e.g., active within last 3 years
    recency_weight: float = 1.0  # Time-decay score (1.0 = recent, 0.2 = historical)
    cross_institutional: bool = False
    source_institution_id: Optional[str] = None
    target_institution_id: Optional[str] = None
    visibility: VisibilityScope = VisibilityScope.PUBLIC
    tenant_id: Optional[str] = None


# --- Cross-Disciplinary Bridge ---

class CrossDisciplinaryBridge(BaseModel):
    bridge_id: str = Field(default_factory=lambda: f"bridge-{uuid.uuid4().hex[:8]}")
    researcher_id: str
    researcher_name: str
    bridged_disciplines: List[str] = Field(default_factory=list)  # e.g., ["Unani Medicine", "Phytochemistry", "Metabolic Pharmacology"]
    bridging_evidence_count: int = 1
    shared_topics: List[str] = Field(default_factory=list)
    evidence_references: List[str] = Field(default_factory=list)
    description: str = "Discovered cross-disciplinary research synthesis."


# --- Research Cluster / Community ---

class ResearchCluster(BaseModel):
    cluster_id: str = Field(default_factory=lambda: f"cluster-{uuid.uuid4().hex[:8]}")
    label: str
    disciplines: List[str] = Field(default_factory=list)
    core_topics: List[str] = Field(default_factory=list)
    dominant_methods: List[str] = Field(default_factory=list)
    member_researcher_ids: List[str] = Field(default_factory=list)
    member_institution_ids: List[str] = Field(default_factory=list)
    total_collaborations: int = 0
    cohesion_score: float = 1.0
    discovered_at: datetime = Field(default_factory=datetime.utcnow)


# --- Objective Research Gap Report ---

class ResearchGapReport(BaseModel):
    gap_id: str = Field(default_factory=lambda: f"gap-{uuid.uuid4().hex[:8]}")
    domain_or_topic: str
    status: GapStatus = GapStatus.SPARSE_IN_INDEXED_SOURCES
    observed_publication_count: int = 0
    indexed_researcher_count: int = 0
    epistemic_disclaimer: str = (
        "Non-negotiable epistemic boundary: 'Sparse in indexed sources' indicates "
        "an absence in indexed public registries and literature databases. It does NOT "
        "assert that research is nonexistent or unperformed in private or regional archives."
    )
    recommended_inquiry_path: List[str] = Field(default_factory=list)


# --- Network Snapshot & Graph Diff ---

class NetworkSnapshot(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: f"snap-{uuid.uuid4().hex[:8]}")
    label: str
    captured_at: datetime = Field(default_factory=datetime.utcnow)
    total_researchers: int = 0
    total_institutions: int = 0
    total_collaboration_edges: int = 0
    total_clusters: int = 0
    researcher_ids: List[str] = Field(default_factory=list)
    edge_ids: List[str] = Field(default_factory=list)
    cluster_ids: List[str] = Field(default_factory=list)


class NetworkDiff(BaseModel):
    diff_id: str = Field(default_factory=lambda: f"diff-{uuid.uuid4().hex[:8]}")
    from_snapshot_id: str
    to_snapshot_id: str
    new_researchers: List[str] = Field(default_factory=list)
    new_edges: List[str] = Field(default_factory=list)
    new_clusters: List[str] = Field(default_factory=list)
    strengthened_collaborations: List[Dict[str, Any]] = Field(default_factory=list)
    emerging_interdisciplinary_bridges: List[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)


# --- Request & Query Models ---

class ResearcherResolveRequest(BaseModel):
    raw_name: str
    orcid: Optional[str] = None
    institution_hint: Optional[str] = None
    department_hint: Optional[str] = None
    coauthor_hints: List[str] = Field(default_factory=list)
    topic_hints: List[str] = Field(default_factory=list)
    tenant_id: Optional[str] = None


class ExpertiseSearchQuery(BaseModel):
    topic: Optional[str] = None
    method: Optional[str] = None
    disease: Optional[str] = None
    min_evidence_count: int = 1
    must_include_cross_disciplinary: bool = False
    tenant_id: Optional[str] = None
