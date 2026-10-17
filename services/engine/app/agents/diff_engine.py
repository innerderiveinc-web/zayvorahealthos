"""
ZMIE Knowledge Versioning & Living Audit Diff Engine
Implements Blueprint Points 21, 22, and 33:
- "What changed?" monitor for tracked topics and saved clinical searches
- Git-like knowledge commits for evolving medical evidence
- Stores: who, what, why, source, previous evidence grade, new evidence grade, reviewer, timestamp
- Alerts clinicians/researchers when an RCT updates, a trial fails, or a study is retracted.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ChangeType(str, Enum):
    NEW_RCT_INDEXED = "new_rct_indexed"
    META_ANALYSIS_UPDATED = "meta_analysis_updated"
    GUIDELINE_SUPERSEDED = "guideline_superseded"
    SAFETY_ALERT_ISSUED = "safety_alert_issued"
    STUDY_RETRACTED = "study_retracted"
    CONTRADICTION_DETECTED = "new_contradiction_detected"
    MAPPING_REVISED = "cross_system_mapping_revised"


class KnowledgeCommit(BaseModel):
    commit_id: str
    topic_or_concept: str
    change_type: ChangeType
    previous_state_summary: str
    new_state_summary: str
    evidence_delta_description: str
    triggering_source_id: str
    triggering_document_doi: Optional[str] = None
    reviewer_or_curator: str
    committed_at: datetime = Field(default_factory=datetime.utcnow)


class KnowledgeDiffEngine:
    """
    Maintains living scientific memory and detects clinical changes over time.
    """

    _KNOWLEDGE_HISTORY: List[KnowledgeCommit] = [
        KnowledgeCommit(
            commit_id="KCMT-2026-001",
            topic_or_concept="Berberine Metabolic Health",
            change_type=ChangeType.NEW_RCT_INDEXED,
            previous_state_summary="27 human RCTs evaluating glucose lowering.",
            new_state_summary="28 human RCTs indexed (+1 multi-center trial with continuous glucose monitoring).",
            evidence_delta_description="New trial confirms 1.2% HbA1c reduction in Asian diabetic cohort without hepatic elevation.",
            triggering_source_id="SRC-PUBMED-NLM",
            triggering_document_doi="10.1016/j.metabol.2025.04.012",
            reviewer_or_curator="ZMIE-Automated-Evidence-Monitor"
        ),
        KnowledgeCommit(
            commit_id="KCMT-2026-002",
            topic_or_concept="Metabolic Micro-RNA Pathways",
            change_type=ChangeType.STUDY_RETRACTED,
            previous_state_summary="Paper 10.1016/j.metabol.fake.2021 cited as preclinical evidence.",
            new_state_summary="Paper retracted by publisher due to western blot manipulation. Dependent claims set to zero.",
            evidence_delta_description="Removed 1 unverified in-vitro claim from the metabolic knowledge graph.",
            triggering_source_id="SRC-CROSSREF-RETRACTION-WATCH",
            triggering_document_doi="10.1016/j.metabol.fake.2021",
            reviewer_or_curator="DR-CHOUDHARY-PHARMA-REVIEWER"
        )
    ]

    @classmethod
    def get_topic_timeline(cls, topic: str) -> List[KnowledgeCommit]:
        topic_clean = topic.strip().lower()
        return [c for c in cls._KNOWLEDGE_HISTORY if topic_clean in c.topic_or_concept.lower()]

    @classmethod
    def get_latest_changes(cls, limit: int = 10) -> List[KnowledgeCommit]:
        return sorted(cls._KNOWLEDGE_HISTORY, key=lambda x: x.committed_at, reverse=True)[:limit]

    @classmethod
    def commit_knowledge_change(
        cls,
        topic: str,
        change_type: ChangeType,
        prev_summary: str,
        new_summary: str,
        delta: str,
        source_id: str,
        reviewer: str,
        doi: Optional[str] = None
    ) -> KnowledgeCommit:
        commit = KnowledgeCommit(
            commit_id=f"KCMT-2026-{len(cls._KNOWLEDGE_HISTORY)+1:03d}",
            topic_or_concept=topic,
            change_type=change_type,
            previous_state_summary=prev_summary,
            new_state_summary=new_summary,
            evidence_delta_description=delta,
            triggering_source_id=source_id,
            triggering_document_doi=doi,
            reviewer_or_curator=reviewer
        )
        cls._KNOWLEDGE_HISTORY.append(commit)
        return commit
