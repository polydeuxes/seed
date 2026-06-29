# Timing Visibility Ownership Audit

## Scope and method

This is a bounded implementation audit of existing timing-producing paths. It does not introduce timing behavior, normalize timing structures, add a framework, alter CLI behavior, change schemas, mutate caches, or change ledger semantics.

Reviewed implementation families:

- state build cache debug
- current facts cache debug
- projection build diagnostics and projection timings
- projection cache visibility
- execution status/progress visibility
- observation collection/ingestion timings
- knowledge reachability diagnostic timing
- diagnostic inventory and shape-audit registrations

The central finding is that timing measurement ownership has **not converged**. The repository has recovered several implementation-visible owners, but timing remains a family of independently evolved local timing responsibilities rather than one shared timing architecture.

## Executive answer

**Has timing measurement ownership converged?**

No. There is shared timing grammar in the human-facing shape of `(phase/name, elapsed seconds)` and in labels such as `timings`, `elapsed`, `total`, and `phase`, but measurement remains independently owned by local implementation paths:

- `ProjectionBuildDiagnostics` owns optional projection-construction subphase timing.
- `state_summary_cache_debug_from_args` owns state-build/cache-debug phase timing.
- `_current_facts_timing_from_args` and `_TimingProjectionStore` own current-facts path and cache-wrapper timing.
- `_ReachabilityTimer` owns knowledge-reachability audit phase timing.
- observation ingestion diagnostics own source collection, normalization, event generation, ledger write, and rates.
- `ProgressCadence` owns elapsed-time gating for transient status emission, not elapsed duration reporting.

**Which timing responsibilities are already implementation-visible?**

- Projection build subphase measurement and aggregation are visible in `ProjectionBuildDiagnostics`.
- State-build cache-debug timing, cache-status explanation, projection diagnostic inclusion, and rendering are visible as separate dataclass payloads and formatter functions.
- Current-facts cache-debug timing separates output visibility, diagnostic payload, cache visibility labels, projection-store timing wrapper, and formatter.
- Execution status separates transient status emission/consumption/rendering from execution ownership.
- Observation ingestion timing separates collection/normalization/event-writing durations from CLI formatting.
- Diagnostic inventory and shape-audit registration make current-facts cache debug visible as an operational diagnostic surface.

**Which timing responsibilities remain compressed?**

- State-build cache debug still measures phases, performs cache lookup, invokes projection, derives summaries, saves summary snapshots, builds diagnostic payloads, and arranges rendering data in one CLI-side function.
- Current-facts cache debug still measures ledger/store/projector/query/render phases, decorates cache-store methods for timing, interprets cache status, extends projection timings, and builds the report in one CLI-side function.
- Projection diagnostics measure and aggregate repeated projection subphases in one class, while projection finalization chooses timing labels inline around each builder call.
- Knowledge reachability combines timing measurement, progress messaging, metadata aggregation, rounding, and report rendering in the audit module.
- Observation ingestion timing records collection/normalization/write durations and rates as source diagnostics, while CLI formatting remains a separate but still source-specific presentation path.

**What is the smallest safe next timing ownership slice?**

The safest first slice is documentation/test-backed ownership recovery around **current-facts cache timing**, not a shared framework: extract or clarify the boundary between (1) measuring the State path/cache wrapper, (2) interpreting `StateCacheStatus` into cache visibility labels, and (3) formatting the timing report. This preserves compatibility because it can keep the same labels, report text, CLI flags, and `ProjectionBuildDiagnostics` payload while reducing the largest remaining compression in a narrow diagnostic surface.

**Should timing work continue through ownership recovery or behavior-oriented improvement?**

Timing work should continue through targeted ownership recovery. The family has not reached behavior-oriented improvement readiness because measurement owners have not converged, aggregation remains local, and presentation/diagnostic explanation are still mixed in important CLI timing surfaces. Behavior changes such as optimization, normalized schemas, or a timing framework are not supported by current evidence.

## Timing-producing families reviewed

