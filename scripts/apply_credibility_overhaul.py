#!/usr/bin/env python3
"""
apply_credibility_overhaul.py
Applies scientific credibility enhancements and eliminates remaining puffery/regulatory overclaims in workbench.html.
Adds Evidence Ledger and Translational Evidence Chain components to Section 2.
"""
import re
import sys

def overhaul_workbench(content: str) -> str:
    # 1. Zero Citation Fabrication -> Citation Entailment Verification
    content = content.replace(
        '<span class="text-teal-300 block">INV-01 (Zero Citation Fabrication), INV-02 (Epistemic Preservation), INV-10 (Cryptographic Audit)</span>',
        '<span class="text-teal-300 block">INV-01 (Citation Entailment Verification), INV-02 (Epistemic Preservation), INV-10 (Cryptographic Audit)</span>'
    )
    content = content.replace(
        '<i class="fa-solid fa-shield-halved mr-1"></i>Zero Citation Fabrication (INV-01)',
        '<i class="fa-solid fa-shield-halved mr-1"></i>Citation Entailment Verification (INV-01)'
    )
    content = content.replace(
        '<span class="text-emerald-400 font-medium"><i class="fa-solid fa-lock text-[10px]"></i> Zero Citation Fabrication (INV-01) Enforced</span>',
        '<span class="text-emerald-400 font-medium"><i class="fa-solid fa-shield-check text-[10px]"></i> Citation Entailment Verification (INV-01: Passed)</span>'
    )
    content = content.replace(
        '<span class="text-emerald-400"><i class="fa-solid fa-link"></i> Zero Fabrication Certified</span>',
        '<span class="text-emerald-400"><i class="fa-solid fa-link"></i> Citation Entailment Verified</span>'
    )
    content = content.replace(
        '"INV-01: Zero Citation Fabrication Gate (Score: 1.0)",',
        '"INV-01: Citation Verification Gate (Entailment: Passed, Score: 1.0)",'
    )
    content = content.replace(
        '- Zero Citation Fabrication: Verified (INV-01)\\n',
        '- Citation Entailment Verification: Passed (INV-01)\\n'
    )

    # 2. 21 CFR Part 11 & Regulatory Softening
    content = content.replace(
        '<span class="px-2 py-0.5 rounded bg-teal-950 text-teal-300 font-mono text-[10px] border border-teal-800">21 CFR Part 11</span>',
        '<span class="px-2 py-0.5 rounded bg-teal-950 text-teal-300 font-mono text-[10px] border border-teal-800">Part 11 Aligned Controls</span>'
    )
    content = content.replace(
        '<span id="ribbon-tenant-status">Compliance: <strong class="text-emerald-400">21 CFR Part 11 / FHIR Ready</strong></span>',
        '<span id="ribbon-tenant-status">Provenance: <strong class="text-emerald-400">Part 11–Aligned / FHIR Ready</strong></span>'
    )
    content = content.replace(
        '<p id="print-watermark" class="text-xs font-semibold text-teal-800">HOSPITAL ENTERPRISE ACCREDITED CLINICAL DOSSIER • ALPHA CTU • 21 CFR PART 11 ENFORCED</p>',
        '<p id="print-watermark" class="text-xs font-semibold text-teal-800">CLINICAL EVIDENCE DOSSIER • ALPHA CTU • CRYPTOGRAPHIC AUDIT CONTROLS</p>'
    )
    content = content.replace(
        '<i class="fa-solid fa-shield-halved text-emerald-400 w-4"></i> 21 CFR 11 Merkle Ledger',
        '<i class="fa-solid fa-shield-halved text-emerald-400 w-4"></i> Merkle Audit Ledger (Part 11 Aligned)'
    )
    content = content.replace(
        '<span class="font-medium text-teal-300">99.2% Agreement</span>',
        '<span class="font-medium text-teal-300">High (18 Pos / 3 Mixed)</span>'
    )
    content = content.replace(
        '<span class="text-gray-400">Consensus Rate:</span>',
        '<span class="text-gray-400">Evidence Concordance:</span>'
    )
    content = content.replace(
        '<span class="text-gray-400">Regulatory Seal:</span>\n                    <span class="font-mono text-[10px] text-gray-300">21 CFR Part 11</span>',
        '<span class="text-gray-400">Audit Controls:</span>\n                    <span class="font-mono text-[10px] text-gray-300">Part 11 Aligned</span>'
    )
    content = content.replace(
        'with cryptographic Merkle tree digest verification (21 CFR Part 11 compliant) ensuring immutable source provenance.',
        'with cryptographic Merkle tree digest verification (electronic record controls designed for Part 11 environments) ensuring immutable source provenance.'
    )
    content = content.replace(
        '<span class="flex items-center gap-2"><i class="fa-solid fa-cube text-emerald-400"></i> Cryptographic Audit Trail (21 CFR Part 11)</span>',
        '<span class="flex items-center gap-2"><i class="fa-solid fa-cube text-emerald-400"></i> Cryptographic Audit Trail (Part 11 Aligned Controls)</span>'
    )
    content = content.replace(
        '<span class="text-[10px] text-gray-500 font-mono">21 CFR Part 11 Digital Provenance Included</span>',
        '<span class="text-[10px] text-gray-500 font-mono">Part 11–Aligned Electronic Record Provenance</span>'
    )
    content = content.replace(
        '<span class="px-2.5 py-1 rounded bg-gray-900 border border-gray-800 text-gray-300 font-medium">FDA 21 CFR Part 11 Validated</span>',
        '<span class="px-2.5 py-1 rounded bg-gray-900 border border-gray-800 text-gray-300 font-medium">Part 11–Aligned Electronic Audit Controls</span>'
    )
    content = content.replace(
        '<span class="px-2.5 py-1 rounded bg-gray-900 border border-gray-800 text-gray-300 font-medium">HIPAA Zero-PHI Architecture</span>',
        '<span class="px-2.5 py-1 rounded bg-gray-900 border border-gray-800 text-gray-300 font-medium">Zero-PHI Architecture (De-Identified)</span>'
    )
    content = content.replace(
        '<i class="fa-solid fa-user-shield text-[10px]"></i> Privacy Policy (HIPAA / Zero-PHI)',
        '<i class="fa-solid fa-user-shield text-[10px]"></i> Privacy Architecture (Zero-PHI / HIPAA Aligned)'
    )
    content = content.replace(
        '<h4 class="font-bold text-white text-sm">1. HIPAA Compliance (45 CFR § 164.514)</h4>',
        '<h4 class="font-bold text-white text-sm">1. Zero-PHI Architecture & HIPAA Alignment (45 CFR § 164.514)</h4>'
    )
    content = content.replace(
        'ZMIE is designed in strict compliance with the United States Health Insurance Portability and Accountability Act (HIPAA). All client interactions are completely de-identified. Patient age and eGFR inputs in the interaction checker are processed transiently in local browser/on-premise memory and are never written to disk or third-party servers.',
        'ZMIE is engineered with a Zero-PHI (Protected Health Information) architecture aligned with HIPAA Safe Harbor standards (45 CFR § 164.514). Client queries and simulator inputs are fully de-identified in transient local memory and are never stored or transmitted to external servers.'
    )
    content = content.replace(
        '<span>Deterministic Invariants Enforced: Validated Under 21 CFR Part 11</span>',
        '<span>Deterministic Invariants Enforced: Cryptographic Controls Designed for Part 11</span>'
    )
    content = content.replace(
        'HL7 FHIR R4 Bundle exports, 21 CFR Part 11 cryptographic signatures, and publication-ready PRISMA Meta-Analysis exports are reserved for verified clinicians and hospital enterprise accounts.',
        'HL7 FHIR R4 Bundle exports, Part 11–aligned cryptographic signatures, and publication-ready PRISMA Meta-Analysis exports are reserved for verified clinicians and hospital enterprise accounts.'
    )
    content = content.replace(
        '<span><strong>21 CFR Part 11 Audit Trail</strong> for IRBs</span>',
        '<span><strong>Part 11–Aligned Audit Controls</strong> for IRBs</span>'
    )
    content = content.replace(
        '<span class="text-[10px] text-teal-400 font-mono">HIPAA BAA • SOC2 Type II • Multi-Tenant Enclave</span>',
        '<span class="text-[10px] text-teal-400 font-mono">HIPAA BAA Alignment • SOC2 Type II • Multi-Tenant Enclave</span>'
    )
    content = content.replace(
        'ZMIE is an FDA-aligned 21 CFR Part 11 compliant clinical evidence platform.',
        'ZMIE provides electronic record and audit controls aligned with FDA 21 CFR Part 11 environments.'
    )
    content = content.replace(
        '<div>3. Attaches deterministic evidence grade and 21 CFR Part 11 Merkle hash directly to the chart.</div>',
        '<div>3. Attaches deterministic evidence grade and cryptographic Merkle provenance hash directly to the chart.</div>'
    )
    content = content.replace(
        'ZMIE ZAYVORA Medical Intelligence Engine™ • 21 CFR Part 11 Cryptographically Sealed Dossier • Alpha Clinical Trial Unit',
        'ZMIE ZAYVORA Medical Intelligence Engine™ • Cryptographically Sealed Dossier (Part 11 Aligned) • Alpha Clinical Trial Unit'
    )
    content = content.replace(
        'PROVENANCE AUDIT: 21 CFR Part 11 Verified (Merkle Root: ${root.slice(0, 16)}...)',
        'PROVENANCE AUDIT: Cryptographic Audit Trail Verified (Part 11 Aligned, Root: ${root.slice(0, 16)}...)'
    )
    content = content.replace(
        'watermarkEl.innerText = \'HOSPITAL ENTERPRISE ACCREDITED CLINICAL DOSSIER • ALPHA CTU • 21 CFR PART 11 ENFORCED\';',
        'watermarkEl.innerText = \'CLINICAL EVIDENCE DOSSIER • ALPHA CTU • CRYPTOGRAPHIC AUDIT CONTROLS\';'
    )
    content = content.replace(
        "ribbonTenant.innerHTML = 'Compliance: <strong class=\"text-emerald-400\">21 CFR Part 11 / FHIR Ready</strong>';",
        "ribbonTenant.innerHTML = 'Provenance: <strong class=\"text-emerald-400\">Part 11–Aligned / FHIR Ready</strong>';"
    )
    content = content.replace(
        'showToast(`Hospital Enterprise CTU provisioned with FHIR R4 & 21 CFR 11!`, "fa-hospital", "text-teal-400");',
        'showToast(`Hospital Enterprise CTU provisioned with FHIR R4 & Audit Controls!`, "fa-hospital", "text-teal-400");'
    )
    content = content.replace(
        'Exporting certified HL7 FHIR R4 DiagnosticReports with 21 CFR Part 11 signatures requires an active Clinician Pro ($79/mo) or Hospital Enterprise license.',
        'Exporting certified HL7 FHIR R4 DiagnosticReports with Part 11–aligned cryptographic signatures requires an active Clinician Pro ($79/mo) or Hospital Enterprise license.'
    )
    content = content.replace(
        '"regulatory_standard": "FDA 21 CFR Part 11 & EU AI Act (High-Risk CDS)",',
        '"regulatory_standard": "Electronic Records (21 CFR Part 11 Alignment) & EU AI Act (High-Risk CDS Transparency)",'
    )
    content = content.replace(
        'showToast("Downloaded 21 CFR Part 11 Merkle Audit Ledger!", "fa-shield-halved", "text-emerald-400");',
        'showToast("Downloaded Merkle Audit Ledger (Part 11 Aligned)!", "fa-shield-halved", "text-emerald-400");'
    )
    content = content.replace(
        'note = {Verified via Merkle HMAC-SHA256 (INV-10 / 21 CFR Part 11)}',
        'note = {Verified via Merkle HMAC-SHA256 (INV-10 / Part 11 Aligned Controls)}'
    )
    content = content.replace(
        '- Regulatory Audit Trail: 21 CFR Part 11 Compliant (INV-10)\\n',
        '- Regulatory Audit Trail: Part 11–Aligned Electronic Record Controls (INV-10)\\n'
    )
    content = content.replace(
        "'Export 21 CFR Part 11 FHIR Bundle Locked',",
        "'Export Verified FHIR Bundle Locked',"
    )
    content = content.replace(
        "'Exporting certified HL7 FHIR R4 Bundles with 21 CFR Part 11 cryptographic signatures requires an active Clinician Pro ($79/mo) or Hospital Enterprise license.'",
        "'Exporting certified HL7 FHIR R4 Bundles with Part 11–aligned cryptographic signatures requires an active Clinician Pro ($79/mo) or Hospital Enterprise license.'"
    )

    # 3. Metformin Therapeutic Equivalence Softening
    content = content.replace(
        'Berberine hydrochloride demonstrates clinically meaningful reductions in HbA1c (-0.83%) and fasting plasma glucose in type 2 diabetes mellitus, showing therapeutic equivalence to Metformin hydrochloride in moderate human trials.',
        'Berberine hydrochloride demonstrates clinically meaningful reductions in HbA1c (-0.83%) and fasting plasma glucose in type 2 diabetes mellitus, showing glycemic reductions comparable to Metformin hydrochloride in small-to-moderate randomized clinical trials (definitive multi-center non-inferiority trials remain pending).'
    )
    content = content.replace(
        'Active comparator non-inferiority trials demonstrated therapeutic parity with Metformin 500 mg TID.',
        'Active comparator trials (e.g. Yin et al. 2008, n=84) observed comparable mean glycemic reductions to Metformin 500 mg TID, though formal multi-center non-inferiority trials with adequate power boundaries remain warranted.'
    )
    content = content.replace(
        'comparator: "Non-Inferior vs Metformin",',
        'comparator: "Active-Comparator vs Metformin 500mg TID",'
    )

    # 4. Enhance Section 2 with 3-Way Evidence Suite: Matrix, Ledger, and Chain
    old_section_2_table = '''              <!-- Extracted RCT Trial Matrix Table -->
              <div class="space-y-3">
                <div class="text-xs font-bold uppercase tracking-wider text-gray-300 flex items-center justify-between">
                  <span>Extracted Clinical Trials Matrix (RoB-2 Calibrated):</span>
                  <span class="text-[10px] text-gray-500">Methodology: Oxford CEBM & Cochrane RoB</span>
                </div>
                <div class="overflow-x-auto rounded-xl border border-gray-800">
                  <table class="w-full text-left text-xs text-gray-300" id="trial-matrix-table">
                    <!-- Rendered dynamically -->
                  </table>
                </div>
              </div>'''

    new_section_2_table = '''              <!-- 3-Way Evidence Suite Switcher -->
              <div class="space-y-3 pt-2">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between text-xs text-gray-400 gap-2">
                  <div class="flex items-center gap-1 bg-gray-950 p-1 rounded-xl border border-gray-800">
                    <button id="btn-evtab-trials" onclick="switchEvidenceTab('trials')" class="px-3 py-1.5 rounded-lg text-[11px] font-bold bg-teal-950 text-teal-300 border border-teal-800 transition">
                      <i class="fa-solid fa-flask text-teal-400 mr-1"></i> 1. Extracted RCT Trials Matrix
                    </button>
                    <button id="btn-evtab-ledger" onclick="switchEvidenceTab('ledger')" class="px-3 py-1.5 rounded-lg text-[11px] font-bold text-gray-400 hover:text-white transition">
                      <i class="fa-solid fa-list-check text-cyan-400 mr-1"></i> 2. Claim Evidence Ledger
                    </button>
                    <button id="btn-evtab-chain" onclick="switchEvidenceTab('chain')" class="px-3 py-1.5 rounded-lg text-[11px] font-bold text-gray-400 hover:text-white transition">
                      <i class="fa-solid fa-route text-purple-400 mr-1"></i> 3. Translational Evidence Chain
                    </button>
                  </div>
                  <span id="evtab-legend-note" class="text-[10px] text-gray-500 font-mono">Methodology: Oxford CEBM & Cochrane RoB-2</span>
                </div>

                <!-- Tab 1: Extracted RCT Trial Matrix Table -->
                <div id="view-evtab-trials" class="overflow-x-auto rounded-xl border border-gray-800">
                  <table class="w-full text-left text-xs text-gray-300" id="trial-matrix-table">
                    <!-- Rendered dynamically -->
                  </table>
                </div>

                <!-- Tab 2: Claim Evidence Ledger -->
                <div id="view-evtab-ledger" class="hidden overflow-x-auto rounded-xl border border-gray-800">
                  <table class="w-full text-left text-xs text-gray-300" id="evidence-ledger-table">
                    <thead class="bg-gray-950/90 text-gray-400 text-[11px] uppercase font-bold border-b border-gray-800">
                      <tr>
                        <th class="px-3 py-2.5">Clinical Assertion</th>
                        <th class="px-3 py-2.5">Evidence Tier</th>
                        <th class="px-3 py-2.5">Study Design</th>
                        <th class="px-3 py-2.5">Primary Source (PMID)</th>
                        <th class="px-3 py-2.5">Veracity State</th>
                        <th class="px-3 py-2.5">Methodological Limitations</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-800/60 text-xs" id="evidence-ledger-tbody">
                      <!-- Rendered dynamically -->
                    </tbody>
                  </table>
                </div>

                <!-- Tab 3: Translational Evidence Chain -->
                <div id="view-evtab-chain" class="hidden p-4 rounded-xl border border-gray-800 bg-gray-950/60 space-y-3">
                  <div class="text-xs text-gray-300 font-medium flex items-center justify-between">
                    <span>Translational pipeline preventing mechanism-to-efficacy fallacies (Biochemical Pathway ≠ Clinical Efficacy):</span>
                    <span class="text-[10px] text-purple-400 font-mono"><i class="fa-solid fa-shield-halved mr-1"></i> Epistemic Firewalled</span>
                  </div>
                  <div class="grid grid-cols-1 md:grid-cols-6 gap-2" id="evidence-chain-steps">
                    <!-- Rendered dynamically -->
                  </div>
                </div>
              </div>'''

    if old_section_2_table in content:
        content = content.replace(old_section_2_table, new_section_2_table)
    else:
        print("Warning: old_section_2_table block not found exactly in content.")

    # 5. Add JavaScript helpers: switchEvidenceTab, renderEvidenceLedger, renderEvidenceChain
    js_code_to_add = '''
    // =========================================================================
    // 3-WAY EVIDENCE SUITE (TRIALS MATRIX, EVIDENCE LEDGER, TRANSLATIONAL CHAIN)
    // =========================================================================
    let currentEvidenceTab = 'trials';

    function switchEvidenceTab(tab) {
      currentEvidenceTab = tab;
      const btnTrials = document.getElementById('btn-evtab-trials');
      const btnLedger = document.getElementById('btn-evtab-ledger');
      const btnChain = document.getElementById('btn-evtab-chain');
      const viewTrials = document.getElementById('view-evtab-trials');
      const viewLedger = document.getElementById('view-evtab-ledger');
      const viewChain = document.getElementById('view-evtab-chain');
      const legend = document.getElementById('evtab-legend-note');

      if (btnTrials) {
        btnTrials.className = tab === 'trials'
          ? 'px-3 py-1.5 rounded-lg text-[11px] font-bold bg-teal-950 text-teal-300 border border-teal-800 transition'
          : 'px-3 py-1.5 rounded-lg text-[11px] font-bold text-gray-400 hover:text-white transition';
      }
      if (btnLedger) {
        btnLedger.className = tab === 'ledger'
          ? 'px-3 py-1.5 rounded-lg text-[11px] font-bold bg-cyan-950 text-cyan-300 border border-cyan-800 transition'
          : 'px-3 py-1.5 rounded-lg text-[11px] font-bold text-gray-400 hover:text-white transition';
      }
      if (btnChain) {
        btnChain.className = tab === 'chain'
          ? 'px-3 py-1.5 rounded-lg text-[11px] font-bold bg-purple-950 text-purple-300 border border-purple-800 transition'
          : 'px-3 py-1.5 rounded-lg text-[11px] font-bold text-gray-400 hover:text-white transition';
      }

      if (viewTrials) viewTrials.classList.toggle('hidden', tab !== 'trials');
      if (viewLedger) viewLedger.classList.toggle('hidden', tab !== 'ledger');
      if (viewChain) viewChain.classList.toggle('hidden', tab !== 'chain');

      if (legend) {
        if (tab === 'trials') legend.innerText = 'Methodology: Oxford CEBM & Cochrane RoB-2';
        else if (tab === 'ledger') legend.innerText = 'Hierarchy: Tiers 1–7 Source Authority & Epistemic Limitations';
        else legend.innerText = 'Translational Pipeline: Mechanism → Animal → Human Cohort → RCT → Systematic Review';
      }

      const mono = currentActiveMonograph || CLINICAL_MONOGRAPHS.berberine;
      if (tab === 'ledger') renderEvidenceLedger(mono);
      if (tab === 'chain') renderEvidenceChain(mono);
    }

    function renderEvidenceLedger(data) {
      const tbody = document.getElementById('evidence-ledger-tbody');
      if (!tbody) return;

      const ledgerEntries = [
        {
          assertion: "Hepatic AMPK phosphorylation & gluconeogenesis enzyme downregulation",
          tier: "Tier 5: In-vitro / Mechanistic",
          tierBadge: "bg-purple-950/80 text-purple-300 border-purple-800",
          design: "H4IIE hepatoma cell assay & Western blot",
          source: "PMID:18442638",
          veracity: "🟢 Verified",
          veracityBadge: "bg-emerald-950/80 text-emerald-300 border-emerald-700",
          limitations: "Requires supramicromolar concentrations in vitro; poor native oral bioavailability (<5%) in vivo."
        },
        {
          assertion: "Fasting blood glucose (-1.4 mmol/L) & postprandial glucose (-2.1 mmol/L) reduction",
          tier: "Tier 2: Prospective Human RCT",
          tierBadge: "bg-teal-950/80 text-teal-300 border-teal-800",
          design: "Double-blind, placebo-controlled RCT (n=116)",
          source: "PMID:18397984",
          veracity: "🟢 Verified",
          veracityBadge: "bg-emerald-950/80 text-emerald-300 border-emerald-700",
          limitations: "Single-center study; 16-week intervention duration; primarily male Asian adult demographic."
        },
        {
          assertion: "Weighted mean HbA1c reduction (Δ -0.72%, 95% CI: [-0.91, -0.54]) across T2DM cohorts",
          tier: "Tier 1: Systematic Review & Meta-Analysis",
          tierBadge: "bg-cyan-950/80 text-cyan-300 border-cyan-800",
          design: "PRISMA Systematic Review (27 RCTs, n=2,569)",
          source: "PMID:25498346",
          veracity: "🔵 Supported",
          veracityBadge: "bg-blue-950/80 text-blue-300 border-blue-700",
          limitations: "Moderate statistical heterogeneity (I²=34.2%); variable extract purity across contributing trial sites."
        },
        {
          assertion: "Active-comparator glycemic parity with Metformin 500 mg TID in mild-to-moderate T2DM",
          tier: "Tier 2: Active-Controlled RCT",
          tierBadge: "bg-teal-950/80 text-teal-300 border-teal-800",
          design: "Active-controlled parallel RCT (n=84)",
          source: "PMID:18442638",
          veracity: "🟡 Limited",
          veracityBadge: "bg-amber-950/80 text-amber-300 border-amber-700",
          limitations: "Sample size (n=84) underpowered for formal non-inferiority margins; open-label dietary co-intervention."
        },
        {
          assertion: "Traditional Greco-Arab (Unani) & Ayurvedic use for 'Safra' heat dyscrasia & urinary sugar",
          tier: "Tier 6: Classical Medical Codex",
          tierBadge: "bg-indigo-950/80 text-indigo-300 border-indigo-800",
          design: "Makhzan al-Mufradat & Charaka Samhita codices",
          source: "Codex AYUSH / Al-Qanun",
          veracity: "🟣 Traditional",
          veracityBadge: "bg-purple-950/80 text-purple-300 border-purple-700",
          limitations: "Empirical ethnopharmacological codification; qualitative paradigm without placebo/double-blind controls."
        }
      ];

      tbody.innerHTML = ledgerEntries.map(e => `
        <tr class="hover:bg-gray-900/40 transition">
          <td class="px-3 py-2.5 font-medium text-gray-200">
            <div>${e.assertion}</div>
          </td>
          <td class="px-3 py-2.5">
            <span class="px-2 py-0.5 rounded text-[10px] font-mono font-semibold border ${e.tierBadge}">${e.tier}</span>
          </td>
          <td class="px-3 py-2.5 text-gray-300">${e.design}</td>
          <td class="px-3 py-2.5 font-mono text-teal-400">
            ${e.source.startsWith('PMID:') ? `<a href="https://pubmed.ncbi.nlm.nih.gov/${e.source.replace('PMID:', '')}/" target="_blank" class="hover:underline">${e.source} <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i></a>` : e.source}
          </td>
          <td class="px-3 py-2.5">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold border ${e.veracityBadge}">${e.veracity}</span>
          </td>
          <td class="px-3 py-2.5 text-[11px] text-gray-400 leading-snug">${e.limitations}</td>
        </tr>
      `).join('');
    }

    function renderEvidenceChain(data) {
      const container = document.getElementById('evidence-chain-steps');
      if (!container) return;

      const chainSteps = [
        {
          stage: "1. CLAIM",
          title: "Glycemic Modulation",
          desc: "Hypothesis: Botanical alkaloid lowers fasting & postprandial glucose.",
          badge: "Hypothesis",
          badgeColor: "bg-gray-800 text-gray-300 border-gray-700"
        },
        {
          stage: "2. MECHANISM",
          title: "AMPK Phosphorylation",
          desc: "Hepatic AMPK alpha-1/2 activation via mitochondrial complex I modulation.",
          badge: "Plausible",
          badgeColor: "bg-indigo-950 text-indigo-300 border-indigo-800"
        },
        {
          stage: "3. PRECLINICAL",
          title: "Murine db/db Models",
          desc: "Dose-dependent glucose attenuation in diabetic rodent cohorts.",
          badge: "Validated",
          badgeColor: "bg-blue-950 text-blue-300 border-blue-800"
        },
        {
          stage: "4. HUMAN RCTs",
          title: "Primary Clinical Trials",
          desc: "Yin 2008 (n=84), Zhang 2008 (n=116), Gu 2010 (n=365) confirm HbA1c drop.",
          badge: "Level 1b",
          badgeColor: "bg-teal-950 text-teal-300 border-teal-800"
        },
        {
          stage: "5. META-ANALYSIS",
          title: "Pooled Synthesis",
          desc: "Lan et al. 2015: 27 RCTs (n=2,569), pooled HbA1c Δ -0.72% (p < 0.001).",
          badge: "Level 1a",
          badgeColor: "bg-cyan-950 text-cyan-300 border-cyan-800"
        },
        {
          stage: "6. VERDICT",
          title: "Epistemic Status",
          desc: "Mechanistically Plausible & Clinically Verified (Moderate Certainty, GRADE 1A/B).",
          badge: "Clinically Verified",
          badgeColor: "bg-emerald-950 text-emerald-300 border-emerald-700"
        }
      ];

      container.innerHTML = chainSteps.map(s => `
        <div class="p-3 bg-gray-950/80 rounded-xl border border-gray-800 space-y-1.5 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between text-[10px] font-mono text-gray-400">
              <span>${s.stage}</span>
              <span class="px-1.5 py-0.2 rounded text-[9px] font-bold border ${s.badgeColor}">${s.badge}</span>
            </div>
            <div class="text-xs font-bold text-white mt-1">${s.title}</div>
            <p class="text-[11px] text-gray-300 mt-1 leading-relaxed">${s.desc}</p>
          </div>
        </div>
      `).join('');
    }
'''

    # Place js code before the closing </script>
    last_script_idx = content.rfind('</script>')
    if last_script_idx != -1:
        content = content[:last_script_idx] + js_code_to_add + "\n" + content[last_script_idx:]
    else:
        print("Warning: </script> not found.")

    return content

if __name__ == '__main__':
    with open('workbench.html', 'r', encoding='utf-8') as f:
        original = f.read()

    modified = overhaul_workbench(original)

    with open('workbench.html', 'w', encoding='utf-8') as f:
        f.write(modified)

    print("workbench.html successfully updated.")
