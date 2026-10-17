# ZMIE Global Medical Ontology & Terminology Evolution Engine

> **Core Foundational Axiom:**  
> **$\text{Term} \ne \text{Concept} \ne \text{Entity} \ne \text{Clinical Reality} \ne \text{Ontological Meaning} \ne \text{Evidence}$**

---

## 1. System Overview & The 10 Absolute Semantic Rules

The **ZMIE Global Medical Ontology & Terminology Evolution Engine** (Prompt 20) provides the living semantic foundation underneath the entire ZMIE platform (**Search $\rightarrow$ Research $\rightarrow$ Evidence $\rightarrow$ Causality $\rightarrow$ RWE $\rightarrow$ Clinical $\rightarrow$ Regulatory $\rightarrow$ Simulation**).

Medical language is never static. The same clinical reality is expressed across modern biomedicine, clinical practice, pharmacology, public health, traditional medicine (Unani, Ayurveda, TCM), historical medical texts, and different languages and scripts.

### The 10 Absolute Semantic Rules Enforced
1. **Rule 1**: Never assume two similar words = same concept.
2. **Rule 2**: Never assume translation = semantic equivalence.
3. **Rule 3**: Never assume historical term = modern diagnosis.
4. **Rule 4**: Never assume traditional concept = biomedical molecular entity.
5. **Rule 5**: Never assume similar clinical presentation = identical disease construct.
6. **Rule 6**: Never assume synonym = interchangeable in every context.
7. **Rule 7**: Never silently convert traditional terminology into modern biomedical terminology.
8. **Rule 8**: Never delete historical meanings because contemporary terminology changed.
9. **Rule 9**: Never overwrite an earlier definition.
10. **Rule 10**: Every important semantic mapping must retain: source, context, language, system, time, evidence, mapping type, mapping confidence, reviewer state, and version.

---

## 2. Core Architecture & Workflow

```text
RAW MEDICAL TEXT
       │
       ▼
SURFACE FORM & SCRIPT EXTRACTION (Arabic, Devanagari, Latin, etc.)
       │
       ▼
LEXICAL NORMALIZATION & VARIANT LOOKUP
       │
       ▼
CANDIDATE CONCEPTS GENERATION
       │
       ▼
CONTEXTUAL & DOMAIN DISAMBIGUATION (Neurology vs Cardiology, etc.)
       │
       ▼
RESOLVED MEDICAL CONCEPT (or EXPLICIT AMBIGUITY / UNKNOWN)
       │
       ▼
CROSS-SYSTEM MAPPING (Functional Analogy, False-Friend Guard)
       │
       ▼
GOVERNANCE & DOUBLE-REVIEW VERIFICATION
       │
       ▼
DOWNSTREAM IMPACT TRACKING (Claims, Guidelines, Studies, Cohorts)
```

---

## 3. Subsystem Components

### A. Contextual Disambiguation & Polysemy
- Disambiguates abbreviations and polysemous terms:
  - `"MS"` in domain **Neurology** $\rightarrow$ `Multiple Sclerosis` (`CON-NEURO-MS-01`).
  - `"MS"` in domain **Cardiology** $\rightarrow$ `Mitral Stenosis` (`CON-CARDIO-MS-01`).
  - `"MS"` without context $\rightarrow$ Flags `is_ambiguous=True` with explicit candidate explanations.

### B. Traditional Medicine & False-Friend Guards
- Preserves native Unani (`Mizaj`, `Akhlat`) and Ayurveda (`Prakriti`, `Dosha`) constructs.
- Prevents forced flattening: `Mizaj` is mapped to `Prakriti` as `FUNCTIONAL_CORRESPONDENCE` with detailed notes on known differences (4 humors vs 3 doshas), and triggers `FALSE_FRIEND` protection against false identity.

### C. Historical Terminology Retention
- Historical terms such as `Dropsy` (William Withering 1785) retain their 18th-century definitions and historical sources. They are mapped via `HISTORICAL_CORRESPONDENCE` without overwriting the historical scientific record.

### D. Deprecated Terminology & Downstream Impact
- Tracks modern reclassifications (e.g. `NAFLD` $\rightarrow$ `MASLD`, 2023 Multinational Delphi Consensus).
- Automatically calculates downstream impact on claims (214), studies (38), guidelines (6), and RWE cohorts (12), generating concrete remediation tasks.

### E. Governance & Human Double-Review
- AI candidate proposals are strictly restricted to `CANDIDATE` assurance state.
- Authoritative promotion mandates human expert review; high-impact mappings trigger mandatory double-review policies.

### F. License Protection & Tenancy Isolation
- Proprietary hospital or institutional vocabularies enforce export controls, blocking unauthorized external redistribution.

---

## 4. API Endpoints (`services/engine/app/api/v1/terminology_evolution.py`)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/v1/terminology/resolve` | Context-aware term resolution with uncertainty preservation |
| `POST` | `/v1/terminology/map` | Cross-system mapping with strict `NO_VALID_MAPPING` fallback |
| `GET` | `/v1/terminology/historical/{term}` | Historical terminology lookup without modern retrofitting |
| `GET` | `/v1/terminology/deprecated/{id}` | Deprecated transition record (e.g. NAFLD $\rightarrow$ MASLD) |
| `GET` | `/v1/terminology/ontologies/diff` | Structured diff between external ontology releases |
| `POST` | `/v1/terminology/impact-analysis` | Downstream impact analysis on claims, studies, and guidelines |
| `POST` | `/v1/terminology/governance/submit` | Submits candidate mapping to governance queue |
| `POST` | `/v1/terminology/governance/decision` | Records human expert review decision |
| `GET` | `/v1/terminology/licenses/verify-export` | Verifies export licensing permissions |

---

## 5. Verification & Acceptance

- **Acceptance Test Suite**: [`tests/test_terminology_evolution_acceptance.py`](file:///Users/irfanashraf/Downloads/zmie/tests/test_terminology_evolution_acceptance.py)
  - Passes all 15 tests specified in Clause 196 (Synonym, Polysemy, Abbreviation, Translation, Historical, Traditional, Partial Mapping, Unknown, Deprecation, Ontology Diff, Impact, License, Provenance, Human Review, Versioning) plus REST API verification.
- **Showcase Script**: [`tests/terminology_evolution_showcase.py`](file:///Users/irfanashraf/Downloads/zmie/tests/terminology_evolution_showcase.py)
- **Status**: **166 passing tests** across the complete repository, 209 registered FastAPI endpoints.
