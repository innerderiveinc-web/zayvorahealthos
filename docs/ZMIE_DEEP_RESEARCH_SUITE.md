# ZMIE Deep Research Operating Engine & Evidence Synthesis Documentation Suite

This document consolidates and formalizes the 15 enterprise architectural deliverables required under Prompt 6 of the ZAYVORA Medical Intelligence Engine™ (ZMIE) Standalone Enterprise Specification.

---

## 1. ZMIE_DEEP_RESEARCH_ARCHITECTURE.md
### Multi-Agent Operating Model
ZMIE's Deep Research Engine transitions from a simple conversational tool to a stateful, reproducible **Medical Research Operating Engine**.
- **Execution Pipeline**: `PLAN -> SEARCH -> SCREEN -> EXTRACT -> ASSESS -> CONTRADICT -> GAP -> SYNTHESIZE -> CITATION AUDIT -> REPORT`.
- **Isolation of Functions**: Subagents handle distinct stages with immutable input/output boundaries.
- **Reproducibility**: Every executed research job produces a SHA-256 reproducibility hash encompassing query terms, evidence IDs, contradiction mappings, and citation audits.

---

## 2. ZMIE_RESEARCH_AGENT_MODEL.md
### Specialized Subagents & Topology
1. **Planner Agent** (`ResearchPlannerAgent`): Responsible for query decomposition, PICO extraction, and inclusion/exclusion definition.
2. **Search & Retrieval Agent**: Queries cross-system sources (OpenAlex, Europe PMC, AYUSH, ClinicalTrials.gov) with evidence ladder prioritization.
3. **Screening Agent** (`ScreeningAndExtractionAgent`): Applies zero-tolerance integrity firewalls (quarantining retracted papers and commercial advertisements) and records transparent exclusion rationales.
4. **Extraction Agent**: Compiles standardized tabular evidence items capturing sample size, study design, effect sizes, and risk of bias.
5. **Contradiction Agent** (`SynthesisAndContradictionAgent`): Discovers divergent trial results and clusters them by root driver without forcing artificial consensus.
6. **Safety Agent** (`SafetyIntelligenceEngine`): Identifies herb-drug interactions, CYP450 competition, pregnancy contraindications, and organ toxicity alerts.
7. **Gap Analysis Agent**: Spots under-investigated populations, duration deficits, and formulation disparities.
8. **Synthesis Agent**: Crafts the integrated report while categorizing assertions by epistemic type.
9. **Citation Validator** (`CitationValidator`): Guarantees zero phantom citations by verifying exact textual entailment and paragraph anchors.

---

## 3. ZMIE_RESEARCH_PLANNER.md
### Plan-First Rule & PICO Formulation
Before retrieving or synthesizing literature, the system compiles a `ResearchPlan`:
- **Population (P)**: Specific diagnostic cohort, disease stage, or physiological phenotype.
- **Intervention (I)**: Active pharmaceutical ingredient, botanical extract, or classical preparation.
- **Comparator (C)**: Standard of care, placebo, or active pharmacological control.
- **Outcomes (O)**: Objective primary and secondary endpoints (biomarkers, mortality, symptom score).
- **Sub-Questions**: At least 4-5 focused investigative prompts targeting efficacy, mechanism, safety, contradiction, and traditional paradigms.
- **Search Matrix**: Formulated across MeSH, EMTREE, and classical traditional terms (Unani Mizaj, Ayurveda Dosha).

---

## 4. ZMIE_RESEARCH_WORKFLOW.md
### State Transitions & Checkpoints
- `DRAFT` $\rightarrow$ Initial initialization.
- `PLANNING` $\rightarrow$ Decomposing PICO and building the search matrix.
- `SEARCHING` $\rightarrow$ Gathering candidate literature from federated connectors.
- `SCREENING` $\rightarrow$ Applying inclusion and exclusion rules.
- `EXTRACTING` $\rightarrow$ Populating the structured Evidence Table.
- `ANALYZING` $\rightarrow$ Clustering trial divergences and evaluating pharmacovigilance.
- `SYNTHESIZING` $\rightarrow$ Draft narrative and grounded assertion categorization.
- `VALIDATING` $\rightarrow$ Entailment verification of all cited statements.
- `COMPLETED` $\rightarrow$ Report publication, checkpoint snapshot, and immutable audit seal.

---

## 5. ZMIE_EVIDENCE_SYNTHESIS.md
### Evidence Ladder Discipline & Grading
- Adheres strictly to the ZMIE Evidence Ladder ($E_0$ Guideline $\rightarrow$ $E_1$ Systematic Review $\rightarrow$ $E_2$ Controlled Trial $\rightarrow$ $E_3$ Observational Study $\rightarrow$ $E_4$ Preclinical $\rightarrow$ $E_5$ Canonical Traditional $\rightarrow$ $E_6$ Anecdotal).
- **Rule of Non-Promotion**: Multiple low-level studies ($E_4$) can never be accumulated to mimic or claim high-level clinical evidence ($E_1$ or $E_2$).
- Epistemic certainty is preserved across traditional systems without reducing complex humoral concepts to isolated receptor affinities.

