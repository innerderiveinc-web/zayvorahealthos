-- ==============================================================================
-- ZMIE — ZAYVORA Medical Intelligence Engine™
-- Production Database Relational Schema (PostgreSQL 16+)
-- Prompt 27 Enterprise Build Specification (Clauses 9, 10, 11, 40)
-- ==============================================================================

-- 1. EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- ==============================================================================
-- 2. CORE IDENTITY & MULTI-TENANCY SCHEMAS
-- ==============================================================================

CREATE TABLE IF NOT EXISTS tenants (
    tenant_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tier VARCHAR(64) DEFAULT 'ENTERPRISE',
    data_residency_region VARCHAR(64) DEFAULT 'us-east-1',
    is_active BOOLEAN DEFAULT TRUE,
    settings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS organizations (
    org_id VARCHAR(64) PRIMARY KEY,
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    org_type VARCHAR(64) DEFAULT 'HOSPITAL', -- HOSPITAL, UNIVERSITY, PHARMA, RESEARCH_INSTITUTE
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workspaces (
    workspace_id VARCHAR(64) PRIMARY KEY,
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    org_id VARCHAR(64) REFERENCES organizations(org_id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    classification VARCHAR(64) DEFAULT 'CONFIDENTIAL',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(64) PRIMARY KEY,
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(64) DEFAULT 'RESEARCHER',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS roles (
    role_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL,
    permissions JSONB DEFAULT '[]'::jsonb,
    description TEXT
);

CREATE TABLE IF NOT EXISTS user_roles (
    user_id VARCHAR(64) REFERENCES users(user_id) ON DELETE CASCADE,
    role_id VARCHAR(64) REFERENCES roles(role_id) ON DELETE CASCADE,
    assigned_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id)
);

-- ==============================================================================
-- 3. GLOBAL SOURCE UNIVERSE & INGESTION
-- ==============================================================================

CREATE TABLE IF NOT EXISTS sources (
    source_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    source_class VARCHAR(64) NOT NULL, -- BIOMEDICAL, TRADITIONAL, REGULATORY, CLINICAL_TRIALS
    base_url TEXT,
    license_type VARCHAR(128) DEFAULT 'OPEN_ACCESS',
    reliability_score DOUBLE PRECISION DEFAULT 1.0,
    status VARCHAR(64) DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_versions (
    source_version_id VARCHAR(64) PRIMARY KEY,
    source_id VARCHAR(64) NOT NULL REFERENCES sources(source_id) ON DELETE CASCADE,
    version_tag VARCHAR(64) NOT NULL,
    snapshot_uri TEXT,
    checksum VARCHAR(128) NOT NULL,
    ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS documents (
    document_id VARCHAR(64) PRIMARY KEY,
    source_id VARCHAR(64) NOT NULL REFERENCES sources(source_id) ON DELETE CASCADE,
    source_version_id VARCHAR(64) REFERENCES source_versions(source_version_id),
    external_id VARCHAR(255), -- DOI, PMID, ClinicalTrialID
    title TEXT NOT NULL,
    authors JSONB DEFAULT '[]'::jsonb,
    abstract TEXT,
    publication_date DATE,
    language VARCHAR(16) DEFAULT 'en',
    storage_path TEXT,
    sha256_hash VARCHAR(64) NOT NULL,
    status VARCHAR(64) DEFAULT 'INDEXED',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ingestion_jobs (
    job_id VARCHAR(64) PRIMARY KEY,
    source_id VARCHAR(64) NOT NULL REFERENCES sources(source_id),
    status VARCHAR(64) DEFAULT 'RUNNING',
    items_processed INT DEFAULT 0,
    errors_count INT DEFAULT 0,
    started_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ
);

-- ==============================================================================
-- 4. MEDICAL ONTOLOGY & TERMINOLOGY EVOLUTION
-- ==============================================================================

CREATE TABLE IF NOT EXISTS ontologies (
    ontology_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    paradigm VARCHAR(64) NOT NULL, -- MODERN, UNANI, AYURVEDA, TCM
    version VARCHAR(64) NOT NULL,
    release_date DATE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS terms (
    term_id VARCHAR(64) PRIMARY KEY,
    ontology_id VARCHAR(64) NOT NULL REFERENCES ontologies(ontology_id),
    original_text TEXT NOT NULL,
    script VARCHAR(64) DEFAULT 'Latin',
    transliteration TEXT,
    language VARCHAR(16) DEFAULT 'en',
    historical_era VARCHAR(64) DEFAULT 'CONTEMPORARY',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS concepts (
    concept_id VARCHAR(64) PRIMARY KEY,
    ontology_id VARCHAR(64) NOT NULL REFERENCES ontologies(ontology_id),
    canonical_name VARCHAR(255) NOT NULL,
    definition TEXT,
    epistemic_state VARCHAR(64) DEFAULT 'ACCEPTED',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS concept_mappings (
    mapping_id VARCHAR(64) PRIMARY KEY,
    source_concept_id VARCHAR(64) NOT NULL REFERENCES concepts(concept_id),
    target_concept_id VARCHAR(64) NOT NULL REFERENCES concepts(concept_id),
    mapping_type VARCHAR(64) NOT NULL, -- EXACT_MATCH, BROAD_MATCH, NARROW_MATCH, PARADIGM_ANALOGUE, NO_EQUIVALENT
    confidence_score DOUBLE PRECISION DEFAULT 1.0,
    justification TEXT,
    reviewed_by VARCHAR(64),
    status VARCHAR(64) DEFAULT 'APPROVED',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- 5. EVIDENCE, CLAIMS & CONTRADICTIONS
-- ==============================================================================

CREATE TABLE IF NOT EXISTS evidence_bundles (
    bundle_id VARCHAR(64) PRIMARY KEY,
    tenant_id VARCHAR(64) REFERENCES tenants(tenant_id),
    research_question TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evidence_items (
    evidence_id VARCHAR(64) PRIMARY KEY,
    document_id VARCHAR(64) REFERENCES documents(document_id),
    study_design VARCHAR(64) NOT NULL, -- RCT, COHORT, CASE_CONTROL, META_ANALYSIS, IN_VITRO
    sample_size INT,
    population TEXT,
    intervention TEXT,
    comparator TEXT,
    outcome TEXT,
    effect_size DOUBLE PRECISION,
    ci_lower DOUBLE PRECISION,
    ci_upper DOUBLE PRECISION,
    p_value DOUBLE PRECISION,
    risk_of_bias VARCHAR(64) DEFAULT 'LOW',
    certainty_grade VARCHAR(64) DEFAULT 'MODERATE',
    source_location TEXT, -- Page/Table reference
    extracted_by VARCHAR(64) NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS claims (
    claim_id VARCHAR(64) PRIMARY KEY,
    tenant_id VARCHAR(64) REFERENCES tenants(tenant_id),
    statement TEXT NOT NULL,
    subject VARCHAR(255) NOT NULL,
    predicate VARCHAR(255) NOT NULL,
    object VARCHAR(255) NOT NULL,
    modality VARCHAR(64) NOT NULL, -- OBSERVED, REPORTED, SUPPORTED, INFERRED, ASSOCIATED, PREDICTED, UNKNOWN, CONTESTED
    strength VARCHAR(64) DEFAULT 'MODERATE',
    status VARCHAR(64) DEFAULT 'ACTIVE',
    version INT DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS claim_evidence_links (
    claim_id VARCHAR(64) REFERENCES claims(claim_id) ON DELETE CASCADE,
    evidence_id VARCHAR(64) REFERENCES evidence_items(evidence_id) ON DELETE CASCADE,
    link_type VARCHAR(64) DEFAULT 'SUPPORTS', -- SUPPORTS, REFUTES, CONTEXTUALIZES
    PRIMARY KEY (claim_id, evidence_id)
);

CREATE TABLE IF NOT EXISTS contradictions (
    contradiction_id VARCHAR(64) PRIMARY KEY,
    claim_a_id VARCHAR(64) NOT NULL REFERENCES claims(claim_id),
    claim_b_id VARCHAR(64) NOT NULL REFERENCES claims(claim_id),
    conflict_type VARCHAR(64) NOT NULL, -- DIRECT_OPPOSING, POPULATION_VARIANCE, DOSAGE_CONFLICT
    detected_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    resolution_status VARCHAR(64) DEFAULT 'UNRESOLVED',
    resolution_rationale TEXT
);

-- ==============================================================================
-- 6. RESEARCH SNAPSHOTS, COMPUTATIONAL PROVENANCE & AUDIT
-- ==============================================================================

CREATE TABLE IF NOT EXISTS research_snapshots (
    snapshot_id VARCHAR(64) PRIMARY KEY,
    tenant_id VARCHAR(64) REFERENCES tenants(tenant_id),
    project_id VARCHAR(64) DEFAULT 'proj-default',
    version VARCHAR(32) NOT NULL DEFAULT '1.0.0',
    parent_snapshot_id VARCHAR(64) REFERENCES research_snapshots(snapshot_id),
    research_question TEXT NOT NULL,
    question_version VARCHAR(16) DEFAULT '1.0',
    manifest_hash VARCHAR(128) NOT NULL,
    workflow_id VARCHAR(64) NOT NULL,
    environment JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_locked BOOLEAN DEFAULT TRUE,
    status VARCHAR(64) DEFAULT 'COMPLETED',
    final_output JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_by VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS compute_jobs (
    job_id VARCHAR(64) PRIMARY KEY,
    tenant_id VARCHAR(64) REFERENCES tenants(tenant_id),
    project_id VARCHAR(64),
    script_path TEXT NOT NULL,
    code_checksum VARCHAR(128) NOT NULL,
    random_seed INT DEFAULT 42,
    is_deterministic BOOLEAN DEFAULT TRUE,
    resources_allocated JSONB DEFAULT '{"cpus": 2, "memory_gb": 4}'::jsonb,
    status VARCHAR(64) DEFAULT 'QUEUED',
    execution_time_ms INT,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS audit_events (
    event_id VARCHAR(64) PRIMARY KEY,
    audit_id VARCHAR(64) NOT NULL,
    tenant_id VARCHAR(64) REFERENCES tenants(tenant_id),
    actor_type VARCHAR(32) NOT NULL, -- HUMAN, AGENT, SERVICE
    actor_id VARCHAR(64) NOT NULL,
    action VARCHAR(64) NOT NULL,
    resource_type VARCHAR(64) NOT NULL,
    resource_id VARCHAR(64) NOT NULL,
    before_state JSONB,
    after_state JSONB,
    reason TEXT,
    previous_event_hash VARCHAR(128) NOT NULL,
    event_hash VARCHAR(128) NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS research_audits (
    audit_id VARCHAR(64) PRIMARY KEY,
    snapshot_id VARCHAR(64) NOT NULL REFERENCES research_snapshots(snapshot_id),
    tenant_id VARCHAR(64) REFERENCES tenants(tenant_id),
    researcher VARCHAR(255) NOT NULL,
    study_name VARCHAR(255) NOT NULL,
    question TEXT NOT NULL,
    status VARCHAR(64) DEFAULT 'VALID',
    verification_passed BOOLEAN DEFAULT TRUE,
    reproducibility_status VARCHAR(64) DEFAULT 'REPRODUCED',
    is_held BOOLEAN DEFAULT FALSE, -- Legal preservation hold
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- 7. EVENT OUTBOX PATTERN (Clause 40)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS event_outbox (
    outbox_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id VARCHAR(64) NOT NULL,
    event_type VARCHAR(128) NOT NULL,
    version VARCHAR(16) DEFAULT '1.0',
    tenant_id VARCHAR(64) REFERENCES tenants(tenant_id),
    actor VARCHAR(64) NOT NULL,
    correlation_id VARCHAR(64),
    causation_id VARCHAR(64),
    payload JSONB NOT NULL,
    provenance JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(32) DEFAULT 'PENDING', -- PENDING, PUBLISHED, FAILED
    retry_count INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMPTZ
);

-- ==============================================================================
-- 8. INDEXES & CONSTRAINTS
-- ==============================================================================

CREATE INDEX IF NOT EXISTS idx_users_tenant ON users(tenant_id);
CREATE INDEX IF NOT EXISTS idx_documents_source ON documents(source_id);
CREATE INDEX IF NOT EXISTS idx_documents_hash ON documents(sha256_hash);
CREATE INDEX IF NOT EXISTS idx_claims_tenant ON claims(tenant_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_tenant ON research_snapshots(tenant_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_parent ON research_snapshots(parent_snapshot_id);
CREATE INDEX IF NOT EXISTS idx_audit_chain ON audit_events(audit_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_outbox_pending ON event_outbox(status, created_at) WHERE status = 'PENDING';

-- ==============================================================================
-- 9. ROW-LEVEL SECURITY (RLS) POLICIES (Clause 11)
-- ==============================================================================

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE workspaces ENABLE ROW LEVEL SECURITY;
ALTER TABLE claims ENABLE ROW LEVEL SECURITY;
ALTER TABLE research_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE compute_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_events ENABLE ROW LEVEL SECURITY;

-- Dynamic Tenant Context Policy Example:
-- CREATE POLICY tenant_isolation_policy ON research_snapshots
--     FOR ALL
--     USING (tenant_id = current_setting('app.current_tenant_id', true));
