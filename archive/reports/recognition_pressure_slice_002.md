# Recognition Pressure Slice 002

## Selected boundary

```text
Dependency Identity Cache Lookup Question

↓

read_model_cache_lookup_request(...)

↓

ReadModelCacheLookupRequest

↓

resolve_read_model_cache_lookup(...)
```

This slice recovers exactly one implementation-local ownership boundary immediately adjacent to Slice 001: after the projected State boundary has already been converted into `ReadModelDependencyIdentity`, the next directly observable implementation-local responsibility is shaping that dependency identity into the cache lookup question consumed by the existing cache resolver.

The selected boundary is not Recognition. It does not introduce a Recognition framework, engine, owner, registry, scheduler, lifecycle, topology, Town Clock, Begin function, Projection Engine, Cache Framework, or Dependency Framework.

## Implementation evidence

Implementation evidence selected this boundary because the read-model ownership module already separates three adjacent handoffs:

1. `ReadModelDependencyIdentity` preserves only the existing projected State dependency evidence: `state_projection_version` and `state_last_event_id`.
2. `read_model_cache_lookup_request(...)` accepts an already-derived dependency identity and returns `ReadModelCacheLookupRequest`.
3. `ReadModelCacheLookupRequest` owns only the lookup question: whether a dependent read-model cache has an entry satisfying that already-derived identity.
4. `resolve_read_model_cache_lookup(...)` consumes the lookup request and invokes the existing storage lookup with `request.dependency_identity`.

The adjacent production paths preserve the same handoff. The projected-state summary path derives `current_last_event_id`, produces `ReadModelDependencyIdentity` through `read_model_dependency_identity_for_state_boundary(...)`, wraps that identity through `read_model_cache_lookup_request(...)`, and passes the request to `resolve_read_model_cache_lookup(...)` before loading the existing summary snapshot. The state-build cache/debug path performs the same identity-to-request handoff before timing the summary snapshot lookup.

This boundary is implementation-local and already bounded by the module's negative ownership statements: it does not derive dependency identity, own cache storage, invalidate caches, construct read models, publish projections, render output, or change lookup semantics.

## Before

```text
ReadModelDependencyIdentity

↓

local orchestration path still has to know that the next handoff is a
cache lookup question over that identity

↓

resolve existing storage lookup
```

The responsibility pressure was compressed at the immediate handoff after Slice 001. The dependency identity was explicit, but the adjacent orchestration still had to pass it into the cache lookup surface at the moment the storage lookup was resolved.

## After

```text
ReadModelDependencyIdentity

↓

read_model_cache_lookup_request(...)

↓

ReadModelCacheLookupRequest

↓

resolve_read_model_cache_lookup(...)
```

The recovered boundary is the existing implementation-local helper/artifact pair that owns only the conversion from an already-derived dependency identity into the read-model cache lookup question.

No runtime behavior changes were made for this slice; the deliverable records the implementation-selected ownership boundary.

## Recovered producer

`read_model_cache_lookup_request(...)` is the recovered producer.

It owns only the already-derived identity-to-lookup-question handoff:

- consume `ReadModelDependencyIdentity`;
- produce `ReadModelCacheLookupRequest`;
- preserve the identity unchanged for the resolver.

It does not derive dependency identity, list events, choose the current event, check cache eligibility, load snapshots, construct read models, publish snapshots, mutate the event ledger, render output, or alter JSON/CLI behavior.

## Recovered artifact/helper

The recovered helper is `read_model_cache_lookup_request(...)`.

The recovered artifact is `ReadModelCacheLookupRequest`.

Together they carry the recovered boundary without changing public compatibility or introducing a new owner framework.

## Recovered consumer

The immediate consumer is `resolve_read_model_cache_lookup(...)`.

Observed downstream consumers in the pressure area are:

- `projected_state_summary_from_args(...)`, which resolves the dependent state-summary read-model cache before projection/rebuild work;
- `_state_build_cache_debug_evidence_from_args(...)`, which times and records evidence around the same summary snapshot lookup boundary.

## Compatibility preserved

No compatibility boundary changed.

The slice changes no runtime behavior, CLI behavior, JSON output, diagnostics, schema, event ledger behavior, cache behavior, projection behavior, or read-model behavior.

Expected answer: `No.`

## Required questions

### 1. What responsibilities were previously compressed?

After the dependency identity boundary recovered by Slice 001, dependency identity handoff and cache lookup question construction remained adjacent in the local orchestration. The code already had a dependency identity, and the next compressed responsibility was preserving that identity as the exact cache lookup question before resolving storage.

### 2. Which implementation-local ownership boundary became directly observable?

The directly observable boundary is **Dependency Identity Cache Lookup Question**: converting an already-derived `ReadModelDependencyIdentity` into `ReadModelCacheLookupRequest` for the existing read-model cache resolver.

### 3. What producer now owns the recovered responsibility?

`read_model_cache_lookup_request(...)` owns the recovered responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`ReadModelCacheLookupRequest` carries the artifact boundary, and `read_model_cache_lookup_request(...)` carries the helper boundary.

### 5. Who consumes it?

`resolve_read_model_cache_lookup(...)` consumes the request immediately. The projected-state summary path and state-build cache/debug evidence path then use the resolved result without changing cache behavior.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `recognition_pressure_slice_002.md`

## LOC changed

```text
recognition_pressure_slice_002.md | 172 +++++++++++++++++++++++++++++++++++++++++++++++++
```

## Tests executed

```text
python -m py_compile scripts/seed_local.py seed_runtime/read_model_ownership.py
pytest -q tests/test_read_model_ownership.py
```

## Remaining compressed responsibilities

This slice intentionally stops at one local ownership boundary. Remaining compressed responsibilities include:

- current-event selection from event listing;
- cache eligibility policy;
- summary snapshot storage lookup policy;
- state/projection cache lookup behavior;
- cache hit/miss interpretation by callers;
- projection replay/build dispatch;
- read-model construction;
- summary snapshot publication;
- cache-debug evidence assembly;
- presentation/report formatting.

Those responsibilities remain unchanged and should not be promoted from orientation language without separate implementation evidence.
