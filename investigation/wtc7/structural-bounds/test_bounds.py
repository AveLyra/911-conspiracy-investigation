"""Known answers and invariants test only the explicitly idealized mechanics."""

import math
from pathlib import Path
import tempfile
import unittest

import bounds


class BoundsTests(unittest.TestCase):
    def test_constant_force_stop_includes_weight(self):
        # Drop h=1; R=3mg. Stop stroke h/(3-1)=0.5, not h/3.
        out = bounds.transit(1, 1, [(1, 3)], gravity=1)
        self.assertTrue(out["stopped"])
        self.assertAlmostEqual(out["distance"], 0.5)
        self.assertAlmostEqual(out["resistance_work"], 1.5)
        self.assertAlmostEqual(out["energy_residual"], 0)

    def test_continue_and_endpoint(self):
        self.assertFalse(bounds.transit(1, 1, [(0.1, 10)], 1)["stopped"])
        self.assertTrue(bounds.transit(1, 1, [(0.1, 11)], 1)["stopped"])
        self.assertAlmostEqual(bounds.transit(1, 1, [(0.1, 10)], 1)["kinetic_out"], 0.1)

    def test_early_barrier_prevents_reaching_positive_final_formula(self):
        # Unchecked final expression is 1 + 2 - 2.5 = +0.5,
        # but high early resistance stops the mass at 1/(25-1).
        out = bounds.transit(1, 1, [(0.1, 25), (1.9, 0)], 1)
        self.assertTrue(out["stopped"])
        self.assertAlmostEqual(out["distance"], 1 / 24)

    def test_zero_energy_hold_and_release(self):
        self.assertTrue(bounds.transit(2, 0, [(1, 2)], 1)["stopped"])
        self.assertTrue(bounds.transit(2, 0, [(1, 3)], 1)["stopped"])
        self.assertFalse(bounds.transit(2, 0, [(1, 1)], 1)["stopped"])

    def test_resistance_subdivision_invariance(self):
        a = bounds.transit(1, 10, [(2, 3)], 1)
        b = bounds.transit(1, 10, [(0.5, 3)] * 4, 1)
        for key in a:
            self.assertAlmostEqual(a[key], b[key])

    def test_dimensional_rescaling(self):
        # Arbitrary base changes M*=7, L*=3, T*=2.
        original = bounds.transit(2, 5, [(0.5, 12)], 4)
        mass_scale, length_scale, time_scale = 7, 3, 2
        force_scale = mass_scale * length_scale / time_scale ** 2
        energy_scale = force_scale * length_scale
        other = bounds.transit(2 * mass_scale, 5 * energy_scale,
                               [(0.5 * length_scale, 12 * force_scale)],
                               4 * length_scale / time_scale ** 2)
        self.assertEqual(original["stopped"], other["stopped"])
        self.assertAlmostEqual(original["distance"] * length_scale, other["distance"])
        self.assertAlmostEqual(original["kinetic_out"] * energy_scale, other["kinetic_out"])

    def test_equal_mass_inelastic(self):
        out = bounds.collision(1, 1, 2, 0)
        self.assertEqual(out["moving_velocity_out"], 1)
        self.assertEqual(out["target_velocity_out"], 1)
        self.assertEqual(out["kinetic_after"], 1)
        self.assertEqual(out["collision_loss"], 1)

    def test_equal_mass_elastic(self):
        out = bounds.collision(1, 1, 2, 1)
        self.assertEqual(out["moving_velocity_out"], 0)
        self.assertEqual(out["target_velocity_out"], 2)
        self.assertEqual(out["collision_loss"], 0)

    def test_collision_conservation_and_restitution_grid(self):
        for m in (0.1, 1, 7):
            for target in (0.25, 1, 4):
                for e in (0, 0.5, 1):
                    out = bounds.collision(m, target, 3, e)
                    self.assertAlmostEqual(out["energy_residual"], 0)
                    self.assertAlmostEqual(out["momentum_residual"], 0)
                    self.assertGreaterEqual(out["collision_loss"], 0)
                    self.assertAlmostEqual(out["target_velocity_out"] - out["moving_velocity_out"], 3 * e)

    def test_cascade_conservation_grid(self):
        for pickup in (False, True):
            for delta in (0.05, 0.1, 0.5):
                for r in (0, 2, 5, 10, 20, 50):
                    for row in bounds.cascade(r, delta, pickup):
                        self.assertAlmostEqual(row["cumulative_energy_residual"], 0, places=11)
                        self.assertGreaterEqual(row["kinetic_out"], 0)

    def test_cascade_retains_both_outcomes(self):
        for pickup in (False, True):
            self.assertTrue(bounds.cascade(50, 0.1, pickup)[-1]["stopped"])
            self.assertEqual(len(bounds.cascade(0, 0.1, pickup)), 8)
            self.assertFalse(bounds.cascade(0, 0.1, pickup)[-1]["stopped"])

    def test_euler_and_dimensions(self):
        ref = bounds.euler_load(2, 3, 4)
        self.assertAlmostEqual(ref, math.pi ** 2 * 6 / 16)
        self.assertAlmostEqual(bounds.euler_load(2, 3, 8), ref / 4)
        self.assertAlmostEqual(bounds.euler_load(1, 3, 4, 2), ref / 8)
        # E has dimensions M L^-1 T^-2, I has L^4; answer M L T^-2.
        scaled = bounds.euler_load(2 * 7 / 3 / 2**2, 3 * 3**4, 4 * 3)
        self.assertAlmostEqual(scaled, ref * 7 * 3 / 2**2)

    def test_gravity_time_equation_and_monotonicity(self):
        for d in (0, 0.1, 1, 4, 10, 30):
            for v in (0, 5):
                t = bounds.gravity_time(d, v)
                self.assertAlmostEqual(v * t + 0.5 * 9.80665 * t * t, d)
            self.assertLessEqual(bounds.gravity_time(d, 5), bounds.gravity_time(d, 0))
        self.assertAlmostEqual(bounds.gravity_time(4, 5) * 2,
                               bounds.gravity_time(4 * 3, 5 * 3 / 2, 9.80665 * 3 / 4))

    def test_invalid_parameters(self):
        for value in (float("nan"), float("inf"), -1, True, "1"):
            with self.assertRaises(ValueError):
                bounds.transit(value, 1, [(1, 1)], 1)
        for args in ((1, 0, 1, 0), (1, 1, 1, 1.1)):
            with self.assertRaises(ValueError):
                bounds.collision(*args)
        with self.assertRaises(ValueError):
            bounds.transit(1, 1, [], 1)

    def test_deterministic_products_and_output_guard(self):
        self.assertEqual(bounds.products(), bounds.products())
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "run"
            result = bounds.save(out)
            self.assertEqual(result["status"], "complete")
            with self.assertRaises(FileExistsError):
                bounds.save(out)


if __name__ == "__main__":
    unittest.main()
