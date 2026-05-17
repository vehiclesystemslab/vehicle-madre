"""
vehicle_madre
=============
Quantitative model package for:
  VEHICLE-MADRE: A Projection-Governed Framework for
  Sustainable Distributed AI Architecture

  Borda Milan, R. (2026). Working Draft v0.2.

Theoretical foundations:
  DOI: 10.5281/zenodo.19807591
  DOI: 10.5281/zenodo.19932124
  DOI: 10.5281/zenodo.19981738
"""

from .model import (
    MADREScenario,
    sensitivity_table,
    reduction_pct,
    SCENARIO_A,
    SCENARIO_B,
    SCENARIO_B_LOW,
    SCENARIO_B_HIGH,
    SCENARIO_C,
    E_CLOUD_WH,
    E_LOCAL_WH,
    WI_GLOBAL_L_PER_KWH,
    WATER_INTENSITY_REGIONAL,
    M1_EMPIRICAL_FLOOR,
    ATTRACTOR_LABELS,
)

__version__ = "0.2.0"
__author__ = "Roberto Borda Milan — VEHICLE Systems Lab / AIMTG"
__doi_theory__ = [
    "10.5281/zenodo.19807591",
    "10.5281/zenodo.19932124",
    "10.5281/zenodo.19981738",
]

__all__ = [
    "MADREScenario",
    "sensitivity_table",
    "reduction_pct",
    "SCENARIO_A", "SCENARIO_B", "SCENARIO_B_LOW", "SCENARIO_B_HIGH", "SCENARIO_C",
    "E_CLOUD_WH", "E_LOCAL_WH", "WI_GLOBAL_L_PER_KWH",
    "WATER_INTENSITY_REGIONAL", "M1_EMPIRICAL_FLOOR", "ATTRACTOR_LABELS",
]
