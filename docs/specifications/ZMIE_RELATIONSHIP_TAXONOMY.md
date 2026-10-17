# ZMIE RELATIONSHIP TAXONOMY & QUALIFIER MODEL
## Controlled Predicates, Clinical Qualifiers & Causality Protections

---

### 1. Controlled Predicates Taxonomy (Section 10)

Free-text relation names are strictly prohibited in the governed graph. All edges must use controlled predicates categorized into six domains:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ZMIE CONTROLLED PREDICATE TAXONOMY                   │
├─────────────────────┬──────────────────────────────────────────────────┤
│ Category            │ Predicates                                       │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Clinical Efficacy   │ TREATS, MAY_TREAT, SUPPORTS_TREATMENT_OF,        │
│ & Prevention        │ PREVENTS, MAY_PREVENT, INDICATED_FOR             │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Etiology & Disease  │ CAUSES, MAY_CAUSE, CONTRIBUTES_TO, PREDISPOSES_TO│
│ Manifestations      │ ASSOCIATED_WITH, HAS_SYMPTOM, HAS_SIGN,          │
│                     │ HAS_BIOMARKER                                    │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Clinical Safety     │ CONTRAINDICATED_IN, INTERACTS_WITH,              │
│ & Pharmacokinetics  │ INCREASES_EFFECT, DECREASES_EFFECT               │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Molecular Mechanism │ TARGETS, ACTS_ON, MODULATES, INHIBITS,           │
│ & Pharmacodynamics  │ ACTIVATES, HAS_TARGET                            │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Compositional       │ PART_OF, LOCATED_IN, DERIVED_FROM, CONTAINS,     │
│ & Anatomical        │ COMPOSED_OF                                      │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Classical / Humoral │ HAS_MIZAJ, HAS_AFAAL, HAS_MIZAJ_OF_DRUG,         │
│ Actions             │ USED_IN_FORMULATION, USED_FOR                    │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Cross-System        │ SIMILAR_TO, RELATED_TO, ANALOGOUS_TO, MAPPED_TO, │
│ Alignment           │ PARTIALLY_OVERLAPS                               │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Evidence & Logic    │ SUPPORTED_BY, CONTRADICTED_BY, QUALIFIED_BY      │
└─────────────────────┴──────────────────────────────────────────────────┘
```

---

### 2. Relationship Qualifiers (Section 11)

No edge is presented as universally valid without its context. Edges carry structured qualifiers:
- **`population`**: Cohort specification (e.g. "Human adults with Type 2 Diabetes", "Post-menopausal females").
- **`dose`**: Specific posology (e.g. "500 mg tid").
- **`route`**: Administration route (oral, intravenous, topical, decoction).
- **`formulation`**: Standardized extract, crude powder, nano-emulsion, classical majun.
- **`duration`**: Exposure timeline (acute 24h, 12 weeks, chronic).
- **`species`**: `human`, `rat`, `mouse`, `cell_line`.
- **`endpoint`**: Target measured parameter (HbA1c, FPG, AST/ALT, inflammatory markers).

---

### 3. Causality Protection (Section 56)

- A path of association edges ($A \xrightarrow{\text{ASSOCIATED\_WITH}} B \xrightarrow{\text{ASSOCIATED\_WITH}} C$) **never implies that $A$ causes $C$**.
- Causal predicates (`CAUSES`, `PREVENTS`) require either:
  1. High-tier double-blind randomized controlled clinical trials ($E_6$) with documented mechanism.
  2. Authoritative statutory guideline consensus ($E_6+$).
- All other relations use tentative or correlative predicates (`MAY_TREAT`, `ASSOCIATED_WITH`, `CONTRIBUTES_TO`).
