#!/usr/bin/env python3
"""
scripts/apply_topbar_footer_upgrades.py
Implements Institutional Topbar & Footer Upgrades across workbench.html:
1. Topbar:
   - Evidence Currency Pill ("Evidence Current: Oct 2026")
   - Global Quick Search Shortcut ("⌘K")
   - Clinical Dose Calculators Quick Launcher ("🧮 Calculators")
   - Global Keyboard Shortcut Listener (Cmd+K / Ctrl+K)
2. Footer:
   - Global ADR Reporting Portals (FDA MedWatch, WHO VigiBase, MHRA, AYUSH)
   - Emergency Poison Control & Acute Toxicity Notice
   - Editorial Independence & Conflict of Interest (COI) Policy Tab in Legal Modal
3. Clinical Calculators Modal:
   - eGFR (CKD-EPI 2021)
   - Cockcroft-Gault CrCl
   - BMI & BSA with clinical extract dose adjustments
"""

import re

with open("workbench.html", "r", encoding="utf-8") as f:
    content = f.read()

# ─────────────────────────────────────────────────────────────────────────────
# 1. UPGRADE TOPBAR HEADER
# ─────────────────────────────────────────────────────────────────────────────
old_topbar_brand = '''        <div class="flex items-center gap-2">
          <span class="font-extrabold text-base tracking-tight text-white group-hover:text-teal-300 leading-tight transition">ZAYVORA Evidence<span class="text-teal-400 font-mono text-xs">™</span></span>
          <span class="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-teal-950 text-teal-300 border border-teal-800">OS 2.0</span>
        </div>
        <span class="text-xs text-gray-400 font-normal">Tri-Paradigm Medical Intelligence &amp; Pharmacovigilance</span>'''

new_topbar_brand = '''        <div class="flex items-center gap-2">
          <span class="font-extrabold text-base tracking-tight text-white group-hover:text-teal-300 leading-tight transition">ZAYVORA Evidence<span class="text-teal-400 font-mono text-xs">™</span></span>
          <span class="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-teal-950 text-teal-300 border border-teal-800">OS 2.0</span>
          <span class="hidden 2xl:inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-gray-900 border border-gray-800 text-[10px] text-gray-400 font-mono">
            <span class="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Live Enclave • Zero-PHI</span>
          </span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs text-gray-400 font-normal">Tri-Paradigm Medical Intelligence &amp; Pharmacovigilance</span>
          <span class="hidden xl:inline-flex items-center gap-1 text-[10px] text-teal-400 font-mono bg-teal-950/60 px-2 py-0.2 rounded border border-teal-800/80">
            <i class="fa-solid fa-calendar-check text-[9px]"></i> Evidence Current: Oct 2026
          </span>
        </div>'''

if old_topbar_brand in content:
    content = content.replace(old_topbar_brand, new_topbar_brand)
    print("Topbar Brand & Evidence Currency updated.")
else:
    print("Warning: old_topbar_brand not found.")

# Add ⌘K Search Pill and Clinical Calculators button in right header actions
old_nav_library_btn = '''      <!-- Research Library Drawer Trigger -->
      <button id="nav-library-btn" onclick="openResearchLibrary()" class="px-3 py-1.5 bg-gray-900/90 hover:bg-gray-800 text-gray-300 hover:text-white border border-gray-800 hover:border-gray-700 font-medium rounded-lg transition-all flex items-center gap-2 shadow-sm" title="Open Saved Research Library">'''

