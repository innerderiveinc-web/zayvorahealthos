# ZMIE — GLOBAL RESEARCH DISCOVERY NETWORK & CONTINUOUS KNOWLEDGE EVOLUTION ENGINE
## Master Architectural Blueprint, Multi-System Research Topology & Continuous Evolution Engine
### Prompt 14 Production Implementation Specification

---

### 1. Executive Summary & Core Philosophy

The **ZMIE Global Research Discovery Network & Continuous Knowledge Evolution Engine** elevates ZMIE from a static literature indexing platform to a **continuously evolving global medical research intelligence infrastructure**.

Medical knowledge is not created only when a journal article is published. Research unfolds across a multi-stage, multi-year lifecycle:

```text
Research Idea
    ↓
Research Proposal
    ↓
Funding / Grant (NIH, MRC, AYUSH, ERC, ICMR)
    ↓
Research Project
    ↓
Researcher / Team (Author Identity & ORCID)
    ↓
Institution / University / Laboratory (ROR ID)
    ↓
Protocol & Preregistration
    ↓
Clinical Trial / Experimental Study (CT.gov, CTRI, EU-CTR)
    ↓
Dataset (Zenodo, Dryad, GEO)
    ↓
Conference Poster / Presentation
    ↓
Preprint (medRxiv, bioRxiv)
    ↓
Thesis / Dissertation
    ↓
Peer-Reviewed Publication
    ↓
Correction / Retraction / Replication
    ↓
Knowledge Claim Revalidation & Release
```

#### Core System Non-Negotiables
1. **First-Class Research Entities**: Researchers, Institutions, Grants, Clinical Trials, Preprints, Theses, Datasets, and Patents are modeled as rich, first-class nodes in the research graph—not mere bibliographic metadata.
2. **Strict Identity Disambiguation**: Resolves name collisions using composite heuristics (ORCID, ROR affiliations, co-authorship networks, subject domains). Never merges distinct individuals based on surname matching.
3. **Canonical Study De-Duplication**: Trial registrations, preprints, and peer-reviewed articles from the same clinical trial cohort are clustered under a single `CanonicalStudy` identifier. This prevents artificial evidence inflation and duplicate-citation counting.
4. **Epistemic & Evidence Boundaries**:
   - `Preprints` $\ne$ peer-reviewed clinical proof.
   - `Patents` $\ne$ validated therapeutic efficacy.
   - `Grants` $\ne$ completed clinical trials.
   - `Theses` $\ne$ consensus guidelines.
   - `Private / Confidential Projects` $\rightarrow$ Enforced `PRIVATE_UNOBSERVABLE` boundary. Zero hallucination or fabrication of private undisclosed research.
5. **Continuous Knowledge Evolution**: When a study is retracted, a trial terminates for safety, or a guideline updates, the system executes an automated **Cascade Impact Analysis**, demoting affected claims and dispatching clinical alerts.
6. **Multi-System Research Topology**: Full parity for modern biomedicine and statutory traditional systems (Unani, Ayurveda, Siddha, TCM) through institutions such as NIUM, AIIA, CCRUM, CCRAS, and CTRI.

---

### 2. Multi-Class Entity Schema & Graph Topology

| Entity Class | Primary Identifiers | Key Attributes | Provenance & Rules |
|---|---|---|---|
| **Researcher** | `researcher_id`, `orcid` | `canonical_name`, `aliases`, `affiliations`, `subject_areas`, `traditional_systems`, `h_index` | Verifiable via ORCID; disambiguation confidence score computed per query. |
| **ResearchInstitution** | `institution_id`, `ror_id` | `name`, `institution_type`, `country`, `departments`, `active_trials_count`, `total_grant_funding_usd` | Cross-referenced against ROR; supports universities, hospitals, and traditional statutory councils (AYUSH/CCRUM). |
| **GrantRecord** | `grant_id`, `grant_number` | `funding_agency`, `title`, `amount_usd`, `pi_ids`, `institution_id`, `start_date`, `end_date`, `status` | Direct grant tracing across MRC, NIH, AYUSH, ERC. |
| **ClinicalTrialRecord** | `trial_id` (NCT, CTRI) | `registry`, `phase`, `recruitment_status`, `interventions`, `conditions`, `canonical_study_id` | Linked to WHO-ICTRP, CT.gov, and CTRI; links directly to publication DOIs. |
| **PreprintRecord** | `preprint_id`, `doi` | `server`, `title`, `deposited_date`, `version`, `canonical_study_id`, `peer_reviewed_doi` | Explicit `PREPRINT` preliminary warning; marked `SUPERSEDED` once journal publication appears. |
| **ThesisRecord** | `thesis_id`, `accession_id` | `title`, `author_id`, `advisor_ids`, `degree` (PhD, MD, Mahir-e-Tibb), `defense_year` | Academic qualification work; explicitly tagged as preliminary academic inquiry. |
| **DatasetRecord** | `dataset_id`, `doi` | `repository`, `title`, `creator_ids`, `related_study_id`, `access_tier` (OPEN, RESTRICTED) | Repositories include Zenodo, Dryad, GEO, PhysioNet. |
| **PatentRecord** | `patent_id`, `patent_number` | `office` (USPTO, EPO, IPO), `inventor_ids`, `assignee_institution_id`, `status` | Explicit `PATENT` intellectual property warning; does not constitute clinical efficacy proof. |
| **ResearchProject** | `project_id` | `title`, `lead_researcher_ids`, `status`, `is_private_unobservable`, `canonical_study_id` | Enforces private/unobservable boundary when research is confidential. |
| **ResearchSignal** | `signal_id`, `topic` | `frontier_velocity_score`, `growth_rate_3yr`, `clinical_trial_acceleration`, `grant_inflow_usd` | Automatically identifies high-momentum medical paradigm shifts and emerging therapies. |
| **ResearchGapAnalysis** | `gap_id`, `topic` | `gap_type`, `deficiency_description`, `missing_evidence_type`, `priority_score`, `suggested_investigation` | Detects population exclusions, lack of replication, and underinvestigated traditional pharmacology. |
| **EvolutionImpactAnalysis** | `impact_id` | `trigger_type`, `trigger_source_id`, `affected_claim_ids`, `new_claim_states`, `alerts_dispatched` | Records downstream degradation or elevation of claims and graph edges upon literature changes. |

