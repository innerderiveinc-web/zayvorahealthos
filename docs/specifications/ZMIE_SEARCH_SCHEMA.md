# ZMIE SEARCH DATA CONTRACTS & PAYLOAD SCHEMAS
## Structured Search Inputs, Candidate Records & Output Contracts

---

### 1. Request Schemas

```json
{
  "query": "What is the human clinical evidence for berberine in metabolic health?",
  "mode": "evidence",
  "filters": {
    "since_year": 2020,
    "medical_system": "modern_biomedicine"
  },
  "user_id": "USR-INVESTIGATOR-01"
}
```

---

### 2. Candidate Record Schema (`RetrievalCandidate`)

```json
{
  "candidate_id": "CAND-PMID:18442638",
  "document_id": "PMID:18442638",
  "title": "Efficacy of Berberine in Patients with Type 2 Diabetes Mellitus",
  "snippet_or_passage": "Berberine lowered fasting blood glucose and HbA1c significantly in adult diabetic patients...",
  "source_id": "SRC-NLM-001",
  "source_organization": "National Library of Medicine / PubMed",
  "authority_tier": "tier_b_biomedical_repo",
  "license_class": "permitted_open_access",
  "publication_year": 2008,
  "medical_system": "modern_biomedicine",
  "study_type": "double_blind_rct",
  "evidence_level": "E6_controlled_clinical_evidence",
  "is_retracted": false,
  "paragraph_anchor_hash": "8a1c90df44b1234a"
}
```

---

### 3. Response Schema (`SearchModeResult`)

```json
{
  "mode": "evidence",
  "query": "What is the human clinical evidence for berberine in metabolic health?",
  "total_results": 2,
  "ranked_results": [
    {
      "candidate": { ... },
      "final_score": 0.885,
      "component_scores": {
        "lexical": 0.8,
        "entity": 0.95,
        "authority": 0.9,
        "evidence": 1.0,
        "graph": 0.9,
        "freshness": 0.72
      },
      "why_this_result": "High-quality controlled clinical evidence (double_blind_rct) | Authoritative statutory repository (NLM)",
      "evidence_badge": "E6_controlled_clinical_evidence",
      "authority_badge": "NLM / PubMed (tier_b_biomedical_repo)"
    }
  ],
  "rag_packet": { ... },
  "execution_time_ms": 2.85
}
```
