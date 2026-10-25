"""
ZMIE Continuous Evidence & Knowledge Revalidation Models
Continuous Evidence Revalidation Data Models

Implements canonical models for:
- Revalidation States (Clause 6)
- Freshness States (Clause 48)
- Content Change Impacts (Clauses 13, 19)
- Revalidation Triggers (Clause 24)
- Revalidation Scopes (Clause 29)
- Revalidation Priorities (Clause 74)
- Revalidation Decisions (Clauses 127, 262)
- Source Watchers & Topic Watchers (Clauses 10, 57-61)
- Source Diff & Multi-dimensional change hashes (Clauses 12-16)
- Dependency Graphs & Impact Analysis (Clauses 17-20)
- Revalidation Jobs & Orchestration (Clauses 76-83)
- Revalidation Certificates (Clause 50)
- Historical Knowledge Versions & Staleness Markers (Clauses 85-90, 184)
- Knowledge Health Profiles (Clause 119)
"""

from __future__ import annotations
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


# --- CLAUSE 13, 19: Content Change Classification ---
class ContentChangeImpact(str, Enum):
    NON_MATERIAL = "NON_MATERIAL"
    LOW_IMPACT = "LOW_IMPACT"
    MODERATE_IMPACT = "MODERATE_IMPACT"
    HIGH_IMPACT = "HIGH_IMPACT"
    CRITICAL_IMPACT = "CRITICAL_IMPACT"
    UNKNOWN_IMPACT = "UNKNOWN_IMPACT"


# --- CLAUSE 21, 50, 74: Severity & Priority ---
class InvalidationSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    INFORMATIONAL = "INFORMATIONAL"


class RevalidationPriority(str, Enum):
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"
    CRITICAL = "CRITICAL"


# --- CLAUSE 6: Revalidation States ---
class RevalidationState(str, Enum):
    CURRENT = "CURRENT"
    REVALIDATION_DUE = "REVALIDATION_DUE"
    REVALIDATION_IN_PROGRESS = "REVALIDATION_IN_PROGRESS"
    REVALIDATED = "REVALIDATED"
    REVALIDATED_NO_CHANGE = "REVALIDATED_NO_CHANGE"
    CHANGED = "CHANGED"
    CONFLICTING = "CONFLICTING"
    OUTDATED = "OUTDATED"
    RETRACTED = "RETRACTED"
    SUPERSEDED = "SUPERSEDED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    REVALIDATION_FAILED = "REVALIDATION_FAILED"
    REVALIDATION_BLOCKED = "REVALIDATION_BLOCKED"
    UNKNOWN = "UNKNOWN"
    POTENTIALLY_STALE = "POTENTIALLY_STALE"
    PARTIALLY_REVALIDATED = "PARTIALLY_REVALIDATED"
    CHECK_UNAVAILABLE = "CHECK_UNAVAILABLE"
    SOURCE_NOT_REVALIDATED = "SOURCE_NOT_REVALIDATED"
    NO_NEW_EVIDENCE_FOUND = "NO_NEW_EVIDENCE_FOUND"


# --- CLAUSE 48: Freshness States ---
class FreshnessState(str, Enum):
    FRESH = "FRESH"
    CURRENT = "CURRENT"
    AGING = "AGING"
    DUE = "DUE"
    OVERDUE = "OVERDUE"
    STALE = "STALE"
    UNKNOWN = "UNKNOWN"


# --- CLAUSE 24: Revalidation Triggers ---
class RevalidationTrigger(str, Enum):
    TIME_TRIGGERED = "TIME_TRIGGERED"
    SOURCE_TRIGGERED = "SOURCE_TRIGGERED"
    EVENT_TRIGGERED = "EVENT_TRIGGERED"
    CONFLICT_TRIGGERED = "CONFLICT_TRIGGERED"
    USER_TRIGGERED = "USER_TRIGGERED"
    POLICY_TRIGGERED = "POLICY_TRIGGERED"
    GOVERNANCE_TRIGGERED = "GOVERNANCE_TRIGGERED"
    DEPENDENCY_TRIGGERED = "DEPENDENCY_TRIGGERED"
    DATA_TRIGGERED = "DATA_TRIGGERED"
    MODEL_TRIGGERED = "MODEL_TRIGGERED"


# --- CLAUSE 29: Revalidation Scopes ---
class RevalidationScope(str, Enum):
    OBJECT_ONLY = "OBJECT_ONLY"
    DEPENDENCIES = "DEPENDENCIES"
    SUBGRAPH = "SUBGRAPH"
    PROJECT = "PROJECT"
    TOPIC = "TOPIC"
    KNOWLEDGE_DOMAIN = "KNOWLEDGE_DOMAIN"
    GLOBAL = "GLOBAL"


