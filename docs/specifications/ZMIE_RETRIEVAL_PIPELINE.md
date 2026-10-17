# ZMIE RETRIEVAL PIPELINE SPECIFICATION
## Multi-Channel Aggregation, Hard Constraints & Failure Resilience

---

### 1. Six Retrieval Channels (Sections 11-15)

1. **Lexical Retrieval Channel**:
   - BM25-style scoring with field boosting:
     $$\text{Score}_{\text{lex}} = 2.0 \times \text{TitleMatch} + 1.5 \times \text{ClaimMatch} + 1.0 \times \text{AbstractMatch}$$
2. **Semantic / Vector Retrieval Channel**:
   - Dense embeddings with cosine similarity. Quarantines Class C full-text from vector stores.
3. **Entity Retrieval Channel**:
   - Queries canonical concepts in `OntologyManager`, matching preferred names and scientific synonyms.
4. **Graph Retrieval Channel**:
   - Traverses knowledge graph edges in `MedicalKnowledgeGraphEngine`, pulling in directly connected studies and multi-hop paths.
5. **Evidence Retrieval Channel**:
   - Matches PICO contexts (Population, Intervention, Comparator, Outcome) and registers ClinicalTrials.gov protocols.
6. **Safety Retrieval Channel**:
   - Conservative retrieval focusing on Cytochrome P450 interactions, contraindications, and clinical red flags.

---

### 2. Hard Constraints Filtering (Section 16, 17)

Before candidate pools enter reranking, hard programmatic gates are enforced:
- **Tenant Scope Gate**: Strict tenant ID partition isolation.
- **Licensing Gate**: Class C documents have full-text purged; only metadata, permitted abstracts, and atomic claims are passed.
- **Retraction Quarantine Gate**: Retracted studies are blocked from general clinical evidence retrieval unless explicitly queried for retraction audits.
- **Temporal Window Gate**: Enforces user-specified `since_year` or `date_range` constraints.

---

### 3. Retrieval Failure States & Fallbacks (Sections 62-64)

The engine distinguishes distinct failure modes rather than reporting false zeros:
- `NO_EVIDENCE_FOUND`: Topic was successfully searched across all repositories, but no empirical records exist.
- `SEARCH_INCOMPLETE`: One or more external repositories (e.g. Europe PMC) timed out; results are partial.
- `SOURCE_UNAVAILABLE`: Specific provider endpoint was unreachable; fallback to local replica executed.
- `QUERY_AMBIGUOUS`: Acronym or query lacks sufficient clinical context to resolve.
