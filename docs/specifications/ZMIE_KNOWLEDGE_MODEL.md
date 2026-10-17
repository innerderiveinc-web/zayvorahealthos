# ZMIE Knowledge & Evidence Object Model

## 1. The Core Transformation Principle
Raw documents are never used directly as answer sources. Documents are parsed and decomposed into atomic, verifiable knowledge objects:

```
DOCUMENT (PDF / XML / Codices)
    ↓
EXTRACTED CLAIMS
    ↓
PICO EVIDENCE CONTEXT
    ↓
ENTITIES & BIOMARKERS
    ↓
RELATIONSHIP EDGES
    ↓
KNOWLEDGE GRAPH
```

---

## 2. The Atomic Unit: Claim Passport (`claim_passports`)
Every medical and scientific fact in ZMIE is anchored by an immutable **Claim Passport**:
- `claim_id`: Persistent UUID (e.g., `CLM-2026-X9921`).
- `claim_text`: Normalized atomic medical assertion.
- `source_id`: Foreign key to the immutable Source Registry.
- `document_id`: Foreign key to Document metadata (DOI, PMID, OpenAlex Work ID).
- `location_id`: Exact structural pointer (section name, page number, paragraph hash).
- `medical_system`: Epistemological tradition (`modern_biomedicine`, `unani_tibb`, `ayurveda`, `tcm`).
- `evidence_tier`: 12-grade classification (`controlled_human_evidence`, `systematic_review`, `preclinical_in_vivo`, `canonical_traditional_claim`, etc.).
- `context` (PICO):
  - `population_species`: Human, animal, or cell line.
  - `condition_or_phenotype`: Target pathology or clinical state.
  - `intervention_agent`: Pharmacological compound, standardized extract, or procedure.
  - `dose`, `route`, `duration`, `comparator`.
- `entailment_score`: NLI entailment metric ($0.0 \dots 1.0$) verifying support in the cited passage.
- `retraction_status`: Real-time Crossref / Retraction Watch monitoring state.

---

## 3. Evidence Status Hierarchy (Section 17)
1. `AUTHORITATIVE`: Official guidelines and national regulatory directives.
2. `GUIDELINE_SUPPORTED`: Recognized specialty association recommendations.
3. `SYSTEMATIC_REVIEW_SUPPORTED`: Cochrane / GRADE high-confidence meta-analyses.
4. `CONTROLLED_HUMAN_RCT`: Double-blind or randomized clinical trials.
5. `OBSERVATIONAL_HUMAN`: Prospective cohorts and registry evaluations.
6. `PRECLINICAL_IN_VIVO`: Animal models (never automatically promoted to human clinical evidence).
7. `IN_VITRO`: Mechanistic cell assays.
8. `COMPUTATIONAL`: In-silico docking and network pharmacology predictions.
9. `CANONICAL_TRADITIONAL`: Validated classical treatises (Al-Qanun fi al-Tibb, Charaka Samhita).
10. `HISTORICAL_USE`: Documented multi-century empirical pharmacopeial usage.
11. `CONFLICTING`: Statistically diverging outcomes across comparable trial designs.
12. `INSUFFICIENT`: Underpowered sample sizes or preliminary pilot data.
13. `UNKNOWN`: Unstudied or unmapped clinical questions.
