"""
ZMIE Continuous Knowledge Evolution Engine
Prompt 14 Implementation.

Executes cascade impact analysis across claims and knowledge graph edges
when new evidence, guideline updates, trial terminations, or retractions occur.
Maintains a prioritized revalidation queue, research gap and blindspot analysis,
and knowledge snapshot versioning.
"""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.models.research_network import (
    EvolutionImpactAnalysis,
    ResearchGapAnalysis,
    KnowledgeSnapshot,
)


class ContinuousKnowledgeEvolutionEngine:
    """
    Monitors global literature and research signals to continuously update
    and revalidate medical knowledge claims, graph edges, and research gaps.
    """

    def __init__(self, network_engine=None):
        self.network_engine = network_engine
        self._impact_history: List[EvolutionImpactAnalysis] = []
        self._revalidation_queue: List[Dict[str, Any]] = []
        self._snapshots: List[KnowledgeSnapshot] = []
        self._active_gaps: Dict[str, ResearchGapAnalysis] = {}

        # Mock claims registry for evolution simulation
        self._claims_registry: Dict[str, Dict[str, Any]] = {
            "claim_sglt2_hfp_01": {
                "claim_id": "claim_sglt2_hfp_01",
                "statement": "SGLT2 inhibitors significantly reduce cardiovascular death and heart failure hospitalization in HFpEF.",
                "status": "SUPPORTED",
                "confidence": 0.96,
                "evidence_sources": ["10.1056/NEJMoa2309811", "NCT05221199"],
                "last_revalidated": "2024-03-01",
            },
            "claim_khamira_endo_01": {
                "claim_id": "claim_khamira_endo_01",
                "statement": "Khamira Abresham Hakim Arshad Wala improves flow-mediated dilation and endothelial function in ischemic cardiac recovery.",
                "status": "VALIDATED",
                "confidence": 0.88,
                "evidence_sources": ["10.1016/j.jep.2024.118021", "CTRI/2022/07/044192"],
                "last_revalidated": "2024-03-15",
            },
            "claim_fictitious_molecule_z": {
                "claim_id": "claim_fictitious_molecule_z",
                "statement": "Compound Z-401 completely reverses established cardiac fibrosis within 4 weeks.",
                "status": "SUPPORTED",
                "confidence": 0.79,
                "evidence_sources": ["10.1016/j.fakecardio.2021.09912"],
                "last_revalidated": "2022-01-10",
            },
        }

        self._seed_initial_gaps()
        self._seed_initial_snapshots()

    def _seed_initial_gaps(self):
        """Seed representative multi-system medical research gaps."""
        gap_hfpef_ckd = ResearchGapAnalysis(
            gap_id="gap_hfpef_ckd_advanced",
            topic="SGLT2 Inhibitor Safety and Efficacy in Advanced CKD (eGFR < 20 mL/min/1.73m²)",
            gap_type="POPULATION_EXCLUSION",
            deficiency_description="Major phase 3 HFpEF trials excluded patients with severe end-stage renal failure, leaving a high-risk therapeutic blindspot.",
            missing_evidence_type="RANDOMIZED_CONTROLLED_TRIAL",
            affected_claims=["claim_sglt2_hfp_01"],
            priority_score=92.0,
            suggested_investigation="Targeted adaptive phase 3 pragmatic trial evaluating SGLT2i in dialysis and pre-dialysis eGFR < 20 cohorts.",
        )
        gap_unani_pk = ResearchGapAnalysis(
            gap_id="gap_unani_khamira_pharmacokinetics",
            topic="Pharmacokinetic & Active Metabolite Profiling of Khamira Polyherbal Fermentations",
            gap_type="TRADITIONAL_SYSTEM_UNDERINVESTIGATED",
            deficiency_description="While classical clinical efficacy in coronary health is documented, LC-MS/MS bioavailability and active sericin-metabolite dynamics remain unmapped in modern biomedical pharmacology.",
            missing_evidence_type="PHARMACOKINETIC_MECHANISTIC_STUDY",
            affected_claims=["claim_khamira_endo_01"],
            priority_score=85.0,
            suggested_investigation="High-resolution tandem mass spectrometry (UHPLC-Q-TOF-MS) tracking serum metabolites post oral administration in healthy and post-infarction human subjects.",
        )
        gap_tcm_herb_drug = ResearchGapAnalysis(
            gap_id="gap_tcm_herb_anticoagulant_interaction",
            topic="Herb-Drug Interactions between Danshen (Salvia miltiorrhiza) and Direct Oral Anticoagulants (DOACs)",
            gap_type="CONTRADICTION_UNRESOLVED",
            deficiency_description="Contradictory findings between in-vitro CYP inhibition assays and small retrospective observational studies regarding bleeding risk with Apixaban.",
            missing_evidence_type="PROSPECTIVE_DRUG_INTERACTION_STUDY",
            affected_claims=[],
            priority_score=88.5,
            suggested_investigation="Standardized pharmacokinetic crossover trial measuring DOAC peak/trough levels with co-administered Danshen extract.",
        )
        for g in [gap_hfpef_ckd, gap_unani_pk, gap_tcm_herb_drug]:
            self._active_gaps[g.gap_id] = g

    def _seed_initial_snapshots(self):
        """Seed baseline knowledge snapshots."""
        snap_v1 = KnowledgeSnapshot(
            snapshot_id="snap-evo-2023-q4",
            timestamp=datetime(2023, 12, 31, 23, 59, 59),
            version=1,
            claims_count=1240,
            supported_claims=1110,
            disputed_claims=98,
            retracted_claims=32,
            active_gaps_count=45,
            frontier_signals_count=12,
            notes="Baseline 2023 Q4 Global Medical Knowledge Freeze.",
        )
        snap_v2 = KnowledgeSnapshot(
            snapshot_id="snap-evo-2024-q1",
            timestamp=datetime(2024, 3, 31, 23, 59, 59),
            version=2,
            claims_count=1320,
            supported_claims=1180,
            disputed_claims=102,
            retracted_claims=38,
            active_gaps_count=48,
            frontier_signals_count=15,
            notes="2024 Q1 Continuous Knowledge Evolution Update.",
        )
        self._snapshots.extend([snap_v1, snap_v2])

    # -------------------------------------------------------------
    # Cascade Impact Analysis
    # -------------------------------------------------------------

    def trigger_cascade_impact(
        self,
        trigger_type: str,
        trigger_source_id: str,
        reason: str = "Automated continuous surveillance trigger"
    ) -> EvolutionImpactAnalysis:
        """
        Executes cascade impact analysis across dependent claims,
        evidence graph edges, and active projects when a trigger occurs.
        """
        affected_claims: List[str] = []
        prev_states: Dict[str, str] = {}
        new_states: Dict[str, str] = {}
        graph_changes: List[Dict[str, Any]] = []
        alerts: List[Dict[str, Any]] = []
        severity = "HIGH"

        if trigger_type.upper() == "RETRACTION":
            severity = "CRITICAL"
            # Find all claims citing this retracted source
            for cid, cdata in self._claims_registry.items():
                if trigger_source_id in cdata.get("evidence_sources", []):
                    affected_claims.append(cid)
                    prev_states[cid] = cdata["status"]
                    cdata["status"] = "RETRACTED"
                    cdata["confidence"] = 0.05
                    new_states[cid] = "RETRACTED"

                    graph_changes.append({
                        "entity_type": "CLAIM",
                        "id": cid,
                        "field": "status",
                        "old_value": prev_states[cid],
                        "new_value": "RETRACTED",
                        "reason": f"Downstream dependency on retracted publication: {trigger_source_id}"
                    })

                    alerts.append({
                        "alert_id": f"alt-retract-{uuid.uuid4().hex[:6]}",
                        "level": "CRITICAL",
                        "claim_id": cid,
                        "message": f"EMERGENCY RETRACTION CASCADE: Claim '{cdata['statement']}' has been invalidated due to formal retraction of underlying source {trigger_source_id}. Clinical recommendations referencing this claim must be immediately withheld.",
                        "timestamp": datetime.utcnow().isoformat()
                    })

        elif trigger_type.upper() == "NEW_STUDY":
            severity = "MEDIUM"
            # Simulate reinforcement of supported claim or conflict resolution
            for cid, cdata in self._claims_registry.items():
                if trigger_source_id in cdata.get("evidence_sources", []):
                    affected_claims.append(cid)
                    prev_states[cid] = cdata["status"]
                    if cdata["status"] in ["PRELIMINARY", "PROVISIONAL"]:
                        cdata["status"] = "SUPPORTED"
                        new_states[cid] = "SUPPORTED"
                    else:
                        new_states[cid] = cdata["status"]

                    graph_changes.append({
                        "entity_type": "CLAIM",
                        "id": cid,
                        "field": "evidence_depth",
                        "old_value": "PROVISIONAL",
                        "new_value": "REINFORCED",
                        "reason": f"New confirmatory landmark study linked: {trigger_source_id}"
                    })

        elif trigger_type.upper() == "GUIDELINE_CHANGE":
            severity = "HIGH"
            # Guideline revision triggers review of clinical practice claims
            affected_claims = list(self._claims_registry.keys())[:2]
            for cid in affected_claims:
                prev_states[cid] = self._claims_registry[cid]["status"]
                new_states[cid] = "UPDATED_GUIDELINE_ALIGNED"
            alerts.append({
                "alert_id": f"alt-guide-{uuid.uuid4().hex[:6]}",
                "level": "HIGH",
                "message": f"Clinical guideline change from {trigger_source_id} reconciled across standard of care claims.",
                "timestamp": datetime.utcnow().isoformat()
            })

        summary = (
            f"Cascade impact executed for trigger [{trigger_type}] from source '{trigger_source_id}'. "
            f"Impacted {len(affected_claims)} claims. Dispatched {len(alerts)} alerts. Severity: {severity}."
        )

        impact_analysis = EvolutionImpactAnalysis(
            trigger_type=trigger_type,
            trigger_source_id=trigger_source_id,
            affected_claim_ids=affected_claims,
            previous_claim_states=prev_states,
            new_claim_states=new_states,
            evidence_graph_changes=graph_changes,
            severity_level=severity,
            alerts_dispatched=alerts,
            revalidation_timestamp=datetime.utcnow(),
            summary=summary,
        )

        self._impact_history.append(impact_analysis)
        return impact_analysis

    # -------------------------------------------------------------
    # Revalidation Queue
    # -------------------------------------------------------------

    def enqueue_revalidation(self, item_id: str, item_type: str, priority: str, rationale: str) -> Dict[str, Any]:
        """Enqueues an item (claim, relation, study) for prioritized revalidation."""
        job = {
            "queue_id": f"q-{uuid.uuid4().hex[:8]}",
            "item_id": item_id,
            "item_type": item_type,
            "priority": priority.upper(),  # CRITICAL, HIGH, MEDIUM, LOW
            "rationale": rationale,
            "enqueued_at": datetime.utcnow().isoformat(),
            "status": "PENDING"
        }
        self._revalidation_queue.append(job)
        return job

    def process_revalidation_queue(self, max_items: int = 10) -> Dict[str, Any]:
        """Processes pending revalidations sorted by priority."""
        priority_weights = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        self._revalidation_queue.sort(
            key=lambda x: priority_weights.get(x["priority"], 0),
            reverse=True
        )

        processed = []
        remaining = []

        for idx, item in enumerate(self._revalidation_queue):
            if idx < max_items and item["status"] == "PENDING":
                item["status"] = "COMPLETED"
                item["processed_at"] = datetime.utcnow().isoformat()
                processed.append(item)
            else:
                remaining.append(item)

        self._revalidation_queue = remaining
        return {
            "processed_count": len(processed),
            "processed_items": processed,
            "remaining_queue_length": len(self._revalidation_queue)
        }

    # -------------------------------------------------------------
    # Research Gap & "What Am I Missing?" Engine
    # -------------------------------------------------------------

    def analyze_research_gaps(self, topic: Optional[str] = None) -> List[ResearchGapAnalysis]:
        """Identifies systemic research blindspots and gaps."""
        if not topic:
            return list(self._active_gaps.values())

        topic_clean = topic.lower()
        matched_gaps = []
        for g in self._active_gaps.values():
            if (
                topic_clean in g.topic.lower()
                or topic_clean in g.deficiency_description.lower()
                or any(topic_clean in c.lower() for c in g.affected_claims)
            ):
                matched_gaps.append(g)

        return matched_gaps

    def add_research_gap(self, gap: ResearchGapAnalysis):
        self._active_gaps[gap.gap_id] = gap

    # -------------------------------------------------------------
    # Knowledge Snapshot & Versioning
    # -------------------------------------------------------------

    def create_snapshot(self, notes: str = "") -> KnowledgeSnapshot:
        """Captures an atomic snapshot of current medical knowledge states."""
        total_claims = len(self._claims_registry)
        supported = sum(1 for c in self._claims_registry.values() if c["status"] in ["SUPPORTED", "VALIDATED"])
        disputed = sum(1 for c in self._claims_registry.values() if c["status"] == "DISPUTED")
        retracted = sum(1 for c in self._claims_registry.values() if c["status"] == "RETRACTED")

        new_version = len(self._snapshots) + 1
        snapshot = KnowledgeSnapshot(
            snapshot_id=f"snap-evo-v{new_version}-{uuid.uuid4().hex[:6]}",
            timestamp=datetime.utcnow(),
            version=new_version,
            claims_count=total_claims,
            supported_claims=supported,
            disputed_claims=disputed,
            retracted_claims=retracted,
            active_gaps_count=len(self._active_gaps),
            frontier_signals_count=len(self.network_engine.get_frontier_signals()) if self.network_engine else 0,
            notes=notes or f"Continuous evolution snapshot v{new_version}",
        )
        self._snapshots.append(snapshot)
        return snapshot

    def get_snapshots(self) -> List[KnowledgeSnapshot]:
        return self._snapshots

    def compute_snapshot_diff(self, snap_id_a: str, snap_id_b: str) -> Dict[str, Any]:
        """Computes differential metrics between two knowledge snapshots."""
        snap_a = next((s for s in self._snapshots if s.snapshot_id == snap_id_a), None)
        snap_b = next((s for s in self._snapshots if s.snapshot_id == snap_id_b), None)

        if not snap_a or not snap_b:
            return {"error": "One or both snapshot IDs not found."}

        return {
            "snapshot_a": snap_a.snapshot_id,
            "snapshot_b": snap_b.snapshot_id,
            "version_a": snap_a.version,
            "version_b": snap_b.version,
            "claims_growth": snap_b.claims_count - snap_a.claims_count,
            "supported_claims_diff": snap_b.supported_claims - snap_a.supported_claims,
            "retracted_claims_diff": snap_b.retracted_claims - snap_a.retracted_claims,
            "disputed_claims_diff": snap_b.disputed_claims - snap_a.disputed_claims,
            "gaps_delta": snap_b.active_gaps_count - snap_a.active_gaps_count,
            "frontier_delta": snap_b.frontier_signals_count - snap_a.frontier_signals_count,
            "summary": (
                f"Evolution Diff (v{snap_a.version} -> v{snap_b.version}): "
                f"Total Claims: {snap_b.claims_count - snap_a.claims_count:+d}, "
                f"Retractions: {snap_b.retracted_claims - snap_a.retracted_claims:+d}, "
                f"Active Gaps: {snap_b.active_gaps_count - snap_a.active_gaps_count:+d}."
            )
        }
