# ZMIE — Implementation Gap Report & Repository Audit

**Audit Date**: October 2026  
**Auditor**: ZMIE Principal Systems & Medical Knowledge Architect  
**Authority**: ZMIE Standalone Enterprise Master Blueprint (Sections 1–108)

---

## 1. Executive Audit Summary

A comprehensive line-by-line inspection of `/Users/irfanashraf/Downloads/zmie` was performed.

### Findings Breakdown
- **Existing & Operable**: The repository has clean Pydantic v2 schemas (`SourceRegistry`, `ClaimPassport`, `ConceptNode`), operational connectors (`OpenAlexConnector`, `EuropePMCConnector`, `AYUSHResearchConnector`), legal licensing classification (Class A/B/C), an AST-verified multi-router FastAPI backend (`/v1/*`), multi-stage Docker containerization, CI/CD workflow, client SDKs (Python & TypeScript), and an offline-runnable Tailwind workbench (`workbench.html`).
- **Partial / Hardcoded (P0/P1)**:
  1. `/v1/search` returns high-fidelity structured data, but the response was static/mock for the query `berberine` rather than dynamically orchestrating hybrid retrieval across ingested records, knowledge graph seeds, and live query parameters.
  2. `DeepResearchAgent` ran a deterministic 17-step pipeline rather than actively dispatching live requests across OpenAlex, Europe PMC, and the cross-system ontology.
  3. `database schema.sql` only had 3 tables (`sources`, `documents`, `claim_passports`), missing Section 4 enterprise tables: `organizations`, `users`, `roles`, `permissions`, `concepts`, `concept_mappings`, `relations`, `relation_evidence`, `studies`, `study_populations`, `guidelines`, `clinical_trials`, `safety_alerts`, `interactions`, `contraindications`, `research_projects`, `research_runs`, `audit_events`.
  4. Authentication & Authorization (RBAC, API Key validation, Tenant Isolation middleware) was stubbed.
  5. LLM Gateway fallback was mock-only; needs active local/API fallback reasoning logic and prompt templates.

---

## 2. Granular Gap Matrix

| Area | Current State | Required State (Blueprint) | Gap | Priority | Planned Action |
|---|---|---|---|---|---|
| **Database Schema** | 3 tables in `schema.sql` (`sources`, `documents`, `claim_passports`). | Complete 32-table relational DDL covering RBAC, studies, guidelines, safety, projects, and audits (Sec 4). | Missing 29 core enterprise relational tables. | **P0** | Expand `schema.sql` to full 32-table schema with constraints & indexes. |
| **Search Engine Retrieval** | Static response for berberine query in `app/api/v1/search.py`. | Dynamic multi-stage hybrid retrieval (Lexical + Semantic + Cross-System Graph + Evidence + Safety). | Hardcoded static search response. | **P0** | Implement dynamic `SearchService` querying entities, seed graph, live connectors, and safety engine. |
| **Deep Research Orchestrator** | Deterministic values for studies count and PICO. | Asynchronous, query-driven 17-step deep research orchestrator with step-by-step telemetry (Sec 22, 32). | Lacks dynamic query-to-PICO decomposition and live search planning. | **P0** | Upgrade `orchestrator.py` to dynamically execute OpenAlex/EuropePMC queries, extract PICO, and audit citations. |
| **Authentication & RBAC** | Open endpoints with dummy bearer checks in SDK. | Role-Based Access Control (`public`, `researcher`, `clinician`, `admin`) with API Key & JWT token verification (Sec 40, 65). | No active auth middleware or tenant isolation checks. | **P1** | Implement `SecurityService` with API Key and Bearer token dependency injection in FastAPI. |
| **Entity & Terminology Engine** | Static dictionary of 3 concepts (`diabetes`, `berberine`, `hypertension`). | Extensible terminology expansion across MeSH, SNOMED, ICD-11, Unani, Ayurveda, and TCM with 50+ mappings (Sec 10, 11, 14). | Limited terminology dictionary. | **P1** | Integrate `ClassicalCorpusBulkLoader` and comprehensive cross-tradition synonym normalizer. |
| **Document Processing & OCR** | Schema pointers for hash and sections exist; raw parser stubbed. | Multiformat parser adapter interface (PDF, TEI-XML, EPUB, TXT) with section and anchor preservation (Sec 9, 11). | Missing actual parser adapter for structural layout extraction. | **P1** | Implement `DocumentParserService` extracting title, abstract, sections, paragraphs, tables, and hash. |
| **Public Encyclopedia (`/medical/{topic}`)** | Not exposed as a distinct dynamic route in engine. | Dynamic endpoint `GET /v1/topics/{topic}` generating governed topic pages from knowledge objects (Sec 30, 45). | Missing `/v1/topics/*` encyclopedia endpoint. | **P2** | Add `/v1/topics/{topic}` to `search.py` or new `topics.py` router. |
| **Research Project Workspace** | Research runs exist; persistent project CRUD missing. | Persistent Research Project Object with queries, included/excluded studies, and notes (Sec 24, 34). | Missing `/v1/projects` CRUD endpoints. | **P2** | Implement project memory manager and router in `app/api/v1/research.py`. |
| **Observability & Metrics** | In-memory admin service. | Prometheus/OpenTelemetry compatible metrics for search latency, citation failures, and queue depth (Sec 51, 69). | Metrics not exposed as standard Prometheus endpoint. | **P2** | Add `/metrics` or structured latency recorder. |
| **Client Documentation & Specs** | `RUNBOOK.md` exists; gap report & specialized specs need formalization. | Full set of 15 architecture and model markdown specifications (Sec 55). | Missing formal standalone markdown specification documents. | **P3** | Author all 15 required documentation assets. |

---

## 3. Action Plan (Execution Order)

1. **Phase 1: Database & Relational Foundation** (P0): Complete `services/engine/app/db/schema.sql` with full 32-table DDL and foreign key relations.
2. **Phase 2: Dynamic Multi-Stage Search & Entity Resolution** (P0): Upgrade `SearchService` to dynamically resolve queries across Modern MeSH, Unani, Ayurveda, and TCM, computing dynamic evidence grades and citation networks.
3. **Phase 3: Dynamic Deep Research Engine & Project Workspace** (P0/P1): Connect `DeepResearchAgent` to live ingestion connectors, dynamic PICO extraction, and persistent project storage.
4. **Phase 4: Security, Authentication & Multi-Tenancy** (P1): Implement API key validation, RBAC (`public`, `researcher`, `clinician`, `admin`), and tenant isolation headers.
5. **Phase 5: Document Ingestion & Provenance Parsing** (P1): Implement `DocumentParserService` for XML/Text/JSON document structures with anchor preservation.
6. **Phase 6: Public Medical Encyclopedia & Dynamic Topics** (P2): Expose `/v1/topics/{topic}` generating governed knowledge pages.
7. **Phase 7: Full 15 Specification Documents & Acceptance Verification** (P3): Write the complete documentation suite and verify with updated automated test suites.
