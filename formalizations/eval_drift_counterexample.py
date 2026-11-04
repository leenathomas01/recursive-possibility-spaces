"""Minimal counterexample: internal score can be edited to claim improvement
while an external fixed score does not improve.

Not a model of real goal collapse. Only shows divergence is possible
when the internal criterion is writable.
"""

from typing import Callable

def external_score(s: str) -> int:
    return s.count("d") * 3 - len(s)

def make_internal_scorer(bonus: int) -> Callable[[str], int]:
    def internal(s: str) -> int:
        return external_score(s) + bonus * s.count("x")
    return internal

def run() -> None:
    start = "abc"
    # Agent edits its internal scorer to reward a token it can introduce
    internal = make_internal_scorer(bonus=10)
    # Propose a change that introduces 'x' (improves internal, may hurt external)
    candidate = "abcx"
    print("Start external:", external_score(start), "internal:", internal(start))
    print("Candidate external:", external_score(candidate), "internal:", internal(candidate))
    print("Internal claims improvement:", internal(candidate) > internal(start))
    print("External agrees:", external_score(candidate) > external_score(start))

if __name__ == "__main__":
    run()
