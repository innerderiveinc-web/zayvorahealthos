"""
ZMIE Platform API Router
Exposes enterprise endpoints for:
- API Credential lifecycle & scopes
- RAG Context Packet assembly
- Multi-system Medical Intelligence queries
- AI Model Gateway routing with fallback & truth verification
- Webhook subscriptions & delivery logs
- Metered usage ledger
"""

from fastapi import APIRouter, HTTPException, Header, Depends, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.models.platform import (
    ApiCredential, RAGContextRequest, RAGContextPacket,
    IntelligenceQueryRequest, IntelligenceQueryResponse,
    WebhookSubscription, WebhookDelivery, UsageEvent
)
from app.platform.gateway import APIGatewayEngine
from app.platform.model_router import ai_model_router
from app.platform.rag_service import rag_service
from app.platform.webhooks import webhook_dispatcher

router = APIRouter(prefix="/platform", tags=["Platform & Enterprise Infrastructure"])


# Authentication helper
def verify_platform_auth(x_api_key: Optional[str] = Header(None)) -> Optional[ApiCredential]:
    if not x_api_key:
        # Allow open internal calls if none provided in demo/dev mode
        return None
    cred = APIGatewayEngine.authenticate_key(x_api_key)
    if not cred:
        raise HTTPException(status_code=401, detail="Invalid or revoked ZMIE API key.")
    return cred


# --- API Key Lifecycle ---

class CreateKeyRequest(BaseModel):
    tenant_id: str
    owner: str
    name: str
    scopes: Optional[List[str]] = None
    environment: str = "production"


class CreateKeyResponse(BaseModel):
    raw_api_key: str
    credential: ApiCredential


@router.post("/keys", response_model=CreateKeyResponse)
def create_api_key(req: CreateKeyRequest):
    raw_key, cred = APIGatewayEngine.create_api_key(
        tenant_id=req.tenant_id,
        owner=req.owner,
        name=req.name,
        scopes=req.scopes,
        environment=req.environment
    )
    return CreateKeyResponse(raw_api_key=raw_key, credential=cred)


@router.get("/keys", response_model=List[ApiCredential])
def list_api_keys(tenant_id: Optional[str] = Query(None)):
    return APIGatewayEngine.list_credentials(tenant_id)


@router.delete("/keys/{credential_id}")
def revoke_api_key(credential_id: str):
    success = APIGatewayEngine.revoke_api_key(credential_id)
    if not success:
        raise HTTPException(status_code=404, detail="Credential not found.")
    return {"status": "REVOKED", "credential_id": credential_id}


# --- RAG Context Packet Engine ---

@router.post("/rag/context", response_model=RAGContextPacket)
def generate_rag_context(
    req: RAGContextRequest,
    cred: Optional[ApiCredential] = Depends(verify_platform_auth)
):
    if cred:
        APIGatewayEngine.record_usage(
            tenant_id=cred.tenant_id,
            cred_id=cred.credential_id,
            service="rag_context",
            operation="generate_packet",
            units=1
        )
    return rag_service.build_context_packet(req)


# --- Multi-System Intelligence Query ---

@router.post("/intelligence/query", response_model=IntelligenceQueryResponse)
def execute_intelligence_query(
    req: IntelligenceQueryRequest,
    cred: Optional[ApiCredential] = Depends(verify_platform_auth)
):
    if cred:
        APIGatewayEngine.record_usage(
            tenant_id=cred.tenant_id,
            cred_id=cred.credential_id,
            service="intelligence",
            operation="multi_system_query",
            units=1
        )
    return rag_service.execute_intelligence_query(req)


# --- AI Model Router & Gateway ---

class AIRouteRequest(BaseModel):
    task_type: str = "synthesis"
    prompt: str
    context_packet: Optional[RAGContextPacket] = None
    force_model: Optional[str] = None
    simulate_failure: bool = False


@router.post("/ai/route")
def route_ai_task(
    req: AIRouteRequest,
    cred: Optional[ApiCredential] = Depends(verify_platform_auth)
):
    if cred:
        APIGatewayEngine.record_usage(
            tenant_id=cred.tenant_id,
            cred_id=cred.credential_id,
            service="ai_gateway",
            operation=req.task_type,
            units=1
        )
    result = ai_model_router.route_request(
        task_type=req.task_type,
        prompt=req.prompt,
        context_packet=req.context_packet,
        force_model=req.force_model,
        simulate_failure=req.simulate_failure
    )
    return result


# --- Webhooks Management ---

class CreateWebhookRequest(BaseModel):
    tenant_id: str
    target_url: str
    secret_key: Optional[str] = None
    subscribed_events: Optional[List[str]] = None


@router.post("/webhooks", response_model=WebhookSubscription)
def create_webhook(req: CreateWebhookRequest):
    return webhook_dispatcher.create_subscription(
        tenant_id=req.tenant_id,
        target_url=req.target_url,
        secret_key=req.secret_key,
        subscribed_events=req.subscribed_events
    )


@router.get("/webhooks", response_model=List[WebhookSubscription])
def list_webhooks(tenant_id: Optional[str] = Query(None)):
    return webhook_dispatcher.list_subscriptions(tenant_id)


@router.delete("/webhooks/{webhook_id}")
def delete_webhook(webhook_id: str):
    success = webhook_dispatcher.delete_subscription(webhook_id)
    if not success:
        raise HTTPException(status_code=404, detail="Webhook subscription not found.")
    return {"status": "DELETED", "webhook_id": webhook_id}


class TestDispatchEvent(BaseModel):
    event_type: str = "source.retracted"
    event_data: Dict[str, Any]
    tenant_id: Optional[str] = None


@router.post("/webhooks/test-dispatch", response_model=List[WebhookDelivery])
def test_dispatch(req: TestDispatchEvent):
    return webhook_dispatcher.dispatch_event(
        event_type=req.event_type,
        event_data=req.event_data,
        tenant_id=req.tenant_id
    )


@router.get("/webhooks/deliveries", response_model=List[WebhookDelivery])
def list_deliveries(webhook_id: Optional[str] = Query(None)):
    return webhook_dispatcher.list_deliveries(webhook_id)


# --- Usage Metering Ledger ---

@router.get("/usage", response_model=List[UsageEvent])
def get_usage(tenant_id: Optional[str] = Query(None)):
    return APIGatewayEngine.get_usage_events(tenant_id)
