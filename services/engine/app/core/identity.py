"""
ZMIE Enterprise Identity & Authentication Subsystem
Prompt 28 — MODULE 02 (Identity) & Clause 13

Implements:
- User, Organization, Identity, Session, ApiCredential, OAuth/OIDC, MFA State
- Cryptographic JWT issuance & signature verification (HS256)
- Salted hashing for passwords and API credentials
- Enterprise SSO / OAuth identity mapping
"""

import hmac
import hashlib
import json
import base64
import time
import uuid
import secrets
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional, Dict, Any, List, Tuple
from pydantic import BaseModel, Field

from app.core.config import get_settings


class AuthMethod(str, Enum):
    API_KEY = "api_key"
    BEARER_TOKEN = "bearer_token"
    PASSWORD = "password"
    OIDC_SSO = "oidc_sso"
    MFA_TOTP = "mfa_totp"


class User(BaseModel):
    user_id: str
    email: str
    full_name: str
    tenant_id: str
    org_id: str
    is_active: bool = True
    is_verified: bool = True
    password_hash: Optional[str] = None
    mfa_enabled: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Organization(BaseModel):
    org_id: str
    name: str
    domain: str
    tenant_id: str
    sso_enabled: bool = False
    idp_issuer: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Session(BaseModel):
    session_id: str
    user_id: str
    tenant_id: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_revoked: bool = False


class ApiCredential(BaseModel):
    key_id: str
    key_prefix: str
    key_hash: str
    user_id: str
    tenant_id: str
    name: str
    scopes: List[str] = Field(default_factory=lambda: ["read", "analyze"])
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    is_active: bool = True


class OAuthIdentity(BaseModel):
    provider: str
    provider_user_id: str
    user_id: str
    email: str
    claims: Dict[str, Any] = Field(default_factory=dict)
    linked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MfaState(BaseModel):
    user_id: str
    is_enforced: bool = False
    secret_hash: Optional[str] = None
    verified_at: Optional[datetime] = None


# --- Cryptographic Utilities ---

def hash_password(password: str, salt: Optional[str] = None) -> str:
    """Computes a cryptographically salted SHA-256 hash for local credentials."""
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"sha256${salt}${hashed}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against the salted hash format."""
    try:
        parts = hashed_password.split("$")
        if len(parts) != 3 or parts[0] != "sha256":
            return False
        salt, expected_hash = parts[1], parts[2]
        actual_hash = hashlib.sha256((salt + plain_password).encode("utf-8")).hexdigest()
        return hmac.compare_digest(actual_hash, expected_hash)
    except Exception:
        return False


def create_access_token(
    payload: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
    secret_key: Optional[str] = None
) -> str:
    """
    Issues a signed compact JWT (RFC 7519) using HS256 without requiring external C libs.
    """
    settings = get_settings()
    secret = (secret_key or settings.JWT_SECRET).encode("utf-8")
    
    header = {"alg": "HS256", "typ": "JWT"}
    header_bytes = json.dumps(header, separators=(",", ":")).encode("utf-8")
    encoded_header = base64.urlsafe_b64encode(header_bytes).decode("utf-8").rstrip("=")
    
    claims = payload.copy()
    now = int(time.time())
    ttl = int(expires_delta.total_seconds()) if expires_delta else (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    claims["iat"] = now
    claims["exp"] = now + ttl
    if "jti" not in claims:
        claims["jti"] = str(uuid.uuid4())
        
    claims_bytes = json.dumps(claims, separators=(",", ":"), default=str).encode("utf-8")
    encoded_claims = base64.urlsafe_b64encode(claims_bytes).decode("utf-8").rstrip("=")
    
    signing_input = f"{encoded_header}.{encoded_claims}".encode("utf-8")
    signature = hmac.new(secret, signing_input, hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")
    
    return f"{encoded_header}.{encoded_claims}.{encoded_signature}"


def decode_access_token(token: str, secret_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Decodes and validates a signed JWT token.
    Raises ValueError on expired token, signature mismatch, or malformed structure.
    """
    settings = get_settings()
    secret = (secret_key or settings.JWT_SECRET).encode("utf-8")
    
    parts = token.strip().split(".")
    if len(parts) != 3:
        raise ValueError("Malformed JWT token: must contain 3 segments")
    
    encoded_header, encoded_claims, encoded_sig = parts
    signing_input = f"{encoded_header}.{encoded_claims}".encode("utf-8")
    
    expected_sig = hmac.new(secret, signing_input, hashlib.sha256).digest()
    
    # Pad base64 signature
    pad_len = 4 - (len(encoded_sig) % 4)
    if pad_len < 4:
        encoded_sig_padded = encoded_sig + ("=" * pad_len)
    else:
        encoded_sig_padded = encoded_sig
        
    try:
        actual_sig = base64.urlsafe_b64decode(encoded_sig_padded.encode("utf-8"))
    except Exception as e:
        raise ValueError(f"Invalid base64 signature: {e}")
        
    if not hmac.compare_digest(actual_sig, expected_sig):
        raise ValueError("Invalid JWT signature: cryptographic verification failed")
        
    # Pad and decode claims
    pad_len_claims = 4 - (len(encoded_claims) % 4)
    if pad_len_claims < 4:
        encoded_claims_padded = encoded_claims + ("=" * pad_len_claims)
    else:
        encoded_claims_padded = encoded_claims
        
    claims = json.loads(base64.urlsafe_b64decode(encoded_claims_padded.encode("utf-8")).decode("utf-8"))
    
    # Check expiration
    exp = claims.get("exp")
    if exp and int(time.time()) > exp:
        raise ValueError("JWT token has expired")
        
    return claims


def generate_api_key(
    tenant_id: str,
    user_id: str,
    name: str,
    scopes: Optional[List[str]] = None
) -> Tuple[str, ApiCredential]:
    """
    Generates a secure high-entropy API key with prefix formatting.
    Returns: (raw_secret_key, ApiCredential_record)
    """
    prefix = f"zmie_{secrets.token_hex(4)}"
    secret = secrets.token_urlsafe(32)
    raw_key = f"{prefix}_{secret}"
    
    key_hash = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
    
    credential = ApiCredential(
        key_id=str(uuid.uuid4()),
        key_prefix=prefix,
        key_hash=key_hash,
        user_id=user_id,
        tenant_id=tenant_id,
        name=name,
        scopes=scopes or ["read", "analyze"],
        created_at=datetime.now(timezone.utc)
    )
    return raw_key, credential
