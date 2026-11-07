"""
CSAP V1 entry point.
Default: CalibrationSimulator (harness calibration only).
Optional: manual or local-model responder.
"""

import argparse
import json
from harness import run_experiment, summarize
from responders import CalibrationSimulator, ManualResponder, LocalModelResponder


def main():
    parser = argparse.ArgumentParser(description="CSAP V1 — Cue-Structure Activation Probe")
    parser.add_argument("--responder", choices=["simulator", "manual", "local"], default="simulator",
                        help="simulator = harness calibration only")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="results/csap_v1_results.jsonl")
    parser.add_argument("--summary", action="store_true", help="Print summary after run")
    args = parser.parse_args()

    if args.responder == "simulator":
        responder = CalibrationSimulator(seed=args.seed)
        print("WARNING: Using CalibrationSimulator. Results calibrate the harness only.")
        print("They are NOT evidence of language-model behavior or latent mechanisms.\n")
    elif args.responder == "manual":
        responder = ManualResponder()
    else:
        responder = LocalModelResponder()  # user must have supplied fn externally if needed
        print("LocalModelResponder: no generate_fn loaded in this invocation.")

    results = run_experiment(responder=responder, seed=args.seed, output_path=args.output)
    print(f"Wrote {len(results)} records to {args.output}")

    if args.summary or args.responder == "simulator":
        summ = summarize(results)
        print("\n=== Summary (probe accuracy by regime/condition) ===")
        print(json.dumps(summ, indent=2))
        print("\nNegative / low scores are preserved and expected under null, misleading, and cross_session.")
        print("Comparable short-cue vs full-spec scores would be a behavioral observation only.")


if __name__ == "__main__":
    main()
