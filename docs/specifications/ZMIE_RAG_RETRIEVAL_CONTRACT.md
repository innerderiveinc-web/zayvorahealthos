# ZMIE RAG RETRIEVAL CONTRACT & CITATION ARCHITECTURE
## Structured AI Packets, Paragraph Anchors & Zero Citation Laundering

---

### 1. The RAG Packet Contract (Section 80, 81)

ZMIE strictly prohibits sending ungrounded "top-20 text chunks" to downstream AI models. The retrieval engine emits a structured `RAGEvidencePacket`:

```json
{
  "query": "What is the evidence for berberine in metabolic health?",
  "intents": ["EVIDENCE", "TREATMENT_RESEARCH"],
  "entities": ["Berberine", "Type 2 Diabetes Mellitus"],
  "primary_citations": [
    {
      "citation_id": "CIT-01",
      "document_id": "PMID:18442638",
      "title": "Efficacy of Berberine in Patients with Type 2 Diabetes Mellitus",
      "source_organization": "National Library of Medicine / PubMed",
      "authority_tier": "tier_b_biomedical_repo",
      "license_class": "permitted_open_access",
      "paragraph_anchor_hash": "8a1c90df44b1234a"
    }
  ],
  "passages": [
    {
      "passage_id": "PSG-01",
      "citation_id": "CIT-01",
      "text_content": "Berberine lowered fasting blood glucose and HbA1c significantly in adult diabetic patients...",
      "paragraph_anchor_hash": "8a1c90df44b1234a",
      "evidence_level": "E6_controlled_clinical_evidence",
      "study_type": "double_blind_rct"
    }
  ],
  "supporting_evidence": [
    {
      "citation_id": "CIT-01",
      "finding": "HbA1c lowered by 1.2% at 3 months (p=0.001)",
      "evidence_level": "E6_controlled_clinical_evidence"
    }
  ],
  "contradicting_evidence": [
    {
      "citation_id": "CIT-02",
      "finding": "Crude unstandardized extract (300mg qd) showed no significant reduction in morbidly obese cohort.",
      "disagreement_factor": "Dose and crude unstandardized extract"
    }
  ],
  "safety_evidence": [
    {
      "citation_id": "CIT-03",
      "finding": "Mechanism-based competitive inhibition of CYP3A4"
    }
  ],
  "explicit_uncertainties": [
    "Longitudinal trials beyond 36 months duration in diverse geographical populations.",
    "Pediatric pharmacokinetic and safety profiles (strictly missing)."
  ]
}
```

---

### 2. Citation-First Guarantee (Section 94)

Downstream AI models are provided with pre-computed, verified citation objects possessing deterministic paragraph anchor hashes. The AI model **never generates or looks up DOIs/PMIDs post-hoc**, permanently eliminating citation laundering.
