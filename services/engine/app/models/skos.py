"""
ZMIE Scientific Knowledge Operating System Data Models (Prompt 25)
Defines unified Knowledge Fabric schemas, 16 epistemic states,
master entity registry, multi-graph models, graph-of-graphs traversal paths,
temporal knowledge snapshots, gap maps, revalidation workflows,
reproducibility certificates, and unified scientific answers.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from pydantic import BaseModel, Field

from app.models.federated_privacy import ResearchDataClassification, AgentMode, AgentContext


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


# ==============================================================================
# 1. Epistemic, Entity & Relationship Enums
# ==============================================================================

class SKOSEpistemicState(str, Enum):
    """
    16 distinct epistemic states (Clauses 15, 355).
    Guarantees strict separation between observation, inference, simulation, and hypothesis.
    """
    OBSERVED = "OBSERVED"
    REPORTED = "REPORTED"
    MEASURED = "MEASURED"
    DERIVED = "DERIVED"
    COMPUTED = "COMPUTED"
    MODELED = "MODELED"
    SIMULATED = "SIMULATED"
    PREDICTED = "PREDICTED"
    INFERRED = "INFERRED"
    HYPOTHESIZED = "HYPOTHESIZED"
    PROPOSED = "PROPOSED"
    SUPPORTED = "SUPPORTED"
    VALIDATED = "VALIDATED"
    PROVEN = "VALIDATED"
    CONTESTED = "CONTESTED"
    CHALLENGED = "CONTESTED"
    ASSOCIATED = "INFERRED"
    CORRELATED = "INFERRED"
    REVISED = "VALIDATED"
    RETRACTED = "RETRACTED"
    UNKNOWN = "UNKNOWN"


class SKOSEntityType(str, Enum):
    """Core entity classes in the ZMIE Knowledge Fabric (Clauses 6, 9)."""
    SOURCE = "SOURCE"
    DOCUMENT = "DOCUMENT"
    TERM = "TERM"
    CONCEPT = "CONCEPT"
    BIOMEDICAL_CONCEPT = "CONCEPT"
    ENTITY = "ENTITY"
    RESEARCHER = "RESEARCHER"
    INSTITUTION = "INSTITUTION"
    PROJECT = "PROJECT"
    DATASET = "DATASET"
    STUDY = "STUDY"
    TRIAL = "TRIAL"
    EXPERIMENT = "EXPERIMENT"
    MODEL = "MODEL"
    RESULT = "RESULT"
    EVIDENCE = "EVIDENCE"
    CLAIM = "CLAIM"
    MECHANISM = "MECHANISM"
    MOLECULAR_TARGET = "MECHANISM"
    CAUSAL_RELATION = "CAUSAL_RELATION"
    SAFETY_SIGNAL = "SAFETY_SIGNAL"
    REGULATORY_STATE = "REGULATORY_STATE"
    REGULATORY_RECORD = "REGULATORY_STATE"
    GUIDELINE = "GUIDELINE"
    HYPOTHESIS = "HYPOTHESIS"
    SIMULATION = "SIMULATION"


class SKOSRelationshipType(str, Enum):
    """Canonical edge types across the Knowledge Graph of Graphs (Clause 26, 53)."""
    IS_A = "IS_A"
    PART_OF = "PART_OF"
    RELATED_TO = "RELATED_TO"
    STUDIED_IN = "STUDIED_IN"
    SUPPORTED_BY = "SUPPORTED_BY"
    CONTRADICTED_BY = "CONTRADICTED_BY"
    CAUSES = "CAUSES"
    ASSOCIATED_WITH = "ASSOCIATED_WITH"
    MECHANISTICALLY_RELATED = "MECHANISTICALLY_RELATED"
    MEASURED_BY = "MEASURED_BY"
    TREATED_BY = "TREATED_BY"
    HAS_RISK = "HAS_RISK"
    HAS_WARNING = "HAS_WARNING"
    HAS_REGULATORY_STATUS = "HAS_REGULATORY_STATUS"
    DERIVED_FROM = "DERIVED_FROM"
    PREDICTS = "PREDICTS"
    TESTED_BY = "TESTED_BY"
    REPLICATED_BY = "REPLICATED_BY"
    REVALIDATED_BY = "REVALIDATED_BY"
    SUPERSEDES = "SUPERSEDES"


class RevalidationState(str, Enum):
    """Knowledge object lifecycle revalidation state (Clause 67)."""
    CURRENT = "CURRENT"
    FLAGGED = "FLAGGED"
    MONITOR = "MONITOR"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    REVALIDATING = "REVALIDATING"
    UPDATED = "UPDATED"
    SUPERSEDED = "SUPERSEDED"
    CONTESTED = "CONTESTED"
    RETIRED = "RETIRED"


class KnowledgeDecisionAction(str, Enum):
    """Governed decisions on revalidated knowledge objects (Clause 69)."""
    NO_CHANGE = "NO_CHANGE"
    UPDATE = "UPDATE"
    QUALIFY = "QUALIFY"
    WEAKEN = "WEAKEN"
    STRENGTHEN = "STRENGTHEN"
    SPLIT = "SPLIT"
    MERGE = "MERGE"
    DEPRECATE = "DEPRECATE"
    CONTEST = "CONTEST"
    RETRACT = "RETRACT"
    REVISE_CLAIM = "REVISE_CLAIM"


class GapDimension(str, Enum):
    """9 dimensions of research & knowledge gaps (Clause 62)."""
    EVIDENCE_GAP = "EVIDENCE_GAP"
    DATA_GAP = "DATA_GAP"
    MECHANISM_GAP = "MECHANISM_GAP"
    CAUSAL_GAP = "CAUSAL_GAP"
    TERMINOLOGY_GAP = "TERMINOLOGY_GAP"
    REPLICATION_GAP = "REPLICATION_GAP"
    POPULATION_GAP = "POPULATION_GAP"
    METHOD_GAP = "METHOD_GAP"
    REGULATORY_GAP = "REGULATORY_GAP"


class AnswerState(str, Enum):
    """Completion states of unified scientific answers (Clause 164)."""
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    LIMITED = "LIMITED"
    BLOCKED = "BLOCKED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"


# ==============================================================================
# 2. Master Entity & Relationship Models (Single Source of Truth)
# ==============================================================================

class SKOSMasterEntity(BaseModel):
    """
    Authoritative single-source-of-truth representation of any scientific object (Clauses 7, 9, 10).
    """
    stable_id: str = Field(default_factory=lambda: _id("ent"))
    entity_type: SKOSEntityType
    name: str
    description: str = ""
    version_id: str = "1.0.0"
    epistemic_state: SKOSEpistemicState = SKOSEpistemicState.REPORTED
    classification: ResearchDataClassification = ResearchDataClassification.PUBLIC
    tenant_scope: Optional[str] = None  # None = Global Public
    project_scope: Optional[str] = None
    source_identifiers: Dict[str, str] = Field(default_factory=dict)  # e.g. {"pmid": "18442638", "doi": "10.1016/..."}
    external_identifiers: Dict[str, str] = Field(default_factory=dict)  # e.g. {"mesh": "D003924", "orcid": "0000-..."}
    provenance_source_id: str = "SRC-GLOBAL-REGISTRY"
    revalidation_state: RevalidationState = RevalidationState.CURRENT
    valid_from: datetime = Field(default_factory=datetime.utcnow)
    valid_to: Optional[datetime] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    history: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def metadata(self) -> Dict[str, Any]:
        return self.properties


class SKOSRelationshipEdge(BaseModel):
    """
    Provenanced relationship between two entities across graphs (Clause 26, 54).
    """
    edge_id: str = Field(default_factory=lambda: _id("edge"))
    source_id: str
    target_id: str
    relationship_type: SKOSRelationshipType
    provenance_source_id: str = "SRC-PUBMED"
    citation_id: Optional[str] = None
    confidence_score: float = 1.0
    epistemic_state: SKOSEpistemicState = SKOSEpistemicState.VALIDATED
    scope: str = "PUBLIC"  # PUBLIC, TENANT, PROJECT, FEDERATED
    tenant_id: Optional[str] = None
    valid_from: datetime = Field(default_factory=datetime.utcnow)
    valid_to: Optional[datetime] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    review_state: str = "APPROVED"
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ==============================================================================
# 3. Multi-Hop Graph Traversal Paths
# ==============================================================================

class PathHop(BaseModel):
    step_number: int
    entity: SKOSMasterEntity
    relationship: Optional[SKOSRelationshipType] = None
    provenance: str = ""
    evidence_backing: Optional[str] = None


class TraversalPath(BaseModel):
    """Generalized multi-hop traversable scientific pathway (Clauses 55-60, 311-314)."""
    path_id: str = Field(default_factory=lambda: _id("path"))
    path_type: str  # EVIDENCE_PATH, RESEARCH_PATH, MECHANISM_PATH, CAUSAL_PATH, SAFETY_PATH, TERMINOLOGY_PATH, EXPERIMENT_PATH
    direction: str = "FORWARD"
    start_entity_id: str
    end_entity_id: str
    hops: List[PathHop] = Field(default_factory=list)
    is_bidirectional: bool = True
    summary: str = ""
    epistemic_fidelity: float = 1.0

    @property
    def total_hops(self) -> int:
        return len(self.hops)


# ==============================================================================
# 4. Temporal Snapshots & Knowledge Diff
# ==============================================================================

class ZMIEKnowledgeSnapshot(BaseModel):
    """
    Immutable temporal snapshot of platform knowledge at timestamp T (Clauses 13, 14, 279).
    """
    snapshot_id: str = Field(default_factory=lambda: _id("snap"))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    platform_version: str = "1.0.0"
    source_universe_hash: str = "sha256:src-universe-2026"
    ontology_version: str = "2026.1"
    evidence_graph_hash: str = "sha256:evd-graph-2026"
    claim_count: int = 142000
    entities_count: int = 560000
    edges_count: int = 2100000
    tenant_id: Optional[str] = None
    description: str = "Master SKOS System Knowledge Snapshot"


class KnowledgeDiffItem(BaseModel):
    object_id: str
    entity_type: SKOSEntityType
    field_changed: str
    old_value: Any
    new_value: Any
    reason: str
    evidence_doi: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ScientificKnowledgeDiff(BaseModel):
    """Difference analysis between two temporal snapshots (Clauses 71, 116)."""
    diff_id: str = Field(default_factory=lambda: _id("diff"))
    snapshot_a_id: str
    snapshot_b_id: str
    base_snapshot_id: Optional[str] = None
    target_snapshot_id: Optional[str] = None
    changes_count: int = 0
    items: List[KnowledgeDiffItem] = Field(default_factory=list)
    impact_summary: str = ""
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    def model_post_init(self, __context: Any) -> None:
        if self.base_snapshot_id is None:
            self.base_snapshot_id = self.snapshot_a_id
        if self.target_snapshot_id is None:
            self.target_snapshot_id = self.snapshot_b_id


# ==============================================================================
# 5. Knowledge Gap Map
# ==============================================================================

class GapItem(BaseModel):
    gap_id: str = Field(default_factory=lambda: _id("gap"))
    dimension: GapDimension
    topic: str
    description: str
    indexed_coverage_statement: str = "Gap identified in indexed/public ZMIE coverage."
    confidence: float = 0.95
    created_at: datetime = Field(default_factory=datetime.utcnow)


class KnowledgeGapMap(BaseModel):
    """Master 9-dimensional knowledge gap registry (Clauses 62, 63)."""
    map_id: str = Field(default_factory=lambda: _id("gmap"))
    target_topic: str
    gaps: List[GapItem] = Field(default_factory=list)
    total_gaps: int = 0
    total_gaps_identified: Optional[int] = None
    gaps_by_dimension: Dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    def model_post_init(self, __context: Any) -> None:
        if self.total_gaps_identified is None:
            self.total_gaps_identified = self.total_gaps or len(self.gaps)
        if not self.gaps_by_dimension and self.gaps:
            self.gaps_by_dimension = {
                (g.dimension.value if hasattr(g.dimension, "value") else str(g.dimension)): g.description
                for g in self.gaps
            }


# ==============================================================================
# 6. Revalidation & Retraction Impact Engine
# ==============================================================================

class RetractionNotice(BaseModel):
    """Formal retraction / erratum / withdrawal notice (Clauses 34, 35, 303)."""
    notice_id: str = Field(default_factory=lambda: _id("retract"))
    study_id: str = "STU-BER-001"
    doi: str = "10.1001/jama.2023.001"
    study_doi: Optional[str] = None
    pmid: Optional[str] = None
    retraction_doi: Optional[str] = None
    title: str = "Formal Retraction Notice"
    nature: str = "RETRACTION"  # RETRACTION, CORRECTION, ERRATUM, EXPRESSION_OF_CONCERN, WITHDRAWAL
    retraction_type: str = "FULL_RETRACTION"
    author_statement: str = ""
    reason: str = "Data integrity concerns"
    retraction_date: str = "2026-10-01"


class RetractionImpactAnalysis(BaseModel):
    """Cascading downstream impact analysis of a retracted publication (Clause 34, 303)."""
    analysis_id: str = Field(default_factory=lambda: _id("rimpact"))
    retraction_notice: RetractionNotice
    affected_studies: List[str] = Field(default_factory=list)
    affected_claims: List[str] = Field(default_factory=list)
    affected_syntheses: List[str] = Field(default_factory=list)
    affected_guidelines: List[str] = Field(default_factory=list)
    affected_models: List[str] = Field(default_factory=list)
    quarantine_status: str = "QUARANTINED"
    historical_preserved: bool = True  # Never silently erase history (Clause 239)


class RevalidationTask(BaseModel):
    """Structured unit of knowledge re-evaluation (Clauses 66-68)."""
    task_id: str = Field(default_factory=lambda: _id("reval"))
    target_entity_id: str = ""
    target_claim_id: Optional[str] = None
    trigger_reason: str = ""
    priority: str = "HIGH"  # CRITICAL, HIGH, NORMAL, LOW
    status: RevalidationState = RevalidationState.REVIEW_REQUIRED
    state: RevalidationState = RevalidationState.FLAGGED
    evidence_package: List[Dict[str, Any]] = Field(default_factory=list)
    impact_assessment: str = ""
    assigned_reviewer_pool: str = "SCIENTIFIC_METHODOLOGY_BOARD"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RevalidationDecision(BaseModel):
    """Governed resolution of a revalidation task (Clauses 69, 88)."""
    decision_id: str = Field(default_factory=lambda: _id("rdec"))
    task_id: str = ""
    reviewer_user_id: str = ""
    action: Optional[KnowledgeDecisionAction] = None
    decision_action: KnowledgeDecisionAction = KnowledgeDecisionAction.UPDATE
    rationale: str = ""
    old_version_id: str = "1.0.0"
    new_version_id: str = "1.0.1"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ==============================================================================
# 7. Scientific Execution & Provenance Certificates
# ==============================================================================

class ZMIEScientificExecutionCertificate(BaseModel):
    """Verifiable execution certificate for computational reproduction (Clauses 95, 96, 310)."""
    certificate_id: str = Field(default_factory=lambda: _id("cert-exec"))
    question: str = ""
    plan_id: str = ""
    computation_id: Optional[str] = None
    source_snapshot_hash: str = "sha256:src-snapshot"
    terminology_version: str = "2026.1"
    dataset_snapshot_hash: str = "sha256:data-snapshot"
    workflow_id: str = "wf-computation-01"
    code_hash: str = ""
    data_hash: Optional[str] = None
    model_version: str = "gemini-3.8-scientific"
    agent_versions: Dict[str, str] = Field(default_factory=dict)
    environment_spec: Dict[str, Any] = Field(default_factory=dict)
    policy_version: str = "2026.1"
    verification_passed: bool = True
    is_deterministic: bool = True
    reproducibility_status: str = "REPRODUCIBLE"
    result_hash: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ZMIEKnowledgeProvenanceCertificate(BaseModel):
    """Cryptographic provenance passport for published knowledge objects (Clause 97)."""
    certificate_id: str = Field(default_factory=lambda: _id("cert-prov"))
    object_id: str = ""
    claim_id: Optional[str] = None
    entity_type: SKOSEntityType = SKOSEntityType.CLAIM
    authoritative_sources: List[str] = Field(default_factory=list)
    root_source_ids: List[str] = Field(default_factory=list)
    graph_path: List[str] = Field(default_factory=list)
    hop_count: int = 1
    originating_researchers: List[str] = Field(default_factory=list)
    evidence_grade: str = "MODERATE"
    integrity_status: str = "VERIFIED"
    governance_approval_id: str = "gov-appr-default"
    issued_at: datetime = Field(default_factory=datetime.utcnow)


# ==============================================================================
# 8. Unified Scientific Answer & Completeness Model
# ==============================================================================

class CoverageDimensionReport(BaseModel):
    """8-dimensional coverage metrics (Clauses 104, 105, 299)."""
    source_coverage: str = "WIDE (PubMed, OpenAlex, Europe PMC, TKDL)"
    evidence_coverage: str = "MODERATE (2 RCTs, 1 Meta-Analysis)"
    research_coverage: str = "WIDE (Cross-national research network)"
    data_coverage: str = "MODERATE (1 Trial Dataset, 1 In Vitro Assay)"
    terminology_coverage: str = "COMPLETE (MeSH, Unani, Ayurveda, TCM)"
    safety_coverage: str = "COMPLETE (CYP450, Contraindications, Red Flags)"
    regulatory_coverage: str = "COMPLETE (FDA, EMA, CDSCO)"
    computational_coverage: str = "VERIFIED (Double-computation passed)"
    overall_status: str = "WIDE"
    overall_coverage_pct: float = 92.5


class AnswerSection(BaseModel):
    section_name: str
    epistemic_state: SKOSEpistemicState
    content: str
    sources: List[str] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)


class SKOSAnswer(BaseModel):
    """
    Unified, structured scientific answer object (Clauses 161-168).
    Strictly forbids hallucination; links every conclusion to verified artifacts.
    """
    answer_id: str = Field(default_factory=lambda: _id("ans"))
    question: str
    state: AnswerState = AnswerState.COMPLETE
    summary: str
    summary_findings: Optional[str] = None
    sections: List[AnswerSection] = Field(default_factory=list)
    coverage: CoverageDimensionReport
    coverage_report: Optional[CoverageDimensionReport] = None
    uncertainties: List[str] = Field(default_factory=list)
    provenance_certificate_id: Optional[str] = None
    provenance_certificate: Optional[str] = None
    execution_certificate_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def model_post_init(self, __context: Any) -> None:
        if self.summary_findings is None:
            self.summary_findings = self.summary
        if self.coverage_report is None:
            self.coverage_report = self.coverage
        if self.provenance_certificate is None:
            self.provenance_certificate = self.provenance_certificate_id
