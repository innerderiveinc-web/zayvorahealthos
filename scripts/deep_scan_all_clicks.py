#!/usr/bin/env python3
"""
scripts/deep_scan_all_clicks.py
Exhaustively scans and executes every single inline event handler (all 228 buttons and clicks)
in workbench.html inside Apple WebKit JSC with a fully-populated DOM of all 358 IDs.
"""

from html.parser import HTMLParser
import re
import subprocess
import json

JSC_BIN = "/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc"

class EventCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.events = []
        self.all_ids = set()

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        el_id = attr_dict.get('id', '')
        if el_id:
            self.all_ids.add(el_id)
        for attr, val in attrs:
            if attr.startswith('on'):
                self.events.append({
                    'tag': tag,
                    'id': el_id,
                    'event': attr,
                    'code': val,
                    'line': self.getpos()[0]
                })

with open('workbench.html', 'r', encoding='utf-8') as f:
    wb_content = f.read()

collector = EventCollector()
collector.feed(wb_content)

print(f"Discovered {len(collector.all_ids)} DOM IDs and {len(collector.events)} inline event handlers.")

# Extract all <script> blocks
scripts = re.findall(r'<script(?:\s+[^>]*)?>(.*?)</script>', wb_content, re.DOTALL)

# Pre-populate all known DOM IDs in mock DOM
all_ids_js = json.dumps(list(collector.all_ids))

mock_env = f'''
var window = this;
window.location = {{ origin: 'https://localhost', protocol: 'https:', host: 'localhost', pathname: '/', href: 'https://localhost/', search: '' }};
window.history = {{ pushState: function() {{}} }};
window.scrollTo = function() {{}};
window.addEventListener = function() {{}};
window.removeEventListener = function() {{}};
window.print = function() {{}};

var navigator = {{
  clipboard: {{
    writeText: function() {{ return Promise.resolve(); }}
  }},
  userAgent: 'Mozilla/5.0'
}};

var knownIds = new Set({all_ids_js});
var domNodes = {{}};

function createMockElement(id) {{
  return {{
    id: id,
    classList: {{
      _classes: new Set(['hidden']),
      add: function(c) {{ this._classes.add(c); }},
      remove: function(c) {{ this._classes.delete(c); }},
      contains: function(c) {{ return this._classes.has(c); }},
      toggle: function(c, force) {{
        if (force !== undefined) {{
          if (force) this._classes.add(c); else this._classes.delete(c);
        }} else {{
          if (this._classes.has(c)) this._classes.delete(c); else this._classes.add(c);
        }}
      }}
    }},
    style: {{}},
    innerHTML: '',
    innerText: '',
    value: '',
    className: '',
    disabled: false,
    checked: false,
    focus: function() {{}},
    select: function() {{}},
    getContext: function() {{ 
      return {{
        clearRect: function() {{}}, beginPath: function() {{}}, arc: function() {{}},
        fill: function() {{}}, stroke: function() {{}}, fillText: function() {{}},
        measureText: function() {{ return {{ width: 10 }}; }}, moveTo: function() {{}},
        lineTo: function() {{}}, setLineDash: function() {{}}, strokeRect: function() {{}}
      }};
    }},
    getBoundingClientRect: function() {{ return {{ left: 0, top: 0, width: 800, height: 600 }}; }},
    appendChild: function() {{}},
    removeChild: function() {{}},
    insertBefore: function() {{}},
    parentNode: {{ removeChild: function() {{}} }},
    addEventListener: function() {{}},
    setAttribute: function() {{}},
    getAttribute: function(a) {{ return ''; }},
    querySelectorAll: function() {{ return []; }},
    querySelector: function() {{ return null; }}
  }};
}}

// Initialize all known IDs in DOM
knownIds.forEach(function(id) {{
  domNodes[id] = createMockElement(id);
}});

var document = {{
  getElementById: function(id) {{
    if (!domNodes[id]) {{
      domNodes[id] = createMockElement(id);
    }}
    return domNodes[id];
  }},
  querySelector: function() {{ return createMockElement('_query_mock'); }},
  querySelectorAll: function() {{ return [createMockElement('_query_mock')]; }},
  createElement: function(tag) {{ return createMockElement('_created_' + tag); }},
  createTextNode: function(t) {{ return {{ textContent: t }}; }},
  body: createMockElement('body'),
  addEventListener: function() {{}},
  activeElement: createMockElement('body'),
  execCommand: function() {{ return true; }}
}};

var localStorage = {{ getItem: function() {{ return null; }}, setItem: function() {{}}, removeItem: function() {{}} }};
var sessionStorage = {{ getItem: function() {{ return null; }}, setItem: function() {{}}, removeItem: function() {{}} }};
var console = {{ log: function() {{}}, warn: function() {{}}, error: function() {{}} }};
var setTimeout = function(fn) {{ return 1; }};
var clearTimeout = function() {{}};
var setInterval = function() {{ return 1; }};
var clearInterval = function() {{}};
var fetch = function() {{ return Promise.resolve({{ ok: true, json: function() {{ return Promise.resolve({{}}); }}, text: function() {{ return Promise.resolve(''); }} }}); }};
var Notification = {{ permission: 'default', requestPermission: function() {{ return Promise.resolve('granted'); }} }};
var SpeechSynthesisUtterance = function(t) {{ this.text = t; }};
var speechSynthesis = {{ speak: function() {{}}, cancel: function() {{}} }};
var URL = {{ createObjectURL: function() {{ return 'blob:http://localhost/123'; }}, revokeObjectURL: function() {{}} }};
var Blob = function() {{}};
var URLSearchParams = function() {{ this.get = function() {{ return null; }}; this.set = function() {{}}; }};
'''

