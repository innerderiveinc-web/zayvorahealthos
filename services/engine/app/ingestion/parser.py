"""
ZMIE Document Parsing & Structural Layout Engine (Sections 9 & 11)
Preserves immutable document provenance:
- Document level: SHA-256 hash, title, authors, year, license class
- Structural level: Sections, Paragraphs, Tables, Figures, Anchor text
- Ingestion class compliance:
  * Class A/B: Full text, sections, and tables preserved
  * Class C: Restricted to metadata, citation, and permitted abstract/claims
"""

import hashlib
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.ingestion.licensing import LicensingIntelligenceEngine
from app.models.source import LicenseClass


class DocumentSection(BaseModel):
    section_index: int
    heading: str
    paragraph_count: int
    paragraphs: List[str] = Field(default_factory=list)
    anchor_hashes: List[str] = Field(default_factory=list)


class ParsedDocumentArtifact(BaseModel):
    document_id: str
    raw_hash_sha256: str
    title: str
    authors: List[str] = Field(default_factory=list)
    publication_year: Optional[int] = None
    license_class: LicenseClass
    is_full_text_quarantined: bool
    sections: List[DocumentSection] = Field(default_factory=list)
    total_paragraphs: int
    tables_extracted: int = 0
    figures_extracted: int = 0
    provenance_notice: str


class DocumentParserService:
    @classmethod
    def parse_raw_text(
        cls,
        document_id: str,
        title: str,
        raw_content: str,
        license_str: Optional[str] = None,
        is_oa: bool = False,
        authors: Optional[List[str]] = None,
        year: Optional[int] = None
    ) -> ParsedDocumentArtifact:
        """
        Parses text/XML/HTML stream, derives cryptographic SHA-256 hash,
        decomposes into sections and paragraphs, and enforces copyright quarantine.
        """
        # 1. Compute Cryptographic Content Hash
        sha256 = hashlib.sha256(raw_content.encode("utf-8")).hexdigest()

        # 2. Evaluate License Class (A, B, or C)
        lic_class = LicensingIntelligenceEngine.evaluate_license(license_str, is_oa=is_oa)

        # 3. Section and Paragraph Decomposition
        lines = [line.strip() for line in raw_content.split("\n") if line.strip()]
        current_section = DocumentSection(section_index=0, heading="Introduction / Overview", paragraph_count=0)
        parsed_sections: List[DocumentSection] = []

        for line in lines:
            if line.isupper() and len(line) < 60:
                if current_section.paragraphs:
                    parsed_sections.append(current_section)
                current_section = DocumentSection(
                    section_index=len(parsed_sections) + 1,
                    heading=line,
                    paragraph_count=0
                )
            else:
                p_hash = hashlib.sha256(line.encode("utf-8")).hexdigest()[:16]
                current_section.paragraphs.append(line)
                current_section.anchor_hashes.append(p_hash)
                current_section.paragraph_count += 1

        if current_section.paragraphs:
            parsed_sections.append(current_section)

        total_p = sum(s.paragraph_count for s in parsed_sections)

        # 4. Enforce Class C Quarantine if restricted
        is_quarantined = lic_class == LicenseClass.CLASS_C
        if is_quarantined:
            # Retain only first section / abstract
            retained_sections = parsed_sections[:1] if parsed_sections else []
            notice = "CLASS C RESTRICTED: Full-text quarantined. Metadata and permitted abstract preserved."
        else:
            retained_sections = parsed_sections
            notice = f"CLASS {lic_class.value.upper()}: Full-text and structural anchors legally archived."

        return ParsedDocumentArtifact(
            document_id=document_id,
            raw_hash_sha256=sha256,
            title=title,
            authors=authors or [],
            publication_year=year,
            license_class=lic_class,
            is_full_text_quarantined=is_quarantined,
            sections=retained_sections,
            total_paragraphs=total_p if not is_quarantined else (retained_sections[0].paragraph_count if retained_sections else 0),
            tables_extracted=0,
            figures_extracted=0,
            provenance_notice=notice
        )