# --- CLAUSE 127, 262: Revalidation Decisions ---
class RevalidationDecision(str, Enum):
    NO_ACTION = "NO_ACTION"
    TARGETED_REVALIDATION = "TARGETED_REVALIDATION"
    FULL_REVALIDATION = "FULL_REVALIDATION"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    RESTRICT = "RESTRICT"
    QUARANTINE = "QUARANTINE"


# --- CLAUSE 10: Source Watch Status ---
class SourceWatchStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    FAILED = "FAILED"
    DEGRADED = "DEGRADED"
    DISABLED = "DISABLED"


# --- CLAUSE 9, 269: Surveillance & Revalidation Event Types ---
class RevalidationEventType(str, Enum):
    STUDY_RETRACTED = "STUDY_RETRACTED"
    EXPRESSION_OF_CONCERN = "EXPRESSION_OF_CONCERN"
    ERRATUM_ISSUED = "ERRATUM_ISSUED"
    NEW_CONFLICTING_RCT = "NEW_CONFLICTING_RCT"
    METHODOLOGY_CHALLENGED = "METHODOLOGY_CHALLENGED"
    NEW_STUDY_PUBLISHED = "NEW_STUDY_PUBLISHED"
    GUIDELINE_UPDATED = "GUIDELINE_UPDATED"
    REGULATORY_STATUS_CHANGED = "REGULATORY_STATUS_CHANGED"
    SAFETY_WARNING_ISSUED = "SAFETY_WARNING_ISSUED"
    DATASET_CORRECTED = "DATASET_CORRECTED"
    ONTOLOGY_MAPPING_CHANGED = "ONTOLOGY_MAPPING_CHANGED"
    MODEL_VERSION_CHANGED = "MODEL_VERSION_CHANGED"
    AGENT_VERSION_CHANGED = "AGENT_VERSION_CHANGED"
    POLICY_CHANGED = "POLICY_CHANGED"
    USER_CHALLENGE = "USER_CHALLENGE"
    TIME_EXPIRED = "TIME_EXPIRED"


# --- CLAUSE 17, 18, 268: Graph Node and Edge Types ---
class DependencyNodeType(str, Enum):
    SOURCE = "SOURCE"
    DOCUMENT = "DOCUMENT"
    PRIMARY_STUDY = "PRIMARY_STUDY"
    EXTRACTED_FINDING = "EXTRACTED_FINDING"
    META_ANALYSIS = "META_ANALYSIS"
    GRADE_PROFILE = "GRADE_PROFILE"
    CLINICAL_RECOMMENDATION = "CLINICAL_RECOMMENDATION"
    RESEARCH_SNAPSHOT = "RESEARCH_SNAPSHOT"
    CLAIM = "CLAIM"
    KNOWLEDGE_OBJECT = "KNOWLEDGE_OBJECT"
    ONTOLOGY_MAPPING = "ONTOLOGY_MAPPING"
    DATASET = "DATASET"
    MODEL = "MODEL"
    SIMULATION = "SIMULATION"
    SAFETY_SIGNAL = "SAFETY_SIGNAL"
    REGULATORY_FACT = "REGULATORY_FACT"
    REPORT = "REPORT"


class DependencyEdge(BaseModel):
    source_id: str
    target_id: str
    relation_type: str = "DEPENDS_ON"
    weight: float = 1.0


# --- CLAUSE 10: Source Watch Entity ---
class SourceWatch(BaseModel):
    watch_id: str = Field(default_factory=lambda: f"watch-{uuid.uuid4().hex[:10]}")
    source_id: str
    watch_type: str = "LITERATURE"
    schedule: str = "0 0 * * *"  # Cron daily
    provider: str = "CROSSREF"
    last_checked_at: Optional[str] = None
    next_check_at: Optional[str] = None
    last_success_at: Optional[str] = None
    last_failure_at: Optional[str] = None
    status: SourceWatchStatus = SourceWatchStatus.ACTIVE
    policy: str = "DEFAULT"
    owner: str = "SYSTEM"
    failure_count: int = 0


# --- CLAUSE 57-61: Topic Watcher Entity ---
class TopicWatcher(BaseModel):
    watcher_id: str = Field(default_factory=lambda: f"topic-watch-{uuid.uuid4().hex[:10]}")
    topic: str
    terms: List[str]
    entities: List[str] = Field(default_factory=list)
    search_strategy: str = "HYBRID_BM25_DENSE"
    sources: List[str] = Field(default_factory=lambda: ["PUBMED", "CROSSREF", "CLINICALTRIALS_GOV"])
    schedule: str = "DAILY"
    owner: str = "SYSTEM"
    scope: str = "PUBLIC"  # PUBLIC, PRIVATE, ENTERPRISE
    tenant_id: Optional[str] = None


