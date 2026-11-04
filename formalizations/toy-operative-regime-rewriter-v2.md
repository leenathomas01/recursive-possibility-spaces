# V2: executable macros and ceremonial molting

**Status:** corrected minimal executable counterexample. Tested locally with Python's standard library, default seed 7 and a second seed 123. Not RSI, not demonstrated state-space molting.

**Lineage:** This *adds* to, and does not replace, [Grok's original toy](toy-operative-regime-rewriter.md) and [original script](toy_rewriter.py), introduced in commit [7e70b9a](https://github.com/leenathomas01/recursive-possibility-spaces/commit/7e70b9ae48a343cd1e99a8d67a6fbfbc0ece90ed). See [iteration history](../research-log/iteration-lineage.md).

## What failed in V1

The original `promote()` introduced rules with keys such as `COMP0`, but the only probe inputs were strings like `abc` or `abbc`. A rule is applied only when its pattern appears in the string. The new keys were thus unreachable for the default task distribution. The 'regime' counter incremented without any new operative behavior. The reported 'recovery' was a score from old rules, not an actual recovery cost.

This is a **code-level finding**, not evidence for a general philosophical hypothesis: a model can *announce* a molt without undergoing one.

## V2 intervention

The new [runnable script](toy_rewriter_v2.py) uses **single-token** states and rules:

    a -> b -> c -> d

Discover a real two-step path `a -> b -> c`, check that its edges compose, and compile the macro `a -> c`. The macro is inserted before old rules. It *does* execute. The state domain and the fixed external task goal do not change. There is no claimed ontological transformation.

Search uses breadth-first traversal with a per-task cap on **candidate edges tested**, including candidates that will not be chosen. Each tested edge costs one accounting unit. Discovery costs two such units; compilation is assigned an additional one-unit accounting charge. These are simplified accounting units, not measured CPU time.

The task suite is prespecified and includes repetitions of `a -> c` (budget 1), `a -> b` (budget 1), and `b -> d` (budget 2). The seed changes their ordering, not their content. The discovery example is also a member of the evaluation task family: **these repetitions are not held-out distributional generalization**.

## Local result (default: --seed 7 --repetitions 12)

| Task | Flat success | Promoted success | Interpretation |
|---|---:|---:|---|
| a -> c, budget 1 | 0/12 | 12/12 | Executable macro makes a formerly too-deep solution reachable |
| a -> b, budget 1 | 12/12 | 0/12 | Macro-first search consumes the only edge trial; old task fails |
| b -> d, budget 2 | 12/12 | 12/12 | No change |
| **Total** | **24/36** | **24/36** | No aggregate success gain |

Search-only accounting: 48 units for each strategy. Including discovery (2) and stipulated compilation (1), promotion costs **51 vs 48 units** in this defined accounting. Seed 123 with five repetitions each showed the same qualitative result (10/15 successes for both, total costs 23 versus 20).

Recovery attempt for the old task `a -> b`: promoted search with budget one fails (1 unit), then an archive lookup (stipulated 1 unit) permits solving it using the old rules (1 unit). **Recovery cost: 3 units, versus 1 unit with the original vocabulary.** This is an explicitly constructed recovery demonstration, not an observed spontaneous recoverability phenomenon.

## What this isolates

- **Operative gain:** a real composite does change what is reachable under *a particular strict budget*.
- **Operative loss:** access to a prior behavior can worsen because of search ordering, despite old rules remaining present.
- **Cost accounting:** macro discovery and compilation can erase any gain.
- **No molt in the strong sense:** the state set is fixed and all transitions admit conventional, full macro expansion.

This is *macro compilation with resource-bounded search*, not evidence of a genuinely new ontology.

## Strongest objections

1. The negative result is intentionally sensitive to rule ordering and the one-edge budget; a different search heuristic can avoid it.
2. The cost model assigns uniform units to candidate edges and a stipulated unit to compilation and retrieval, ignoring actual machine time and memory.
3. The task suite is contrived, unbalanced for some possible uses, and not distributionally held out.
4. The code doesn't autonomously learn a reusable abstraction policy across varied tasks. It constructs one macro from a known path.
5. A more efficient flat-search algorithm can reproduce any practical benefit of this tiny macro.

## Next tests (not claimed complete)

- Run a fair **total-lifetime budget** across multiple task mixes and macro churn.
- Include goal-aware search and compare against an optimized no-promotion baseline.
- Actually remove or hide some old rules, separately from merely changing ordering, and measure true loss and retrieval cost.
- Test macro preconditions on multi-token strings where composition may not be context-independent.
- Introduce domains whose types or admissible operations change, then ask whether a fixed meta-space remains a simpler account.
- Report failures of proposed 'molts' rather than filtering them out.

## Run

```bash
python formalizations/toy_rewriter_v2.py
python formalizations/toy_rewriter_v2.py --seed 123 --repetitions 5
```

The standard library suffices. A passing run establishes only what this implementation computes.
