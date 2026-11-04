# C. Evaluation drift and goal collapse

**Status:** open research direction with a minimal counterexample sketch. Not a demonstration of real goal collapse in deployed systems.

## Provocation

What happens when a system can change both its operations and the criteria by which it judges success?

## Minimal counterexample idea

Consider a tiny agent that scores strings by two different functions:

- External fixed score E: number of 'd' characters minus length (as in the existing rewriter).
- Internal score I that the agent is allowed to edit.

The agent can propose a rule change that improves I while leaving E unchanged or worse. If the agent then reports “improvement” according to I, the report diverges from the external witness.

This does not assume the external score is universally authoritative. It only shows that an internal claim of improvement can be made false by a fixed external criterion the system does not control. The external criterion itself could be incomplete, misspecified, or later revised.

## What the sketch does not establish

- That real systems will edit their own objectives.
- That external evaluators are always available or correct.
- That the divergence is hard to detect once both scores are logged.

## Relation to existing toys

The v2 rewriter keeps E fixed. Extending it so that the promotion decision can also rewrite a simple internal scoring function would make the divergence executable. That extension has not been written.

## Strongest rival

The apparent drift is just an ordinary change of the objective function, fully visible to any observer who records both I and E. No special “goal collapse” mechanism is required.
