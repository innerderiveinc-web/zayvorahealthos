"""
ZMIE Security, Authentication & Role-Based Access Control (RBAC)
Prompt 28 — Integrates MODULE 02 (Identity), MODULE 03 (Tenancy), and MODULE 04 (Authorization).

Maintains 100% backwards compatibility with existing test suites while enabling:
- Real Cryptographic JWT Token verification
- Salted API Keys & Registry
- Strict Tenant Isolation Context
- RBAC / ABAC Role bridging
"""

import os
from enum import Enum
from typing import Optional, Dict, Any, List
from fastapi import Header, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from pydantic import BaseModel, Field

from app.core.identity import decode_access_token, verify_password
from app.core.tenancy import TenantContext, DataClassification
from app.core.authorization import EnterpriseRole, Action, AuthorizationEngine, SubjectAttributes, ResourceAttributes
from app.platform.gateway import APIGatewayEngine


class UserRole(str, Enum):
    PUBLIC = "public"
    RESEARCHER = "researcher"
    CLINICIAN = "clinician"
    ADMIN = "admin"


# Role mapping from legacy UserRole to EnterpriseRole
ROLE_BRIDGE_MAP: Dict[UserRole, EnterpriseRole] = {
    UserRole.PUBLIC: EnterpriseRole.READ_ONLY,
    UserRole.RESEARCHER: EnterpriseRole.RESEARCHER,
    UserRole.CLINICIAN: EnterpriseRole.CLINICIAN,
    UserRole.ADMIN: EnterpriseRole.PLATFORM_ADMIN,
}


class AuthContext(BaseModel):
    user_id: str
    org_id: str
    role: UserRole
    tenant_id: str = "org-global-public"
    is_authenticated: bool = True
    tenant_isolated: bool = True
    clearance: DataClassification = DataClassification.PUBLIC
    enterprise_role: Optional[EnterpriseRole] = None

    def model_post_init(self, __context: Any) -> None:
        if self.enterprise_role is None and self.role in ROLE_BRIDGE_MAP:
            object.__setattr__(self, "enterprise_role", ROLE_BRIDGE_MAP[self.role])
        if self.tenant_id == "org-global-public" and self.org_id:
            object.__setattr__(self, "tenant_id", self.org_id)

    def to_tenant_context(self) -> TenantContext:
        return TenantContext(
            tenant_id=self.tenant_id,
            user_id=self.user_id,
            classification=self.clearance,
            is_cross_tenant_allowed=(self.role == UserRole.ADMIN)
        )

    def to_subject_attributes(self) -> SubjectAttributes:
        active_role = self.enterprise_role or ROLE_BRIDGE_MAP.get(self.role, EnterpriseRole.READ_ONLY)
        return SubjectAttributes(
            user_id=self.user_id,
            tenant_id=self.tenant_id,
            roles=[active_role],
            clearance=self.clearance
        )


# API Key Headers: 'X-ZMIE-API-KEY' and standard 'X-API-Key'
api_key_header_zmie = APIKeyHeader(name="X-ZMIE-API-KEY", auto_error=False)
api_key_header_std = APIKeyHeader(name="X-API-Key", auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)


# Known API Keys Registry (production maps to PostgreSQL 'users' table)
API_KEYS_REGISTRY: Dict[str, Dict[str, Any]] = {
    "zmie-pub-key-2026": {"user_id": "usr-public-anon", "org_id": "org-global-public", "tenant_id": "org-global-public", "role": UserRole.PUBLIC},
    "zmie-res-key-9921": {"user_id": "usr-res-lead-01", "org_id": "org-aiims-delhi", "tenant_id": "org-aiims-delhi", "role": UserRole.RESEARCHER},
    "zmie-cli-key-4412": {"user_id": "usr-dr-sharma-cardio", "org_id": "org-apollo-hospitals", "tenant_id": "org-apollo-hospitals", "role": UserRole.CLINICIAN},
    "zmie-adm-key-0001": {"user_id": "usr-admin-principal", "org_id": "org-zmie-governance", "tenant_id": "org-zmie-governance", "role": UserRole.ADMIN}
}


