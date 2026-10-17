"""
ZMIE Global Research Discovery Network Engine
Prompt 14 Implementation.

Coordinates researchers, institutions, grants, projects, trials, preprints,
theses, datasets, patents, and lifecycle provenance edges.
Includes author disambiguation, canonical study clustering to prevent double-counting,
frontier research detection, and query resolvers.
"""

import uuid
import re
from typing import List, Dict, Any, Optional, Set, Tuple
from app.models.research_network import (
    Researcher,
    ResearchInstitution,
    InstitutionType,
    GrantRecord,
    ClinicalTrialRecord,
    PreprintRecord,
    ThesisRecord,
    DatasetRecord,
    PatentRecord,
    ResearchProject,
    LifecycleEdge,
    LifecycleRelation,
    ResearchSignal,
    ProjectStatus,
)


class ResearchNetworkEngine:
    """
    Core engine managing the global research discovery graph, author disambiguation,
    study lifecycle linking, and research frontier discovery.
    """

    def __init__(self):
        self._researchers: Dict[str, Researcher] = {}
        self._institutions: Dict[str, ResearchInstitution] = {}
        self._grants: Dict[str, GrantRecord] = {}
        self._projects: Dict[str, ResearchProject] = {}
        self._trials: Dict[str, ClinicalTrialRecord] = {}
        self._preprints: Dict[str, PreprintRecord] = {}
        self._theses: Dict[str, ThesisRecord] = {}
        self._datasets: Dict[str, DatasetRecord] = {}
        self._patents: Dict[str, PatentRecord] = {}
        self._edges: List[LifecycleEdge] = []
        self._frontier_signals: Dict[str, ResearchSignal] = {}

        self._seed_initial_network()

    def _seed_initial_network(self):
        """Seed rich realistic multi-system biomedical and traditional research network."""
        # 1. Institutions (Modern & Traditional)
        inst_oxford = ResearchInstitution(
            institution_id="inst_oxford_01",
            name="University of Oxford - Nuffield Department of Medicine",
            ror_id="https://ror.org/052gg0110",
            institution_type=InstitutionType.UNIVERSITY,
            country="United Kingdom",
            city="Oxford",
            departments=["Nuffield Dept of Medicine", "Oxford Centre for Diabetes"],
            traditional_systems=["modern"],
            active_trials_count=84,
            total_grant_funding_usd=120000000.0,
        )
        inst_nium = ResearchInstitution(
            institution_id="inst_nium_blr",
            name="National Institute of Unani Medicine (NIUM)",
            ror_id="https://ror.org/nium_blr_01",
            institution_type=InstitutionType.TRADITIONAL_COUNCIL,
            country="India",
            city="Bengaluru",
            departments=["Department of Moalajat (Medicine)", "Department of Ilmul Advia (Pharmacology)"],
            traditional_systems=["unani"],
            active_trials_count=22,
            total_grant_funding_usd=15000000.0,
        )
        inst_aiia = ResearchInstitution(
            institution_id="inst_aiia_delhi",
            name="All India Institute of Ayurveda (AIIA)",
            ror_id="https://ror.org/aiia_delhi_01",
            institution_type=InstitutionType.TRADITIONAL_COUNCIL,
            country="India",
            city="New Delhi",
            departments=["Kayachikitsa (Internal Medicine)", "Dravyaguna (Pharmacognosy)"],
            traditional_systems=["ayurveda"],
            active_trials_count=35,
            total_grant_funding_usd=25000000.0,
        )
        inst_harvard = ResearchInstitution(
            institution_id="inst_harvard_med",
            name="Harvard Medical School & Brigham and Women's Hospital",
            ror_id="https://ror.org/03vek6s52",
            institution_type=InstitutionType.UNIVERSITY,
            country="United States",
            city="Boston",
            departments=["Department of Cardiology", "Division of Preventive Medicine"],
            traditional_systems=["modern"],
            active_trials_count=190,
            total_grant_funding_usd=340000000.0,
        )
        inst_ccrum = ResearchInstitution(
            institution_id="inst_ccrum_hq",
            name="Central Council for Research in Unani Medicine (CCRUM)",
            ror_id="https://ror.org/ccrum_hq_01",
            institution_type=InstitutionType.TRADITIONAL_COUNCIL,
            country="India",
            city="New Delhi",
            departments=["Clinical Research Division", "Drug Standardization Section"],
            traditional_systems=["unani"],
            active_trials_count=48,
            total_grant_funding_usd=30000000.0,
        )

        for inst in [inst_oxford, inst_nium, inst_aiia, inst_harvard, inst_ccrum]:
            self._institutions[inst.institution_id] = inst

        # 2. Researchers
        # Dr. Sarah Jenkins (Oxford Cardiology)
        res_jenkins = Researcher(
            researcher_id="res_jenkins_s",
            canonical_name="Prof. Sarah E. Jenkins",
            aliases=["S. E. Jenkins", "Sarah Jenkins"],
            orcid="0000-0002-1825-0097",
            affiliations=[{
                "institution_id": "inst_oxford_01",
                "name": "University of Oxford",
                "department": "Nuffield Dept of Medicine",
                "role": "Professor of Cardiovascular Medicine",
                "current": True
            }],
            subject_areas=["Cardiology", "Heart Failure", "SGLT2 Inhibitors", "Metabolism"],
            traditional_systems=["modern"],
            co_author_ids=["res_collins_r"],
            disambiguation_confidence=0.98,
            h_index=64,
            citation_count=18200,
            publication_count=142,
            active_projects_count=4,
            is_verified=True,
        )

        # Another "Sarah Jenkins" at different institution to test disambiguation!
        res_jenkins_jr = Researcher(
            researcher_id="res_jenkins_s_junior",
            canonical_name="Dr. Sarah M. Jenkins",
            aliases=["S. M. Jenkins", "Sarah Jenkins"],
            orcid="0000-0003-9912-4411",
            affiliations=[{
                "institution_id": "inst_harvard_med",
                "name": "Harvard Medical School",
                "department": "Department of Dermatology",
                "role": "Postdoctoral Fellow",
                "current": True
            }],
            subject_areas=["Dermatology", "Psoriasis", "Biologics"],
            traditional_systems=["modern"],
            co_author_ids=[],
            disambiguation_confidence=0.92,
            h_index=12,
            citation_count=480,
            publication_count=16,
            active_projects_count=1,
            is_verified=True,
        )

        # Prof. Hakim Aslam Siddiqui (NIUM Unani Cardiology & Metabolic)
        res_aslam = Researcher(
            researcher_id="res_aslam_siddiqui",
            canonical_name="Prof. Hakim Aslam Siddiqui",
            aliases=["H. A. Siddiqui", "Mohammad Aslam Siddiqui"],
            orcid="0000-0001-7723-5510",
            affiliations=[{
                "institution_id": "inst_nium_blr",
                "name": "National Institute of Unani Medicine",
                "department": "Department of Moalajat",
                "role": "Dean & Head of Department",
                "current": True
            }],
            subject_areas=["Unani Medicine", "Ziabetus Shakari (Diabetes)", "Khamira Abresham", "Cardioprotection"],
            traditional_systems=["unani"],
            co_author_ids=["res_ccrum_lead"],
            disambiguation_confidence=0.95,
            h_index=28,
            citation_count=3200,
            publication_count=65,
            active_projects_count=3,
            is_verified=True,
        )

        # Prof. Rajesh Vaidya (AIIA Ayurveda)
        res_vaidya = Researcher(
            researcher_id="res_rajesh_vaidya",
            canonical_name="Prof. Rajesh K. Sharma",
            aliases=["R. K. Sharma", "Vaidya Rajesh Sharma"],
            orcid="0000-0002-3341-9988",
            affiliations=[{
                "institution_id": "inst_aiia_delhi",
                "name": "All India Institute of Ayurveda",
                "department": "Kayachikitsa",
                "role": "Professor & Senior Consultant",
                "current": True
            }],
            subject_areas=["Ayurveda", "Madhumeha", "Ashwagandha", "Guduchi", "Metabolic Syndrome"],
            traditional_systems=["ayurveda"],
            co_author_ids=[],
            disambiguation_confidence=0.94,
            h_index=31,
            citation_count=4100,
            publication_count=78,
            active_projects_count=3,
            is_verified=True,
        )

        for res in [res_jenkins, res_jenkins_jr, res_aslam, res_vaidya]:
            self._researchers[res.researcher_id] = res

        # 3. Grants
        grant_ox = GrantRecord(
            grant_id="grant_ox_sglt2_2023",
            grant_number="MRC-MR/T012345/1",
            funding_agency="Medical Research Council (MRC UK)",
            title="SGLT2 Inhibition in Normoglycemic Heart Failure Phenotypes",
            abstract="Investigating molecular myocardial metabolic switching induced by SGLT2 inhibitors.",
            amount_usd=2800000.0,
            currency="GBP",
            pi_ids=["res_jenkins_s"],
            institution_id="inst_oxford_01",
            start_date="2023-01-01",
            end_date="2026-12-31",
            status="ACTIVE",
        )

        grant_unani = GrantRecord(
            grant_id="grant_ayush_khamira_01",
            grant_number="AYUSH/EMR/2022/UN-04",
            funding_agency="Ministry of AYUSH / CCRUM",
            title="Randomized Placebo-Controlled Trial of Khamira Abresham Hakim Arshad Wala in Endothelial Dysfunction",
            abstract="Evaluating traditional Unani compound formulation Khamira Abresham in vascular remodeling.",
            amount_usd=450000.0,
            currency="INR",
            pi_ids=["res_aslam_siddiqui"],
            institution_id="inst_nium_blr",
            start_date="2022-06-01",
            end_date="2025-05-31",
            status="ACTIVE",
        )

        for g in [grant_ox, grant_unani]:
            self._grants[g.grant_id] = g

        # 4. Clinical Trials
        trial_ox = ClinicalTrialRecord(
            trial_id="NCT05221199",
            registry="ClinicalTrials.gov",
            title="Dapagliflozin in Myocardial Energetics (DAPA-ENERGY)",
            phase="Phase 3",
            recruitment_status="ACTIVE_NOT_RECRUITING",
            interventions=["Dapagliflozin 10mg", "Placebo"],
            conditions=["Heart Failure with Preserved Ejection Fraction", "Metabolic Syndrome"],
            sponsor_id="inst_oxford_01",
            investigator_ids=["res_jenkins_s"],
            canonical_study_id="study_dapa_energy_canonical",
            results_published=True,
            publication_dois=["10.1056/NEJMoa2309811"],
        )

        trial_unani = ClinicalTrialRecord(
            trial_id="CTRI/2022/07/044192",
            registry="CTRI",
            title="Efficacy and Safety of Khamira Abresham in Post-Myocardial Infarction Vascular Health: A Double Blind RCT",
            phase="Phase 2",
            recruitment_status="COMPLETED",
            interventions=["Khamira Abresham Hakim Arshad Wala 5g bid", "Standard Medical Care"],
            conditions=["Endothelial Dysfunction", "Post-PCI Recovery"],
            sponsor_id="inst_nium_blr",
            investigator_ids=["res_aslam_siddiqui"],
            canonical_study_id="study_khamira_vascular_canonical",
            results_published=True,
            publication_dois=["10.1016/j.jep.2024.118021"],
        )

        for tr in [trial_ox, trial_unani]:
            self._trials[tr.trial_id] = tr

        # 5. Preprints
        preprint_ox = PreprintRecord(
            preprint_id="prep_medrxiv_2023_8891",
            doi="10.1101/2023.08.15.23294101",
            server="medRxiv",
            title="Myocardial metabolic flux under SGLT2 inhibition: early findings from DAPA-ENERGY cohort",
            authors=["Jenkins SE", "Collins R"],
            author_ids=["res_jenkins_s"],
            deposited_date="2023-08-16",
            version=1,
            canonical_study_id="study_dapa_energy_canonical",
            peer_reviewed_doi="10.1056/NEJMoa2309811",
            is_superseded_by_peer_review=True,
        )

        for prep in [preprint_ox]:
            self._preprints[prep.preprint_id] = prep

        # 6. Projects
        proj_ox = ResearchProject(
            project_id="proj_dapa_energy",
            title="Cardiometabolic Energetics under SGLT2 Inhibition",
            description="Comprehensive investigation of cardiac metabolic remodeling.",
            lead_researcher_ids=["res_jenkins_s"],
            collaborator_ids=[],
            institution_ids=["inst_oxford_01"],
            grant_ids=["grant_ox_sglt2_2023"],
            status=ProjectStatus.PUBLISHED,
            is_private_unobservable=False,
            clinical_trial_ids=["NCT05221199"],
            canonical_study_id="study_dapa_energy_canonical",
            outputs=[
                {"type": "PREPRINT", "id": "prep_medrxiv_2023_8891"},
                {"type": "TRIAL", "id": "NCT05221199"},
                {"type": "PUBLICATION", "doi": "10.1056/NEJMoa2309811"}
            ],
        )

        # Private project to test unobservable boundary!
        proj_private = ResearchProject(
            project_id="proj_secret_pharma_01",
            title="Internal Pre-Clinical Molecule X-912 Formulation",
            description="Proprietary undisclosed compound screen in lead optimization.",
            lead_researcher_ids=[],
            collaborator_ids=[],
            institution_ids=["inst_harvard_med"],
            grant_ids=[],
            status=ProjectStatus.UNKNOWN,
            is_private_unobservable=True,
            clinical_trial_ids=[],
            canonical_study_id=None,
            outputs=[],
        )

        proj_unani = ResearchProject(
            project_id="proj_khamira_cardio",
            title="Clinical Evaluation of Khamira Abresham in Cardiovascular Protection",
            description="Rigorous randomized controlled evaluation of classical Khamira formulation.",
            lead_researcher_ids=["res_aslam_siddiqui"],
            collaborator_ids=[],
            institution_ids=["inst_nium_blr"],
            grant_ids=["grant_ayush_khamira_01"],
            status=ProjectStatus.VALIDATED,
            is_private_unobservable=False,
            clinical_trial_ids=["CTRI/2022/07/044192"],
            canonical_study_id="study_khamira_vascular_canonical",
            outputs=[
                {"type": "TRIAL", "id": "CTRI/2022/07/044192"},
                {"type": "PUBLICATION", "doi": "10.1016/j.jep.2024.118021"}
            ],
        )

        for p in [proj_ox, proj_private, proj_unani]:
            self._projects[p.project_id] = p

        # 7. Lifecycle Edges
        edges = [
            LifecycleEdge(
                source_id="res_jenkins_s",
                target_id="inst_oxford_01",
                relation_type=LifecycleRelation.AFFILIATED_WITH,
                timestamp="2020-01-01",
            ),
            LifecycleEdge(
                source_id="grant_ox_sglt2_2023",
                target_id="proj_dapa_energy",
                relation_type=LifecycleRelation.FUNDED_BY,
                timestamp="2023-01-01",
            ),
            LifecycleEdge(
                source_id="proj_dapa_energy",
                target_id="NCT05221199",
                relation_type=LifecycleRelation.CONDUCTS,
                timestamp="2023-02-15",
            ),
            LifecycleEdge(
                source_id="NCT05221199",
                target_id="prep_medrxiv_2023_8891",
                relation_type=LifecycleRelation.GENERATES_PREPRINT,
                timestamp="2023-08-16",
            ),
            LifecycleEdge(
                source_id="prep_medrxiv_2023_8891",
                target_id="10.1056/NEJMoa2309811",
                relation_type=LifecycleRelation.SUPERSEDED_BY,
                timestamp="2024-02-10",
            ),
            # Unani lifecycle
            LifecycleEdge(
                source_id="grant_ayush_khamira_01",
                target_id="proj_khamira_cardio",
                relation_type=LifecycleRelation.FUNDED_BY,
                timestamp="2022-06-01",
            ),
            LifecycleEdge(
                source_id="proj_khamira_cardio",
                target_id="CTRI/2022/07/044192",
                relation_type=LifecycleRelation.CONDUCTS,
                timestamp="2022-07-20",
            ),
            LifecycleEdge(
                source_id="CTRI/2022/07/044192",
                target_id="10.1016/j.jep.2024.118021",
                relation_type=LifecycleRelation.PUBLISHED_AS,
                timestamp="2024-03-12",
            ),
        ]
        self._edges.extend(edges)

        # 8. Frontier Signals
        sig_glp1 = ResearchSignal(
            signal_id="sig_glp1_dual_agonism",
            topic="Dual & Triple Incretin Receptor Agonists in Neurodegenerative Pathology",
            growth_rate_3yr=285.4,
            preprints_to_papers_ratio=0.42,
            clinical_trial_acceleration=3.4,
            grant_inflow_usd=85000000.0,
            frontier_velocity_score=94.5,
            status="EMERGING_FRONTIER",
            key_breakthrough_compounds=["Tirzepatide", "Retatrutide", "GLP-1/GIP co-agonists"],
            key_institutions=["Harvard Medical School", "Oxford University", "Karolinska Institutet"],
        )
        sig_unani_phytotherapy = ResearchSignal(
            signal_id="sig_unani_microbiome",
            topic="Unani Khamira Polyherbal Fermentations on Gut-Cardiovascular Axis",
            growth_rate_3yr=140.2,
            preprints_to_papers_ratio=0.25,
            clinical_trial_acceleration=2.1,
            grant_inflow_usd=12000000.0,
            frontier_velocity_score=82.0,
            status="ACCELERATING",
            key_breakthrough_compounds=["Khamira Abresham", "Bombax ceiba extracts", "Silk cocoon sericin metabolites"],
            key_institutions=["National Institute of Unani Medicine", "Central Council for Research in Unani Medicine"],
        )
        self._frontier_signals[sig_glp1.signal_id] = sig_glp1
        self._frontier_signals[sig_unani_phytotherapy.signal_id] = sig_unani_phytotherapy

    # -------------------------------------------------------------
    # Disambiguation & Entity Resolution
    # -------------------------------------------------------------

    def disambiguate_researcher(
        self,
        name: str,
        orcid: Optional[str] = None,
        institution_name: Optional[str] = None,
        subject_area: Optional[str] = None
    ) -> List[Tuple[Researcher, float, str]]:
        """
        Disambiguates a researcher name against candidate records.
        Returns a list of tuples: (Researcher, Confidence Score, Disambiguation Reason).
        Guarantees that multiple people with identical names (e.g. 'Sarah Jenkins')
        are not collapsed if ORCID or affiliations differ.
        """
        results: List[Tuple[Researcher, float, str]] = []
        name_clean = name.strip().lower()

        for res in self._researchers.values():
            score = 0.0
            reasons = []

            # 1. Exact ORCID match (Gold Standard: 1.0)
            if orcid and res.orcid and orcid.strip() == res.orcid:
                score = 1.0
                reasons.append("Exact ORCID match")
                results.append((res, score, "; ".join(reasons)))
                continue

            # 2. Name match (canonical or alias)
            name_matched = False
            if name_clean == res.canonical_name.lower():
                score += 0.45
                name_matched = True
                reasons.append("Exact canonical name match")
            elif any(name_clean == a.lower() for a in res.aliases):
                score += 0.35
                name_matched = True
                reasons.append("Alias match")
            elif any(part in res.canonical_name.lower() for part in name_clean.split()):
                score += 0.15
                name_matched = True
                reasons.append("Partial token match")

            if not name_matched:
                continue

            # 3. Institution match
            if institution_name:
                inst_match = False
                for aff in res.affiliations:
                    if institution_name.lower() in aff.get("name", "").lower() or institution_name.lower() in aff.get("institution_id", "").lower():
                        score += 0.35
                        inst_match = True
                        reasons.append("Affiliation match")
                        break
                if not inst_match and len(res.affiliations) > 0:
                    score -= 0.20
                    reasons.append("Institutional mismatch penalty")

            # 4. Subject Area match
            if subject_area:
                subj_clean = subject_area.lower()
                if any(subj_clean in s.lower() or s.lower() in subj_clean for s in res.subject_areas):
                    score += 0.20
                    reasons.append("Field of expertise overlap")

            final_score = max(0.05, min(0.99, score))
            results.append((res, round(final_score, 2), "; ".join(reasons)))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    # -------------------------------------------------------------
    # Canonical Study De-duplication & Evidence Gating
    # -------------------------------------------------------------

    def resolve_canonical_study(self, identifier: str) -> Dict[str, Any]:
        """
        Clusters trial registry, preprint, and peer-reviewed publication
        under a single Canonical Study ID to prevent artificial evidence inflation.
        """
        canonical_id: Optional[str] = None
        linked_trial: Optional[ClinicalTrialRecord] = None
        linked_preprint: Optional[PreprintRecord] = None
        linked_project: Optional[ResearchProject] = None

        # Check if identifier is trial ID
        if identifier in self._trials:
            linked_trial = self._trials[identifier]
            canonical_id = linked_trial.canonical_study_id
        # Check if preprint
        elif identifier in self._preprints:
            linked_preprint = self._preprints[identifier]
            canonical_id = linked_preprint.canonical_study_id
        # Check if project
        elif identifier in self._projects:
            linked_project = self._projects[identifier]
            canonical_id = linked_project.canonical_study_id

        # Search by canonical id if not found directly
        if not canonical_id:
            for t in self._trials.values():
                if t.canonical_study_id == identifier:
                    canonical_id = identifier
                    linked_trial = t
                    break

        if not canonical_id:
            return {
                "canonical_study_id": identifier,
                "found": False,
                "warning": "No canonical study cluster found for identifier."
            }

        # Collect all linked components
        all_trials = [t for t in self._trials.values() if t.canonical_study_id == canonical_id]
        all_preprints = [p for p in self._preprints.values() if p.canonical_study_id == canonical_id]
        all_projects = [p for p in self._projects.values() if p.canonical_study_id == canonical_id]

        peer_reviewed_dois = set()
        for t in all_trials:
            peer_reviewed_dois.update(t.publication_dois)
        for p in all_preprints:
            if p.peer_reviewed_doi:
                peer_reviewed_dois.add(p.peer_reviewed_doi)

        return {
            "canonical_study_id": canonical_id,
            "found": True,
            "clinical_trials": [t.trial_id for t in all_trials],
            "preprints": [p.preprint_id for p in all_preprints],
            "projects": [p.project_id for p in all_projects],
            "peer_reviewed_dois": list(peer_reviewed_dois),
            "evidence_weight_rule": "COUNT_AS_ONE_CANONICAL_STUDY",
            "suppressed_duplicate_count": max(0, len(all_trials) + len(all_preprints) + len(peer_reviewed_dois) - 1),
            "guidance": "Trial registration, preliminary preprint, and final publication belong to identical empirical cohort. Evidence must not be summed as independent citations."
        }

    # -------------------------------------------------------------
    # Query Resolvers
    # -------------------------------------------------------------

    def who_is_researching(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Resolves: 'Who is researching this topic / condition / drug?'
        Returns top ranked researchers, active projects, affiliations, and evidence track record.
        """
        q_tokens = set(re.findall(r"\w+", query.lower()))
        matched_researchers = []

        for res in self._researchers.values():
            match_score = 0
            all_text = " ".join(res.subject_areas + res.aliases + res.traditional_systems).lower()
            for tok in q_tokens:
                if tok in all_text:
                    match_score += 1

            if match_score > 0:
                # Rank by match score, active projects, and h-index
                composite_rank = (match_score * 10) + (res.active_projects_count * 5) + ((res.h_index or 0) * 0.5)
                matched_researchers.append({
                    "researcher_id": res.researcher_id,
                    "canonical_name": res.canonical_name,
                    "affiliations": res.affiliations,
                    "subject_areas": res.subject_areas,
                    "traditional_systems": res.traditional_systems,
                    "active_projects_count": res.active_projects_count,
                    "publication_count": res.publication_count,
                    "h_index": res.h_index,
                    "composite_rank_score": round(composite_rank, 2),
                })

        matched_researchers.sort(key=lambda x: x["composite_rank_score"], reverse=True)
        return {
            "query": query,
            "total_matches": len(matched_researchers),
            "top_researchers": matched_researchers[:limit],
            "timestamp": "UTC_LIVE"
        }

    def where_is_research_happening(self, query: str) -> Dict[str, Any]:
        """
        Resolves: 'Where is this research happening globally?'
        Returns institutional and geographical distribution.
        """
        q_tokens = set(re.findall(r"\w+", query.lower()))
        matched_institutions = []

        for inst in self._institutions.values():
            match_score = 0
            inst_text = " ".join([inst.name, inst.country, inst.institution_type.value] + inst.departments + inst.traditional_systems).lower()
            for tok in q_tokens:
                if tok in inst_text:
                    match_score += 1

            # Also check if any affiliated researcher matches query
            for res in self._researchers.values():
                for aff in res.affiliations:
                    if aff.get("institution_id") == inst.institution_id:
                        for tok in q_tokens:
                            if any(tok in s.lower() for s in res.subject_areas):
                                match_score += 1

            if match_score > 0 or len(q_tokens) == 0:
                matched_institutions.append({
                    "institution_id": inst.institution_id,
                    "name": inst.name,
                    "institution_type": inst.institution_type.value,
                    "country": inst.country,
                    "city": inst.city,
                    "active_trials_count": inst.active_trials_count,
                    "traditional_systems": inst.traditional_systems,
                    "total_grant_funding_usd": inst.total_grant_funding_usd,
                    "relevance_score": match_score
                })

        matched_institutions.sort(key=lambda x: (x["relevance_score"], x["active_trials_count"]), reverse=True)
        return {
            "query": query,
            "institutions_count": len(matched_institutions),
            "institutions": matched_institutions
        }

    def get_frontier_signals(self) -> List[ResearchSignal]:
        """Returns frontier and emerging research signals with velocity metrics."""
        return list(self._frontier_signals.values())

    def get_lifecycle_trace(self, root_id: str) -> Dict[str, Any]:
        """
        Traverses lifecycle edges forward and backward from a root identifier
        (e.g., Grant -> Project -> Trial -> Preprint -> Publication).
        """
        nodes_visited: Set[str] = set()
        edges_found: List[Dict[str, Any]] = []

        def traverse(current_id: str, depth: int):
            if depth > 5 or current_id in nodes_visited:
                return
            nodes_visited.add(current_id)

            for e in self._edges:
                if e.source_id == current_id:
                    edges_found.append({
                        "source": e.source_id,
                        "target": e.target_id,
                        "relation": e.relation_type.value,
                        "timestamp": e.timestamp
                    })
                    traverse(e.target_id, depth + 1)
                elif e.target_id == current_id:
                    edges_found.append({
                        "source": e.source_id,
                        "target": e.target_id,
                        "relation": e.relation_type.value,
                        "timestamp": e.timestamp
                    })
                    traverse(e.source_id, depth + 1)

        traverse(root_id, 0)

        # Check if any associated project is private unobservable
        is_private = False
        if root_id in self._projects and self._projects[root_id].is_private_unobservable:
            is_private = True
            return {
                "root_id": root_id,
                "is_private_unobservable": True,
                "boundary_status": "PRIVATE_UNOBSERVABLE",
                "message": "Project is confidential/pre-publication. In accordance with ZMIE integrity guidelines, private unobservable research cannot be fabricated or hallucinatively reconstructed.",
                "nodes": [root_id],
                "edges": []
            }

        return {
            "root_id": root_id,
            "is_private_unobservable": is_private,
            "boundary_status": "OBSERVABLE_PUBLIC_RECORD",
            "nodes_count": len(nodes_visited),
            "nodes": list(nodes_visited),
            "edges": edges_found
        }

    # -------------------------------------------------------------
    # Storage & Retrieval CRUD
    # -------------------------------------------------------------

    def get_researcher(self, researcher_id: str) -> Optional[Researcher]:
        return self._researchers.get(researcher_id)

    def get_institution(self, institution_id: str) -> Optional[ResearchInstitution]:
        return self._institutions.get(institution_id)

    def get_project(self, project_id: str) -> Optional[ResearchProject]:
        return self._projects.get(project_id)

    def get_trial(self, trial_id: str) -> Optional[ClinicalTrialRecord]:
        return self._trials.get(trial_id)

    def get_grant(self, grant_id: str) -> Optional[GrantRecord]:
        return self._grants.get(grant_id)

    def add_researcher(self, researcher: Researcher):
        self._researchers[researcher.researcher_id] = researcher

    def add_institution(self, institution: ResearchInstitution):
        self._institutions[institution.institution_id] = institution

    def add_project(self, project: ResearchProject):
        self._projects[project.project_id] = project

    def add_edge(self, edge: LifecycleEdge):
        self._edges.append(edge)
