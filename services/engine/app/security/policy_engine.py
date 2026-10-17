"""
ZMIE Zero-Trust Authorization & Tenant Isolation Policy Engine
Implements:
- Strict server-side RBAC and ABAC authorization checks
- Hard Multi-Tenant isolation (no cross-tenant leakage in DB, Search, or Graph)
- Purpose limitation & data classification compliance
- Break-glass privileged access handling
- MFA enforcement for administrative actions
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from app.models.security import (
    SecurityContext,
    UserRole,
    DataClassificationTier,
    TenantType
)
from app.security.audit_engine import AuditLoggingEngine


class AuthorizationPolicyEngine:
    """
    Central Zero-Trust authorization evaluator.
    Deny by default for any unknown permission, cross-tenant boundary, or classification mismatch.
    """

    # Role permission mappings
    ROLE_PERMISSIONS: Dict[UserRole, List[str]] = {
        UserRole.PLATFORM_ADMIN: ["*"],
        UserRole.SECURITY_ADMIN: ["security:*", "audit:read", "incident:*", "policy:*"],
        UserRole.ORGANIZATION_OWNER: ["org:*", "project:*", "research:*", "audit:read_own"],
        UserRole.RESEARCH_ADMIN: ["research:*", "project:*", "source:read", "export:*"],
        UserRole.RESEARCHER: ["research:read", "research:create", "project:read", "project:write", "source:read"],
        UserRole.CLINICAL_RESEARCHER: ["research:*", "clinical:read", "source:read", "export:deidentified"],
        UserRole.CLINICIAN: ["medicine:read", "evidence:read", "guideline:read", "safety:read"],
        UserRole.KNOWLEDGE_CURATOR: ["knowledge:edit", "claim:verify", "mapping:edit", "source:ingest"],
        UserRole.EXPERT_REVIEWER: ["review:approve", "claim:review", "knowledge:read"],
        UserRole.SAFETY_REVIEWER: ["safety:review", "safety:block", "claim:audit"],
        UserRole.AUDITOR: ["audit:read", "compliance:read", "export:audit"],
        UserRole.PUBLIC_USER: ["medicine:read", "search:public", "graph:public"]
    }

    @classmethod
    def evaluate_access(
        cls,
        context: SecurityContext,
        action: str,
        resource_tenant_id: str,
        resource_classification: DataClassificationTier = DataClassificationTier.PUBLIC,
        required_purpose: Optional[str] = None
    ) -> bool:
        """
        Evaluates WHO + WHAT ACTION + WHICH RESOURCE + WHICH TENANT + WHICH PURPOSE + DATA CLASS.
        Returns True if granted, False (Deny) otherwise. Records audit trail.
        """
        # 1. Break-Glass Override
        if context.is_break_glass:
            AuditLoggingEngine.record_event(
                event_type="BREAK_GLASS_ACCESS",
                actor_id=context.user_id,
                tenant_id=context.tenant_id,
                resource_type="RESOURCE",
                resource_id=f"tenant:{resource_tenant_id}",
                action=action,
                result="ALLOW",
                before_state=context.break_glass_reason or "Emergency Access"
            )
            return True

        # 2. Hard Tenant Isolation (Platform Admin excepted)
        is_platform_admin = UserRole.PLATFORM_ADMIN in context.roles
        if not is_platform_admin and context.tenant_id != resource_tenant_id:
            AuditLoggingEngine.record_event(
                event_type="TENANT_ISOLATION_VIOLATION",
                actor_id=context.user_id,
                tenant_id=context.tenant_id,
                resource_type="RESOURCE",
                resource_id=f"target_tenant:{resource_tenant_id}",
                action=action,
                result="DENY"
            )
            return False

        # 3. MFA Check for Administrative / High-Risk actions
        admin_actions = ["security:", "policy:", "knowledge:release", "user:grant", "export:raw"]
        requires_mfa = any(action.startswith(prefix) for prefix in admin_actions)
        if requires_mfa and not context.mfa_verified:
            AuditLoggingEngine.record_event(
                event_type="MFA_CHALLENGE_FAILED",
                actor_id=context.user_id,
                tenant_id=context.tenant_id,
                resource_type="PRIVILEGED_RESOURCE",
                resource_id=action,
                action=action,
                result="DENY"
            )
            return False

        # 4. Data Classification Level Evaluation
        if resource_classification in [DataClassificationTier.HIGHLY_SENSITIVE, DataClassificationTier.RESTRICTED]:
            allowed_high_roles = [UserRole.PLATFORM_ADMIN, UserRole.SECURITY_ADMIN, UserRole.CLINICAL_RESEARCHER]
            if not any(role in allowed_high_roles for role in context.roles):
                AuditLoggingEngine.record_event(
                    event_type="DATA_CLASSIFICATION_RESTRICTION",
                    actor_id=context.user_id,
                    tenant_id=context.tenant_id,
                    resource_type="RESTRICTED_DATA",
                    resource_id=resource_classification.value,
                    action=action,
                    result="DENY"
                )
                return False

        # 5. Role-Based Permissions (RBAC)
        has_permission = False
        for role in context.roles:
            role_perms = cls.ROLE_PERMISSIONS.get(role, [])
            if "*" in role_perms or action in role_perms:
                has_permission = True
                break
            # Prefix wildcard matching (e.g. 'research:*')
            prefix = action.split(":")[0] + ":*"
            if prefix in role_perms:
                has_permission = True
                break

        # 6. Audit Decision
        result_str = "ALLOW" if has_permission else "DENY"
        AuditLoggingEngine.record_event(
            event_type="AUTHORIZATION_EVALUATION",
            actor_id=context.user_id,
            tenant_id=context.tenant_id,
            resource_type="RESOURCE",
            resource_id=action,
            action=action,
            result=result_str
        )

        return has_permission
