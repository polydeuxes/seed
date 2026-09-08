# Operational timing and preservation recovery 001

## Status

Report-only recovery. This file is repository testimony and is not a canonical Book amendment. It does not change production code, CLI behavior, tests, timing persistence, EventLedger behavior, projection behavior, or cache behavior.

## Central Finding

Seed presently produces several operational timing and resource testimonies, but they are not one coherent operational telemetry system. The current implementation contains:

- transient phase timings rendered by `--current-facts-cache-debug`;
- transient state-build/read-model/cache timings rendered by `--state-build-cache-debug`;
- transient observation ingestion timings rendered by `--observe-timings`;
- projection-build diagnostic timings and counters that are collected in memory and selected into the two debug reports;
- projection and summary cache-status testimony retained in persisted projection-store snapshots, but not elapsed timing samples;
- transient `ExecutionStatus` lifecycle/progress updates;
- ordinary runtime/resource observations emitted as normal `Observation` objects by `SeedRuntimeObservationSource`, which can become EventLedger evidence when collected through the ordinary observation ingestion path.

Seed does not presently retain enough evidence to reconstruct the elapsed timing samples printed by the debug commands after the process exits. It can reconstruct some cache status and projection/read-model dependency boundaries from retained ledger events and projection-store snapshots, but not the original per-run durations. Seed presently has isolated operational measurements, cache diagnostics, and ordinary runtime observations; it does not have an operational timing baseline, tolerance boundary, deviation comparison, regression finding, or baseline transition testimony for these surfaces.

## Repository witnesses examined

Primary implementation witnesses:

- `scripts/seed_local.py`: CLI flags, current-facts timing report, state-build cache-debug evidence/report, observation timing formatter, and command dispatch.
- `seed_runtime/projection_store.py`: `StateCacheStatus`, `project_state_with_cache(...)`, projection snapshot eligibility, cache-hit/miss/incremental replay paths, and state snapshot save path.
- `seed_runtime/state.py`: `ProjectionBuildDiagnostics`, projection replay/finalization timing, and projection counters.
- `seed_runtime/observation_sources.py`: `ObservationIngestionDiagnostics`, `_ObservationIngestionTiming`, `ObservationCollectionService.collect(...)`, `SeedRuntimeObservationSource`, process duration/resource observations, and observation inventory predicate questions.
- `seed_runtime/execution_status.py`: `ExecutionStatus`, `ExecutionStatusConsumer`, recording/CLI/null consumers, `ProgressCadence`, lifecycle/status/progress emission.
- `seed_runtime/fact_index.py`: derived fact-index cache load/build/save status and cache status artifacts.
- `seed_runtime/events.py`: EventLedger append/list/status paths.
- `seed_runtime/operational_surface_inventory.py`: current known operational flags including `--observe-timings`.
- `tests/test_seed_local_script.py`, `tests/test_projection_store.py`, `tests/test_execution_status.py`, `tests/test_runtime_self_observation.py`, `tests/test_observation_inventory.py`, and `tests/test_fact_index.py`: tests preserving current rendered surfaces, cache behavior, status behavior, and runtime observation predicates.

Historical/testimony documents inspected as secondary witnesses:

- `docs/execution_timing_adversarial_audit.md`
- `docs/execution_visibility_investigation.md`
- `docs/execution_concepts_implementation_investigation.md`
- `docs/execution_status_measurement_implementation_audit.md`
- `docs/execution_status_producer_contract_reconciliation.md`
- `docs/runtime_self_observation_investigation.md`
- `docs/self_observation_ordinary_domain_reconciliation.md`
- `timing_visibility_current_facts_completion_audit.md`
- `history_projection_bridge_pressure_audit.md`
- `incremental_state_evolution_architecture_investigation.md`

## Timing producer and artifact inventory

