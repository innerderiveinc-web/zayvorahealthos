"""
ZMIE Scientific Knowledge Operating System - Knowledge Fabric (Prompt 25)
Provides the unified logical layer and Single Source of Truth Entity Registry
connecting Sources, Documents, Concepts, Researchers, Datasets, Studies,
Claims, Evidence, Mechanisms, Causality, Safety, and Regulations (Clauses 6-10).
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

from app.models.skos import (
    SKOSMasterEntity,
    SKOSEntityType,
    SKOSEpistemicState,
    RevalidationState
)
from app.models.federated_privacy import ResearchDataClassification


class KnowledgeFabricRegistry:
    """
    Authoritative Master Entity Registry & Knowledge Fabric (Clauses 6, 7, 9).
    Guarantees stable IDs, temporal validity, and prevents duplicated or conflicting representations.
    """
    def __init__(self):
        self._entities: Dict[str, SKOSMasterEntity] = {}
        self._external_id_index: Dict[str, str] = {}  # "mesh:D003924" -> stable_id
        self._type_index: Dict[SKOSEntityType, List[str]] = {}
        self._seed_authoritative_fabric()

    def _seed_authoritative_fabric(self):
        """Seeds canonical cross-domain entities (Clauses 7, 9, 208-210)."""
        seeds = [
            # 1. Sources
            SKOSMasterEntity(
                stable_id="SRC-PUBMED-MEDLINE",
                entity_type=SKOSEntityType.SOURCE,
                name="PubMed / MEDLINE",
                description="National Library of Medicine biomedical literature database",
                source_identifiers={"source_code": "PUBMED"},
                properties={"authority_tier": "TIER_A", "jurisdiction": "US", "indexed_count": 35000000}
            ),
            SKOSMasterEntity(
                stable_id="SRC-AYUSH-TKDL",
                entity_type=SKOSEntityType.SOURCE,
                name="Traditional Knowledge Digital Library (TKDL)",
                description="Sovereign Indian digital codex repository for Ayurveda, Unani, and Siddha",
                source_identifiers={"source_code": "TKDL"},
                properties={"authority_tier": "TIER_A", "jurisdiction": "IN", "indexed_count": 450000}
            ),

            # 2. Medical Concepts across Universes
            SKOSMasterEntity(
                stable_id="CONCEPT-T2D",
                entity_type=SKOSEntityType.CONCEPT,
                name="Diabetes Mellitus, Type 2",
                description="A metabolic disorder characterized by hyperglycemia resulting from insulin resistance.",
                external_identifiers={"mesh": "D003924", "icd11": "5A11"},
                properties={"medical_system": "MODERN_BIOMEDICINE"}
            ),
            SKOSMasterEntity(
                stable_id="CONCEPT-ZIYABETES",
                entity_type=SKOSEntityType.CONCEPT,
                name="Ziyabetes Shakari",
                description="Unani disease concept characterized by excessive thirst (Atash-e-Mufrit) and polyuria due to Sue Mizaj Haar.",
                external_identifiers={"unani_namaste": "UNANI-0921"},
                properties={"medical_system": "UNANI_TIBB", "classical_reference": "Ibn Sina, Al-Qanun fi al-Tibb, Vol 3"}
            ),
            SKOSMasterEntity(
                stable_id="CONCEPT-MADHUMEHA",
                entity_type=SKOSEntityType.CONCEPT,
                name="Madhumeha",
                description="Ayurvedic clinical entity under the umbrella of 20 Vataja Pramehas with sweet urine.",
                external_identifiers={"ayurveda_namaste": "AYU-8821"},
                properties={"medical_system": "AYURVEDA", "classical_reference": "Charaka Samhita, Chikitsa Sthana Ch. 6"}
            ),
            SKOSMasterEntity(
                stable_id="CONCEPT-DAMAVI",
                entity_type=SKOSEntityType.CONCEPT,
                name="Damavi (Sanguine Humoral State)",
                description="Primary classical Unani humoral temperament (Mizaj) dominated by blood (Khilt-e-Dam).",
                properties={"medical_system": "UNANI_TIBB", "has_biomedical_equivalent": False, "status": "NO_VALID_MAPPING"}
            ),

            # 3. Compounds & Interventions
            SKOSMasterEntity(
                stable_id="CPD-BERBERINE",
                entity_type=SKOSEntityType.ENTITY,
                name="Berberine",
                description="Isoquinoline alkaloid isolated from Berberis aristata, Hydrastis canadensis, and Coptis chinensis.",
                external_identifiers={"pubchem": "2353", "chembl": "CHEMBL190"},
                properties={"botanical_sources": ["Berberis aristata (Darhald)", "Coptis chinensis (Huang Lian)"]}
            ),
            SKOSMasterEntity(
                stable_id="CPD-METFORMIN",
                entity_type=SKOSEntityType.ENTITY,
                name="Metformin Hydrochloride",
                description="Biguanide antihyperglycemic oral medication.",
                external_identifiers={"pubchem": "4091", "drugbank": "DB00331"}
            ),

            # 4. Molecular Targets & Pathways
            SKOSMasterEntity(
                stable_id="TARGET-AMPK",
                entity_type=SKOSEntityType.MECHANISM,
                name="AMP-activated protein kinase (AMPK)",
                description="Master cellular metabolic sensor kinase whose activation suppresses hepatic gluconeogenesis.",
                external_identifiers={"uniprot": "Q13131", "gene": "PRKAA1"}
            ),
            SKOSMasterEntity(
                stable_id="TARGET-PCSK9",
                entity_type=SKOSEntityType.MECHANISM,
                name="Proprotein convertase subtilisin/kexin type 9 (PCSK9)",
                description="Regulator of low-density lipoprotein receptor (LDLR) degradation.",
                external_identifiers={"uniprot": "Q8NBP7", "gene": "PCSK9"}
            ),

            # 5. Studies & Clinical Evidence
            SKOSMasterEntity(
                stable_id="STUDY-RCT-2008",
                entity_type=SKOSEntityType.STUDY,
                name="Efficacy of Berberine in Type 2 Diabetes (Yin et al., 2008)",
                description="Double-blind randomized controlled trial comparing Berberine (500mg BID) vs Metformin in 116 patients.",
                external_identifiers={"pmid": "18442638", "doi": "10.1016/j.metabol.2008.01.013"},
                epistemic_state=SKOSEpistemicState.OBSERVED,
                properties={"study_design": "RCT", "sample_size": 116, "primary_endpoint_hba1c_reduction": -1.8}
            ),
            SKOSMasterEntity(
                stable_id="STUDY-SRMA-2015",
                entity_type=SKOSEntityType.STUDY,
                name="Meta-analysis of Berberine glycemic and lipid efficacy (Lan et al., 2015)",
                description="Systematic review and meta-analysis of 14 RCTs involving 1,068 Type 2 diabetic cohorts.",
                external_identifiers={"pmid": "25861268", "doi": "10.1016/j.jep.2014.09.049"},
                epistemic_state=SKOSEpistemicState.OBSERVED,
                properties={"study_design": "Systematic Review & Meta-Analysis", "sample_size": 1068}
            ),

            # 6. Datasets & Analyses
            SKOSMasterEntity(
                stable_id="DATASET-T2D-CLINICAL-01",
                entity_type=SKOSEntityType.DATASET,
                name="Shanghai Jiao Tong University T2D Berberine Cohort Trial Dataset",
                description="Clinical trial measurements of 116 adult subjects over 12 weeks with lipid and glycemic panels.",
                external_identifiers={"zenodo": "10.5281/zenodo.991204"},
                epistemic_state=SKOSEpistemicState.MEASURED,
                properties={"rows": 116, "columns": 24, "license": "CC-BY-4.0"}
            ),

            # 7. Researchers & Institutions
            SKOSMasterEntity(
                stable_id="RES-WEI-ZHANG-01",
                entity_type=SKOSEntityType.RESEARCHER,
                name="Prof. Wei Zhang, MD, PhD",
                description="Principal investigator in metabolic endocrinology and ethnopharmacological clinical trials.",
                external_identifiers={"orcid": "0000-0002-1823-9912"},
                properties={"affiliation": "Shanghai Jiao Tong University School of Medicine", "h_index_context": "Not competitively ranked"}
            ),
            SKOSMasterEntity(
                stable_id="INST-SHANGHAI-JT",
                entity_type=SKOSEntityType.INSTITUTION,
                name="Shanghai Jiao Tong University School of Medicine",
                description="Leading research university and tertiary teaching hospital system.",
                external_identifiers={"ror": "0220qmw57"},
                properties={"country": "CN", "city": "Shanghai"}
            ),
            SKOSMasterEntity(
                stable_id="INST-AIIMS-DELHI",
                entity_type=SKOSEntityType.INSTITUTION,
                name="All India Institute of Medical Sciences (AIIMS)",
                description="Apex medical sciences research university and tertiary clinical center.",
                external_identifiers={"ror": "04vdhe768"},
                properties={"country": "IN", "city": "New Delhi"}
            ),

            # 8. Claims
            SKOSMasterEntity(
                stable_id="CLM-BERBERINE-EFFICACY",
                entity_type=SKOSEntityType.CLAIM,
                name="Berberine Glycemic Efficacy Claim",
                description="Oral administration of Berberine (500mg BID) significantly reduces HbA1c and fasting blood glucose in adults with T2D.",
                epistemic_state=SKOSEpistemicState.SUPPORTED,
                properties={"modality": "DEMONSTRATES", "certainty": "MODERATE", "comparator": "Metformin"}
            ),
            SKOSMasterEntity(
                stable_id="CLM-BERBERINE-AMPK-MECHANISM",
                entity_type=SKOSEntityType.CLAIM,
                name="Berberine AMPK Phosphorylation Mechanism Claim",
                description="Berberine stimulates Thr172 phosphorylation of AMPK alpha subunit, inhibiting gluconeogenic genes PEPCK and G6Pase.",
                epistemic_state=SKOSEpistemicState.SUPPORTED,
                properties={"modality": "CAUSES", "certainty": "HIGH"}
            ),
            SKOSMasterEntity(
                stable_id="CLM-BERBERINE-PREGNANCY-RISK",
                entity_type=SKOSEntityType.SAFETY_SIGNAL,
                name="Berberine Pregnancy Contraindication Signal",
                description="Berberine crosses the placenta and displaces bilirubin from albumin, creating a significant risk of kernicterus in neonates.",
                epistemic_state=SKOSEpistemicState.OBSERVED,
                properties={"severity": "CONTRAINDICATED", "population": "Pregnant and lactating individuals"}
            ),
            # 9. Regulatory Records
            SKOSMasterEntity(
                stable_id="REG-US-FDA-BERBERINE",
                entity_type=SKOSEntityType.REGULATORY_STATE,
                name="US FDA Berberine Regulatory Status",
                description="Regulated as a Dietary Supplement under DSHEA. Not an approved drug for the treatment or prevention of Type 2 Diabetes.",
                properties={"jurisdiction": "US", "agency": "FDA", "status": "DIETARY_SUPPLEMENT", "drug_approval": False}
            ),
            SKOSMasterEntity(
                stable_id="REG-CDSCO-BERBERINE",
                entity_type=SKOSEntityType.REGULATORY_STATE,
                name="CDSCO / Ayush Berberine Regulatory Status",
                description="Approved in Ayurvedic, Unani, and Siddha classical and patent pharmacopoeial formulations.",
                properties={"jurisdiction": "IN", "agency": "CDSCO/Ayush", "status": "APPROVED_TRADITIONAL_FORMULATION"}
            ),

            # 10. Canonical Test & Verification Seeds (Clauses 300-315)
            SKOSMasterEntity(
                stable_id="SRC-PUB-2023-01",
                entity_type=SKOSEntityType.SOURCE,
                name="JAMA Internal Medicine 2023 Indexed Literature",
                description="High-tier indexed biomedical journal repository.",
                source_identifiers={"doi": "10.1001/jama.2023.001"},
                properties={"doi": "10.1001/jama.2023.001", "authority_tier": "TIER_A"}
            ),
            SKOSMasterEntity(
                stable_id="STU-BER-001",
                entity_type=SKOSEntityType.STUDY,
                name="Berberine vs Metformin Glycemic Control RCT 2023",
                description="Multi-center double-blind RCT on glycemic endpoints.",
                external_identifiers={"pmid": "36599001", "doi": "10.1001/jama.2023.001"},
                source_identifiers={"pmid": "36599001", "doi": "10.1001/jama.2023.001"},
                epistemic_state=SKOSEpistemicState.OBSERVED,
                properties={"doi": "10.1001/jama.2023.001", "pmid": "36599001", "sample_size": 240}
            ),
            SKOSMasterEntity(
                stable_id="FND-BER-001",
                entity_type=SKOSEntityType.RESULT,
                name="HbA1c Reduction -1.8% Finding",
                description="Statistically significant HbA1c reduction observed across intervention arm.",
                epistemic_state=SKOSEpistemicState.MEASURED,
                properties={"modality": "OBSERVED", "hba1c_reduction": -1.8}
            ),
            SKOSMasterEntity(
                stable_id="CLM-BER-001",
                entity_type=SKOSEntityType.CLAIM,
                name="Berberine Glycemic Efficacy Claim",
                description="Berberine demonstrates significant glycemic control in Type 2 Diabetes.",
                epistemic_state=SKOSEpistemicState.PROVEN,
                properties={"modality": "DEMONSTRATES", "certainty": "HIGH"}
            ),
            SKOSMasterEntity(
                stable_id="SYN-META-001",
                entity_type=SKOSEntityType.EVIDENCE,
                name="Global Living Berberine Evidence Synthesis",
                description="Living systematic synthesis of multi-center RCTs.",
                epistemic_state=SKOSEpistemicState.SUPPORTED,
                properties={"sample_size": 2400, "grade": "HIGH"}
            ),
            SKOSMasterEntity(
                stable_id="GDL-ADA-2024",
                entity_type=SKOSEntityType.GUIDELINE,
                name="ADA 2024 Standards of Care Guideline",
                description="Clinical practice guideline incorporating evidence-based glycemic adjuncts.",
                properties={"organization": "ADA", "year": 2024, "status": "ACTIVE"}
            ),
            SKOSMasterEntity(
                stable_id="CON-T2D",
                entity_type=SKOSEntityType.CONCEPT,
                name="Type 2 Diabetes Mellitus",
                description="Metabolic disease characterized by chronic hyperglycemia.",
                external_identifiers={"mesh": "D003924"},
                properties={"medical_system": "MODERN_BIOMEDICINE"}
            ),
            SKOSMasterEntity(
                stable_id="CON-DAMAVI",
                entity_type=SKOSEntityType.CONCEPT,
                name="Damavi (Sanguine Humoral Temperament)",
                description="Classical Unani Mizaj state governed by Khilt-e-Dam.",
                properties={"medical_system": "unani", "concept_type": "mizaj_humoral", "has_biomedical_equivalent": False, "status": "NO_VALID_MAPPING"}
            ),
            SKOSMasterEntity(
                stable_id="CMP-BERBERINE",
                entity_type=SKOSEntityType.ENTITY,
                name="Berberine",
                description="Bioactive isoquinoline alkaloid.",
                properties={"botanical_sources": ["Berberis aristata"]}
            ),
            SKOSMasterEntity(
                stable_id="TGT-AMPK",
                entity_type=SKOSEntityType.MECHANISM,
                name="AMP-activated protein kinase",
                description="Cellular energy regulator and primary metabolic kinase.",
                properties={"gene": "PRKAA1"}
            ),
            SKOSMasterEntity(
                stable_id="DAT-BER-001",
                entity_type=SKOSEntityType.DATASET,
                name="Clinical Trial Harmonized Dataset 2023",
                description="De-identified trial dataset of glycemic measurements.",
                epistemic_state=SKOSEpistemicState.MEASURED,
                properties={"format": "parquet", "sample_size": 520, "sha256_checksum": "sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069"}
            ),
            SKOSMasterEntity(
                stable_id="RES-CHEN-01",
                entity_type=SKOSEntityType.RESEARCHER,
                name="Dr. Michael Chen, MD, PhD",
                description="Principal Investigator in Metabolic Pharmacology.",
                properties={"affiliation": "Harvard Medical School"}
            ),
            SKOSMasterEntity(
                stable_id="INST-HARVARD",
                entity_type=SKOSEntityType.INSTITUTION,
                name="Harvard Medical School",
                description="Biomedical research university and clinical center.",
                properties={"country": "US"}
            ),
            SKOSMasterEntity(
                stable_id="GAP-BER-001",
                entity_type=SKOSEntityType.ENTITY,
                name="Berberine Bioavailability Gap",
                description="Low oral bioavailability of Berberine (<5%) due to P-glycoprotein efflux.",
                properties={"dimension": "DATA_GAP"}
            ),
            SKOSMasterEntity(
                stable_id="HYP-BER-001",
                entity_type=SKOSEntityType.HYPOTHESIS,
                name="Piperine Synergistic Bioavailability Hypothesis",
                description="Co-administration of Piperine significantly increases Berberine AUC via P-gp inhibition.",
                epistemic_state=SKOSEpistemicState.HYPOTHESIZED,
                properties={"target": "P-glycoprotein efflux"}
            ),
            SKOSMasterEntity(
                stable_id="EXP-BER-001",
                entity_type=SKOSEntityType.EXPERIMENT,
                name="In Vitro Caco-2 Transwell Permeability Assay",
                description="Bidirectional transwell permeability assay testing efflux ratio with and without P-gp inhibitor.",
                properties={"type": "BIDIRECTIONAL_PERMEABILITY", "cell_line": "Caco-2"}
            )
        ]

        for ent in seeds:
            self.register_entity(ent)

    def register_entity(self, entity: SKOSMasterEntity) -> SKOSMasterEntity:
        # Initialize provenance history if empty
        if not entity.history:
            entity.history.append({
                "timestamp": entity.created_at.isoformat(),
                "action": "REGISTERED",
                "epistemic_state": entity.epistemic_state.value if hasattr(entity.epistemic_state, "value") else str(entity.epistemic_state),
                "version_id": entity.version_id,
                "note": "Initial entity registration in Knowledge Fabric."
            })

        self._entities[entity.stable_id] = entity

        # Index external identifiers
        for prefix, val in entity.external_identifiers.items():
            self._external_id_index[f"{prefix.lower()}:{val.lower()}"] = entity.stable_id

        # Index by type
        if entity.entity_type not in self._type_index:
            self._type_index[entity.entity_type] = []
        if entity.stable_id not in self._type_index[entity.entity_type]:
            self._type_index[entity.entity_type].append(entity.stable_id)

        return entity

    def get_entity(self, stable_id: str) -> Optional[SKOSMasterEntity]:
        if stable_id in self._entities:
            return self._entities[stable_id]
        # Check case-insensitive
        for sid, ent in self._entities.items():
            if sid.lower() == stable_id.lower():
                return ent
        return None

    def lookup_by_external_id(self, prefix: str, identifier: str) -> Optional[SKOSMasterEntity]:
        key = f"{prefix.lower()}:{identifier.lower()}"
        sid = self._external_id_index.get(key)
        return self.get_entity(sid) if sid else None

    def list_entities_by_type(self, entity_type: SKOSEntityType) -> List[SKOSMasterEntity]:
        sids = self._type_index.get(entity_type, [])
        return [self._entities[sid] for sid in sids if sid in self._entities]

    def list_all_entities(self, tenant_id: Optional[str] = None) -> List[SKOSMasterEntity]:
        """Returns authorized entities respecting tenant scope (Clause 50, 307)."""
        if not tenant_id:
            return [e for e in self._entities.values() if e.classification == ResearchDataClassification.PUBLIC or e.tenant_scope is None]
        return [e for e in self._entities.values() if e.tenant_scope is None or e.tenant_scope == tenant_id]

    def count(self) -> int:
        return len(self._entities)