# --- CLAUSE 12-16: Source Diff & Content Hashing ---
class SourceDiff(BaseModel):
    diff_id: str = Field(default_factory=lambda: f"diff-{uuid.uuid4().hex[:10]}")
    source_id: str
    old_version: str
    new_version: str
    old_hash: str
    new_hash: str
    is_material: bool
    impact_level: ContentChangeImpact
    added_passages: List[str] = Field(default_factory=list)
    removed_passages: List[str] = Field(default_factory=list)
    modified_sections: List[str] = Field(default_factory=list)
    metadata_diff: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


# --- CLAUSE 19, 20: Impact Analysis Report ---
class ImpactAnalysisReport(BaseModel):
    impact_id: str = Field(default_factory=lambda: f"impact-{uuid.uuid4().hex[:10]}")
    trigger_event_id: str
    target_object_id: str
    impact_level: ContentChangeImpact
    affected_categories: List[str]
    affected_nodes: List[str]
    downstream_claims: List[str] = Field(default_factory=list)
    downstream_guidelines: List[str] = Field(default_factory=list)
    downstream_snapshots: List[str] = Field(default_factory=list)
    downstream_models: List[str] = Field(default_factory=list)
    downstream_datasets: List[str] = Field(default_factory=list)
    requires_human_review: bool = False
    rationale: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


# --- CLAUSE 76-83: Revalidation Job Model ---
class RevalidationJob(BaseModel):
    job_id: str = Field(default_factory=lambda: f"rev-job-{uuid.uuid4().hex[:10]}")
    object_type: DependencyNodeType
    object_id: str
    trigger: RevalidationTrigger
    priority: RevalidationPriority = RevalidationPriority.NORMAL
    scope: RevalidationScope = RevalidationScope.DEPENDENCIES
    policy_version: str = "v1.0.0"
    status: str = "QUEUED"  # QUEUED, RUNNING, WAITING_REVIEW, COMPLETED, PARTIAL, FAILED, CANCELLED, BLOCKED
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result_summary: Optional[str] = None
    decision: Optional[RevalidationDecision] = None
    error: Optional[str] = None
    audit_id: Optional[str] = None
    revalidation_key: str = ""
    tenant_id: Optional[str] = None


# --- CLAUSE 50: Revalidation Certificate ---
class RevalidationCertificate(BaseModel):
    certificate_id: str = Field(default_factory=lambda: f"cert-rev-{uuid.uuid4().hex[:10]}")
    object_id: str
    object_version: str
    revalidation_id: str
    issued_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    sources_checked: List[str]
    search_scope: RevalidationScope
    evidence_state: RevalidationState
    conflict_state: str
    reviewer: str
    policy_version: str
    result: str
    hmac_signature: str


# --- CLAUSE 85-90, 202-208: Knowledge Version & Snapshots ---
class KnowledgeVersion(BaseModel):
    version_id: str = Field(default_factory=lambda: f"kv-{uuid.uuid4().hex[:10]}")
    knowledge_id: str
    version_number: int
    state: RevalidationState
    claims: List[Dict[str, Any]] = Field(default_factory=list)
    evidence_summary: str
    valid_from: str
    valid_to: Optional[str] = None
    superseded_by: Optional[str] = None
    revalidation_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


# --- CLAUSE 119: Multidimensional Knowledge Health ---
class KnowledgeHealth(BaseModel):
    knowledge_id: str
    evidence_health: str = "SOUND"
    freshness_state: FreshnessState = FreshnessState.FRESH
    provenance_score: float = 1.0
    conflict_state: str = "RESOLVED"
    review_state: str = "EXPERT_REVIEWED"
    revalidation_state: RevalidationState = RevalidationState.CURRENT
    last_verified_at: str
    next_revalidation_at: Optional[str] = None


# --- CLAUSE 45, 54: Surveillance Event (Backwards Compatible) ---
class SurveillanceEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"surv-{uuid.uuid4().hex[:10]}")
    study_id: str
    doi: Optional[str] = None
    event_type: RevalidationEventType
    severity: InvalidationSeverity = InvalidationSeverity.CRITICAL
    source_notice_url: Optional[str] = None
    reason: str
    detected_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    verified_by_firewall: bool = False
    tenant_id: Optional[str] = None


# --- CLAUSE 56: Evidence Delta Report (Backwards Compatible) ---
class EvidenceDeltaReport(BaseModel):
    delta_id: str = Field(default_factory=lambda: f"delta-{uuid.uuid4().hex[:10]}")
    trigger_event: SurveillanceEvent
    affected_nodes_count: int
    affected_node_ids: List[str]
    previous_grade_certainty: Optional[str] = None
    new_grade_certainty: Optional[str] = None
    previous_pooled_effect: Optional[float] = None
    recomputed_pooled_effect: Optional[float] = None
    epistemic_shift_magnitude: float
    affected_guidelines: List[str] = Field(default_factory=list)
    affected_snapshots: List[str] = Field(default_factory=list)
    requires_human_review: bool
    status: str = "PENDING_REVIEW"
    decision: RevalidationDecision = RevalidationDecision.HUMAN_REVIEW
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
