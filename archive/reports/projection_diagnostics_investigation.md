# Projection Diagnostics Implementation Investigation

## Scope

This is a bounded implementation investigation. It does not implement ownership recovery, new payloads, wrappers, projection redesign, timing framework, runtime surfaces, behavior changes, or compatibility changes.

The question reviewed is whether repository implementation currently exposes a recurring **Projection Diagnostics** responsibility suitable for a future bounded ownership recovery family.

## Implementation evidence reviewed

Reviewed implementation-local evidence around projection construction, cache replay, debug consumers, and tests:

- `seed_runtime/state.py`
  - `ProjectionBuildDiagnostics`
  - `StateProjector.project(...)`
  - `StateProjector.project_from_state(...)`
  - `StateProjector.finalize(...)`
  - `StateProjector.apply(...)`
- `seed_runtime/projection_store.py`
  - `project_state_with_cache(...)`
  - incremental projection replay path
  - full projection rebuild path
  - cached projection materialization path
  - `rebuild_state_cache(...)` diagnostic pass-through
- `scripts/seed_local.py`
  - state-build cache-debug report/payload/formatter
  - current-facts timing interpretation/payload/presentation
  - projection-store timing wrapper used by current-facts cache debug
- `tests/test_state_projector.py`
  - direct projection diagnostic accumulation expectations
- `tests/test_seed_local_script.py`
  - state-build cache-debug projection diagnostic separation
  - current-facts timing interpretation/payload/presentation tests

Commands used for investigation:

```bash
rg -n "class ProjectionBuildDiagnostics|ProjectionBuildDiagnostics|def project_from_state|def finalize|project_state_with_cache|state_summary_cache_debug|current_facts" seed_runtime tests -S
sed -n '130,230p' seed_runtime/state.py
sed -n '840,1015p' seed_runtime/state.py
sed -n '1015,1095p' seed_runtime/state.py
sed -n '1095,1175p' seed_runtime/state.py
sed -n '520,735p' seed_runtime/projection_store.py
sed -n '740,785p' seed_runtime/projection_store.py
rg -n "ProjectionBuildDiagnostics|projection_timings|projection_counters|StateSummaryCacheDebugReport|_ProjectionCacheDiagnosticPayload|CurrentFacts|projection diagnostics|projection timings|projection counters|full projection rebuild|cached projection" scripts seed_runtime tests -S
sed -n '3220,3560p' scripts/seed_local.py
sed -n '5240,5525p' scripts/seed_local.py
```

## Recurring implementation patterns

### 1. Projection measurement exists as optional, non-authoritative instrumentation

`ProjectionBuildDiagnostics` is an explicit dataclass for optional projected-State construction diagnostics. It stores `timings` and `counters`, measures elapsed time with `time.perf_counter()`, accumulates duplicate timing names by adding elapsed durations to the existing entry, and accumulates named counters.

This is implementation evidence for a projection measurement and aggregation object, not just comments or architecture prose.

### 2. Projection replay and finalization pass diagnostics through multiple projection phases

`StateProjector.project(...)` accepts optional diagnostics and passes them into `project_from_state(...)`. `project_from_state(...)` measures input event materialization, counts total projection events, counts event kinds during replay, times event replay through the replay-selection executor, and passes diagnostics into `finalize(...)`.

`StateProjector.finalize(...)` uses the same optional diagnostics object to time many named finalization subphases, including alias projection, measurement evidence scan, measurement history retention, inferred fact projection, fact partitioning, measurement provenance pruning, fact support construction, relationship projection, entity type assertion projection, graph issue construction, alias list materialization, and fact conflict handling. It then updates structure counters such as entities, facts, relationships, graph issues, evidence, and observations.

This is strong evidence for a recurring diagnostic lifecycle inside projection construction:

```text
Projection measurement
  -> Projection diagnostic accumulation
  -> Projection diagnostic payload fields
  -> Projection diagnostic consumers
```

The lifecycle is not implemented as a single named lifecycle type, but the same diagnostics object crosses replay, finalization, cache rebuild, and debug presentation paths.

### 3. Projection diagnostic labels are currently embedded where projection work is performed

Diagnostic names such as `projection input event materialization`, `event replay`, `event replay: fact event decoding`, `full projection rebuild`, `cached projection load/materialize`, and `finalization: ...` are literal strings embedded at measurement call sites.

This means diagnostic naming is a real implementation responsibility, but it is not isolated from projection execution/finalization code. The labels function as the diagnostic grammar consumed by debug output and tests.

