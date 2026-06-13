# Source Navigation Without Grep Audit

## Purpose

This document records a bounded implementation-navigation audit prompted by a
practical operator question:

```text
Why did the operator need to grep for the state-summary cache path?
```

The audit asks whether Seed should answer implementation-navigation questions
from preserved repository observations rather than from ad hoc grep output.

This is documentation-only.

It does not implement code, modify schemas, change repository observation
behavior, change state summary behavior, change projection caching, modify tests,
execute repository scans, or introduce runtime semantics.

## Authority And Evidence Basis

This audit is scoped by:

- `docs/source_definitions_and_entrypoint_observation_reconciliation.md`
- `docs/repository_reconciliation_v1_frontier.md`
- `seed_runtime/knowledge/relationship_observation.py`
- the observed operator grep over `scripts/seed_local.py`

Repository authority wins over this audit. This audit records an implementation
navigation gap; it does not promote a new ontology or authorize implementation
changes by itself.

## Current Trigger

The operator needed to answer:

```text
Does seedstate use the projection cache?
Where does --state-summary call project_state_with_cache?
Which code path invokes state_summary(state)?
```

The actual evidence was found through grep:

```text
scripts/seed_local.py imports SQLiteProjectionStore, project_state_with_cache,
and rebuild_state_cache.

scripts/seed_local.py calls project_state_with_cache in local CLI paths.

scripts/seed_local.py renders --state-summary by calling build_state_summary(state)
and state_summary(state).
```

The problem is not that grep is invalid. The problem is that grep output is not
Seed self-knowledge. It is an acquisition capability result that still needs to
be preserved as structured source observations before Seed can answer reliably.

## Current Implementation Baseline

The current relationship observation implementation remains intentionally narrow.

`seed_runtime/knowledge/relationship_observation.py` describes itself as a
`Deterministic Relationship Observation v0 Python import adapter`.

It states that Python import extraction is the first adapter and supports only
static Python `import` and `from ... import ...` syntax from caller-provided
source text.

It also explicitly warns that import relationships are dependency and
name-availability evidence only. They do not prove behavior, calls, routes,
boundaries, or ownership.

Therefore the current implemented source relationship surface can answer:

```text
Which modules or symbols does this file import?
```

It cannot directly answer:

```text
Where is this symbol defined?
Where is this CLI flag declared?
Which branch handles this CLI flag?
Which function calls project_state_with_cache?
Which renderer calls state_summary(state)?
Which path reaches projection cache load/save?
```

## Boundary Finding

Grep is a capability.

Source observation is knowledge acquisition.

They should not be collapsed.

The safer chain is:

```text
grep / AST parser / file scan
        ↓
source observations
        ↓
evidence
        ↓
relationship facts
        ↓
projection / query surface
```

The operator may use grep during investigation, but Seed should not treat raw
grep output as the final knowledge model. The preserved repository knowledge
should name source relationships explicitly and conservatively.

## Existing Architectural Direction

`source_definitions_and_entrypoint_observation_reconciliation.md` already states
that imports reveal dependency, definitions reveal ownership, entrypoints reveal
reachability, and calls / registrations / reads / writes / emits reveal behavior
knowledge.

That reconciliation also identifies a recommended priority:

```text
1. file defines symbol
2. source file declares entrypoint
3. entrypoint invokes or dispatches to symbol
4. module/function direct call edges
5. capability implemented_by symbol, only with explicit registration/catalog evidence
6. domain behavior markers: emits, promotes, produces, reads, writes
```

This audit confirms that the priority remains correct for the current
implementation-navigation problem.

## What Seed Should Have Been Able To Answer

For the state-summary cache question, Seed should eventually answer structured
questions such as:

```text
Which source file imports project_state_with_cache?
Which source file defines project_state_with_cache?
Which CLI flag declares --state-summary?
Which function or branch handles --state-summary?
Which handler calls build_state_summary(state)?
Which handler calls state_summary(state)?
Which code path uses SQLiteProjectionStore?
Which code path rebuilds the projection cache?
```

Import observation alone can partially answer only the first question.

The remaining questions require definitions, entrypoints, dispatch edges, and
selected call/reference observations.

## Relationship Types Needed Next

The next source-observation work should not jump straight to a broad call graph.

A broad call graph without ownership and entrypoint anchors can create many
edges without explaining operator reachability.

The highest-value next layer is:

```text
definitions + entrypoints + conservative dispatch/reference edges
```

Concrete relationship candidates:

```text
file defines symbol
module defines symbol
source file declares CLI flag
CLI flag dispatches to branch/function
function calls function
function references imported symbol
function formats projection
function uses projection cache
```

The last two are more interpretive and should be introduced only when the
relationship vocabulary is defined clearly enough to avoid overclaiming.

## What Should Not Be Done

Do not make Repository Reconciliation own file scanning.

Do not make source observation depend on arbitrary grep output as a final model.

Do not infer ownership from imports.

Do not infer behavior from symbol names alone.

Do not infer CLI reachability from a function definition alone.

Do not infer capability ownership from a file path or import edge alone.

Do not treat source navigation facts as authority to mutate runtime behavior.

## Immediate Implementation Implication

Before expecting Seed to answer implementation-navigation questions without
grep, repository observation needs at least one new source relationship layer
beyond imports.

The most bounded next slice is:

```text
observe Python definitions with file/module ownership and line ranges
```

The next slice after that is:

```text
observe CLI entrypoint declarations and conservative dispatch edges
```

Only after those are stable should broad call/reference observation be used for
state-summary, projection-cache, Prometheus, and repository-observation audits.

## Architectural Invariants Supported

```text
Grep is a capability, not repository knowledge.
Source observation is knowledge acquisition, not final authority.
Imports reveal dependency, not ownership.
Definitions reveal ownership, not invocation.
Entrypoints reveal reachability, not capability authority.
Dispatch/call edges require explicit source evidence.
Implementation navigation requires more than imports.
Source observation must remain read-only and evidence-backed.
```

## Direct Answer

Seed should not merely grep the repository and report grep output as knowledge.

Seed may use grep, AST parsing, or file scanning as acquisition mechanisms, but
the result should be preserved as structured source observations with evidence,
scope, and conservative relationship kinds.

For the current problem, the repository needs source definition and entrypoint
observation before Seed can reliably answer where `seedstate`, projection cache,
and state-summary behavior live without operator-provided grep.
