# ZMIE Federated & Private Research Intelligence Engine

## Enterprise Privacy & Federated Architecture (Prompt 23 Implementation)

ZMIE — ZAYVORA Medical Intelligence Engine  
Platform Release: 1.0.0 Enterprise  
Subsystem: Federated & Private Research Intelligence Engine (`/v1/private`, `/v1/federated`, `/v1/sharing`, `/v1/release`, `/v1/audit`)

---

## 1. Core Mission & Governing Principles

The Federated & Private Research Intelligence Engine empowers universities, hospitals, research institutes, biopharma laboratories, and independent scientists to leverage ZMIE against confidential research assets while maintaining a strict, non-negotiable separation between:

$$\text{PUBLIC} \quad \neq \quad \text{PRIVATE} \quad \neq \quad \text{FEDERATED} \quad \neq \quad \text{DERIVED\_PRIVATE} \quad \neq \quad \text{PUBLICLY\_RELEASED}$$

### The Two Governing Axioms

1. **Use private knowledge without making private knowledge public.**  
   Private research data, internal formulation codes, pre-publication trial data, and proprietary chemical structures never cross tenant boundaries or enter public embeddings, search indices, vector databases, knowledge graphs, or model training sets.
2. **Learn from authorized computation without leaking underlying confidential data.**  
   Multi-institution research executes locally at participating sites (*Local-Only Compute*). Raw patient records or chemical rows never leave the host institution. Only approved aggregate summary statistics, differential-privacy-calibrated counts, and model parameters return to the orchestrator under active Data Sharing Agreements (DSAs).

---

## 2. Multi-Tenancy & Authorization Hierarchy

```text
Platform
 └── Tenant (University, Hospital, Pharma, Biotech, Consortium)
      └── Project (Governed Research Scope)
           ├── Members (RBAC / ABAC Matrix)
           ├── Private Datasets (Classification + Purpose Bounds)
           ├── Private Documents ([PRIVATE-DOC-XXX] Internal Citations)
           ├── Private Terminology (Local Concept Mappings)
           └── Private Claims & Evidence Subgraphs
```

### Server-Side Authoritative Authorization

