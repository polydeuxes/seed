# Read-Model Ownership Slice 005

## Selected architectural boundary

```text
Read-Model Construction
    !=
Read-Model Cache Publication
```

The recovered owner is implementation-local read-model cache publication. It covers only the post-construction handoff from a completed read model into the existing dependent cache snapshot save path.

## Implementation evidence

Construction was already explicit through `ReadModelConstructionRequest`, `ReadModelConstructionResult`, and `construct_read_model(...)` in `seed_runtime/read_model_ownership.py`.

The compressed responsibility appeared immediately after construction in two recurring dependent read-model cache paths:

1. State summary construction returned `(StateSummary, operator_summary)`, and the caller immediately assembled and saved a `SummaryProjectionSnapshot`.
2. Fact index construction returned a `DerivedFactIndex`, and the caller immediately assembled and saved a `DerivedIndexSnapshot`.

Both paths were not constructing the read model anymore at that point. They were publishing the completed read model into the existing reusable cache snapshot store.

## Before

```text
ReadModelConstructionResult
    -> caller manually creates cache snapshot
    -> caller directly invokes save_summary_snapshot / save_derived_index_snapshot
```

The same caller scope therefore held both:

- the completed read-model construction result; and
- the cache publication handoff into the existing store save method.

## After

```text
ReadModelConstructionResult
    -> ReadModelCachePublicationRequest
    -> publish_read_model_cache(...)
    -> existing store save method
```

The implementation now introduces:

- `ReadModelCachePublicationRequest`
- `ReadModelCachePublicationResult`
- `read_model_cache_publication_request(...)`
- `publish_read_model_cache(...)`

The publication function accepts the existing construction result, the existing snapshot creation logic, and the existing cache save operation. It does not alter save semantics, cache keys, payload contents, lookup decisions, or compatibility behavior.

## Boundary made explicit

The explicit boundary is:

```text
Constructed read model
    -> cache publication request
    -> existing cache snapshot persistence
```

The owner is intentionally narrow. It does not own:

- read-model construction;
- cache lookup;
- cache invalidation;
- dependency identity;
- projection publication;
- rendering;
- CLI;
- scheduling.

## Answers to required questions

### 1. Where were read-model construction and cache publication previously mixed?

They were mixed in the callers that handled a cache miss: after constructing the read model, the same flow directly created and saved dependent cache snapshots. The state summary path directly called `store.save_summary_snapshot(...)` after `summary_construction`; the fact index path directly called `store.save_derived_index_snapshot(...)` after `construction`.

### 2. Which recovered architectural boundary became more explicit?

```text
Read-Model Construction
    !=
Read-Model Cache Publication
```

### 3. How does the implementation now better reflect the recovered architecture?

A completed `ReadModelConstructionResult` is now consumed by a `ReadModelCachePublicationRequest`, then published through `publish_read_model_cache(...)`. Snapshot shape creation remains supplied by the existing caller, and persistence remains the existing store save call, but the ownership handoff is now directly observable.

### 4. Did implementation evidence suggest a more precise responsibility name than "Read-Model Cache Publication"?

Insufficient implementation evidence.

The implementation evidence supports dependent read-model cache publication for summary and fact-index snapshots, but it does not require a narrower family name without risking vocabulary migration.

### 5. Did any compatibility boundary change?

No.

## Compatibility preserved

No public CLI, JSON, event, ledger replay, cache key, cache hit/miss, cache invalidation, summary payload, fact-index payload, or projection behavior was intentionally changed.

The new owner delegates to the same store save operations:

- `save_summary_snapshot(...)`
- `save_derived_index_snapshot(...)`

## Files changed

- `seed_runtime/read_model_ownership.py`
- `seed_runtime/fact_index.py`
- `scripts/seed_local.py`
- `tests/test_read_model_ownership.py`
- `read_model_ownership_slice_005.md`

## LOC changed

Pre-report implementation/test diff before adding this report:

```text
scripts/seed_local.py                | 31 insertions, 11 deletions
seed_runtime/fact_index.py           | 15 insertions, 9 deletions
seed_runtime/read_model_ownership.py | 46 insertions, 0 deletions
tests/test_read_model_ownership.py   | 37 insertions, 0 deletions
Total                                | 129 insertions, 20 deletions
```

## Tests executed

```text
black seed_runtime/read_model_ownership.py seed_runtime/fact_index.py scripts/seed_local.py tests/test_read_model_ownership.py
pytest -q tests/test_read_model_ownership.py tests/test_fact_index.py tests/test_projection_store.py
```

Result:

```text
45 passed
```

## Remaining compressed read-model ownership responsibilities

Potential remaining compression should be investigated separately and one boundary at a time. Current likely areas are:

- state-summary debug timing path, where separate summary derivations and snapshot save remain adjacent for measurement purposes;
- exact responsibility separation between cache snapshot shape creation and cache store persistence;
- dependent read-model cache publication versus lower-level projection-store snapshot storage;
- cache publication completion/status visibility versus runtime diagnostic surfaces.

No additional owner was recovered in this slice.

## Observations about the emerging family vocabulary

The family vocabulary is becoming more implementation-backed as a sequence of narrow boundaries:

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
    !=
Read-Model Cache Publication
    !=
Future Cache Lookup
```

This slice reinforces that "publication" in this family means an implementation-local handoff into reuse, not a new runtime surface or conceptual migration. The completed read model remains the construction result; publication is only the act of converting that result into the existing cached snapshot and saving it through the existing cache store interface.
