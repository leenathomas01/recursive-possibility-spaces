# CSAP — Cue-Structure Activation Probe (V1)

Small, reproducible research instrument for examining whether compact natural-language cues can elicit implied procedural and relational behavior.

**This is a measurement harness, not a demonstration engineered to succeed.**

**Status — audit note (2026-11-07):** V1 contains verified measurement and isolation defects and is **not yet valid for real-model capability claims**. In particular, the claimed cross-session and implied-only conditions are not implemented as described, and the committed JSONL is a placeholder. The original V1 code and preregistration are preserved for traceability. See [CSAP V1 audit, observations, and unresolved research directions](../../research-log/csap-v1-audit-and-directions.md). This retrospective note does not select or prescribe a V2.

## What it does
- Three regimes: conventional schemas, novel compositions, seeded arbitrary episode-specific rules.
- Conditions: null, compact, paraphrase, misleading, full-specification, cross-session isolation.
- Implied-only / blind scoring: correct answer or decision must demonstrate relations or procedures **not stated in the cue**.
- Multi-turn persistence check.
- At least one evaluation via observable decision on a novel task.
- Default responder is a **CalibrationSimulator** explicitly labeled as harness calibration only — never evidence of model behavior.
- Optional manual (paste) responder and local-model interface stub.

## Quick start (harness calibration)
```bash
cd experiments/csap
python main.py --responder simulator --seed 42 --output results/csap_v1_results.jsonl --summary
```

Negative and low scores under null, misleading, and cross_session are expected and preserved.

## Files
- `structures.py` — three example structures covering the regimes
- `scoring.py` — deterministic implied-only scoring
- `responders.py` — CalibrationSimulator, ManualResponder, LocalModelResponder
- `harness.py` — full factorial runner, JSONL writer
- `main.py` — CLI
- `PREREGISTRATION.md` — analysis plan fixed before real-model data
- `tests/` — unit tests for scoring and harness determinism
- `results/` — raw JSONL output (simulator calibration only)

## Interpreting results
Comparable performance between a short cue and a full specification is a **behavioral observation**.  
It does not establish any particular latent mechanism.  
It may motivate later mechanistic investigation.  
The CalibrationSimulator exists only so researchers can verify that the scoring and reporting machinery correctly registers both successes and failures.

## Extending
- Add structures in `structures.py` (keep implied elements out of the compact/paraphrase cues).
- Implement a real `generate_fn` and pass it to `LocalModelResponder`.
- Or use `--responder manual` and paste outputs from any model.
- Re-run; raw JSONL and summary will include whatever the responder actually produced.

## Requirements
Python 3.8+. Standard library only. No network, no GPU, no API keys.
