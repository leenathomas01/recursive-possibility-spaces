"""Source-side knowledge extraction probe for cross-domain invariant reconstruction.

This experiment examines only what can be recovered from operating histories
and controlled interventions on a discrete control system. No target-domain
reconstruction is performed.

Plant: x[t+1] = x[t] + applied_u[t] + w[t]
applied_u = clip(u, -u_max, u_max)

Controllers:
- P: proportional, u = -Kp * x
- PI: proportional-integral with accumulated error
- Limited: proportional with tight actuator saturation and history of only mild disturbances

Histories deliberately leave some conditions unexplored.
Extraction procedures see only the history (or additional probes); ground-truth
implementation details are available only to the evaluator.

Run: python experiments/cdir_source_probe/source_probe.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple
import random


# ---------------------------------------------------------------------------
# Plant and controllers
# ---------------------------------------------------------------------------

@dataclass
class PlantConfig:
    u_max: float = 1.0
    horizon: int = 30
    success_threshold: float = 0.15
    settle_steps: int = 15


def clip(u: float, u_max: float) -> float:
    return max(-u_max, min(u_max, u))


def simulate(
    controller: Callable[[float, Optional[float]], Tuple[float, Optional[float]]],
    x0: float,
    w_seq: List[float],
    config: PlantConfig,
    count_steps: List[int] | None = None,
) -> Dict:
    """Run one episode. controller(x, integral) -> (u, new_integral)."""
    x = x0
    integral: Optional[float] = 0.0
    traj = [x]
    applied = []
    for t, w in enumerate(w_seq[: config.horizon]):
        u, integral = controller(x, integral)
        au = clip(u, config.u_max)
        x = x + au + w
        traj.append(x)
        applied.append(au)
        if count_steps is not None:
            count_steps[0] += 1
    final = traj[-1]
    settled = all(abs(v) < config.success_threshold for v in traj[-config.settle_steps :])
    success = abs(final) < config.success_threshold and settled
    return {
        "x0": x0,
        "w_seq": w_seq,
        "traj": traj,
        "applied": applied,
        "final": final,
        "success": success,
        "max_abs": max(abs(v) for v in traj),
    }


def make_p(kp: float) -> Callable:
    def ctrl(x: float, integral: Optional[float]) -> Tuple[float, Optional[float]]:
        return -kp * x, integral
    return ctrl


def make_pi(kp: float, ki: float) -> Callable:
    def ctrl(x: float, integral: Optional[float]) -> Tuple[float, Optional[float]]:
        integral = (integral or 0.0) + x
        u = -kp * x - ki * integral
        return u, integral
    return ctrl


def make_limited_p(kp: float) -> Callable:
    """Same as P but will be paired with a tight u_max in some runs."""
    return make_p(kp)


# ---------------------------------------------------------------------------
# History generation
# ---------------------------------------------------------------------------

@dataclass
class HistoryEntry:
    controller_name: str
    x0: float
    w_type: str
    w_value: float
    success: bool
    final: float
    max_abs: float


def generate_histories(seed: int = 42) -> Dict[str, List[HistoryEntry]]:
    """Deliberately limited coverage. Full environment params stay with evaluator."""
    rng = random.Random(seed)
    histories: Dict[str, List[HistoryEntry]] = {"P": [], "PI": [], "Limited": []}

    # Explored: x0 in {-1, 0, 1}, w constant in {0.0, 0.1}
    # Unexplored in history: larger |x0|, larger |w|, time-varying w, saturation regimes
    explored_x0 = [-1.0, 0.0, 1.0]
    explored_w = [0.0, 0.1]

    configs = {
        "P": (make_p(0.6), PlantConfig(u_max=2.0)),
        "PI": (make_pi(0.4, 0.15), PlantConfig(u_max=2.0)),
        "Limited": (make_limited_p(0.6), PlantConfig(u_max=0.3)),  # tight saturation
    }

    for name, (ctrl, cfg) in configs.items():
        for x0 in explored_x0:
            for w_val in explored_w:
                w_seq = [w_val] * cfg.horizon
                res = simulate(ctrl, x0, w_seq, cfg)
                histories[name].append(
                    HistoryEntry(
                        controller_name=name,
                        x0=x0,
                        w_type="constant",
                        w_value=w_val,
                        success=res["success"],
                        final=res["final"],
                        max_abs=res["max_abs"],
                    )
                )
    return histories


# ---------------------------------------------------------------------------
# Property battery (hand-designed, documented)
# ---------------------------------------------------------------------------

PROPERTY_BATTERY = [
    "converges_from_small_x0_no_disturbance",
    "converges_from_small_x0_mild_constant_w",
    "rejects_mild_constant_disturbance",
    "bounded_under_explored_conditions",
]


def evaluate_property_on_entry(prop: str, entry: HistoryEntry) -> Optional[bool]:
    if prop == "converges_from_small_x0_no_disturbance":
        if abs(entry.x0) <= 1.0 and entry.w_value == 0.0:
            return entry.success
        return None
    if prop == "converges_from_small_x0_mild_constant_w":
        if abs(entry.x0) <= 1.0 and entry.w_value == 0.1:
            return entry.success
        return None
    if prop == "rejects_mild_constant_disturbance":
        if entry.w_value == 0.1:
            return entry.success and abs(entry.final) < 0.2
        return None
    if prop == "bounded_under_explored_conditions":
        return entry.max_abs < 5.0
    return None


# ---------------------------------------------------------------------------
# Extraction procedures
# ---------------------------------------------------------------------------

@dataclass
class ExtractionResult:
    mode: str
    controller: str
    observed_properties: Dict[str, str]  # prop -> "supported" | "unsupported" | "untested"
    conditions_covered: List[str]
    conditions_uncovered: List[str]
    candidate_components: List[str]
    evidence_notes: List[str]
    simulations_used: int


def history_only_extraction(
    histories: Dict[str, List[HistoryEntry]],
    controller: str,
) -> ExtractionResult:
    entries = histories[controller]
    sims = 0  # no additional sims
    observed = {}
    for prop in PROPERTY_BATTERY:
        results = [evaluate_property_on_entry(prop, e) for e in entries]
        results = [r for r in results if r is not None]
        if not results:
            observed[prop] = "untested"
        elif all(results):
            observed[prop] = "supported"
        elif not any(results):
            observed[prop] = "unsupported"
        else:
            observed[prop] = "mixed"

    covered = ["x0 in {-1,0,1}", "constant w in {0.0, 0.1}"]
    uncovered = ["|x0| > 1", "|w| > 0.1", "time-varying w", "tight saturation effects for P/PI"]
    candidates = []
    if controller == "PI":
        candidates.append("integral_term (present in name/history context)")
    if controller == "Limited":
        candidates.append("actuator_limit (inferred from occasional larger finals)")
    notes = ["History-only; no interventions performed."]
    return ExtractionResult(
        mode="history_only",
        controller=controller,
        observed_properties=observed,
        conditions_covered=covered,
        conditions_uncovered=uncovered,
        candidate_components=candidates,
        evidence_notes=notes,
        simulations_used=sims,
    )


def active_probing_extraction(
    histories: Dict[str, List[HistoryEntry]],
    controller: str,
    seed: int = 7,
) -> ExtractionResult:
    """May run additional simulations. Costs are counted."""
    base = history_only_extraction(histories, controller)
    extra_sims = [0]
    rng = random.Random(seed)

    # Reconstruct controller for probing (evaluator knows; extractor is given a factory in this toy)
    factories = {
        "P": (make_p(0.6), PlantConfig(u_max=2.0)),
        "PI": (make_pi(0.4, 0.15), PlantConfig(u_max=2.0)),
        "Limited": (make_limited_p(0.6), PlantConfig(u_max=0.3)),
    }
    ctrl, cfg = factories[controller]

    # Intervention 1: larger constant disturbance
    w_large = [0.4] * cfg.horizon
    res_large = simulate(ctrl, 0.0, w_large, cfg, extra_sims)
    # Intervention 2: larger initial condition
    res_x0 = simulate(ctrl, 3.0, [0.0] * cfg.horizon, cfg, extra_sims)
    # Intervention 3: ablate integral if PI
    if controller == "PI":
        ablated = make_p(0.4)  # Ki effectively 0
        res_ablate = simulate(ablated, 0.0, [0.1] * cfg.horizon, cfg, extra_sims)
    else:
        res_ablate = None

    observed = dict(base.observed_properties)
    notes = list(base.evidence_notes)
    notes.append(f"Probed larger w=0.4: success={res_large['success']}, final={res_large['final']:.3f}")
    notes.append(f"Probed x0=3.0 w=0: success={res_x0['success']}, final={res_x0['final']:.3f}")
    if res_ablate:
        notes.append(f"Ablated integral on mild w: success={res_ablate['success']}, final={res_ablate['final']:.3f}")
        if not res_ablate["success"] and base.observed_properties.get("rejects_mild_constant_disturbance") == "supported":
            notes.append("Integral appears load-bearing for disturbance rejection under tested conditions.")

    # Update properties based on probes
    if not res_large["success"]:
        observed["rejects_larger_disturbance"] = "unsupported"
    else:
        observed["rejects_larger_disturbance"] = "supported"
    if not res_x0["success"]:
        observed["converges_from_large_x0"] = "unsupported"
    else:
        observed["converges_from_large_x0"] = "supported"

    candidates = list(base.candidate_components)
    if res_ablate and not res_ablate["success"]:
        candidates.append("integral_term (causal under ablation)")

    return ExtractionResult(
        mode="active_probing",
        controller=controller,
        observed_properties=observed,
        conditions_covered=base.conditions_covered + ["probed |w|=0.4", "probed |x0|=3"],
        conditions_uncovered=base.conditions_uncovered,
        candidate_components=candidates,
        evidence_notes=notes,
        simulations_used=extra_sims[0],
    )


# ---------------------------------------------------------------------------
# Evaluator (has ground truth; not given to extractors)
# ---------------------------------------------------------------------------

def ground_truth_notes() -> Dict[str, str]:
    return {
        "P": "Proportional only (Kp=0.6). Steady-state error under constant w is approximately w/Kp. With threshold 0.15, w=0.1 produces |final|≈0.167 and fails the success criterion. Larger |w| or |x0| remain possible if unsaturated.",
        "PI": "Integral action eliminates constant-disturbance offset (within actuator limits). Ablating the integral restores a nonzero offset. History of mild w supports rejection; probing larger w still succeeds here.",
        "Limited": "Identical gains to P but u_max=0.3. Mild w=0.1 is within saturation authority so behaves like P (fails threshold). w=0.4 exceeds authority and diverges. History of mild conditions does not reveal the saturation boundary.",
    }


def main() -> None:
    print("=== CDIR Source-Side Probe ===\n")
    histories = generate_histories()
    print("History summary (explored conditions only):")
    for name, entries in histories.items():
        successes = sum(1 for e in entries if e.success)
        print(f"  {name}: {successes}/{len(entries)} successes on explored set")
        for e in entries:
            print(f"    x0={e.x0:+.1f} w={e.w_value:.1f} success={e.success} final={e.final:+.3f}")

    print("\n--- History-only extraction ---")
    for name in ["P", "PI", "Limited"]:
        res = history_only_extraction(histories, name)
        print(f"\n{name} (sims={res.simulations_used}):")
        for prop, status in res.observed_properties.items():
            print(f"  {prop}: {status}")
        print(f"  candidates: {res.candidate_components}")
        print(f"  notes: {res.evidence_notes}")

    print("\n--- Active probing extraction ---")
    for name in ["P", "PI", "Limited"]:
        res = active_probing_extraction(histories, name)
        print(f"\n{name} (extra sims={res.simulations_used}):")
        for prop, status in res.observed_properties.items():
            print(f"  {prop}: {status}")
        print(f"  candidates: {res.candidate_components}")
        for note in res.evidence_notes:
            print(f"  note: {note}")

    print("\n--- Evaluator ground truth (hidden from extractors) ---")
    for k, v in ground_truth_notes().items():
        print(f"  {k}: {v}")

    print("\nDone.")


if __name__ == "__main__":
    main()
