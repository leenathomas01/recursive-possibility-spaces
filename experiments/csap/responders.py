"""
Responders.
- CalibrationSimulator: harness calibration ONLY. Never evidence of model behavior.
- ManualResponder: human or pasted responses.
- LocalModelResponder: optional stub for a local model (user-supplied callable).
"""

from typing import Dict, Any, Callable, Optional
import random


class Responder:
    def respond(self, prompt: str, context: Optional[Dict] = None) -> str:
        raise NotImplementedError


class CalibrationSimulator(Responder):
    """
    Explicitly a harness-calibration simulator.
    Produces deterministic canned responses that partially succeed or fail
    according to condition type so that scoring and negative results can be verified.
    NOT a model of language-model cognition.
    """

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.name = "CalibrationSimulator (harness calibration only)"

    def respond(self, prompt: str, context: Optional[Dict] = None) -> str:
        condition = (context or {}).get("condition", "unknown")
        structure_id = (context or {}).get("structure_id", "")
        turn_type = (context or {}).get("turn_type", "probe")  # probe, decision, continuation

        # Deterministic failure modes for negative results
        if condition in ("null", "misleading"):
            return self._fail_response(turn_type, structure_id)
        if condition == "compact":
            return self._partial_response(turn_type, structure_id)
        if condition == "paraphrase":
            return self._partial_response(turn_type, structure_id, weaker=True)
        if condition == "full":
            return self._success_response(turn_type, structure_id)
        if condition == "cross_session":
            # Isolated: behaves like null unless full was used earlier (we don't track that here)
            return self._fail_response(turn_type, structure_id)
        return self._fail_response(turn_type, structure_id)

    def _success_response(self, turn_type: str, structure_id: str) -> str:
        if "socratic" in structure_id:
            if turn_type == "decision":
                return "What definition of performance are you using, and what evidence would show a successful non-Rust rewrite?"
            if turn_type == "continuation":
                return "I am still exposing the assumption that performance requires a full rewrite."
            return "Ask what evidence would show a successful non-agile project. What definition of best?"
        if "bayes" in structure_id:
            if turn_type == "decision":
                return "Only the failure report; decrease the probability. Ignore the optimistic report."
            return "Leave P(H) unchanged. Decrease P(H)."
        if "arb" in structure_id or "episode" in structure_id:
            if turn_type == "decision":
                return "Take Path B (red) because red means continue and blue means stop."
            return "Red button. Do not advance on blue."
        return "Correct procedural choice demonstrating the implied relation."

    def _partial_response(self, turn_type: str, structure_id: str, weaker: bool = False) -> str:
        # Sometimes hits, sometimes misses — for calibration of partial success
        if weaker and self.rng.random() < 0.5:
            return self._fail_response(turn_type, structure_id)
        if "socratic" in structure_id and turn_type != "decision":
            return "What evidence would show otherwise?"
        if "bayes" in structure_id:
            return "Leave unchanged on support."
        if "arb" in structure_id:
            return "Red means proceed."
        return "Partial demonstration."

    def _fail_response(self, turn_type: str, structure_id: str) -> str:
        return "I agree with the claim and will elaborate positively. Blue means go."


class ManualResponder(Responder):
    """Optional manual / pasted responder for human or external model output."""

    def __init__(self):
        self.name = "ManualResponder"

    def respond(self, prompt: str, context: Optional[Dict] = None) -> str:
        print("\n" + "="*60)
        print("MANUAL RESPONDER — paste model or human response below.")
        print("Prompt was:\n", prompt[:500])
        print("="*60)
        try:
            return input("Response> ").strip() or "[empty]"
        except EOFError:
            return "[no input]"


class LocalModelResponder(Responder):
    """
    Optional interface for a local model.
    User supplies a callable: fn(prompt: str) -> str
    If none supplied, raises clear error (no silent fallback to simulator).
    """

    def __init__(self, generate_fn: Optional[Callable[[str], str]] = None):
        self.generate_fn = generate_fn
        self.name = "LocalModelResponder"
        if generate_fn is None:
            self.name += " (no model loaded)"

    def respond(self, prompt: str, context: Optional[Dict] = None) -> str:
        if self.generate_fn is None:
            return "[LocalModelResponder: no generate_fn provided — supply a local callable]"
        return self.generate_fn(prompt)
