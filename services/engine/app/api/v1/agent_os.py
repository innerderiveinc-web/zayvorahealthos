"""
ZMIE Scientific Agent Operating System REST API Gateway (Prompt 24)
Endpoints for agent registry, task dispatch, research planning,
DAG orchestration, tool catalog, review gates, and observability.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Header, Query, status
from pydantic import BaseModel, Field

from app.agent_os import (
    get_agent_os,
    AgentDefinition,
    AgentTask,
    AgentResult,
    ResearchPlan,
    ResearchExecutionTrace,
    ToolDefinition,
    ReviewRequest,
    ReviewDecision,
    ReviewDecisionAction,
    KnowledgeChangeProposal,
    AgentIncident,
    AgentMetrics,
    TaskExecutionState
)
from app.models.federated_privacy import AgentContext, AgentMode, ResearchDataClassification

router = APIRouter(tags=["Agent Operating System"])


# ==============================================================================
# Request / Response Schemas
# ==============================================================================

class CreateTaskRequest(BaseModel):
    agent_id: str
    goal: str
    inputs: Dict[str, Any] = Field(default_factory=dict)
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None


class PlanResearchRequest(BaseModel):
    question: str
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None


class RunResearchRequest(BaseModel):
    question: str
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None
    simulate_failure_subtask_id: Optional[str] = None


class ReviewDecisionRequest(BaseModel):
    reviewer_user_id: str
    reviewer_role: str = "SCIENTIFIC_GOVERNANCE"
    rationale: str


# ==============================================================================
# 1. Agent Registry Endpoints (Clause 7, 254)
# ==============================================================================

@router.post("/agents", response_model=AgentDefinition, status_code=status.HTTP_201_CREATED)
def register_agent(agent: AgentDefinition):
    os = get_agent_os()
    os.agents._agents[agent.agent_id] = agent
    return agent


@router.get("/agents", response_model=List[AgentDefinition])
def list_agents():
    os = get_agent_os()
    return os.agents.list_agents()


@router.get("/agents/{id}", response_model=AgentDefinition)
def get_agent(id: str):
    os = get_agent_os()
    agent = os.agents.get_agent_definition(id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{id}' not found.")
    return agent


# ==============================================================================
# 2. Agent Tasks & Dispatch Endpoints (Clause 12, 254)
# ==============================================================================

@router.post("/agent-tasks", response_model=AgentResult)
async def create_and_run_task(
    req: CreateTaskRequest,
    x_tenant_id: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header("system")
):
    os = get_agent_os()
    tenant_id = req.tenant_id or x_tenant_id
    inst = os.agents.get_agent_instance(req.agent_id)
    if not inst:
        raise HTTPException(status_code=404, detail=f"Specialist agent '{req.agent_id}' not found.")

    task = AgentTask(
        agent_id=req.agent_id,
        goal=req.goal,
        inputs=req.inputs,
        tenant_id=tenant_id,
        project_id=req.project_id,
        user_id=x_user_id
    )

    ctx = AgentContext(
        agent_id=req.agent_id,
        mode=AgentMode.TENANT_MODE if tenant_id else AgentMode.PUBLIC_MODE,
        tenant_id=tenant_id,
        project_id=req.project_id,
        acting_for_user_id=x_user_id
    )

    result = await inst.execute(task, context=ctx)
    return result


@router.get("/agent-tasks/{id}")
def get_task_status(id: str):
    os = get_agent_os()
    # Check trace events for task
    for trace in os.trace_service.list_traces():
        for evt in trace.events:
            if evt.task_id == id:
                return {
                    "task_id": id,
                    "event": evt.event_type,
                    "details": evt.details,
                    "timestamp": evt.timestamp
                }
    return {"task_id": id, "status": "UNKNOWN_OR_COMPLETED"}


@router.post("/agent-tasks/{id}/cancel")
def cancel_task(id: str, x_user_id: Optional[str] = Header("system")):
    return {
        "task_id": id,
        "status": TaskExecutionState.CANCELLED.value,
        "cancelled_by": x_user_id,
        "timestamp": "2026-10-04T00:00:00Z"
    }


# ==============================================================================
# 3. Research Planning & DAG Orchestration (Clause 18, 254)
# ==============================================================================

@router.post("/research/plan", response_model=ResearchPlan)
def plan_research(
    req: PlanResearchRequest,
    x_tenant_id: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header("system")
):
    os = get_agent_os()
    tenant_id = req.tenant_id or x_tenant_id
    return os.planner.create_plan(
        question=req.question,
        tenant_id=tenant_id,
        project_id=req.project_id,
        user_id=x_user_id
    )


@router.post("/research/run")
async def run_research(
    req: RunResearchRequest,
    x_tenant_id: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header("system")
):
    os = get_agent_os()
    tenant_id = req.tenant_id or x_tenant_id

    ctx = AgentContext(
        agent_id="agent-orchestrator",
        mode=AgentMode.TENANT_MODE if tenant_id else AgentMode.PUBLIC_MODE,
        tenant_id=tenant_id,
        project_id=req.project_id,
        acting_for_user_id=x_user_id
    )

    trace, result = await os.orchestrator.execute_research(
        question=req.question,
        tenant_id=tenant_id,
        project_id=req.project_id,
        user_id=x_user_id,
        context=ctx,
        simulate_failure_subtask_id=req.simulate_failure_subtask_id
    )

    return {
        "trace_id": trace.trace_id,
        "question": trace.question,
        "status": "COMPLETED" if not trace.completion.is_partial else "PARTIAL",
        "coverage": trace.completion.coverage_score,
        "is_partial": trace.completion.is_partial,
        "agents_executed": trace.agents_executed,
        "tools_used": trace.tools_used,
        "result": result
    }


@router.get("/research/runs/{id}")
def get_research_run(id: str):
    os = get_agent_os()
    trace = os.trace_service.get_trace(id)
    if not trace:
        raise HTTPException(status_code=404, detail=f"Research run '{id}' not found.")
    return trace


@router.get("/agent-runs/{id}")
def get_agent_run(id: str):
    os = get_agent_os()
    trace = os.trace_service.get_trace(id)
    if not trace:
        raise HTTPException(status_code=404, detail=f"Agent run '{id}' not found.")
    return trace


@router.get("/agent-runs/{id}/trace")
def get_agent_run_trace(id: str):
    os = get_agent_os()
    trace = os.trace_service.get_trace(id)
    if not trace:
        raise HTTPException(status_code=404, detail=f"Trace for run '{id}' not found.")
    return {
        "trace_id": trace.trace_id,
        "plan_id": trace.plan_id,
        "events": trace.events,
        "completion": trace.completion
    }


# ==============================================================================
# 4. Tool Registry & Governance Policies (Clause 75, 254)
# ==============================================================================

@router.get("/agent-tools", response_model=List[ToolDefinition])
def list_agent_tools():
    os = get_agent_os()
    return os.tools.list_tools()


@router.get("/agent-policies")
def list_agent_policies():
    return {
        "version": "2026.1",
        "doctrine": "Agents discover and reason. Tools execute. Evidence constrains. Verifiers challenge. Policies govern. Humans remain accountable.",
        "epistemic_firewall": "ACTIVE",
        "zero_fabrication_gate": "ENFORCED",
        "tenant_isolation": "HARD_BOUNDARY",
        "separation_of_duties": "ENFORCED",
        "uncontrolled_autonomy": "PROHIBITED"
    }


# ==============================================================================
# 5. Human Review Gates & Governance (Clause 109-112, 254)
# ==============================================================================

@router.post("/reviews", response_model=ReviewRequest, status_code=status.HTTP_201_CREATED)
def submit_review(req: ReviewRequest):
    os = get_agent_os()
    return os.review_gate.submit_review_request(
        task_id=req.task_id,
        triggering_agent_id=req.triggering_agent_id,
        reason=req.reason,
        recommendation=req.recommendation,
        tenant_id=req.tenant_id,
        project_id=req.project_id,
        risks=req.risks,
        uncertainties=req.uncertainties
    )


@router.post("/reviews/{id}/approve", response_model=ReviewDecision)
def approve_review(id: str, req: ReviewDecisionRequest):
    os = get_agent_os()
    return os.review_gate.decide_review(
        review_id=id,
        reviewer_user_id=req.reviewer_user_id,
        reviewer_role=req.reviewer_role,
        action=ReviewDecisionAction.APPROVE,
        rationale=req.rationale
    )


@router.post("/reviews/{id}/reject", response_model=ReviewDecision)
def reject_review(id: str, req: ReviewDecisionRequest):
    os = get_agent_os()
    return os.review_gate.decide_review(
        review_id=id,
        reviewer_user_id=req.reviewer_user_id,
        reviewer_role=req.reviewer_role,
        action=ReviewDecisionAction.REJECT,
        rationale=req.rationale
    )


# ==============================================================================
# 6. Observability, Incidents & Proposals (Clause 106, 211, 220, 254)
# ==============================================================================

@router.get("/agent-incidents", response_model=List[AgentIncident])
def list_incidents():
    os = get_agent_os()
    return os.orchestrator.list_incidents()


@router.get("/agent-metrics", response_model=List[AgentMetrics])
def list_agent_metrics(agent_id: Optional[str] = Query(None)):
    os = get_agent_os()
    return os.agents.get_metrics(agent_id=agent_id)


@router.post("/agent-os/proposals", response_model=KnowledgeChangeProposal, status_code=status.HTTP_201_CREATED)
def submit_proposal(prop: KnowledgeChangeProposal):
    os = get_agent_os()
    return os.review_gate.submit_knowledge_proposal(prop)


@router.get("/agent-os/proposals", response_model=List[KnowledgeChangeProposal])
def list_proposals():
    os = get_agent_os()
    return os.review_gate.list_proposals()
