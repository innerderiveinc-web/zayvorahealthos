"""
ZMIE Enterprise Tenant & Workspace Hierarchy Subsystem
Prompt 28 — MODULE 03 (Tenant / Workspace) & Clause 14

Enforces the strict hierarchy:
    Tenant
      ↓
    Workspace
      ↓
    Project
      ↓
    Research / Data / Knowledge / Computation

Ensures every execution context carries unambiguous tenant scope.
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class TenantTier(str, Enum):
    PUBLIC = "public"
    ACADEMIC = "academic"
    HEALTHCARE = "healthcare"
    ENTERPRISE = "enterprise"
    GOVERNMENT = "government"


class IsolationMode(str, Enum):
    LOGICAL = "logical"
    PHYSICAL = "physical"
    FEDERATED_ENCLAVE = "federated_enclave"


class DataClassification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED_PHI = "restricted_phi"


class Tenant(BaseModel):
    tenant_id: str
    name: str
    tier: TenantTier = TenantTier.ENTERPRISE
    isolation_mode: IsolationMode = IsolationMode.LOGICAL
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    config: Dict[str, Any] = Field(default_factory=dict)


class Workspace(BaseModel):
    workspace_id: str
    tenant_id: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Project(BaseModel):
    project_id: str
    workspace_id: str
    tenant_id: str
    name: str
    classification: DataClassification = DataClassification.INTERNAL
    is_archived: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Team(BaseModel):
    team_id: str
    tenant_id: str
    name: str
    lead_user_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Membership(BaseModel):
    membership_id: str
    user_id: str
    tenant_id: str
    workspace_id: Optional[str] = None
    project_id: Optional[str] = None
    role: str = "researcher"
    granted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TenantContext(BaseModel):
    """Immutable context carried on all authenticated research & data operations."""
    tenant_id: str
    workspace_id: Optional[str] = None
    project_id: Optional[str] = None
    user_id: str
    classification: DataClassification = DataClassification.INTERNAL
    is_cross_tenant_allowed: bool = False


class TenantAccessDeniedException(Exception):
    """Raised whenever a boundary violation occurs across isolated tenants."""
    def __init__(self, resource_tenant: str, caller_tenant: str, message: Optional[str] = None):
        detail = message or f"Tenant isolation violation: resource tenant '{resource_tenant}' != caller tenant '{caller_tenant}'"
        super().__init__(detail)
        self.resource_tenant = resource_tenant
        self.caller_tenant = caller_tenant


# Alias for Prompt 28 invariant compliance
TenantIsolationException = TenantAccessDeniedException


def assert_tenant_boundary(
    resource_tenant_id: str,
    caller_tenant_id: str,
    allow_public: bool = True
) -> None:
    """
    Enforces strict tenant boundary isolation (Invariant INV-02 & Clause 16).
    If resource_tenant_id is 'public' and allow_public is True, access is permitted.
    Otherwise caller_tenant_id must match resource_tenant_id.
    """
    if allow_public and resource_tenant_id in ("public", "global", "org-global-public"):
        return
    if resource_tenant_id != caller_tenant_id:
        raise TenantAccessDeniedException(
            resource_tenant=resource_tenant_id,
            caller_tenant=caller_tenant_id
        )
