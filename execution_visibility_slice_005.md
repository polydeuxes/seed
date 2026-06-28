# Execution Visibility Slice 005

## selected architectural boundary

```text
State Build Visibility
    !=
Projection Cache Diagnostics
```

This slice selected the `--state-build-cache-debug` implementation because the state-build cache debug report already carried both state-build-facing visibility fields and projection-cache diagnostic evidence in one return shape.

## implementation evidence

Implementation review found the transition from state-build visibility to projection cache diagnostics inside `state_summary_cache_debug_from_args(...)` in `scripts/seed_local.py`.

Evidence:

- state-build visibility fields were calculated and returned from the same report as projection-cache fields:
  - `cache_eligible`
  - `cache_ineligible_reason`
  - `summary_cache_status`
  - `current_last_event_id`
  - `cached_summary_last_event_id`
  - `notes`
- projection-cache diagnostic fields were also returned by that same report:
  - `state_cache_status`
  - `cached_state_last_event_id`
  - `projection_timings`
  - `projection_counters`
- `format_state_summary_cache_debug_report(...)` consumed the report through the same existing public property names, so the compatibility boundary could remain unchanged.

## before

Before this slice, `StateSummaryCacheDebugReport` directly owned both state-build visibility and projection-cache diagnostic evidence:

```text
StateSummaryCacheDebugReport
    cache_eligible
    cache_ineligible_reason
    summary_cache_status
    state_cache_status
    current_last_event_id
    cached_summary_last_event_id
    cached_state_last_event_id
    timings
    projection_timings
    projection_counters
    notes
```

That made one implementation concept carry both:

```text
rendered state-build/cache-debug visibility
projection cache diagnostics and replay/build evidence
```

## after

`StateSummaryCacheDebugReport` now separates implementation-local ownership into two private payloads while preserving legacy accessors:

```text
StateSummaryCacheDebugReport
    visibility: _StateBuildVisibilityPayload
    projection_diagnostics: _ProjectionCacheDiagnosticPayload
    timings
```

The state-build visibility payload owns:

```text
cache_eligible
cache_ineligible_reason
summary_cache_status
current_last_event_id
cached_summary_last_event_id
notes
```

The projection-cache diagnostic payload owns:

```text
state_cache_status
cached_state_last_event_id
projection_timings
projection_counters
```

The report keeps compatibility properties for all previous field names, so formatter and caller behavior remain unchanged.

## boundary made explicit

The recovered boundary made explicit is:

```text
State Build Visibility
    !=
Projection Cache Diagnostics
```

The implementation now shows that state-build visibility owns summary/cache-debug presentation evidence, while projection cache diagnostics own projection cache status, cached projection identity, projection replay/build subphase timings, and projection/build counters.

## compatibility preserved

No compatibility boundary changed.

This slice did not perform public renames, schema changes, event changes, CLI changes, JSON changes, ledger changes, cache behavior changes, projection behavior changes, timing behavior changes, counter behavior changes, or vocabulary migration.

Rendered `--state-build-cache-debug` output remains unchanged because `format_state_summary_cache_debug_report(...)` still reads the same report property names.

## files changed

- `scripts/seed_local.py`
- `tests/test_seed_local_script.py`
- `execution_visibility_slice_005.md`

## LOC changed

From `git diff --numstat` before adding this report:

```text
85 insertions, 26 deletions: scripts/seed_local.py
38 insertions, 0 deletions: tests/test_seed_local_script.py
```

Report LOC is documentation-only for this slice.

## tests executed

```text
pytest -q tests/test_seed_local_script.py::test_state_summary_cache_debug_separates_visibility_from_projection_diagnostics tests/test_seed_local_script.py::test_cli_state_summary_cache_debug_without_db_reports_unavailable tests/test_seed_local_script.py::test_cli_state_summary_cache_debug_does_not_ingest_or_execute tests/test_seed_local_script.py::test_cli_state_summary_cache_debug_reports_warm_summary_hit tests/test_seed_local_script.py::test_cli_state_summary_cache_debug_does_not_change_normal_summary_output
```

Result:

```text
5 passed
```

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
44 passed
```

## remaining compressed execution visibility boundaries

Remaining boundaries should be recovered one slice at a time. Current candidates include:

- projection build diagnostics that still pass replay/build phase evidence through cache-building paths;
- cache-status emission and projection replay/build timing that still meet in some projection-cache call sites;
- fact-index cache lookup/load timing and cache-status reporting adjacency inside current-facts filtered query execution;
- knowledge-reachability metadata that still carries cache visibility and timing fields through one audit metadata structure;
- progress cadence timing that still mixes elapsed time with status-emission throttling.
