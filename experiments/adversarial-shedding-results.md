# Adversarial representational shedding — observed results

**Status:** minimal executable probe. Run 2026-11-04. Not evidence of recursive molting, novel ontology, or RSI.

**Code:** [adversarial_shedding.py](adversarial_shedding.py)

**Lineage:** Follows the three-regime accessibility note, the Circuit Library payload/recipe distinction, and the Gemini/Sol exchange on whether adversarial pressure can force a change of operative representation rather than repair or retrieval.

## Architecture

Underlying fixed rewrite graph with tokens a–f.

- **Atomic presentation:** single-step edges only. Search cost = number of edges traversed (BFS, budget-capped).
- **Macro presentation:** selected multi-step paths (ac, ae, be) treated as cost-1 operations while their expansions are trusted.

Strategies compared under the same task suite and budgets:

- atomic / macro (operate in the current presentation)
- archive (reload full previous atoms, pay +1)
- meta (fixed interpreter that always possesses the complete underlying graph)

External outcome: tasks solved and total operations expended. No internal scores.

## Observed results (budget=4 except where noted)

| Condition | atomic | macro | archive | meta |
|---|---:|---:|---:|---:|
| Healthy | 6/6 (ops 14) | 6/6 (ops 9) | 6/6 (ops 20) | 6/6 (ops 14) |
| A: Structural (edge b removed, macros untrusted) | 1/6 (ops 22) | 1/6 (ops 22) | 6/6 (ops 20) | 6/6 (ops 14) |
| B: Representational (macros untrusted, atoms intact) | 6/6 (ops 14) | 6/6 (ops 14) | 6/6 (ops 20) | 6/6 (ops 14) |
| Preservation trap (one macro corrupted but trusted) | 6/6 (ops 14) | 6/6 (ops 9) | — | 6/6 (ops 14) |
| Premature shedding (budget=2, most macros removed) | 4/6 (ops 12) | 5/6 (ops 9) | — | 4/6 (ops 12) |

## What the numbers show

- Different presentations can change practical cost: healthy macros solved the suite more cheaply than pure atoms.
- Structural removal of an edge is recovered by archive or meta; staying in the damaged presentation fails.
- Invalidating macro trust (representational shedding) causes the macro strategy to fall back to atomic performance. No additional capability appears.
- The preservation-trap setup did not punish continued macro use; the corrupted macro was simply not selected for the paths that succeeded.
- Premature removal of macros under a tight budget hurt the atomic strategy more than the remaining-macro strategy.

## What the numbers do not show

- No condition required a change to an operative representation that the fixed meta-interpreter could not also employ.
- No irreversible loss that archive/meta could not restore.
- No cycle or progressive degradation under repeated attack (single-shot adversary only).
- The two presentations are different granularities of the same graph, not incommensurable domains.

## Strongest simpler explanation

Macro use is ordinary caching / compilation of paths. Structural recovery is ordinary archival. Representational invalidation is cache invalidation. A fixed meta-interpreter with the full graph dominates or matches every positive result. The experiment supplies no evidence that adversarial pressure forced a transition outside conventional program transformation.

## Strongest criticism of this experiment

The representations are not different enough. Macros are labeled expansions of atomic paths; trusting or distrusting them never creates a situation in which the best continuation is unavailable to a meta-interpreter that simply stores the underlying edges. A more demanding test would need two presentations whose primitive operations are not inter-translatable by local expansion (different type disciplines, different observable alphabets, or different composition rules) and an adversary that can attack the translation mechanism itself under a shared budget. Until that exists, the stronger reading of “representational shedding” remains unearned.

## Relation to the pulsing-ball metaphor

The runs show cost differences and recovery via prior structure. They do not show a system leaving a descriptive envelope that cannot be re-entered by ordinary means. The metaphor is neither confirmed nor refuted; the probe was too weak to force the distinction.
