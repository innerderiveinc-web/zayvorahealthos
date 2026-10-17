"""
ZMIE Medical Causal & Mechanistic Intelligence Engine Models
Connecting molecular targets, pathways, physiology, biomarkers, and clinical outcomes
with strict epistemic boundaries: Association != Mechanism != Causal Effect != Clinical Efficacy.
"""

from typing import List, Dict, Any, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field


class BiologicalScale(str, Enum):
    SUBATOMIC_CHEMICAL = "SUBATOMIC_CHEMICAL"
    MOLECULAR_TARGET = "MOLECULAR_TARGET"
    PATHWAY_NETWORK = "PATHWAY_NETWORK"
    ORGANELLE_CELLULAR = "ORGANELLE_CELLULAR"
    TISSUE_MICROENVIRONMENT = "TISSUE_MICROENVIRONMENT"
    ORGAN_SYSTEM = "ORGAN_SYSTEM"
    ORGANISM_PHYSIOLOGY = "ORGANISM_PHYSIOLOGY"
    CLINICAL_PHENOTYPE = "CLINICAL_PHENOTYPE"
    POPULATION_OUTCOME = "POPULATION_OUTCOME"


class CausalityState(str, Enum):
    UNKNOWN = "UNKNOWN"
    HYPOTHESIZED = "HYPOTHESIZED"
    ASSOCIATED = "ASSOCIATED"
    MECHANISTICALLY_SUPPORTED = "MECHANISTICALLY_SUPPORTED"
    CAUSALLY_SUPPORTED = "CAUSALLY_SUPPORTED"
    CAUSALLY_CONTESTED = "CAUSALLY_CONTESTED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class MechanismState(str, Enum):
    UNKNOWN_MECHANISM = "UNKNOWN_MECHANISM"
    PROPOSED_MECHANISM = "PROPOSED_MECHANISM"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    PRECLINICALLY_SUPPORTED = "PRECLINICALLY_SUPPORTED"
    HUMAN_MECHANISTIC_EVIDENCE = "HUMAN_MECHANISTIC_EVIDENCE"
    SUPPORTED_WITH_LIMITATIONS = "SUPPORTED_WITH_LIMITATIONS"
    CONFLICTING_MECHANISTIC_EVIDENCE = "CONFLICTING_MECHANISTIC_EVIDENCE"


class ExperimentalValidationLevel(str, Enum):
    COMPUTATIONAL_IN_SILICO = "COMPUTATIONAL_IN_SILICO"
    IN_VITRO_ACELLULAR = "IN_VITRO_ACELLULAR"
    IN_VITRO_CELL_LINE = "IN_VITRO_CELL_LINE"
    IN_VITRO_PRIMARY_HUMAN_CELLS = "IN_VITRO_PRIMARY_HUMAN_CELLS"
    EX_VIVO_TISSUE = "EX_VIVO_TISSUE"
    ORGANOID_3D = "ORGANOID_3D"
    ANIMAL_IN_VIVO = "ANIMAL_IN_VIVO"
    HUMAN_PK_PD = "HUMAN_PK_PD"
    HUMAN_CLINICAL_TRIAL = "HUMAN_CLINICAL_TRIAL"
    EPIDEMIOLOGICAL_OBSERVATIONAL = "EPIDEMIOLOGICAL_OBSERVATIONAL"


class CausalIdentificationStatus(str, Enum):
    IDENTIFIED = "IDENTIFIED"
    UNIDENTIFIED = "UNIDENTIFIED"
    IDENTIFICATION_NOT_ESTABLISHED = "IDENTIFICATION_NOT_ESTABLISHED"
    CONDITIONAL_ON_UNOBSERVED = "CONDITIONAL_ON_UNOBSERVED"


class MedicalTraditionSystem(str, Enum):
    ALLOPATHIC_CONVENTIONAL = "ALLOPATHIC_CONVENTIONAL"
    UNANI = "UNANI"
    AYURVEDA = "AYURVEDA"
    CHINESE_MEDICINE = "CHINESE_MEDICINE"


class MechanismStepType(str, Enum):
    BINDS_TO = "BINDS_TO"
    INHIBITS = "INHIBITS"
    ACTIVATES = "ACTIVATES"
    PHOSPHORYLATES = "PHOSPHORYLATES"
    DEPHOSPHORYLATES = "DEPHOSPHORYLATES"
    UPREGULATES = "UPREGULATES"
    DOWNREGULATES = "DOWNREGULATES"
    TRANSLOCATES = "TRANSLOCATES"
    CLEAVES = "CLEAVES"
    METABOLIZES_TO = "METABOLIZES_TO"
    MODULATES = "MODULATES"
    CAUSES_PHENOTYPE = "CAUSES_PHENOTYPE"


# -------------------------------------------------------------
# Entity Records
# -------------------------------------------------------------

class CompoundMetabolite(BaseModel):
    metabolite_id: str
    name: str
    active: bool = False
    toxic: bool = False
    enzyme_responsible: Optional[str] = None
    half_life_hours: Optional[float] = None


