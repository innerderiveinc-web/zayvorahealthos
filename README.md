# ZMIE — ZAYVORA Medical Intelligence Engine™
### Enterprise Scientific Knowledge Operating System for Medicine & Life Sciences

[![License](https://img.shields.io/badge/License-Apache_2.0_with_Healthcare_Rider-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal.svg)](https://fastapi.tiangolo.com)
[![Tests](https://img.shields.io/badge/Tests-501%20Passing-success.svg)](tests/)
[![Architecture](https://img.shields.io/badge/Release-v1.0.0--PROD-teal.svg)](docs/ZMIE_CANONICAL_ARCHITECTURE_V1.md)
[![Validation](https://img.shields.io/badge/Benchmark-100%25%20GO-brightgreen.svg)](docs/ZMIE_REAL_IMPLEMENTATION_AND_OPERATIONS_REPORT.md)

---

## Overview

**ZMIE** is a standalone, enterprise-grade, API-first scientific and medical knowledge infrastructure platform. It transforms the medical research paradigm from passive literature search into an active, verifiable, and reproducible **Scientific Knowledge Operating System (SKOS)**.

ZMIE natively unifies:
1. **Global Source Universe:** Continuous ingestion across PubMed, OpenAlex, Europe PMC, ClinicalTrials.gov, and classical polyglot medical corpora (Unani, Ayurveda, TCM, Sanskrit, Arabic, Urdu, Persian, Latin).
2. **Atomic Claim Passports:** Every factual proposition is anchored to immutable source spans, confidence intervals, GRADE certainty ratings, and contradiction vectors.
3. **Reproducible Research Compute:** Sandboxed execution kernels, protocol DAGs, and deterministic research snapshots capable of historical bit-for-bit replay.
4. **Living Evidence Synthesis:** Automated PICO extraction, dynamic meta-analyses, and automated retraction invalidation cascades.
5. **Privacy-Preserving Federated Intelligence:** Multi-institutional research networks governed by formal \((\varepsilon, \delta)\)-differential privacy and Zero-Trust tenant boundaries.

---

## Master Quickstart (One-Command Production CLI)

ZMIE provides a turnkey single-command executable CLI (`./zmie`):

```bash
# 1. Start Engine & Open Interactive Web Workbench UI in Browser
./zmie serve

# 2. Run Commercial Demonstration (Universities, AYUSH, Investors)
./zmie demo

# 3. Run Complete Automated Test Suite (501 tests)
./zmie test

# 4. Run 12 Golden Benchmark Batteries (Outputs SHA-256 Certificate)
./zmie benchmark

# 5. Inspect Engine Health, Invariants & Cryptographic Audit
./zmie status
./zmie audit
```

### Key Make Targets

| Target | Description |
|:---|:---|
| `make dev` | Complete local developer environment bootstrap |
| `make dev-up` | Launch Docker Compose backing services in background |
| `make dev-down` | Stop all local containers and prune temporary networks |
| `make test` | Execute complete test suite (288+ tests) |
| `make test-acceptance` | Run Prompt 26 & Prompt 27 acceptance test suites |
| `make lint` | Run flake8 / ruff linter |
| `make typecheck` | Run mypy type analysis |
| `make verify-all` | Run lint, typecheck, unit tests, and acceptance gates |
| `make showcase` | Execute the end-to-end Python SDK production showcase |

---

## Architecture & Directory Layout

```text
zmie/
├── Makefile                                # Monorepo build and automation orchestrator
├── LICENSE                                 # Apache 2.0 with Scientific Integrity Rider
├── README.md                               # System overview & developer guide
├── CONTRIBUTING.md                         # Contribution workflows & PR templates
├── ARCHITECTURE.md                         # Deep architecture & invariant documentation
├── SECURITY.md                             # Threat model, HIPAA/GDPR & disclosure
├── CHANGELOG.md                            # Versioned history across Prompts 1-28
├── .env.example                            # Enterprise environment variables
├── docker-compose.yml                      # Backing services orchestration
│
├── docs/                                   # Enterprise Specifications & ADRs
│   ├── ZMIE_ENTERPRISE_PRODUCTION_BUILD_SPECIFICATION.md
│   ├── ZMIE_CURRENT_STATE_REPORT.md
│   └── ... (Subsystem Architecture Specs)
│
├── sdk/
│   └── python/                             # Official Python SDK (`zmie`)
│       ├── zmie/client.py                  # Typed ZMIEClient
│       └── pyproject.toml
│
├── services/
│   ├── engine/                             # Core FastAPI Backend & Intelligence Services
│   │   ├── app/
│   │   │   ├── main.py                     # API Gateway & Route Registry
│   │   │   ├── core/                       # Identity, Tenancy, RBAC/ABAC, Audit
│   │   │   ├── models/                     # Canonical domain models
│   │   │   ├── db/                         # PostgreSQL DDL, migrations, Neo4j
│   │   │   ├── api/v1/                     # REST API route handlers
│   │   │   ├── sources/                    # Source Registry & Authority Tiers
│   │   │   ├── ingestion/                  # 12-stage Ingestion Pipeline
│   │   │   ├── ontology/                   # Cross-System Ontologies (Unani/Ayurveda/Biomed)
│   │   │   ├── graph/                      # Knowledge, Evidence & Safety Graphs
│   │   │   ├── search/                     # Hybrid BM25 + Vector + Graph search
│   │   │   ├── rwe/                        # FHIR & OMOP CDM v5.4 Harmonizer
│   │   │   ├── causal_mechanistic/         # Causal DAGs & Target Modulation
│   │   │   ├── living_evidence/            # PICO Extraction & Synthesis
│   │   │   ├── clinical_regulatory/        # Regulatory Guidance (FDA, EMA, CDSCO)
│   │   │   ├── simulation_hypothesis/      # In Silico Trials & Simulation
│   │   │   ├── scientific_compute/         # Sandbox Execution & Protocol DAGs
│   │   │   ├── collaboration_network/      # Global Co-authorship & COI Engine
│   │   │   ├── federated_privacy/          # Differential Privacy & Tenant Enclaves
│   │   │   ├── agent_os/                   # Scientific Agent OS Runtime
│   │   │   ├── skos/                       # Unified Answer & Revalidation Engine
│   │   │   ├── audit/                      # Hash-Chained Audit Ledger
│   │   │   └── enterprise_spec/            # Specification Engine & ADRs
│   │   └── pyproject.toml
│   └── web/                                # Next.js 15 Web Workbench
└── tests/                                  # 288+ Automated Verification Tests
```

---

## Core Invariants

1. **Zero Fabrication (INV-01):** Absence of evidence yields `UNKNOWN` or `NO_EVIDENCE`. Plausible synthetic citations are strictly prohibited.
2. **Tenant Boundary Isolation (INV-02):** Cryptographically enforced separation across all tenant datasets, agent memory, and cache tiers.
3. **Tamper-Evident Audit Trails (INV-05):** Every research query and computational mutation produces a SHA-256 hash-chained block.
4. **Epistemic Distance Preservation (INV-04):** Traditional systems and modern molecular targets interact across explicit epistemic bridge vectors rather than lossy 1:1 equivalencies.

---

## Enterprise Specification & Verification

To verify the enterprise specification and production readiness:

```bash
# Run the enterprise specification test suite (15 tests)
.venv/bin/python3 -m unittest tests/test_production_build_acceptance.py

# Run the reproducibility and research audit test suite (18 tests)
.venv/bin/python3 -m unittest tests/test_research_audit_acceptance.py

# Run the full end-to-end production showcase
.venv/bin/python3 tests/production_build_showcase.py
```
