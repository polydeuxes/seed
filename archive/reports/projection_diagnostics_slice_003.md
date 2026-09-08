# Projection Diagnostics Slice 003

## Selected architectural boundary

`Projection Diagnostic Payload != Projection Diagnostic Selection`

The recovered implementation-local owner is `_ProjectionDiagnosticSelection`. It represents the narrow handoff where a diagnostic consumer selects the already-aggregated projection diagnostic evidence it needs from `_ProjectionDiagnosticPayload`.

## Implementation evidence

- `ProjectionBuildDiagnostics.payload` remains the compatibility surface that snapshots `_ProjectionDiagnosticAggregation` into `_ProjectionDiagnosticPayload`.
- State-build cache debug consumed `projection_diagnostics.payload` directly while constructing `_ProjectionCacheDiagnosticPayload`, selecting projection timings and counters for the state-build diagnostic report.
- Current-facts timing consumed `projection_diagnostics.payload` directly inside `_CurrentFactsTimingInterpretation.from_cache_evidence(...)`, selecting projection timings for the current-facts diagnostic report.
- Those two consumers needed different portions and shapes of the same projection diagnostic payload: state-build needed list-shaped timings and dict-shaped counters; current-facts needed tuple-shaped timings.

## Before

The implementation-local flow was compressed at each consumer:

```text
ProjectionBuildDiagnostics.payload
  -> _ProjectionDiagnosticPayload
  -> consumer-specific field extraction inline
  -> _ProjectionCacheDiagnosticPayload / _CurrentFactsTimingInterpretation
```

The payload owner and the consumer-specific request/selection boundary were adjacent and implicit. Consumers reached directly into `_ProjectionDiagnosticPayload` when deciding which evidence to carry forward.

## After

The implementation-local flow is now:

```text
ProjectionBuildDiagnostics.payload
  -> _ProjectionDiagnosticPayload
  -> _ProjectionDiagnosticSelection
  -> _ProjectionCacheDiagnosticPayload / _CurrentFactsTimingInterpretation
```

`_ProjectionDiagnosticSelection` consumes the unchanged payload snapshot and exposes only existing consumer handoff shapes:

- tuple timings for current-facts timing interpretation;
- list timings for state-build cache debug;
- copied counters for state-build cache debug.

It does not own measurement, aggregation, payload construction, projection execution, replay, publication, cache behavior, formatting, CLI, JSON, rendering, or diagnostic surface registration.

## Boundary made explicit

The boundary made explicit is:

```text
Projection Diagnostic Payload
  !=
Projection Diagnostic Selection
```

This is the implementation-backed equivalent of the expected pressure `Projection Diagnostic Payload != Projection Diagnostic Consumer Request`. The code evidence favored the more precise local word `Selection` because consumers were not constructing new diagnostic meaning; they were selecting existing evidence portions and existing container shapes.

## Compatibility preserved

No compatibility boundary changed.

`ProjectionBuildDiagnostics` still exposes:

- `timings`;
- `counters`;
- `payload`;
- `timed(...)`;
- `add_count(...)`.

The downstream report payloads, CLI output, JSON behavior, timing labels, counter names, values, cache behavior, projection behavior, replay behavior, event behavior, and ledger behavior remain unchanged.

## Files changed

- `seed_runtime/state.py`
  - Added `_ProjectionDiagnosticSelection`.
- `scripts/seed_local.py`
  - Routed state-build cache debug and current-facts timing through `_ProjectionDiagnosticSelection` before constructing their existing consumer payloads.
- `tests/test_state_projector.py`
  - Added regression coverage for the new selection owner and copy/shape preservation.
- `projection_diagnostics_slice_003.md`
  - Added this slice report.

## LOC changed

Before adding this report, implementation and test diff was:

```text
scripts/seed_local.py         | 21 +++++++++++++++------
seed_runtime/state.py         | 26 ++++++++++++++++++++++++++
tests/test_state_projector.py | 16 ++++++++++++++++
3 files changed, 57 insertions(+), 6 deletions(-)
```

## Tests executed

- `pytest -q tests/test_state_projector.py::test_projection_diagnostic_selection_preserves_consumer_handoff tests/test_seed_local_script.py::test_current_facts_timing_interpretation_keeps_measurements_unchanged`
- `pytest -q tests/test_state_projector.py tests/test_seed_local_script.py::test_current_facts_timing_interpretation_keeps_measurements_unchanged tests/test_seed_local_script.py::test_current_facts_timing_diagnostic_payload_preserves_interpreted_evidence tests/test_seed_local_script.py::test_current_facts_timing_presentation_formats_preserved_diagnostics`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed Projection Diagnostics responsibilities

- Projection phase labels are still embedded at measurement call sites.
- Projection diagnostic measurement and aggregation still live behind the `ProjectionBuildDiagnostics` compatibility surface.
- Projection diagnostic payload consumption remains surface-local after the selection boundary: state-build cache debug and current-facts timing still decide how their own reports interpret or present selected evidence.
- No evidence in this slice supports a shared diagnostics framework.

## Observations about the emerging family vocabulary

The implementation continues to show a narrow Projection Diagnostics family vocabulary:

```text
Projection Measurement
  -> Projection Diagnostic Aggregation
  -> Projection Diagnostic Payload
  -> Projection Diagnostic Selection
  -> Projection Diagnostic Consumers
```

This vocabulary is implementation-local and evidence-backed only at the boundaries recovered so far. It should not be promoted into repository knowledge beyond the code evidence without a dedicated audit.

## Questions

### 1. Where were projection diagnostic payload and consumer-specific diagnostic request previously mixed?

They were mixed where consumers directly extracted fields from `ProjectionBuildDiagnostics.payload` / `_ProjectionDiagnosticPayload`:

- state-build cache debug selected `projection_payload.timings` and `projection_payload.counters` inline while constructing `_ProjectionCacheDiagnosticPayload`;
- current-facts timing selected `projection_payload.timings` inline inside `_CurrentFactsTimingInterpretation.from_cache_evidence(...)`.

### 2. Which recovered architectural boundary became more explicit?

`Projection Diagnostic Payload != Projection Diagnostic Selection` became explicit through `_ProjectionDiagnosticSelection`.

### 3. How does the implementation now better reflect the recovered architecture?

Projection Diagnostics still produces an unchanged `_ProjectionDiagnosticPayload`. Consumers no longer reach directly into that payload at the handoff point; they first pass through `_ProjectionDiagnosticSelection`, which owns only the request/selection of already-produced diagnostic evidence in existing consumer-needed shapes.

### 4. Did implementation evidence suggest a more precise responsibility name than "Projection Diagnostic Consumer Request"?

Yes. The implementation evidence supports `Projection Diagnostic Selection`, represented by `_ProjectionDiagnosticSelection`, because the consumers select existing evidence portions and container shapes from an already-aggregated diagnostic payload rather than creating a broader request protocol.

### 5. Did any compatibility boundary change?

No.
