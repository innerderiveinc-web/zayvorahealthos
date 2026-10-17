"""
ZMIE Scientific Agent Operating System Data Models (Prompt 24)
Comprehensive schema definitions for multi-agent scientific execution,
epistemic boundaries, task DAGs, tool registries, scoped memory,
verification gates, and human governance.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from pydantic import BaseModel, Field

from app.models.federated_privacy import ResearchDataClassification, AgentMode


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


# ==============================================================================
# 1. Epistemic & Classification Enums
# ==============================================================================

class EpistemicState(str, Enum):
    """
    14 distinct epistemic states (Clause 16, 292, 293).
    No agent output is automatically truth; every output belongs to an epistemic state.
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
    VALIDATED = "VALIDATED"
    CONTESTED = "CONTESTED"
    UNKNOWN = "UNKNOWN"


class AgentRiskLevel(str, Enum):
    """Risk classification determines approval requirements (Clause 9)."""
    LOW_RISK = "LOW_RISK"
    RESEARCH_SUPPORT = "RESEARCH_SUPPORT"
    DATA_ANALYSIS = "DATA_ANALYSIS"
    SCIENTIFIC_REASONING = "SCIENTIFIC_REASONING"
    CLINICAL_SUPPORT = "CLINICAL_SUPPORT"
    REGULATORY = "REGULATORY"
    HIGH_IMPACT = "HIGH_IMPACT"
    PRIVATE_DATA = "PRIVATE_DATA"
    EXTERNAL_ACTION = "EXTERNAL_ACTION"


class AgentLifecycleState(str, Enum):
    """Lifecycle states for agents (Clause 10). Never allow unapproved agents in prod."""
    REGISTERED = "REGISTERED"
    AVAILABLE = "AVAILABLE"
    DISABLED = "DISABLED"
    DEPRECATED = "DEPRECATED"
    EXPERIMENTAL = "EXPERIMENTAL"
    EVALUATION = "EVALUATION"
    APPROVED = "APPROVED"
    RESTRICTED = "RESTRICTED"
    RETIRED = "RETIRED"


class AgentCapability(str, Enum):
    """Granular agent capabilities (Clause 8)."""
    SEARCH_PUBLIC = "SEARCH_PUBLIC"
    SEARCH_PRIVATE = "SEARCH_PRIVATE"
    READ_DATASET = "READ_DATASET"
    WRITE_ANALYSIS = "WRITE_ANALYSIS"
    RUN_COMPUTE = "RUN_COMPUTE"
    USE_GRAPH = "USE_GRAPH"
    USE_MODEL = "USE_MODEL"
    CREATE_HYPOTHESIS = "CREATE_HYPOTHESIS"
    CREATE_REPORT = "CREATE_REPORT"
    REQUEST_REVIEW = "REQUEST_REVIEW"
    PROPOSE_KNOWLEDGE_UPDATE = "PROPOSE_KNOWLEDGE_UPDATE"


class TaskExecutionState(str, Enum):
    """Task states throughout DAG execution (Clause 11)."""
    CREATED = "CREATED"
    PLANNED = "PLANNED"
    WAITING_FOR_INPUT = "WAITING_FOR_INPUT"
    AUTHORIZED = "AUTHORIZED"
    RUNNING = "RUNNING"
    WAITING_FOR_TOOL = "WAITING_FOR_TOOL"
    WAITING_FOR_REVIEW = "WAITING_FOR_REVIEW"
    COMPLETED = "COMPLETED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    BLOCKED = "BLOCKED"


class ToolActionCategory(str, Enum):
    """Tool permission category (Clause 78, 251). Defaults to READ_ONLY."""
    READ_ONLY = "READ_ONLY"
    ANALYZE = "ANALYZE"
    COMPUTE = "COMPUTE"
    PROPOSE = "PROPOSE"
    WRITE_PRIVATE = "WRITE_PRIVATE"
    WRITE_SHARED = "WRITE_SHARED"
    REQUEST_APPROVAL = "REQUEST_APPROVAL"
    EXTERNAL_ACTION = "EXTERNAL_ACTION"
    PUBLISH = "PUBLISH"


class MemoryScope(str, Enum):
    """Scope of agent memory (Clause 29, 191-192)."""
    WORKING = "WORKING"
    TASK = "TASK"
    PROJECT = "PROJECT"
    TENANT = "TENANT"
    LONG_TERM_SCIENTIFIC = "LONG_TERM_SCIENTIFIC"


class MemoryState(str, Enum):
    """Epistemic classification of stored memory (Clause 30)."""
    FACT = "FACT"
    SOURCE_REFERENCE = "SOURCE_REFERENCE"
    DECISION = "DECISION"
    ASSUMPTION = "ASSUMPTION"
    HYPOTHESIS = "HYPOTHESIS"
    TASK_STATE = "TASK_STATE"
    PREFERENCE = "PREFERENCE"
    PRIVATE_CONTEXT = "PRIVATE_CONTEXT"


