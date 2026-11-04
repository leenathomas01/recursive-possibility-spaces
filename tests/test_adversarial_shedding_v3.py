"""Regression tests for v3. Run: python -m unittest discover -s tests -v"""
import unittest
from experiments.adversarial_shedding_v3 import (
    BASE, MACROS, Macro, certified, recover, search, suite,
)


class CorrectedSheddingTests(unittest.TestCase):
    def test_start_matters(self):
        self.assertFalse(search("a", "e", BASE, (MACROS[2],), budget=1).success)
        self.assertTrue(search("b", "e", BASE, (MACROS[2],), budget=1).success)

    def test_missing_edge_invalidates_macro(self):
        missing = tuple(e for e in BASE if e != ("b", "c"))
        for macro in MACROS:
            self.assertFalse(certified(macro, set(missing)))

    def test_corruption_rejected(self):
        poison = Macro("bad", ("a", "b", "x", "e"))
        self.assertFalse(certified(poison, set(BASE)))
        result = search("a", "e", BASE, (poison,) + MACROS, budget=4)
        self.assertTrue(result.success)
        self.assertEqual(result.path, ("a", "e"))

    def test_unverified_false_positive(self):
        poison = Macro("bad", ("a", "b", "x", "e"))
        self.assertTrue(search("a", "e", BASE, (poison,), budget=1,
                               verify=False).success)
        self.assertFalse(certified(poison, set(BASE)))

    def test_fixed_meta_fair_macro_baseline(self):
        self.assertEqual(suite(BASE, MACROS), (6, 14))
        damaged = tuple(e for e in BASE if e[0] != "b")
        self.assertEqual(suite(damaged, MACROS), (1, 5))
        self.assertEqual(suite(BASE, ()), (5, 19))

    def test_archive_cost_and_budget(self):
        damaged = tuple(e for e in BASE if e[0] != "b")
        rec = recover("a", "e", damaged, BASE, total_budget=8)
        self.assertTrue(rec.success)
        self.assertEqual(rec.examined, 6)
        self.assertFalse(recover("a", "e", damaged, BASE,
                                 total_budget=1).success)

    def test_unreachable_target(self):
        self.assertFalse(search("a", "z", BASE, MACROS, budget=100).success)


if __name__ == "__main__":
    unittest.main()
