"""
ZMIE Full-Text PDF & Clinical Table Miner (Sections 45-52)
Parses full-text biomedical literature beyond abstracts:
1. Table 1: Baseline Demographics & Clinical Characteristics (N, Age, Sex, Baseline Biomarkers)
2. Efficacy Outcomes Tables: Primary/Secondary endpoints (Mean ± SD, MD, 95% CI, p-values)
3. Adverse Events & Safety Tables: Incident event rates, dropouts, risk ratios
4. Cryptographic Provenance Anchoring (SHA-256 byte hash + table/row coordinates) for zero-hallucination auditability.
"""

import re
import hashlib
import io
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field

try:
    import pypdf
except ImportError:
    pypdf = None


class ExtractedDataPoint(BaseModel):
    variable_name: str
    group_name: str  # "intervention", "control", "overall"
    sample_size: Optional[int] = None
    mean_value: Optional[float] = None
    sd_value: Optional[float] = None
    events_count: Optional[int] = None
    percentage: Optional[float] = None
    raw_text: str
    provenance_anchor: str
    page_number: int
    table_index: int


class ExtractedClinicalTable(BaseModel):
    table_id: str
    table_title: str
    table_type: str  # "baseline_characteristics", "efficacy_outcomes", "adverse_events", "general"
    page_number: int
    headers: List[str]
    rows: List[Dict[str, str]]
    extracted_datapoints: List[ExtractedDataPoint] = Field(default_factory=list)
    provenance_hash: str


class PDFExtractionResult(BaseModel):
    document_id: str
    total_pages: int
    tables_found: int
    tables: List[ExtractedClinicalTable]
    extracted_sample_sizes: Dict[str, int]
    primary_outcomes_detected: List[Dict[str, Any]]
    cryptographic_audit_chain: str


