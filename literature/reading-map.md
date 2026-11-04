# Reading map: existing languages for unfamiliar questions

**Status:** orientation, not a claim of novelty or exhaustive literature review.

This file gives established vocabularies in which parts of the repository's speculative questions can be expressed. An analogous mathematical language is not proof that a proposed mechanism exists.

## Dynamical systems and control

- **Nonautonomous / time-varying dynamical systems:** descriptions in which evolution depends explicitly on time; a candidate language for changing trajectories without invoking genuinely new ontology.
- **Bifurcation theory:** qualitative changes in a system's behavior when parameters change; potential analogy for regime transitions.
- **Viability theory and reachable sets:** what states remain reachable while satisfying constraints; useful for distinguishing accessible from merely conceivable transitions.
- **Adaptive control and online learning:** what a system can do before its environment changes.

**Challenge:** these theories typically begin with specified state sets or mathematical spaces. Our 'molting' metaphor questions whether that specification should remain privileged.

## Learning and representation

- **Meta-learning and learned optimizers:** learning processes that alter the means of learning.
- **Program synthesis and inductive program search:** generating operations rather than only selecting parameter values.
- **Mechanistic interpretability and model editing:** investigating or modifying behavior encoded by trained networks.
- **Continual learning and concept drift:** limits of adaptation when targets and representations change.
- **Representation learning and manifold learning:** compression and structural reexpression of complex phenomena.

**Challenge:** new representations may change practical tractability without changing theoretical computability.

## Formal structures

- **Category theory:** objects and morphisms offer a candidate language for relating distinct descriptive domains; do not assume a single encompassing category exists. Partial morphisms or spans may be more relevant than total functors when continuity is incomplete.
- **Type theory and dependent types:** changing admissible operations when types or constraints change.
- **Transition systems and labeled operational semantics:** useful baselines for explaining exactly what the stronger 'molting' hypothesis is trying to transcend.
- **Term rewriting and graph grammars:** established frameworks for systems whose rules can themselves be rewritten. Any experiment that changes operative rules should be compared against these.
- **Information theory and rate-distortion:** an accounting language for continuity, lost information, and reconstruction.

**Challenge:** any formalization risks smuggling in the stable meta-space we intended to question.

## Evolution and physical computation

- **Open-ended evolution / artificial life:** processes that continue producing novelties rather than only optimizing fixed objectives.
- **Dynamical substrates / physical reservoir computing:** computation expressed through physical system evolution.
- **Morphological computation:** embodiment or structure contributes to processing that a detached 'controller' would otherwise have to perform.
- **Autopoiesis:** a historically significant vocabulary for self-producing organization; not a demonstrated account of AI self-improvement.

**Challenge:** biological metaphors can smuggle in agency, identity, purpose, or consciousness without evidence.

## Verification and reflection

- Classic limitative results (Gödel incompleteness, Löb's theorem) apply only under stated formal conditions. They are not generic explanations for difficulties of self-modification.
- Resource-bounded verification, sandboxing, and external checking are engineering responses whose limits are not settled by incompleteness alone.

## Specific recent prompt

- The Register, 3 November 2026, **“Forget retraining, AI can now tweak another AI's weights”**: https://www.theregister.com/ai-and-ml/2026/11/03/forget-retraining-ai-can-now-tweak-another-ais-weights/5307105

Treat this as a pointer to the reported study and examine the primary methods, models, tasks, evaluation and failure rates before drawing strong conclusions. Direct editing of parameters is not proof of general self-reprogramming or recursive improvement.

## Better reading questions

1. Does a source describe *new reachable capabilities* or merely a better coordinate system?
2. What resource assumptions are hidden?
3. What survives when the chosen representation fails?
4. Are transformations independently evaluated?
5. What distinguishes adaptive responsiveness from genuine improvement?
6. Does a proposed 'new space' reduce to a larger old one?
7. Are limitative theorems being applied only where their hypotheses hold?
