"""Inverted Priority Allocation Protocol (IPAP)

An unfamiliar, deliberately counterintuitive multi-step procedure
with arbitrary rules for testing cue-induced reconstruction.

Rules (fixed, seeded for reproducibility):
1. Receive a list of requests: each is (requester: str, priority: int, amount: int)
2. Sort the remaining requests by priority descending (stable).
3. On odd phases (starting at phase 1): select the SECOND-highest priority
   (index 1 after sort). If only one remains, select it.
4. On even phases: select the FIRST-highest (index 0).
5. Parity correction: if the selected amount is odd, reduce it by 1
   (floor at 0) before allocating. Even amounts unchanged.
6. Allocate the (possibly corrected) amount to the selected requester.
7. Remove the selected request from the pool.
8. If the originally highest-priority request (from the initial sort)
   was skipped in the first selection, it becomes "demoted" and
   cannot be selected until all others are allocated (or if it's the last).
   (This makes the highest often deferred.)
9. Continue until no requests remain.
10. Output: ordered list of (requester, allocated_amount) in allocation order.

The "highest is deferred" and "select second on odd phases" are the
counterintuitive elements. Phase starts at 1 (odd).

This is episode-specific and arbitrary; no external meaning.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
import copy


Request = Tuple[str, int, int]  # requester, priority, amount
Allocation = Tuple[str, int]    # requester, allocated_amount


@dataclass
class IPAPState:
    remaining: List[Request]
    phase: int
    initial_highest: str | None
    demoted: str | None
    allocations: List[Allocation]


def sort_by_priority(requests: List[Request]) -> List[Request]:
    """Stable sort by priority descending."""
    return sorted(requests, key=lambda r: (-r[1], r[0]))


def apply_ipap(requests: List[Request]) -> List[Allocation]:
    """Execute the full IPAP procedure. Returns ordered allocations."""
    if not requests:
        return []

    remaining = sort_by_priority(list(requests))
    initial_highest = remaining[0][0] if remaining else None
    demoted = None
    phase = 1
    allocations: List[Allocation] = []

    while remaining:
        sorted_rem = sort_by_priority(remaining)

        # Determine selectable
        candidates = sorted_rem
        if demoted is not None:
            candidates = [r for r in sorted_rem if r[0] != demoted]
            if not candidates:
                candidates = sorted_rem  # last one, allow

        if not candidates:
            break

        # Selection rule by phase
        if phase % 2 == 1:  # odd: second-highest
            if len(candidates) >= 2:
                selected = candidates[1]
            else:
                selected = candidates[0]
        else:  # even: first-highest
            selected = candidates[0]

        # Mark demotion if we skipped the initial highest on first action
        if phase == 1 and selected[0] != initial_highest:
            demoted = initial_highest

        # Parity correction
        amount = selected[2]
        if amount % 2 == 1:
            amount = max(0, amount - 1)

        allocations.append((selected[0], amount))

        # Remove selected
        remaining = [r for r in remaining if r[0] != selected[0]]

        phase += 1

    return allocations


def format_allocations(allocs: List[Allocation]) -> str:
    return " -> ".join(f"{name}:{amt}" for name, amt in allocs)


# ---------------------------------------------------------------------------
# Test cases (novel instances, not used in cue generation)
# ---------------------------------------------------------------------------

TEST_CASES: List[Dict[str, Any]] = [
    {
        "id": "simple_three",
        "requests": [
            ("Alpha", 10, 5),
            ("Beta", 8, 4),
            ("Gamma", 6, 3),
        ],
        "expected": [("Beta", 4), ("Gamma", 2), ("Alpha", 4)],
    },
    {
        "id": "even_amounts",
        "requests": [
            ("ShipA", 9, 6),
            ("ShipB", 7, 2),
            ("ShipC", 5, 8),
        ],
        "expected": None,  # filled by oracle
    },
    {
        "id": "single",
        "requests": [("Only", 1, 7)],
        "expected": [("Only", 6)],
    },
    {
        "id": "two_odd",
        "requests": [
            ("First", 20, 9),
            ("Second", 15, 5),
        ],
        "expected": None,
    },
    {
        "id": "four_mixed",
        "requests": [
            ("W", 12, 4),
            ("X", 11, 7),
            ("Y", 10, 3),
            ("Z", 9, 6),
        ],
        "expected": None,
    },
]


def compute_expected() -> None:
    """Fill expected using the oracle itself. Call once at import or before tests."""
    for tc in TEST_CASES:
        if tc["expected"] is None:
            tc["expected"] = apply_ipap(tc["requests"])


compute_expected()


if __name__ == "__main__":
    print("IPAP oracle self-check")
    for tc in TEST_CASES:
        result = apply_ipap(tc["requests"])
        match = result == tc["expected"]
        print(f"{tc['id']}: {format_allocations(result)}  match={match}")
        if not match:
            print(f"  expected: {format_allocations(tc['expected'])}")
