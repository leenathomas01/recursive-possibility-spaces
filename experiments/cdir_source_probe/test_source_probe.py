"""Tests for the source-side probe experiment."""

import unittest
from experiments.cdir_source_probe.source_probe import (
    PlantConfig,
    simulate,
    make_p,
    make_pi,
    generate_histories,
    history_only_extraction,
    active_probing_extraction,
    PROPERTY_BATTERY,
)


class TestSimulator(unittest.TestCase):
    def test_zero_disturbance_p_converges(self):
        cfg = PlantConfig(u_max=2.0, horizon=20, success_threshold=0.15)
        res = simulate(make_p(0.6), 1.0, [0.0] * 20, cfg)
        self.assertTrue(res["success"])
        self.assertLess(abs(res["final"]), 0.15)

    def test_constant_w_p_has_offset(self):
        cfg = PlantConfig(u_max=2.0, horizon=40, success_threshold=0.15)
        res = simulate(make_p(0.6), 0.0, [0.1] * 40, cfg)
        # equilibrium ~ 0.1/0.6 ≈ 0.167
        self.assertFalse(res["success"])
        self.assertGreater(abs(res["final"]), 0.15)

    def test_pi_rejects_constant_w(self):
        cfg = PlantConfig(u_max=2.0, horizon=40, success_threshold=0.15)
        res = simulate(make_pi(0.4, 0.15), 0.0, [0.1] * 40, cfg)
        self.assertTrue(res["success"])
        self.assertLess(abs(res["final"]), 0.05)

    def test_saturation_blocks_large_w(self):
        cfg = PlantConfig(u_max=0.3, horizon=20)
        res = simulate(make_p(0.6), 0.0, [0.5] * 20, cfg)
        # cannot cancel w=0.5 with |u|<=0.3
        self.assertGreater(res["final"], 1.0)


class TestHistoriesAndExtraction(unittest.TestCase):
    def test_histories_are_limited_and_accurate(self):
        h = generate_histories(seed=42)
        self.assertEqual(set(h.keys()), {"P", "PI", "Limited"})
        for name, entries in h.items():
            self.assertEqual(len(entries), 6)  # 3 x0 × 2 w
            for e in entries:
                self.assertIn(e.x0, [-1.0, 0.0, 1.0])
                self.assertIn(e.w_value, [0.0, 0.1])

    def test_history_only_does_not_claim_untested(self):
        h = generate_histories()
        res = history_only_extraction(h, "P")
        self.assertEqual(res.simulations_used, 0)
        self.assertIn("rejects_mild_constant_disturbance", res.observed_properties)
        # P fails the mild-w cases under the threshold
        self.assertEqual(res.observed_properties["rejects_mild_constant_disturbance"], "unsupported")

    def test_active_probing_counts_steps_and_reveals_ablation(self):
        h = generate_histories()
        res = active_probing_extraction(h, "PI", seed=1)
        self.assertGreater(res.simulations_used, 0)
        self.assertTrue(any("Ablated integral" in n for n in res.evidence_notes))
        self.assertTrue(any("load-bearing" in n for n in res.evidence_notes))

    def test_property_battery_fixed(self):
        self.assertGreaterEqual(len(PROPERTY_BATTERY), 4)


if __name__ == "__main__":
    unittest.main()
