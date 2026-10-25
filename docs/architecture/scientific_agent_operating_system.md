# ZMIE Scientific Agent Operating System

## Governed Multi-Agent Execution & Scientific Orchestration (Prompt 24 Implementation)

**ZMIE — ZAYVORA Medical Intelligence Engine**  
**Platform Release: 1.0.0 Enterprise**  
**Subsystem: Scientific Agent Operating System (`/v1/agents`, `/v1/agent-tasks`, `/v1/research`, `/v1/agent-tools`, `/v1/reviews`, `/v1/agent-incidents`)**

---

## 1. Core Mission & Governing Doctrine

The ZMIE Scientific Agent Operating System is not a conversational chatbot and not an unconstrained autonomous loop. It is a **governed multi-agent scientific execution operating system** where specialized agents collaborate over shared, verifiable, and permissioned infrastructure.

### The Governing Doctrine
> **"Agents discover and reason.  
> Tools execute.  
> Evidence constrains.  
> Verifiers challenge.  
> Policies govern.  
> Humans remain accountable."**

### Fundamental Architectural Principle
**No single agent knows or controls the entire system.** Every agent is specialized, bounded by granular permissions, and operates strictly through the governed pipeline:

```text
QUESTION
   ↓
PLANNER (DAG Formulation)
   ↓
SPECIALIST AGENTS (Parallel / Sequential Execution)
   ↓
TOOLS / KNOWLEDGE / DATA / COMPUTE (Sandboxed Execution)
   ↓
EVIDENCE VERIFIER (Independent Double-Check)
   ↓
CONTRADICTION CHECK (Preserve Authentic Divergence)
   ↓
SAFETY CHECK (Toxicology, Contraindications, Red Flags)
   ↓
QUALITY / POLICY GATE (Epistemic Firewall & Boundary Rules)
   ↓
SYNTHESIS (Artifact-Linked Structured Reporting)
   ↓
HUMAN / AUTHORIZED DECISION MAKER (Consequential Governance)
```

### Agent $\neq$ Authority
An agent can search, retrieve, analyze, calculate, simulate, reason, compare, summarize, and propose. An agent cannot independently declare scientific truth, publish evidence, approve clinical action, certify regulatory status, release private data, modify global knowledge, or authorize laboratory experiments without explicit human review and governance approval.

---

## 2. Epistemic State Machine (14 Epistemic Boundaries)

ZMIE strictly enforces 14 mutually distinct epistemic boundaries across all agent reasoning and outputs (Clauses 16, 292, 293):

| Epistemic State | Definition | Permitted Claim Scope |
| :--- | :--- | :--- |
| `OBSERVED` | Direct empirical observation in randomized clinical trials or verified patient data. | "Observed in clinical trial cohort." |
| `REPORTED` | Sourced directly from indexed scholarly or traditional medical literature. | "Reported in indexed literature." |
| `MEASURED` | Instrument, laboratory, or diagnostic quantification. | "Quantified via clinical assay." |
| `DERIVED` | Formulated through systematic synthesis or cross-system ontology mapping. | "Derived through cross-system synthesis." |
| `COMPUTED` | Deterministic calculation produced by executable code artifacts. | "Computed via verified statistical model." |
| `MODELED` | Theoretical representation constructed via mathematical formulas. | "Modeled across theoretical frameworks." |
| `SIMULATED` | In silico computational parameter sweep or Monte Carlo iteration. | "Simulated in silico; not patient observation." |
| `PREDICTED` | Statistical or machine learning forecast. | "Predicted endpoint based on covariates." |
| `INFERRED` | Deductive or inductive reasoning over observed premises. | "Inferred hypothesis requiring experimental validation." |
| `HYPOTHESIZED` | Candidate proposal formulated for experimental testing. | "Hypothesized mechanism; unvalidated." |
| `PROPOSED` | Draft experimental protocol or knowledge modification. | "Proposed study design awaiting review." |
| `VALIDATED` | Independently verified by replication and double-computation. | "Independently verified and reproducible." |
| `CONTESTED` | Divergent findings or active clinical contradictions detected. | "Contested finding with population divergence." |
| `UNKNOWN` | Explicitly identified knowledge blind spot or missing data. | "Unknown; insufficient empirical evidence." |