### 4. Projection counters are accumulated alongside timing diagnostics

The diagnostics object is not timing-only. It also stores counters for total projection events, per-event-kind replay counts, and final State structure counts. State-build cache debug renders these counters as `Projection/build structure counts`.

This supports treating projection diagnostics as broader than current-facts timing or state-build timing. The implementation has projection-specific measurement and projection-specific structure counting in the same diagnostic carrier.

### 5. Projection diagnostic payloads are consumed by more than one debug surface

State-build cache debug constructs `ProjectionBuildDiagnostics`, passes it into projection build/cache paths, then packages `projection_diagnostics.timings` and `projection_diagnostics.counters` into `_ProjectionCacheDiagnosticPayload`. The report exposes compatibility properties for `projection_timings` and `projection_counters`, and the formatter renders counters and subphase timings.

Current-facts cache debug also constructs `ProjectionBuildDiagnostics`, passes it through `project_state_with_cache(...)`, interprets the resulting projection timings with cache evidence, folds those timings into `_CurrentFactsTimingDiagnosticPayload`, and presents them as current-facts timing output.

The same producer object is therefore consumed by separate callers with different presentation boundaries.

## Counterexamples and limits

### 1. Projection diagnostics remain optional and non-authoritative

The implementation names `ProjectionBuildDiagnostics` as optional and non-authoritative. Projection still runs without diagnostics. The diagnostic object does not define projection correctness, state authority, cache validity, or publication behavior.

This is a counterexample to any claim that projection diagnostics own projection execution.

### 2. Projection execution, replay selection, finalization, and publication are already distinct from diagnostics

`project_from_state(...)` performs event materialization, replay scope recovery/assessment/selection, replay execution, finalization, and publication. Diagnostics wrap parts of this process but do not choose replay targets or publish visible state.

The implementation includes projection publication request/publication dataclasses, and publication is a handoff of finalized state. That publication boundary is separate from the diagnostics carrier.

### 3. Projection cache responsibility is not projection diagnostics ownership

`project_state_with_cache(...)` owns cache lookup, snapshot validation, incremental replay orchestration, status emission, snapshot save, and `StateCacheStatus` construction. Diagnostics are passed through and may measure cached projection materialization or full rebuild, but cache-hit/miss semantics belong to projection-store/cache code.

Projection diagnostics should not be inferred to own projection cache behavior.

### 4. Current-facts timing and state-build timing are separate consumers, not owners of projection diagnostics

Current-facts cache debug has its own timing report, cache visibility interpretation, diagnostic payload, and presentation objects. State-build cache debug has its own visibility payload, report, local timing closure, summary-cache behavior, and formatter. They consume projection diagnostics but also measure and present their own non-projection phases.

This prevents concluding that projection diagnostics are owned by current-facts timing or state-build timing.

### 5. There is no explicit Projection Diagnostics lifecycle abstraction yet

The lifecycle is recoverable from repeated implementation behavior, but the repository does not currently expose a single `ProjectionDiagnosticsLifecycle`, typed phase enum, label registry, payload schema, or consumer interface. Existing behavior is object-and-call-site based.

Therefore, a future ownership recovery should be bounded and implementation-local if attempted; a broad framework is not supported by current evidence.

## Answers to central questions

### 1. Does a recurring Projection Diagnostics responsibility currently exist?

Yes, with bounded scope.

The recurring responsibility exists as optional projection-build diagnostic instrumentation centered on `ProjectionBuildDiagnostics`, not as a broad diagnostic framework. The same diagnostics object measures projection subphases, accumulates duplicate timing names, records projection counters, is passed through replay/finalization/cache paths, and is consumed by state-build cache debug and current-facts cache debug.

The evidence supports a recoverable implementation family for projection diagnostics, but not a redesign of projection execution, projection cache, current-facts timing, or state-build timing.

### 2. If yes, where is the strongest implementation evidence?

Strongest evidence appears in four places:

1. `ProjectionBuildDiagnostics` itself: explicit timings/counters fields, elapsed measurement, duplicate timing accumulation, and counter accumulation.
2. `StateProjector.project_from_state(...)`: event materialization timing, event count accumulation, per-event-kind count accumulation, timed replay, and diagnostics pass-through to finalization.
3. `StateProjector.finalize(...)`: repeated named finalization subphase timings and final projection structure counters.
4. Consumers in `scripts/seed_local.py`: state-build cache debug packages projection timings/counters into `_ProjectionCacheDiagnosticPayload`; current-facts cache debug turns projection diagnostics into interpreted diagnostic payload entries.

