"use client";

import React, { useState } from "react";
import { Compass, BookOpen, Layers, CheckSquare, Search, FileText, ArrowRight, ShieldCheck } from "lucide-react";
import { NavigationHeader } from "../../components/NavigationHeader";
import { ResearchWorkspace } from "../../components/ResearchWorkspace";
import { EvidenceTable } from "../../components/EvidenceTable";
import { ResearchPlanData, EvidenceTableItem } from "../../lib/types";

export default function DeepResearchStudioPage() {
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
    }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <NavigationHeader activeTab="research" />

      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-8 space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 text-teal-400 font-mono text-xs uppercase tracking-wider mb-1">
              <Compass className="h-4 w-4" /> Autonomous Deep Research Studio
            </div>
            <h1 className="text-2xl font-bold text-white">Systematic Investigation & PICO Protocol</h1>
            <p className="text-slate-400 text-xs mt-1">
              Deterministic search strategy generation, automated trial screening, and citation-grounded synthesis.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono px-3 py-1.5 rounded-lg bg-teal-950/60 border border-teal-800 text-teal-300">
              PRISMA 2020 Protocol
            </span>
          </div>
        </div>

        {/* Research Plan & Workspace */}
        <ResearchWorkspace plan={samplePlan} status="COMPLETED" />

        {/* Screening Summary */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Layers className="h-4 w-4 text-teal-400" /> Screening & Study Eligibility Funnel
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono">
            <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
              <span className="text-slate-500 uppercase block mb-1">Records Identified</span>
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
              <span className="text-xl font-bold text-emerald-400">18</span>
            </div>
          </div>
        </div>

        {/* Included Evidence Matrix */}
        <div className="space-y-4">
          <h2 className="text-base font-bold text-white">Included Studies & Extraction Record</h2>
          <EvidenceTable items={sampleEvidence} />
        </div>
      </main>
    </div>
  );
}
