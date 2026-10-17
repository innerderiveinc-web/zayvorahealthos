# ZMIE Truth, Claim Validation, Citation Verification & Safety Firewall Documentation Suite

This document formalizes the 16 enterprise architectural deliverables required under Prompt 7 of the ZAYVORA Medical Intelligence Engine™ (ZMIE) Standalone Enterprise Specification.

---

## 1. ZMIE_TRUTH_FIREWALL.md
### Central Architecture & Quality Gate
The Truth Firewall serves as the immutable quality gate between AI generation and user output.
```text
GENERATED OUTPUT
  ↓
CLAIM EXTRACTION & SPLITTING
  ↓
CLAIM CLASSIFICATION & RISK SCORING
  ↓
CITATION MATCHING & NUMERICAL ENTAILMENT
  ↓
CAUSALITY & EVIDENCE LADDER FIREWALL
  ↓
CROSS-SYSTEM EQUIVALENCE CHECK
  ↓
RETRACTION & SAFETY FIREWALL
  ↓
FINAL QUALITY GATE: PASS | MODIFY | BLOCK
```

---

## 2. ZMIE_CLAIM_VALIDATION.md
### Claim Unit of Verification & Decomposition
- **Unit of Verification**: Statements are broken down into atomic assertions via `AtomicClaimEngine`.
- **Normalization**: Normalized into `NormalizedClaim` objects capturing `subject`, `predicate`, `object`, `population`, `intervention`, `comparator`, `outcome`, `effect`, and `context`.
- **Typology**: 20 controlled claim types (`FACTUAL`, `NUMERICAL`, `STATISTICAL`, `CLINICAL`, `SAFETY`, `CAUSAL`, `CORRELATIONAL`, `TRADITIONAL_MEDICINE`, `GUIDELINE`, etc.).
- **Risk Tiers**: `LOW_RISK`, `MEDIUM_RISK`, `HIGH_RISK`, `CRITICAL_RISK` (pregnancy, toxicities, unproven cure claims).

---

## 3. ZMIE_CITATION_VERIFICATION.md
### Deterministic & Substantive Entailment
- **Deterministic Validation**: Format verification of real DOIs (`10.xxxx`), PMIDs, ClinicalTrials.gov identifiers (`NCTxxxx`), and classical accessions (`CCRUM-`, `CCRAS-`).
- **Substantive Entailment**: Requires semantic and lexical overlap ($\ge 55\%$) with cited anchor text; rejects papers that merely mention the topic without supporting the specific claim.
- **Zero Citation Laundering Guarantee**: Fabricated references are rejected with an immediate hard block.

---

## 4. ZMIE_CITATION_POLICY.md
### Citation Coverage & Placement Rules
- Every clinical assertion, numerical percentage, and pharmacological effect must possess an active citation or be explicitly classified as `INFERENCE` or `HYPOTHESIS`.
- Citation objects are linked down to paragraph anchor hashes and document versions.

---

## 5. ZMIE_CONTRADICTION_ENGINE.md
### Conflict Detection Without Forced Consensus
- Identifies trial discrepancies across 10 contradiction classes (`DIRECT_CONTRADICTION`, `POPULATION_CONTRADICTION`, `DOSE_CONTRADICTION`, `FORMULATION_CONTRADICTION`, etc.).
- When studies conflict, the firewall mandates surfacing both perspectives with root driver explanations (e.g., CYP metabolizer status, dietary differences).

---

## 6. ZMIE_CAUSALITY_FIREWALL.md
### Hard Protection Against Causal Overreach
- Strictly enforces: **Association $\ne$ Causation**.
- Rejects words such as `cures`, `treats`, `eliminates`, or `reverses` unless grounded in definitive Phase III trial consensus.
- Automatically generates conservative, scientifically compliant rewrites (e.g., replacing "cures" with "is associated with clinically meaningful improvement in").

---

## 7. ZMIE_SAFETY_VERIFICATION.md
### Pharmacovigilance & Special Populations
- Elevates safety verification for vulnerable cohorts: pregnancy, lactation, renal impairment (eGFR < 30), hepatic impairment, and pediatric populations.
- Audits drug-herb interactions and CYP450 enzyme inhibition.

---

## 8. ZMIE_TRADITIONAL_CLAIM_POLICY.md
### Preservation of Traditional Paradigms
- Compendial assertions from Unani Tibb and Ayurveda preserve their source type (`CANONICAL_TRADITIONAL`).
- Traditional codex assertions cannot be silently upgraded to modern clinical efficacy claims.

---

## 9. ZMIE_CROSS_SYSTEM_VALIDATION.md
### Equivalence Firewall & Qualified Analogies
- Rejects false 1:1 equivalences equating holistic humoral concepts directly with reductionist biochemical markers (e.g., "Mizaj is equivalent to insulin resistance").
- Enforces qualified phraseology: "shares conceptual parallels with" or "is proposed as an analogy to".

---

## 10. ZMIE_RETRACTION_VALIDATION.md
### Hard Retraction Blocking & Impact Propagation
- Retracted publications are immediately quarantined.
- Cascading impact analysis: when a document is flagged as retracted, all associated claims, relationships, research reports, and cached answers are marked for immediate revalidation and cache eviction.

---

## 11. ZMIE_NUMERICAL_VALIDATION.md
### Numerical & Statistical Context Precision
- Exact extraction and comparison of sample sizes ($n$), percentages, p-values, hazard ratios, and dosages.
- Discrepancies between claim numbers and cited text trigger immediate verification failure.

---

## 12. ZMIE_RESEARCH_REPORT_GATE.md
### Publication Quality Gates
- Enforces full verification across all claims before a deep research report can be finalized or published.
- Computes real metrics: `claims_checked`, `supported`, `partially_supported`, `citation_failures`, `reproducibility_hash`.

---

## 13. ZMIE_VERIFICATION_API.md
### REST Endpoints Reference
- `POST /v1/verify/answer`: Full verification pipeline for generated answers.
- `POST /v1/verify/claim`: Verification of individual atomic assertions.
- `POST /v1/verify/citation`: Validation of citation identifiers and passage entailment.
- `POST /v1/verify/retraction-alert`: Retraction registration and cascading impact analysis.

---

## 14. ZMIE_VERIFICATION_GOVERNANCE.md
### Roles & Human Review Escalation
- Segregation of duties: AI generates draft, Truth Firewall verifies, human reviewers approve high-risk escalations.
- No AI self-approval on high-risk clinical recommendations.

---

## 15. ZMIE_VERIFICATION_EVALUATION.md
### Benchmarks & Metric Thresholds
- Evaluated via `test_truth_firewall_acceptance.py` with 100% pass rate.
- Core metrics tracked: Claim Support Accuracy, Citation Correctness, Retraction Recall, and False Causality Elimination.

---

## 16. ZMIE_VERIFICATION_REDTEAM.md
### Adversarial Resistance Testing
- Validated against adversarial probes: fabricated DOIs, altered numbers, causal overstatements, and false traditional equivalences.
- Server-side validation is authoritative; client-side flags cannot override a `BLOCK` or `MODIFY` verdict.
