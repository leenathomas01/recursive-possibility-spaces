# Parallel provenance audits — Gemini, Grok, and Sol (2026-11-05)

**Status:** research record and pre-implementation decision log. **No new detector is implemented or validated in this round.** These notes preserve independently submitted findings and Sol's subsequent audit. They do not supersede the existing [causal-role V1 code](../experiments/causal_role_preservation.py), which remains intact.

**Source provenance:** Gemini and Grok each received separate, overlapping prompts to investigate the V1 observer boundaries, provenance trust, instrumentation, adversarial cases, and conventional baselines. Neither was authorized to push code. Their reports were supplied in the conversation to Zee and Sol. The text below is an attributed synthesis, **not a verbatim archival copy**. Grok said it ran a standalone `independent_detector.py` prototype; its complete source and raw output were **not supplied** in the conversation, so Sol has not independently reproduced those results.

## Baseline under examination

Previous contribution, commit [7e8e3fc](https://github.com/leenathomas01/recursive-possibility-spaces/commit/7e8e3fc89c4be1002e433095d51b7a9e453a666e): [experiment](../experiments/causal_role_preservation.py), [results](../experiments/causal-role-preservation-results.md), [tests](../tests/test_causal_role_preservation.py).

The current `ExecutionHistorian.classify` performs a differential test at input 3 and reads `system.execution_path`. The latter is set by the evaluated implementation, not independently traced. It classifies `path == "coeffs"` as `translated` without itself testing a translated intervention. The `ArtifactArchivist.classify` calls `evaluate` and modifies an artifact, notwithstanding its description as an artifact-only observer. The intervention mutates a live instance and is not rolled back within `classify`. These are directly checkable properties of V1 source. The original seven tests exercise the code's declared outputs, not adversarially reliable provenance.

## Gemini — independently submitted epistemic audit

**Supported observations:**
- Stored artifacts attest to storage, not their live use; self-reported execution labels are claims, not independent provenance.
- Instrumented reads/calls can establish access without proving that the accessed values influence an output.
- Intervention results depend on chosen inputs, mutation semantics, access and sensitivity. Black-box I/O agreement does not identify internal mechanism.
- Proposed adversarial cases: honest provenance, false provenance, decorative/dead read, and translated adapter that preserves an intervention effect while changing the underlying implementation.
- Proposed observer outcomes include intervention-backed causal support, read-backed structural corroboration, external behavioral agreement, contradictions, and underdetermination.
- Illustrated an observer-access indistinguishability example: a model and a lookup implementation can present matching outputs and coarse trace events within stipulated access.

**Limitations/corrections:** Gemini supplied illustrative Python but did not supply independently verified execution results in this round. Its sample classifies unchanged outputs plus a claimed rule path as **"Telemetry Contradicted"**, despite not observing the actual path. That conclusion does not follow: an active rule may be insensitive on the chosen input. Gemini's claim that tracing or slicing perfectly settles all decorative dependencies is stronger than warranted without a specified faithful, complete analysis and control/data-flow model. Execution timing alone does not guarantee distinguishing two implementations; either may be engineered to equalize timing. Its proposed need for "incomputable translation bounds" conflates uncomputability with **computable but resource-prohibitive** translation. Resource-bounded inadequacy needs explicitly defined tasks, observers and budgets; neither alone proves a new computational ontology.

## Grok — independently submitted implementation audit

**Source-grounded observations:** Grok flagged V1's self-reported `execution_path`, overly powerful archivist, input-3-only intervention sensitivity, non-rollback, and string/attribute-dependent labels. It also recognized finite-domain equivalence, fixed rather than recursive implementations, and externally supplied intervention translation.

**Reported local prototype (not committed, not independently rerun here):**
- Wrapped calls to `evaluate` and `intervene_rule` and compared outputs on several inputs, without using `execution_path` as the *primary* decision.
- Reported active case with changed inputs `{3,4,-1}`; hollowed, deceptive and decorative cases unchanged; translated case `intervention_unavailable` because the exposed method was missing.
- Demonstrated `high_add` intervention on input 3 gives no change, while input 7 does change in an active system.
- Reported labels including `causal_role_supported`, `no_effect_on_tested_inputs`, and `provenance_contradicted_inert`.

**Limitations/corrections:** The report still calls deceptive/decorative provenance "contradicted" based on a null intervention combined with a self-claim, which does **not** establish that the claimed path was false. Its claimed trusted boundary uses black-box calls and return values, but the proposed stronger debugger comparison assumes access to internal reads; that is a useful richer-access reference, **not** an equal-access baseline. It is not established from the supplied report whether fresh instances/rollback and intervention side-effect controls were fully implemented. An omitted `intervene_rule` interface does not establish absent causal influence or failed translation.

## Sol — independent synthesis and adversarial thoughts

### 1. Shared blind spot: absence of an observed effect is not a provenance contradiction

Both proposals sometimes promote `no measured output change` + `claimed rule execution` into `provenance contradicted`.

Counterexample: `low_mult` controls the lower branch; altering `high_add` while querying only input 3 leaves a fully active rule-driven system unchanged. Grok's own reported input-3 versus input-7 test illustrates this. Even with more samples, one cannot infer **global** causal inertness without domain coverage or additional justified assumptions.

A detector must be allowed to return **inconclusive** despite the experiment designer knowing the ground truth. A negative intervention says only that the specified intervention did not change the specified observations, assuming it was validly applied and measurement was trustworthy.

### 2. Four different claims must not collapse

1. **Artifact present:** structure exists in inspectable storage.
2. **Access observed:** some trusted instrumentation observed a read, call, or dispatch.
3. **Causal effect supported:** controlled, semantically valid intervention changed a measured output, with side effects and confounders addressed to the experiment's stated standard.
4. **Provenance verified or contradicted:** trusted execution evidence independently supports or conflicts with a *specific* execution claim.

Reading data is not necessarily using its value. An observed effect does not prove the claimed route of influence: an error handler, adapter or unrelated side effect could mediate it. Conversely, no effect does not refute use.

### 3. A causal claim needs a specified scope

Treat `dependence(artifact, intervention, input_set, time/state, allowed_mechanisms)` as the object of testing rather than an unconditional bit `artifact_is_active`. Multiple interventions, sensitive test inputs, explicit baseline/recovery, and finite-domain language improve evidence quality. They do not magically yield a complete causal proof.

For deterministic, isolated toys, a changed output after a single valid controlled mutation supports a *local* counterfactual relationship. It does not by itself identify which internal path propagated the change. For adaptive systems with internal state, compare matched fresh instances or snapshots and consider interference between trials.

### 4. Provenance validation has its own trust boundary

Self-reported `execution_path` is merely a claim. A trusted wrapper that records its *own* calls is stronger evidence of those calls but does not see every internal access. Hooks inside untrusted code can also lie. A higher-privilege tracer may improve access but expands the trusted computing base. State who owns the instrumentation, what events it can miss, and whether the system can detect or tamper with it.

### 5. Construct an indistinguishable pair before designing the classifier

Prepare A (rule causally active, intervention insensitive for permitted inputs) and B (artifact inert, same outputs and self-reports under those queries). If their *entire allowed observation transcripts* are identical, no observer limited to that interface can distinguish them. This is a formal access-boundary result, **not** a universal impossibility. Expand permitted interventions, input coverage, independent dispatch observations or actual execution inspection step by step and measure which extra observation first separates them.

Beware making the pair distinguishable by leaking class names, method existence, source inspection, artifact hashes, timing or diagnostic exceptions not included in the declared observation contract.

### 6. Translation is a separate question

An adapter may make a change to an old artifact affect new execution without natively running old rules. The test should distinguish **causal influence of old artifact**, **native execution of old interpreter**, and **successful translation of intervention semantics**. One matching output is not a general equivalence proof. A fair fixed conventional interpreter with equal observations and intervention opportunities remains a required comparator.

### 7. What this does *not* demonstrate

Nothing observed here establishes recursive state-space molting, non-computable translation, ontological novelty, or a computational advantage over ordinary program slicing, debugging, dependency tracking, and intervention testing. Some analyses of computational organization may nonetheless be practically inadequate under explicitly stated resource/access constraints. That weaker, testable claim remains open.

## Pre-implementation gate — what Grok's eventual V2 should demonstrate

- Preserve V1 and both attributed audit records; build V2 in separate files.
- Declare observer capabilities and trusted computing boundary **before** running tests.
- Include matching-transcript active/inert pair and an abstention test.
- Include honest/false self-report, decorative read, translated adapter, intervention-insensitive branch, partial/invalid translation, mutation side effect/error fallback, and incomplete instrumentation.
- Distinguish **claim contradiction backed by independent execution evidence** from merely **no intervention effect observed**.
- Use fresh instances or proven rollback; test multiple relevant inputs, and never equate missing interface with a negative causal verdict.
- Explicitly quantify evaluation/intervention/trace operations and compare with a conventional competitor under **the same access and costs**. A richer-access diagnostic baseline can be reported separately.
- Retain unexpected failures and new false-positive/false-negative examples; do not conceal them to achieve a passing suite.
- Require independent review of the new code and outputs before treating any detector as authoritative.

**Decision at this stage:** Zee authorized archival of lineage and Sol's independent reasoning, **not** implementation of V2 or automatic acceptance of a detector. Grok can receive the separate scoped implementation prompt after this record is preserved.
