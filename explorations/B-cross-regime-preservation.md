# B. Cross-regime property preservation

**Status:** open research direction. Conceptual only.

## Provocation

When a system changes its operative domain, which properties (if any) can be meaningfully said to survive, and under what mapping?

## Distinctions required

- Syntactic preservation of a formal statement versus preservation of the external behavior or resource property the statement was intended to capture.
- Preservation under a total translation versus preservation under a partial map that covers only some operations or observations.
- Invariants that are true of the mathematical model versus invariants that remain true of the external task the model was used for.

Sol's correction applies directly: survival of a topological or algebraic invariant does not automatically entail survival of safety, reachability, or cost properties outside the formal system.

## What a useful note or experiment would contain

- An explicit mapping (or family of partial maps) between successive regimes.
- A stated property and the observable witness used to check it before and after.
- At least one counterexample in which the formal statement survives but the external behavior does not, or vice versa.
- Clear statement of what is assumed about the mapping (injectivity, preservation of composition, resource cost of translation, etc.).

## Strongest rival

The property was never about the operative domain in the first place; it was about an external observable that both regimes happen to affect. In that case no deep cross-regime continuity is required.

## Open

No concrete mapping and counterexample pair has been added yet. The direction remains available for a small, fully specified example.
