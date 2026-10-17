# ZMIE INGESTION ARCHITECTURE SPECIFICATION
## The 14-Stage Governed Acquisition Lifecycle Pipeline

---

### 1. Architectural Pipeline Diagram

```text
┌───────────┐    ┌──────────┐    ┌─────────┐    ┌───────────────┐
│ DISCOVER  │───>│ IDENTIFY │───>│ VERIFY  │───>│ LICENSE CHECK │
└───────────┘    └──────────┘    └─────────┘    └───────┬───────┘
                                                        │
┌───────────┐    ┌──────────┐    ┌─────────┐    ┌───────▼───────┐
│  VERSION  │<───│   HASH   │<───│ ACQUIRE │<───│ ACCESS CHECK  │
└─────┬─────┘    └──────────┘    └─────────┘    └───────────────┘
      │
┌─────▼─────┐    ┌──────────┐    ┌───────────┐  ┌───────────────┐
│   PARSE   │───>│ EXTRACT  │───>│ NORMALIZE │─>│   VALIDATE    │
└───────────┘    └──────────┘    └───────────┘  └───────┬───────┘
                                                        │
                                 ┌─────────┐    ┌───────▼───────┐
                                 │ RELEASE │<───│     INDEX     │
                                 └─────────┘    └───────────────┘
```

---

### 2. Stage-by-Stage Specifications

1. **Stage 1: DISCOVER**
   - Ingestion adapters query federated APIs (OpenAlex, Europe PMC, AYUSH, ClinicalTrials.gov) with biomedical search queries, MeSH tags, and traditional nomenclature.
2. **Stage 2: IDENTIFY**
   - Canonical identifiers are extracted and verified (DOI, PMID, PMCID, NCT ID, Codex URN).
3. **Stage 3: VERIFY**
   - Evaluates source organization authority, SSL certificate validity, and registered Tier (Tier A through Tier G).
4. **Stage 4: LICENSE CHECK**
   - Evaluates publisher license strings against the ZMIE Intellectual Property matrix to classify into Class A, B, or C.
5. **Stage 5: ACCESS CHECK**
   - Checks institutional contracts or open endpoints. Rejects unauthorized bypass of access controls.
6. **Stage 6: ACQUIRE**
   - Ingests raw XML, HTML, PDF, or JSON payload into isolated temporary buffer.
7. **Stage 7: HASH (SHA-256)**
   - Computes 256-bit cryptographic content hash (`raw_hash_sha256`) of the acquired document before any transformation.
8. **Stage 8: VERSION**
   - Compares hash with historical versions via `DocumentVersionTracker`. Categorizes as `NEW`, `UPDATED`, `UNCHANGED`, or `SUPERSEDED`.
9. **Stage 9: PARSE**
   - Decomposes document structure into Sections, Headings, Paragraphs, Tables, and Figures. Generates deterministic paragraph anchor hashes.
   - **Enforces Class C Quarantine**: If Class C, strips all full-text body paragraphs; retains only abstract and metadata.
10. **Stage 10: EXTRACT**
    - Identifies atomic medical assertions, entities, and PICO contexts (Population, Intervention, Comparator, Outcome).
11. **Stage 11: NORMALIZE**
    - Maps chemical names, herbs, and pathologies to canonical ontology concepts without epistemic flattening.
12. **Stage 12: VALIDATE**
    - Performs cross-source claim entailment validation and checks for retraction flags via Retraction Watch / Crossref.
13. **Stage 13: INDEX**
    - Writes normalized records to PostgreSQL relational store, generates dense embeddings, and commits nodes/edges to the Knowledge Graph.
14. **Stage 14: RELEASE**
    - Publishes the versioned commit into the production queryable index, triggering telemetry events and subscriber notifications.