Together these show producer, aggregator, payload, and consumers.

### 3. What implementation responsibilities currently appear compressed?

The following responsibilities appear compressed in current implementation:

- Measurement and aggregation are combined in `ProjectionBuildDiagnostics.timed(...)`: it both measures elapsed time and merges duplicate names.
- Diagnostic label vocabulary is embedded inline in projection execution and finalization call sites.
- Projection replay/finalization code owns both projection work and diagnostic measurement call placement.
- Projection counters share the same carrier as timings even though they represent structural summaries rather than elapsed measurements.
- State-build cache debug combines local state-build timing, projection-cache visibility, projection diagnostic payload construction, summary-cache behavior, and rendering data assembly in one command path.
- Current-facts cache debug combines projection-store wrapper timing, projection diagnostic interpretation, query/render timing, and final report assembly in one command path.

These compressions are implementation-local evidence for possible bounded recovery. They do not justify a global timing framework.

### 4. Which projection responsibilities are already sufficiently explicit?

The following projection responsibilities are already sufficiently explicit and should not be folded into projection diagnostics:

- Event replay authority and state projection entry points in `StateProjector.project(...)` and `project_from_state(...)`.
- Replay selection/execution and finalization handoff inside `project_from_state(...)`.
- Projection publication as finalized-state handoff through implementation-local publication dataclasses.
- Derived index rebuilding in `finalize(...)`.
- Event application in `apply(...)`.
- Projection cache lookup, snapshot validation, incremental replay orchestration, status creation, and snapshot saving in `project_state_with_cache(...)`.
- State-build cache visibility/reporting and current-facts visibility/reporting as separate debug consumers.

These responsibilities may call or consume diagnostics, but implementation evidence does not show they belong to a Projection Diagnostics owner.

### 5. Should Projection Diagnostics become the next implementation responsibility family?

Yes, but only as a bounded ownership recovery candidate, and only if the next task remains implementation-local and compatibility-preserving.

The repository contains enough recurring evidence to justify a bounded family around projection diagnostic measurement, aggregation, naming, payload transfer, and consumer handoff. It is mature enough to investigate/recover ownership boundaries because the same diagnostic object and data shape already recur across projection build, projection cache, state-build cache debug, and current-facts cache debug.

However, the evidence does not support redesigning projection execution, changing projection cache semantics, creating a global timing framework, changing CLI output, or normalizing every timing surface under one owner.

## Supported conclusions

- A recurring Projection Diagnostics responsibility exists in implementation.
- It is centered on optional, non-authoritative `ProjectionBuildDiagnostics` data and behavior.
- It includes projection subphase timing, duplicate timing accumulation, projection/event counters, diagnostic labels, and consumer-facing payload fields.
- It is consumed by at least state-build cache debug and current-facts cache debug.
- Projection diagnostics are separate from projection execution authority, projection publication, projection cache correctness, current-facts timing ownership, and state-build timing ownership.
- The candidate family is mature enough for a future bounded ownership recovery task.

## Unsupported conclusions

- Unsupported: projection diagnostics own projection execution.
- Unsupported: projection diagnostics own replay selection, projection publication, or cache validity.
- Unsupported: current-facts timing or state-build timing owns projection diagnostics.
- Unsupported: the repository needs a global timing framework.
- Unsupported: diagnostic labels should be redesigned now.
- Unsupported: any CLI/report behavior should change as part of this investigation.
- Unsupported: projection diagnostic findings should become cluster truth.

## Confidence

Confidence: **medium-high**.

Reason: implementation evidence is direct and recurring across producer, projection phases, cache paths, and multiple consumers. Confidence is not high because the lifecycle is implicit rather than represented by one explicit lifecycle abstraction, and diagnostic labels remain inline in projection execution/finalization code.

## Recommended next action

Begin a future bounded ownership recovery only if explicitly requested.

Recommended scope for that future task:

1. Preserve behavior, labels, CLI output, JSON behavior, cache semantics, and tests.
2. Keep projection execution, replay, publication, and cache ownership out of scope.
3. Recover only implementation-local ownership around projection diagnostic measurement/aggregation/label handoff/payload transfer.
4. Add or update tests only to preserve existing diagnostic behavior if code is changed.
5. Run the operational diagnostic inventory and shape-audit tests if any runtime diagnostic surface or recordable output changes.

For this investigation, no implementation change is recommended.
