# ZMIE SEARCH & RETRIEVAL INTELLIGENCE ARCHITECTURE
## Multi-Channel Hybrid Retrieval Subsystem Specification

---

### 1. Architectural Philosophy

Traditional search engines ask:
> *"Which documents contain these keywords?"*

ZMIE asks:
> **"Which governed knowledge, empirical evidence, and source material most directly answers this question in this clinical context, what conflicts exist, and what critical information is still missing?"**

```text
USER QUESTION
      │
      ▼
QUERY UNDERSTANDING ──> INTENT CLASSIFICATION ──> FALSE PREMISE NEUTRALIZER
      │
      ▼
QUERY STRUCTURING & CONTROLLED EXPANSION (Synonyms, Transliterations, Traditions)
      │
      ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  MULTI-CHANNEL HYBRID RETRIEVAL POOL                   │
├──────────────┬──────────────┬──────────────┬──────────────┬────────────┤
│ 1. LEXICAL   │ 2. SEMANTIC  │ 3. ENTITY    │ 4. GRAPH     │ 5. EVIDENCE│
│ (BM25/Boost) │ (Embeddings) │ (Taxonomies) │ (Multi-Hop)  │ (PICO/E0-6)│
└──────────────┴──────────────┴──────────────┴──────────────┴────────────┘
      │
      ▼
HARD CONSTRAINTS FILTER (Tenant scope, License Class A/B/C, Retraction quarantine, Dates)
      │
      ▼
CANONICAL DEDUPLICATION (DOI, PMID, Trial ID, Content Hash)
      │
      ▼
MULTI-DIMENSIONAL RERANKING (Relevance, Evidence Level, Source Authority, Freshness)
      │
      ▼
CONTEXT WINDOW ASSEMBLY & DIVERSITY CONTROL (Supporting vs Contradicting)
      │
      ▼
CITATION PREPARATION & PARAGRAPH ANCHORING
      │
      ▼
STRUCTURED RAG EVIDENCE PACKET ──> DOWNSTREAM AI / RESEARCH / CLINICAL WORKBENCH
```

---

### 2. Search Modes (Section 3)

1. **Mode A — Quick Search**: Fast clinical lookup, concise top-ranked evidence.
2. **Mode B — Evidence Search**: Focus on human controlled trials ($E_6$), systematic reviews, and PICO outcome measures.
3. **Mode C — Safety Search**: Prioritizes cytochrome P450 interactions, black-box warnings, contraindications, and pregnancy cautions.
4. **Mode D — Compare**: Multi-system comparative lens across Modern, Unani, Ayurveda, and TCM preserving epistemic non-equivalence.
5. **Mode E — Deep Research**: Multi-stage iterative retrieval with automated gap analysis and coverage auditing.
6. **Mode F — Entity Search**: Entity-centric cards detailing identity, aliases, targets, conditions, and evidence timelines.
7. **Mode G — Source Search**: Direct inspection of original source registries and licensing rights.
