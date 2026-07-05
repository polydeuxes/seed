# Recognition Pressure Slice 001

## Selected boundary

```text
Projected State Boundary Dependency Identity

↓

read_model_dependency_identity_for_state_boundary(...)

↓

ReadModelDependencyIdentity

↓

read_model_cache_lookup_request(...)
```

This slice recovers exactly one implementation-local ownership boundary at the history / event-boundary / affected-state projection seam: the conversion of already-known projected State boundary evidence into the dependency identity used by dependent read-model cache lookup.

The selected boundary is not Recognition. It does not introduce a Recognition framework, engine, owner, registry, scheduler, lifecycle, topology, Town Clock, Begin function, Projection Engine, Cache Framework, or Dependency Framework.

## Implementation evidence

Implementation evidence selected this boundary because the state-build cache/debug path and the production projected-state summary path both perform the same local handoff:

1. The event ledger is queried for the current workspace events.
2. The current last event id is derived from the final event, or `None` for an empty ledger.
3. `read_model_dependency_identity_for_state_boundary(...)` converts that already-known state boundary into `ReadModelDependencyIdentity`.
4. `read_model_cache_lookup_request(...)` uses that identity before resolving the state-summary read-model cache lookup.

The boundary is implementation-local and already adjacent to cache/debug, event-boundary identity, cache eligibility, affected read-model lookup, and projection-facing evidence assembly.

The helper's module-level authority states that read models consume already-published projected `State` and that the module preserves the local construction input boundary without publishing projections, replaying events, invalidating caches, rendering output, persisting snapshots, or changing semantics.

The `ReadModelDependencyIdentity` artifact carries only:

- `state_projection_version`;
- `state_last_event_id`.

The helper `read_model_dependency_identity_for_state_boundary(...)` is the implementation-local producer for the selected pressure area because it accepts an already-known projected State boundary rather than read-model construction inputs. That directly matches the recovered seam:

```text
preserved event history / current last-event evidence

↓

projected State boundary identity

↓

dependent read-model cache lookup input
```

## Before

```text
ledger.list_events(...)

↓

current_last_event_id = latest_events[-1].id if latest_events else None

↓

state-build cache/debug or projected-state summary code must know how to shape
that event-boundary evidence for dependent read-model cache lookup
```

The responsibility pressure was compressed into the local orchestration path: event-boundary evidence and read-model cache lookup identity were adjacent in the same functions, and the local cache/debug path had to remain aware that `current_last_event_id` is the read-model dependency identity input.

## After

```text
ledger.list_events(...)

↓

current_last_event_id = latest_events[-1].id if latest_events else None

↓

read_model_dependency_identity_for_state_boundary(...)

↓

ReadModelDependencyIdentity

↓

read_model_cache_lookup_request(...)
```

The recovered boundary is the existing implementation-local helper/artifact pair that owns only the conversion from already-known projected State boundary evidence into dependent read-model cache lookup identity.

No runtime behavior changes were made for this slice; the deliverable records the implementation-selected ownership boundary.

## Recovered producer

`read_model_dependency_identity_for_state_boundary(...)` is the recovered producer.

It owns only the already-known projected State boundary identity conversion:

- consume `state_projection_version`;
- consume `state_last_event_id` derived from the event boundary;
- produce `ReadModelDependencyIdentity`.

It does not list events, choose the current event, project state, check cache eligibility, load snapshots, construct read models, publish snapshots, mutate the event ledger, render output, or alter JSON/CLI behavior.

## Recovered artifact/helper

The recovered helper is `read_model_dependency_identity_for_state_boundary(...)`.

The recovered artifact is `ReadModelDependencyIdentity`.

Together they carry the recovered boundary without changing public compatibility or introducing a new owner framework.

## Recovered consumer

The immediate consumer is `read_model_cache_lookup_request(...)`.

Observed downstream consumers in the pressure area are:

- `projected_state_summary_from_args(...)`, which resolves the dependent state-summary read-model cache before projection/rebuild work;
- `_state_build_cache_debug_evidence_from_args(...)`, which records state-build cache/debug evidence around the same lookup boundary.

## Compatibility preserved

No compatibility boundary changed.

The slice changes no runtime behavior, CLI behavior, JSON output, diagnostics, schema, event ledger behavior, cache behavior, projection behavior, or read-model behavior.

Expected answer: `No.`

## Required questions

### 1. What responsibilities were previously compressed?

Event-boundary evidence selection and dependent read-model cache identity shaping were compressed in the local orchestration paths. The same functions that list events and derive `current_last_event_id` also immediately prepare the identity used to look up affected state-summary read-model cache entries.

### 2. Which implementation-local ownership boundary became directly observable?

The directly observable boundary is **Projected State Boundary Dependency Identity**: converting already-known projected State boundary evidence into `ReadModelDependencyIdentity` for dependent read-model cache lookup.

### 3. What producer now owns the recovered responsibility?

`read_model_dependency_identity_for_state_boundary(...)` owns the recovered responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`ReadModelDependencyIdentity` carries the artifact boundary, and `read_model_dependency_identity_for_state_boundary(...)` carries the helper boundary.

### 5. Who consumes it?

`read_model_cache_lookup_request(...)` consumes the identity immediately. The state-build cache/debug evidence path and projected-state summary path then use the resulting lookup request through `resolve_read_model_cache_lookup(...)`.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `recognition_pressure_slice_001.md`

## LOC changed

```text
recognition_pressure_slice_001.md | 194 +++++++++++++++++++++++++++++++++++++++++++++++++
```

## Tests executed

```text
python -m py_compile scripts/seed_local.py seed_runtime/read_model_ownership.py
pytest -q tests/test_seed_local_script.py -k 'state_summary_cache_debug or projected_state_summary'
```

## Remaining compressed responsibilities

This slice intentionally stops at one local ownership boundary. Remaining compressed responsibilities include:

- current-event selection from event listing;
- cache eligibility policy;
- summary snapshot lookup policy;
- state/projection cache lookup behavior;
- projection replay/build dispatch;
- read-model construction;
- summary snapshot publication;
- cache-debug evidence assembly;
- presentation/report formatting.

Those responsibilities remain unchanged and should not be promoted from orientation language without separate implementation evidence.