new_nav_library_btn = '''      <!-- Global ⌘K Quick Search Pill -->
      <button onclick="focusGlobalSearch()" class="hidden lg:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-gray-900/90 hover:bg-gray-800 border border-gray-800 hover:border-teal-700/60 text-gray-400 hover:text-teal-300 text-xs font-mono transition shadow-sm" title="Global Quick Search (Press ⌘K or Ctrl+K)">
        <i class="fa-solid fa-magnifying-glass text-[10px] text-gray-500"></i>
        <span>Search</span>
        <kbd class="px-1.5 py-0.2 rounded bg-gray-950 border border-gray-700 text-[9px] text-gray-300 font-semibold shadow-inner">⌘K</kbd>
      </button>

      <!-- Clinical Dose Calculators Launcher -->
      <button id="btn-topbar-calculators" onclick="openClinicalCalculatorsModal()" class="px-2.5 py-1.5 bg-gray-900/90 hover:bg-gray-800 text-gray-300 hover:text-white border border-gray-800 hover:border-indigo-700/60 font-medium rounded-lg transition-all flex items-center gap-1.5 shadow-sm" title="Clinical Calculators (eGFR CKD-EPI, CrCl, BMI / Body Surface Area)">
        <i class="fa-solid fa-calculator text-indigo-400 text-xs"></i>
        <span class="hidden sm:inline text-xs">Calculators</span>
      </button>

      <!-- Research Library Drawer Trigger -->
      <button id="nav-library-btn" onclick="openResearchLibrary()" class="px-3 py-1.5 bg-gray-900/90 hover:bg-gray-800 text-gray-300 hover:text-white border border-gray-800 hover:border-gray-700 font-medium rounded-lg transition-all flex items-center gap-2 shadow-sm" title="Open Saved Research Library">'''

if old_nav_library_btn in content:
    content = content.replace(old_nav_library_btn, new_nav_library_btn)
    print("Topbar ⌘K and Calculators button added.")
else:
    print("Warning: old_nav_library_btn not found.")

# ─────────────────────────────────────────────────────────────────────────────
# 2. UPGRADE FOOTER: GLOBAL ADR CHANNELS & EMERGENCY POISON NOTICE
# ─────────────────────────────────────────────────────────────────────────────
old_legal_links_row = '''      <!-- Legal & Institutional Policy Links Row -->
      <div class="flex flex-wrap items-center justify-between pt-3 border-t border-gray-800/80 text-[11px] text-gray-400 gap-3">
        <div class="flex items-center gap-4 flex-wrap">
          <button onclick="openLegalModal('disclaimer')" class="hover:text-teal-400 transition flex items-center gap-1.5 font-medium underline">
            <i class="fa-solid fa-notes-medical text-[10px]"></i> Medical Disclaimer
          </button>
          <button onclick="openLegalModal('terms')" class="hover:text-teal-400 transition flex items-center gap-1.5 font-medium underline">
            <i class="fa-solid fa-file-contract text-[10px]"></i> Terms & Conditions
          </button>
          <button onclick="openLegalModal('privacy')" class="hover:text-teal-400 transition flex items-center gap-1.5 font-medium underline">
            <i class="fa-solid fa-user-shield text-[10px]"></i> Privacy Architecture (Zero-PHI / HIPAA Aligned)
          </button>
          <button onclick="openLegalModal('pharmacovigilance')" class="hover:text-teal-400 transition flex items-center gap-1.5 font-medium underline">
            <i class="fa-solid fa-capsules text-[10px]"></i> Pharmacovigilance & Safety
          </button>
        </div>
        <div class="text-[10px] text-gray-500 font-mono">
          Regulatory Ref: <strong>IRB-ZM-2026-REG</strong>
        </div>
      </div>'''

