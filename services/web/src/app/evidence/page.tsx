"use client";

import React, { useState } from "react";
import { ShieldCheck, RefreshCw, AlertCircle, ArrowUpRight, Filter, TrendingDown, CheckCircle2 } from "lucide-react";
import { NavigationHeader } from "../../components/NavigationHeader";
import { StatusBadge } from "../../components/StatusBadge";
import { EvidenceTable } from "../../components/EvidenceTable";
import { EvidenceTableItem, GRADEProfileItem } from "../../lib/types";

export default function EvidenceSynthesisPage() {
  const [selectedDomain, setSelectedDomain] = useState<string>("All");

  const gradeProfiles: GRADEProfileItem[] = [
    {
      outcomeName: "HbA1c Reduction (%) at 12 Weeks",
      relativeEffect: "MD: -0.72% [95% CI: -0.91, -0.53]",
      absoluteRisk: "Clinically meaningful glycemic control",
      participants: 1240,
      studiesCount: 14,
      riskOfBias: "LOW",
      inconsistency: "NONE",
      indirectness: "NONE",
      imprecision: "NONE",
      certainty: "HIGH"
    },
    {
      outcomeName: "Fasting Blood Glucose (mmol/L)",
      relativeEffect: "MD: -0.87 mmol/L [95% CI: -1.12, -0.62]",
      absoluteRisk: "Consistent baseline reduction",
      participants: 1088,
      studiesCount: 12,
      riskOfBias: "LOW",
      inconsistency: "NONE",
      indirectness: "NONE",
      imprecision: "NONE",
      certainty: "HIGH"
    },
    {
      outcomeName: "Low-Density Lipoprotein (LDL-C)",
      relativeEffect: "MD: -0.48 mmol/L [95% CI: -0.78, -0.18]",
      absoluteRisk: "Heterogeneity observed across dietary cohorts",
      participants: 860,
      studiesCount: 8,
      riskOfBias: "LOW",
      inconsistency: "SERIOUS",
      indirectness: "NONE",
      imprecision: "NONE",
      certainty: "MODERATE"
    },
    {
      outcomeName: "Gastrointestinal Adverse Events (GI Distress)",
      relativeEffect: "RR: 1.42 [95% CI: 1.05, 1.92]",
      absoluteRisk: "8.6% incidence in 1000mg/day cohorts",
      participants: 1410,
      studiesCount: 16,
      riskOfBias: "LOW",
      inconsistency: "NONE",
      indirectness: "NONE",
      imprecision: "NONE",
      certainty: "HIGH"
    }
  ];

  const evidenceItems: EvidenceTableItem[] = [
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
    }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <NavigationHeader activeTab="evidence" />

      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-8 space-y-8">
        {/* Page Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 text-teal-400 font-mono text-xs uppercase tracking-wider mb-1">
              <ShieldCheck className="h-4 w-4" /> Living Evidence Synthesis & GRADE Profiling
            </div>
            <h1 className="text-2xl font-bold text-white">Evidence Evaluation & Certainty Registry</h1>
            <p className="text-slate-400 text-xs mt-1">
              Continuous synthesis of randomized trials, meta-analyses, and living Cochrane/GRADE certainty frameworks.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono px-3 py-1.5 rounded-lg bg-teal-950/60 border border-teal-800 text-teal-300 flex items-center gap-1.5">
              <RefreshCw className="h-3.5 w-3.5 text-teal-400" /> Continuous Monitor Active
            </span>
          </div>
        </div>

        {/* GRADE Certainty Matrix */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-400" /> GRADE Evidence Profile (Summary of Findings)
            </h2>
            <span className="text-xs font-mono text-slate-400">Standard: GRADE Handbook 2024 / PRISMA 2020</span>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-slate-800 bg-slate-950/90 text-slate-400 font-mono uppercase">
                    <th className="p-3">Outcome</th>
                    <th className="p-3">Pooled Effect (95% CI)</th>
                    <th className="p-3">Studies (N)</th>
                    <th className="p-3">Risk of Bias</th>
                    <th className="p-3">Inconsistency</th>
                    <th className="p-3">Certainty</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-300">
                  {gradeProfiles.map((p, idx) => (
                    <tr key={idx} className="hover:bg-slate-800/40 transition">
                      <td className="p-3 font-semibold text-white">{p.outcomeName}</td>
                      <td className="p-3 font-mono text-teal-300">{p.relativeEffect}</td>
                      <td className="p-3 font-mono">{p.studiesCount} RCTs ({p.participants})</td>
                      <td className="p-3">
                        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-mono">
                          {p.riskOfBias}
                        </span>
                      </td>
                      <td className="p-3">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${
                          p.inconsistency === "NONE" 
                            ? "bg-slate-950 text-slate-400 border border-slate-800" 
                            : "bg-amber-950 text-amber-300 border border-amber-800"
                        }`}>
                          {p.inconsistency}
                        </span>
                      </td>
                      <td className="p-3">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                          p.certainty === "HIGH"
                            ? "bg-emerald-950 text-emerald-300 border border-emerald-700"
                            : "bg-blue-950 text-blue-300 border border-blue-700"
                        }`}>
                          GRADE {p.certainty}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Evidence Matrix */}
        <div className="space-y-4">
          <h2 className="text-base font-bold text-white">Extracted Controlled Trials & Evidence Passages</h2>
          <EvidenceTable items={evidenceItems} />
        </div>
      </main>
    </div>
  );
}
