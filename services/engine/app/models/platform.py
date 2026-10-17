"""
ZMIE Medical Knowledge Infrastructure Platform Models
Defines contracts for:
- API Credentials, scopes, and tenant associations
- RAG Context Packets & Medical Intelligence queries
- Model Router configurations and provider abstractions
- Webhook subscriptions, delivery logs, and event payloads
- Usage metering events
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class ApiCredentialType(str, Enum):
    API_KEY = "api_key"
    JWT = "jwt"
    SERVICE_ACCOUNT = "service_account"
    OAUTH2 = "oauth2"


class ApiCredentialStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"
    SUSPENDED = "suspended"


class ApiCredential(BaseModel):
    credential_id: str = Field(default_factory=lambda: f"cred-{uuid.uuid4().hex[:8]}")
    tenant_id: str
    owner: str
    name: str
    key_hash: str
    key_prefix: str
    type: ApiCredentialType = ApiCredentialType.API_KEY
    scopes: List[str] = Field(default_factory=lambda: ["knowledge:read", "search:read", "evidence:read"])
    status: ApiCredentialStatus = ApiCredentialStatus.ACTIVE
    environment: str = "production"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None


class RAGContextRequest(BaseModel):
    query: str
    filters: Dict[str, Any] = Field(default_factory=dict)
    max_items: int = 20
    evidence_minimum: str = "E5"
    include_safety: bool = True
    include_contradictions: bool = True


class RAGContextPacket(BaseModel):
    query: str
    knowledge_version: str = "2026.10"
    retrieval_version: str = "v1.0"
    entities: List[Dict[str, Any]] = Field(default_factory=list)
    verified_claims: List[Dict[str, Any]] = Field(default_factory=list)
    evidence_items: List[Dict[str, Any]] = Field(default_factory=list)
    contradictions: List[Dict[str, Any]] = Field(default_factory=list)
    safety_context: Dict[str, Any] = Field(default_factory=dict)
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    context_token_estimate: int = 0


class IntelligenceQueryRequest(BaseModel):
    query: str
    mode: str = "evidence"  # search, evidence, compare, safety, explain, research
    systems: List[str] = Field(default_factory=lambda: ["modern", "unani", "ayurveda"])
    strict_verification: bool = True


class IntelligenceQueryResponse(BaseModel):
    query: str
    interpretation: str
    entities: List[Dict[str, Any]] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    graph_context: Dict[str, Any] = Field(default_factory=dict)
    safety: Dict[str, Any] = Field(default_factory=dict)
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    knowledge_version: str = "2026.10"
    verified: bool = True


class ModelRouteConfig(BaseModel):
    route_id: str = Field(default_factory=lambda: f"route-{uuid.uuid4().hex[:8]}")
    task_type: str  # synthesis, classification, verification, summarization
    risk_level: str = "MEDIUM"
    allowed_models: List[str] = Field(default_factory=list)
    primary_model: str = "claude-3-5-sonnet"
    fallback_model: str = "gpt-4o"
    latency_target_ms: int = 1500
    status: str = "active"


class WebhookSubscription(BaseModel):
    webhook_id: str = Field(default_factory=lambda: f"whk-{uuid.uuid4().hex[:8]}")
    tenant_id: str
    target_url: str
    secret_key: str
    subscribed_events: List[str] = Field(default_factory=lambda: ["research.completed", "source.retracted"])
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WebhookDelivery(BaseModel):
    delivery_id: str = Field(default_factory=lambda: f"deliv-{uuid.uuid4().hex[:8]}")
    webhook_id: str
    event_id: str
    event_type: str
    target_url: str
    status: str = "DELIVERED"
    response_code: int = 200
    attempt: int = 1
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class UsageEvent(BaseModel):
    usage_id: str = Field(default_factory=lambda: f"usg-{uuid.uuid4().hex[:8]}")
    tenant_id: str
    credential_id: str
    service: str  # search, knowledge, evidence, graph, research, ai_gateway
    operation: str
    units: int = 1
    timestamp: datetime = Field(default_factory=datetime.utcnow)
