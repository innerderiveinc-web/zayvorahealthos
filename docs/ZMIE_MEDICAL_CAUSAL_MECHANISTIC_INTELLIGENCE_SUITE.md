# ZMIE Medical Causal & Mechanistic Intelligence Suite
## Architecture, Scientific Principles & Implementation Specification

> **Epistemic Maxim:**
> $$\text{Association} \ne \text{Mechanism} \ne \text{Prediction} \ne \text{Causal Effect} \ne \text{Clinical Efficacy}$$
> Mechanistic plausibility $\ne$ proof. Observational correlation $\ne$ causal effect. Computational docking $\ne$ target validation. Animal models $\ne$ human efficacy.

---

## 1. Executive Overview

The **ZMIE Medical Causal & Mechanistic Intelligence Engine** (Prompt 16) provides a first-class scientific inference layer connecting biological entities across multiple scales:

$$\text{Disease} \longrightarrow \text{Phenotype} \longrightarrow \text{Risk Factor} \longrightarrow \text{Exposure} \longrightarrow \text{Intervention} \longrightarrow \text{Compound} \longrightarrow \text{Target} \longrightarrow \text{Protein} \longrightarrow \text{Gene} \longrightarrow \text{Pathway} \longrightarrow \text{Cell} \longrightarrow \text{Tissue} \longrightarrow \text{Organ} \longrightarrow \text{Physiology} \longrightarrow \text{Biomarker} \longrightarrow \text{Clinical Outcome}$$

