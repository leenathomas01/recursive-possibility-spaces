"""Runner for the procedural cue reconstruction experiments.

Executes:
1. Calibration of simulated responders on IPAP.
2. Cross-domain translation success rates.

All results are from executable code. No fabricated model outputs.
Real isolated model sessions remain untested; the harness is ready for them.
"""

from __future__ import annotations
import json
from harness import evaluate_cue_on_cases, perfect_oracle_responder, null_responder, partial_heuristic_responder
from cues import CUES
from cross_domain_naval import evaluate_translation, generate_test_starts
from ipap_procedure import TEST_CASES


def main() -> None:
    print("=" * 60)
    print("EXPERIMENT 2: Cue-induced procedural reconstruction (IPAP)")
    print("Status: proxy / calibration only. No independent model sessions.")
    print("=" * 60)

    responders = {
        "perfect_oracle": perfect_oracle_responder,
        "null_conventional": null_responder,
        "partial_heuristic": partial_heuristic_responder,
    }

    summary = {}
    for cue_name in ["compact_cue", "paraphrase_cue", "generic_cue", "random_cue", "concise_summary", "full_specification"]:
        summary[cue_name] = {}
        for resp_name, responder in responders.items():
            results = evaluate_cue_on_cases(cue_name, responder)
            exacts = sum(1 for r in results if r["exact_match"])
            avg_prefix = sum(r["prefix_length"] for r in results) / len(results)
            summary[cue_name][resp_name] = {
                "exact_matches": exacts,
                "total_cases": len(results),
                "avg_prefix": round(avg_prefix, 2),
            }
            print(f"{cue_name:20} | {resp_name:20} | exact {exacts}/{len(results)} | avg_prefix {avg_prefix:.2f}")

    print("\n" + "=" * 60)
    print("EXPERIMENT 1: Cross-domain invariant translation (CA -> Naval)")
    print("=" * 60)
    starts = generate_test_starts(n=30, length=6, seed=7)
    scores = evaluate_translation(starts)
    for name, score in scores.items():
        print(f"  {name}: {score:.2f}")

    # Write machine-readable summary
    with open("results_summary.json", "w") as f:
        json.dump({"ipap_summary": summary, "cross_domain_scores": scores}, f, indent=2)
    print("\nWrote results_summary.json")


if __name__ == "__main__":
    main()
