# Three-regime accessibility after promotion

**Status:** experimental design note. Not yet implemented as a full runnable suite. Not evidence of recursive molting or RSI. Intended to separate search-order effects from genuine loss of available operations and from loss of interpretability.

**Lineage:** Prompted by review of the v2 rewriter (where old rules remain executable but can be deprioritized under a tight budget) and by Sol's refinement of the distinction. See [v2 note](toy-operative-regime-rewriter-v2.md) and [iteration lineage](../research-log/iteration-lineage.md).

## The distinction to isolate

After a composite is promoted, three different things can happen to prior operations. They are easy to conflate and should not be.

| Regime | What happened to prior operations | What recovery requires | Relation to v2 toy |
|---|---|---|---|
| **A — Reprioritization** | Old operations remain in the active vocabulary but are examined later or under a tighter residual budget | Better search ordering, larger budget, or goal-aware selection | Exactly what the current v2 demonstrates under budget 1 |
| **B — Shedding** | Old operations leave the active set but remain in an explicit archive | Retrieval cost + reintegration into the current interpreter | Stronger than v2; requires actually removing rules from the live set |
| **C — Loss of interpretation** | Records survive, but the current system cannot directly execute the stored form | Translation, reconstruction from recipe/witness, or independent rediscovery | Closest to the Circuit Library question; requires a representational shift that breaks direct applicability |

A saved rule is not automatically a recoverable capability. A recoverable capability is not automatically worth recovering.

## Proposed measurement

Use the same external task suite and accounting units already defined in the v2 rewriter. For each regime, run under matched total budgets (including discovery, compilation, retrieval, translation, or rediscovery costs).

Report, for each regime and each task:

- Success rate under the current operative vocabulary.
- Recovery cost when the current vocabulary fails.
- Whether recovery used the archive, a translation step, or independent rediscovery.
- Net accounting units versus a flat baseline and versus a fixed meta-space simulator that can always expand every historical rule.

## Fixed-meta-space competitor (required)

Every result must be compared against a conventional simulator that stores the full history of rules and can expand any prior composite on demand. Prefer the simpler account whenever it matches the success and cost numbers. No free philosophical victories.

## Relation to Circuit Library notes

Regime C is where the distinction between payload, recipe, witness, and lineage becomes operational. A library entry that stores only a literal rule (payload) fails under C. An entry that stores a construction procedure plus a test witness may still support reconstruction. Admission of the entry does not imply permission or duty to apply it.

## Ways the experiment can fail to be interesting

- If regimes A, B, and C produce statistically indistinguishable cost and success profiles under the chosen budgets, the distinctions are not doing work at this scale.
- If the fixed-meta-space simulator always dominates, the stronger language is not yet earned.
- If recovery is almost always cheaper than rediscovery, the “shed ring as active constraint” reading remains unsupported.
- If the only way to produce regime C is an artificial, unmotivated change of token vocabulary, the result is an artifact of the toy rather than a useful probe.

## Minimal next implementation step

Extend the v2 script (or add a sibling) so that after promotion one can choose:

- Mode A: reorder rules (current behavior).
- Mode B: move selected old rules to an archive dict; recovery pays a retrieval unit and reloads them.
- Mode C: replace the live interpreter with one that rejects old patterns unless a separate translation function is invoked (stub translation cost for now).

Keep the task suite and accounting identical so the three modes can be compared directly.

No molt is claimed by running any of these modes. The point is to make the next falsifiable claim precise enough to fail.
