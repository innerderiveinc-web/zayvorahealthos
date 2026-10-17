"""
ZMIE Ontology & Graph API Router
Provides cross-system concept lookups, comparative graphs, and epistemic mapping details.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.db.knowledge_graph_seed import KnowledgeGraphSeedService

router = APIRouter(prefix="/ontology", tags=["Cross-System Ontology & Knowledge Graph"])


@router.get("/concepts")
async def list_concepts(system: Optional[str] = Query(None, description="Filter by system: 'modern_biomedicine', 'unani_tibb', 'ayurveda', 'traditional_chinese_medicine'")):
    """
    Returns canonical concepts across medical traditions.
    """
    all_concepts = KnowledgeGraphSeedService.get_all_concepts()
    if system:
        return [c for c in all_concepts if c.get("system") == system]
    return all_concepts


@router.get("/mappings")
async def list_cross_system_mappings(concept_id: Optional[str] = Query(None, description="Concept ID to find cross-system correspondences")):
    """
    Returns explicit mappings with epistemic rationales and confidence scores.
    """
    all_mappings = KnowledgeGraphSeedService.get_all_mappings()
    if concept_id:
        return [m for m in all_mappings if m.get("source_concept_id") == concept_id or m.get("target_concept_id") == concept_id]
    return all_mappings


@router.get("/compare")
async def compare_systems(topic: str = Query(..., description="E.g. 'digestion', 'constitution', 'berberine'")):
    """
    Signature ZMIE feature: Returns a multi-system side-by-side epistemological comparison.
    """
    topic_clean = topic.lower()
    
    if "digest" in topic_clean or "stomach" in topic_clean or "gastric" in topic_clean:
        return {
            "topic": "Digestion & Metabolic Transformation",
            "modern": {
                "concept": "Gastric Motility & Enzymatic Breakdown",
                "organ_axis": "Gastrointestinal tract, Vagus nerve, Enteric nervous system",
                "pathology": "Functional Dyspepsia, Delayed Gastric Emptying"
            },
            "unani": {
                "concept": "Hazm (Digestion) & Quwwat-e-Hazima",
                "organ_axis": "Meda (Stomach) & Jigar (Liver)",
                "pathology": "Zoaf-e-Meda (Barid Mizaj / Loss of digestive heat)"
            },
            "ayurveda": {
                "concept": "Jatharagni (Digestive Fire)",
                "organ_axis": "Amashaya (Stomach) & Grahani (Duodenum)",
                "pathology": "Mandagni & formation of Ama (toxic undigested residue)"
            },
            "tcm": {
                "concept": "Pi/Wei (Spleen/Stomach Rotting & Ripening)",
                "organ_axis": "Middle Jiao / Spleen-Stomach network",
                "pathology": "Spleen Qi Deficiency with Dampness accumulation"
            },
            "cross_system_synthesis": "All four traditions converge on the fundamental requirement of metabolic heat/vital tone for nutrient assimilation; loss of this heat produces systemic biological debris (Ama in Ayurveda, Khilt-e-Ghaleez in Unani, Dampness in TCM, Endotoxin/LPS in Modern)."
        }

    return {
        "topic": topic,
        "modern": {"concept": "Standard biomedical cellular model"},
        "unani": {"concept": "Humoral/Mizaj framework"},
        "ayurveda": {"concept": "Tridosha/Dhatus framework"},
        "tcm": {"concept": "Zang-Fu/Meridian framework"},
        "cross_system_synthesis": "Parallel medical frameworks with distinct foundational axioms."
    }