This subsystem addresses fundamental epistemic fallacies in medical AI:
1. **Conflating Association with Causation:** Observational associations are gated through formal Directed Acyclic Graph (DAG) identification criteria, collider detection, and target trial emulation before being designated as causal.
2. **Ignoring Pharmacokinetic Plausibility:** High-affinity in-vitro cellular targets (e.g., $10\,\mu\text{M}$ assays) are contrasted with human achievable peak plasma concentrations ($C_{\max} \approx 0.07\,\mu\text{M}$ for oral polyphenols/alkaloids) to prevent ungrounded translational leaps.
3. **Ontological Flattening of Traditional Medicine:** Unani (*Mizaj*, *Akhlat*, *Afa'al*) and Ayurveda (*Prakriti*, *Dosha*, *Dhatu*, *Agni*) concepts are preserved in their native theoretical systems rather than forcefully reduced to isolated modern biomarkers.
4. **Premature Consensus on Competing Mechanisms:** Divergent scientific hypotheses are maintained in explicit competing clusters, complete with discriminating experimental protocols.

---

## 2. Core Architecture & Scale Hierarchy

### 2.1 Biological Scales
The engine operates across nine discrete biological scales:
1. `SUBATOMIC_CHEMICAL`: Functional groups, ligand stereochemistry, metabolites.
2. `MOLECULAR_TARGET`: GPCRs, kinases, nuclear receptors, ion channels, transporters.
3. `PATHWAY_NETWORK`: Intracellular signaling, metabolic flux, transcriptional networks.
4. `ORGANELLE_CELLULAR`: Mitochondrial respiration, lysosomal autophagy, cell survival/apoptosis.
5. `TISSUE_MICROENVIRONMENT`: Extracellular matrix, inflammatory infiltrate, paracrine gradients.
6. `ORGAN_SYSTEM`: Hepatic glucose output, renal proximal reabsorption, cardiac remodeling.
7. `ORGANISM_PHYSIOLOGY`: Systemic blood pressure, glycemic homeostasis, neuroendocrine tone.
8. `CLINICAL_PHENOTYPE`: Microvascular/macrovascular outcomes, symptom severity scales.
9. `POPULATION_OUTCOME`: Real-world incidence, hospital admission rates, all-cause mortality.

### 2.2 Epistemic State Classifications

#### Causality States
- `UNKNOWN`: No evaluated causal relationship.
- `HYPOTHESIZED`: Proposed causal link without identified structural graph.
- `ASSOCIATED`: Statistical dependency observed, but unmeasured confounding or selection bias suspected.
- `MECHANISTICALLY_SUPPORTED`: Biological pathway plausible, but formal population causal identification incomplete.
- `CAUSALLY_SUPPORTED`: Defensible under backdoor criterion, negative controls, and target trial emulation.
- `CAUSALLY_CONTESTED`: Severe identification threats (e.g. collider stratification / M-bias).
- `INSUFFICIENT_EVIDENCE`: Inconclusive data.

#### Mechanism States
- `UNKNOWN_MECHANISM`: Observed clinical phenomenon with unknown biological substrate.
- `PROPOSED_MECHANISM`: Hypothetical mechanism without direct experimental confirmation.
- `PARTIALLY_SUPPORTED`: Evidence for isolated steps in the mechanistic chain.
- `PRECLINICALLY_SUPPORTED`: Validated in cell lines or animal models at translatable exposures.
- `HUMAN_MECHANISTIC_EVIDENCE`: Direct human target engagement and biomarker modulation at therapeutic doses.
- `SUPPORTED_WITH_LIMITATIONS`: Established mechanism burdened by significant translational or PK gaps.
- `CONFLICTING_MECHANISTIC_EVIDENCE`: Competing, mutually incompatible mechanisms supported by empirical data.

---

## 3. Scientific Subsystems

### 3.1 Multi-Level Biological Decomposition & PK Plausibility
The engine decomposes interventions through structured multi-step paths:
- **Compound:** Canonical identity, metabolites, $C_{\max}$, bioavailability, AUC, protein binding, CYP/transporter affinities.
- **Target Engagement:** Binding kinetics ($K_d, K_i, \text{IC}_{50}$), cellular localization, rodent-human homology.
- **Pathway Modulation:** Upstream triggers, downstream effectors, feedback inhibition.
- **Translational Gap Detection:**
  $$\text{Ratio} = \frac{\text{Concentration}_{\text{in-vitro}}}{\text{Achievable } C_{\max, \text{human}}}$$
  If $\text{Ratio} > 10$, the engine automatically raises an `IN_VITRO_CONCENTRATION_EXCEEDS_HUMAN_CMAX` warning and demotes the mechanistic state to `SUPPORTED_WITH_LIMITATIONS`.

### 3.2 Causality Firewall & DAG Identification Gatekeeper
1. **Backdoor Criterion Verification:** Verifies all confounders on backdoor paths are observed and controlled.
2. **Collider Stratification Detection:** Gating rule: Conditioning on a common effect (collider node) opens spurious non-causal paths (Berkson's bias / M-bias). The firewall immediately marks the proposition `IDENTIFICATION_NOT_ESTABLISHED` and `CAUSALLY_CONTESTED`.
3. **Sensitivity Analysis (E-value):** Computes minimum strength of unmeasured confounding required to explain away the observed effect:
   $$E\text{-value} = RR + \sqrt{RR(RR - 1)}$$
4. **Target Trial Emulation:** Formulates protocol components (eligibility, treatment strategy, assignment emulation, follow-up, causal contrasts).

### 3.3 Multi-System Traditional Medicine Parity
- **Unani Framework:**
  - *Mizaj* (Temperament: Hot/Cold/Dry/Moist degrees 1–4).
  - *Akhlat* (Humors: Dam, Balgham, Safra, Sauda).
  - *Afa'al* (Pharmacological actions: Mohallil, Muqawwi, Munzij).
  - *Tadbir-e-Adwiyah* (Pharmaceutical detoxification and rectification).
- **Ayurveda Framework:**
  - *Doshas* (Vata, Pitta, Kapha) and *Dhatus* (Tissues).
  - *Rasa-Virya-Vipaka-Prabhava* (Pharmacological energetic profile).
  - *Shodhana* (Purification) and *Bhavana* (Trituration).
- **Bioenhancers & Polyherbal Networks:**
  - Models bioavailability amplification (e.g. *Trikatu* / Piperine inhibiting intestinal/hepatic glucuronidation and P-gp efflux, enhancing Curcumin exposure by 2.5–20-fold).
  - Identifies narrow therapeutic index herb-drug interaction advisories (e.g. co-administration with Warfarin, Theophylline, Phenytoin).
- **Non-Reductive Epistemic Bridging:** Native concepts are linked via `CONCEPTUALLY_RELATED` or `SYSTEM_ANALOGUE_HYPOTHESIS` with explicit disclaimers preventing false reductionist equivalence.

### 3.4 Competing Hypotheses & Next-Best Experiments
Rather than forcing artificial consensus:
- Competing mechanisms (e.g. Berberine direct systemic AMPK vs gut microbiome-mediated GLP-1 secretion) are clustered together.
- The engine generates targeted **Next-Best Discriminating Experiments** specifying factorial designs, discriminating readouts (e.g. portal GLP-1 vs hepatic phospho-AMPK in germ-free mice), and expected outcomes under each competing hypothesis.

---

## 4. API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/v1/causal-mechanistic/mechanisms/decompose` | Decompose compound into multi-scale biological chain with PK gap detection |
| `GET` | `/v1/causal-mechanistic/mechanisms/competing/{compound_id}` | Retrieve competing mechanistic hypotheses cluster |
| `POST` | `/v1/causal-mechanistic/mechanisms/experiments/propose` | Propose discriminating next-best experiment for competing hypotheses |
| `POST` | `/v1/causal-mechanistic/causal/dag/validate` | Causality Firewall: Validate DAG identification, detect colliders & E-value |
| `POST` | `/v1/causal-mechanistic/traditional/bridge` | Map native traditional terms to modern correlates with epistemic warnings |
| `GET` | `/v1/causal-mechanistic/traditional/formulations/{id}/interactions` | Analyze polyherbal synergy, bioenhancement, and herb-drug interactions |
| `GET` | `/v1/causal-mechanistic/entities/compounds/{compound_id}` | Retrieve compound entity with PK/ADME profile |
| `GET` | `/v1/causal-mechanistic/entities/targets/{target_id}` | Retrieve target record with species homology |
| `GET` | `/v1/causal-mechanistic/entities/pathways/{pathway_id}` | Retrieve biological pathway record |
| `POST` | `/v1/causal-mechanistic/snapshots` | Capture versioned snapshot of mechanistic proposition |

---

## 5. Verification & Acceptance Testing

The suite is verified by:
1. **Unit & Acceptance Suite:** `tests/test_causal_mechanistic_acceptance.py` (11/11 tests passing, covering multi-scale decomposition, gap detection, DAG identification gating, collider stratification, traditional parity, and REST APIs).
2. **Full Regression Suite:** `tests/test_*.py` (121/121 tests passing across all 16 prompt subsystems).
3. **End-to-End Showcase:** `tests/causal_mechanistic_showcase.py` executing live demonstrations of all 5 scientific scenarios.
