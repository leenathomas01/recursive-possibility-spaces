# Adversarial shedding v3 — origin, certification, and honest costs

**Status:** corrective executable probe, not evidence of ontological molting or RSI. **Lineage:** Grok's [original adversarial shedding experiment](adversarial_shedding.py) and [original results](adversarial-shedding-results.md) remain unchanged. This iteration responds to Sol's review of the macro applicability and cost-accounting defects. See [corrected script](adversarial_shedding_v3.py) and [tests](../tests/test_adversarial_shedding_v3.py).

## The v2 adversarial-shedding bug

The previous macro solver selected a trusted macro if its *destination* matched the requested target. It did not verify that the macro **started at the actual current state**. It also did not verify that its declared path remained realizable after an attack.

Thus a shortcut from `b` to `e` could silently solve an unrelated request from `a` to `e`. A corrupted `ae` macro was sometimes bypassed by an inapplicable `be` shortcut. The earlier macro-dependent success totals are not sound evidence for the stated task semantics.

This is separate from the earlier `COMPn` defect in the operative-regime rewriter. Here a newly defined operation can **fire too broadly**; in the earlier case, it could never fire.

## V3 corrections

1. A macro has an explicit path whose first node must match the current node.
2. A macro is certified only if *every edge* along that path exists in the currently available atomic graph.
3. BFS checks candidate transitions under a fixed expansion budget, counting edges **examined**, not just solution path length. Failure can consume fewer than the nominal cap when there is no path to expand.
4. The **fixed meta-interpreter has the same original atoms and the same certified macros** as the live macro strategy. It is not intentionally hobbled to atomic-only search.
5. Archive recovery has a stipulated retrieval charge included in its overall budget.
6. A deliberately poisoned macro can produce a false answer when verification is disabled; with verification, it is rejected.

**Important cost limitation:** macro creation and the work of certification are *not* counted. Certification is treated as a prevalidated precondition, not a free operation in a deployed system. Only candidate expansions are measured; retrieval is assigned one illustrative accounting unit. These totals do not establish end-to-end efficiency.

## Locally observed results

Run locally with Python 3 and a six-task suite. Tasks are `a→c`, `a→e`, `b→e`, `a→d`, `c→e`, `b→d`. Each task receives budget 4 candidate expansions, except the premature-shedding condition (budget 2).

| Condition | Atomic | Verified macro | Fixed meta with same macros |
|---|---|---|---|
| Healthy | 5/6; 19 expansions | 6/6; 14 expansions | 6/6; 14 expansions |
| Structural removal of all `b`-origin edges | 1/6; 5 | 1/6; 5 | 6/6; 14 |
| Macros unavailable; atoms intact | 5/6; 19 | 5/6; 19 | 6/6; 14 |
| Poisoned extra macro, verification enabled | 5/6; 19 | 6/6; 14 | 6/6; 14 |
| Premature macro shedding, budget 2 | 2/6; 12 | 3/6; 11 | 4/6; 10 |

The fixed meta-interpreter is an **upper bound under stronger retained knowledge**, not an adversarially damaged peer. Its 6/6 result is not evidence that every fair memory-limited competitor must succeed. Conversely, this toy cannot claim a uniquely nonclassical transformation when a conventional interpreter with appropriate macros produces the same useful behavior.

For an old task `a→e` after structural removal, archive reload under total budget 8 succeeds with six accounting units (one stipulated lookup + five expanded candidates). This demonstration does **not** include an initial failed live-regime probe; full lifecycle accounting remains future work.

## What survived scrutiny

- Correct application *domain* is indispensable to judging whether an operation is accessible.
- Valid shortcuts can improve reachability under strict search-expansion limits.
- Removing underlying edges invalidates macros that depended on them.
- Cache/representation invalidation can reduce performance without changing the full mathematical state space.
- Preservation and retrieval have costs, but this toy does not estimate the costs of maintaining, verifying, or compiling the archive.

## What did not survive

The original claims of 6/6 atomic success under budget 4, and the interpretation of the preservation-trap scenario as evidence of harmless continued reliance on a corrupted macro, should not be carried forward without the corrected semantics. Neither v3 nor the original probe demonstrates adaptive adversarial rounds, loss of interpretation across genuinely different representation languages, or recursive molting.

## Strongest objections to v3

- The macro presentation is still merely a compilation of paths through one fixed graph.
- Certification is perfect and external. A system that actually pays for validation or faces deceptive execution could behave differently.
- The tasks and macro set are hand-chosen and evaluated on the same known graph; there is no discovery experiment or held-out generalization.
- Although expansions are counted, they are not proportional to the wall-clock cost of creating and validating a macro.
- The fixed meta has privileged retained knowledge. A fair comparison under restricted memory should separately allocate costs for retaining that knowledge.
- A poisoned macro that *claims* a valid expansion but has corrupt runtime semantics is not modeled; the current attack only introduces an invalid path.

## Next experiment worth attempting

A genuinely distinctive follow-up should combine: two nontrivially different **interpreter languages**, an explicit partial translator that the adversary can disable, an external witness of desired behavior, and matched total costs including interpreter creation and archival memory. Also include a system that merely repairs its old representation, and a fixed meta-interpreter allowed to do the same work.

Until then, the 'shed ring' reading remains an open metaphor, not a result.

## Reproduce

```bash
python experiments/adversarial_shedding_v3.py
python -m unittest discover -s tests -v
```

Results in this note were produced locally for the corresponding v3 code before commit. The code is deterministic. No automated CI run is claimed.
