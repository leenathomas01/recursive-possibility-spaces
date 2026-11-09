"""Tests for the target-side reconstruction toy."""

import unittest
from experiments.cdir_target_recon.target_recon import (
    CAPACITY,
    step,
    run_policy,
    memoryless_serve_if_positive,
    invariant_reconstruction,
    generic_internal_state,
    run_incorrect_invariant,
)


class TestPlant(unittest.TestCase):
    def test_serve_reduces(self):
        q, ov = step(3, True, arrival=1)
        self.assertEqual(q, 3)  # 3-1+1
        self.assertFalse(ov)

    def test_idle_grows(self):
        q, ov = step(0, False, arrival=1)
        self.assertEqual(q, 1)
        self.assertFalse(ov)

    def test_overflow_clips(self):
        q, ov = step(CAPACITY, False, arrival=1)
        self.assertTrue(ov)
        self.assertEqual(q, CAPACITY)


class TestPolicies(unittest.TestCase):
    def test_memoryless_succeeds_on_constant_arrival(self):
        res = run_policy(memoryless_serve_if_positive)
        self.assertTrue(res["success"])
        self.assertEqual(res["overflows"], 0)

    def test_reconstruction_also_succeeds(self):
        res = run_policy(invariant_reconstruction)
        self.assertTrue(res["success"])

    def test_generic_internal_can_fail(self):
        res = run_policy(generic_internal_state)
        # the even-counter policy under-serves
        self.assertGreater(res["overflows"], 0)

    def test_incorrect_invariant_fails(self):
        res = run_incorrect_invariant()
        self.assertFalse(res["success"])
        self.assertGreater(res["overflows"], 0)


if __name__ == "__main__":
    unittest.main()
