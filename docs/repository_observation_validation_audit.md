# Repository Observation Validation Audit

## Purpose

This document validates the current repository-observation work at the boundary
between source observation capability and implementation navigation usefulness.

The central question is:

```text
What repository knowledge is currently observable?
```

This is an audit.

It is not an implementation proposal, reconciliation, schema proposal, runtime
change, or command-design document.

## Context

Recent source-observation work added deterministic repository relationship
observation in stages:

```text
imports
    -> dependency knowledge

defines
    -> source definition / ownership-location knowledge
```

The next question is not immediately what else should be implemented.

The next question is whether the current source-observation layers are useful
for Seed's own implementation navigation.

## Evidence Basis

This audit is grounded in the current source-observation and navigation work,
including:

- `docs/source_definitions_and_entrypoint_observation_reconciliation.md`
- `docs/source_navigation_without_grep_audit.md`
- `docs/repository_observation_source_design.md`
- `docs/repository_observation_v0_implementation_characterization.md`
- `seed_runtime/knowledge/relationship_observation.py`

Repository authority wins if this audit diverges from an authoritative document.

## Current Observed Relationship Coverage

Current repository relationship observation is expected to cover:

```text
file/module imports symbol or module
file/module defines top-level function
file/module defines async function
file/module defines class
```

These relationships support two important implementation-navigation questions:

```text
What does this source file depend on?
Where is this symbol declared?
```

They do not yet support execution reachability.

## Validation Questions

A local validation pass should ask whether Seed can locate and explain source
relationships for known implementation symbols such as:

```text
project_state_with_cache
SQLiteProjectionStore
StateProjector
state_summary
build_state_summary
ObservationIngestor
ObservationIngestor.ingest_many
EventLedger.append_many
SQLiteEventLedger.append_many
```

Expected answerable questions with the current relationship surface:

```text
Which module defines StateProjector?
Which module defines project_state_with_cache?
Which module defines state_summary?
Which module imports project_state_with_cache?
Which module defines ObservationIngestor?
Which module defines EventLedger?
```

Expected still-unanswerable questions:

```text
Which CLI flag reaches state_summary?
Which branch dispatches --state-summary?
Which function calls project_state_with_cache?
Which path reaches summary-cache load?
Which path reaches projection-cache save?
Which command reaches ObservationIngestor.ingest_many?
```

Those require entrypoint, dispatch, call/reference, or behavior-marker
observations that are not part of the current imports/defines surface.

## What Works In Principle

The current imports + definitions layers should let Seed preserve:

```text
source dependency knowledge
source definition knowledge
module-level symbol ownership/location knowledge
```

This is already useful.

It moves repository navigation from:

```text
grep for a name
```

toward:

```text
query observed source relationships
```

For example, a definition relationship can preserve that a symbol exists in a
specific module without asserting behavior, invocation, or authority.

## What Does Not Work Yet

The current relationship surface should not be expected to answer:

```text
how operator commands reach behavior
which functions call which functions
which code path performs a projection
which code path writes a cache
which source unit implements a capability
```

Those questions require additional relationship families.

## Boundary Findings

The audit preserves these distinctions:

```text
Import != Ownership
Definition != Invocation
Definition != Behavior
Entrypoint != Capability
Dependency != Reachability
Symbol != Behavior
File != Capability
```

Current `defines` observations improve source navigation but must not be treated
as proof that a symbol is executed, reachable, correct, authoritative, or
capability-owning.

## Operational Validation Needed

A concrete local validation pass should run repository observation and inspect
facts for selected source modules.

Suggested commands:

```bash
seed --observe-repository .
seedstate
cf scripts.seed_local | grep -E "imports|defines" | head -80
cf seed_runtime.projection_store | grep -E "imports|defines" | head -80
cf seed_runtime.state | grep -E "imports|defines" | head -80
cf seed_runtime.observations | grep -E "imports|defines" | head -80
cf seed_runtime.events | grep -E "imports|defines" | head -80
```

The validation should determine whether observed facts are:

```text
correct
queryable
not overly noisy
not collapsed onto host identity
not confused with runtime capability authority
```

## Likely Next Missing Relationship

If imports and definitions validate successfully, the next highest-value missing
relationship is likely:

```text
entrypoint observation
```

Reason:

```text
definitions answer where a symbol is declared
entrypoints answer where behavior can be entered
```

The recent `seedstate` tracing problem needed more than definitions.

It needed to answer:

```text
which operator surface reaches this behavior?
```

That is an entrypoint / dispatch question, not a definition question.

## Non-Goals

This audit does not:

- implement entrypoint observation;
- implement dispatch observation;
- implement call graphs;
- implement source query commands;
- modify repository observation behavior;
- modify runtime behavior;
- define new schema;
- create authority over code execution.

## Final Finding

The current repository-observation surface should be validated before adding more
source relationships.

The expected useful coverage is:

```text
imports + definitions
```

which supports dependency and declaration-location questions.

The expected remaining gap is:

```text
entrypoints + dispatch/reachability
```

which supports operator-path questions.

A future implementation should only move to entrypoint observation after local
validation confirms that imports and definitions are being observed, preserved,
and queried safely.