class PKADMEProfile(BaseModel):
    absorption_bioavailability_pct: Optional[float] = None
    cmax_human_achievable_umol: Optional[float] = None  # in micromolar (uM)
    tmax_hours: Optional[float] = None
    auc_ug_h_ml: Optional[float] = None
    volume_distribution_l_kg: Optional[float] = None
    plasma_protein_binding_pct: Optional[float] = None
    terminal_half_life_hours: Optional[float] = None
    cyp_interactions: List[str] = Field(default_factory=list)  # e.g. ["CYP3A4 inhibitor", "CYP2D6 substrate"]
    transporter_interactions: List[str] = Field(default_factory=list)  # e.g. ["P-gp substrate"]
    cns_penetration: bool = False
    notes: Optional[str] = None


class CompoundRecord(BaseModel):
    compound_id: str
    canonical_name: str
    synonyms: List[str] = Field(default_factory=list)
    chemical_class: Optional[str] = None
    smiles: Optional[str] = None
    inchikey: Optional[str] = None
    metabolites: List[CompoundMetabolite] = Field(default_factory=list)
    pk_adme: Optional[PKADMEProfile] = None
    source_origin: MedicalTraditionSystem = MedicalTraditionSystem.ALLOPATHIC_CONVENTIONAL


class TargetRecord(BaseModel):
    target_id: str
    gene_symbol: str
    canonical_name: str
    uniprot_id: Optional[str] = None
    target_class: str  # Kinase, GPCR, Nuclear Receptor, Ion Channel, Transporter, Enzyme
    cellular_localization: str  # Membrane, Cytosol, Nucleus, Mitochondria, Extracellular
    physiologic_role: str
    species_homology_mouse_pct: Optional[float] = None
    known_ligands: List[str] = Field(default_factory=list)


class PathwayRecord(BaseModel):
    pathway_id: str  # e.g. KEGG:hsa04151, REACTOME:R-HSA-1640170
    name: str
    domain: str  # Metabolism, Immunology, Apoptosis, Signal Transduction, Cell Cycle
    upstream_inputs: List[str] = Field(default_factory=list)
    downstream_effectors: List[str] = Field(default_factory=list)
    feedback_loops: List[str] = Field(default_factory=list)
    tissue_specificity: List[str] = Field(default_factory=list)


class BiomarkerRecord(BaseModel):
    biomarker_id: str
    name: str
    biomarker_type: str  # DIAGNOSTIC, PROGNOSTIC, PREDICTIVE, PHARMACODYNAMIC, SURROGATE, SAFETY
    matrix: str  # Serum, Plasma, Whole Blood, Urine, CSF, Tissue
    reference_range: Optional[str] = None
    surrogate_for_outcome: Optional[str] = None


class OrganAxisRecord(BaseModel):
    axis_id: str
    name: str  # e.g. Gut-Liver-Axis, HPA-Axis, Renin-Angiotensin-Aldosterone-System
    participating_organs: List[str]
    mediating_messengers: List[str]  # e.g. Cortisol, Bile acids, Short-chain fatty acids
    regulatory_feedback: str


# -------------------------------------------------------------
# Traditional Medicine Epistemic Formulations & Frameworks
# -------------------------------------------------------------

class UnaniMizajProfile(BaseModel):
    hotness_degree: int = 0  # 0 to 4
    coldness_degree: int = 0  # 0 to 4
    dryness_degree: int = 0  # 0 to 4
    moistness_degree: int = 0  # 0 to 4
    primary_temperament: str  # e.g. "Har-Yabis" (Hot & Dry), "Barid-Yabis" (Cold & Dry)
    dominant_khilt: str  # Dam, Balgham, Safra, Sauda
    afaaal_actions: List[str] = Field(default_factory=list)  # Mohallil, Muqawwi, Munzij, etc.


class AyurvedaDoshaProfile(BaseModel):
    vata_effect: str  # Shamaka (pacifying), Kopaka (aggravating), etc.
    pitta_effect: str
    kapha_effect: str
    rasa_tastes: List[str] = Field(default_factory=list)  # Madhura, Amla, Lavana, Tikta, Katu, Kashaya
    virya_potency: str  # Ushna (hot) or Sheeta (cold)
    vipaka_post_digestive: str  # Madhura, Amla, Katu
    prabhava_special_action: Optional[str] = None
    dhatu_target: List[str] = Field(default_factory=list)  # Rasa, Rakta, Mamsa, Meda, Asthi, Majja, Shukra
    srotas_channel: List[str] = Field(default_factory=list)


class TraditionalMedicineBridge(BaseModel):
    native_term: str
    tradition: MedicalTraditionSystem
    native_definition: str
    modern_biological_correlate: Optional[str] = None
    bridge_relation_type: str = "CONCEPTUALLY_RELATED"  # NEVER "IDENTICAL_TO"
    epistemic_warning: str = (
        "Traditional holistic construct cannot be reduced strictly to single biochemical pathways. "
        "Correlate provided solely as a research translational hypothesis."
    )


