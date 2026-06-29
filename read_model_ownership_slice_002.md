# Read-Model Ownership Slice 002

## Selected architectural boundary

**Read-Model Construction Inputs != Read-Model Dependency Identity.**

This slice recovered an implementation-local `ReadModelDependencyIdentity` boundary. It owns only the existing dependency evidence that proves a dependent read model is valid for a projected State boundary:

- state projection version;
- State last event id.

It does not own cache invalidation, cache storage, cache lookup policy, read-model construction, projection publication, rendering, CLI, JSON, events, ledger replay, or compatibility behavior.

## Implementation evidence

- `ReadModelConstructionInputs` already made the visible projected `State` handoff into builders explicit.
- State summary cache lookup already used `STATE_PROJECTION_VERSION` plus the current ledger last event id before loading a `SummaryProjectionSnapshot`.
- State summary cache save already persisted `STATE_PROJECTION_VERSION` plus `state.last_event_id` into the snapshot dependency fields.
- Fact index cache lookup already used `STATE_PROJECTION_VERSION` plus `visible_state.last_event_id` before loading a `DerivedIndexSnapshot`.
- Fact index construction already copied the same dependency evidence into the returned `DerivedFactIndex`.
- Projection store implementations already enforce those identity values as exact-match cache validity checks.

## Before

Read-model construction inputs and dependency identity were adjacent but compressed:

```text
ReadModelConstructionInputs
    -> visible_state.last_event_id / STATE_PROJECTION_VERSION selected inline
    -> cache lookup or read-model build/save
```

The behavior was already correct, but the code paths that consumed projected State also directly selected the cache-validity identity values. This appeared in both dependent read-model families reviewed in this slice:

- state summary cache lookup/save in `projected_state_summary_from_args(...)` and `state_summary_cache_debug_from_args(...)`;
- fact index cache lookup/build in `load_or_build_fact_index(...)` and `build_fact_index(...)`.

## After

The implementation now recovers dependency identity before cache lookup or snapshot save:

```text
ReadModelConstructionInputs
    -> ReadModelDependencyIdentity
    -> cache lookup / build / save using the same values
```

For cache lookups that happen before a projected `State` object is rebuilt, the same owner can be recovered from the already-known projected State boundary evidence: current ledger last event id plus the State projection version. This preserves the existing exact-match identity semantics without pretending to implement partial refresh or new invalidation rules.

## Boundary made explicit

`ReadModelDependencyIdentity` is now the owner for the dependency identity already used by dependent read-model caches. It carries:

```text
state_projection_version
state_last_event_id
```

The recovered boundary is narrower than cache identity policy. It only names the evidence. The projection store still owns exact-match cache lookup behavior, and read-model builders still own construction.

## Compatibility preserved

No compatibility boundary changed.

The same values are passed to summary snapshot lookup/save, fact-index snapshot lookup/save, and derived fact-index construction. CLI behavior, JSON shape, event shape, ledger replay, projection behavior, summary contents, fact index contents, and cache hit/miss semantics remain unchanged.

## Files changed

- `seed_runtime/read_model_ownership.py` — added the implementation-local dependency identity boundary and helpers.
- `seed_runtime/fact_index.py` — fact index cache lookup/build now recovers dependency identity before passing the same values onward.
- `scripts/seed_local.py` — state summary cache lookup/save and cache-debug lookup/save now recover dependency identity before passing the same values onward.
- `tests/test_read_model_ownership.py` — added tests proving the dependency identity preserves the existing projection-version and last-event-id evidence.
- `read_model_ownership_slice_002.md` — this report.

## LOC changed

Implementation before this report/test accounting:

```text
scripts/seed_local.py                | 29 insertions, 8 deletions
seed_runtime/fact_index.py           | 15 insertions, 6 deletions
seed_runtime/read_model_ownership.py | 36 insertions, 0 deletions
```

Implementation subtotal: **80 insertions, 14 deletions**.

## Tests executed

```text
pytest -q tests/test_read_model_ownership.py tests/test_fact_index.py tests/test_state_views.py tests/test_projection_store.py
```

Result: **60 passed**.

## Questions answered from implementation evidence

### 1. Where were read-model construction inputs and dependency identity previously mixed?

They were mixed where read-model cache/build paths accepted construction inputs and then selected dependency identity values inline. The clearest recurring examples were fact index lookup/build and state summary cache lookup/save. In those paths, the code used `STATE_PROJECTION_VERSION` and `visible_state.last_event_id`, `state.last_event_id`, or current ledger last event id directly at the cache handoff.

### 2. Which recovered architectural boundary became more explicit?

`ReadModelDependencyIdentity` became explicit as the boundary between construction inputs and cache lookup/build/save handoffs.

### 3. How does the implementation now better reflect the recovered architecture?

Read-model paths now recover dependency identity as a distinct implementation-local object before passing the same identity evidence to cache lookup/save or derived read-model records. Construction still consumes projected State; cache lookup still applies the same exact-match rules; the dependency identity is no longer selected ad hoc inside those handoffs.

### 4. Did implementation evidence suggest a more precise responsibility name than "Read-Model Dependency Identity"?

Insufficient implementation evidence.

The implementation evidence supports dependency identity for dependent read models, but does not justify a narrower vocabulary such as cache identity, dependency key, or validity proof as the family name. The recovered owner is intentionally limited to the existing projection version plus last-event-id evidence.

### 5. Did any compatibility boundary change?

No.

## Remaining compressed read-model ownership responsibilities

The following responsibilities remain compressed and were intentionally not recovered in this slice:

- state summary cache/debug visibility versus summary read-model ownership;
- fact index cache storage versus derived index construction;
- operator state summary composition versus compact StateSummary construction;
- current-facts query/filter/render behavior versus fact-index construction;
- read-model payload serialization versus projection-store snapshot persistence;
- dependent read-model cache observability vocabulary across state-build and current-facts surfaces.

## Observations about the emerging family vocabulary

The family vocabulary is becoming layered rather than monolithic:

```text
Projection Publication
    -> Read-Model Construction Inputs
    -> Read-Model Dependency Identity
    -> Cache lookup / build / save
```

This slice did not promote presentation terms into repository knowledge and did not add a runtime surface. The emerging vocabulary remains implementation-local and evidence-backed by existing cache dependency fields and exact-match store checks.
