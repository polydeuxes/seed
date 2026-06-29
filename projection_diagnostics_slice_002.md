# Projection Diagnostics Slice 002

## Selected architectural boundary

This slice recovered the implementation-local boundary between **Projection Diagnostic Aggregation** and **Projection Diagnostic Payload**.

The selected owner is `_ProjectionDiagnosticPayload`.

## Implementation evidence

- `_ProjectionDiagnosticAggregation` already owned the repeated diagnostic measurement preservation rules: duplicate timing names are accumulated into a single elapsed value, and counters are incremented by name.
- `ProjectionBuildDiagnostics` remained the compatibility surface that measures elapsed phases with `time.perf_counter()` and exposes the existing `timings` and `counters` attributes.
- Downstream diagnostic consumers did not need aggregation behavior. They needed a payload containing the already-aggregated projection timing tuples and counters.
- State-build cache debug previously handed `projection_diagnostics.timings` and `projection_diagnostics.counters` directly into `_ProjectionCacheDiagnosticPayload`.
- Current-facts timing interpretation previously read `projection_diagnostics.timings` directly when assembling timing evidence for its diagnostic payload.

## Before

Projection diagnostic aggregation and projection diagnostic payload were mixed at the `ProjectionBuildDiagnostics` compatibility boundary.

`ProjectionBuildDiagnostics` simultaneously:

1. measured elapsed projection phases;
2. delegated repeated timing/counter preservation to `_ProjectionDiagnosticAggregation`;
3. exposed mutable `timings` and `counters` as the evidence consumed by state-build and current-facts diagnostic payload assembly.

That meant consumers reached through the compatibility surface directly for the payload shape, even though they did not own measurement or aggregation.

## After

`_ProjectionDiagnosticPayload` now snapshots aggregated diagnostic evidence for consumers.

It consumes `_ProjectionDiagnosticAggregation` and preserves:

- timing tuples as the projection diagnostic timing evidence handed downstream;
- counters as the projection diagnostic counter evidence handed downstream.

It does not own:

- elapsed-time measurement;
- aggregation of repeated timings;
- counter increment semantics;
- replay execution;
- projection execution;
- publication;
- cache behavior;
- diagnostic consumers;
- CLI output;
- JSON output;
- rendering.

`ProjectionBuildDiagnostics.payload` is the compatibility-preserving handoff point. Existing `ProjectionBuildDiagnostics.timings` and `ProjectionBuildDiagnostics.counters` remain available unchanged.

## Boundary made explicit

The explicit boundary is now:

```text
Projection Diagnostic Aggregation
        !=
Projection Diagnostic Payload
```

Aggregation answers:

```text
How are repeated diagnostic measurements preserved?
```

Payload answers:

```text
What projection diagnostic evidence is handed to downstream consumers?
```

## Compatibility preserved

No compatibility boundary changed.

`ProjectionBuildDiagnostics` remains the public compatibility surface, and the existing `timings` and `counters` fields remain present with the same list/dict shapes. The state-build cache debug and current-facts cache debug paths receive the same timing names, elapsed values, and counter values as before.

No CLI, JSON, projection behavior, cache behavior, event, ledger replay, timing label, timing value, counter value, or diagnostic content change was introduced.

## Files changed

- `seed_runtime/state.py`
- `scripts/seed_local.py`
- `tests/test_state_projector.py`
- `projection_diagnostics_slice_002.md`

## LOC changed

Measured with `git diff --stat` after the implementation:

```text
projection_diagnostics_slice_002.md | 157 ++++++++++++++++++++++++++++++++++++
scripts/seed_local.py               |   8 +-
seed_runtime/state.py               |  27 +++++++
tests/test_state_projector.py       |  25 ++++++
4 files changed, 214 insertions(+), 3 deletions(-)
```

## Tests executed

- `pytest -q tests/test_state_projector.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Questions answered with implementation evidence

### 1. Where were projection diagnostic aggregation and projection diagnostic payload previously mixed?

They were mixed at `ProjectionBuildDiagnostics` and its direct consumers. Aggregation had already moved into `_ProjectionDiagnosticAggregation`, but downstream code still consumed `ProjectionBuildDiagnostics.timings` and `ProjectionBuildDiagnostics.counters` directly as the diagnostic payload for state-build cache debug and current-facts timing diagnostics.

### 2. Which recovered architectural boundary became more explicit?

The boundary between **Projection Diagnostic Aggregation** and **Projection Diagnostic Payload** became directly observable through `_ProjectionDiagnosticPayload` and `ProjectionBuildDiagnostics.payload`.

### 3. How does the implementation now better reflect the recovered architecture?

The implementation now routes downstream projection diagnostic evidence through a payload owner instead of making consumers read the aggregation-backed mutable compatibility fields directly. Measurement stays in `ProjectionBuildDiagnostics.timed(...)`; repeated timing and counter preservation stay in `_ProjectionDiagnosticAggregation`; payload handoff now belongs to `_ProjectionDiagnosticPayload`.

### 4. Did implementation evidence suggest a more precise responsibility name than "Projection Diagnostic Payload"?

Insufficient implementation evidence.

The implementation evidence supported a consumer-facing diagnostic evidence payload, but did not justify a narrower vocabulary such as snapshot or evidence as a stronger owner name.

### 5. Did any compatibility boundary change?

No.

## Remaining compressed Projection Diagnostics responsibilities

Remaining implementation pressure appears outside this slice:

- projection finalization still carries phase-label selection adjacent to projection work;
- state-build cache debug still combines cache visibility, projection diagnostic payload consumption, summary-cache behavior, and report assembly;
- current-facts cache debug still combines State-path timing, fact-index cache timing, query/render timing, and report assembly;
- diagnostic consumers still decide how projection diagnostic payloads are presented in their local reports.

This slice does not recover those boundaries.

## Observations about the emerging family vocabulary

The current implementation evidence supports a narrow family vocabulary:

```text
Projection Measurement
↓
Projection Diagnostic Aggregation
↓
Projection Diagnostic Payload
↓
Projection Diagnostic Consumers
```

The vocabulary remains implementation-local. It describes diagnostic construction and handoff only; it does not promote presentation vocabulary into repository knowledge or projection authority.
