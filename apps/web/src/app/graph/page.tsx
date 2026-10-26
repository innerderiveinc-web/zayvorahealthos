"use client";

import React, { useState } from "react";
import { Network, Filter, Layers, ShieldCheck, Info, Share2, ZoomIn } from "lucide-react";
import { NavigationHeader } from "../../components/NavigationHeader";
import { KnowledgeGraphViewer } from "../../components/KnowledgeGraphViewer";

export default function KnowledgeGraphPage() {
  const [activeParadigm, setActiveParadigm] = useState<"ALL" | "MODERN" | "TRADITIONAL">("ALL");

  const nodes = [
    { id: "berberine", label: "Berberine (Compound)", type: "compound" },
    { id: "darhald", label: "Darhald (Berberis aristata)", type: "plant", system: "Unani" },
    { id: "ampk", label: "AMPK Pathway (Target)", type: "target" },
    { id: "t2d", label: "Type 2 Diabetes (Condition)", type: "condition" },
    { id: "mizaj", label: "Mizaj Har (Unani)", type: "unani_concept", system: "Unani" },
    { id: "prakriti", label: "Pitta Prakriti (Ayurveda)", type: "ayurveda_concept", system: "Ayurveda" }
  ];

  const edges = [
    { source: "Berberine", target: "AMPK", relationship: "activates", evidenceGrade: "E3_MECHANISTIC" },
    { source: "Berberine", target: "Type 2 Diabetes", relationship: "reduces_fbg", evidenceGrade: "E1_META_ANALYSIS" },
    { source: "Darhald", target: "Berberine", relationship: "contains_constituent", evidenceGrade: "E0_GUIDELINE" },
    { source: "Darhald", target: "Mizaj Har", relationship: "modulates_temperament", evidenceGrade: "E5_CANONICAL" }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <NavigationHeader activeTab="graph" />

      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-8 space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 text-teal-400 font-mono text-xs uppercase tracking-wider mb-1">
              <Network className="h-4 w-4" /> Multi-Paradigm Knowledge Graph Explorer
            </div>
            <h1 className="text-2xl font-bold text-white">Epistemic Evidence & Semantic Relational Fabric</h1>
            <p className="text-slate-400 text-xs mt-1">
              Tri-layer ontology connecting biomedical targets, clinical trials, and classical Ayurvedic/Unani concepts.
            </p>
          </div>
          <div className="flex items-center gap-2">
            {(["ALL", "MODERN", "TRADITIONAL"] as const).map((p) => (
              <button
                key={p}
                onClick={() => setActiveParadigm(p)}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono transition ${
                  activeParadigm === p
                    ? "bg-teal-500/20 text-teal-300 border border-teal-500/40"
                    : "bg-slate-900 text-slate-400 border border-slate-800 hover:text-white"
                }`}
              >
                {p}
              </button>
            ))}
          </div>
        </div>

        {/* Graph Viewer Component */}
        <KnowledgeGraphViewer
          nodes={nodes}
          edges={edges}
          focusNode="berberine"
        />

        {/* Graph Statistics & Schema Inspector */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <span className="text-xs font-mono uppercase text-teal-400 font-bold block">Biomedical Layer</span>
            <ul className="text-xs space-y-1.5 text-slate-300">
              <li className="flex justify-between"><span>Compounds:</span> <span className="font-mono text-white">412,980</span></li>
              <li className="flex justify-between"><span>Molecular Targets:</span> <span className="font-mono text-white">18,450</span></li>
              <li className="flex justify-between"><span>Disease Phenotypes:</span> <span className="font-mono text-white">9,820</span></li>
            </ul>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <span className="text-xs font-mono uppercase text-amber-400 font-bold block">Traditional Epistemic Layer</span>
            <ul className="text-xs space-y-1.5 text-slate-300">
              <li className="flex justify-between"><span>NAMASTE Morbidities:</span> <span className="font-mono text-white">4,510</span></li>
              <li className="flex justify-between"><span>Unani Mizaj Entities:</span> <span className="font-mono text-white">1,240</span></li>
              <li className="flex justify-between"><span>Ayurvedic Dhatus/Doshas:</span> <span className="font-mono text-white">890</span></li>
            </ul>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <span className="text-xs font-mono uppercase text-cyan-400 font-bold block">Evidence & Claim Layer</span>
            <ul className="text-xs space-y-1.5 text-slate-300">
              <li className="flex justify-between"><span>Atomic Claims:</span> <span className="font-mono text-white">2,840,110</span></li>
              <li className="flex justify-between"><span>Verified Edges:</span> <span className="font-mono text-white">6,120,490</span></li>
              <li className="flex justify-between"><span>Firewall Clean Rate:</span> <span className="font-mono text-emerald-400">99.8%</span></li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}