class MultiConstituentFormulation(BaseModel):
    formulation_id: str
    name: str
    tradition: MedicalTraditionSystem
    chief_ingredients: List[Dict[str, Any]]  # [{"herb": "Curcuma longa", "role": "Active", "ratio": 1.0}]
    bioenhancer_adjuvant: Optional[Dict[str, Any]] = None  # e.g. Piperine increasing Curcumin bioavailability
    synergy_mechanism: Optional[str] = None
    processing_purification_method: Optional[str] = None  # Shodhana or Tadbir
    known_herb_drug_interactions: List[str] = Field(default_factory=list)


# -------------------------------------------------------------
# Mechanistic Propositions & Multi-Hop Biological Decomposition
# -------------------------------------------------------------

class MechanismStep(BaseModel):
    step_index: int
    source_entity_id: str
    source_scale: BiologicalScale
    step_type: MechanismStepType
    target_entity_id: str
    target_scale: BiologicalScale
    experimental_level: ExperimentalValidationLevel
    species: str = "HOMO_SAPIENS"
    concentration_tested_umol: Optional[float] = None
    human_achievable_cmax_umol: Optional[float] = None
    is_pk_plausible: bool = True
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class TranslationalGapReport(BaseModel):
    has_gap: bool
    flags: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)
    in_vitro_vs_human_cmax_ratio: Optional[float] = None
    target_engagement_in_human_proven: bool = False
    epistemic_verdict: str


class MechanisticProposition(BaseModel):
    proposition_id: str
    intervention_or_compound_id: str
    final_outcome: str
    mechanism_state: MechanismState
    steps: List[MechanismStep] = Field(default_factory=list)
    translational_gap: TranslationalGapReport
    competing_hypotheses_count: int = 1
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    summary_narrative: str


# -------------------------------------------------------------
# Causal Inference & Directed Acyclic Graph (DAG) Structures
# -------------------------------------------------------------

class TargetTrialEmulation(BaseModel):
    eligibility_criteria: str
    treatment_strategy: str
    assignment_procedure: str
    follow_up_period: str
    outcome_specification: str
    causal_contrast: str = "PER_PROTOCOL"  # or INTENTION_TO_TREAT
    analysis_plan: str


class DAGNode(BaseModel):
    node_id: str
    label: str
    node_type: str  # EXPOSURE, OUTCOME, CONFOUNDER, MEDIATOR, COLLIDER, INSTRUMENTAL_VARIABLE
    observed: bool = True


class DAGEdge(BaseModel):
    source_node_id: str
    target_node_id: str
    direction: str = "DIRECTED"
    assumed: bool = True


class CausalProposition(BaseModel):
    proposition_id: str
    exposure: str
    outcome: str
    causality_state: CausalityState
    identification_status: CausalIdentificationStatus
    dag_nodes: List[DAGNode] = Field(default_factory=list)
    dag_edges: List[DAGEdge] = Field(default_factory=list)
    confounders_controlled: List[str] = Field(default_factory=list)
    unmeasured_confounding_suspected: bool = False
    collider_stratification_detected: bool = False
    negative_control_exposure: Optional[str] = None
    negative_control_outcome: Optional[str] = None
    e_value: Optional[float] = None  # Minimum strength of unmeasured confounder to explain away effect
    estimated_causal_effect: Optional[Dict[str, Any]] = None  # {"point": -0.85, "ci_95": [-1.10, -0.60], "unit": "HbA1c %", "method": "TMLE"}
    target_trial: Optional[TargetTrialEmulation] = None
    epistemic_disclaimer: str = (
        "Causal claims are subject to untestable identifying assumptions (positivity, exchangeability, consistency). "
        "Observational association alone does not establish causation."
    )


# -------------------------------------------------------------
# Competing Mechanisms & Next-Best Experiment
# -------------------------------------------------------------

class CompetingMechanismCluster(BaseModel):
    cluster_id: str
    phenomenon: str
    primary_hypothesis: MechanisticProposition
    competing_hypotheses: List[MechanisticProposition] = Field(default_factory=list)
    points_of_divergence: List[str] = Field(default_factory=list)
    resolution_status: str = "UNRESOLVED_COMPETING"


class NextBestExperimentProposal(BaseModel):
    proposal_id: str
    competing_cluster_id: str
    research_question: str
    recommended_experimental_model: ExperimentalValidationLevel
    design_protocol: str
    discriminating_biomarker_or_readout: str
    expected_outcome_if_hypothesis_a: str
    expected_outcome_if_hypothesis_b: str
    feasibility_score: float = Field(default=0.8, ge=0.0, le=1.0)
    translational_value: str


# -------------------------------------------------------------
# Knowledge Evolution & Versioning
# -------------------------------------------------------------

class MechanismSnapshot(BaseModel):
    snapshot_id: str
    timestamp: str
    proposition_id: str
    mechanism_state: MechanismState
    steps_count: int
    confidence_score: float


class MechanisticKnowledgeDiff(BaseModel):
    previous_snapshot_id: str
    new_snapshot_id: str
    changed_state: bool
    state_transition: Optional[str] = None  # e.g. "PRECLINICALLY_SUPPORTED -> HUMAN_MECHANISTIC_EVIDENCE"
    new_steps_added: int = 0
    refuted_steps: int = 0
    change_summary: str
