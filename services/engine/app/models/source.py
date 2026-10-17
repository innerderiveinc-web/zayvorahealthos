"""
ZMIE Core Models: Source Registry & Authority Hierarchy
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl


class AuthorityTier(str, Enum):
    TIER_A = "tier_a_official"         # WHO, Ministries, Guideline bodies
    TIER_B = "tier_b_biomedical_repo"   # NLM, PubMed, PMC, NCBI Bookshelf
    TIER_C = "tier_c_evidence_synthesis"# Systematic reviews, Cochrane, Meta-analyses
    TIER_D = "tier_d_primary_empirical" # RCTs, Prospective Cohorts, In-vivo
    TIER_E = "tier_e_classical_corpus"  # Canonical Unani, Ayurvedic, TCM texts & Pharmacopoeias
    TIER_F = "tier_f_institutional"     # Universities, Theses, Medical school repositories
    TIER_G = "tier_g_general_web"       # Discovery/context only, quarantined from evidence scoring


class SourceStatus(str, Enum):
    AUTHORITATIVE = "authoritative"
    RECOGNIZED = "recognized"
    ACADEMIC = "academic"
    PEER_REVIEWED = "peer_reviewed"
    HISTORICAL_CLASSICAL = "historical_classical"
    SECONDARY = "secondary"
    RESTRICTED = "restricted"
    UNVERIFIED = "unverified"
    DEPRECATED = "deprecated"
    RETRACTED = "retracted"


class LicenseClass(str, Enum):
    CLASS_A = "full_text_licensed"      # Full storage, analysis, embeddings & derivations permitted
    CLASS_B = "permitted_open_access"   # Full text analysis under license (e.g. CC-BY, CC0)
    CLASS_C = "restricted_metadata_only" # Metadata, citations, permitted snippet, external link only


class SourceRegistryEntry(BaseModel):
    """
    Immutable identity record for any data source in ZMIE.
    """
    source_id: str = Field(..., description="Unique persistent identifier (e.g., SRC-OPENALEX-001)")
    organization: str = Field(..., description="Operating entity (e.g. 'National Library of Medicine', 'Ministry of Ayush')")
    publisher: Optional[str] = None
    domain: str = Field(..., description="Primary domain or namespace (e.g., 'ncbi.nlm.nih.gov')")
    jurisdiction: str = Field(..., description="Country or international body (e.g., 'Global', 'IN', 'US')")
    source_type: str = Field(..., description="'biomedical_repository', 'traditional_registry', 'guideline_body'")
    authority_tier: AuthorityTier
    status: SourceStatus = SourceStatus.RECOGNIZED
    license_class: LicenseClass
    peer_review_governed: bool = True
    retraction_monitored: bool = True
    version: Optional[str] = "1.0"
    update_frequency: str = Field(default="continuous", description="'daily', 'monthly', 'static'")
    provenance_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_verified_at: Optional[datetime] = None
