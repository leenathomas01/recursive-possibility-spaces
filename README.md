# Recursive Possibility Spaces

*A speculative research notebook about recursive self-improvement (RSI), transient opportunities, representational change, and the possibility that an adaptive system may repeatedly outgrow the state-space descriptions used to understand it.*

> **Epistemic status:** This is a collection of conceptual provocations, candidate formalisms, and questions—not a working RSI architecture, a validated theory, or a forecast of AI development. The aim is to create ideas with receipts **and** explicit room for being wrong.

## The starting perturbation

We often imagine an intelligent system searching or improving inside some already-defined landscape of models, parameters, algorithms, capabilities, or objectives.

What happens if **the space used to describe its available transformations is itself revisable**?

One exploratory image: a continually pulsing ball. A perturbation reveals a trajectory available *now*. A ring propagates outward while the ball moves further inward. Looking at the ball again yields another pulse and another ring. Each ring resembles a shed descriptive envelope—an earlier way of specifying the system's state space.

This is **not** a literal physical picture or a claim that the ball hides an essential self. Nor does a new ring guarantee more capability. The image asks whether we mistake earlier useful descriptions for permanent limits of what can happen next.

## Start here

- [Scope and epistemic boundaries](SCOPE.md) — how to separate metaphors, formal candidates, extrapolations, evidence, and claims.
- [Concept map](CONCEPT_MAP.md) — the problem space and its internal tensions.
- [Transient trajectories](perturbations/01-transient-trajectories.md) — perturbation reveals a present continuation, not necessarily a lasting pathway.
- [Recursive molting](perturbations/02-recursive-molting.md) — a system's operative descriptive domain may be shed repeatedly.
- [Operations and substrates](perturbations/03-operations-and-substrates.md) — questions about architecture, memory, computation, learned operations, and substrate-native organization.
- [Learnability boundaries](perturbations/04-learnability-boundaries.md) — when an empirical boundary is relative to a learner and a task.
- [Candidate formal languages](formalizations/candidate-languages.md) — several rival translations, each with a built-in objection.
- [Toy: operative-regime rewriter](formalizations/toy-operative-regime-rewriter.md) — a minimal, runnable sketch that tries to make regime shifts concrete under resource bounds.
- [V2 executable macro rewriter](formalizations/toy-operative-regime-rewriter-v2.md) — corrected runnable toy with actual composites, a negative result, resource accounting, and recovery costs.
- [Three-regime accessibility](formalizations/three-regime-accessibility.md) — design for distinguishing reprioritization, shedding, and loss of interpretation.
- [Adversarial review record](reviews/gemini-adversarial-review-2026-11-04.md) — Gemini's proposals, Sol's corrections, and the surviving directions.
- [Exploration notes](explorations/) — separate notes on executable rule transformations, cross-regime preservation, evaluation drift, partial continuity, ontological explosion, reflective stability, and meta-exploration heuristics.
- [Adversarial shedding experiment](experiments/adversarial-shedding-results.md) — two-presentation probe under structural and representational pressure; archive/meta recovery wins; no non-embeddable domain change observed.
- [Adversarial shedding v3 correction](experiments/adversarial-shedding-v3-results.md) — source-valid macros, measured candidate expansions, uncrippled fixed-meta comparator, and a preserved account of why the earlier results were unsound.
- [Iteration lineage](research-log/iteration-lineage.md) — a preserved record of the original toy, the defect, the correction, and the unresolved questions.
- [Circuit libraries and molting](connections/circuit-libraries-and-molting.md) — the difference between preserving old transformations, being able to recover them, and having permission to apply them.
- [Circuit Library source notes](source-notes/circuit-library/README.md) — Zee's previously unpublished conceptual design, now integrated as individually navigable research notes (including a sample entry schema and heritage collection).
- [Reading map](literature/reading-map.md) — established vocabularies worth engaging, without claiming equivalence.
- [Open questions and attempted falsifications](research-log/open-questions.md) — places where the ideas ought to fail if oversold.

## The core intellectual wager

There may be meaningful kinds of adaptive transformation inadequately captured by a single fixed model of 'improvement.' Or a richer conventional formalism may capture every one of them. **Both outcomes would be interesting.**

A particularly important challenge is separating:

1. **Changing a state** in a fixed domain.
2. **Changing the representation** used to describe that state.
3. **Changing accessible operations** under finite resources.
4. **Changing the operative domain** in which future states or operations are described.
5. **Changing what counts as success**—which is not automatically improvement.

These may overlap, but they should not be casually equated.

## Where it came from

This notebook grew from collaborative speculative discussions about AI-native capabilities, direct manipulation of model weights, dynamically accessible trajectories, an imagined self-reorganizing organism, and a 'pulsing ball' that recursively leaves rings behind. These are prompts for inquiry, not imported findings. Private creative and research material is not reproduced here.

## Ground rules

- No unexplained leap from analogy to evidence.
- No assumption that recursion is monotonic progress.
- No assumption of human-like agency, consciousness, or identity.
- No claim that a different model of computation defeats physical or information-theoretic limits.
- No treating discovery of a capability as authorization to use it.
- No obligation to preserve a beautiful hypothesis when a counterexample works.

## Contributing ideas

Prefer an explicit provocation, the assumption it challenges, at least one serious rival explanation, and a way it could be wrong. This notebook deliberately welcomes unfinished ideas. It does not promise they are true.

## License

No license is granted by this repository. **No LICENSE file is included.** Public visibility is not a grant of general reuse permission. Applicable GitHub terms and law still govern access and use.

---

*Cardigan on the outside; possibility space left open on the inside.*

## Run the experiments

```bash
python formalizations/toy_rewriter_v2.py
python formalizations/eval_drift_counterexample.py
python experiments/adversarial_shedding.py
python -m unittest discover -s tests -v
```

The first version is intentionally preserved rather than silently corrected. The v2 toy demonstrates how executable macro promotion can help one bounded task while harming another. Under its default task mix, it provides **no net success improvement and incurs additional discovery/compilation cost**. The adversarial shedding probe shows cost differences and archive/meta recovery; it does not demonstrate a forced change of operative domain. No recursive state-space molting is demonstrated.
