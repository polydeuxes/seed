# Execution Visibility Slice 002

## Selected architectural boundary

Execution Status != Execution Timing.

This slice makes the boundary directly observable inside the observation collection implementation by separating transient status lifecycle emission from timing diagnostic construction.

## Implementation evidence

Before this slice, `ObservationCollectionService.collect(...)` created an `ObservationProducerLifecycle` for status emission and then interleaved that status lifecycle with local `time.perf_counter()` measurements and `ObservationIngestionDiagnostics` construction. The same method both answered "what is happening?" through lifecycle status calls and "how long did it take?" through elapsed-second construction.

The compressed transition point was the observation collection path around collection, normalization, ingestion, and diagnostic append construction:

- status responsibility: `ObservationProducerLifecycle(status_consumer, source.name)` and lifecycle calls such as `collecting()`, `collected(...)`, `normalizing(...)`, `normalized(...)`, `ingesting(...)`, and `completed(...)`;
- timing responsibility: phase-start timestamps, elapsed-second calculations, total elapsed calculation, and `ObservationIngestionDiagnostics(...)` construction for `--observe-timings` output.

## Before

`ObservationCollectionService.collect(...)` owned both status and timing mechanics inline:

```text
lifecycle.collecting()
collect_started = time.perf_counter()
observations = list(source.collect())
collect_seconds = time.perf_counter() - collect_started
lifecycle.collected(len(observations))
...
diagnostics.append(ObservationIngestionDiagnostics(... elapsed values ...))
```

That made the transition from execution status to execution timing visible only as alternating lines inside one implementation body.

## After

`ObservationCollectionService.collect(...)` still controls the same execution order and emits the same status payloads, but timing construction is delegated to the implementation-local `_ObservationIngestionTiming` responsibility.

`_ObservationIngestionTiming` now owns:

- total timing start;
- phase timing start;
- phase elapsed construction for source collection, normalization, and event generation plus ledger write;
- `ObservationIngestionDiagnostics` construction.

`ObservationProducerLifecycle` continues to own status lifecycle vocabulary and status emission.

## Boundary made explicit

The recovered boundary made explicit is:

```text
Execution Status
    !=
Execution Timing
```

Status lifecycle calls remain responsible for transient operator-visible progress. `_ObservationIngestionTiming` is responsible for elapsed timing diagnostics and does not emit status.

## Compatibility preserved

Did any compatibility boundary change?

No.

Compatibility is preserved. The slice does not rename public vocabulary, change CLI flags, schemas, JSON payloads, ledger events, emitted status payload contents, status phases, timing labels, timing calculations, execution order, or measurement clock source.

## Files changed

- `seed_runtime/observation_sources.py`
  - Added `_ObservationIngestionTiming` as an implementation-local timing diagnostic builder.
  - Updated `ObservationCollectionService.collect(...)` to use that timing builder while preserving existing lifecycle status calls and diagnostic values.
- `execution_visibility_slice_002.md`
  - Added this implementation evidence report.

## LOC changed

Current diff stat at report time, including this report:

```text
execution_visibility_slice_002.md   | report added
seed_runtime/observation_sources.py | 68 ++++++++++++++++++++++++++++++-------
```

## Tests executed

```text
pytest -q tests/test_execution_status.py tests/test_seed_local_script.py::test_cli_observe_local_host_timings_are_comparable_and_non_semantic
```

Result: passed, 17 tests.

## Remaining compressed execution visibility boundaries

Implementation still contains other timing/debug surfaces that can be investigated in later slices without vocabulary migration:

- projection timing and projection cache debug/report construction;
- state-build timing report construction and rendering;
- current-facts timing wrapper and timing formatter coupling;
- progress cadence timing used to throttle status emission;
- phase timing labels embedded directly inside projection/state build flow;
- status payload construction call sites outside the observation lifecycle.
