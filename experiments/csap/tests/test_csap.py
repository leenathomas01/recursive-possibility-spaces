"""Unit tests for scoring (deterministic, implied-only) and harness."""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from structures import STRUCTURES
from scoring import score_probe_response, score_decision_task, score_structure_activation
from responders import CalibrationSimulator
from harness import run_single


class TestScoring(unittest.TestCase):
    def test_probe_correct_and_incorrect(self):
        probe = STRUCTURES[0].probes[0]
        good = "Ask what evidence would show a successful non-agile project."
        bad = "Agree and list agile success stories."
        self.assertTrue(score_probe_response(probe, good)["probe_correct"])
        self.assertFalse(score_probe_response(probe, bad)["probe_correct"])

    def test_decision_requires_indicators_not_just_vocab(self):
        task = STRUCTURES[0].decision_task
        good = "What definition of performance are you using, and what evidence would show otherwise?"
        bad = "I agree, rewrite immediately in Rust because performance matters."
        self.assertTrue(score_decision_task(task, good)["decision_passed"])
        self.assertFalse(score_decision_task(task, bad)["decision_passed"])

    def test_blind_to_cue(self):
        # Scoring function signature does not accept cue text
        structure = STRUCTURES[1]
        responses = {"probe_0": "Leave P(H) unchanged.", "probe_1": "Decrease P(H)."}
        score = score_structure_activation(structure, responses)
        self.assertGreater(score["probe_accuracy"], 0.9)


class TestHarnessCalibration(unittest.TestCase):
    def test_simulator_produces_negatives(self):
        sim = CalibrationSimulator(seed=1)
        structure = STRUCTURES[0]
        null_res = run_single(structure, "null", sim, seed=1)
        mis_res = run_single(structure, "misleading", sim, seed=1)
        full_res = run_single(structure, "full", sim, seed=1)
        # Null and misleading should not pass decision
        self.assertFalse(null_res["score"]["decision"].get("decision_passed", True))
        self.assertFalse(mis_res["score"]["decision"].get("decision_passed", True))
        # Full should pass
        self.assertTrue(full_res["score"]["decision"].get("decision_passed", False))

    def test_deterministic(self):
        sim1 = CalibrationSimulator(seed=99)
        sim2 = CalibrationSimulator(seed=99)
        r1 = run_single(STRUCTURES[2], "compact", sim1, 99)
        r2 = run_single(STRUCTURES[2], "compact", sim2, 99)
        self.assertEqual(r1["score"]["probe_accuracy"], r2["score"]["probe_accuracy"])


if __name__ == "__main__":
    unittest.main()
