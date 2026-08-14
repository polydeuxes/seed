# Read-Model Ownership Slice 003

## Selected architectural boundary

This slice recovered the implementation-local boundary:

```text
Read-Model Dependency Identity
    !=
Read-Model Cache Lookup
```

The recovered owner is `ReadModelCacheLookupRequest` / `ReadModelCacheLookupResult`, resolved by `resolve_read_model_cache_lookup(...)`.

This owner consumes an already-derived `ReadModelDependencyIdentity` and preserves only the existing cache lookup decision: whether the storage lookup returned a matching dependent read-model snapshot. It does not own dependency identity derivation, cache storage, cache invalidation, read-model construction, projection publication, rendering, CLI, scheduling, JSON, events, or ledger replay.

## Implementation evidence

The implementation already had multiple dependent read-model cache lookups that used the same pattern:

1. Derive or recover a `ReadModelDependencyIdentity`.
2. Pass that identity's `state_projection_version` and `state_last_event_id` directly to a projection-store load method.
3. Interpret `snapshot is not None` as a cache hit and `None` as a miss.
4. Continue into the unchanged read-model construction path on miss.

Concrete evidence:

- Fact index cache lookup used `ReadModelDependencyIdentity` and immediately called `store.load_derived_index_snapshot(...)` with the identity fields.
- State summary cache lookup used `read_model_dependency_identity_for_state_boundary(...)` and immediately called `store.load_summary_snapshot(...)` with the identity fields.
- State summary cache debug used the same identity-to-store-lookup-to-hit/miss pattern for its measured summary snapshot lookup.
- Projection-store methods still own persistence mechanics and exact matching by state projection version and last event id.

## Before

The code had an explicit dependency identity owner, but lookup was still compressed into individual read-model paths:

```text
ReadModelDependencyIdentity
    -> direct store.load_*_snapshot(...identity fields...)
    -> snapshot is not None hit/miss branch
    -> cached snapshot reuse or read-model construction
```

That mixed two responsibilities at the handoff:

- naming the dependency identity that must be satisfied; and
- deciding whether an existing cached read model satisfies it.

## After

The cache lookup question is now a separate implementation-local boundary:

```text
ReadModelDependencyIdentity
    -> ReadModelCacheLookupRequest
    -> resolve_read_model_cache_lookup(...existing storage lookup...)
    -> ReadModelCacheLookupResult.cache_hit / snapshot
    -> cached snapshot reuse or unchanged read-model construction
```

The storage call remains the same call, with the same identity values, against the same projection store. The result only names the already-existing decision boundary around `None` versus snapshot.

## Boundary made explicit

`ReadModelCacheLookupRequest` makes the lookup request observable as a separate handoff from dependency identity.

`ReadModelCacheLookupResult` makes the existing hit/miss decision observable without changing its semantics. The `cache_hit` property is still exactly `snapshot is not None`.

`resolve_read_model_cache_lookup(...)` keeps cache storage external by accepting the existing storage operation as a callable. This keeps the owner narrow: it resolves the cache lookup decision, but it does not own storage, keys, invalidation, cache population, read-model construction, or projection behavior.

## Compatibility preserved

No compatibility boundary changed.

Preserved behavior:

- cache keys are unchanged;
- cache hit/miss rules are unchanged;
- state summary contents are unchanged;
- fact index contents are unchanged;
- projection behavior is unchanged;
- read-model construction is unchanged;
- CLI and JSON surfaces are unchanged;
- events and ledger replay are unchanged.

## Files changed

- `seed_runtime/read_model_ownership.py` — added the implementation-local read-model cache lookup request/result and resolver.
- `seed_runtime/fact_index.py` — routed fact-index cache lookup through the explicit lookup boundary while preserving the same storage call and hit/miss behavior.
- `scripts/seed_local.py` — routed state-summary cache lookup and state-summary cache-debug lookup through the explicit lookup boundary while preserving the same storage calls and timing labels.
- `tests/test_read_model_ownership.py` — added tests proving the lookup boundary preserves the existing hit and miss decisions.
- `read_model_ownership_slice_003.md` — recorded this slice.

## LOC changed

Final staged changes are:

```text
5 files changed, 333 insertions(+), 23 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_read_model_ownership.py tests/test_fact_index.py
```

Result:

```text
14 passed
```

```text
pytest -q tests/test_read_model_ownership.py tests/test_fact_index.py tests/test_state_summary_cache.py
```

Result:

```text
ERROR: file or directory not found: tests/test_state_summary_cache.py
```

```text
pytest -q tests/test_read_model_ownership.py tests/test_fact_index.py tests/test_state_summary_views.py tests/test_projected_state_consumers.py
```

Result:

```text
47 passed
```

## Questions

### 1. Where were read-model dependency identity and cache lookup previously mixed?

They were mixed at the cache handoff in the dependent read-model paths. `ReadModelDependencyIdentity` was recovered, but the fact-index and state-summary paths still immediately unpacked its fields into `store.load_derived_index_snapshot(...)` or `store.load_summary_snapshot(...)` and then interpreted `snapshot is not None` inline.

The clearest recurring locations were:

- fact-index lookup in `load_or_build_fact_index(...)`;
- state-summary cache lookup in `projected_state_summary_from_args(...)`;
- state-summary cache-debug lookup in `state_summary_cache_debug_from_args(...)`.

### 2. Which recovered architectural boundary became more explicit?

`Read-Model Dependency Identity != Read-Model Cache Lookup` became explicit.

Dependency identity now answers:

```text
What identity must be satisfied?
```

Cache lookup now answers:

```text
Does an existing read model already satisfy that identity?
```

### 3. How does the implementation now better reflect the recovered architecture?

The implementation now passes an already-derived `ReadModelDependencyIdentity` into a `ReadModelCacheLookupRequest`, resolves that request through the existing storage lookup, and receives a `ReadModelCacheLookupResult` whose `cache_hit` preserves the previous `snapshot is not None` decision.

This makes the lookup responsibility observable before read-model construction begins, without moving identity derivation, storage ownership, invalidation, or construction into the lookup owner.

### 4. Did implementation evidence suggest a more precise responsibility name than "Read-Model Cache Lookup"?

Insufficient implementation evidence.

The repeated implementation pattern supports a cache lookup boundary, but the repository does not yet provide stronger evidence for a more precise recurring name such as resolution, reuse, or cache satisfaction.

### 5. Did any compatibility boundary change?

No.

## Remaining compressed read-model ownership responsibilities

- cache storage versus cache lookup remains intentionally separate but still adjacent at projection-store calls;
- cache save/population versus read-model construction remains adjacent after misses;
- state summary cache/debug visibility versus summary read-model ownership remains adjacent;
- fact index cache storage versus derived index construction remains adjacent;
- read-model reuse reporting versus operational timing remains adjacent in debug surfaces.

These are candidates for future slices only if implementation evidence supports exactly one narrow ownership recovery at a time.

## Observations about the emerging family vocabulary

The Read-Model Ownership family now has an implementation-backed sequence:

```text
Projection Publication
    !=
Read-Model Construction Inputs
    !=
Read-Model Dependency Identity
    !=
Read-Model Cache Lookup
    !=
Read-Model Construction
```

The vocabulary remains narrow and implementation-local. This slice did not promote presentation terms into repository knowledge, did not add runtime surfaces, and did not change diagnostic, CLI, event, JSON, or ledger behavior.
