# 04 — Recipes and weights

Two preservation targets are distinct.

- **Transformation:** the concrete weight edit or circuit instance associated with an original target.
- **Method:** the reasoning, procedure, or construction recipe by which an intervention was discovered.

| Question | Concrete transformation | Method / recipe |
|---|---|---|
| Portability | Typically tied to architecture and alignment | Potentially broader, unproven |
| Reproducibility | Can be replayed on an unchanged compatible target | Depends on execution context and interpreter |
| Verification | Direct tests of the stored artifact | Needs reconstruction and fresh testing |
| Generativity | Fixed instance | May yield multiple new interventions |

Store both when available, linking them to provenance, assumptions, compatibility, and test evidence.

The original note proposes treating methods as the main portability candidate and transformations as reference instances. This is a design preference, not an experimentally demonstrated optimal policy.

### Recursive door

A library might contain a method for building further library entries. A future reader could inspect and revise such methods. This suggests recursive *method revision* but does not demonstrate autonomous self-improvement. The latter would additionally require reliable evaluation, control, safe execution boundaries, and evidence of actual gains.