new_legal_links_row = '''      <!-- Global Adverse Drug Reaction (ADR) Reporting Hub & Poison Emergency Notice -->
      <div class="p-4 rounded-xl bg-gray-900/40 border border-gray-800 text-[11px] space-y-2.5">
        <div class="flex items-center justify-between flex-wrap gap-2">
          <span class="font-bold text-gray-200 flex items-center gap-1.5 text-xs">
            <i class="fa-solid fa-tower-broadcast text-rose-400"></i> Global Pharmacovigilance &amp; Adverse Reaction (ADR) Reporting Channels:
          </span>
          <span class="text-[10px] text-gray-500 font-mono">Statutory Health Authority Expedited Reporting</span>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[10px]">
          <a href="https://www.accessdata.fda.gov/scripts/medwatch/" target="_blank" rel="noopener noreferrer" class="p-2 rounded-lg bg-gray-950 border border-gray-800 hover:border-teal-500/50 hover:bg-gray-900 transition flex items-center justify-between text-gray-300">
            <span>🇺🇸 FDA MedWatch 3500</span>
            <i class="fa-solid fa-arrow-up-right-from-square text-[9px] text-gray-500"></i>
          </a>
          <a href="https://who-umc.org/vigibase/" target="_blank" rel="noopener noreferrer" class="p-2 rounded-lg bg-gray-950 border border-gray-800 hover:border-teal-500/50 hover:bg-gray-900 transition flex items-center justify-between text-gray-300">
            <span>🌍 WHO VigiBase / UMC</span>
            <i class="fa-solid fa-arrow-up-right-from-square text-[9px] text-gray-500"></i>
          </a>
          <a href="https://yellowcard.mhra.gov.uk/" target="_blank" rel="noopener noreferrer" class="p-2 rounded-lg bg-gray-950 border border-gray-800 hover:border-teal-500/50 hover:bg-gray-900 transition flex items-center justify-between text-gray-300">
            <span>🇬🇧 MHRA Yellow Card</span>
            <i class="fa-solid fa-arrow-up-right-from-square text-[9px] text-gray-500"></i>
          </a>
          <a href="https://ayush.gov.in/" target="_blank" rel="noopener noreferrer" class="p-2 rounded-lg bg-gray-950 border border-gray-800 hover:border-teal-500/50 hover:bg-gray-900 transition flex items-center justify-between text-gray-300">
            <span>🇮🇳 AYUSH ADR Portal</span>
            <i class="fa-solid fa-arrow-up-right-from-square text-[9px] text-gray-500"></i>
          </a>
        </div>
        <div class="text-[10px] text-amber-300/90 pt-1 flex items-start gap-1.5 leading-relaxed">
          <i class="fa-solid fa-circle-radiation text-amber-400 mt-0.5 shrink-0"></i>
          <span><strong>Emergency Acute Toxicity Protocol:</strong> In cases of severe suspected botanical poisoning or acute accidental overdose, immediately alert your institutional resuscitation team or National Poison Control Center (US: <strong>1-800-222-1222</strong> | UK: <strong>111</strong> | EU: <strong>112</strong> | India: <strong>1800-116-117</strong>).</span>
        </div>
      </div>

      <!-- Legal & Institutional Policy Links Row -->
      <div class="flex flex-wrap items-center justify-between pt-3 border-t border-gray-800/80 text-[11px] text-gray-400 gap-3">
        <div class="flex items-center gap-4 flex-wrap">
          <button onclick="openLegalModal('disclaimer')" class="hover:text-teal-400 transition flex items-center gap-1.5 font-medium underline">
            <i class="fa-solid fa-notes-medical text-[10px]"></i> Medical Disclaimer
          </button>
          <button onclick="openLegalModal('editorial_coi')" class="hover:text-teal-400 transition flex items-center gap-1.5 font-medium underline">
            <i class="fa-solid fa-scale-unbalanced-flip text-[10px]"></i> Editorial &amp; COI Policy
          </button>
          <button onclick="openLegalModal('terms')" class="hover:text-teal-400 transition flex items-center gap-1.5 font-medium underline">
            <i class="fa-solid fa-file-contract text-[10px]"></i> Terms &amp; Conditions
          </button>
          <button onclick="openLegalModal('privacy')" class="hover:text-teal-400 transition flex items-center gap-1.5 font-medium underline">
            <i class="fa-solid fa-user-shield text-[10px]"></i> Privacy Architecture (Zero-PHI / HIPAA Aligned)
          </button>
          <button onclick="openLegalModal('pharmacovigilance')" class="hover:text-teal-400 transition flex items-center gap-1.5 font-medium underline">
            <i class="fa-solid fa-capsules text-[10px]"></i> Pharmacovigilance &amp; Safety
          </button>
        </div>
        <div class="text-[10px] text-gray-500 font-mono">
          Regulatory Ref: <strong>IRB-ZM-2026-REG</strong>
        </div>
      </div>'''

if old_legal_links_row in content:
    content = content.replace(old_legal_links_row, new_legal_links_row)
    print("Footer ADR hub & Poison Emergency notice added.")
else:
    print("Warning: old_legal_links_row not found.")

# ─────────────────────────────────────────────────────────────────────────────
# 3. ADD EDITORIAL & COI POLICY TAB TO LEGAL MODAL
# ─────────────────────────────────────────────────────────────────────────────
old_legal_tabs = '''        <button id="legal-tab-pharmacovigilance" onclick="switchLegalTab('pharmacovigilance')" class="px-3.5 py-2 rounded-t-lg font-semibold border-b-2 border-transparent text-gray-400 hover:text-white">
          Pharmacovigilance Policy
        </button>'''

