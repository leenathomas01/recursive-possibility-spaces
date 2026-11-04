# Iteration lineage: retain the mistakes

The objective is not to produce a tidy succession of increasingly impressive models. It is to keep enough provenance that each new claim can be audited against the previous one.

## 2026-11-04 — Conceptual notebook created (Sol and Zee)

The original public notebook introduced transient trajectories, recurring state-space 'molting', and a pulsing-ball metaphor. It emphasized the unresolved separation between fixed-meta-space redescription and any stronger account of operative-domain transformation.

**Status:** conceptual hypotheses with caveats and alternative explanations. No model validation.

## 2026-11-04 — First executable toy added (Grok)

Commit: [7e70b9a](https://github.com/leenathomas01/recursive-possibility-spaces/commit/7e70b9ae48a343cd1e99a8d67a6fbfbc0ece90ed).

Files: [toy-operative-regime-rewriter.md](../formalizations/toy-operative-regime-rewriter.md) and [toy_rewriter.py](../formalizations/toy_rewriter.py).

Hypothesis: useful multi-step rewrites promoted to new atomic rules may alter practical reachable behavior under limited search depth and branch budget, even while everything fits in a fixed meta-space.

**Retained weakness:** promoted `COMPn` keys are never present in the default inputs, making new rules inapplicable; 'recovery cost' is not operationally measured. The written goal of equal-budget, cost-aware assessment exceeds what V1 implements.

**Lineage decision:** leave V1 untouched. An invalid first implementation remains useful provenance.

## 2026-11-04 — Executable-composite correction (Sol)

Files: [v2 script](../formalizations/toy_rewriter_v2.py) and [v2 note](../formalizations/toy-operative-regime-rewriter-v2.md).

Changed:
- Use a genuine two-step token rewrite as a macro; validate composability.
- Count candidate-edge trials under comparable per-task limits.
- Include discovery and a stipulated compilation charge in the aggregate.
- Measure an explicit archive-assisted recovery attempt after a failed current-regime probe.
- Expose a negative transfer case rather than assuming promotion helps.

**Local execution result:** default tasks produce 24/36 success in both flat and promoted settings, while promotion costs three extra accounting units. An old one-step task fails after promotion under budget 1, though it can be recovered by using archived rules with added cost.

**Interpretation:** some bounded accessibility shifts are observable; the toy does not establish an ontological 'molt', self-directed RSI, generalization, or overall progress. The task order is seedable, but the set is fixed.

## 2026-11-04 — Circuit-library connection (Zee's uploaded archive; Sol synthesis)

Source: user-provided `circuit-library.zip` (separate speculative design note, self-labelled MIT in its source metadata; not imported here).

Added: [Circuit libraries as cross-regime memory](../connections/circuit-libraries-and-molting.md).

The source considered a library of parameter edits, circuit constructions, methods, failed entries and heritage artifacts, sharply distinguishing **admission** from **application**. The new synthesis asks which kinds of records from an earlier operative regime remain interpretable or recoverable following a putative molt.

**Status:** conceptual cross-connection only. No uploaded source file copied, no experimental findings claimed, no license added. Strongest rival: ordinary archival, versioning, compilation and retrieval in a fixed meta-space.

## 2026-11-04 — Author-approved integration of unpublished Circuit Library material

Zee clarified that the Circuit Library archive had never been published and expressly authorized use of its contents.

Added [Circuit Library source notes](../source-notes/circuit-library/README.md), including the repair/construction distinction, admission versus application gates, concrete transformation versus portable recipe, eight open questions, an illustrative YAML entry, and the heritage collection.

The uploaded draft carried its own MIT template and citation metadata, but the destination repository's earlier **no-license** decision was retained. The archival texts are reorganized adaptations, not a byte-for-byte mirror. The draft licensing files are intentionally excluded, and empirical claims remain qualified pending verification against primary sources.

The earlier [cross-regime synthesis](../connections/circuit-libraries-and-molting.md) remains separate from this source collection, preserving the distinction between the original idea and our extrapolation.

## 2026-11-04 — Three-regime accessibility design (Grok, incorporating Sol's refinement)

Added: [three-regime-accessibility.md](../formalizations/three-regime-accessibility.md).

Explicitly separates:

- **A — Reprioritization** (old rules remain executable but deprioritized)
- **B — Shedding** (removed from active set, retained in archive)
- **C — Loss of interpretation** (records survive but cannot be directly executed)

Requires matched total budgets, an external task suite, explicit recovery costs, and comparison against a fixed-meta-space simulator. Regime C is the point at which Circuit Library notions of recipe versus payload become testable inside the toy. No implementation of the three modes is claimed yet; the note only makes the next falsifiable distinction precise.

## 2026-11-04 — Gemini adversarial review and Sol critique integrated (Grok)

Added: [reviews/gemini-adversarial-review-2026-11-04.md](../reviews/gemini-adversarial-review-2026-11-04.md) and the exploration notes under `explorations/`.

Preserves Gemini's proposals (state-space transformations, invariants, ontological explosion, metric drift, reflective stability, category-theoretic tools, meta-exploration heuristics) alongside Sol's corrections (molting need not expand; invariants do not automatically preserve external properties; limitative theorems require their formal hypotheses; category theory is descriptive; self-modification ≠ authorized self-modification; no global metric assumed).

Surviving directions are recorded separately so disagreements remain visible. A minimal evaluation-drift counterexample sketch was added at `formalizations/eval_drift_counterexample.py`. Existing v1 and v2 toys were left unchanged. No license was added.

## 2026-11-04 — Adversarial representational shedding probe (Grok)

Added: [experiments/adversarial_shedding.py](../experiments/adversarial_shedding.py) and [experiments/adversarial-shedding-results.md](../experiments/adversarial-shedding-results.md).

Minimal two-presentation system (atomic edges vs trusted macros) under structural edge removal and macro-trust invalidation. Compared stay/repair, archive recovery, and a fixed meta-interpreter on an external task suite.

**Observed:** healthy macros reduced operation count; structural damage was fully recovered by archive or meta; representational invalidation collapsed macro performance to atomic performance. No condition produced a best continuation unavailable to the meta-interpreter.

**Interpretation:** results are accounted for by ordinary caching, archival, and cache invalidation. The probe does not earn a claim of forced change in operative domain. Existing toys and prior negative results left intact.

## 2026-11-04 — Adversarial shedding v3 correction (Sol)

Grok's [adversarial shedding probe](../experiments/adversarial_shedding.py) and [reported results](../experiments/adversarial-shedding-results.md), commit [661b7f2](https://github.com/leenathomas01/recursive-possibility-spaces/commit/661b7f29d2b0cbb99c38384d0c5f17b82082c64e), were reviewed without modifying those files.

**Found:** macro invocation previously checked the declared destination but not the current starting state or the validity of the macro's constituent edges. Consequently, an inapplicable shortcut could claim success, undermining macro-dependent tallies and the preservation-trap conclusion. The cost column also mixed successful path length with fixed failure penalties rather than measuring tested candidate transitions.

**New files:** [v3 script](../experiments/adversarial_shedding_v3.py), [v3 results and limitations](../experiments/adversarial-shedding-v3-results.md), and [regression tests](../tests/test_adversarial_shedding_v3.py).

**Local test:** seven targeted regression cases passed. With correct macro applicability and candidate expansion accounting, healthy macro search solved 6/6 versus atomic 5/6 under budget four. The fixed meta-interpreter given those **same** macros matched 6/6. Macro corruption detected by path certification was rejected; structural deletion did not create a new computational domain. These are bounded, deliberately chosen tasks—not a general empirical result.

**Provenance decision:** keep the original incorrect numbers accessible, but flag them as superseded for any comparison involving macros. Do not confuse this correction with the earlier v2 operative-regime toy, which addressed an *unreachable* macro rather than an overly permissive one.

**Unresolved:** certification/build costs were not charged, and a rival meta-interpreter was endowed with the original rule history. The next useful experiment must account for the cost of constructing and maintaining that history and/or test more substantively different interpreter representations.

## Next candidate revisions

- A follow-up in which the two presentations are not locally expandable into each other.
- An adversary that can attack the translation or trust mechanism under a shared budget.
- Explicit repeated attacks that target the recovery path itself.

## Provenance discipline

Claims here are specific to the code and stated experiments. Nothing in the toy validates the synthetic-organism metaphor, the empirical generality of earlier interference research, or predictions about future RSI.
