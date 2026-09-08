# Projection Diagnostics Slice 001

## Selected architectural boundary

Recovered one implementation-local owner: `_ProjectionDiagnosticAggregation`.

The selected boundary is:

```text
Projection Measurement
        !=
Projection Diagnostic Aggregation
```

The recovered owner preserves only aggregation semantics for projection diagnostic evidence:

- repeated measured timing values are accumulated under the existing phase name;
- counter updates are accumulated under the existing counter name;
- existing `ProjectionBuildDiagnostics.timings` and `ProjectionBuildDiagnostics.counters` shapes remain unchanged.

## Implementation evidence

`ProjectionBuildDiagnostics` previously mixed two responsibilities in `timed(...)`:

1. measurement: calling `time.perf_counter()` before and after the supplied callable;
2. aggregation: mutating the timing tuple list by adding duplicate phase elapsed time or appending a new timing tuple.

`ProjectionBuildDiagnostics.add_count(...)` also owned counter aggregation directly.

Projection callers continue to provide phase names and execution boundaries:

- `StateProjector.project_from_state(...)` labels event materialization and event replay;
- `StateProjector.finalize(...)` labels finalization subphases;
- `StateProjector.apply(...)` labels fact event decoding.

Those callers still own projection/replay/finalization execution and labels. The recovered owner does not execute projection work and does not measure elapsed time.

## Before

`ProjectionBuildDiagnostics` directly owned:

- `time.perf_counter()` elapsed-time measurement;
- duplicate timing accumulation;
- timing tuple mutation;
- counter accumulation.

This compressed measurement and aggregation in a single diagnostics object.

## After

`ProjectionBuildDiagnostics.timed(...)` still measures elapsed time using the same `time.perf_counter()` semantics, then delegates preservation of the measured value to `_ProjectionDiagnosticAggregation.add_timing(...)`.

`ProjectionBuildDiagnostics.add_count(...)` delegates counter accumulation to `_ProjectionDiagnosticAggregation.add_count(...)`.

The public diagnostic container remains the same compatibility surface: callers still construct `ProjectionBuildDiagnostics`, pass it through projector/cache paths, and read `timings` and `counters` directly.

## Boundary made explicit

`_ProjectionDiagnosticAggregation` is now the implementation-local owner of projection diagnostic aggregation.

It explicitly does not own:

- elapsed-time measurement;
- projection execution;
- replay execution;
- projection publication;
- cache behavior;
- diagnostic consumers;
- CLI behavior;
- JSON/rendering behavior.

## Compatibility preserved

No compatibility boundary changed.

Preserved:

- projection phase labels;
- timing values and accumulation semantics;
- counter values and accumulation semantics;
- public `ProjectionBuildDiagnostics` construction and field access;
- CLI output shape;
- JSON/debug payload shapes;
- cache behavior;
- projection behavior;
- events and ledger replay behavior.

## Files changed

- `seed_runtime/state.py`
- `tests/test_state_projector.py`
- `projection_diagnostics_slice_001.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/state.py         | 37 ++++++++++++++++++++++++++++++-------
tests/test_state_projector.py | 32 ++++++++++++++++++++++++++++++++
2 files changed, 62 insertions(+), 7 deletions(-)
```

## Tests executed

- `pytest -q tests/test_state_projector.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Required questions

### 1. Where were projection measurement and projection diagnostic aggregation previously mixed?

They were mixed in `ProjectionBuildDiagnostics.timed(...)`, which both measured elapsed time with `time.perf_counter()` and mutated `timings` to accumulate duplicate phase values or append new timing tuples. Counter aggregation was also directly in `ProjectionBuildDiagnostics.add_count(...)`.

### 2. Which recovered architectural boundary became more explicit?

The boundary between projection measurement and projection diagnostic aggregation became explicit.

### 3. How does the implementation now better reflect the recovered architecture?

`ProjectionBuildDiagnostics.timed(...)` remains responsible for the measurement boundary because it owns the start/stop calls around the supplied callable. `_ProjectionDiagnosticAggregation` now owns how measured timing values and counter updates are preserved in the existing diagnostic evidence structures.

### 4. Did implementation evidence suggest a more precise responsibility name than "Projection Diagnostic Aggregation"?

Insufficient implementation evidence.

### 5. Did any compatibility boundary change?

No.

## Remaining compressed Projection Diagnostics responsibilities

Remaining pressure belongs outside this slice and should not be recovered here:

- projection phase naming remains embedded in projector/replay/finalization call sites;
- projection diagnostic measurement remains in `ProjectionBuildDiagnostics.timed(...)`;
- diagnostic consumption remains in state-build/current-facts/cache debug paths;
- CLI/JSON/rendering surfaces remain unchanged consumers of existing diagnostic data.

## Observations about the emerging family vocabulary

The implementation supports a narrow Projection Diagnostics vocabulary around optional, non-authoritative projection build evidence. The evidence supports separating measurement from aggregation, but it does not justify a broader timing framework, a projection execution redesign, or promotion of diagnostic phase labels into authoritative projection vocabulary.