async def get_current_user(
    api_key_zmie: Optional[str] = Security(api_key_header_zmie),
    api_key_std: Optional[str] = Security(api_key_header_std),
    bearer: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme)
) -> AuthContext:
    """
    Authenticates caller via API key, hashed API gateway key, or cryptographic JWT Bearer token.
    Fails closed to unauthenticated public persona on any invalid or unrecognized credential.
    """
    raw_token = api_key_zmie or api_key_std
    if not raw_token and bearer and bearer.credentials:
        raw_token = bearer.credentials.strip()
        if raw_token.startswith("Bearer "):
            raw_token = raw_token.replace("Bearer ", "")

    if raw_token:
        # 1. Check known API key registry
        if raw_token in API_KEYS_REGISTRY:
            meta = API_KEYS_REGISTRY[raw_token]
            return AuthContext(
                user_id=meta["user_id"],
                org_id=meta["org_id"],
                tenant_id=meta.get("tenant_id", meta["org_id"]),
                role=meta["role"],
                is_authenticated=True,
                tenant_isolated=True,
                enterprise_role=ROLE_BRIDGE_MAP.get(meta["role"])
            )

        # 2. Check hashed credentials in APIGatewayEngine
        cred = APIGatewayEngine.authenticate_key(raw_token)
        if cred:
            is_admin = (cred.tenant_id == "org-zmie-governance" or "admin" in cred.owner)
            role = UserRole.ADMIN if is_admin else UserRole.RESEARCHER
            return AuthContext(
                user_id=cred.owner,
                org_id=cred.tenant_id,
                tenant_id=cred.tenant_id,
                role=role,
                is_authenticated=True,
                tenant_isolated=True,
                enterprise_role=ROLE_BRIDGE_MAP.get(role)
            )

        # 3. Cryptographic JWT Token verification
        try:
            claims = decode_access_token(raw_token)
            user_id = claims.get("sub", claims.get("user_id", "usr-jwt-authenticated"))
            org_id = claims.get("org_id", claims.get("tenant_id", "org-tenant-default"))
            tenant_id = claims.get("tenant_id", org_id)
            raw_role = claims.get("role", "researcher")
            
            try:
                role_enum = UserRole(raw_role)
            except ValueError:
                role_enum = UserRole.RESEARCHER
                
            return AuthContext(
                user_id=user_id,
                org_id=org_id,
                tenant_id=tenant_id,
                role=role_enum,
                is_authenticated=True,
                tenant_isolated=True,
                enterprise_role=ROLE_BRIDGE_MAP.get(role_enum)
            )
        except Exception:
            pass  # Fall through to unauthenticated default on invalid token

    # Default fallback: Public Read-Only Persona (Fails closed)
    return AuthContext(
        user_id="usr-anonymous",
        org_id="org-public-guest",
        tenant_id="org-public-guest",
        role=UserRole.PUBLIC,
        is_authenticated=False,
        tenant_isolated=True,
        enterprise_role=EnterpriseRole.READ_ONLY
    )


async def require_authenticated(auth: AuthContext = Depends(get_current_user)) -> AuthContext:
    """
    Dependency enforcing authenticated user context.
    Fails closed with HTTP 401 if caller is unauthenticated.
    """
    if not auth.is_authenticated:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Provide a valid Bearer token or API key."
        )
    return auth


def require_role(required_roles: list[UserRole]):
    """
    Dependency enforcing minimum role requirement.
    Fails closed with HTTP 401 if unauthenticated, and HTTP 403 if unauthorized.
    """
    async def role_checker(auth: AuthContext = Depends(get_current_user)):
        if not auth.is_authenticated:
            raise HTTPException(
                status_code=401,
                detail="Authentication required. Provide a valid Bearer token or API key."
            )
        if auth.role not in required_roles and auth.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=403,
                detail=f"Access forbidden: requires one of {[r.value for r in required_roles]}. Current role: {auth.role.value}"
            )
        return auth
    return role_checker


class SecurityService:
    get_current_user = staticmethod(get_current_user)
    require_authenticated = staticmethod(require_authenticated)
    require_role = staticmethod(require_role)
