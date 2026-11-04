# G. Meta-exploration heuristics

**Status:** open research direction. Conceptual.

## Provocation

Can a system evaluate candidate transformations of its own operations using criteria other than immediate task success—reachability of new states, recoverability of old ones, option value, robustness to distribution shift, or resource efficiency—and what happens when those criteria conflict?

## Requirements

- At least two distinct heuristics that can rank the same candidate transformation differently.
- An external task suite that is not identical to any of the heuristics.
- Explicit cases in which optimizing one heuristic degrades another or degrades the external suite.
- No assumption that expansion of the operation set is the definition of improvement.

## Relation to evaluation drift

If the heuristics themselves can be edited, this direction collapses into C. Keeping the heuristics fixed while the operation set changes is the cleaner first experiment.

## Strongest rival

The heuristics are simply additional objective functions. Multi-objective optimization and Pareto comparisons already describe the conflicts. No new meta-exploration mechanism is required.

## Open

No executable comparison of conflicting heuristics has been added.
