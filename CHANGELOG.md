# ZMIE Changelog

All notable changes to the **ZMIE (ZAYVORA Medical Intelligence Engine)** platform are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), adhering to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0-PROD] - October 2026

### Added (Production Build & Architectural Hardening)
- **Foundation & Standards:** Normalized repository structure, `Makefile`, `CONTRIBUTING.md`, `ARCHITECTURE.md`, `SECURITY.md`, `LICENSE`, `CHANGELOG.md`, `.env.example`, and canonical architecture specifications.
- **Infrastructure:** Unified configuration (`core/config.py`), production `docker-compose.yml` with healthchecks, MinIO initialization, and developer bootstrap scripts.
- **Identity & Authentication:** Cryptographic JWT token manager, Argon2id password hashing, API credential validation, and enterprise SSO interfaces.
- **Tenancy & Authorization:** Formal Tenant -> Workspace -> Project hierarchy with ABAC policy engine and 4-way mandatory Tenant Isolation test suite (Clause 16).
- **Domain Models, Audit & Provenance:** Canonical domain entities, unified tamper-evident hash-chained audit dispatcher, and PROV-O provenance engine.
- **Agentic Operating Pipeline:** Closed-loop Reflection & Critic auto-repair engine, ReAct multi-hop tool loop, SQLite state persistence, and Adversarial Debate consensus engine.

---

## [0.9.0] - October 2026

### Added (Enterprise Specification Engine & Invariants)
- Production-grade Enterprise Specification Engine (`services/engine/app/enterprise_spec/engine.py`).
- 15 Architectural Decision Records (ADR-001 through ADR-015).
- 10 Core Architectural Invariants (INV-01 through INV-10).
- Production Relational Schema DDL (`services/engine/app/db/production_schema.sql`).
- REST API router (`/api/v1/spec/*`) mounted in API gateway.
- Python SDK namespace `client.spec` with 15 typed methods.
- Enterprise Specification Acceptance Tests (`tests/test_production_build_acceptance.py`).

---

## [0.8.0] - October 2026

### Added (Scientific Reproducibility & Research Audit System)
- Immutable Cryptographic Audit Ledger (`services/engine/app/audit/engine.py`).
- Deterministic Research Snapshot Engine with SHA-256 state freezing.
- Re-execution Verification Engine comparing baseline vs. re-run outputs.
- Retraction Impact Tracer with recursive downstream claim invalidation.
- Research Audit Acceptance Tests (`tests/test_research_audit_acceptance.py`).

---

## [0.7.0] - October 2026

### Added (Scientific Knowledge Operating System - SKOS)
- Unified Answer Engine with 7-layer validation pipeline.
- Continuous Evidence Revalidation and Retraction listener.
- Full-stack developer showcase and SDK integration.

---

## [0.3.0 - 0.6.0] - October 2026

### Added (Specialized Intelligence Engines)
- **Scientific Agent OS:** Sandboxed execution kernels with budget limits and tool capabilities.
- **Federated Privacy Engine:** Multi-institutional differential privacy \((\varepsilon, \delta)\) and zero-knowledge enclaves.
- **Scientific Collaboration Network:** Global co-authorship tracking, COI detection, and author authority scoring.
- **Computational Data Fabric:** Sandboxed code execution and deterministic scientific computing kernels.
- **Ontology Evolution Engine:** Cross-system semantic mapping (Unani, Ayurveda, Biomedicine) with epistemic preservation.
- **In Silico Trial Simulator:** Mechanistic hypothesis generation and simulated clinical endpoints.
- **Regulatory Intelligence:** CDSCO, FDA, and EMA harmonized guidance engines.
- **Living Evidence Synthesis:** Automated PICO deconstruction and GRADE certainty appraisal.
- **Causal Mechanistic Intelligence:** Direct DAG causal inferences and target modulation analysis.
- **Data Interoperability:** HL7 FHIR R5 and OMOP CDM v5.4 clinical harmonizer.
- **Global Medical Source Universe:** Continuous ingestion across PubMed, Europe PMC, and ClinicalTrials.gov.

---

## [0.1.0 - 0.2.0] - Initial Platform Inception
- Core Hybrid Search Engine (BM25 + pgvector + Cypher).
- Cross-System Traditional Medicine Ontologies (Unani, Ayurveda, TCM).
- Atomic Claim Passports and Truth Firewall.
