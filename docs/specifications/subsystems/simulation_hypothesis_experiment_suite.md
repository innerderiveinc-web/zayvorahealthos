# ZMIE Medical Knowledge Simulation, Research Hypothesis & Next-Best-Experiment Engine

## 1. System Overview & Epistemic Maxims

The **ZMIE Medical Knowledge Simulation, Research Hypothesis & Next-Best-Experiment Engine** (Prompt 19) converts existing medical literature, causal graphs, and living evidence syntheses into an active scientific inquiry and simulation architecture:

$$\text{Knowledge Integration} \longrightarrow \text{Causal/Mechanistic Model} \longrightarrow \text{Uncertainty Identification} \longrightarrow \text{Hypothesis Generation} \longrightarrow \text{Simulation} \longrightarrow \text{Next-Best-Experiment} \longrightarrow \text{Observed Data} \longrightarrow \text{Bayesian Update}$$

### Strict Epistemic Boundaries

In accordance with scientific and regulatory integrity, the engine strictly maintains 6 non-overlapping epistemic states:
1. `OBSERVED`: Direct experimental, laboratory, or clinical measurement.
2. `REPORTED`: Published findings from literature or clinical study reports.
3. `SUPPORTED_BY_EVIDENCE`: Synthesized conclusion meeting predefined evidentiary thresholds.
4. `MODEL_PREDICTED`: Computational output from mathematical/simulation algorithms.
5. `HYPOTHESIZED`: Proposed conceptual proposition awaiting empirical test.
6. `ACTUALLY_TESTED`: Empirical study conducted with definitive methodology and controls.

> [!CAUTION]
> **Core Scientific Epistemic Axioms**:
> - $\text{Prediction} \ne \text{Observation}$
> - $\text{Simulation} \ne \text{Experiment}$
> - $\text{Simulation} \ne \text{Proof}$
> - $\text{Hypothesis} \ne \text{Fact}$
> - $\text{Mechanistic Plausibility} \ne \text{Clinical Efficacy}$
> - $\text{Information Gain} \ne \text{Clinical Value}$
> - $\text{Model Posterior} \ne \text{Empirical Proof}$

---

## 2. Architecture & Subsystems

```
┌────────────────────────────────────────────────────────────────────────┐
│                   ZMIE SIMULATION & HYPOTHESIS ENGINE                  │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Hypothesis Formulation & Management                                 │
│    - Mechanistic, Causal, Predictive, Translational                    │
│    - Traditional Medicine Bridge Hypotheses (Unani/Ayurveda)          │
│                                                                        │
│ 2. Competing Hypothesis Discrimination                                  │
│    - Isolate Divergence Points                                         │
│    - Identify Decisive Biomarkers & Endpoint Readouts                 │
│                                                                        │
│ 3. Parametric Simulation Sweeps (Monte Carlo PK/PD)                   │
│    - Two-Compartment Pharmacokinetics                                 │
│    - Parameter Uncertainty Distributions (Normal, Lognormal, Uniform) │
│    - 95% Credible Intervals & Mandatory Epistemic Disclaimers          │
│                                                                        │
│ 4. Next-Best-Experiment Design                                         │
│    - Expected Information Gain E[ΔU] (Entropy Reduction)               │
│    - Rigorous Controls: Positive, Negative, Orthogonal Knockouts      │
│    - Anti-Redundancy Verification (Checks literature/RWE first)        │
│    - Human-in-the-Loop Approval Safeguard                              │
│                                                                        │
│ 5. Empirical Ingestion & Bayesian Posterior Updating                   │
│    - Ingests Observed Results with P-values / Bayes Factors           │
│    - Updates Target Hypothesis (SUPPORTED / REJECTED)                 │
│    - Weakens/Prunes Competing Explanations                             │
│                                                                        │
│ 6. Research Opportunity Portfolios                                     │
│    - Prioritization across Feasibility, Clinical Need, and Cost        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Models (`services/engine/app/models/simulation_hypothesis.py`)

- [`Hypothesis`](file:///Users/irfanashraf/Downloads/zmie/services/engine/app/models/simulation_hypothesis.py): Formal representation with prior/posterior probabilities, assumptions, causal DAG edges, observable predictions, and disconfirming falsification criteria.
- [`ObservablePrediction`](file:///Users/irfanashraf/Downloads/zmie/services/engine/app/models/simulation_hypothesis.py): Falsifiable quantitative expectation tagged `MODEL_PREDICTED`.
- [`DisconfirmingCriterion`](file:///Users/irfanashraf/Downloads/zmie/services/engine/app/models/simulation_hypothesis.py): Explicit criterion threshold that would falsify the hypothesis.
- [`ScientificModel`](file:///Users/irfanashraf/Downloads/zmie/services/engine/app/models/simulation_hypothesis.py): Kinetic, compartmental PK/PD, or systems dynamics computational model.
- [`SimulationRun`](file:///Users/irfanashraf/Downloads/zmie/services/engine/app/models/simulation_hypothesis.py): Sweep run tracking timecourses, parameter distributions, 95% credible intervals, and epistemic disclaimer.
- [`ExperimentProposal`](file:///Users/irfanashraf/Downloads/zmie/services/engine/app/models/simulation_hypothesis.py): Actionable protocol with controls, expected information gain $E[\Delta U]$, discrimination power, feasibility, and human review requirement.
- [`ExperimentResultRecord`](file:///Users/irfanashraf/Downloads/zmie/services/engine/app/models/simulation_hypothesis.py): Empirical finding tagged `OBSERVED`, updating Bayesian posteriors and competing models.

---

## 4. API Endpoints (`services/engine/app/api/v1/simulation_hypothesis.py`)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/v1/simulation-hypothesis/hypotheses` | Lists all registered hypotheses with current posteriors |
| `POST` | `/v1/simulation-hypothesis/hypotheses` | Registers a new hypothesis with falsification criteria |
| `GET` | `/v1/simulation-hypothesis/hypotheses/{id}` | Retrieves full hypothesis record and predictions |
| `POST` | `/v1/simulation-hypothesis/hypotheses/competing/discriminate` | Contrasts competing hypotheses to find decisive tests |
| `POST` | `/v1/simulation-hypothesis/hypotheses/generate-from-conflict` | Formulates competing hypotheses from evidence conflicts |
| `POST` | `/v1/simulation-hypothesis/models` | Registers mathematical/computational model |
| `POST` | `/v1/simulation-hypothesis/simulations/run` | Executes Monte Carlo simulation sweep |
| `POST` | `/v1/simulation-hypothesis/experiments/next-best` | Generates optimal experiment proposal via information gain |
| `POST` | `/v1/simulation-hypothesis/experiments/results` | Ingests empirical result and updates Bayesian posterior |
| `GET` | `/v1/simulation-hypothesis/opportunities` | Discovers prioritized research opportunities |

---

## 5. Verification & Acceptance

- **Acceptance Test Suite**: [`tests/test_simulation_hypothesis_acceptance.py`](file:///Users/irfanashraf/Downloads/zmie/tests/test_simulation_hypothesis_acceptance.py)
  - 8 comprehensive test cases verifying epistemic boundaries, Unani bridge hypotheses, competing model discrimination, PK/PD simulations, next-best-experiment design, result ingestion with Bayesian updates, and REST APIs.
- **End-to-End Showcase**: [`tests/simulation_hypothesis_showcase.py`](file:///Users/irfanashraf/Downloads/zmie/tests/simulation_hypothesis_showcase.py)
- **Total Test Suite Status**: **147 passing tests** with 0 failures, 196 registered FastAPI routes.
