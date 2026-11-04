# Circuit libraries as cross-regime memory

**Status:** speculative synthesis prompted by Zee's uploaded `circuit-library.zip` (dated 2026-11-03 in its citation metadata). This document is an original connection, not a mirror of that archive, a claim about deployed technology, or a license transfer.

## Provocation

Suppose a system can store not only successful parameter changes but the **procedures that led to them**, including abandoned, incompatible, or untested attempts. What happens after the system changes its operative representation so radically that yesterday's modification cannot be directly expressed in today's vocabulary?

This connects two independent sketches:

- **Circuit Library:** a hypothetical archive of neural circuit repairs, constructed mechanisms, methods, failures, and historical artifacts. Keeping an item is not permission to apply it.
- **Recursive molting:** a process leaves behind earlier descriptive envelopes ('rings') as its current operative domain changes.

The question is not merely whether a model can remember an old intervention, but whether it can preserve *an interpretable relation to an intervention from another regime*.

## Four different preservation targets

1. **Payload:** an exact delta or network component. Highly tied to the original architecture.
2. **Recipe:** a procedure for finding or reconstructing an intervention. More portable in principle, but depends on what the present system understands and can execute.
3. **Witness:** what the intervention was tested against, including failures and side effects.
4. **Lineage:** which earlier entries and assumptions produced the new one.

A 'ring' could preserve some or all of these. None guarantees an old capability survives, nor that it ought to be restored.

## Admission is not application

A library may admit contradictory, obsolete, failed, aesthetic, or contextless entries without demanding demonstrated usefulness. Applying an entry is different: it has consequences for an actual target system and requires compatibility evaluation, independent tests, provenance, and explicit authorization.

This distinction is **not** a consequence of RSI; it is a deliberate governance constraint on possible uses of stored techniques. Discovering a modification does not mint permission to apply it.

## Two rival pictures

**Archive as museum:** earlier regimes remain external records. They are evidence of previous configurations, but impose no present operational constraint. A future reader may lack the ability to understand them.

**Archive as active interface:** older regimes' recipes or witnesses are retained in a format the current regime can still query. They may constrain, enable, or complicate new work.

We should not presume that an active interface survives arbitrary molting. Every cross-regime adapter has a cost and can fail silently.

## Connection to the operative-regime rewriter

In the existing v2 rewriter, a promoted macro can consume the budget needed to execute an older, simpler operation. Recovery is performed by explicitly loading an archived rule set and paying a modeled retrieval cost.

A circuit library invites a richer version: archive **the proof of what a macro does, its original context, and how to rederive it**—not just the macro's expansion. But such metadata incurs costs, can become stale, and may be impossible to transport after a representational shift.

## A stronger thought experiment

Consider regimes D_0, D_1, and D_2, each with different operator vocabularies. A library holds an entry authored in D_0:

- literal intervention delta in D_0;
- a recipe expressed in D_0;
- a test outcome observable from outside;
- provenance linking it to D_0's assumptions.

At D_2, the direct delta and recipe are no longer readable. The external test may remain meaningful, or may not. Does this count as **memory**, **fossil**, **unusable data**, or **potentially reconstructable capability**?

No single answer follows. The point is to ask what exactly the claim 'the system remembers its previous form' entails.

## Relation to practical possibility spaces

Under a resource budget R, an archived capability can be:

- physically representable but inaccessible to the current interpreter;
- retrievable but too costly to recover;
- cheaply reconstructible but unsafe or unauthorized to apply;
- available and testable, yet harmful to the current task distribution.

Thus **stored possibility**, **operational accessibility**, **desirability**, and **permission** are distinct dimensions. A growing library does not imply monotonically growing capability.

## Counterarguments and failure modes

- A conventional, sufficiently general program representation can store all recipes; 'cross-molt memory' might just be ordinary archival and compilation.
- A purported method may only describe one successful local weight edit and have no transferable mechanism.
- A library may accumulate unvalidated modifications until retrieval noise overwhelms useful entries.
- Cross-architecture translation can invalidate semantic claims even when a patch executes.
- Reconstruction may be more expensive than rediscovery.
- A library can become an attack surface: provenance and signed artifacts do not replace behavioral testing.
- The source Circuit Library is **conceptual**. It supplies no empirical evidence that the library works or that direct weight-space interventions generalize across architectures.

## Falsifiable small-scale follow-ups

1. Add to the macro toy an archival entry with both executable expansion and a trace of tests. Compare exact reuse, re-compilation, and independent rediscovery under equal total budgets.
2. Perturb the operator vocabulary so that earlier rules cannot be executed directly; measure translation success and recovery cost rather than inferring them.
3. Insert useless and conflicting recipes into the archive. Does selection degrade as the library grows?
4. Distinguish *compatible but unauthorized* from *incompatible* actions in a toy policy gate. This models permission separation, not autonomous authority.
5. Compare against a fixed meta-interpreter that can run every old rule: prefer this simpler explanation wherever it accounts for the evidence.

## Provenance and rights

Prompted by the user-supplied `circuit-library.zip`, containing a README, five design notes, an example entry schema, and an appendix on heritage preservation. Its own metadata identifies the work as speculative and MIT-licensed. **No files from that ZIP were copied into this repository.** This note paraphrases and extends the high-level design question while preserving the main repository's no-license status.

Related internal links: [recursive molting](../perturbations/02-recursive-molting.md), [operation/substrate possibilities](../perturbations/03-operations-and-substrates.md), [v2 rewriter](../formalizations/toy-operative-regime-rewriter-v2.md), and [open questions](../research-log/open-questions.md).
