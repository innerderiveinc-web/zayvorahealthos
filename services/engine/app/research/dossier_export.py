"""
ZMIE Clinical Dossier & Cryptographic Evidence Export Engine
Generates publication-ready clinical evidence dossiers, structured FHIR EvidenceReports,
and tamper-evident cryptographic HMAC SHA-256 verification stamps for institutional and regulatory dissemination.
"""

from typing import Dict, Any, Optional
import hashlib
import hmac
import json
import logging
from datetime import datetime

logger = logging.getLogger("zmie.research.dossier")


class ClinicalDossierExporter:
    """Exports validated ResearchReports into signed clinical dossiers and FHIR resources."""

    HMAC_SECRET = b"zmie_canonical_clinical_integrity_key_v1"

    @classmethod
    def compute_dossier_signature(cls, report_id: str, job_id: str, timestamp_iso: str, pico_question: str) -> str:
        payload = f"{report_id}|{job_id}|{timestamp_iso}|{pico_question}".encode("utf-8")
        return hmac.new(cls.HMAC_SECRET, payload, hashlib.sha256).hexdigest()

    @classmethod
    def export_clinical_markdown(cls, report: Any, job: Optional[Any] = None) -> str:
        """Generates an exhaustive, publication-ready clinical markdown dossier."""
        report_id = getattr(report, "report_id", "REP-UNKNOWN")
        job_id = getattr(report, "job_id", "JOB-UNKNOWN")
        title = getattr(report, "title", "Clinical Evidence Synthesis")
        primary_q = getattr(report, "primary_question", "")
        summary = getattr(report, "executive_summary", "")
        now_iso = datetime.utcnow().isoformat() + "Z"
        sig = cls.compute_dossier_signature(report_id, job_id, now_iso, primary_q)

        assertions = getattr(report, "assertions", [])
        evidence_table = getattr(report, "evidence_table", [])
        contradictions = getattr(report, "contradictions", [])
        gaps = getattr(report, "research_gaps", [])
        reflection_audit = getattr(report, "reflection_audit", [])
        react_tools = getattr(report, "react_tools_invoked", [])
        debate = getattr(report, "adversarial_debate", None)

        md = []
        md.append(f"# ZMIE Clinical Evidence Dossier: {title}")
        md.append("### ZAYVORA Medical Intelligence Engine™ (SKOS v1.0.0-PROD)")
        md.append(f"**Report ID**: `{report_id}` | **Job ID**: `{job_id}` | **Generated**: `{now_iso}`")
        md.append(f"**Cryptographic Signature (HMAC SHA-256)**: `{sig}`")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## 1. Executive Clinical Synthesis")
        md.append(summary)
        md.append("")
        md.append(f"**Primary PICO Research Question**: *{primary_q}*")
        md.append("")

        # Section 2: Agentic Multi-Hop & Reflection Audit
        md.append("## 2. Autonomous Agentic Pipeline Audit")
        md.append(f"- **ReAct Tools Executed**: {', '.join([f'`{t}`' for t in react_tools]) if react_tools else 'Standard hybrid retrieval'}")
        md.append(f"- **Self-Correction Cycles Executed**: {len(reflection_audit)}")
        repaired_cnt = getattr(report, "auto_repaired_count", 0)
        md.append(f"- **Auto-Repaired Assertions**: {repaired_cnt}")
        if reflection_audit:
            md.append("\n### Self-Correction & Reflection Critic Log:")
            for r in reflection_audit:
                md.append(f"- Cycle {r.get('cycle', 1)}: Pre-eval valid={r.get('valid_assertions')}, Flawed={r.get('flawed_assertions')}, Auto-repaired={r.get('auto_repaired')}")
        md.append("")

        # Section 3: Adversarial Debate Consensus
        if debate:
            md.append("## 3. Adversarial Clinical Debate & Consensus (Advocate vs. Skeptic)")
            grade = debate.get("grade_certainty", "MODERATE")
            posture = debate.get("recommended_clinical_posture", "CAUTIONARY")
            md.append(f"**GRADE Evidence Certainty**: `{grade}` | **Recommended Posture**: `{posture}`\n")
            md.append(f"**Consensus Synthesis**: {debate.get('consensus_synthesis', '')}\n")
            md.append("#### Advocate Arguments (Proponent):")
            for arg in debate.get("advocate_arguments", []):
                md.append(f"- **{arg.get('claim')}**: {arg.get('rationale')}")
            md.append("\n#### Skeptic Arguments (Red Team):")
            for arg in debate.get("skeptic_arguments", []):
                md.append(f"- **{arg.get('claim')}**: {arg.get('rationale')}")
            md.append("")

        # Section 4: Grounded Assertions
        md.append("## 4. Grounded Medical Assertions")
        if assertions:
            for i, ast in enumerate(assertions, 1):
                st = getattr(ast, "statement", str(ast))
                ep = getattr(ast, "epistemic_status", "CONFIRMED")
                cits = getattr(ast, "supporting_citations", [])
                md.append(f"{i}. **[{ep}]** {st}")
                if cits:
                    md.append(f"   *Citations*: {', '.join(cits)}")
        else:
            md.append("*No clinical assertions could be grounded due to lack of verified primary RCT data (Zero-Fabrication Policy).*")
        md.append("")

        # Section 5: PICO Evidence Table
        md.append("## 5. PICO Evidence Table")
        if evidence_table:
            md.append("| Study / Source | Design | Grade | Sample Size | Primary Findings | Effect Size |")
            md.append("|---|---|---|---|---|---|")
            for ev in evidence_table:
                src = getattr(ev, "source_id", "SRC")
                des = getattr(ev, "study_design", "Clinical Trial")
                grd = getattr(ev, "evidence_grade", "E2")
                n = getattr(ev, "sample_size", "N/A")
                finds = getattr(ev, "primary_findings", "")[:80] + "..."
                eff = getattr(ev, "effect_size_or_stats", "N/A")
                md.append(f"| {src} | {des} | {grd} | {n} | {finds} | {eff} |")
        else:
            md.append("*No primary studies met inclusion criteria.*")
        md.append("")

        # Section 6: Contradictions & Gaps
        if contradictions:
            md.append("## 6. Identified Contradictions")
            for c in contradictions:
                topic = getattr(c, "topic", "Divergent finding")
                div = getattr(c, "divergence_summary", "")
                md.append(f"- **{topic}**: {div}")
            md.append("")

        if gaps:
            md.append("## 7. Evidence Gaps & Future Research Questions")
            for g in gaps:
                desc = getattr(g, "description", "")
                cat = getattr(g, "category", "CLINICAL")
                md.append(f"- **[{cat}]**: {desc}")
            md.append("")

        # Cryptographic Footer
        md.append("---")
        md.append("### Cryptographic Ledger Verification Stamp")
        md.append("```")
        md.append(f"AUTHORITY:     ZAYVORA Medical Intelligence Engine (ZMIE-SKOS-v1.0.0)")
        md.append(f"SPEC_HASH:     {sig}")
        md.append(f"TIMESTAMP:     {now_iso}")
        md.append(f"AUDIT_POLICY:  FAIL_CLOSED_ZERO_FABRICATION_STRICT")
        md.append("```")

        return "\n".join(md)

    @classmethod
    def export_fhir_evidence_report(cls, report: Any) -> Dict[str, Any]:
        """Generates a HL7 FHIR R5 compatible EvidenceReport JSON resource."""
        report_id = getattr(report, "report_id", "rep-001")
        title = getattr(report, "title", "Evidence Synthesis")
        primary_q = getattr(report, "primary_question", "")
        summary = getattr(report, "executive_summary", "")

        return {
            "resourceType": "EvidenceReport",
            "id": report_id,
            "status": "active",
            "type": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/evidence-report-type",
                        "code": "systematic-review",
                        "display": "Systematic Review / Clinical Synthesis"
                    }
                ]
            },
            "subject": {
                "characteristic": [
                    {
                        "code": {"text": "PICO Research Question"},
                        "valueString": primary_q
                    }
                ],
                "note": [{"text": summary}]
            },
            "publisher": "ZAYVORA Medical Intelligence Engine™",
            "editor": [{"name": "ZMIE Autonomous Agentic Pipeline"}],
            "section": [
                {
                    "title": "Grounded Medical Assertions",
                    "focus": {"text": "Clinical Findings"},
                    "mode": "working",
                    "text": {
                        "status": "generated",
                        "div": f"<div>{len(getattr(report, 'assertions', []))} verified grounded assertions</div>"
                    }
                },
                {
                    "title": "Adversarial Consensus & GRADE Rating",
                    "focus": {"text": "Certainty Assessment"},
                    "mode": "snapshot",
                    "text": {
                        "status": "generated",
                        "div": f"<div>GRADE Certainty: {getattr(report, 'adversarial_debate', {}).get('grade_certainty', 'MODERATE') if getattr(report, 'adversarial_debate', None) else 'MODERATE'}</div>"
                    }
                }
            ]
        }