new_legal_tabs = '''        <button id="legal-tab-editorial_coi" onclick="switchLegalTab('editorial_coi')" class="px-3.5 py-2 rounded-t-lg font-semibold border-b-2 border-transparent text-gray-400 hover:text-white">
          Editorial &amp; COI Policy
        </button>
        <button id="legal-tab-pharmacovigilance" onclick="switchLegalTab('pharmacovigilance')" class="px-3.5 py-2 rounded-t-lg font-semibold border-b-2 border-transparent text-gray-400 hover:text-white">
          Pharmacovigilance Policy
        </button>'''

if old_legal_tabs in content:
    content = content.replace(old_legal_tabs, new_legal_tabs)
    print("Legal Modal: Editorial & COI tab added.")
else:
    print("Warning: old_legal_tabs not found.")

# Add editorial_coi content section in legal modal
old_legal_body_end = '''        <!-- Pharmacovigilance Content -->
        <div id="legal-content-pharmacovigilance" class="hidden space-y-3">'''

new_legal_body_coi = '''        <!-- Editorial & Conflict of Interest (COI) Policy Content -->
        <div id="legal-content-editorial_coi" class="hidden space-y-3">
          <h4 class="text-xs font-bold uppercase tracking-wider text-teal-400">Editorial Independence, Evidence Grading &amp; COI Declaration</h4>
          <p>
            ZAYVORA Health Sciences and the ZMIE Evidence Engine operate under strict scientific non-commercial independence. We maintain zero financial sponsorship, advertising relationships, or formulary partnerships with pharmaceutical or nutraceutical manufacturing corporations.
          </p>
          <div class="p-3 bg-gray-950 border border-gray-800 rounded-xl space-y-2 text-[11px]">
            <div class="font-bold text-white flex items-center gap-1.5">
              <i class="fa-solid fa-certificate text-emerald-400"></i> Evidence Synthesis Methodology Standards:
            </div>
            <ul class="list-disc list-inside space-y-1 text-gray-300">
              <li><strong>Cochrane RoB-2 Calibration:</strong> Randomized trials are algorithmically evaluated across 5 bias domains.</li>
              <li><strong>GRADE Working Group Concordance:</strong> Recommendations reflect certainty of evidence (High, Moderate, Low, Very Low).</li>
              <li><strong>ICMJE COI Disclosure:</strong> All contributing clinician investigators are required to declare direct and indirect financial interests.</li>
              <li><strong>Classical Corpus Authentication:</strong> Unani and Ayurveda codices are referenced strictly from statutory regulatory pharmacopoeias (UPI, API) and classical manuscripts.</li>
            </ul>
          </div>
          <p class="text-[10px] text-gray-500">
            For editorial review inquiries or clinical corrections, contact the Clinical Synthesis Board at editorial@zayvora.internal.
          </p>
        </div>

        <!-- Pharmacovigilance Content -->
        <div id="legal-content-pharmacovigilance" class="hidden space-y-3">'''

if old_legal_body_end in content:
    content = content.replace(old_legal_body_end, new_legal_body_coi)
    print("Legal Modal: Editorial & COI body content added.")
else:
    print("Warning: old_legal_body_end not found.")

