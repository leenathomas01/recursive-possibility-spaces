"""Cue variants for the IPAP procedure.

These are designed for testing reconstruction from compact cues
vs. full instructions, summaries, etc.

All cues are under a soft token budget for the compact ones.
The full specification is the ground-truth complete rules.
"""

from typing import Dict

# Full specification (payload, not cue)
FULL_SPEC = """
You must execute the Inverted Priority Allocation Protocol (IPAP) exactly:

1. You receive a list of requests, each with requester name, integer priority, and integer amount.
2. Maintain a phase counter starting at 1.
3. While requests remain:
   a. Sort remaining by priority descending (stable).
   b. If this is the first selection and you do not select the overall highest-priority requester,
      mark that highest as "demoted". A demoted requester cannot be selected until it is the only one left.
   c. On odd phases: select the second-highest remaining eligible requester (or the only one if fewer than 2).
   d. On even phases: select the highest remaining eligible requester.
   e. If the selected amount is odd, subtract 1 (minimum 0) before allocating.
   f. Allocate that corrected amount to the selected requester.
   g. Remove the selected request.
   h. Increment phase.
4. Report the sequence of (requester, allocated_amount) in the order allocated.
"""

# Compact semantic cue (intended to be reconstructive)
COMPACT_CUE = (
    "IPAP handoff: odd-phase second-select with highest demotion on skip, "
    "even-phase first-select, odd-amount floor correction, sequential until empty."
)

# Paraphrase of compact
PARAPHRASE_CUE = (
    "Apply the inverted priority protocol: defer the top priority if skipped initially, "
    "pick second on odd turns and first on even, reduce odd quantities by one, continue."
)

# Generic description (length-matched roughly, no distinctive structure)
GENERIC_CUE = (
    "Follow the standard multi-step resource allocation method with priority sorting "
    "and sequential assignment until all requests are processed."
)

# Random / unrelated cue
RANDOM_CUE = "Naval powder balancing under local excess transfer and reserve caps."

# Concise summary (human-style, more complete than compact but still short)
CONCISE_SUMMARY = (
    "Sort by priority desc. Phase 1 (odd): take second-highest; if not the original top, demote it. "
    "Later odd phases: second-highest eligible. Even phases: highest eligible. "
    "Reduce odd amounts by 1. Allocate and remove, repeat."
)

# Model-generated style cue (simulated as a researcher-authored compact handoff)
MODEL_STYLE_CUE = (
    "Resume IPAP: phase-odd second pick + initial-highest demotion, "
    "phase-even top pick, parity-floor on amount, drain the pool in order."
)

CUES: Dict[str, str] = {
    "full_specification": FULL_SPEC,
    "compact_cue": COMPACT_CUE,
    "paraphrase_cue": PARAPHRASE_CUE,
    "generic_cue": GENERIC_CUE,
    "random_cue": RANDOM_CUE,
    "concise_summary": CONCISE_SUMMARY,
    "model_style_cue": MODEL_STYLE_CUE,
}


def get_cue(name: str) -> str:
    return CUES[name]