---

## 6. ZMIE_CONTRADICTION_RESEARCH.md
### Disagreement Typology & Root Causes
When trials reach conflicting conclusions, the engine explicitly rejects "forced consensus":
- **Direct Outcome Divergence**: Differing primary endpoint results in similar cohorts.
- **Population-Specific Divergence**: Genetic polymorphisms (e.g., CYP2D6 metabolizers), dietary background, or baseline metabolic health.
- **Formulation & Extract Divergence**: Isolated alkaloid salts vs whole-plant hydroalcoholic extracts.
- **Dose & Duration Divergence**: Sub-therapeutic dosages or inadequate intervention windows.
- **Resolution Pathway**: For every contradiction cluster, the engine prescribes concrete trial protocols to resolve the ambiguity.

---

## 7. ZMIE_RESEARCH_GAP_ENGINE.md
### Clinical & Pharmacological Blindspots
Systematic identification of research deficits:
- **Trial Phase & Longitudinal Gaps**: Scarcity of hard endpoint cardiovascular outcomes trials (CVOTs).
- **Vulnerable Cohort Gaps**: Exclusion of chronic kidney disease (eGFR < 30) and elderly patients.
- **Formulation Standardization Gaps**: Inadequate pharmacokinetic bioequivalence between classical decoctions and standardized extracts.

---

## 8. ZMIE_HYPOTHESIS_ENGINE.md
### Next-Best-Research-Question & Study Design
Each detected gap automatically generates prioritized next research questions equipped with:
- Proposed study methodology (e.g., event-driven Phase III double-blind RCT, crossover PK study).
- Anticipated clinical impact and regulatory guideline relevance.
- Explicit rationale directly tied to the unaddressed gap identifier.

---

## 9. ZMIE_RESEARCH_MEMORY.md
### Snapshots, Checkpoints & Version Tracking
- Immutable `ResearchSnapshot` objects captured at milestone intervals or upon manual request.
- Preserves full state including plan, candidate screening logs, evidence tables, and compiled reports.
- Supports comparative delta tracking to visualize knowledge drift over time.

---

## 10. ZMIE_RESEARCH_REPRODUCIBILITY.md
### Audit Trail & Cryptographic Anchoring
- Every research execution generates an immutable SHA-256 hash.
- Hash computation takes into account the question text, active evidence IDs, contradiction topology, and timestamp.
- Allows external auditors and regulatory reviewers to verify that the report has not been tampered with or modified post-synthesis.

---

## 11. ZMIE_RESEARCH_REPORT_SPEC.md
### Report Data Structure & Grounded Assertions
Reports strictly decouple:
- `FACT`: Direct statements backed by cited human trials.
- `SYNTHESIS`: High-level aggregated meta-findings.
- `INFERENCE`: Mechanistic or biochemical deductions downstream of observed facts.
- `HYPOTHESIS`: Unproven translational conjectures requiring prospective validation.

---

## 12. ZMIE_RESEARCH_API.md
### REST Endpoints Reference
- `POST /v1/research/jobs`: Initiates research job and generates pre-flight plan.
- `GET /v1/research/jobs`: Lists all research jobs.
- `GET /v1/research/{job_id}`: Retrieves job metadata and current lifecycle state.
- `GET /v1/research/{job_id}/plan`: Returns decomposed PICO, criteria, and search matrix.
- `GET /v1/research/{job_id}/evidence`: Returns structured Evidence Table.
- `GET /v1/research/{job_id}/conflicts`: Returns contradiction clusters and root causes.
- `GET /v1/research/{job_id}/gaps`: Returns identified research gaps and next-best questions.
- `GET /v1/research/{job_id}/report`: Returns full synthesized evidence report.
- `POST /v1/research/{job_id}/snapshot`: Captures immutable checkpoint snapshot.
- `POST /v1/research/{job_id}/diff`: Computes structured differences between two snapshots.

---

## 13. ZMIE_RESEARCH_SECURITY.md
### Provenance & Anti-Fabrication Safeguards
- Zero Citation Laundering Guarantee: Citations cannot be synthesized or guessed.
- Real-time screening removes retracted publications and unverified commercial literature.
- Safety Intelligence Engine audits all proposed compounds against drug interaction databases.

---

## 14. ZMIE_RESEARCH_EVALUATION.md
### Quality Benchmarks & Testing
- Automated unit and acceptance test suites (`test_deep_research_acceptance.py`).
- 100% pass rate across test suites verifying planning, screening, contradiction discovery, and API routes.
- Continuous regression testing against all prior system prompts.

---

## 15. ZMIE_RESEARCH_OPERATIONS.md
### Deployment, Caching & Scaling
- Asynchronous FastAPI execution with stateful job store.
- Designed for horizontal scaling across worker nodes.
- Compatible with Redis task queues and PostgreSQL persistent backends.
