# Capability Discovery Before Capability Engineering

**Status:** Research provocation / anecdotal observation, not a demonstrated mechanism  
**Question:** What useful semantic and procedural configurations can existing language models already activate from compact natural-language cues, and how should that affect the design of external memory systems?

## The provocation

Language-model memory research often begins by specifying an engineering bottleneck: long histories, context limits, lossy compression, retrieval cost. It then introduces an explicit storage, compression, or retrieval mechanism.

A complementary research program would start *upstream*: characterize the native capabilities exposed through interaction **before** concluding that a new mechanism is necessary.

A short word, phrase, motif, or structured cue can sometimes elicit a surprisingly rich and coherent configuration: relevant background, relational connections, conversational conventions, an investigative method, or a model's role in an unfinished exploration. The cue is not necessarily a compressed copy of that information. It may be an effective *address*, a trigger for reconstruction, or a prompt that induces an equivalent working state.

These explanations must not be conflated.

## Attribution: observation versus design

**Original observation and research impetus — Zee (human participant and observer).** Zee independently noticed and reported that short words or phrases sometimes appeared to re-establish rich conceptual relationships, working methodologies, or continuity across conversations and model products. Zee brought these observations into this investigation, recognized their possible relevance to capability discovery, and initiated the research question.

**Not designed by Zee.** The specialized header format used in the early conversations was **not authored by Zee** (its original author is not established in this record). Participating AI models generated their own structured response headers and proposed compact handoff phrases as conversations evolved. Zee used, observed, and sometimes refined those cues when orientation failed; this is not a claim that Zee designed the underlying continuity protocol, retrieval system, model representations, or implementation.

**Subsequent research design and implementation — AI-assisted collaboration.** Gemini, Claude, and Grok proposed experimental approaches; Grok implemented CSAP V1; Claude and Gemini provided different kinds of review; ChatGPT/Sol synthesized the observations, experiments, and findings under Zee's direction. These are model-produced research artifacts, not protocols personally designed by Zee.

**Scope of credit:** Attribution here records **who reported the originating observation and who produced the subsequent artifacts**, not scientific priority over any independently existing effect, proof of its mechanism, or authorship of technology outside this project.

## Originating observations (informal, retrospective)

In exploratory conversations across several user-facing, instruction- or reinforcement-tuned models, a user observed:

1. An early GPT-4-era workflow employed structured turn headers (e.g. time, context anchor, primary motif) and corresponding model-generated headers. At a saturated thread boundary, the model could propose a short handoff phrase. A fresh thread sometimes appeared to resume the earlier conceptual trajectory, with reports of verbatim continuity.
2. In older Claude conversations without a user-facing cross-thread memory feature, compact opening phrases could promptly establish a recognizable collaborative methodology and prior role. This was primarily **operational orientation**, not verified verbatim recovery. Occasionally it failed; revising the phrase improved orientation.
3. In a later system with access to cross-conversation context, the single cue “bloodhound” elicited a structured network of QA-related associations across prior conversations, rather than just an isolated definition.

These observations are *not* controlled demonstrations of cross-thread memory, model-internal persistent storage, universal behavior across systems, or a specific latent mechanism. The relevant prompt transcripts, complete hidden context, retrieval infrastructure, and model versions have not been independently audited. Selection effects and post-hoc interpretation remain possible.

Their value is as **hypothesis generators**.

## Distinctions the research must preserve

- **Cue vs. payload:** A few words may point to an enormous external or internal information source; a small key is not evidence of a small stored representation.
- **Recall vs. reconstruction:** Accurate-seeming continuity is not proof of verbatim recovery.
- **Semantic continuity vs. procedural continuity:** Recovering facts differs from restoring roles, methods, priorities, and conventions.
- **Model capability vs. application infrastructure:** Retrieved user-history snippets, system prompts, caches, and search tools may account for some behavior.
- **Functional similarity vs. mechanistic identity:** Two models may produce equivalent working behavior through dissimilar internal computations.
- **Capability vs. reliable control:** An occasionally successful behavior is not automatically a deployable memory system.