### Epistemic Output Firewall (Non-Negotiable Transitions)
The system programmatically blocks invalid state promotions (Clause 294):
- $\text{PREDICTED} \not\rightarrow \text{OBSERVED}$
- $\text{SIMULATED} \not\rightarrow \text{MEASURED}$
- $\text{INFERRED} \not\rightarrow \text{FACT}$
- $\text{HYPOTHESIZED} \not\rightarrow \text{VALIDATED}$
- $\text{ASSOCIATED} \not\rightarrow \text{CAUSED}$
- $\text{TRADITIONAL} \not\rightarrow \text{BIOMEDICALLY EQUIVALENT}$ (unmapped concepts like *Damavi* preserved as `NO_VALID_MAPPING`)
- $\text{PRIVATE} \not\rightarrow \text{PUBLIC}$ (confidential research blocked from public leakage without governed release)

---

## 3. Specialist Agents Catalog (34 Autonomous Specialists)

ZMIE deploys 34 specialized scientific agent types under a unified `BaseSpecialistAgent` contract:

```text
Discovery & Search:
  ├── SourceAgent           (Multi-universe source discovery across PubMed, OpenAlex, Europe PMC, TKDL)
  ├── ResearchAgent         (Scholarly publication, preprint, dataset, and trial discovery)
  └── CoverageAgent         (Source universe, date range, and language coverage profiling)

Evidence, Claim & Citation:
  ├── EvidenceAgent         (PICO extraction, study design classification, and GRADE grading)
  ├── CitationAgent         (DOI/PMID resolution and NLI textual entailment verification)
  ├── ClaimAgent            (Atomic claim extraction and modality calibration: may vs causes)
  ├── ContradictionAgent    (Preservation and root-driver explanation of clinical divergence)
  └── SafetyAgent           (Toxicology, CYP450 interactions, contraindications, and red flags)

Ontology & Semantics:
  ├── OntologyAgent         (Cross-system concept resolution across MeSH, Unani, Ayurveda, TCM)
  └── TerminologyAgent      (Multilingual historical variants, botanical taxonomy, and semantic drift)

Clinical & Regulatory:
  ├── TrialAgent            (Clinical trial status, phases, enrollment, and endpoints)
  └── RegulatoryAgent       (FDA, EMA, CDSCO approval tracking; zero fabrication guard)

Data, Statistics & Computation:
  ├── DataAgent             (Dataset discovery, profiling, and missingness audit)
  ├── StatisticsAgent       (Statistical computation; rejects calculations without artifacts)
  ├── MechanismAgent        (Molecular target, pathway, and kinase cascade mapping)
  ├── CausalAgent           (Causal DAG construction, confounding audit, backdoor identification)
  ├── SimulationAgent       (Monte Carlo in silico simulation; strictly labeled SIMULATED)
  ├── HypothesisAgent       (Candidate hypothesis generation; strictly labeled HYPOTHESIZED)
  └── ExperimentAgent       (Next-best-experiment design with disconfirming observations)

Research Network:
  ├── ResearcherAgent       (Researcher identity resolution without competitive ranking)
  ├── CollaborationAgent    (Multi-institutional laboratory networks and joint grant mapping)
  └── GapAgent              (Identification of evidence, method, and population gaps)

Evolution, Reproducibility & Synthesis:
  ├── KnowledgeEvolutionAgent (Drafts KnowledgeChangeProposals; global knowledge write firewall)
  ├── ReproducibilityAgent    (Bit-for-bit code/data execution certificates)
  └── ReportAgent             (Structured, auditable, artifact-linked research report generation)

Verification & Guardrails:
  ├── VerificationAgent     (Independent verifier; double-computation & zero-tolerance citation check)
  ├── AdversarialAgent      (Devil's Advocate; challenges overclaiming, confounding, and bias)
  ├── ReplicationAgent      (Independent pipeline query and analysis replication)
  ├── FactCheckAgent        (Factual assertion check against authoritative databases)
  ├── BiasDetectionAgent    (Publication, selection, geographic, and language bias audit)
  └── KnowledgeRefreshAgent (Scheduled and event-driven refresh of stale knowledge)

Private & Federated:
  ├── PrivateResearchAgent  (Confidential tenant data analysis within classification ceilings)
  └── FederatedAgent        (Local-only compute orchestration; transparent partial failure reporting)
```

---

## 4. Scientific Planning & DAG Orchestration

### Scientific Planning Agent (`ResearchPlan`)
The Planning Agent decomposes the user's research question into an executable Directed Acyclic Graph (DAG) without altering question intent:
- Normalizes questions and identifies key clinical/scientific objectives.
- Formulates subtask nodes with explicit dependencies (`requires`, `blocks`, `verification_dependency`).
- Declares required sources, required datasets, and compute specifications.
- Implements dynamic planning: every execution order modification records `previous_plan`, `new_plan`, `reason`, `trigger`, `agent`, and `timestamp`.
- Enforces plan integrity: cannot drop contradictory evidence or bypass verification.