class ContradictionNature(str, Enum):
    """Classification of detected research contradictions (Clause 43)."""
    DIRECT_CONTRADICTION = "DIRECT_CONTRADICTION"
    APPARENT_CONTRADICTION = "APPARENT_CONTRADICTION"
    CONTEXT_DIFFERENCE = "CONTEXT_DIFFERENCE"
    TEMPORAL_DIFFERENCE = "TEMPORAL_DIFFERENCE"
    METHOD_DIFFERENCE = "METHOD_DIFFERENCE"
    POPULATION_DIFFERENCE = "POPULATION_DIFFERENCE"
    TERMINOLOGY_DIFFERENCE = "TERMINOLOGY_DIFFERENCE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class ReviewDecisionAction(str, Enum):
    """Human review actions (Clause 111)."""
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    MODIFY = "MODIFY"
    REQUEST_MORE_EVIDENCE = "REQUEST_MORE_EVIDENCE"
    ASSIGN_REVIEWER = "ASSIGN_REVIEWER"
    PAUSE = "PAUSE"


# ==============================================================================
# 2. Agent Registry & Lifecycle Objects
# ==============================================================================

class AgentDefinition(BaseModel):
    """Core registration for every agent in the OS (Clause 7)."""
    agent_id: str = Field(default_factory=lambda: _id("agent"))
    name: str
    purpose: str
    capabilities: List[AgentCapability] = Field(default_factory=list)
    inputs: List[str] = Field(default_factory=list)
    outputs: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    models: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    risk_level: AgentRiskLevel = AgentRiskLevel.RESEARCH_SUPPORT
    tenant_scope: Optional[str] = None  # None = Global/Platform agent
    version: str = "1.0.0"
    status: AgentLifecycleState = AgentLifecycleState.APPROVED
    owner: str = "zmIE-Core"
    evaluation_status: str = "VERIFIED_GOLDEN"
    classification_ceiling: ResearchDataClassification = ResearchDataClassification.INTERNAL
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AgentVersion(BaseModel):
    """Version metadata for agent code and prompts (Clause 93, 94)."""
    version_id: str = Field(default_factory=lambda: _id("agv"))
    agent_id: str
    version_number: str
    prompt_version: str
    model_version: str
    tool_version_compatibility: List[str] = Field(default_factory=list)
    policy_version: str = "2026.1"
    changelog: str = ""
    released_at: datetime = Field(default_factory=datetime.utcnow)
    active: bool = True


# ==============================================================================
# 3. Tool Registry & Sandboxing Objects
# ==============================================================================

class ToolDefinition(BaseModel):
    """Registered tool contract (Clause 75, 77, 78)."""
    tool_id: str = Field(default_factory=lambda: _id("tool"))
    name: str
    description: str
    category: ToolActionCategory = ToolActionCategory.READ_ONLY
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    permission_required: str = "tool:read"
    risk_level: AgentRiskLevel = AgentRiskLevel.LOW_RISK
    side_effects: bool = False
    requires_approval: bool = False
    max_timeout_ms: int = 15000
    cost_per_call: float = 0.001
    audit_required: bool = True


class ToolExecutionRecord(BaseModel):
    """Audit log record for tool execution (Clause 131)."""
    execution_id: str = Field(default_factory=lambda: _id("tx"))
    tool_id: str
    tool_name: str
    agent_id: str
    task_id: str
    tenant_id: Optional[str] = None
    arguments_metadata: Dict[str, Any] = Field(default_factory=dict)  # Scrubbed of secrets
    output_summary: str = ""
    status: str = "SUCCESS"  # SUCCESS, FAILED, BLOCKED_BY_FIREWALL
    cost: float = 0.0
    latency_ms: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ==============================================================================
# 4. Scoped Memory & Context Objects
# ==============================================================================

class MemoryItem(BaseModel):
    """Structured memory entry with provenance and isolation (Clauses 29-32)."""
    item_id: str = Field(default_factory=lambda: _id("mem"))
    scope: MemoryScope
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None
    agent_id: str
    user_id: Optional[str] = None
    state: MemoryState
    content: str
    source_reference: Optional[str] = None
    confidence_score: float = 1.0
    version: str = "1.0"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ContextSnapshot(BaseModel):
    """Exact context assembled for an execution for replayability (Clause 206, 207)."""
    snapshot_id: str = Field(default_factory=lambda: _id("ctxsnap"))
    task_id: str
    agent_id: str
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None
    authorized_sources: List[str] = Field(default_factory=list)
    memory_items: List[str] = Field(default_factory=list)
    active_policies: List[str] = Field(default_factory=list)
    token_budget: int = 4096
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ==============================================================================
# 5. Agent Tasks, Runs & Protocol
# ==============================================================================

