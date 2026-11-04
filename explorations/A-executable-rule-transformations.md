# A. Executable transformations of operative rules

**Status:** open research direction. Not implemented beyond the existing rewriter toys. Not a claim of novel ontology.

## Provocation

Can a small system change the set of operations it is allowed to apply, and can we distinguish that change from ordinary state updates, representation changes, or reparameterizations inside a fixed meta-interpreter?

## What would need to be shown

A useful experiment would have:

- An interpreter (or graph-rewriting engine) whose current rule set is itself data.
- A mechanism that can add, remove, or rewrite rules.
- A baseline fixed meta-interpreter that can represent every such change as ordinary data and still execute the expanded history.
- Resource bounds so that “theoretically representable” and “practically accessible under the current regime” can come apart.
- Explicit logging of whether a change is only a state update, a change of representation, a change of the active operation set, or something that resists clean embedding.

The existing v1 and v2 rewriters already perform limited versions of operation-set change (macro promotion). They remain fully embeddable. The open question is whether a more radical rule-rewriting loop produces a practically different intervention profile under equal budgets.

## Strongest rival

Any such system is still a conventional program transforming its own data structures. A meta-interpreter with a larger fixed language can simulate every step. Prefer this account unless a concrete accessibility, latency, or recovery difference survives the comparison.

## Relation to earlier work

Builds on the operative-regime rewriter and the three-regime accessibility note. Does not replace them.

## Open

No executable system in this repository currently changes its own generative rules in a way that escapes ordinary program transformation. That is not a defect; it is the current state of the evidence.
