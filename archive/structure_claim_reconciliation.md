# Structure Claim Reconciliation

## Purpose

This document reconciles the next evidence boundary after explicit existence-claim reconciliation.

The first implementation slice is intentionally tiny and fixture-only. It does not modify runtime behavior, repository scanning, file reading, LLM extraction, tool execution, event storage, projection behavior, or package exports.

The motivating question is:

```text
When is repository evidence strong enough to support a structure claim,
and how is that different from existence or ownership?
```

## Position In The Evidence Ladder

The current self-model evidence ladder is:

```text
Existence
        ↓
Structure
        ↓
Behavior
        ↓
Boundary
        ↓
Ownership
```

Existence asks whether named artifacts exist.

Structure asks whether artifacts are arranged or related in a specific static shape.

Behavior asks whether code actually participates in a runtime behavior.

Boundary asks whether tests, invariants, or architecture metadata preserve a responsibility boundary.

Ownership asks whether a component is the architectural owner of a responsibility.

This document covers only the structure layer.

## Relationship To Existing Existence Claims

`docs/existence_claim_reconciliation.md` defines these existence forms:

```text
X exists.
X defines Y.
```

The tightened `X defines Y.` existence rule requires exact symbols for `X` and `Y` from the same supplied source path.

That is still not full structural evidence.

Same-path evidence means:

```text
The supplied artifact facts show X and Y exist in the same source file.
```

It does not mean:

```text
Y is a method of X.
Y is nested under X.
X owns Y.
X calls Y.
X routes to Y.
X implements Y's behavior.
```

Structure reconciliation starts where same-path existence stops.

## What Is A Structure Claim?

A structure claim asserts a static relationship between repository artifacts.

Examples:

```text
Runtime defines method handle_user_message.
ToolExecutor defines method execute.
ProjectionStore declares get_snapshot.
SQLiteProjectionStore implements ProjectionStore.
ContextPacket has field current_input.
Runtime imports ToolExecutor.
```

These are stronger than pure existence claims because they assert a relationship or shape, not just symbol presence.

They are weaker than behavior or ownership claims because they do not prove runtime flow, policy behavior, or architectural responsibility.

## Candidate Structure Claim Forms

Implemented v1 supports only one explicit form. Other forms remain future work.

### `X defines method Y.`

Status: implemented as the only v1 `structure` claim form.

Meaning:

```text
Class or object X has a method named Y in the supplied source structure.
```

Example:

```text
Runtime defines method handle_user_message.
```

Likely evidence:

- class artifact `Runtime`;
- function/method artifact `handle_user_message`;
- containment metadata showing `handle_user_message` belongs to `Runtime`.

Same-path alone is insufficient for this claim.

V1 reconciliation reports `supported` only when the supplied fixture artifact facts contain both:

```text
artifact_kind="class"
symbol=X
```

and:

```text
artifact_kind="method"
symbol=Y
parent_symbol=X
```

If the `X defines method Y.` pattern is recognized but those facts are not present, v1 reports `missing_support`. Structure prose that does not match this exact pattern is `not_evaluable` if manually supplied and is not extracted by documentation observation.

### `X defines function Y.`

Status: future work.

Meaning:

```text
Module or artifact X defines a top-level function named Y.
```

Example:

```text
repository_observation defines function extract_repository_artifact_facts.
```

Likely evidence:

- module artifact for `repository_observation` or its path;
- function artifact for `extract_repository_artifact_facts`;
- top-level function metadata or module-level containment evidence.

### `X has field Y.`

Status: future work.

Meaning:

```text
Class, dataclass, model, or record X declares a field named Y.
```

Example:

```text
ContextPacket has field current_input.
```

Likely evidence:

- class artifact `ContextPacket`;
- field artifact `current_input`;
- containment metadata linking the field to `ContextPacket`.

### `X imports Y.`

Status: future work.

Meaning:

```text
Source artifact X imports symbol or module Y.
```

Example:

```text
Runtime imports ToolExecutor.
```

Likely evidence:

- module artifact for `Runtime`'s source path;
- import artifact for `ToolExecutor` from that same path.

### `X implements Y.`

Status: future work.

Meaning:

```text
Class X structurally implements or subclasses protocol/interface/base Y.
```

This is more complex and should probably not be the first implementation slice.

Potential evidence:

- class artifact `X`;
- base-class artifact or inheritance metadata for `Y`;
- optionally import evidence for `Y`.

Do not infer implementation from name similarity or existence alone.

## Required Repository Observation Upgrade

Current Repository Observation v0 emits these artifact kinds:

```text
module
class
function
import
```

That is enough for existence claims, but not enough for strong structure claims.

Structure reconciliation likely needs additional artifact metadata, such as:

```text
parent_symbol
scope
lineno
qualname
base_symbols
field_symbols
imported_from
```

