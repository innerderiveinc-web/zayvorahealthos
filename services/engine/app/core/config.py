"""
ZMIE Enterprise Centralized Configuration Management
Prompt 28 — MODULE 01 (Infrastructure) & Clause 11
Uses Pydantic BaseSettings for type-safe environment configuration,
secrets management, and default fallbacks for local and production deployments.
"""

import os
from enum import Enum
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    # --- Environment & Logging ---
    ZMIE_ENV: str = Field(default="development", description="Runtime environment")
    LOG_LEVEL: str = Field(default="INFO", description="Global log verbosity level")
    DEBUG: bool = Field(default=False, description="Enable debug diagnostics")
    ALLOWED_ORIGINS: str = Field(default="http://localhost:3000,http://localhost:8000")

    # --- Cryptography & Identity Security ---
    JWT_SECRET: str = Field(
        default="zmie_dev_insecure_jwt_secret_change_in_production_min32chars",
        description="HMAC/RSA secret key for JWT issuance and signature verification"
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT cryptographic signature algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, description="Access token TTL in minutes")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="Refresh token TTL in days")
    AUDIT_HMAC_SECRET: str = Field(
        default="zmie_dev_insecure_audit_secret_change_in_production",
        description="Secret key for signing immutable audit hash chains"
    )

    # --- Enterprise SSO / OIDC ---
    OIDC_ISSUER_URL: Optional[str] = Field(default=None)
    OIDC_CLIENT_ID: Optional[str] = Field(default="zmie-core-service")
    OIDC_CLIENT_SECRET: Optional[str] = Field(default=None)
    OIDC_AUDIENCE: Optional[str] = Field(default="zmie-api")

    # --- Database & Storage Configuration ---
    DATABASE_URL: str = Field(
        default="postgresql://zmie_admin:zmie_secure_password@localhost:5432/zmie_knowledge_db",
        description="PostgreSQL + pgvector connection string"
    )
    DATABASE_POOL_SIZE: int = Field(default=20)
    DATABASE_MAX_OVERFLOW: int = Field(default=10)

    # --- Neo4j Graph Database ---
    NEO4J_URI: str = Field(default="bolt://localhost:7687")
    NEO4J_USER: str = Field(default="neo4j")
    NEO4J_PASSWORD: str = Field(default="zmie_graph_password")
    NEO4J_DATABASE: str = Field(default="neo4j")

    # --- Redis Cache & Event Broker ---
    REDIS_URL: str = Field(default="redis://localhost:6379/0")

    # --- OpenSearch Cluster ---
    OPENSEARCH_URL: str = Field(default="http://localhost:9200")
    OPENSEARCH_USER: str = Field(default="admin")
    OPENSEARCH_PASSWORD: str = Field(default="admin")

    # --- MinIO Immutable Object Storage ---
    MINIO_ENDPOINT: str = Field(default="localhost:9000")
    MINIO_ACCESS_KEY: str = Field(default="zmie_minio_admin")
    MINIO_SECRET_KEY: str = Field(default="zmie_minio_secret_key")
    MINIO_BUCKET_NAME: str = Field(default="zmie-immutable-documents")
    MINIO_SECURE: bool = Field(default=False)

    # --- Scholarly APIs ---
    OPENALEX_MAILTO: str = Field(default="engineering@zmie.org")
    NCBI_API_KEY: Optional[str] = Field(default=None)
    PUBMED_API_KEY: Optional[str] = Field(default=None)
    CROSSREF_MAILTO: str = Field(default="engineering@zmie.org")

    # --- Multi-Model LLM Gateway ---
    GEMINI_API_KEY: Optional[str] = Field(default=None)
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None)
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    LOCAL_LLM_BASE_URL: str = Field(default="http://localhost:11434/v1")
    LOCAL_LLM_MODEL: str = Field(default="biomistral-7b")

    # --- Scientific Compute Sandbox & Guardrails ---
    COMPUTE_SANDBOX_TIMEOUT_SEC: int = Field(default=300)
    COMPUTE_SANDBOX_MEMORY_MB: int = Field(default=4096)
    COMPUTE_SANDBOX_MAX_CORES: int = Field(default=2)
    AGENT_MAX_TOOL_CALLS_PER_RUN: int = Field(default=50)
    AGENT_EXECUTION_BUDGET_USD: float = Field(default=10.00)

    # --- Differential Privacy & Governance ---
    DP_DEFAULT_EPSILON: float = Field(default=1.0)
    DP_DEFAULT_DELTA: float = Field(default=0.00001)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def is_production(self) -> bool:
        return self.ZMIE_ENV.lower() == EnvironmentType.PRODUCTION.value

    @property
    def parsed_allowed_origins(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

    @property
    def ENVIRONMENT(self) -> str:
        """Alias for ZMIE_ENV to support deep_health diagnostics."""
        return self.ZMIE_ENV

    @property
    def effective_ncbi_api_key(self) -> Optional[str]:
        """Returns either NCBI_API_KEY or PUBMED_API_KEY if configured."""
        return self.NCBI_API_KEY or self.PUBMED_API_KEY



_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """Singleton accessor for platform configuration."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
