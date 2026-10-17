# ZMIE API Specification & Integration Contracts

Base URL: `http://localhost:8000/v1`

---

## 1. Public & Medical Search
- `GET /v1/search?q={query}&mode={public|evidence_only|researcher_deep}`: Unified hybrid search across modern and traditional corpora.
- `GET /v1/search/why-this/{claim_id}`: Signature atomic provenance audit drawer.
- `GET /v1/topics/{topic}`: Dynamic governed medical encyclopedia page.

---

## 2. Research Workbench
- `POST /v1/research/investigate`: Runs 17-step Deep Research Agent returning PICO tables, gap maps, and synthesis.
- `GET /v1/research/gaps?topic={topic}`: Dedicated research gap identification.
- `GET /v1/projects`: Lists persistent research workspaces.
- `POST /v1/projects`: Creates a new isolated research project.
- `GET /v1/projects/{id}`: Retrieves full project memory, included/excluded studies, and snapshots.
- `POST /v1/projects/{id}/notes`: Appends a timestamped research note.

---

## 3. Clinical Safety & Retraction Watch
- `POST /v1/safety/evaluate`: Evaluates herb-drug interactions, pregnancy contraindications, and red-flag symptoms.
- `GET /v1/safety/retraction-check?doi={doi}`: Real-time Crossref / Retraction Watch verification.

---

## 4. Cross-System Ontology & Comparative Medicine
- `GET /v1/ontology/concepts?system={system}`: Lists canonical concept nodes.
- `GET /v1/ontology/mappings?concept_id={id}`: Returns explicit correspondence edges with epistemic rationales.
- `GET /v1/ontology/compare?topic={topic}`: Multi-tradition side-by-side epistemological comparison.

---

## 5. Human Governance & Living Memory
- `GET /v1/governance/queue?pool={pool}`: Returns pending tasks for specialist review pools.
- `POST /v1/governance/resolve/{task_id}`: Physician / Hakeem / Vaidya verification dispatch.
- `GET /v1/timeline/changes`: Global feed of latest verified medical knowledge commits.
- `GET /v1/timeline/topic?topic={topic}`: "What changed" longitudinal timeline.

---

## 6. Scholarly Exports & Coverage Auditing
- `GET /v1/export/coverage?topic={topic}`: Returns measured source completeness and acknowledged blindspots.
- `POST /v1/export/bibtex`: One-click BibTeX export.
- `POST /v1/export/ris`: One-click RIS reference export.

---

## 7. Clinical CDS & Enterprise Federation
- `POST /v1/clinical/evaluate-patient`: Governed decision support for EHR patient phenotype and lab intake.
- `POST /v1/enterprise/federated-search`: Federated search across ZMIE public network + private institutional sandboxes.
- `GET /v1/global-network/federate?q={q}`: Sovereign multi-jurisdictional federation (WHO, AYUSH, NLM, Europe PMC).

---

## 8. Admin Control Plane & Observability
- `GET /v1/admin/telemetry`: Real-time system health, memory, and worker status.
- `GET /v1/admin/quality-dashboard`: Knowledge quality metrics, verified claims, and zero-hallucination stats.
- `GET /v1/admin/research-metrics`: Research platform run statistics and contradiction rates.
- `GET /v1/admin/audit-logs`: Audit trail logs tracking who, what, and when.
