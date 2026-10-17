# ZMIE Living Evidence Synthesis & Evidence Update Suite
## Continuous Surveillance, Reproducible Meta-Analysis & Versioned Evidence Architecture

> **The Golden Principle:**
> A living review is not a document regenerated blindly every day.
> It is an auditable, versioned scientific evidence object with prespecified eligibility, continuous surveillance, transparent appraisal, reproducible meta-analysis, and explicit change governance.
>
> $$\text{New Research Paper} \ne \text{Automatic Conclusion Change}$$
> $$\text{New Research Paper} \longrightarrow \text{Screening} \longrightarrow \text{Impact Appraisal} \longrightarrow \text{Synthesis Recalculation} \longrightarrow \text{Versioned Release}$$

---

## 1. Executive Summary & Ten Golden Rules

The **ZMIE Living Evidence Synthesis & Evidence Update Engine** (Prompt 17) transforms static evidence reviews into **Living Evidence Objects** that continuously monitor the global research ecosystem while strictly preventing unauthorized or hallucinated rewrites of scientific consensus.

### The Ten Golden Rules of Living Synthesis
1. **Rule 1 (No Blind Auto-Updates):** New evidence must undergo screening, eligibility appraisal, and impact classification before modifying published synthesis.
2. **Rule 2 (Historical Preservation):** Never overwrite historical versions. Maintain an immutable audit trail of past releases.
3. **Rule 3 (Transparency of Pending Evidence):** Never conceal known eligible research. If new evidence is discovered but awaiting synthesis, display `NEW_EVIDENCE_PENDING`.
4. **Rule 4 (AI Governance):** AI accelerates search, screening, and data extraction, but can never autonomously change eligibility, primary endpoints, or publish conclusions without human review gating.
5. **Rule 5 (Currency $\ne$ Completeness):** Current as of today does not imply zero blind spots. Source coverage limitations must remain explicit.
6. **Rule 6 (Evidence $\ne$ Prescription):** Evidence updates describe empirical findings; they do not constitute autonomous clinical prescribing recommendations.
7. **Rule 7 (Meta-Analysis $\ne$ Causal Proof):** Statistical pooling across observational or heterogeneous data does not bypass causal identification requirements.
8. **Rule 8 (No Cross-System Pooling):** Traditional knowledge (Unani, Ayurveda) and modern clinical trials maintain separate, parallel evidence streams without invalid statistical pooling.
9. **Rule 9 (RWE $\ne$ RCTs):** Real-world observational datasets are labeled and analyzed separately from randomized trials.
10. **Rule 10 (New Evidence $\ne$ Stronger Evidence):** New studies may confirm, weaken, contradict, or simply add precision to existing estimates.

---

## 2. Core Architecture & Entity Model

```text
GLOBAL RESEARCH SOURCES
         │
         ▼
SURVEILLANCE PLAN (Scheduled / Event-Driven)
         │
         ▼
SCREENING QUEUE (AI-Assisted with Human Gates)
  [New -> Duplicate Check -> Title/Abstract -> Full Text -> Included / Excluded]
         │
         ▼
STUDY FAMILY DE-DUPLICATION (Registry + Protocol + Preprint + Article + Follow-up)
         │
         ▼
STRUCTURED EXTRACTION & RISK OF BIAS (RoB 2 / ROBINS-I)
         │
         ▼
QUANTITATIVE SYNTHESIS (DerSimonian-Laird Random Effects Meta-Analysis)
         │
         ▼
GRADE CERTAINTY ASSESSMENT (5 Downgrade Domains + Upgrades)
         │
         ▼
IMPACT & RETRACTION MONITORING (Urgent Quarantine & Recalculation)
         │
         ▼
VERSION RELEASE (PRISMA Flow, What's New Changelog, Version Diffing)
```

### 2.1 The Canonical `LivingEvidenceSynthesis` Object
Each living review maintains:
- `research_question`: Structured PICO/PECO/PICOT framework with versioning (`RQ-v1`).
- `eligibility_criteria`: Inclusion/exclusion rules with audit trails (`ELIG-v1`).
- `surveillance_plan`: Cadence (e.g. 7 days), target databases, and alert thresholds.
- `search_strategy`: Exact reproducible MeSH query strings and database filters.
- `study_families`: Study entity linking trial registries (e.g. `NCT03036124`), preprints, primary articles, and secondary follow-up papers to eliminate double-counting.
- `screening_queue`: Dual-reviewer screening records with explicit exclusion reasons.
- `extractions`: Verified effect sizes, standard errors, sample sizes, and provenance tags.
- `versions`: Immutable sequence of releases (`v1.0`, `v2.0`, `v3.0`).

---

## 3. Statistical Synthesis & Meta-Analysis Engine

