# ZMIE Changelog

All notable changes to the **ZMIE (ZAYVORA Medical Intelligence Engine)** platform are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), adhering to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0-PROD-BUILD] - October 2026

### Added (Prompt 28: Build Execution & Code Generation)
- **Module 00 (Architecture & Foundation):** Normalized repository structure, `Makefile`, `CONTRIBUTING.md`, `ARCHITECTURE.md`, `SECURITY.md`, `LICENSE`, `CHANGELOG.md`, `.env.example`, and `docs/ZMIE_CURRENT_STATE_REPORT.md`.
- **Module 01 (Infrastructure):** Unified settings (`core/config.py`), enhanced `docker-compose.yml` with healthchecks, MinIO initialization, and developer bootstrap scripts.
- **Module 02 (Identity & Authentication):** Cryptographic JWT token manager, Argon2id password hashing, API credential validation, and enterprise SSO interfaces.
- **Module 03 & 04 (Tenancy & Authorization):** Formal Tenant -> Workspace -> Project hierarchy with ABAC policy engine and 4-way mandatory Tenant Isolation test suite (Clause 16).
- **Module 05, 06, 07 (Domain Models, Audit & Provenance):** Canonical domain entities, unified tamper-evident hash-chained audit dispatcher, and PROV-O provenance engine.

---

## [0.27.0] - October 2026

### Added (Prompt 27: Enterprise Production Build Specification)
- Production-grade Enterprise Specification Engine (`services/engine/app/enterprise_spec/engine.py`).
- 15 Architectural Decision Records (ADR-001 through ADR-015).
- 10 Core Architectural Invariants (INV-01 through INV-10).
- Production Relational Schema DDL (`services/engine/app/db/production_schema.sql`).
- REST API router (`/api/v1/spec/*`) mounted in API gateway.
- Python SDK namespace `client.spec` with 15 typed methods.
- 15/15 Enterprise Specification Acceptance Tests (`tests/test_production_build_acceptance.py`).

---

## [0.26.0] - October 2026

### Added (Prompt 26: Scientific Reproducibility & Research Audit System)
- Immutable Cryptographic Audit Ledger (`services/engine/app/audit/engine.py`).
- Deterministic Research Snapshot Engine with SHA-256 state freezing.
- Re-execution Verification Engine comparing baseline vs. re-run outputs.
- Retraction Impact Tracer with recursive downstream claim invalidation.
- 18/18 Acceptance Tests (`tests/test_research_audit_acceptance.py`).

---

## [0.25.0] - October 2026

### Added (Prompt 25: Scientific Knowledge Operating System - SKOS)
- Unified Answer Engine with 7-layer validation pipeline.
- Continuous Evidence Revalidation and Retraction listener.
- Full-stack developer showcase and SDK integration.

---

## [0.13.0 - 0.24.0] - October 2026

### Added (Specialized Intelligence Engines)
- **Prompt 24:** Scientific Agent Operating System with tool sandboxing and budget caps.
- **Prompt 23:** Federated & Private Research Intelligence with Differential Privacy.
- **Prompt 22:** Global Scientific Collaboration & Researcher Network.
- **Prompt 21:** Scientific Data Fabric & Computational Research Engine.
- **Prompt 20:** Global Medical Ontology & Terminology Evolution Engine.
- **Prompt 19:** Simulation, Hypothesis & In Silico Trial Engine.
- **Prompt 18:** Global Clinical & Regulatory Intelligence Engine.
- **Prompt 17:** Living Evidence Synthesis Suite (PICO + GRADE).
- **Prompt 16:** Medical Causal & Mechanistic Intelligence Suite.
- **Prompt 15:** Research Data Interoperability (FHIR + OMOP CDM + SDTM).
- **Prompt 14:** Global Research Discovery Network (OpenAlex, Europe PMC).
- **Prompt 13:** Global Medical Source Universe & Authority Tiers (A–G).

---

## [0.1.0 - 0.12.0] - Initial Platform Inception
- Core Hybrid Search Engine (BM25 + pgvector + Cypher).
- Cross-System Traditional Medicine Ontologies (Unani, Ayurveda, TCM).
- Atomic Claim Passports and Truth Firewall.
