-- ==============================================================================
-- ZMIE Core Relational & Vector Schema (PostgreSQL 16 + pgvector)
-- Complete 32-Table Enterprise Relational Foundation (Section 4)
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- ------------------------------------------------------------------------------
-- 1. SECURITY, ORGANIZATIONS & RBAC
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS organizations (
    org_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    org_type VARCHAR(64) NOT NULL, -- 'university', 'hospital', 'biotech', 'regulator', 'public'
    jurisdiction VARCHAR(64) DEFAULT 'Global',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(64) PRIMARY KEY,
    org_id VARCHAR(64) REFERENCES organizations(org_id) ON DELETE SET NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(32) NOT NULL DEFAULT 'researcher', -- 'public', 'researcher', 'clinician', 'admin'
    api_key VARCHAR(128) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS permissions (
    permission_id VARCHAR(64) PRIMARY KEY,
    role VARCHAR(32) NOT NULL,
    resource VARCHAR(64) NOT NULL,
    action VARCHAR(32) NOT NULL -- 'read', 'write', 'review', 'admin'
);

-- ------------------------------------------------------------------------------
-- 2. SOURCE REGISTRY & LICENSING (Tiers A-G & Class A/B/C)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sources (
    source_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    organization VARCHAR(255) NOT NULL,
    publisher VARCHAR(255),
    domain VARCHAR(255) NOT NULL,
    country VARCHAR(64) DEFAULT 'Global',
    jurisdiction VARCHAR(64) DEFAULT 'Global',
    source_type VARCHAR(64) NOT NULL,
    authority_class VARCHAR(32) NOT NULL, -- 'tier_a_official', 'tier_b_biomedical_repo', etc.
    status VARCHAR(32) NOT NULL DEFAULT 'recognized', -- 'authoritative', 'peer_reviewed', etc.
    license_class VARCHAR(32) NOT NULL, -- 'full_text_licensed', 'permitted_open_access', 'restricted_metadata_only'
    peer_review_status BOOLEAN DEFAULT TRUE,
    editorial_policy TEXT,
    retraction_status VARCHAR(32) DEFAULT 'clean',
    verification_method VARCHAR(64) DEFAULT 'domain_and_contract_audit',
    verification_status VARCHAR(32) DEFAULT 'verified',
    provenance_url TEXT,
    last_verified TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_licenses (
    license_id VARCHAR(64) PRIMARY KEY,
    source_id VARCHAR(64) REFERENCES sources(source_id) ON DELETE CASCADE,
    license_type VARCHAR(64) NOT NULL, -- 'cc_by_4_0', 'cc0', 'proprietary_contract', 'restricted'
    rights_holder VARCHAR(255) NOT NULL,
    full_text_storage_allowed BOOLEAN DEFAULT FALSE,
    analysis_allowed BOOLEAN DEFAULT TRUE,
    embedding_allowed BOOLEAN DEFAULT TRUE,
    redistribution_allowed BOOLEAN DEFAULT FALSE,
    commercial_use_allowed BOOLEAN DEFAULT FALSE,
    attribution_required BOOLEAN DEFAULT TRUE,
    restriction_notes TEXT,
    verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 3. DOCUMENTS, REPOSITORIES & LOCATIONS
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS documents (
    document_id VARCHAR(128) PRIMARY KEY,
    source_id VARCHAR(64) REFERENCES sources(source_id) ON DELETE CASCADE,
    doi VARCHAR(128),
    pmid VARCHAR(32),
    pmcid VARCHAR(32),
    title TEXT NOT NULL,
    authors TEXT[],
    publication_year INT,
    license_class VARCHAR(32) NOT NULL,
    raw_license VARCHAR(128),
    external_url TEXT,
    abstract TEXT,
    full_text_hash VARCHAR(64),
    is_retracted BOOLEAN DEFAULT FALSE,
    retraction_checked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS document_locations (
    location_id VARCHAR(64) PRIMARY KEY,
    document_id VARCHAR(128) REFERENCES documents(document_id) ON DELETE CASCADE,
    section_name VARCHAR(128),
    page_number INT,
    paragraph_number INT,
    anchor_text TEXT,
    hash VARCHAR(64)
);

-- ------------------------------------------------------------------------------
-- 4. ENTITIES, CONCEPTS & CROSS-SYSTEM ONTOLOGY
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities (
    entity_id VARCHAR(64) PRIMARY KEY,
    canonical_name VARCHAR(255) NOT NULL,
    category VARCHAR(64) NOT NULL, -- 'disease', 'drug', 'plant', 'pathway', 'target', 'phenotype'
    system VARCHAR(64) NOT NULL, -- 'modern_biomedicine', 'unani_tibb', 'ayurveda', 'tcm'
    definition TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS entity_aliases (
    alias_id VARCHAR(64) PRIMARY KEY,
    entity_id VARCHAR(64) REFERENCES entities(entity_id) ON DELETE CASCADE,
    alias_name VARCHAR(255) NOT NULL,
    language VARCHAR(32) DEFAULT 'en',
    is_preferred BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS concepts (
    concept_id VARCHAR(64) PRIMARY KEY,
    system VARCHAR(64) NOT NULL,
    canonical_name VARCHAR(255) NOT NULL,
    original_script_name VARCHAR(255),
    transliteration VARCHAR(255),
    category VARCHAR(64) NOT NULL,
    definition TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS concept_mappings (
    mapping_id VARCHAR(64) PRIMARY KEY,
    source_concept_id VARCHAR(64) REFERENCES concepts(concept_id) ON DELETE CASCADE,
    target_concept_id VARCHAR(64) REFERENCES concepts(concept_id) ON DELETE CASCADE,
    mapping_state VARCHAR(64) NOT NULL, -- 'exact_equivalence', 'functional_analogy', 'partial_overlap', etc.
    confidence_score FLOAT NOT NULL,
    epistemic_rationale TEXT NOT NULL,
    classical_citations TEXT[],
    expert_validated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 5. CLAIMS, EVIDENCE & PICO STUDY CONTEXT
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS claim_passports (
    claim_id VARCHAR(64) PRIMARY KEY,
    document_id VARCHAR(128) REFERENCES documents(document_id) ON DELETE CASCADE,
    source_id VARCHAR(64) REFERENCES sources(source_id) ON DELETE CASCADE,
    location_id VARCHAR(64) REFERENCES document_locations(location_id) ON DELETE SET NULL,
    claim_text TEXT NOT NULL,
    medical_system VARCHAR(64) NOT NULL,
    evidence_tier VARCHAR(64) NOT NULL,
    study_design VARCHAR(64),
    
    -- PICO Context
    population_species VARCHAR(64),
    condition_or_phenotype VARCHAR(255),
    intervention_agent VARCHAR(255),
    preparation_or_formulation VARCHAR(255),
    dose VARCHAR(128),
    duration VARCHAR(128),
    comparator VARCHAR(128),
    
    -- Verification & Governance
    entailment_score FLOAT DEFAULT 1.0,
    is_retracted BOOLEAN DEFAULT FALSE,
    is_superseded BOOLEAN DEFAULT FALSE,
    human_reviewed BOOLEAN DEFAULT FALSE,
    reviewer_id VARCHAR(64),
    
    -- Embeddings (pgvector 1536 dim)
    embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS studies (
    study_id VARCHAR(64) PRIMARY KEY,
    document_id VARCHAR(128) REFERENCES documents(document_id) ON DELETE CASCADE,
    study_design VARCHAR(64) NOT NULL,
    sample_size INT,
    population_description TEXT,
    primary_intervention TEXT,
    comparator TEXT,
    trial_registration_id VARCHAR(64) -- e.g. NCT01234567, CTRI/2021/...
);

CREATE TABLE IF NOT EXISTS study_outcomes (
    outcome_id VARCHAR(64) PRIMARY KEY,
    study_id VARCHAR(64) REFERENCES studies(study_id) ON DELETE CASCADE,
    endpoint_name VARCHAR(255) NOT NULL,
    direction VARCHAR(32) NOT NULL, -- 'increased', 'decreased', 'no_significant_change'
    effect_size VARCHAR(64),
    p_value VARCHAR(32),
    adverse_events_observed TEXT
);

-- ------------------------------------------------------------------------------
-- 6. RELATIONS & KNOWLEDGE GRAPH EDGES
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS relations (
    relation_id VARCHAR(64) PRIMARY KEY,
    source_entity_id VARCHAR(64) REFERENCES entities(entity_id) ON DELETE CASCADE,
    predicate VARCHAR(64) NOT NULL, -- 'TARGETS', 'AFFECTS', 'CAUSES', 'FUNCTIONALLY_ANALOGOUS_TO'
    target_entity_id VARCHAR(64) REFERENCES entities(entity_id) ON DELETE CASCADE,
    weight FLOAT DEFAULT 1.0,
    provenance_claim_id VARCHAR(64) REFERENCES claim_passports(claim_id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 7. CLINICAL SAFETY, GUIDELINES & INTERACTIONS
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS safety_alerts (
    alert_id VARCHAR(64) PRIMARY KEY,
    substance VARCHAR(255) NOT NULL,
    severity VARCHAR(32) NOT NULL, -- 'low', 'moderate', 'high', 'contraindicated'
    alert_type VARCHAR(64) NOT NULL, -- 'cyp450_interaction', 'pregnancy_contraindication', 'organ_toxicity'
    clinical_mechanism TEXT NOT NULL,
    clinical_action TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clinical_guidelines (
    guideline_id VARCHAR(64) PRIMARY KEY,
    issuing_body VARCHAR(255) NOT NULL, -- 'NICE', 'AHA', 'WHO', 'ICMR'
    condition VARCHAR(255) NOT NULL,
    recommendation_summary TEXT NOT NULL,
    evidence_class VARCHAR(32) NOT NULL,
    publication_year INT,
    superseded_by VARCHAR(64)
);

-- ------------------------------------------------------------------------------
-- 8. LIVING KNOWLEDGE VERSIONING & AUDIT TRAIL
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS knowledge_versions (
    version_id VARCHAR(64) PRIMARY KEY, -- e.g. 'K-2026.10.001'
    release_notes TEXT NOT NULL,
    released_by VARCHAR(64) REFERENCES users(user_id) ON DELETE SET NULL,
    total_claims_count INT,
    released_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS knowledge_changes (
    change_id VARCHAR(64) PRIMARY KEY,
    version_id VARCHAR(64) REFERENCES knowledge_versions(version_id) ON DELETE CASCADE,
    topic VARCHAR(255) NOT NULL,
    change_type VARCHAR(64) NOT NULL, -- 'new_rct', 'retraction', 'guideline_update'
    previous_state TEXT NOT NULL,
    new_state TEXT NOT NULL,
    delta_description TEXT NOT NULL,
    committed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS review_tasks (
    task_id VARCHAR(64) PRIMARY KEY,
    task_type VARCHAR(64) NOT NULL,
    target_object_id VARCHAR(64) NOT NULL,
    required_pool VARCHAR(64) NOT NULL,
    priority VARCHAR(32) DEFAULT 'routine',
    status VARCHAR(32) DEFAULT 'pending_review',
    ai_draft_payload TEXT NOT NULL,
    evidence_source_url TEXT,
    reviewer_notes TEXT,
    reviewer_id VARCHAR(64) REFERENCES users(user_id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS audit_events (
    event_id VARCHAR(64) PRIMARY KEY,
    actor_id VARCHAR(64) NOT NULL,
    action VARCHAR(64) NOT NULL,
    target_resource VARCHAR(255) NOT NULL,
    details JSONB,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 9. RESEARCH PROJECTS & WORKBENCH MEMORY
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS research_projects (
    project_id VARCHAR(64) PRIMARY KEY,
    owner_id VARCHAR(64) REFERENCES users(user_id) ON DELETE CASCADE,
    org_id VARCHAR(64) REFERENCES organizations(org_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    research_question TEXT NOT NULL,
    is_confidential BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS research_runs (
    run_id VARCHAR(64) PRIMARY KEY,
    project_id VARCHAR(64) REFERENCES research_projects(project_id) ON DELETE CASCADE,
    query_text TEXT NOT NULL,
    search_strategy JSONB,
    pico_matrix JSONB,
    contradictions JSONB,
    gaps_identified JSONB,
    synthesis_report TEXT,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS saved_searches (
    saved_search_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) REFERENCES users(user_id) ON DELETE CASCADE,
    query VARCHAR(255) NOT NULL,
    alert_frequency VARCHAR(32) DEFAULT 'weekly', -- 'real_time', 'daily', 'weekly', 'none'
    last_notified TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- INDEXES FOR LOW-LATENCY RETRIEVAL & FILTERING
-- ------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_documents_doi ON documents(doi);
CREATE INDEX IF NOT EXISTS idx_documents_pmid ON documents(pmid);
CREATE INDEX IF NOT EXISTS idx_claims_system ON claim_passports(medical_system);
CREATE INDEX IF NOT EXISTS idx_claims_condition ON claim_passports(condition_or_phenotype);
CREATE INDEX IF NOT EXISTS idx_claims_intervention ON claim_passports(intervention_agent);
CREATE INDEX IF NOT EXISTS idx_concepts_system ON concepts(system);
CREATE INDEX IF NOT EXISTS idx_concept_mappings_source ON concept_mappings(source_concept_id);
CREATE INDEX IF NOT EXISTS idx_concept_mappings_target ON concept_mappings(target_concept_id);
CREATE INDEX IF NOT EXISTS idx_relations_source ON relations(source_entity_id);
CREATE INDEX IF NOT EXISTS idx_relations_target ON relations(target_entity_id);
CREATE INDEX IF NOT EXISTS idx_safety_substance ON safety_alerts(substance);
CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_events(actor_id);
CREATE INDEX IF NOT EXISTS idx_research_runs_project ON research_runs(project_id);
