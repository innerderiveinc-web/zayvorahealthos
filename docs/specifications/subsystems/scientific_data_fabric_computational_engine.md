# ZMIE Scientific Data Fabric & Computational Research Engine

> **Fundamental Scientific Principle:**  
> **“No scientific result without a traceable computational path.”**  
> **$\text{Data} \ne \text{Knowledge},\ \text{Computation} \ne \text{Observation},\ \text{Model} \ne \text{Reality},\ \text{Result} \ne \text{Claim},\ \text{Claim} \ne \text{Evidence}$**

---

## 1. System Overview & Core Mission

The **ZMIE Scientific Data Fabric & Computational Research Engine** (Prompt 21) expands ZMIE from a system that can find, map, and reason into a platform that can **ingest, standardize, compute, analyze, reproduce, validate, and publish** empirical research results.

Every scientific output answers:
- What data was used?
- Where did it come from?
- What exact version was used?
- How was it transformed?
- What code executed?
- Which parameters were set?
- Which software environment was containerized?
- Can it be deterministically reproduced?

### Strict Scientific State Axioms
Outputs are strictly categorized into non-overlapping states:
- `OBSERVED`: Direct experimental or clinical measurements.
- `COMPUTED`: Statistical estimates, regressions, or derived metrics.
- `MODELED`: Mechanistic or dynamic biological representations.
- `SIMULATED`: Parametric in-silico sweeps (Monte Carlo).
- `VALIDATED`: Certified through independent reproduction and expert governance.

> [!CAUTION]
> A statistical estimate is **never** treated as raw observation.  
> A model prediction is **never** treated as clinical evidence.

---

## 2. Architecture & Pipeline

```text
                   ZMIE SCIENTIFIC DATA FABRIC
                                │
    ┌───────────────────────────┼───────────────────────────┐
    ▼                           ▼                           ▼
RAW INGESTION          STANDARDIZATION & QC         IMMUTABLE SNAPSHOTS
(CSV, FHIR, OMOP)      (Missingness & Units)        (SHA256 Content Hash)
                                │
                                ▼
                       ANALYSIS PLANNING
                    (Leakage Gating & Covariates)
                                │
                                ▼
                    CONTAINERIZED EXECUTION
                  (Runtime & Seed Determinism)
                                │
                                ▼
                        EFFECT ESTIMATES
                    (Strictly COMPUTED state)
                                │
    ┌───────────────────────────┼───────────────────────────┐
    ▼                           ▼                           ▼
DATA LINEAGE GRAPH     REPRODUCE ENGINE            CANDIDATE CLAIMS
(Root to Leaf DAG)     (Signed Certificate)        (Gated Human Release)
```

---

## 3. Subsystem Capabilities

### A. Data Fabric Ingestion & Profiling
- Ingests structured clinical and trial cohorts.
- Automatically generates multi-dimensional `DataQualityReport` evaluating completeness scores, missingness mechanisms (`MCAR`, `MAR`, `MNAR`), unit consistency, and fitness for purpose.

### B. Cryptographic Snapshot Pinning
- Pinned datasets are sealed with `content_sha256` and `fields_schema_hash`.
- Prevents silent modifications, retrospective retrofitting, or dataset tampering.

### C. Data Leakage Detection
- Intercepts preregistered analysis plans containing post-outcome flags, future events, or label-derived variables in covariates.
- Blocks execution immediately until the protocol is remediated.

### D. Computational Execution & Effect Estimates
- Containerized statistical workflows (e.g. Cox Proportional Hazards regression).
- Generates `EffectEstimate` tracking measure type (`HAZARD_RATIO`), point estimate, 95% confidence intervals, $p$-values, standard errors, sample size, and event counts.
- Strict scientific state tag: `COMPUTED`.

### E. Reproducibility Engine & Computational Certificates
- `reproduce_run(run_id)` re-executes analyses from the exact immutable snapshot, code hash, dependencies, and seed.
- Validates numerical divergence ($\Delta < 10^{-6}$).
- Issues a cryptographically signed `ComputationalCertificate`.

### F. Computation Diffing (Run A vs Run B)
- Inspects whether variances in scientific results stem from dataset updates, code alterations, or parameter perturbations.

### G. Complete Data Lineage Graph
- Traces end-to-end directed acyclic graph:
  $$\text{RAW\_DATASET} \longrightarrow \text{NORMALIZED\_DATASET} \longrightarrow \text{SNAPSHOT} \longrightarrow \text{ANALYSIS\_PLAN} \longrightarrow \text{RUN} \longrightarrow \text{ESTIMATE}$$

### H. Candidate Claim & Evidence Promotion Gating
- Bridges computational results into the global Evidence Graph.
- Strictly gated: AI suggestions remain in `PENDING_REVIEW` state; only verified human investigators can approve and promote claims.

### I. License & Tenancy Enforcement
- Blocks unauthorized external export of proprietary or commercial datasets.

---

## 4. API Endpoints (`services/engine/app/api/v1/scientific_compute.py`)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/v1/compute/datasets/ingest` | Ingests dataset and returns quality report |
| `GET` | `/v1/compute/datasets/{id}` | Retrieves schema, fields, and privacy classification |
| `POST` | `/v1/compute/datasets/{id}/snapshot` | Creates an immutable cryptographic snapshot |
| `POST` | `/v1/compute/analyses/plan` | Registers analysis plan with leakage checks |
| `POST` | `/v1/compute/workflows/run` | Executes containerized statistical modeling run |
| `GET` | `/v1/compute/runs/{id}` | Retrieves run details and effect estimates |
| `POST` | `/v1/compute/runs/{id}/reproduce` | Re-executes run and issues `ComputationalCertificate` |
| `GET` | `/v1/compute/runs/diff` | Compares Run A vs Run B across data/code/parameters |
| `GET` | `/v1/compute/lineage/{id}` | Traces complete end-to-end data lineage DAG |
| `POST` | `/v1/compute/claims/candidate` | Generates candidate claim from result artifact |
| `POST` | `/v1/compute/claims/promote` | Human review gate for promotion to Evidence Graph |
| `GET` | `/v1/compute/licenses/verify` | Verifies export rights before data egress |

---

## 5. Verification & Acceptance

- **Acceptance Test Suite**: [`tests/test_scientific_compute_acceptance.py`](file:///Users/irfanashraf/Downloads/zmie/tests/test_scientific_compute_acceptance.py)
  - Golden End-to-End Test (Clause 219) passing.
  - Data leakage prevention verified.
  - Computation diffing verified.
  - License export restrictions verified.
  - REST endpoints verified.
- **Showcase Script**: [`tests/scientific_compute_showcase.py`](file:///Users/irfanashraf/Downloads/zmie/tests/scientific_compute_showcase.py)
- **Status**: **171 passing tests** across the entire repository with 0 regressions, 221 operational FastAPI endpoints.
