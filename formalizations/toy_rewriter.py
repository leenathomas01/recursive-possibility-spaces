"""Minimal operative-regime string rewriter.

Promotes frequently useful composite rewrite sequences into new atomic rules.
Designed as a toy for distinguishing state change, representation change,
and operative-domain change under resource bounds.

Not a theory. Not RSI. Just a small object you can break.
"""

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Core types
# ---------------------------------------------------------------------------

Rule = Tuple[str, str]  # pattern -> replacement


@dataclass
class Regime:
    rules: Dict[str, str]
    generation: int = 0
    history: List[Dict[str, str]] = field(default_factory=list)

    def copy(self) -> Regime:
        return Regime(
            rules=self.rules.copy(),
            generation=self.generation,
            history=self.history.copy(),
        )


# ---------------------------------------------------------------------------
# Simple string rewriting
# ---------------------------------------------------------------------------

def apply_rule(s: str, pattern: str, repl: str) -> Optional[str]:
    if pattern in s:
        return s.replace(pattern, repl, 1)
    return None


def score(s: str) -> int:
    """Toy external score: prefer strings that contain 'd' and are shorter."""
    return s.count("d") * 3 - len(s)


# ---------------------------------------------------------------------------
# Limited-depth probe (the "pulse")
# ---------------------------------------------------------------------------

def probe(
    regime: Regime,
    start: str,
    max_depth: int = 3,
    beam: int = 4,
    rng: random.Random | None = None,
) -> List[Tuple[List[Rule], str, int]]:
    """Return high-value sequences found under a tight budget."""
    rng = rng or random.Random(0)
    results = []

    # BFS-like limited beam search over rule sequences
    frontier = [(start, [], 0)]  # string, path, cost
    for _ in range(max_depth):
        next_frontier = []
        for current, path, cost in frontier:
            for pat, repl in regime.rules.items():
                nxt = apply_rule(current, pat, repl)
                if nxt is None:
                    continue
                new_path = path + [(pat, repl)]
                new_cost = cost + 1
                sc = score(nxt)
                results.append((new_path, nxt, sc))
                next_frontier.append((nxt, new_path, new_cost))
        # Keep only the best beam
        next_frontier.sort(key=lambda x: score(x[0]), reverse=True)
        frontier = next_frontier[:beam]
        if not frontier:
            break

    # Return the most valuable sequences (by final score)
    results.sort(key=lambda x: x[2], reverse=True)
    return results[:5]


# ---------------------------------------------------------------------------
# Promotion
# ---------------------------------------------------------------------------

def promote(regime: Regime, composite: List[Rule]) -> Regime:
    """Promote a sequence into a single new atomic rule (naive concatenation)."""
    if not composite:
        return regime
    # For the toy we just invent a new pattern that stands for the sequence.
    # Real systems would need a proper macro or learned abstraction.
    new_pat = "COMP" + str(regime.generation)
    # Approximate net effect by applying the sequence to a probe string
    probe_str = "abc"
    result = probe_str
    for pat, repl in composite:
        r = apply_rule(result, pat, repl)
        if r is not None:
            result = r
    new_repl = result if result != probe_str else "d"

    new_regime = regime.copy()
    new_regime.history.append(regime.rules.copy())
    new_regime.rules[new_pat] = new_repl
    new_regime.generation += 1
    return new_regime


# ---------------------------------------------------------------------------
# Main loop (very small)
# ---------------------------------------------------------------------------

def run_toy(steps: int = 20, seed: int = 0) -> None:
    rng = random.Random(seed)
    regime = Regime(rules={"ab": "c", "bc": "d", "cd": "a"})

    print(f"Initial regime {regime.generation}: {regime.rules}")

    for step in range(steps):
        start = rng.choice(["abc", "bcd", "abcd", "abbc"])
        found = probe(regime, start, max_depth=3, beam=3, rng=rng)

        if found and found[0][2] > score(start) + 1:
            # Promote the best composite if it looks useful
            best_path = found[0][0]
            if len(best_path) >= 2:  # only promote real composites
                regime = promote(regime, best_path)
                print(
                    f"Step {step}: promoted composite -> regime {regime.generation}"
                )
                print(f"  new rules: {regime.rules}")

        # Occasional recovery probe against previous grain
        if regime.generation > 0 and step % 5 == 0:
            old_rules = regime.history[-1]
            old_regime = Regime(rules=old_rules)
            old_found = probe(old_regime, start, max_depth=3, beam=3, rng=rng)
            print(
                f"  recovery probe (old grain) best score: {old_found[0][2] if old_found else 'n/a'}"
            )

    print("\nFinal regime:", regime.generation)
    print("Final rules:", regime.rules)
    print("History length:", len(regime.history))


if __name__ == "__main__":
    run_toy()
