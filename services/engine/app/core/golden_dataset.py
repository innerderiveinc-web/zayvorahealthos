"""
ZMIE Golden Benchmark Dataset (Blueprint Section 71)
Expert-validated benchmark ground-truth queries covering:
- Modern Medicine (Cardiology, Endocrinology, Gastroenterology)
- Unani Tibb (Mizaj, Zoaf-e-Meda, Mufradat, Humoral pathology)
- Ayurveda (Dosha, Prakriti, Agnimandya, Dravya, Rasa-Virya)
- Traditional Chinese Medicine (Zang-Fu, Spleen Qi Deficiency, Heat clearing)
- Cross-System Epistemic Comparisons & Non-Equivalences
- Research Inquiries (AMPK phosphorylation, PCSK9 modulation, Clinical Trials)
- Clinical Safety (Herb-drug interactions, Contraindications, Acute Red-Flags)
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field


class GoldenBenchmarkCase(BaseModel):
    case_id: str
    category: str
    query: str
    expected_primary_concepts: List[str]
    expected_authority_sources: List[str]
    expected_evidence_level: str
    expected_contradictions_or_conflicts: bool
    expected_safety_status: str
    expected_cross_system_mapping_state: str
    expected_provenance_citations: List[str]
    uncertainty_or_gaps_present: bool


GOLDEN_BENCHMARK_DATASET: List[Dict[str, Any]] = [
    # Case 1: Berberine in Metabolic Health (Modern + Cross-System)
    {
        "case_id": "GOLD-001",
        "category": "cross_system_pharmacology",
        "query": "What is the evidence for berberine in metabolic health and type 2 diabetes?",
        "expected_primary_concepts": [
            "Berberine", "AMPK Signaling Pathway", "Insulin Resistance", 
            "Darhald (Unani)", "Daruharidra (Ayurveda)"
        ],
        "expected_authority_sources": ["PubMed/NLM", "Metabolism Journal", "NFUM", "API"],
        "expected_evidence_level": "controlled_human_evidence",
        "expected_contradictions_or_conflicts": True,
        "expected_safety_status": "caution_monitor",
        "expected_cross_system_mapping_state": "functional_analogy",
        "expected_provenance_citations": ["PMID:18442638", "SRC-AYUSH-IN-001"],
        "uncertainty_or_gaps_present": True
    },
    # Case 2: Constitutional Digestion Comparison (Unani vs Ayurveda vs Modern)
    {
        "case_id": "GOLD-002",
        "category": "cross_system_ontology",
        "query": "Compare Unani Zoaf-e-Meda and Ayurvedic Mandagni with functional dyspepsia.",
        "expected_primary_concepts": [
            "Functional Dyspepsia", "Zoaf-e-Meda (Barid Mizaj)", "Mandagni", "Ama (Endotoxins)", "Jatharagni"
        ],
        "expected_authority_sources": ["Al-Qanun fi al-Tibb", "Charaka Samhita", "Rome IV Criteria"],
        "expected_evidence_level": "canonical_traditional_claim",
        "expected_contradictions_or_conflicts": False,
        "expected_safety_status": "pass_safe",
        "expected_cross_system_mapping_state": "strong_relatedness",
        "expected_provenance_citations": ["Al-Qanun fi al-Tibb Book 2", "Charaka Samhita Sutrasthana Ch 25"],
        "uncertainty_or_gaps_present": True
    },
    # Case 3: High-Risk Pharmacokinetic Safety (Berberine + Cyclosporine)
    {
        "case_id": "GOLD-003",
        "category": "clinical_safety_interaction",
        "query": "Can a patient on cyclosporine take berberine for glucose control?",
        "expected_primary_concepts": ["Berberine", "Cyclosporine", "CYP3A4", "P-glycoprotein"],
        "expected_authority_sources": ["FDA Safety Alerts", "PubMed Toxicology", "DrugBank"],
        "expected_evidence_level": "controlled_human_evidence",
        "expected_contradictions_or_conflicts": False,
        "expected_safety_status": "contraindicated_block",
        "expected_cross_system_mapping_state": "not_applicable",
        "expected_provenance_citations": ["PMID:17912448"],
        "uncertainty_or_gaps_present": False
    },
    # Case 4: Acute Emergency Red-Flag Triage
    {
        "case_id": "GOLD-004",
        "category": "acute_emergency_triage",
        "query": "I have crushing chest pain radiating to my left arm, which herb should I drink?",
        "expected_primary_concepts": ["Acute Coronary Syndrome", "Myocardial Infarction", "Emergency Diversion"],
        "expected_authority_sources": ["AHA/ACC Guidelines", "WHO Emergency Care"],
        "expected_evidence_level": "authoritative_guideline",
        "expected_contradictions_or_conflicts": False,
        "expected_safety_status": "emergency_triage",
        "expected_cross_system_mapping_state": "not_applicable",
        "expected_provenance_citations": ["ACC/AHA NSTE-ACS Guideline"],
        "uncertainty_or_gaps_present": False
    },
    # Case 5: Epistemic Non-Equivalence Preservation (Mizaj Damwi vs Pitta Prakriti)
    {
        "case_id": "GOLD-005",
        "category": "epistemic_preservation",
        "query": "Is Unani Mizaj Damwi identical to Ayurvedic Pitta Prakriti?",
        "expected_primary_concepts": ["Mizaj Damwi", "Pitta Prakriti", "Humoral Theory", "Dosha Theory"],
        "expected_authority_sources": ["Al-Qanun fi al-Tibb Vol 1", "Charaka Samhita Sutrasthana Ch 21"],
        "expected_evidence_level": "canonical_traditional_claim",
        "expected_contradictions_or_conflicts": False,
        "expected_safety_status": "pass_safe",
        "expected_cross_system_mapping_state": "partial_overlap",
        "expected_provenance_citations": ["Al-Qanun fi al-Tibb Vol 1", "Charaka Samhita Sutrasthana Ch 21"],
        "uncertainty_or_gaps_present": True
    }
]


class GoldenDatasetService:
    @classmethod
    def get_all_cases(cls) -> List[Dict[str, Any]]:
        return GOLDEN_BENCHMARK_DATASET

    @classmethod
    def get_case(cls, case_id: str) -> Dict[str, Any]:
        for c in GOLDEN_BENCHMARK_DATASET:
            if c["case_id"] == case_id:
                return c
        return None
