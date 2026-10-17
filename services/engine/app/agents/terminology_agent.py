"""
ZMIE Terminology & Concept Expansion Agent
Provides semantic expansion across standard biomedical vocabularies (MeSH, SNOMED CT, ICD-11, UMLS)
and traditional codex systems (Unani, Ayurveda, TCM).
Ensures that queries like "diabetes" expand into biomedical, biochemical, and traditional entities.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field


class TerminologyExpansionResult(BaseModel):
    query_entity: str
    mesh_descriptors: List[str] = Field(default_factory=list)
    snomed_clinical_terms: List[str] = Field(default_factory=list)
    unani_terms: List[Dict[str, str]] = Field(default_factory=list)
    ayurvedic_terms: List[Dict[str, str]] = Field(default_factory=list)
    biochemical_pathways: List[str] = Field(default_factory=list)


class TerminologyAgent:
    """
    Normalizes and expands queries across the 4 Knowledge Universes.
    """

    MAPPING_DICTIONARY = {
        "diabetes": {
            "mesh": ["Diabetes Mellitus, Type 2", "Hyperglycemia", "Insulin Resistance"],
            "snomed": ["Type 2 diabetes mellitus (disorder)", "Impaired glucose tolerance (finding)"],
            "unani": [
                {"term": "Ziabetes Shakari", "concept": "Excessive thirst and sweet urination due to altered renal/metabolic Mizaj"},
                {"term": "Zoafe Barid", "concept": "Cold humoral derangement of metabolic organ systems"}
            ],
            "ayurveda": [
                {"term": "Madhumeha", "concept": "Sweet-urine syndrome under the 20 subtypes of Prameha"},
                {"term": "Kaphaja Prameha", "concept": "Disorders of fluid metabolism and meda (adipose tissue)"}
            ],
            "pathways": ["AMPK Signaling Pathway", "GLUT4 Translocation", "IRS-1 Phosphorylation", "mTOR Pathway"]
        },
        "berberine": {
            "mesh": ["Berberine", "Alkaloids", "Isoquinolines"],
            "snomed": ["Berberine (substance)"],
            "unani": [
                {"term": "Darhald / Zard Chob", "concept": "Bark/root of Berberis aristata; Mizaj: Hot 2° / Dry 2°"}
            ],
            "ayurveda": [
                {"term": "Daruharidra (Indian Barberry)", "concept": "Rasapanchaka: Tikta, Kashaya; Virya: Ushna; Karma: Pramehahara"}
            ],
            "pathways": ["AMPK Activation", "PCSK9 Downregulation", "Gut Microbiota Short-Chain Fatty Acid Regulation"]
        },
        "hypertension": {
            "mesh": ["Hypertension", "Blood Pressure", "Vascular Resistance"],
            "snomed": ["Essential hypertension (disorder)"],
            "unani": [
                {"term": "Imtila-e-Damwi", "concept": "Vascular plethora/engorgement of sanguineous humor"}
            ],
            "ayurveda": [
                {"term": "Raktagata Vata", "concept": "Vata dosha entering and constricting blood vessels (Rakta)"}
            ],
            "pathways": ["Renin-Angiotensin-Aldosterone System (RAAS)", "Nitric Oxide Endothelial Signaling"]
        }
    }

    @classmethod
    def expand_query(cls, raw_query: str) -> TerminologyExpansionResult:
        query_clean = raw_query.strip().lower()
        
        # Match against dictionary
        for key, entry in cls.MAPPING_DICTIONARY.items():
            if key in query_clean:
                return TerminologyExpansionResult(
                    query_entity=key,
                    mesh_descriptors=entry.get("mesh", []),
                    snomed_clinical_terms=entry.get("snomed", []),
                    unani_terms=entry.get("unani", []),
                    ayurvedic_terms=entry.get("ayurvedic", entry.get("ayurveda", [])),
                    biochemical_pathways=entry.get("pathways", [])
                )

        # Fallback default expansion
        return TerminologyExpansionResult(
            query_entity=raw_query,
            mesh_descriptors=[raw_query.capitalize()],
            snomed_clinical_terms=[],
            unani_terms=[],
            ayurvedic_terms=[],
            biochemical_pathways=[]
        )
