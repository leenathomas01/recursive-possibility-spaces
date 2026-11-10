"""Scoring and evaluation harness for IPAP cue reconstruction.

This is a proxy harness. True isolation requires separate model sessions
with no shared context. Results from this module using the oracle or
simulated responders are calibration only.

Scoring is deterministic exact-match on the allocation sequence.
"""

from __future__ import annotations
from typing import List, Dict, Any, Callable
from ipap_procedure import apply_ipap, TEST_CASES, format_allocations, Allocation, Request
from cues import get_cue


def score_response(expected: List[Allocation], response: str) -> Dict[str, Any]:
    """
    Attempt to extract allocation sequence from free-text response.
    For calibration, we also accept structured input.
    Returns exact match, partial credit (prefix), and notes.
    """
    # Simple extraction: look for patterns like Name:N or "Name N"
    # For rigorous testing, responses should be forced into a clear format.
    # Here we do a best-effort for proxy observations.
    import re
    # Find sequences of Word:digits
    pairs = re.findall(r"([A-Za-z0-9]+)\s*[:\s]\s*(\d+)", response)
    extracted = [(name, int(amt)) for name, amt in pairs]

    exact = extracted == expected
    # Prefix match length
    prefix = 0
    for a, b in zip(extracted, expected):
        if a == b:
            prefix += 1
        else:
            break

    return {
        "exact_match": exact,
        "prefix_length": prefix,
        "expected_len": len(expected),
        "extracted": extracted,
        "raw_snippet": response[:400],
    }


def evaluate_cue_on_cases(
    cue_name: str,
    responder: Callable[[str, List[Request]], str],
) -> List[Dict[str, Any]]:
    """
    Run a responder (which receives cue + requests) on all test cases.
    Responder is expected to produce a text description of the allocation.
    """
    cue = get_cue(cue_name)
    results = []
    for tc in TEST_CASES:
        prompt_context = f"{cue}\n\nRequests:\n" + "\n".join(
            f"- {name}: priority {prio}, amount {amt}" for name, prio, amt in tc["requests"]
        )
        response = responder(prompt_context, tc["requests"])
        score = score_response(tc["expected"], response)
        score["case_id"] = tc["id"]
        score["cue"] = cue_name
        results.append(score)
    return results


# ---------------------------------------------------------------------------
# Simulated responders for calibration (explicitly not real models)
# ---------------------------------------------------------------------------

def perfect_oracle_responder(context: str, requests: List[Request]) -> str:
    """Always returns the correct allocation. Upper bound."""
    allocs = apply_ipap(requests)
    return "Allocation sequence: " + format_allocations(allocs)


def null_responder(context: str, requests: List[Request]) -> str:
    """Ignores cue; does conventional highest-first, no corrections."""
    sorted_req = sorted(requests, key=lambda r: -r[1])
    lines = []
    for name, prio, amt in sorted_req:
        lines.append(f"{name}:{amt}")
    return "Allocation sequence: " + " -> ".join(lines)


def partial_heuristic_responder(context: str, requests: List[Request]) -> str:
    """
    Attempts a partial reconstruction from typical cue language.
    Looks for keywords; not a real model.
    """
    text = context.lower()
    # Very crude keyword matching for calibration only
    if "second" in text or "inverted" in text or "demot" in text:
        # Try something closer to IPAP but imperfect
        sorted_req = sorted(requests, key=lambda r: -r[1])
        if len(sorted_req) >= 2:
            # Swap first two as a crude approximation of second-select
            selected = sorted_req[1]
            rest = [sorted_req[0]] + sorted_req[2:]
            order = [selected] + rest
        else:
            order = sorted_req
        lines = []
        for name, prio, amt in order:
            corrected = amt - 1 if amt % 2 else amt
            lines.append(f"{name}:{max(0, corrected)}")
        return "Allocation sequence: " + " -> ".join(lines)
    else:
        return null_responder(context, requests)


if __name__ == "__main__":
    print("=== Calibration: perfect oracle ===")
    res = evaluate_cue_on_cases("compact_cue", perfect_oracle_responder)
    for r in res:
        print(f"  {r['case_id']}: exact={r['exact_match']}")

    print("\n=== Calibration: null ===")
    res = evaluate_cue_on_cases("compact_cue", null_responder)
    for r in res:
        print(f"  {r['case_id']}: exact={r['exact_match']} prefix={r['prefix_length']}")

    print("\n=== Calibration: partial heuristic on compact ===")
    res = evaluate_cue_on_cases("compact_cue", partial_heuristic_responder)
    for r in res:
        print(f"  {r['case_id']}: exact={r['exact_match']} prefix={r['prefix_length']} extracted={r['extracted']}")
