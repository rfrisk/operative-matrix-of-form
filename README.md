# The Operative Matrix of Form (OMF)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dataset: CC BY 4.0](https://img.shields.io/badge/Dataset-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

> **Companion repository for the research study:**  
> *The Operative Matrix of Form: A Multi-dimensional Taxonomy of Materialization as Embodied Socio-Technical Extensions*  
> **Author:** Ryan Pescatore Frisk  
> For questions or bug reports regarding the matrix utilities, please open an issue in this repository.

---

## Overview

The **Operative Matrix of Form (OMF)** is an extensible, multi-layered data taxonomy designed to track the historical evolution of formal characteristics and spatial formatting from classical antiquity to contemporary automated systems. Moving beyond medium-specific histories that isolate analog craftsmanship from digital software engineering, this framework treats foundational design treatises, architectural canons, perceptual theories, and computational specifications as structured semiotic repositories.

The matrix parameterizes a benchmark corpus of **130 foundational sources** across **63 operational analytical variables** organized into eight thematic bands:

```
 Axis of Increasing Socio-Technical Complexity
  ▼
[Band 1] Historiographic & Epistemic Trajectories (Archival Metadata: Cols 1–6)
[Band 2] Domain, Context & Spatial Registers (Analytical Scope: Cols 7–17)
[Band 3] Elements of Spatial & Formal Articulation (Primitives: Cols 18–24)
[Band 4] Relational Principles of Visual Organization (Syntactic Rules: Cols 25–32)
[Band 5] Gestalt Configurations & Phenomenological Field (Grouping Laws: Cols 33–38)
[Band 6] Compositional Mechanics & Typographic Syntax (Lattices & Grids: Cols 39–46)
[Band 7] Interactive Behaviors & Relational Affordances (Topologies: Cols 47–55)
[Band 8] Ecosocial Substrates, Enclosure & Algorithmic Governance (Cols 56–69)
```

---

## Repository Structure

```text
├── omf_benchmark_corpus.csv     # Master benchmark corpus (130 sources × 69 columns)
├── omf_audit.py                 # Appendix B: Corpus verification and reporting utility
├── omf_switchboard.py           # Appendix C: Interactive browser switchboard generator
├── omf_audit_report.html        # Pre-compiled HTML audit distribution report
├── omf_switchboard.html         # Pre-compiled interactive micro-grid switchboard
├── LICENSE                      # Open-source license terms
└── README.md                    # Project documentation and quickstart guide
```

---

## Quickstart & Utilities

### Prerequisites
* Python 3.9+
* Required libraries:
  ```bash
  pip install pandas numpy
  ```

### 1. Corpus Verification & Audit Utility (`omf_audit.py`)
Validates structural integrity across historical phases, checks operational band variables, and compiles a comprehensive standalone HTML report:

```bash
python omf_audit.py omf_benchmark_corpus.csv
```
* **Output:** Generates `omf_audit_report.html`, summarizing historical phase distributions and active operational coordinates.

### 2. Interactive Matrix Switchboard (`omf_switchboard.py`)
Generates a zero-dependency, standalone HTML/JS web application that displays the complete 130-source corpus in an ultra-dense, micro-grid matrix:

```bash
python omf_switchboard.py omf_benchmark_corpus.csv
```
* **Output:** Generates `omf_switchboard.html`. Open the file in any modern web browser to:
  * **Inspect Coordinates:** Hover over any row or cell to view citation metadata and precise `(Row, Column)` coordinate values.
  * **Trace Diagnostic Lineages:** Click preset assemblies (e.g., Alberti → Dürer → Müller-Brockmann → Latent Diffusion Tensors) with a two-tier visual overlay (primary narrative exemplars vs. incidental corpus connections).
  * **Free Exploration Mode:** Click across any combination of sources and parameters to dynamically log and audit custom multi-node lineages in real time.

---

## Analytical Modalities

1. **Diagnostic Nodal Assemblies:** Synchronic, cross-band query clusters that isolate how formal primitives, compositional rules, and institutional contexts assemble into immediate mechanisms (e.g., computer vision edge segmentation, generative diffusion engines).
2. **Longitudinal Trajectories:** Diachronic threads tracking single formal mechanisms (such as the orthogonal grid or spatial framing) across shifting media substrates.
3. **Macro-Structural Audits:** Aggregate cross-tabulations auditing systemic tensions, including vernacular cosmopolitanism versus corporate enclosure and the ideological disavowal of physical material costs.

---

## Citation

If you utilize the Operative Matrix of Form taxonomy, benchmark dataset, or computational switchboard in your research, please cite:

```bibtex
@article{frisk2026operative,
  title={The Operative Matrix of Form: A Multi-dimensional Taxonomy of Materialization as Embodied Socio-Technical Extensions},
  author={Frisk, Ryan Pescatore},
  journal={Art \& Perception},
  year={2026},
  note={Under review}
}
```

## License
* Software & Scripts: [MIT License](LICENSE)
* Dataset & Codebooks: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
