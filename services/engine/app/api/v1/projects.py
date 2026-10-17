"""
ZMIE Research Projects API Router (Sections 24, 33 & 34)
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel

from app.agents.project_service import ProjectWorkspaceService, ResearchProject
from app.core.security import SecurityService, AuthContext, UserRole

router = APIRouter(prefix="/projects", tags=["Research Projects Workspace (Sec 24, 33, 34)"])


class CreateProjectPayload(BaseModel):
    title: str
    research_question: str


class AddNotePayload(BaseModel):
    content: str


@router.get("", response_model=List[ResearchProject])
async def list_user_projects(auth: AuthContext = Depends(SecurityService.get_current_user)):
    """
    Lists research projects belonging to current user/organization.
    """
    return ProjectWorkspaceService.list_projects()


@router.post("", response_model=ResearchProject)
async def create_research_project(
    payload: CreateProjectPayload,
    auth: AuthContext = Depends(SecurityService.require_role([UserRole.RESEARCHER, UserRole.CLINICIAN, UserRole.ADMIN]))
):
    """
    Creates a new isolated research project workspace.
    """
    return ProjectWorkspaceService.create_project(
        owner_id=auth.user_id,
        org_id=auth.org_id,
        title=payload.title,
        question=payload.research_question
    )


@router.get("/{project_id}", response_model=ResearchProject)
async def get_project_details(project_id: str):
    """
    Retrieves full project memory: included studies, excluded reasons, notes, and snapshots.
    """
    proj = ProjectWorkspaceService.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


@router.post("/{project_id}/notes", response_model=ResearchProject)
async def add_project_note(
    project_id: str,
    payload: AddNotePayload,
    auth: AuthContext = Depends(SecurityService.get_current_user)
):
    """
    Appends a timestamped research note to the project workspace.
    """
    proj = ProjectWorkspaceService.add_note(
        project_id=project_id,
        author=auth.user_id,
        content=payload.content
    )
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj
