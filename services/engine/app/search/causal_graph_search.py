"""
ZMIE Causal Knowledge Graph Traversal & Pathway Pathfinder (Sections 14-16)
Provides:
- Multi-hop causal pathfinding: Substance -> Target -> Signaling Pathway -> Phenotype -> Disease
- Mechanistic reasoning linking natural compounds and pharmaceuticals to biomolecular cascades
- Causal score propagation and path explainability
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from pydantic import BaseModel, Field


class CausalEdge(BaseModel):
    source: str
    target: str
    predicate: str  # ACTIVATES, INHIBITS, REGULATES, TREATS, INDUCES, ASSOCIATED_WITH
    mechanism: str
    evidence_level: str
    confidence: float
    pmid_support: Optional[str] = None


class CausalPath(BaseModel):
    path_nodes: List[str]
    edges: List[CausalEdge]
    overall_confidence: float
    mechanistic_narrative: str


class CausalGraphSearchEngine:
    """
    Traverses causal biochemical and physiological pathways to link clinical queries
    with empirical mechanisms and publications.
    """

    def __init__(self):
        self._graph: Dict[str, List[CausalEdge]] = self._build_causal_network()

    def _build_causal_network(self) -> Dict[str, List[CausalEdge]]:
        edges: List[CausalEdge] = [
            # Berberine -> AMPK -> Gluconeogenesis -> Blood Glucose -> T2DM
            CausalEdge(
                source="berberine",
                target="ampk",
                predicate="ACTIVATES",
                mechanism="Phosphorylates AMP-activated protein kinase at Thr172 by increasing intracellular AMP/ATP ratio",
                evidence_level="E4_in_vivo_preclinical",
                confidence=0.98,
                pmid_support="PMID:18442638"
            ),
            CausalEdge(
                source="ampk",
                target="gluconeogenesis",
                predicate="INHIBITS",
                mechanism="Downregulates transcription factors PEPCK and G6Pase in hepatocytes",
                evidence_level="E4_in_vivo_preclinical",
                confidence=0.95
            ),
            CausalEdge(
                source="gluconeogenesis",
                target="blood glucose",
                predicate="REGULATES",
                mechanism="Reduces hepatic glucose output and increases peripheral GLUT4 glucose uptake",
                evidence_level="E6_controlled_clinical_evidence",
                confidence=0.96,
                pmid_support="PMID:18442638"
            ),
            CausalEdge(
                source="blood glucose",
                target="type 2 diabetes mellitus",
                predicate="TREATS",
                mechanism="Reduces HbA1c and fasting blood glucose levels towards normative glycemic control",
                evidence_level="E6_controlled_clinical_evidence",
                confidence=0.99,
                pmid_support="PMID:18442638"
            ),

            # Berberine -> CYP3A4 -> Drug Bioavailability -> Adverse Interaction
            CausalEdge(
                source="berberine",
                target="cyp3a4",
                predicate="INHIBITS",
                mechanism="Mechanism-based competitive inhibition of Cytochrome P450 3A4 and P-glycoprotein efflux pump",
                evidence_level="E5_human_observational",
                confidence=0.97,
                pmid_support="PMID:22105432"
            ),
            CausalEdge(
                source="cyp3a4",
                target="cyclosporine bioavailability",
                predicate="REGULATES",
                mechanism="Decreases first-pass hepatic and intestinal clearance of CYP3A4 substrates, doubling plasma AUC",
                evidence_level="E5_human_observational",
                confidence=0.95,
                pmid_support="PMID:22105432"
            ),
            CausalEdge(
                source="cyclosporine bioavailability",
                target="drug toxicity",
                predicate="INDUCES",
                mechanism="Elevated drug serum concentration increases nephrotoxicity and neurotoxicity risk",
                evidence_level="E6_controlled_clinical_evidence",
                confidence=0.94,
                pmid_support="PMID:22105432"
            ),

            # Metformin -> AMPK -> T2DM
            CausalEdge(
                source="metformin",
                target="ampk",
                predicate="ACTIVATES",
                mechanism="Inhibits mitochondrial complex I, leading to elevated AMP and indirect AMPK activation",
                evidence_level="E6_controlled_clinical_evidence",
                confidence=0.99,
                pmid_support="PMID:18442638"
            ),

            # Curcumin -> NF-kB -> COX-2 -> Inflammation -> Rheumatoid Arthritis
            CausalEdge(
                source="curcumin",
                target="nf-kb",
                predicate="INHIBITS",
                mechanism="Blocks IkappaB kinase (IKK) phosphorylation and subsequent NF-kB nuclear translocation",
                evidence_level="E4_in_vivo_preclinical",
                confidence=0.96
            ),
            CausalEdge(
                source="nf-kb",
                target="cox-2",
                predicate="INHIBITS",
                mechanism="Suppresses transcription of pro-inflammatory enzymes cyclooxygenase-2 and inducible nitric oxide synthase",
                evidence_level="E4_in_vivo_preclinical",
                confidence=0.95
            ),
            CausalEdge(
                source="cox-2",
                target="rheumatoid arthritis",
                predicate="TREATS",
                mechanism="Alleviates joint stiffness, synovial swelling, and morning pain index",
                evidence_level="E6_controlled_clinical_evidence",
                confidence=0.92
            ),

            # Unani: Su-e-Mizaj Barid -> Zoaf-e-Meda -> Balgham-e-Kham -> Dyspepsia
            CausalEdge(
                source="su-e-mizaj barid",
                target="zoaf-e-meda",
                predicate="INDUCES",
                mechanism="Cold temperamental dyscrasia dampens innate metabolic heat of the stomach",
                evidence_level="canonical_traditional_claim",
                confidence=0.90,
                pmid_support="CODEX:AL_QANUN_BOOK_3"
            ),
            CausalEdge(
                source="zoaf-e-meda",
                target="irritable bowel syndrome",
                predicate="ASSOCIATED_WITH",
                mechanism="Impaired gastric digestion leads to abdominal fullness, variable stooling, and visceral sensitivity",
                evidence_level="canonical_traditional_claim",
                confidence=0.88,
                pmid_support="CODEX:AL_QANUN_BOOK_3"
            ),

            # Ayurveda: Mandagni -> Ama -> Grahani Roga / IBS
            CausalEdge(
                source="mandagni",
                target="ama",
                predicate="INDUCES",
                mechanism="Hypoactive digestive fire results in unprocessed, toxic bio-metabolic residue (Ama)",
                evidence_level="canonical_traditional_claim",
                confidence=0.90,
                pmid_support="CODEX:CHARAKA_SAMHITA_CHIKITSA_15"
            ),
            CausalEdge(
                source="ama",
                target="irritable bowel syndrome",
                predicate="ASSOCIATED_WITH",
                mechanism="Accumulation in Grahani disturbs enteric function causing alternating diarrhea and constipation",
                evidence_level="canonical_traditional_claim",
                confidence=0.89,
                pmid_support="CODEX:CHARAKA_SAMHITA_CHIKITSA_15"
            )
        ]

        graph: Dict[str, List[CausalEdge]] = {}
        for edge in edges:
            src = edge.source.lower()
            if src not in graph:
                graph[src] = []
            graph[src].append(edge)
        return graph

    def find_causal_paths(self, start_concept: str, target_concept: Optional[str] = None, max_depth: int = 4) -> List[CausalPath]:
        """
        Finds directed causal multi-hop paths starting from a source concept.
        """
        start = start_concept.lower().strip()
        results: List[CausalPath] = []

        # Find best matching root node
        matching_roots = [k for k in self._graph.keys() if start in k or k in start]
        if not matching_roots:
            return []

        for root in matching_roots:
            queue: List[Tuple[str, List[CausalEdge], float]] = [(root, [], 1.0)]
            visited_paths: Set[str] = set()

            while queue:
                current_node, current_edges, current_conf = queue.pop(0)

                if len(current_edges) >= max_depth:
                    continue

                if current_node in self._graph:
                    for edge in self._graph[current_node]:
                        next_node = edge.target.lower()

                        # Prevent cycles
                        if next_node in [e.source for e in current_edges] or next_node == root:
                            continue

                        new_edges = current_edges + [edge]
                        new_conf = round(current_conf * edge.confidence * 0.95, 4)

                        path_key = "->".join([root] + [e.target for e in new_edges])
                        if path_key in visited_paths:
                            continue
                        visited_paths.add(path_key)

                        narrative = " ➔ ".join([f"{e.source.title()} [{e.predicate}] {e.target.title()}" for e in new_edges])

                        path_obj = CausalPath(
                            path_nodes=[root] + [e.target for e in new_edges],
                            edges=new_edges,
                            overall_confidence=new_conf,
                            mechanistic_narrative=narrative
                        )

                        # Check if matches target concept or return valid deep path
                        if target_concept:
                            tgt_l = target_concept.lower().strip()
                            if tgt_l in next_node or next_node in tgt_l:
                                results.append(path_obj)
                            else:
                                queue.append((next_node, new_edges, new_conf))
                        else:
                            results.append(path_obj)
                            queue.append((next_node, new_edges, new_conf))

        # Sort by confidence descending
        results.sort(key=lambda p: p.overall_confidence, reverse=True)
        return results[:10]

    def score_document_causality(self, doc_text: str, query_concepts: List[str]) -> Tuple[float, List[CausalPath]]:
        """
        Evaluates whether a document's content connects to active causal pathways for the query concepts.
        """
        doc_l = doc_text.lower()
        matched_paths: List[CausalPath] = []
        max_score = 0.0

        for concept in query_concepts:
            paths = self.find_causal_paths(concept)
            for path in paths:
                # Check how many nodes in the causal path are mentioned in document
                present_nodes = sum(1 for node in path.path_nodes if node in doc_l)
                if present_nodes >= 2:
                    matched_paths.append(path)
                    score = (present_nodes / len(path.path_nodes)) * path.overall_confidence
                    if score > max_score:
                        max_score = score

        return round(min(1.0, max_score), 4), matched_paths[:3]
