# ZMIE SOURCE QUALITY & EVIDENCE DECOUPLING MODEL
## Orthogonal Authority Tiers, Methodological Grading & Quality Assurance

---

### 1. Orthogonal Decoupling Principle

A foundational architecture rule in ZMIE is:
$$\text{Source Authority} \neq \text{Evidence Grade}$$

- **Source Authority (Tier A–G)**: Reflects *who published the work* and their institutional governance (e.g. WHO is Tier A; a predatory blog is Tier G).
- **Evidence Grade (GRADE / Oxford CEBM)**: Reflects *what study design was used* and the empirical strength of the finding (e.g. Double-blind RCT vs Rodent model vs In-vitro binding assay).

#### The Decoupling Matrix

| Document Example | Source Authority Tier | Evidence Grade | Clinical Interpretation |
|---|---|---|---|
| In-vitro cellular study published in *Nature* | Tier D (High Authority) | `IN_VITRO` (Low Clinical Actionability) | Valid molecular mechanism, but **strictly prohibited** from being claimed as human efficacy. |
| Large-scale Phase 3 RCT published in regional journal | Tier D (Moderate Authority) | `CONTROLLED_HUMAN_RCT` (High Clinical Actionability) | High empirical evidence; requires validation of sample size and blinding. |
| Statutory Clinical Guideline issued by Ministry | Tier A (Maximum Authority) | `AUTHORITATIVE_GUIDELINE` (Consensus Practice) | High policy authority; represents standard of care. |
| Classical Unani pharmacopoeia monograph | Tier E (Classical Canonical) | `CANONICAL_TRADITIONAL` (Empirical Codex) | Centuries of clinical experiential consensus; distinct from modern biochemical trials. |

---

### 2. Quality Scoring Formula

ZMIE computes a composite **Source Reliability Index (SRI)** for every document during ingestion:

$$\text{SRI} = 0.35 \times \text{AuthorityScore} + 0.30 \times \text{MethodologyScore} + 0.20 \times \text{ReplicationScore} + 0.15 \times \text{FreshnessScore}$$

Where:
- $\text{AuthorityScore} \in [0.0, 1.0]$ based on Tier A (1.0), Tier B (0.9), Tier C (0.85), Tier D (0.75), Tier E (0.70), Tier F (0.5), Tier G (0.1).
- $\text{MethodologyScore} \in [0.0, 1.0]$ based on sample size, blinding, control groups, and risk-of-bias indicators.
- $\text{ReplicationScore} \in [0.0, 1.0]$ based on citation velocity and confirmation in systematic reviews.
- $\text{FreshnessScore} \in [0.0, 1.0]$ decaying exponentially based on half-life of medical knowledge (5 years for pharmacotherapy, 10 years for anatomy/physiology).
