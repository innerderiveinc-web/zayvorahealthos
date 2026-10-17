"""
ZMIE Federated & Private Research Intelligence Engine Models
Prompt 23 Implementation.

Schemas for:
- Data / knowledge classification tiers and knowledge boundaries
- Tenancy hierarchy (Platform -> Tenant -> Project) and request contexts
- Policy engine inputs / outputs (RBAC + ABAC + purpose + project + data scope)
- Private datasets, documents, terminology mappings, claims, graph nodes
- Access requests, data sharing agreements, classification change records
- Governed release candidates (privacy / IP / scientific review, separation of duties)
- Federated sites, queries, site-level results, coverage, certificates
- AI context firewall, model registry policies, agent contexts
- Private reports, connectors, incidents and containment

NOTE ON HONESTY: field presence (e.g. `ethics_review_state`) never implies that an
approval exists. Defaults are always the most conservative state.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import uuid


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

class ResearchDataClassification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"
    SENSITIVE = "SENSITIVE"
    PERSONAL = "PERSONAL"
    HEALTH_DATA = "HEALTH_DATA"
    PHI = "PHI"
    PII = "PII"
    RESEARCH_CONFIDENTIAL = "RESEARCH_CONFIDENTIAL"
    TRADE_SECRET = "TRADE_SECRET"
    IP_SENSITIVE = "IP_SENSITIVE"
    REGULATED = "REGULATED"
    HIGHLY_RESTRICTED = "HIGHLY_RESTRICTED"


# Higher rank = stricter handling. Used for "strictest classification wins" inheritance.
CLASSIFICATION_RANK: Dict[str, int] = {
    "PUBLIC": 0,
    "INTERNAL": 1,
    "CONFIDENTIAL": 2,
    "SENSITIVE": 3,
    "PERSONAL": 3,
    "RESEARCH_CONFIDENTIAL": 3,
    "RESTRICTED": 4,
    "HEALTH_DATA": 4,
    "PII": 4,
    "IP_SENSITIVE": 4,
    "REGULATED": 4,
    "PHI": 5,
    "TRADE_SECRET": 5,
    "HIGHLY_RESTRICTED": 6,
}


def strictest(classifications: List[ResearchDataClassification]) -> ResearchDataClassification:
    if not classifications:
        return ResearchDataClassification.INTERNAL
    return max(classifications, key=lambda c: CLASSIFICATION_RANK[c.value])


def is_external_sensitive(c: ResearchDataClassification) -> bool:
    """Anything stricter than INTERNAL must not reach external AI providers by default."""
    return CLASSIFICATION_RANK[c.value] >= CLASSIFICATION_RANK["CONFIDENTIAL"]


class KnowledgeClassification(str, Enum):
    PUBLIC_KNOWLEDGE = "PUBLIC_KNOWLEDGE"
    TENANT_KNOWLEDGE = "TENANT_KNOWLEDGE"
    PROJECT_KNOWLEDGE = "PROJECT_KNOWLEDGE"
    PRIVATE_KNOWLEDGE = "PRIVATE_KNOWLEDGE"
    FEDERATED_DERIVED_KNOWLEDGE = "FEDERATED_DERIVED_KNOWLEDGE"
    PUBLIC_RELEASE_CANDIDATE = "PUBLIC_RELEASE_CANDIDATE"
    PUBLIC_RELEASED = "PUBLIC_RELEASED"


class KnowledgeBoundary(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    FEDERATED = "FEDERATED"
    DERIVED_PRIVATE = "DERIVED_PRIVATE"
    PUBLICLY_RELEASED = "PUBLICLY_RELEASED"
    INFERRED = "INFERRED"
    SYNTHETIC = "SYNTHETIC"


# ---------------------------------------------------------------------------
# Roles, policy decisions, states
# ---------------------------------------------------------------------------

class EnterpriseRole(str, Enum):
    PLATFORM_ADMINISTRATOR = "PLATFORM_ADMINISTRATOR"
    TENANT_ADMINISTRATOR = "TENANT_ADMINISTRATOR"
    SECURITY_ADMINISTRATOR = "SECURITY_ADMINISTRATOR"
    PRIVACY_ADMINISTRATOR = "PRIVACY_ADMINISTRATOR"
    RESEARCH_ADMINISTRATOR = "RESEARCH_ADMINISTRATOR"
    RESEARCHER = "RESEARCHER"
    CLINICIAN_RESEARCHER = "CLINICIAN_RESEARCHER"
    DATA_SCIENTIST = "DATA_SCIENTIST"
    STATISTICIAN = "STATISTICIAN"
    PRINCIPAL_INVESTIGATOR = "PRINCIPAL_INVESTIGATOR"
    PROJECT_MANAGER = "PROJECT_MANAGER"
    DATA_STEWARD = "DATA_STEWARD"
    COMPLIANCE_REVIEWER = "COMPLIANCE_REVIEWER"
    EXTERNAL_COLLABORATOR = "EXTERNAL_COLLABORATOR"
    AUDITOR = "AUDITOR"
    READ_ONLY_RESEARCHER = "READ_ONLY_RESEARCHER"


WRITE_CAPABLE_ROLES = {
    "PRINCIPAL_INVESTIGATOR", "RESEARCHER", "CLINICIAN_RESEARCHER", "DATA_SCIENTIST",
    "STATISTICIAN", "DATA_STEWARD", "PROJECT_MANAGER",
}


class PolicyDecision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    REDACT = "REDACT"
    AGGREGATE_ONLY = "AGGREGATE_ONLY"
    LOCAL_ONLY = "LOCAL_ONLY"


class AccessState(str, Enum):
    REQUESTED = "REQUESTED"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    SUSPENDED = "SUSPENDED"


class FederatedExecutionStatus(str, Enum):
    COMPLETED = "COMPLETED"
    PARTIAL_FEDERATED_RESULT = "PARTIAL_FEDERATED_RESULT"
    FAILED = "FAILED"
    BLOCKED_BY_POLICY = "BLOCKED_BY_POLICY"


class ModelTier(str, Enum):
    PUBLIC_HOSTED = "PUBLIC_HOSTED"
    APPROVED_ENTERPRISE = "APPROVED_ENTERPRISE"
    PRIVATE_MODEL = "PRIVATE_MODEL"
    ON_PREMISE = "ON_PREMISE"
    SELF_HOSTED = "SELF_HOSTED"
    AIR_GAPPED = "AIR_GAPPED"
    FEDERATED = "FEDERATED"


EXTERNAL_MODEL_TIERS = {ModelTier.PUBLIC_HOSTED, ModelTier.APPROVED_ENTERPRISE}


class AgentMode(str, Enum):
    PUBLIC_MODE = "PUBLIC_MODE"
    TENANT_MODE = "TENANT_MODE"
    PROJECT_MODE = "PROJECT_MODE"
    FEDERATED_MODE = "FEDERATED_MODE"


class DeploymentMode(str, Enum):
    SAAS = "SAAS"
    SINGLE_TENANT_CLOUD = "SINGLE_TENANT_CLOUD"
    DEDICATED_VPC = "DEDICATED_VPC"
    PRIVATE_CLOUD = "PRIVATE_CLOUD"
    ON_PREMISE = "ON_PREMISE"
    AIR_GAPPED = "AIR_GAPPED"
    HYBRID = "HYBRID"
    FEDERATED = "FEDERATED"


# ---------------------------------------------------------------------------
# Tenancy
# ---------------------------------------------------------------------------

class TenantEntity(BaseModel):
    tenant_id: str = Field(default_factory=lambda: _id("tenant"))
    name: str
    organization_type: str = "RESEARCH_INSTITUTE"
    deployment_mode: DeploymentMode = DeploymentMode.SAAS
    data_residency_region: str = "UNSPECIFIED"
    allow_cross_border_transfer: bool = False
    allow_external_models: bool = False  # default: no restricted data to external AI
    user_roles: Dict[str, str] = Field(default_factory=dict)  # tenant-level role per user
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProjectEntity(BaseModel):
    project_id: str = Field(default_factory=lambda: _id("proj"))
    tenant_id: str
    name: str
    description: str = ""
    members: Dict[str, str] = Field(default_factory=dict)  # user_id -> EnterpriseRole value
    shared_with_tenants: List[str] = Field(default_factory=list)  # governed shared projects
    ethics_review_state: str = "NOT_RECORDED"  # never implies approval
    consent_state: str = "NOT_RECORDED"  # consent is NOT technical authorization; never defaults to granted
    is_isolated: bool = False  # set by incident containment
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RequestContext(BaseModel):
    """Server-side resolved identity. In production this is derived from a verified token,
    never from client-asserted headers alone."""
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    project_id: Optional[str] = None
    purpose: Optional[str] = None
    is_agent: bool = False
    agent_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Policy engine
# ---------------------------------------------------------------------------

class PolicyRequest(BaseModel):
    context: RequestContext
    resource_id: str
    resource_type: str = "DATASET"
    resource_tenant_id: str
    resource_project_id: Optional[str] = None
    classification: ResearchDataClassification = ResearchDataClassification.CONFIDENTIAL
    operation: str = "READ"  # READ, WRITE, EXPORT, EXTERNAL_MODEL_CALL, FEDERATED_COMPUTE, TRAIN_MODEL
    destination: Optional[str] = None  # e.g. PUBLIC, PARTNER, INTERNAL, region code
    allowed_purposes: List[str] = Field(default_factory=list)
    requires_object_grant: bool = False


class PolicyEvaluation(BaseModel):
    decision: PolicyDecision
    matched_rule: str
    user_facing_reason: str  # non-sensitive, actionable
    internal_explanation: str  # for policy simulator / admins
    policy_version: str
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Private assets
# ---------------------------------------------------------------------------

class PrivateDataset(BaseModel):
    dataset_id: str = Field(default_factory=lambda: _id("pds"))
    tenant_id: str
    project_id: str
    name: str
    classification: ResearchDataClassification = ResearchDataClassification.CONFIDENTIAL
    owner_user_id: str
    steward_user_id: Optional[str] = None
    allowed_purposes: List[str] = Field(default_factory=lambda: ["APPROVED_RESEARCH"])
    requires_object_grant: bool = False  # project membership alone insufficient
    row_count: int = 0
    feature_columns: List[str] = Field(default_factory=list)
    is_blinded: bool = False
    retention_hold: bool = False
    deletion_status: str = "ACTIVE"
    license_or_agreement: str = "INTERNAL_USE_ONLY"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PrivateDocument(BaseModel):
    document_id: str = Field(default_factory=lambda: _id("pdoc"))
    tenant_id: str
    project_id: str
    title: str
    doc_type: str = "LAB_NOTEBOOK"
    classification: ResearchDataClassification = ResearchDataClassification.CONFIDENTIAL
    content: str
    owner_user_id: str = "unknown"
    internal_citation_tag: str = Field(default_factory=lambda: f"PRIVATE-DOC-{uuid.uuid4().hex[:6].upper()}")
    derived_from: List[str] = Field(default_factory=list)
    deletion_status: str = "ACTIVE"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PrivateTermMapping(BaseModel):
    mapping_id: str = Field(default_factory=lambda: _id("ptm"))
    scope_level: str = "PROJECT"  # TENANT or PROJECT
    tenant_id: str
    project_id: Optional[str] = None
    internal_term: str
    private_concept_id: str
    global_concept_candidate: Optional[str] = None
    released_globally: bool = False


class PrivateClaim(BaseModel):
    claim_id: str = Field(default_factory=lambda: _id("pclm"))
    tenant_id: str
    project_id: str
    statement: str
    claim_state: str = "UNCERTAIN"  # SUPPORTED, CONTRADICTED, UNCERTAIN, HYPOTHESIZED
    supporting_artifacts: List[str] = Field(default_factory=list)
    classification: ResearchDataClassification = ResearchDataClassification.CONFIDENTIAL
    knowledge_class: KnowledgeClassification = KnowledgeClassification.PROJECT_KNOWLEDGE
    contradicts_public_claim_ids: List[str] = Field(default_factory=list)
    is_publicly_released: bool = False


class PrivateGraphNode(BaseModel):
    node_id: str = Field(default_factory=lambda: _id("pgn"))
    label: str  # PrivateResearcher, PrivateExperiment, PrivateResult, PrivateConcept ...
    name: str
    tenant_id: str
    project_id: Optional[str] = None
    classification: ResearchDataClassification = ResearchDataClassification.CONFIDENTIAL
    visibility: str = "PROJECT"  # PROJECT, TENANT, SHARED
    properties: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Governance
# ---------------------------------------------------------------------------

class AccessRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: _id("accreq"))
    requester_user_id: str
    tenant_id: str
    project_id: str
    target_resource_id: str
    purpose: str
    requested_fields: List[str] = Field(default_factory=list)
    requested_operations: List[str] = Field(default_factory=lambda: ["READ"])
    requested_duration_days: int = 30
    status: AccessState = AccessState.PENDING
    approver_user_id: Optional[str] = None
    starts_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_break_glass: bool = False
    break_glass_reason: Optional[str] = None
    post_access_review_required: bool = False


class DataSharingAgreement(BaseModel):
    agreement_id: str = Field(default_factory=lambda: _id("dsa"))
    parties: List[str]  # tenant ids
    shared_project_id: Optional[str] = None
    dataset_ids: List[str] = Field(default_factory=list)
    purpose: str
    allowed_operations: List[str] = Field(default_factory=lambda: ["FEDERATED_COMPUTE"])
    allowed_outputs: List[str] = Field(default_factory=lambda: ["AGGREGATE_ONLY"])
    jurisdictions: List[str] = Field(default_factory=list)
    license: str = "RESEARCH_COLLABORATION_AGREEMENT"
    status: str = "ACTIVE"  # ACTIVE, TERMINATED
    starts_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(days=365))


class ClassificationChange(BaseModel):
    change_id: str = Field(default_factory=lambda: _id("clschg"))
    object_id: str
    previous: ResearchDataClassification
    new: ResearchDataClassification
    changed_by: str
    is_ai_proposal: bool = False
    reason: str
    policy_version: str
    status: str = "APPLIED"  # APPLIED, PROPOSED, REJECTED
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ReleaseCandidate(BaseModel):
    candidate_id: str = Field(default_factory=lambda: _id("relcand"))
    tenant_id: str
    project_id: str
    object_type: str = "PRIVATE_CLAIM"
    object_id: str
    requested_by: str
    original_classification: ResearchDataClassification
    license: Optional[str] = None
    reviews: Dict[str, Dict[str, Any]] = Field(default_factory=dict)  # review_type -> {reviewer, approved, at}
    automated_scan_findings: List[str] = Field(default_factory=list)
    status: str = "PENDING_REVIEW"  # PENDING_REVIEW, RELEASED, REJECTED, WITHDRAWN
    released_at: Optional[datetime] = None
    released_by: Optional[str] = None
    public_version: Optional[str] = None
    history: List[Dict[str, Any]] = Field(default_factory=list)


REQUIRED_RELEASE_REVIEWS = ["PRIVACY_REVIEW", "IP_REVIEW", "SCIENTIFIC_REVIEW", "LICENSE_REVIEW"]


# ---------------------------------------------------------------------------
# Federated research
# ---------------------------------------------------------------------------

class FederatedSite(BaseModel):
    site_id: str
    tenant_id: str
    organization_name: str
    status: str = "ONLINE"  # ONLINE, OFFLINE, DEGRADED
    supported_methods: List[str] = Field(default_factory=lambda: ["AGGREGATE_COHORT", "SITE_MEAN_ESTIMATE"])
    available_variables: List[str] = Field(default_factory=lambda: ["age", "has_condition", "outcome"])
    data_model: str = "OMOP"
    local_terminology_overrides: Dict[str, str] = Field(default_factory=dict)
    quality_report: Dict[str, Any] = Field(default_factory=dict)  # completeness etc. (no records)
    privacy_budget_total: float = 5.0
    privacy_budget_spent: float = 0.0
    local_only_compute: bool = True


class FederatedQueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: _id("fedq"))
    orchestrator_tenant_id: str
    requested_by: str
    participating_site_ids: List[str]
    query_type: str = "AGGREGATE_COHORT"  # AGGREGATE_COHORT, SITE_MEAN_ESTIMATE
    cohort_criteria: Dict[str, Any] = Field(default_factory=dict)  # e.g. {"min_age": 40, "has_condition": True}
    purpose: str = "APPROVED_RESEARCH"
    allowed_output: str = "AGGREGATE_ONLY"
    min_cell_size: int = 10
    enable_differential_privacy: bool = False
    epsilon: float = 1.0
    delta: float = 0.0


class SiteResult(BaseModel):
    site_id: str
    status: str  # COMPLETED, FAILED, UNAVAILABLE, EXCLUDED
    reason: Optional[str] = None
    local_run_id: Optional[str] = None
    reported_count: Optional[int] = None
    suppressed: bool = False
    estimate: Optional[float] = None
    standard_error: Optional[float] = None
    data_model: Optional[str] = None


class FederatedRunResult(BaseModel):
    run_id: str = Field(default_factory=lambda: _id("fedrun"))
    query_id: str
    execution_status: FederatedExecutionStatus
    result_label: str
    coverage: Dict[str, Any]
    site_results: List[SiteResult] = Field(default_factory=list)
    aggregate: Dict[str, Any] = Field(default_factory=dict)
    privacy_transformations: List[str] = Field(default_factory=list)
    heterogeneity: Dict[str, Any] = Field(default_factory=dict)
    limitations: List[str] = Field(default_factory=list)
    certificate: Dict[str, Any] = Field(default_factory=dict)
    classification: KnowledgeClassification = KnowledgeClassification.FEDERATED_DERIVED_KNOWLEDGE
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# AI / agents / models
# ---------------------------------------------------------------------------

class ModelRegistration(BaseModel):
    model_id: str
    tier: ModelTier
    provider: str
    region: str = "UNSPECIFIED"
    training_use_policy: str = "NO_TRAINING_ON_CUSTOMER_DATA"
    retention_policy: str = "ZERO_RETENTION"
    logging_policy: str = "NO_PROMPT_LOGGING"
    max_classification: ResearchDataClassification = ResearchDataClassification.INTERNAL
    owner_tenant_id: Optional[str] = None  # private models are tenant-bound


class AgentContext(BaseModel):
    agent_id: str = Field(default_factory=lambda: _id("agent"))
    mode: AgentMode
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None
    acting_for_user_id: Optional[str] = None
    session_id: str = Field(default_factory=lambda: _id("sess"))
    allowed_tools: List[str] = Field(default_factory=list)
    write_permitted_tools: List[str] = Field(default_factory=list)
    classification_ceiling: ResearchDataClassification = ResearchDataClassification.CONFIDENTIAL
    purpose: str = "APPROVED_RESEARCH"
    model_id: str = "zmie-onprem-llm"


class PrivateReport(BaseModel):
    report_id: str = Field(default_factory=lambda: _id("prep"))
    tenant_id: str
    project_id: Optional[str]
    title: str
    public_inputs: List[Dict[str, Any]] = Field(default_factory=list)
    private_inputs: List[Dict[str, Any]] = Field(default_factory=list)
    derived_analysis: str = ""
    classification: ResearchDataClassification = ResearchDataClassification.CONFIDENTIAL
    provenance: Dict[str, Any] = Field(default_factory=dict)
    access_notice: str = "CONFIDENTIAL — contains organization-private research. Internal citations are not public URLs."
    created_by: str = "unknown"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PrivateConnector(BaseModel):
    connector_id: str = Field(default_factory=lambda: _id("conn"))
    tenant_id: str
    connector_type: str  # S3, POSTGRES, ELN, LIMS, FHIR_SERVER, INTERNAL_API
    credential_ref: str  # reference into secret manager, never the secret itself
    allowed_dataset_ids: List[str] = Field(default_factory=list)
    network_policy: str = "PRIVATE_ENDPOINT_ONLY"
    read_only: bool = True
    status: str = "ACTIVE"  # ACTIVE, PAUSED


class PrivacyIncident(BaseModel):
    incident_id: str = Field(default_factory=lambda: _id("pinc"))
    incident_type: str  # SECURITY_INCIDENT, PRIVACY_INCIDENT, DATA_LEAK_INCIDENT, POLICY_VIOLATION, MODEL_LEAKAGE_INCIDENT
    category: str
    tenant_id: Optional[str]
    actor_id: Optional[str]
    details: str  # redacted; never contains private payloads
    severity: str = "MEDIUM"
    status: str = "DETECTED"  # DETECTED, UNDER_REVIEW, CONTAINED, RESOLVED
    containment_actions: List[str] = Field(default_factory=list)
    detected_at: datetime = Field(default_factory=datetime.utcnow)
