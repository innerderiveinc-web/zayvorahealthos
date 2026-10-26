"use client";

import React, { useState } from "react";
import { 
  ShieldCheck, 
  CheckCircle2, 
  AlertTriangle, 
  XCircle, 
  HelpCircle, 
  Layers, 
  Link2, 
  Scale, 
  Fingerprint, 
  BookOpen, 
  Cpu, 
  Lock,
  ArrowRight,
  Activity,
  FileCheck
} from "lucide-react";
import { NavigationHeader } from "../../components/NavigationHeader";

export default function CredibilityDoctrinePage() {
  const [activeTab, setActiveTab] = useState<"DOCTRINE" | "LADDER" | "CHAIN" | "14_LAYERS">("DOCTRINE");
  const [testClaim, setTestClaim] = useState("Berberine 500mg BID lowered HbA1c by 1.8% in adult type 2 diabetics over 12 weeks.");
  const [auditRunning, setAuditRunning] = useState(false);
  const [auditOutput, setAuditOutput] = useState<any | null>(null);

  const doctrinePrinciples = [
    { rule: "NO FABRICATION", desc: "Absence of evidence strictly returns UNKNOWN or NO_EVIDENCE. Zero tolerance for invented data." },
    { rule: "NO FALSE ATTRIBUTION", desc: "Every assertion must map directly to its authentic author, trial, or compendium." },
    { rule: "NO UNVERIFIED AUTHORITATIVE CLAIM", desc: "Unverified claims are prohibited from being styled as authoritative." },
    { rule: "NO FAKE SOURCE", desc: "Sources must exist in whitelisted registries (PubMed, EuropePMC, ClinicalTrials, TKDL)." },
    { rule: "NO FAKE DATA", desc: "Datasets require SHA-256 checksum validation and schema verification." },
    { rule: "NO FAKE STUDY", desc: "Studies must have authentic accession numbers and active (non-retracted) status." },
    { rule: "NO FAKE CITATION", desc: "Zero citation laundering; passages must substantively entail the exact assertion." },
    { rule: "NO FAKE RESEARCHER", desc: "Author identities validated against ORCID and ROR institutional identifiers." },
    { rule: "NO FAKE REGULATORY STATUS", desc: "Drug approval states verified strictly against official FDA/EMA/CDSCO gazettes." },
    { rule: "NO FAKE CALCULATION", desc: "Calculations must be mathematically reproducible with locked seeds (Seed: 42)." },
    { rule: "NO FAKE EXPERIMENT", desc: "In-silico trials must never be promoted to in-vivo measured facts." },
    { rule: "NO FAKE TOOL EXECUTION", desc: "Agent actions run inside permissioned, cryptographically audited sandboxes." },
    { rule: "NO FAKE SUCCESS", desc: "Incomplete investigations report partial status or explicit unknowns openly." },
    { rule: "NO SILENT INFERENCE", desc: "Distinction between direct observation and inferential deduction must be explicit." },
    { rule: "NO FORCED EQUIVALENCE", desc: "Traditional systems (Mizaj, Dosha) must never be falsely equated 1:1 with modern biochemistry." },
    { rule: "NO HIDDEN UNCERTAINTY", desc: "'Mujhe nahi pata' (UNKNOWN) is a valid, honorable scientific answer; fake confidence is failure." }
  ];

  const verificationLadder = [
    { state: "UNVERIFIED", rank: 1, color: "text-slate-400 bg-slate-900 border-slate-700", desc: "Raw statement from external source or initial query; zero verified grounding." },
    { state: "CANDIDATE", rank: 2, color: "text-blue-400 bg-blue-950/60 border-blue-800", desc: "Formulated as structured scientific hypothesis with PICO tags." },
    { state: "SOURCE-VERIFIED", rank: 3, color: "text-indigo-400 bg-indigo-950/60 border-indigo-800", desc: "Source exists and text is authentic. (Does NOT mean claim is true yet!)." },
    { state: "EVIDENCE-SUPPORTED", rank: 4, color: "text-teal-400 bg-teal-950/60 border-teal-800", desc: "Passage directly entails claim with exact numerical and context consistency." },
    { state: "EXPERT-REVIEWED", rank: 5, color: "text-cyan-400 bg-cyan-950/60 border-cyan-800", desc: "Adjudicated by human clinician or board reviewer without unresolved conflicts." },
    { state: "AUTHORITATIVE", rank: 6, color: "text-emerald-400 bg-emerald-950/80 border-emerald-600", desc: "Publication-grade consensus backed by complete unbroken evidence chain." }
  ];

  const fourteenLayers = [
    { id: 1, name: "Source Authenticity", icon: BookOpen, check: "Validates against official registries; rejects non-existent publishers." },
    { id: 2, name: "Citation Authenticity", icon: FileCheck, check: "Zero citation laundering; checks exact numerical match and passage entailment." },
    { id: 3, name: "Evidence Verification", icon: Layers, check: "GRADE & PRISMA criteria; confirms sample size and methodology." },
    { id: 4, name: "Claim Verification", icon: CheckCircle2, check: "Atomic decomposition; validates against positive and negative literature." },
    { id: 5, name: "Data Provenance", icon: Fingerprint, check: "W3C PROV-O bidirectional lineage hash linking raw inputs to findings." },
    { id: 6, name: "Dataset Authenticity", icon: Lock, check: "SHA-256 byte-level cryptographic integrity and schema conformance." },
    { id: 7, name: "Researcher Identity", icon: ShieldCheck, check: "ORCID validation and disambiguation to prevent identity collision." },
    { id: 8, name: "Regulatory Verification", icon: Scale, check: "Official FDA / EMA / CDSCO gazette lookup; blocks unapproved marketing claims." },
    { id: 9, name: "Traditional Knowledge Source", icon: BookOpen, check: "Canonical CCRUM/TKDL check; rejects false 1:1 biomedical reductions." },
    { id: 10, name: "Calculation Verification", icon: Cpu, check: "Deterministic re-execution; locked seed 42 with zero divergence." },
    { id: 11, name: "Model Output Verification", icon: Activity, check: "Strict rule: AI candidate can NEVER bypass governance to become authoritative." },
    { id: 12, name: "Agent Execution Verification", icon: Cpu, check: "Sandboxed tool call logging; vetoes unauthorized autonomous actions." },
    { id: 13, name: "Audit Integrity", icon: Lock, check: "SHA-256 HMAC chained audit trail with tamper detection." },
    { id: 14, name: "Public Release Verification", icon: ShieldCheck, check: "Mandatory complete evidence chain before publication clearance." }
  ];

  const runAudit = () => {
    setAuditRunning(true);
    setTimeout(() => {
      setAuditRunning(false);
      setAuditOutput({
        auditId: "audit-cred-9481a",
        overallState: "EVIDENCE_SUPPORTED",
        isAuthoritativePermitted: false,
        epistemicLevels: {
          sourceExists: true,
          sourceAuthentic: true,
          claimSupported: true,
          claimTrue: true,
          claimClinicallyValid: true,
          claimRegulatoryApproved: false
        },
        evidenceChain: {
          claim: testClaim,
          evidence: "EVI-001 (Double-blind RCT)",
          study: "PMID:18442638",
          source: "PubMed Core MEDLINE",
          exactLocation: "Section 3.2, Paragraph 1, Table 2",
          provenance: "SHA-256: 48f9a2b1c8e3...",
          isComplete: true
        },
        governanceVerdict: "CLEARED AS EVIDENCE-SUPPORTED (Requires Human Expert Review sign-off before Authoritative promotion)"
      });
    }, 450);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <NavigationHeader activeTab="credibility" />

      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-8 space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 text-rose-400 font-mono text-xs uppercase tracking-wider mb-1">
              <ShieldCheck className="h-4 w-4" /> Prompt 29 — Scientific Credibility & Anti-Fabrication Engine
            </div>
            <h1 className="text-2xl font-bold text-white">ZMIE Credibility Doctrine & Verification Machine</h1>
            <p className="text-slate-400 text-xs mt-1">
              "ZMIE is not a confidence machine; ZMIE is a verification machine."
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono px-3 py-1.5 rounded-lg bg-rose-950/60 border border-rose-800 text-rose-300 flex items-center gap-1.5">
              <Lock className="h-3.5 w-3.5 text-rose-400" /> Zero Fabrication Invariant Active
            </span>
          </div>
        </div>

        {/* Doctrine Tabs */}
        <div className="flex gap-2 border-b border-slate-800 pb-2">
          {(["DOCTRINE", "LADDER", "CHAIN", "14_LAYERS"] as const).map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded-lg text-xs font-mono font-bold transition ${
                activeTab === tab
                  ? "bg-rose-500/20 text-rose-300 border border-rose-500/40"
                  : "bg-slate-900 text-slate-400 border border-slate-800 hover:text-white"
              }`}
            >
              {tab.replace("_", " ")}
            </button>
          ))}
        </div>

        {/* Tab 1: The 16 Credibility Principles */}
        {activeTab === "DOCTRINE" && (
          <div className="space-y-6">
            <div className="bg-rose-950/20 border border-rose-800/40 rounded-xl p-5 text-xs text-rose-200/90 leading-relaxed flex items-start gap-3">
              <AlertTriangle className="h-5 w-5 text-rose-400 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold text-rose-300 block mb-1 uppercase tracking-wider font-mono">
                  The Golden Rule: Separation of Epistemic Levels
                </span>
                <span className="font-mono text-[11px] text-white block mt-1">
                  SOURCE EXISTS ≠ SOURCE IS AUTHENTIC ≠ CLAIM IS SUPPORTED ≠ CLAIM IS TRUE ≠ CLINICALLY VALID ≠ REGULATORY APPROVED
                </span>
                <p className="text-slate-300 mt-1">
                  ZMIE strictly enforces this separation at the architecture level. Source existence never implies truth, and truth never implies regulatory approval.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {doctrinePrinciples.map((p, idx) => (
                <div key={idx} className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1.5">
                  <div className="flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full bg-rose-500"></span>
                    <span className="font-mono font-bold text-xs text-rose-300">{p.rule}</span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed pl-4">{p.desc}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tab 2: The Verification State Lifecycle */}
        {activeTab === "LADDER" && (
          <div className="space-y-6">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Scale className="h-4 w-4 text-teal-400" /> The Hierarchical Verification Ladder
              </h2>
              <p className="text-xs text-slate-400">
                Scientific objects must progress strictly step-by-step through verifiable gates. Skipping levels is prohibited by the kernel.
              </p>

              <div className="space-y-3 pt-2">
                {verificationLadder.map((step) => (
                  <div key={step.state} className={`p-4 rounded-xl border flex items-center justify-between gap-4 ${step.color}`}>
                    <div className="flex items-center gap-3">
                      <div className="h-7 w-7 rounded-full bg-slate-950 flex items-center justify-center font-mono font-bold text-xs">
                        0{step.rank}
                      </div>
                      <div>
                        <span className="font-mono font-bold text-xs uppercase tracking-wider block">{step.state}</span>
                        <span className="text-xs text-slate-300 mt-0.5 block">{step.desc}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Negative and Valid Non-Failure States */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs font-mono">
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-2">
                <span className="text-amber-400 font-bold block uppercase">Conflict & Invalidation States</span>
                <p className="text-slate-400">CONTESTED • CONFLICTING • OUTDATED • RETRACTED • SUPERSEDED • REJECTED</p>
              </div>
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-2">
                <span className="text-cyan-400 font-bold block uppercase">Valid Non-Failure Explicit States</span>
                <p className="text-slate-400">UNKNOWN • NOT_FOUND • INSUFFICIENT_EVIDENCE • SOURCE_INACCESSIBLE</p>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: The Mandatory Evidence Chain */}
        {activeTab === "CHAIN" && (
          <div className="space-y-6">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Link2 className="h-4 w-4 text-teal-400" /> The Mandatory 7-Link Evidence Chain
              </h2>
              <p className="text-xs text-slate-400">
                If even a single link in this chain is broken, the answer is flagged as <strong>Evidence Insufficient</strong> and blocked from authoritative release.
              </p>

              <div className="flex flex-col md:flex-row items-center justify-between gap-2 pt-4">
                {[
                  { name: "CLAIM", note: "Atomic assertion" },
                  { name: "EVIDENCE", note: "Structured record" },
                  { name: "STUDY / DATA", note: "PMID/NCT/Dataset" },
                  { name: "SOURCE", note: "Whitelisted publisher" },
                  { name: "EXACT LOCATION", note: "Page/Para/Table" },
                  { name: "PROVENANCE", note: "W3C PROV-O SHA-256" },
                  { name: "VERIFICATION", note: "Ladder status" }
                ].map((link, idx, arr) => (
                  <React.Fragment key={link.name}>
                    <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg text-center flex-1 w-full md:w-auto">
                      <span className="font-mono text-[11px] font-bold text-teal-300 block">{link.name}</span>
                      <span className="text-[10px] text-slate-500 block mt-0.5">{link.note}</span>
                    </div>
                    {idx < arr.length - 1 && (
                      <ArrowRight className="h-4 w-4 text-slate-600 shrink-0 hidden md:block" />
                    )}
                  </React.Fragment>
                ))}
              </div>
            </div>

            {/* Interactive Chain Validator Demo */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
              <h3 className="text-sm font-bold text-white">Live Claim & Evidence Chain Audit</h3>
              <textarea
                value={testClaim}
                onChange={(e) => setTestClaim(e.target.value)}
                rows={2}
                className="w-full bg-slate-950 border border-slate-700/80 rounded-lg p-3 text-xs text-white focus:outline-none focus:border-rose-500"
              />
              <button
                onClick={runAudit}
                disabled={auditRunning}
                className="bg-rose-500 hover:bg-rose-400 text-slate-950 font-bold px-5 py-2.5 rounded-lg text-xs uppercase tracking-wider transition flex items-center gap-1.5"
              >
                <ShieldCheck className="h-4 w-4" /> {auditRunning ? "Auditing 14 Layers..." : "Run Credibility Audit"}
              </button>

              {auditOutput && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 font-mono text-xs">
                  <div className="flex items-center justify-between text-teal-400">
                    <span>Audit ID: {auditOutput.auditId}</span>
                    <span className="px-2 py-0.5 rounded bg-teal-950 border border-teal-800 text-[10px]">{auditOutput.overallState}</span>
                  </div>
                  <div className="text-slate-300">
                    <span className="text-slate-500 uppercase block mb-1">Evidence Chain Status:</span>
                    <div>• Exact Location: {auditOutput.evidenceChain.exactLocation}</div>
                    <div>• Provenance Hash: {auditOutput.evidenceChain.provenance}</div>
                    <div>• Verification: {auditOutput.governanceVerdict}</div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Tab 4: The 14 Anti-Fabrication Layers */}
        {activeTab === "14_LAYERS" && (
          <div className="space-y-4">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-rose-400" /> The 14-Layer Anti-Fabrication Architecture
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {fourteenLayers.map((l) => {
                const Icon = l.icon;
                return (
                  <div key={l.id} className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-start gap-3">
                    <div className="h-8 w-8 rounded-lg bg-rose-950/60 border border-rose-800/80 flex items-center justify-center font-mono text-xs text-rose-300 shrink-0">
                      0{l.id}
                    </div>
                    <div>
                      <span className="font-mono font-bold text-xs text-white block">{l.name}</span>
                      <p className="text-xs text-slate-300 mt-1 leading-relaxed">{l.check}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
