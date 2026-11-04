# Transient trajectories: availability in the present

**Status:** original speculative framing with known analogues in dynamical systems and online control.

## Provocation

Imagine a continually pulsing entity. A perturbation reveals a presently available trajectory. The entity keeps evolving; the same perturbation at another moment need not reveal the same continuation.

The discovered trajectory is not necessarily a permanent road on a preexisting map.

## What this challenges

A common picture of optimization begins with a fixed set of states and transitions, then searches it. Here, what is useful or accessible may depend on the system's *current* organization and on the intervention itself.

This does **not** mean there is no full state description. It means an agent may neither possess nor require one for a useful situated action.

## Distinguish three operations

1. **Infer:** construct a persistent model of underlying dynamics.
2. **Track:** continually adapt a representation of changing dynamics.
3. **Exploit locally:** detect an actionable continuation whose usefulness may expire before any general model stabilizes.

The third is a research question, not a free pass around sensing, latency, causality, or information limits.

## A minimal thought experiment

At time t, perturbation p produces observation o and a set of candidate continuations A(t,p,o). At time t+Δ, the system has changed; neither A nor the meaning of o must remain stable.

Even if an external observer writes A(t,p,o) as an ordinary set, that representation is *the observer's approximation*. The metaphor does not commit to a globally enumerable catalogue.

## Tests of the intuition

- Compare a model-building strategy with a local-action policy under a changing environment and equal information budgets.
- Measure usefulness before the inferred pattern expires.
- Count costs shifted into probes, instrumentation, resets, or coordination.
- Test whether local-action advantage survives on held-out dynamics.

## Objections

A sufficiently expressive fixed formal model may capture the entire process. Local advantage does not establish ontological novelty. In fast-changing systems, probing may itself destroy the only exploitable opportunity.

## Open question

Can a system preserve the *ability to find actionable transients* while repeatedly changing the representational language of those transients?
