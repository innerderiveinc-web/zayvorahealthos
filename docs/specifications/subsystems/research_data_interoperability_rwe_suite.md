# ZMIE — RESEARCH DATA INTEROPERABILITY & REAL-WORLD EVIDENCE (RWE) ENGINE
## Master Production Architectural Blueprint, Multi-Standard Crosswalk & Observational Evidence Governance
### Prompt 15 Master Implementation Specification (Clauses 1–275)

---

### 1. Executive Summary & Core Philosophy

The **ZMIE Research Data Interoperability & Real-World Evidence (RWE) Engine** is the scientific data infrastructure layer that bridges published medical literature with properly governed, authorized, privacy-preserving structured research data and real-world health records.

```text
Healthcare Data / Clinical Trials / Laboratory / Claims / Wearables / Registries / Traditional Systems
                                              │
                                              ▼
                                   [INGESTION & DATA CONTRACT]
                                              │
                                              ▼
                               [FOUR-TIER SOURCE PRESERVATION]
                         RAW ──► NORMALIZED ──► STANDARDIZED ──► ANALYTIC
                                              │
                                              ▼
                         [9-DIMENSION DATA QUALITY & FITNESS GATE]
                                              │
                                              ▼
                            [MULTI-STANDARD INTEROPERABILITY]
               ┌──────────────────────────────┼──────────────────────────────┐
               ▼                              ▼                              ▼
        [HL7 FHIR R4/R5]            [OHDSI OMOP CDM v5.4/v5.5]      [CDISC SDTM v1.7 / ADaM]
               └──────────────────────────────┬──────────────────────────────┘
                                              ▼
                        [MULTI-SYSTEM TRADITIONAL CLINICAL RECORDS]
                        - NAMASTE Portal Morbidity Terminologies
                        - WHO ICD-11 Traditional Medicine Module 2 (TM2)
                        - Unani Mizaj & Su-e-Mizaj Clinical Diagnostics
                        - Ayurvedic Prakriti & Vikriti Doshic Profiles
                                              │
                                              ▼
                     [TARGET TRIAL EMULATION (TTE) & CAUSAL DAGs]
                     - Explicit Time Zero (New-User Active-Comparator)
                     - Confounding by Indication Control (IPTW / PS Matching)
                     - Directed Acyclic Graphs (DAGs) & Negative Controls
                                              │
                                              ▼
                        [FEDERATED CLEAN ROOM & PRIVACY CONTROLS]
                        - HMAC Tokenization (research_subject_id)
                        - Small-Cell Suppression (< 5 subjects obscured)
                                              │
                                              ▼
                        [CAUSALITY & OVERSTATEMENT FIREWALL]
                        - Association ≠ Causation
                        - Prediction ≠ Treatment Effect
                        - RWD ≠ RWE | RWE ≠ Double-Blind RCT
                                              │
                                              ▼
                       [EVIDENCE GRAPH BRIDGE & RCT TRIANGULATION]
                        - Tier E5 Human Observational Real-World Evidence
                        - Cryptographic Provenance Hash (SHA-256)
                        - Triangulation against Landmark Phase 3 RCTs
```

---

### 2. The 15 Non-Negotiable Core Axioms

1. **$RWD \ne RWE$**: Real-world data becomes real-world evidence only through an explicit research design, rigorous data-quality assessment, and scientific interpretation.
2. **$RWE \ne \text{Randomized Trial Evidence}$**: Observational findings are locked at Evidence Ladder Tier **$E_5$** and must never be conflated with or elevated to double-blind RCT ($E_6$) status.
3. **$\text{Association} \ne \text{Causation}$**: Observational correlations are never phrased as "causes" or "cures" without explicit Target Trial Emulation (TTE) and sensitivity testing.
4. **$\text{Prediction} \ne \text{Treatment Effect}$**: Predictive models cannot automatically establish causal therapeutic effectiveness.
5. **Large Dataset $\ne$ High-Quality Evidence**: Millions of uncurated EHR records do not substitute for rigorous phenotyping and bias control.
6. **More Records $\ne$ More Scientific Validity**: Power does not resolve systematic selection bias or confounding by indication.
7. **Hospital Data $\ne$ Globally Representative Population**: Tertiary academic centers inherently exhibit referral and severity bias.
8. **Traditional Medicine RWD $\ne$ Automatic Efficacy Proof**: Documented real-world Unani or Ayurvedic treatment outcomes must be recorded as observational usage, not definitive clinical proof.
9. **AI-Generated Cohort $\ne$ Approved Cohort**: Cohort logic drafted by AI must be human-reviewable and verifiable.
10. **AI-Generated Analysis $\ne$ Validated Analysis**: Statistical execution requires strict reproducibility and code provenance.
11. **AI-Generated Result $\ne$ Research Result**: AI must never invent effect sizes, confidence intervals, or sample sizes.
12. **Synthetic Data $\ne$ Real-World Data**: Synthetic data used for pipeline testing must be isolated and labeled `SYNTHETIC`.
13. **Private Patient Data $\ne$ Public Knowledge**: Confidential EHR and clinical registry data remain strictly isolated within sovereign tenants.
14. **New Data $\ne$ Automatically New Knowledge**: Ingested updates require quality checks and revalidation gates before updating the Knowledge Graph.
15. **New RWE $\ne$ Automatically Changed Clinical Guidance**: Observational evidence informs surveillance and revalidation queues without unilaterally overwriting authoritative professional society guidelines.

