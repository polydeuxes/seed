# Timing Visibility Slice 007

## Selected architectural boundary

`Timing Interpretation != Diagnostic Payload`

The recovered implementation-local owner is `_CurrentFactsTimingDiagnosticPayload`. It preserves the existing current-facts timing diagnostic payload material from already-interpreted timing evidence and a measured State-path elapsed value.

## Implementation evidence

The implementation pressure was in the cached current-facts timing branch of `_current_facts_timing_from_args(...)`.

Before this slice, `_CurrentFactsTimingInterpretation.from_cache_evidence(...)` already interpreted cache evidence into:

- `_CurrentFactsCacheVisibility.cache_status`;
- `_CurrentFactsCacheVisibility.state_path_label`;
- projection diagnostic timings copied from `ProjectionBuildDiagnostics.timings`.

However, `_current_facts_timing_from_args(...)` still assembled the diagnostic payload by:

- appending the interpreted State-path label with the measured State-path elapsed value;
- extending the report timings with interpreted projection timings;
- selecting the report `cache_status` from cache visibility;
- passing the resulting `cache_status` and `timings` into `_CurrentFactsDiagnosticPayload`.

That mixed the interpretation result with the payload-preservation step.

## Before

The cached current-facts timing path flowed as:

```text
measure State-cache elapsed time

↓

_CurrentFactsTimingInterpretation.from_cache_evidence(...)

↓

_current_facts_timing_from_args appends interpreted timing labels,
projection timings, and cache_status into report diagnostics

↓

_CurrentFactsDiagnosticPayload

↓

_format_current_facts_timing_report
```

Timing interpretation was visible, but diagnostic payload construction remained embedded in the CLI-adjacent orchestration function.

## After

The cached current-facts timing path now flows as:

```text
measure State-cache elapsed time

↓

_CurrentFactsTimingInterpretation.from_cache_evidence(...)

↓

_CurrentFactsTimingDiagnosticPayload.from_timing_interpretation(...)

↓

_CurrentFactsDiagnosticPayload

↓

_format_current_facts_timing_report
```

`_CurrentFactsTimingDiagnosticPayload` consumes:

- `_CurrentFactsTimingInterpretation`;
- the measured State-path elapsed value.

It preserves:

- the existing `cache_status` value;
- the existing State-path timing tuple;
- the existing projection timing tuples.

It does not own elapsed-time measurement, timing interpretation, formatting, CLI behavior, cache behavior, projection behavior, events, or ledger replay.

## Boundary made explicit

The explicit recovered boundary is:

```text
_CurrentFactsTimingInterpretation
        !=
_CurrentFactsTimingDiagnosticPayload
```

Timing interpretation answers what the cache and projection timing evidence means. `_CurrentFactsTimingDiagnosticPayload` answers which interpreted timing facts are preserved for downstream diagnostic consumers.

## Compatibility preserved

No compatibility boundary changed.

The slice intentionally preserved:

- timing labels;
- elapsed values;
- diagnostic contents;
- CLI output shape;
- JSON behavior;
- cache behavior;
- projection behavior;
- event behavior;
- ledger replay behavior.

## Questions

### 1. Where were timing interpretation and diagnostic payload construction previously mixed?

They were mixed in `_current_facts_timing_from_args(...)` after `project_state_with_cache(...)` returned. That block constructed `_CurrentFactsTimingInterpretation`, then directly appended the interpreted State-path timing tuple, merged `projection_timings`, selected `cache_status`, and later supplied those values to `_CurrentFactsDiagnosticPayload`.

### 2. Which recovered architectural boundary became more explicit?

`Timing Interpretation != Diagnostic Payload` became explicit through the new `_CurrentFactsTimingDiagnosticPayload` owner.

### 3. How does the implementation now better reflect the recovered architecture?

The implementation now separates three local responsibilities:

1. `_current_facts_timing_from_args(...)` measures elapsed time and orchestrates the current-facts path.
2. `_CurrentFactsTimingInterpretation` interprets cache/projection timing evidence.
3. `_CurrentFactsTimingDiagnosticPayload` preserves the interpreted timing evidence in the diagnostic payload shape consumed by `CurrentFactsTimingReport`.

### 4. Did implementation evidence suggest a more precise responsibility name than "Diagnostic Payload"?

Yes. The evidence supports the more precise local responsibility name `Current-Facts Timing Diagnostic Payload`, represented by `_CurrentFactsTimingDiagnosticPayload`, because the recovered owner only preserves the timing portion of the current-facts diagnostic payload rather than all diagnostic material for the report.

### 5. Did any compatibility boundary change?

No.

## Files changed

- `scripts/seed_local.py`
- `tests/test_seed_local_script.py`
- `timing_visibility_slice_007.md`

## LOC changed

Implementation and test diff before this report:

```text
scripts/seed_local.py           | 36 ++++++++++++++++++++++++++++++------
tests/test_seed_local_script.py | 21 +++++++++++++++++++++
2 files changed, 51 insertions(+), 6 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_seed_local_script.py -q
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed timing responsibilities

- `_current_facts_timing_from_args(...)` still owns current-facts orchestration and several local measurements.
- The top-level `timings` list remains the final aggregation point for cached and uncached current-facts diagnostic timing tuples.
- The final bridge from `_CurrentFactsTimingDiagnosticPayload` into `_CurrentFactsDiagnosticPayload` remains intentionally compatibility-preserving and current-facts-local.
