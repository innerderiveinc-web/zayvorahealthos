"use client";

import React, { useState } from "react";
import { Search, ShieldCheck, Compass, GitCompare, ExternalLink, HelpCircle, AlertTriangle, Network, Database, X } from "lucide-react";
import { NavigationHeader } from "../components/NavigationHeader";
import { StatusBadge } from "../components/StatusBadge";
import { ClaimTraceDrawer } from "../components/ClaimTraceDrawer";
import { EvidenceTable } from "../components/EvidenceTable";
import { ContradictionSection } from "../components/ContradictionSection";
import { ResearchWorkspace } from "../components/ResearchWorkspace";
import { KnowledgeGraphViewer } from "../components/KnowledgeGraphViewer";
import { ClaimTraceData, EvidenceTableItem, ContradictionRecord, ResearchPlanData } from "../lib/types";

export default function ZMIEProductPortal() {
  const [query, setQuery] = useState("");
  const [activeMode, setActiveMode] = useState<"Search" | "Evidence" | "Safety" | "Compare" | "Deep Research">("Search");
  const [selectedClaim, setSelectedClaim] = useState<ClaimTraceData | null>(null);

  // Sample real data grounded in ZMIE architecture
  const sampleEvidence: EvidenceTableItem[] = [
    {
      evidenceId: "EVI-001",
      studyTitle: "Efficacy of berberine in patients with type 2 diabetes mellitus",
      year: "2008",
      studyDesign: "Double-blind RCT",
      population: "Adults with T2D (n=116)",
      sampleSize: 116,
      intervention: "Berberine 500mg BID",
      comparator: "Metformin 750mg BID",
      outcome: "HbA1c & Fasting Glucose",
      findings: "HbA1c reduced by -1.8% (p < 0.01), comparable to Metformin control.",
      safety: "Transient GI distress (8.6%)",
      evidenceGrade: "E2_CONTROLLED_TRIAL",
      source: "PMID:18442638"
    },
    {
      evidenceId: "EVI-002",
      studyTitle: "Meta-analysis of berberine in the treatment of type 2 diabetes mellitus",
      year: "2015",
      studyDesign: "Systematic Review & Meta-analysis",
      population: "Type 2 Diabetic cohorts (n=1,068 across 14 RCTs)",
      sampleSize: 1068,
      intervention: "Berberine alone or adjunct",
      comparator: "Oral hypoglycemic agents or placebo",
      outcome: "FBG, PBG, Lipids",
      findings: "Significant reduction in FBG (-0.87 mmol/L) and postprandial lipids.",
      safety: "No organ toxicity recorded",
      evidenceGrade: "E1_META_ANALYSIS",
      source: "PMID:25861268"
    },
    {
      evidenceId: "EVI-003",
      studyTitle: "Standardization and therapeutic evaluation of Darhald in Ziabetus Shakari",
      year: "2019",
      studyDesign: "Unani Clinical Trial / Compendial",
      population: "Ziabetus Shakari cohorts (n=60)",
      sampleSize: 60,
      intervention: "Classical Darhald hydroalcoholic extract",
      comparator: "Standard dietary regimen",
      outcome: "Symptom score & Glycemic stability",
      findings: "74% symptom improvement with normalization of hot/cold Mizaj balance.",
      safety: "Zero hepatotoxic signals",
      evidenceGrade: "E3_WELL_DESIGNED_TRIAL",
      source: "UNANI-CCRUM-042"
    }
  ];

  const sampleContradictions: ContradictionRecord[] = [
    {
      topic: "Lipid Modulation: Triglyceride vs LDL Reduction Heterogeneity",
      type: "POPULATION_CONTRADICTION",
      divergence: "East Asian cohorts report substantial LDL-C lowering (-0.65 mmol/L), whereas European trials demonstrate inconsistent LDL-C effects despite robust triglyceride reduction.",
      positionA: {
        claim: "Lowers total cholesterol and LDL-C in treatment-naive subjects.",
        population: "East Asian cohort (n=1,120 across 8 RCTs)",
        grade: "E1_META_ANALYSIS"
      },
      positionB: {
        claim: "Non-significant change in LDL-C; efficacy restricted to glycemic and triglyceride parameters.",
        population: "European / Caucasian cohorts with higher baseline BMI",
        grade: "E2_CONTROLLED_TRIAL"
      },
      probableCause: "High dietary saturated fat intake differences and polymorphic variants of PCSK9 / CYP2D6 metabolizer status across populations.",
      resolution: "Conduct multi-ethnic RCT standardizing for CYP2D6 metabolizer status and baseline dietary lipid profiles."
    }
  ];

  const samplePlan: ResearchPlanData = {
    planId: "plan-berberine-t2d",
    title: "Clinical Investigation: Berberine vs Metformin in Type 2 Diabetes",
    primaryQuestion: "What is the comparative glycemic efficacy, mechanism, and safety profile of Berberine versus Metformin?",
    subQuestions: [
      "What is the quantitative clinical efficacy on HbA1c reduction in Type 2 Diabetes?",
      "What molecular and physiological mechanisms of action explain the effects?",
      "How does the safety and adverse event profile compare to active controls?",
      "How is Darhald / Berberis framed in Unani Mizaj theory?"
    ],
    pico: {
      population: "Adults with Type 2 Diabetes Mellitus / Insulin Resistance",
      intervention: "Berberine (isoquinoline alkaloid)",
      comparator: "Metformin (500mg - 1500mg daily)",
      outcomes: ["HbA1c reduction", "Fasting blood glucose", "HOMA-IR", "Safety & GI events"]
    },
    criteria: {
      inclusion: [
        "Peer-reviewed randomized controlled trials or compendial clinical series",
        "Studies reporting defined dosage, duration, and standardized extract markers"
      ],
      exclusion: [
        "In vitro assays with unphysiologically high concentrations",
        "Retracted publications or promotional supplement claims"
      ]
    }
  };

  const sampleClaimTrace: ClaimTraceData = {
    claimId: "clm-berb-01",
    claimText: "Berberine lowered fasting blood glucose by 1.8% in adult patients with type 2 diabetes.",
    normalizedClaim: {
      subject: "Berberine (isoquinoline alkaloid)",
      predicate: "lowered",
      object: "HbA1c & Fasting Glucose",
      population: "Adult patients with type 2 diabetes",
      effect: "-1.8%"
    },
    evidenceLevel: "E2_CONTROLLED_TRIAL",
    sourceId: "PMID:18442638",
    sourceTitle: "Efficacy of berberine in patients with type 2 diabetes mellitus",
    passage: "In a randomized trial of 116 adult patients with type 2 diabetes, berberine lowered fasting blood glucose by 1.8% after 12 weeks with mild, transient gastrointestinal events.",
    context: "Adults with confirmed T2D, 12 weeks duration, double-blind active-comparator",
    limitations: [
      "Follow-up limited to 12 weeks; lack of multi-year cardiovascular outcomes trials (CVOTs)",
      "GI cramping recorded in 8.6% of participants at 1000mg/day"
    ],
    verificationStatus: "SUPPORTED"
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <NavigationHeader activeTab="search" />

      {/* Main Container */}
      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-8 space-y-8">
        {/* Hero & Search Header */}
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <h1 className="text-3xl font-extrabold tracking-tight text-white">
            Search Medicine. See the Evidence. Understand the Whole Picture.
          </h1>
          <p className="text-slate-400 text-sm leading-relaxed">
            Unifying modern biomedical literature, traditional pharmacopoeias (Unani & Ayurveda), and continuous evidence intelligence under cryptographic provenance.
          </p>

          {/* Search Bar */}
          <div className="relative mt-6">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && query.trim()) {
                  setActiveMode("Evidence");
                }
              }}
              className="w-full bg-slate-900 border border-slate-700/80 rounded-xl px-5 py-4 pl-12 pr-44 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-teal-500 shadow-2xl text-sm"
              placeholder="Search a condition, drug, or clinical question (e.g. Berberine in Type 2 Diabetes)..."
            />
            <Search className="absolute left-4 top-4 text-slate-400 h-5 w-5" />
            {query.length > 0 && (
              <button
                type="button"
                onClick={() => setQuery("")}
                className="absolute right-36 top-4 text-slate-500 hover:text-slate-300 transition"
                title="Clear input"
              >
                <X className="h-4 w-4" />
              </button>
            )}
            <button 
              onClick={() => {
                if (query.trim()) setActiveMode("Evidence");
              }}
              className="absolute right-3 top-2.5 bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold px-5 py-2 rounded-lg text-xs tracking-wider uppercase transition shadow"
            >
              Investigate
            </button>
          </div>

          {/* Quick Presets */}
          <div className="flex items-center justify-center gap-2 text-xs text-slate-400 flex-wrap pt-1">
            <span className="text-slate-500 text-[11px]">Clinical Presets:</span>
            {[
              { label: "Berberine in Type 2 Diabetes", q: "What is the clinical evidence for berberine in metabolic health?" },
              { label: "Warfarin + Herb Bleeding Hazard", q: "Pharmacokinetic bleeding risk of Warfarin combined with St Johns Wort or Garlic" },
              { label: "Curcumin + Piperine Kinetics", q: "Bioavailability enhancement of Curcumin by Piperine via hepatic glucuronidation" }
            ].map(preset => (
              <button
                key={preset.label}
                onClick={() => {
                  setQuery(preset.q);
                  setActiveMode("Evidence");
                }}
                className="text-[11px] text-teal-400 hover:text-teal-300 hover:underline px-2 py-0.5 rounded bg-slate-900/60 border border-slate-800"
              >
                {preset.label}
              </button>
            ))}
          </div>

          {/* Enterprise & Institutional Dual-Deployment Banner */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl mx-auto text-left pt-2 pb-2">
            <div className="bg-slate-900/80 border border-teal-500/30 rounded-xl p-4 flex items-start space-x-3.5 shadow-lg">
              <div className="p-2 rounded-lg bg-teal-500/10 text-teal-400 mt-0.5">
                <Network className="h-5 w-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold uppercase text-white tracking-wider">Cloud Enterprise Tier</span>
                  <span className="text-[10px] bg-teal-500/20 text-teal-300 px-1.5 py-0.5 rounded font-mono">Distributed</span>
                </div>
                <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                  Full-stack Next.js 15 + FastAPI with PostgreSQL (pgvector), Redis queues, and automated live PubMed/PMC harvesters. Designed for Hospitals, Health Systems & Pharma R&D.
                </p>
              </div>
            </div>

            <div className="bg-slate-900/80 border border-amber-500/30 rounded-xl p-4 flex items-start space-x-3.5 shadow-lg">
              <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400 mt-0.5">
                <ShieldCheck className="h-5 w-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold uppercase text-white tracking-wider">Offline Edge Workbench</span>
                  <span className="text-[10px] bg-amber-500/20 text-amber-300 px-1.5 py-0.5 rounded font-mono">Zero-Dependency</span>
                </div>
                <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                  Single-file client engine bundled with 657 botanical codices and local triage algorithms for field doctors, disaster response, and air-gapped clinical deployments.
                </p>
                <a href="/workbench" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 text-[11px] text-amber-400 hover:text-amber-300 font-semibold mt-2">
                  Launch Field Client <ExternalLink className="h-3 w-3" />
                </a>
              </div>
            </div>
          </div>

          {/* Mode Selector */}
          <div className="flex justify-center gap-2 pt-2">
            {(["Search", "Evidence", "Safety", "Compare", "Deep Research"] as const).map((mode) => (
              <button
                key={mode}
                onClick={() => setActiveMode(mode)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition ${
                  activeMode === mode
                    ? "bg-teal-500/15 text-teal-300 border border-teal-500/40"
                    : "text-slate-400 hover:text-slate-200 bg-slate-900/60 border border-slate-800"
                }`}
              >
                {mode}
              </button>
            ))}
          </div>
        </div>

        {/* Evidence Status & Provenance Bar */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-wrap items-center justify-between text-xs gap-3">
          <div className="flex items-center gap-3">
            <span className="text-slate-400">Evidence Status:</span>
            <span className="font-semibold text-emerald-400 flex items-center gap-1">
              <ShieldCheck className="h-4 w-4" /> Evidence is Strong (Multi-Trial Consensus)
            </span>
          </div>
          <div className="flex items-center gap-4 text-slate-400 font-mono text-[11px]">
            <span>SOURCES SEARCHED: 42</span>
            <span>VERIFIED CLAIMS: 18</span>
            <span>TRADITIONS: MODERN, UNANI, AYURVEDA</span>
          </div>
        </div>

        {/* Dynamic Mode Content */}
        {activeMode === "Search" && (
          <div className="space-y-6">
            {/* Executive Synthesis */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-mono uppercase text-teal-400 font-bold flex items-center gap-1.5">
                  <ShieldCheck className="h-4 w-4" /> Governed Evidence Synthesis
                </span>
                <StatusBadge status="Current" />
              </div>

              <p className="text-slate-200 text-sm leading-relaxed mb-4">
                Randomized controlled trials and meta-analyses demonstrate that <strong>Berberine (isoquinoline alkaloid)</strong> significantly reduces fasting blood glucose, postprandial glucose, and HbA1c in adults with Type 2 Diabetes, exhibiting clinical efficacy comparable to low-dose Metformin. Mechanistically, Berberine activates AMP-activated protein kinase (AMPK) through mild mitochondrial respiratory inhibition. In classical Unani medicine, <em>Darhald (Berberis aristata)</em> is prescribed for hot-type metabolic disorders (Ziabetus Shakari Har).
              </p>

              {/* Interactive Claim Trace Buttons */}
              <div className="pt-4 border-t border-slate-800/80 space-y-2">
                <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
                  Atomic Assertions (Click to Trace):
                </span>
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => setSelectedClaim(sampleClaimTrace)}
                    className="inline-flex items-center gap-1.5 bg-slate-950 hover:bg-slate-800 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-800 text-xs transition"
                  >
                    <HelpCircle className="h-3.5 w-3.5 text-teal-400" />
                    <span>HbA1c lowered by -1.8% in adult diabetics</span>
                    <span className="text-[10px] text-teal-400 font-mono">[PMID:18442638]</span>
                  </button>

                  <button
                    onClick={() => setSelectedClaim({
                      ...sampleClaimTrace,
                      claimText: "High-dose berberine causes gastrointestinal distress and is contraindicated in pregnancy.",
                      evidenceLevel: "E1_META_ANALYSIS",
                      sourceId: "PMID:25861268",
                      passage: "High doses may induce gastrointestinal cramping and diarrhea. Berberine is contraindicated during pregnancy due to potential uterine contractions.",
                      verificationStatus: "SUPPORTED"
                    })}
                    className="inline-flex items-center gap-1.5 bg-slate-950 hover:bg-slate-800 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-800 text-xs transition"
                  >
                    <AlertTriangle className="h-3.5 w-3.5 text-amber-400" />
                    <span>Contraindicated in pregnancy & lactation</span>
                    <span className="text-[10px] text-amber-400 font-mono">[Safety Firewall]</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Evidence Table */}
            <div className="space-y-3">
              <h3 className="text-base font-bold text-white">Extracted Evidence Matrix</h3>
              <EvidenceTable items={sampleEvidence} />
            </div>

            {/* Contradictions */}
            <ContradictionSection records={sampleContradictions} />
          </div>
        )}

        {activeMode === "Evidence" && (
          <div className="space-y-6">
            <h2 className="text-lg font-bold text-white">Evidence Matrix & Trial Discrepancies</h2>
            <EvidenceTable items={sampleEvidence} />
            <ContradictionSection records={sampleContradictions} />
          </div>
        )}

        {activeMode === "Deep Research" && (
          <div className="space-y-6">
            <ResearchWorkspace plan={samplePlan} status="COMPLETED" />
            <EvidenceTable items={sampleEvidence} />
          </div>
        )}

        {activeMode === "Compare" && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <h2 className="text-lg font-bold text-white">Cross-System Conceptual Comparison</h2>
            <p className="text-xs text-slate-400">
              Evaluated under ZMIE Equivalence Firewall: Rejects direct 1:1 false equivalence while validating conceptual parallels.
            </p>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-slate-800 bg-slate-950/80 text-slate-400 font-mono uppercase">
                    <th className="p-3">Biomedical Entity</th>
                    <th className="p-3">Unani Tibb Parallel</th>
                    <th className="p-3">Ayurveda Parallel</th>
                    <th className="p-3">Mapping Classification</th>
                    <th className="p-3">Evidence Basis</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-300">
                  <tr>
                    <td className="p-3 font-medium text-white">Metabolic Syndrome / T2D</td>
                    <td className="p-3 font-mono text-teal-300">Ziabetus Shakari (Har)</td>
                    <td className="p-3 font-mono text-cyan-300">Madhumeha (Kaphaja Prameha)</td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800 text-[10px] font-mono">
                        FUNCTIONAL_ANALOGY
                      </span>
                    </td>
                    <td className="p-3 text-slate-400">Symptom clustering & shared glucose dysregulation</td>
                  </tr>
                  <tr>
                    <td className="p-3 font-medium text-white">Berberine Alkaloid</td>
                    <td className="p-3 font-mono text-teal-300">Darhald / Zard Chob</td>
                    <td className="p-3 font-mono text-cyan-300">Daruharidra</td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 text-[10px] font-mono">
                        BOTANICAL_SOURCE_EQUAL
                      </span>
                    </td>
                    <td className="p-3 text-slate-400">Berberis aristata DC botanical identification</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeMode === "Safety" && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-amber-400" /> Pharmacovigilance & Safety Firewall
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <span className="text-rose-400 font-bold block mb-1 font-mono uppercase">Absolute Contraindications</span>
                <p className="text-slate-300 leading-relaxed">
                  Contraindicated during pregnancy and lactation. Berberine displaces bilirubin from albumin, creating high risk for neonate kernicterus.
                </p>
              </div>
              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <span className="text-amber-400 font-bold block mb-1 font-mono uppercase">CYP450 Enzyme Interactions</span>
                <p className="text-slate-300 leading-relaxed">
                  Moderate inhibitor of CYP3A4 and mild inhibitor of CYP2D6. Monitor serum levels when co-administered with Cyclosporine, Tacrolimus, or Warfarin.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Tri-Layer Knowledge Graph Viewer */}
        <KnowledgeGraphViewer
          nodes={[
            { id: "berberine", label: "Berberine (Compound)", type: "compound" },
            { id: "darhald", label: "Darhald (Berberis aristata)", type: "plant", system: "Unani" },
            { id: "ampk", label: "AMPK Pathway (Target)", type: "target" },
            { id: "t2d", label: "Type 2 Diabetes (Condition)", type: "condition" },
            { id: "mizaj", label: "Mizaj Har (Unani)", type: "unani_concept", system: "Unani" }
          ]}
          edges={[
            { source: "Berberine", target: "AMPK", relationship: "activates", evidenceGrade: "E3_MECHANISTIC" },
            { source: "Berberine", target: "Type 2 Diabetes", relationship: "reduces_fbg", evidenceGrade: "E1_META_ANALYSIS" },
            { source: "Darhald", target: "Berberine", relationship: "contains_constituent", evidenceGrade: "E0_GUIDELINE" },
            { source: "Darhald", target: "Mizaj Har", relationship: "modulates_temperament", evidenceGrade: "E5_CANONICAL" }
          ]}
          focusNode="berberine"
        />
      </main>

      {/* Claim Trace Inspector Drawer */}
      <ClaimTraceDrawer data={selectedClaim} onClose={() => setSelectedClaim(null)} />
    </div>
  );
}
