# Procedural Cue Reconstruction

Executable exploration of whether compact semantic cues can induce complex procedural configurations, and whether procedural invariants survive radical domain translation.

**Epistemic status:** Toy experiments and calibration harness. Not evidence of language-model capability. Genuine isolated sessions remain untested.

## Quick start

```bash
cd experiments/procedural-cue-reconstruction
python run_experiments.py
```

## Contents

- `ipap_procedure.py` — Inverted Priority Allocation Protocol (arbitrary, counterintuitive rules) and test cases
- `cues.py` — Full specification, compact cue, paraphrase, generic, random, concise summary, model-style cue
- `harness.py` — Deterministic scoring and simulated responders (perfect / null / partial)
- `cross_domain_naval.py` — Cellular-automaton resource rule translated into eighteenth-century naval powder logistics
- `run_experiments.py` — Runner that prints calibration tables
- `results.md` — Observations, limitations, and untested directions
- `results_summary.json` — Machine-readable summary (generated)

## Distinctions preserved

Cue vs. payload, recall vs. reconstruction, functional equivalence vs. mechanistic identity, capability vs. reliable control.  
All simulated results are explicitly labeled as calibration only.

## Related

- [Capability Discovery Before Capability Engineering](../../explorations/capability-discovery-before-engineering.md)
- [Procedural cue reconstruction note](../../explorations/procedural-cue-reconstruction-note.md)
