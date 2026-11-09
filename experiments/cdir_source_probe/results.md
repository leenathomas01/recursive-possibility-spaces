# CDIR source-side probe — observed results

**Status:** executable source-side extraction experiment. No target-domain transfer. Round 1 experiment left unchanged.

**Code:** [source_probe.py](source_probe.py)  
**Tests:** [test_source_probe.py](test_source_probe.py)

## What was built

A small discrete plant

\[
x[t+1] = x[t] + \mathrm{clip}(u[t], -u_{\max}, u_{\max}) + w[t]
\]

with three controllers:

- **P**: \(u = -0.6 x\), \(u_{\max}=2.0\)
- **PI**: \(u = -0.4 x - 0.15 \int x\), \(u_{\max}=2.0\)
- **Limited**: same gains as P but \(u_{\max}=0.3\)

Update order: controller computes \(u\) from current \(x\) (and integral for PI), actuator clips, then plant steps. Success requires both \(|x_{\mathrm{final}}| < 0.15\) and the last 15 steps inside the threshold.

Histories cover only \(x_0 \in \{-1,0,1\}\) and constant \(w \in \{0.0, 0.1\}\). Larger \(|x_0|\), larger \(|w|\), time-varying disturbances, and explicit saturation boundaries are left unexplored.

A fixed hand-designed property battery is applied to every history. Two extraction modes:

- History-only: inspects recorded outcomes only (0 extra simulations).
- Active probing: may run additional episodes (larger \(w\), larger \(x_0\), integral ablation). Every plant step is counted.

Ground-truth implementation notes are available only to the evaluator.

## What the histories actually contained

| Controller | Explored successes | Notes |
|---|---|---|
| P | 3/6 | Succeeds on \(w=0\); fails on \(w=0.1\) because steady-state offset \(\approx 0.167 > 0.15\) |
| PI | 6/6 | Succeeds on all explored cases; integral removes offset |
| Limited | 3/6 | Identical to P on the explored set (mild \(w\) still within saturation authority) |

No mechanism was labeled successful on a scenario it failed.

## What the automated procedure extracted

**History-only**

- Correctly reported that P and Limited do not support “rejects mild constant disturbance” or “converges under mild \(w\)” under the declared threshold.
- Correctly reported that PI supports those properties on the explored set.
- Marked larger conditions as untested.
- Candidate list for PI mentioned the integral (from controller identity); for Limited mentioned actuator limit (weak inference from finals).
- Zero additional simulations.

**Active probing**

- Confirmed history-only conclusions and added:
  - P fails \(w=0.4\) (offset larger).
  - PI still succeeds on \(w=0.4\) and on \(x_0=3\).
  - Ablating the integral on mild \(w\) causes PI to fail (final \(\approx 0.25\)). The note “integral appears load-bearing under the tested intervention” is recorded.
  - Limited fails dramatically on \(w=0.4\) (final \(\approx 3.36\)), revealing the saturation boundary that the history did not contain.
- Extra simulation steps: 60 (P), 90 (PI, includes ablation), 60 (Limited).

## What was missed or misidentified

- History-only cannot distinguish “P fails the threshold because of offset” from “Limited fails for the same reason.” Both look identical on the explored set.
- The candidate “actuator_limit” for Limited is only weakly supported by history; the decisive evidence appears only under probing.
- No procedure discovered the precise gain values or the exact equilibrium formula; they reported only the property-level outcomes.
- Probing on P for large \(x_0\) succeeded and added little new causal information beyond “still works.”

## Interventions that supplied new information

- Integral ablation on PI: established a local causal dependence that history alone could not prove (history is consistent with many explanations for why PI succeeded).
- Larger disturbance on Limited: revealed a hard saturation boundary outside the historical envelope.
- Larger disturbance on P: confirmed the expected growth of offset; not surprising but quantified.
- Large \(x_0\) probes: mostly redundant with existing convergence evidence for these gains.

## Cost

Active probing consumed 60–90 additional plant steps per controller (instrumented, not arbitrary). History-only consumed zero. No claim is made that the extra information is worth the cost in general; on this toy the ablation and the saturation probe were the only clearly non-redundant results.

## What remained ambiguous or broke

- The success threshold of 0.15 interacts with the P equilibrium at \(w/K_p \approx 0.167\). A slightly looser threshold would have made P appear successful on mild \(w\), changing the history-only report. This sensitivity is intentional and documented.
- Limited and P are observationally identical on the historical set; only an intervention outside that set separates them.
- The multi-source / composition case was not run (out of scope for this source-side probe).
- Random seeds are fixed; results are deterministic.

## What the experiment can and cannot establish

**Can establish (inside the toy):**

- That a history of successful mild-disturbance rejection by PI does not by itself prove the integral is necessary; an ablation does.
- That a limited historical envelope can hide a saturation boundary.
- That property-level extraction from trajectories is possible without reading controller source, and that the cost of additional probes can be counted.

**Cannot establish:**

- That the extracted “invariants” would transfer to a different domain.
- That active probing is generally superior; on several probes it added no new distinction.
- Precise parametric identification or robustness margins beyond the tested interventions.
- Anything about cross-domain reconstruction.

## Strongest criticism

The extraction procedures are still quite close to the property battery that was hand-designed with knowledge of the plant. The “automated” step mainly aggregates already-defined predicates over trajectories and then runs a small menu of interventions that an engineer who already suspected integral action or saturation would have chosen. A more skeptical reading is that the experiment demonstrates careful instrumentation and the value of ablation, not a general method for recovering causal structure from opaque histories. The ground-truth notes were written after seeing the runs; while they were not fed to the extractors, the property battery itself encodes expectations about what matters.

## Commands

```bash
python experiments/cdir_source_probe/source_probe.py
python -m unittest experiments/cdir_source_probe/test_source_probe.py -v
```
