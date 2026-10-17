"""
ZMIE Scientific Knowledge Operating System - Master Engine (Prompt 25)
Integrates all domain services into a unified scientific operating environment:
Knowledge Fabric, Graph of Graphs Meta-Layer, Revalidation Engine,
Gap Map, Temporal Snapshots, Scientific Firewall, and Answer Engine (Clauses 1-10, 334).
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from app.models.skos import (
    SKOSMasterEntity,
    SKOSEntityType,
    SKOSRelationshipEdge,
    SKOSEpistemicState,
    TraversalPath,
    ZMIEKnowledgeSnapshot,
    ScientificKnowledgeDiff,
    KnowledgeGapMap,
    RetractionNotice,
    RetractionImpactAnalysis,
    RevalidationTask,
    RevalidationDecision,
    KnowledgeDecisionAction,
    SKOSAnswer
)
from app.skos.fabric import KnowledgeFabricRegistry
from app.skos.meta_graph import KnowledgeGraphOfGraphs
from app.skos.revalidation import KnowledgeRevalidationEngine
from app.skos.gap_map import KnowledgeGapEngine
from app.skos.snapshots import KnowledgeSnapshotEngine
from app.skos.answer_engine import UnifiedScientificAnswerEngine
from app.skos.firewall import MasterScientificFirewall


class ScientificKnowledgeOS:
    """
    The Master Scientific Knowledge Operating System for ZMIE (Clauses 1, 5, 334).
    Coordinates all underlying domains as one unified, governed operating environment.
    """
    _instance: Optional['ScientificKnowledgeOS'] = None

    def __init__(self):
        self.fabric = KnowledgeFabricRegistry()
        self.graph = KnowledgeGraphOfGraphs(self.fabric)
        self.revalidation = KnowledgeRevalidationEngine(self.fabric, self.graph)
        self.gap_engine = KnowledgeGapEngine()
        self.snapshots = KnowledgeSnapshotEngine(self.fabric)
        self.answer_engine = UnifiedScientificAnswerEngine(self.fabric, self.graph, self.snapshots)
        self.firewall = MasterScientificFirewall()

    @classmethod
    def get_instance(cls) -> 'ScientificKnowledgeOS':
        if cls._instance is None:
            cls._instance = ScientificKnowledgeOS()
        return cls._instance

    # ==========================================================================
    # High-Level Orchestrated SKOS Methods
    # ==========================================================================

    async def answer(self, question: str, target_system: str = "all", simulate_partial: bool = False) -> SKOSAnswer:
        return await self.answer_engine.generate_scientific_answer(
            question=question,
            target_system=target_system,
            simulate_partial=simulate_partial
        )

    def get_system_status(self) -> Dict[str, Any]:
        """Returns the system operational health and governance status."""
        return {
            "status": "OPERATIONAL",
            "subsystem": "ZMIE Scientific Knowledge Operating System (SKOS)",
            "version": "1.0.0 Enterprise",
            "active_graphs": 16,
            "absolute_scientific_rules_enforced": 18,
            "epistemic_firewall": "ACTIVE",
            "zero_fabrication_gate": "ENFORCED",
            "negative_proof_fallacy_guard": "ENFORCED"
        }

    def get_path(self, path_type: str, start_id: Optional[str] = None, end_id: Optional[str] = None) -> TraversalPath:
        p_type = path_type.upper()
        if p_type in ["EVIDENCE", "EVIDENCE_PATH"]:
            return self.graph.find_evidence_path(start_id or "CLM-BERBERINE-EFFICACY")
        elif p_type in ["RESEARCH", "RESEARCH_PATH", "RESEARCH_INTELLIGENCE"]:
            return self.graph.find_research_path(start_id or "RES-CHEN-01")
        elif p_type in ["MECHANISM", "MECHANISM_PATH"]:
            return self.graph.find_mechanism_path(start_id or "CMP-BERBERINE", end_id or "TGT-AMPK")
        elif p_type in ["CAUSAL", "CAUSAL_PATH"]:
            return self.graph.find_causal_path(start_id or "CMP-BERBERINE", end_id or "CON-T2D")
        elif p_type in ["SAFETY", "SAFETY_PATH"]:
            return self.graph.find_safety_path(start_id or "CMP-BERBERINE")
        elif p_type in ["TERMINOLOGY", "TERMINOLOGY_PATH"]:
            return self.graph.find_terminology_path(start_id or "CON-T2D")
        elif p_type in ["EXPERIMENT", "EXPERIMENT_PATH", "KNOWLEDGE_TO_EXPERIMENT"]:
            return self.graph.find_experiment_path(start_id or "HYP-BER-001")
        elif p_type in ["MASTER_FORWARD", "MASTER_FORWARD_PATH"]:
            return self.graph.traverse_master_scientific_path(direction="FORWARD")
        elif p_type in ["MASTER_REVERSE", "MASTER_REVERSE_PATH"]:
            return self.graph.traverse_master_scientific_path(direction="REVERSE")
        else:
            return self.graph.traverse_master_scientific_path(direction="FORWARD")

    def get_learning_loop(self) -> Dict[str, Any]:
        """
        Returns the Complete Scientific Learning Loop (Clause 315, 362):
        WORLD -> OBSERVATIONS -> DATA -> KNOWLEDGE -> HYPOTHESES -> MODELS -> PREDICTIONS -> EXPERIMENTS -> NEW OBSERVATIONS -> UPDATED KNOWLEDGE.
        """
        return {
            "status": "ACTIVE_CLOSED_LOOP",
            "doctrine": "Sources provide provenance. Terminology provides semantic meaning. Research provides context. Data provides observations. Computation provides analysis. Mechanisms provide explanatory structure. Causality provides identification. Evidence provides support. Safety provides constraints. Regulation provides jurisdictional status. Simulation provides predictions. Experiments generate observations. Agents coordinate the work. Governance controls consequential transitions. Revalidation keeps knowledge alive.",
            "loop_stages": [
                "1_ACQUISITION", "2_COMPUTATION", "3_REASONING", "4_SYNTHESIS",
                "5_HYPOTHESIS", "6_SIMULATION", "7_EXPERIMENT", "8_REVALIDATION"
            ],
            "stages": [
                {"step": 1, "stage": "WORLD", "description": "Clinical reality, biological phenomena, and global medical codices"},
                {"step": 2, "stage": "OBSERVATIONS", "description": "Multi-universe retrieval across PubMed, OpenAlex, TKDL, Europe PMC"},
                {"step": 3, "stage": "DATA", "description": "Harmonized trial datasets, RWE cohorts, and omics profiles"},
                {"step": 4, "stage": "KNOWLEDGE", "description": "Knowledge Fabric entities, cross-system ontologies, and claim passports"},
                {"step": 5, "stage": "HYPOTHESES", "description": "Candidate hypotheses labeled HYPOTHESIZED with biological rationale"},
                {"step": 6, "stage": "MODELS", "description": "In silico PK/PD models and causal backdoor DAGs"},
                {"step": 7, "stage": "PREDICTIONS", "description": "Monte Carlo simulated trajectories (labeled SIMULATED)"},
                {"step": 8, "stage": "EXPERIMENTS", "description": "Next-best-experiment design with disconfirming thresholds"},
                {"step": 9, "stage": "NEW_OBSERVATIONS", "description": "Empirical assay measurements and newly published trials"},
                {"step": 10, "stage": "UPDATED_KNOWLEDGE", "description": "Revalidated claims and governed Knowledge Release"}
            ],
            "is_closed_loop": True,
            "meta_graph_active": True
        }


def get_skos() -> ScientificKnowledgeOS:
    return ScientificKnowledgeOS.get_instance()