Suggested future artifact examples:

```text
artifact_kind="method"
symbol="handle_user_message"
parent_symbol="Runtime"
path="seed_runtime/runtime.py"
```

```text
artifact_kind="field"
symbol="current_input"
parent_symbol="ContextPacket"
```

```text
artifact_kind="import"
symbol="ToolExecutor"
imported_from="seed_runtime.execution"
path="seed_runtime/runtime.py"
```

This implies the next implementation may need to extend repository observation before structure reconciliation can be meaningful.

## Same-Path vs Containment

Same-path evidence is useful but limited.

Same path can support:

```text
X defines Y.
```

as an existence-level claim under the current rules.

Same path should not support:

```text
X defines method Y.
X has field Y.
Y belongs to X.
X implements Y.
```

Those need containment or structural metadata.

Example:

```python
class Runtime:
    pass

def handle_user_message():
    pass
```

This supports the existence-level statement:

```text
Runtime defines handle_user_message.
```

under the current same-path rule.

It does not support the structure claim:

```text
Runtime defines method handle_user_message.
```

because `handle_user_message` is top-level, not a method of `Runtime`.

## Outcome Semantics

Use the existing alignment outcomes:

```text
supported
missing_support
potential_conflict
not_evaluable
```

### `supported`

Use when:

```text
The structure claim pattern is recognized,
and supplied artifact facts contain the required structural relationship evidence.
```

### `missing_support`

Use when:

```text
The structure claim pattern is recognized,
but supplied artifact facts do not contain required structural relationship evidence.
```

This does not prove the structure is absent globally unless acquisition scope is explicit and sufficient.

### `not_evaluable`

Use when:

```text
The claim does not match a supported structure pattern,
or the artifact facts lack the metadata required to evaluate that structure type.
```

For early implementation, many plausible structure claims may be `not_evaluable` until repository observation emits richer metadata.

### `potential_conflict`

Use rarely for structure claims. It may become relevant when supplied artifact facts show a competing structure, such as a method under a different parent than claimed. That is future work.

## Structure vs Behavior

Structure claims do not prove behavior.

Example:

```text
Runtime defines method handle_user_message.
```

Even if supported, this does not prove:

```text
Runtime.handle_user_message appends input.user_message.
Runtime routes validated decisions.
Runtime owns user-message intake.
```

Those require behavioral or boundary evidence.

## Structure vs Ownership

Structure claims do not prove ownership.

Example:

```text
ToolExecutor defines method execute.
```

This can support a structural statement about `ToolExecutor`.

It does not by itself prove:

```text
ToolExecutor owns registered-operation execution.
```

Ownership requires stronger evidence, likely including:

- structure;
- runtime call sites;
- invariant documentation;
- tests preserving the boundary;
- absence of competing owners under explicit acquisition scope.

## Recommended First Implementation Slice

Do not implement broad structure reconciliation first.

Recommended first slice:

```text
Repository Observation emits method containment facts.
```

For caller-provided Python source text, extend repository observation to distinguish:

```text
function: top-level def
method: def nested directly inside class
class: class definition
```

Then add a single structure claim rule:

```text
X defines method Y.
```

Supported when supplied artifact facts contain:

```text
artifact_kind="class", symbol=X
artifact_kind="method", symbol=Y, parent_symbol=X
```

If the current `RepositoryArtifactFact` model cannot represent `parent_symbol`, do not overload `fact` text or `path`. Either defer implementation or introduce a carefully scoped structural artifact record after documentation review.

## Implementation Non-Goals

Structure reconciliation should not:

- read files;
- scan repositories;
- use LLMs;
- infer ownership;
- infer behavior;
- infer call graphs;
- treat same-path as method containment;
- parse documentation broadly;
- integrate with Runtime;
- integrate with ToolExecutor;
- integrate with EventLedger;
- integrate with ProjectionStore;
- add graph construction;
- add confidence scoring.

## Recommended Tests For Future Implementation

Fixture-only tests should cover:

1. `Runtime defines method handle_user_message.` with a real method inside class `Runtime` -> `supported`.
2. Same claim with `Runtime` class and top-level `handle_user_message` function -> `missing_support` or `not_evaluable`, depending on whether method facts exist.
3. `ToolExecutor defines method execute.` with method containment -> `supported`.
4. `Runtime defines handle_user_message.` continues to use existence semantics, not structure semantics.
5. Ownership claims remain ownership claims and are not supported merely by method structure.
6. No runtime/tool/event/projection loading.
7. No file reads, repository scanning, or LLM usage.

## Documentation-Only Status

This document defines the structure-claim evidence boundary only. It does not modify production code, tests, reconciliation behavior, acquisition behavior, runtime behavior, tool execution, event storage, projection behavior, package exports, or local CLI behavior.
