import unittest
from experiments.causal_role_preservation_v2 import (
    ActiveSystem, InertSystem, DecorativeReadSystem, SideEffectSystem,
    TranslatedSystem, TrustedHarness, restricted_transcript,
)


class TestV2(unittest.TestCase):
    def test_indistinguishable_pair_same_transcript(self):
        inputs = [1, 2, 3, 4]
        t1 = restricted_transcript(ActiveSystem, "high_add", 999, inputs)
        t2 = restricted_transcript(InertSystem, "high_add", 999, inputs)
        self.assertEqual(t1, t2)

    def test_detector_underdetermined_on_pair(self):
        h = TrustedHarness()
        inputs = [1, 2, 3, 4]
        for Cls in (ActiveSystem, InertSystem):
            obs = h.probe(Cls(), "high_add", 999, inputs)
            conclusions = h.classify(obs)
            self.assertIn("no_effect_on_tested_inputs", conclusions)
            self.assertNotIn("local_causal_effect_supported", conclusions)
            self.assertFalse(any("contradict" in c for c in conclusions))

    def test_sensitive_input_separates(self):
        h = TrustedHarness()
        obs_a = h.probe(ActiveSystem(), "high_add", 999, [3, 7])
        obs_i = h.probe(InertSystem(), "high_add", 999, [3, 7])
        self.assertIn(7, obs_a.changed_inputs)
        self.assertEqual(obs_i.changed_inputs, set())
        self.assertIn("local_causal_effect_supported", h.classify(obs_a))
        self.assertIn("no_effect_on_tested_inputs", h.classify(obs_i))

    def test_misleading_path_does_not_drive_classification(self):
        h = TrustedHarness()
        obs = h.probe(InertSystem(), "low_mult", 99, [3])
        conclusions = h.classify(obs)
        self.assertIn("no_effect_on_tested_inputs", conclusions)
        self.assertNotIn("local_causal_effect_supported", conclusions)

    def test_decorative_read_not_causal(self):
        h = TrustedHarness()
        obs = h.probe(DecorativeReadSystem(), "low_mult", 99, [3, 7])
        self.assertEqual(obs.changed_inputs, set())
        self.assertIn("no_effect_on_tested_inputs", h.classify(obs))

    def test_insensitive_intervention_not_contradiction(self):
        h = TrustedHarness()
        obs = h.probe(ActiveSystem(), "high_add", 999, [3])
        conclusions = h.classify(obs)
        self.assertIn("no_effect_on_tested_inputs", conclusions)
        self.assertFalse(any("contradict" in c for c in conclusions))

    def test_side_effect_does_not_prove_rule_path(self):
        h = TrustedHarness()
        obs = h.probe(SideEffectSystem(), "low_mult", 99, [3])
        self.assertTrue(obs.changed_inputs)
        conclusions = h.classify(obs)
        self.assertIn("local_causal_effect_supported", conclusions)
        self.assertNotIn("provenance_verified", conclusions)

    def test_valid_translation(self):
        ts = TranslatedSystem()
        self.assertEqual(ts.evaluate(3), 6)
        self.assertTrue(ts.intervene_translated("low_mult", 99))
        self.assertEqual(ts.evaluate(3), 297)

    def test_invalid_translation(self):
        ts = TranslatedSystem()
        self.assertFalse(ts.intervene_translated("nonexistent", 1))

    def test_fresh_instances_no_contamination(self):
        h = TrustedHarness()
        h.probe(ActiveSystem(), "low_mult", 99, [3])
        obs = h.probe(ActiveSystem(), "low_mult", 2, [3])
        self.assertEqual(obs.before[3], 6)

    def test_out_of_domain(self):
        self.assertEqual(InertSystem().evaluate(100), -999)
        self.assertEqual(ActiveSystem().evaluate(100), 110)


if __name__ == "__main__":
    unittest.main()
