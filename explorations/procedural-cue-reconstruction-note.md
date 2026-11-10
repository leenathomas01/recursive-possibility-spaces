# Procedural Reconstruction from Compact Cues — Exploratory Note

**Date:** 2026-11-10  
**Status:** Early exploration; harness built, real isolation untested  
**Related:** [Capability Discovery Before Capability Engineering](../explorations/capability-discovery-before-engineering.md)

## What was investigated

Whether compact semantic cues can induce or functionally approximate complex procedural configurations, and whether a procedural invariant can survive radical domain translation.

Two complementary directions were implemented as executable toys:

1. **Cross-domain invariant translation**  
   A three-stage local resource rule (observe neighbors, transfer excess to poorer neighbor, apply reserve cap) was translated from a cellular-automaton framing into an eighteenth-century naval logistics framing. Functional success of the invariant versus a naive copy was measured.

2. **Cue-induced procedural reconstruction**  
   An unfamiliar multi-step procedure (Inverted Priority Allocation Protocol) with deliberately counterintuitive rules was defined. Multiple cue types were created. A scoring harness and simulated responders were used for calibration.

## What was actually run

- The IPAP oracle on five novel test cases (deterministic exact match scoring).
- Calibration of three simulated responders (perfect, null, partial heuristic) across six cue types.
- Cross-domain translation evaluation on 30 random configurations.

No independent language-model sessions were executed. All model-related results are proxy/calibration only.

## Observations

- The procedural invariant translated perfectly (1.00 match) while a naive copy matched only 0.17. The specific “to the poorer neighbor” rule is load-bearing.
- In the IPAP calibration, a keyword-triggered partial simulator produced identical behavior on compact, paraphrase, concise, and full cues once distinctive words were present, and weaker behavior on generic/random cues. This collapses the cue-vs-payload distinction inside the simulator.
- Exact reconstruction of the full counterintuitive procedure (demotion + phase alternation + parity) was not achieved by the partial simulator except on the simplest cases.

## Failures and contradictions to expectations

- Expected that a compact cue would be distinguishable from a full specification even in a crude simulator; instead, keyword presence dominated.
- The cross-domain experiment did not require any model and therefore does not speak to cue induction; it only shows the procedure is translatable.

## Unresolved questions

- Can a fresh, isolated model reconstruct the IPAP allocation sequence from the compact cue alone, above the level of a generic priority sort?
- Does the naval framing + CA invariant cue cause a model to apply the poorer-neighbor transfer without an explicit mapping?
- Where does reconstruction fail: demotion rule, phase alternation, parity correction, or the combination?
- Are model-generated handoff cues systematically better than the researcher-authored compact cue under the same token budget?

## Distinctions reinforced

- Functional equivalence (same next state) is not mechanistic identity.
- A successful translation in code is not evidence of cue-induced reconstruction in a model.
- Capability (the oracle exists) is not reliable control (a short cue does not yet reliably evoke it).

The harness is ready for real isolated sessions. Negative results from those sessions would be informative.
