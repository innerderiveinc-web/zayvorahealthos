# ZMIE SOURCE ACQUISITION & INGESTION TEST PLAN
## Comprehensive Quality Assurance, Contract Testing & Acceptance Matrix

---

### 1. Test Levels & Strategy

The ZMIE Ingestion Quality Assurance framework operates at four distinct levels:

```text
┌────────────────────────────────────────────────────────┐
│ LEVEL 4: Master End-to-End Acceptance (Section 108)   │
├────────────────────────────────────────────────────────┤
│ LEVEL 3: Ingestion Acceptance (test_source_ingestion)  │
├────────────────────────────────────────────────────────┤
│ LEVEL 2: Connector Contract & Provider Integration     │
├────────────────────────────────────────────────────────┤
│ LEVEL 1: Unit Tests (Parsing, Hashing, License Logic)  │
└────────────────────────────────────────────────────────┘
```

---

### 2. Required Test Scenarios

#### Scenario 1: Connector Contract Adherence
- **Test File**: `tests/test_source_ingestion_acceptance.py::test_01_connector_contract_adherence`
- **Assertion**: All registered connectors instantiate `BaseSourceConnector`, implement all 9 required abstract methods, and return valid status telemetry.

#### Scenario 2: Clinical Trial PICO Normalization
- **Test File**: `tests/test_source_ingestion_acceptance.py::test_02_clinical_trials_connector_normalization`
- **Assertion**: JSON from ClinicalTrials.gov v2 correctly decomposes into NCT ID, overall status, phase, interventions array, primary outcomes, and PICO contexts.

#### Scenario 3: Class C Copyright Quarantine
- **Test File**: `tests/test_source_ingestion_acceptance.py::test_03_licensing_quarantine_enforcement`
- **Assertion**: When input is Class C (closed access), `full_text` is strictly set to `None`, body sections array is emptied, only abstract is retained, and copyright notice is appended.

#### Scenario 4: Cryptographic SHA-256 & Paragraph Anchoring
- **Test File**: `tests/test_source_ingestion_acceptance.py::test_04_document_parser_and_cryptographic_anchors`
- **Assertion**: Document hashing produces a verified 64-character hex string; paragraphs generate 16-character anchor hashes.

#### Scenario 5: Immutable Versioning & Supersession
- **Test File**: `tests/test_source_ingestion_acceptance.py::test_05_document_versioning_and_supersession`
- **Assertion**: Verifies mutation states `NEW` $\rightarrow$ `UNCHANGED` $\rightarrow$ `SUPERSEDED` $\rightarrow$ `RETRACTED`. Older guidelines are preserved and marked `SUPERSEDED` rather than deleted.

#### Scenario 6: Operational Health & Error Budgets
- **Test File**: `tests/test_source_ingestion_acceptance.py::test_06_source_health_monitor_and_error_budget`
- **Assertion**: Verifies status transitions between `HEALTHY`, `DEGRADED`, and `BLOCKED` based on error rate, latency, and rate limits.

#### Scenario 7: 14-Stage Ingestion Lifecycle
- **Test File**: `tests/test_source_ingestion_acceptance.py::test_07_ingestion_job_runner_lifecycle`
- **Assertion**: `IngestionJobRunner` executes query through all 14 stages, producing `JobStatus.COMPLETED` with non-zero acquired documents and extracted claim passports.

---

### 3. Automated Test Execution Commands

```bash
# Run source acquisition acceptance suite
PYTHONPATH=services/engine:sdk/python .venv/bin/python3 tests/test_source_ingestion_acceptance.py

# Run master section 108 acceptance suite
PYTHONPATH=services/engine:sdk/python .venv/bin/python3 tests/test_section_108_acceptance.py

# Run master end-to-end showcase
PYTHONPATH=services/engine:sdk/python .venv/bin/python3 tests/master_showcase.py
```