class AgentTask(BaseModel):
    """Governed unit of scientific work (Clause 12)."""
    task_id: str = Field(default_factory=lambda: _id("task"))
    parent_task_id: Optional[str] = None
    root_task_id: Optional[str] = None
    agent_id: str
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None
    user_id: str = "system"
    goal: str
    inputs: Dict[str, Any] = Field(default_factory=dict)
    constraints: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    risk_class: AgentRiskLevel = AgentRiskLevel.RESEARCH_SUPPORT
    status: TaskExecutionState = TaskExecutionState.CREATED
    deadline: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AgentMessage(BaseModel):
    """Type-safe communication between agents (Clause 14, 172-174)."""
    message_id: str = Field(default_factory=lambda: _id("msg"))
    message_type: str = "TASK_RESULT"  # TASK_REQUEST, TASK_RESULT, VERIFICATION_REQUEST, CONFLICT_ALERT
    task_id: str
    agent_id: str
    recipient_agent_id: Optional[str] = None
    status: TaskExecutionState = TaskExecutionState.COMPLETED
    findings: List[str] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)
    artifacts: List[Dict[str, Any]] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentResult(BaseModel):
    """Structured agent output with explicit epistemic boundaries (Clause 15, 16)."""
    result_id: str = Field(default_factory=lambda: _id("res"))
    task_id: str
    agent_id: str
    epistemic_state: EpistemicState
    summary: str
    findings: List[str] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_components: Dict[str, float] = Field(default_factory=dict)
    uncertainties: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    tool_usage: List[str] = Field(default_factory=list)
    artifacts: List[Dict[str, Any]] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    recommended_next_step: Optional[str] = None
    verified_by: Optional[str] = None
    classification: ResearchDataClassification = ResearchDataClassification.INTERNAL
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AgentRun(BaseModel):
    """Complete record of an agent invocation run (Clause 13)."""
    run_id: str = Field(default_factory=lambda: _id("run"))
    agent_id: str
    agent_name: str
    model: str = "gemini-3.8-scientific"
    version: str = "1.0.0"
    task_id: str
    context: Dict[str, Any] = Field(default_factory=dict)
    tools_invoked: List[str] = Field(default_factory=list)
    retrieval_count: int = 0
    result: Optional[AgentResult] = None
    errors: List[str] = Field(default_factory=list)
    tokens: int = 0
    cost: float = 0.0
    status: TaskExecutionState = TaskExecutionState.COMPLETED
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


# ==============================================================================
# 6. Scientific Planning & DAG Objects
# ==============================================================================

class PlanSubtask(BaseModel):
    """A single node in the research plan DAG (Clause 18, 19)."""
    subtask_id: str = Field(default_factory=lambda: _id("stask"))
    name: str
    agent_id: str
    goal: str
    dependencies: List[str] = Field(default_factory=list)  # IDs of tasks that must complete first
    optional_dependencies: List[str] = Field(default_factory=list)
    verification_dependency: Optional[str] = None
    required_sources: List[str] = Field(default_factory=list)
    required_data: List[str] = Field(default_factory=list)
    required_compute: List[str] = Field(default_factory=list)
    risk_class: AgentRiskLevel = AgentRiskLevel.RESEARCH_SUPPORT
    status: TaskExecutionState = TaskExecutionState.CREATED


class PlanModificationRecord(BaseModel):
    """Audit entry for dynamic planning modifications (Clause 20)."""
    mod_id: str = Field(default_factory=lambda: _id("pmod"))
    plan_id: str
    previous_plan_hash: str
    new_plan_hash: str
    reason: str
    trigger: str
    agent_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ResearchPlan(BaseModel):
    """Authoritative research execution plan (Clause 18)."""
    plan_id: str = Field(default_factory=lambda: _id("plan"))
    original_question: str
    normalized_question: str
    objectives: List[str] = Field(default_factory=list)
    subtasks: List[PlanSubtask] = Field(default_factory=list)
    agents_involved: List[str] = Field(default_factory=list)
    dependencies: Dict[str, List[str]] = Field(default_factory=dict)
    required_sources: List[str] = Field(default_factory=list)
    required_data: List[str] = Field(default_factory=list)
    required_compute: List[str] = Field(default_factory=list)
    verification_requirements: List[str] = Field(default_factory=list)
    risk_class: AgentRiskLevel = AgentRiskLevel.RESEARCH_SUPPORT
    approval_requirements: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1


# ==============================================================================
# 7. Disagreement, Knowledge Change & Governance Objects
# ==============================================================================

