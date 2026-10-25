# ZMIE Scientific Closed-Loop Discovery & Autonomous Knowledge Learning System

```
SCIENTIFIC KNOWLEDGE ──▶ HYPOTHESIS ──▶ EXPERIMENT ──▶ EVIDENCE ──▶ KNOWLEDGE LEARNING SYSTEM
       ▲                                                                      │
       └──────────────────────── Continuous Feedback Loop ────────────────────┘
```

## 1. System Philosophy & Discovery Cycle

The **ZMIE Scientific Closed-Loop Discovery & Autonomous Knowledge Learning System** connects every prior intelligence subsystem (Prompts 13–19) into a self-evolving, epistemically disciplined scientific learning continuum.

Scientific progress does not end when a trial publishes or when a living review is updated. True scientific intelligence continuously asks:
1. What does the current body of knowledge predict?
2. Where are the crucial ambiguities, contradictions, or competing mechanistic claims?
3. What is the single decisive experiment or observational study that maximizes expected information gain $E[\Delta U]$?
4. When empirical data arrives, how should our prior credences, causal DAG weights, and living syntheses update?
5. What assumptions must now be retired, and what new downstream frontiers have opened?

---

## 2. The 5 Continuous Stages

| Stage | Name | Key Operations | Epistemic Boundary |
|---|---|---|---|
| **Stage 1** | **SCIENTIFIC KNOWLEDGE** | Knowledge base aggregation, Causal DAG integration, Living Review baseline snapshot ($t_0$), Shannon entropy calculation | `SUPPORTED_BY_EVIDENCE` / `REPORTED` |
| **Stage 2** | **HYPOTHESIS FORMULATION** | Competing hypothesis clustering, divergence point isolation, falsification criteria specification | `HYPOTHESIZED` |
| **Stage 3** | **EXPERIMENT DESIGN** | In-silico parameter sweeps (Monte Carlo PK/PD), Information Gain optimization ($E[\Delta U]$), Positive/Negative/Vehicle controls, anti-redundancy checks | `MODEL_PREDICTED` (Simulation) |
| **Stage 4** | **EVIDENCE INGESTION** | Ingestion of empirical wet-lab or clinical study data, $p$-value / Bayes factor verification, laboratory provenance verification | `OBSERVED` / `ACTUALLY_TESTED` |
| **Stage 5** | **KNOWLEDGE LEARNING** | Bayesian posterior updating, competing hypothesis weakening/refutation, causal DAG edge re-weighting, living review updates, assumption retirement, frontier question formulation | `SUPPORTED_BY_EVIDENCE` (Updated $t_1$) |

---

## 3. Data Models & Architecture

- **Models File**: [`closed_loop_learning.py`](file:///Users/irfanashraf/Downloads/zmie/services/engine/app/models/closed_loop_learning.py)
  - `KnowledgeStateSnapshot`: Captures immutable state vectors, active hypotheses, confirmed causal edges, and Shannon entropy $H(X)$.
  - `EpistemicDelta`: Formulates exact state transitions ($P(H) \rightarrow P(H|E)$), edge updates, retired assumptions, and opened research questions.
  - `ClosedLoopCycleExecution`: Traceable end-to-end audit record for scientific peer review and regulatory inspection.
- **Engine File**: [`closed_loop_learning.py`](file:///Users/irfanashraf/Downloads/zmie/services/engine/app/research/closed_loop_learning.py)
  - `ScientificClosedLoopLearningEngine`: Orchestrates baseline capture, hypothesis discrimination, simulation, next-best-experiment design, evidence ingestion, and knowledge propagation.
- **API Router**: [`closed_loop_learning.py`](file:///Users/irfanashraf/Downloads/zmie/services/engine/app/api/v1/closed_loop_learning.py)
  - `POST /v1/closed-loop/execute`
  - `GET /v1/closed-loop/snapshot`
  - `GET /v1/closed-loop/executions`
  - `GET /v1/closed-loop/executions/{id}`

---

## 4. Empirical Verification & Showcase

- **Acceptance Test Suite**: [`test_closed_loop_learning_acceptance.py`](file:///Users/irfanashraf/Downloads/zmie/tests/test_closed_loop_learning_acceptance.py)
- **Interactive Demonstration**: [`closed_loop_learning_showcase.py`](file:///Users/irfanashraf/Downloads/zmie/tests/closed_loop_learning_showcase.py)
- **Suite Status**: **150 passing tests**, 200 operational FastAPI endpoints.
