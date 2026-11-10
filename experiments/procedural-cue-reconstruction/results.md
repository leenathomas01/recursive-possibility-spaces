# Procedural Cue Reconstruction — Observed Results

**Status:** Executable toy experiments + calibration harness.  
**Isolation:** Proxy only. No genuinely independent model sessions were run.  
All simulated responders are explicitly labeled and are not evidence of language-model behavior.

**Code:**
- `ipap_procedure.py` — Inverted Priority Allocation Protocol oracle
- `cues.py` — cue variants
- `harness.py` — scoring and simulated responders
- `cross_domain_naval.py` — CA-to-naval translation
- `run_experiments.py` — runner

## Experiment 1: Cross-domain invariant translation

**Source:** 1D cellular automaton with local excess transfer to poorer neighbor + reserve cap.  
**Target:** Eighteenth-century naval squadron powder distribution (same functional rule, different vocabulary and framing).

**Observation (executed):**
- Invariant reconstruction policy matched the target oracle on 100% of 30 random starts (length 6).
- Naive direct-copy policy matched on only 17%.

**Interpretation:**
The procedural invariant survives pure domain translation when the target grammar can express the same operations. This is functional equivalence under a hand-aligned mapping, not evidence that a model would spontaneously recover the mapping from a compact cue.

**Limitation:**
The “reconstruction” was written by the experimenter, not induced in a model. The experiment demonstrates that the procedure is translatable, not that a cue can induce the translation.

## Experiment 2: Cue-induced procedural reconstruction (IPAP)

**Procedure:** Arbitrary, counterintuitive multi-step allocation with:
- Odd-phase second-highest selection
- Initial-highest demotion if skipped
- Even-phase first-highest selection
- Odd-amount floor correction (subtract 1)

**Cues tested:** full specification, compact semantic, paraphrase, concise summary, generic, random.

**Simulated responders (calibration only):**
- Perfect oracle: always correct (upper bound)
- Null conventional: highest-first, no corrections → 0/5 exact on all cues
- Partial heuristic (keyword-triggered crude approximation): 
  - On cues containing “second”, “inverted”, “demot”, or similar: 2/5 exact, average prefix ~1.2
  - On generic and random cues: 1/5 exact, average prefix ~0.4

**Raw observation:**
The partial heuristic’s success depended on surface keyword presence rather than on any deep reconstruction. It treated compact, paraphrase, concise, and full specification identically once the keywords were present. This is an artifact of the simulator, not a model result.

**What was not observed:**
No independent model was given only a compact cue in a fresh session and asked to produce the allocation sequence. Therefore no claim is made about actual cue-induced reconstruction performance.

## Negative findings and surprises

- A deliberately counterintuitive procedure can be implemented cleanly as an oracle and scored exactly.
- Keyword-based partial simulation collapses the distinction between compact cues and full specifications; real models may or may not do the same.
- The cross-domain translation succeeded perfectly for the invariant and failed for the naive copy, as designed. The surprise was how low the naive score was (0.17), showing the specific “transfer to poorer neighbor” rule is not recovered by a simple leftward excess transfer.

## What remains untested

- Genuinely isolated model sessions.
- Model-generated cues vs. human-designed cues under matched budgets.
- Degradation under paraphrasing with real models.
- Cue collisions (one cue, two incompatible procedures).
- Token-constrained reconstruction.
- Whether models spontaneously invent the demotion or parity rules from a short cue, or merely pattern-match familiar allocation schemas.

## Proposed next experiments (not executed)

1. Manual paste protocol: give a fresh model only the compact cue + a novel request list; score exact match.
2. Ablation of individual rule components (remove demotion, remove parity) to see which parts are load-bearing for reconstruction.
3. Cross-domain cue: give the naval scenario and the CA invariant description; measure whether the model applies the transfer-to-poorer rule without being told the naval mapping.

All code is deterministic and reproducible.
