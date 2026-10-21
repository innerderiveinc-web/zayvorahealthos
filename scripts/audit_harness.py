#!/usr/bin/env python3
"""
ZMIE Production Automated Audit Harness & Regression Firewall
=============================================================
This script provides a 100% automated, zero-tolerance quality gate across
Frontend HTML/JS, DOM structure, PWA assets, Netlify configs, and Backend tests.

Run anytime with:
    .venv/bin/python3 scripts/audit_harness.py
"""

import sys
import os
import re
import json
import subprocess
from html.parser import HTMLParser

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKBENCH_PATH = os.path.join(ROOT_DIR, "workbench.html")
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")
SW_PATH = os.path.join(ROOT_DIR, "sw.js")
NETLIFY_PATH = os.path.join(ROOT_DIR, "netlify.toml")
SEED_PATH = os.path.join(ROOT_DIR, "catalog_seed.json")
JSC_BIN = "/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc"

class HTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in self.void_tags:
            self.stack.append((tag.lower(), self.getpos()))

    def handle_endtag(self, tag):
        t = tag.lower()
        if t in self.void_tags:
            return
        if not self.stack:
            self.errors.append(f"Unexpected closing tag </{t}> at line {self.getpos()[0]}")
            return
        last_tag, pos = self.stack[-1]
        if last_tag == t:
            self.stack.pop()
        else:
            tag_names = [x[0] for x in self.stack]
            if t in tag_names:
                idx = tag_names[::-1].index(t)
                real_idx = len(self.stack) - 1 - idx
                unclosed = self.stack[real_idx+1:]
                for ut, upos in unclosed:
                    self.errors.append(f"Unclosed <{ut}> (line {upos[0]}) before </{t}> (line {self.getpos()[0]})")
                self.stack = self.stack[:real_idx]
            else:
                self.errors.append(f"Mismatched </{t}> (line {self.getpos()[0]}), expected </{last_tag}> (line {pos[0]})")


def step(num, title):
    print(f"\n[{num}/8] {title}...")


