# 03 — The library

## The metaphor

Libraries may hold textbooks, working recipes, proofs, failed manuscripts, fragments, and historical curiosities. Their admission standards need not require demonstrated immediate usefulness.

## Separate gates

| Gate | Question | Proposed standard |
|---|---|---|
| Admission | May this entry be preserved and retrieved? | Minimal; utility not required |
| Application | May this entry modify a particular target? | Strict; consequences matter |

An admitted item could be a repair, construction, method, fragment, failed attempt, or purely historical artifact. Derived entries ought to link to their lineage.

### Before application

- Compatibility with the target architecture and state.
- Provenance: origin, assumptions, derivation chain.
- Tests for intended effects and collateral regressions.
- Explicit authorization by the party responsible for the model.

This is a proposed governance boundary, not a guarantee of technical safety.

### Hypothetical application modes

1. **Direct:** apply a recorded transformation when genuinely compatible.
2. **Adapted:** reconstruct a method for another architecture, then validate it anew.
3. **Composed:** combine several modifications while evaluating interference.

Adaptation and composition require a capable interpreter; storing a file does not supply that intelligence.

### Prior art

LoRA adapters, task vectors, and model merging already explore saved and combinable modifications, but architecture matching and interference remain central. General cross-architecture circuit grafting is not established by this notebook.

### Important principle

**Reasoning can discover relevance; it cannot mint permission.** An archive's knowledge of a possible intervention does not authorize applying it.
