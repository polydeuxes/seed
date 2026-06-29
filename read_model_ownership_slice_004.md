# Read-Model Ownership Slice 004

## Selected architectural boundary

This slice recovered the implementation-local boundary:

```text
Read-Model Cache Lookup
    !=
Read-Model Construction
```

The recovered owner is `ReadModelConstructionRequest` / `ReadModelConstructionResult`, executed by `construct_read_model(...)`.

This owner consumes already-published construction inputs, an already-derived dependency identity, and the already-resolved cache lookup result when one exists. It preserves only the existing construction handoff into read-model builders. It does not own cache lookup, cache storage, cache invalidation, cache save, projection publication, rendering, CLI, scheduling, JSON, events, or ledger replay.

## Implementation evidence

The implementation already had repeated cache-miss transitions that moved directly from cache lookup into construction:

1. Fact-index cache miss in `load_or_build_fact_index(...)` resolved `ReadModelCacheLookupResult`, emitted the miss status, and immediately invoked `build_fact_index(...)` before saving the derived-index snapshot.
2. State-summary cache miss in `projected_state_summary_from_args(...)` resolved summary cache lookup, rebuilt projected state if needed, derived read-model inputs and dependency identity, and immediately invoked `build_state_summary(state)` and `state_summary(state)` before saving a summary snapshot.
3. State-summary cache-debug miss in `state_summary_cache_debug_from_args(...)` followed the same lookup-to-rebuild-to-summary-construction path while preserving existing timing labels.

The recurring implementation pressure was not cache identity or lookup anymore. Those were already explicit. The remaining compression was the handoff from "cache did not provide a reusable read model" to "invoke the existing read-model builder with the visible projected State."

## Before

The post-lookup miss paths still compressed cache lookup and construction at adjacent call sites:

```text
ReadModelCacheLookupResult.cache_hit == False
    -> emit cache miss status
    -> direct build_state_summary(state) / state_summary(state)
    -> direct build_fact_index(state, ...)
    -> cache save when configured
```

That made the miss path readable but left the construction boundary implicit. The code had to infer that construction began at each direct builder call after the lookup branch.

## After

The miss paths now create an explicit construction request before invoking the existing builders:

```text
ReadModelCacheLookupResult.cache_hit == False
    -> ReadModelConstructionRequest(inputs, dependency_identity, cache_lookup)
    -> construct_read_model(...existing builder...)
    -> ReadModelConstructionResult.read_model
    -> unchanged cache save when configured
```

The builders still receive the same visible projected State through `ReadModelConstructionInputs`. The constructed read-model objects are the same objects returned by the existing builders.

## Boundary made explicit

`ReadModelConstructionRequest` names the input handoff into construction after lookup. Its fields preserve the evidence already present at the handoff:

- `inputs` — the already-visible projected State boundary;
- `dependency_identity` — the identity the read model is built against;
- `cache_lookup` — the already-resolved lookup result when the path passed through cache lookup.

`construct_read_model(...)` invokes the supplied existing builder with `ReadModelConstructionInputs` and returns a `ReadModelConstructionResult`. The helper intentionally keeps storage, lookup, invalidation, save, rendering, CLI, events, and ledger behavior outside the construction owner.

## Compatibility preserved

No compatibility boundary changed.

Preserved behavior:

- cache hit/miss rules are unchanged;
- cache lookup behavior is unchanged;
- cache keys are unchanged;
- cache save behavior is unchanged;
- state summary contents are unchanged;
- fact-index contents are unchanged;
- projection behavior is unchanged;
- CLI and JSON surfaces are unchanged;
- events and ledger replay are unchanged.

## Files changed

- `seed_runtime/read_model_ownership.py` — added the implementation-local construction request/result and construction helper.
- `seed_runtime/fact_index.py` — routed the existing fact-index cache-miss builder call through the explicit construction boundary.
- `scripts/seed_local.py` — routed existing state-summary miss/debug builder calls through the explicit construction boundary while preserving cache lookup, timings, and save behavior.
- `tests/test_read_model_ownership.py` — added a test proving the construction boundary passes the same inputs to the existing builder and returns the same read model.
- `read_model_ownership_slice_004.md` — recorded this slice.

## LOC changed

Final staged changes are:

```text
5 files changed, 336 insertions(+), 18 deletions(-)
```

## Tests executed

```text
python -m black seed_runtime/read_model_ownership.py seed_runtime/fact_index.py scripts/seed_local.py tests/test_read_model_ownership.py && pytest -q tests/test_read_model_ownership.py tests/test_fact_index.py tests/test_state_views.py
```

Result:

```text
34 passed
```

```text
pytest -q tests/test_read_model_ownership.py tests/test_fact_index.py tests/test_state_views.py tests/test_projection_store.py tests/test_seed_local_script.py
```

Result:

```text
221 passed
```

## Questions

### 1. Where were read-model cache lookup and read-model construction previously mixed?

They were mixed at the cache-miss handoff in dependent read-model paths. The fact-index path resolved cache lookup and then directly called `build_fact_index(...)`. The state-summary path resolved summary cache lookup and then directly called `build_state_summary(state)` and `state_summary(state)`. The state-summary cache-debug path did the same construction directly inside timing wrappers.

### 2. Which recovered architectural boundary became more explicit?

`Read-Model Cache Lookup != Read-Model Construction` became explicit.

Cache lookup answers:

```text
Can an existing read model be reused?
```

Construction now answers:

```text
Build the read model from the visible projected State using the existing builder.
```

### 3. How does the implementation now better reflect the recovered architecture?

The implementation now carries the miss-path handoff through `ReadModelConstructionRequest` and `construct_read_model(...)` before receiving `ReadModelConstructionResult.read_model`. This makes the transition from lookup result to construction directly observable without moving cache lookup, cache storage, cache save, projection, rendering, CLI, JSON, events, or ledger behavior into the construction owner.

### 4. Did implementation evidence suggest a more precise responsibility name than "Read-Model Construction"?

Insufficient implementation evidence.

The repeated implementation pattern supports a construction boundary after cache lookup, but the repository does not yet provide stronger evidence for a more precise recurring name such as construction request, construction execution, read-model build, or materialization.

### 5. Did any compatibility boundary change?

No.

## Remaining compressed read-model ownership responsibilities

- cache save/population remains adjacent to construction in miss paths;
- state-summary compact construction and operator-summary construction are still adjacent in the same miss path;
- state-summary cache-debug timing and construction ownership remain adjacent;
- fact-index construction and derived-index snapshot payload conversion remain adjacent;
- cache storage mechanics remain close to read-model callers through projection-store save/load calls.

These are future candidates only if implementation evidence supports exactly one narrow ownership recovery at a time.

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
    !=
Cache Save
```

The vocabulary remains implementation-local and evidence-backed. This slice did not add a runtime surface, did not promote presentation vocabulary into preserved knowledge, and did not alter diagnostic, CLI, JSON, event, ledger, or compatibility behavior.
