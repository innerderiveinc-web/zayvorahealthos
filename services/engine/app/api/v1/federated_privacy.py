"""
ZMIE Federated & Private Research Intelligence API (Prompt 23).

Identity: in production, tenant/user are resolved from a verified token by the gateway.
In this reference build they are read from X-Tenant-ID / X-User-ID / X-Project-ID / X-Purpose
headers, and the server-side policy engine is authoritative for every decision.

Denials return non-sensitive, actionable reasons; cross-tenant probes receive 404
("not found in your authorized scope") so resource existence is not revealed.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from app.models.federated_privacy import (
    RequestContext,
    ResearchDataClassification,
    FederatedQueryRequest,
    PolicyDecision,
)
from app.federated_privacy.engine import (
    FederatedPrivacyEngine,
    AccessDenied,
    ReleaseGovernanceBlocked,
    AIContextFirewallViolation,
    RetentionHoldActive,
    GovernanceError,
)

router = APIRouter(tags=["Federated & Private Research Intelligence"])
_engine = FederatedPrivacyEngine()

_NOT_FOUND_RULES = {"TENANT_ISOLATION", "NOT_FOUND", "UNKNOWN_PROJECT"}


def get_engine() -> FederatedPrivacyEngine:
    return _engine


def get_ctx(
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    x_project_id: Optional[str] = Header(None, alias="X-Project-ID"),
    x_purpose: Optional[str] = Header(None, alias="X-Purpose"),
) -> RequestContext:
    return RequestContext(tenant_id=x_tenant_id, user_id=x_user_id, project_id=x_project_id, purpose=x_purpose)


def _run(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except AccessDenied as e:
        code = 404 if e.evaluation.matched_rule in _NOT_FOUND_RULES else 403
        raise HTTPException(status_code=code, detail=e.evaluation.user_facing_reason)
    except AIContextFirewallViolation as e:
        raise HTTPException(status_code=403, detail=str(e))
    except (ReleaseGovernanceBlocked, RetentionHoldActive, GovernanceError) as e:
        raise HTTPException(status_code=409, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="Resource not found in your authorized scope")


def _require_auth(ctx: RequestContext) -> None:
    if not ctx.tenant_id or not ctx.user_id:
        raise HTTPException(status_code=401, detail="Authentication required")


# ---------------------------------------------------------------- schemas

class SearchScope(BaseModel):
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None


class PrivateSearchRequest(BaseModel):
    query: str
    scope: SearchScope = Field(default_factory=SearchScope)


class ResolveRequest(BaseModel):
    term: str


class AnalysisRequest(BaseModel):
    title: str
    public_ids: List[str] = Field(default_factory=list)
    private_ids: List[str] = Field(default_factory=list)
    analysis: str = ""


class AIContextRequest(BaseModel):
    object_ids: List[str]
    model_id: Optional[str] = None


class PolicySimRequest(BaseModel):
    resource_id: str
    operation: str = "READ"
    destination: Optional[str] = None


class AccessRequestBody(BaseModel):
    project_id: str
    resource_id: str
    purpose: str
    duration_days: int = 30
    operations: List[str] = Field(default_factory=lambda: ["READ"])


class AccessDecisionBody(BaseModel):
    request_id: str
    approve: bool = True


class SharingRequestBody(BaseModel):
    partner_tenant_id: str
    purpose: str
    allowed_operations: List[str]
    shared_project_id: Optional[str] = None
    dataset_ids: List[str] = Field(default_factory=list)


class SharingApproveBody(BaseModel):
    agreement_id: str


class ReleaseRequestBody(BaseModel):
    object_id: str
    license: str = "CC-BY-4.0"


class ReleaseReviewBody(BaseModel):
    candidate_id: str
    review_type: str
    approved: bool = True
    notes: str = ""


class ReleaseExecuteBody(BaseModel):
    candidate_id: str


class FederatedQueryBody(BaseModel):
    query_type: str = "AGGREGATE_COHORT"
    sites: List[str]
    cohort_criteria: Dict[str, Any] = Field(default_factory=dict)
    allowed_output: str = "AGGREGATE_ONLY"
    min_cell_size: int = 10
    enable_differential_privacy: bool = False
    epsilon: float = 1.0


class ExportBody(BaseModel):
    destination: str
    recipient: str


# ---------------------------------------------------------------- private

@router.get("/private/datasets")
def list_private_datasets(ctx: RequestContext = Depends(get_ctx), eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    out = []
    for d in eng.datasets.values():
        if d.deletion_status == "ACTIVE" and eng.authorize(ctx, d.dataset_id, "READ", audit=False).decision == PolicyDecision.ALLOW:
            out.append({"dataset_id": d.dataset_id, "name": d.name, "project_id": d.project_id,
                        "classification": d.classification.value, "label": "PRIVATE"})
    return {"datasets": out, "classification": "PRIVATE"}


@router.get("/private/documents")
def list_private_documents(ctx: RequestContext = Depends(get_ctx), eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    out = [{"document_id": d.document_id, "title": d.title, "project_id": d.project_id,
            "classification": d.classification.value, "citation": f"[{d.internal_citation_tag}]", "label": "PRIVATE"}
           for d in eng.documents.values()
           if d.deletion_status == "ACTIVE" and eng.authorize(ctx, d.document_id, "READ", audit=False).decision == PolicyDecision.ALLOW]
    return {"documents": out, "classification": "PRIVATE"}


@router.get("/private/knowledge")
def list_private_knowledge(ctx: RequestContext = Depends(get_ctx), eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    claims = [{"claim_id": c.claim_id, "statement": c.statement, "claim_state": c.claim_state,
               "knowledge_class": c.knowledge_class.value, "label": "PRIVATE CLAIM (not globally validated)"}
              for c in eng.claims.values()
              if not c.is_publicly_released and eng.authorize(ctx, c.claim_id, "READ", audit=False).decision == PolicyDecision.ALLOW]
    return {"claims": claims, "graph": eng.graph_query(ctx, "")["private_nodes"], "classification": "PRIVATE"}


@router.post("/private/search")
def private_search(body: PrivateSearchRequest, ctx: RequestContext = Depends(get_ctx),
                   eng: FederatedPrivacyEngine = Depends(get_engine)):
    # Scope in the body can only NARROW the authenticated context, never widen it.
    if body.scope.tenant_id and body.scope.tenant_id != ctx.tenant_id:
        raise HTTPException(status_code=404, detail="Resource not found in your authorized scope")
    if body.scope.project_id:
        ctx = ctx.model_copy(update={"project_id": body.scope.project_id})
    return eng.search(ctx if ctx.tenant_id else None, body.query)


@router.post("/private/resolve")
def private_resolve(body: ResolveRequest, ctx: RequestContext = Depends(get_ctx),
                    eng: FederatedPrivacyEngine = Depends(get_engine)):
    return eng.resolve_term(ctx if ctx.tenant_id else None, body.term)


@router.post("/private/analysis")
def private_analysis(body: AnalysisRequest, ctx: RequestContext = Depends(get_ctx),
                     eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    rep = _run(eng.generate_report, ctx, body.title, body.public_ids, body.private_ids, body.analysis)
    return rep.model_dump()


@router.post("/private/reports/{report_id}/export")
def export_private_report(report_id: str, body: ExportBody, ctx: RequestContext = Depends(get_ctx),
                          eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    return _run(eng.export_report, ctx, report_id, body.destination, body.recipient)


@router.post("/private/ai-context")
def private_ai_context(body: AIContextRequest, ctx: RequestContext = Depends(get_ctx),
                       eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    model_id = body.model_id or eng.route_model(ctx, ResearchDataClassification.CONFIDENTIAL)["model_id"]
    return _run(eng.prepare_ai_context, ctx, body.object_ids, model_id)


# ---------------------------------------------------------------- policy / access

@router.post("/policy/simulate")
def policy_simulate(body: PolicySimRequest, ctx: RequestContext = Depends(get_ctx),
                    eng: FederatedPrivacyEngine = Depends(get_engine)):
    return eng.simulate_policy(ctx, body.resource_id, body.operation, body.destination)


@router.post("/access/request")
def access_request(body: AccessRequestBody, ctx: RequestContext = Depends(get_ctx),
                   eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    return _run(eng.request_access, ctx, body.project_id, body.resource_id, body.purpose,
                body.duration_days, body.operations).model_dump()


@router.post("/access/decide")
def access_decide(body: AccessDecisionBody, ctx: RequestContext = Depends(get_ctx),
                  eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    return _run(eng.decide_access, ctx, body.request_id, body.approve).model_dump()


# ---------------------------------------------------------------- sharing / release

@router.post("/sharing/request")
def sharing_request(body: SharingRequestBody, ctx: RequestContext = Depends(get_ctx),
                    eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    return _run(eng.propose_sharing_agreement, ctx, body.partner_tenant_id, body.purpose, body.allowed_operations,
                body.shared_project_id, body.dataset_ids).model_dump()


@router.post("/sharing/approve")
def sharing_approve(body: SharingApproveBody, ctx: RequestContext = Depends(get_ctx),
                    eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    return _run(eng.approve_sharing_agreement, ctx, body.agreement_id).model_dump()


@router.post("/release/request")
def release_request(body: ReleaseRequestBody, ctx: RequestContext = Depends(get_ctx),
                    eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    return _run(eng.request_release, ctx, body.object_id, body.license).model_dump()


@router.post("/release/review")
def release_review(body: ReleaseReviewBody, ctx: RequestContext = Depends(get_ctx),
                   eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    return _run(eng.review_release, ctx, body.candidate_id, body.review_type, body.approved, body.notes).model_dump()


@router.post("/release/execute")
def release_execute(body: ReleaseExecuteBody, ctx: RequestContext = Depends(get_ctx),
                    eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    return _run(eng.execute_release, ctx, body.candidate_id)


# ---------------------------------------------------------------- federated

@router.get("/federated/capabilities")
def federated_capabilities(method: str = "AGGREGATE_COHORT", ctx: RequestContext = Depends(get_ctx),
                           eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    return {"sites": eng.discover_capabilities(ctx, method, ["age"])}


@router.post("/federated/query")
def federated_query(body: FederatedQueryBody, ctx: RequestContext = Depends(get_ctx),
                    eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    req = FederatedQueryRequest(orchestrator_tenant_id=ctx.tenant_id, requested_by=ctx.user_id,
                                participating_site_ids=body.sites, query_type=body.query_type,
                                cohort_criteria=body.cohort_criteria, allowed_output=body.allowed_output,
                                min_cell_size=body.min_cell_size, purpose=ctx.purpose or "APPROVED_RESEARCH",
                                enable_differential_privacy=body.enable_differential_privacy, epsilon=body.epsilon)
    return _run(eng.execute_federated_query, ctx, req).model_dump()


@router.get("/federated/jobs/{run_id}")
def federated_job(run_id: str, ctx: RequestContext = Depends(get_ctx), eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    run = eng.federated_runs.get(run_id)
    req = eng._federated_requests.get(run.query_id) if run else None
    if run is None or req is None or req.orchestrator_tenant_id != ctx.tenant_id:
        raise HTTPException(status_code=404, detail="Resource not found in your authorized scope")
    return run.model_dump()


@router.post("/federated/jobs/{run_id}/reproduce")
def federated_reproduce(run_id: str, ctx: RequestContext = Depends(get_ctx),
                        eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    run = eng.federated_runs.get(run_id)
    if run is None or eng._federated_requests[run.query_id].orchestrator_tenant_id != ctx.tenant_id:
        raise HTTPException(status_code=404, detail="Resource not found in your authorized scope")
    return _run(eng.reproduce_federated_run, ctx, run_id)


# ---------------------------------------------------------------- audit / privacy

@router.get("/audit/private")
def audit_private(ctx: RequestContext = Depends(get_ctx), eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    return {"events": _run(eng.tenant_audit, ctx), "chain_valid": eng.verify_audit_chain()}


@router.get("/privacy/dashboard")
def privacy_dashboard(ctx: RequestContext = Depends(get_ctx), eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    return _run(eng.privacy_dashboard, ctx)


@router.get("/privacy/boundary-report")
def boundary_report(ctx: RequestContext = Depends(get_ctx), eng: FederatedPrivacyEngine = Depends(get_engine)):
    _require_auth(ctx)
    return eng.knowledge_boundary_report(ctx)
