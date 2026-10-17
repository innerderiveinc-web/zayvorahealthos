"""
ZMIE Security, Governance, Multi-Tenancy & Privacy Models
Comprehensive schemas for:
- Data classification (Public, Internal, Confidential, Sensitive, Highly Sensitive, Restricted)
- Granular consent management (purpose-bound, revocable, time-aware, ABDM-ready)
- Hard multi-tenant hierarchy (Platform, Organization, Workspace, Project, Resource)
- RBAC / ABAC policies and identity contracts
- Tamper-resistant immutable audit logging
- Security incidents & containment workflows
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class DataClassificationTier(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    SENSITIVE = "SENSITIVE"
    HIGHLY_SENSITIVE = "HIGHLY_SENSITIVE"
    RESTRICTED = "RESTRICTED"


class ConsentStatus(str, Enum):
    PENDING = "PENDING"
    GRANTED = "GRANTED"
    DENIED = "DENIED"
    WITHDRAWN = "WITHDRAWN"
    EXPIRED = "EXPIRED"
    SUPERSEDED = "SUPERSEDED"


class ConsentPurpose(str, Enum):
    HEALTH_RECORD_ACCESS = "health_record_access"
    RESEARCH_USE = "research_use"
    DATA_SHARING = "data_sharing"
    CAREGIVER_ACCESS = "caregiver_access"
    ANALYTICS = "analytics"
    AI_ASSISTANCE = "AI_assistance"
    CLINICAL_DATA_LINKING = "clinical_data_linking"
    EXTERNAL_INTEGRATION = "external_integration"


class TenantType(str, Enum):
    PUBLIC = "PUBLIC"
    RESEARCHER = "RESEARCHER"
    INSTITUTION = "INSTITUTION"
    ENTERPRISE = "ENTERPRISE"
    PRIVATE_KNOWLEDGE = "PRIVATE_KNOWLEDGE"


class UserRole(str, Enum):
    PLATFORM_ADMIN = "PLATFORM_ADMIN"
    SECURITY_ADMIN = "SECURITY_ADMIN"
    ORGANIZATION_OWNER = "ORGANIZATION_OWNER"
    RESEARCH_ADMIN = "RESEARCH_ADMIN"
    RESEARCHER = "RESEARCHER"
    CLINICAL_RESEARCHER = "CLINICAL_RESEARCHER"
    CLINICIAN = "CLINICIAN"
    KNOWLEDGE_CURATOR = "KNOWLEDGE_CURATOR"
    EXPERT_REVIEWER = "EXPERT_REVIEWER"
    SAFETY_REVIEWER = "SAFETY_REVIEWER"
    AUDITOR = "AUDITOR"
    ANALYST = "ANALYST"
    API_CLIENT = "API_CLIENT"
    PUBLIC_USER = "PUBLIC_USER"


class SecurityIncidentSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentStatus(str, Enum):
    DETECTED = "DETECTED"
    CONTAINED = "CONTAINED"
    INVESTIGATING = "INVESTIGATING"
    REMEDIATED = "REMEDIATED"
    CLOSED = "CLOSED"


class ConsentRecord(BaseModel):
    consent_id: str = Field(default_factory=lambda: f"cns-{uuid.uuid4().hex[:8]}")
    subject_id: str
    purpose: ConsentPurpose
    scope: str = "DEFAULT"
    policy_version: str = "v1.0"
    status: ConsentStatus = ConsentStatus.PENDING
    granted_at: Optional[datetime] = None
    withdrawn_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    source: str = "web_portal"
    proof_hash: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SecurityContext(BaseModel):
    user_id: str
    tenant_id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    roles: List[UserRole] = Field(default_factory=lambda: [UserRole.PUBLIC_USER])
    purpose: str = "care"
    data_classification: DataClassificationTier = DataClassificationTier.PUBLIC
    mfa_verified: bool = False
    is_break_glass: bool = False
    break_glass_reason: Optional[str] = None


class AuditEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt-{uuid.uuid4().hex[:8]}")
    event_type: str  # LOGIN, PERMISSION_CHANGE, CONSENT_CHANGE, DATA_ACCESS, DATA_EXPORT, RETRACTION, SAFETY_BLOCK
    actor_type: str = "USER"  # USER, AGENT, SYSTEM, API_CLIENT
    actor_id: str
    tenant_id: str
    resource_type: str
    resource_id: str
    action: str
    result: str  # ALLOW, DENY, PASS, BLOCK, ERROR
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None
    ip_address: Optional[str] = "127.0.0.1"
    policy_version: str = "v1.0"
    before_state_hash: Optional[str] = None
    after_state_hash: Optional[str] = None


class SecurityIncident(BaseModel):
    incident_id: str = Field(default_factory=lambda: f"inc-{uuid.uuid4().hex[:8]}")
    severity: SecurityIncidentSeverity
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    detected_by: str = "SecurityMonitor"
    scope: str
    affected_tenants: List[str] = Field(default_factory=list)
    affected_resources: List[str] = Field(default_factory=list)
    containment_action: str = ""
    root_cause: Optional[str] = None
    status: IncidentStatus = IncidentStatus.DETECTED
    closed_at: Optional[datetime] = None


class DataSubjectRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: f"dsr-{uuid.uuid4().hex[:8]}")
    subject_id: str
    request_type: str  # ACCESS, CORRECTION, DELETION, PORTABILITY, RESTRICTION, WITHDRAWAL
    scope: str = "ALL"
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED, REJECTED
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_to: Optional[str] = None
    resolution_notes: Optional[str] = None
    completed_at: Optional[datetime] = None
