"""V2: executable composite operations with explicit, bounded accounting.

Run: python formalizations/toy_rewriter_v2.py [--seed 7] [--repetitions 12]
Standard library only. Illustrates macro compilation and limited-search tradeoffs,
NOT ontological state-space change, unrestricted RSI, or new computability.
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

Rule = tuple[str, str]
BASE: tuple[Rule, ...] = (("a", "b"), ("b", "c"), ("c", "d"))


@dataclass(frozen=True)
class Result:
    success: bool
    cost: int  # number of rule applications attempted (candidate edges)
    path: tuple[Rule, ...]


def search(start: str, goal: str, rules: tuple[Rule, ...], *, budget: int, depth: int = 3) -> Result:
    """Deterministic BFS; each applicable candidate costs 1, including discarded ones.

    Budget is a cap on tested candidate edges, not elapsed time or wall-clock compute.
    Operates on single-token states, so a->c is exactly the composition a->b->c.
    """
    if start == goal:
        return Result(True, 0, ())
    frontier: list[tuple[str, tuple[Rule, ...]]] = [(start, ())]
    visited = {start}
    cost = 0
    for _ in range(depth):
        next_frontier = []
        for current, path in frontier:
            for source, target in rules:
                if source != current:
                    continue
                if cost >= budget:
                    return Result(False, cost, ())
                cost += 1
                step = (source, target)
                new_path = path + (step,)
                if target == goal:
                    return Result(True, cost, new_path)
                if target not in visited:
                    visited.add(target)
                    next_frontier.append((target, new_path))
        frontier = next_frontier
        if not frontier:
            break
    return Result(False, cost, ())


def compile_macro(path: tuple[Rule, ...]) -> Rule:
    """Only compile a contiguous chain; never fabricate a rule from a label."""
    if len(path) < 2 or any(left[1] != right[0] for left, right in zip(path, path[1:])):
        raise ValueError("requires a real, composable multi-step path")
    return (path[0][0], path[-1][1])


def experiment(seed: int = 7, repetitions: int = 12) -> dict:
    if repetitions < 1:
        raise ValueError("repetitions must be >= 1")
    # The discovery phase is part of the promoter's total cost.
    discovery = search("a", "c", BASE, budget=10, depth=3)
    assert discovery.success and len(discovery.path) == 2
    macro = compile_macro(discovery.path)
    compile_cost = 1  # stipulated accounting unit, not a measured runtime
    promoted = (macro,) + BASE  # macro-first creates search interference under tight budgets

    tasks = ([("a", "c", 1)] * repetitions  # macro useful on a held-out repetition
             + [("a", "b", 1)] * repetitions  # old one-step task displaced by the macro
             + [("b", "d", 2)] * repetitions) # unchanged transfer task
    rng = random.Random(seed)
    rng.shuffle(tasks)
    summaries = {"flat": {"success": 0, "cost": 0},
                 "promoted": {"success": 0, "cost": 0}}
    per_task = {}
    for start, goal, budget in tasks:
        label = f"{start}->{goal} (budget={budget})"
        per_task.setdefault(label, {"flat_ok": 0, "promoted_ok": 0,
                                    "flat_cost": 0, "promoted_cost": 0, "n": 0})
        old = search(start, goal, BASE, budget=budget)
        new = search(start, goal, promoted, budget=budget)
        per_task[label]["n"] += 1
        for key, result in (("flat", old), ("promoted", new)):
            summaries[key]["success"] += int(result.success)
            summaries[key]["cost"] += result.cost
        for prefix, result in (("flat", old), ("promoted", new)):
            per_task[label][f"{prefix}_ok"] += int(result.success)
            per_task[label][f"{prefix}_cost"] += result.cost

    # Recovery: attempt with present regime, then explicitly load the old rule set.
    # Task-specific budget is 1 per stage. Total recovery accounting includes the failed probe.
    recovery_probe = search("a", "b", promoted, budget=1)
    archive_lookup_cost = 1  # stipulated bookkeeping cost, not measured runtime
    recovery_old = search("a", "b", BASE, budget=1)
    recovery_total = recovery_probe.cost + archive_lookup_cost + recovery_old.cost
    return {"seed": seed, "macro": macro, "discovery_cost": discovery.cost,
            "compile_cost": compile_cost, "tasks": per_task,
            "summaries": summaries, "promoted_total_cost": summaries["promoted"]["cost"] + discovery.cost + compile_cost,
            "flat_total_cost": summaries["flat"]["cost"],
            "recovery": {"first_success": recovery_probe.success,
                         "archive_success": recovery_old.success,
                         "total_cost": recovery_total}}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--repetitions", type=int, default=12)
    args = parser.parse_args()
    out = experiment(args.seed, args.repetitions)
    print(f"macro={out['macro']} | discovery={out['discovery_cost']} + compile={out['compile_cost']} accounting units")
    for task, v in sorted(out["tasks"].items()):
        print(f"{task}: flat={v['flat_ok']}/{v['n']} cost={v['flat_cost']}; "
              f"promoted={v['promoted_ok']}/{v['n']} cost={v['promoted_cost']}")
    print(f"overall: flat={out['summaries']['flat']} total_cost={out['flat_total_cost']}; "
          f"promoted={out['summaries']['promoted']} including_build_cost={out['promoted_total_cost']}")
    print(f"recovery old task a->b: {out['recovery']}")


if __name__ == "__main__":
    main()
