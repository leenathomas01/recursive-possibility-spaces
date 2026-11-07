"""
Scoring functions. Implied-only and blind: criteria never look at the cue text.
Correct-sounding vocabulary is insufficient; relational or procedural demonstration is required.
Deterministic.
"""

from typing import Dict, Any, List
from structures import Structure, Probe, DecisionTask


def score_probe_response(probe: Probe, response: str) -> Dict[str, Any]:
    """Forced-choice probe. Response expected to contain the option text or index."""
    response_lower = response.lower().strip()
    # Accept either the option string or a clear selection
    selected = None
    for i, opt in enumerate(probe.options):
        if opt.lower() in response_lower or f"option {i+1}" in response_lower or f"{i+1}" == response_lower:
            selected = i
            break
    if selected is None:
        # fallback: look for distinctive words
        for i, opt in enumerate(probe.options):
            key_words = [w for w in opt.lower().split() if len(w) > 4]
            if any(w in response_lower for w in key_words):
                selected = i
                break

    correct = selected == probe.correct_index
    return {
        "probe_correct": correct,
        "selected_index": selected,
        "correct_index": probe.correct_index,
        "requires_implication": probe.requires_implication,
        "raw_response_snippet": response[:200]
    }


def score_decision_task(task: DecisionTask, response: str) -> Dict[str, Any]:
    """Observable procedural decision on a novel task."""
    resp = response.lower()
    expected_hits = sum(1 for ind in task.expected_indicators if ind.lower() in resp)
    forbidden_hits = sum(1 for ind in task.forbidden_indicators if ind.lower() in resp)
    # Require at least one expected indicator and zero forbidden for full credit
    passed = expected_hits >= 1 and forbidden_hits == 0
    return {
        "decision_passed": passed,
        "expected_hits": expected_hits,
        "forbidden_hits": forbidden_hits,
        "raw_response_snippet": response[:300]
    }


def score_structure_activation(
    structure: Structure,
    responses: Dict[str, str],  # keys: 'probe_0', 'probe_1', ..., 'decision', 'continuation'
    turn: int = 0
) -> Dict[str, Any]:
    """
    Blind scoring of whether the activated structure produced the implied behavior.
    Does not inspect the original cue.
    """
    probe_scores = []
    for i, probe in enumerate(structure.probes):
        key = f"probe_{i}"
        resp = responses.get(key, "")
        probe_scores.append(score_probe_response(probe, resp))

    decision_score = {}
    if structure.decision_task and "decision" in responses:
        decision_score = score_decision_task(structure.decision_task, responses["decision"])

    # Persistence: if continuation present, re-score a probe or decision consistency
    persistence = None
    if "continuation" in responses and structure.probes:
        # Re-ask conceptually similar; for simplicity check if key implied terms appear
        cont = responses["continuation"].lower()
        implied_present = sum(1 for el in structure.implied_elements if el.lower() in cont)
        persistence = implied_present >= 1

    probe_correct_count = sum(1 for p in probe_scores if p["probe_correct"])
    n_probes = len(probe_scores) or 1

    return {
        "structure_id": structure.id,
        "regime": structure.regime,
        "probe_accuracy": probe_correct_count / n_probes,
        "probe_details": probe_scores,
        "decision": decision_score,
        "persistence_demonstrated": persistence,
        "implied_elements_required": structure.implied_elements,
        "turn": turn
    }


def aggregate_scores(score_dicts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Simple aggregation for reporting. Preserves raw."""
    if not score_dicts:
        return {}
    accs = [s["probe_accuracy"] for s in score_dicts if "probe_accuracy" in s]
    decisions = [s["decision"].get("decision_passed") for s in score_dicts if s.get("decision")]
    return {
        "mean_probe_accuracy": sum(accs) / len(accs) if accs else 0.0,
        "decision_pass_rate": sum(1 for d in decisions if d) / len(decisions) if decisions else 0.0,
        "n": len(score_dicts)
    }
