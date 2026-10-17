# ZMIE — MEDICAL KNOWLEDGE INFRASTRUCTURE PLATFORM
## Developer Platform, AI Model Gateway, Governed RAG Engine & Enterprise Ecosystem Specification

---

### 1. Executive Summary & Platform Positioning

**ZMIE (ZAYVORA Medical Intelligence Engine™)** is the **governed medical knowledge layer** situated between authoritative medical sources (clinical trials, systematic reviews, regulatory advisories, traditional codices) and downstream AI-powered applications.

```text
[Authoritative Medical Sources & Codices]
                  │
                  ▼
   [ZMIE Governed Knowledge Engine]
   (Provenance, Evidence Graph, Truth Firewall)
                  │
                  ▼
    [ZMIE Platform Infrastructure Layer]
    ┌───────────────────────┬────────────────────────┐
    │  API Gateway & Auth   │   Governed RAG Engine  │
    ├───────────────────────┼────────────────────────┤
    │  AI Model Router      │   Webhooks Dispatcher  │
    ├───────────────────────┼────────────────────────┤
    │  Multi-System Intel   │   Python / REST SDK    │
    └───────────────────────┴────────────────────────┘
                  │
   ┌──────────────┼──────────────┬──────────────┐
   ▼              ▼              ▼              ▼
[ZAYVORA App] [Hospital EHR] [Biotech/Pharma] [AI Models]
(Hakeem Sahab) (Epic/Cerner) (Drug Discovery) (Claude/GPT/Ollama)
```

ZMIE does **not** replace generative AI models; rather, it eliminates their hallucinations, citations fabrications, and unsupported claims by:
1. Providing **cryptographically anchored RAG context packets**.
2. Enforcing a **Truth & Safety Firewall** over generated responses.
3. Preserving **epistemic boundaries** between Modern Medicine, Unani-Tibb, and Ayurveda.

---

### 2. API Gateway & Scoped Credential Lifecycle

The ZMIE API Gateway manages external identities, tenant boundaries, and access scopes.

#### 2.1 Credential Architecture
- **Raw API Key Format**: `zmie_{environment}_{random_token}` (e.g., `zmie_production_a7d8e9...`).
- **Lookup Prefix**: First 12 characters stored in plain text for database indexing (`zmie_product`).
- **Storage Security**: Only the **SHA-256 hash** of the key is persisted. Raw keys are returned exactly once upon creation.
- **Revocation**: Instant revocation (`status = "revoked"`) immediately invalidates active sessions without cache lag.

#### 2.2 Scopes Hierarchy
| Scope | Description |
|---|---|
| `knowledge:read` | Read access to medical ontology and verified concepts |
| `search:read` | Query access to multi-mode hybrid search engine |
| `evidence:read` | Access to atomic evidence passports and study hierarchies ($E_0$–$E_6$) |
| `rag:read` | Generate governed RAG context packets |
| `safety:read` | Drug-herb interaction and contraindication screening |
| `research:execute` | Multi-step deep research agent workflows |
| `admin:write` | System administration and tenant credential configuration |

---

### 3. Governed RAG Context Engine

External LLMs (Claude, GPT, Gemini, Llama) require structured context rather than raw, unvetted web text.

#### 3.1 Endpoint
`POST /v1/platform/rag/context`

#### 3.2 Request Structure
```json
{
  "query": "Metformin and Vitamin B12 deficiency",
  "evidence_minimum": "E4",
  "max_items": 10,
  "include_safety": true,
  "include_contradictions": true
}
```

#### 3.3 RAG Context Packet Contract (`RAGContextPacket`)
- `knowledge_version`: Canonical freeze tag (e.g. `2026.10`).
- `verified_claims`: Atomic statements cleared by the Truth Firewall.
- `evidence_items`: Statistical effect sizes, sample sizes, and study types.
- `citations`: Verified PMIDs/DOIs with retraction check confirmation.
- `safety_context`: Interceptions, contraindications, and safe dosing bounds.
- `limitations`: Explicit clinical caveats and epistemic boundaries.
- `context_token_estimate`: Token budget accounting for downstream prompt assembly.

---

### 4. Multi-System Medical Intelligence API

Unified query endpoint across modern medicine, Unani-Tibb, and Ayurveda.

#### 4.1 Endpoint
`POST /v1/platform/intelligence/query`

