"use client";

import React, { useState } from "react";
import { BookOpen, ShieldAlert, Sparkles, CheckCircle, HelpCircle, Layers, Globe } from "lucide-react";
import { NavigationHeader } from "../../components/NavigationHeader";

export default function TraditionalMedicinePage() {
  const [selectedSystem, setSelectedSystem] = useState<"UNANI" | "AYURVEDA">("UNANI");

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <NavigationHeader activeTab="medicine" />

      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-8 space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 text-amber-400 font-mono text-xs uppercase tracking-wider mb-1">
              <BookOpen className="h-4 w-4" /> Traditional Medicine & Epistemic Distance Preservation
            </div>
            <h1 className="text-2xl font-bold text-white">Traditional Systems, Pharmacopoeias & NAMASTE Codices</h1>
            <p className="text-slate-400 text-xs mt-1">
              Canonical preservation of Unani Tibb and Ayurveda without reductive 1:1 biomedical distortion.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setSelectedSystem("UNANI")}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition ${
                selectedSystem === "UNANI"
                  ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                  : "bg-slate-900 text-slate-400 border border-slate-800 hover:text-white"
              }`}
            >
              UNANI TIBB
            </button>
            <button
              onClick={() => setSelectedSystem("AYURVEDA")}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition ${
                selectedSystem === "AYURVEDA"
                  ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                  : "bg-slate-900 text-slate-400 border border-slate-800 hover:text-white"
              }`}
            >
              AYURVEDA
            </button>
          </div>
        </div>

        {/* Epistemic Distance Invariant Banner */}
        <div className="bg-amber-950/20 border border-amber-800/40 rounded-xl p-5 text-xs text-amber-200/90 leading-relaxed flex items-start gap-3">
          <ShieldAlert className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-bold text-amber-300 block mb-1 uppercase tracking-wider font-mono">
              Invariant INV-04: Epistemic Distance Preservation Active
            </span>
            <span>
              Traditional diagnostic concepts (e.g. Mizaj Har, Balghami plethora, Kaphaja Prameha) are maintained with explicit epistemic distance scores (0.76–0.81) rather than false 1:1 equivalences. Cross-system identity claims are mathematically intercepted and rewritten as conceptual analogies.
            </span>
          </div>
        </div>

        {/* System Specific Details */}
        {selectedSystem === "UNANI" ? (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
                <span className="text-xs font-mono uppercase text-amber-400 font-bold block">
                  Core Theory: Arkan, Mizaj & Akhlat
                </span>
                <p className="text-xs text-slate-300 leading-relaxed">
                  In Unani Tibb, health represents the equilibrium of the four humors (Akhlat-e-Arba'a): Dam (Blood), Balgham (Phlegm), Safra (Yellow Bile), and Sauda (Black Bile). Diseases arise from Su-e-Mizaj (temperamental dyscrasia) or abnormal humor buildup.
                </p>
                <div className="space-y-2 pt-2 border-t border-slate-800">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-400">Damawi (Sanguine):</span>
                    <span className="font-mono text-white">Hot & Moist</span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-400">Balghami (Phlegmatic):</span>
                    <span className="font-mono text-white">Cold & Moist</span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-400">Safrawi (Choleric):</span>
                    <span className="font-mono text-white">Hot & Dry</span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-400">Saudawi (Melancholic):</span>
                    <span className="font-mono text-white">Cold & Dry</span>
                  </div>
                </div>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
                <span className="text-xs font-mono uppercase text-teal-400 font-bold block">
                  Compendial Drug: Darhald (Berberis aristata)
                </span>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Darhald (Indian Barberry / Zarishk root) is categorized as Hot 2° / Dry 2°. Its primary therapeutic actions (Afaal) include Musaffi-e-Dam (blood purifier) and Daf-e-Taffun (anti-putrefactive).
                </p>
                <div className="space-y-2 pt-2 border-t border-slate-800 text-xs">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Indication in Compendia:</span>
                    <span className="font-mono text-white">Ziabetus Shakari (Diabetes)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Epistemic Analogy Basis:</span>
                    <span className="font-mono text-teal-300">Glycemic stabilization (Score 0.76)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Classical Formulation:</span>
                    <span className="font-mono text-white">Qurs-e-Ziabetus / Rasaut</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
                <span className="text-xs font-mono uppercase text-emerald-400 font-bold block">
                  Core Theory: Tridosha & Sapta Dhatu
                </span>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Ayurvedic physiology is governed by Vata, Pitta, and Kapha across seven structural tissues (Dhatus: Rasa, Rakta, Mamsa, Meda, Asthi, Majja, Shukra). Pathology (Vikriti) stems from Agni impairment (Ama formation) and dosha aggravation.
                </p>
                <div className="space-y-2 pt-2 border-t border-slate-800">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-400">Vata Dosha:</span>
                    <span className="font-mono text-white">Movement, dry, cold, light</span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-400">Pitta Dosha:</span>
                    <span className="font-mono text-white">Transformation, hot, sharp, liquid</span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-400">Kapha Dosha:</span>
                    <span className="font-mono text-white">Structure, cold, heavy, stable</span>
                  </div>
                </div>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
                <span className="text-xs font-mono uppercase text-cyan-400 font-bold block">
                  Herb: Daruharidra (Berberis aristata)
                </span>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Daruharidra possesses Tikta (bitter) and Kashaya (astringent) tastes with Ushna (heating) virya. It is renowned for Pramehahara (anti-diabetic) and Lekhana (scraping adipose tissue) karma.
                </p>
                <div className="space-y-2 pt-2 border-t border-slate-800 text-xs">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Ayurvedic Morbidity:</span>
                    <span className="font-mono text-white">Madhumeha (Kaphaja Prameha)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Epistemic Analogy Basis:</span>
                    <span className="font-mono text-cyan-300">Insulin resistance & Medo-dhatu scraping (0.81)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Classical Samhita:</span>
                    <span className="font-mono text-white">Charaka Samhita Chikitsa 6</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
