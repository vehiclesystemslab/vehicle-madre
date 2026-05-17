"""
vehicle_madre.model
===================
Core quantitative model for the VEHICLE-MADRE paper.

Reproduces all numerical results in:
  Borda Milan, R. (2026). VEHICLE-MADRE: A Projection-Governed Framework
  for Sustainable Distributed AI Architecture. Working Draft v0.2.

Theoretical basis:
  Borda Milan, R. (2026a). DOI: 10.5281/zenodo.19807591
  Borda Milan, R. (2026b). DOI: 10.5281/zenodo.19932124
  Borda Milan, R. (2026c). DOI: 10.5281/zenodo.19981738
"""

from dataclasses import dataclass, field
from typing import Optional
import numpy as np


# ── Empirical constants (cited in paper §5) ───────────────────────────────

#: Energy per cloud inference query (Wh). Source: Brookings (2026).
E_CLOUD_WH: float = 2.9

#: Energy per local inference query (Wh).
#: Derived: P_device(1.5 W) × t_query(24 s) = 0.01 Wh. Source: §5.2.
E_LOCAL_WH: float = 0.01

#: Water intensity factor (L/kWh, combined on-site + indirect).
#: Source: Li et al. (2025). Communications of the ACM 68(7).
WI_GLOBAL_L_PER_KWH: float = 3.69

#: Regional water intensity factors (L/kWh). Source: Appendix A.
WATER_INTENSITY_REGIONAL = {
    "global_average": 3.69,
    "nordic":         0.50,
    "us_average":     2.80,
    "arid":           8.50,   # Arizona / Nevada / Singapore
    "southeast_asia": 5.00,
}

#: Local model correct resolution rate empirical floor.
#: Source: Wan et al. (2025). arXiv:2511.07885.
M1_EMPIRICAL_FLOOR: float = 0.887

#: Attractor labels (VEHICLE taxonomy A0–A6, applied to AI infrastructure).
#: Source: Borda Milan (2026a), §5; extended in this paper §3.1.
ATTRACTOR_LABELS = {
    "A0": "Pre-digital baseline",
    "A1": "Cloud-centralized rigid (Scenario A)",
    "A2": "Cloud with optimized PUE",
    "A3": "Hybrid cloud, no formal governance",
    "A4": "MADRE hybrid governed (Scenario B, early)",
    "A5": "MADRE mature with federated learning (Scenario B, mature)",
    "A6": "Distributed renewable stable fluid (Scenario C)",
}


@dataclass
class MADREScenario:
    """
    Represents one deployment scenario as a VEHICLE attractor regime.

    Parameters
    ----------
    name : str
        Human-readable scenario name.
    attractor : str
        VEHICLE attractor label (A0–A6).
    f_local : float
        Fraction of inference queries resolved locally (0.0–1.0).
    queries_per_day : float
        Mean queries per user per day.
    e_cloud : float
        Energy per cloud inference query (Wh). Default: E_CLOUD_WH.
    e_local : float
        Energy per local inference query (Wh). Default: E_LOCAL_WH.
    wi_region : str
        Water intensity region key. Default: 'global_average'.
    """
    name: str
    attractor: str
    f_local: float
    queries_per_day: float = 20.0
    e_cloud: float = E_CLOUD_WH
    e_local: float = E_LOCAL_WH
    wi_region: str = "global_average"

    def __post_init__(self):
        assert 0.0 <= self.f_local <= 1.0, "f_local must be in [0, 1]"
        assert self.queries_per_day > 0, "queries_per_day must be positive"

    @property
    def water_intensity(self) -> float:
        """Water intensity (L/kWh) for the selected region."""
        return WATER_INTENSITY_REGIONAL[self.wi_region]

    @property
    def energy_per_day_wh(self) -> float:
        """Per-user daily energy consumption (Wh/user/day)."""
        return self.queries_per_day * (
            (1 - self.f_local) * self.e_cloud
            + self.f_local * self.e_local
        )

    @property
    def energy_per_day_kwh(self) -> float:
        """Per-user daily energy consumption (kWh/user/day)."""
        return self.energy_per_day_wh / 1000.0

    @property
    def water_per_day_ml(self) -> float:
        """Per-user daily water footprint (mL/user/day)."""
        return self.energy_per_day_kwh * self.water_intensity * 1000.0

    @property
    def tension_ext_normalized(self) -> float:
        """
        Normalized external tension T_ext ∈ [0, 1].
        Proportional to fraction of queries transmitted to cloud.
        High T_ext = high unnecessary data movement (Borda Milan 2026a, §3.1).
        """
        return 1.0 - self.f_local

    @property
    def tension_int_normalized(self) -> float:
        """
        Normalized internal tension T_int ∈ [0, 1].
        Proxy: 1 − M1_floor × f_local.
        A node with zero local capacity has maximum internal tension.
        (Borda Milan 2026a, §3.2)
        """
        return 1.0 - M1_EMPIRICAL_FLOOR * self.f_local

    @property
    def total_tension_normalized(self) -> float:
        """
        Normalized T(G) = T_ext + T_int (additive decomposition).
        (Borda Milan 2026a, §3; orthogonality argument in §3.4)
        """
        return self.tension_ext_normalized + self.tension_int_normalized

    @property
    def attractor_description(self) -> str:
        return ATTRACTOR_LABELS.get(self.attractor, "Unknown attractor")

    def summary(self) -> dict:
        return {
            "scenario": self.name,
            "attractor": self.attractor,
            "f_local": self.f_local,
            "Q (queries/day)": self.queries_per_day,
            "E (Wh/user/day)": round(self.energy_per_day_wh, 3),
            "W (mL/user/day)": round(self.water_per_day_ml, 1),
            "T_ext (norm.)": round(self.tension_ext_normalized, 3),
            "T_int (norm.)": round(self.tension_int_normalized, 3),
            "T_total (norm.)": round(self.total_tension_normalized, 3),
        }