# ─────────────────────────────────────────────────────────────────────────────
# 4. ADD CLINICAL CALCULATORS MODAL
# ─────────────────────────────────────────────────────────────────────────────
calculators_modal_html = '''
  <!-- Clinical Dose Calculators Modal (eGFR, CrCl, BMI) -->
  <div id="clinical-calculators-modal" onclick="if(event.target === this) closeClinicalCalculatorsModal()" class="fixed inset-0 drawer-backdrop hidden z-50 flex items-center justify-center p-4">
    <div class="bg-gray-900 border border-gray-800 rounded-2xl max-w-xl w-full max-h-[90vh] flex flex-col shadow-2xl overflow-hidden glass-card">
      <div class="p-5 border-b border-gray-800 flex items-center justify-between bg-gray-950/80">
        <div class="flex items-center gap-2.5">
          <i class="fa-solid fa-calculator text-indigo-400 text-lg"></i>
          <div>
            <h3 class="text-sm font-bold text-white">Clinical Dose &amp; Renal Impairment Calculators</h3>
            <span class="text-[10px] text-gray-400">CKD-EPI 2021 eGFR • Cockcroft-Gault CrCl • BMI</span>
          </div>
        </div>
        <button onclick="closeClinicalCalculatorsModal()" class="text-gray-400 hover:text-white text-lg font-bold px-2 py-1">✕</button>
      </div>

      <div class="p-5 overflow-y-auto space-y-4 text-xs">
        <!-- Calculator Selector Tabs -->
        <div class="flex bg-gray-950 p-1 rounded-xl border border-gray-800 gap-1">
          <button id="calc-tab-egfr" onclick="switchCalcTab('egfr')" class="flex-1 py-1.5 rounded-lg font-semibold text-xs bg-indigo-950 text-indigo-300 border border-indigo-800 transition">
            eGFR (CKD-EPI)
          </button>
          <button id="calc-tab-crcl" onclick="switchCalcTab('crcl')" class="flex-1 py-1.5 rounded-lg font-semibold text-xs text-gray-400 hover:text-white transition">
            CrCl (Cockcroft)
          </button>
          <button id="calc-tab-bmi" onclick="switchCalcTab('bmi')" class="flex-1 py-1.5 rounded-lg font-semibold text-xs text-gray-400 hover:text-white transition">
            BMI / BSA
          </button>
        </div>

        <!-- eGFR Calculator -->
        <div id="calc-content-egfr" class="space-y-3">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-gray-400 text-[11px] mb-1">Serum Creatinine (mg/dL)</label>
              <input type="number" id="calc-scr" value="1.0" step="0.1" class="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-1.5 text-white font-mono text-xs focus:border-indigo-500">
            </div>
            <div>
              <label class="block text-gray-400 text-[11px] mb-1">Patient Age (Years)</label>
              <input type="number" id="calc-age" value="54" class="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-1.5 text-white font-mono text-xs focus:border-indigo-500">
            </div>
          </div>
          <div>
            <label class="block text-gray-400 text-[11px] mb-1">Biological Sex</label>
            <select id="calc-sex" class="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-1.5 text-white text-xs focus:border-indigo-500">
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>
          <button onclick="calculateEgfr()" class="w-full py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs transition shadow-md">
            Compute eGFR &amp; Botanical Clearance Staging
          </button>
          <div id="calc-egfr-result" class="p-3.5 rounded-xl bg-gray-950 border border-gray-800 space-y-1 font-mono text-xs">
            <div class="flex justify-between items-center text-gray-400">
              <span>eGFR (CKD-EPI 2021):</span>
              <strong id="calc-egfr-val" class="text-base text-emerald-400 font-bold">88.5 mL/min/1.73m²</strong>
            </div>
            <div id="calc-egfr-stage" class="text-[11px] text-gray-300">Stage G1: Normal / High kidney clearance. Full botanical extract titration indicated.</div>
          </div>
        </div>

        <!-- CrCl Calculator -->
        <div id="calc-content-crcl" class="hidden space-y-3">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-gray-400 text-[11px] mb-1">Serum Creatinine (mg/dL)</label>
              <input type="number" id="calc-crcl-scr" value="1.1" step="0.1" class="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-1.5 text-white font-mono text-xs focus:border-indigo-500">
            </div>
            <div>
              <label class="block text-gray-400 text-[11px] mb-1">Patient Weight (kg)</label>
              <input type="number" id="calc-crcl-wt" value="70" class="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-1.5 text-white font-mono text-xs focus:border-indigo-500">
            </div>
          </div>
          <button onclick="calculateCrcl()" class="w-full py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs transition shadow-md">
            Compute Cockcroft-Gault CrCl
          </button>
          <div id="calc-crcl-result" class="p-3.5 rounded-xl bg-gray-950 border border-gray-800 space-y-1 font-mono text-xs">
            <div class="flex justify-between items-center text-gray-400">
              <span>Estimated CrCl:</span>
              <strong id="calc-crcl-val" class="text-base text-teal-400 font-bold">78.0 mL/min</strong>
            </div>
            <div id="calc-crcl-note" class="text-[11px] text-gray-300">Renal clearance adequate for standard therapeutic dosing.</div>
          </div>
        </div>

        <!-- BMI Calculator -->
        <div id="calc-content-bmi" class="hidden space-y-3">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-gray-400 text-[11px] mb-1">Height (cm)</label>
              <input type="number" id="calc-bmi-ht" value="175" class="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-1.5 text-white font-mono text-xs focus:border-indigo-500">
            </div>
            <div>
              <label class="block text-gray-400 text-[11px] mb-1">Weight (kg)</label>
              <input type="number" id="calc-bmi-wt" value="75" class="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-1.5 text-white font-mono text-xs focus:border-indigo-500">
            </div>
          </div>
          <button onclick="calculateBmi()" class="w-full py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs transition shadow-md">
            Compute BMI &amp; Body Surface Area
          </button>
          <div id="calc-bmi-result" class="p-3.5 rounded-xl bg-gray-950 border border-gray-800 space-y-1 font-mono text-xs">
            <div class="flex justify-between items-center text-gray-400">
              <span>Body Mass Index:</span>
              <strong id="calc-bmi-val" class="text-base text-indigo-400 font-bold">24.5 kg/m²</strong>
            </div>
            <div id="calc-bmi-class" class="text-[11px] text-gray-300">Normal Range • Standard mg/kg dosing baseline</div>
          </div>
        </div>
      </div>
    </div>
  </div>
'''

