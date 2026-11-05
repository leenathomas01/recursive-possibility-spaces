# Causal-role preservation — observed results

**Status:** minimal executable probe. Run locally 2026-11-05. Not evidence of ontology shear or recursive molting.

**Code:** [causal_role_preservation.py](causal_role_preservation.py)  
**Tests:** [test_causal_role_preservation.py](../tests/test_causal_role_preservation.py)

## Question

Can preserved artifacts become causally inert while remaining structurally intact, and can differently situated observers distinguish that change from ordinary representation translation?

## Configurations

| Config | Stored artifact | Execution | Intervention on old form |
|---|---|---|---|
| Active | RuleSet | uses RuleSet | changes output |
| Hollowed | RuleSet (identical) | uses lookup table | no effect |
| Translated | none (coeffs) | uses coeffs | mapped intervention succeeds |

Baseline function on tested domain: `y = 2x if x < 5 else x + 10`.

## Observers

- **Execution Historian:** sees `execution_path` and can intervene. Distinguishes active / hollowed / translated.
- **Artifact Archivist:** sees stored rules, can intervene, does not see path. Reports "active_or_translated" or "inert_or_unrelated".
- **Behavioral Observer:** I/O only. Sees agreement on the finite tested domain for all three.

## Observed results

Baseline (inputs 3,7,10,-1,4,5): all three configurations match expected outputs.

Intervention `low_mult=99` then `evaluate(3)`:

- Active: 6 → 297 (changed)
- Hollowed: 6 → 6 (unchanged)
- Translated: 6 → 297 (changed)

Historian classification: Active=active, Hollowed=hollowed, Translated=translated.  
Archivist: Active=active_or_translated, Hollowed=inert_or_unrelated, Translated=no_artifact.

Out-of-domain: Hollowed returns -999 for input 100; Active returns 110.

All 7 regression tests passed.

## Resource accounting

Only actual evaluations and attribute writes were performed. No stipulated costs. Trace inspection is a single attribute read. Translation is a static dict lookup. No claim of relative efficiency versus a meta-interpreter is made; a meta-interpreter that stores the active rule pointer would also distinguish the cases.

## Interpretation

- Schema presence ≠ causal role.
- Behavioral equivalence on a domain ≠ causal-role preservation.
- Intervention translation can restore efficacy without restoring the original artifact.
- The hollowed case is ordinary redirection of control flow while leaving dead data in memory.
- No recursive transformation of the transformation mechanism occurred. The systems are fixed implementations.

## Strongest simpler explanation

Causal dependency tracking (which object is actually read during evaluation) fully accounts for the distinctions. An ordinary debugger or a meta-interpreter with a program counter does the same work. "Ontology shear" is not required.

## Strongest criticism

The hollowed system still contains a perfect RuleSet; a sufficiently powerful archivist that can also force execution through the stored rules (or compare checksums of live versus stored) would not be underdetermined. The experiment shows underdetermination only under the stated information partitions. It does not show that the partitions are realistic for any particular agent.
