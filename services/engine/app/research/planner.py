"""
ZMIE Research Planner Agent
Decomposes complex biomedical and cross-system medical research questions into:
- Structured PICO framework
- Precise sub-questions
- Explicit Inclusion/Exclusion criteria
- Cross-tradition terminology search matrix
"""

from typing import List, Dict, Any, Optional
import uuid
import re

from app.models.research import ResearchPlan, PICOFramework, InclusionExclusionCriteria, SearchMatrixItem
from app.models.claim import MedicalSystem, EvidenceGrade


class ResearchPlannerAgent:
    """
    Subagent responsible for decomposing and pre-flight planning research tasks.
    Enforces the 'Plan-First' architectural rule.
    """

    @classmethod
    def create_plan(
        cls,
        question: str,
        target_systems: Optional[List[str]] = None,
        budget_limit: int = 100
    ) -> ResearchPlan:
        """
        Decomposes the query into sub-questions, extracts PICO, and formulates search matrix.
        """
        if not target_systems:
            target_systems = ["modern", "unani", "ayurveda"]

        enum_systems = []
        for s in target_systems:
            s_clean = s.lower().strip()
            if s_clean == "unani":
                enum_systems.append(MedicalSystem.UNANI)
            elif s_clean == "ayurveda":
                enum_systems.append(MedicalSystem.AYURVEDA)
            elif s_clean in ["siddha", "tcm"]:
                enum_systems.append(MedicalSystem.TRADITIONAL)
            else:
                enum_systems.append(MedicalSystem.MODERN)

        # 1. PICO Extraction heuristic
        pico = cls._extract_pico(question, enum_systems)

        # 2. Sub-questions decomposition
        sub_questions = cls._decompose_sub_questions(question, pico)

        # 3. Inclusion & Exclusion Criteria
        criteria = cls._formulate_criteria(pico, target_systems)

        # 4. Cross-domain Search Matrix
        search_matrix = cls._build_search_matrix(pico, sub_questions)

        plan = ResearchPlan(
            plan_id=f"plan-{uuid.uuid4().hex[:8]}",
            title=f"Investigation: {question[:80]}...",
            primary_question=question,
            sub_questions=sub_questions,
            pico=pico,
            criteria=criteria,
            search_matrix=search_matrix,
            budget_limit_sources=budget_limit,
            plan_version=1
        )
        return plan

    @classmethod
    def _extract_pico(cls, question: str, systems: List[MedicalSystem]) -> PICOFramework:
        q_lower = question.lower()

        # Intervention extraction heuristics
        intervention = "Target Medical Intervention"
        if "berberine" in q_lower:
            intervention = "Berberine (isoquinoline alkaloid)"
        elif "curcumin" in q_lower or "turmeric" in q_lower:
            intervention = "Curcumin / Standardized Curcuminoids"
        elif "metformin" in q_lower:
            intervention = "Metformin"
        elif "ashwagandha" in q_lower or "withania" in q_lower:
            intervention = "Withania somnifera (Ashwagandha extract)"
        elif "asgandh" in q_lower:
            intervention = "Asgandh (Withania somnifera root powder)"
        elif "artemisia" in q_lower or "afsanteen" in q_lower:
            intervention = "Artemisia absinthium (Afsanteen)"
        else:
            # Fallback simple extraction
            match = re.search(r'(?:effect of|role of|efficacy of|does)\s+([a-zA-Z0-9\s\-_]+?)(?:\s+in|\s+on|\s+for|\s+reduce|\s+cause|\?|$)', question, re.IGNORECASE)
            if match:
                intervention = match.group(1).strip().title()

        # Population extraction heuristics
        population = "Target Clinical Population"
        if "type 2 diabetes" in q_lower or "t2d" in q_lower or "diabetic" in q_lower:
            population = "Adults with Type 2 Diabetes Mellitus / Insulin Resistance"
        elif "alzheimer" in q_lower or "cognitive" in q_lower:
            population = "Patients with Mild-to-Moderate Cognitive Impairment / Alzheimer's Disease"
        elif "hypertension" in q_lower or "blood pressure" in q_lower:
            population = "Adults with Stage 1 or Stage 2 Essential Hypertension"
        elif "fatty liver" in q_lower or "nafld" in q_lower or "mash" in q_lower:
            population = "Adult patients with Non-Alcoholic Fatty Liver Disease (NAFLD / MASH)"
        elif "insomnia" in q_lower or "sleep" in q_lower:
            population = "Adults with primary or stress-induced insomnia"
        elif "rheumatoid" in q_lower or "arthritis" in q_lower:
            population = "Adult patients with Active Rheumatoid Arthritis"
        else:
            match = re.search(r'(?:in|for|among)\s+([a-zA-Z0-9\s\-_]+?)(?:\s+patients|\s+cohorts|\s+subjects|\?|$)', question, re.IGNORECASE)
            if match:
                population = f"Patients with {match.group(1).strip()}"

        # Comparator extraction heuristics
        comparator = "Standard Care or Placebo"
        if "versus" in q_lower or " vs " in q_lower or "compared to" in q_lower:
            match = re.search(r'(?:versus|vs\.?|compared to)\s+([a-zA-Z0-9\s\-_]+?)(?:\s+in|\s+for|\?|$)', question, re.IGNORECASE)
            if match:
                comparator = match.group(1).strip().title()
        elif "metformin" in q_lower and "berberine" in q_lower:
            comparator = "Metformin standard dosing (500mg-1500mg/day)"

        # Outcomes extraction
        outcomes = []
        if "glucose" in q_lower or "hba1c" in q_lower or "diabetes" in q_lower:
            outcomes.extend(["HbA1c reduction", "Fasting blood glucose", "Homeostatic model insulin resistance (HOMA-IR)"])
        if "lipid" in q_lower or "cholesterol" in q_lower or "triglyceride" in q_lower:
            outcomes.extend(["LDL-C reduction", "Total triglycerides", "HDL-C levels"])
        if "safety" in q_lower or "adverse" in q_lower or "toxic" in q_lower:
            outcomes.extend(["Incidence of adverse events", "Hepatic safety (ALT/AST)", "Renal safety (eGFR/Creatinine)"])
        if "cognitive" in q_lower or "memory" in q_lower:
            outcomes.extend(["MMSE / ADAS-Cog score change", "Neuroinflammatory biomarkers"])
        if not outcomes:
            outcomes = ["Primary efficacy biomarker endpoint", "Secondary clinical symptom score", "Safety profile and adverse events"]

        return PICOFramework(
            population=population,
            intervention=intervention,
            comparator=comparator,
            outcomes=outcomes,
            target_systems=systems
        )

    @classmethod
    def _decompose_sub_questions(cls, question: str, pico: PICOFramework) -> List[str]:
        sub_questions = [
            f"What is the quantitative clinical efficacy of {pico.intervention} on {', '.join(pico.outcomes[:2])} in {pico.population}?",
            f"What molecular and physiological mechanisms of action explain the effects of {pico.intervention}?",
            f"How does the safety and adverse event profile of {pico.intervention} compare to {pico.comparator or 'standard care'}?",
            f"What conflicting outcomes or contradictory trial findings exist in the current literature regarding {pico.intervention}?",
            f"How is {pico.intervention} framed in traditional paradigms (Unani Mizaj / Ayurveda Dosha), and what classical preparation nuances affect bioavailability?"
        ]
        return sub_questions

    @classmethod
    def _formulate_criteria(cls, pico: PICOFramework, systems: List[str]) -> InclusionExclusionCriteria:
        inclusion = [
            f"Peer-reviewed studies or authoritative classical compendia addressing {pico.intervention}",
            f"Studies involving {pico.population} or physiologically relevant in vivo animal models",
            "Human clinical trials (RCTs), prospective cohort studies, systematic reviews, or recognized pharmacopoeial entries",
            "Studies published in English or official translation with verified methodology and attribution"
        ]
        exclusion = [
            "In vitro cell-line assays with unphysiologically high concentrations without bioavailability correlation",
            "Unsubstantiated marketing brochures or non-peer-reviewed promotional claims",
            "Retracted papers or papers under active integrity investigation",
            "Studies missing defined dosage, duration, or extract standardization specifics"
        ]
        return InclusionExclusionCriteria(
            inclusion=inclusion,
            exclusion=exclusion,
            min_evidence_grade=EvidenceGrade.CANONICAL_TRADITIONAL,
            allowed_systems=systems
        )

    @classmethod
    def _build_search_matrix(cls, pico: PICOFramework, sub_questions: List[str]) -> List[SearchMatrixItem]:
        matrix = []

        # Interventions terms
        int_base = pico.intervention.split()[0]
        matrix.append(
            SearchMatrixItem(
                sub_question=sub_questions[0],
                target_domains=["OpenAlex", "Europe PMC", "ClinicalTrials.gov"],
                mesh_terms=[int_base, "Clinical Trials as Topic", "Treatment Outcome", "Biomarkers"],
                traditional_terms=[],
                retrieval_strategy="EVIDENCE_LADDER_FIRST"
            )
        )
        matrix.append(
            SearchMatrixItem(
                sub_question=sub_questions[1],
                target_domains=["OpenAlex", "Europe PMC"],
                mesh_terms=[int_base, "Mechanisms of Action", "Signal Transduction", "Pharmacology"],
                traditional_terms=[],
                retrieval_strategy="MECHANISTIC_PATHWAY"
            )
        )
        matrix.append(
            SearchMatrixItem(
                sub_question=sub_questions[2],
                target_domains=["Europe PMC", "FDA/EMA Guidance", "ClinicalTrials.gov"],
                mesh_terms=[int_base, "Drug-Related Side Effects and Adverse Reactions", "Drug Interactions", "Cytochrome P-450"],
                traditional_terms=[],
                retrieval_strategy="SAFETY_FIREWALL"
            )
        )
        matrix.append(
            SearchMatrixItem(
                sub_question=sub_questions[4],
                target_domains=["AYUSH Portal", "CCUM", "CCRAS", "Traditional Compendia"],
                mesh_terms=[],
                traditional_terms=[int_base, "Mizaj", "Mufradat", "Dosha", "Dravyaguna", "Shodhana"],
                retrieval_strategy="CROSS_SYSTEM_SYNTHESIS"
            )
        )
        return matrix
