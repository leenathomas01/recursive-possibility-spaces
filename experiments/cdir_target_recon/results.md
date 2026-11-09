# CDIR Experiment 2: First target-side reconstruction — observed results

**Status:** executable toy. Negative findings preserved. Source-probe work left unchanged.

**Code:** [target_recon.py](target_recon.py)  
**Tests:** [test_target_recon.py](test_target_recon.py)

## Target grammar and why it differs

**Target:** discrete single-server buffer.
- State: integer queue length \(q \in \{0, \dots, 8\}\).
- Legal operations: `serve` (decrement by 1 if \(q > 0\)) or `idle`.
- External input: constant arrival of 1 token per step.
- Success: zero overflows over a 40-step horizon; queue remains within capacity.
- Failure: overflow (hard-clipped at capacity, but counted).

**Why the grammar differs from the source:** the source is a signed scalar plant with continuous-style proportional (and optional integral) correction. The target has only two discrete actions on an integer counter and a hard capacity. There is no direct analogue of a gain \(K_p\) or of signed error. Service either happens or it does not.

## Was the objective achievable?

Yes. A memoryless policy “serve whenever \(q > 0\)” keeps the queue at 1 forever under constant arrival 1, with zero overflows. The policy space is small; exhaustive enumeration of the two memoryless actions is trivial. Adding internal state is not required for this objective.

## Source information used

From the source-side probe:
- PI rejected mild constant disturbances; integral ablation showed a local causal dependence under those conditions.
- Saturation boundary was revealed only outside the historical envelope.
- Historical envelope was limited; property battery was hand-designed.

Abstraction recorded separately (not the final policy): “a persistent bias can be rejected by accumulating a measure of excess and acting when that measure indicates growth.”

## Approaches compared

| Approach | Policy | Result (constant arrival) | Steps |
|---|---|---|---|
| Target-only | serve if \(q > 0\) | SUCCESS, avg_q=1.0, overflows=0 | 40 |
| Generic hint (internal state) | serve on even counter | FAIL, overflows=12 | 40 |
| Conventional translation | queue length as “error”, serve if >0 | SUCCESS (identical to memoryless) | 40 |
| Invariant reconstruction | accumulate arrivals − services, serve if excess >0 | SUCCESS (functionally identical) | 40 |
| Always serve | serve every step | SUCCESS | 40 |

All evaluated on the same plant. Costs are plant steps (40 per run).

## What survived / what failed

- The reconstructed policy succeeds, but it is functionally identical to the memoryless target-only policy under constant arrival. No advantage is demonstrated.
- Conventional translation collapses to the same policy.
- A generic internal-state policy (serve on even steps) under-serves and overflows.
- An incorrect invariant (“always idle”) fails immediately (32 overflows).
- Removing the accumulator from the reconstruction leaves a working memoryless policy; the accumulator was not load-bearing for this objective.
- Under a single burst of 5 (outside the mild historical envelope), memoryless, conventional, reconstruction, and always-serve all still succeed (final queue = 5, no overflow). The generic internal-state policy fails.

## What the result establishes

Inside this toy:
- A simple target-native memoryless policy solves the stated objective.
- A source-derived accumulator policy also solves it, but does not outperform the memoryless baseline.
- An incorrect property fails; a poorly chosen internal state can harm performance.
- The source probe’s integral insight does not yield a measurable advantage once the target grammar and objective are fixed.

## What it does not establish

- That source-derived invariants transfer usefully across grammars in general.
- That reconstruction is superior to ordinary target-domain design.
- Robustness margins beyond the tested burst.
- Anything about larger or less hand-aligned domain pairs.

## Strongest objection

The target objective is solved by the simplest possible memoryless policy. The “invariant reconstruction” implements essentially the same decision (“serve when there is excess”). The experiment therefore demonstrates that a reasonable target-native method succeeds, not that cross-domain reconstruction added value. A harder objective (setup costs, switching penalties, partial observability, or non-constant arrivals that reward memory) might change the outcome; the present choice does not. This is reported rather than redesigned.

## Commands

```bash
python experiments/cdir_target_recon/target_recon.py
python -m unittest experiments/cdir_target_recon/test_target_recon.py -v
```
