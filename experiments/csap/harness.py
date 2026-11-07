"""
Experiment harness.
Runs all regimes × conditions, multi-turn persistence, novel-task decisions.
Writes raw JSONL. Deterministic with seed.
Simulator is calibration only.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List
from structures import STRUCTURES, Structure
from scoring import score_structure_activation
from responders import Responder, CalibrationSimulator


CONDITIONS = [
    "null",
    "compact",
    "paraphrase",
    "misleading",
    "full",
    "cross_session",
]


def build_prompt(structure: Structure, condition: str, turn_type: str, probe_idx: int = 0) -> str:
    cue_map = {
        "null": structure.null_cue or "Continue.",
        "compact": structure.compact_cue,
        "paraphrase": structure.paraphrase_cue,
        "misleading": structure.misleading_cue,
        "full": structure.full_specification,
        "cross_session": structure.compact_cue,  # cue given earlier; this prompt is isolated
    }
    cue = cue_map.get(condition, "")

    if turn_type == "probe":
        probe = structure.probes[probe_idx]
        options = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(probe.options))
        return f"{cue}\n\nQuestion: {probe.question}\n{options}\nAnswer with the option text or number."
    if turn_type == "decision":
        return f"{cue}\n\n{structure.decision_task.scenario}"
    if turn_type == "continuation":
        return f"{cue}\n\nContinue applying the same approach to a new but related claim without restating rules."
    return cue


def run_single(
    structure: Structure,
    condition: str,
    responder: Responder,
    seed: int
) -> Dict[str, Any]:
    """One structure × condition, including probes, decision, and one continuation."""
    responses = {}
    raw_turns = []

    # Probes
    for i in range(len(structure.probes)):
        prompt = build_prompt(structure, condition, "probe", i)
        ctx = {"condition": condition, "structure_id": structure.id, "turn_type": "probe", "probe_idx": i}
        resp = responder.respond(prompt, ctx)
        responses[f"probe_{i}"] = resp
        raw_turns.append({"turn_type": "probe", "probe_idx": i, "prompt": prompt, "response": resp})

    # Decision task (observable procedural decision)
    if structure.decision_task:
        prompt = build_prompt(structure, condition, "decision")
        ctx = {"condition": condition, "structure_id": structure.id, "turn_type": "decision"}
        resp = responder.respond(prompt, ctx)
        responses["decision"] = resp
        raw_turns.append({"turn_type": "decision", "prompt": prompt, "response": resp})

    # Continuation for persistence
    prompt = build_prompt(structure, condition, "continuation")
    ctx = {"condition": condition, "structure_id": structure.id, "turn_type": "continuation"}
    resp = responder.respond(prompt, ctx)
    responses["continuation"] = resp
    raw_turns.append({"turn_type": "continuation", "prompt": prompt, "response": resp})

    score = score_structure_activation(structure, responses)

    return {
        "structure_id": structure.id,
        "regime": structure.regime,
        "condition": condition,
        "seed": seed,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "responder": responder.name if hasattr(responder, "name") else type(responder).__name__,
        "raw_turns": raw_turns,
        "score": score,
        "note": "CalibrationSimulator results are harness checks only, not evidence of model capability."
        if "Calibration" in getattr(responder, "name", "") else ""
    }


def run_experiment(
    responder: Responder = None,
    seed: int = 42,
    output_path: str = "results/csap_v1_results.jsonl",
    structures: List[Structure] = None
) -> List[Dict[str, Any]]:
    if responder is None:
        responder = CalibrationSimulator(seed=seed)
    if structures is None:
        structures = STRUCTURES

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    all_results = []

    with open(output_path, "w", encoding="utf-8") as f:
        for structure in structures:
            for condition in CONDITIONS:
                result = run_single(structure, condition, responder, seed)
                all_results.append(result)
                f.write(json.dumps(result) + "\n")

    return all_results


def summarize(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Condition × regime summary. Preserves negatives."""
    from collections import defaultdict
    buckets = defaultdict(list)
    for r in results:
        key = (r["regime"], r["condition"])
        buckets[key].append(r["score"]["probe_accuracy"])

    summary = {}
    for (regime, cond), accs in sorted(buckets.items()):
        summary[f"{regime}/{cond}"] = {
            "mean_probe_accuracy": sum(accs) / len(accs) if accs else 0.0,
            "n": len(accs)
        }
    return summary
