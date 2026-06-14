# Source Navigation Query Surface Design Audit

## Purpose

This audit designs the next bounded source-observation navigation surface now
that imports, definitions, and current fact-view duplicate stabilization exist.

It is a documentation-only implementation design audit.

It does not change code, schemas, projections, observations, facts, tests,
runtime behavior, source observation behavior, CLI behavior, or storage.

## Trigger

Repository self-observation has moved beyond imports. Live operator checks and
recent implementation work show that `imports` and `defines` facts are present,
evidence-backed, and no longer need to duplicate in the broad current-facts view
after repeated repository observation.

The remaining problem is not preservation. It is navigation.

Operators still need to answer questions like:

```text
Where is state_summary defined?
What file owns this symbol?
What symbols does this file define?
Where is --state-summary exposed?
What implementation surface should I inspect next?
```

The broad `--current-facts` view can contain the answer, but it is not the right
operator interface for source navigation.

## Central Finding

Seed needs a source-focused read-only query surface over existing source facts.

The core boundary is:

```text
source facts preserved in current state
        !=
source navigation answer
```

`imports`, `defines`, and entrypoint observations should remain ordinary
provenance-backed facts. A source navigation surface should be a read-only view
over those facts, not a new source of truth and not a new ingestion path.

## Existing Implementation Surface

### Current Fact View Is Now Support-Based

`seed_runtime/state_views.py` now builds `FactView` rows from
`state.fact_supports` rather than raw `state.facts`:

```python
for support in sorted(state.fact_supports, ...):
    FactView(...)
```

This is the correct stable base for source navigation because repeated durable
claims render once while supporting provenance remains attached.

### CLI Already Has Read-Only View Patterns

`scripts/seed_local.py` already exposes read-only surfaces such as:

```text
--current-facts
--current-observations
--current-issues
--fact-support
--why-fact
--relationships
--state-summary
```

A source navigation query should follow that style: project existing state,
print a deterministic read-only view, and exit without ingesting observations or
executing tools.

### Repository Source Observation Already Emits Relationship Facts

`RepositorySourceObservationSource` emits relationship observations from source
files with:

```text
subject = module identity
predicate = imports or defines
value = imported symbol/module or defined symbol
dimensions.path = repository path
```

That means source navigation can start without changing repository observation
semantics.

## Design Boundary

A source navigation query surface should answer navigation questions, not broaden
what source observations mean.

It must preserve:

```text
imports != calls
defines != invocation
entrypoint != capability
module identity != path identity
symbol identity != behavior
navigation != authority
```

A source navigation surface may say:

```text
seed_runtime.state_summary_views defines seed_runtime.state_summary_views.state_summary
```

It must not say:

```text
state_summary is correct
state_summary is reachable
state_summary is authorized
state_summary owns all summary behavior
```

unless additional relationships support those stronger claims.

## Recommended Minimal Surface

Start with one read-only source query command rather than several commands.

Candidate CLI shape:

```text
seed --source QUERY
```

or:

```text
seed --source-symbol QUERY
```

The exact name is implementation choice, but the surface should initially support
three operator lookup modes:

1. symbol lookup;
2. file/path lookup;
3. module lookup.

### Symbol Lookup

Input examples:

```text
state_summary
seed_runtime.state_summary_views.state_summary
PrometheusObservationSource
```

Should return matching `defines` facts, including:

```text
symbol
module
path
predicate=defines
support count
representative fact id or support ids
```

### File / Path Lookup

Input examples:

```text
seed_runtime/state_summary_views.py
scripts/seed_local.py
```

Should return source facts with matching `dimensions.path`, grouped by type:

```text
defines:
  ...
imports:
  ...
entrypoints:
  ... when present
```

### Module Lookup

Input examples:

```text
seed_runtime.state_summary_views
scripts.seed_local
```

Should return source facts where the module identity is the subject.

## Query Matching Requirements

The surface should tolerate common operator terms without changing fact identity.

### Path-like input

If the query contains `/` or ends in `.py`, match against:

```text
dimensions.path
metadata.source_path when available through evidence
```

Do not rewrite stored subject identity.

