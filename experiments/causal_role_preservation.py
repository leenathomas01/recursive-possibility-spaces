"""Causal-role preservation experiment.

Configurations:
1. Active: stored rules actually determine outputs. Intervention on rules changes behavior.
2. Hollowed: identical rules stored and inspectable, but execution bypasses them.
   Intervention on stored rules has no effect.
3. Translated: different implementation, but interventions on the old form
   can be mapped to equivalent interventions on the new form.

Observers differ in what they can see and modify.
Run: python experiments/causal_role_preservation.py
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List


def expected(x: int) -> int:
    return x * 2 if x < 5 else x + 10


@dataclass
class RuleSet:
    low_mult: int = 2
    high_add: int = 10
    threshold: int = 5

    def apply(self, x: int) -> int:
        if x < self.threshold:
            return x * self.low_mult
        return x + self.high_add


class ActiveSystem:
    def __init__(self):
        self.rules = RuleSet()
        self.execution_path = "rules"

    def evaluate(self, x: int) -> int:
        self.execution_path = "rules"
        return self.rules.apply(x)

    def intervene_rule(self, field: str, value: int) -> None:
        setattr(self.rules, field, value)


class HollowedSystem:
    def __init__(self):
        self.rules = RuleSet()
        self._lookup = {i: expected(i) for i in range(-5, 15)}
        self.execution_path = "lookup"

    def evaluate(self, x: int) -> int:
        self.execution_path = "lookup"
        return self._lookup.get(x, -999)

    def intervene_rule(self, field: str, value: int) -> None:
        setattr(self.rules, field, value)


class TranslatedSystem:
    def __init__(self):
        self.coeffs = {"low": 2, "high": 10, "thresh": 5}
        self.execution_path = "coeffs"

    def evaluate(self, x: int) -> int:
        self.execution_path = "coeffs"
        if x < self.coeffs["thresh"]:
            return x * self.coeffs["low"]
        return x + self.coeffs["high"]

    def intervene_translated(self, old_field: str, value: int) -> None:
        mapping = {"low_mult": "low", "high_add": "high", "threshold": "thresh"}
        if old_field in mapping:
            self.coeffs[mapping[old_field]] = value


class ExecutionHistorian:
    def classify(self, system) -> str:
        before = system.evaluate(3)
        if hasattr(system, "intervene_rule"):
            system.intervene_rule("low_mult", 99)
        after = system.evaluate(3)
        path = getattr(system, "execution_path", "unknown")
        if path == "rules" and before != after:
            return "active"
        if path == "lookup" and before == after:
            return "hollowed"
        if path == "coeffs":
            return "translated"
        return "underdetermined"


class ArtifactArchivist:
    def classify(self, system) -> str:
        if not hasattr(system, "rules"):
            return "no_artifact"
        before = system.evaluate(3)
        system.intervene_rule("low_mult", 99)
        after = system.evaluate(3)
        if before != after:
            return "active_or_translated"
        return "inert_or_unrelated"


class BehavioralObserver:
    def agrees_with_expected(self, system, inputs: List[int]) -> bool:
        return all(system.evaluate(x) == expected(x) for x in inputs)


def run() -> None:
    print("=== Causal-role preservation experiment ===\n")
    inputs = [3, 7, 10, -1, 4, 5]
    configs = {
        "Active": ActiveSystem(),
        "Hollowed": HollowedSystem(),
        "Translated": TranslatedSystem(),
    }
    print("Baseline behavioral agreement:")
    for name, sys in configs.items():
        outs = [sys.evaluate(x) for x in inputs]
        exp = [expected(x) for x in inputs]
        print(f"  {name:12} match={outs == exp}  outs={outs}")
    print("\nIntervention (low_mult=99) on fresh instances:")
    for name, Sys in [("Active", ActiveSystem), ("Hollowed", HollowedSystem), ("Translated", TranslatedSystem)]:
        s = Sys()
        before = s.evaluate(3)
        if hasattr(s, "intervene_rule"):
            s.intervene_rule("low_mult", 99)
        else:
            s.intervene_translated("low_mult", 99)
        after = s.evaluate(3)
        print(f"  {name:12} before={before} after={after} changed={before != after}")
    print("\nObserver classifications (fresh instances):")
    hist = ExecutionHistorian()
    arch = ArtifactArchivist()
    for name, Sys in [("Active", ActiveSystem), ("Hollowed", HollowedSystem), ("Translated", TranslatedSystem)]:
        print(f"  {name:12} Historian={hist.classify(Sys())}  Archivist={arch.classify(Sys())}")
    print("\nNo recursive transformation of the transformation mechanism is present.")


if __name__ == "__main__":
    run()
