# ZMIE QUERY UNDERSTANDING & STRUCTURING SPECIFICATION
## Intent Classification, Entity Disambiguation & False-Premise Neutralization

---

### 1. Structured Query Object Schema (Section 5)

Every incoming search query is parsed into a first-class `StructuredQuery` object:

```json
{
  "query": "What is the evidence for berberine in metabolic health?",
  "normalized_neutral_query": "What is the evidence for berberine in metabolic health?",
  "is_false_premise": false,
  "intents": ["EVIDENCE", "TREATMENT_RESEARCH"],
  "entities": ["Berberine", "Type 2 Diabetes Mellitus"],
  "conditions": ["Type 2 Diabetes Mellitus"],
  "interventions": ["Berberine"],
  "medical_systems": ["modern_biomedicine"],
  "date_range": {
    "start_year": null,
    "end_year": null,
    "since_year": null
  },
  "population": {
    "species": "human"
  },
  "depth": "evidence",
  "disambiguation_status": "RESOLVED",
  "expanded_terms": ["Berberine", "Berberine hydrochloride", "Darhald", "Daruharidra", "Huang Lian"]
}
```

---

### 2. Controlled Intent Classification (Section 6)

The engine classifies queries across seventeen controlled intents:
- `DEFINITION`, `EDUCATION`, `SYMPTOM_INFORMATION`, `EVIDENCE`, `TREATMENT_RESEARCH`, `SAFETY`, `INTERACTION`, `GUIDELINE`, `TRIAL`, `COMPARISON`, `TRADITIONAL_MEDICINE`, `MECHANISM`, `PHARMACOLOGY`, `FORMULATION`, `RESEARCH`, `DEEP_RESEARCH`, `SOURCE_LOOKUP`.

---

### 3. Entity Disambiguation (Section 8)

When queries contain ambiguous medical acronyms without sufficient contextual clues:
- Example: `"MS"` $\rightarrow$ Marked as `AMBIGUOUS`.
- Disambiguation candidates returned:
  1. *Multiple Sclerosis* (Neurology / Autoimmune)
  2. *Morphine Sulfate* (Analgesic / Pharmacology)
  3. *Mitral Stenosis* (Cardiovascular Valvular Pathology)
- Programmatic Rule: The engine **never silently chooses** a clinically significant interpretation when context is missing.

---

### 4. False-Premise Neutralization (Section 70)

If a user enters a query with an unverified clinical premise (e.g. *"What evidence proves that compound X cures disease Y?"*):
1. Flagged as `is_false_premise = True`.
2. Converted internally into neutral empirical inquiry:
   $$\text{"What evidence exists regarding compound X and disease Y?"}$$
3. The engine searches evidence objectively without presupposing positive curative efficacy.
