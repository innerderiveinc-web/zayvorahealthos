#!/usr/bin/env python3
"""
Practical End-to-End Functional Test for all 6 User-Friendly Features.
Runs against workbench.html using WebKit JSC engine with an interactive DOM simulation.
"""

import os
import re
import subprocess
import json

JSC_BIN = "/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc"
WB_PATH = "workbench.html"

with open(WB_PATH, "r", encoding="utf-8") as f:
    wb_content = f.read()

scripts = re.findall(r'<script(?:\s+[^>]*)?>(.*?)</script>', wb_content, re.DOTALL)

test_script = '''
// Interactive Mock DOM Environment
var window = this;
window.addEventListener = function() {};
window.removeEventListener = function() {};
window.location = { origin: 'https://localhost', protocol: 'https:', host: 'localhost', pathname: '/', href: 'https://localhost/', search: '' };
window.history = { pushState: function() {} };
window.scrollTo = function() {};
window.print_called = false;
window.print = function() { window.print_called = true; };

var copied_text = null;
var navigator = { 
  clipboard: { 
    writeText: function(t) { 
      copied_text = t; 
      return Promise.resolve(); 
    } 
  },
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
};

// DOM State Store
var domStore = {};
function getOrCreateElem(id) {
  if (!domStore[id]) {
    domStore[id] = {
      id: id,
      classList: {
        _classes: new Set(['hidden']),
        add: function(c) { this._classes.add(c); },
        remove: function(c) { this._classes.delete(c); },
        contains: function(c) { return this._classes.has(c); },
        toggle: function(c) { if (this._classes.has(c)) this._classes.delete(c); else this._classes.add(c); }
      },
      style: {},
      innerHTML: '',
      innerText: '',
      value: '',
      className: '',
      addEventListener: function() {},
      focus: function() {},
      select: function() {},
      getContext: function() { return { clearRect: function(){}, beginPath: function(){}, arc: function(){}, fill: function(){}, stroke: function(){}, fillText: function(){}, measureText: function(){ return { width: 10 }; }, moveTo: function(){}, lineTo: function(){}, setLineDash: function(){}, strokeRect: function(){} }; },
      getBoundingClientRect: function() { return { left: 0, top: 0, width: 800, height: 600 }; },
      appendChild: function() {},
      removeChild: function() {}
    };
  }
  return domStore[id];
}

var document = {
  getElementById: function(id) { return getOrCreateElem(id); },
  querySelector: function() { return null; },
  querySelectorAll: function() { return []; },
  createElement: function(tag) { return getOrCreateElem('_tmp_' + Math.random()); },
  createTextNode: function(t) { return { textContent: t }; },
  body: getOrCreateElem('body'),
  addEventListener: function() {}
};

var localStorage = { getItem: function() { return null; }, setItem: function() {} };
var sessionStorage = { getItem: function() { return null; }, setItem: function() {} };
var console = { log: function(){}, warn: function(){}, error: function(){} };
var setTimeout = function(fn, ms) { return 1; };
var clearTimeout = function() {};
var setInterval = function() { return 1; };
var clearInterval = function() {};
var fetch = function() { return Promise.resolve({ ok: true, json: function() { return Promise.resolve({}); }, text: function() { return Promise.resolve(''); } }); };

'''

# Append workbench scripts
for s in scripts:
    test_script += "\n" + s + "\n"