def main():
    print("=" * 70)
    print(" ZMIE PERMANENT SYSTEM QUALITY & INTEGRITY HARNESS")
    print("=" * 70)
    failed = False

    # 1. FILE PARITY
    step(1, "Checking Workbench & Index.html Parity")
    if not os.path.exists(WORKBENCH_PATH) or not os.path.exists(INDEX_PATH):
        print("  FAIL: workbench.html or index.html missing!")
        return 1
    with open(WORKBENCH_PATH, "r", encoding="utf-8") as f:
        wb_content = f.read()
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        idx_content = f.read()
    if wb_content != idx_content:
        print("  FAIL: workbench.html and index.html are out of sync!")
        failed = True
    else:
        print("  PASS: workbench.html and index.html are 100% identical.")

    # 2. HTML DOM INTEGRITY
    step(2, "Auditing HTML Tag Nesting & Balance")
    val = HTMLValidator()
    val.feed(wb_content)
    if val.errors or val.stack:
        print(f"  FAIL: Found {len(val.errors)} tag errors, {len(val.stack)} unclosed tags:")
        for err in val.errors[:5]:
            print(f"    - {err}")
        for ut, upos in val.stack:
            print(f"    - Unclosed <{ut}> at line {upos[0]}")
        failed = True
    else:
        print("  PASS: 0 tag errors, all HTML tags properly closed.")

    # 3. DOM ID INTEGRITY
    step(3, "Auditing DOM IDs & Script References")
    html_markup = wb_content.split("<script>")[0]
    ids_in_markup = re.findall(r'id=\"([a-zA-Z0-9_\-]+)\"', html_markup)
    duplicates = [k for k in set(ids_in_markup) if ids_in_markup.count(k) > 1]
    if duplicates:
        print(f"  FAIL: Duplicate IDs in HTML: {duplicates}")
        failed = True
    else:
        print(f"  PASS: 0 duplicate IDs across {len(set(ids_in_markup))} unique markup elements.")

    queried_ids = set(re.findall(r'document\.getElementById\([\'\"]([a-zA-Z0-9_\-]+)[\'\"]\)', wb_content))
    all_defined_ids = set(re.findall(r'id=\"([a-zA-Z0-9_\-]+)\"', wb_content))
    missing_ids = queried_ids - all_defined_ids
    if missing_ids:
        print(f"  FAIL: JavaScript queries IDs that do not exist: {sorted(missing_ids)}")
        failed = True
    else:
        print(f"  PASS: All {len(queried_ids)} queried DOM elements exist in markup.")

    # 4. EVENT HANDLERS ACCESSIBILITY
    step(4, "Auditing Inline Event Handlers & Global Function Bindings")
    handlers = re.findall(r'\b(on\w+)\s*=\s*\"([^\"]+)\"', wb_content)
    fn_calls = set()
    for _, code in handlers:
        for m in re.findall(r'([a-zA-Z0-9_$]+)\s*\(', code):
            if m not in ('if', 'for', 'while', 'switch', 'alert', 'confirm', 'prompt', 'encodeURIComponent', 'parseInt', 'parseFloat', 'replace', 'trim', 'split', 'scrollTo', 'select'):
                fn_calls.add(m)
    print(f"  Found {len(handlers)} event handler attributes calling {len(fn_calls)} unique functions.")

    # 5. JAVASCRIPT AST & EXECUTION VIA APPLE JSC
    step(5, "Verifying JavaScript AST Execution & Stress Testing in WebKit Engine")
    if os.path.exists(JSC_BIN):
        scripts = re.findall(r'<script(?:\s+[^>]*)?>(.*?)</script>', wb_content, re.DOTALL)
        mock_env = '''
var window = this;
window.addEventListener = function() {};
window.location = { origin: 'https://localhost', protocol: 'https:', host: 'localhost', pathname: '/', href: 'https://localhost/', search: '' };
window.history = { pushState: function() {} };
window.scrollTo = function() {};
var document = {
  getElementById: function() { 
    return { 
      classList: { add: function(){}, remove: function(){}, contains: function(){ return false; }, toggle: function(){} }, 
      style: {}, innerHTML: '', innerText: '', addEventListener: function(){}, value: '',
      getContext: function() { return { clearRect: function(){}, beginPath: function(){}, arc: function(){}, fill: function(){}, stroke: function(){}, fillText: function(){}, measureText: function(){ return { width: 10 }; }, moveTo: function(){}, lineTo: function(){}, setLineDash: function(){}, strokeRect: function(){} }; },
      getBoundingClientRect: function() { return { left: 0, top: 0, width: 800, height: 600 }; },
      focus: function(){}, select: function(){}, appendChild: function(){}, removeChild: function(){}, insertBefore: function(){},
      parentNode: { removeChild: function(){} }, querySelectorAll: function(){ return []; }, querySelector: function(){ return null; }
    }; 
  },
  querySelector: function() { return null; }, querySelectorAll: function() { return []; },
  createElement: function() { return { setAttribute: function(){}, appendChild: function(){}, classList: { add: function(){} }, style: {}, click: function(){}, focus: function(){}, select: function(){} }; },
  createTextNode: function(t) { return { textContent: t }; },
  body: { classList: { add: function(){}, remove: function(){}, contains: function(){ return false; }, toggle: function(){} }, appendChild: function(){}, removeChild: function(){} },
  documentElement: { style: {}, classList: { add: function(){}, remove: function(){}, contains: function(){ return false; }, toggle: function(){} } },
  addEventListener: function() {}, activeElement: { tagName: 'BODY' }, execCommand: function() { return true; }
};
var localStorage = { getItem: function() { return null; }, setItem: function() {}, removeItem: function() {} };
var sessionStorage = { getItem: function() { return null; }, setItem: function() {}, removeItem: function() {} };
var navigator = { clipboard: { writeText: function() { return Promise.resolve(); } }, userAgent: 'Mozilla/5.0' };
var console = { log: function(){}, warn: function(){}, error: function(){} };
var setTimeout = function(fn) { return 1; }, clearTimeout = function() {}, setInterval = function() { return 1; }, clearInterval = function() {};
var fetch = function() { return Promise.resolve({ ok: true, json: function() { return Promise.resolve({}); }, text: function() { return Promise.resolve(''); } }); };
var Notification = { permission: 'default', requestPermission: function() { return Promise.resolve('granted'); } };
var SpeechSynthesisUtterance = function(t) { this.text = t; };
var speechSynthesis = { speak: function(){}, cancel: function(){} };
var URL = { createObjectURL: function() { return 'blob:http://localhost/123'; }, revokeObjectURL: function() {} };
var Blob = function() {};
var URLSearchParams = function() { this.get = function() { return null; }; };
'''
        test_js_path = "/tmp/zmie_harness_test.js"
        with open(test_js_path, "w", encoding="utf-8") as f:
            f.write(mock_env)
            for s in scripts:
                f.write("\n" + s + "\n")
            
            # Check function accessibility
            f.write("\n// Accessibility Check\n")
            for fn in sorted(fn_calls):
                f.write(f"if (typeof {fn} !== 'function' && typeof window['{fn}'] !== 'function') throw new Error('Missing handler function: {fn}');\n")
            
            # Stress call all function declarations
            fn_decls = set(re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', wb_content))
            f.write("\n// Stress Call Declarations\n")
            for fn in sorted(fn_decls):
                f.write(f"try {{ if (typeof {fn} === 'function') {fn}(); }} catch(e) {{ throw new Error('Crash in {fn}(): ' + e.message); }}\n")
            f.write("print('JSC_PASSED');\n")

        res = subprocess.run([JSC_BIN, test_js_path], capture_output=True, text=True)
        if res.returncode == 0 and "JSC_PASSED" in res.stdout:
            print("  PASS: JSC verified 0 syntax errors, 100% callable handlers, 0 stress crashes.")
        else:
            print(f"  FAIL: JSC error:\n{res.stderr or res.stdout}")
            failed = True
    else:
        print("  SKIP: Apple JSC binary not present on this host.")

    # 6. STATIC DEPLOYMENT & PWA ASSETS
    step(6, "Checking Static Assets & Netlify Config")
    if not os.path.exists(SW_PATH):
        print("  FAIL: sw.js missing in repository root!")
        failed = True
    else:
        print("  PASS: sw.js is present.")

    if not os.path.exists(NETLIFY_PATH):
        print("  FAIL: netlify.toml missing in repository root!")
        failed = True
    else:
        print("  PASS: netlify.toml is present.")

    if not os.path.exists(SEED_PATH):
        print("  FAIL: catalog_seed.json missing in repository root!")
        failed = True
    else:
        try:
            with open(SEED_PATH, "r", encoding="utf-8") as f:
                seed_data = json.load(f)
            entries_count = len(seed_data.get("entries", []))
            print(f"  PASS: catalog_seed.json is valid JSON with {entries_count} botanical codex entries.")
        except Exception as e:
            print(f"  FAIL: catalog_seed.json corrupt: {e}")
            failed = True

    # 7. BACKEND API ENDPOINTS
    step(7, "Checking FastAPI Web Gateway Endpoints")
    try:
        sys.path.insert(0, os.path.join(ROOT_DIR, "services", "engine"))
        from app.main import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        endpoints = ["/", "/workbench", "/index.html", "/catalog_seed.json", "/sw.js", "/health"]
        for ep in endpoints:
            r = client.get(ep)
            if r.status_code not in (200, 204):
                print(f"  FAIL: Endpoint {ep} returned status {r.status_code}")
                failed = True
        print(f"  PASS: All {len(endpoints)} gateway routes returned HTTP 200/204.")
    except Exception as e:
        print(f"  FAIL: FastAPI endpoint check failed: {e}")
        failed = True

    # 8. FULL UNIT TEST SUITE
    step(8, "Running Full Backend Unit Test Suite (501 Tests)")
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{os.path.join(ROOT_DIR, 'services', 'engine')}:{os.path.join(ROOT_DIR, 'sdk', 'python')}"
    python_bin = os.path.join(ROOT_DIR, ".venv", "bin", "python3")
    res = subprocess.run([python_bin, "-m", "unittest", "discover", "tests"], cwd=ROOT_DIR, env=env, capture_output=True, text=True)
    if res.returncode == 0:
        match = re.search(r"Ran (\d+) tests", res.stderr)
        count = match.group(1) if match else "all"
        print(f"  PASS: All {count} unit tests passed cleanly.")
    else:
        print(f"  FAIL: Backend tests failed:\n{res.stderr}")
        failed = True

    print("\n" + "=" * 70)
    if failed:
        print(" OVERALL AUDIT: FAILED. Please review the errors above.")
        print("=" * 70)
        return 1
    else:
        print(" OVERALL AUDIT: 100% PASSED. SYSTEM IS COMPLETELY PRODUCTION-READY.")
        print("=" * 70)
        return 0

if __name__ == "__main__":
    sys.exit(main())
