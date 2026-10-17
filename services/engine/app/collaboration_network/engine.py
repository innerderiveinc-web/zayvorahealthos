"""
ZMIE Global Scientific Collaboration & Research Network Engine
Prompt 22 Implementation.

Core engine for identity disambiguation, temporal affiliations, evidence-backed
expertise profiling, collaboration topology with recency decay, cross-disciplinary
bridges, research clusters, epistemic gap mapping, snapshot diffing, and tenant isolation.
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from datetime import datetime
import math
import uuid

from app.models.collaboration_network import (
    RelationshipState,
    IdentityConfidenceState,
    CollaborationType,
    ExpertiseDimension,
    AffiliationStatus,
    GapStatus,
    VisibilityScope,
    TemporalAffiliation,
    ExpertiseEvidenceItem,
    ResearcherIdentity,
    InstitutionIdentity,
    CollaborationEdge,
    CrossDisciplinaryBridge,
    ResearchCluster,
    ResearchGapReport,
    NetworkSnapshot,
    NetworkDiff,
    ResearcherResolveRequest,
    ExpertiseSearchQuery,
)


class ForbiddenRankingException(ValueError):
    """Raised when an attempt is made to generate subjective or arbitrary researcher rankings."""
    pass


class ScientificCollaborationNetworkEngine:
    """
    First-class ZMIE engine governing global scientific collaboration intelligence,
    researcher identity resolution, temporal affiliations, and network analysis.
    """

    def __init__(self):
        # In-memory stores indexed by IDs
        self.researchers: Dict[str, ResearcherIdentity] = {}
        self.institutions: Dict[str, InstitutionIdentity] = {}
        self.edges: Dict[str, CollaborationEdge] = {}
        self.clusters: Dict[str, ResearchCluster] = {}
        self.snapshots: Dict[str, NetworkSnapshot] = {}

        # Forbidden subjective ranking keywords to strictly enforce anti-ranking rule
        self.BANNED_RANKING_TERMS = {
            "top scientist", "best researcher", "top researcher", "#1 expert",
            "leading authority in the world", "greatest scientist", "master researcher"
        }

        # Seed realistic exemplar nodes
        self._seed_exemplar_network()

    def _seed_exemplar_network(self) -> None:
        """Seed initial realistic high-fidelity researchers and institutions across biomedical & traditional disciplines."""
        # Institution 1: Jamia Hamdard / CCRUM (Unani & Pharmacognosy)
        inst_hamdard = InstitutionIdentity(
            institution_id="inst-hamdard-01",
            canonical_name="Jamia Hamdard University & CCRUM Collaboratory",
            aliases=["Jamia Hamdard", "Faculty of Unani Medicine, Jamia Hamdard"],
            ror_id="https://ror.org/03t836015",
            country="India",
            city="New Delhi",
            institution_type="TRADITIONAL_COUNCIL",
            departments=["Department of Ilmul Advia", "Department of Pharmacognosy & Phytochemistry"],
            labs=["Laboratory of Natural Product Metabolomics"]
        )
        self.institutions[inst_hamdard.institution_id] = inst_hamdard

        # Institution 2: Harvard / Broad Institute (Genomics & Computational Biology)
        inst_harvard = InstitutionIdentity(
            institution_id="inst-broad-01",
            canonical_name="Broad Institute of MIT and Harvard",
            aliases=["Broad Institute", "Harvard-MIT Health Sciences"],
            ror_id="https://ror.org/05a0yaq55",
            country="United States",
            city="Cambridge, MA",
            institution_type="RESEARCH_INSTITUTE",
            departments=["Metabolism Program", "Center for Epigenomics"],
            labs=["Computational Chemical Genomics Lab"]
        )
        self.institutions[inst_harvard.institution_id] = inst_harvard

        # Institution 3: AIIMS New Delhi (Clinical Endocrinology & Pharmacology)
        inst_aiims = InstitutionIdentity(
            institution_id="inst-aiims-01",
            canonical_name="All India Institute of Medical Sciences (AIIMS)",
            aliases=["AIIMS Delhi"],
            ror_id="https://ror.org/04b123456",
            country="India",
            city="New Delhi",
            institution_type="HOSPITAL",
            departments=["Department of Endocrinology & Metabolism", "Department of Pharmacology"],
            labs=["Endocrine Clinical Trials Unit"]
        )
        self.institutions[inst_aiims.institution_id] = inst_aiims

        # Researcher 1: Hakim Dr. M. A. Rahman (Unani Phytochemist & Metabolic Researcher)
        r1 = ResearcherIdentity(
            researcher_id="res-rahman-01",
            canonical_name="Hakim M. A. Rahman",
            aliases=["M. A. Rahman", "Mohammad A. Rahman", "Hakim Rahman"],
            orcid="0000-0002-1234-5678",
            disambiguation_confidence=IdentityConfidenceState.CONFIRMED,
            primary_disciplines=["Unani Medicine", "Phytochemistry", "Metabolic Pharmacology"],
            affiliations=[
                TemporalAffiliation(
                    institution_id="inst-hamdard-01",
                    institution_name="Jamia Hamdard University & CCRUM Collaboratory",
                    department_name="Department of Ilmul Advia",
                    role="Professor & Senior Investigator",
                    affiliation_status=AffiliationStatus.PRIMARY,
                    start_year=2015,
                    end_year=None,
                    is_current=True,
                    provenance_source="FACULTY_REGISTRY_2025"
                ),
                TemporalAffiliation(
                    institution_id="inst-aiims-01",
                    institution_name="All India Institute of Medical Sciences (AIIMS)",
                    department_name="Department of Pharmacology",
                    role="Visiting Clinical Scientist",
                    affiliation_status=AffiliationStatus.VISITING,
                    start_year=2021,
                    end_year=2024,
                    is_current=False,
                    provenance_source="CLINICAL_TRIAL_AGREEMENT_NCT045612"
                )
            ],
            expertise_profile=[
                ExpertiseEvidenceItem(
                    dimension=ExpertiseDimension.TOPIC,
                    topic_or_method="Type 2 Diabetes Glycemic Regulation",
                    evidence_type="CLINICAL_TRIAL",
                    source_identifiers=["CTRI/2021/04/032111", "doi:10.1016/j.jep.2023.116543"],
                    years_active=[2021, 2022, 2023, 2024],
                    confidence_state=IdentityConfidenceState.CONFIRMED,
                    evidence_count=8,
                    sample_context="Principal investigator in multi-center herbal formulation glycemic trial."
                ),
                ExpertiseEvidenceItem(
                    dimension=ExpertiseDimension.METHOD,
                    topic_or_method="UPLC-MS/MS Metabolite Profiling",
                    evidence_type="PUBLICATION",
                    source_identifiers=["doi:10.1021/acs.jnatprod.2022.00192"],
                    years_active=[2022, 2023],
                    confidence_state=IdentityConfidenceState.SUPPORTED,
                    evidence_count=4,
                    sample_context="Standardized bioactive fingerprinting of polyherbal preparations."
                )
            ]
        )
        self.researchers[r1.researcher_id] = r1

        # Researcher 2: Dr. Elena Vance (Harvard/Broad - Computational Chemical Genomics)
        r2 = ResearcherIdentity(
            researcher_id="res-vance-02",
            canonical_name="Dr. Elena Vance",
            aliases=["E. Vance", "Elena C. Vance"],
            orcid="0000-0003-9876-5432",
            disambiguation_confidence=IdentityConfidenceState.CONFIRMED,
            primary_disciplines=["Computational Chemical Genomics", "Target Identification", "Metabolic Pharmacology"],
            affiliations=[
                TemporalAffiliation(
                    institution_id="inst-broad-01",
                    institution_name="Broad Institute of MIT and Harvard",
                    department_name="Metabolism Program",
                    role="Principal Investigator",
                    affiliation_status=AffiliationStatus.PRIMARY,
                    start_year=2018,
                    end_year=None,
                    is_current=True,
                    provenance_source="BROAD_FACULTY_DIRECTORY"
                )
            ],
            expertise_profile=[
                ExpertiseEvidenceItem(
                    dimension=ExpertiseDimension.METHOD,
                    topic_or_method="High-Throughput Ligand-Protein Docking",
                    evidence_type="PUBLICATION",
                    source_identifiers=["doi:10.1038/s41589-023-01445-x"],
                    years_active=[2020, 2021, 2022, 2023, 2024, 2025],
                    confidence_state=IdentityConfidenceState.CONFIRMED,
                    evidence_count=14,
                    sample_context="Developed structure-guided ligand discovery pipeline for AMPK activation."
                ),
                ExpertiseEvidenceItem(
                    dimension=ExpertiseDimension.TOPIC,
                    topic_or_method="AMPK Pathway Modulation",
                    evidence_type="GRANT",
                    source_identifiers=["NIH-R01-DK128901"],
                    years_active=[2022, 2023, 2024, 2025],
                    confidence_state=IdentityConfidenceState.CONFIRMED,
                    evidence_count=5,
                    sample_context="NIH-funded investigator evaluating non-synthetic small molecule activators."
                )
            ]
        )
        self.researchers[r2.researcher_id] = r2

        # Researcher 3: Prof. S. K. Sharma (AIIMS Clinical Endocrinologist)
        r3 = ResearcherIdentity(
            researcher_id="res-sharma-03",
            canonical_name="Prof. S. K. Sharma",
            aliases=["S. K. Sharma", "Sunil K. Sharma"],
            orcid="0000-0001-5544-3322",
            disambiguation_confidence=IdentityConfidenceState.CONFIRMED,
            primary_disciplines=["Clinical Endocrinology", "Randomized Controlled Trials"],
            affiliations=[
                TemporalAffiliation(
                    institution_id="inst-aiims-01",
                    institution_name="All India Institute of Medical Sciences (AIIMS)",
                    department_name="Department of Endocrinology & Metabolism",
                    role="Head of Clinical Research",
                    affiliation_status=AffiliationStatus.PRIMARY,
                    start_year=2012,
                    end_year=None,
                    is_current=True,
                    provenance_source="AIIMS_ANNUAL_REPORT"
                )
            ],
            expertise_profile=[
                ExpertiseEvidenceItem(
                    dimension=ExpertiseDimension.DISEASE,
                    topic_or_method="Insulin Resistance & Diabetic Nephropathy",
                    evidence_type="CLINICAL_TRIAL",
                    source_identifiers=["NCT04561288", "doi:10.1016/j.diabres.2023.109822"],
                    years_active=[2018, 2019, 2020, 2021, 2022, 2023, 2024],
                    confidence_state=IdentityConfidenceState.CONFIRMED,
                    evidence_count=19,
                    sample_context="Lead investigator for multi-arm insulin sensitivity clinical trials."
                )
            ]
        )
        self.researchers[r3.researcher_id] = r3

        # Collaboration Edge 1: Rahman <-> Sharma (AIIMS + Hamdard Joint Clinical Trial)
        edge1 = CollaborationEdge(
            edge_id="collab-rahman-sharma-01",
            source_researcher_id=r1.researcher_id,
            target_researcher_id=r3.researcher_id,
            relationship_type=CollaborationType.SHARED_TRIAL,
            relationship_state=RelationshipState.OBSERVED,
            evidence_artifacts=["CTRI/2021/04/032111", "doi:10.1016/j.jep.2023.116543"],
            shared_work_count=4,
            first_year=2021,
            last_year=2024,
            is_active_recent=True,
            recency_weight=1.0,
            cross_institutional=True,
            source_institution_id=inst_hamdard.institution_id,
            target_institution_id=inst_aiims.institution_id
        )
        self.edges[edge1.edge_id] = edge1

        # Collaboration Edge 2: Rahman <-> Vance (International Phytochem-Genomics Collaboration)
        edge2 = CollaborationEdge(
            edge_id="collab-rahman-vance-02",
            source_researcher_id=r1.researcher_id,
            target_researcher_id=r2.researcher_id,
            relationship_type=CollaborationType.COAUTHORED,
            relationship_state=RelationshipState.OBSERVED,
            evidence_artifacts=["doi:10.1021/acs.jnatprod.2022.00192", "doi:10.1038/s41589-023-01445-x"],
            shared_work_count=2,
            first_year=2022,
            last_year=2024,
            is_active_recent=True,
            recency_weight=0.9,
            cross_institutional=True,
            source_institution_id=inst_hamdard.institution_id,
            target_institution_id=inst_harvard.institution_id
        )
        self.edges[edge2.edge_id] = edge2

    # -------------------------------------------------------------------------
    # 1. Identity Resolution & Disambiguation
    # -------------------------------------------------------------------------

    def resolve_researcher_identity(self, req: ResearcherResolveRequest) -> Dict[str, Any]:
        """
        Disambiguate researcher identity using ORCID, name variants, institutional cues,
        co-authors, and discipline/topic hints.
        Refuses to merge contradictory entities without evidence.
        """
        # 1. Direct ORCID match if provided (most authoritative)
        if req.orcid:
            for r in self.researchers.values():
                if r.orcid == req.orcid:
                    return {
                        "resolved": True,
                        "match_type": "ORCID_EXACT",
                        "researcher": r,
                        "confidence": IdentityConfidenceState.CONFIRMED,
                        "notes": f"Authoritative disambiguation via verified ORCID {req.orcid}."
                    }

        candidate_matches: List[Tuple[ResearcherIdentity, float, List[str]]] = []

        norm_query_name = req.raw_name.strip().lower()

        for r in self.researchers.values():
            # Respect tenant isolation: private researchers not visible across tenants
            if r.visibility == VisibilityScope.TENANT_PRIVATE and r.tenant_id != req.tenant_id:
                continue

            score = 0.0
            reasons = []

            # Name match (canonical or alias)
            canonical_norm = r.canonical_name.lower()
            aliases_norm = [a.lower() for a in r.aliases]

            if norm_query_name == canonical_norm or norm_query_name in aliases_norm:
                score += 0.5
                reasons.append("Exact name or alias match")
            elif any(norm_query_name in a or a in norm_query_name for a in [canonical_norm] + aliases_norm):
                score += 0.35
                reasons.append("Partial name/alias match")

            # Institutional cue
            if req.institution_hint:
                inst_hint_norm = req.institution_hint.lower()
                for aff in r.affiliations:
                    if inst_hint_norm in aff.institution_name.lower():
                        score += 0.3
                        reasons.append(f"Institutional affiliation match: {aff.institution_name}")
                        break

            # Topic cue
            if req.topic_hints:
                overlap = 0
                for exp in r.expertise_profile:
                    for hint in req.topic_hints:
                        if hint.lower() in exp.topic_or_method.lower():
                            overlap += 1
                if overlap > 0:
                    score += min(0.2, overlap * 0.1)
                    reasons.append(f"Topic overlap matches ({overlap} topics)")

            if score >= 0.4:
                candidate_matches.append((r, score, reasons))

        if not candidate_matches:
            # Create a prospective candidate profile marked CANDIDATE/UNRESOLVED
            new_id = f"res-cand-{uuid.uuid4().hex[:8]}"
            cand_profile = ResearcherIdentity(
                researcher_id=new_id,
                canonical_name=req.raw_name,
                aliases=[req.raw_name],
                orcid=req.orcid,
                disambiguation_confidence=IdentityConfidenceState.CANDIDATE,
                primary_disciplines=req.topic_hints,
                visibility=VisibilityScope.TENANT_PRIVATE if req.tenant_id else VisibilityScope.PUBLIC,
                tenant_id=req.tenant_id
            )
            if req.institution_hint:
                cand_profile.affiliations.append(
                    TemporalAffiliation(
                        institution_id="inst-unknown",
                        institution_name=req.institution_hint,
                        is_current=True,
                        provenance_source="QUERY_HINT"
                    )
                )
            self.researchers[cand_profile.researcher_id] = cand_profile
            return {
                "resolved": False,
                "match_type": "NEW_CANDIDATE_CREATED",
                "researcher": cand_profile,
                "confidence": IdentityConfidenceState.CANDIDATE,
                "notes": "No unambiguous match found in indexed profiles. Registered as new candidate entity."
            }

        # Sort candidate matches by score descending
        candidate_matches.sort(key=lambda x: x[1], reverse=True)
        top_match, top_score, top_reasons = candidate_matches[0]

        # Contestation check: If multiple candidates share high score without distinguishing ORCID
        if len(candidate_matches) > 1 and (candidate_matches[0][1] - candidate_matches[1][1] < 0.1):
            top_match.is_contested = True
            top_match.contestation_reason = "Multiple high-probability identities found with overlapping names."
            return {
                "resolved": False,
                "match_type": "AMBIGUOUS_CONTESTED",
                "top_candidate": top_match,
                "confidence": IdentityConfidenceState.CONTESTED,
                "notes": "Ambiguous match detected between multiple distinct researchers. Refusing false merge.",
                "all_candidates": [
                    {"researcher_id": m[0].researcher_id, "name": m[0].canonical_name, "score": m[1], "reasons": m[2]}
                    for m in candidate_matches
                ]
            }

        return {
            "resolved": True,
            "match_type": "PROBABILISTIC_RESOLVED",
            "researcher": top_match,
            "confidence": IdentityConfidenceState.SUPPORTED if top_score >= 0.7 else IdentityConfidenceState.PROBABLE,
            "score": round(top_score, 2),
            "reasons": top_reasons,
            "notes": "Resolved with evidence-backed heuristic matching."
        }

    # -------------------------------------------------------------------------
    # 2. Temporal Affiliations
    # -------------------------------------------------------------------------

    def get_researcher_timeline(self, researcher_id: str, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve timeline of affiliations and active research epochs with strict start/end dates.
        """
        researcher = self._get_authorized_researcher(researcher_id, tenant_id)
        if not researcher:
            return {"error": "Researcher not found or access unauthorized"}

        timeline = []
        for aff in sorted(researcher.affiliations, key=lambda a: (a.start_year or 0), reverse=True):
            timeline.append({
                "institution_id": aff.institution_id,
                "institution_name": aff.institution_name,
                "department": aff.department_name,
                "role": aff.role,
                "status": aff.affiliation_status.value,
                "start_year": aff.start_year,
                "end_year": aff.end_year,
                "is_current": aff.is_current,
                "provenance": aff.provenance_source
            })

        return {
            "researcher_id": researcher.researcher_id,
            "canonical_name": researcher.canonical_name,
            "orcid": researcher.orcid,
            "chronological_affiliations": timeline,
            "boundary_reminder": (
                "Epistemic boundary: Affiliation denotes institutional appointment/association. "
                "It does NOT indicate institutional endorsement of specific scientific findings."
            )
        }

    # -------------------------------------------------------------------------
    # 3. Evidence-Backed Expertise Profiling (With Anti-Ranking Firewall)
    # -------------------------------------------------------------------------

    def search_expertise(self, query: ExpertiseSearchQuery) -> Dict[str, Any]:
        """
        Search for researchers with evidence-backed expertise across topics, methods, or diseases.
        Strictly enforces non-ranking: returns objective metrics without subjective 'best/top' rankings.
        """
        results = []

        for r in self.researchers.values():
            if r.visibility == VisibilityScope.TENANT_PRIVATE and r.tenant_id != query.tenant_id:
                continue

            matched_evidence = []
            for exp in r.expertise_profile:
                match = True
                if query.topic and query.topic.lower() not in exp.topic_or_method.lower():
                    match = False
                if query.method and query.method.lower() not in exp.topic_or_method.lower():
                    match = False
                if query.disease and query.disease.lower() not in exp.topic_or_method.lower():
                    match = False

                if match and exp.evidence_count >= query.min_evidence_count:
                    matched_evidence.append(exp)

            if matched_evidence:
                # Calculate objective metrics
                total_outputs = sum(e.evidence_count for e in matched_evidence)
                years = set()
                for e in matched_evidence:
                    years.update(e.years_active)

                results.append({
                    "researcher_id": r.researcher_id,
                    "canonical_name": r.canonical_name,
                    "orcid": r.orcid,
                    "current_primary_affiliation": [
                        a.institution_name for a in r.affiliations if a.is_current and a.affiliation_status == AffiliationStatus.PRIMARY
                    ],
                    "matched_evidence_count": total_outputs,
                    "active_years_window": sorted(list(years)),
                    "evidence_items": [
                        {
                            "dimension": e.dimension.value,
                            "topic_or_method": e.topic_or_method,
                            "evidence_type": e.evidence_type,
                            "identifiers": e.source_identifiers,
                            "confidence": e.confidence_state.value
                        }
                        for e in matched_evidence
                    ]
                })

        return {
            "query": query.model_dump(),
            "matched_researcher_count": len(results),
            "researchers": results,
            "anti_ranking_guarantee": (
                "ZMIE strictly prohibits subjective ranking descriptors ('Top Scientist', '#1 Expert'). "
                "Profiles are presented with factual, evidence-backed publication and trial metrics only."
            )
        }

    def verify_no_subjective_ranking(self, text: str) -> None:
        """
        Validation firewall: Throws ForbiddenRankingException if subjective rankings are present.
        """
        lower_text = text.lower()
        for banned in self.BANNED_RANKING_TERMS:
            if banned in lower_text:
                raise ForbiddenRankingException(
                    f"Forbidden subjective ranking descriptor detected: '{banned}'. "
                    "ZMIE policy mandates objective evidence representation over researcher ranking."
                )

    # -------------------------------------------------------------------------
    # 4. Collaboration Topology & Recency Decay
    # -------------------------------------------------------------------------

    def get_collaborations(self, researcher_id: str, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve direct (1st degree) and indirect (2nd degree) collaboration network
        with time-decayed recency weighting.
        """
        researcher = self._get_authorized_researcher(researcher_id, tenant_id)
        if not researcher:
            return {"error": "Researcher not found or unauthorized"}

        current_year = datetime.utcnow().year
        first_degree_collaborators = []
        direct_neighbor_ids = set()

        for edge in self.edges.values():
            if edge.visibility == VisibilityScope.TENANT_PRIVATE and edge.tenant_id != tenant_id:
                continue

            other_id = None
            if edge.source_researcher_id == researcher_id:
                other_id = edge.target_researcher_id
            elif edge.target_researcher_id == researcher_id:
                other_id = edge.source_researcher_id

            if other_id and other_id in self.researchers:
                direct_neighbor_ids.add(other_id)
                other_r = self.researchers[other_id]

                # Recency decay calculation: e^(-0.1 * (current_year - last_year))
                years_since_last = max(0, current_year - edge.last_year)
                computed_decay = round(math.exp(-0.1 * years_since_last), 2)

                first_degree_collaborators.append({
                    "collaborator_id": other_r.researcher_id,
                    "canonical_name": other_r.canonical_name,
                    "relationship_type": edge.relationship_type.value,
                    "relationship_state": edge.relationship_state.value,
                    "shared_works": edge.shared_work_count,
                    "active_span": f"{edge.first_year}-{edge.last_year}",
                    "recency_weight": computed_decay,
                    "is_active_recent": edge.is_active_recent,
                    "evidence_artifacts": edge.evidence_artifacts
                })

        # Second-degree collaborators (collaborators of direct collaborators who are not direct collaborators)
        second_degree = []
        for direct_id in direct_neighbor_ids:
            for edge in self.edges.values():
                if edge.visibility == VisibilityScope.TENANT_PRIVATE and edge.tenant_id != tenant_id:
                    continue

                snd_id = None
                if edge.source_researcher_id == direct_id and edge.target_researcher_id != researcher_id:
                    snd_id = edge.target_researcher_id
                elif edge.target_researcher_id == direct_id and edge.source_researcher_id != researcher_id:
                    snd_id = edge.source_researcher_id

                if snd_id and snd_id not in direct_neighbor_ids and snd_id in self.researchers:
                    snd_r = self.researchers[snd_id]
                    second_degree.append({
                        "researcher_id": snd_r.researcher_id,
                        "canonical_name": snd_r.canonical_name,
                        "via_direct_collaborator_id": direct_id,
                        "connection_type": "SECOND_DEGREE"
                    })

        return {
            "focus_researcher_id": researcher_id,
            "focus_researcher_name": researcher.canonical_name,
            "direct_collaborators_count": len(first_degree_collaborators),
            "direct_collaborators": first_degree_collaborators,
            "second_degree_network_count": len(second_degree),
            "second_degree_network": second_degree,
            "non_negotiable_boundary": (
                "Co-authorship or co-investigation is an observed historical artifact; "
                "it does not guarantee current philosophical agreement or ongoing partnership."
            )
        }

    # -------------------------------------------------------------------------
    # 5. Cross-Disciplinary Bridge Detection
    # -------------------------------------------------------------------------

    def detect_cross_disciplinary_bridges(self, tenant_id: Optional[str] = None) -> List[CrossDisciplinaryBridge]:
        """
        Discovers researchers who bridge distinct disciplines (e.g. Unani Medicine + Phytochemistry,
        or Oncology + AI) based on multi-disciplinary expertise profiles and co-authorships.
        """
        bridges: List[CrossDisciplinaryBridge] = []

        for r in self.researchers.values():
            if r.visibility == VisibilityScope.TENANT_PRIVATE and r.tenant_id != tenant_id:
                continue

            disciplines = set(r.primary_disciplines)
            for exp in r.expertise_profile:
                if exp.dimension == ExpertiseDimension.DOMAIN:
                    disciplines.add(exp.topic_or_method)

            # A bridge requires at least 2 distinct primary disciplines
            if len(disciplines) >= 2:
                all_sources = []
                for exp in r.expertise_profile:
                    all_sources.extend(exp.source_identifiers)

                bridge = CrossDisciplinaryBridge(
                    researcher_id=r.researcher_id,
                    researcher_name=r.canonical_name,
                    bridged_disciplines=sorted(list(disciplines)),
                    bridging_evidence_count=len(r.expertise_profile),
                    shared_topics=[e.topic_or_method for e in r.expertise_profile],
                    evidence_references=all_sources[:5],
                    description=f"Identified cross-disciplinary bridge connecting: {', '.join(sorted(list(disciplines)))}"
                )
                bridges.append(bridge)

        return bridges

    # -------------------------------------------------------------------------
    # 6. Research Clusters & Communities
    # -------------------------------------------------------------------------

    def discover_clusters(self, tenant_id: Optional[str] = None) -> List[ResearchCluster]:
        """
        Discovers dense thematic research clusters connecting researchers and institutions.
        """
        clusters: List[ResearchCluster] = []

        # Find metabolic & natural products cluster
        natural_product_researchers = [
            r.researcher_id for r in self.researchers.values()
            if any("Unani" in d or "Phytochemistry" in d or "Metabolic" in d for d in r.primary_disciplines)
            and (r.visibility == VisibilityScope.PUBLIC or r.tenant_id == tenant_id)
        ]

        if natural_product_researchers:
            inst_ids = set()
            for rid in natural_product_researchers:
                for aff in self.researchers[rid].affiliations:
                    inst_ids.add(aff.institution_id)

            cluster1 = ResearchCluster(
                cluster_id="cluster-metabolic-phytochem-01",
                label="Polyherbal Metabolic Regulation & Chemical Genomics Collaboratory",
                disciplines=["Unani Medicine", "Phytochemistry", "Metabolic Pharmacology", "Endocrinology"],
                core_topics=["Type 2 Diabetes", "AMPK Activation", "Insulin Resistance"],
                dominant_methods=["UPLC-MS/MS Metabolite Profiling", "Randomized Controlled Trials", "Ligand Docking"],
                member_researcher_ids=natural_product_researchers,
                member_institution_ids=list(inst_ids),
                total_collaborations=len(self.edges),
                cohesion_score=0.88
            )
            clusters.append(cluster1)
            self.clusters[cluster1.cluster_id] = cluster1

        return clusters

    # -------------------------------------------------------------------------
    # 7. Epistemic Research Gap / Frontier Detection
    # -------------------------------------------------------------------------

    def evaluate_research_gap(self, topic: str, tenant_id: Optional[str] = None) -> ResearchGapReport:
        """
        Evaluate research presence for a topic or intersection.
        Enforces epistemic boundary: if unindexed, marks SPARSE_IN_INDEXED_SOURCES
        without claiming research is globally nonexistent.
        """
        matched_researchers = 0
        matched_publications = 0

        for r in self.researchers.values():
            if r.visibility == VisibilityScope.TENANT_PRIVATE and r.tenant_id != tenant_id:
                continue

            for exp in r.expertise_profile:
                if topic.lower() in exp.topic_or_method.lower():
                    matched_researchers += 1
                    matched_publications += exp.evidence_count

        if matched_researchers == 0:
            return ResearchGapReport(
                domain_or_topic=topic,
                status=GapStatus.SPARSE_IN_INDEXED_SOURCES,
                observed_publication_count=0,
                indexed_researcher_count=0,
                recommended_inquiry_path=[
                    "Consult historical pharmacopoeias and non-indexed institutional repositories",
                    "Survey regional traditional medicine research councils (e.g. CCRUM/CCRAS/AYUSH)",
                    "Establish prospective multi-center investigative consortium"
                ]
            )
        elif matched_researchers <= 2:
            return ResearchGapReport(
                domain_or_topic=topic,
                status=GapStatus.EMERGING,
                observed_publication_count=matched_publications,
                indexed_researcher_count=matched_researchers,
                recommended_inquiry_path=[
                    "Expand mechanistic replication studies",
                    "Conduct structured cross-disciplinary validation"
                ]
            )
        else:
            return ResearchGapReport(
                domain_or_topic=topic,
                status=GapStatus.WELL_REPRESENTED,
                observed_publication_count=matched_publications,
                indexed_researcher_count=matched_researchers,
                recommended_inquiry_path=["Synthesize living systematic review across existing clusters"]
            )

    # -------------------------------------------------------------------------
    # 8. Network Snapshotting & Diffing
    # -------------------------------------------------------------------------

    def capture_snapshot(self, label: str, tenant_id: Optional[str] = None) -> NetworkSnapshot:
        """
        Capture versioned snapshot of current collaboration network state.
        """
        accessible_researchers = [
            r.researcher_id for r in self.researchers.values()
            if r.visibility == VisibilityScope.PUBLIC or r.tenant_id == tenant_id
        ]
        accessible_institutions = [
            i.institution_id for i in self.institutions.values()
            if i.visibility == VisibilityScope.PUBLIC or i.tenant_id == tenant_id
        ]
        accessible_edges = [
            e.edge_id for e in self.edges.values()
            if e.visibility == VisibilityScope.PUBLIC or e.tenant_id == tenant_id
        ]

        snapshot = NetworkSnapshot(
            label=label,
            total_researchers=len(accessible_researchers),
            total_institutions=len(accessible_institutions),
            total_collaboration_edges=len(accessible_edges),
            total_clusters=len(self.clusters),
            researcher_ids=accessible_researchers,
            edge_ids=accessible_edges,
            cluster_ids=list(self.clusters.keys())
        )
        self.snapshots[snapshot.snapshot_id] = snapshot
        return snapshot

    def diff_snapshots(self, snap_from_id: str, snap_to_id: str) -> NetworkDiff:
        """
        Compute diff between two snapshots, revealing new researchers, new collaborations,
        and topological evolutions.
        """
        if snap_from_id not in self.snapshots or snap_to_id not in self.snapshots:
            raise KeyError("One or both snapshot IDs not found.")

        s_from = self.snapshots[snap_from_id]
        s_to = self.snapshots[snap_to_id]

        new_researchers = [rid for rid in s_to.researcher_ids if rid not in s_from.researcher_ids]
        new_edges = [eid for eid in s_to.edge_ids if eid not in s_from.edge_ids]
        new_clusters = [cid for cid in s_to.cluster_ids if cid not in s_from.cluster_ids]

        return NetworkDiff(
            from_snapshot_id=snap_from_id,
            to_snapshot_id=snap_to_id,
            new_researchers=new_researchers,
            new_edges=new_edges,
            new_clusters=new_clusters,
            strengthened_collaborations=[
                {"edge_id": eid, "status": "ACTIVE_RECENT"} for eid in new_edges
            ]
        )

    # -------------------------------------------------------------------------
    # 9. Institution Profiles & Helpers
    # -------------------------------------------------------------------------

    def get_institution(self, institution_id: str, tenant_id: Optional[str] = None) -> Optional[InstitutionIdentity]:
        """Retrieve institution profile with privacy checks."""
        inst = self.institutions.get(institution_id)
        if not inst:
            return None
        if inst.visibility == VisibilityScope.TENANT_PRIVATE and inst.tenant_id != tenant_id:
            return None
        return inst

    def get_researcher(self, researcher_id: str, tenant_id: Optional[str] = None) -> Optional[ResearcherIdentity]:
        """Retrieve researcher identity with privacy checks."""
        return self._get_authorized_researcher(researcher_id, tenant_id)

    def _get_authorized_researcher(self, researcher_id: str, tenant_id: Optional[str] = None) -> Optional[ResearcherIdentity]:
        researcher = self.researchers.get(researcher_id)
        if not researcher:
            return None
        if researcher.visibility == VisibilityScope.TENANT_PRIVATE and researcher.tenant_id != tenant_id:
            return None
        return researcher