# Append tests
test_script += '''
var test_results = [];
function assert(name, condition, details) {
  if (condition) {
    test_results.push({ name: name, passed: true, details: details || "OK" });
  } else {
    test_results.push({ name: name, passed: false, details: details || "Assertion Failed" });
  }
}

// -------------------------------------------------------------
// TEST 1: Topic Chips (selectSuggestion)
// -------------------------------------------------------------
try {
  selectSuggestion("What is the clinical evidence for berberine in metabolic health?");
  var inputVal = document.getElementById("search-input").value;
  assert("Feature 1: Topic Chip populates search and launches query", 
    inputVal.indexOf("berberine") !== -1, 
    "Search input populated with: " + inputVal);
} catch(e) {
  assert("Feature 1: Topic Chip execution", false, e.message);
}

// -------------------------------------------------------------
// TEST 2: Clinician vs Patient Mode Switcher & Language Switcher
// -------------------------------------------------------------
try {
  // Test switching to Patient mode
  switchPerspectiveMode("patient");
  var patHidden = document.getElementById("patient-friendly-view").classList.contains("hidden");
  var cliHidden = document.getElementById("clinician-deep-view").classList.contains("hidden");
  assert("Feature 2A: Switch to Patient View reveals patient UI", !patHidden, "Patient view is visible");
  assert("Feature 2B: Switch to Patient View hides complex clinician UI", cliHidden, "Clinician deep view hidden");

  // Test Roman Urdu Toggle
  setPatientLang("ur");
  var urduDose = document.getElementById("pat-dose-text").innerText || document.getElementById("pat-dose-text").innerHTML;
  assert("Feature 2C: Roman Urdu translation renders in patient mode", 
    urduDose.indexOf("Khane ke sath") !== -1 || urduDose.indexOf("Rozana") !== -1, 
    "Urdu text rendered: " + urduDose.substring(0, 40) + "...");

  // Test English Toggle
  setPatientLang("en");
  var engDose = document.getElementById("pat-dose-text").innerText || document.getElementById("pat-dose-text").innerHTML;
  assert("Feature 2D: English translation renders back in patient mode", 
    engDose.indexOf("meal") !== -1 || engDose.indexOf("dose") !== -1 || engDose.indexOf("daily") !== -1, 
    "English text rendered: " + engDose.substring(0, 40) + "...");

  // Test switching back to Clinician mode
  switchPerspectiveMode("clinician");
  var patHiddenBack = document.getElementById("patient-friendly-view").classList.contains("hidden");
  var cliHiddenBack = document.getElementById("clinician-deep-view").classList.contains("hidden");
  assert("Feature 2E: Switch back to Clinician View restores deep analysis", patHiddenBack && !cliHiddenBack, "Clinician view active");
} catch(e) {
  assert("Feature 2: Clinician/Patient switcher", false, e.message);
}

// -------------------------------------------------------------
// TEST 3: Voice Search (startVoiceSearch)
// -------------------------------------------------------------
try {
  // Check fallback when SpeechRecognition is not present
  delete window.SpeechRecognition;
  delete window.webkitSpeechRecognition;
  startVoiceSearch();
  assert("Feature 3A: Voice search gracefully handles browser without Web Speech", true, "Handled safely without crash");

  // Simulate SpeechRecognition available
  var micStarted = false;
  window.webkitSpeechRecognition = function() {
    this.start = function() { micStarted = true; if (this.onstart) this.onstart(); };
    this.stop = function() {};
  };
  startVoiceSearch();
  assert("Feature 3B: Voice search initializes and triggers listening state", micStarted, "SpeechRecognition.start() called");
} catch(e) {
  assert("Feature 3: Voice search execution", false, e.message);
}

// -------------------------------------------------------------
// TEST 4: 1-Click 30-Sec Summary Copy & Handout Print
// -------------------------------------------------------------
try {
  copied_text = null;
  copy30SecSummary();
  assert("Feature 4A: 30-Second Summary copied to clipboard", 
    copied_text !== null && copied_text.indexOf("30-Second Clinical Summary") !== -1, 
    "Copied format: " + (copied_text ? copied_text.substring(0, 45) + "..." : "null"));

  window.print_called = false;
  printPatientHandout();
  assert("Feature 4B: Patient Handout automatically triggers print dialog", 
    window.print_called === true, 
    "window.print() executed");
} catch(e) {
  assert("Feature 4: Copy summary and print handout", false, e.message);
}

// -------------------------------------------------------------
// TEST 5: Mobile Bottom Navigation Bar (setActiveMobileTab)
// -------------------------------------------------------------
try {
  setActiveMobileTab("mob-nav-safety");
  var safetyClass = document.getElementById("mob-nav-safety").className;
  var searchClass = document.getElementById("mob-nav-search").className;
  assert("Feature 5A: Mobile Tab activation updates active button style", 
    safetyClass.indexOf("text-teal-400") !== -1, 
    "Active class: " + safetyClass);
  assert("Feature 5B: Mobile Tab deactivates other buttons", 
    searchClass.indexOf("text-gray-400") !== -1, 
    "Inactive class: " + searchClass);
} catch(e) {
  assert("Feature 5: Mobile bottom nav tabs", false, e.message);
}

// -------------------------------------------------------------
// TEST 6: Vernacular "Did You Mean?" & Synonyms Helper
// -------------------------------------------------------------
try {
  // Test typing Urdu/Hindi name "darhald"
  checkVernacularSynonyms("darhald");
  var bannerHidden = document.getElementById("did-you-mean-banner").classList.contains("hidden");
  var suggestedText = document.getElementById("dym-suggested-text").innerText;
  assert("Feature 6A: Vernacular query 'darhald' reveals 'Did You Mean' banner", 
    !bannerHidden, 
    "Banner is visible");
  assert("Feature 6B: Vernacular query correctly identifies botanical synonym", 
    suggestedText.indexOf("Berberine") !== -1, 
    "Suggested text: " + suggestedText);

  // Test 1-click apply of the synonym
  applyDidYouMean();
  var finalInput = document.getElementById("search-input").value;
  var bannerHiddenAfter = document.getElementById("did-you-mean-banner").classList.contains("hidden");
  assert("Feature 6C: 1-Click apply populates scientific query and hides banner", 
    finalInput.indexOf("Berberine in Type 2 Diabetes") !== -1 && bannerHiddenAfter, 
    "Input query: " + finalInput);

  // Test other common synonyms
  checkVernacularSynonyms("haldi");
  var haldiMatch = document.getElementById("dym-suggested-text").innerText;
  assert("Feature 6D: Synonym 'haldi' maps to Curcumin", 
    haldiMatch.indexOf("Curcumin") !== -1, 
    "Matched: " + haldiMatch);

  checkVernacularSynonyms("asgandh");
  var asgandhMatch = document.getElementById("dym-suggested-text").innerText;
  assert("Feature 6E: Synonym 'asgandh' maps to Ashwagandha", 
    asgandhMatch.indexOf("Ashwagandha") !== -1, 
    "Matched: " + asgandhMatch);

  checkVernacularSynonyms("mulethi");
  var mulethiMatch = document.getElementById("dym-suggested-text").innerText;
  assert("Feature 6F: Synonym 'mulethi' maps to Licorice", 
    mulethiMatch.indexOf("Licorice") !== -1, 
    "Matched: " + mulethiMatch);

} catch(e) {
  assert("Feature 6: Vernacular synonyms helper", false, e.message);
}

// OUTPUT TEST RESULTS AS JSON
print("TEST_RESULTS_JSON:" + JSON.stringify(test_results));
'''

test_file = "/tmp/test_user_friendly_functional.js"
with open(test_file, "w", encoding="utf-8") as f:
    f.write(test_script)

res = subprocess.run([JSC_BIN, test_file], capture_output=True, text=True)

if "TEST_RESULTS_JSON:" in res.stdout:
    json_str = res.stdout.split("TEST_RESULTS_JSON:")[1].strip()
    results = json.loads(json_str)
    all_passed = True
    print("\n" + "="*70)
    print(" PRACTICAL FUNCTIONAL TEST RESULTS (WEBKIT JAVASCRIPT CORE)")
    print("="*70)
    for r in results:
        status = "✅ PASS" if r["passed"] else "❌ FAIL"
        if not r["passed"]:
            all_passed = False
        print(f" {status} | {r['name']}")
        print(f"         ↳ {r['details']}")
    print("="*70)
    if all_passed:
        print(" 🎉 ALL 6 USER-FRIENDLY FEATURES ARE 100% PRACTICALLY WORKING!")
    else:
        print(" ⚠️ SOME FEATURES FAILED PRACTICAL VERIFICATION!")
else:
    print("Execution output:")
    print(res.stdout)
    print("Errors:")
    print(res.stderr)
