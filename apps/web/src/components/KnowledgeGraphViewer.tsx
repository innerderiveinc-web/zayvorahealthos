import React from "react";
import { Network, ZoomIn, ZoomOut, Filter, Info } from "lucide-react";

export interface GraphNode {
  id: string;
  label: string;
  type: "condition" | "compound" | "plant" | "target" | "unani_concept" | "study";
  system?: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  relationship: string;
  evidenceGrade: string;
}

export const KnowledgeGraphViewer: React.FC<{
  nodes: GraphNode[];
  edges: GraphEdge[];
  focusNode?: string;
}> = ({ nodes, edges, focusNode }) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl space-y-4">
      {/* Controls */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Network className="h-4 w-4 text-teal-400" />
          <h3 className="font-semibold text-sm text-white">Tri-Layer Knowledge & Evidence Graph</h3>
        </div>
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <span className="font-mono">Nodes: {nodes.length}</span>
          <span>•</span>
          <span className="font-mono">Edges: {edges.length}</span>
        </div>
      </div>

      {/* Visual Canvas Representation */}
      <div className="relative min-h-[320px] bg-slate-950 rounded-lg border border-slate-800/80 p-6 flex flex-col justify-between overflow-hidden">
        {/* Graph Legend */}
        <div className="flex flex-wrap gap-2 text-[10px] font-mono z-10">
          <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">COMPOUND</span>
          <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">PLANT / BOTANICAL</span>
          <span className="px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800">CONDITION</span>
          <span className="px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800">UNANI CONCEPT</span>
          <span className="px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">TARGET / PATHWAY</span>
        </div>

        {/* Nodes Grid Layout */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 my-6">
          {nodes.map((node) => {
            const isFocus = node.id === focusNode;
            return (
              <div
                key={node.id}
                className={`p-3 rounded-lg border transition cursor-pointer ${
                  isFocus
                    ? "bg-teal-950/60 border-teal-500 shadow-lg shadow-teal-500/10"
                    : "bg-slate-900/80 border-slate-800 hover:border-slate-700"
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[10px] font-mono uppercase text-slate-500">{node.type}</span>
                  {node.system && (
                    <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-slate-800 text-teal-400">
                      {node.system}
                    </span>
                  )}
                </div>
                <div className="font-medium text-xs text-slate-200">{node.label}</div>
              </div>
            );
          })}
        </div>

        {/* Relationships list */}
        <div className="border-t border-slate-800/80 pt-3">
          <span className="text-[11px] font-mono text-slate-500 uppercase tracking-wider block mb-2">Grounding Relationship Edges</span>
          <div className="space-y-1.5 text-xs">
            {edges.map((e, idx) => (
              <div key={idx} className="flex items-center justify-between bg-slate-900/60 px-3 py-1.5 rounded border border-slate-800/60">
                <div className="flex items-center gap-2">
                  <span className="text-slate-300 font-medium">{e.source}</span>
                  <span className="text-teal-400 font-mono text-[10px]">--[{e.relationship}]--&gt;</span>
                  <span className="text-slate-300 font-medium">{e.target}</span>
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                  {e.evidenceGrade}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