| Surface / artifact | Operation being measured | Operation-instance identity | Phase boundaries | Clock / measurement method | Context captured | Producer | Artifact produced | Consumer | Retained? | EventLedger? | Projection/cache/diagnostic structure? | Reproducible from retained evidence? | Lawful assertion | Stronger assertion not supported |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CurrentFactsTimingReport` via `--current-facts-cache-debug` | Current-facts/current-selection read-only State path plus rendering path | CLI invocation, workspace, optional `--db`, optional current-selection subject/predicate; no durable run id | ledger open, projection store open, projector construction, cache path or full rebuild, read-model build or fact-index build/load, query/filter/render, stdout placeholder, total | `time.perf_counter()` in `_current_facts_timing_from_args(...)`; cache-store wrapper also uses `time.perf_counter()` | cache availability/status, state-cache label, selected projection diagnostic timings, rendered output | `_current_facts_timing_from_args(...)`, `_TimingProjectionStore`, `project_state_with_cache(...)`, `ProjectionBuildDiagnostics` | `CurrentFactsTimingReport` with visibility output and diagnostic cache/timings | `_format_current_facts_timing_report(...)`, CLI stdout, tests | Transient only | No | In-memory report/diagnostic payload; may consult persisted state and fact-index caches | Durations no; cache status may be recomputed for current ledger/cache state, not for the old run | This invocation took measured elapsed times for listed local phases and observed cache hit/miss/unavailable status | Ordinary behavior, baseline, future duration, correctness, or changed regime |
| `StateSummaryCacheDebugReport` via `--state-build-cache-debug` | State-build summary/read-model cache boundary, projection cache boundary, projection replay/build, summary derivation, rendering | CLI invocation, workspace, optional `--db`; current and cached last-event ids in report; no durable run id | projection store open, ledger open, event listing/current last event lookup, summary snapshot lookup/decode, state cache lookup/decode, projector construction, projection replay/build, fact-support count, compact/operator summary derivation, summary snapshot save, rendering, total runtime; projection subphases separately | `time.perf_counter()` in local `timed(...)`; `ProjectionBuildDiagnostics.timed(...)` uses `time.perf_counter()` | cache eligibility and reason, summary/state cache statuses, current/cached event ids, notes, projection counters, summary-source/published evidence internally | `_state_build_cache_debug_evidence_from_args(...)`, `_StateBuildCacheDebugTimingEvidence`, `ProjectionBuildDiagnostics`, `project_state_with_cache(...)` | `_StateBuildCacheDebugEvidence`, `StateSummaryCacheDebugReport` | `format_state_summary_cache_debug_report(...)`, CLI stdout, tests | Timings transient; summary/state snapshots retained when saved | No direct timing event; summary snapshot save writes projection store, not EventLedger | In-memory report; persisted projection and summary snapshots are cache/projection structures | Durations no; cache statuses and dependency identity can be recomputed for retained current state/cache, not the old elapsed sample | This invocation observed cache eligibility/status/event ids and measured listed phase durations | Baseline, regression, failure, or projection correctness solely from hit/miss/timing |
| `ProjectionBuildDiagnostics` | Projected-State construction subphases | Invocation-local diagnostic object; no durable run id | projection input event materialization, event replay, full projection rebuild, cached projection load/materialize, plus apply/finalize subphase timings where instrumented | `time.perf_counter()` in `ProjectionBuildDiagnostics.timed(...)` | timing name/value pairs; counters such as projection events and event kind counts | `StateProjector.project(...)`, `StateProjector.project_from_state(...)`, `project_state_with_cache(...)`, callers that pass diagnostics | In-memory `ProjectionBuildDiagnostics.payload` selected by `_ProjectionDiagnosticSelection` | Current-facts and state-build debug reports | Transient unless selected into a transient report | No | In-memory diagnostic structure | Counters may be derivable from ledger events; elapsed timings are not | This projection build invocation spent measured time in instrumented subphases and processed counted event kinds | Projection correctness, baseline, deviation, or future performance |
| `StateCacheStatus` | Cache reuse outcome of `project_state_with_cache(...)` | Workspace, projection name/version, current/snapshot last-event ids | cache snapshot load/materialize, exact last-event match, stale snapshot incremental replay, full replay fallback, snapshot save | No elapsed clock in the dataclass; statuses arise from ledger/cache identity comparison | `cache_hit`, `projection_version`, `snapshot_last_event_id`, `current_last_event_id`, `incremental_replay`, `events_applied` | `project_state_with_cache(...)` | State-cache status dataclass returned to caller | CLI helpers, tests, possible callers | Return value transient; underlying snapshot retained if saved | No | Projection-store snapshot; status object is transient | Yes for current cache/ledger status; no for the historical returned object unless separately recorded | Whether this cache invocation hit, missed, replayed incrementally, and how many events were applied | Operation correctness, timing, baseline, failure, or regime change |
| State-summary cache diagnostics | Dependent read-model cache lookup/build/save for operator state summary | Workspace, summary projection name/version, state projection version, state last event id | summary snapshot lookup, decode/payload reconstruction, constructed read model derivation, summary snapshot save | `time.perf_counter()` for report phases; persisted snapshot has created-at and dependency identity but not elapsed | summary cache hit/miss/unavailable, current/cached summary last-event ids, summary-source, publication evidence internally | `_state_build_cache_debug_evidence_from_args(...)`; state-build path also saves/loads summaries | `SummaryProjectionSnapshot` and transient debug report | `--state-build`, `--state-build-cache-debug` | Snapshot retained; timing transient | No | Projection-store summary snapshot; transient report | Snapshot and dependency identity yes; elapsed timing no | Whether a summary snapshot satisfied/build was keyed to a state boundary | That the summary is canonically true independent of ledger/projection authority, or that elapsed time is ordinary |
| Observation ingestion diagnostics via `--observe-timings` | Observation source collection, normalization, event generation plus ledger write | Source name, workspace, CLI invocation; no durable diagnostic run id | source collection, normalization, ingestion/event write, total | `time.perf_counter()` in `_ObservationIngestionTiming` | source name, total observations, total events, facts promoted, source counters, observations/sec, events/sec | `ObservationCollectionService.collect(...)` when caller passes diagnostics list | `ObservationIngestionDiagnostics` list | `format_observation_ingestion_diagnostics(...)`, CLI stdout, tests | Transient list/output; underlying observations/facts/events may be retained when `--record` is used | Timings no; observation/fact events yes when recording ingestion | In-memory diagnostic list | Counts may be partly reconstructable from EventLedger; elapsed durations and source counters not guaranteed | This ingestion invocation produced measured phase durations and throughput counters | Performance baseline, failure, outlier, or expected future ingestion speed |
| `ExecutionStatus` / `ExecutionStatusConsumer` | Activity lifecycle and progress status, not timing testimony | Phase/message/current/total/completed within current operation; no durable run id | producer-chosen status phases and progress cadence | `ProgressCadence` uses `time.monotonic()` only to decide emission cadence, not to measure operation duration | phase, message, current, total, completed | `emit_status(...)`, `ExecutionStatusEmitter`, lifecycle helpers in observation/projection/event/cache paths | `ExecutionStatus` payloads | CLI stderr, recording tests, null consumer | Transient unless a test recording consumer holds in memory | No | No projection/cache persistence | No after process exit | An operation reached a producer-declared status/progress boundary while a consumer was attached | Timing, success/failure by itself, retained knowledge, baseline, or correctness |
| `SeedRuntimeObservationSource` / `seed_runtime_duration_seconds` | Current Seed process/runtime/resource state | Subject default `Seed`, process id, observed_at, optional start monotonic value | One observation collection sample | `time.monotonic()` delta for runtime duration; `/proc/<pid>/status` for memory/thread count; file stat for configured DB/ledger sizes | observation metadata: collector, source, read-only/local-only, mutates_cluster=false, process id, predicate-specific source/field | `SeedRuntimeObservationSource.collect()` | ordinary `Observation` objects | Observation ingestion service, inventory, tests; may be recorded as evidence/facts | Retained only if ingested/recorded through ordinary observation path; otherwise transient | Yes when ordinary observation ingestion records observations/events | Ordinary observation/fact/projection path, not timing diagnostic cache | Yes if recorded as events; no if collected but not recorded | At observed time, the Seed subject/process had the measured runtime/resource value | Operational phase timing, command latency, baseline, deviation, or future duration |
| Fact-index cache timing/status | Derived current-facts index load/build/save path | Workspace, state last event id/projection version, derived-index identity | fact-index cache lookup/load, build, save | `_TimingProjectionStore` uses `time.perf_counter()` in current-facts debug; status emission in `fact_index.py` | cache hit/miss messages; derived index snapshot when persisted | `load_or_build_fact_index(...)`; `_TimingProjectionStore` wrapper | derived index snapshot and/or transient timing line | current-facts timing report, CLI/tests | Snapshot retained; timing transient | No | Projection-store derived-index snapshot | Snapshot yes; elapsed timing no | Whether fact-index cache was used/built in current invocation | Current-facts correctness, baseline, or performance regression |
| Cache snapshots and rebuild paths | Projection/read-model/derived-index materialization and reuse, not elapsed behavior | Workspace, projection names/versions, last-event ids, cache boundary metadata | load snapshot, validate, materialize, replay tail/full, save snapshot; explicit rebuild clears/rebuilds | Snapshot metadata uses timestamps/identity; debug paths may time adjacent operations | projection payloads, last-event ids, mutates_cluster boundary, created_at, dependency identity | `ProjectionStore`, `project_state_with_cache(...)`, state-build/fact-index helpers | persisted snapshots | later cache users and debug reports | Retained until cleared/replaced | No | Projection-store cache | Yes for derived artifact content/status at current boundary; not for old timings | Derived State/read-model/index can be rebuilt or reused against ledger boundary | Elapsed performance baseline or correctness beyond cache validity conditions |

## Producer → artifact → consumer topology

### Current-facts timing path

`_current_facts_timing_from_args(...)` performs work, measures work, interprets cache status, constructs a report, and leaves presentation to `_format_current_facts_timing_report(...)`. Its local `timed(...)` helper appends elapsed seconds for orchestration phases, while `_TimingProjectionStore` measures projection-store cache calls. When cache use is possible, it also calls `project_state_with_cache(...)` with a `ProjectionBuildDiagnostics` instance, interprets `StateCacheStatus`, and appends selected projection diagnostic timings. The only downstream consumer is formatting/printing or tests. The elapsed samples are not written to the EventLedger or projection store.

### State-build cache debug path

`_state_build_cache_debug_evidence_from_args(...)` collects separate cache evidence, projection evidence, read-model evidence, and timing evidence, then assembles a `StateSummaryCacheDebugReport`. It both reads persisted projection/summary snapshots and may save a summary snapshot, but the timing values are only in the report path. Projection diagnostics are nested subphase testimony, not persisted projection knowledge.

### Projection cache path

`project_state_with_cache(...)` produces a projected `State` and a transient `StateCacheStatus`. Its retained artifacts are projection snapshots saved through the projection store, not elapsed timings. The status is an invocation-local interpretation of ledger/cache identity: exact hit, incremental replay, or full rebuild/miss.

### Observation ingestion path

`ObservationCollectionService.collect(...)` builds `_ObservationIngestionTiming`, measures collection/normalization/ingestion phases, and appends `ObservationIngestionDiagnostics` only when the caller supplied a diagnostics list. `--observe-timings` renders that list. Observation facts/events may be persisted by the ordinary record path, but the diagnostic timing list is not itself recorded.

### Execution status path

`emit_status(...)` and `emit_progress_if_due(...)` construct `ExecutionStatus` payloads for attached consumers. `CliExecutionStatusConsumer` renders them to stderr, `RecordingExecutionStatusConsumer` stores them only in process memory, and `NullExecutionStatusConsumer` ignores them. Status emission is operational visibility, not preserved timing evidence.

### Runtime self-observation path

`SeedRuntimeObservationSource.collect()` produces ordinary observations for process memory, thread count, runtime duration, and configured database/ledger file sizes. These can enter the ordinary observation ingestion/EventLedger path. This is Seed-observed runtime/resource testimony, not a diagnostic timing report.

## Transient / retained / projected / rebuildable matrix

| Artifact | Transient | Retained | Projected | Rebuildable | Classification |
| --- | --- | --- | --- | --- | --- |
| Current-facts phase timing values | Yes | No | No | No | Non-rebuildable transient measurement |
| Current-facts rendered report | Yes | No | No | No | Diagnostic output only |
| Current-facts visibility output | Yes | No as a report; derived from retained/current State when rerun | Read-model rendering from projected State | Partly, if ledger/cache state remains compatible | Re-renderable presentation, not preserved timing |
| State-build cache-debug phase timing values | Yes | No | No | No | Non-rebuildable transient measurement |
| State-build cache-debug cache status/event ids | Yes as report | Underlying snapshots/event ledger retained where present | Cache/projection structures | Recomputable for current retained boundary, not historical invocation | Cached projection of retained evidence plus transient report |
| ProjectionBuildDiagnostics timings | Yes | No | No | No | Non-rebuildable transient measurement |
| ProjectionBuildDiagnostics counters | Yes | No | No | Partly from ledger events for event counts/kinds | Compressed invocation summary whose source may be retained but selection context is transient |
| `StateCacheStatus` return value | Yes | No | No | Partly from ledger/cache snapshots at current boundary | Transient cache-status testimony backed by retained artifacts |
| Projection snapshots | No, if persisted | Yes | Yes | Yes from EventLedger, assuming projection implementation available | Cached projection of retained evidence |
| Summary snapshots | No, if persisted | Yes | Yes | Yes from projected State/EventLedger, assuming implementation available | Cached dependent projection/read-model |
| Derived fact-index snapshots | No, if persisted | Yes | Yes | Yes from projected State/EventLedger, assuming implementation available | Cached derived index |
| Observation ingestion timings | Yes | No | No | No | Non-rebuildable transient measurement |
| Observation/fact events from recording | No | Yes | Yes | Replayable | Retained operation evidence, but not timing diagnostic samples |
| `ExecutionStatus` updates | Yes | No | No | No | Transient status/lifecycle emission |
| Runtime/resource observations collected but not recorded | Yes | No | No | No | Ordinary runtime observation discarded after collection |
| Runtime/resource observations recorded | No | Yes | Yes as ordinary facts/observations | Yes from EventLedger replay | Ordinary runtime observation |

## Preservation-loss analysis

The preservation principle separates derived artifacts from evidence that cannot be reconstructed.

### Derived artifacts that need not be preserved when retained evidence remains

- Persisted projection snapshots are rebuildable from EventLedger history and projection code. Discarding a projection snapshot loses cache warmth and the exact saved snapshot artifact, but not the underlying ledger-supported State understanding.
- Persisted summary snapshots are rebuildable from projected State and state-summary construction. Discarding a summary snapshot loses a read-model cache and its created-at/cache artifact, but not the State-supported summary content if source ledger and projection code remain.
- Derived fact-index snapshots are rebuildable from projected State. Discarding them loses lookup acceleration and cache-status continuity, but not the underlying facts.

### Artifacts whose loss erases timing testimony

- Current-facts phase durations, state-build phase durations, observation ingestion phase durations, projection diagnostic elapsed subphase timings, throughput values derived from those timings, and `ExecutionStatus` emission timing cadence are non-rebuildable after process exit because Seed does not retain their samples or associate them with a durable operation-instance identity.
- Discarding those transient measurements erases only testimony that the specific invocation took those measured times in those producer-defined phases. It does not erase the ledger facts, projected State, cache snapshots, or ordinary domain knowledge.
- However, because no retained timing series exists, discarding every transient timing output also prevents later reconstruction of ordinary operational behavior, material deviation, or changed baseline from these diagnostics. The loss is not just UI loss; it is loss of the only current evidence for that invocation's operational duration.

### Diagnostic output only

Rendered debug text is a presentation artifact. If the in-memory diagnostic values are gone and no external operator captured stdout/stderr, Seed cannot later consume the text. Diagnostic rendering is therefore not Seed-consumable knowledge unless separately recorded outside the present implementation.

### Ordinary runtime observations

`SeedRuntimeObservationSource` is the exception: its runtime duration/resource samples are ordinary observations. If collected through a recording ingestion path, the observation/fact events preserve the sample and can be replayed/projected. If merely collected and rendered/used transiently, the sample is lost.

## Baseline / tolerance / deviation vocabulary recovery

Search terms included timing, duration, elapsed, latency, throughput, baseline, tolerance, threshold, deviation, outlier, regression, performance, ordinary behavior, expected duration, historical range, and changed regime.

| Concept | Status | Evidence and boundary |
| --- | --- | --- |
| Individual operational measurements | Present | Debug reports and observation ingestion diagnostics collect individual elapsed samples; runtime self-observation can collect `seed_runtime_duration_seconds`. |
| Retained series of operational timing measurements | Absent | Debug timing samples are not recorded to EventLedger/projection store; runtime observations can be retained as ordinary observations, but they are process-duration/resource samples, not command phase timing series. |
| Summary/snapshot of ordinary operational behavior | Absent | Cache snapshots summarize derived State/read-model/index payloads, not timing distributions or ordinary durations. |
| Comparison boundary or tolerance for timing | Absent | No inspected timing/debug path compares elapsed duration to a tolerance, expected duration, threshold, or historical range. Existing thresholds in repository documents/tests concern other concepts and do not establish operational timing tolerance. |
| Deviation/outlier/regression testimony | Absent | No current producer emits an out-of-tolerance, regression, outlier, or material-deviation artifact for operation timing. |
| Baseline transition testimony / changed operating regime | Absent | No retained operational timing baseline exists, so no transition from ordinary behavior to a new operating regime is represented. |
| Cache correctness/eligibility boundaries | Present | Projection/read-model cache statuses use version/last-event/mutates_cluster eligibility. This is cache validity testimony, not timing baseline testimony. |
| Throughput counters | Present transiently | Observation ingestion diagnostics compute observations/sec and events/sec from current invocation timings. These are individual-run rates, not a retained baseline. |
| Runtime resource observations | Present/Partial | Runtime duration/memory/thread/file-size observations are present and can be retained if ingested/recorded. They do not by themselves define ordinary behavior or deviations. |

To establish a baseline without prescribing implementation, Seed would need retained operation-instance measurements with stable identity, comparable context, and an explicit comparison authority or accepted reference range. Existing single-run timings and cache diagnostics are insufficient because they lack retained series, baseline selection, tolerance, and transition testimony.

## Current Seed-consumption findings

Current timing artifacts are not used by Seed to alter later lawful movement.

- Seed measures and immediately discards: current-facts timings, state-build debug timings, projection diagnostic timings, observation ingestion timings unless an external operator captures output.
- Seed measures and renders externally: `--current-facts-cache-debug`, `--state-build-cache-debug`, and `--observe-timings`.
- Seed retains a diagnostic artifact: not for these timing diagnostics. Projection/summary/fact-index snapshots are retained cache artifacts, but elapsed timing samples are not.
- Seed projects retained timing evidence: only ordinary runtime observations can be projected if ingested as observations. The diagnostic timing reports are not projected.
- Seed can use timing evidence to constrain later selection, budget, stopping, capability, or reachability decisions: no present consumer was found. Cache hit/miss can affect whether work is reused/rebuilt, but that decision is based on identity/eligibility, not elapsed timing evidence. `ProgressCadence` uses elapsed wall-clock intervals only to decide whether to render a progress update, not to decide lawful movement.

## Compression analysis for `--current-facts-cache-debug`

`--current-facts-cache-debug` is a compressed witness, not a single responsibility. It presently combines:

| Responsibility | Present? | Belongs to measured operation or presentation? | Evidence boundary |
| --- | --- | --- | --- |
| Fact-support inventory rendering | Present in standalone form | Measured operation/read-model presentation | With no `--current-selection`, it builds fact views and renders `format_fact_views(...)`. |
| Current-selection rendering | Present in filtered form | Measured operation/read-model presentation | With `--current-selection SUBJECT PREDICATE`, it calls `format_current_facts(...)` for selected values. |
| State projection timing | Present | Measured operation | It times full projection rebuild or cache-backed state path. |
| Cache-path timing | Present | Measured operation/cache diagnostics | It times projection-store load/save methods through `_TimingProjectionStore` and outer state-cache path. |
| Projection diagnostic subphase timing | Present when cache path supplies diagnostics | Measured operation/projection diagnostics | It consumes `ProjectionBuildDiagnostics.payload` through `_CurrentFactsTimingInterpretation`. |
| Fact-index timing | Present in filtered form | Measured operation/cache/read-model support | It times `fact-index build/load` for current-selection lookup support. |
| Render timing | Present | Presentation timing | It times `render` or `query/filter + render`. |
| Stdout timing | Present only as placeholder | Presentation artifact, not actual stdout measurement | It appends `("stdout/output time", 0.0)`, so it does not measure actual write time. |
| Cache-state testimony | Present | Diagnostic/cache evidence | It reports `hit`, `miss`, or `unavailable` derived from `StateCacheStatus` or cache eligibility. |
| Total runtime | Present | Whole command-path measurement | It appends `total` from local start time. |

Standalone and filtered forms measure constitutionally different operational subjects:

- Standalone `--current-facts-cache-debug` measures full fact-view read-model build plus fact-view rendering after State projection/cache work.
- Filtered `--current-facts-cache-debug --current-selection SUBJECT PREDICATE` measures the current-selection path, including optional fact-index build/load and query/filter/render for a particular subject/predicate.
- Both share ledger/store/projector/cache-path timing, but the post-State operation differs. Therefore their elapsed values are not interchangeable samples of one operation without additional identity/context.

## Recovered distinctions

| Distinction | Finding | Repository evidence |
| --- | --- | --- |
| execution status != operation timing testimony | Accepted | `ExecutionStatus` carries phase/message/count/completed; elapsed clocks are absent from the payload. Progress cadence uses time only for throttling emission. |
| operation timing testimony != performance baseline | Accepted | Timing reports contain single-run elapsed values and no retained comparison range or baseline authority. |
| performance baseline != predicted future duration | Accepted | No performance baseline exists; even if one did, the repository contains no prediction artifact for future duration. |
| out-of-tolerance observation != operation failure | Accepted as a required boundary; currently no out-of-tolerance operational timing observation exists | The absence of timing tolerance/deviation means no timing sample presently establishes failure. Cache misses and slow timings are diagnostic observations only. |
| cache hit or miss != operation correctness | Accepted | Cache status follows projection/version/last-event/eligibility paths. A miss triggers rebuild/replay; it is not treated as incorrectness. |
| one slow sample != changed operational regime | Accepted | No retained series, baseline, or transition authority exists; one sample can only testify about that invocation. |
| diagnostic rendering != Seed-consumable knowledge | Accepted | Debug reports are formatted to stdout; no current path records them into EventLedger or projections for later decisions. |
| rebuildable projection != preserved understanding | Qualified | For State/read-model content, rebuildable projection means the understanding can survive cache loss if EventLedger and code remain. For timing samples, there is no retained evidence to rebuild elapsed duration, so discarding transient timing erases that operational testimony. |

## What is Present / Partial / Absent / Unknown

### Present

- Individual timing samples for current-facts, current-selection/fact-index, state-build cache-debug, projection-build subphases, and observation ingestion.
- Cache status testimony for projection cache, summary/read-model cache, and fact-index cache.
- Projection/read-model/index snapshots that are retained cache artifacts and mostly rebuildable from ledger/projected State.
- Execution lifecycle/progress visibility as transient status messages.
- Runtime duration and resource observations as ordinary observation-source outputs.
- Tests preserving major rendered timing/status surfaces and runtime observation predicates.

### Partial

- Operation-instance identity: present only as invocation context, workspace, source name, subject/predicate, current/cached event ids, process id, or source name. There is no durable diagnostic run id for debug timing samples.
- Rebuildability: cache-derived State/read-model/index artifacts are rebuildable; elapsed timing samples are not.
- Retained runtime observations: possible through ordinary observation recording, but not automatic for diagnostic timings.
- Throughput: present for an observation ingestion invocation, absent as retained trend/baseline.

### Absent

- Retained diagnostic timing series.
- Operational timing baseline.
- Expected duration, tolerance, threshold, or historical range for these operations.
- Outlier/regression/deviation artifact for timing.
- Baseline transition or changed-operating-regime testimony.
- Seed consumer that uses timing evidence to constrain later selection, stopping, budget, reachability, capability, or refusal decisions.
- EventLedger recording of debug timing artifacts.

### Unknown

- Whether external operators preserve stdout/stderr timing reports outside Seed.
- Whether future canonical Book reconciliation should promote any of these transient diagnostic samples into preserved operational evidence.
- Whether all historical report vocabulary aligns with current post-PR-1893 implementation after future refactors; this recovery privileges current implementation evidence.

## Required conclusions

### What operational timing artifacts presently exist?

`CurrentFactsTimingReport`, `StateSummaryCacheDebugReport` timing fields, `ProjectionBuildDiagnostics`, `ObservationIngestionDiagnostics`, `ExecutionStatus` progress/lifecycle visibility, fact-index/cache wrapper timings inside current-facts debug, and ordinary runtime/resource observations including `seed_runtime_duration_seconds`.

### Which are transient, retained, projected, or rebuildable?

Debug elapsed timings and execution statuses are transient and non-rebuildable. Projection, summary, and fact-index snapshots are retained/projected/cache artifacts and rebuildable from retained evidence if ledger history and projection code remain. Runtime/resource observations are transient unless ingested/recorded; when recorded, they become retained/projectable ordinary observations.

### Does Seed presently retain enough evidence to reconstruct its timing understanding after the process exits?

No for diagnostic timing reports and status/progress emission. Seed can reconstruct cache-status conditions and projected/read-model content from retained EventLedger/cache artifacts, but it cannot reconstruct the elapsed seconds originally measured by current-facts, state-build, projection diagnostics, or observation-ingestion timing after the process exits unless the operator captured output externally.

### Does Seed presently possess an operational baseline, or only isolated measurements and cache diagnostics?

Only isolated measurements, transient throughput counters, cache diagnostics, and ordinary runtime/resource observations. No operational timing baseline is presently implemented.

### Is any current tolerance or deviation comparison performed?

No current tolerance, threshold, outlier, regression, material-deviation, or changed-baseline comparison was found for operational timing surfaces.

### Does Seed consume timing evidence when selecting or refusing later movement?

No present consumer was found that uses timing evidence to constrain later selection, budget, stopping, capability, reachability, or refusal decisions. Cache reuse/rebuild decisions use identity and eligibility, not elapsed timing.

### What understanding would be lost if current transient measurements were discarded?

Seed would lose the only in-process evidence that a specific invocation spent specific elapsed time in named phases, including projection subphases and observation ingestion phases. It would not lose ledger facts, projected State, or cache contents. It would lose the possibility of later deriving ordinary behavior, deviations, or baseline transitions from those samples because no retained timing series exists.

### Which responsibilities are compressed inside `--current-facts-cache-debug`?

It compresses fact-support inventory rendering, current-selection rendering, State projection timing, cache-path timing, projection diagnostic subphase timing, fact-index timing, render/query timing, stdout placeholder timing, cache-state testimony, and total runtime into one operator-facing command. Standalone and filtered forms share some setup/cache measurement but measure different post-State subjects.

### What is the smallest next coherent step: Book reconciliation, another report, or a bounded implementation recovery?

The smallest coherent next step is Book reconciliation, not implementation recovery. This topology recovery finds conceptual mismatch and missing preservation/baseline semantics rather than a narrowly failing command. Before adding persistence, CLI seams, EventLedger events, or baseline artifacts, the canonical Book should reconcile whether operational timing testimony is knowledge Seed should preserve, when transient diagnostics may remain disposable, and what authority would distinguish a timing sample from ordinary behavior, deviation, or changed baseline.

## Smallest coherent next step

Book reconciliation should explicitly decide the preservation status of operational timing testimony. The implementation should not yet add a timing database, EventLedger timing events, CLI flags, a universal timing class, or baseline/deviation artifacts, because the recovered topology shows multiple distinct witnesses with different preservation properties and no current authority selecting one preservation rule for all of them.

## One bounded unresolved question

When an operator invokes a diagnostic timing surface and does not record it, is Seed allowed to treat the elapsed sample as intentionally disposable presentation, or must the sample be considered operational testimony whose loss erases the only evidence of that operation instance?
