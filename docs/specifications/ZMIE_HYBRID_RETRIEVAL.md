# ZMIE HYBRID RETRIEVAL SPECIFICATION
## Multi-Channel Fusion & Signal Intersection Architecture

---

### 1. Hybrid Fusion Architecture (Section 14)

ZMIE avoids relying on any single search modality. A candidate document receives signals across six distinct channels:

```text
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ LEXICAL CHANNEL │       │ SEMANTIC VECTOR │       │ ENTITY CHANNEL  │
│ (Exact / BM25)  │       │ (Dense Cosine)  │       │ (Concept Nodes) │
└────────┬────────┘       └────────┬────────┘       └────────┬────────┘
         │                         │                         │
         └────────────────┬────────┴────────┬────────────────┘
                          ▼                 ▼
                 ┌─────────────────┐ ┌───────────────┐
                 │  GRAPH CHANNEL  │ │EVIDENCE CHANN.│
                 │ (Path Traversal)│ │ (PICO / E0-6) │
                 └────────┬────────┘ └───────┬───────┘
                          │                  │
                          └────────┬─────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │   SAFETY CHANNEL    │
                        │ (CYP450 / Red Flags)│
                        └──────────┬──────────┘
                                   │
                                   ▼
                        CANDIDATE POOL UNION
```

---

### 2. Multi-Signal Scoring

Every candidate in the aggregated pool carries a channel score vector:
$$\vec{S}_c = \begin{bmatrix} S_{\text{lex}}, & S_{\text{sem}}, & S_{\text{ent}}, & S_{\text{graph}}, & S_{\text{evd}}, & S_{\text{safety}} \end{bmatrix}$$

- **High-Confidence Intersection**: When a document is retrieved across $\ge 3$ channels (e.g. lexical match + entity match + graph edge), its baseline relevance receives a cross-channel boost.
- **Channel Fallback**: If vector search returns zero hits (e.g. specialized classical Persian codex term), the lexical and entity channels guarantee graceful degradation without zero-result dropouts.
