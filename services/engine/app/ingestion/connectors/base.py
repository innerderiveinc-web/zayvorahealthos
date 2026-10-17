"""
ZMIE Base Source Connector Framework
Provides abstract contract and standardized protocols for all acquisition adapters:
- Biomedical Literature (OpenAlex, Europe PMC, PubMed)
- Clinical Trial Registries (ClinicalTrials.gov, CTRI, WHO ICTRP)
- Traditional Medicine Codices & Portals (AYUSH, Unani CCRUM, Ayurveda CCRAS, TCM)
- Guidelines & Regulatory Authorities (WHO, FDA, EMA, CDSCO)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.models.source import AuthorityTier, LicenseClass, SourceStatus
from app.ingestion.licensing import LicensingIntelligenceEngine


class BaseSourceConnector(ABC):
    """
    Standard contract for all ZMIE knowledge acquisition connectors.
    Enforces unified discovery, licensing classification, provenance tracking,
    and normalized payload delivery.
    """

    def __init__(
        self,
        source_id: str,
        source_name: str,
        authority_tier: AuthorityTier,
        default_license_class: LicenseClass = LicenseClass.CLASS_C
    ):
        self.source_id = source_id
        self.source_name = source_name
        self.authority_tier = authority_tier
        self.default_license_class = default_license_class
        self.last_sync_time: Optional[datetime] = None
        self.error_count: int = 0
        self.request_count: int = 0

    @abstractmethod
    async def discover(self, query: str, limit: int = 10, **kwargs) -> List[Dict[str, Any]]:
        """
        Discovers candidate documents, clinical trials, or codex entries matching the query.
        """
        pass

    @abstractmethod
    async def identify(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Resolves an exact identifier (DOI, PMID, NCT ID, ISBN, Codex ID) to a canonical record.
        """
        pass

    @abstractmethod
    async def fetch_metadata(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves bibliographic or registry metadata without full-text payload.
        """
        pass

    @abstractmethod
    async def fetch_document(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Acquires document payload, strictly respecting license boundaries and Class C quarantine.
        """
        pass

    @abstractmethod
    async def fetch_updates(self, since: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Retrieves updated, retracted, or newly published records since a timestamp.
        """
        pass

    def check_access(self, identifier: str) -> bool:
        """
        Validates if ZMIE has authenticated or open access to this document.
        """
        return True

    def check_license(self, raw_license: Optional[str], is_oa: bool = False, full_text_contract: bool = False) -> LicenseClass:
        """
        Determines legal storage class (Class A, Class B, Class C) via LicensingIntelligenceEngine.
        """
        return LicensingIntelligenceEngine.evaluate_license(
            raw_license_str=raw_license,
            is_oa=is_oa,
            full_text_contract=full_text_contract
        )

    @abstractmethod
    def normalize(self, raw_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts provider-specific data into ZMIE canonical schema and enforces license quarantine.
        """
        pass

    def report_status(self) -> Dict[str, Any]:
        """
        Reports operational health, error budgets, and connector telemetry.
        """
        status_val = SourceStatus.RECOGNIZED.value if self.error_count == 0 else SourceStatus.UNVERIFIED.value
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "authority_tier": self.authority_tier.value,
            "status": status_val,
            "requests_made": self.request_count,
            "errors_encountered": self.error_count,
            "last_sync": self.last_sync_time.isoformat() if self.last_sync_time else None
        }
