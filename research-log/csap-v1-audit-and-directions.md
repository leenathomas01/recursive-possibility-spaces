# CSAP V1 — observations, independent reviews, and unresolved directions

**Date:** 2026-11-07  
**Status:** Retrospective audit and research log; **open-ended**. No V2 chosen, no claims of model capability established.  
**Scope:** [CSAP V1](../experiments/csap/) and the prior [research provocation](../explorations/capability-discovery-before-engineering.md).  
**Implementation provenance:** Grok reported initial commit `b06ffb248c9aa4b70dde645c03202cb78b4e1770`, followed by small commits on `main`. Claude reported auditing HEAD `ddeaba5`. File paths below refer to the inspected `main` implementation on 2026-11-07.

## 1. Why this exists

The originating question was **not** simply whether short prompts can alter a model's output. It was whether models can *discover, express, and reactivate rich conceptual or procedural configurations* from compact cues—sometimes across conversational boundaries—with much less explicit orientation than a conventional handoff document.

An informal history motivated the question:

- In an earlier GPT-4-era workflow, conversations used structured headers with time, context anchors, and motifs. The model wrote its own headers and sometimes proposed a short handoff phrase before a thread became saturated. In new threads, the user observed striking continuation, sometimes described as verbatim recovery.
- In older Claude interactions without user-visible cross-thread continuity, an opening phrase seemed to re-establish a recognizable **working methodology and model role**, with low orientation overhead. Verbatim recovery was **not** established. Some cues failed and were refined.
- In a later conversation with cross-conversation context available, the cue “bloodhound” elicited a network of relationships around QA practices, investigations, and past experiences. The response was coherent and contextually relevant, but that observation does **not** isolate model-internal capability from the retrieval/context supplied by the product.
- These were user-facing observations across several model products, not controlled tests. Exact model versions, hidden prompts, archived transcripts, and active memory/retrieval mechanisms were not independently audited.

**Initial research wager:** Before engineering a specialized mechanism to recover a working state, characterize what models can already elicit through compact natural-language interfaces. This is a question about *capability discovery*, not evidence of a magical store or lossless compression. MEMORILLA is motivation and comparison, not a target for refutation: https://arxiv.org/abs/2610.21375.

### Essential distinctions

1. A **cue** may be an address, an explicit miniature specification, a compositional instruction, or a trigger for reconstruction. A tiny cue does **not** imply a tiny stored representation.
2. Reinstating a **procedure** is not the same as recalling **episode-specific facts**, and neither establishes how the system did it.
3. Reproducing fluent language about a method is not evidence of **executing** that method.
4. Session continuity may arise from **model priors, current context, product memory, retrieved history, user scaffolding, or combinations**. No model can infer genuinely inaccessible arbitrary assignments by magic.
5. Similar behavior across models is not proof of the same internal representation.

## 2. Origin of CSAP V1

Three independent model proposals were gathered:

- **Gemini — Latent Procedural Unpacker (LPU):** short vs verbose cues, objective structural evaluation. Strength: simplicity. Risk: surface formatting is an inadequate proxy for enacted procedure.
- **Claude — Cue Amplification Probe:** implied-only probes, conventional/novel/arbitrary tiers, distractors, explicit alternative hypotheses, isolation and blind scoring. Strength: experimental discrimination. Risk: forced-choice recall alone can miss actual procedure.
- **Grok — Cue-Structure Activation Probe (CSAP):** relational fidelity and multi-turn procedural persistence, calibration simulator and reusable harness. Strength: attention to behavior across turns. Risk: hand-authored patterns and heuristic metrics may measure superficial compliance.

Grok implemented CSAP V1 with the combined direction and reported five passing tests and a simulator calibration run. These are **implementation claims**, not independently reproduced tests in this log. A later code audit exposed important gaps.

## 3. Audit provenance and confidence

- **Claude:** reported cloning the repository, reading the files, running tests/simulator, and constructing adversarial scorer probes without modifications. Its observations were supplied as a review.
- **Gemini:** could not access the repository and explicitly restricted itself to a **design-level critique**. Its assertion that the repository did not publicly exist was an access-dependent conclusion, not a verified defect. The repository was accessible through a connected GitHub integration during subsequent inspection.
- **Independent source inspection:** the CSAP `structures.py`, `scoring.py`, `responders.py`, `harness.py`, `main.py`, `README.md`, `PREREGISTRATION.md`, tests and results files were read on `main`. The central code-level findings below were corroborated by inspection. **No new local execution of the CSAP tests is claimed here.**

