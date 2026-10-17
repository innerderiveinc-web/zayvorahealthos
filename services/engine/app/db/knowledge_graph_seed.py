"""
ZMIE Knowledge Graph Expansion Seed Data
Populates the Cross-System Medical Ontology across:
1. Modern Biomedical Pathologies, Pathways & Biochemical Targets
2. Unani Tibb (Mizaj, Amraz, Afaal, Mufradat, Murakkabat)
3. Ayurveda (Dosha, Prakriti, Dhatus, Agni, Dravya, Chikitsa)
4. Traditional Chinese Medicine (Zang-Fu, Qi, Meridians, Classical Formulas)
Maintains explicit epistemological mapping states (Functional Analogy, Strong Relatedness, Partial Overlap).
"""

from typing import List, Dict, Any
from app.models.ontology import CrossSystemMappingState


CANONICAL_CONCEPTS_SEED: List[Dict[str, Any]] = [
    # --- MODERN BIOMEDICINE ---
    {
        "concept_id": "CON-MOD-METABOLIC-HOMEOSTASIS",
        "system": "modern_biomedicine",
        "canonical_name": "Metabolic Homeostasis & Energy Sensor",
        "category": "physiology",
        "definition": "Cellular and systemic balance of catabolic and anabolic pathways primarily regulated by AMPK, mTOR, and insulin signaling."
    },
    {
        "concept_id": "CON-MOD-GASTRIC-DYSFUNCTION",
        "system": "modern_biomedicine",
        "canonical_name": "Functional Dyspepsia & Impaired Gastric Emptying",
        "category": "pathology",
        "definition": "Disordered gastric motility and mucosal hypersensitivity without structural ulceration."
    },
    {
        "concept_id": "CON-MOD-INFLAMMATORY-CASCADE",
        "system": "modern_biomedicine",
        "canonical_name": "Systemic Low-Grade Chronic Inflammation",
        "category": "pathology",
        "definition": "Persistent release of pro-inflammatory cytokines (TNF-alpha, IL-6, CRP) driving vascular and metabolic damage."
    },

    # --- UNANI TIBB ---
    {
        "concept_id": "CON-UNANI-MIZAJ-DAMWI",
        "system": "unani_tibb",
        "canonical_name": "Mizaj Damwi (Sanguinous Temperament: Hot & Moist)",
        "original_script_name": "مزاج دموی",
        "transliteration": "Mizaj Damwi",
        "category": "constitutional",
        "definition": "Dominance of Dam (Blood humor); individuals possess high vascularity, warmth, robust physique, and elevated metabolic rate."
    },
    {
        "concept_id": "CON-UNANI-ZOAFF-MEDA",
        "system": "unani_tibb",
        "canonical_name": "Zoaf-e-Meda (Gastric Asthenia / Weakness of Stomach)",
        "original_script_name": "ضعف معدہ",
        "transliteration": "Zo'af-e-Meda",
        "category": "pathology",
        "definition": "Impairment of Quwwat-e-Hazima (digestive faculty) due to cold humoral derangement (Barid Mizaj) or excessive moisture."
    },
    {
        "concept_id": "CON-UNANI-DARHALD",
        "system": "unani_tibb",
        "canonical_name": "Darhald / Rasaut (Berberis aristata)",
        "original_script_name": "دارہلد / رسوت",
        "transliteration": "Darhald",
        "category": "pharmacology_mufrad",
        "definition": "Mufrad (Single Drug). Mizaj: Hot 2° / Dry 2°. Indicated for Daf-e-Taffun (Antiseptic/Anti-rot) and Musaffi-e-Dam (Blood Purifier)."
    },

    # --- AYURVEDA ---
    {
        "concept_id": "CON-AYUR-PITTA-PRAKRITI",
        "system": "ayurveda",
        "canonical_name": "Pitta Prakriti",
        "original_script_name": "पित्त प्रकृति",
        "transliteration": "Pitta Prakriti",
        "category": "constitutional",
        "definition": "Constitutional predominance of Pitta dosha governed by Tejas (Fire) and Jala (Water); keen appetite, sharp intellect, metabolic heat."
    },
    {
        "concept_id": "CON-AYUR-MANDAGNI",
        "system": "ayurveda",
        "canonical_name": "Mandagni (Hypoactive Digestive Fire)",
        "original_script_name": "मन्दाग्नि",
        "transliteration": "Mandagni",
        "category": "pathology",
        "definition": "Depression of Jatharagni leading to incomplete food transformation, accumulation of Ama (endotoxins), and sluggish digestion."
    },
    {
        "concept_id": "CON-AYUR-DARUHARIDRA",
        "system": "ayurveda",
        "canonical_name": "Daruharidra (Indian Barberry)",
        "original_script_name": "दारुहरिद्रा",
        "transliteration": "Daruharidra",
        "category": "pharmacology_dravya",
        "definition": "Dravya with Tikta/Kashaya Rasa, Ushna Virya, Katu Vipaka. Classical actions: Pramehahara (Anti-diabetic) and Lekhana (Scraping tissue)."
    },

    # --- TRADITIONAL CHINESE MEDICINE (TCM) ---
    {
        "concept_id": "CON-TCM-PI-QI-XU",
        "system": "traditional_chinese_medicine",
        "canonical_name": "Spleen Qi Deficiency (Pi Qi Xu)",
        "original_script_name": "脾气虚",
        "transliteration": "Pi Qi Xu",
        "category": "pathology",
        "definition": "Failure of the Spleen organ system to govern transport and transformation of nutrients, manifesting as fatigue and postprandial bloating."
    },
    {
        "concept_id": "CON-TCM-HUANG-LIAN",
        "system": "traditional_chinese_medicine",
        "canonical_name": "Huang Lian (Coptis chinensis - Berberine rich)",
        "original_script_name": "黄连",
        "transliteration": "Huang Lian",
        "category": "pharmacology_herb",
        "definition": "Cold nature, bitter flavor. Clears heat, dries dampness, and drains fire especially in Stomach and Heart channels."
    }
]


