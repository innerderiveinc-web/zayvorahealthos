"""
ZMIE Licensing Intelligence Engine
Classifies scholarly and medical content into Storage & Analysis Classes:
- Class A: Full-Text Licensed (Commercial/Proprietary/Internal institutional license)
- Class B: Permitted Open Access (CC-BY, CC0, Public Domain, etc.)
- Class C: Restricted (Metadata + Abstract + Extracted Facts snippet + Outward Link only)
"""

from typing import Dict, Any, Optional
from app.models.source import LicenseClass


class LicensingIntelligenceEngine:
    # Standard Open Access licenses that allow full-text derivative extraction
    PERMITTED_OA_LICENSES = {
        "cc-by", "cc-by-4.0", "cc-by-3.0", "cc-by-2.0",
        "cc0", "public domain", "cc-by-sa", "cc-by-sa-4.0",
        "open-access", "gold"
    }

    # Restrictive licenses where only metadata/snippets are legally indexed
    RESTRICTED_LICENSES = {
        "all-rights-reserved", "cc-by-nc-nd", "closed", "subscription"
    }

    @classmethod
    def evaluate_license(cls, raw_license_str: Optional[str], is_oa: bool = False, full_text_contract: bool = False) -> LicenseClass:

        """
        Determines the ZMIE legal ingestion class for any document artifact.
        """
        if full_text_contract:
            return LicenseClass.CLASS_A

        if not raw_license_str:
            if is_oa:
                return LicenseClass.CLASS_B
            return LicenseClass.CLASS_C

        normalized_license = raw_license_str.strip().lower()

        for oa_lic in cls.PERMITTED_OA_LICENSES:
            if oa_lic in normalized_license:
                return LicenseClass.CLASS_B

        return LicenseClass.CLASS_C

    @classmethod
    def filter_storage_payload(cls, document_data: Dict[str, Any], license_class: LicenseClass) -> Dict[str, Any]:
        """
        Guarantees copyright compliance before archiving or passing to indexing pipelines.
        """
        sanitized = {
            "title": document_data.get("title"),
            "doi": document_data.get("doi"),
            "pmid": document_data.get("pmid"),
            "authors": document_data.get("authors"),
            "publication_year": document_data.get("publication_year"),
            "source_id": document_data.get("source_id"),
            "license_class": license_class.value,
            "external_url": document_data.get("external_url")
        }

        if license_class in (LicenseClass.CLASS_A, LicenseClass.CLASS_B):
            # Full text & section paragraphs permitted
            sanitized["full_text"] = document_data.get("full_text")
            sanitized["sections"] = document_data.get("sections")
            sanitized["tables"] = document_data.get("tables")
        else:
            # Class C: Permitted abstract, claims, and external citation link only
            sanitized["abstract"] = document_data.get("abstract")
            sanitized["full_text"] = None
            sanitized["sections"] = []
            sanitized["notice"] = "Class C: Full text restricted under publisher copyright. Stored as metadata + atomic extracted claims."

        return sanitized
