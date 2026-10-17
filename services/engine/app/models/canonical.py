"""
ZMIE Canonical Core Domain Models
Prompt 28 — MODULE 05 (Core Domain Model) & Clause 17

Defines unified canonical schemas across all ZMIE subsystems:
- Tenant, User, Workspace, Project
- Source, Document
- Entity, Concept, Term
- Claim, Evidence
- ResearchQuestion, ResearchTask, ResearchSnapshot
- Dataset, DatasetVersion
- Computation, Model, Agent, AgentRun
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from app.core.tenancy import DataClassification, TenantTier


class CanonicalStatus(str, Enum):
    ACTIVE = "active"
    DRAFT = "draft"
    COMPLETED = "completed"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    FAILED = "failed"


# --- 1. Tenancy & Organization Hierarchy ---

class TenantRecord(BaseModel):
    tenant_id: str
    name: str
    tier: TenantTier = TenantTier.ENTERPRISE
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class UserRecord(BaseModel):
    user_id: str
    tenant_id: str
    email: str
    full_name: str
    role: str = "researcher"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WorkspaceRecord(BaseModel):
    workspace_id: str
    tenant_id: str
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProjectRecord(BaseModel):
    project_id: str
    workspace_id: str
    tenant_id: str
    name: str
    classification: DataClassification = DataClassification.INTERNAL
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# --- 2. Ingestion & Documents ---

class SourceRecord(BaseModel):
    source_id: str
    name: str
    authority_tier: str = "TIER_A"  # TIER_A to TIER_G
    publisher: Optional[str] = None
    license_type: str = "CC-BY"
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DocumentRecord(BaseModel):
    document_id: str
    source_id: str
    tenant_id: str = "global"
    title: str
    raw_sha256: str
    storage_uri: str
    publication_year: Optional[int] = None
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# --- 3. Ontology & Concept Graph ---

class TermRecord(BaseModel):
    term_id: str
    text: str
    language: str = "en"
    transliteration: Optional[str] = None
    script: Optional[str] = None


class ConceptRecord(BaseModel):
    concept_id: str
    canonical_name: str
    ontology_system: str  # MeSH, SNOMED, ICD-11, UNANI_NAMASTE, AYURVEDA_NAMASTE
    code: Optional[str] = None
    definition: Optional[str] = None


class EntityRecord(BaseModel):
    entity_id: str
    concept_id: str
    entity_type: str  # Disease, Drug, Target, Biomarker, Mizaj, Dosha
    confidence: float = 1.0
    epistemic_distance: float = 0.0


# --- 4. Evidence & Atomic Claims ---

class EvidenceRecord(BaseModel):
    evidence_id: str
    document_id: str
    study_type: str  # RCT, Meta-Analysis, Cohort, Preclinical, InVitro
    pico_population: Optional[str] = None
    pico_intervention: Optional[str] = None
    pico_comparison: Optional[str] = None
    pico_outcome: Optional[str] = None
    grade_score: str = "HIGH"  # HIGH, MODERATE, LOW, VERY_LOW


class ClaimRecord(BaseModel):
    claim_id: str
    subject_entity_id: str
    predicate: str  # INHIBITS, REDUCES_RISK, INTERACTS_WITH, HARMONIZES_MIZAJ
    object_entity_id: str
    evidence_ids: List[str] = Field(default_factory=list)
    confidence: float = 1.0
    is_disputed: bool = False
    is_retracted: bool = False
    provenance_hash: str


# --- 5. Research Workspace & Execution ---

class ResearchQuestionRecord(BaseModel):
    question_id: str
    tenant_id: str
    project_id: str
    raw_query: str
    clinical_domain: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ResearchTaskRecord(BaseModel):
    task_id: str
    question_id: str
    task_type: str  # EVIDENCE_SYNTHESIS, CAUSAL_DISCOVERY, SIMULATION
    status: CanonicalStatus = CanonicalStatus.DRAFT
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ResearchSnapshotRecord(BaseModel):
    snapshot_id: str
    tenant_id: str
    task_id: str
    state_hash: str
    provenance_chain_root: str
    is_frozen: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# --- 6. Data Fabric & Scientific Compute ---

class DatasetRecord(BaseModel):
    dataset_id: str
    tenant_id: str
    project_id: str
    name: str
    format: str  # OMOP_CDM, FHIR_BUNDLE, SDTM, PARQUET, CSV
    classification: DataClassification = DataClassification.INTERNAL
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DatasetVersionRecord(BaseModel):
    version_id: str
    dataset_id: str
    version_tag: str  # v1.0.0
    row_count: int
    data_sha256: str
    storage_uri: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ComputationRecord(BaseModel):
    computation_id: str
    tenant_id: str
    runtime_environment: str  # python:3.11-scientific, r:4.3-bioconductor
    entrypoint_script: str
    input_dataset_version_id: str
    status: CanonicalStatus = CanonicalStatus.COMPLETED
    exit_code: int = 0
    duration_ms: int = 1500
    provenance_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# --- 7. AI Models & Agents ---

class ModelRecord(BaseModel):
    model_id: str
    name: str
    provider: str  # GEMINI, CLAUDE, OPENAI, LOCAL_VLLM
    context_window: int
    is_firewalled: bool = True
    active: bool = True


class AgentRecord(BaseModel):
    agent_id: str
    role_name: str
    allowed_tools: List[str] = Field(default_factory=list)
    max_budget_usd: float = 10.0
    max_steps: int = 50


class AgentRunRecord(BaseModel):
    run_id: str
    agent_id: str
    tenant_id: str
    task_id: str
    steps_executed: int = 0
    total_cost_usd: float = 0.0
    status: CanonicalStatus = CanonicalStatus.COMPLETED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
