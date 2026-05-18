# VEHICLE-MADRE

**A Projection-Governed Framework for Sustainable Distributed AI Architecture**

[![DOI Theory](https://zenodo.org/badge/DOI/10.5281/zenodo.19807591.svg)](https://doi.org/10.5281/zenodo.19807591)
[![DOI Pyramid](https://zenodo.org/badge/DOI/10.5281/zenodo.19932124.svg)](https://doi.org/10.5281/zenodo.19932124)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Author:** Roberto Borda Milan  
**Institution:** VEHICLE Systems Lab / AIMTG — International Agency for Global Tension Measurement  
**ORCID:** [0009-0009-9047-1036](https://orcid.org/0009-0009-9047-1036)  
**Website:** [vehiclesystemslab.com](https://vehiclesystemslab.com)

---

## Overview

This repository contains the complete reproducibility package for the paper:

> **VEHICLE-MADRE: A Projection-Governed Framework for Sustainable Distributed AI Architecture**  
> Borda Milan, R. (2026). Working Draft v0.2. VEHICLE Systems Lab / AIMTG.

The paper argues that migrating 60–80% of AI inference interactions from centralized cloud 
architecture to locally-governed personal agents (the MADRE architecture) reduces:
- **Aggregate energy consumption per user by ~70%** (Wh/user/day)
- **Direct water footprint per user by ~70%** (mL/user/day)

...while maintaining functional equivalence (M1: local correct resolution ≥ 88.7%).

---

## Theoretical Foundations

This paper applies the VEHICLE framework to AI infrastructure sustainability. The formal basis is:

| Publication | DOI | Description |
|---|---|---|
| VEHICLE 3D with E.I.A.R.(V) | [10.5281/zenodo.19807591](https://doi.org/10.5281/zenodo.19807591) | Core formal framework |
| Borda Milan Pyramid v1.0 | [10.5281/zenodo.19932124](https://doi.org/10.5281/zenodo.19932124) | Architectural synthesis |
| Borda Milan Pyramid v1.1 | [10.5281/zenodo.19981738](https://doi.org/10.5281/zenodo.19981738) | Working draft (clean) |

---

## Repository Structure

```
vehicle-madre/
├── vehicle_madre/
│   ├── __init__.py          # Package exports
│   └── model.py             # Core quantitative model (MADREScenario, sensitivity_table)
├── notebooks/
│   └── reproducibility_notebook.py   # Reproduces all paper tables and claims
├── figures/
│   └── generate_figures.py  # Generates Figures 1–3 (requires matplotlib)
├── tests/
│   └── test_model.py        # Unit tests (pytest)
├── requirements.txt
└── README.md
```

---

## Quick Start

```bash
# Install dependencies
pip install numpy pandas matplotlib

# Reproduce all paper results
python notebooks/reproducibility_notebook.py

# Regenerate figures
python figures/generate_figures.py

# Run tests
pytest tests/
```

---

## Key Model Parameters

| Parameter | Value | Source |
|---|---|---|
| E_cloud (energy/cloud query) | 2.9 Wh | Brookings (2026) |
| E_local (energy/local query) | 0.01 Wh | Derived: 1.5W × 24s |
| WI (water intensity) | 3.69 L/kWh | Li et al. (2025) |
| M1 empirical floor | 88.7% | Wan et al. (2025) arXiv:2511.07885 |
| f_local central estimate | 70% | Sensitivity: 60–80% |

---

## Core Results (verified by `reproducibility_notebook.py`)

| Metric | Scenario A (Cloud-only) | Scenario B (MADRE Hybrid) | Reduction |
|---|---|---|---|
| Energy (Wh/user/day) | 58.0 | 17.5 | **−69.8%** |
| Water (mL/user/day) | 214.0 | 64.7 | **−69.8%** |
| VEHICLE attractor | A1 (rigid) | A4–A5 (governed) | — |
| T_total (normalized) | 2.000 | 0.679 | −66.1% |

All results are reproducible by running `notebooks/reproducibility_notebook.py`. 
Seven automated checks verify consistency between the model and the paper's claims.

---

## Citation

```bibtex
@misc{bordamilan2026vehiclemadre,
  author       = {Borda Milan, Roberto},
  title        = {{VEHICLE-MADRE}: A Projection-Governed Framework for 
                  Sustainable Distributed {AI} Architecture},
  year         = {2026},
  month        = {May},
  institution  = {VEHICLE Systems Lab / AIMTG},
  note         = {Working Draft v0.2. Pre-submission.},
  url          = {https://vehiclesystemslab.com}
}
```

**Cite the theoretical foundations:**
```bibtex
@misc{bordamilan2026vehicle3d,
  author = {Borda Milan, Roberto},
  title  = {{VEHICLE 3D} with {E.I.A.R.(V)}: A Projection-Governed Framework 
            for Self-Stabilizing Relational Networks},
  year   = {2026},
  doi    = {10.5281/zenodo.19807591},
}
```

---

## License

Code: [MIT License](LICENSE-CODE)  
Paper content and figures: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

*VEHICLE Systems Lab / AIMTG — International Agency for Global Tension Measurement*  
*vehiclesystemslab.com*
## Citation

Borda Milan, R. (2026). *VEHICLE-MADRE: A Projection-Governed Framework for Sustainable Distributed AI Architecture* (v0.4.2). Zenodo. https://doi.org/10.5281/zenodo.20263484

## DOI

https://doi.org/10.5281/zenodo.20263484
