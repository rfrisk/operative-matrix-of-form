"""
Appendix B: Operative Matrix of Form (OMF) - Corpus Audit & Report Generator
Author: Ryan Pescatore Frisk
"""

import sys
import os
import pandas as pd
import numpy as np

BANDS = {
    1: "Historiographic & Epistemic Trajectories",
    2: "Domain, Context & Spatial Registers",
    3: "Elements of Spatial & Formal Articulation",
    4: "Relational Principles of Visual Organization",
    5: "Gestalt Configurations & Phenomenological Field",
    6: "Compositional Mechanics & Typographic Syntax",
    7: "Interactive Behaviors & Relational Affordances",
    8: "Ecosocial Substrates, Enclosure & Algorithmic Governance"
}

PHASES = {
    "1": "Classical Era to c. 1400 (Embodied Tectonics & Sacred Proportions)",
    "2": "c. 1400–1750 (Orthogonal Projection, Perspective & Architectural Orders)",
    "3": "c. 1750–1870s (Industrialization & Mechanical Standardization)",
    "4": "1873–1954 (Psychophysical Optics, Gestalt & Bauhaus Pedagogy)",
    "5": "1955–2000 (Swiss Systems, GUI Hardware Defaults & Postmodern Critique)",
    "6": "2000–Present (Algorithmic Culture, Real-Time Vision & Latent Enclosures)"
}

METADATA_IGNORE = {
    "id", "source_id", "author", "authors", "date", "year", 
    "title", "source", "publication", "notes", "phase", "era", "period", "epoch"
}
OMF_PREFIXES = ("E-", "P-", "G-", "C-", "R-", "I-", "M-", "S-", "D-", "DC", "DT")


def infer_phase_from_date(val):
    try:
        y = float(str(val).split("-")[0].replace("c.", "").strip())
        if y < 1400: return "1"
        elif y < 1750: return "2"
        elif y < 1873: return "3"
        elif y < 1955: return "4"
        elif y < 2000: return "5"
        else: return "6"
    except:
        return "Unknown"
        
