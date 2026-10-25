"use client";

import React, { useState } from "react";
import { Compass, BookOpen, Layers, CheckSquare, Search, FileText, ArrowRight, ShieldCheck, TreePine, GitBranch, Dna } from "lucide-react";
import { NavigationHeader } from "../../components/NavigationHeader";
import { ResearchWorkspace } from "../../components/ResearchWorkspace";
import { EvidenceTable } from "../../components/EvidenceTable";
import { ForestPlotViewer } from "../../components/ForestPlotViewer";
import { PRISMAFlowViewer } from "../../components/PRISMAFlowViewer";
import { DDHGSafetyCard } from "../../components/DDHGSafetyCard";
import { ResearchPlanData, EvidenceTableItem } from "../../lib/types";

export default function DeepResearchStudioPage() {
  const [activeStudioTab, setActiveStudioTab] = useState<"workspace" | "forest" | "prisma" | "ddhg">("workspace");

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
      studyTitle: "Meta-analysis of the effect and safety of berberine in type 2 diabetes",
      year: "2015",
      studyDesign: "Systematic Review & Meta-Analysis (27 RCTs, n=2,569)",
      population: "Adult T2D cohorts",
      sampleSize: 2569,
      intervention: "Berberine (various doses)",
      comparator: "Lifestyle / Metformin",
      outcome: "HbA1c & Fasting Lipids",
      findings: "Pooled HbA1c reduction of -0.72% (95% CI -0.91 to -0.53, p < 0.001) with improved lipid profiles.",
      safety: "No severe hepatic or renal adverse events reported.",
      evidenceGrade: "E6_CONTROLLED_CLINICAL",
      source: "PMID:25498346"
    }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <NavigationHeader activeTab="research" />

      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-8 space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 text-teal-400 font-mono text-xs uppercase tracking-wider mb-1">
              <Compass className="h-4 w-4" /> Autonomous Deep Research Studio (v3.0)
            </div>
            <h1 className="text-2xl font-bold text-white">Systematic Evidence & Meta-Synthesis Suite</h1>
            <p className="text-slate-400 text-xs mt-1">
              3-Tier Hybrid Retrieval (MeSH BM25 + Dense Vector + Causal Graph) &bull; DerSimonian-Laird Pooling &bull; DDHG Pharmacogenomics
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono px-3 py-1.5 rounded-lg bg-teal-950/60 border border-teal-800 text-teal-300">
              PRISMA 2020 Compliant
            </span>
          </div>
        </div>

        {/* Studio Sub-Navigation Tabs */}
        <div className="flex items-center gap-2 p-1 bg-slate-900 border border-slate-800 rounded-xl overflow-x-auto text-xs font-mono">
          <button
            onClick={() => setActiveStudioTab("workspace")}
            className={`px-3 py-1.5 rounded-lg transition flex items-center gap-1.5 ${
              activeStudioTab === "workspace"
                ? "bg-teal-950 text-teal-300 border border-teal-800 font-bold"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <BookOpen className="h-3.5 w-3.5" /> PICO Protocol & Screening
          </button>
          <button
            onClick={() => setActiveStudioTab("forest")}
            className={`px-3 py-1.5 rounded-lg transition flex items-center gap-1.5 ${
              activeStudioTab === "forest"
                ? "bg-teal-950 text-teal-300 border border-teal-800 font-bold"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <TreePine className="h-3.5 w-3.5" /> Forest Plot & Meta-Analysis
          </button>
          <button
            onClick={() => setActiveStudioTab("prisma")}
            className={`px-3 py-1.5 rounded-lg transition flex items-center gap-1.5 ${
              activeStudioTab === "prisma"
                ? "bg-teal-950 text-teal-300 border border-teal-800 font-bold"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <GitBranch className="h-3.5 w-3.5" /> PRISMA 2020 Flow Funnel
          </button>
          <button
            onClick={() => setActiveStudioTab("ddhg")}
            className={`px-3 py-1.5 rounded-lg transition flex items-center gap-1.5 ${
              activeStudioTab === "ddhg"
                ? "bg-rose-950 text-rose-300 border border-rose-800 font-bold"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Dna className="h-3.5 w-3.5" /> Drug-Herb-Gene (DDHG) Safety
          </button>
        </div>

        {/* Tab 1: PICO Workspace & Evidence Matrix */}
        {activeStudioTab === "workspace" && (
          <div className="space-y-6">
            <ResearchWorkspace plan={samplePlan} status="COMPLETED" />

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Layers className="h-4 w-4 text-teal-400" /> Multi-Source Identification Funnel
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono">
                <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                  <span className="text-slate-500 uppercase block mb-1">Records Harvested</span>
                  <span className="text-xl font-bold text-white">1,482</span>
                </div>
                <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                  <span className="text-slate-500 uppercase block mb-1">Deduplicated</span>
                  <span className="text-xl font-bold text-teal-400">924</span>
                </div>
                <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                  <span className="text-slate-500 uppercase block mb-1">Screened Relevant</span>
                  <span className="text-xl font-bold text-cyan-400">42</span>
                </div>
                <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                  <span className="text-slate-500 uppercase block mb-1">Included in Synthesis</span>
                  <span className="text-xl font-bold text-emerald-400">18 RCTs</span>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h2 className="text-base font-bold text-white">Included Studies & Extraction Record</h2>
              <EvidenceTable items={sampleEvidence} />
            </div>
          </div>
        )}

        {/* Tab 2: Forest Plot Studio */}
        {activeStudioTab === "forest" && (
          <ForestPlotViewer />
        )}

        {/* Tab 3: PRISMA 2020 Flow Funnel */}
        {activeStudioTab === "prisma" && (
          <PRISMAFlowViewer />
        )}

        {/* Tab 4: Drug-Herb-Gene (DDHG) Safety Engine */}
        {activeStudioTab === "ddhg" && (
          <DDHGSafetyCard />
        )}
      </main>
    </div>
  );
}
