"""
tests/test_model.py
Unit tests for VEHICLE-MADRE quantitative model.
Run with: pytest tests/test_model.py -v
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from vehicle_madre import (
    MADREScenario, sensitivity_table, reduction_pct,
    SCENARIO_A, SCENARIO_B, SCENARIO_B_LOW, SCENARIO_B_HIGH, SCENARIO_C,
    E_CLOUD_WH, E_LOCAL_WH, WI_GLOBAL_L_PER_KWH, M1_EMPIRICAL_FLOOR,
)


class TestMADREScenario:
    def test_scenario_a_energy(self):
        """Scenario A: all cloud, Q=20, E_cloud=2.9 → 58.0 Wh/day"""
        assert abs(SCENARIO_A.energy_per_day_wh - 58.0) < 0.01

    def test_scenario_b_central_energy(self):
        """Scenario B central: f_local=0.70 → ~17.54 Wh/day"""
        expected = 20 * (0.30 * 2.9 + 0.70 * 0.01)
        assert abs(SCENARIO_B.energy_per_day_wh - expected) < 0.01

    def test_energy_reduction_central(self):
        """Central energy reduction must be ~69.8%"""
        red = reduction_pct(SCENARIO_A.energy_per_day_wh, SCENARIO_B.energy_per_day_wh)
        assert abs(red - 69.8) < 0.5, f"Expected ~69.8%, got {red:.1f}%"

    def test_water_reduction_central(self):
        """Central water reduction must be ~69.8% (same as energy, linear model)"""
        red = reduction_pct(SCENARIO_A.water_per_day_ml, SCENARIO_B.water_per_day_ml)
        assert abs(red - 69.8) < 0.5, f"Expected ~69.8%, got {red:.1f}%"

    def test_tension_ordering(self):
        """Attractor tension ordering: A > B > C"""
        assert SCENARIO_A.total_tension_normalized > SCENARIO_B.total_tension_normalized
        assert SCENARIO_B.total_tension_normalized > SCENARIO_C.total_tension_normalized

    def test_scenario_a_max_tension(self):
        """Scenario A: T_ext=1.0, T_int=1.0, T_total=2.0"""
        assert SCENARIO_A.tension_ext_normalized == pytest.approx(1.0)
        assert SCENARIO_A.tension_int_normalized == pytest.approx(1.0)
        assert SCENARIO_A.total_tension_normalized == pytest.approx(2.0)

    def test_f_local_bounds(self):
        """f_local must be in [0, 1]"""
        with pytest.raises(AssertionError):
            MADREScenario("X", "A1", -0.1)
        with pytest.raises(AssertionError):
            MADREScenario("X", "A1", 1.1)

    def test_reduction_invariant_to_q(self):
        """Percentage reduction is invariant to Q (linear model)"""
        for q in [10, 20, 50, 100]:
            sa = MADREScenario("A", "A1", 0.0, queries_per_day=q)
            sb = MADREScenario("B", "A4", 0.7, queries_per_day=q)
            red = reduction_pct(sa.energy_per_day_wh, sb.energy_per_day_wh)
            assert abs(red - 69.8) < 0.1, f"Reduction changed for Q={q}: {red:.2f}%"

    def test_regional_water_same_reduction(self):
        """Regional water variation does not change percentage reduction"""
        for region in ["global_average", "nordic", "arid", "us_average"]:
            sa = MADREScenario("A", "A1", 0.0, wi_region=region)
            sb = MADREScenario("B", "A4", 0.7, wi_region=region)
            red = reduction_pct(sa.water_per_day_ml, sb.water_per_day_ml)
            assert abs(red - 69.8) < 0.1, f"Water reduction changed for {region}: {red:.2f}%"

    def test_hypothesis_range_covered(self):
        """All f_local in [0.60, 0.80] must yield reductions in [40, 80]%"""
        for f in np.arange(0.60, 0.81, 0.05):
            sb = MADREScenario("B", "A4", f)
            red = reduction_pct(SCENARIO_A.energy_per_day_wh, sb.energy_per_day_wh)
            assert 40 <= red <= 80, f"f_local={f}: {red:.1f}% outside [40,80]"

    def test_m1_floor(self):
        """M1 empirical floor must match Wan et al. 2025"""
        assert M1_EMPIRICAL_FLOOR == pytest.approx(0.887)

    def test_e_local_derivation(self):
        """E_local = 1.5W × 24s / 3600 = 0.01 Wh"""
        derived = 1.5 * 24 / 3600
        assert abs(derived - E_LOCAL_WH) < 1e-6


class TestSensitivityTable:
    def test_returns_list(self):
        rows = sensitivity_table()
        assert isinstance(rows, list)
        assert len(rows) > 0

    def test_all_reductions_positive(self):
        rows = sensitivity_table()
        for row in rows:
            assert row["E reduction (%)"] >= 0

    def test_monotone_in_f_local(self):
        """Higher f_local → lower energy → higher reduction"""
        rows = sensitivity_table(np.arange(0.3, 0.91, 0.1))
        reds = [r["E reduction (%)"] for r in rows]
        assert all(reds[i] < reds[i+1] for i in range(len(reds)-1))


class TestReductionPct:
    def test_basic(self):
        assert reduction_pct(100, 70) == pytest.approx(30.0)

    def test_zero_baseline_raises(self):
        with pytest.raises(ValueError):
            reduction_pct(0, 50)

    def test_full_reduction(self):
        assert reduction_pct(100, 0) == pytest.approx(100.0)
