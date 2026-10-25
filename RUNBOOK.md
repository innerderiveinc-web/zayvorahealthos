# ZMIE — ZAYVORA Medical Intelligence Engine™
## Enterprise Deployment, Runbook & Production Operations Guide

---

## 1. Quickstart & Local Verification

### Prerequisites
- Python $\ge$ 3.9 (or Python 3.11/3.12 recommended for production)
- Docker & Docker Compose (for PostgreSQL 16 + pgvector, Neo4j, Redis, MinIO)
- Node.js $\ge$ 20.x (for Next.js 15 Web Workbench)

### Quick Verification Command
Run the complete, offline-capable master verification test suite to ensure all 9 architectural pillars are functioning with zero regressions:
```bash
PYTHONPATH=services/engine .venv/bin/python3 examples/master_showcase.py
```

Run the quantitative evaluation & adversarial safety benchmark:
```bash
PYTHONPATH=services/engine .venv/bin/python3 services/engine/app/core/eval_suite.py
```

---

## 2. Starting Local Infrastructure Stack

Launch PostgreSQL with `pgvector`, Neo4j 5.x, Redis 7, and MinIO:
```bash
docker compose up -d
```

### Inspect Database Services
- **PostgreSQL 16**: `localhost:5432` (`user: zmie_admin`, `db: zmie_knowledge_db`)
- **Neo4j Graph Browser**: `http://localhost:7474` (`user: neo4j`, `pass: zmie_graph_password`)
- **MinIO S3 Console**: `http://localhost:9001` (`user: zmie_minio_admin`)
- **Redis Cache**: `localhost:6379`

### Run Database Migrations
Initialize relational tables and vector indexes:
```bash
docker exec -i zmie-postgres psql -U zmie_admin -d zmie_knowledge_db < services/engine/app/db/schema.sql
```

Seed initial Neo4j cross-system constraints:
```bash
cypher-shell -u neo4j -p zmie_graph_password -f services/engine/app/db/neo4j_seed.cypher
```

---

## 3. Launching Backend Engine API

Start the FastAPI ASGI server with auto-reload:
```bash
cd /Users/irfanashraf/Downloads/zmie
PYTHONPATH=services/engine .venv/bin/uvicorn app.main:app --app-dir services/engine --reload --host 0.0.0.0 --port 8000
```

### Interactive API Documentation
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 4. API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/v1/search` | Unified search across Biomedical literature + Unani + Ayurveda |
| `GET` | `/v1/search/why-this/{claim_id}` | Signature "Why This Claim?" atomic provenance audit trail |
| `POST`| `/v1/research/investigate` | Autonomous 17-step Deep Research Agent runner |
| `GET` | `/v1/research/gaps` | Research Gap Engine identifying unstudied populations/doses |
| `POST`| `/v1/safety/evaluate` | CYP450 drug interactions, contraindications, red-flag triage |
| `GET` | `/v1/safety/retraction-check`| Real-time Crossref / Retraction Watch verification |
| `GET` | `/v1/ontology/concepts` | Multi-system concept directory (Modern, Unani, Ayurveda, TCM) |
| `GET` | `/v1/ontology/mappings` | Epistemic correspondence mappings with confidence scores |
| `GET` | `/v1/ontology/compare` | Multi-tradition side-by-side epistemological comparison |
| `GET` | `/v1/governance/queue` | Human-in-the-loop specialist review queue |
| `POST`| `/v1/governance/resolve/{id}`| Physician / Hakeem / Vaidya verification dispatch |
| `GET` | `/v1/timeline/changes` | Living Scientific Memory global change feed |
| `GET` | `/v1/timeline/topic` | "What changed" longitudinal timeline for a tracked topic |
| `GET` | `/v1/export/coverage` | Transparent source completeness and acknowledged blindspots |
| `POST`| `/v1/export/bibtex` | One-click BibTeX export for LaTeX/Overleaf |
| `POST`| `/v1/export/ris` | One-click RIS reference export for Zotero/EndNote |

---

## 5. Next.js 15 Web Workbench

Launch the frontend:
```bash
cd services/web
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to access the Public Search interface and Researcher Studio.
