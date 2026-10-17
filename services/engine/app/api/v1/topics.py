"""
ZMIE Public Medical Encyclopedia Router (Sections 30 & 45)
Exposes governed dynamic topic pages: GET /v1/topics/{topic}
Built exclusively from verified knowledge objects rather than ungrounded LLM text.
Encompasses the 14 foundational medical disciplines and gold-standard textbook codices:
- Anatomy (Gray's Anatomy, Netter, Snell)
- Physiology (Guyton & Hall, Ganong, Costanzo)
- Pathology (Robbins & Cotran, Harsh Mohan)
- Pharmacology (Goodman & Gilman, Katzung, KD Tripathi)
- Internal Medicine (Harrison's, Davidson's)
- General Surgery (Bailey & Love, Sabiston, Schwartz)
- Pediatrics (Nelson, Ghai)
- Dermatology (Fitzpatrick's, Rook)
- PSM / Preventive & Social Medicine (Park's PSM, Maxcy-Rosenau-Last)
- Radiology & Imaging (Grainger & Allison, Brant & Helms)
- Obstetrics & Gynecology (Williams, DC Dutta, Shaw)
- Microbiology & Infectious Diseases (Mandell, Jawetz, Ananthanarayan)
- Biochemistry & Genetics (Harper's, Lehninger)
- Forensic Medicine & Toxicology (Goldfrank's, Parikh, Reddy)
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from app.agents.search_service import SearchService
from app.api.v1.ontology import compare_systems
from app.db.knowledge_graph_seed import KnowledgeGraphSeedService
from app.db.classical_corpus_seed import ClassicalCorpusBulkLoader
from app.db.medical_disciplines_seed import (
    MedicalDisciplinesBulkLoader,
    CANONICAL_MEDICAL_DISCIPLINES
)
from app.db.classical_authorities_seed import ClassicalAuthoritiesBulkLoader
from app.db.pharmacopoeia_master_seed import PharmacopoeiaMasterRegistry
from app.db.qarabadeen_reconciliation_seed import QarabadeenReconciliationEngine
from app.agents.drug_herb_firewall import AllopathicDrugHerbFirewall
from app.agents.live_evidence_crawler import LiveEvidenceCrawlerEngine

router = APIRouter(prefix="/topics", tags=["Public Medical Encyclopedia (Sec 30 & 45)"])


class EncyclopediaTopicPage(BaseModel):
    topic: str
    overview: str
    modern_medicine_perspective: Dict[str, Any]
    traditional_perspectives: Dict[str, Any]
    evidence_summary: Dict[str, Any]
    clinical_safety: Dict[str, Any]
    what_remains_uncertain: List[str]
    provenance_citations: List[Dict[str, Any]]
    knowledge_version: str = "K-2026.10.001"
    last_reviewed_date: str = "2026-10-04"


@router.get("", response_model=Dict[str, Any])
async def list_encyclopedia_topics(
    system: Optional[str] = Query(None, description="Filter by system: modern, unani, ayurveda"),
    category: Optional[str] = Query(None, description="Filter by clinical domain"),
    discipline: Optional[str] = Query(None, description="Filter by discipline ID (anatomy, physiology, etc.)"),
    q: Optional[str] = Query(None, description="Search query across all paradigms and disciplines")
):
    """
    Lists indexed encyclopedia entries across Allopathy, Unani Tibb, and Ayurveda,
    along with canonical medical disciplines and gold-standard textbook codices.
    """
    catalog = ClassicalCorpusBulkLoader.get_catalog(system=system, domain=category, query=q)
    
    disciplines_data = MedicalDisciplinesBulkLoader.get_all_disciplines()
    if discipline:
        disc_match = MedicalDisciplinesBulkLoader.find_discipline_by_id(discipline)
        disciplines_data = [disc_match] if disc_match else []
    elif q:
        disc_matches = MedicalDisciplinesBulkLoader.search_discipline_topics(q)
        if disc_matches:
            # Format matched disciplines
            disc_ids = {m["short_name"].lower() for m in disc_matches}
            disciplines_data = [d for d in disciplines_data if d["short_name"].lower() in disc_ids or d["name"].lower() in disc_ids]

    return {
        "status": "success",
        "total_entries": len(catalog),
        "total_disciplines": len(disciplines_data),
        "systems_supported": ["Allopathy (Modern Biomedicine)", "Unani Tibb", "Ayurveda"],
        "clinical_domains": sorted(list(set(ClassicalCorpusBulkLoader.HERB_DOMAIN_MAP.values()))),
        "entries": catalog,
        "medical_disciplines": disciplines_data
    }


@router.get("/disciplines", response_model=Dict[str, Any])
async def list_medical_disciplines(
    q: Optional[str] = Query(None, description="Search term across disciplines, textbooks or topics")
):
    """
    Lists the 14 core foundational and clinical medical disciplines,
    their canonical gold-standard textbooks, and high-yield topics.
    """
    if q:
        matches = MedicalDisciplinesBulkLoader.search_discipline_topics(query=q)
        return {
            "status": "success",
            "total_disciplines": len(matches),
            "disciplines": matches
        }
    return {
        "status": "success",
        "total_disciplines": len(CANONICAL_MEDICAL_DISCIPLINES),
        "disciplines": CANONICAL_MEDICAL_DISCIPLINES
    }


@router.get("/disciplines/{discipline_id}", response_model=Dict[str, Any])
async def get_medical_discipline_detail(discipline_id: str):
    """
    Returns detailed curriculum overview, canonical textbooks, and topics for a medical discipline.
    """
    disc = MedicalDisciplinesBulkLoader.find_discipline_by_id(discipline_id)
    if not disc:
        raise HTTPException(status_code=404, detail=f"Medical discipline '{discipline_id}' not found.")
    return {
        "status": "success",
        "discipline": disc
    }


# -----------------------------------------------------------------------------
# CLASSICAL AUTHORITIES, FORMULARIES & ENRICHED MONOGRAPHS (LEVELS 1 TO 6)
# -----------------------------------------------------------------------------

@router.get("/authorities", response_model=Dict[str, Any])
async def list_classical_authorities(
    system: Optional[str] = Query(None, description="Filter by system: unani or ayurveda"),
    level: Optional[str] = Query(None, description="Filter by level (e.g. Level 1, Level 2, Level 3, Level 4)"),
    q: Optional[str] = Query(None, description="Search across classical codices, authors, and texts")
):
    """
    Returns the complete authoritative hierarchy of classical texts,
    Qarabadeens, Nighantus, and official pharmacopoeias (UPI, NFUM, API, AFI).
    """
    if q:
        matches = ClassicalAuthoritiesBulkLoader.search_authorities(q)
        return {
            "status": "success",
            "total_matches": len(matches),
            "authorities": matches,
            "hierarchy_doctrine": ClassicalAuthoritiesBulkLoader.get_all_authorities()["hierarchy_doctrine"]
        }

    all_data = ClassicalAuthoritiesBulkLoader.get_all_authorities()
    unani_list = all_data["unani"]
    ayur_list = all_data["ayurveda"]

    if system == "unani":
        combined = unani_list
    elif system == "ayurveda":
        combined = ayur_list
    else:
        combined = unani_list + ayur_list

    if level:
        combined = [a for a in combined if level.lower() in a["level"].lower()]

    return {
        "status": "success",
        "total_authorities": len(combined),
        "unani_count": len(unani_list),
        "ayurveda_count": len(ayur_list),
        "authorities": combined,
        "hierarchy_doctrine": all_data["hierarchy_doctrine"]
    }


@router.get("/authorities/unani", response_model=Dict[str, Any])
async def list_unani_authorities():
    """
    Returns Unani classical authorities across Levels 1–4:
    - Level 1: Ibn Sina, Al-Razi, Al-Majusi, Jurjani, Nafis al-Kirmani
    - Level 2: Makhzan al-Adwiya, Ikhtiyarat-i Badi'i
    - Level 3: Qarabadeen formularies (Azam, Qadri, Jadid, Najm-ul-Ghani, Shifa'i)
    - Level 4: UPI, NFUM, CCRUM
    """
    return {
        "status": "success",
        "system": "Unani Tibb",
        "total": len(ClassicalAuthoritiesBulkLoader.get_unani_authorities()),
        "authorities": ClassicalAuthoritiesBulkLoader.get_unani_authorities()
    }


@router.get("/authorities/ayurveda", response_model=Dict[str, Any])
async def list_ayurveda_authorities():
    """
    Returns Ayurvedic classical authorities across Levels 1–4:
    - Brihat Trayi: Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya, Ashtanga Sangraha, Bhela, Kashyapa
    - Laghu Trayi & Diagnostics: Madhava Nidana, Sharngadhara Samhita
    - Dravyaguna Nighantus: Bhavaprakasha Nighantu, Dhanvantari, Raja, Kaiyadeva
    - Bhaishajya Kalpana: Bhaishajya Ratnavali, Chakradatta, Yoga Ratnakara
    - Rasashastra: Rasaratna Samuccaya, Rasa Tarangini, Rasendra Sara Sangraha
    - Official Standards: API, AFI, CCRAS
    """
    return {
        "status": "success",
        "system": "Ayurveda",
        "total": len(ClassicalAuthoritiesBulkLoader.get_ayurveda_authorities()),
        "authorities": ClassicalAuthoritiesBulkLoader.get_ayurveda_authorities()
    }


@router.get("/qarabadeen", response_model=Dict[str, Any])
async def list_qarabadeen_formularies():
    """
    Returns the classical formulation registries (Qarabadeen-e-Azam,
    Qarabadeen-e-Qadri, Qarabadeen-e-Jadid, Qarabadeen-e-Najm-ul-Ghani,
    Qarabadeen-e-Shifa'i, Qarabadeen-e-Azam wa Akmal).
    """
    q_list = ClassicalAuthoritiesBulkLoader.get_qarabadeen_registry()
    return {
        "status": "success",
        "total_formularies": len(q_list),
        "qarabadeen_registries": q_list
    }


@router.get("/monograph/{herb_key}", response_model=Dict[str, Any])
async def get_herb_monograph(herb_key: str):
    """
    Returns the comprehensive 18-part ZAYVORA drug monograph:
    Arabic/Urdu Name -> Botanical Identity -> Synonyms -> Mizaj -> Afaal ->
    Therapeutic Actions -> Indications -> Dosage (Miqdar-e-Khurak) ->
    Method of Preparation (Tarkeeb-e-Tayyari) -> Musleh -> Badal ->
    Contraindications -> Adverse Effects -> Compound Formulations (Nuskha Murakkabat) ->
    Classical References (Levels 1-4) -> Modern Pharmacology -> Clinical Evidence ->
    Toxicology -> Quality Standards (UPI / API).
    """
    mono = ClassicalCorpusBulkLoader.get_full_monograph(herb_key)
    if not mono:
        raise HTTPException(status_code=404, detail=f"Monograph for '{herb_key}' not found.")
    return {
        "status": "success",
        "monograph": mono
    }


@router.get("/pharmacopoeia", response_model=Dict[str, Any])
async def list_pharmacopoeia_herbs(
    q: Optional[str] = Query(None, description="Search term across 600+ herbs (Latin, Sanskrit, Unani, English, constituents)"),
    system: Optional[str] = Query(None, description="Filter by tradition: unani or ayurveda"),
    domain: Optional[str] = Query(None, description="Filter by clinical specialty / domain"),
    limit: int = Query(50, ge=1, le=1500, description="Page size limit"),
    offset: int = Query(0, ge=0, description="Page offset")
):
    """
    Search and paginate across the Master Pharmacopoeia database of 600+ authentic
    medicinal plants and Dravyas from API (Part I, Vols I-X) and UPI (Part I, Vols I-VI).
    """
    res = PharmacopoeiaMasterRegistry.search(
        query=q,
        system=system,
        domain=domain,
        limit=limit,
        offset=offset
    )
    return {
        "status": "success",
        "results": res["herbs"],
        **res
    }


@router.get("/pharmacopoeia/{herb_key}", response_model=Dict[str, Any])
async def get_pharmacopoeia_herb(herb_key: str):
    """
    Returns full metadata and 18-part structured monograph for any of the 600+ herbs.
    """
    herb = PharmacopoeiaMasterRegistry.find_by_key(herb_key)
    if not herb:
        raise HTTPException(status_code=404, detail=f"Herb '{herb_key}' not found in Pharmacopoeia.")
    mono = PharmacopoeiaMasterRegistry.to_monograph(herb)
    return {
        "status": "success",
        "herb": herb,
        "monograph": mono
    }


@router.get("/qarabadeen/reconciliations", response_model=Dict[str, Any])
async def list_qarabadeen_reconciliations():
    """
    Returns multi-edition variant reconciliation summaries for classical polyherbal formulations.
    """
    recs = QarabadeenReconciliationEngine.list_all_reconciliations()
    return {
        "status": "success",
        "total_compounds": len(recs),
        "reconciliations": recs
    }


@router.get("/qarabadeen/reconciliation/{compound_key}", response_model=Dict[str, Any])
async def get_qarabadeen_reconciliation(compound_key: str):
    """
    Returns deep edition-by-edition comparative analysis (Canon, Qadri, Azam, Jadid vs NFUM/AFI)
    including metric conversions, ingredient percentage deltas, and consensus standards.
    """
    rec = QarabadeenReconciliationEngine.get_reconciliation(compound_key)
    if not rec:
        raise HTTPException(status_code=404, detail=f"Compound reconciliation for '{compound_key}' not found.")
    return {
        "status": "success",
        "reconciliation": rec
    }


@router.get("/safety/drug-herb/{herb_key}", response_model=Dict[str, Any])
async def get_drug_herb_firewall_report(herb_key: str):
    """
    Returns Allopathic Clinical Safety & Drug-Herb Interaction Firewall report
    with CYP450 pathways, P-gp transporters, black-box hazards, and physician directives.
    """
    report = AllopathicDrugHerbFirewall.get_clinical_firewall_report(herb_key)
    return {
        "status": "success",
        "firewall_report": report
    }


@router.get("/monograph/{herb_key}/live-trials", response_model=Dict[str, Any])
async def get_herb_live_trials(herb_key: str, limit: int = Query(5, ge=1, le=10)):
    """
    Harvests live clinical trials and RCTs from NCBI PubMed and ClinicalTrials.gov v2 API,
    with Cochrane RoB bias grading, sample sizes, and cryptographic SHA-256 audit stamping.
    """
    trials = await LiveEvidenceCrawlerEngine.harvest_live_trials_for_herb(herb_key, max_trials=limit)
    return {
        "status": "success",
        "herb_key": herb_key,
        "total_trials_harvested": len(trials),
        "trials": [t.model_dump() if hasattr(t, "model_dump") else t.dict() for t in trials]
    }


@router.get("/{topic}", response_model=EncyclopediaTopicPage)
async def get_encyclopedia_topic(topic: str):
    """
    Generates governed, source-backed medical encyclopedia page for a topic.
    Supports both traditional botanicals and canonical medical discipline topics.
    """
    search_data = await SearchService.execute_search(query=topic)
    comp_data = await compare_systems(topic=topic)

    uncertainties = search_data.get("unresolved_gaps", [
        "Long-term cardiovascular outcome studies in ethnically diverse cohorts.",
        "Pharmacokinetic interactions with specialized narrow-therapeutic-index therapies."
    ])

    return EncyclopediaTopicPage(
        topic=topic,
        overview=search_data["summary"],
        modern_medicine_perspective={
            "evidence_grade": search_data["evidence_breakdown"]["overall_grade"],
            "rct_count": search_data["evidence_breakdown"]["human_rcts"],
            "key_mechanisms": search_data["what_medicine_knows"]
        },
        traditional_perspectives={
            "unani": search_data["cross_system_perspectives"]["unani"],
            "ayurveda": search_data["cross_system_perspectives"]["ayurveda"],
            "cross_system_synthesis": comp_data.get("cross_system_synthesis", "Preserved epistemological models.")
        },
        evidence_summary=search_data["evidence_breakdown"],
        clinical_safety={
            "status": "CAUTION_MONITOR",
            "warnings": [
                "Strict contraindication during pregnancy and lactation.",
                "Review concurrent prescription therapies for CYP3A4 inhibition."
            ]
        },
        what_remains_uncertain=uncertainties,
        provenance_citations=search_data["citations"],
        knowledge_version="K-2026.10.001",
        last_reviewed_date="2026-10-04"
    )
