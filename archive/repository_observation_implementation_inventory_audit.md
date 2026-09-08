# Repository Observation Implementation Inventory Audit

## Purpose

This audit investigates the gap exposed when the operator attempted:

```bash
seed --observe-repository .
```

and the CLI returned:

```text
seed_local.py: error: unrecognized arguments: --observe-repository
```

The central question is:

```text
What repository observation implementation actually exists?
```

This is an audit.

It is not a reconciliation, implementation proposal, schema proposal, CLI design,
or roadmap.

## Triggering Finding

Recent work implemented source relationship primitives such as imports and
definitions. Follow-on discussion assumed an operator-accessible repository
observation command existed.

The CLI failure shows that assumption was false.

This exposes an important distinction:

```text
observation primitive exists
        !=
acquisition workflow exists
        !=
operator-accessible CLI entrypoint exists
```

## Evidence Basis

Evidence used for this audit:

- operator execution failure for `seed --observe-repository .`
- existing repository observation/design docs
- recent source relationship observation work
- repository searches for `observe-repository`, `observe_repository`,
  `relationship_observation`, `RepositoryArtifactFact`, and related terms

The repository code search available to this session was incomplete, so this
audit treats the observed CLI failure as decisive for the operator-surface
question, while leaving detailed file-level inventory for a local follow-up if
needed.

## Current Implementation Status

The current implementation appears to include source-observation primitives:

```text
Python import relationship extraction
Python definition relationship extraction
RelationshipFact records
```

These primitives can observe relationships from supplied source text.

They do not by themselves prove that Seed has:

```text
repository traversal
repository file selection
repository observation service
operator CLI entrypoint
fact ingestion path for repository observations
query surface for repository relationships
```

## Boundary Finding

The strongest boundary finding is:

```text
Observation Adapter
        !=
Observation Source
        !=
Observation Acquisition Workflow
        !=
Operator Command
```

An adapter may know how to parse one file.

A source may know how to collect observations from a domain.

An acquisition workflow may coordinate traversal, normalization, ingestion, and
status.

An operator command exposes that workflow.

The current failure indicates the operator command is absent, regardless of the
primitive implementation status.

## What Appears Implemented

Based on recent work and known files, Seed appears to have implemented:

```text
relationship observation primitives
import relationship extraction
definition relationship extraction
unit tests for supplied source text
```

This is useful, but it is not an end-to-end repository observation capability.

## What Is Not Confirmed

This audit does not confirm the existence of:

```text
--observe-repository CLI flag
repository-wide traversal
file filtering rules
source-root selection
repository relationship ingestion into the main event ledger
state summary visibility for repository relationships
current-facts query workflow for source modules
```

The attempted command directly confirms at least the first item is currently
absent.

## Likely Current Shape

The likely current shape is:

```text
caller-provided source text
    ↓
relationship observation adapter
    ↓
RelationshipFact records
```

not yet:

```text
repository root path
    ↓
repository traversal
    ↓
source file observation
    ↓
relationship facts
    ↓
ledger ingestion
    ↓
queryable projected repository knowledge
```

## Why This Matters

Without the acquisition workflow, Seed can have correct source-observation logic
while still being unable to observe its own repository operationally.

That means repository observation validation cannot begin with:

```bash
seed --observe-repository .
```

until an operator-accessible acquisition path exists.

## Distinctions Preserved

```text
Primitive implementation != runnable capability
Runnable capability != operator command
Operator command != authority to execute arbitrary behavior
Source relationship fact != repository-wide knowledge
Test fixture coverage != operational acquisition
```

## Next Safe Work

The next safe work is not more source relationship types.

The next safe work is to complete the vertical acquisition slice:

```text
repository root input
    ↓
file discovery/filtering
    ↓
relationship adapter invocation
    ↓
observation/fact ingestion
    ↓
operator-accessible command
    ↓
queryable output
```

Only after that can the current imports/definitions relationship layers be
validated operationally.

## Non-Goals

This audit does not:

- implement `--observe-repository`;
- define repository traversal rules;
- define file filtering rules;
- add source relationship types;
- change relationship facts;
- change execution authority;
- change CLI behavior.

## Final Finding

The repository observation work currently appears to be a partial horizontal
slice: source relationship primitives exist, but the operator-accessible
repository acquisition path is absent or at least not exposed as
`--observe-repository`.

The next implementation should complete the vertical slice before adding more
relationship depth.