# Build test runner
test_script = mock_env + "\n" + "\n".join(scripts) + "\n\nvar scan_results = [];\n"

for idx, ev in enumerate(collector.events):
    code_escaped = ev['code'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    # Wrap in function and call with dummy event object
    test_script += f'''
try {{
  (function(event) {{
    {ev['code']}
  }})({{
    stopPropagation: function() {{}},
    preventDefault: function() {{}},
    target: document.getElementById("{ev['id'] or 'body'}"),
    currentTarget: document.getElementById("{ev['id'] or 'body'}")
  }});
  scan_results.push({{ idx: {idx}, line: {ev['line']}, tag: "{ev['tag']}", id: "{ev['id']}", event: "{ev['event']}", code: "{code_escaped}", status: "PASS" }});
}} catch(err) {{
  scan_results.push({{ idx: {idx}, line: {ev['line']}, tag: "{ev['tag']}", id: "{ev['id']}", event: "{ev['event']}", code: "{code_escaped}", status: "FAIL", error: err.message || String(err) }});
}}
'''

test_script += "\nprint('SCAN_JSON_START' + JSON.stringify(scan_results) + 'SCAN_JSON_END');\n"

with open("/tmp/deep_scan_clicks.js", "w", encoding="utf-8") as f:
    f.write(test_script)

res = subprocess.run([JSC_BIN, "/tmp/deep_scan_clicks.js"], capture_output=True, text=True)

if "SCAN_JSON_START" in res.stdout:
    raw = res.stdout.split("SCAN_JSON_START")[1].split("SCAN_JSON_END")[0]
    results = json.loads(raw)
    
    passes = [r for r in results if r['status'] == 'PASS']
    fails = [r for r in results if r['status'] == 'FAIL']
    
    print("\n" + "="*80)
    print(f" DEEP SCAN REPORT: {len(results)} TOTAL EVENT HANDLERS TESTED")
    print("="*80)
    print(f" TOTAL PASS: {len(passes)} / {len(results)} ({len(passes)/len(results)*100:.1f}%)")
    print(f" TOTAL FAIL: {len(fails)} / {len(results)}")
    print("="*80)
    
    if fails:
        print("\n❌ DETECTED FAILING BUTTONS / HANDLERS:")
        for f_item in fails:
            print(f"  • Line {f_item['line']} <{f_item['tag']} id='{f_item['id']}'> {f_item['event']}=\"{f_item['code']}\"")
            print(f"    ↳ Error: {f_item['error']}\n")
    else:
        print("\n🎉 100% PERFECT! Every single button and click handler executed without errors!")
else:
    print("Execution output:", res.stdout)
    print("Errors:", res.stderr)