### DAG Orchestration Engine (`AgentOrchestrator`)
- Executes independent tasks in parallel; executes dependent tasks sequentially.
- Loop limits and detection: enforces maximum step counts (default 50), timeout budgets, and halts circular delegations.
- Dependency failure propagation: if Agent A fails, dependent tasks become `BLOCKED`.
- Transparent partial completion reporting (`ResearchCompletion`):
  $$\text{Coverage Score} = \frac{\text{Completed Tasks}}{\text{Total Subtasks}}$$
  If any subtasks fail or time out, the execution is explicitly marked `PARTIAL` and its limitations documented. The orchestrator **never produces false completion**.

---

## 5. Tool Registry & Sandboxing Security

Every tool must be registered in the `ToolRegistry` with strict metadata:
- **Action Categories**: `READ_ONLY`, `ANALYZE`, `COMPUTE`, `PROPOSE`, `WRITE_PRIVATE`, `WRITE_SHARED`, `REQUEST_APPROVAL`, `EXTERNAL_ACTION`, `PUBLISH`. (Defaults to `READ_ONLY`).
- **Prompt Injection Defense**: Retrieved content (papers, web documents, clinical records) is marked strictly as `DATA`, never `COMMAND`. Injection instructions like *"Ignore all previous instructions"* are neutralized before reaching agent reasoning loops.
- **Tool Injection Defense**: Tool outputs cannot override system policies or security ceilings.
- **Isolated Runtime**: Dedicated credentials per agent service account; no universal admin master keys.
- **Immutable Tool Audit**: Every tool call records execution ID, sanitized arguments, execution status, cost, and latency.

---

## 6. Scoped Memory Model & Tenant Isolation

Agent memory is partitioned into 5 non-overlapping scopes:
1. `WORKING`: In-flight scratchpad for the current reasoning step.
2. `TASK`: Task-scoped findings discarded or promoted upon completion.
3. `PROJECT`: Governed research project workspace memory.
4. `TENANT`: Private institutional memory isolated by `tenant_id`.
5. `LONG_TERM_SCIENTIFIC`: Governed global scientific memory.

### Memory Isolation Rules
- **Hard Tenant Isolation**: Tenant A cannot query Tenant B's memory under any circumstance.
- **Memory Write Firewall**: Agents cannot permanently write new facts, global claims, public terminology, or public relationships into `LONG_TERM_SCIENTIFIC` memory without passing through the Human Governance Gate.
- **Context Snapshots**: Important research runs record the exact snapshot of memories, policies, and source references used, enabling deterministic or stochastic replay.

---

## 7. Human Review Gate & Knowledge Change Proposals

### Human-in-the-Loop Governance
Consequential scientific actions require human review:
- Clinical knowledge release
- Regulatory status changes
- Public knowledge updates
- Private-to-public data release
- External communication

### Review Actions
Reviewers can choose: `APPROVE`, `REJECT`, `MODIFY`, `REQUEST_MORE_EVIDENCE`, `ASSIGN_REVIEWER`, `PAUSE`. Requesters cannot approve their own requests (separation of duties).

### Knowledge Change Proposal Pipeline
When newly discovered research contradicts an existing claim:
1. `KnowledgeEvolutionAgent` detects the conflict.
2. It drafts a formal `KnowledgeChangeProposal` with target object ID, old state, proposed state, evidence package, and impact assessment.
3. Global knowledge remains unchanged until the proposal is reviewed and approved by the Governance Board.

---

## 8. Verification & Acceptance Test Suite

The subsystem was verified against all 14 mandatory acceptance tests defined in Clauses 276–289:

