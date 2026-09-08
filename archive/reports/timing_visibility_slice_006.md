# Timing Visibility Slice 006

## Selected architectural boundary

Recovered exactly one implementation-local boundary in the current-facts cache-debug path:

```text
Timing Measurement != Current-Facts Timing Interpretation
```

The recovered owner is `_CurrentFactsTimingInterpretation`. It is current-facts-local and only interprets already-measured State-cache evidence for the current-facts diagnostic report.

## Implementation evidence

The implementation evidence is the current-facts cache-debug construction path around `_current_facts_timing_from_args(...)`.

Before this slice, the same function both measured the State-cache path and directly interpreted the resulting cache/projection evidence:

- `state_path_started = time.perf_counter()` measured elapsed State-cache work.
- `project_state_with_cache(...)` returned `StateCacheStatus` and filled `ProjectionBuildDiagnostics`.
- `_CurrentFactsCacheVisibility.from_state_cache_status(status)` interpreted cache hit/miss/incremental replay into operator-facing labels.
- `_current_facts_timing_from_args(...)` appended the interpreted State-path label with the measured elapsed value.
- `_current_facts_timing_from_args(...)` appended projection diagnostic timings into the same report timing list.
- `_current_facts_timing_from_args(...)` selected the report `cache_status` string.

After this slice:

- `_current_facts_timing_from_args(...)` still owns elapsed-time measurement.
- `_CurrentFactsTimingInterpretation.from_cache_evidence(...)` owns the interpretation boundary over `StateCacheStatus` and `ProjectionBuildDiagnostics`.
- `_CurrentFactsTimingInterpretation` exposes the interpreted cache visibility and projection timing evidence needed by the existing diagnostic payload construction.
- `_format_current_facts_timing_report(...)` remains unchanged and still owns presentation formatting.

## Before

The current-facts cache-debug implementation had this local compression:

```text
measure State-cache elapsed time
↓
interpret StateCacheStatus as cache visibility
↓
merge ProjectionBuildDiagnostics timings
↓
construct _CurrentFactsDiagnosticPayload
↓
format report
```

The cache visibility boundary already existed, but the broader timing interpretation step remained embedded inside `_current_facts_timing_from_args(...)` alongside measurement and diagnostic payload assembly.

## After

The path now reads as:

```text
_current_facts_timing_from_args
  owns elapsed-time measurement and report assembly

_CurrentFactsTimingInterpretation
  owns current-facts-local interpretation of measured cache/projection evidence

_CurrentFactsDiagnosticPayload
  carries the existing diagnostic payload shape

_format_current_facts_timing_report
  owns presentation
```

No generic timing family was introduced. The recovered owner is intentionally local to the current-facts cache-debug surface.

## Boundary made explicit

`_CurrentFactsTimingInterpretation` makes the transition from measured/cache evidence into interpreted current-facts diagnostic meaning directly observable.

It consumes only:

- `StateCacheStatus`;
- `ProjectionBuildDiagnostics`.

It does not own:

- elapsed-time measurement;
- report formatting;
- CLI routing;
- cache behavior;
- projection behavior;
- rendering;
- execution status.

## Compatibility preserved

No compatibility boundary changed.

Preserved unchanged:

- CLI output text;
- timing labels;
- elapsed timing measurement sites;
- diagnostic payload shape;
- JSON behavior;
- event behavior;
- ledger behavior;
- projection/cache behavior.

## Files changed

- `scripts/seed_local.py`
- `tests/test_seed_local_script.py`
- `timing_visibility_slice_006.md`

## LOC changed

Final changed-file summary:

```text
scripts/seed_local.py              | 31 ++++++++++++++++++++++++++-----
tests/test_seed_local_script.py    | 27 +++++++++++++++++++++++++++
timing_visibility_slice_006.md     | 175 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
3 files changed, 228 insertions(+), 5 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_seed_local_script.py -k "current_facts_cache_debug or current_facts_timing_interpretation"
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
7 passed, 152 deselected
44 passed
```

## Questions

### 1. Where were timing measurement and timing interpretation previously mixed?

They were mixed inside `_current_facts_timing_from_args(...)` after `project_state_with_cache(...)` returned. That block measured elapsed State-cache duration with `time.perf_counter()`, interpreted `StateCacheStatus` through `_CurrentFactsCacheVisibility.from_state_cache_status(...)`, appended the interpreted State-path timing label, merged `ProjectionBuildDiagnostics.timings`, and selected the diagnostic `cache_status`.

### 2. Which recovered architectural boundary became more explicit?

The current-facts-local boundary between timing measurement and timing interpretation became explicit:

```text
Timing Measurement != Current-Facts Timing Interpretation
```

### 3. How does the implementation now better reflect the recovered architecture?

The measurement owner still records elapsed time in `_current_facts_timing_from_args(...)`, while `_CurrentFactsTimingInterpretation.from_cache_evidence(...)` interprets cache/projection evidence into the existing current-facts diagnostic meaning. Report construction still uses the same `_CurrentFactsDiagnosticPayload`, and presentation remains in `_format_current_facts_timing_report(...)`.

### 4. Did implementation evidence suggest a more precise responsibility name than "Timing Interpretation"?

Yes. The implementation evidence supports the more precise local responsibility name `Current-Facts Timing Interpretation`, represented by `_CurrentFactsTimingInterpretation`, because the owner is scoped to the current-facts cache-debug path and consumes current-facts State-cache evidence rather than defining a generic timing concept.

### 5. Did any compatibility boundary change?

No.

## Remaining compressed timing responsibilities

This slice intentionally stops after one recovered boundary. Remaining compression includes:

- `_current_facts_timing_from_args(...)` still assembles the final `CurrentFactsTimingReport` while owning several local measurements.
- `_TimingProjectionStore` still times projection-store operations directly into the caller-owned timing list.
- `ProjectionBuildDiagnostics` timings are still merged into caller-specific timing reports.
- Current-facts timing remains independent from other execution visibility timing surfaces.

These are not addressed in this slice.

## Observations about the emerging self-observation vocabulary

The repository continues to show a recurring grammar of measurement, interpretation, payload construction, and presentation. This slice does not promote that grammar into a shared framework. The implementation evidence supports only a current-facts-local owner, not a generic Timing family. The self-observation vocabulary is useful as a reading aid, but repository authority remains with implementation-local boundaries and compatibility-preserving tests.