---

### 3. Continuous Knowledge Evolution: Cascade Impact Workflow

```text
       [Literature Surveillance / Regulatory Event]
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
      [RETRACTION EVENT]        [GUIDELINE CHANGE]
               │                         │
               ├─────────────────────────┤
               ▼
   [Locate Downstream Dependencies]
   - Knowledge Graph Relations
   - Evidence Graph Citations
   - Research Workbench Projects
   - Clinical Recommendation Claims
               │
               ▼
   [State Transition & Confidence Degradation]
   - Old: SUPPORTED (0.96) ──► New: RETRACTED (0.05)
               │
               ▼
   [Dispatch High-Priority Alerts]
   - EMERGENCY RETRACTION CASCADE Alert
   - Withhold Clinical Practice Decisions
               │
               ▼
   [Atomic Snapshot Capture & Time-Series Diff]
   - Snapshot Version N ──► Version N+1
```

---

### 4. REST API Endpoint Catalog

All routes are mounted under `/v1/research-network`:

| Endpoint | Method | Description |
|---|---|---|
| `/v1/research-network/researchers/{id}` | `GET` | Retrieves comprehensive researcher dossier with ORCID and institutional affiliations. |
| `/v1/research-network/researchers/disambiguate` | `POST` | Disambiguates author name using composite ORCID, institution, and subject criteria. |
| `/v1/research-network/institutions/{id}` | `GET` | Returns institutional research profile, ROR ID, and active trial counts. |
| `/v1/research-network/projects/{id}` | `GET` | Retrieves project details with `PRIVATE_UNOBSERVABLE` boundary protection. |
| `/v1/research-network/who-is-researching` | `GET` | Resolves "Who is researching this topic?", returning ranked researchers and affiliations. |
| `/v1/research-network/where-is-research-happening` | `GET` | Resolves global distribution of trials, funding, and institutions for a query. |
| `/v1/research-network/canonical-study/{id}` | `GET` | Clusters trial, preprint, and publication under a single Canonical Study to prevent double-counting. |
| `/v1/research-network/lifecycle/{root_id}` | `GET` | Full lifecycle graph traversal from Grant to Publication. |
| `/v1/research-network/frontier` | `GET` | Lists high-velocity frontier research signals and emerging medical paradigms. |
| `/v1/research-network/gaps` | `GET` | "What Am I Missing?" structural research gap analyzer. |
| `/v1/research-network/evolution/cascade` | `POST` | Executes or simulates cascade impact analysis for retractions, new trials, or guidelines. |
| `/v1/research-network/evolution/revalidate/enqueue` | `POST` | Enqueues claims or relations into prioritized revalidation queue (`CRITICAL`, `HIGH`, `LOW`). |
| `/v1/research-network/evolution/revalidate/process` | `POST` | Processes pending revalidation queue items in priority order. |
| `/v1/research-network/evolution/snapshots` | `GET` | Retrieves versioned knowledge snapshots. |
| `/v1/research-network/evolution/snapshots` | `POST` | Creates an atomic snapshot of current medical knowledge states. |
| `/v1/research-network/evolution/diff` | `POST` | Computes differential delta between two knowledge snapshots. |

---

### 5. Verification & Test Evidence

#### Automated Acceptance Test Suite
Executed via:
```bash
PYTHONPATH=services/engine:sdk/python .venv/bin/python3 -m unittest tests/test_research_discovery_acceptance.py
```
- `test_01_researcher_disambiguation_orcid_and_affiliation`: **PASS** (100% ORCID match vs 70% institutional match; uncollapsed entities verified).
- `test_02_canonical_study_clustering_and_deduplication`: **PASS** (Canonical cluster verified; 2 redundant citations suppressed).
- `test_03_lifecycle_tracing_and_unobservable_boundary`: **PASS** (Public lifecycle traced across 5 nodes; private project guarded with `PRIVATE_UNOBSERVABLE`).
- `test_04_who_is_researching_multi_system`: **PASS** (Correctly retrieved Sarah Jenkins for modern cardiology and Hakim Aslam Siddiqui for Unani medicine).
- `test_05_where_is_research_happening`: **PASS** (Global institutional mapping verified).
- `test_06_frontier_signals_velocity`: **PASS** (Frontier velocity scores verified at 94.5 and 82.0).
- `test_07_continuous_evolution_retraction_cascade`: **PASS** (Retracted study triggered claim invalidation and CRITICAL alert dispatch).
- `test_08_revalidation_queue_priority_ordering`: **PASS** (CRITICAL jobs processed before LOW priority).
- `test_09_research_gaps_and_blindspots`: **PASS** (Population exclusion and traditional pharmacokinetic gaps identified).
- `test_10_knowledge_snapshot_and_diff`: **PASS** (Versioned snapshots and time-series diffs verified).
- `test_11_rest_api_endpoints`: **PASS** (FastAPI REST endpoints verified).

#### Regression Test Suite
- Ran all tests across Prompts 1 through 14: **98/98 tests passing in 0.12s (100% pass rate, 0 regressions)**.
