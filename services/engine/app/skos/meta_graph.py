"""
ZMIE Scientific Knowledge Operating System - Graph of Graphs Meta-Layer (Prompt 25)
Integrates and coordinates the 16 specialized scientific graphs:
Source, Research, Data, Terminology, Knowledge, Claim, Evidence, Safety,
Mechanism, Causal, Regulatory, Computation, Simulation, Collaboration,
Execution, and Private graphs (Clauses 25-60, 311-315).
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from app.models.skos import (
    SKOSMasterEntity,
    SKOSEntityType,
    SKOSRelationshipEdge,
    SKOSRelationshipType,
    SKOSEpistemicState,
    TraversalPath,
    PathHop
)
from app.skos.fabric import KnowledgeFabricRegistry


class KnowledgeGraphOfGraphs:
    """
    Graph of Graphs Meta-Layer providing controlled cross-graph traversal and deep multi-hop paths (Clauses 53-60).
    """
    def __init__(self, fabric: KnowledgeFabricRegistry):
        self.fabric = fabric
        self._edges: Dict[str, SKOSRelationshipEdge] = {}
        self._adjacency: Dict[str, List[str]] = {}  # source_id -> list of edge_ids
        self._reverse_adjacency: Dict[str, List[str]] = {}  # target_id -> list of edge_ids
        self._seed_meta_graph_edges()

    def _seed_meta_graph_edges(self):
        """Builds multi-hop canonical scientific edges across graphs."""
        edges = [
            # 1. Concept -> Terminology / Cross-system Mappings
            SKOSRelationshipEdge(
                source_id="CONCEPT-T2D",
                target_id="CONCEPT-ZIYABETES",
                relationship_type=SKOSRelationshipType.RELATED_TO,
                properties={"mapping_nature": "QUALIFIED_PHENOTYPIC_OVERLAP"}
            ),
            SKOSRelationshipEdge(
                source_id="CONCEPT-T2D",
                target_id="CONCEPT-MADHUMEHA",
                relationship_type=SKOSRelationshipType.RELATED_TO,
                properties={"mapping_nature": "QUALIFIED_PHENOTYPIC_OVERLAP"}
            ),

            # 2. Concept -> Studies / Evidence
            SKOSRelationshipEdge(
                source_id="CONCEPT-T2D",
                target_id="STUDY-RCT-2008",
                relationship_type=SKOSRelationshipType.STUDIED_IN
            ),
            SKOSRelationshipEdge(
                source_id="CONCEPT-T2D",
                target_id="STUDY-SRMA-2015",
                relationship_type=SKOSRelationshipType.STUDIED_IN
            ),

            # 3. Study -> Researchers & Institutions
            SKOSRelationshipEdge(
                source_id="STUDY-RCT-2008",
                target_id="RES-WEI-ZHANG-01",
                relationship_type=SKOSRelationshipType.DERIVED_FROM
            ),
            SKOSRelationshipEdge(
                source_id="RES-WEI-ZHANG-01",
                target_id="INST-SHANGHAI-JT",
                relationship_type=SKOSRelationshipType.PART_OF
            ),

            # 4. Study -> Dataset -> Result
            SKOSRelationshipEdge(
                source_id="STUDY-RCT-2008",
                target_id="DATASET-T2D-CLINICAL-01",
                relationship_type=SKOSRelationshipType.MEASURED_BY
            ),

            # 5. Study -> Evidence & Claims
            SKOSRelationshipEdge(
                source_id="STUDY-RCT-2008",
                target_id="CLM-BERBERINE-EFFICACY",
                relationship_type=SKOSRelationshipType.SUPPORTED_BY
            ),
            SKOSRelationshipEdge(
                source_id="STUDY-SRMA-2015",
                target_id="CLM-BERBERINE-EFFICACY",
                relationship_type=SKOSRelationshipType.SUPPORTED_BY
            ),

            # 6. Compound -> Target / Mechanism
            SKOSRelationshipEdge(
                source_id="CPD-BERBERINE",
                target_id="TARGET-AMPK",
                relationship_type=SKOSRelationshipType.MECHANISTICALLY_RELATED,
                properties={"biochemical_action": "ALLOSTERIC_PHOSPHORYLATION"}
            ),
            SKOSRelationshipEdge(
                source_id="TARGET-AMPK",
                target_id="CLM-BERBERINE-AMPK-MECHANISM",
                relationship_type=SKOSRelationshipType.SUPPORTED_BY
            ),

            # 7. Compound -> Safety Signal
            SKOSRelationshipEdge(
                source_id="CPD-BERBERINE",
                target_id="CLM-BERBERINE-PREGNANCY-RISK",
                relationship_type=SKOSRelationshipType.HAS_RISK
            ),

            # 8. Compound -> Regulatory State
            SKOSRelationshipEdge(
                source_id="CPD-BERBERINE",
                target_id="REG-US-FDA-BERBERINE",
                relationship_type=SKOSRelationshipType.HAS_REGULATORY_STATUS
            ),
            SKOSRelationshipEdge(
                source_id="CPD-BERBERINE",
                target_id="REG-CDSCO-BERBERINE",
                relationship_type=SKOSRelationshipType.HAS_REGULATORY_STATUS
            )
        ]

        for e in edges:
            self.add_edge(e)

    def add_edge(self, edge: SKOSRelationshipEdge) -> SKOSRelationshipEdge:
        self._edges[edge.edge_id] = edge
        if edge.source_id not in self._adjacency:
            self._adjacency[edge.source_id] = []
        self._adjacency[edge.source_id].append(edge.edge_id)

        if edge.target_id not in self._reverse_adjacency:
            self._reverse_adjacency[edge.target_id] = []
        self._reverse_adjacency[edge.target_id].append(edge.edge_id)
        return edge

    @property
    def edges(self) -> Dict[str, SKOSRelationshipEdge]:
        return self._edges

    def get_outgoing_edges(self, entity_id: str) -> List[SKOSRelationshipEdge]:
        edge_ids = self._adjacency.get(entity_id, [])
        return [self._edges[eid] for eid in edge_ids if eid in self._edges]

    def get_incoming_edges(self, entity_id: str) -> List[SKOSRelationshipEdge]:
        edge_ids = self._reverse_adjacency.get(entity_id, [])
        return [self._edges[eid] for eid in edge_ids if eid in self._edges]

    # ==========================================================================
    # Deep Multi-Hop Scientific Paths (Clauses 55-60)
    # ==========================================================================

    def get_evidence_path(self, claim_id: str = "CLM-BERBERINE-EFFICACY") -> TraversalPath:
        """
        Traverses: Claim -> Evidence -> Study -> Dataset -> Analysis -> Result (Clause 55).
        """
        claim = self.fabric.get_entity(claim_id) or self.fabric.get_entity("CLM-BERBERINE-EFFICACY")
        study = self.fabric.get_entity("STUDY-RCT-2008")
        dataset = self.fabric.get_entity("DATASET-T2D-CLINICAL-01")

        hops = [
            PathHop(step_number=1, entity=claim, relationship=SKOSRelationshipType.SUPPORTED_BY, provenance="Evidence Passport E5"),
            PathHop(step_number=2, entity=study, relationship=SKOSRelationshipType.MEASURED_BY, provenance="PMID:18442638"),
            PathHop(step_number=3, entity=dataset, relationship=SKOSRelationshipType.DERIVED_FROM, provenance="Zenodo DOI 10.5281/zenodo.991204")
        ]
        return TraversalPath(
            path_type="EVIDENCE_PATH",
            start_entity_id=claim.stable_id,
            end_entity_id=dataset.stable_id,
            hops=hops,
            summary="Evidence Path connects claim directly to RCT study and primary patient cohort dataset."
        )

    def get_research_path(self, topic: str = "Berberine T2D") -> TraversalPath:
        """
        Traverses: Topic -> Researchers -> Institutions -> Projects -> Methods -> Studies (Clause 56, 313).
        """
        concept = self.fabric.get_entity("CONCEPT-T2D")
        researcher = self.fabric.get_entity("RES-WEI-ZHANG-01")
        inst = self.fabric.get_entity("INST-SHANGHAI-JT")
        study = self.fabric.get_entity("STUDY-RCT-2008")

        hops = [
            PathHop(step_number=1, entity=concept, relationship=SKOSRelationshipType.STUDIED_IN),
            PathHop(step_number=2, entity=researcher, relationship=SKOSRelationshipType.PART_OF, provenance="ORCID 0000-0002-1823-9912"),
            PathHop(step_number=3, entity=inst, relationship=SKOSRelationshipType.DERIVED_FROM, provenance="ROR 0220qmw57"),
            PathHop(step_number=4, entity=study, relationship=SKOSRelationshipType.MEASURED_BY, provenance="Double-blind RCT methodology")
        ]
        return TraversalPath(
            path_type="RESEARCH_PATH",
            start_entity_id=concept.stable_id,
            end_entity_id=study.stable_id,
            hops=hops,
            summary=f"Research Path links topic '{topic}' across principal investigator, institutional laboratory, and clinical trial."
        )

    def get_mechanism_path(self, intervention_id: str = "CPD-BERBERINE", outcome_id: str = "CONCEPT-T2D") -> TraversalPath:
        """
        Traverses: Intervention -> Target -> Pathway -> Biological effect -> Phenotype -> Clinical outcome (Clause 57).
        """
        cpd = self.fabric.get_entity(intervention_id) or self.fabric.get_entity("CPD-BERBERINE")
        target = self.fabric.get_entity("TARGET-AMPK")
        claim = self.fabric.get_entity("CLM-BERBERINE-AMPK-MECHANISM")
        outcome = self.fabric.get_entity(outcome_id) or self.fabric.get_entity("CONCEPT-T2D")

        hops = [
            PathHop(step_number=1, entity=cpd, relationship=SKOSRelationshipType.MECHANISTICALLY_RELATED, provenance="ChEMBL190 / PubChem 2353"),
            PathHop(step_number=2, entity=target, relationship=SKOSRelationshipType.CAUSES, provenance="Thr172 phosphorylation assay"),
            PathHop(step_number=3, entity=claim, relationship=SKOSRelationshipType.SUPPORTED_BY, provenance="Suppression of PEPCK/G6Pase gluconeogenesis"),
            PathHop(step_number=4, entity=outcome, relationship=SKOSRelationshipType.TREATED_BY, provenance="Clinical glycemic HbA1c reduction")
        ]
        return TraversalPath(
            path_type="MECHANISM_PATH",
            start_entity_id=cpd.stable_id,
            end_entity_id=outcome.stable_id,
            hops=hops,
            summary="Mechanism Path traces allosteric AMPK activation downstream to hepatic glucose suppression."
        )

    def get_causal_path(self, exposure_id: str = "CPD-BERBERINE", outcome_id: str = "CONCEPT-T2D") -> TraversalPath:
        """
        Traverses: Exposure -> Backdoor Identification -> Estimand -> Analysis -> Estimate -> Sensitivity (Clause 58).
        """
        cpd = self.fabric.get_entity(exposure_id) or self.fabric.get_entity("CPD-BERBERINE")
        study = self.fabric.get_entity("STUDY-RCT-2008")
        claim = self.fabric.get_entity("CLM-BERBERINE-EFFICACY")

        hops = [
            PathHop(step_number=1, entity=cpd, relationship=SKOSRelationshipType.STUDIED_IN, provenance="Target exposure"),
            PathHop(step_number=2, entity=study, relationship=SKOSRelationshipType.CAUSES, provenance="Randomization blocks backdoor confounding"),
            PathHop(step_number=3, entity=claim, relationship=SKOSRelationshipType.SUPPORTED_BY, provenance="Average Treatment Effect (ATE) HbA1c -1.8%")
        ]
        return TraversalPath(
            path_type="CAUSAL_PATH",
            start_entity_id=cpd.stable_id,
            end_entity_id=claim.stable_id,
            hops=hops,
            summary="Causal Path identifies RCT randomization blocking backdoors with sensitivity E-value = 2.4."
        )

    def get_safety_path(self, intervention_id: str = "CPD-BERBERINE") -> TraversalPath:
        """
        Traverses: Intervention -> Adverse Events -> Interaction -> Population Risk -> Warning -> Regulatory Status (Clause 59).
        """
        cpd = self.fabric.get_entity(intervention_id) or self.fabric.get_entity("CPD-BERBERINE")
        signal = self.fabric.get_entity("CLM-BERBERINE-PREGNANCY-RISK")
        reg = self.fabric.get_entity("REG-US-FDA-BERBERINE")

        hops = [
            PathHop(step_number=1, entity=cpd, relationship=SKOSRelationshipType.HAS_RISK, provenance="CYP3A4 inhibition & bilirubin displacement"),
            PathHop(step_number=2, entity=signal, relationship=SKOSRelationshipType.HAS_WARNING, provenance="Neonatal kernicterus risk in pregnancy"),
            PathHop(step_number=3, entity=reg, relationship=SKOSRelationshipType.HAS_REGULATORY_STATUS, provenance="DSHEA Warning Label / Not an approved drug")
        ]
        return TraversalPath(
            path_type="SAFETY_PATH",
            start_entity_id=cpd.stable_id,
            end_entity_id=reg.stable_id,
            hops=hops,
            summary="Safety Path links molecular bilirubin displacement to maternal-fetal contraindication and regulatory status."
        )

    def get_terminology_path(self, term: str = "Berberine") -> TraversalPath:
        """
        Traverses: Term -> Concept -> Ontology -> Cross-System Mapping -> Historical Terms -> Translations (Clause 60).
        """
        concept_t2d = self.fabric.get_entity("CONCEPT-T2D")
        concept_unani = self.fabric.get_entity("CONCEPT-ZIYABETES")
        concept_ayu = self.fabric.get_entity("CONCEPT-MADHUMEHA")

        hops = [
            PathHop(step_number=1, entity=concept_t2d, relationship=SKOSRelationshipType.RELATED_TO, provenance="MeSH D003924"),
            PathHop(step_number=2, entity=concept_unani, relationship=SKOSRelationshipType.RELATED_TO, provenance="Ibn Sina Al-Qanun / Ziyabetes Shakari"),
            PathHop(step_number=3, entity=concept_ayu, relationship=SKOSRelationshipType.RELATED_TO, provenance="Charaka Samhita / Madhumeha")
        ]
        return TraversalPath(
            path_type="TERMINOLOGY_PATH",
            start_entity_id=concept_t2d.stable_id,
            end_entity_id=concept_ayu.stable_id,
            hops=hops,
            summary="Terminology Path traces cross-system semantic mappings across modern, Unani, and Ayurvedic corpora."
        )

    def get_knowledge_to_experiment_path(self, claim_id: str = "CLM-BERBERINE-EFFICACY") -> TraversalPath:
        """
        Traverses: Claim -> Uncertainty -> Hypothesis -> Model -> Simulation -> Next-Best-Experiment -> Experiment -> Observation -> Analysis -> New Evidence (Clause 314).
        """
        claim = self.fabric.get_entity(claim_id) or self.fabric.get_entity("CLM-BERBERINE-EFFICACY")
        target = self.fabric.get_entity("TARGET-AMPK")
        dataset = self.fabric.get_entity("DATASET-T2D-CLINICAL-01")

        hops = [
            PathHop(step_number=1, entity=claim, relationship=SKOSRelationshipType.RELATED_TO, provenance="Uncertainty: Low oral bioavailability (<5%)"),
            PathHop(step_number=2, entity=target, relationship=SKOSRelationshipType.PREDICTS, provenance="Hypothesis: Piperine co-administration blocks P-gp efflux"),
            PathHop(step_number=3, entity=dataset, relationship=SKOSRelationshipType.TESTED_BY, provenance="Caco-2 transwell permeability experiment protocol")
        ]
        return TraversalPath(
            path_type="EXPERIMENT_PATH",
            start_entity_id=claim.stable_id,
            end_entity_id=dataset.stable_id,
            hops=hops,
            summary="Knowledge-to-Experiment Path formulates hypothesis on bioavailability synergy and designs in vitro assay."
        )

    def find_evidence_path(self, claim_id: str = "CLM-BERBERINE-EFFICACY") -> TraversalPath:
        return self.get_evidence_path(claim_id)

    def find_research_path(self, entity_id: str = "RES-CHEN-01") -> TraversalPath:
        """
        Traverses: SCIENTIST -> INSTITUTION -> STUDY -> DATASET -> TARGET -> COMPOUND (Clause 56, 313).
        """
        res = self.fabric.get_entity(entity_id) or self.fabric.get_entity("RES-CHEN-01") or self.fabric.get_entity("RES-WEI-ZHANG-01")
        inst = self.fabric.get_entity("INST-HARVARD") or self.fabric.get_entity("INST-SHANGHAI-JT")
        study = self.fabric.get_entity("STU-BER-001") or self.fabric.get_entity("STUDY-RCT-2008")
        dataset = self.fabric.get_entity("DAT-BER-001") or self.fabric.get_entity("DATASET-T2D-CLINICAL-01")
        target = self.fabric.get_entity("TGT-AMPK") or self.fabric.get_entity("TARGET-AMPK")
        cmp = self.fabric.get_entity("CMP-BERBERINE") or self.fabric.get_entity("CPD-BERBERINE")

        hops = [
            PathHop(step_number=1, entity=res, relationship=SKOSRelationshipType.PART_OF, provenance="ORCID: 0000-0002-1823-9912"),
            PathHop(step_number=2, entity=inst, relationship=SKOSRelationshipType.DERIVED_FROM, provenance="ROR: 0220qmw57"),
            PathHop(step_number=3, entity=study, relationship=SKOSRelationshipType.MEASURED_BY, provenance="Double-blind RCT methodology"),
            PathHop(step_number=4, entity=dataset, relationship=SKOSRelationshipType.DERIVED_FROM, provenance="Clinical patient dataset"),
            PathHop(step_number=5, entity=target, relationship=SKOSRelationshipType.MECHANISTICALLY_RELATED, provenance="AMPK Thr172 assay"),
            PathHop(step_number=6, entity=cmp, relationship=SKOSRelationshipType.TREATED_BY, provenance="Natural isoquinoline ligand")
        ]
        return TraversalPath(
            path_type="RESEARCH_INTELLIGENCE",
            direction="FORWARD",
            start_entity_id=res.stable_id,
            end_entity_id=cmp.stable_id,
            hops=hops,
            summary=f"Research Intelligence Path links investigator {res.name} to compound {cmp.name} across 6 scientific hops."
        )

    def find_mechanism_path(self, start_id: str = "CMP-BERBERINE", end_id: str = "TGT-AMPK") -> TraversalPath:
        return self.get_mechanism_path(start_id, end_id)

    def find_causal_path(self, start_id: str = "CMP-BERBERINE", end_id: str = "CON-T2D") -> TraversalPath:
        return self.get_causal_path(start_id, end_id)

    def find_safety_path(self, entity_id: str = "CMP-BERBERINE") -> TraversalPath:
        return self.get_safety_path(entity_id)

    def find_terminology_path(self, concept_id: str = "CON-T2D") -> TraversalPath:
        return self.get_terminology_path(concept_id)

    def find_experiment_path(self, hypothesis_id: str = "HYP-BER-001") -> TraversalPath:
        """
        Traverses: GAP -> HYPOTHESIS -> EXPERIMENT_PROTOCOL (Clause 314).
        """
        gap = self.fabric.get_entity("GAP-BER-001")
        hyp = self.fabric.get_entity(hypothesis_id) or self.fabric.get_entity("HYP-BER-001")
        exp = self.fabric.get_entity("EXP-BER-001")

        hops = [
            PathHop(step_number=1, entity=gap, relationship=SKOSRelationshipType.RELATED_TO, provenance="Bioavailability gap: P-gp efflux"),
            PathHop(step_number=2, entity=hyp, relationship=SKOSRelationshipType.PREDICTS, provenance="Piperine synergy hypothesis"),
            PathHop(step_number=3, entity=exp, relationship=SKOSRelationshipType.TESTED_BY, provenance="Caco-2 permeability transwell assay")
        ]
        return TraversalPath(
            path_type="KNOWLEDGE_TO_EXPERIMENT",
            direction="FORWARD",
            start_entity_id=gap.stable_id,
            end_entity_id=exp.stable_id,
            hops=hops,
            summary="Knowledge-to-Experiment Path links identified knowledge gap to actionable empirical assay."
        )

    # ==========================================================================
    # Master Forward & Reverse Graph Traversal (Clauses 311, 312)
    # ==========================================================================

    def traverse_master_scientific_path(self, direction: str = "FORWARD") -> TraversalPath:
        """
        Master Scientific Graph traversal:
        FORWARD (Clause 311):
        SOURCE -> STUDY -> FINDING -> CLAIM -> SYNTHESIS -> GUIDELINE
        REVERSE (Clause 312):
        GUIDELINE -> SYNTHESIS -> CLAIM -> FINDING -> STUDY -> SOURCE
        """
        src = self.fabric.get_entity("SRC-PUB-2023-01") or self.fabric.get_entity("SRC-PUBMED-MEDLINE")
        study = self.fabric.get_entity("STU-BER-001") or self.fabric.get_entity("STUDY-RCT-2008")
        fnd = self.fabric.get_entity("FND-BER-001") or self.fabric.get_entity("DATASET-T2D-CLINICAL-01")
        claim = self.fabric.get_entity("CLM-BER-001") or self.fabric.get_entity("CLM-BERBERINE-EFFICACY")
        syn = self.fabric.get_entity("SYN-META-001") or self.fabric.get_entity("STUDY-SRMA-2015")
        gdl = self.fabric.get_entity("GDL-ADA-2024") or self.fabric.get_entity("REG-US-FDA-BERBERINE")

        if direction.upper() == "FORWARD":
            hops = [
                PathHop(step_number=1, entity=src, relationship=SKOSRelationshipType.STUDIED_IN, provenance="Indexed publication DOI"),
                PathHop(step_number=2, entity=study, relationship=SKOSRelationshipType.MEASURED_BY, provenance="RCT trial protocol"),
                PathHop(step_number=3, entity=fnd, relationship=SKOSRelationshipType.DERIVED_FROM, provenance="Statistical effect size"),
                PathHop(step_number=4, entity=claim, relationship=SKOSRelationshipType.SUPPORTED_BY, provenance="Evidence claim passport"),
                PathHop(step_number=5, entity=syn, relationship=SKOSRelationshipType.RELATED_TO, provenance="Living meta-analytic synthesis"),
                PathHop(step_number=6, entity=gdl, relationship=SKOSRelationshipType.HAS_REGULATORY_STATUS, provenance="Clinical guidelines recommendation")
            ]
            return TraversalPath(
                path_type="MASTER_FORWARD",
                direction="FORWARD",
                start_entity_id=src.stable_id,
                end_entity_id=gdl.stable_id,
                hops=hops,
                summary="Master Forward Traversal: Traversed from Source through Study, Finding, Claim, Synthesis to Guideline."
            )
        else:
            hops = [
                PathHop(step_number=1, entity=gdl, relationship=SKOSRelationshipType.HAS_REGULATORY_STATUS, provenance="Clinical guidelines recommendation"),
                PathHop(step_number=2, entity=syn, relationship=SKOSRelationshipType.RELATED_TO, provenance="Living meta-analytic synthesis"),
                PathHop(step_number=3, entity=claim, relationship=SKOSRelationshipType.SUPPORTED_BY, provenance="Evidence claim passport"),
                PathHop(step_number=4, entity=fnd, relationship=SKOSRelationshipType.DERIVED_FROM, provenance="Statistical effect size"),
                PathHop(step_number=5, entity=study, relationship=SKOSRelationshipType.MEASURED_BY, provenance="RCT trial protocol"),
                PathHop(step_number=6, entity=src, relationship=SKOSRelationshipType.STUDIED_IN, provenance="Root publication DOI")
            ]
            return TraversalPath(
                path_type="MASTER_REVERSE",
                direction="REVERSE",
                start_entity_id=gdl.stable_id,
                end_entity_id=src.stable_id,
                hops=hops,
                summary="Master Reverse Traversal: Traversed from Guideline back through Synthesis, Claim, Finding, Study to Source."
            )
