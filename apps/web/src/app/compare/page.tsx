"use client";

import React, { useState } from "react";
import { GitCompare, ShieldCheck, AlertTriangle, Layers, Info, CheckCircle2 } from "lucide-react";
import { NavigationHeader } from "../../components/NavigationHeader";

export default function CompareSystemsPage() {
  const [selectedEntity, setSelectedEntity] = useState("Berberine / Darhald / Daruharidra");

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <NavigationHeader activeTab="compare" />

      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-8 space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 text-indigo-400 font-mono text-xs uppercase tracking-wider mb-1">
              <GitCompare className="h-4 w-4" /> Cross-System Comparative Analysis & Equivalence Firewall
            </div>
            <h1 className="text-2xl font-bold text-white">Epistemic Cross-System Parallel Analyzer</h1>
            <p className="text-slate-400 text-xs mt-1">
              Side-by-side analysis across Biomedicine, Unani Tibb, and Ayurveda with automatic false-equivalence rejection.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono px-3 py-1.5 rounded-lg bg-indigo-950/60 border border-indigo-800 text-indigo-300">
              Firewall Strictness: ACTIVE
            </span>
          </div>
        </div>

        {/* Comparative Lens Table */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6 shadow-xl">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white">Tri-Paradigm Concordance Matrix</h2>
            <span className="text-xs font-mono text-teal-400 font-semibold">Entity: {selectedEntity}</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-slate-800 bg-slate-950/90 text-slate-400 font-mono uppercase">
                  <th className="p-3.5">Dimension</th>
                  <th className="p-3.5 text-teal-300">Modern Biomedicine</th>
                  <th className="p-3.5 text-amber-300">Unani Tibb</th>
                  <th className="p-3.5 text-emerald-300">Ayurveda</th>
                  <th className="p-3.5">Firewall Verification</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300">
                <tr>
                  <td className="p-3.5 font-semibold text-white">Entity Identity</td>
                  <td className="p-3.5 font-mono text-teal-300">Berberine (Isoquinoline alkaloid)</td>
                  <td className="p-3.5 font-mono text-amber-300">Darhald / Zard Chob</td>
                  <td className="p-3.5 font-mono text-emerald-300">Daruharidra (Kasturiharidra)</td>
                  <td className="p-3.5">
                    <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-mono text-[10px]">
                      BOTANICAL_SOURCE_EQUAL
                    </span>
                  </td>
                </tr>
                <tr>
                  <td className="p-3.5 font-semibold text-white">Primary Indication</td>
                  <td className="p-3.5">Type 2 Diabetes Mellitus & Dyslipidemia</td>
                  <td className="p-3.5">Ziabetus Shakari (Hot type) & Su-e-Qabid</td>
                  <td className="p-3.5">Madhumeha (Kaphaja/Vataja Prameha)</td>
                  <td className="p-3.5">
                    <span className="px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800 font-mono text-[10px]">
                      FUNCTIONAL_ANALOGY (0.78)
                    </span>
                  </td>
                </tr>
                <tr>
                  <td className="p-3.5 font-semibold text-white">Mechanism / Action</td>
                  <td className="p-3.5">Hepatic AMPK phosphorylation, downregulates PEPCK & G6Pase</td>
                  <td className="p-3.5">Musaffi-e-Dam, Daf-e-Taffun, resolves Khilt-e-Damwi heat</td>
                  <td className="p-3.5">Tikta/Kashaya rasa, Ushna virya, Medohara & Lekhana karma</td>
                  <td className="p-3.5">
                    <span className="px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800 font-mono text-[10px]">
                      DISTINCT_ONTOLOGY_MAPPED
                    </span>
                  </td>
                </tr>
                <tr>
                  <td className="p-3.5 font-semibold text-white">Primary Caution</td>
                  <td className="p-3.5">CYP3A4 inhibition, pregnancy Kernicterus</td>
                  <td className="p-3.5">High dosage induces Su-e-Mizaj Barid (cold weakness)</td>
                  <td className="p-3.5">Vata aggravation in emaciated (Krisha) individuals</td>
                  <td className="p-3.5">
                    <span className="px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800 font-mono text-[10px]">
                      HARMONIZED_SAFETY_ALERT
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Equivalence Firewall Explanation */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-2">
            <span className="font-bold text-emerald-400 uppercase font-mono block">Validated Analogies (PASS)</span>
            <p className="text-slate-300 leading-relaxed">
              Conceptual analogies based on observable physiological phenomena (e.g. chronic hyperglycemia manifesting as polyuria, polydipsia, and tissue wasting) are mapped as functional parallels with explicit epistemic distance scores.
            </p>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-2">
            <span className="font-bold text-rose-400 uppercase font-mono block">Prohibited Identity Claims (BLOCKED)</span>
            <p className="text-slate-300 leading-relaxed">
              Literal identity statements such as <em>"Mizaj is homeostasis"</em> or <em>"Dosha is hormonal balance"</em> are rejected by the ZMIE Equivalence Firewall because they obliterate the distinct conceptual foundations of traditional systems.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
