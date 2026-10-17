"""
ZMIE Research Provenance & Bidirectional Lineage Graph (Prompt 26)
Constructs full execution traces and performs backward attribution and forward impact analysis (Clauses 15, 16, 122, 125, 142, 198).
"""

from typing import Dict, List, Optional, Any, Set
from collections import deque
import logging

from app.models.audit import (
    ResearchSnapshot,
    TraceNode,
    TraceEdge,
    ScientificResearchTrace,
)

logger = logging.getLogger("zmie.audit.provenance_graph")


class ResearchProvenanceGraph:
    """
    Constructs and navigates the end-to-end scientific research lineage graph:
    Question -> Plan -> Search -> Sources -> Studies -> Screening -> Extraction
             -> Data -> Analysis -> Model -> Result -> Claim -> Review -> Conclusion
    """

    def __init__(self):
        # Key: snapshot_id -> ScientificResearchTrace
        self._traces: Dict[str, ScientificResearchTrace] = {}

    def build_trace(self, snapshot: ResearchSnapshot) -> ScientificResearchTrace:
        """
        Builds a comprehensive directed acyclic graph (DAG) representing the complete
        lifecycle of a research snapshot.
        """
        nodes: List[TraceNode] = []
        edges: List[TraceEdge] = []

        q_node_id = f"node-q-{snapshot.snapshot_id}"
        nodes.append(TraceNode(
            node_id=q_node_id,
            node_type="QUESTION",
            label="Research Question",
            properties={"text": snapshot.research_question, "version": snapshot.question_version}
        ))

        # 1. Plan node
        plan_node_id = None
        if snapshot.analysis_plan:
            plan_node_id = f"node-plan-{snapshot.analysis_plan.plan_id}"
            nodes.append(TraceNode(
                node_id=plan_node_id,
                node_type="PLAN",
                label="Analysis Plan",
                properties={"method": snapshot.analysis_plan.analysis_method, "estimand": snapshot.analysis_plan.estimand}
            ))
            edges.append(TraceEdge(
                source_id=q_node_id,
                target_id=plan_node_id,
                relation="GENERATES",
                provenance="Research plan formalized from question"
            ))

        # 2. Search strategy
        search_node_id = None
        if snapshot.search_strategy:
            search_node_id = f"node-search-{snapshot.search_strategy.query_id}"
            nodes.append(TraceNode(
                node_id=search_node_id,
                node_type="SEARCH",
                label="Search Strategy",
                properties={
                    "original_query": snapshot.search_strategy.original_query,
                    "results_count": snapshot.search_strategy.results_count
                }
            ))
            parent_for_search = plan_node_id or q_node_id
            edges.append(TraceEdge(
                source_id=parent_for_search,
                target_id=search_node_id,
                relation="SEARCHES",
                provenance="Search strategy formulated"
            ))

        # 3. Sources and Studies
        study_node_ids = []
        for idx, item in enumerate(snapshot.evidence_items):
            s_id = item.get("study_id") or f"study-{idx}"
            s_node_id = f"node-study-{s_id}"
            study_node_ids.append(s_node_id)
            nodes.append(TraceNode(
                node_id=s_node_id,
                node_type="STUDY",
                label=f"Study: {item.get('title', s_id)[:50]}",
                properties=item
            ))
            parent_for_study = search_node_id or q_node_id
            edges.append(TraceEdge(
                source_id=parent_for_study,
                target_id=s_node_id,
                relation="RETRIEVES",
                provenance="Study retrieved from search strategy"
            ))

        # 4. Screening decisions
        screen_node_ids = []
        for decision in snapshot.screening_decisions:
            scr_node_id = f"node-scr-{decision.decision_id}"
            screen_node_ids.append(scr_node_id)
            nodes.append(TraceNode(
                node_id=scr_node_id,
                node_type="SCREENING",
                label=f"Screening: {decision.decision}",
                properties={"decision": decision.decision, "reason": str(decision.reason)}
            ))
            matching_study_node = f"node-study-{decision.study_id}"
            if any(n.node_id == matching_study_node for n in nodes):
                edges.append(TraceEdge(
                    source_id=matching_study_node,
                    target_id=scr_node_id,
                    relation="SCREENS",
                    provenance=f"Decision {decision.decision} applied to study"
                ))

        # 5. Extractions
        ext_node_ids = []
        for ext in snapshot.extractions:
            ext_node_id = f"node-ext-{ext.record_id}"
            ext_node_ids.append(ext_node_id)
            nodes.append(TraceNode(
                node_id=ext_node_id,
                node_type="EXTRACTION",
                label=f"Extract: {ext.field_name}",
                properties={
                    "field": ext.field_name,
                    "normalized": ext.normalized_value,
                    "source_val": ext.original_source_value
                }
            ))
            matching_study_node = f"node-study-{ext.study_id}"
            if any(n.node_id == matching_study_node for n in nodes):
                edges.append(TraceEdge(
                    source_id=matching_study_node,
                    target_id=ext_node_id,
                    relation="EXTRACTS",
                    provenance=f"Extracted {ext.field_name} from study"
                ))

        # 6. Analysis / Computation step
        analysis_node_id = f"node-analysis-{snapshot.snapshot_id}"
        nodes.append(TraceNode(
            node_id=analysis_node_id,
            node_type="ANALYSIS",
            label="Statistical & Computational Analysis",
            properties={
                "workflow": snapshot.workflow_id,
                "environment_os": snapshot.environment.os
            }
        ))
        # Connect extractions or studies to analysis
        for e_id in (ext_node_ids or study_node_ids or [q_node_id]):
            edges.append(TraceEdge(
                source_id=e_id,
                target_id=analysis_node_id,
                relation="ANALYZES",
                provenance="Evidence inputs fed to computational analysis"
            ))

        # 7. Results
        result_node_ids = []
        for idx, res in enumerate(snapshot.results):
            r_id = res.get("result_id") or f"res-{idx}"
            r_node_id = f"node-res-{r_id}"
            result_node_ids.append(r_node_id)
            nodes.append(TraceNode(
                node_id=r_node_id,
                node_type="RESULT",
                label=f"Result: {res.get('name', 'Computed Estimate')}",
                properties=res
            ))
            edges.append(TraceEdge(
                source_id=analysis_node_id,
                target_id=r_node_id,
                relation="COMPUTES",
                provenance="Result derived from analysis execution"
            ))

        # 8. Claims
        claim_node_ids = []
        for idx, cl in enumerate(snapshot.claims):
            c_id = cl.get("claim_id") or f"claim-{idx}"
            c_node_id = f"node-claim-{c_id}"
            claim_node_ids.append(c_node_id)
            nodes.append(TraceNode(
                node_id=c_node_id,
                node_type="CLAIM",
                label=f"Claim: {str(cl.get('statement', 'Scientific Claim'))[:50]}",
                properties=cl
            ))
            for r_id in (result_node_ids or [analysis_node_id]):
                edges.append(TraceEdge(
                    source_id=r_id,
                    target_id=c_node_id,
                    relation="SUPPORTS",
                    provenance="Result supports scientific claim"
                ))

        # 9. Conclusion Node
        concl_node_id = f"node-concl-{snapshot.snapshot_id}"
        nodes.append(TraceNode(
            node_id=concl_node_id,
            node_type="CONCLUSION",
            label="Final Scientific Synthesis",
            properties=snapshot.final_output or {"conclusion": "Research completed"}
        ))
        for c_id in (claim_node_ids or result_node_ids or [analysis_node_id]):
            edges.append(TraceEdge(
                source_id=c_id,
                target_id=concl_node_id,
                relation="CONCLUDES",
                provenance="Synthesized into final research answer"
            ))

        trace = ScientificResearchTrace(
            snapshot_id=snapshot.snapshot_id,
            question_id=q_node_id,
            conclusion_id=concl_node_id,
            nodes=nodes,
            edges=edges,
            total_hops=len(edges),
            is_complete=True
        )

        self._traces[snapshot.snapshot_id] = trace
        logger.info(f"Built provenance trace for snapshot {snapshot.snapshot_id}: {len(nodes)} nodes, {len(edges)} edges")
        return trace

    def get_trace(self, snapshot_id: str) -> Optional[ScientificResearchTrace]:
        return self._traces.get(snapshot_id)

    def backward_trace(self, snapshot_id: str, start_node_id: str) -> List[TraceNode]:
        """
        Traverses upstream from a conclusion, claim, or result to discover all contributing
        sources, queries, screening decisions, data extractions, and original questions.
        """
        trace = self.get_trace(snapshot_id)
        if not trace:
            return []

        # Build reverse adjacency map: target_id -> list of source_ids
        rev_adj: Dict[str, List[str]] = {}
        node_map = {n.node_id: n for n in trace.nodes}

        for edge in trace.edges:
            rev_adj.setdefault(edge.target_id, []).append(edge.source_id)

        visited: Set[str] = set()
        queue = deque([start_node_id])
        result_nodes: List[TraceNode] = []

        while queue:
            curr = queue.popleft()
            if curr in visited:
                continue
            visited.add(curr)
            if curr in node_map:
                result_nodes.append(node_map[curr])

            for upstream in rev_adj.get(curr, []):
                if upstream not in visited:
                    queue.append(upstream)

        return result_nodes

    def forward_trace(self, snapshot_id: str, start_node_id: str) -> List[TraceNode]:
        """
        Traverses downstream from a modified or retracted source/study/extraction to identify
        all affected analyses, results, claims, reviews, and conclusions (impact analysis).
        """
        trace = self.get_trace(snapshot_id)
        if not trace:
            return []

        # Build forward adjacency map: source_id -> list of target_ids
        fwd_adj: Dict[str, List[str]] = {}
        node_map = {n.node_id: n for n in trace.nodes}

        for edge in trace.edges:
            fwd_adj.setdefault(edge.source_id, []).append(edge.target_id)

        visited: Set[str] = set()
        queue = deque([start_node_id])
        result_nodes: List[TraceNode] = []

        while queue:
            curr = queue.popleft()
            if curr in visited:
                continue
            visited.add(curr)
            if curr in node_map:
                result_nodes.append(node_map[curr])

            for downstream in fwd_adj.get(curr, []):
                if downstream not in visited:
                    queue.append(downstream)

        return result_nodes
