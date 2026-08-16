# Source Navigation Practical Validation Audit

## Purpose

This audit validates whether the current source-observation facts and existing
general read-model surfaces are sufficient for practical operator source
navigation.

It is a documentation-only implementation validation audit.

It does not change code, schemas, projections, observations, facts, tests,
runtime behavior, source observation behavior, CLI behavior, or storage.

## Trigger

Recent repository work established and stabilized the prerequisite layers for
source navigation:

- repository source observation emits source facts;
- imports and definitions are preserved as evidence-backed relationships;
- repeated repository observation no longer duplicates broad current-fact rows;
- source navigation has been reconciled as orientation over preserved knowledge,
  not a new observation or stronger fact.

The remaining practical question is:

```text
Can an operator answer source-location questions using the existing surfaces,
without a dedicated source navigation surface?
```

## Central Finding

The answer is: partially, but not safely or ergonomically enough.

Existing source facts can answer source-location questions only after the
operator already knows how the source fact is normalized. That means practical
navigation still fails at the operator-term bridge.

The strongest finding is:

```text
existing source facts are sufficient evidence
existing general views are insufficient orientation
```

## Validation Question

The representative operator question is:

```text
Where is state_summary defined?
```

The current repository can preserve an answer such as:

```text
seed_runtime.state_summary_views defines seed_runtime.state_summary_views.state_summary
path=seed_runtime/state_summary_views.py
```

But the operator must often discover this by grepping broad current facts.

## Existing Surfaces Tested Conceptually

### `--current-facts`

`--current-facts` can contain the answer.

It can show rows like:

```text
seed_runtime.state_summary_views defines seed_runtime.state_summary_views.state_summary
```

and path dimensions such as:

```text
path=seed_runtime/state_summary_views.py
```

However, it is a broad fact view, not a source navigator. It requires filtering
or grep and mixes source facts with all other projected fact views.

### `--current-facts SUBJECT PREDICATE`

This can filter if the operator already knows the exact normalized subject and
predicate:

```text
seed_runtime.state_summary_views defines
```

This is useful after discovery, but weak as first-contact navigation.

### `--why-fact`

`--why-fact` can explain exact facts, but it is brittle for source navigation
because the operator must know the canonical subject, predicate, and often the
fully qualified object.

The operator may ask with:

```text
seed_runtime/state_summary_views.py defines state_summary
```

while the stored fact shape is closer to:

```text
seed_runtime.state_summary_views defines seed_runtime.state_summary_views.state_summary
```

The existing explanation surface is therefore evidence-capable but not
navigation-capable from ordinary operator terms.

### `--fact-support`

`--fact-support` exposes support groups for known subject/predicate pairs. It is
valuable after the source relationship is found, but it does not solve initial
source discovery.

### Documentation Surfaces

The source navigation reconciliation and audits explain the boundary, but they do
not provide executable navigation.

## Practical Failure Mode

The practical failure mode is not missing evidence.

It is:

```text
operator knows:        state_summary
stored subject:        seed_runtime.state_summary_views
stored object:         seed_runtime.state_summary_views.state_summary
stored path dimension: seed_runtime/state_summary_views.py
```

Existing general views do not bridge those shapes directly.

The operator must manually infer or grep through:

```text
short symbol
qualified symbol
module identity
repository path
relationship kind
support group
```

This is exactly the gap identified by the source navigation reconciliation:
operators should not need to reverse-engineer fact shape before reaching
preserved source evidence.

## Boundary Finding

The current state has crossed the preservation threshold but not the navigation
threshold.

```text
source observations preserved
source facts support-backed
current fact rows stabilized
        ↓
source navigation now implementation-justified
```

This does not mean Seed needs stronger source claims. It means Seed needs a
read-only orientation surface over the source claims it already has.

## What Is Already Sufficient

The following are sufficient for a first source navigation slice:

- `defines` facts;
- `imports` facts;
- source path dimensions;
- support grouping through `state.fact_supports`;
- stable broad current-fact view;
- exact explanation through `--why-fact` once a fact shape is known.

The first source navigation implementation does not need:

- call graph observation;
- reads/writes/emits/promotes observations;
- behavior inference;
- capability ownership inference;
- runtime reachability inference;
- a planner;
- natural-language interpretation.

## What Is Not Yet Sufficient

The following remain insufficient without a source-specific surface:

- short-symbol lookup;
- path-to-module lookup;
- module-to-path grouping;
- source-specific grouping by `defines` and `imports`;
- support summary for source facts;
- safe bounded output for source-heavy files;
- clear disclosure that definition is not reachability and import is not call.

## Implementation Readiness Finding

A small implementation slice is justified.

It should be read-only and source-specific. It should not add new observation
semantics. It should not infer behavior. It should not modify source extraction.
It should project existing source facts into a navigation view.

The minimal useful behavior is:

```text
input:  state_summary
output: matching definitions, paths, owner module, support summary
```

and:

```text
input:  seed_runtime/state_summary_views.py
output: definitions/imports grouped for that path
```

and:

```text
input:  seed_runtime.state_summary_views
output: definitions/imports grouped for that module
```

## Recommended Next Implementation Prompt Scope

The next implementation prompt should request a narrow source navigation surface,
not another audit.

It should require:

1. a read-only projection/helper over `state.fact_supports` or `build_fact_view`;
2. matching by short symbol, qualified symbol, module, and path;
3. grouping by relationship kind;
4. output of path, module, symbol/object, and support counts;
5. tests proving repeated repository observation does not duplicate navigation
   rows;
6. tests proving no observation ingestion or ledger mutation occurs during
   navigation query;
7. explicit non-goals around call graph, behavior inference, capability
   ownership, and reachability inference.

## Non-Goals

This audit does not recommend:

- adding behavior observations yet;
- adding call graph extraction;
- inferring entrypoints from argparse;
- treating definitions as reachability;
- treating imports as calls;
- changing `--current-facts` again;
- changing source observation extraction;
- changing evidence preservation;
- changing fact support semantics;
- using natural language interpretation for this first slice.

## Invariants

```text
Source navigation should use existing source facts, not create new source facts.
```

```text
Operator-term matching is query orientation, not identity collapse.
```

```text
Definition lookup does not prove reachability.
```

```text
Import lookup does not prove invocation.
```

```text
A source navigation surface must not mutate the ledger.
```

```text
The first source navigation surface should be useful before behavior observations
exist.
```

## Conclusion

The practical validation shows that existing facts and general views are enough
to prove source knowledge exists, but not enough to make that knowledge usable as
operator navigation. The next step should be a narrow read-only source navigation
implementation over existing `imports`, `defines`, path dimensions, and support
projection.
