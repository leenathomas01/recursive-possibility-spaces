# E. Ontological explosion and search constraints

**Status:** open research direction. Conceptual.

## Provocation

When a system can add or rewrite its own operations, when does the set of reachable behaviors grow combinatorially, collapse, cycle, or simplify? Theoretical cardinality and practical accessibility under a resource budget need not move together.

## Distinctions

- Adding a macro can reduce search depth for some tasks while increasing the branching factor for others (already visible in the v2 rewriter).
- Removing operations can shrink the reachable set.
- Cycles of promotion and demotion can leave the operative vocabulary oscillating without net expansion.
- A fixed meta-interpreter may see monotonic growth in its data structures while the operative regime experiences contraction.

## What would be useful

A small generator that can both add and delete rules, run under a shared budget, and report the size of the practically reachable set (not merely the size of the rule table) before and after each change. Negative cases (net shrinkage, cycles) should be included by construction.

## Strongest rival

All observed growth or shrinkage is ordinary search-cost change inside a fixed language. No new cardinality phenomena are required.

## Open

No such generator has been added. The v2 rewriter already supplies one data point of non-expansion under promotion.
