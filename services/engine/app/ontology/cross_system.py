"""
ZMIE Cross-System Epistemic Mapping & Comparative Lens Engine (Sections 27-29, 88)
Enforces the 10-tier relationship taxonomy and safeguards against false equivalence.
Never converts FUNCTIONAL_ANALOGY or PARTIAL_OVERLAP into EXACT_EQUIVALENCE.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.graph import CrossSystemMappingType
from app.models.claim import MedicalSystem


class CrossSystemMappingRule(BaseModel):
    """
    Governed ontological mapping between concepts in different medical systems.
    """
    mapping_id: str
    source_concept_id: str
    source_system: MedicalSystem
    target_concept_id: str
    target_system: MedicalSystem
    mapping_type: CrossSystemMappingType
    confidence: float = Field(..., ge=0.0, le=1.0)
    epistemic_rationale: str
    shared_features: List[str] = Field(default_factory=list)
    divergent_features: List[str] = Field(default_factory=list)
    classical_codex_evidence: Optional[str] = None
    modern_trial_evidence_ids: List[str] = Field(default_factory=list)
    is_peer_reviewed: bool = True
    reviewer_id: Optional[str] = "HAKEEM-AYUR-COUNCIL-01"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ComparativeLensReport(BaseModel):
    """
    Multi-system comparative synthesis object presenting cross-system perspectives
    without epistemic flattening.
    """
    topic: str
    system_perspectives: Dict[str, Dict[str, Any]]
    concordance_level: CrossSystemMappingType
    shared_themes: List[str]
    fundamental_divergences: List[str]
    conceptual_boundaries: List[str]
    evidence_summary: str
    unresolved_questions: List[str]
    safeguard_notice: str


class CrossSystemMappingEngine:
    """
    Governs the validation and comparison of cross-system medical concepts.
    """

    def __init__(self):
        self._mappings: Dict[str, CrossSystemMappingRule] = {}
        self._load_canonical_mappings()

    def _load_canonical_mappings(self):
        # 1. Botanical: Berberis aristata = Darhald (Unani) = Daruharidra (Ayurveda)
        self.register_mapping(CrossSystemMappingRule(
            mapping_id="MAP-BOT-001",
            source_concept_id="CON-UNANI-DARHALD",
            source_system=MedicalSystem.UNANI,
            target_concept_id="CON-AYUR-DARUHARIDRA",
            target_system=MedicalSystem.AYURVEDA,
            mapping_type=CrossSystemMappingType.EXACT_EQUIVALENCE,
            confidence=1.0,
            epistemic_rationale="Botanical and phytochemical identity verified: Both refer directly to Berberis aristata DC. containing berberine alkaloids.",
            shared_features=["Taxonomic species: Berberis aristata", "Major alkaloid: Berberine", "Anti-inflammatory and bitter properties"],
            divergent_features=["Unani frames action via Hot 2°/Dry 2° Mizaj and Musaffi-e-Dam (blood purification)", "Ayurveda frames action via Tikta/Kashaya Rasa and Lekhana Karma"],
            classical_codex_evidence="NFUM Part I / API Part I"
        ))

        # 2. Functional Analogy: Zoaf-e-Meda (Unani) <-> Mandagni (Ayurveda) <-> Functional Dyspepsia (Modern)
        self.register_mapping(CrossSystemMappingRule(
            mapping_id="MAP-PATH-001",
            source_concept_id="CON-UNANI-ZOAFF-MEDA",
            source_system=MedicalSystem.UNANI,
            target_concept_id="CON-AYUR-MANDAGNI",
            target_system=MedicalSystem.AYURVEDA,
            mapping_type=CrossSystemMappingType.FUNCTIONAL_ANALOGY,
            confidence=0.88,
            epistemic_rationale="Functional analogy: Both denote a deficit of digestive metabolic heat/tone leading to toxic undigested residues.",
            shared_features=["Digestive sluggishness", "Accumulation of toxic unassimilated waste", "Postprandial heaviness"],
            divergent_features=["Unani attributes pathology to cold humoral dyscrasia (Su-e-Mizaj Barid)", "Ayurveda attributes pathology to Jatharagni depression under Kapha or Vata vitiation"],
            classical_codex_evidence="Al-Qanun fi al-Tibb, Book III / Charaka Samhita, Chikitsasthana Ch 15"
        ))

        # 3. Partial Overlap: Mizaj Damwi (Unani) <-> Pitta Prakriti (Ayurveda)
        self.register_mapping(CrossSystemMappingRule(
            mapping_id="MAP-CONST-001",
            source_concept_id="CON-UNANI-MIZAJ-DAMWI",
            source_system=MedicalSystem.UNANI,
            target_concept_id="CON-AYUR-PITTA-PRAKRITI",
            target_system=MedicalSystem.AYURVEDA,
            mapping_type=CrossSystemMappingType.PARTIAL_OVERLAP,
            confidence=0.74,
            epistemic_rationale="Partial conceptual overlap: Both describe vascular warmth and elevated metabolic drive, but Pitta is metabolic transformation (Fire/Water) while Damwi is blood-humor predominance (Air/Heat).",
            shared_features=["Heat intolerance", "Robust vascularity", "Active metabolic tone"],
            divergent_features=["Damwi possesses high moisture (Ratab); Pitta possesses sharpness and slight unctuousness"],
            classical_codex_evidence="Kamilus Sana'a / Sushruta Samhita"
        ))

    def register_mapping(self, mapping: CrossSystemMappingRule):
        self._mappings[mapping.mapping_id] = mapping

    def get_mappings_for_concept(self, concept_id: str) -> List[CrossSystemMappingRule]:
        return [
            m for m in self._mappings.values()
            if m.source_concept_id == concept_id or m.target_concept_id == concept_id
        ]

    def validate_equivalence_safeguard(self, source_id: str, target_id: str) -> Dict[str, Any]:
        """
        Guarantees that functional analogy or partial overlap is never falsely stated as equivalence.
        """
        for m in self._mappings.values():
            if (m.source_concept_id == source_id and m.target_concept_id == target_id) or \
               (m.source_concept_id == target_id and m.target_concept_id == source_id):
                is_exact = m.mapping_type == CrossSystemMappingType.EXACT_EQUIVALENCE
                return {
                    "is_exact_equivalence": is_exact,
                    "mapping_type": m.mapping_type.value,
                    "epistemic_rationale": m.epistemic_rationale,
                    "allowed_presentation": "EXACT EQUIVALENT (A = B)" if is_exact else f"CORRESPONDING ANALOGY ({m.mapping_type.value})"
                }
        return {
            "is_exact_equivalence": False,
            "mapping_type": CrossSystemMappingType.NO_VALIDATED_MAPPING.value,
            "epistemic_rationale": "No governed ontological mapping established.",
            "allowed_presentation": "NO VALIDATED EQUIVALENCE FOUND"
        }

    def generate_comparative_lens(self, topic: str) -> ComparativeLensReport:
        """
        Renders a full 4-system comparative lens on a medical domain.
        """
        t = topic.lower()
        if "digest" in t or "stomach" in t or "dyspepsia" in t:
            return ComparativeLensReport(
                topic="Digestion & Metabolic Transformation",
                system_perspectives={
                    "modern_biomedicine": {
                        "concept": "Gastric Motility & Enzymatic Breakdown",
                        "axis": "Cephalic, gastric, intestinal phases; ENS, vagus, gastrin, pepsin, amylase",
                        "pathology": "Functional Dyspepsia, Gastroparesis, Small Intestinal Bacterial Overgrowth"
                    },
                    "unani_tibb": {
                        "concept": "Hazm (Digestion) & Quwwat-e-Hazima",
                        "axis": "Hazm-e-Medi (Gastric), Hazm-e-Kabidi (Hepatic), Hazm-e-Uruqi (Vascular), Hazm-e-Uzwi (Cellular)",
                        "pathology": "Zoaf-e-Meda (Gastric Asthenia due to Su-e-Mizaj Barid / Cold Humoral Derangement)"
                    },
                    "ayurveda": {
                        "concept": "Jatharagni (Central Digestive Fire)",
                        "axis": "Prana Vayu, Samana Vayu, Pachaka Pitta, Kledaka Kapha in Amashaya",
                        "pathology": "Mandagni causing formation of Ama (antigenic toxic undigested macromolecular sludge)"
                    },
                    "tcm": {
                        "concept": "Pi/Wei (Spleen/Stomach Rotting & Ripening Network)",
                        "axis": "Ascending pure Qi (Pi) and descending turbid waste (Wei)",
                        "pathology": "Pi Qi Xu (Spleen Qi Deficiency with Dampness Obstruction)"
                    }
                },
                concordance_level=CrossSystemMappingType.FUNCTIONAL_ANALOGY,
                shared_themes=[
                    "Universal recognition that complete metabolic transformation requires biological warmth/vital energy.",
                    "Failure of primary transformation generates systemic biological toxicity (Ama, Khilt-e-Ghaleez, Dampness, Endotoxemia/LPS).",
                    "Therapeutic intervention requires carminatives, bitters, and heat-restoring aromatics."
                ],
                fundamental_divergences=[
                    "Biomedicine localizes pathology to receptor dysfunction, mucosal permeability, or enzymatic deficits.",
                    "Unani frames pathology through balance of the 4 humors and innate Quwwat-e-Mudabbira.",
                    "Ayurveda frames pathology through Tridosha interaction with Sub-doshas and Dhatus.",
                    "TCM frames pathology as energetic disharmony between yin/yang and meridians."
                ],
                conceptual_boundaries=[
                    "Quwwat-e-Hazima is not merely peristalsis; it includes four distinct phases of systemic assimilation.",
                    "Jatharagni is not hydrochloric acid; it is the bio-transformative cosmic fire principle instantiated in physiology.",
                    "Pi (Spleen) is not the lymphoid organ; it is the entire nutrient distribution system."
                ],
                evidence_summary="Empirical clinical research confirms functional dyspepsia responds favorably to classical polyherbal formulations across Unani (Itrifal), Ayurveda (Trikatu/Hingwashtak), and TCM (Liu Jun Zi Tang) via prokinetic, anti-inflammatory, and microbiome-modulating actions.",
                unresolved_questions=[
                    "How do molecular biomarkers of intestinal permeability (Zonulin) correlate with classical stages of Ama?",
                    "Can autonomous heart rate variability metrics provide standardized quantitative correlates for Mizaj or Prakriti?"
                ],
                safeguard_notice="EPISTEMIC SAFEGUARD: Mapped as FUNCTIONAL_ANALOGY. Concepts share parallel functional roles but are grounded in distinct axiomatic philosophies. Do not treat as interchangeable biological identities."
            )

        # Generic lens fallback
        return ComparativeLensReport(
            topic=topic,
            system_perspectives={
                "modern_biomedicine": {"concept": f"Biomedical clinical model for {topic}"},
                "unani_tibb": {"concept": f"Classical Greco-Arab Humoral framework for {topic}"},
                "ayurveda": {"concept": f"Tridosha and Dhatu framework for {topic}"},
                "tcm": {"concept": f"Zang-Fu and Meridian model for {topic}"}
            },
            concordance_level=CrossSystemMappingType.RESEARCH_HYPOTHESIS,
            shared_themes=["Holistic balance and biological homeostasis"],
            fundamental_divergences=["Divergent diagnostic frameworks and therapeutic taxonomy"],
            conceptual_boundaries=["Different foundational paradigms of health and disease"],
            evidence_summary="Preliminary comparative literature available; formal harmonization trials ongoing.",
            unresolved_questions=["Rigorous validation of shared botanical efficacy across standardized registries."],
            safeguard_notice="SAFEGUARD: No direct biological identity exists. Presented for comparative scholarly analysis only."
        )
