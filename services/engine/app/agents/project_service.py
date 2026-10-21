"""
ZMIE Research Project Workspace Manager & Memory (Sections 24, 33 & 34)
Maintains persistent research project objects:
- queries, inclusion/exclusion criteria, notes, evidence tables, snapshots
- allows "What changed since my last review?" comparison
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ResearchNote(BaseModel):
    note_id: str
    author: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ResearchProject(BaseModel):
    project_id: str
    owner_id: str
    org_id: str
    title: str
    research_question: str
    search_history: List[str] = Field(default_factory=list)
    included_studies: List[Dict[str, Any]] = Field(default_factory=list)
    excluded_studies: List[Dict[str, Any]] = Field(default_factory=list)
    notes: List[ResearchNote] = Field(default_factory=list)
    reports: List[Dict[str, Any]] = Field(default_factory=list)
    last_snapshot_date: str = "2026-10-03"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProjectWorkspaceService:
    _PROJECTS: Dict[str, ResearchProject] = {
        "PROJ-METABOLIC-01": ResearchProject(
            project_id="PROJ-METABOLIC-01",
            owner_id="usr-res-lead-01",
            org_id="org-aiims-delhi",
            title="Berberine vs Metformin Longitudinal Evaluation",
            research_question="Evaluate comparative glycemic efficacy and hepatic safety in Asian cohorts",
            search_history=["Berberine clinical trials", "Metformin comparative RCTs"],
            included_studies=[
                {"study_id": "PMID:18442638", "title": "Efficacy of Berberine in Patients with T2D", "year": 2008}
            ],
            excluded_studies=[
                {"study_id": "PMID:FAKE-2021", "reason": "Retracted due to image manipulation"}
            ],
            notes=[
                ResearchNote(note_id="N-01", author="Dr. Ashraf", content="Focus on 12-week HbA1c reductions and GI tolerability.")
            ]
        )
    }

    @classmethod
    def list_projects(
        cls,
        owner_id: Optional[str] = None,
        org_id: Optional[str] = None,
        is_admin: bool = False
    ) -> List[ResearchProject]:
        if is_admin:
            return list(cls._PROJECTS.values())
        results = []
        for p in cls._PROJECTS.values():
            if org_id and p.org_id == org_id:
                results.append(p)
            elif owner_id and p.owner_id == owner_id:
                results.append(p)
        return results

    @classmethod
    def get_project(cls, project_id: str) -> Optional[ResearchProject]:
        return cls._PROJECTS.get(project_id)

    @classmethod
    def create_project(cls, owner_id: str, org_id: str, title: str, question: str) -> ResearchProject:
        pid = f"PROJ-{int(datetime.utcnow().timestamp())}"
        proj = ResearchProject(
            project_id=pid,
            owner_id=owner_id,
            org_id=org_id,
            title=title,
            research_question=question
        )
        cls._PROJECTS[pid] = proj
        return proj

    @classmethod
    def add_note(cls, project_id: str, author: str, content: str) -> Optional[ResearchProject]:
        proj = cls._PROJECTS.get(project_id)
        if proj:
            note = ResearchNote(note_id=f"N-{len(proj.notes)+1}", author=author, content=content)
            proj.notes.append(note)
            proj.updated_at = datetime.utcnow()
            return proj
        return None
