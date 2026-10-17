# ZMIE EVIDENCE-AWARE RETRIEVAL SPECIFICATION
## PICO Matching, Evidence Ladder Prioritization & Contradiction Awareness

---

### 1. PICO Context Matching (Section 21)

When answering therapeutic or clinical questions, the Evidence Retrieval Channel extracts and matches PICO dimensions:
- **Population (P)**: Human adult cohorts prioritized over animal or cell-line models.
- **Intervention (I)**: Active molecule, standardized fraction, or classical formula.
- **Comparator (C)**: Placebo, active pharmacological control, or standard of care.
- **Outcome (O)**: Clinically relevant endpoints (HbA1c, cardiovascular events, mortality) prioritized over surrogate in-vitro binding markers.

---

### 2. Contradiction-Aware Retrieval (Section 34)

When scientific literature contains divergent or conflicting findings:
- The engine **actively seeks out and retrieves both supporting and contradicting studies**.
- Rejects confirmation bias: avoids returning only the top-scoring positive trial.
- Pairs positive trials (e.g. *Metabolism 2008* $E_6$ trial showing $-1.2\%$ HbA1c reduction) with non-significant or conflicting pilot trials (e.g. *JEP 2023* low-dose crude extract trial).
- Explains the methodological drivers of disagreement (dose, extraction purity, sample size, baseline severity).
