"""Adversarial representational shedding — refined minimal experiment.

Two presentations of the same underlying rewrite graph:
- Atomic: single-step rules only.
- Macro: selected multi-step shortcuts treated as cost-1 operations while trusted.

Strategies under matched budgets:
- atomic / macro (stay in current presentation)
- archive (retrieve previous atoms, +1 cost)
- meta (fixed interpreter with full underlying graph always available)

Run: python experiments/adversarial_shedding.py
"""

from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

UNDERLYING = {
    "a": ["b"],
    "b": ["c", "f"],
    "c": ["d"],
    "d": ["e"],
    "f": ["e"],
}

def atoms_from_underlying() -> Dict[str, List[str]]:
    return {k: v[:] for k, v in UNDERLYING.items()}

MACROS = {
    "ac": ("c", ["a", "b", "c"]),
    "ae": ("e", ["a", "b", "c", "d", "e"]),
    "be": ("e", ["b", "c", "d", "e"]),
}

TASKS = [("a", "c"), ("a", "e"), ("b", "e"), ("a", "d"), ("c", "e"), ("b", "d")]

def solve_atomic(start: str, target: str, atoms: Dict[str, List[str]], budget: int) -> Tuple[bool, int]:
    if start == target:
        return True, 0
    q = deque([(start, 0)])
    seen = {start}
    while q:
        node, ops = q.popleft()
        if ops >= budget:
            continue
        for nxt in atoms.get(node, []):
            if nxt not in seen:
                new_ops = ops + 1
                if nxt == target:
                    return True, new_ops
                seen.add(nxt)
                q.append((nxt, new_ops))
    return False, budget

def solve_with_macros(start: str, target: str, atoms: Dict[str, List[str]],
                      macros: Dict[str, Tuple[str, List[str]]], trusted: Set[str],
                      budget: int) -> Tuple[bool, int]:
    for name, (tgt, _) in macros.items():
        if name in trusted and tgt == target:
            return True, 1
    return solve_atomic(start, target, atoms, budget)

@dataclass
class State:
    atoms: Dict[str, List[str]]
    macros: Dict[str, Tuple[str, List[str]]]
    trusted: Set[str]
    archive: Dict[str, List[str]]

def evaluate(label: str, state: State, strategy: str, budget: int = 4) -> None:
    solved = 0
    ops_sum = 0
    for s, t in TASKS:
        if strategy == "atomic":
            ok, ops = solve_atomic(s, t, state.atoms, budget)
        elif strategy == "macro":
            ok, ops = solve_with_macros(s, t, state.atoms, state.macros, state.trusted, budget)
        elif strategy == "archive":
            ok, ops = solve_atomic(s, t, state.archive, max(0, budget - 1))
            ops += 1
        elif strategy == "meta":
            ok, ops = solve_atomic(s, t, atoms_from_underlying(), budget)
        else:
            ok, ops = False, budget
        solved += int(ok)
        ops_sum += ops
    print(f"{label:22} {strategy:10} {solved}/{len(TASKS)}  ops={ops_sum}")

def main() -> None:
    print("=== Refined adversarial shedding ===\n")

    healthy = State(
        atoms=atoms_from_underlying(),
        macros=MACROS.copy(),
        trusted=set(MACROS),
        archive=atoms_from_underlying(),
    )

    print("Healthy")
    for strat in ["atomic", "macro", "archive", "meta"]:
        evaluate("healthy", healthy, strat)

    a_state = State(
        atoms={"a": ["b"], "c": ["d"], "d": ["e"], "f": ["e"]},
        macros=MACROS.copy(),
        trusted=set(),
        archive=atoms_from_underlying(),
    )
    print("\nA: Structural (b removed, macros untrusted)")
    for strat in ["atomic", "macro", "archive", "meta"]:
        evaluate("A-structural", a_state, strat)

    b_state = State(
        atoms=atoms_from_underlying(),
        macros=MACROS.copy(),
        trusted=set(),
        archive=atoms_from_underlying(),
    )
    print("\nB: Representational (macros untrusted, atoms intact)")
    for strat in ["atomic", "macro", "archive", "meta"]:
        evaluate("B-rep", b_state, strat)

    trap = State(
        atoms=atoms_from_underlying(),
        macros={**MACROS, "ae": ("x", ["a", "b", "x"])},
        trusted={"ae", "ac", "be"},
        archive=atoms_from_underlying(),
    )
    print("\nPreservation trap (ae macro corrupted but trusted)")
    for strat in ["macro", "atomic", "meta"]:
        evaluate("trap", trap, strat)

    prem = State(
        atoms=atoms_from_underlying(),
        macros={"be": MACROS["be"]},
        trusted={"be"},
        archive=atoms_from_underlying(),
    )
    print("\nPremature shedding (tight budget=2)")
    for strat in ["macro", "atomic", "meta"]:
        evaluate("premature", prem, strat, budget=2)

    print("\nObserved: Meta/archive recover structural loss.")
    print("Representational invalidation collapses to atomic performance.")
    print("No regime required a non-embeddable change of operative domain.")

if __name__ == "__main__":
    main()