class AgentDisagreement(BaseModel):
    """Formal record of scientific divergence between agents (Clause 113, 114)."""
    disagreement_id: str = Field(default_factory=lambda: _id("disagree"))
    task_id: str
    agents_involved: List[str] = Field(default_factory=list)
    claims: List[str] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    nature: ContradictionNature = ContradictionNature.CONTEXT_DIFFERENCE
    root_cause: str = ""
    resolution: Optional[str] = None  # None = preserved divergence (Clause 115)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class KnowledgeChangeProposal(BaseModel):
    """Governed proposal for changing global/authoritative knowledge (Clauses 106, 107)."""
    proposal_id: str = Field(default_factory=lambda: _id("kcp"))
    target_object_id: str
    old_state: Dict[str, Any] = Field(default_factory=dict)
    proposed_state: Dict[str, Any] = Field(default_factory=dict)
    evidence_package: List[Dict[str, Any]] = Field(default_factory=list)
    reason: str
    proposing_agent_id: str
    tenant_id: Optional[str] = None
    status: str = "PENDING_REVIEW"  # PENDING_REVIEW, APPROVED, REJECTED
    reviewed_by: Optional[str] = None
    review_comments: Optional[str] = None
    impact_assessment: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ReviewRequest(BaseModel):
    """Human review request for high-impact decisions (Clauses 109-112)."""
    review_id: str = Field(default_factory=lambda: _id("rev"))
    task_id: str
    triggering_agent_id: str
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None
    reason: str
    recommendation: str
    uncertainties: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    supporting_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    status: str = "PENDING"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ReviewDecision(BaseModel):
    """Human governance action on a review request (Clause 111, 112)."""
    decision_id: str = Field(default_factory=lambda: _id("rdec"))
    review_id: str
    reviewer_user_id: str
    reviewer_role: str
    action: ReviewDecisionAction
    decision_rationale: str
    modifications: Optional[Dict[str, Any]] = None
    decided_at: datetime = Field(default_factory=datetime.utcnow)


# ==============================================================================
# 8. Execution Trace & Audit Objects
# ==============================================================================

class TraceEvent(BaseModel):
    """Atomic event in the research execution timeline (Clause 143, 255)."""
    event_id: str = Field(default_factory=lambda: _id("evt"))
    trace_id: str
    event_type: str  # AGENT_STARTED, TOOL_CALLED, VERIFICATION_PASSED, etc.
    agent_id: Optional[str] = None
    task_id: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ResearchCompletion(BaseModel):
    """Transparent summary of research execution completeness (Clause 102, 103)."""
    completed_tasks: List[str] = Field(default_factory=list)
    failed_tasks: List[str] = Field(default_factory=list)
    skipped_tasks: List[str] = Field(default_factory=list)
    blocked_tasks: List[str] = Field(default_factory=list)
    coverage_score: float = 1.0  # 0.0 - 1.0
    verification_status: str = "VERIFIED"  # VERIFIED, UNVERIFIED, PARTIAL
    safety_status: str = "SAFE"
    limitations: List[str] = Field(default_factory=list)
    is_partial: bool = False


class ResearchExecutionTrace(BaseModel):
    """Complete, auditable, replayable research trace (Clause 142, 143, 209)."""
    trace_id: str = Field(default_factory=lambda: _id("trace"))
    question: str
    plan_id: str
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None
    user_id: str = "system"
    agents_executed: List[str] = Field(default_factory=list)
    tools_used: List[str] = Field(default_factory=list)
    sources_retrieved: List[str] = Field(default_factory=list)
    data_artifacts: List[str] = Field(default_factory=list)
    verification_events: List[str] = Field(default_factory=list)
    events: List[TraceEvent] = Field(default_factory=list)
    completion: Optional[ResearchCompletion] = None
    final_synthesis: Optional[str] = None
    epistemic_state: EpistemicState = EpistemicState.DERIVED
    total_cost: float = 0.0
    total_latency_ms: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ==============================================================================
# 9. Incidents & Metrics
# ==============================================================================

class AgentIncident(BaseModel):
    """Recorded agent failure, hallucination, or policy block (Clause 211)."""
    incident_id: str = Field(default_factory=lambda: _id("inc"))
    incident_type: str  # HallucinationIncident, PrivacyIncident, ToolIncident, ScientificIntegrityIncident
    agent_id: str
    task_id: str
    severity: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    description: str
    action_taken: str = "QUARANTINED"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentMetrics(BaseModel):
    """Observability metrics for agent runtime (Clause 133, 219, 220)."""
    agent_id: str
    total_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0
    verification_failures: int = 0
    policy_blocks: int = 0
    total_cost: float = 0.0
    avg_latency_ms: float = 0.0
    citation_accuracy: float = 1.0
    claim_accuracy: float = 1.0
