# ZMIE INGESTION OPERATIONS RUNBOOK
## Production Worker Queues, Cron Schedules & Reliability Engineering

---

### 1. Ingestion Queue Architecture

ZMIE utilizes an asynchronous distributed task topology powered by Redis / Celery:

```text
┌─────────────────┐       ┌─────────────────┐       ┌──────────────────┐
│  High-Priority  │       │ Batch-Harvester │       │ Dead-Letter Queue│
│   (Retractions) │       │  (OpenAlex/PMC) │       │     (DLQ)        │
└────────┬────────┘       └────────┬────────┘       └────────▲─────────┘
         │                         │                         │ (On Exhausted
         ▼                         ▼                         │  Retries)
┌────────────────────────────────────────────────────────┐   │
│             INGESTION WORKER POOL (4-16 Cores)         ├───┘
└────────────────────────────────────────────────────────┘
```

---

### 2. Scheduled Synchronization Cadences

| Task Name | Target Connector | Frequency | Cron Expression | Priority |
|---|---|---|---|---|
| `sync_retractions` | Europe PMC & Crossmark | Every 6 hours | `0 */6 * * *` | High (P0) |
| `sync_clinical_trials` | ClinicalTrials.gov API | Daily at 02:00 UTC | `0 2 * * *` | Medium (P1) |
| `sync_biomedical_openalex` | OpenAlex Works Feed | Daily at 04:00 UTC | `0 4 * * *` | Normal (P2) |
| `audit_source_health` | All registered connectors | Every 15 minutes | `*/15 * * * *` | High (P0) |
| `recompute_coverage_indices`| Internal Graph Index | Weekly (Sunday) | `0 0 * * 0` | Low (P3) |

---

### 3. Failure Handling & Dead-Letter Queue (DLQ)

1. **Retry Policy**:
   - Initial retry: 2 minutes
   - Second retry: 10 minutes
   - Third retry: 60 minutes
2. **Dead-Letter Routing**:
   - If a document fails parsing after 3 attempts (e.g. malformed XML, unparseable PDF stream), the payload is quarantined in the DLQ (`zmie:ingestion:dlq`).
   - Alerts are dispatched to on-call data engineers via PagerDuty / Slack webhook with full stack trace and source ID.
3. **Graceful Degraded Mode**:
   - If an external connector (e.g. Europe PMC) experiences an outage, search and clinical synthesis continue seamlessly using cached knowledge graph nodes, with the `SourceHealthMonitor` reporting `DEGRADED` status.
