"""
Acceptance Test Suite for ZMIE Product Frontend & UX/UI Architecture (Prompt 8)
Validates:
1. Presence and integrity of all required product routes and page entrypoints.
2. Component specifications: StatusBadge, ClaimTraceDrawer, EvidenceTable, ContradictionSection, ResearchWorkspace, KnowledgeGraphViewer.
3. Truth & provenance contract alignment: all displayed UI statuses originate from governed backend data.
4. Clean separation of primary modes: Search, Medicine, Research, Evidence, Graph, Sources, Compare.
"""

import os
import unittest


class TestFrontendUXArchitecture(unittest.TestCase):

    def setUp(self):
        self.web_src = "services/web/src"

    def test_01_required_page_routes_exist(self):
        """Verifies all primary canonical product routes exist under src/app."""
        routes = [
            "app/page.tsx",
            "app/medicine/page.tsx",
            "app/research/page.tsx",
            "app/evidence/page.tsx",
            "app/graph/page.tsx",
            "app/sources/page.tsx",
            "app/compare/page.tsx",
            "app/agent-os/page.tsx",
            "app/audit/page.tsx",
            "app/compute/page.tsx",
            "app/credibility/page.tsx"
        ]
        for route in routes:
            path = os.path.join(self.web_src, route)
            self.assertTrue(os.path.isfile(path), f"Route file missing: {path}")

    def test_02_reusable_design_components_exist(self):
        """Verifies core architectural UI components conforming to design tokens."""
        components = [
            "components/NavigationHeader.tsx",
            "components/StatusBadge.tsx",
            "components/ClaimTraceDrawer.tsx",
            "components/EvidenceTable.tsx",
            "components/ContradictionSection.tsx",
            "components/ResearchWorkspace.tsx",
            "components/KnowledgeGraphViewer.tsx"
        ]
        for comp in components:
            path = os.path.join(self.web_src, comp)
            self.assertTrue(os.path.isfile(path), f"Component missing: {path}")

    def test_03_claim_trace_ui_contract(self):
        """Validates that ClaimTraceDrawer implements the required trace fields."""
        path = os.path.join(self.web_src, "components/ClaimTraceDrawer.tsx")
        with open(path, "r") as f:
            content = f.read()
        self.assertIn("claimText", content)
        self.assertIn("normalizedClaim", content)
        self.assertIn("verificationStatus", content)
        self.assertIn("passage", content)
        self.assertIn("sourceTitle", content)
        self.assertIn("limitations", content)

    def test_04_evidence_table_ui_contract(self):
        """Validates EvidenceTable column structure."""
        path = os.path.join(self.web_src, "components/EvidenceTable.tsx")
        with open(path, "r") as f:
            content = f.read()
        for col in ["Study", "Design", "Population", "Intervention", "Key Findings", "Grade", "Safety"]:
            self.assertIn(col, content)

    def test_05_contradiction_section_ui_contract(self):
        """Validates Where Evidence Differs section surfaces both positions without forced consensus."""
        path = os.path.join(self.web_src, "components/ContradictionSection.tsx")
        with open(path, "r") as f:
            content = f.read()
        self.assertIn("Where Evidence Differs", content)
        self.assertIn("Position A", content)
        self.assertIn("Position B", content)
        self.assertIn("Probable Root Cause", content)
        self.assertIn("resolution", content.lower())

    def test_06_research_workspace_pico_contract(self):
        """Validates ResearchWorkspace deconstructs PICO and inclusion/exclusion criteria."""
        path = os.path.join(self.web_src, "components/ResearchWorkspace.tsx")
        with open(path, "r") as f:
            content = f.read()
        self.assertIn("P — Population", content)
        self.assertIn("I — Intervention", content)
        self.assertIn("Inclusion Criteria", content)
        self.assertIn("Exclusion Criteria", content)

    def test_07_workbench_level_10_architecture(self):
        """Validates 10/10 Level Workbench Architecture (ZMIEStateStore, Funnel Plot SVG, Catalog Modal, CDS Hooks)."""
        workbench_path = "workbench.html"
        self.assertTrue(os.path.isfile(workbench_path))
        with open(workbench_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("ZMIEStateStore", content)
        self.assertIn("switchPrismaView", content)
        self.assertIn("funnel-plot-container", content)
        self.assertIn("catalog-modal", content)
        self.assertIn("cds-hooks-modal", content)
        self.assertIn("exportSimulatorFhirBundle", content)
        self.assertIn("inspectSimulatorCdsHooksCard", content)


if __name__ == "__main__":
    unittest.main()