content = content.replace('</body>', calculators_modal_html + '\n</body>')
print("Clinical Calculators Modal added.")

# ─────────────────────────────────────────────────────────────────────────────
# 5. JAVASCRIPT HANDLERS FOR NEW FEATURES
# ─────────────────────────────────────────────────────────────────────────────
new_js_logic = '''
    // =========================================================================
    // INSTITUTIONAL TOPBAR & FOOTER ENHANCEMENTS: ⌘K, CALCULATORS, EDITORIAL COI
    // =========================================================================

    // Global Search Focus Shortcut (⌘K / Ctrl+K)
    function focusGlobalSearch() {
      handleEvidenceTabClick();
      const inp = document.getElementById('search-input');
      if (inp) {
        inp.focus();
        inp.select();
        safeScrollTo({ top: 0, behavior: 'smooth' });
      }
      showToast("Clinical Evidence Search active (⌘K)", "fa-magnifying-glass", "text-teal-400");
    }

    // Keyboard listener for ⌘K / Ctrl+K
    window.addEventListener('keydown', function(e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        focusGlobalSearch();
      }
    });

    // Clinical Calculators Modal Controller
    function openClinicalCalculatorsModal() {
      const modal = document.getElementById('clinical-calculators-modal');
      if (modal) modal.classList.remove('hidden');
    }

    function closeClinicalCalculatorsModal() {
      const modal = document.getElementById('clinical-calculators-modal');
      if (modal) modal.classList.add('hidden');
    }

    function switchCalcTab(tab) {
      const tabs = ['egfr', 'crcl', 'bmi'];
      tabs.forEach(t => {
        const btn = document.getElementById(`calc-tab-${t}`);
        const cnt = document.getElementById(`calc-content-${t}`);
        if (t === tab) {
          if (btn) btn.className = 'flex-1 py-1.5 rounded-lg font-semibold text-xs bg-indigo-950 text-indigo-300 border border-indigo-800 transition';
          if (cnt) cnt.classList.remove('hidden');
        } else {
          if (btn) btn.className = 'flex-1 py-1.5 rounded-lg font-semibold text-xs text-gray-400 hover:text-white transition';
          if (cnt) cnt.classList.add('hidden');
        }
      });
    }

    function calculateEgfr() {
      const scr = parseFloat(document.getElementById('calc-scr')?.value || 1.0);
      const age = parseFloat(document.getElementById('calc-age')?.value || 50);
      const sex = document.getElementById('calc-sex')?.value || 'male';

      // CKD-EPI 2021 race-free equation
      const k = sex === 'female' ? 0.7 : 0.9;
      const alpha = sex === 'female' ? -0.241 : -0.302;
      const sexMult = sex === 'female' ? 1.012 : 1.0;

      const minVal = Math.min(scr / k, 1);
      const maxVal = Math.max(scr / k, 1);

      const egfr = Math.round(142 * Math.pow(minVal, alpha) * Math.pow(maxVal, -1.200) * Math.pow(0.9938, age) * sexMult);

      const valEl = document.getElementById('calc-egfr-val');
      const stgEl = document.getElementById('calc-egfr-stage');

      if (valEl) valEl.innerText = `${egfr} mL/min/1.73m²`;
      if (stgEl) {
        if (egfr >= 90) {
          valEl.className = 'text-base text-emerald-400 font-bold';
          stgEl.innerText = 'Stage G1: Normal renal clearance. Standard botanical dosage appropriate.';
        } else if (egfr >= 60) {
          valEl.className = 'text-base text-emerald-300 font-bold';
          stgEl.innerText = 'Stage G2: Mild reduction. Monitor hydration and maintain standard titration.';
        } else if (egfr >= 45) {
          valEl.className = 'text-base text-amber-400 font-bold';
          stgEl.innerText = 'Stage G3a: Mild-to-moderate. Reduce high-oxalate & nephro-active botanicals by 25%.';
        } else if (egfr >= 30) {
          valEl.className = 'text-base text-amber-500 font-bold';
          stgEl.innerText = 'Stage G3b: Moderate-to-severe. Reduce dose by 50%; mandatory baseline renal panel.';
        } else {
          valEl.className = 'text-base text-rose-400 font-bold';
          stgEl.innerText = 'Stage G4/G5: Severe impairment / Failure. Botanicals contraindicated due to metabolite accumulation.';
        }
      }
    }

    function calculateCrcl() {
      const scr = parseFloat(document.getElementById('calc-crcl-scr')?.value || 1.0);
      const wt = parseFloat(document.getElementById('calc-crcl-wt')?.value || 70);
      const age = parseFloat(document.getElementById('calc-age')?.value || 50);
      const sex = document.getElementById('calc-sex')?.value || 'male';

      let crcl = Math.round(((140 - age) * wt) / (72 * scr));
      if (sex === 'female') crcl = Math.round(crcl * 0.85);

      const valEl = document.getElementById('calc-crcl-val');
      const noteEl = document.getElementById('calc-crcl-note');

      if (valEl) valEl.innerText = `${crcl} mL/min`;
      if (noteEl) {
        if (crcl >= 60) {
          noteEl.innerText = 'Cockcroft-Gault clearance normal. Standard clinical protocol titration.';
        } else if (crcl >= 30) {
          noteEl.innerText = 'Moderate clearance impairment. Adjust dosage of renal-eliminated alkaloids.';
        } else {
          noteEl.innerText = 'Severe clearance reduction. Botanical therapy contraindicated without nephrologist clearance.';
        }
      }
    }

    function calculateBmi() {
      const ht = parseFloat(document.getElementById('calc-bmi-ht')?.value || 170) / 100;
      const wt = parseFloat(document.getElementById('calc-bmi-wt')?.value || 70);

      const bmi = (wt / (ht * ht)).toFixed(1);
      const bsa = Math.sqrt((ht * 100 * wt) / 3600).toFixed(2);

      const valEl = document.getElementById('calc-bmi-val');
      const clsEl = document.getElementById('calc-bmi-class');

      if (valEl) valEl.innerText = `${bmi} kg/m² (BSA: ${bsa} m²)`;
      if (clsEl) {
        if (bmi < 18.5) clsEl.innerText = 'Underweight range • Consider lower initial loading doses';
        else if (bmi < 25) clsEl.innerText = 'Normal weight range • Standard mg/kg dosing baseline';
        else if (bmi < 30) clsEl.innerText = 'Overweight range • Consider lipophilic bioavailability adjustments';
        else clsEl.innerText = 'Obesity class range • Increased volume of distribution for lipophilic bioactives';
      }
    }
'''

# Insert JS before </script>
last_script = content.rfind('</script>')
if last_script != -1:
    content = content[:last_script] + new_js_logic + "\n" + content[last_script:]
    print("New JavaScript logic added.")

# Hook editorial_coi in switchLegalTab
old_switch_legal = '''      const tabs = ['disclaimer', 'terms', 'privacy', 'pharmacovigilance'];'''
new_switch_legal = '''      const tabs = ['disclaimer', 'editorial_coi', 'terms', 'privacy', 'pharmacovigilance'];'''

if old_switch_legal in content:
    content = content.replace(old_switch_legal, new_switch_legal)
    print("switchLegalTab updated to support editorial_coi.")

with open("workbench.html", "w", encoding="utf-8") as f:
    f.write(content)

print("workbench.html updated successfully with Topbar & Footer upgrades.")
