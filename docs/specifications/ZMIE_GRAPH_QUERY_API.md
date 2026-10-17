# ZMIE GRAPH QUERY API SPECIFICATION
## REST Endpoints, Payloads & Traversal Contracts

---

### 1. Core Endpoints Overview

All endpoints are mounted under the `/v1/graph` and `/v1/ontology` namespaces:

```text
┌──────────────────────────────────────┬────────┬────────────────────────────────────────┐
│ Endpoint                             │ Method │ Description                            │
├──────────────────────────────────────┼────────┼────────────────────────────────────────┤
│ /v1/graph/entities/{id}              │ GET    │ Full concept passport & aliases        │
│ /v1/graph/entities/{id}/relationships│ GET    │ Connected knowledge & evidence edges   │
│ /v1/graph/entities/{id}/timeline     │ GET    │ Chronological evidence milestones      │
│ /v1/graph/relations/{id}             │ GET    │ Rich relationship edge details         │
│ /v1/graph/relations/{id}/evidence    │ GET    │ Empirical studies grounding the edge   │
│ /v1/graph/relations/{id}/conflicts   │ GET    │ Contradicting trials & disagreement    │
│ /v1/graph/claims/{id}/trace          │ GET    │ Reverse provenance trace to paragraph  │
│ /v1/graph/why-relationship           │ POST   │ "Why this relationship exists?"        │
│ /v1/graph/what-am-i-missing          │ POST   │ "What am I missing?" gap engine        │
│ /v1/graph/path                       │ POST   │ Controlled multi-hop path finder       │
│ /v1/graph/retract-impact             │ POST   │ Downstream retraction impact analysis  │
│ /v1/graph/knowledge-diff             │ GET    │ Release delta between two versions     │
│ /v1/graph/grounding-packet           │ GET    │ Structured packet for AI synthesis     │
│ /v1/ontology/concepts                │ GET    │ List concepts filtered by tradition    │
│ /v1/ontology/mappings                │ GET    │ Cross-system mappings & rationales     │
│ /v1/ontology/compare                 │ GET    │ 4-system comparative lens              │
└──────────────────────────────────────┴────────┴────────────────────────────────────────┘
```

---

### 2. Sample Payloads

#### `POST /v1/graph/why-relationship`
```json
// Request
{
  "relation_id": "REL-BERB-T2D-001"
}

// Response
{
  "relation_id": "REL-BERB-T2D-001",
  "subject_name": "Berberine",
  "predicate": "MAY_TREAT",
  "object_name": "Type 2 Diabetes Mellitus",
  "medical_system": "modern_biomedicine",
  "knowledge_status": "ESTABLISHED",
  "evidence_level": "E6_controlled_clinical_evidence",
  "supporting_studies_count": 2,
  "contradicting_studies_count": 1,
  "primary_populations": ["Human adults with Type 2 Diabetes Mellitus"],
  "disagreement_reasons": ["different dose (500mg tid vs 300mg qd)"],
  "causality_warning": "CAUSALITY SAFEGUARD: Predicate 'MAY_TREAT' represents correlation/observed association."
}
```