def reduction_pct(baseline: float, target: float) -> float:
    """Percentage reduction of target vs. baseline."""
    if baseline == 0:
        raise ValueError("Baseline must be non-zero")
    return (baseline - target) / baseline * 100.0


def sensitivity_table(
    f_local_values: Optional[np.ndarray] = None,
    queries_per_day: float = 20.0,
    e_cloud: float = E_CLOUD_WH,
    e_local: float = E_LOCAL_WH,
    wi_l_per_kwh: float = WI_GLOBAL_L_PER_KWH,
) -> list[dict]:
    """
    Compute sensitivity table across f_local values.
    Reproduces Appendix A, Table A1 and Table A3 of the paper.

    Parameters
    ----------
    f_local_values : array-like, optional
        Fraction of queries resolved locally. Default: [0.3, 0.4, ..., 0.9].
    queries_per_day : float
        Mean queries per user per day.
    e_cloud, e_local : float
        Energy per cloud / local query (Wh).
    wi_l_per_kwh : float
        Water intensity (L/kWh).

    Returns
    -------
    list of dict, one row per f_local value.
    """
    if f_local_values is None:
        f_local_values = np.arange(0.3, 0.95, 0.1)

    E_A = queries_per_day * e_cloud
    rows = []
    for f in f_local_values:
        s = MADREScenario("B", "A4", f, queries_per_day, e_cloud, e_local)
        rows.append({
            "f_local": round(float(f), 2),
            "E_B (Wh/day)": round(s.energy_per_day_wh, 3),
            "E reduction (%)": round(reduction_pct(E_A, s.energy_per_day_wh), 1),
            "W_B (mL/day)": round(s.water_per_day_ml, 1),
            "W reduction (%)": round(reduction_pct(E_A * wi_l_per_kwh * 1000,
                                                    s.water_per_day_ml), 1),
            "T_ext": round(s.tension_ext_normalized, 3),
            "T_int": round(s.tension_int_normalized, 3),
            "T_total": round(s.total_tension_normalized, 3),
        })
    return rows


# ── Standard scenarios (paper §5.1) ─────────────────────────────────────

SCENARIO_A = MADREScenario(
    name="Scenario A — Cloud-only",
    attractor="A1",
    f_local=0.0,
    queries_per_day=20.0,
)

SCENARIO_B = MADREScenario(
    name="Scenario B — MADRE Hybrid (central)",
    attractor="A4",
    f_local=0.70,
    queries_per_day=20.0,
)

SCENARIO_B_LOW = MADREScenario(
    name="Scenario B — MADRE Hybrid (conservative)",
    attractor="A4",
    f_local=0.60,
    queries_per_day=20.0,
)

SCENARIO_B_HIGH = MADREScenario(
    name="Scenario B — MADRE Hybrid (optimistic)",
    attractor="A5",
    f_local=0.80,
    queries_per_day=20.0,
)

SCENARIO_C = MADREScenario(
    name="Scenario C — Distributed Renewable",
    attractor="A6",
    f_local=0.90,
    queries_per_day=20.0,
)


def print_scenario_comparison():
    """Print the main scenario comparison table (paper Table 5)."""
    print("\n" + "="*70)
    print("VEHICLE-MADRE Paper — Scenario Comparison (Table 5 reproduction)")
    print("="*70)
    for s in [SCENARIO_A, SCENARIO_B_LOW, SCENARIO_B, SCENARIO_B_HIGH, SCENARIO_C]:
        d = s.summary()
        print(f"\n{d['scenario']}")
        print(f"  Attractor:       {d['attractor']} — {ATTRACTOR_LABELS.get(d['attractor'], '')}")
        print(f"  f_local:         {d['f_local']:.0%}")
        print(f"  Energy:          {d['E (Wh/user/day)']:.3f} Wh/user/day")
        print(f"  Water:           {d['W (mL/user/day)']:.1f} mL/user/day")
        if s != SCENARIO_A:
            e_red = reduction_pct(SCENARIO_A.energy_per_day_wh, s.energy_per_day_wh)
            w_red = reduction_pct(SCENARIO_A.water_per_day_ml, s.water_per_day_ml)
            print(f"  Energy reduction: {e_red:.1f}% vs. Scenario A")
            print(f"  Water reduction:  {w_red:.1f}% vs. Scenario A")
        print(f"  T_ext:           {d['T_ext (norm.)']:.3f}")
        print(f"  T_int:           {d['T_int (norm.)']:.3f}")
        print(f"  T_total:         {d['T_total (norm.)']:.3f}")

    print("\n" + "="*70)
    print("Sensitivity Table (Appendix A, Table A1)")
    print("="*70)
    rows = sensitivity_table()
    header = " | ".join(f"{k:>14}" for k in rows[0].keys())
    print(header)
    print("-" * len(header))
    for row in rows:
        print(" | ".join(f"{str(v):>14}" for v in row.values()))
    print()


if __name__ == "__main__":
    print_scenario_comparison()
