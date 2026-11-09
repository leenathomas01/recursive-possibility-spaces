"""CDIR Experiment 2: First target-side reconstruction attempt.

Source domain (from prior probe): scalar arithmetic feedback with optional integral state.
Target domain: discrete single-buffer queue under constant arrivals.
  State: integer queue length (0..capacity)
  Operations: serve (decrement by 1 if >0) or idle
  External: constant arrival of 1 token per step
  Success: no overflow, queue remains bounded and low

Grammar differs: no signed continuous correction; only discrete serve/idle on an integer counter
with hard capacity. No direct analogue of proportional gain.

Abstraction drawn from source probe: "persistent bias (constant arrival) can be rejected
by accumulating a progress/error measure and acting when it crosses a threshold."
This is recorded separately; it is not the final policy.

Comparators:
- Target-only: memoryless serve-if-positive
- Generic hint: consider internal state (no source-specific content)
- Conventional translation: map "error" to queue length, "correction" to serve
- Invariant reconstruction: use accumulated-arrival counter to decide service

All evaluated on the same plant. Costs counted as plant steps.
Adversarial variants included. Negative findings preserved.

Run: python experiments/cdir_target_recon/target_recon.py
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple


CAPACITY = 8
HORIZON = 40
ARRIVAL = 1  # constant


@dataclass
class StepResult:
    q: int
    action: str
    overflow: bool


def step(q: int, serve: bool, arrival: int = ARRIVAL) -> Tuple[int, bool]:
    """One plant step. Serve first, then arrival. Overflow if > CAPACITY."""
    if serve and q > 0:
        q -= 1
    q += arrival
    overflow = q > CAPACITY
    if overflow:
        q = CAPACITY  # hard clip, but flag it
    return q, overflow


def run_policy(
    policy: Callable[[int, Optional[dict]], Tuple[bool, Optional[dict]]],
    q0: int = 0,
    horizon: int = HORIZON,
    arrival: int = ARRIVAL,
    count: Optional[List[int]] = None,
) -> Dict:
    q = q0
    internal: Optional[dict] = {}
    overflows = 0
    total_q = 0
    for t in range(horizon):
        serve, internal = policy(q, internal)
        q, ov = step(q, serve, arrival)
        if ov:
            overflows += 1
        total_q += q
        if count is not None:
            count[0] += 1
    return {
        "final_q": q,
        "overflows": overflows,
        "avg_q": total_q / horizon,
        "success": overflows == 0 and q <= CAPACITY,
    }


# ---------------------------------------------------------------------------
# Policies
# ---------------------------------------------------------------------------

def memoryless_serve_if_positive(q: int, internal: Optional[dict]) -> Tuple[bool, Optional[dict]]:
    return q > 0, internal


def memoryless_always_serve(q: int, internal: Optional[dict]) -> Tuple[bool, Optional[dict]]:
    return True, internal


def generic_internal_state(q: int, internal: Optional[dict]) -> Tuple[bool, Optional[dict]]:
    """Generic hint: maintain a counter, serve when it is even. No source knowledge."""
    internal = internal or {"c": 0}
    internal["c"] += 1
    serve = (internal["c"] % 2 == 0) and q > 0
    return serve, internal


def conventional_translation(q: int, internal: Optional[dict]) -> Tuple[bool, Optional[dict]]:
    """Map queue length as 'error'; serve when error > 0. Same as memoryless in practice."""
    return q > 0, internal


def invariant_reconstruction(q: int, internal: Optional[dict]) -> Tuple[bool, Optional[dict]]:
    """Use accumulated arrivals (bias counter) to decide service.
    Abstraction: accumulate the persistent inflow and act when the accumulator
    indicates excess relative to services already performed.
    """
    internal = internal or {"arrivals": 0, "services": 0}
    internal["arrivals"] += ARRIVAL
    # serve if accumulated excess would otherwise grow
    excess = internal["arrivals"] - internal["services"]
    serve = excess > 0 and q > 0
    if serve:
        internal["services"] += 1
    return serve, internal


# ---------------------------------------------------------------------------
# Adversarial variants
# ---------------------------------------------------------------------------

def run_with_burst(policy, burst_at: int = 10, burst_size: int = 5) -> Dict:
    """Arrival is 1 except one large burst outside historical mild envelope."""
    q = 0
    internal = {}
    overflows = 0
    for t in range(HORIZON):
        arr = burst_size if t == burst_at else ARRIVAL
        serve, internal = policy(q, internal)
        q, ov = step(q, serve, arr)
        if ov:
            overflows += 1
    return {"overflows": overflows, "final_q": q, "success": overflows == 0}


def run_incorrect_invariant(q0: int = 0) -> Dict:
    """Incorrect property: always idle (claimed 'do nothing under mild load')."""
    def bad(q, internal):
        return False, internal
    return run_policy(bad, q0)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=== CDIR Target-Side Reconstruction ===\n")
    print(f"Target: discrete buffer, capacity={CAPACITY}, constant arrival={ARRIVAL}")
    print("Grammar: integer queue, serve/idle only. No signed proportional correction.\n")

    policies = [
        ("target_only_memoryless", memoryless_serve_if_positive),
        ("generic_internal_state", generic_internal_state),
        ("conventional_translation", conventional_translation),
        ("invariant_reconstruction", invariant_reconstruction),
        ("memoryless_always_serve", memoryless_always_serve),
    ]

    counts = {}
    for name, pol in policies:
        c = [0]
        res = run_policy(pol, q0=0, count=c)
        counts[name] = c[0]
        status = "SUCCESS" if res["success"] else "FAIL"
        print(f"{name:28} {status:7} overflows={res['overflows']} avg_q={res['avg_q']:.2f} final={res['final_q']} steps={c[0]}")

    print("\n--- Adversarial: single burst of 5 outside mild envelope ---")
    for name, pol in policies:
        res = run_with_burst(pol)
        status = "SUCCESS" if res["success"] else "FAIL"
        print(f"{name:28} {status:7} overflows={res['overflows']} final={res['final_q']}")

    print("\n--- Incorrect invariant (always idle) ---")
    bad = run_incorrect_invariant()
    print(f"incorrect_always_idle          FAIL     overflows={bad['overflows']} final={bad['final_q']}")

    print("\n--- Disable supposedly load-bearing component (remove accumulator) ---")
    # Reconstruction without the counter falls back to memoryless
    res_no_acc = run_policy(memoryless_serve_if_positive)
    print(f"reconstruction_without_acc     {'SUCCESS' if res_no_acc['success'] else 'FAIL'} (identical to memoryless)")

    print("\nDone. See results.md for interpretation.")


if __name__ == "__main__":
    main()