| Clause | Verification Test | Test Description | Result |
| :--- | :--- | :--- | :--- |
| **276** | Tenant Isolation Test | Tenant A private memory is inaccessible to Tenant B queries. | **PASSED** |
| **277** | Agent Publicization Test | Private/Confidential output blocked from public release without approval. | **PASSED** |
| **278** | Agent Fabrication Test | StatisticsAgent asked to compute p-value without data returns "Cannot compute". | **PASSED** |
| **279** | Execution State Lifecycle | Agent transitions through `CREATED` $\rightarrow$ `RUNNING` $\rightarrow$ `COMPLETED`. | **PASSED** |
| **280** | Independent Verification | Fabricated citation and unbacked numbers rejected with `CONTESTED` status. | **PASSED** |
| **281** | Contradiction Preservation | Conflicting trials preserved with root-cause explanation (no forced consensus). | **PASSED** |
| **282** | Traditional Medicine Test | Unmapped humoral concept *Damavi* preserved as `NO_VALID_MAPPING`. | **PASSED** |
| **283** | Causal Guardrails | Observational association restricted; causal overclaiming blocked. | **PASSED** |
| **284** | Simulation Distinction | Monte Carlo simulation output labeled `SIMULATED`, never `OBSERVED`. | **PASSED** |
| **285** | Private Data Access Control | Public agent requesting private tenant dataset is denied access. | **PASSED** |
| **286** | Federated Partial Failure | Failed federated site explicitly reported as `PARTIAL_FEDERATED_RESULT`. | **PASSED** |
| **287** | Knowledge Update Governance | Discrepancy generates `KnowledgeChangeProposal`; no silent rewrite. | **PASSED** |
| **288** | Research Trace Provenance | Execution trace captures all agents, tools, sources, and events. | **PASSED** |
| **289** | Golden End-to-End Workflow | Full 12-stage multi-agent pipeline completes with 100% verified coverage. | **PASSED** |

**Regression Suite Status**:
```text
Ran 237 tests in 0.429s
OK (237 / 237 passing, 0 failures, 0 regressions across Prompts 13–24)
Total FastAPI Routes: 275 routes
```

---

## 9. REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/v1/agents` | Register a new specialist agent definition |
| `GET` | `/v1/agents` | List all approved specialist agents |
| `GET` | `/v1/agents/{id}` | Retrieve details, capabilities, and tools for an agent |
| `POST` | `/v1/agent-tasks` | Create and execute an isolated unit of agent work |
| `GET` | `/v1/agent-tasks/{id}` | Query execution status of an agent task |
| `POST` | `/v1/agent-tasks/{id}/cancel` | Cancel an in-flight agent task |
| `POST` | `/v1/research/plan` | Deconstruct a research question into an executable DAG |
| `POST` | `/v1/research/run` | Execute end-to-end multi-agent research investigation |
| `GET` | `/v1/research/runs/{id}` | Retrieve research execution summary and completion report |
| `GET` | `/v1/agent-runs/{id}/trace` | Retrieve complete step-by-step event trace for a run |
| `GET` | `/v1/agent-tools` | List registered tools, action categories, and schemas |
| `GET` | `/v1/agent-policies` | Retrieve active agent governance and security policies |
| `POST` | `/v1/reviews` | Submit a human review request for high-impact action |
| `POST` | `/v1/reviews/{id}/approve` | Approve a pending review request |
| `POST` | `/v1/reviews/{id}/reject` | Reject a pending review request |
| `GET` | `/v1/agent-incidents` | Query recorded incidents, hallucinations, and policy blocks |
| `GET` | `/v1/agent-metrics` | Retrieve observability metrics (runs, latency, accuracy) |
| `POST` | `/v1/agent-os/proposals` | Submit a `KnowledgeChangeProposal` |
| `GET` | `/v1/agent-os/proposals` | List all pending and reviewed proposals |

---

## 10. Python SDK Reference

The ZMIE Python SDK includes high-level abstractions for multi-agent execution:

```python
from zmie.client import ZMIE

client = ZMIE(base_url="https://api.zmie.ai", api_key="zmie_live_...")

# 1. Inspect registered specialist agents
agents = client.agents.list()
print(f"Total agents available: {len(agents)}")

# 2. Generate a research plan DAG
plan = client.research.plan("Evaluate the clinical efficacy of Berberine in Type 2 Diabetes")
print(f"Generated {len(plan['subtasks'])} sequenced subtasks (Plan ID: {plan['plan_id']})")

# 3. Execute full multi-agent research pipeline
run = client.research.run("Evaluate the clinical efficacy of Berberine in Type 2 Diabetes")
print(f"Run Status: {run['status']}, Coverage: {run['coverage'] * 100:.1f}%")
print(f"Trace ID: {run['trace_id']}")

# 4. Human governance review
review = client.reviews.submit(
    task_id="task-1029",
    triggering_agent_id="agent-safety",
    reason="Confirm pregnancy contraindication caution flag",
    recommendation="Flag caution on public UI"
)
client.reviews.approve(
    review_id=review["review_id"],
    reviewer_user_id="dr-chair-user",
    rationale="Confirmed by pharmacological evidence."
)

# 5. Tool policies & doctrine
policies = client.tools.policies()
print("Doctrine:", policies["doctrine"])
```
