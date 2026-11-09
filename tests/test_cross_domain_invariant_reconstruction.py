"""Tests for the cross-domain invariant reconstruction toy."""

import unittest
import random
from experiments.cross_domain_invariant_reconstruction import (
    source_feedback,
    source_misleading,
    transfer,
    imbalance,
    min_achievable_imbalance,
    is_optimal,
    reconstructed_policy,
    incorrect_reconstructed_policy,
    conventional_translation,
    direct_copy_attempt,
    run_policy,
    evaluate_all,
)


class TestSourceDomain(unittest.TestCase):
    def test_feedback_reaches_zero(self):
        for start in range(-10, 11):
            p = start
            for _ in range(abs(start) + 1):
                p = source_feedback(p)
            self.assertEqual(p, 0)

    def test_misleading_only_positive(self):
        self.assertEqual(source_misleading(5), 4)
        self.assertEqual(source_misleading(-5), -5)
        self.assertEqual(source_misleading(0), 0)


class TestTargetDomain(unittest.TestCase):
    def test_transfer_and_conservation(self):
        s = (5, 3)
        self.assertEqual(transfer(s, True), (4, 4))
        self.assertEqual(sum(transfer(s, True)), sum(s))
        self.assertEqual(transfer((0, 3), True), (0, 3))  # blocked

    def test_parity_constraint(self):
        self.assertEqual(min_achievable_imbalance((3, 5)), 0)  # even total
        self.assertEqual(min_achievable_imbalance((3, 8)), 1)  # odd total
        self.assertTrue(is_optimal((4, 4)))
        self.assertTrue(is_optimal((5, 4)))
        self.assertFalse(is_optimal((6, 3)))


class TestPolicies(unittest.TestCase):
    def test_reconstructed_even(self):
        ok, steps, imb = run_policy((5, 1), reconstructed_policy)
        self.assertTrue(ok)
        self.assertEqual(imb, 0)

    def test_reconstructed_odd(self):
        ok, steps, imb = run_policy((3, 8), reconstructed_policy)
        self.assertTrue(ok)
        self.assertEqual(imb, 1)

    def test_incorrect_fails_when_right_larger(self):
        ok, steps, imb = run_policy((1, 5), incorrect_reconstructed_policy, max_steps=10)
        self.assertFalse(ok)
        self.assertGreater(imb, 1)

    def test_conventional_succeeds(self):
        ok, _, imb = run_policy((0, 4), conventional_translation)
        self.assertTrue(ok)
        self.assertEqual(imb, 0)

    def test_direct_copy_fails_on_right_excess(self):
        ok, _, imb = run_policy((1, 5), direct_copy_attempt, max_steps=15)
        self.assertFalse(ok)


class TestEvaluateAll(unittest.TestCase):
    def test_evaluate_returns_all_methods(self):
        results = evaluate_all((4, 2), budget=20, seed=1)
        methods = {r.method for r in results}
        self.assertIn("direct_copy", methods)
        self.assertIn("conventional_translation", methods)
        self.assertIn("target_only_search", methods)
        self.assertIn("invariant_reconstruction", methods)
        self.assertIn("incorrect_invariant", methods)

    def test_reconstruction_and_translation_both_can_succeed(self):
        results = evaluate_all((6, 2), budget=20, seed=7)
        by_name = {r.method: r for r in results}
        self.assertTrue(by_name["invariant_reconstruction"].success)
        self.assertTrue(by_name["conventional_translation"].success)


if __name__ == "__main__":
    unittest.main()
