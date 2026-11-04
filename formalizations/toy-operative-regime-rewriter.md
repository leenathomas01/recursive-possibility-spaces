# Toy: Operative-regime string rewriter with abstraction promotion

**Status:** Minimal executable sketch. Not a theory of recursive self-improvement, not a claim that molting has been demonstrated, and not an architecture for real systems. It exists to make a few distinctions from the concept map concrete enough to measure and to fail.

## Provocation

What happens if a system can promote frequently useful *sequences* of its current transformations into new atomic operations, so that subsequent search primarily operates in the coarser vocabulary?

## Fixed assumptions being challenged

- That the set of accessible transformations remains fixed while only states or parameters change.
- That a redescription in a larger fixed meta-space is automatically equivalent for intervention under resource bounds.
- That promotion of abstractions is automatically progress.

## Minimal example

The system rewrites short strings over a tiny alphabet using a set of atomic rules. A tight local probe (limited depth and branching) can discover multi-step sequences that achieve useful intermediate results. When a composite is used often enough and reduces future search cost, it is promoted to a new atomic rule. The old fine-grained rules remain in history but are no longer the primary operative vocabulary.

An external observer can always embed the entire history inside a fixed meta-space of “all possible rule sets + current index.” The toy does not escape that. It only tries to make the practical difference visible under explicit resource bounds and intervention latency.

## Candidate formalization (Model A style)

Regime $i$ is written:

$$
D_i = (S_i, T_i, E_i)
$$

- $S_i$: strings (unchanged across regimes in the basic version).
- $T_i$: current set of atomic rewrite rules.
- $E_i$: evaluation relative to a fixed external score function plus a search-cost term.

A provisional molt:

$$
(S_i, T_i, E_i) \xrightarrow{M_i} (S_{i+1}, T_{i+1}, E_{i+1})
$$

where $T_{i+1}$ contains a newly promoted composite. $M_i$ is not required to be invertible or to preserve every earlier capability.

## What the toy tries to make observable

1. Search cost (steps or nodes) before versus after promotion, under equal total compute including discovery cost.
2. Recovery cost of a capability that lived primarily in the pre-promotion grain.
3. At least one regime in which promotion harms held-out performance (over-abstraction).
4. Whether an external fixed task can still serve as a cross-regime witness even when the internal operative vocabulary has shifted.

## Strongest rival explanations

- The whole process is an ordinary state transition in a fixed meta-space of rule sets. Prefer this account if it preserves all predictions at lower descriptive cost.
- Promotion is merely macro expansion / compiler optimization; nothing about the operative domain has changed beyond convenience.
- Any apparent loss of earlier competencies is an artifact of the particular search heuristic, not of the regime shift.

## Ways it can be wrong (or uninteresting)

- If a flat search baseline that never promotes matches or beats the promoter under equal total compute, the toy has not earned its complexity.
- If every useful composite remains cheaply available without promotion, the “operative domain” claim collapses.
- If recovery of pre-molt capabilities is always free, the rings are pure historical traces with no residual constraint.
- The external score is fixed; the toy therefore sidesteps the harder question of evaluation drift (see open questions Q06).

## Relation to other notes

- Closest to the provisional scaffold in [recursive molting](../perturbations/02-recursive-molting.md).
- Intended as one concrete candidate under [candidate formal languages](candidate-languages.md), Model A.
- Directly engages open questions Q01, Q04, and Q07 in the research log.

## Runnable sketch

A minimal Python implementation lives at `formalizations/toy_rewriter.py`. It is deliberately small, deterministic-seedable, and instrumented to log regime shifts, search costs, and recovery attempts. Run it, modify the promotion threshold or probe budget, and watch the distinctions appear or fail to appear.

No novel computability is claimed. No physical limit is circumvented. Promotion is not authorization.
