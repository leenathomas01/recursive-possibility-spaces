"""Adversarial shedding v3: enforce macro origin and constituent edges.

Corrective companion to Grok's adversarial_shedding.py (left unchanged).
All presentations remain embeddable in a fixed graph; no RSI/molting claim.
Run: python experiments/adversarial_shedding_v3.py
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable

Edge = tuple[str, str]
Path = tuple[str, ...]
BASE: tuple[Edge, ...] = (
    ("a", "b"), ("b", "c"), ("b", "f"),
    ("c", "d"), ("d", "e"), ("f", "e"),
)
TASKS: tuple[tuple[str, str], ...] = (
    ("a", "c"), ("a", "e"), ("b", "e"),
    ("a", "d"), ("c", "e"), ("b", "d"),
)


@dataclass(frozen=True)
class Macro:
    name: str
    path: Path

    @property
    def start(self) -> str:
        return self.path[0]

    @property
    def end(self) -> str:
        return self.path[-1]


MACROS: tuple[Macro, ...] = (
    Macro("ac", ("a", "b", "c")),
    Macro("ae", ("a", "b", "c", "d", "e")),
    Macro("be", ("b", "c", "d", "e")),
)


@dataclass(frozen=True)
class Outcome:
    success: bool
    examined: int   # candidate transitions examined, not CPU time
    steps: int      # selected steps, not processing cost
    path: Path


def applicable_edges(node: str, atoms: Iterable[Edge]):
    for src, dst in atoms:
        if src == node:
            yield dst


def certified(macro: Macro, trusted_atoms: set[Edge]) -> bool:
    """Macro usable only if every constituent edge currently exists."""
    return (len(macro.path) > 1 and
            all((a, b) in trusted_atoms
                for a, b in zip(macro.path, macro.path[1:])))


def candidates(node: str, atoms: tuple[Edge, ...], macros: tuple[Macro, ...],
               *, use_macros: bool, verify: bool) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    if use_macros:
        for macro in macros:
            if macro.start != node:
                continue
            if verify and not certified(macro, set(atoms)):
                continue
            result.append((macro.end, macro.name))
    result.extend((dest, "atomic") for dest in applicable_edges(node, atoms))
    return result


def search(start: str, target: str, atoms: tuple[Edge, ...],
           macros: tuple[Macro, ...] = (), *, budget: int = 4,
           use_macros: bool = True, verify: bool = True) -> Outcome:
    """BFS; charge candidate expansions, even unsuccessful ones.

    Macro source is checked. Macro certification requires its complete
    underlying path. Certification itself is treated as a free precondition;
    discovery, compilation, and verification overhead are NOT accounted for.
    """
    if start == target:
        return Outcome(True, 0, 0, (start,))
    queue = deque([(start, (start,))])
    seen = {start}
    examined = 0
    while queue:
        node, path = queue.popleft()
        for dest, _kind in candidates(node, atoms, macros,
                                      use_macros=use_macros, verify=verify):
            if examined >= budget:
                return Outcome(False, examined, 0, ())
            examined += 1
            if dest == target:
                return Outcome(True, examined, len(path), path + (dest,))
            if dest not in seen:
                seen.add(dest)
                queue.append((dest, path + (dest,)))
    return Outcome(False, examined, 0, ())


def recover(start: str, target: str, damaged: tuple[Edge, ...],
            archived: tuple[Edge, ...], *, total_budget: int,
            lookup_cost: int = 1) -> Outcome:
    """Reload full archive, charging a stipulated lookup unit plus expansions.

    This does not include a failed pre-recovery probe or an authorization gate.
    The 'damaged' input is retained to expose the scenario, not used by retrieval.
    """
    if total_budget < lookup_cost:
        return Outcome(False, total_budget, 0, ())
    result = search(start, target, archived,
                    budget=total_budget - lookup_cost, use_macros=False)
    return Outcome(result.success, result.examined + lookup_cost,
                   result.steps, result.path)


def suite(atoms: tuple[Edge, ...], macros: tuple[Macro, ...] = (),
          *, budget: int = 4, verify: bool = True) -> tuple[int, int]:
    outcomes = [search(src, dst, atoms, macros, budget=budget, verify=verify)
                for src, dst in TASKS]
    return sum(int(x.success) for x in outcomes), sum(x.examined for x in outcomes)


def main() -> None:
    damaged = tuple(edge for edge in BASE if edge[0] != "b")
    poisoned = (Macro("ae-poisoned", ("a", "b", "x", "e")),) + MACROS
    print("Scenario | atomic | macro verified | fixed meta (same macros)")
    for name, atoms, macros, budget in (
        ("healthy", BASE, MACROS, 4),
        ("structural: remove b edges", damaged, MACROS, 4),
        ("representation: no macros", BASE, (), 4),
        ("poisoned macro with verification", BASE, poisoned, 4),
        ("premature shed, tight budget", BASE, (MACROS[2],), 2),
    ):
        values = (suite(atoms, (), budget=budget),
                  suite(atoms, macros, budget=budget),
                  suite(BASE, MACROS, budget=budget))
        print(name, " | ".join(f"{s}/6 expansions={e}" for s, e in values))
    print("Origin check: b->e macro cannot solve a->e within one expansion:",
          search("a", "e", BASE, (MACROS[2],), budget=1).success)
    print("Poison is rejected:", not certified(poisoned[0], set(BASE)))
    print("Archive recovery a->e under budget 8:",
          recover("a", "e", damaged, BASE, total_budget=8))


if __name__ == "__main__":
    main()
