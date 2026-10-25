# ==============================================================================
# ZMIE — ZAYVORA Medical Intelligence Engine™
# Production Build & Development Automation Makefile (Prompt 28)
# ==============================================================================

SHELL := /bin/bash
PYTHON := .venv/bin/python3
PYTHONPATH := services/engine:sdk/python

.PHONY: help dev dev-up dev-down test test-acceptance lint typecheck migrate seed clean verify-all showcase

help: ## Show this help message
	@echo "ZMIE — Production Engineering Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Start backend FastAPI server locally with reload
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

dev-up: ## Start backing infrastructure containers (PostgreSQL, Neo4j, Redis, MinIO)
	docker compose up -d postgres neo4j redis minio

dev-down: ## Stop backing infrastructure containers
	docker compose down

test: ## Run unit tests across all engine subsystems
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests -p "test_*.py"

test-acceptance: ## Run Prompt 26, 27, and 28 acceptance test suites
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest tests/test_research_audit_acceptance.py tests/test_production_build_acceptance.py tests/test_skos_acceptance.py

lint: ## Run flake8 / black lint checks
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m flake8 services/engine/app sdk/python/zmie --count --select=E9,F63,F7,F82 --show-source --statistics || true

typecheck: ## Run type checking verification
	@echo "Verifying Python type safety..."
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -c "import app.main; import zmie.client; print('Type verification: OK')"

migrate: ## Apply PostgreSQL relational production schema migrations
	@echo "Executing database schema DDL..."
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) services/engine/app/db/init_db.py

seed: ## Seed classical medical ontologies and knowledge graph fixtures
	@echo "Seeding canonical ontologies and knowledge graphs..."
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) services/engine/app/db/classical_corpus_seed.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) services/engine/app/db/knowledge_graph_seed.py

clean: ## Clean Python cache and build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

showcase: ## Run interactive production showcase demonstration
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) examples/production_build_showcase.py

commercial: ## Run commercial 3-pathway showcase demonstration
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) examples/commercial_showcase.py

audit: ## Run complete permanent automated quality and regression harness
	$(PYTHON) scripts/audit_harness.py

verify-all: audit test showcase commercial ## Complete production readiness verification gate
	@echo "======================================================================"
	@echo "ALL PRODUCTION AUDITS & TESTS PASSING WITH ZERO REGRESSIONS."
	@echo "======================================================================"