def generate_html_report(df, analytical_cols, phase_counts, band_clusters, output_filename="omf_audit_report.html"):
    phase_rows = "".join(
        f"<tr><td><strong>Phase {p}</strong></td><td>{PHASES.get(str(p).strip(), 'Historical Period')}</td><td>{cnt}</td></tr>"
        for p, cnt in phase_counts.items()
    ) if phase_counts else "<tr><td colspan='3'>No Phase metadata column identified.</td></tr>"
    
    band_rows = "".join(
        f"<tr><td><strong>{bname}</strong></td><td>{len(cols)}</td><td><code>{', '.join(cols[:8])}{'...' if len(cols) > 8 else ''}</code></td></tr>"
        for bname, cols in band_clusters.items() if cols
    )

    # Clean preview table: replace NaN with em-dash
    clean_preview_df = df.iloc[:20].fillna("—")
    table_headers = "".join(f"<th>{c}</th>" for c in clean_preview_df.columns[:14])
    table_rows = ""
    for _, row in clean_preview_df.iterrows():
        cells = ""
        for c in clean_preview_df.columns[:14]:
            val = str(row[c]).strip()
            if val.lower() in ["nan", "none", "", "null"]:
                val = "—"
            cells += f"<td title='{val}'>{val[:25]}</td>"
        table_rows += f"<tr>{cells}</tr>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>OMF Benchmark Corpus Audit Report</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 30px; background: #fdfdfd; color: #212529; line-height: 1.5; }}
  h1 {{ font-size: 22px; margin-bottom: 4px; border-bottom: 2px solid #228be6; padding-bottom: 8px; }}
  h2 {{ font-size: 15px; margin-top: 24px; color: #495057; text-transform: uppercase; letter-spacing: 0.5px; }}
  .metric-badge {{ display: inline-block; background: #e7f5ff; color: #1971c2; padding: 6px 12px; border-radius: 6px; font-weight: bold; margin-right: 12px; margin-bottom: 16px; font-size: 13px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 20px; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
  th, td {{ border: 1px solid #dee2e6; padding: 6px 8px; text-align: left; }}
  th {{ background: #f1f3f5; font-weight: 600; color: #343a40; }}
  tr:nth-child(even) {{ background: #fafafa; }}
  code {{ background: #e9ecef; padding: 2px 4px; border-radius: 3px; font-size: 11px; }}
  .dense-preview {{ overflow-x: auto; white-space: nowrap; max-width: 100%; border: 1px solid #ced4da; }}
</style>
</head>
<body>
<h1>Operative Matrix of Form (OMF) — Corpus Audit Report</h1>
<div>
  <span class="metric-badge">Total Sources: {len(df)}</span>
  <span class="metric-badge">Operational Variables: {len(analytical_cols)} / 63</span>
  <span class="metric-badge">Historical Phases: {len(phase_counts)}</span>
</div>

<h2>1. Historical Distribution Across Epochs</h2>
<table>
  <thead><tr><th>Phase</th><th>Epoch Designation</th><th>Count</th></tr></thead>
  <tbody>{phase_rows}</tbody>
</table>

<h2>2. Thematic Band Variable Distribution</h2>
<table>
  <thead><tr><th>Band Category</th><th>Active Variables</th><th>Sample Coordinates</th></tr></thead>
  <tbody>{band_rows}</tbody>
</table>

<h2>3. Benchmark Corpus Snapshot (Sample Sources)</h2>
<div class="dense-preview">
  <table>
    <thead><tr>{table_headers}</tr></thead>
    <tbody>{table_rows}</tbody>
  </table>
</div>
<p style="font-size:11px; color:#868e96;">Generated automatically via OMF Audit Utility.</p>
</body>
</html>
"""
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated standalone HTML audit report: {output_filename}")


def audit_corpus(filepath):
    sep = "\t" if filepath.endswith((".tsv", ".tab")) else ","
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}. Please provide a valid CSV/TSV.")
        return

    df = pd.read_csv(filepath, sep=sep)
    print("=================================================================")
    print(" OPERATIVE MATRIX OF FORM (OMF) - CORPUS AUDIT")
    print(f" Source: {filepath} | Total Benchmark Entries: {len(df)}")
    print("=================================================================\n")

    # Flexible Phase Identification
    phase_col = None
    for c in df.columns:
        if c.strip().lower() in ["phase", "era", "period", "epoch"]:
            phase_col = c
            break

    if phase_col:
        phase_counts = df[phase_col].dropna().astype(str).str.strip().value_counts().sort_index().to_dict()
    else:
        # Fallback: check Date / Year column
        date_col = next((c for c in df.columns if c.strip().lower() in ["date", "year"]), None)
        if date_col:
            inferred = df[date_col].apply(infer_phase_from_date)
            phase_counts = inferred.value_counts().sort_index().to_dict()
        else:
            phase_counts = {}

    analytical_cols = [
        c for c in df.columns
        if c.startswith(OMF_PREFIXES) or (c.lower() not in METADATA_IGNORE and not c.startswith("Unnamed"))
    ]

    band_clusters = {
        "Band 2 (Context / Register: D-)": [c for c in analytical_cols if c.startswith(("D-", "Dc", "Dt"))],
        "Band 3 (Elements: E-)": [c for c in analytical_cols if c.startswith("E-")],
        "Band 4 (Principles: P-)": [c for c in analytical_cols if c.startswith("P-")],
        "Band 5 (Gestalt: G-)": [c for c in analytical_cols if c.startswith("G-")],
        "Band 6 (Composition: C-)": [c for c in analytical_cols if c.startswith("C-")],
        "Band 7 (Interaction / Relational: R-, I-)": [c for c in analytical_cols if c.startswith(("R-", "I-"))],
        "Band 8 (Ecosocial / Governance: M-, S-)": [c for c in analytical_cols if c.startswith(("M-", "S-"))],
    }

    generate_html_report(df, analytical_cols, phase_counts, band_clusters)
    return df


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "omf_benchmark_corpus.csv"
    audit_corpus(path)