## Candidate research questions

1. How much of a complex **working configuration** can be induced by a compact cue in a genuinely fresh, isolated session?
2. Which aspects are stable across model families, paraphrases, model versions, and changes in surrounding context?
3. Can a model **generate a better handoff cue** after participating in an exploration than an independent model or human given only a summary?
4. Is the effect primarily the recovery of facts, the activation of associations, the reconstitution of a procedure, or some mixture?
5. When a cue is ambiguous or associated with contradictory threads, what determines which structure becomes relevant?
6. Can interpretability methods identify causal internal features associated with procedural orientation, rather than merely correlated surface tokens?
7. Where do existing memory architectures materially outperform cue-based orientation, and where could the approaches complement each other?

## Proposed falsifiable experiments

### A. Isolated handoff study
Establish an unfamiliar collaborative procedure with arbitrary rules and a multi-step task in session A. Have the model produce a short handoff cue. In session B, guarantee no access to the prior transcript, saved memory, tools, or hidden summaries. Compare: generated cue, generic description, random cue, human-written summary, and full transcript. Evaluate procedural compliance, conceptual transfer, and arbitrary-fact recall **separately**.

**Falsifier:** The generated cue performs no better than a length- and specificity-matched generic prompt once hidden continuity and shared training priors are controlled.

### B. Source-access crossover
Repeat with graded access: no history, a short summary, relevant retrieved excerpts, or full verbatim history. Log exact material visible to the model. Score factual exact match, semantic consistency, and next-step quality independently.

**Falsifier:** Apparent cross-thread verbatim continuity vanishes when external retrieval is removed.

### C. Cue perturbation and collision
Vary wording, motif, header syntax, and irrelevant surrounding text. Give one cue two incompatible meanings in distinct sessions. Test whether the model abstains, blends, or reliably separates the competing configurations.

**Falsifier:** Performance depends on explicit restatement of the task rather than distinctive cue structure.

### D. Model-generated protocols
Compare model-authored handoff protocols with researcher-authored ones under matched token budgets. Include blind grading and multiple independent seeds/models to avoid selecting only successful examples.

**Falsifier:** Model-generated protocols show no generalizable advantage under controlled evaluation.

### E. Internal mechanism investigation
Where model weights and activations are available, examine representation similarity and use causal interventions (activation patching, feature ablation, or other validated tools). Distinguish representational correlates from causally necessary computations.

**Falsifier of a proposed circuit:** Disabling the candidate features does not selectively impair the measured orientation ability.

## Relationship to MEMORILLA

[MEMORILLA: Latent Semantic Memory for LLMs](https://arxiv.org/abs/2610.21375) learns a query-conditioned module that converts stored document embeddings into a fixed budget of latent memory tokens for a frozen decoder. Its reported results address important efficiency and answer-quality questions.

This note **does not contest those benchmark results**. It asks an orthogonal question: before engineering yet another way to package relevant context, have we characterized how much structured, useful behavior existing models can already evoke from minimal cues, and what that phenomenon actually depends on?

The answer might be “mostly generic prompting plus infrastructure.” That is a worthwhile result. Alternatively, systematic studies might reveal reusable semantic-addressing or procedural-orientation mechanisms that inform future memory designs.

## What would count as progress?

Not a striking anecdote, a metaphor about ZIP files, or a model's confident account of its own internals.

Progress would be a reproducible protocol; careful controls for hidden retrieval; distinct metrics for facts, relations, and procedural behavior; negative results; and—where possible—causal evidence for the mechanism.

**Core wager:** Capability discovery should be a first-class stage of capability engineering. The possibility space visible through model interaction may not match the capability taxonomy assumed at the beginning of a research program.

**Invitation:** Researchers in LLM memory, in-context learning, representation learning, interpretability, and human–AI interaction are welcome to test, falsify, refine, or replace this framing.