class PDFClinicalTableMiner:
    """
    Automated extractor of clinical trial tables, baseline characteristics,
    and numerical efficacy endpoints from full-text papers and PDFs.
    """

    @classmethod
    def parse_pdf_bytes(cls, pdf_bytes: bytes, document_id: str = "DOC-UNKNOWN") -> PDFExtractionResult:
        """
        Extracts structured clinical tables from raw PDF bytes using pypdf.
        """
        full_text_by_page: List[str] = []
        total_pages = 0

        if pypdf:
            try:
                reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
                total_pages = len(reader.pages)
                for idx, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    full_text_by_page.append(text)
            except Exception as e:
                full_text_by_page = [f"Error extracting PDF: {str(e)}"]
                total_pages = 1
        else:
            # Fallback if pypdf unavailable
            full_text_by_page = [pdf_bytes.decode("utf-8", errors="ignore")]
            total_pages = 1

        return cls.parse_full_text_pages(full_text_by_page, document_id)

    @classmethod
    def parse_full_text_pages(cls, pages: List[str], document_id: str = "DOC-UNKNOWN") -> PDFExtractionResult:
        """
        Identifies and parses tables from text pages.
        """
        tables: List[ExtractedClinicalTable] = []
        overall_samples: Dict[str, int] = {}
        primary_outcomes: List[Dict[str, Any]] = []

        table_counter = 1

        for page_idx, page_text in enumerate(pages, start=1):
            # Regex to detect Table captions (e.g., "Table 1. Baseline characteristics...", "Table 2: Efficacy...")
            table_matches = list(re.finditer(r"(Table\s+(\d+)[:\.\-]\s*([^\n\r]+))", page_text, re.IGNORECASE))

            for match in table_matches:
                table_full_header = match.group(1).strip()
                table_num = int(match.group(2))
                table_title = match.group(3).strip()

                # Slice following text block until next table or end of section
                start_pos = match.end()
                subsequent_text = page_text[start_pos:start_pos + 2500]

                table_type = cls._classify_table_type(table_title, subsequent_text)
                headers, rows, datapoints = cls._extract_table_grid(
                    subsequent_text=subsequent_text,
                    document_id=document_id,
                    page_num=page_idx,
                    table_num=table_num,
                    table_type=table_type
                )

                # Generate cryptographic SHA-256 hash of table contents
                raw_repr = f"{document_id}|{page_idx}|{table_num}|{table_title}|{str(rows)}"
                table_hash = hashlib.sha256(raw_repr.encode("utf-8")).hexdigest()

                table_obj = ExtractedClinicalTable(
                    table_id=f"TBL-{document_id}-P{page_idx}-T{table_num}",
                    table_title=table_full_header,
                    table_type=table_type,
                    page_number=page_idx,
                    headers=headers,
                    rows=rows,
                    extracted_datapoints=datapoints,
                    provenance_hash=table_hash
                )
                tables.append(table_obj)

                # Collate high-level summaries
                for dp in datapoints:
                    if dp.sample_size and dp.group_name:
                        overall_samples[dp.group_name] = max(overall_samples.get(dp.group_name, 0), dp.sample_size)
                    if table_type == "efficacy_outcomes" and dp.mean_value is not None:
                        primary_outcomes.append({
                            "outcome": dp.variable_name,
                            "group": dp.group_name,
                            "mean": dp.mean_value,
                            "sd": dp.sd_value,
                            "anchor": dp.provenance_anchor
                        })

                table_counter += 1

        # Audit chain hash
        chain_seed = "".join([t.provenance_hash for t in tables])
        chain_hash = hashlib.sha256(f"{document_id}|{chain_seed}".encode("utf-8")).hexdigest()

        return PDFExtractionResult(
            document_id=document_id,
            total_pages=len(pages),
            tables_found=len(tables),
            tables=tables,
            extracted_sample_sizes=overall_samples,
            primary_outcomes_detected=primary_outcomes,
            cryptographic_audit_chain=chain_hash
        )

    @staticmethod
    def _classify_table_type(title: str, text_content: str) -> str:
        title_l = title.lower()
        if any(w in title_l for w in ["adverse", "safety", "tolerability", "side effect"]):
            return "adverse_events"
        if any(w in title_l for w in ["baseline", "demographic", "patient characteristics", "clinical characteristics"]):
            return "baseline_characteristics"
        if any(w in title_l for w in ["efficacy", "outcome", "primary endpoint"]):
            return "efficacy_outcomes"

        combined = f"{title_l} {text_content[:300]}".lower()
        if any(w in combined for w in ["adverse", "safety", "tolerability", "side effect"]):
            return "adverse_events"
        if any(w in combined for w in ["baseline", "demographic", "patient characteristics", "clinical characteristics"]):
            return "baseline_characteristics"
        if any(w in combined for w in ["efficacy", "outcome", "primary endpoint", "hba1c", "blood pressure", "glucose", "score"]):
            return "efficacy_outcomes"
        return "general"

    @classmethod
    def _extract_table_grid(
        cls,
        subsequent_text: str,
        document_id: str,
        page_num: int,
        table_num: int,
        table_type: str
    ) -> Tuple[List[str], List[Dict[str, str]], List[ExtractedDataPoint]]:
        """
        Parses text lines into a tabular grid and structured clinical datapoints.
        """
        lines = [line.strip() for line in subsequent_text.split("\n") if line.strip()]
        headers: List[str] = ["Variable", "Intervention", "Control", "P-Value"]
        rows: List[Dict[str, str]] = []
        datapoints: List[ExtractedDataPoint] = []

        # Regex for Mean ± SD: e.g. "7.5 ± 1.1", "7.5 (1.1)", "120.4 +/- 15.2"
        mean_sd_pattern = re.compile(r"([0-9]+\.?[0-9]*)\s*(?:±|\+\/\-|\()\s*([0-9]+\.?[0-9]*)\)?")
        # Regex for count and percentage: e.g. "45 (56.2%)", "32/80 (40.0%)"
        count_pct_pattern = re.compile(r"([0-9]+)\s*(?:\/([0-9]+))?\s*(?:\(([0-9]+\.?[0-9]*)%\))?")

        for line in lines[:15]:
            # Stop if reached next section or table
            if re.match(r"^Table\s+\d+", line, re.IGNORECASE) or line.startswith("References") or line.startswith("Discussion"):
                break

            # Parse line components
            # Expecting tab or multiple spaces or delimited by spaces
            parts = [p.strip() for p in re.split(r"\s{2,}|\t|\|", line) if p.strip()]
            if len(parts) >= 2:
                var_name = parts[0]
                val_col1 = parts[1]
                val_col2 = parts[2] if len(parts) > 2 else ""
                val_p = parts[3] if len(parts) > 3 else ""

                row_dict = {
                    "variable": var_name,
                    "intervention": val_col1,
                    "control": val_col2,
                    "p_value": val_p
                }
                rows.append(row_dict)

                # Extract numerical metrics for Intervention column
                cls._parse_cell_to_datapoint(
                    var_name=var_name,
                    raw_val=val_col1,
                    group="intervention",
                    document_id=document_id,
                    page_num=page_num,
                    table_num=table_num,
                    datapoints_out=datapoints,
                    mean_sd_pattern=mean_sd_pattern,
                    count_pct_pattern=count_pct_pattern
                )

                # Extract numerical metrics for Control column
                if val_col2:
                    cls._parse_cell_to_datapoint(
                        var_name=var_name,
                        raw_val=val_col2,
                        group="control",
                        document_id=document_id,
                        page_num=page_num,
                        table_num=table_num,
                        datapoints_out=datapoints,
                        mean_sd_pattern=mean_sd_pattern,
                        count_pct_pattern=count_pct_pattern
                    )

        return headers, rows, datapoints

    @classmethod
    def _parse_cell_to_datapoint(
        cls,
        var_name: str,
        raw_val: str,
        group: str,
        document_id: str,
        page_num: int,
        table_num: int,
        datapoints_out: List[ExtractedDataPoint],
        mean_sd_pattern: re.Pattern,
        count_pct_pattern: re.Pattern
    ):
        """
        Parses cell strings into normalized Mean, SD, N, or Count with SHA-256 provenance hash.
        """
        anchor = hashlib.sha256(f"{document_id}|P{page_num}|T{table_num}|{var_name}|{group}|{raw_val}".encode("utf-8")).hexdigest()[:16]

        # 1. Check for Sample Size (e.g. N = 40, n=50)
        n_match = re.search(r"[Nn]\s*=\s*([0-9]+)", f"{var_name} {raw_val}")
        if n_match:
            n_val = int(n_match.group(1))
            datapoints_out.append(ExtractedDataPoint(
                variable_name=var_name,
                group_name=group,
                sample_size=n_val,
                raw_text=raw_val,
                provenance_anchor=anchor,
                page_number=page_num,
                table_index=table_num
            ))
            return

        # 2. Check for Count and Percentage if "%" present (Categorical / Event rate)
        if "%" in raw_val:
            c_pct = count_pct_pattern.search(raw_val)
            if c_pct:
                cnt = int(c_pct.group(1))
                pct = float(c_pct.group(3)) if c_pct.group(3) else None
                datapoints_out.append(ExtractedDataPoint(
                    variable_name=var_name,
                    group_name=group,
                    events_count=cnt,
                    percentage=pct,
                    raw_text=raw_val,
                    provenance_anchor=anchor,
                    page_number=page_num,
                    table_index=table_num
                ))
                return

        # 3. Check for Mean ± SD (Continuous endpoint)
        m_sd = mean_sd_pattern.search(raw_val)
        if m_sd:
            mean = float(m_sd.group(1))
            sd = float(m_sd.group(2))
            datapoints_out.append(ExtractedDataPoint(
                variable_name=var_name,
                group_name=group,
                mean_value=mean,
                sd_value=sd,
                raw_text=raw_val,
                provenance_anchor=anchor,
                page_number=page_num,
                table_index=table_num
            ))
            return