| Family | Measurement owner | Aggregation owner | Diagnostic owner | Presentation owner | Cache visibility owner | Implementation evidence | Remaining compression | Limitations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Projection build diagnostics | `ProjectionBuildDiagnostics.timed(...)` around projection phases. | `ProjectionBuildDiagnostics.timings` appends or accumulates duplicate names; `counters` stores structure counts. | `ProjectionBuildDiagnostics` plus `StateProjector.project_from_state(...)` and `finalize(...)` label phases. | Downstream formatters, especially state-build and current-facts debug, render projection timings. | None directly; projection cache only passes diagnostics through when building/loading state. | `ProjectionBuildDiagnostics` uses `time.perf_counter()`, accumulates duplicate timing names, and exposes counters. `StateProjector.project_from_state(...)` times event materialization/event replay and `finalize(...)` times finalization subphases. | Measurement, aggregation, and naming grammar are together in one diagnostics class; projection finalization still embeds diagnostic labels inline with build calls. | Does not prove a global timing contract. Optional and non-authoritative. |
| Projection cache / State cache | Cache path duration is not owned globally; timing is supplied by callers or diagnostics around materialization. | `StateCacheStatus` aggregates cache hit/miss, snapshot IDs, incremental replay, and events applied, not elapsed time. | `project_state_with_cache(...)` owns cache-path status and diagnostic pass-through. | CLI surfaces render cache status and timings. | `project_state_with_cache(...)` and `StateCacheStatus`. | `StateCacheStatus` records cache hit/version/event ids/incremental replay/events applied. `project_state_with_cache(...)` loads snapshots, detects hit/miss/incremental replay, emits status, invokes projector, and saves snapshots. | Cache visibility, replay orchestration, status emission, diagnostic pass-through, and snapshot save remain in one function. | Cache status is not timing ownership; it only explains the measured path for callers. |
| State build cache debug | Local `timed(...)` closure inside `state_summary_cache_debug_from_args`. | `StateSummaryCacheDebugReport.timings` plus `_ProjectionCacheDiagnosticPayload.projection_timings/counters`. | `_StateBuildVisibilityPayload` and `_ProjectionCacheDiagnosticPayload`. | `format_state_summary_cache_debug_report(...)`. | `_StateBuildVisibilityPayload` plus projection cache status strings inside report. | The function times store open, ledger open, event listing, summary lookup, state cache lookup, projection build, summary derivation, snapshot save, and rendering; the formatter prints cache status, ids, counters, timings, and projection subphase timings. | Measurement, cache lookup, projection invocation, summary read-model construction, snapshot save, report construction, and placeholder render timing are together in one CLI function. | Good local visibility, but not evidence that state build timing owns projection timing or cache timing globally. |
| Current facts cache debug | Local `timed(...)` closure plus `_TimingProjectionStore._timed(...)` wrapper. | `_CurrentFactsDiagnosticPayload.timings`; projection diagnostics are appended into the same list. | `_CurrentFactsDiagnosticPayload`; `_CurrentFactsCacheVisibility` explains state cache path labels. | `_format_current_facts_timing_report(...)`. | `_CurrentFactsCacheVisibility.from_state_cache_status(...)`. | `_current_facts_timing_from_args(...)` measures ledger/store/projector/projection/read-model/query/render phases. `_TimingProjectionStore` times cache metadata lookup, snapshot save, and fact-index cache load/save. The formatter renders cache status and timings. | Measurement, cache wrapper instrumentation, projection diagnostics inclusion, query/render timing, and final report assembly remain compressed in the CLI function. | The surface is registered in diagnostic inventory and shape audit, but registration does not imply timing architecture convergence. |
| Execution status / visibility | `ProgressCadence` measures elapsed time only for status-cadence gating via `monotonic`. | `RecordingExecutionStatusConsumer` aggregates emitted statuses for tests; status itself has no elapsed field. | `ExecutionStatusEmitter`/producer calls own status payload emission. | `CliExecutionStatusConsumer` renders status messages. | None. | `ExecutionStatus` is renderer-independent and non-authoritative. `ProgressCadence.should_emit(...)` uses item interval and elapsed time interval to decide when progress appears. | Elapsed-time cadence is intentionally mixed with progress visibility, not diagnostic timing. | Execution status is not execution timing; it does not report durations. |
| Observation collection / ingestion | Observation ingestion path diagnostics measure source collection, normalization, event generation + ledger write, and total seconds. | `ObservationIngestionDiagnostics` aggregates durations, counts, facts promoted, counters, and rates. | Observation ingestion diagnostics. | `format_observation_ingestion_diagnostics(...)`. | None. | CLI formatter prints source collection, normalization, event generation + ledger write, total, counts, facts promoted, observations/sec, events/sec, and source counters. | Source timing remains coupled to ingestion diagnostic shape; presentation is separate but strongly tied to those fields. | This is observation timing, not projection/cache/execution timing. |
| Knowledge reachability diagnostic timing | `_ReachabilityTimer.phase(...)` uses `time.monotonic()`. | `KnowledgeReachabilityMetadata.timings` and `indexes`; metadata rounds timings and stores counters. | Knowledge reachability audit result metadata. | `format_knowledge_reachability_table(...)` renders timing metadata. | Cache metadata may be reported, but it is audit-specific cache visibility. | `_ReachabilityTimer` emits start/end/progress, records elapsed phase timings, computes total, and metadata includes timings/indexes/cache. | Timing, progress emission, metadata aggregation, rounding, index timing, and presentation are all audit-local. | This path shows independent diagnostic timing evolution outside projection/cache debug. |
| Diagnostic inventory / shape audit | No runtime measurement. | Inventory/shape specs aggregate declared diagnostic shape. | `DiagnosticInventoryEntry` and `DiagnosticImplementationSpec`. | Inventory formatters and CLI. | Surface registration only. | `current_facts_cache_debug` is registered as read-only, non-recording, non-mutating, and shape-audited with build/format functions. | Visibility registration is distinct from timing measurement ownership. | Does not validate timing labels or phase durations. |