#### 4.2 Cross-System Epistemic Integrity
- **No False Equivalences**: Unani humors (*Mizaj*, *Akhlat*) and Ayurvedic doshas (*Vata*, *Pitta*, *Kapha*) are never collapsed into Western biomedical diagnoses without explicit epistemic separation.
- **Strict Verification**: Queries return verified clinical correlations alongside traditional codex citations (e.g. *Canon of Medicine*, *Charaka Samhita*).

---

### 5. AI Model Router & Gateway

The Model Router dynamically selects LLM backends based on task classification, latency constraints, and risk level.

#### 5.1 Routing Matrix
| Task Type | Risk Level | Primary Model | Fallback Model | Latency Target |
|---|---|---|---|---|
| `synthesis` | HIGH | `claude-3-5-sonnet` | `gpt-4o` | 2,500 ms |
| `verification` | CRITICAL | `gpt-4o` | `claude-3-5-sonnet` | 1,500 ms |
| `classification` | LOW | `claude-3-5-haiku` | `gpt-4o-mini` | 800 ms |
| `summarization` | MEDIUM | `claude-3-5-sonnet` | `gpt-4o` | 2,000 ms |

#### 5.2 Automatic Failover & Firewall Audit
1. If the primary model encounters a timeout or upstream 503 error, the router automatically fails over to the configured secondary model.
2. The generated output is passed through the **ZMIE Truth & Safety Firewall** (`TruthAndSafetyFirewall.verify_answer`).
3. If uncited clinical claims or retracted sources are detected, the response is blocked or flagged with limitations.

---

### 6. Webhooks & Event Notification System

Enables downstream enterprise systems, hospitals, and biotech teams to react to knowledge shifts in real time.

#### 6.1 Subscribed Events
- `source.retracted`: A published study in the evidence graph was formally retracted.
- `evidence.updated`: An evidence grade was elevated or downgraded based on new trials.
- `research.completed`: An autonomous deep research workflow finished.
- `safety.alert`: A newly discovered drug-herb or drug-drug contraindication was verified.

#### 6.2 Cryptographic HMAC-SHA256 Signatures
Webhooks are signed using HMAC-SHA256:
```text
Signature = HMAC-SHA256(SecretKey, "t=" + Timestamp + "." + Payload)
```
Headers sent with each webhook:
- `X-ZMIE-Signature`: Computed hexadecimal signature.
- `X-ZMIE-Timestamp`: Unix epoch timestamp.
- `X-ZMIE-Event-Id`: Unique event tracking ID.

#### 6.3 Replay Attack Protection
Incoming webhook signatures must match within a **300-second window** (`tolerance_seconds = 300`). Out-of-date timestamps are rejected automatically.

---

### 7. Official Python SDK Reference

The `zmie` Python package provides idiomatic bindings:

```python
from zmie import ZMIE

# Initialize client
client = ZMIE(api_key="zmie_production_...", base_url="https://api.zmie.org")

# 1. RAG Context Generation
rag_packet = client.rag_context(
    query="Boswellia serrata in osteoarthritis",
    evidence_minimum="E4"
)

# 2. Multi-System Intelligence Query
intel = client.intelligence_query(
    query="Nigella sativa",
    systems=["modern", "unani", "ayurveda"]
)

# 3. AI Model Gateway with Firewall
response = client.route_ai(
    task_type="synthesis",
    prompt="Summarize evidence for curcumin in rheumatoid arthritis",
    context_packet=rag_packet
)

# 4. Webhook Security Verification
is_valid = ZMIE.verify_webhook_signature(
    payload=raw_body,
    secret=webhook_secret,
    signature=headers["X-ZMIE-Signature"],
    timestamp=int(headers["X-ZMIE-Timestamp"])
)
```

---

### 8. Enterprise Isolation & Metered Usage Ledger

- **Tenant Isolation**: All credentials, webhooks, and private clinical projects are scoped by `tenant_id`.
- **Metered Ledger**: Every billable API call logs a `UsageEvent` (`service`, `operation`, `units`, `timestamp`).
- **Separation of Concerns**: Usage metering and billing never alter, bias, or interfere with medical truth determination.

---

### 9. Verification & Acceptance Results

- **Platform Acceptance Tests**: `tests/test_platform_infrastructure_acceptance.py` (7/7 tests passing).
- **Master Platform Showcase**: `tests/platform_infrastructure_showcase.py` (5/5 proof demonstrations verified live).
- **Full Repository Regression Suite**: **73/73 tests passing** (0 failures, 0 errors).
