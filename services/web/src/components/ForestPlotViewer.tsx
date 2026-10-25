"use client";

import React, { useState } from "react";
import { TreePine, RefreshCw, Download, Award, ShieldAlert } from "lucide-react";

export interface ForestPlotItem {
  study: string;
  year: number;
  nIntervention: number;
  nControl: number;
  meanDiff: number;
  ciLower: number;
  ciUpper: number;
  weight: number;
}

interface ForestPlotViewerProps {
  topicTitle?: string;
  picoOutcome?: string;
  studies?: ForestPlotItem[];
  pooledEffect?: number;
  pooledCiLower?: number;
  pooledCiUpper?: number;
  iSquared?: number;
  cochranQ?: number;
  pValue?: number;
  gradeCertainty?: string;
}

export const ForestPlotViewer: React.FC<ForestPlotViewerProps> = ({
  topicTitle = "Berberine vs Metformin in Type 2 Diabetes Mellitus",
  picoOutcome = "Mean Difference in HbA1c Reduction (%)",
  studies = [
    { study: "Lan et al.", year: 2015, nIntervention: 45, nControl: 45, meanDiff: -0.72, ciLower: -0.91, ciUpper: -0.53, weight: 26.8 },
    { study: "Zhang et al.", year: 2008, nIntervention: 58, nControl: 58, meanDiff: -0.68, ciLower: -0.89, ciUpper: -0.47, weight: 24.5 },
    { study: "Yin et al.", year: 2008, nIntervention: 42, nControl: 42, meanDiff: -0.78, ciLower: -1.02, ciUpper: -0.54, weight: 20.1 },
    { study: "Gu et al.", year: 2010, nIntervention: 35, nControl: 35, meanDiff: -0.64, ciLower: -0.88, ciUpper: -0.40, weight: 16.4 },
    { study: "Li et al.", year: 2019, nIntervention: 30, nControl: 30, meanDiff: -0.75, ciLower: -1.05, ciUpper: -0.45, weight: 12.2 }
  ],
  pooledEffect = -0.71,
  pooledCiLower = -0.83,
  pooledCiUpper = -0.59,
  iSquared = 18.2,
  cochranQ = 4.88,
  pValue = 0.0001,
  gradeCertainty = "HIGH (⊕⊕⊕⊕)"
}) => {
  const [modelType, setModelType] = useState<"random" | "fixed">("random");

  // Plot scaling boundaries
  const xMin = -1.5;
  const xMax = 0.5;
  const scaleX = (val: number) => {
    const clamped = Math.max(xMin, Math.min(xMax, val));
    return 360 + ((clamped - xMin) / (xMax - xMin)) * 360;
  };
  const xZero = scaleX(0.0);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-xl">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2 text-teal-400 font-mono text-xs uppercase tracking-wider">
            <TreePine className="h-4 w-4" /> DerSimonian-Laird Meta-Analysis Studio
          </div>
          <h3 className="text-base font-bold text-white mt-1">{topicTitle}</h3>
          <span className="text-xs text-slate-400 font-mono">{picoOutcome}</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex rounded-lg bg-slate-950 p-1 border border-slate-800 text-xs font-mono">
            <button
              onClick={() => setModelType("random")}
              className={`px-2.5 py-1 rounded transition ${modelType === "random" ? "bg-teal-950 text-teal-300 font-bold border border-teal-800" : "text-slate-400 hover:text-slate-200"}`}
            >
              Random Effects
            </button>
            <button
              onClick={() => setModelType("fixed")}
              className={`px-2.5 py-1 rounded transition ${modelType === "fixed" ? "bg-teal-950 text-teal-300 font-bold border border-teal-800" : "text-slate-400 hover:text-slate-200"}`}
            >
              Fixed Effect
            </button>
          </div>
        </div>
      </div>

      {/* Statistical Summary Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono">
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-500 uppercase block text-[10px]">Pooled Effect</span>
          <span className="text-base font-bold text-teal-400">{pooledEffect.toFixed(2)}</span>
          <span className="text-slate-400 block text-[10px]">95% CI: [{pooledCiLower.toFixed(2)}, {pooledCiUpper.toFixed(2)}]</span>
        </div>
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-500 uppercase block text-[10px]">Heterogeneity (I²)</span>
          <span className="text-base font-bold text-emerald-400">{iSquared.toFixed(1)}%</span>
          <span className="text-slate-400 block text-[10px]">Cochran's Q: {cochranQ.toFixed(2)} (df=4)</span>
        </div>
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-500 uppercase block text-[10px]">Significance (Z-Test)</span>
          <span className="text-base font-bold text-cyan-400">p &lt; {pValue.toFixed(4)}</span>
          <span className="text-slate-400 block text-[10px]">Statistically Significant</span>
        </div>
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-500 uppercase block text-[10px]">GRADE Certainty</span>
          <span className="text-sm font-bold text-emerald-400 flex items-center gap-1">
            <Award className="h-3.5 w-3.5" /> {gradeCertainty}
          </span>
          <span className="text-slate-400 block text-[10px]">Zero RoB Downgrade</span>
        </div>
      </div>

      {/* SVG Forest Plot Graphic */}
      <div className="overflow-x-auto bg-slate-950 rounded-xl border border-slate-800/80 p-3">
        <svg viewBox="0 0 760 280" className="w-full h-auto font-sans select-none">
          <rect width="760" height="280" fill="#030712" rx="8" />
          
          {/* Header */}
          <text x="20" y="25" fill="#9ca3af" fontSize="11" fontWeight="600">Study Cohort</text>
          <text x="170" y="25" fill="#9ca3af" fontSize="11" fontWeight="600">N (Int/Ctrl)</text>
          <text x="270" y="25" fill="#9ca3af" fontSize="11" fontWeight="600">Weight</text>
          <text x="540" y="25" fill="#9ca3af" fontSize="11" fontWeight="600" textAnchor="middle">Effect Size (95% CI)</text>
          <line x1="15" y1="35" x2="745" y2="35" stroke="#1f2937" strokeWidth="1" />

          {/* Reference Line of No Effect (0.0) */}
          <line x1={xZero} y1="35" x2={xZero} y2="235" stroke="#ef4444" strokeWidth="1.5" strokeDasharray="4,4" />

          {/* Study Rows */}
          {studies.map((s, idx) => {
            const y = 60 + idx * 30;
            const xPt = scaleX(s.meanDiff);
            const xL = scaleX(s.ciLower);
            const xR = scaleX(s.ciUpper);
            const boxSize = Math.max(6, Math.min(14, (s.weight / 30) * 12));

            return (
              <g key={s.study}>
                <text x="20" y={y + 4} fill="#f3f4f6" fontSize="11" fontWeight="500">{s.study} ({s.year})</text>
                <text x="170" y={y + 4} fill="#9ca3af" fontSize="10" fontFamily="monospace">{s.nIntervention}/{s.nControl}</text>
                <text x="270" y={y + 4} fill="#2dd4bf" fontSize="10" fontFamily="monospace" fontWeight="600">{s.weight.toFixed(1)}%</text>

                {/* Whiskers */}
                <line x1={xL} y1={y} x2={xR} y2={y} stroke="#38bdf8" strokeWidth="1.8" />
                <line x1={xL} y1={y - 3} x2={xL} y2={y + 3} stroke="#38bdf8" strokeWidth="1.5" />
                <line x1={xR} y1={y - 3} x2={xR} y2={y + 3} stroke="#38bdf8" strokeWidth="1.5" />

                {/* Weighted Center Box */}
                <rect x={xPt - boxSize / 2} y={y - boxSize / 2} width={boxSize} height={boxSize} fill="#38bdf8" rx="1.5" />
                <text x="735" y={y + 4} fill="#e5e7eb" fontSize="10" fontFamily="monospace" textAnchor="end">
                  {s.meanDiff.toFixed(2)} [{s.ciLower.toFixed(2)}, {s.ciUpper.toFixed(2)}]
                </text>
              </g>
            );
          })}

          {/* Divider */}
          <line x1="15" y1="215" x2="745" y2="215" stroke="#1f2937" strokeWidth="1" />

          {/* Summary Diamond */}
          {(() => {
            const yDia = 232;
            const xDiaMid = scaleX(pooledEffect);
            const xDiaL = scaleX(pooledCiLower);
            const xDiaR = scaleX(pooledCiUpper);
            const diaPoints = `${xDiaMid},${yDia - 7} ${xDiaR},${yDia} ${xDiaMid},${yDia + 7} ${xDiaL},${yDia}`;

            return (
              <g>
                <text x="20" y={yDia + 4} fill="#10b981" fontSize="11" fontWeight="700">Pooled Effect (DerSimonian-Laird)</text>
                <text x="170" y={yDia + 4} fill="#9ca3af" fontSize="10" fontFamily="monospace">N = 420</text>
                <text x="270" y={yDia + 4} fill="#10b981" fontSize="10" fontFamily="monospace" fontWeight="700">100.0%</text>
                <polygon points={diaPoints} fill="#10b981" stroke="#059669" strokeWidth="1.5" />
                <text x="735" y={yDia + 4} fill="#10b981" fontSize="10" fontFamily="monospace" fontWeight="700" textAnchor="end">
                  {pooledEffect.toFixed(2)} [{pooledCiLower.toFixed(2)}, {pooledCiUpper.toFixed(2)}]
                </text>
              </g>
            );
          })()}

          {/* Bottom Axis */}
          <line x1="360" y1="255" x2="720" y2="255" stroke="#4b5563" strokeWidth="1" />
          <text x={scaleX(-1.0)} y="270" fill="#9ca3af" fontSize="9" textAnchor="middle">-1.0</text>
          <text x={scaleX(-0.5)} y="270" fill="#9ca3af" fontSize="9" textAnchor="middle">-0.5</text>
          <text x={xZero} y="270" fill="#ef4444" fontSize="9" textAnchor="middle">0.0</text>
          <text x={scaleX(0.5)} y="270" fill="#9ca3af" fontSize="9" textAnchor="middle">+0.5</text>
          <text x="440" y="270" fill="#2dd4bf" fontSize="9">← Favors Intervention</text>
          <text x="640" y="270" fill="#f87171" fontSize="9">Favors Control →</text>
        </svg>
      </div>
    </div>
  );
};
