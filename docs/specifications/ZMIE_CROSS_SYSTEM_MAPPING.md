# ZMIE CROSS-SYSTEM MAPPING & COMPARATIVE LENS SPECIFICATION
## Epistemic Harmonization without Reductive Flattening

---

### 1. The 10-Tier Mapping Relationship Taxonomy (Section 28)

Cross-system edges connecting concepts between distinct medical traditions are restricted to ten rigorous types:

```text
┌────────────────────────────────────────────────────────────────────────┐
│             ZMIE CROSS-SYSTEM MAPPING RELATIONSHIP TAXONOMY            │
├────────────────────────────┬───────────────────────────────────────────┤
│ Mapping Type               │ Exact Operational Definition              │
├────────────────────────────┼───────────────────────────────────────────┤
│ 1. EXACT_EQUIVALENCE       │ Strict taxonomic, botanical, or chemical  │
│                            │ identity (e.g. Berberis aristata =        │
│                            │ Darhald = Daruharidra).                   │
├────────────────────────────┼───────────────────────────────────────────┤
│ 2. CLOSE_EQUIVALENCE       │ Minor diagnostic divergence with ~95%     │
│                            │ clinical overlap.                         │
├────────────────────────────┼───────────────────────────────────────────┤
│ 3. PARTIAL_OVERLAP         │ Shares symptoms or targets, but distinct  │
│                            │ diagnostic boundaries.                    │
├────────────────────────────┼───────────────────────────────────────────┤
│ 4. RELATED_CONCEPT         │ Clinically relevant connection within the │
│                            │ same organ or functional axis.            │
├────────────────────────────┼───────────────────────────────────────────┤
│ 5. FUNCTIONAL_ANALOGY      │ Parallel physiological role across        │
│                            │ axiomatic paradigms (e.g. Gastric Motility│
│                            │ ↔ Quwwat-e-Hazima ↔ Jatharagni ↔ Pi/Wei). │
├────────────────────────────┼───────────────────────────────────────────┤
│ 6. HISTORICAL_ASSOCIATION  │ Textual cross-reference in historical     │
│                            │ scholarly translations.                   │
├────────────────────────────┼───────────────────────────────────────────┤
│ 7. RESEARCH_HYPOTHESIS     │ Active clinical or in-silico trial        │
│                            │ investigating hypothetical alignment.     │
├────────────────────────────┼───────────────────────────────────────────┤
│ 8. NO_VALIDATED_MAPPING    │ Valid concept in Tradition A with no      │
│                            │ counterpart in Tradition B.               │
├────────────────────────────┼───────────────────────────────────────────┤
│ 9. CONFLICTING             │ Fundamental theoretical opposition        │
│                            │ between traditions.                       │
├────────────────────────────┼───────────────────────────────────────────┤
│ 10. UNKNOWN                │ Insufficient comparative literature.      │
└────────────────────────────┴───────────────────────────────────────────┘
```

---

### 2. Safeguard Against False Equivalence (Section 88)

The engine implements a hard programmatic firewall:
- A relation marked as `FUNCTIONAL_ANALOGY` or `PARTIAL_OVERLAP` is **strictly prohibited from being rendered as an identity ($A = B$)** in user-facing search results or AI summaries.
- The UI and API must explicitly state:
  > *"Concepts share parallel functional roles but are grounded in distinct axiomatic philosophies. Do not treat as interchangeable biological identities."*

---

### 3. Governed Alignment Workflow (Section 30)

```text
DISCOVER ──> CANDIDATE MATCH ──> SEMANTIC COMPARISON ──> CONTEXT COMPARISON
                                                                │
APPROVED MAPPING <── HUMAN EXPERT REVIEW <── EVIDENCE CHECK <───┘
```
All approved mappings require sign-off by credentialed experts across both traditions (e.g. BUMS/MD Unani and BAMS/MD Ayurveda).
