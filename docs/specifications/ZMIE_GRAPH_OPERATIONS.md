# ZMIE GRAPH OPERATIONS & OBSERVABILITY SPECIFICATION
## Deployment Topology, Relational-to-Graph Projections & Disaster Recovery

---

### 1. Production Deployment Topology (Section 98)

```text
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ PostgreSQL 16   │       │  Neo4j / Redis  │       │     pgvector    │
│ (Authoritative  │──────>│ (Graph Traversal│       │(Semantic Vector │
│ Relational Store│       │  & Ontologies)  │       │   Retrieval)    │
└────────┬────────┘       └────────▲────────┘       └────────▲────────┘
         │                         │                         │
         ▼                         │                         │
┌──────────────────────────────────┴─────────────────────────┴────────┐
│               DISTRIBUTED GRAPH PROJECTION WORKERS                  │
└──────────────────────────────────▲──────────────────────────────────┘
                                   │
┌──────────────────────────────────┴──────────────────────────────────┐
│           GRAPH SYNCHRONIZATION EVENT BUS (Kafka / Redis)           │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 2. Relational to Graph Projection Pipeline (Section 36)

To prevent split-brain inconsistencies between PostgreSQL (source of truth) and the graph layer:
1. All changes commit to PostgreSQL within transactional boundaries.
2. A database trigger publishes a `KnowledgeChangeEvent`.
3. Projection workers consume the event and project the change into the graph layer.
4. If a graph write fails, the worker retries with exponential backoff; the relational state remains uncompromised.
5. The projection tracks `projection_version`, `last_synced`, and `sync_status`.

---

### 3. Observability & SLOs (Section 99)

- **Graph Traversal Latency**: P95 $< 45\text{ms}$ for 2-hop subgraphs.
- **Why This Explanation Latency**: P95 $< 60\text{ms}$.
- **Orphan Node Rate**: $< 0.1\%$ monitored via automated daily integrity audits.
- **Disaster Recovery**: Automated point-in-time recovery (PITR) for PostgreSQL and nightly cold graph snapshots to S3-compatible object storage.