## Implementation evidence by responsibility

### Measurement

Measurement is local and repeated:

- Projection timing uses `time.perf_counter()` inside `ProjectionBuildDiagnostics.timed(...)`.
- State-build cache debug defines its own `timed(...)` closure with `time.perf_counter()`.
- Current-facts cache debug defines another `timed(...)` closure and a `_TimingProjectionStore` wrapper with its own `_timed(...)` method.
- Knowledge reachability uses a separate `_ReachabilityTimer` with `time.monotonic()`.
- Execution status uses `monotonic` only to decide whether enough time has elapsed to emit progress.

This supports the conclusion that measurement ownership has **not** converged. It has recovered into implementation-visible local owners.

### Aggregation

Aggregation is also local:

- Projection diagnostics aggregate `list[tuple[str, float]]` plus counters.
- State-build cache debug aggregates visibility payload, projection diagnostic payload, and top-level timings.
- Current-facts cache debug aggregates output visibility plus diagnostic payload.
- Knowledge reachability aggregates timings, indexes, counters, cache metadata, scan counts, and truncation metadata.
- Observation ingestion diagnostics aggregate durations, counts, rates, and source counters.

The recurring shape is similar, but the structures are not shared and should not be treated as one timing schema.

### Diagnostics and explanation

Diagnostic explanation is partially recovered:

- `StateCacheStatus` explains cache hit/miss, snapshot/current event ids, incremental replay, and events applied.
- `_CurrentFactsCacheVisibility` translates `StateCacheStatus` into human-readable cache-path labels.
- State-build cache debug separates visibility payload from projection diagnostic payload.
- Diagnostic inventory and shape audit register current-facts cache debug as read-only and non-mutating.

However, explanation is still frequently built inside the same path that measures and performs the work.

### Presentation

Presentation is more separated than measurement:

- `format_state_summary_cache_debug_report(...)` renders state-build cache debug.
- `_format_current_facts_timing_report(...)` renders current-facts timing.
- `format_observation_ingestion_diagnostics(...)` renders observation timing.
- `format_knowledge_reachability_table(...)` renders reachability timing metadata.
- `CliExecutionStatusConsumer` renders transient execution status.

Presentation separation exists, but presentation labels are still local and do not prove shared timing ownership.

### Cache visibility

Cache visibility is implementation-visible but not centralized:

- Projection state cache visibility is carried by `StateCacheStatus` and status emissions in `project_state_with_cache(...)`.
- State-build cache debug has its own summary-cache and state-cache status fields.
- Current-facts cache debug translates `StateCacheStatus` into cache labels and timing path names.
- Knowledge reachability has audit-specific cache metadata.

Cache timing and cache visibility remain related but distinct. Cache status explains what path was taken; it does not own elapsed-time measurement globally.

## Recurring timing responsibilities

### Elapsed time measurement

Elapsed measurement recurs with both `perf_counter()` and `monotonic()`. The repository does not expose a single timing clock owner, and current evidence does not justify adding one.

### Phase timing

Phase timing is common across projection diagnostics, state-build cache debug, current-facts cache debug, and knowledge reachability. The grammar is shared informally: a phase name mapped to elapsed seconds. The implementation is not shared.

### Projection timing

Projection timing is the clearest recovered owner: `ProjectionBuildDiagnostics` owns optional projection construction timings and counters. But projection callers still decide whether and how to merge those timings into their reports.

### Cache timing

Cache timing is caller-local. State-build cache debug times snapshot lookup and decode directly. Current-facts cache debug wraps `ProjectionStore` to time load/save calls. `project_state_with_cache(...)` owns cache behavior and cache status but does not own top-level elapsed reporting.

### Execution timing

Execution status is not duration reporting. It owns transient progress/status visibility and cadence gating. Recent execution timing work should not be read as convergence with projection/cache timing.

### Status timing

Status timing exists only as cadence: emit progress after enough item or wall-clock interval. It does not report measured durations.

### Diagnostic timing

Diagnostic timing remains diagnostic-local. Knowledge reachability, observation ingestion, current-facts cache debug, and state-build cache debug each retain their own timing structures.

## Counterexamples and duplicated local structures

