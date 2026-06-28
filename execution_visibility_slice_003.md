# Execution Visibility Slice 003

## selected architectural boundary

Execution Timing != Cache Visibility.

This slice keeps execution measurement separate from the explanation of why the measured current-facts State path took the cache path it took.

## implementation evidence

The implementation evidence is in the current-facts cache-debug path in `scripts/seed_local.py`.

`_current_facts_timing_from_args(...)` measures elapsed work for the current-facts State path and renders those measurements through `CurrentFactsTimingReport`. The same path also receives `StateCacheStatus` from `project_state_with_cache(...)`, whose fields identify cache hit, cache miss, and incremental replay outcomes.

Before this slice, the transition from timing to cache visibility occurred immediately after `project_state_with_cache(...)` returned:

- `state_path_started = time.perf_counter()` began timing construction.
- `project_state_with_cache(...)` returned `StateCacheStatus`.
- inline `if status.cache_hit / elif status.incremental_replay / else` logic chose the human-visible cache path label.
- the selected cache path label was appended directly as a timing row.
- `cache_status` was derived inline from the same cache status object.

That made the timing builder also own cache explanation vocabulary for hit, miss, and incremental replay paths.

## before

`_current_facts_timing_from_args(...)` mixed responsibilities in one implementation body:

```text
measure State path elapsed time
    + inspect cache-hit / cache-miss status
    + choose cache explanation label
    + append measured timing row under that cache explanation
    + choose rendered cache status
```

The code still behaved correctly, but the architectural boundary between measurement and explanation was observable only as adjacent inline statements.

## after

The current-facts cache-debug path now uses the implementation-local `_CurrentFactsCacheVisibility` value object.

`_CurrentFactsCacheVisibility.from_state_cache_status(...)` owns cache explanation construction:

- `hit` versus `miss` rendered cache status;
- cache-hit path label;
- cache-miss incremental replay path label;
- cache-miss full rebuild path label.

`_current_facts_timing_from_args(...)` still owns timing construction:

- start timestamp capture;
- elapsed duration calculation;
- appending elapsed timing rows;
- extending projection diagnostic timings;
- total timing construction.

## boundary made explicit

The recovered boundary made explicit is:

```text
Execution Timing
    !=
Cache Visibility
```

Timing construction now measures and records elapsed time. Cache visibility construction now explains which cache path produced that elapsed time.

## compatibility preserved

Did any compatibility boundary change?

No.

No compatibility boundary changed. This slice does not rename public vocabulary, change CLI flags, schemas, JSON, event records, ledger behavior, cache behavior, hit/miss logic, cache reuse logic, emitted timing values, emitted cache diagnostics, or measurement clock source.

The existing rendered labels are preserved exactly:

- `state cache hit path (metadata validation + cached projection load)`
- `state cache miss path (incremental event replay)`
- `state cache miss path (full projection rebuild)`

## files changed

- `scripts/seed_local.py`
  - imported `StateCacheStatus` for the implementation-local cache visibility adapter.
  - added `_CurrentFactsCacheVisibility`.
  - replaced inline cache explanation branching inside `_current_facts_timing_from_args(...)` with `_CurrentFactsCacheVisibility.from_state_cache_status(...)`.

## LOC changed

`git diff --stat` reported:

```text
scripts/seed_local.py | 44 ++++++++++++++++++++++++++++++++++++--------
1 file changed, 36 insertions(+), 8 deletions(-)
```

## tests executed

```text
python -m py_compile scripts/seed_local.py
```

Result:

```text
passed
```

```text
pytest -q tests/test_seed_local_script.py::test_cli_current_facts_cache_debug_renders_timing_section tests/test_seed_local_script.py::test_cli_current_facts_cache_debug_warm_hit_labels_cached_projection_load
```

Result:

```text
2 passed in 2.54s
```

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
44 passed in 1.27s
```

## remaining compressed execution visibility boundaries

Implementation still contains other execution visibility seams that can be investigated in later slices without vocabulary migration:

- state-build cache-debug report construction still combines cache eligibility/status explanation with phase timing collection;
- projection cache status emission and projection replay/build timing still meet inside `project_state_with_cache(...)` and projector diagnostics;
- fact-index cache lookup/load timing and cache-status reporting are still adjacent inside current-facts filtered query execution;
- knowledge-reachability timing metadata still carries cache visibility and timing fields through one audit metadata structure;
- progress cadence timing still mixes elapsed time with status-emission throttling.