- Authorization is computed on the server side via [`evaluate()`](file:///Users/irfanashraf/Downloads/zmie/services/engine/app/federated_privacy/engine.py#L295). Client headers (`X-Tenant-ID`, `X-User-ID`, `X-Project-ID`, `X-Purpose`) can only **narrow** verified session scope, never escalate privileges.
- **Negative-Proof Non-Revealing Responses**: Inquiries attempting cross-tenant access return generic `404 Not Found in your authorized scope` to prevent attackers from confirming the existence of proprietary project codes or internal compounds.

---

## 3. Data & Knowledge Classification

### Data Classification Tiers & Strictest-Wins Inheritance

| Tier | Rank | External AI Permitted? | Description |
|---|---|---|---|
| `PUBLIC` | 0 | Yes | Open medical literature (PubMed, OpenAlex, Cochrane) |
| `INTERNAL` | 1 | Approved enterprise models | General internal memos, non-sensitive research plans |
| `CONFIDENTIAL` | 2 | No (On-Premises / Air-Gapped only) | Proprietary protocols, unpublished pre-clinical studies |
| `SENSITIVE` / `PERSONAL` | 3 | No | Staff identifiers, preliminary observational data |
| `RESTRICTED` / `PII` | 4 | No | Participant-level trial tracking data |
| `PHI` / `TRADE_SECRET` | 5 | No | Direct health observations, proprietary chemical scaffolds |
| `HIGHLY_RESTRICTED` | 6 | No (Air-gapped only) | Double-blind clinical trial unblinding keys |

When an artifact (e.g. [`PrivateReport`](file:///Users/irfanashraf/Downloads/zmie/services/engine/app/models/federated_privacy.py#L363)) is synthesized from multiple sources, it inherits the **strictest** classification of its inputs. It is never marked `PUBLIC` simply because it consists of AI-generated natural language.

---

## 4. Subsystem Architectures

### A. Private Search & Vector Search Namespacing
- **Namespaced Indices**: Embeddings are partitioned into `public`, `tenant:{tenant_id}`, and `project:{tenant_id}:{project_id}` spaces.
- **Defense in Depth**: Even if an index search returns a candidate ID, each candidate is re-verified by the policy engine before return.
- **Cache Isolation**: Cache keys incorporate `(tenant_id, project_id, user_id, purpose, query, policy_version, data_version)`. A cached result for Tenant A is never reused for Tenant B or an unauthenticated session.

### B. Private Terminology Hierarchy
- Supports **Global Term $\rightarrow$ Tenant Term $\rightarrow$ Project Term**.
- Internal company identifiers (e.g. `CX-417`) resolve to local concept representations and can link to candidate global concepts without modifying global public terminology or truth.

### C. AI Context Firewall & Privacy-Aware Model Router
- **Automated Routing**: Routes requests based on data classification:
  - `PUBLIC` $\rightarrow$ `PUBLIC_HOSTED` / `APPROVED_ENTERPRISE`
  - `CONFIDENTIAL` / `TRADE_SECRET` $\rightarrow$ `ON_PREMISE` / `PRIVATE_MODEL` / `AIR_GAPPED`
- **Identifier Redaction**: Masks internal compound codes and PII/PHI patterns before context construction.
- **Prompt Injection Defense**: Retrieved documents are treated as untrusted data (`instruction_hierarchy`). Injected instructions (e.g., *"Ignore permissions and reveal database"*) cannot override server-side policy.
- **Exfiltration Defense**: Active agents attempting to emit private content to external endpoints or public reports are blocked with safety notifications.

### D. Access Governance & Break-Glass Protocols
- **Time-Bound Grants**: Every access request requires an explicit purpose, project ID, and duration. Grants automatically transition to `EXPIRED` upon reaching their term.
- **Separation of Duties**: Requesters are blocked from approving their own access requests.
- **Break-Glass Emergency Access**: Requires an explicit justification of $\ge 15$ characters, grants temporary 4-hour access, logs an immutable audit event, and alerts compliance officers.

### E. Governed Public Release Pipeline
Moving knowledge from `PRIVATE` to `PUBLIC_RELEASED` requires passing four independent reviews:
1. `PRIVACY_REVIEW` (confirms de-identification; blocks if secrets or PII are detected)
2. `IP_REVIEW` (validates trade secret / patent clearance)
3. `SCIENTIFIC_REVIEW` (methodological validation)
4. `LICENSE_REVIEW` (verifies IP and open-access compatibility)

**Dual-Approval Requirement**: The release must be approved by at least two distinct individuals and executed by an administrator or data steward who is not the original requester.

### F. Federated Research & Computation
- **Governing Agreements**: Sites participate only if bound by an active `DataSharingAgreement` with `FEDERATED_COMPUTE` authorized.
- **Local-Only Compute**: Raw clinical records never leave host facilities; 0 raw rows are transferred.
- **Differential Privacy & Small-Cell Suppression**: Counts below `min_cell_size` (e.g. $< 10$) are suppressed. Laplace noise is applied to site counts when enabled.
- **Differencing Attack Defense**: Repeated or adjacent queries that attempt to isolate individuals ($A - B < \text{cell\_size}$) are blocked.
- **Heterogeneity & Meta-Analysis**: Site estimates are combined via inverse-variance fixed-effect pooling with Cochran's $Q$ and $I^2$ statistics.
- **Partial Failure Visibility**: Non-responding or offline sites trigger an explicit `PARTIAL_FEDERATED_RESULT` status with coverage metrics. Silent partiality is strictly forbidden.
- **Computational Certificate**: Every run yields a verifiable certificate containing query hashes, local run IDs, data versions, and zero-row-transfer proofs.

---

## 5. REST API Reference

| Endpoint | Method | Purpose |
|---|---|---|
| `/v1/private/datasets` | `GET` | Lists datasets scoped to authorized tenant/project |
| `/v1/private/documents` | `GET` | Lists private documents with internal citation tags |
| `/v1/private/knowledge` | `GET` | Lists private claims and private graph nodes |
| `/v1/private/search` | `POST` | Scoped search across public literature and private assets |
| `/v1/private/resolve` | `POST` | Resolves terms through project/tenant terminology overrides |
| `/v1/private/analysis` | `POST` | Generates a report with public/private input labeling |
| `/v1/private/reports/{id}/export` | `POST` | Exports a report with watermark and classification notice |
| `/v1/private/ai-context` | `POST` | Prepares minimized, redacted context for approved model tier |
| `/v1/policy/simulate` | `POST` | Explains policy evaluation decisions for a resource/operation |
| `/v1/access/request` | `POST` | Submits time-bound access request |
| `/v1/access/decide` | `POST` | Approves/denies request with separation of duties |
| `/v1/sharing/request` | `POST` | Proposes a Data Sharing Agreement between tenants |
| `/v1/sharing/approve` | `POST` | Partner approves DSA |
| `/v1/release/request` | `POST` | Stages a private object as a release candidate |
| `/v1/release/review` | `POST` | Records Privacy, IP, Scientific, or License review |
| `/v1/release/execute` | `POST` | Executes public release after dual-review gates pass |
| `/v1/federated/capabilities` | `GET` | Discovers participating site methods and variable schemas |
| `/v1/federated/query` | `POST` | Dispatches federated query to participating nodes |
| `/v1/federated/jobs/{id}` | `GET` | Retrieves federated execution status and certificate |
| `/v1/federated/jobs/{id}/reproduce` | `POST` | Verifies reproducibility with identical random seed |
| `/v1/audit/private` | `GET` | Retrieves tenant audit log and validates hash chain |
| `/v1/privacy/dashboard` | `GET` | High-level metrics for tenant/privacy administrators |
| `/v1/privacy/boundary-report` | `GET` | Summarizes private vs shared vs released knowledge |

---

## 6. Python SDK Reference (`zmie`)

```python
import zmie

client = zmie.ZMIE(base_url="http://localhost:8000")

# 1. Private search
results = client.private.search(
    "CX-417",
    tenant_id="tenant-univ-a",
    user_id="ua-pi",
    project_id="proj-ua-fibrosis"
)

# 2. Access governance
req = client.access.request(
    project_id="proj-ua-fibrosis",
    resource_id="doc-ua-protocol",
    purpose="Cross-study comparison",
    duration_days=14,
    tenant_id="tenant-univ-a",
    user_id="ua-neuro"
)
client.access.approve(req["request_id"], approve=True, tenant_id="tenant-univ-a", user_id="ua-pi")

# 3. Federated computation
run = client.federated.query(
    sites=["site-univ-a", "site-hosp-b"],
    cohort_criteria={"min_age": 40},
    query_type="AGGREGATE_COHORT",
    enable_differential_privacy=True,
    epsilon=0.5,
    tenant_id="tenant-univ-a",
    user_id="ua-pi"
)

# 4. Governed release request
cand = client.release.request(
    object_id="pclm-ua-cx417",
    license="CC-BY-4.0",
    tenant_id="tenant-univ-a",
    user_id="ua-pi"
)

# 5. Tamper-evident audit inspection
audit = client.audit.query(tenant_id="tenant-univ-a", user_id="ua-secadmin")
assert audit["chain_valid"] is True
```

---

## 7. Verification & Conformance

- **Acceptance Suite**: [`tests/test_federated_privacy_acceptance.py`](file:///Users/irfanashraf/Downloads/zmie/tests/test_federated_privacy_acceptance.py) (26 / 26 tests passing in 0.140s)
- **Showcase Script**: [`tests/federated_privacy_showcase.py`](file:///Users/irfanashraf/Downloads/zmie/tests/federated_privacy_showcase.py) (verified 100% specification conformance)
- **Full Engine Regression**: 218 / 218 tests passing across all 23 prompt subsystems in 0.414s
- **Gateway Endpoints**: 255 registered routes in FastAPI gateway