### 3.1 DerSimonian-Laird Random Effects Model
For a collection of $k$ independent studies with effect estimates $y_i$ and variances $v_i$:

1. **Fixed-Effect Weight:**
   $$w_{i,\text{fixed}} = \frac{1}{v_i}$$
2. **Fixed-Effect Pooled Estimate:**
   $$\bar{y}_{\text{fixed}} = \frac{\sum w_{i,\text{fixed}} y_i}{\sum w_{i,\text{fixed}}}$$
3. **Cochran's Heterogeneity Statistic ($Q$):**
   $$Q = \sum w_{i,\text{fixed}} \left( y_i - \bar{y}_{\text{fixed}} \right)^2$$
4. **Between-Study Variance ($\tau^2$):**
   $$\tau^2 = \max\left( 0, \frac{Q - (k - 1)}{\sum w_{i,\text{fixed}} - \frac{\sum w_{i,\text{fixed}}^2}{\sum w_{i,\text{fixed}}}} \right)$$
5. **Heterogeneity Index ($I^2$):**
   $$I^2 = \max\left( 0, \frac{Q - (k - 1)}{Q} \right) \times 100\%$$
6. **Random-Effects Weight & Pooled Estimate:**
   $$w_i^* = \frac{1}{v_i + \tau^2}, \quad \bar{y}_{\text{random}} = \frac{\sum w_i^* y_i}{\sum w_i^*}$$

### 3.2 GRADE Certainty Assessment
Evaluates 5 predefined domains:
1. **Risk of Bias:** Methodological limitations in study design.
2. **Inconsistency:** Heterogeneity across effect sizes ($I^2 > 50\%$).
3. **Indirectness:** Population, intervention, or outcome differences from PICO.
4. **Imprecision:** 95% confidence intervals crossing clinical decision thresholds.
5. **Publication Bias:** Asymmetric small-study effects or missing negative trials.

Certainty Levels: `HIGH`, `MODERATE`, `LOW`, `VERY_LOW`.

---

## 4. Continuous Surveillance & Retraction Protocols

### 4.1 Update Trigger Classification
- **Urgent Triggers:**
  - `RETRACTION` of pivotal trial $\longrightarrow$ Immediate quarantine and synthesis recalculation.
  - `NEW_SAFETY_SIGNAL` $\longrightarrow$ Elevated to urgent benefit-risk update.
  - `MAJOR_CONTRADICTION` $\longrightarrow$ Flagged for methodologist review.
- **Routine Triggers:**
  - `NEW_RCT`, `NEW_RWE` $\longrightarrow$ Screened and incorporated in next scheduled release.

### 4.2 Retraction Quarantine Workflow
```text
1. Retraction alert detected (e.g. unverified source data).
2. Flag StudyFamily: is_active = False, is_retracted = True.
3. Automatically recompute DerSimonian-Laird meta-analysis excluding compromised data.
4. Assess change in pooled effect, I^2 heterogeneity, and GRADE certainty.
5. Publish transparent version (v3.0) with WHAT'S CHANGED statement.
```

---

## 5. API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/v1/living-evidence` | List all registered living syntheses |
| `GET` | `/v1/living-evidence/{id}` | Retrieve complete living evidence synthesis object |
| `POST` | `/v1/living-evidence/{id}/start-living` | Activate living surveillance mode |
| `POST` | `/v1/living-evidence/{id}/pause` | Temporarily pause surveillance |
| `GET` | `/v1/living-evidence/{id}/health` | Check surveillance currency, backlog, and staleness |
| `POST` | `/v1/living-evidence/{id}/screening` | AI-assisted title/abstract screening with human gates |
| `POST` | `/v1/living-evidence/{id}/triggers` | Register update trigger & determine urgency |
| `POST` | `/v1/living-evidence/{id}/incorporate` | Incorporate new study, recompute meta-analysis, release new version |
| `POST` | `/v1/living-evidence/{id}/retract` | Quarantine retracted study, recalculate, release urgent update |
| `GET` | `/v1/living-evidence/{id}/diff` | Compare two review versions (studies delta, pooled delta) |

---

## 6. Verification Results

- **Unit & Acceptance Suite**: [`test_living_evidence_acceptance.py`](file:///Users/irfanashraf/Downloads/zmie/tests/test_living_evidence_acceptance.py) (7/7 tests passing in 0.03s).
- **End-to-End Showcase**: [`living_evidence_showcase.py`](file:///Users/irfanashraf/Downloads/zmie/tests/living_evidence_showcase.py) verifying 6 live scenarios (Baseline PICO review, AI screening, trigger detection, study incorporation, retraction quarantine, version diffing).
- **Full Regression Suite**: 128 / 128 tests passing across all 17 ZMIE prompts.