Labels: **[CODE]** directly supported by inspected files; **[METHOD]** methodological interpretation of design; **[HYPOTHESIS]** speculative explanation or proposed research.

## 4. Verified V1 problems (retain, do not silently rewrite history)

| Severity | Finding | Evidence / impact |
|---|---|---|
| Critical | **[CODE] Cross-session and compact use identical prompts.** | `harness.py:build_prompt` assigns `structure.compact_cue` to both conditions. The simulator forces cross-session failure by reading the condition label in `responders.py`. Thus cross-session isolation is not implemented for a real responder. |
| Critical | **[CODE] “Implied-only” answers appear in cues.** | `structures.py` describes “ignore supporting evidence” in the compact Bayes cue and blue=stop/red=continue in the arbitrary cue; corresponding probes ask about exactly those rules. `requires_implication=True` is a flag, not a verified property. |
| High | **[CODE] Option-position bias.** | Five of six correct answers use `correct_index=1` (second displayed option); options are not shuffled. A constant “2” responder would score well without demonstrating understanding. |
| High | **[CODE] Scorer is vulnerable to order, negation, and substring collisions.** | `scoring.py:score_probe_response` scans option text in fixed order and uses token substring fallback. `score_decision_task` checks bare substrings. “disagree” contains forbidden “agree”; “considered” contains expected “red”; mentioning a forbidden path as something *to avoid* can be penalized. |
| High | **[CODE] Persistence is not an actual uncued multi-turn test.** | `run_single` sends independent prompts, each constructed with the cue; prior responses are not passed as conversation history. `score_structure_activation` uses exact implied-phrase matching for continuation. |
| High | **[CODE] Committed result file is not JSONL evidence.** | `results/csap_v1_results.jsonl` contains `PLACEHOLDER_FOR_JSONL_CONTENT_SEE_NOTE`; `results/README.md` describes a seeded calibration run. The supplied summary may reflect a local run, but the claimed raw results are not reproducible from this committed file as-is. |
| High | **[CODE] Calibration is circular.** | `CalibrationSimulator.respond` receives `condition`, `structure_id`, `turn_type`, and emits canned pass/fail text to match the scorer. Tests verify those same conditions. This checks plumbing, not evaluator validity. |
| Medium | **[CODE] Arbitrary configuration is not seeded generation.** | `structures.py` hardcodes one blue/red mapping; `seeded_arbitrary` is descriptive text. No random binding is constructed from the seed. |
| Medium | **[CODE] The `local` CLI path does not load a model.** | `main.py` constructs `LocalModelResponder()` with no `generate_fn`; `responders.py` returns a placeholder string instead of producing a model response or raising. Outputs can be scored despite absence of a loaded model. |
| Medium | **[METHOD] Design has one structure per tier and no real sampling-based uncertainty analysis.** | Three structures × six conditions = 18 cells, each with one structure. A simulator-only result cannot supply statistical evidence of generalization. |
| Medium | **[METHOD] Controls have content confounds.** | The full-specification Bayes prompt announces its composition; the arbitrary misleading cue adds “as usual”; and “later” appears in probe wording without an actual time gap. |

**Consequence:** CSAP V1 is **not ready for model-facing evaluation**, and its scores should not be presented as evidence of compact-cue activation, cross-session persistence, or mechanism. These are flaws in the instrument, not negative findings about the capability itself.

## 5. What survived the audit

- The **question** survives: how do small natural-language cues orient models to complex, useful methods or conceptual configurations?
- The distinctions between **conventional schema**, **novel composition**, and **arbitrary episode-specific rule** are useful, provided tasks and controls are redesigned.
- The **harness skeleton** (separate responder interface, logging intention, condition matrix) may be reusable after the score and condition design are repaired.
- A clearly labeled **simulator-only calibration** remains useful for infrastructure, but cannot establish construct validity.
- Preserving **negative results, competing explanations, and version lineage** is good practice.
- The V1 preregistration is historically useful as a dated pre-real-model plan; it does not rescue an invalid implementation. Future protocol changes should be separately documented rather than retroactively relabeling V1.

## 6. Where the reviews converge—and where they do not

