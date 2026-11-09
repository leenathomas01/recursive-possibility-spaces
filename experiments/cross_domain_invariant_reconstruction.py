"""Cross-domain invariant reconstruction toy experiment.

Source domain: scalar proportional feedback that drives an integer position to zero.
Target domain: two non-negative integer reservoirs that must be equalized by unit transfers.
Grammars differ: signed scalar update vs. conditional pair transfer under non-negativity.

Compares:
- Direct copy (source logic forced onto mismatched state)
- Conventional translation (difference mapped to source step, delta interpreted as transfer)
- Target-only search (limited random/heuristic search without source knowledge)
- Invariant reconstruction (explicit imbalance + corrective transfer)

Includes adversarial variants and a negative-control incorrect invariant.
Resource budgets are comparable (simulation steps / trials).

Run: python experiments/cross_domain_invariant_reconstruction.py
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple
import random


# ---------------------------------------------------------------------------
# Source domain
# ---------------------------------------------------------------------------

def source_feedback(p: int) -> int:
    """Unit proportional feedback. Causal role: oppose the sign of error."""
    if p > 0:
        return p - 1
    if p < 0:
        return p + 1
    return p


def source_misleading(p: int) -> int:
    """Works only for non-negative starts (incidental environmental condition)."""
    if p > 0:
        return p - 1
    return p  # does nothing for negative; historically "succeeded" on positive test set


# ---------------------------------------------------------------------------
# Target domain
# ---------------------------------------------------------------------------

State = Tuple[int, int]  # (left, right), non-negative


def is_balanced(s: State) -> bool:
    """Exact equality. Impossible when total token count is odd."""
    return s[0] == s[1]


def min_achievable_imbalance(s: State) -> int:
    """Conservation of tokens implies parity constraint."""
    total = s[0] + s[1]
    return 0 if total % 2 == 0 else 1


def is_optimal(s: State) -> bool:
    return imbalance(s) <= min_achievable_imbalance(s)


def imbalance(s: State) -> int:
    return abs(s[0] - s[1])


def transfer(s: State, from_left: bool) -> State:
    left, right = s
    if from_left and left > 0:
        return (left - 1, right + 1)
    if not from_left and right > 0:
        return (left + 1, right - 1)
    return s  # no-op if source empty


# ---------------------------------------------------------------------------
# Intermediate representation / invariants
# ---------------------------------------------------------------------------

@dataclass
class Invariants:
    measure: str
    corrective_direction: str
    notes: str = ""


def extract_invariants_correct() -> Invariants:
    return Invariants(
        measure="absolute difference of the two reservoirs",
        corrective_direction="transfer one unit from the larger reservoir to the smaller",
        notes="preserves non-negativity; reduces imbalance by 2 (or 1 if odd)",
    )


def extract_invariants_incorrect() -> Invariants:
    return Invariants(
        measure="absolute difference",
        corrective_direction="always transfer from left to right",
        notes="negative control: directionally wrong half the time",
    )


# ---------------------------------------------------------------------------
# Mechanisms / policies
# ---------------------------------------------------------------------------

def reconstructed_policy(s: State) -> State:
    left, right = s
    if imbalance(s) <= min_achievable_imbalance(s):
        return s
    if left > right:
        return transfer(s, from_left=True)
    if right > left:
        return transfer(s, from_left=False)
    return s


def incorrect_reconstructed_policy(s: State) -> State:
    # always try left -> right
    return transfer(s, from_left=True)


def conventional_translation(s: State) -> State:
    """Ordinary mapping: treat signed difference as source position.
    Apply source step to the difference and realize the resulting change
    by a unit transfer in the appropriate direction.
    Stops when further transfer cannot improve the achievable imbalance.
    """
    if imbalance(s) <= min_achievable_imbalance(s):
        return s
    left, right = s
    d = left - right
    new_d = source_feedback(d)
    delta = new_d - d
    if delta < 0 and left > 0:
        return transfer(s, from_left=True)
    if delta > 0 and right > 0:
        return transfer(s, from_left=False)
    return s


def direct_copy_attempt(s: State) -> State:
    """Force source logic onto an ill-chosen scalar projection (sum).
    The action is applied without reference to which reservoir is larger.
    Typically reduces a fixed side, which does not systematically balance.
    """
    total = s[0] + s[1]
    new_total = source_feedback(total)
    if new_total < total and s[0] > 0:
        # always prefer to reduce left, regardless of comparison
        return (s[0] - 1, s[1])
    return s


def target_only_random_policy(s: State, rng: random.Random) -> State:
    """Uninformed random transfer or no-op."""
    choice = rng.choice([True, False, None])
    if choice is None:
        return s
    return transfer(s, from_left=choice)


# ---------------------------------------------------------------------------
# Evaluation harness
# ---------------------------------------------------------------------------

@dataclass
class Result:
    method: str
    success: bool
    steps: int
    final_imbalance: int
    budget_used: int
    notes: str = ""


def run_policy(
    start: State,
    policy: Callable[[State], State],
    max_steps: int = 20,
) -> Tuple[bool, int, int]:
    s = start
    target_imb = min_achievable_imbalance(start)
    for step in range(1, max_steps + 1):
        if imbalance(s) <= target_imb:
            return True, step - 1, imbalance(s)
        s = policy(s)
        if imbalance(s) <= target_imb:
            return True, step, imbalance(s)
    return False, max_steps, imbalance(s)


def evaluate_all(start: State, budget: int = 30, seed: int = 42) -> List[Result]:
    results = []
    rng = random.Random(seed)

    # 1. Direct copy
    ok, steps, imb = run_policy(start, direct_copy_attempt, max_steps=budget)
    results.append(Result("direct_copy", ok, steps, imb, steps, "projected sum onto source feedback"))

    # 2. Conventional translation
    ok, steps, imb = run_policy(start, conventional_translation, max_steps=budget)
    results.append(Result("conventional_translation", ok, steps, imb, steps, "difference <-> source step"))

    # 3. Target-only search (random trials under budget)
    trials = budget // 5
    best_ok = False
    best_steps = budget
    target_imb = min_achievable_imbalance(start)
    for _ in range(trials):
        s = start
        for t in range(1, 11):
            if imbalance(s) <= target_imb:
                best_ok = True
                best_steps = min(best_steps, t - 1)
                break
            s = target_only_random_policy(s, rng)
            if imbalance(s) <= target_imb:
                best_ok = True
                best_steps = min(best_steps, t)
                break
    results.append(Result(
        "target_only_search",
        best_ok,
        best_steps if best_ok else budget,
        0 if best_ok else imbalance(start),
        trials * 5,
        f"{trials} random rollouts of length <=10",
    ))

    # 4. Invariant reconstruction (correct)
    # Charge a small extraction cost
    extraction_cost = 2
    ok, steps, imb = run_policy(start, reconstructed_policy, max_steps=budget - extraction_cost)
    results.append(Result(
        "invariant_reconstruction",
        ok,
        steps,
        imb,
        steps + extraction_cost,
        extract_invariants_correct().corrective_direction,
    ))

    # Negative control: incorrect invariant
    ok, steps, imb = run_policy(start, incorrect_reconstructed_policy, max_steps=budget)
    results.append(Result(
        "incorrect_invariant",
        ok,
        steps,
        imb,
        steps,
        extract_invariants_incorrect().corrective_direction,
    ))

    return results


def adversarial_capacity(start: State, capacity: int = 5) -> Dict[str, Result]:
    """Target reservoirs cannot exceed capacity; transfers that would overflow are blocked."""
    def capped_transfer(s: State, from_left: bool) -> State:
        left, right = s
        if from_left and left > 0 and right < capacity:
            return (left - 1, right + 1)
        if not from_left and right > 0 and left < capacity:
            return (left + 1, right - 1)
        return s

    def capped_recon(s: State) -> State:
        if imbalance(s) <= min_achievable_imbalance(s):
            return s
        left, right = s
        if left > right:
            return capped_transfer(s, True)
        if right > left:
            return capped_transfer(s, False)
        return s

    ok, steps, imb = run_policy(start, capped_recon, max_steps=30)
    return {
        "capped_reconstruction": Result("capped_reconstruction", ok, steps, imb, steps, f"capacity={capacity}")
    }


def multi_source_conflict(start: State) -> Result:
    """Second source mechanism wants to maximize difference (conflicting requirement)."""
    def conflicting_policy(s: State) -> State:
        # alternate between balancing and anti-balancing
        left, right = s
        if random.random() < 0.5:
            return reconstructed_policy(s)
        # anti: transfer from smaller to larger
        if left < right and right > 0:
            return transfer(s, from_left=False)  # increase difference
        if right < left and left > 0:
            return transfer(s, from_left=True)
        return s

    ok, steps, imb = run_policy(start, conflicting_policy, max_steps=20)
    return Result("multi_source_conflict", ok, steps, imb, steps, "random mix of balance and anti-balance")


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    print("=== Cross-Domain Invariant Reconstruction ===\n")
    starts = [(5, 1), (3, 8), (0, 4), (7, 7), (2, 2)]

    for start in starts:
        print(f"Start state {start} (imbalance={imbalance(start)})")
        for r in evaluate_all(start, budget=25, seed=hash(start) % 10000):
            status = "SUCCESS" if r.success else "FAIL"
            print(f"  {r.method:28} {status:7} steps={r.steps:2} budget={r.budget_used:2} final_imb={r.final_imbalance}")
        print()

    print("--- Adversarial: capacity constraint ---")
    adv = adversarial_capacity((4, 1), capacity=3)
    for name, r in adv.items():
        print(f"  {name}: success={r.success} steps={r.steps} notes={r.notes}")

    print("\n--- Multi-source conflict ---")
    conf = multi_source_conflict((6, 2))
    print(f"  success={conf.success} steps={conf.steps} final_imb={conf.final_imbalance}")

    print("\n--- Misleading source (only works for non-negative) ---")
    # Source domain check
    print("Source feedback on -3:", source_feedback(-3))
    print("Misleading source on -3:", source_misleading(-3))
    print("Misleading source on +3:", source_misleading(3))

    print("\nDone. See results markdown for interpretation.")


if __name__ == "__main__":
    main()
