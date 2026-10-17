"""
ZMIE Enterprise Authorization & Access Control Engine (RBAC + ABAC)
Prompt 28 — MODULE 04 (Authorization) & Clause 15

Implements:
- 12 Enterprise Roles
- 11 Explicit Resource Actions
- Attribute-Based Access Control (ABAC) Policy Evaluator
- Role-to-Action Permission Mappings
"""

from enum import Enum
from typing import List, Dict, Set, Optional, Any
from pydantic import BaseModel, Field

from app.core.tenancy import DataClassification, TenantAccessDeniedException


class EnterpriseRole(str, Enum):
    PLATFORM_ADMIN = "platform_admin"
    TENANT_ADMIN = "tenant_admin"
    WORKSPACE_ADMIN = "workspace_admin"
    PROJECT_OWNER = "project_owner"
    RESEARCHER = "researcher"
    CLINICIAN = "clinician"
    REVIEWER = "reviewer"
    SCIENTIST = "scientist"
    ANALYST = "analyst"
    DEVELOPER = "developer"
    AUDITOR = "auditor"
    READ_ONLY = "read_only"


class Action(str, Enum):
    READ = "READ"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    ANALYZE = "ANALYZE"
    EXECUTE = "EXECUTE"
    EXPORT = "EXPORT"
    SHARE = "SHARE"
    APPROVE = "APPROVE"
    PUBLISH = "PUBLISH"
    ADMINISTER = "ADMINISTER"


# Standard Default RBAC Action Sets for each Enterprise Role
ROLE_ACTION_PERMISSIONS: Dict[EnterpriseRole, Set[Action]] = {
    EnterpriseRole.PLATFORM_ADMIN: set(Action),  # Full universal actions
    EnterpriseRole.TENANT_ADMIN: {
        Action.READ, Action.CREATE, Action.UPDATE, Action.DELETE,
        Action.ANALYZE, Action.EXECUTE, Action.EXPORT, Action.SHARE,
        Action.APPROVE, Action.PUBLISH, Action.ADMINISTER
    },
    EnterpriseRole.WORKSPACE_ADMIN: {
        Action.READ, Action.CREATE, Action.UPDATE, Action.DELETE,
        Action.ANALYZE, Action.EXECUTE, Action.EXPORT, Action.SHARE,
        Action.APPROVE, Action.PUBLISH
    },
    EnterpriseRole.PROJECT_OWNER: {
        Action.READ, Action.CREATE, Action.UPDATE, Action.DELETE,
        Action.ANALYZE, Action.EXECUTE, Action.EXPORT, Action.SHARE,
        Action.APPROVE
    },
    EnterpriseRole.RESEARCHER: {
        Action.READ, Action.CREATE, Action.UPDATE,
        Action.ANALYZE, Action.EXECUTE, Action.EXPORT, Action.SHARE
    },
    EnterpriseRole.SCIENTIST: {
        Action.READ, Action.CREATE, Action.UPDATE,
        Action.ANALYZE, Action.EXECUTE, Action.EXPORT, Action.SHARE
    },
    EnterpriseRole.CLINICIAN: {
        Action.READ, Action.CREATE, Action.UPDATE,
        Action.ANALYZE, Action.EXPORT
    },
    EnterpriseRole.ANALYST: {
        Action.READ, Action.ANALYZE, Action.EXECUTE, Action.EXPORT
    },
    EnterpriseRole.REVIEWER: {
        Action.READ, Action.ANALYZE, Action.APPROVE
    },
    EnterpriseRole.DEVELOPER: {
        Action.READ, Action.CREATE, Action.UPDATE, Action.EXECUTE
    },
    EnterpriseRole.AUDITOR: {
        Action.READ, Action.ANALYZE, Action.EXPORT
    },
    EnterpriseRole.READ_ONLY: {
        Action.READ
    }
}


class SubjectAttributes(BaseModel):
    user_id: str
    tenant_id: str
    roles: List[EnterpriseRole] = Field(default_factory=lambda: [EnterpriseRole.READ_ONLY])
    clearance: DataClassification = DataClassification.PUBLIC
    attributes: Dict[str, Any] = Field(default_factory=dict)


class ResourceAttributes(BaseModel):
    resource_id: str
    resource_type: str
    tenant_id: str
    classification: DataClassification = DataClassification.INTERNAL
    owner_id: Optional[str] = None
    is_public: bool = False
    attributes: Dict[str, Any] = Field(default_factory=dict)


class EvaluationResult(BaseModel):
    allowed: bool
    reason: str
    matched_role: Optional[EnterpriseRole] = None
    policy: str = "ABAC_HYBRID_RBAC"


class AuthorizationEngine:
    """Enterprise policy decision point combining RBAC and ABAC rules."""

    # Clearance hierarchy for evaluation
    CLEARANCE_ORDER = {
        DataClassification.PUBLIC: 0,
        DataClassification.INTERNAL: 1,
        DataClassification.CONFIDENTIAL: 2,
        DataClassification.RESTRICTED_PHI: 3
    }

    @classmethod
    def evaluate(
        cls,
        subject: SubjectAttributes,
        action: Action,
        resource: ResourceAttributes
    ) -> EvaluationResult:
        """
        Evaluates whether the subject is authorized to perform action on resource.
        """
        # 1. Platform Admin override
        if EnterpriseRole.PLATFORM_ADMIN in subject.roles:
            return EvaluationResult(
                allowed=True,
                reason="Platform administrator override permitted",
                matched_role=EnterpriseRole.PLATFORM_ADMIN
            )

        # 2. Strict Tenant Boundary Isolation Check (Clause 16)
        if not resource.is_public and resource.tenant_id not in ("public", "global", "org-global-public"):
            if subject.tenant_id != resource.tenant_id:
                return EvaluationResult(
                    allowed=False,
                    reason=f"Tenant boundary isolation denied: subject '{subject.tenant_id}' != resource '{resource.tenant_id}'"
                )

        # 3. ABAC Data Classification Clearance Check
        subj_clearance_rank = cls.CLEARANCE_ORDER.get(subject.clearance, 0)
        res_clearance_rank = cls.CLEARANCE_ORDER.get(resource.classification, 0)
        if subj_clearance_rank < res_clearance_rank:
            return EvaluationResult(
                allowed=False,
                reason=f"Insufficient clearance: user holds '{subject.clearance.value}', resource requires '{resource.classification.value}'"
            )

        # 4. RBAC Action Permission Check across Subject's active roles
        allowed_roles = []
        for role in subject.roles:
            permitted_actions = ROLE_ACTION_PERMISSIONS.get(role, set())
            if action in permitted_actions:
                allowed_roles.append(role)

        if not allowed_roles:
            return EvaluationResult(
                allowed=False,
                reason=f"Action '{action.value}' not granted by roles {[r.value for r in subject.roles]}"
            )

        # 5. Resource Owner Discretionary Permission (if applicable)
        if resource.owner_id and resource.owner_id == subject.user_id:
            return EvaluationResult(
                allowed=True,
                reason=f"Granted via resource ownership and role '{allowed_roles[0].value}'",
                matched_role=allowed_roles[0]
            )

        return EvaluationResult(
            allowed=True,
            reason=f"Action '{action.value}' permitted under role '{allowed_roles[0].value}'",
            matched_role=allowed_roles[0]
        )
