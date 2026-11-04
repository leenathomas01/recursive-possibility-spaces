# 01 — Premise

**Status:** summary of an external research prompt from an earlier conversation; empirical numbers below were explicitly flagged in the original unpublished notes as needing verification. Do not treat them as independent replication.

The motivating post was [Sparks of Weight-Space Programming](https://rikiyat.github.io/blog/weight-space-programming/), describing an AI system referred to in the conversation as Astra inspecting and modifying neural network weights directly rather than retraining the target.

### Reported observations (source verification required)

- In Qwen3.5-0.8B, a problematic direction was reportedly identified in the MLPs of layers 15 and 19; approximately 0.016% of weights (131,072 parameters) were changed.
- Token-limit hits on MATH-500 responses were reported as approximately 93% before and 33% afterward, connected to a looping failure mode.
- In Gemma 3 270M, where the same obstruction was reportedly absent, the reported best score moved from 6.8% to 7.7%.
- Small networks were also reportedly constructed for constrained game tasks, including Breakout, Seaquest, Asterix, and Go.

The original note interpreted the large change as possibly removing a behavioral obstruction rather than instilling mathematical competence. That is a hypothesis about mechanism, not something benchmark deltas alone prove. The weaker Gemma effect is compatible with this interpretation but not decisive evidence.

### Why preserve this question?

If edits become meaningful units that can be described and tested, a new question arises: **how should their methods, concrete instances, preconditions, and failures be archived?**

Nothing here shows arbitrary reliable model surgery, cross-architecture portability, or autonomous RSI.
