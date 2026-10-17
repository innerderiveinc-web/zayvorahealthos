# ZMIE RETRACTION MONITORING & CLAIM QUARANTINE MODEL
## Retraction Surveillance, Downstream Claim Flagging & Knowledge Commits

---

### 1. The Retraction Dilemma in Medical AI

Standard LLMs trained on static snapshots ingest papers that are subsequently retracted due to fabrication, methodology flaws, or patient harm. LLMs continue citing retracted studies indefinitely because they have no living retraction lifecycle.

ZMIE solves this through an automated, event-driven **Retraction Monitoring Engine**.

---

### 2. Surveillance Sources & Triggers

1. **Europe PMC `hasRetraction` Flag**: Real-time XML tag indicating official retraction notices.
2. **Crossref Retraction Feed**: Evaluates updates matching DOIs with Crossmark `retraction` assertions.
3. **PubMed `Retracted Publication` Publication Type**: Daily automated sync against the NLM PubMed catalog.
4. **Editorial Notices & Corrigenda**: Automated natural language extraction of "Expression of Concern" and "Notice of Retraction".

---

### 3. Cascading Downstream Quarantine Protocol

When a document is flagged as retracted:

```text
DOCUMENT FLAGGED AS RETRACTED (DOI: 10.1001/jama.2021.0001)
                    │
                    ▼
DOCUMENT STATUS MUTATED TO: is_retracted = True
                    │
                    ▼
ISOLATE DEPENDENT ATOMIC CLAIMS (CLM-2021-001, CLM-2021-002)
                    │
                    ▼
DOWNGRADE EVIDENCE STATUS: is_retracted = True, warning = ACTIVE_RETRACTION
                    │
                    ▼
PRUNE FROM SEARCH & CLINICAL SYNTHESIS
                    │
                    ▼
RECORD LIVING COMMIT (action = 'retraction_pruned', author = 'RetractionMonitorAgent')
```

- **Safety Intercept**: If a user directly queries a retracted paper, ZMIE displays a prominent alert explaining that the study was retracted, detailing the retraction rationale, and cautioning against clinical application.
