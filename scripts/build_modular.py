#!/usr/bin/env python3
"""
ZMIE Modular Source Decomposer & Build Compiler
================================================
Breaks the monolithic workbench.html into modular source files in src/
and provides a one-command build tool to compile src/ into workbench.html & index.html.

Usage:
    python3 scripts/build_modular.py --split     # Extract workbench.html into modular src/
    python3 scripts/build_modular.py --build     # Rebuild workbench.html and index.html from src/
    python3 scripts/build_modular.py --verify    # Run audit harness after build
"""

import sys
import os
import json
import shutil
import subprocess

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
WORKBENCH_PATH = os.path.join(ROOT_DIR, "workbench.html")
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")

def ensure_dirs():
    os.makedirs(os.path.join(SRC_DIR, "components"), exist_ok=True)
    os.makedirs(os.path.join(SRC_DIR, "data"), exist_ok=True)
    os.makedirs(os.path.join(SRC_DIR, "scripts"), exist_ok=True)

def split_monolith():
    print(f"Decomposing {WORKBENCH_PATH} into modular files under src/...")
    ensure_dirs()
    
    with open(WORKBENCH_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the main <script> tag that holds application logic
    script_start_idx = content.find("<script>")
    script_end_idx = content.rfind("</script>")
    
    if script_start_idx == -1 or script_end_idx == -1:
        print("Error: Could not locate <script> block in workbench.html")
        return False

    html_markup = content[:script_start_idx]
    js_bundle = content[script_start_idx + len("<script>"):script_end_idx]
    html_footer = content[script_end_idx + len("</script>"):]

    # Save HTML templates
    with open(os.path.join(SRC_DIR, "components", "markup.html"), "w", encoding="utf-8") as f:
        f.write(html_markup.strip() + "\n")
        
    with open(os.path.join(SRC_DIR, "components", "footer.html"), "w", encoding="utf-8") as f:
        f.write(html_footer.strip() + "\n")

    # Split JavaScript bundle into data, engines, and main app
    # Look for major boundary comments
    sections = {}
    current_sec = "core_logic"
    sec_lines = []
    
    for line in js_bundle.splitlines():
        if "const PUBMED_MESH_DICTIONARY" in line or "1. PubMed MeSH Ontology" in line:
            sections[current_sec] = "\n".join(sec_lines)
            current_sec = "mesh_dictionary"
            sec_lines = [line]
        elif "const rxKnowledgeBase" in line or "Feature 1: Unified Integrative Rx Safety" in line:
            sections[current_sec] = "\n".join(sec_lines)
            current_sec = "rx_knowledge_base"
            sec_lines = [line]
        elif "const CLASSICAL_CODEX_FOLIOS" in line or "Feature 3: Classical Codex Folio Vault" in line:
            sections[current_sec] = "\n".join(sec_lines)
            current_sec = "codex_data"
            sec_lines = [line]
        elif "const DIFFERENTIAL_DIAGNOSIS_DATA" in line or "Feature 3b: Dual-Lens Differential" in line:
            sections[current_sec] = "\n".join(sec_lines)
            current_sec = "differential_data"
            sec_lines = [line]
        elif "const CLINICAL_MONOGRAPHS" in line or "CLINICAL DATA REGISTRY" in line:
            sections[current_sec] = "\n".join(sec_lines)
            current_sec = "clinical_monographs"
            sec_lines = [line]
        elif "function initApp" in line or "window.addEventListener('DOMContentLoaded'" in line:
            sections[current_sec] = "\n".join(sec_lines)
            current_sec = "app_init"
            sec_lines = [line]
        else:
            sec_lines.append(line)
            
    sections[current_sec] = "\n".join(sec_lines)

    # Write data files
    for name, code in sections.items():
        if name in ("mesh_dictionary", "rx_knowledge_base", "codex_data", "differential_data", "clinical_monographs"):
            target = os.path.join(SRC_DIR, "data", f"{name}.js")
        elif name == "app_init":
            target = os.path.join(SRC_DIR, "scripts", "main.js")
        else:
            target = os.path.join(SRC_DIR, "scripts", f"{name}.js")
            
        with open(target, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
            
    # Write manifest manifest.json
    manifest = {
        "version": "2.4.0",
        "description": "ZMIE Modular Source Architecture",
        "components": ["components/markup.html"],
        "data": [
            "data/mesh_dictionary.js",
            "data/clinical_monographs.js",
            "data/rx_knowledge_base.js",
            "data/codex_data.js",
            "data/differential_data.js"
        ],
        "scripts": [
            "scripts/core_logic.js",
            "scripts/main.js"
        ],
        "footer": "components/footer.html"
    }
    with open(os.path.join(SRC_DIR, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"  ✓ Monolith successfully decomposed into {len(sections)} modular scripts under {SRC_DIR}")
    return True

def build_monolith():
    print("Assembling modular source files from src/ into workbench.html & index.html...")
    manifest_path = os.path.join(SRC_DIR, "manifest.json")
    if not os.path.exists(manifest_path):
        print("  Error: src/manifest.json not found! Run --split first.")
        return False
        
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # 1. Read markup
    markup_parts = []
    for c in manifest.get("components", []):
        with open(os.path.join(SRC_DIR, c), "r", encoding="utf-8") as f:
            markup_parts.append(f.read().strip())

    # 2. Read JS data and scripts
    js_parts = []
    for d in manifest.get("data", []):
        p = os.path.join(SRC_DIR, d)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                js_parts.append(f.read().strip())

    for s in manifest.get("scripts", []):
        p = os.path.join(SRC_DIR, s)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                js_parts.append(f.read().strip())

    # 3. Read footer
    footer_path = os.path.join(SRC_DIR, manifest.get("footer", "components/footer.html"))
    footer_content = ""
    if os.path.exists(footer_path):
        with open(footer_path, "r", encoding="utf-8") as f:
            footer_content = f.read().strip()

    # Reassemble complete HTML
    assembled_html = "\n".join(markup_parts) + "\n  <script>\n" + "\n\n".join(js_parts) + "\n  </script>\n" + footer_content + "\n"

    with open(WORKBENCH_PATH, "w", encoding="utf-8") as f:
        f.write(assembled_html)
    shutil.copyfile(WORKBENCH_PATH, INDEX_PATH)
    print(f"  ✓ Successfully compiled to {WORKBENCH_PATH} and {INDEX_PATH} ({len(assembled_html)} bytes)")
    return True

def run_verify():
    print("Running audit harness verification...")
    res = subprocess.run([os.path.join(ROOT_DIR, ".venv", "bin", "python3"), os.path.join(ROOT_DIR, "scripts", "audit_harness.py")])
    return res.returncode == 0

def main():
    import json
    if "--split" in sys.argv:
        split_monolith()
    elif "--build" in sys.argv:
        if build_monolith():
            if "--verify" in sys.argv:
                run_verify()
    elif "--verify" in sys.argv:
        run_verify()
    else:
        print("ZMIE Modular Source Tool")
        print("Commands:")
        print("  python3 scripts/build_modular.py --split   # Decompose workbench.html into src/")
        print("  python3 scripts/build_modular.py --build   # Compile src/ into workbench.html & index.html")
        print("  python3 scripts/build_modular.py --verify  # Run audit harness")

if __name__ == "__main__":
    main()
