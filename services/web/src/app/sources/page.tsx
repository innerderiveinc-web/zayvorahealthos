"use client";

import React, { useState } from "react";
import { Database, ShieldCheck, CheckCircle2, AlertTriangle, ExternalLink, RefreshCw, Radio } from "lucide-react";
import { NavigationHeader } from "../../components/NavigationHeader";

export default function SourceUniversePage() {
  const [selectedTier, setSelectedTier] = useState<string>("ALL");

  const sources = [
    {
      sourceId: "SRC-PUBMED-001",
      name: "PubMed / MEDLINE Core Scholarly Literature",
      tier: "TIER_A",
      license: "CLASS_A",
      type: "Biomedical Literature",
      status: "OPERATIONAL",
      documents: "36.2M",
      lastSync: "12m ago"
    },
    {
      sourceId: "SRC-CLINICALTRIALS-002",
      name: "ClinicalTrials.gov Protocol & Results Registry",
      tier: "TIER_A",
      license: "CLASS_A",
      type: "Clinical Trial Registry",
      status: "OPERATIONAL",
      documents: "492K",
      lastSync: "25m ago"
    },
    {
      sourceId: "SRC-COCHRANE-003",
      name: "Cochrane Database of Systematic Reviews",
      tier: "TIER_A",
      license: "CLASS_B",
      type: "Systematic Review Library",
      status: "OPERATIONAL",
      documents: "14.8K",
      lastSync: "1h ago"
    },
    {
      sourceId: "SRC-AYUSH-TKDL-004",
      name: "Traditional Knowledge Digital Library (TKDL) & NAMASTE",
      tier: "TIER_A",
      license: "CLASS_C",
      type: "Canonical Traditional Corpus",
      status: "OPERATIONAL",
      documents: "285K",
      lastSync: "45m ago"
    },
    {
      sourceId: "SRC-OPENALEX-005",
      name: "OpenAlex Global Scientific Citation Graph",
      tier: "TIER_D",
      license: "CLASS_A",
      type: "Bibliometric Graph",
      status: "OPERATIONAL",
      documents: "250M",
      lastSync: "5m ago"
    },
    {
      sourceId: "SRC-RETRACTIONWATCH-006",
      name: "Retraction Watch Database (Crossref)",
      tier: "TIER_A",
      license: "CLASS_A",
      type: "Integrity & Retraction Radar",
      status: "OPERATIONAL",
      documents: "52K",
      lastSync: "2m ago"
    }
  ];

  const filteredSources = selectedTier === "ALL" 
    ? sources 
    : sources.filter(s => s.tier === selectedTier);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <NavigationHeader activeTab="sources" />

      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-8 space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 text-teal-400 font-mono text-xs uppercase tracking-wider mb-1">
              <Database className="h-4 w-4" /> Global Medical Source Universe (Tiers A–G)
            </div>
            <h1 className="text-2xl font-bold text-white">Governed Medical Source Registry & Licensing Gate</h1>
            <p className="text-slate-400 text-xs mt-1">
              Cryptographic provenance, legal licensing classes (Class A–E), and real-time retraction interception.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono px-3 py-1.5 rounded-lg bg-teal-950/60 border border-teal-800 text-teal-300 flex items-center gap-1.5">
              <Radio className="h-3.5 w-3.5 text-emerald-400 animate-pulse" /> Fleet Status: HEALTHY
            </span>
          </div>
        </div>

        {/* Source Table */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
          <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/50">
            <span className="text-xs font-mono uppercase text-slate-400 font-bold">Registered Ingestion Feeds</span>
            <div className="flex gap-1.5">
              {(["ALL", "TIER_A", "TIER_D"] as const).map(t => (
                <button
                  key={t}
                  onClick={() => setSelectedTier(t)}
                  className={`px-2.5 py-1 rounded text-[11px] font-mono transition ${
                    selectedTier === t
                      ? "bg-teal-500/20 text-teal-300 border border-teal-500/40"
                      : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-slate-800 bg-slate-950/80 text-slate-400 font-mono uppercase">
                  <th className="p-3.5">Source Identifier</th>
                  <th className="p-3.5">Authority Tier</th>
                  <th className="p-3.5">License Class</th>
                  <th className="p-3.5">Documents Indexed</th>
                  <th className="p-3.5">Sync Freshness</th>
                  <th className="p-3.5">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300">
                {filteredSources.map((s, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40 transition">
                    <td className="p-3.5">
                      <div className="font-semibold text-white">{s.name}</div>
                      <div className="font-mono text-[10px] text-teal-400">{s.sourceId} • {s.type}</div>
                    </td>
                    <td className="p-3.5">
                      <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-mono text-[10px]">
                        {s.tier}
                      </span>
                    </td>
                    <td className="p-3.5">
                      <span className="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-slate-800 font-mono text-[10px]">
                        {s.license}
                      </span>
                    </td>
                    <td className="p-3.5 font-mono text-white">{s.documents}</td>
                    <td className="p-3.5 font-mono text-slate-400">{s.lastSync}</td>
                    <td className="p-3.5">
                      <span className="inline-flex items-center gap-1 text-emerald-400 font-mono text-[11px]">
                        <CheckCircle2 className="h-3 w-3" /> {s.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
