# ZMIE Architecture Specification

## 1. System Overview
ZMIE (ZAYVORA Medical Intelligence Engine™) is a source-governed, multi-system medical intelligence and research platform.

```
┌────────────────────────────────────────────────────────┐
│                        ZMIE UI                         │
│       Next.js 15 Workbench + Standalone Browser UI     │
└───────────────────────────┬────────────────────────────┘
                            │ REST / JSON
┌───────────────────────────▼────────────────────────────┐
│                    FastAPI Gateway                     │
│  - /v1/search           - /v1/research  - /v1/safety   │
│  - /v1/ontology         - /v1/governance- /v1/timeline │
│  - /v1/topics           - /v1/projects  - /v1/admin    │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│              Governed Multi-Agent Layer                │
│  - SearchService        - DeepResearchAgent            │
│  - CitationValidator    - ContradictionEngine          │
│  - SafetyIntelligence   - RetractionMonitor            │
└─────────────┬───────────────────────────┬──────────────┘
              │                           │
┌─────────────▼─────────────┐ ┌───────────▼──────────────┐
│  Multi-Source Ingestion   │ │   Knowledge & Evidence   │
│  - OpenAlex Connector     │ │   - PostgreSQL 16        │
│  - Europe PMC Connector   │ │   - pgvector 1536 dim    │
│  - AYUSH Samhita Loader   │ │   - Neo4j Graph DB       │
│  - Class A/B/C License    │ │   - Redis 7.2 Broker     │
└───────────────────────────┘ └──────────────────────────┘
```

## 2. Core Service Boundaries
1. **Source & License Registry**: Enforces legal rights classes (Class A, B, C) and prevents copyrighted full-text distribution.
2. **Ingestion & Document Parser**: Derives cryptographic SHA-256 hashes, parses sections/paragraphs, and anchors provenance.
3. **Knowledge & Evidence Engine**: Deconstructs raw literature into atomic Claim Passports with PICO contexts.
4. **Cross-System Ontology**: Preserves Modern, Unani, Ayurveda, and TCM epistemological boundaries with explicit non-equivalence mapping.
5. **Zero-Hallucination Guardrail**: Natural Language Inference (NLI) validator rejecting unsupported assertions.
