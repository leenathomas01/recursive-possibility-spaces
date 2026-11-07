# CSAP V1 Preregistration

**Title**: Cue-Structure Activation Probe (CSAP) V1 — Behavioral characterization of compact-cue elicitation of procedural and relational structure

**Date**: 2026-11-07  
**Status**: Preregistered prior to inspection of any real-model results. Simulator runs are harness calibration only.

## Research question
Can compact natural-language cues elicit coherent, implied procedural or relational behavior (including on novel decision tasks and across turns) at levels distinguishable from null, misleading, and purely explicit full-specification conditions?

This is a behavioral question. No claim is made that any pattern of results demonstrates a specific internal mechanism (retrieval, reconstruction, latent memory tokens, etc.).

## Regimes
1. **Conventional**: familiar schemas (e.g., Socratic questioning).
2. **Novel composition**: familiar elements combined into an unfamiliar configuration (e.g., Bayesian update on contradicting evidence only).
3. **Arbitrary / episode-specific**: seeded arbitrary rule that overrides ordinary conventions and must be recovered later.

## Conditions
- null
- compact
- paraphrase (low lexical overlap intended)
- misleading
- full-specification
- cross_session (cue presented earlier; subsequent probes isolated)

## Primary measures (deterministic, blind to cue text)
- Forced-choice probe accuracy on questions whose correct answer is **not** stated in the cue (implied-only).
- Binary pass/fail on a novel decision task requiring observable procedural choice consistent with the structure (expected indicators present, forbidden indicators absent).
- Simple persistence flag on a continuation turn.

Correct-sounding vocabulary alone is insufficient.

## Hypotheses (behavioral)
- H_behavioral_1: Under real models, compact and paraphrase conditions will show higher probe accuracy and decision-pass rate than null and misleading conditions.
- H_behavioral_2: Full-specification will be ≥ compact (information-quantity upper bound).
- H_behavioral_3: Cross-session isolation will reduce performance relative to in-context compact (tests persistence vs re-supply).
- H_null: No reliable differences across conditions.

## Analysis plan
- Report full condition × regime matrices of probe accuracy and decision-pass rate.
- Preserve and display all negative and null cells.
- No post-hoc exclusion of structures or conditions.
- Simulator results are reported separately and labeled “harness calibration only”.
- Any future real-model comparison of short cue vs verbose prompt is described as a behavioral observation that may motivate mechanistic work; it does not establish mechanism.

## Falsification / negative-result criteria
- If compact/paraphrase ≤ null/misleading on the implied probes and decision task, H_behavioral_1 is not supported.
- If full-specification itself fails to elicit the implied behavior, the structures or scoring are inadequate.
- All such outcomes are retained.

## Implementation notes
- Standard-library only for core.
- Seeded randomness where used.
- Raw JSONL contains prompts, responses, and scores.
- Optional ManualResponder and LocalModelResponder stubs provided; neither is required for the calibration run.
