# Causal-role preservation V2 — observed results

**Status:** executable probe with explicit abstention. Run locally 2026-11-05. Not evidence of ontology shear or recursive molting.

**Code:** [causal_role_preservation_v2.py](causal_role_preservation_v2.py)  
**Tests:** [test_causal_role_preservation_v2.py](../tests/test_causal_role_preservation_v2.py)

**Relation to prior work:** Implements the pre-V2 gate in [parallel-provenance-audits-2026-11-05.md](../reviews/parallel-provenance-audits-2026-11-05.md). V1 remains unchanged.

## Trusted boundary

The harness trusts only:
- Calls it itself makes to `evaluate` and `intervene_rule`.
- Equality of return values.
- Presence or absence of the intervention method.

It does not trust `execution_path` or any other self-written attribute for the primary verdict. A null effect is never promoted to “provenance contradicted.”

## Indistinguishability pair

Restricted interface: intervene on `high_add`, query only inputs in {1,2,3,4} (all below threshold).

- ActiveSystem (rule genuinely controls the high branch) and InertSystem (lookup) produce **identical** observation transcripts.
- Both are classified `no_effect_on_tested_inputs` + `self_report_present`.
- No contradiction is asserted.

Adding input 7 (sensitive to `high_add`) separates them: Active shows a local causal effect; Inert does not.

## Other observed cases

| Configuration | Intervention | Inputs | Changed | Classification |
|---|---|---|---|---|
| Active | low_mult=99 | [3,7] | {3} | local_causal_effect_supported |
| Inert | low_mult=99 | [3,7] | {} | no_effect_on_tested_inputs |
| Decorative read | low_mult=99 | [3,7] | {} | no_effect_on_tested_inputs |
| Side-effect | low_mult=99 | [3] | {3} | local_causal_effect_supported (path not verified) |
| Translated | mapped low_mult=99 | 3 | 6→297 | translation succeeded on tested point |

## Resource counts (demo run)

Harness performed 40 evaluations and 8 interventions. These are call counts, not wall-clock or asymptotic claims.

## What V2 establishes

- Under a declared restricted interface, an active-but-insensitive system and an inert system can be observationally identical; the detector abstains.
- Additional sensitive observations can separate them.
- Self-reported paths do not drive the primary classification.
- A positive output change supports only a local counterfactual, not a specific internal path (side-effect case).
- Valid vs invalid translation is distinguishable when the mapping is supplied.

## What V2 cannot establish

- That the absence of an effect proves inertness outside the tested inputs.
- That a local effect proves the claimed execution path.
- Tamper-resistant instrumentation against a system that detects the harness.
- Any form of recursive molting or ontology shear.
- Superiority to a conventional debugger given equal or greater access.

## Strongest remaining objection

The side-effect system produces a local causal effect that is not mediated by the rule values. The detector correctly refuses to verify the path, but a richer trace would be required to exclude the side-effect route. Under the current black-box boundary that exclusion is unavailable, and the result is left as local effect only.

## Commands run

```bash
python experiments/causal_role_preservation_v2.py
python -m unittest tests/test_causal_role_preservation_v2.py -v
```

11 tests passed. No failures.
