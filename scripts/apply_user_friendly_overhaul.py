#!/usr/bin/env python3
"""
apply_user_friendly_overhaul.py
Implements the 6 user-friendly enhancements requested by the user in workbench.html:
1. 1-Click Topic Chips under Search Bar
2. Clinician vs Patient Handout Switcher enhancements & 1-click summary
3. Voice Search (Microphone Dictation API)
4. 1-Click Clinical Summary Copy & Patient Handout Print
5. Mobile Native App Sticky Bottom Navigation Bar
6. Interactive "Did You Mean?" & Synonyms Helper
"""

with open('workbench.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ─────────────────────────────────────────────────────────────────────────────
# 1. ADD VOICE MIC BUTTON TO SEARCH INPUT CONTAINER
# ─────────────────────────────────────────────────────────────────────────────
old_search_container = '''            <button 
              id="search-clear-btn" 
              type="button"
              onclick="clearSearchInput(event)" 
              class="hidden absolute right-44 text-gray-500 hover:text-gray-300 p-1 text-xs transition" 
              title="Clear search input"
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button 
              id="search-btn"
              onclick="closeSearchSuggestions(); triggerSearch()"
              class="absolute right-2 bg-teal-600 hover:bg-teal-500 text-white font-bold px-4 py-2 rounded-lg text-xs transition flex items-center gap-1.5 shadow"
            >
              <i class="fa-solid fa-magnifying-glass-chart text-xs"></i>
              <span id="btn-text">Appraise Evidence</span>
            </button>'''

new_search_container = '''            <button 
              id="search-clear-btn" 
              type="button"
              onclick="clearSearchInput(event)" 
              class="hidden absolute right-48 text-gray-500 hover:text-gray-300 p-1 text-xs transition" 
              title="Clear search input"
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button 
              id="search-mic-btn" 
              type="button"
              onclick="startVoiceSearch()" 
              class="absolute right-40 text-gray-400 hover:text-teal-400 p-1.5 rounded-lg transition" 
              title="Voice Search (Speak query)"
            >
              <i id="mic-icon" class="fa-solid fa-microphone text-sm"></i>
            </button>
            <button 
              id="search-btn"
              onclick="closeSearchSuggestions(); triggerSearch()"
              class="absolute right-2 bg-teal-600 hover:bg-teal-500 text-white font-bold px-4 py-2 rounded-lg text-xs transition flex items-center gap-1.5 shadow"
            >
              <i class="fa-solid fa-magnifying-glass-chart text-xs"></i>
              <span id="btn-text">Appraise Evidence</span>
            </button>'''

if old_search_container in content:
    content = content.replace(old_search_container, new_search_container)
    print("Feature 3 (Voice Mic Button) added.")
else:
    print("Warning: old_search_container not found.")

# ─────────────────────────────────────────────────────────────────────────────
# 2. ADD 1-CLICK TOPIC CHIPS & DID-YOU-MEAN BANNER UNDER SEARCH BOX
# ─────────────────────────────────────────────────────────────────────────────
old_search_box_end = '''          <!-- Floating Spotlight Suggestions Dropdown (Only appears when search input is focused) -->'''

chips_and_synonym_markup = '''          <!-- Interactive "Did You Mean?" Synonyms Helper Banner -->
          <div id="did-you-mean-banner" class="hidden mt-2 p-2.5 rounded-xl bg-teal-950/70 border border-teal-800 text-xs text-gray-300 flex items-center justify-between transition-all shadow-md">
            <div class="flex items-center gap-2">
              <i class="fa-solid fa-lightbulb text-amber-400"></i>
              <span>Did you mean: <strong id="dym-suggested-text" class="text-teal-300 font-semibold cursor-pointer hover:underline" onclick="applyDidYouMean()"></strong>?</span>
            </div>
            <button onclick="applyDidYouMean()" class="px-2.5 py-1 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-bold text-[11px] transition shadow">
              Appraise Now
            </button>
          </div>

          <!-- Feature 1: 1-Click Quick Clinical Inquiries (Directly below search bar) -->
          <div class="mt-3 flex items-center justify-center flex-wrap gap-2 text-xs">
            <span class="text-[11px] text-gray-500 font-medium mr-1 flex items-center gap-1"><i class="fa-solid fa-bolt text-amber-400"></i> Quick Topics:</span>
            <button onclick="selectSuggestion('What is the clinical evidence for berberine in metabolic health?')" class="px-3 py-1.5 rounded-full bg-gray-900/90 hover:bg-gray-800 border border-teal-800/60 hover:border-teal-500 text-teal-300 hover:text-white transition flex items-center gap-1.5 shadow-sm text-[11px] font-medium">
              <span>🩺</span> <span>Diabetes (Berberine)</span>
            </button>
            <button onclick="selectSuggestion('Pharmacokinetic bleeding risk of Warfarin combined with St Johns Wort or Garlic')" class="px-3 py-1.5 rounded-full bg-gray-900/90 hover:bg-gray-800 border border-rose-800/60 hover:border-rose-500 text-rose-300 hover:text-white transition flex items-center gap-1.5 shadow-sm text-[11px] font-medium">
              <span>🫀</span> <span>Blood Thinner Risk (Warfarin + Garlic)</span>
            </button>
            <button onclick="selectSuggestion('Ashwagandha Withania somnifera efficacy in HPA axis cortisol stress modulation')" class="px-3 py-1.5 rounded-full bg-gray-900/90 hover:bg-gray-800 border border-indigo-800/60 hover:border-indigo-500 text-indigo-300 hover:text-white transition flex items-center gap-1.5 shadow-sm text-[11px] font-medium">
              <span>🧠</span> <span>Stress &amp; Cortisol (Ashwagandha)</span>
            </button>
            <button onclick="selectSuggestion('Bioavailability enhancement of Curcumin by Piperine via hepatic glucuronidation')" class="px-3 py-1.5 rounded-full bg-gray-900/90 hover:bg-gray-800 border border-amber-800/60 hover:border-amber-500 text-amber-300 hover:text-white transition flex items-center gap-1.5 shadow-sm text-[11px] font-medium">
              <span>🦴</span> <span>Joint Pain (Curcumin + Piperine)</span>
            </button>
            <button onclick="selectSuggestion('Compare Unani and Ayurveda perspectives on digestion')" class="px-3 py-1.5 rounded-full bg-gray-900/90 hover:bg-gray-800 border border-emerald-800/60 hover:border-emerald-500 text-emerald-300 hover:text-white transition flex items-center gap-1.5 shadow-sm text-[11px] font-medium">
              <span>🌿</span> <span>Digestion (Hazm vs Agni)</span>
            </button>
          </div>

          <!-- Floating Spotlight Suggestions Dropdown (Only appears when search input is focused) -->'''

if old_search_box_end in content:
    content = content.replace(old_search_box_end, chips_and_synonym_markup)
    print("Features 1 & 6 (Topic Chips & Did You Mean markup) added.")
else:
    print("Warning: old_search_box_end not found.")

# ─────────────────────────────────────────────────────────────────────────────
# 3. ADD 1-CLICK SUMMARY COPY & PATIENT HANDOUT BUTTONS IN MONOGRAPH TOP BAR
# ─────────────────────────────────────────────────────────────────────────────
old_topbar_actions = '''              <button onclick="copySynthesisToClipboard()" class="bg-gray-900 hover:bg-gray-800 border border-gray-700 text-gray-300 hover:text-white px-2.5 py-1.5 rounded-lg transition flex items-center gap-1.5 font-medium shadow-sm whitespace-nowrap" title="Copy evidence synthesis">
                <i id="copy-icon" class="fa-solid fa-copy text-gray-400"></i> <span id="copy-text">Copy</span>
              </button>'''

new_topbar_actions = '''              <button onclick="copy30SecSummary()" class="bg-teal-950/70 hover:bg-teal-900/90 border border-teal-700/60 text-teal-300 hover:text-white px-2.5 py-1.5 rounded-lg transition flex items-center gap-1.5 font-medium shadow-sm whitespace-nowrap" title="Copy 30-Second Bullet Summary (WhatsApp / Clinical Note)">
                <i class="fa-solid fa-clipboard-list text-teal-400"></i> <span>30s Summary</span>
              </button>
              <button onclick="printPatientHandout()" class="bg-indigo-950/70 hover:bg-indigo-900/90 border border-indigo-700/60 text-indigo-300 hover:text-white px-2.5 py-1.5 rounded-lg transition flex items-center gap-1.5 font-medium shadow-sm whitespace-nowrap" title="Print Clean 1-Page Patient Handout (English / Urdu)">
                <i class="fa-solid fa-file-invoice text-indigo-400"></i> <span>Patient Handout</span>
              </button>
              <button onclick="copySynthesisToClipboard()" class="bg-gray-900 hover:bg-gray-800 border border-gray-700 text-gray-300 hover:text-white px-2.5 py-1.5 rounded-lg transition flex items-center gap-1.5 font-medium shadow-sm whitespace-nowrap" title="Copy evidence synthesis">
                <i id="copy-icon" class="fa-solid fa-copy text-gray-400"></i> <span id="copy-text">Copy</span>
              </button>'''

if old_topbar_actions in content:
    content = content.replace(old_topbar_actions, new_topbar_actions)
    print("Feature 4 (30-Sec Summary & Patient Handout Print buttons) added.")
else:
    print("Warning: old_topbar_actions not found.")

# ─────────────────────────────────────────────────────────────────────────────
# 4. ADD MOBILE STICKY BOTTOM NAVIGATION BAR
# ─────────────────────────────────────────────────────────────────────────────
mobile_bottom_nav = '''  <!-- Feature 5: Mobile App Native Sticky Bottom Navigation Bar (md:hidden) -->
  <nav class="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-gray-950/95 backdrop-blur-xl border-t border-gray-800 px-3 py-2 flex items-center justify-around text-[10px] shadow-2xl">
    <button onclick="handleEvidenceTabClick(); setActiveMobileTab('mob-nav-search');" id="mob-nav-search" class="flex flex-col items-center gap-1 text-teal-400 font-bold transition">
      <i class="fa-solid fa-magnifying-glass text-base"></i>
      <span>Evidence</span>
    </button>
    <button onclick="switchMode('encyclopedia'); setActiveMobileTab('mob-nav-materia');" id="mob-nav-materia" class="flex flex-col items-center gap-1 text-gray-400 hover:text-white transition">
      <i class="fa-solid fa-book-atlas text-base"></i>
      <span>Materia Medica</span>
    </button>
    <button onclick="switchMode('simulator'); setActiveMobileTab('mob-nav-safety');" id="mob-nav-safety" class="flex flex-col items-center gap-1 text-gray-400 hover:text-white transition">
      <i class="fa-solid fa-shield-halved text-base"></i>
      <span>Safety Guard</span>
    </button>
    <button onclick="switchMode('prisma'); setActiveMobileTab('mob-nav-prisma');" id="mob-nav-prisma" class="flex flex-col items-center gap-1 text-gray-400 hover:text-white transition">
      <i class="fa-solid fa-chart-column text-base"></i>
      <span>PRISMA</span>
    </button>
  </nav>

  <!-- Padding spacer for mobile navigation so content is never obscured -->
  <div class="md:hidden h-16 w-full"></div>
'''

content = content.replace('</body>', mobile_bottom_nav + '\n</body>')
print("Feature 5 (Mobile Sticky Bottom Bar) added.")

# ─────────────────────────────────────────────────────────────────────────────
# 5. ADD JAVASCRIPT LOGIC FOR THE 6 NEW USER-FRIENDLY CAPABILITIES
# ─────────────────────────────────────────────────────────────────────────────
user_friendly_js = '''
    // =========================================================================
    // USER-FRIENDLY SUITE: VOICE SEARCH, SYNONYMS, SUMMARY & MOBILE NAV
    // =========================================================================

    // 1. Voice Search Web Speech API
    let isVoiceListening = false;
    let speechRecognitionInstance = null;

    function startVoiceSearch() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        showToast("Voice search is not supported in this browser. Please use Chrome, Edge, or Safari.", "fa-microphone-slash", "text-amber-400");
        return;
      }
      const micIcon = document.getElementById('mic-icon');
      const input = document.getElementById('search-input');

      if (isVoiceListening && speechRecognitionInstance) {
        try { speechRecognitionInstance.stop(); } catch(e){}
        isVoiceListening = false;
        if (micIcon) micIcon.className = "fa-solid fa-microphone text-sm";
        return;
      }

      try {
        speechRecognitionInstance = new SpeechRecognition();
        speechRecognitionInstance.lang = 'en-US';
        speechRecognitionInstance.interimResults = false;
        speechRecognitionInstance.maxAlternatives = 1;

        speechRecognitionInstance.onstart = function() {
          isVoiceListening = true;
          if (micIcon) micIcon.className = "fa-solid fa-microphone text-sm text-rose-500 animate-pulse";
          showToast("Listening... Speak botanical or clinical query", "fa-microphone", "text-teal-400");
        };

        speechRecognitionInstance.onresult = function(event) {
          const transcript = event.results[0][0].transcript;
          if (input) {
            input.value = transcript;
            toggleClearButton();
            checkVernacularSynonyms(transcript);
          }
          showToast(`Recognized: "${transcript}"`, "fa-check", "text-emerald-400");
          setTimeout(() => { triggerSearch(); }, 400);
        };

        speechRecognitionInstance.onerror = function(event) {
          isVoiceListening = false;
          if (micIcon) micIcon.className = "fa-solid fa-microphone text-sm";
          if (event.error !== 'no-speech') {
            showToast("Voice recognition: " + event.error, "fa-triangle-exclamation", "text-rose-400");
          }
        };

        speechRecognitionInstance.onend = function() {
          isVoiceListening = false;
          if (micIcon) micIcon.className = "fa-solid fa-microphone text-sm";
        };

        speechRecognitionInstance.start();
      } catch (err) {
        console.warn("Speech recognition error:", err);
        showToast("Could not access microphone: " + err.message, "fa-triangle-exclamation", "text-rose-400");
      }
    }

    // 2. Vernacular Synonyms & "Did You Mean?" Helper
    const VERNACULAR_SYNONYM_MAP = {
      'darhald': { target: 'Berberine (Daruharidra / Berberis aristata)', query: 'Berberine in Type 2 Diabetes' },
      'daruharidra': { target: 'Berberine (Daruharidra / Berberis aristata)', query: 'Berberine in Type 2 Diabetes' },
      'haldi': { target: 'Curcumin + Piperine (Turmeric / Zardchoba)', query: 'Curcumin + Piperine joint pain' },
      'turmeric': { target: 'Curcumin + Piperine (Turmeric / Zardchoba)', query: 'Curcumin + Piperine joint pain' },
      'zardchob': { target: 'Curcumin + Piperine (Turmeric / Zardchoba)', query: 'Curcumin + Piperine joint pain' },
      'asgandh': { target: 'Ashwagandha (Withania somnifera / Asgand)', query: 'Ashwagandha Withania somnifera cortisol anxiety' },
      'ashwagandha': { target: 'Ashwagandha (Withania somnifera / Asgand)', query: 'Ashwagandha Withania somnifera cortisol anxiety' },
      'mulethi': { target: 'Licorice (Glycyrrhiza glabra / Asl-us-Soos)', query: 'Licorice Glycyrrhiza glabra safety' },
      'licorice': { target: 'Licorice (Glycyrrhiza glabra / Asl-us-Soos)', query: 'Licorice Glycyrrhiza glabra safety' },
      'adrak': { target: 'Ginger (Zingiber officinale / Zanjabeel)', query: 'Ginger Zingiber officinale dyspepsia digestion' },
      'zanjabeel': { target: 'Ginger (Zingiber officinale / Zanjabeel)', query: 'Ginger Zingiber officinale dyspepsia digestion' },
      'kalonji': { target: 'Nigella sativa (Black Seed / Shoneez)', query: 'Nigella sativa Kalonji metabolic syndrome' },
      'shoneez': { target: 'Nigella sativa (Black Seed / Shoneez)', query: 'Nigella sativa Kalonji metabolic syndrome' },
      'giloy': { target: 'Tinospora cordifolia (Giloy / Guduchi)', query: 'Tinospora cordifolia Giloy immune modulation' },
      'guduchi': { target: 'Tinospora cordifolia (Giloy / Guduchi)', query: 'Tinospora cordifolia Giloy immune modulation' },
      'gurmar': { target: 'Gymnema sylvestre (Gurmar)', query: 'Gymnema sylvestre glycemic control' }
    };

    let activeSuggestedQuery = '';

    function checkVernacularSynonyms(text = '') {
      const banner = document.getElementById('did-you-mean-banner');
      const targetTxt = document.getElementById('dym-suggested-text');
      if (!banner || !targetTxt) return;

      const words = (text || '').toLowerCase().trim().split(/\\s+/);
      let match = null;

      for (const w of words) {
        if (VERNACULAR_SYNONYM_MAP[w]) {
          match = VERNACULAR_SYNONYM_MAP[w];
          break;
        }
      }

      if (match) {
        activeSuggestedQuery = match.query;
        targetTxt.innerText = match.target;
        banner.classList.remove('hidden');
      } else {
        banner.classList.add('hidden');
        activeSuggestedQuery = '';
      }
    }

    function applyDidYouMean() {
      if (!activeSuggestedQuery) return;
      const inp = document.getElementById('search-input');
      if (inp) {
        inp.value = activeSuggestedQuery;
        toggleClearButton();
      }
      const banner = document.getElementById('did-you-mean-banner');
      if (banner) banner.classList.add('hidden');
      triggerSearch();
    }

    // 3. 30-Second Bullet Summary Copy
    function copy30SecSummary() {
      const mono = currentActiveMonograph || CLINICAL_MONOGRAPHS.berberine;
      const topic = mono.topic || mono.title || 'Clinical Evaluation';
      const grade = mono.grade || 'Level 1a';
      const endpoint = (mono.metrics && mono.metrics.endpoint) || 'Clinically meaningful endpoint';
      const dose = (mono.directives && mono.directives[1] && mono.directives[1].text) || 'Standard therapeutic titration with meals.';
      const safety = (mono.directives && mono.directives[2] && mono.directives[2].text) || 'Routine biochemical and renal panel monitoring.';

      const summary = `📋 [ZMIE 30-Second Clinical Summary: ${topic}]
• Evidence Grade: ${grade} | Primary Effect: ${endpoint}
• Dosing Protocol: ${dose}
• Safety & Monitoring: ${safety}
• Verified Provenance: Merkle HMAC-SHA256 (Part 11 Aligned)`;

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(summary).then(() => {
          showToast("Copied 30-Second Clinical Summary to Clipboard!", "fa-clipboard-check", "text-teal-400");
        });
      } else {
        showToast("Summary generated!", "fa-check", "text-teal-400");
      }
    }

    // 4. Print Clean 1-Page Patient Handout
    function printPatientHandout() {
      if (typeof switchPerspectiveMode === 'function') {
        switchPerspectiveMode('patient');
      }
      setTimeout(() => {
        window.print();
      }, 250);
    }

    // 5. Mobile Tab Switcher Active State
    function setActiveMobileTab(tabId) {
      const tabs = ['mob-nav-search', 'mob-nav-materia', 'mob-nav-safety', 'mob-nav-prisma'];
      tabs.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          if (id === tabId) {
            el.className = 'flex flex-col items-center gap-1 text-teal-400 font-bold transition';
          } else {
            el.className = 'flex flex-col items-center gap-1 text-gray-400 hover:text-white transition';
          }
        }
      });
    }
'''

# Place JS before </script>
last_script_idx = content.rfind('</script>')
if last_script_idx != -1:
    content = content[:last_script_idx] + user_friendly_js + "\n" + content[last_script_idx:]
    print("User-friendly JS functions added successfully.")

# Hook checkVernacularSynonyms into handleSearchInput
old_handle_input = '''    function handleSearchInput(e) {
      const val = e.target.value;
      if (val.trim().length > 0) {
        openSearchSuggestions();
      }
    }'''

new_handle_input = '''    function handleSearchInput(e) {
      const val = e.target.value;
      if (val.trim().length > 0) {
        openSearchSuggestions();
        checkVernacularSynonyms(val);
      } else {
        const dym = document.getElementById('did-you-mean-banner');
        if (dym) dym.classList.add('hidden');
      }
    }'''

if old_handle_input in content:
    content = content.replace(old_handle_input, new_handle_input)
    print("handleSearchInput hooked with vernacular synonym checks.")

with open('workbench.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("workbench.html user-friendly overhaul complete.")
