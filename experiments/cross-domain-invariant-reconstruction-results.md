# Cross-domain invariant reconstruction — observed results

**Status:** executable toy. Run locally. Not evidence of general cross-domain transfer. Negative findings are preserved.

**Code:** [cross_domain_invariant_reconstruction.py](cross_domain_invariant_reconstruction.py)  
**Tests:** [test_cross_domain_invariant_reconstruction.py](../tests/test_cross_domain_invariant_reconstruction.py)

## Methods

**Source domain.** Scalar integer position. Mechanism `source_feedback` applies a unit step opposing the sign of the error. Functional property: reaches 0; error magnitude decreases by 1 each step. A misleading variant acts only on positive positions (historical success on a non-negative test distribution).

**Target domain.** Pair of non-negative integer reservoirs `(left, right)`. Primitive: unit transfer from one reservoir to the other (blocked if the source is empty). Objective: reach the minimal achievable imbalance. Token count is conserved, so exact equality is impossible when the total is odd (minimal imbalance = 1). This is a genuine grammatical and constraint difference: signed scalar update versus conditional pair transfer under a conservation law.

**Intermediate representation.**  
- Correct: “imbalance = |left − right|; corrective action = transfer one unit from the larger reservoir to the smaller.”  
- Incorrect (negative control): same measure but “always transfer left → right.”

**Comparators (comparable budgets):**

1. Direct copy — source feedback applied to the sum, then a fixed-side reduction. No reference to which reservoir is larger.  
2. Conventional translation — difference mapped to the source step; the resulting delta is realized by a transfer.  
3. Target-only search — limited random rollouts with no access to source traces or invariants.  
4. Invariant reconstruction — policy constructed from the intermediate representation (small extraction cost charged).  
5. Incorrect invariant — negative control.

## Configuration

Starts: `(5,1)`, `(3,8)`, `(0,4)`, `(7,7)`, `(2,2)`. Budget 25 simulation steps (search receives multiple short rollouts inside that budget). Seeded randomness. Capacity-constrained and multi-source conflict variants also run.

## Observed results (representative)

| Start | direct_copy | conventional_translation | target_only_search | invariant_reconstruction | incorrect_invariant |
|---|---|---|---|---|---|
| (5,1) even | success (4) | success (2) | success (4) | success (2 + cost) | success |
| (3,8) odd | fail (final imb 8) | success (final imb 1) | success | success (final imb 1) | fail (imb grows) |
| (0,4) even | fail | success (2) | success | success (2 + cost) | fail |
| already balanced | success (0) | success (0) | success | success (cost only) | success |

- Capacity constraint (start `(4,1)`, capacity 3): capped reconstruction reached optimal in 1 step in this instance.  
- Multi-source conflict (random mixture of balancing and anti-balancing): succeeded in the seeded trial; not robust.  
- Misleading source: confirmed inert on negative inputs.

## Interpretation

On this toy the invariant-reconstruction policy succeeds on the tested starts once the success criterion respects token conservation. Conventional translation succeeds on the same starts and often with equal or lower step count (no extraction cost). Limited target-only random search also succeeds inside the budget on most starts. Direct copy fails when the excess is not on the side it arbitrarily reduces. The incorrect directional invariant fails when the larger reservoir is on the right.

The parity constraint is a real domain difference that both the reconstruction and the conventional mapping must accommodate; neither can reach exact equality on odd totals.

## Limitations

- Domains are tiny and hand-aligned; the intermediate representation is close to an ordinary description of the required transfer.  
- Extraction of the invariant is manual, not the output of an independent discovery procedure.  
- Resource accounting is in simulation steps / trials, not wall-clock or asymptotic complexity.  
- The capacity and multi-source variants are weak; stronger adversarial configurations remain possible.  
- No claim is made that the same pattern holds for larger or less similar domain pairs.

## Negative findings

- Conventional translation and limited target-only search match the functional success of invariant reconstruction under the budgets used.  
- An incorrectly extracted directional invariant fails, as expected.  
- Direct copying of the source step onto an unrelated projection fails on several starts.  
- Exact equality is impossible under the target conservation law when the token count is odd; any method that ignores this fails the stricter criterion.

## Strongest remaining objection

The experiment may have hidden an ordinary mapping inside the setup. The “invariant” is essentially the statement of the greedy balancing policy, and the conventional translation implements nearly the same policy via an explicit difference-to-transfer mapping. Both succeed for the same reason. The toy therefore does not yet separate “reconstruction of causal invariants” from “ordinary translation plus a parity-aware success definition.” A stronger test would require an intermediate representation that is not already a near-compiler for the target, or a target grammar in which the ordinary mapping is ill-defined while a more abstract invariant remains usable.

## Commands

```bash
python experiments/cross_domain_invariant_reconstruction.py
python -m unittest tests/test_cross_domain_invariant_reconstruction.py -v
```