### Module-like input

If the query contains `.`, match against:

```text
subject
object
```

### Short symbol input

If the query has no path separator and no module prefix, match against the final
symbol segment of the object:

```text
state_summary
```

matching:

```text
seed_runtime.state_summary_views.state_summary
```

This should be query aliasing, not identity collapse.

## Output Requirements

Output should be compact and grouped.

Suggested shape:

```text
Source Navigation

query: state_summary

Definitions:
  seed_runtime.state_summary_views.state_summary
    path: seed_runtime/state_summary_views.py
    owner: seed_runtime.state_summary_views
    support: 1 fact / 1 evidence

Related imports:
  (optional, only if directly matched)

Entrypoints:
  (none)
```

For path lookup:

```text
Source Navigation

query: seed_runtime/state_summary_views.py

Defines:
  state_summary
  storage_state_projection
  ...

Imports:
  State
  is_fact_expired
  ...
```

The first implementation should avoid dumping hundreds of rows without limits.
Use clear bounded output with a count if necessary, but do not hide exact-match
results.

## Evidence / Support Behavior

The source navigation output should not require full evidence rendering by
default. It should expose enough support metadata to preserve trust:

```text
support facts: N
support evidence: N
representative fact id: ...
```

A follow-up can use existing `--why-fact` or future source-specific explanation
commands.

The source navigation surface should reuse support groups where possible so
repeated observations do not duplicate rows.

## Relationship Types Included

Initial scope:

```text
imports
defines
```

Include entrypoints only if current implementation already emits entrypoint
facts. If entrypoint facts are not yet emitted, the command should not invent
entrypoints from argparse or prose.

Future scope may include:

```text
entrypoints
calls
reads
writes
emits
promotes
```

but those should not be added until the corresponding observations exist and are
bounded.

## What This Solves

This surface would let the operator answer:

```text
Where is this symbol defined?
What source file owns this definition?
What does this file import?
What does this module define?
What source facts support this navigation answer?
```

without grepping raw `--current-facts` output.

## What This Does Not Solve

This surface does not answer:

```text
Who calls this function?
Which CLI flag dispatches here?
What behavior does this function perform?
What runtime capability owns this path?
Is this code correct?
Is this code reachable?
```

unless future source observations add entrypoint, call, dispatch, behavior, or
capability-binding relationships.

## Candidate Implementation Files

Likely implementation surfaces:

```text
seed_runtime/state_views.py
scripts/seed_local.py
tests/test_seed_local_script.py or tests/test_observation_sources.py
```

A small helper module may be justified if source navigation logic becomes larger
than a few functions, but the first slice should remain narrow.

## Tests To Add

Add tests that observe a small repository fixture and prove:

1. short symbol lookup finds a fully qualified `defines` fact;
2. path lookup returns definitions for that file;
3. module lookup returns definitions/imports for that module;
4. repeated repository observation does not duplicate source navigation rows;
5. support counts increase or remain explainable after repeated observation;
6. unsupported facts remain absent;
7. no source query appends events or ingests observations.

## Non-Goals

Do not:

- change source extraction;
- add call graph extraction;
- infer entrypoints from argparse unless an entrypoint observation already exists;
- collapse path identity into module identity;
- collapse short symbol identity into fully qualified symbol identity;
- change `--current-facts` semantics again;
- modify observation ingestion;
- modify evidence preservation;
- execute repository code;
- import observed repository modules;
- call providers;
- mutate the ledger.

## Invariants

```text
Source navigation is a read-only projection over preserved source observations.
```

```text
Query aliases are not identity claims.
```

```text
Definitions answer ownership, not reachability.
```

```text
Imports answer dependency/name availability, not behavior.
```

```text
Stable source navigation should reuse support-group semantics, not raw fact-row
multiplicity.
```

## Conclusion

The next implementation slice should be a small read-only source navigation query
surface over existing `imports` and `defines` facts. The system now preserves the
necessary source observations and stabilizes duplicate current durable claims.
The missing layer is a navigation view that accepts operator terms and maps them
to existing source relationship support without changing the underlying
observation, evidence, or fact semantics.
