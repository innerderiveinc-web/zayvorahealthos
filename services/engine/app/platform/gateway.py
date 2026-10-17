"""
ZMIE Centralized API Gateway & Credential Engine
Handles:
- API Key creation, hashing, validation, rotation, and revocation
- Scope-based and tenant-isolated request authentication
- Usage metering event recording
"""

import hashlib
import uuid
from datetime import datetime
from typing import Dict, Optional, List, Tuple

from app.models.platform import ApiCredential, ApiCredentialStatus, UsageEvent


class APIGatewayEngine:
    """
    Manages API keys and caller identity authentication across all platform endpoints.
    """

    _credentials_store: Dict[str, ApiCredential] = {}
    _usage_ledger: List[UsageEvent] = []

    @classmethod
    def create_api_key(
        cls,
        tenant_id: str,
        owner: str,
        name: str,
        scopes: Optional[List[str]] = None,
        environment: str = "production"
    ) -> Tuple[str, ApiCredential]:
        """
        Creates an API key: returns (raw_api_key, ApiCredential).
        The raw key is returned only once; only SHA-256 hash is stored.
        """
        if scopes is None:
            scopes = ["knowledge:read", "search:read", "evidence:read", "safety:read"]

        raw_secret = f"zmie_{environment}_{uuid.uuid4().hex}{uuid.uuid4().hex[:12]}"
        key_hash = hashlib.sha256(raw_secret.encode()).hexdigest()
        key_prefix = raw_secret[:12]

        cred = ApiCredential(
            credential_id=f"cred-{uuid.uuid4().hex[:8]}",
            tenant_id=tenant_id,
            owner=owner,
            name=name,
            key_hash=key_hash,
            key_prefix=key_prefix,
            scopes=scopes,
            status=ApiCredentialStatus.ACTIVE,
            environment=environment,
            created_at=datetime.utcnow()
        )
        cls._credentials_store[cred.credential_id] = cred
        return raw_secret, cred

    @classmethod
    def authenticate_key(cls, raw_key: str, required_scope: Optional[str] = None) -> Optional[ApiCredential]:
        """
        Authenticates an incoming raw API key against stored credentials.
        Validates active status and required scope.
        """
        if not raw_key or not raw_key.startswith("zmie_"):
            return None

        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        for cred in cls._credentials_store.values():
            if cred.key_hash == key_hash:
                if cred.status != ApiCredentialStatus.ACTIVE:
                    return None
                if required_scope and required_scope not in cred.scopes and "*" not in cred.scopes:
                    return None
                cred.last_used_at = datetime.utcnow()
                return cred
        return None

    @classmethod
    def revoke_api_key(cls, credential_id: str) -> bool:
        """
        Revokes an API key immediately.
        """
        cred = cls._credentials_store.get(credential_id)
        if cred:
            cred.status = ApiCredentialStatus.REVOKED
            return True
        return False

    @classmethod
    def record_usage(cls, tenant_id: str, cred_id: str, service: str, operation: str, units: int = 1):
        """
        Records metered usage event in the ledger.
        """
        evt = UsageEvent(
            tenant_id=tenant_id,
            credential_id=cred_id,
            service=service,
            operation=operation,
            units=units
        )
        cls._usage_ledger.append(evt)

    @classmethod
    def list_credentials(cls, tenant_id: Optional[str] = None) -> List[ApiCredential]:
        if tenant_id:
            return [c for c in cls._credentials_store.values() if c.tenant_id == tenant_id]
        return list(cls._credentials_store.values())

    @classmethod
    def get_tenant_usage(cls, tenant_id: str) -> List[UsageEvent]:
        return [u for u in cls._usage_ledger if u.tenant_id == tenant_id]

    @classmethod
    def get_usage_events(cls, tenant_id: Optional[str] = None) -> List[UsageEvent]:
        if tenant_id:
            return [u for u in cls._usage_ledger if u.tenant_id == tenant_id]
        return cls._usage_ledger
