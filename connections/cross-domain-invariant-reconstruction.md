# Cross-domain invariant reconstruction

**Status:** speculative research note and accompanying executable toy. Not evidence of general transferability across human disciplines. The toy produces both successes and failures; both are preserved.

## 1. Provocation and research question

Human technical disciplines accumulate mechanisms that have survived prolonged practical use. Some of those mechanisms appear to rest on relatively compact load-bearing properties (conservation laws, opposing error, monotonic progress measures, local-to-global guarantees) while the surrounding implementation details are replaceable.

The provocation is that an AI system could, in principle:

- observe a mature mechanism in a source domain,
- extract a compact description of the properties that appear causally responsible for its functional success,
- discard or reimplement the incidental domain-specific machinery, and
- construct a mechanism in a different domain that realizes the same properties with different primitives.

**Research question:** Does this process produce useful capabilities that are not already available by ordinary abstraction, translation, analogy, or target-domain search? Or does it largely repackage those familiar operations?

We do not resolve the question by assertion. The accompanying experiment is a small, interrogable system in which the question can be asked concretely and answered under stated limitations.

## 2. Distinctions

| Term | Meaning in this note |
|---|---|
| Source mechanism | A concrete procedure that demonstrably produces a functional property inside its native domain and resource regime. |
| Invariant / load-bearing property | A relation or progress measure that the source mechanism maintains or improves, and that is conjectured to be responsible for the observed function. |
| Causal dependency | A dependence without which the functional property fails under intervention. |
| Incidental dependency | A dependence that co-occurs with success in the historical test distribution but is not necessary once the distribution or substrate changes. |
| Target-domain implementation | A procedure written in the primitives, constraints, and representation of the destination domain. |

An invariant is not automatically portable. A causal dependency in the source may become incidental, or vice versa, once the domain grammar changes.

## 3. Proposed reconstruction process

1. Observe source trajectories and interventions sufficient to identify candidate invariants and causal roles.
2. Record those candidates in an intermediate representation that is deliberately thinner than either domain’s full grammar (progress measure, opposing action, conservation constraint, etc.).
3. Given a target domain specification (primitives, constraints, objective), search for or construct a target-native procedure whose local steps are predicted to preserve or improve the recorded invariants.
4. Verify the constructed procedure against the target objective, including failure cases and resource cost.
5. Optionally compose invariants drawn from more than one source.

The intermediate representation is the critical and most contestable step. If it is rich enough to contain a ready-made compiler for the target, the experiment has engineered the result.

## 4. What AI-mediated exploration might contribute

- Faster enumeration of candidate invariants from traces than unaided human inspection.
- Systematic generation of negative controls (incorrect invariants, misleading historical successes).
- Cheap simulation of target-native candidates under altered constraints.
- Explicit accounting of extraction, translation, search, and verification cost so that “it worked” can be compared with “a simpler method also worked inside the same budget.”

None of these contributions is unique to the reconstruction framing; they are ordinary uses of search and simulation. The framing’s distinctive claim is that the intermediate representation isolates transferable causal structure rather than merely enabling ordinary program translation.

## 5. Collaboration opportunity versus validated transfer

Discovering that a source mechanism and a target problem share a superficial similarity (both “balance something,” both “reduce an error”) is a collaboration opportunity. It is not evidence that a reconstructed mechanism will succeed, nor that the reconstruction route is more efficient than alternatives.

Validation requires:

- an explicitly extracted intermediate representation,
- a construction procedure that uses that representation,
- comparable-budget baselines that do not receive the same intermediate representation,
- and at least one configuration in which the reconstruction can fail for reasons the experiment itself can detect.

## 6. Multiple-source composition

Two or more mature mechanisms may each contribute an independent property (e.g., one supplies a progress measure, another supplies a conservation constraint or a safety envelope). Composition can also introduce conflicting requirements. The toy includes a simple conflicting multi-source case; richer composition remains untested.

## 7. Competing explanations, failure modes, and possible falsifications

Competing explanations that would make the reconstruction framing unnecessary:

- The intermediate representation is an ordinary program transformation or partial evaluator.
- The target domain already contains a short search path to a solution; the source merely supplies a hint that a conventional search could also have used.
- Apparent historical success of the source rested on incidental environmental conditions that do not hold in the target.

Failure modes the toy is designed to be able to exhibit:

- Hidden source dependencies that the extraction step does not surface.
- Spurious similarities that lead to an incorrect invariant.
- Changed target constraints (capacity, conservation parity, non-negativity) that invalidate a transferred step size or direction.
- Multi-source conflict.
- Reconstruction cost that exceeds the cost of target-only search.

A result in which conventional translation or limited target-only search matches or exceeds invariant reconstruction under equal budgets is a negative finding for the distinctive claim, not a defect to be removed.

## 8. Connections to existing circuit-library and causal-role experiments

The circuit-library notes distinguish payload, recipe, witness, and lineage, and separate admission from application. An invariant extracted here is closer to a recipe-plus-witness than to a payload: it is not the original source code, yet it is also not a fully compiled target implementation.

The causal-role experiments emphasize that local counterfactual effect under a declared interface is weaker than verified internal path. The same caution applies: functional success of a reconstructed policy does not by itself establish that the recorded invariant was the operative cause, nor that an alternative invariant would have failed.

Both lines of work already treat ordinary archival, compilation, and differential testing as the default explanations to be preferred whenever they account for the observations. The present note inherits that preference.

## Epistemic status

The idea is untested beyond the accompanying toy. The toy’s strongest result is that a compact corrective-transfer policy can be written down and that several simpler methods also succeed on the same instances. Whether that pattern survives contact with larger, less hand-aligned domain pairs is open.

Related: [circuit libraries and molting](circuit-libraries-and-molting.md), [causal-role preservation V2](../experiments/causal-role-preservation-v2-results.md), [open questions](../research-log/open-questions.md).