Counterexamples where measurement, aggregation, diagnostic explanation, and presentation remain compressed or adjacent:

1. **State build cache debug**: the CLI function opens resources, measures phases, performs cache lookups, invokes projection, builds read models, saves summary snapshots, constructs visibility/diagnostic payloads, and returns report data.
2. **Current facts cache debug**: the CLI function opens resources, seeds dev state when needed, measures projection and query phases, wraps the store for cache timings, appends projection diagnostics, interprets cache status, and constructs the report.
3. **Projection finalization diagnostics**: finalization labels are embedded inline around projection-builder operations.
4. **Knowledge reachability**: the timer emits progress, records timings, computes total, metadata rounds/aggregates timings, and the formatter presents them.

Duplicated timing structures that appear implementation-local rather than intentionally shared:

- `list[tuple[str, float]]` in `ProjectionBuildDiagnostics`, state-build debug, current-facts debug, and CLI reports.
- `dict[str, float]` in knowledge reachability metadata.
- Local `timed(...)` closures in multiple CLI debug paths.
- Local cache timing wrappers rather than a shared cache instrumentation boundary.

These duplications are not necessarily defects. They are evidence that timing responsibilities evolved independently.

## Supported conclusions

1. Timing measurement ownership has **not converged**.
2. The repository has recovered multiple implementation-visible timing owners.
3. Projection build timing is the strongest localized owner.
4. Execution status and execution timing remain distinct; status cadence is not duration reporting.
5. Cache visibility and cache timing are distinct; cache status explains a path, while elapsed measurement is usually caller-owned.
6. Presentation is mostly separated into formatter functions, but labels and report shapes remain local.
7. A shared timing framework, generic API, registry, schema, or normalization is not supported by the current audit evidence.

## Unsupported conclusions

The implementation evidence does **not** support concluding that:

- all timing should converge into one framework;
- projection timing should own cache timing;
- execution visibility should own timing diagnostics;
- cache status is equivalent to elapsed-time measurement;
- `list[tuple[str, float]]` is a repository-wide timing schema;
- diagnostic inventory registration proves timing-label consistency;
- timing work is ready for behavior-changing optimization;
- presentation vocabulary should be promoted into preserved knowledge.

## Recommended first timing slice

The smallest safe next ownership slice is **current-facts cache timing ownership recovery**:

1. Preserve existing CLI flag, report text, timing labels, and cache behavior.
2. Keep `ProjectionBuildDiagnostics` optional and unchanged.
3. Separate the current-facts State-path timing owner from the current-facts report assembly owner.
4. Keep `_CurrentFactsCacheVisibility` as the cache-path explanation boundary or make that boundary more explicit without changing labels.
5. Add characterization tests only if implementation changes are made.

This is safer than starting with projection timing because projection diagnostics already has a coherent local owner, and safer than starting with state-build cache debug because that path also performs summary read-model cache work. Current-facts cache debug is narrower, already registered in diagnostic inventory and shape audit, and visibly contains the same compression pattern the family needs to recover.

## Final answer to acceptance questions

**Who owns timing measurement?**

No single owner. Measurement is owned by local paths: `ProjectionBuildDiagnostics`, state-build cache debug, current-facts cache debug, `_TimingProjectionStore`, `_ReachabilityTimer`, observation ingestion diagnostics, and `ProgressCadence` for cadence only.

**Who owns timing aggregation?**

Aggregation is local to each report/diagnostic payload. Projection diagnostics, state-build cache debug, current-facts cache debug, knowledge reachability metadata, and observation ingestion diagnostics aggregate independently.

**Who owns timing diagnostics?**

Diagnostic ownership is path-specific. Projection diagnostics owns projection construction diagnostics; state-build and current-facts CLI debug paths own their cache/timing diagnostics; knowledge reachability and observation ingestion own their diagnostic timings.

**Who owns timing presentation?**

Formatter functions and CLI consumers own presentation: `format_state_summary_cache_debug_report(...)`, `_format_current_facts_timing_report(...)`, `format_observation_ingestion_diagnostics(...)`, `format_knowledge_reachability_table(...)`, and `CliExecutionStatusConsumer`.

**Where is timing still compressed?**

Most visibly in state-build cache debug, current-facts cache debug, projection finalization diagnostic labeling, and knowledge reachability metadata/report construction.

**What implementation evidence supports those conclusions?**

The evidence is the repeated local use of timing helpers/closures/classes, local timing payload dataclasses, local formatters, and cache/status objects described above. The code shows shared timing grammar without shared timing implementation.

**What is the safest first timing slice that preserves compatibility?**

Recover current-facts cache timing ownership boundaries while preserving behavior: separate State-path timing, cache-path explanation, and report assembly without changing CLI output or timing labels.
