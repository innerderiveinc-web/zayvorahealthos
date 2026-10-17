# ZMIE SEARCH OPERATIONS & TELEMETRY SPECIFICATION
## Index Versioning, Cache Topology, Rate Limiting & Observability

---

### 1. Production Topology & Caching Architecture (Sections 98, 105)

```text
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  Search Gateway │──────>│ Redis Query     │──────>│ Elastic / Open- │
│  (FastAPI / V1) │       │ Cache (TTL 1h)  │       │ search (Lexical)│
└────────┬────────┘       └─────────────────┘       └────────▲────────┘
         │                                                   │
         ├───────────────────────────────────────────────────┤
         ▼                                                   ▼
┌─────────────────┐                                 ┌─────────────────┐
│     pgvector    │                                 │  Neo4j / Graph  │
│ (Dense Vectors) │                                 │ (Paths & Rels)  │
└─────────────────┘                                 └─────────────────┘
```

---

### 2. Search Index Versioning (Section 76)

- Supports Blue/Green index rotation (`INDEX_V1` $\rightarrow$ `INDEX_V2`).
- Reindexing pipeline runs asynchronously in the background; newly indexed documents are validated before traffic is switched.

---

### 3. Rate Limiting & Resource Quotas (Section 99, 100)

- Standard Public Search: 60 requests/minute per IP / API key.
- Deep Research Investigations: 5 concurrent jobs per tenant, metered by computational budget.

---

### 4. Search Telemetry & Observability (Sections 104, 112)

Every query logs structured telemetry:
- `request_id`, `query_text_sanitized`, `mode`, `latency_ms`, `total_candidates`, `top_result_id`, `evidence_level`, `tenant_id`.
- Zero-result rates, slow queries ($> 200\text{ms}$), and external provider timeouts are monitored via Prometheus & Grafana alerts.
