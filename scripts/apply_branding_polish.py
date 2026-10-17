#!/usr/bin/env python3
"""
apply_branding_polish.py
Elevates ZMIE to ZAYVORA Evidence™ with prestigious institutional branding,
cleans mock text (Hospital Alpha -> Institutional CTU),
and refines navigation & hero copy.
"""

with open('workbench.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Page Title
content = content.replace(
    '<title>ZMIE — Evidence-Based Clinical Decision Support Workstation</title>',
    '<title>ZAYVORA Evidence™ — Integrative Medical Intelligence & Decision Support</title>'
)

# 2. Top-Left Brand Logo & Title
old_brand = '''        <div class="flex items-center gap-2">
          <span class="font-bold text-base tracking-tight text-white group-hover:text-teal-300 leading-tight transition">ZMIE Clinical Workstation</span>
        </div>
        <span class="text-xs text-gray-400 font-normal">Evidence Synthesis & Pharmacovigilance</span>'''

new_brand = '''        <div class="flex items-center gap-2">
          <span class="font-extrabold text-base tracking-tight text-white group-hover:text-teal-300 leading-tight transition">ZAYVORA Evidence<span class="text-teal-400 font-mono text-xs">™</span></span>
          <span class="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-teal-950 text-teal-300 border border-teal-800">OS 2.0</span>
        </div>
        <span class="text-xs text-gray-400 font-normal">Tri-Paradigm Medical Intelligence &amp; Pharmacovigilance</span>'''

content = content.replace(old_brand, new_brand)

# 3. Center Navigation Tabs
content = content.replace(
    '''      <button id="tab-encyclopedia" onclick="switchMode('encyclopedia')" class="px-4 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-2 text-gray-400 hover:text-white hover:bg-gray-800/50" title="Classical & Modern Medical Encyclopedia">
        <i class="fa-solid fa-book-atlas text-emerald-400"></i> <span>Medical Encyclopedia</span>
      </button>''',
    '''      <button id="tab-encyclopedia" onclick="switchMode('encyclopedia')" class="px-4 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-2 text-gray-400 hover:text-white hover:bg-gray-800/50" title="Classical & Modern Botanical Materia Medica">
        <i class="fa-solid fa-book-atlas text-emerald-400"></i> <span>Botanical Materia Medica</span>
      </button>'''
)

content = content.replace(
    '''      <button id="tab-simulator" onclick="switchMode('simulator')" class="px-4 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-2 text-gray-400 hover:text-white hover:bg-gray-800/50" title="Check Drug-Herb Interactions">
        <i class="fa-solid fa-shield-halved text-amber-400"></i> <span>Drug-Herb Safety</span>
      </button>''',
    '''      <button id="tab-simulator" onclick="switchMode('simulator')" class="px-4 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-2 text-gray-400 hover:text-white hover:bg-gray-800/50" title="Check Drug-Herb Interactions">
        <i class="fa-solid fa-shield-halved text-amber-400"></i> <span>Drug-Herb Safety Guard</span>
      </button>'''
)

content = content.replace(
    '''      <button id="tab-prisma" onclick="switchMode('prisma')" class="px-4 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-2 text-gray-400 hover:text-white hover:bg-gray-800/50" title="PRISMA Systematic Review Generator">
        <i class="fa-solid fa-chart-column text-indigo-400"></i> <span>PRISMA Review</span>
      </button>''',
    '''      <button id="tab-prisma" onclick="switchMode('prisma')" class="px-4 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-2 text-gray-400 hover:text-white hover:bg-gray-800/50" title="PRISMA Systematic Review Generator">
        <i class="fa-solid fa-chart-column text-indigo-400"></i> <span>PRISMA Meta-Analysis</span>
      </button>'''
)

# 4. Top-Right Profile Dropdown Pill (Replace "Hospital Alpha" with real clinical/institutional wording)
content = content.replace(
    '<span id="role-badge-text" class="font-medium text-gray-200 group-hover:text-teal-300 transition">Attending Clinician • Hospital Alpha</span>\n          <span id="topbar-plan-pill" class="ml-1 text-[10px] bg-teal-950 text-teal-300 border border-teal-800 px-1.5 py-0.2 rounded font-mono font-semibold">Pro</span>',
    '<span id="role-badge-text" class="font-medium text-gray-200 group-hover:text-teal-300 transition">Institutional Access • Verified Clinician</span>\n          <span id="topbar-plan-pill" class="ml-1 text-[10px] bg-teal-950 text-teal-300 border border-teal-800 px-1.5 py-0.2 rounded font-mono font-semibold">Enterprise</span>'
)

content = content.replace(
    '''              <div>
                <div class="font-bold text-white text-sm">Dr. Ashraf</div>
                <div class="text-[11px] text-gray-400">Attending Physician • Clinical Lead</div>
                <div class="text-[10px] text-teal-400 font-mono mt-0.5 flex items-center gap-1">
                  <span class="h-1.5 w-1.5 rounded-full bg-emerald-400"></span> Hospital Alpha Enclave
                </div>
              </div>''',
    '''              <div>
                <div class="font-bold text-white text-sm">Dr. Ashraf, MD</div>
                <div class="text-[11px] text-gray-400">Attending Physician • Clinical Research Lead</div>
                <div class="text-[10px] text-teal-400 font-mono mt-0.5 flex items-center gap-1">
                  <span class="h-1.5 w-1.5 rounded-full bg-emerald-400"></span> Institutional CTU Enclave
                </div>
              </div>'''
)

# 5. Tier Banner & Ribbon Text
content = content.replace(
    '<span><strong>Hospital Enterprise Enclave:</strong> Connected to Hospital Alpha CTU • Tenant Boundary Isolation (INV-02) Active • Bi-directional FHIR R4 Gateway Ready.</span>',
    '<span><strong>Institutional Healthcare Enclave:</strong> Connected to Institutional CTU • Tenant Boundary Isolation (INV-02) Active • Bi-directional FHIR R4 Gateway Ready.</span>'
)
content = content.replace(
    '<span id="ribbon-quality-text">Enclave: <strong>Hospital Alpha CTU</strong></span>',
    '<span id="ribbon-quality-text">Enclave: <strong>Institutional CTU</strong></span>'
)
content = content.replace(
    '<span class="text-[10px] text-teal-400 font-mono">Connected Target: Epic Systems / Cerner Millennium (Hospital Alpha CTU)</span>',
    '<span class="text-[10px] text-teal-400 font-mono">Connected Target: Epic Systems / Cerner Millennium (Institutional Health Gateway)</span>'
)
content = content.replace(
    '<span><strong>HTTP 201 Created:</strong> DiagnosticReport ingested successfully into Hospital Alpha Epic EHR.',
    '<span><strong>HTTP 201 Created:</strong> DiagnosticReport ingested successfully into Institutional Epic EHR.'
)

# 6. Hero Section Titles & Copy
old_hero = '''        <!-- Hero Header -->
        <div class="text-center max-w-2xl mx-auto mb-2">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-950/80 border border-teal-800/80 text-teal-300 text-[11px] font-semibold mb-3 shadow-sm">
            <i class="fa-solid fa-stethoscope text-teal-400"></i> Evidence-Based Clinical Decision Support
          </div>
          <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight mb-2">
            Search Verified Medical Evidence
          </h1>
          <p class="text-gray-400 text-xs sm:text-sm leading-relaxed">
            Connected to 38+ million biomedical records and clinical study registries (PubMed / NLM, Cochrane, Europe PMC) alongside classical pharmacopeial codices. Every assertion is backed by primary source citation and transparent verification.
          </p>
        </div>'''

new_hero = '''        <!-- Hero Header -->
        <div class="text-center max-w-3xl mx-auto mb-2">
          <div class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-teal-950/80 border border-teal-800/80 text-teal-300 text-[11px] font-semibold mb-3 shadow-sm">
            <i class="fa-solid fa-microscope text-teal-400"></i> Tri-Paradigm Clinical Decision Support (Biomedicine • Unani • Ayurveda)
          </div>
          <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight mb-2">
            Integrative Medical Intelligence &amp; Evidence Engine
          </h1>
          <p class="text-gray-400 text-xs sm:text-sm leading-relaxed max-w-2xl mx-auto">
            Synthesizing 38+ million biomedical records and clinical study registries (PubMed / NLM, Cochrane CENTRAL, Europe PMC) with classical pharmacopeial codices (UPI, NFUM, CCRUM). Every clinical assertion is backed by deterministic citation provenance.
          </p>
        </div>'''

content = content.replace(old_hero, new_hero)

# 7. Search Input Placeholder
content = content.replace(
    'placeholder="Search a condition, drug, or clinical question (e.g. Berberine in Type 2 Diabetes)..."',
    'placeholder="Search a condition, botanical, pharmaceutical, or clinical question (e.g. Berberine in Type 2 Diabetes, Curcumin, Warfarin)..."'
)

# 8. Living Encyclopedia Title
content = content.replace(
    '<h1 class="text-2xl md:text-3xl font-extrabold tracking-tight">\n            The Living Medical Encyclopedia\n          </h1>',
    '<h1 class="text-2xl md:text-3xl font-extrabold tracking-tight">\n            The Living Materia Medica &amp; Codex\n          </h1>'
)

# 9. Script Role Badge & Toast Strings
content = content.replace(
    "roleBadge.innerText = 'Attending Clinician • Hospital Alpha CTU';",
    "roleBadge.innerText = 'Clinical Lead • Institutional CTU';"
)
content = content.replace(
    "ribbonQuality.innerHTML = 'Enclave: <strong>Hospital Alpha CTU</strong>';",
    "ribbonQuality.innerHTML = 'Enclave: <strong>Institutional CTU</strong>';"
)
content = content.replace(
    'summary.innerHTML = \'Current Active Workstation Profile: <strong class="text-teal-300">Hospital Enterprise (Alpha CTU)</strong>\';',
    'summary.innerHTML = \'Current Active Workstation Profile: <strong class="text-teal-300">Hospital Enterprise (Institutional CTU)</strong>\';'
)
content = content.replace(
    'showToast("FHIR R4 DiagnosticReport delivered to Hospital Alpha Epic Gateway!", "fa-hospital-user", "text-emerald-400");',
    'showToast("FHIR R4 DiagnosticReport delivered to Institutional Epic Gateway!", "fa-hospital-user", "text-emerald-400");'
)

with open('workbench.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Branding polish script executed successfully.")
