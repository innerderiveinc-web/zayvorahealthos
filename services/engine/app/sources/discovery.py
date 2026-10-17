"""
ZMIE Universal Source Discovery Engine
Discovers, classifies, and evaluates candidate medical sources from:
- Citation networks & Crossref references
- Publisher catalogs & institutional repositories
- Failed search demand signals
- Research gap engine triggers
Enforces the rule: Discovery does not equal acceptance; candidates require governance review.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from app.models.source_universe import (
    DiscoveryCandidate, SourceRecord, SourceClass, MedicalSystem,
    AuthorityLevel, LicenseStatus, InclusionStatus
)
from app.sources.registry import SourceUniverseRegistry


class SourceDiscoveryEngine:
    """
    Manages the continuous source discovery pipeline and candidate queue.
    """

    _discovery_queue: Dict[str, DiscoveryCandidate] = {}

    @classmethod
    def initialize_defaults(cls):
        if cls._discovery_queue:
            return

        # Pre-seed candidate discovery queue with authentic candidates
        candidates = [
            DiscoveryCandidate(
                candidate_id="CAND-DISC-01",
                candidate_name="Journal of Ethnopharmacology (Elsevier)",
                candidate_url="https://www.sciencedirect.com/journal/journal-of-ethnopharmacology",
                discovered_from="citation_network",
                discovery_method="Crossref bibliographic reference extraction",
                domain="sciencedirect.com",
                country="Netherlands",
                language="en",
                suspected_publisher="Elsevier BV",
                medical_system=MedicalSystem.INTEGRATIVE,
                source_class=SourceClass.SCHOLARLY_LITERATURE,
                confidence=0.95,
                detected_api="https://api.elsevier.com/content/search/sciencedirect",
                detected_license="Subscription / Hybrid OA (Requires Scopus/API key)",
                review_state="PENDING_REVIEW"
            ),
            DiscoveryCandidate(
                candidate_id="CAND-DISC-02",
                candidate_name="Hamdard Medicus (Quarterly Journal of Science & Medicine)",
                candidate_url="https://hamdardmedicus.com.pk",
                discovered_from="research_gap",
                discovery_method="Unani research gap analysis: clinical Unani literature underrepresented",
                domain="hamdardmedicus.com.pk",
                country="Pakistan",
                language="en",
                suspected_publisher="Bait al-Hikmah / Hamdard Foundation",
                medical_system=MedicalSystem.UNANI,
                source_class=SourceClass.TRADITIONAL_MEDICINE,
                confidence=0.91,
                detected_api="OAI-PMH XML Endpoint",
                detected_license="Open Access (CC-BY-NC)",
                review_state="PENDING_REVIEW"
            ),
            DiscoveryCandidate(
                candidate_id="CAND-DISC-03",
                candidate_name="Chinese Clinical Trial Registry (ChiCTR)",
                candidate_url="https://www.chictr.org.cn",
                discovered_from="clinical_trials_network",
                discovery_method="WHO ICTRP primary registry audit",
                domain="chictr.org.cn",
                country="China",
                language="zh",
                suspected_publisher="West China Hospital, Sichuan University",
                medical_system=MedicalSystem.TCM,
                source_class=SourceClass.CLINICAL_TRIALS,
                confidence=0.98,
                detected_api="REST / XML Registry Export",
                detected_license="Public Domain / WHO Open Trial Policy",
                review_state="PENDING_REVIEW"
            )
        ]
        for c in candidates:
            cls._discovery_queue[c.candidate_id] = c

    @classmethod
    def discover_from_citation(cls, cited_journal_or_url: str, citing_source_id: str) -> DiscoveryCandidate:
        """
        Discovers a candidate source from citations in newly ingested documents.
        """
        cand_id = f"cand-{uuid.uuid4().hex[:8]}"
        domain_name = cited_journal_or_url.split("//")[-1].split("/")[0] if "//" in cited_journal_or_url else "scholarly.org"
        
        # Categorize system
        med_sys = MedicalSystem.MODERN
        s_class = SourceClass.SCHOLARLY_LITERATURE
        lower_name = cited_journal_or_url.lower()
        if "unani" in lower_name or "tibb" in lower_name:
            med_sys = MedicalSystem.UNANI
            s_class = SourceClass.TRADITIONAL_MEDICINE
        elif "ayurved" in lower_name:
            med_sys = MedicalSystem.AYURVEDA
            s_class = SourceClass.TRADITIONAL_MEDICINE
        elif "trial" in lower_name:
            s_class = SourceClass.CLINICAL_TRIALS

        cand = DiscoveryCandidate(
            candidate_id=cand_id,
            candidate_name=cited_journal_or_url,
            candidate_url=f"https://{domain_name}",
            discovered_from="citation_network",
            discovery_method=f"Cited by documents in source [{citing_source_id}]",
            domain=domain_name,
            medical_system=med_sys,
            source_class=s_class,
            confidence=0.88,
            review_state="PENDING_REVIEW"
        )
        cls._discovery_queue[cand_id] = cand
        return cand

    @classmethod
    def discover_from_search_gap(cls, query: str, search_miss_reason: str) -> DiscoveryCandidate:
        """
        Triggers candidate discovery when searches repeatedly experience domain gaps.
        """
        cand_id = f"cand-{uuid.uuid4().hex[:8]}"
        med_sys = MedicalSystem.UNANI if "mizaj" in query.lower() or "unani" in query.lower() else MedicalSystem.MODERN

        cand = DiscoveryCandidate(
            candidate_id=cand_id,
            candidate_name=f"Specialized Repository for '{query}'",
            candidate_url=f"https://discovery.zmie.org/gap-fill/{uuid.uuid4().hex[:6]}",
            discovered_from="failed_search",
            discovery_method=f"Demand gap signal: {search_miss_reason}",
            domain="zmie-gap-fill.org",
            medical_system=med_sys,
            source_class=SourceClass.TRADITIONAL_MEDICINE if med_sys == MedicalSystem.UNANI else SourceClass.SCHOLARLY_LITERATURE,
            confidence=0.75,
            review_state="PENDING_REVIEW"
        )
        cls._discovery_queue[cand_id] = cand
        return cand

    @classmethod
    def list_candidates(cls) -> List[DiscoveryCandidate]:
        cls.initialize_defaults()
        return list(cls._discovery_queue.values())

    @classmethod
    def get_candidate(cls, candidate_id: str) -> Optional[DiscoveryCandidate]:
        cls.initialize_defaults()
        return cls._discovery_queue.get(candidate_id)

    @classmethod
    def approve_candidate(cls, candidate_id: str, authority_tier: AuthorityLevel = AuthorityLevel.S3_PEER_REVIEWED) -> Optional[SourceRecord]:
        """
        Human / Governance board approval promoting candidate into the SourceUniverseRegistry.
        """
        cand = cls.get_candidate(candidate_id)
        if not cand:
            return None

        cand.review_state = "APPROVED"
        source_id = f"SRC-DISC-{uuid.uuid4().hex[:6].upper()}"

        source_rec = SourceRecord(
            source_id=source_id,
            source_name=cand.candidate_name,
            canonical_url=cand.candidate_url,
            source_type="discovered_repository",
            source_class=cand.source_class,
            country=cand.country,
            languages=[cand.language],
            medical_systems=[cand.medical_system],
            authority_level=authority_tier,
            api_available=bool(cand.detected_api),
            api_url=cand.detected_api,
            license_status=LicenseStatus.METADATA_ONLY,
            inclusion_status=InclusionStatus.APPROVED,
            created_at=datetime.utcnow()
        )
        SourceUniverseRegistry.register_source(source_rec)
        return source_rec

    @classmethod
    def reject_candidate(cls, candidate_id: str, reason: str) -> bool:
        cand = cls.get_candidate(candidate_id)
        if not cand:
            return False
        cand.review_state = "REJECTED"
        return True


# Auto-initialize
SourceDiscoveryEngine.initialize_defaults()