**Convergence:** Both Claude and Gemini challenged surface-form scoring, encouraged tests on unfamiliar tasks, and emphasized real procedural application. Both warned against confusing a successful compact prompt with a discovered internal mechanism.

**Different emphases:**

- **Claude:** privileged *self-keying* (models authoring their own handoff cue), *cue-basin mapping* (decreasing explicit information), and *cross-model convergence*. It suggested redesigning items rather than only patching the scorer.
- **Gemini:** proposed *alien-task transfer*, *multi-turn interruption and resumption*, and *procedural resistance* to conflicting explicit instructions.
- **Current synthesis:** self-keying most closely reflects the initiating anecdote; alien-task decisions and real, uncued continuations are valuable controls. Procedural resistance is lower-priority because instruction precedence can dominate its results without illuminating latent structure.

These are **directions for consideration, not a V2 specification or decision**.

## 7. Candidate research directions (all unselected)

### A. Model-authored self-keying

In a development session, a model participates in constructing a distinctive working methodology. It then authors a very short handoff phrase. A genuinely fresh session receives the phrase and must *execute* the method on unseen tasks.

Compare with length-matched human summaries, truncated specifications, generic descriptions, swapped cues, decoy cues, and null. Keep exact session boundaries and all available context logged. Separate **procedural decisions**, **relation recovery**, and **arbitrary factual recall**.

**Critical boundary:** If an arbitrary rule is absent from the cue and unavailable in the fresh session, success is not expected from priors alone. Unexpected success calls first for leakage checks, not a claim of model-internal memory.

### B. Cue-basin mapping

Build a ladder from full explicit instruction through increasingly compressed paraphrases to opaque handles. Measure held-out task fidelity against *information actually communicated*, not just prompt token count. Look for robust thresholds and nonlinear declines, with counterbalanced paraphrases and cue collisions.

### C. Cross-model convergence with unfamiliar (“alien”) tasks

Use a shared cue across diverse model families, including smaller open models. Test whether they make **comparable procedural decisions** on unfamiliar synthetic inputs; compare against nonce handles, swapped mappings, and explicit full-spec baselines. Similar outcomes do not imply shared internal circuits.

### D. Real persistence and interruption

Supply the cue **once**, continue a real transcript through multiple turns and an unrelated interruption, and probe whether the methodology returns when the task resumes without restating the cue. Distinguish same-session context retention from truly fresh-session behavior.

### E. Mechanistic follow-up, only after reproducible behavior

Where weights and activations are available, use causal interventions and rigorous baselines to distinguish features that merely correlate with orientation from computations necessary for it. Natural-language outputs are not direct views of internal representations.

### Lower-priority control

Conflicting-instruction “procedural resistance” may help characterize robustness, but cannot by itself demonstrate that a compact cue accesses a deep latent configuration; prompt priority and ordinary instruction-following remain alternatives.

## 8. What would make future evidence credible

- Hold out tasks, decisions, and relationship probes from cue creation; do not let the cue explicitly contain the target answer while calling it “implied.”
- Generate truly random bindings when testing episode-specific information; counterbalance answer positions and controls.
- Use exact, unambiguous machine-readable selections for forced choice; score decision *outcomes* rather than accidental substrings. Where free text is essential, blind evaluation and adjudication need separate validation.
- Verify isolation *at the actual model/context boundary*, not through a condition label.
- Preserve full prompts, model/version/settings, memory/tool configuration, transcript history, raw outputs, seeds, and exclusion rules.
- Distinguish what a model can infer from shared prior knowledge, what a cue explicitly carries, and what requires access to earlier episodes.
- Avoid over-interpreting success: behavioral activation alone does not identify storage, encoding, or retrieval circuits.
- Preserve null, failure, and ambiguous observations without tuning the task after seeing a desired answer.

## 9. State of the work

**Recorded today:** qualitative observations, three design approaches, Grok's V1 implementation, Claude's code-level audit, Gemini's design-level critique, and independently corroborated source-level flaws.

**Not done:** no real-model benchmark has been validated; no mechanism has been established; no fixed protocol for the next experiment has been selected; no V1 code or scoring was changed as part of this note.

**Open question:** Can models generate compact, transferable interfaces for operationally rich working configurations, and if so, what information makes the handoff possible?

The project remains deliberately **open-ended**. Future reviewers may argue for repair, replacement, or abandonment of the premise. All are acceptable outcomes when supported by evidence.
