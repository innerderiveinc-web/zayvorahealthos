"use client";

import React from "react";
import { Dna, AlertTriangle, ShieldCheck, Flame, Ban } from "lucide-react";

export interface DDHGAlertItem {
  id: string;
  severity: "CRITICAL_CONTRAINDICATION" | "MAJOR_WARNING" | "MODERATE_MONITOR";
  type: string;
  agents: string[];
  mechanism: string;
  risk: string;
  directive: string;
  fdaWarning?: string;
}

interface DDHGSafetyCardProps {
  status?: string;
  criticalCount?: number;
  majorCount?: number;
  alerts?: DDHGAlertItem[];
}

export const DDHGSafetyCard: React.FC<DDHGSafetyCardProps> = ({
  status = "BLOCKED_CONTRAINDICATION",
  criticalCount = 2,
  majorCount = 1,
  alerts = [
    {
      id: "ALERT-DG-CYP2C19-CLOPIDOGREL",
      severity: "CRITICAL_CONTRAINDICATION",
      type: "DRUG_GENE",
      agents: ["CYP2C19 (*2/*2)", "Clopidogrel"],
      mechanism: "Impaired bioactivation of clopidogrel prodrug into active thiol metabolite.",
      risk: "[Poor Metabolizer] Lack of antiplatelet protection, 3-fold elevated risk of stent thrombosis and ischemic stroke.",
      directive: "AVOID CLOPIDOGREL. Switch to an alternative antiplatelet not dependent on CYP2C19 (e.g. Prasugrel or Ticagrelor).",
      fdaWarning: "FDA Black Box Warning: Diminished Antiplatelet Effect in CYP2C19 Poor Metabolizers."
    },
    {
      id: "ALERT-TRIAD-CLOP-GINKGO-CYP2C19",
      severity: "CRITICAL_CONTRAINDICATION",
      type: "DRUG_HERB_GENE_TRIAD",
      agents: ["Clopidogrel", "Ginkgo biloba", "CYP2C19 PM"],
      mechanism: "Compounded catastrophic hazard: CYP2C19 PM state disables vascular protection, while concurrent Ginkgo introduces unmonitored antiplatelet bleeding risk.",
      risk: "Simultaneous arterial thrombosis hazard AND spontaneous mucosal hemorrhage.",
      directive: "CRITICAL: Discontinue Ginkgo biloba immediately. Switch Clopidogrel to Ticagrelor.",
      fdaWarning: "FDA Black Box Warning on Antiplatelet Failure + Herbal Hemorrhagic Risk."
    },
    {
      id: "ALERT-DH-BERBERINE-CYCLOSPORINE",
      severity: "CRITICAL_CONTRAINDICATION",
      type: "DRUG_HERB",
      agents: ["Berberine", "Cyclosporine"],
      mechanism: "Competitive inhibition of CYP3A4 and intestinal P-glycoprotein efflux.",
      risk: "Surges Cyclosporine AUC by 2.8-fold; acute calcineurin inhibitor nephrotoxicity and graft injury.",
      directive: "Strictly avoid Berberine with Cyclosporine. Mandatory daily C0 trough monitoring if co-administered."
    }
  ]
}) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-xl">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2 text-rose-400 font-mono text-xs uppercase tracking-wider">
            <Dna className="h-4 w-4" /> Deep Drug-Herb-Gene (DDHG) Safety Engine
          </div>
          <h3 className="text-base font-bold text-white mt-1">Pharmacogenomic & Botanical Triad Validator</h3>
          <span className="text-xs text-slate-400 font-mono">CPIC Level 1A &bull; PharmGKB &bull; 657 Catalogued Botanicals</span>
        </div>
        <div className="flex items-center gap-2">
          {criticalCount > 0 ? (
            <span className="text-xs font-mono px-2.5 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 flex items-center gap-1.5 font-bold">
              <Ban className="h-3.5 w-3.5" /> {criticalCount} Critical Contraindications
            </span>
          ) : (
            <span className="text-xs font-mono px-2.5 py-1 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 flex items-center gap-1.5 font-bold">
              <ShieldCheck className="h-3.5 w-3.5" /> All Pathways Clear
            </span>
          )}
        </div>
      </div>

      <div className="space-y-3">
        {alerts.map((alert) => (
          <div key={alert.id} className="p-4 rounded-xl bg-slate-950 border border-rose-900/40 space-y-2 text-xs">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-900 pb-2">
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded text-[10px] font-bold font-mono bg-rose-950 text-rose-300 border border-rose-800">
                  {alert.severity}
                </span>
                <span className="text-slate-400 font-mono text-[10px]">{alert.type}</span>
              </div>
              <div className="flex items-center gap-1 text-[11px] font-mono text-slate-300">
                {alert.agents.map((agent, i) => (
                  <span key={agent} className="px-2 py-0.5 rounded bg-slate-900 text-teal-300 border border-slate-800">
                    {agent}
                  </span>
                ))}
              </div>
            </div>

            <p className="text-slate-300 text-[11px] leading-relaxed">
              <strong className="text-white">Mechanism:</strong> {alert.mechanism}
            </p>
            <p className="text-rose-300 text-[11px] leading-relaxed">
              <strong className="text-rose-400">Clinical Risk:</strong> {alert.risk}
            </p>
            <div className="p-2 rounded bg-slate-900/80 border border-slate-800 text-teal-300 text-[11px] font-mono">
              <strong>Actionable Directive:</strong> {alert.directive}
            </div>

            {alert.fdaWarning && (
              <div className="text-[10px] text-amber-400 flex items-center gap-1 font-mono pt-1">
                <AlertTriangle className="h-3 w-3" /> {alert.fdaWarning}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
