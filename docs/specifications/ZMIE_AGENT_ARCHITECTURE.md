# ZMIE Agent Architecture & Multi-Agent Orchestration

## 1. Orchestration Philosophy
The Large Language Model is the **reasoning and explanation layer**, not the source of truth. The system enforces:

```
USER QUESTION
      ↓
QUERY UNDERSTANDING
      ↓
KNOWLEDGE ORCHESTRATOR
      ↓
SPECIALIZED AGENTS (Search, Evidence, Safety, Terminology)
      ↓
EVIDENCE & CONTRADICTION ENGINES
      ↓
SYNTHESIS DRAFT
      ↓
MANDATORY CITATION VALIDATION (NLI)
      ↓
FINAL ANSWER WITH PROVENANCE TRACE
```

---

## 2. Directory of Specialized Autonomous Agents (Section 30)

| Agent Name | Module Path | Purpose & Responsibilities |
| :--- | :--- | :--- |
| **Search Service** | `app/agents/search_service.py` | Dynamic hybrid lexical + semantic + graph retrieval. |
| **Deep Research Agent** | `app/agents/orchestrator.py` | Executes 17-step autonomous investigation, extracts PICO, clusters conflicts, and maps gaps. |
| **Citation Validator** | `app/agents/citation_validator.py` | Natural Language Inference (NLI) entailment check enforcing zero-hallucination and intercepting citation laundering. |
| **Safety Intelligence** | `app/agents/safety_agent.py` | Evaluates CYP450 interactions, organ toxicities, absolute contraindications, and acute red-flag triage. |
| **Contradiction Engine** | `app/agents/contradiction_agent.py` | Decomposes conflicting outcomes into formulation, dosage, duration, and population differences. |
| **Terminology Agent** | `app/agents/terminology_agent.py` | Normalizes and expands queries across MeSH, SNOMED, Unani, and Ayurveda concepts. |
| **Retraction Monitor** | `app/agents/retraction_monitor.py` | Tracks Crossref / Retraction Watch updates, quarantines contaminated papers, and prunes dependent graph edges. |
| **Coverage Agent** | `app/agents/coverage_agent.py` | Audits search sweeps and transparently reports full-text ratios and acknowledged blindspots. |
| **Review Queue Manager**| `app/agents/review_queue.py` | Human-in-the-loop specialist pools (Physicians, Hakeems, Vaidyas, Pharmacologists). |
| **Knowledge Diff Engine**| `app/agents/diff_engine.py` | Living scientific memory tracking git-like commits for evolving medical evidence. |
| **Clinical CDS Bridge** | `app/agents/clinical_bridge.py` | Governed decision support evaluating EHR patient phenotypes, renal function, and polypharmacy. |
| **Federated Connector** | `app/agents/federated_connector.py`| Multi-tenant private institutional cloud sandboxing with zero data leakage. |
| **Global Network Router**| `app/agents/global_network.py` | Sovereign multi-jurisdictional federation (WHO TMGL, AYUSH TKDL, NLM, Europe PMC). |
| **Citation Exporter** | `app/agents/citation_exporter.py`| One-click export to BibTeX, RIS, and Vancouver formats. |
| **Admin Control Plane** | `app/agents/admin_service.py` | Observability, health telemetry, knowledge quality dashboards, and cryptographically anchored audit trails. |
