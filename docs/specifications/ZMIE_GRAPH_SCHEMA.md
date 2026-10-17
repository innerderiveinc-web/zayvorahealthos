# ZMIE GRAPH SCHEMA SPECIFICATION
## Node & Edge Schemas across Knowledge, Evidence and Provenance Layers

---

### 1. Node Types & Property Schemas

#### A. Canonical Concept Node (`CanonicalConcept`)
- **`concept_id`** (`string`, PK): Canonical identifier (e.g. `CON-MOD-IBS-001`, `CON-UNANI-MIZAJ-DAMWI`).
- **`canonical_name`** (`string`): Primary English or scientific designation.
- **`medical_system`** (`enum`): `modern_biomedicine`, `unani_tibb`, `ayurveda`, `traditional_chinese_medicine`, `siddha`.
- **`entity_class`** (`string`): Domain class (`Condition`, `Disease`, `Symptom`, `Compound`, `Plant`, `Mizaj`, `Dosha`, `Dravya`, `Pathway`, `Protein`).
- **`definition`** (`string`): Canonical definition preserved in original epistemic context.
- **`lifecycle_status`** (`enum`): `ACTIVE`, `DEPRECATED`, `SUPERSEDED`, `MERGED`, `SPLIT`.
- **`parent_concept_ids`** (`list[string]`): Structural hierarchical links.

#### B. Medical Term Node (`MedicalTerm`)
- **`term_id`** (`string`, PK): Persistent term ID.
- **`concept_id`** (`string`, FK): Associated canonical concept.
- **`term_text`** (`string`): Text string in native script.
- **`language`** (`string`): ISO 639-1 code (`en`, `ar`, `ur`, `fa`, `sa`, `hi`, `zh`, `la`).
- **`script`** (`string`): Writing system (`Latin`, `Arabic/Nastaliq`, `Devanagari`, `Simplified Hanzi`).
- **`synonym_type`** (`enum`): `EXACT_SYNONYM`, `ABBREVIATION`, `HISTORICAL_NAME`, `TRANSLITERATION`, `TRANSLATION`.
- **`is_preferred`** (`boolean`): Preferred term indicator for search ranking.

#### C. Evidence Node (`EvidenceObject`)
- **`evidence_id`** (`string`, PK): Persistent evidence ID.
- **`claim_id`** (`string`, FK): Associated atomic claim.
- **`study_type`** (`enum`): `DOUBLE_BLIND_RCT`, `OPEN_LABEL_RCT`, `PROSPECTIVE_COHORT`, `ANIMAL_IN_VIVO`, `CELL_LINE_IN_VITRO`.
- **`evidence_level`** (`enum`): $E_0$ through $E_6$.
- **`pico_context`** (`JSON`): Population species, condition, intervention agent, comparator.
- **`effect_measure`** (`string`): e.g. "HbA1c Reduction", "Relative Risk".
- **`effect_value`** (`float`): Quantitative result.
- **`p_value`** (`float`): Statistical significance.
- **`sample_size`** (`integer`): Cohort size ($n$).
- **`paragraph_anchor_hash`** (`string`): 16-character SHA-256 anchor.

---

### 2. Edge Schema (`RelationshipEdge`)

Edges in ZMIE are first-class structured objects with rich qualifiers:

```json
{
  "relation_id": "REL-BERB-T2D-001",
  "subject_id": "CON-MOD-BERBERINE-001",
  "predicate": "MAY_TREAT",
  "object_id": "CON-MOD-T2D-001",
  "medical_system": "modern_biomedicine",
  "inference_type": "SUPPORTED_RELATION",
  "temporal_status": "ACTIVE",
  "knowledge_status": "ESTABLISHED",
  "qualifiers": {
    "population": "Adults with Type 2 Diabetes",
    "dose": "500 mg oral tid",
    "duration": "12-16 weeks",
    "species": "human",
    "study_type": "double_blind_rct"
  },
  "supporting_claim_ids": ["CLM-RCT-BERB-01", "CLM-RCT-BERB-02"],
  "contradicting_claim_ids": ["CLM-RCT-BERB-03"],
  "evidence_level": "E6_controlled_clinical_evidence",
  "confidence_dimensions": {
    "source_authority": 0.95,
    "evidence_strength": 0.88,
    "clinical_relevance": 0.90
  }
}
```
