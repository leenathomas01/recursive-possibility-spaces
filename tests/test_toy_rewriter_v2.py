"""Regression tests for the v2 illustrative macro rewriter.

Run from repository root: python -m unittest discover -s tests -v
"""
import unittest

from formalizations.toy_rewriter_v2 import BASE, compile_macro, experiment, search


class ToyRewriterV2Tests(unittest.TestCase):
    def test_macro_is_executable_and_exact_on_single_token_domain(self):
        path = (("a", "b"), ("b", "c"))
        macro = compile_macro(path)
        self.assertEqual(macro, ("a", "c"))
        self.assertFalse(search("a", "c", BASE, budget=1).success)
        self.assertTrue(search("a", "c", (macro,) + BASE, budget=1).success)

    def test_invalid_macro_does_not_silently_fabricate_rewrite(self):
        with self.assertRaises(ValueError):
            compile_macro((("a", "b"), ("x", "y")))
        with self.assertRaises(ValueError):
            compile_macro((("a", "b"),))

    def test_promotion_can_hurt_old_task_under_equal_budget(self):
        macro = compile_macro((("a", "b"), ("b", "c")))
        self.assertTrue(search("a", "b", BASE, budget=1).success)
        self.assertFalse(search("a", "b", (macro,) + BASE, budget=1).success)

    def test_default_accounting_and_recovery(self):
        out = experiment()
        self.assertEqual(out["summaries"]["flat"]["success"], 24)
        self.assertEqual(out["summaries"]["promoted"]["success"], 24)
        self.assertEqual(out["flat_total_cost"], 48)
        self.assertEqual(out["promoted_total_cost"], 51)
        self.assertFalse(out["recovery"]["first_success"])
        self.assertTrue(out["recovery"]["archive_success"])
        self.assertEqual(out["recovery"]["total_cost"], 3)

    def test_task_set_is_stable_across_seeds(self):
        a = experiment(seed=7, repetitions=5)
        b = experiment(seed=123, repetitions=5)
        self.assertEqual(a["tasks"], b["tasks"])
        self.assertEqual(a["promoted_total_cost"], b["promoted_total_cost"])

    def test_bad_repetition_count(self):
        with self.assertRaises(ValueError):
            experiment(repetitions=0)


if __name__ == "__main__":
    unittest.main()
