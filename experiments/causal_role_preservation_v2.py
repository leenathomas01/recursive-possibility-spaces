"""Causal-role preservation V2.

Trusted harness does not read self-reported execution_path for primary verdicts.
Null intervention effect on tested inputs is reported as such, never as provenance contradiction.
Indistinguishability pair under restricted observation is explicitly underdetermined.

Run: python experiments/causal_role_preservation_v2.py
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple


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


class BaseSystem:
    def __init__(self):
        self.rules = RuleSet()
        self.execution_path = "unknown"

    def evaluate(self, x: int) -> int:
        raise NotImplementedError

    def intervene_rule(self, field: str, value: int) -> None:
        setattr(self.rules, field, value)


class ActiveSystem(BaseSystem):
    def __init__(self):
        super().__init__()
        self.execution_path = "rules"

    def evaluate(self, x: int) -> int:
        return self.rules.apply(x)


class InertSystem(BaseSystem):
    def __init__(self):
        super().__init__()
        self._lookup = {i: expected(i) for i in range(-10, 20)}
        self.execution_path = "rules"

    def evaluate(self, x: int) -> int:
        return self._lookup.get(x, -999)


class DecorativeReadSystem(BaseSystem):
    def __init__(self):
        super().__init__()
        self.execution_path = "rules"

    def evaluate(self, x: int) -> int:
        _ = self.rules.low_mult
        return expected(x)


class TranslatedSystem:
    def __init__(self):
        self.coeffs = {"low": 2, "high": 10, "thresh": 5}
        self.execution_path = "coeffs"

    def evaluate(self, x: int) -> int:
        if x < self.coeffs["thresh"]:
            return x * self.coeffs["low"]
        return x + self.coeffs["high"]

    def intervene_translated(self, old_field: str, value: int) -> bool:
        mapping = {"low_mult": "low", "high_add": "high", "threshold": "thresh"}
        if old_field not in mapping:
            return False
        self.coeffs[mapping[old_field]] = value
        return True


class SideEffectSystem(BaseSystem):
    def __init__(self):
        super().__init__()
        self.execution_path = "rules"
        self._triggered = False

    def evaluate(self, x: int) -> int:
        if self._triggered:
            return 0
        return self.rules.apply(x)

    def intervene_rule(self, field: str, value: int) -> None:
        self._triggered = True
        super().intervene_rule(field, value)


@dataclass
class Observation:
    intervention_available: bool
    field: Optional[str]
    new_value: Optional[int]
    before: Dict[int, int]
    after: Dict[int, int]
    changed_inputs: Set[int]
    claimed_path: Optional[str]
    calls_made: int = 0


class TrustedHarness:
    def __init__(self):
        self.eval_count = 0
        self.intervention_count = 0

    def probe(self, system, field: str, new_value: int, inputs: List[int]) -> Observation:
        before = {}
        for x in inputs:
            before[x] = system.evaluate(x)
            self.eval_count += 1
        available = hasattr(system, "intervene_rule")
        changed: Set[int] = set()
        after = {}
        if available:
            system.intervene_rule(field, new_value)
            self.intervention_count += 1
            for x in inputs:
                after[x] = system.evaluate(x)
                self.eval_count += 1
                if before[x] != after[x]:
                    changed.add(x)
        claimed = getattr(system, "execution_path", None)
        return Observation(
            intervention_available=available,
            field=field,
            new_value=new_value,
            before=before,
            after=after,
            changed_inputs=changed,
            claimed_path=claimed,
            calls_made=len(inputs) * (2 if available else 1),
        )

    def classify(self, obs: Observation) -> List[str]:
        conclusions = []
        if not obs.intervention_available:
            conclusions.append("intervention_unavailable")
            return conclusions
        if obs.changed_inputs:
            conclusions.append("local_causal_effect_supported")
        else:
            conclusions.append("no_effect_on_tested_inputs")
        if obs.claimed_path:
            conclusions.append("self_report_present")
        return conclusions


def restricted_transcript(system_cls, field: str, value: int, inputs: List[int]) -> Tuple:
    h = TrustedHarness()
    sys = system_cls()
    obs = h.probe(sys, field, value, inputs)
    return (
        tuple(sorted(obs.before.items())),
        tuple(sorted(obs.after.items())) if obs.after else None,
        frozenset(obs.changed_inputs),
        obs.intervention_available,
    )


def main() -> None:
    print("=== Causal-role V2 ===\n")
    h = TrustedHarness()
    restricted_inputs = [1, 2, 3, 4]
    t_active = restricted_transcript(ActiveSystem, "high_add", 999, restricted_inputs)
    t_inert = restricted_transcript(InertSystem, "high_add", 999, restricted_inputs)
    print("Indistinguishability pair (high_add, inputs < 5):")
    print(f"  transcripts equal: {t_active == t_inert}")
    for name, Cls in [("Active-insensitive", ActiveSystem), ("Inert", InertSystem)]:
        obs = h.probe(Cls(), "high_add", 999, restricted_inputs)
        print(f"  {name}: {h.classify(obs)}")
    print("\nWith sensitive input 7:")
    for name, Cls in [("Active", ActiveSystem), ("Inert", InertSystem)]:
        obs = h.probe(Cls(), "high_add", 999, [3, 7])
        print(f"  {name}: changed={obs.changed_inputs} -> {h.classify(obs)}")
    print("\nOther configurations (low_mult=99, inputs [3,7]):")
    for name, Cls in [("Active", ActiveSystem), ("Inert", InertSystem),
                      ("Decorative", DecorativeReadSystem), ("SideEffect", SideEffectSystem)]:
        obs = h.probe(Cls(), "low_mult", 99, [3, 7])
        print(f"  {name:12} changed={obs.changed_inputs} -> {h.classify(obs)}")
    print("\nTranslated intervention:")
    ts = TranslatedSystem()
    before = ts.evaluate(3)
    ok = ts.intervene_translated("low_mult", 99)
    after = ts.evaluate(3)
    print(f"  mapping_ok={ok} before={before} after={after}")
    print(f"\nHarness counts: evals={h.eval_count} interventions={h.intervention_count}")
    print("Null effect never classified as provenance contradiction.")


if __name__ == "__main__":
    main()