CROSS_SYSTEM_MAPPINGS_SEED: List[Dict[str, Any]] = [
    # 1. Mizaj Damwi <-> Pitta Prakriti
    {
        "relation_id": "REL-CS-001",
        "source_concept_id": "CON-UNANI-MIZAJ-DAMWI",
        "target_concept_id": "CON-AYUR-PITTA-PRAKRITI",
        "mapping_state": CrossSystemMappingState.PARTIAL_OVERLAP.value,
        "confidence": 0.76,
        "epistemic_rationale": "Both describe hyper-metabolic, warm, and highly vascular constitutions, but Pitta is centered on transformation/enzymes whereas Damwi centers on circulatory humor.",
        "classical_evidence": "Al-Qanun fi al-Tibb, Vol 1 / Charaka Samhita, Sutrasthana Ch 21"
    },
    # 2. Zoaf-e-Meda <-> Mandagni <-> Gastric Dysfunction
    {
        "relation_id": "REL-CS-002",
        "source_concept_id": "CON-UNANI-ZOAFF-MEDA",
        "target_concept_id": "CON-AYUR-MANDAGNI",
        "mapping_state": CrossSystemMappingState.STRONG_RELATEDNESS.value,
        "confidence": 0.88,
        "epistemic_rationale": "Direct operational concordance: both identify a deficit in innate digestive heat/tone causing accumulation of raw, toxic metabolic residues.",
        "classical_evidence": "Kamilus Sana'a, Maqala 2 / Sushruta Samhita, Uttaratantra"
    },
    {
        "relation_id": "REL-CS-003",
        "source_concept_id": "CON-UNANI-ZOAFF-MEDA",
        "target_concept_id": "CON-TCM-PI-QI-XU",
        "mapping_state": CrossSystemMappingState.FUNCTIONAL_ANALOGY.value,
        "confidence": 0.82,
        "epistemic_rationale": "Functional analogy: Spleen Qi deficiency matches the cold asthenic failure of Quwwat-e-Hazima in Unani.",
        "classical_evidence": "Shanghan Lun / Ibn Sina"
    },
    # 3. Botanical / Phytochemical Concordance: Darhald <-> Daruharidra <-> Huang Lian
    {
        "relation_id": "REL-CS-004",
        "source_concept_id": "CON-UNANI-DARHALD",
        "target_concept_id": "CON-AYUR-DARUHARIDRA",
        "mapping_state": CrossSystemMappingState.EXACT_EQUIVALENCE.value,
        "confidence": 1.0,
        "epistemic_rationale": "Botanical and taxonomic identity: Both refer directly to the root, wood, and standardized extracts of Berberis aristata DC.",
        "classical_evidence": "Ayurvedic Pharmacopoeia of India (API) Part I / National Formulary of Unani Medicine (NFUM) Part I"
    },
    {
        "relation_id": "REL-CS-005",
        "source_concept_id": "CON-UNANI-DARHALD",
        "target_concept_id": "CON-TCM-HUANG-LIAN",
        "mapping_state": CrossSystemMappingState.FUNCTIONAL_ANALOGY.value,
        "confidence": 0.89,
        "epistemic_rationale": "Phytochemical & Functional Analogy: Both serve as classical sources of isoquinoline alkaloids (berberine) used for clearing infectious/inflammatory heat.",
        "classical_evidence": "Chinese Pharmacopoeia / Unani Makhzan al-Mufradat"
    }
]


class KnowledgeGraphSeedService:
    @classmethod
    def get_all_concepts(cls) -> List[Dict[str, Any]]:
        return CANONICAL_CONCEPTS_SEED

    @classmethod
    def get_all_mappings(cls) -> List[Dict[str, Any]]:
        return CROSS_SYSTEM_MAPPINGS_SEED
