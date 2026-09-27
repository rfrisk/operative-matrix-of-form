"""
Appendix C: Interactive Full-Corpus Diagnostic Switchboard Generator
Author: Ryan Pescatore Frisk
"""

import sys
import os
import json
import pandas as pd

def build_switchboard(csv_path="omf_benchmark_corpus.csv", output_html="omf_switchboard.html"):
    sep = "\t" if csv_path.endswith((".tsv", ".tab")) else ","
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, sep=sep).fillna("")
    else:
        cols = ["ID", "Author", "Date", "Title", "Phase", "C-Grid", "C-Modular", "G-Proximity", "I-Detachment", "P-Contrast", "M-AI_Network_Bias"]
        df = pd.DataFrame([
            {"ID": f"SRC-{i:03d}", "Author": f"Author {i}", "Date": 1500 + (i*4), "Title": f"Treatise Volume {i}", "Phase": (i % 6) + 1, "C-Grid": "1" if i % 2 == 0 else "", "C-Modular": "x" if i % 3 == 0 else "", "G-Proximity": "1" if i % 4 == 0 else "", "I-Detachment": "x" if i % 5 == 0 else "", "P-Contrast": "1" if i % 6 == 0 else "", "M-AI_Network_Bias": "1" if i > 115 else ""}
            for i in range(1, 131)
        ])

    columns = list(df.columns)
    records = df.to_dict(orient="records")

    meta_cols = [c for c in columns if c.lower() in ["id", "source_id", "author", "authors", "date", "year", "title", "phase", "era"]]
    param_cols = [c for c in columns if c not in meta_cols]

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Operative Matrix of Form — Diagnostic Switchboard</title>
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ height: 100%; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; padding: 10px 14px; background: #101216; color: #c9d1d9; font-size: 11px; }}
  
  .container {{ display: flex; flex-direction: column; height: calc(100vh - 20px); gap: 10px; }}
  
  /* UPPER SECTION: Matrix grid */
  .grid-viewport {{ flex: 1 1 auto; overflow: auto; border: 1px solid #282c34; background: #16181d; position: relative; border-radius: 4px; min-height: 220px; }}
  table {{ border-collapse: separate; border-spacing: 1px; background: #1e2228; table-layout: fixed; }}
  
  th {{ position: sticky; top: 0; background: #16181d; color: #8b949e; padding: 4px 2px; font-weight: 600; border-bottom: 2px solid #282c34; z-index: 50; font-size: 9px; vertical-align: bottom; }}
  th.meta-th {{ width: 90px; min-width: 70px; text-align: left; padding: 4px 6px; vertical-align: middle; }}
  th.param-th {{ width: 22px; min-width: 22px; max-width: 22px; height: 115px; padding: 2px; white-space: nowrap; }}
  th.param-th div {{ writing-mode: vertical-rl; transform: rotate(180deg); text-align: left; max-height: 110px; overflow: hidden; text-overflow: ellipsis; }}
  
  /* Compact row & cell styling */
  tr {{ height: 15px; max-height: 15px; }}
  tr.selected-row td.meta-td {{ background: #1f6feb !important; color: #fff !important; font-weight: bold; }}
  tr.selected-row td.param-td.active-val {{ font-size: 11px; font-weight: bold; color: #79c0ff; }}
  tr:hover td.meta-td {{ background: #262c36; color: #f0f6fc; }}
  
  td {{ padding: 0; text-align: center; position: relative !important; height: 15px; max-height: 15px; line-height: 14px; overflow: visible; }}
  td.meta-td {{ background: #101216; color: #8b949e; padding: 1px 5px; text-align: left; font-size: 9.5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100px; cursor: pointer; }}
  td.param-td {{ width: 22px; min-width: 22px; max-width: 22px; background: #101216; cursor: crosshair; font-size: 9.5px; font-family: monospace; color: #5a626e; }}
  td.param-td.active-val {{ color: #adb5bd; background: #181b20; }}
  td.param-td:hover {{ background: #262c36; color: #fff; }}
  
  /* 1. PRIMARY NARRATIVE OVERLAY: Big, Vibrant, 18px Pulsing Dot */
  .node-overlay-primary {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 18px;
    height: 18px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 60;
    box-shadow: 0 0 10px currentColor;
    opacity: 0.95;
    animation: primaryPulse 1.4s infinite ease-in-out;
  }}
  @keyframes primaryPulse {{
    0% {{ transform: translate(-50%, -50%) scale(0.9); opacity: 0.85; }}
    50% {{ transform: translate(-50%, -50%) scale(1.35); opacity: 1; }}
    100% {{ transform: translate(-50%, -50%) scale(0.9); opacity: 0.85; }}
  }}

  /* 2. INCIDENTAL CORPUS OVERLAY: 9px Muted Dot */
  .node-overlay-incidental {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 9px;
    height: 9px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 25;
    opacity: 0.65;
    box-shadow: 0 0 3px rgba(0,0,0,0.8);
  }}

  /* 3. FREE CUSTOM PIN: 16px Electric Cyan */
  .node-overlay-custom {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #00f2fe;
    color: #00f2fe;
    box-shadow: 0 0 12px #00f2fe;
    pointer-events: none;
    z-index: 70;
    animation: customPulse 1.2s infinite ease-in-out;
  }}
  @keyframes customPulse {{
    0% {{ transform: translate(-50%, -50%) scale(0.85); opacity: 0.9; }}
    50% {{ transform: translate(-50%, -50%) scale(1.3); opacity: 1; }}
    100% {{ transform: translate(-50%, -50%) scale(0.85); opacity: 0.9; }}
  }}
  
  /* Instant Cursor Tooltip */
  #cursorTooltip {{
    position: fixed;
    display: none;
    pointer-events: none;
    z-index: 1000;
    background: #161b22;
    border: 1px solid #388bfd;
    color: #f0f6fc;
    padding: 6px 10px;
    border-radius: 4px;
    font-size: 11px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.6);
    white-space: nowrap;
    transform: translate(12px, 12px);
  }}
  
  /* LOWER SECTION */
  .control-deck {{ flex: 0 0 auto; display: grid; grid-template-columns: 290px 1fr; gap: 12px; background: #16181d; border: 1px solid #282c34; border-radius: 4px; padding: 12px 14px; min-height: 230px; }}
  .btn-group {{ display: flex; flex-direction: column; gap: 4px; overflow-y: auto; max-height: 270px; }}
  .deck-btn {{ background: #1e2228; color: #c9d1d9; border: 1px solid #282c34; border-radius: 3px; padding: 6px 9px; text-align: left; cursor: pointer; font-size: 11px; font-weight: 500; transition: all 0.15s; }}
  .deck-btn:hover {{ background: #262c36; border-color: #58a6ff; }}
  .deck-btn.active {{ background: #1f6feb; border-color: #58a6ff; color: #fff; font-weight: bold; }}
  .deck-btn.clear-btn {{ background: #2b181c; border-color: #f85149; color: #ff7b72; margin-top: 4px; text-align: center; }}
  .deck-btn.clear-btn:hover {{ background: #da3633; color: #fff; }}
  
  .readout-panel {{ background: #101216; border: 1px solid #282c34; border-radius: 3px; padding: 12px 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 7px; max-height: 270px; }}
  
  /* Inspection & Status Banner: Left-Aligned Grouping */
  .inspection-banner {{ background: #1a202c; border: 1px solid #3182ce; border-radius: 4px; padding: 6px 10px; font-size: 11.5px; color: #e2e8f0; display: flex; align-items: center; gap: 10px; min-height: 28px; }}
  .source-inspect {{ font-size: 11.5px; color: #63b3ed; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 65%; }}
  .highlight-badge {{ font-size: 11px; color: #ecc94b; background: rgba(236, 201, 75, 0.15); padding: 2px 7px; border-radius: 3px; border: 1px solid rgba(236, 201, 75, 0.35); font-weight: 600; white-space: nowrap; }}
  
  .readout-title {{ font-size: 13.5px; font-weight: bold; color: #58a6ff; margin-top: 2px; }}
  .readout-lineage {{ font-size: 12px; font-weight: 600; color: #e6edf3; background: #16181d; border-left: 3px solid #58a6ff; padding: 4px 8px; border-radius: 2px; }}
  .readout-path {{ font-size: 11px; color: #79c0ff; font-family: monospace; }}
  .diagnostic-body {{ font-size: 12px; line-height: 1.6; color: #d0d7de; }}
  .coord-tags {{ margin-top: 2px; display: flex; flex-wrap: wrap; gap: 4px; }}
  .coord-pill {{ display: inline-block; background: #1e2228; border: 1px solid #30363d; color: #79c0ff; padding: 2px 6px; border-radius: 3px; font-family: monospace; font-size: 10.5px; }}
  
  .custom-chain-box {{ margin-top: 4px; padding: 6px 8px; background: #161b22; border: 1px dashed #388bfd; border-radius: 3px; font-size: 11px; color: #58a6ff; }}
  .custom-chain-list {{ display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }}
  .custom-pill {{ background: rgba(0, 242, 254, 0.15); border: 1px solid #00f2fe; color: #00f2fe; padding: 2px 6px; border-radius: 3px; font-family: monospace; font-size: 10px; }}
</style>
</head>
<body>

<div id="cursorTooltip"></div>

<div class="container">
  <!-- UPPER SECTION: Matrix grid -->
  <div class="grid-viewport" id="viewport">
    <table id="matrixTable">
      <thead>
        <tr>
          {"".join(f'<th class="meta-th" title="{c}">{c}</th>' for c in meta_cols)}
          {"".join(f'<th class="param-th" title="{c}"><div>{c}</div></th>' for c in param_cols)}
        </tr>
      </thead>
      <tbody>
        {"".join(
          f'<tr data-row="{idx}" onclick="handleRowClick({idx}, event)">' +
          "".join(
            f'<td class="meta-td" title="{str(row[c])}" '
            f'onmouseenter="inspectMeta({idx}, \'{c}\', \'{str(row[c])}\', event)" '
            f'onmousemove="moveTip(event)" '
            f'onmouseleave="hideTip()">{str(row[c])}</td>' 
            for c in meta_cols
          ) +
          "".join(
            (lambda val, sval: 
              f'<td class="param-td {("active-val" if sval not in ["", "0", "0.0", "nan", "none", "—", "-"] else "")}" '
              f'data-col="{c.strip()}" data-col-clean="{c.strip().upper().replace(" ", "").replace("_", "").replace("-", "")}" data-row="{idx}" data-val="{sval}" '
              f'onmouseenter="inspectNode({idx}, \'{c}\', \'{sval}\', event)" '
              f'onmousemove="moveTip(event)" '
              f'onmouseleave="hideTip()" '
              f'onclick="handleNodeClick({idx}, \'{c}\', \'{sval}\', event)">'
              f'{("×" if sval not in ["", "0", "0.0", "nan", "none", "—", "-"] else "")}</td>'
            )(row[c], str(row[c]).strip())
            for c in param_cols
          ) + '</tr>'
          for idx, row in enumerate(records)
        )}
      </tbody>
    </table>
  </div>

  <!-- LOWER SECTION: Interactive Diagnostics -->
  <div class="control-deck">
    <div class="btn-group">
      <div style="font-weight:bold; color:#8b949e; margin-bottom:4px; font-size:10.5px; text-transform:uppercase;">Diagnostic Assemblies & Trajectories:</div>
      <button class="deck-btn active" id="btn-0" onclick="activateTrace(0)">Assembly 1: Canonical Substrate</button>
      <button class="deck-btn" id="btn-1" onclick="activateTrace(1)">Assembly 2: Vernacular vs. Diffusion</button>
      <button class="deck-btn" id="btn-2" onclick="activateTrace(2)">Assembly 3: Post-War Systematization</button>
      <button class="deck-btn" id="btn-3" onclick="activateTrace(3)">Assembly 4: Embodying Screen Enclosure</button>
      <button class="deck-btn" id="btn-4" onclick="activateTrace(4)">Trajectory A: Euclidean Snapping</button>
      <button class="deck-btn" id="btn-5" onclick="activateTrace(5)">Trajectory B: Typographic Enclosure</button>
      <button class="deck-btn" id="btn-6" onclick="activateTrace(6)">Free Exploration Mode</button>
      <button class="deck-btn clear-btn" onclick="clearCustomTrace()">Clear Custom Selection</button>
    </div>

    <div class="readout-panel">
      <div class="inspection-banner">
        <div class="source-inspect" id="bannerSource">Selected: Row 0 | Dürer, A. (1525)</div>
        <div class="highlight-badge" id="bannerBadge">0 Exemplar | 0 Corpus Nodes</div>
      </div>

      <div class="readout-title" id="rTitle">Assembly 1: The Canonical Substrate (1450–1550)</div>
      <div class="readout-lineage" id="rLineage">Alberti (1435) → Dürer (1525) → Kandinsky (1926) → Real-Time Semantic Edge Segmentation.</div>
      <div class="readout-path" id="rPath">Active Matrix Path: Band 3 (E-Line, E-Shape), Band 4 (P-Proportion, P-Scale), Band 6 (C-Grid, C-Modular), Band 8 (M-Media).</div>
      <div class="coord-tags" id="rCoords"></div>
      <div class="diagnostic-body" id="rBody">Select a diagnostic assembly or click any cell above to inspect.</div>
      
      <div class="custom-chain-box" id="customChainContainer" style="display:none;">
        <strong>Custom Audit Selection Chain:</strong>
        <div class="custom-chain-list" id="customChainList"></div>
      </div>
    </div>
  </div>
</div>

<script>
const profiles = [
  {{
    title: "Assembly 1: The Canonical Substrate (1450–1550)",
    lineage: "Alberti (1435) → Dürer (1525) → Kandinsky (1926) → Real-Time Semantic Edge Segmentation.",
    path: "Active Matrix Path: Band 3 (E-Line, E-Shape), Band 4 (P-Proportion, P-Scale), Band 6 (C-Grid, C-Modular), Band 8 (M-Media).",
    coords: ["C-Grid", "C-Modular", "P-Contrast", "E-Direction", "P-Scale", "C-Symmetry"],
    authorKeywords: ["Dürer", "Alberti", "Pacioli", "Piero", "Kandinsky"],
    color: "#ff6b6b",
    desc: "Exposes the geometric codification established by Renaissance perspective systems, demonstrating how orthogonal woodcut matrices laid the mathematical substrate for bounding boxes and spatial discretization in computer vision models."
  }},
  {{
    title: "Assembly 2: Vernacular Density vs. Generative Diffusion",
    lineage: "Polykleitos (c. 440 BCE) / Alberti (1435) vs. Vernacular Signage Traditions → Generative Diffusion Models.",
    path: "Active Matrix Path: Band 5 (G-Proximity, G-Similarity), Band 7 (I-Detachment, I-Touching), Band 8 (M-AI_Network_Bias, M-Vernacular_Cosmo).",
    coords: ["I-Detachment", "M-AI_Network_Bias", "G-Proximity", "E-Space", "M-Vernacular_Cosmo"],
    authorKeywords: ["Diffusion", "OpenAI", "Midjourney", "Stability", "Scollon", "Pauwels"],
    color: "#339af0",
    desc: "Diagnoses how contemporary diffusion engines systematically smooth out the layered, tactile friction of vernacular urban signage, enforcing normalized Western aesthetic symmetry and commercial detachment defaults."
  }},
  {{
    title: "Assembly 3: Post-War Systematization & Structural Semiotics",
    lineage: "Barthes (1957) → Müller-Brockmann (1961/81) → Kress & van Leeuwen (1996) → Apple Computer Inc. (1987/1991).",
    path: "Active Matrix Path: Band 4 (P-Unity, P-Rhythm), Band 6 (C-Grid, C-Hierarchy), Band 7 (R-Frame, I-Detachment), Band 8 (M-Power).",
    coords: ["C-Grid", "C-Hierarchy", "I-Detachment", "R-Frame", "P-Unity"],
    authorKeywords: ["Müller-Brockmann", "Ruder", "Barthes", "Kress", "Apple"],
    color: "#51cf66",
    desc: "Highlights post-war Swiss graphic systems, exposing how corporate identity manuals and objective institutional layout grids prefigured the strict containment hierarchies of graphical user interfaces."
  }},
  {{
    title: "Assembly 4: Embodying Screen Enclosure & GUI Touchscreens",
    lineage: "Vischer (1873) / Hildebrand (1893) → Schlemmer & Bauhaus (1925) → Touchscreen Interfaces (Apple Computer Inc., 1991).",
    path: "Active Matrix Path: Band 3 (E-Space), Band 7 (I-Touching, I-Detachment, R-Frame), Band 8 (P-Haptic, M-Media, M-Enclosure).",
    coords: ["I-Detachment", "R-Frame", "M-Media", "P-Haptic"],
    authorKeywords: ["Vischer", "Hildebrand", "Schlemmer", "Gibson", "Noë"],
    color: "#fcc419",
    desc: "Traces the transformation of phenomenological motor habits and physical empathy into commodified, enclosed gestures (tapping, swiping, pinch-to-zoom) bounded by glass screen surfaces."
  }},
  {{
    title: "Trajectory A: The Euclidean Snapping Lineage",
    lineage: "Alberti (1435) → Dürer (1525) → Müller-Brockmann (1961/81) → Apple HIG (1987) → Latent Diffusion Tensors.",
    path: "Active Matrix Path: Band 6 (C-Grid, C-Modular, C-Symmetry) across diachronic media substrates.",
    coords: ["C-Grid", "C-Modular", "C-Symmetry"],
    authorKeywords: ["Alberti", "Dürer", "Müller-Brockmann", "Apple"],
    color: "#ff6b6b",
    desc: "Traces the uninterrupted 500-year historical trajectory of orthogonal planar snapping, tracking how physical framing tools became structural algorithmic rules in modern software."
  }},
  {{
    title: "Trajectory B: Typographic Enclosure Lineage",
    lineage: "Movable Metal Type Matrices (1450) → Phototypesetting (1950) → PostScript (1984) → CSS Flexbox & Web Layout.",
    path: "Active Matrix Path: Band 6 (C-Hierarchy), Band 7 (I-Detachment), Band 8 (M-Media).",
    coords: ["C-Hierarchy", "I-Detachment", "M-Media"],
    authorKeywords: ["Tschichold", "Ruder", "Müller-Brockmann", "Bringhurst"],
    color: "#cc5de8",
    desc: "Exposes how mechanical physical spacing (metal slugs, furniture, leading) became formalized into mathematical bounding boxes and automated responsive layout algorithms."
  }}
];

const recordsData = {json.dumps(records)};
const tooltip = document.getElementById("cursorTooltip");
let selectedCustomNodes = [];
let currentActiveAssembly = 0;

function cleanName(str) {{
  return (str || "").toUpperCase().replace(/[\\s_\\-]/g, "");
}}

function getRowMeta(rowIdx) {{
  const row = recordsData[rowIdx] || {{}};
  let author = "";
  let date = "";
  let title = "";
  let phase = "";

  for (const k of Object.keys(row)) {{
    const kl = k.toLowerCase().trim();
    if (kl.includes("author")) author = author || row[k];
    else if (kl.includes("date") || kl.includes("year")) date = date || row[k];
    else if (kl.includes("title") || kl.includes("source") || kl.includes("treatise")) title = title || row[k];
    else if (kl.includes("phase") || kl.includes("era")) phase = phase || row[k];
  }}
  return {{
    author: author || "Source " + rowIdx,
    date: date || "",
    title: title || "",
    phase: phase || ""
  }};
}}

function inspectMeta(rowIdx, field, val, e) {{
  const m = getRowMeta(rowIdx);
  const dateStr = m.date ? ` (${{m.date}})` : "";
  const titleStr = m.title ? ` — "${{m.title}}"` : "";
  const phaseStr = m.phase ? ` [Phase ${{m.phase}}]` : "";

  document.getElementById("bannerSource").innerText = `Row ${{rowIdx}}: ${{m.author}}${{dateStr}}${{titleStr}}${{phaseStr}}`;
  document.getElementById("bannerBadge").innerText = `${{field}}: "${{val}}"`;

  tooltip.style.display = "block";
  tooltip.innerHTML = `<strong>${{m.author}}${{dateStr}}</strong><br>${{m.title}}<br><span style="color:#58a6ff;">${{field}}: ${{val}}</span>`;
  moveTip(e);
}}

function inspectNode(rowIdx, colName, val, e) {{
  const m = getRowMeta(rowIdx);
  const cleanVal = (val || "").trim() || "—";
  const dateStr = m.date ? ` (${{m.date}})` : "";
  const titleStr = m.title ? ` — "${{m.title}}"` : "";

  document.getElementById("bannerSource").innerText = `Row ${{rowIdx}}: ${{m.author}}${{dateStr}}${{titleStr}}`;
  document.getElementById("bannerBadge").innerText = `${{colName}}: "${{cleanVal}}"`;

  tooltip.style.display = "block";
  tooltip.innerHTML = `<strong>${{m.author}}${{dateStr}}</strong><br>${{m.title}}<br><span style="color:#79c0ff;">${{colName}}: <code>${{cleanVal}}</code></span>`;
  moveTip(e);
}}

function moveTip(e) {{
  if (!e) return;
  tooltip.style.left = (e.clientX + 14) + "px";
  tooltip.style.top = (e.clientY + 14) + "px";
}}

function hideTip() {{
  tooltip.style.display = "none";
}}

function highlightRowUI(rowIdx) {{
  document.querySelectorAll("tr").forEach(r => r.classList.remove("selected-row"));
  const tr = document.querySelector(`tr[data-row='${{rowIdx}}']`);
  if (tr) tr.classList.add("selected-row");

  const m = getRowMeta(rowIdx);
  const dateStr = m.date ? ` (${{m.date}})` : "";
  const titleStr = m.title ? ` — "${{m.title}}"` : "";
  document.getElementById("bannerSource").innerText = `Row ${{rowIdx}}: ${{m.author}}${{dateStr}}${{titleStr}}`;
}}

function handleRowClick(rowIdx, e) {{
  if (currentActiveAssembly !== 6) {{
    activateTrace(6);
  }}
  highlightRowUI(rowIdx);
}}

function handleNodeClick(rowIdx, colName, val, e) {{
  if (e) e.stopPropagation();
  
  if (currentActiveAssembly !== 6) {{
    activateTrace(6);
  }}
  
  highlightRowUI(rowIdx);
  const m = getRowMeta(rowIdx);
  const td = e ? e.currentTarget : document.querySelector(`td[data-row='${{rowIdx}}'][data-col='${{colName}}']`);
  const cleanVal = (val || "").trim() || "1";

  const existingIdx = selectedCustomNodes.findIndex(n => n.row === rowIdx && n.col === colName);
  if (existingIdx >= 0) {{
    selectedCustomNodes.splice(existingIdx, 1);
    if (td) {{
      const existingMarker = td.querySelector(".node-overlay-custom");
      if (existingMarker) existingMarker.remove();
    }}
  }} else {{
    selectedCustomNodes.push({{
      row: rowIdx,
      author: m.author,
      date: m.date,
      col: colName,
      val: cleanVal
    }});

    if (td) {{
      const marker = document.createElement("div");
      marker.className = "node-overlay-custom";
      td.appendChild(marker);
    }}
  }}

  updateCustomReadout();
}}

function updateCustomReadout() {{
  const container = document.getElementById("customChainContainer");
  const list = document.getElementById("customChainList");

  if (selectedCustomNodes.length === 0) {{
    container.style.display = "none";
    document.getElementById("bannerBadge").innerText = "Free Audit Ready";
    return;
  }}

  container.style.display = "block";
  document.getElementById("bannerBadge").innerText = `${{selectedCustomNodes.length}} Custom Nodes Selected`;
  list.innerHTML = selectedCustomNodes.map(n => 
    `<span class="custom-pill">Row ${{n.row}} (${{n.author}} ${{n.date ? "'" + n.date.toString().slice(-2) : ""}}) → ${{n.col}}</span>`
  ).join("");
}}

function clearCustomTrace() {{
  selectedCustomNodes = [];
  document.querySelectorAll(".node-overlay-custom").forEach(m => m.remove());
  updateCustomReadout();
}}

function activateTrace(idx) {{
  hideTip();
  currentActiveAssembly = idx;
  
  const btns = document.querySelectorAll(".deck-btn");
  btns.forEach((b, i) => b.classList.toggle("active", i === idx));
  
  document.querySelectorAll(".node-overlay-primary, .node-overlay-incidental").forEach(m => m.remove());

  if (idx === 6) {{
    document.getElementById("rTitle").innerText = "Free Matrix Exploration Mode";
    document.getElementById("rLineage").innerText = "Preset lineages cleared. Click on any row or parameter to create a custom trajectory.";
    document.getElementById("rPath").innerText = "Interactive Custom Mode: Click cells across rows to trace custom multi-author lineages.";
    document.getElementById("rCoords").innerHTML = "";
    document.getElementById("rBody").innerText = "Every parameter cell you click places an electric-cyan marker and appends that node to the custom lineage sequence below.";
    updateCustomReadout();
    return;
  }}

  clearCustomTrace();

  const p = profiles[idx];
  document.getElementById("rTitle").innerText = p.title;
  document.getElementById("rLineage").innerText = p.lineage;
  document.getElementById("rPath").innerText = p.path;
  document.getElementById("rCoords").innerHTML = p.coords.map(c => `<span class="coord-pill" style="color:${{p.color}}">${{c}}</span>`).join("");
  document.getElementById("rBody").innerText = p.desc;

  const exemplarRowIndices = [];
  recordsData.forEach((row, rIdx) => {{
    const authorVal = (row.Author || row.author || "").toLowerCase();
    const titleVal = (row.Title || row.title || "").toLowerCase();
    if (p.authorKeywords.some(kw => authorVal.includes(kw.toLowerCase()) || titleVal.includes(kw.toLowerCase()))) {{
      exemplarRowIndices.push(rIdx);
    }}
  }});

  if (exemplarRowIndices.length === 0) {{
    const fallback = [idx * 15, idx * 15 + 1, idx * 15 + 2];
    fallback.forEach(fr => {{ if (fr < recordsData.length) exemplarRowIndices.push(fr); }});
  }}

  const targetCleans = p.coords.map(cleanName);
  let primaryCount = 0;
  let incidentalCount = 0;

  document.querySelectorAll("td.param-td.active-val").forEach(td => {{
    const colClean = td.getAttribute("data-col-clean");
    const isCoordMatch = targetCleans.some(tc => colClean === tc || colClean.includes(tc) || tc.includes(colClean));
    
    if (isCoordMatch) {{
      const rIdx = parseInt(td.getAttribute("data-row"), 10);
      const isExemplar = exemplarRowIndices.includes(rIdx);

      const marker = document.createElement("div");
      if (isExemplar) {{
        marker.className = "node-overlay-primary";
        marker.style.color = p.color;
        marker.style.backgroundColor = p.color;
        primaryCount++;
      }} else {{
        marker.className = "node-overlay-incidental";
        marker.style.backgroundColor = p.color;
        incidentalCount++;
      }}
      td.appendChild(marker);
    }}
  }});

  document.getElementById("bannerBadge").innerText = `${{primaryCount}} Exemplar | ${{incidentalCount}} Corpus Nodes`;

  if (exemplarRowIndices.length > 0) {{
    highlightRowUI(exemplarRowIndices[0]);
  }}

  setTimeout(() => {{
    const firstPrimary = document.querySelector(".node-overlay-primary");
    const viewport = document.getElementById("viewport");
    if (firstPrimary && viewport) {{
      const cell = firstPrimary.closest("td");
      if (cell) {{
        const cellRect = cell.getBoundingClientRect();
        const vRect = viewport.getBoundingClientRect();
        
        viewport.scrollTo({{
          left: viewport.scrollLeft + (cellRect.left - vRect.left) - (vRect.width / 2) + (cellRect.width / 2),
          top: viewport.scrollTop + (cellRect.top - vRect.top) - (vRect.height / 2) + (cellRect.height / 2),
          behavior: "smooth"
        }});
      }}
    }}
  }}, 60);
}}

window.addEventListener("DOMContentLoaded", () => {{
  activateTrace(0);
}});
</script>
</body>
</html>
"""
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully generated updated switchboard: {output_html}")


if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "omf_benchmark_corpus.csv"
    build_switchboard(csv_file)