---

### 3. Standards Architecture & Supported Models

| Standard | Target Domain | Primary Models | Key Vocabularies / Versions |
|---|---|---|---|
| **HL7 FHIR** | Clinical Interoperability | `Patient`, `Condition`, `Observation`, `MedicationStatement`, `ResearchStudy`, `Bundle` | FHIR R5 / R4, SNOMED CT, LOINC, RxNorm, UCUM |
| **OHDSI OMOP CDM** | Federated Observational Analytics | `PERSON`, `CONDITION_OCCURRENCE`, `DRUG_EXPOSURE`, `MEASUREMENT`, `OBSERVATION_PERIOD` | OMOP CDM v5.4 / v5.5, Athena Concept IDs |
| **CDISC SDTM / ADaM** | Regulatory Clinical Research | `DM` (Demographics), `LB` (Laboratory Tests), `EX` (Exposure), `AE` (Adverse Events) | CDISC SDTM v1.7, Define-XML v2.1, ODM v1.3 |
| **NAMASTE / ICD-11 TM2** | Traditional Medicine Clinical Records | `NAMASTEConcept`, `MizajAssessmentRecord`, `PrakritiAssessmentRecord` | NAMASTE Morbidity Codes, WHO ICD-11 TM2, NFUM / API Pharmacopoeias |

---

### 4. Target Trial Emulation (TTE) & Causal DAG Engine

- **Target Trial Emulation**: Formulates observational studies using the Hernán & Robins target trial specification:
  - **Eligibility**: Synchronized at Time Zero.
  - **Strategies**: New-user active-comparator design (e.g. SGLT2i vs active comparator).
  - **Assignment**: Propensity score matching / Inverse Probability of Treatment Weighting (IPTW).
  - **Time Zero**: Date of first eligible prescription dispensing (preventing immortal time bias).
  - **Causal Contrast**: Observational analog of Intention-to-Treat (ITT) and Per-Protocol effects.
- **Causal DAGs**: Explicitly maps exposure, mediators, colliders, and measured vs unmeasured confounders. Prohibits conditioning on colliders (e.g. hospitalization selection).
- **Negative Control Calibrations**: Supports negative control exposures (e.g. influenza vaccination in summer) and negative control outcomes (e.g. accidental fracture) to detect unmeasured residual confounding.

---

### 5. Federated Research Clean Room & Privacy Controls

- **HMAC-SHA256 Tokenization**: Converts hospital MRNs into salted, irreversible `research_subject_id` tokens (e.g. `SUBJ-AFE804F85CBC4529`). Direct patient identifiers never leave the sovereign hospital enclave.
- **Small-Cell Disclosure Suppression**: Any query returning $< 5$ subjects at an institutional node is obscured as `0` / `< 5` to defeat re-identification and linkage attacks.
- **Multi-Node Clean Room Queries**: Aggregates cohort counts across participating centers (Oxford, Harvard/Brigham, NIUM, AIIA) without centralizing raw microdata.

---

### 6. REST API Endpoint Catalog

All routes are mounted under `/v1/rwe`:

| Endpoint | Method | Response Model | Description |
|---|---|---|---|
| `/v1/rwe/sources` | `GET` | `List[RWDSourceRecord]` | Lists registered authorized RWD sources across jurisdictions. |
| `/v1/rwe/sources/{id}` | `GET` | `RWDSourceRecord` | Retrieves RWD source metadata, licensing, and governance contracts. |
| `/v1/rwe/quality/audit` | `POST` | `DataQualityReport` | Executes 9-dimension quality audit and plausibility verification. |
| `/v1/rwe/quality/fitness-check` | `POST` | `FitnessForPurposeAssessment` | Evaluates dataset fitness against a specific research question. |
| `/v1/rwe/tte/protocols` | `POST` | `TargetTrialProtocol` | Registers a Target Trial Emulation protocol. |
| `/v1/rwe/tte/protocols/{id}` | `GET` | `TargetTrialProtocol` | Inspects TTE protocol details and censoring rules. |
| `/v1/rwe/tte/dag` | `POST` | `CausalDAG` | Registers a Causal Directed Acyclic Graph. |
| `/v1/rwe/tte/audit-claim` | `POST` | `Dict[str, Any]` | Causality Firewall: blocks claims asserting 'causes'/'cures' without TTE. |
| `/v1/rwe/tte/negative-control` | `GET` | `Dict[str, Any]` | Generates negative control exposure and outcome designs. |
| `/v1/rwe/federated/query` | `POST` | `FederatedQueryResult` | Executes multi-site federated query with small-cell suppression (< 5). |
| `/v1/rwe/federated/tokenize` | `GET` | `Dict[str, Any]` | Pseudonymizes direct patient ID to `research_subject_id`. |
| `/v1/rwe/harmonize/raw-to-fhir` | `POST` | `FHIRBundle` | Translates raw EHR encounter JSON into HL7 FHIR Bundle. |
| `/v1/rwe/harmonize/fhir-to-omop` | `POST` | `Dict[str, Any]` | Maps FHIR resources to OHDSI OMOP CDM v5.4 tables. |
| `/v1/rwe/harmonize/omop-to-cdisc` | `POST` | `Dict[str, Any]` | Translates OMOP CDM into CDISC SDTM domains (DM, LB, EX). |
| `/v1/rwe/harmonize/traditional` | `POST` | `Dict[str, Any]` | Harmonizes Unani Mizaj and Ayurvedic Prakriti registry records. |
| `/v1/rwe/cohorts/define` | `POST` | `RWECohortDefinition` | Registers observational cohort study definition. |
| `/v1/rwe/cohorts/analyze` | `POST` | `RWEEvidenceSummary` | Runs propensity-adjusted analysis and observational bias audit. |
| `/v1/rwe/triangulate` | `POST` | `Dict[str, Any]` | Triangulates RWE effect size against landmark Phase 3 RCT benchmark. |

---

### 7. Verification & Test Evidence

#### Master Acceptance Test Suite
Executed via:
```bash
PYTHONPATH=services/engine:sdk/python .venv/bin/python3 -m unittest tests/test_rwe_interop_acceptance.py
```
- `test_01_raw_to_fhir_bundle`: **PASS** (Patient, Condition, Observation, and MedicationStatement created).
- `test_02_fhir_to_omop_cdm_mapping`: **PASS** (OMOP v5.4 concepts resolved: SNOMED 316139, RxNorm 43534760, LOINC 3004410).
- `test_03_omop_to_cdisc_sdtm_mapping`: **PASS** (CDISC SDTM DM, LB, EX domains populated).
- `test_04_traditional_registry_harmonization`: **PASS** (NAMASTE `UN-DIS-002` aligned to `TM2-UN-I50` and Unani Balghami Mizaj diagnostic preserved).
- `test_05_data_quality_audit_9_dimensions_and_plausibility`: **PASS** (Plausibility checks flagged impossible age 142, future date 2099, and HbA1c 29.0%).
- `test_06_fitness_for_purpose_gate`: **PASS** (Dataset evaluated against research question; achieved FIT status).
- `test_07_target_trial_emulation_and_causal_dag`: **PASS** (TTE protocol with Time Zero and Causal DAG registered).
- `test_08_causality_firewall`: **PASS** (Blocked ungrounded 'causes/cures' claims without TTE; passed compliant associative claim).
- `test_09_federated_clean_room_and_small_cell_suppression`: **PASS** (Suppressed cells with < 5 subjects across 3 nodes; HMAC tokenization verified).
- `test_10_rwe_cohort_definition_and_bias_audit`: **PASS** (Controlled for 6 covariates, immortal time bias protected).
- `test_11_evidence_graph_bridge_and_triangulation`: **PASS** (EvidenceObject $E_5$ created; DAPA-HF triangulation yielded `HIGHLY_CONCORDANT` delta 0.000).
- `test_12_master_rest_api_endpoints`: **PASS** (FastAPI REST endpoints verified).

#### Regression Test Suite
- Ran all tests across Prompts 1 through 15: **110/110 tests passing in 0.21s (100% pass rate, 0 regressions)**.
