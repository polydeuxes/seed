# Execution Concepts Implementation Investigation

This investigation is documentation-only. It does not rename phases, normalize vocabulary, add diagnostics, alter projection/cache behavior, or change runtime behavior. It preserves implementation-backed findings about the execution concepts that already exist in Seed.

## Implementation summary

Seed already preserves multiple implementation-backed execution concepts, but they are not one universal execution model. The concepts are owned by distinct implementation responsibilities: event replay into projected state, reusable projection snapshots, dependent read-model snapshots/indexes, surface-local timing/debug reports, knowledge-reachability audit evaluation, observation ingestion, runtime trace reconstruction, transient execution status, and audit-snapshot policy/comparison visibility.

The repository evidence supports a layered model for selected paths: dispatch/CLI routing invokes owners; owners read append-only events or observations; projection builds `State`; projection store may reuse snapshots; dependent builders derive read models; formatters render output; execution status may expose transient progress; runtime trace reconstructs historical runs from events. The implementation does not support collapsing all terms into one phase vocabulary.

## Execution concepts recovered

### 1. Append-only event history

**Implementation responsibility:** preserve the historical event stream that projection, runtime trace, and read-only views consume.

**Boundary:** event history is the authority; derived state and traces read from it. Projection-store code states that ledgers own append-only historical events while projection stores own reusable snapshots derived from those events.

**Evidence:** `projection_store.py` declares this boundary in the module docstring and imports `EventLedger` as the source for cache-backed state projection. `runtime_trace.py` reconstructs a run by listing events from a read-only event API.

### 2. State projection / event replay

**Implementation responsibility:** build projected `State` from ledger events and rebuild derived indexes.

**Boundary:** `StateProjector.project()` creates a new `State`, lists workspace events, and calls `project_from_state()` with status phase `projection_replay`. `project_from_state()` materializes events, applies each event to state, emits progress if requested, and calls `finalize()` to rebuild projection indexes. This is not rendering and not cache storage.

**Evidence:** `StateProjector.project()` and `project_from_state()` own event replay into state and finalization. `finalize()` explicitly rebuilds derived projection indexes after event application.

### 3. Projection build diagnostics

**Implementation responsibility:** optionally time and count subparts of projected-State construction.

**Boundary:** `ProjectionBuildDiagnostics` stores optional, non-authoritative timings and counters. Callers may render or merge these values, but they do not define projection truth.

**Evidence:** the dataclass docstring calls the timings optional and non-authoritative. The projector records `projection input event materialization`, `projection events`, per-kind projection event counts, `event replay`, and finalization subphases when diagnostics are supplied.

### 4. Projection cache / projection store

**Implementation responsibility:** save and load reusable projected-state snapshots derived from events.

**Boundary:** `ProjectionStore` owns snapshots, not event history. `project_state_with_cache()` checks snapshots, returns exact cache hits, incrementally replays events after a compatible snapshot, or falls back to full projection replay and saves a snapshot.

**Evidence:** `ProjectionStore` has load/save/clear APIs for state snapshots and dependent summary/index snapshots. `project_state_with_cache()` emits projection-cache status, attempts cached materialization, returns hit status with `events_applied=0`, performs incremental replay when possible, and otherwise performs full projection rebuild.

### 5. Projection cache status / path metadata

**Implementation responsibility:** describe which projection-cache path occurred.

**Boundary:** `StateCacheStatus` is the structured result from cache-backed projection. It is separate from timings and separate from the `State` payload. It records hit/miss, projection version, snapshot/current event ids, incremental replay, and events applied.

**Evidence:** `project_state_with_cache()` returns `StateCacheStatus` for hit, incremental replay, and full rebuild paths with distinct field values.

### 6. Dependent read-model caches

**Implementation responsibility:** cache derived read-models that depend on a specific state projection identity.

**Boundary:** `SummaryProjectionSnapshot` and `DerivedIndexSnapshot` include `state_projection_version` and `state_last_event_id`. The store only returns them when these match the caller's state projection identity. They are not the primary state projection cache.

**Evidence:** the protocol exposes `load_summary_snapshot()` and `load_derived_index_snapshot()` with required `state_projection_version` and `state_last_event_id` parameters, and in-memory implementations reject mismatches.

### 7. State-build cache debug

**Implementation responsibility:** measure the state-summary/read-model cache boundary for the `--state-build-cache-debug` surface.

**Boundary:** this surface times projection-store open, ledger open, event listing/current last-event lookup, summary snapshot lookup/decode, state cache lookup/decode, projector construction, projection replay/build, summary derivation, snapshot save, rendering, and total runtime. It also renders projection diagnostics when a projection build occurs. It does not ingest observations or execute tools.

**Evidence:** `state_summary_cache_debug_from_args()` says it measures the state-build cache boundary without ingesting or executing tools and constructs a `StateSummaryCacheDebugReport` with command-local timings, projection timings, counters, cache eligibility, and notes.

### 8. Current-facts cache debug / timing

**Implementation responsibility:** measure the `--current-facts` state path, including projection cache, fact-index cache, read-model build, query/filter, and render.

**Boundary:** this is a current-facts-specific timing surface. It wraps projection-store operations with `_TimingProjectionStore`, reports cache path labels from `StateCacheStatus`, appends projection diagnostics, and separately times read-model build or fact-index build/load plus query/filter/render. It is not identical to state-build cache debug even though both use projection cache.

**Evidence:** `_current_facts_timing_from_args()` builds a read-only timing report for the current-facts State path, with separate labels for cache hit, incremental replay miss, full rebuild miss, full rebuild without cache, read-model build, render, fact-index build/load, query/filter + render, stdout/output time, and total.

### 9. Knowledge reachability audit execution

**Implementation responsibility:** evaluate candidate knowledge reachability across preserved, projected, read-model, inquiry, and rendered stages with audit metadata.

**Boundary:** knowledge reachability owns its own timer, metadata, candidate counts, scan counts, cache metadata, indexes, render timing, and total timing. Its `load_state/cache` terminology is surface-local to the audit path and is not identical to projection replay or state-build debug.

**Evidence:** `KnowledgeReachabilityMetadata` stores timings, candidate counts, kind/loss counts, algorithmic counters, candidate sources, scan counts, cache data, and index timings. `_ReachabilityTimer` records named phases and progress messages, and the audit writes `render` and `total` timings into metadata.

### 10. Observation ingestion

**Implementation responsibility:** collect observations, normalize them, ingest them as events/facts, and optionally report comparable timing counters.

**Boundary:** observation ingestion begins with a source's `collect()`, normalizes observations, optionally uses current state during normalization, then writes through `ObservationIngestor`. It exposes source collection, normalization, event-generation plus ledger-write, total, observation/event counts, facts promoted, and source counters. It is not projection rendering, though normalization may call `StateProjector` when a normalization pipeline is present.

**Evidence:** `ObservationIngestionDiagnostics` defines these counters. `ObservationCollectionService.collect()` times collection, normalization, ingestion, and appends diagnostics. The CLI prints them only when observation paths pass `--observe-timings`.

### 11. Runtime trace

**Implementation responsibility:** reconstruct one recorded runtime run from append-only events without replaying or mutating it.

**Boundary:** runtime trace is historical and ledger-backed. It snapshots matching events, identifies user input, decision, policy, tool, assistant, and error events, and builds a summary. It is not transient execution status and not projection-cache timing.

**Evidence:** `runtime_trace.py` states read-only runtime trace reconstruction from append-only events; `RuntimeTraceReader.trace()` lists matching events and returns a `RuntimeTrace` with event snapshots and summary.

### 12. Execution status

**Implementation responsibility:** emit transient, renderer-independent activity visibility to consumers.

**Boundary:** execution status is not event history, not projection truth, not cache authority, and not a timing record. Producers emit phase/message/current/total/completed updates; consumers render or record them.

**Evidence:** `ExecutionStatus` is described as renderer-independent, non-authoritative activity visibility. `ExecutionStatusConsumer` consumes status without owning execution state. CLI and recording consumers expose it differently.

### 13. Audit snapshots, snapshot policy, and snapshot comparison

**Implementation responsibility:** preserve and inspect local audit-snapshot evidence and comparison availability for supported audit snapshot kinds.

**Boundary:** audit snapshots and snapshot policy are separate from projection-store snapshots. Snapshot policy reports repository context, snapshot kinds, comparison availability, recommendations, constrained surfaces, and explicitly declares no event-ledger writes or cluster mutation.

**Evidence:** `SnapshotPolicyAudit` contains repository context, snapshot kind policies, comparison availability, recommendations, operational surfaces, `writes_event_ledger=False`, and `mutates_cluster=False`.

### 14. Formatting / output rendering

**Implementation responsibility:** convert already-built reports/read models into CLI text.

**Boundary:** formatting functions render local report data. They do not own projection, cache reuse, event replay, observation collection, or runtime trace reconstruction. Some timing surfaces measure rendering (`render`, `rendering`, or `query/filter + render`) with different boundaries.

**Evidence:** state-build debug times a placeholder `rendering`; current-facts timing measures `render` for all-facts output and `query/filter + render` for filtered output; knowledge reachability records a `render` phase after evaluation.

## Execution terminology matrix

| Current term | Implementation concept | Implementation boundary | Surfaces exposing it | Evidence |
| --- | --- | --- | --- | --- |
| `projection` | State projection / event replay | Apply ledger events into `State` and finalize derived indexes | Architecture docs, `StateProjector`, state views | `StateProjector.project()` / `project_from_state()` |
| `projection replay` | State projection / event replay | Status phase and message while replaying events | execution status from projector/cache path | `status_phase="projection_replay"` and emitted progress |
| `event replay` | Projection build diagnostics subphase | Timed loop applying events during projection | `ProjectionBuildDiagnostics` consumers | diagnostics label in `project_from_state()` |
| `projection replay / build` | Surface-local combined projection path | One state-build debug timing wrapper around cache-backed or direct projection | `--state-build-cache-debug` | `state_summary_cache_debug_from_args()` |
| `full projection rebuild` | Projection-cache miss path | Build state from all events and save snapshot | `project_state_with_cache()`, current-facts timing | cache fallback branch |
| `full projection rebuild (event replay)` | Current-facts no-cache path | Direct projector call when cache unavailable/ineligible | `--current-facts-cache-debug` | `_current_facts_timing_from_args()` |
| `incremental projection replay` | Projection-cache stale compatible snapshot path | Replay events after snapshot into prior state | execution status/cache status/current-facts timing | `project_state_with_cache()` |
| `projection cache` | Projection store state snapshot cache | Load/save reusable state snapshot | `--state-cache-status`, `--rebuild-state-cache`, debug surfaces | `ProjectionStore`, `project_state_with_cache()` |
| `state cache` | Same state projection snapshot as projection cache in current-facts/state-build surfaces | Surface-local view of projection-store state snapshot | current-facts timing, state-build cache debug | `state_cache_status`, state path labels |
| `state-build cache` | Dependent state-summary read-model cache | Summary snapshot keyed by state projection version and last event id | `--state-build-cache-debug`, `--state-build` | `SummaryProjectionSnapshot` load/save |
| `fact-index cache` | Dependent derived-index cache | Fact index keyed by state projection version and last event id | current-facts timing | `DerivedIndexSnapshot`, `_TimingProjectionStore` |
| `cached projection load/materialize` | Projection-cache materialization | Decode cached snapshot payload to `State` | projection diagnostics/current-facts timing | `project_state_with_cache()` |
| `cache metadata lookup + cached projection row load` | Projection-store operation timing | Wrapper timing around `load_snapshot()` | current-facts timing | `_TimingProjectionStore.load_snapshot()` |
| `load_state/cache` | Knowledge reachability audit load boundary | Audit-specific load-state/cache timing and cache metadata | `--knowledge-reachability-audit` JSON/table metadata | `KnowledgeReachabilityMetadata` and timer phases |
| `render` | Surface-local formatting/output phase | Convert built rows/views to text or mark render phase | current-facts, knowledge reachability | `_current_facts_timing_from_args()`, reachability timer |
| `rendering` | State-build debug formatting phase | Placeholder timing for state-build report rendering | state-build cache debug | `format_state_summary_cache_debug_report_placeholder()` timing |
| `query/filter + render` | Current-facts filtered output phase | Filter current facts with optional index and format result | current-facts timing | `_current_facts_timing_from_args()` |
| `stdout/output time` | Current-facts timing placeholder | Explicit output timing placeholder, currently zero | current-facts timing | `_current_facts_timing_from_args()` |
| `observation ingestion timings` | Observation ingestion diagnostics | Source collection, normalization, ingest/write, totals | `--observe-timings` | `ObservationIngestionDiagnostics`, formatter |
| `runtime trace` | Historical run reconstruction | Read matching ledger events and summarize run | `--trace-run`, `--why-run` | `RuntimeTraceReader` |
| `execution status` | Transient activity visibility | Phase/message/progress emitted to consumers | CLI stderr/progress, recording tests | `execution_status.py` |
| `snapshot policy` | Audit snapshot policy visibility | Snapshot health/recommendation/comparison availability | `--snapshot-policy-audit` | `SnapshotPolicyAudit` |
| `snapshot comparison` | Audit-snapshot comparison availability | Supported audit kinds and comparison rows | snapshot policy, impact/history/reference surfaces | snapshot policy uses `build_impact_audit()` |
| `projection store` | Backend-independent projection snapshot store | State snapshots plus dependent summary/index snapshots | cache-backed projection paths | `ProjectionStore` protocol |

## Multiple terms describing the same implementation concept

- **State projection event application:** `projection`, `projection replay`, `event replay`, and parts of `projection replay / build` refer to the implementation concept that applies ledger events into `State`. They occur at different surfaces: projector status uses `projection_replay`, diagnostics use `event replay`, and state-build debug wraps the whole projection/cache-backed call as `projection replay / build`.
- **Projection-store state snapshot reuse:** `projection cache`, `state cache`, `cached projection load/materialize`, and current-facts' `cache metadata lookup + cached projection row load` all refer to loading or describing the same state snapshot cache concept, but at different levels of detail.
- **Full rebuild from events:** `full projection rebuild`, `full projection rebuild (event replay)`, and state-build debug's miss case under `projection replay / build` all describe rebuilding projected state from ledger events rather than using an exact snapshot hit.
- **Output formatting:** `render`, `rendering`, and the render half of `query/filter + render` all describe output/report formatting, but their measured boundaries differ by surface.

## Similar terminology that represents different concepts

- **Projection cache snapshot vs audit snapshot:** projection-store snapshots cache derived `State`; audit snapshots preserve diagnostic/audit outputs and support policy/comparison visibility. They share the word `snapshot` but have different owners, payloads, invalidation, and consumers.
- **State projection cache vs state-build cache:** projection cache stores projected `State`; state-build cache stores a compact summary/read-model snapshot dependent on the state projection identity. Both are cache terms, but one is primary projected state and the other is a dependent read model.
- **Runtime trace vs execution status:** runtime trace is historical and event-backed; execution status is transient and non-authoritative. Both expose execution visibility, but one reads persisted events and the other is consumed during execution.
- **Observation ingestion vs projection:** ingestion writes observation/fact events; projection reads events into current state. Ingestion may use projection during normalization, but its responsibility is source collection/normalization/event writing.
- **Render vs projection:** formatters convert built data to output; projection builds state from events. Timing labels that include render must not be collapsed into projection phases.
- **Knowledge reachability `projected` stage vs projection cache:** reachability evaluates candidate presence across conceptual audit stages, including projected/read-model/rendered, while projection cache is a state snapshot implementation.

## Concept ownership table

| Concept | Owner | Exposes | Consumes |
| --- | --- | --- | --- |
| Append-only event history | `EventLedger` / SQLite ledger implementations | event list APIs | `StateProjector`, runtime trace, ingestion/read views |
| State projection / event replay | `StateProjector` | projected `State`, optional status/diagnostics | `EventLedger`, catalogs, events |
| Projection build diagnostics | `ProjectionBuildDiagnostics` plus callers | timings/counters when rendered | projector phases and caller timing reports |
| Projection cache / store | `ProjectionStore` implementations | snapshots, dependent summary/index snapshots | cache-backed projection, state-build/current-facts paths |
| Projection cache status | `project_state_with_cache()` | `StateCacheStatus`, emitted status phases | projection store, event ledger, projector |
| Dependent read-model caches | `ProjectionStore` summary/index APIs and builders | summary/fact-index snapshots | current state projection identity |
| State-build cache debug | CLI `state_summary_cache_debug_from_args()` and formatter | `StateSummaryCacheDebugReport` text | projection store, ledger, projector, summary builders |
| Current-facts cache debug | CLI `_current_facts_timing_from_args()` and formatter | `CurrentFactsTimingReport` text | projection store, ledger, projector, fact view/index builders |
| Knowledge reachability | `seed_runtime.knowledge_reachability` | rows plus `KnowledgeReachabilityMetadata` | projected state/read models/source scans |
| Observation ingestion | `ObservationCollectionService`, `ObservationIngestor`, sources | facts and optional `ObservationIngestionDiagnostics` | observation sources, normalization pipeline, ledger |
| Runtime trace | `RuntimeTraceReader` | `RuntimeTrace` and CLI trace/why formatting | append-only runtime events |
| Execution status | `ExecutionStatus` producers and consumers | transient status updates / CLI stderr / recording consumer | work-producing paths such as projection and observation collection |
| Audit snapshot policy/comparison | audit snapshot and snapshot-policy modules | policy JSON/text, comparison availability | snapshot files, repository observation, impact audit |
| Formatting/output | CLI formatter functions | human-readable output | reports, read models, trace/result objects |

## Layered execution model supported by implementation

The smallest supported layered model is local and compositional, not universal:

1. **Dispatch/CLI routing:** argparse flags choose observation, state/debug, reachability, trace, or snapshot-policy paths.
2. **Source/history access:** observation sources collect external observations; ledgers list append-only events; audit snapshot code reads snapshot files.
3. **Projection:** `StateProjector` applies events and finalizes derived indexes.
4. **Cache:** `ProjectionStore` may serve state snapshots; dependent summary/index caches may serve read models.
5. **Builder/read model:** state summary, fact views, fact indexes, knowledge reachability rows, runtime-trace summaries, and snapshot-policy reports are built from their inputs.
6. **Formatter/output:** CLI formatters render reports/rows/traces/facts.
7. **Runtime visibility side channel:** execution status can be emitted during long work; diagnostics/timing reports can measure selected boundaries.

The implementation evidence does not support one shared phase taxonomy across all surfaces.

## Recurring terminology

Recurring terms already present in implementation include `projection`, `projection cache`, `state cache`, `state-build cache`, `snapshot`, `render`, `runtime trace`, `execution status`, `timings`, `diagnostics`, `read-model`, and `event replay`.

The recurring terms are partly stable by owner: projection/cache language is stable inside `state.py` and `projection_store.py`; trace/status language is stable inside their modules; timing/render labels are surface-local.

## Divergent terminology

Terminology diverges in these exact places:

- State-build debug uses `projection replay / build` and `rendering`.
- Current-facts timing uses `full projection rebuild (event replay)`, `render`, `query/filter + render`, `stdout/output time`, and state-cache path labels.
- Projection diagnostics use `event replay`, `full projection rebuild`, `cached projection load/materialize`, and finalization labels.
- Execution status uses phases such as `projection_cache_load`, `projection_replay`, and `incremental_projection_replay` as transient status identifiers.
- Knowledge reachability uses audit-stage vocabulary such as preserved/projected/read-model/inquiry/rendered plus its own `render` and total timing metadata.
- Snapshot-policy language uses snapshot health, comparison availability, recommendation, and operational surfaces; this is not projection-cache vocabulary.

## Implementation-backed concept boundaries

- Event history is authoritative input; projection and trace derive from it.
- Projection builds current `State`; projection diagnostics observe it but are non-authoritative.
- Projection cache stores reusable projected state; dependent caches store read models keyed to state projection identity.
- State-build and current-facts debug reports are surface-local timing reports, not global execution traces.
- Knowledge reachability is an audit with stage-presence rows and metadata, not a projection-builder phase list.
- Observation ingestion is a write path from collected observations into ledger facts/events; its diagnostics are optional timing counters.
- Runtime trace is durable historical reconstruction from events; execution status is transient operator visibility.
- Audit snapshots/snapshot policy are diagnostic history/comparison artifacts, not projection-store snapshots.
- Formatting/output phases are consumers of already-built data, not owners of execution semantics.

## Implementation-backed gaps

- There is no single universal execution trace for every CLI command.
- There is no shared timing schema across state-build debug, current-facts debug, knowledge reachability, observation ingestion, snapshot policy, runtime trace, and execution status.
- There is no stable cross-surface phase vocabulary for render/output timing boundaries.
- Cache participation is explicit for projection/state-build/current-facts paths, but not uniformly tied to runtime trace ids or command ids.
- Execution status has shared consumer types, but production phase names remain operation-specific.
- Snapshot comparison exists for audit snapshots, while projection-store snapshots expose cache reuse rather than comparison semantics.

## Stable implicit vocabulary assessment

A stable implicit vocabulary exists at the owner boundary level, not at the word level. The strongest implicit vocabulary is:

- ledger/event history;
- state projection/event replay/finalization;
- projection cache/projection store/state snapshot;
- dependent summary/index read-model cache;
- observation collection/normalization/ingestion;
- runtime trace;
- execution status;
- audit snapshot policy/comparison;
- formatter/render/output.

A stable universal phase vocabulary does not exist. The divergences above are implementation-backed and surface-local rather than merely naming noise.

## Why terminology differs

- **True implementation differences:** projection cache vs audit snapshots; runtime trace vs execution status; state projection vs observation ingestion; projection cache vs dependent read-model caches.
- **Surface-local vocabulary:** state-build debug `projection replay / build`, current-facts `query/filter + render`, knowledge reachability audit stages, and `stdout/output time` are local to those reports.
- **Historical evolution:** runtime trace is tied to recorded RuntimeLoop-style events and remains adjacent to current inquiry/debug paths; some docs call it historical compatibility. The implementation preserves it as a read-only event reconstruction rather than a current universal execution profiler.
- **Unresolved implementation concepts:** global command execution traces, shared phase/timing schema, and consistent render/output timing boundaries are not implemented as shared concepts.

## Smallest implementation-backed execution ontology already recoverable

1. **Event history** records what happened.
2. **Observation ingestion** turns observations into ledger events/facts.
3. **State projection** derives current state from event history.
4. **Projection diagnostics** observe projection construction timings/counters without authority.
5. **Projection cache** stores/reuses projected state snapshots.
6. **Dependent read-model caches** store summaries/indexes keyed to projected-state identity.
7. **Read-model builders/audits** derive command-specific views such as state summary, current facts, knowledge reachability, trace summaries, and snapshot policy.
8. **Runtime trace** reconstructs recorded runs from events.
9. **Execution status** emits transient activity visibility during work.
10. **Formatter/output** renders already-built data.
11. **Audit snapshots/comparison** preserve and compare diagnostic snapshot artifacts.

This ontology should not be extended without new implementation evidence.

## Vocabulary normalization conclusion

Future vocabulary normalization, if any, should occur at the level of implementation concepts and relationships, not words. Repository evidence shows that identical or similar words can refer to different responsibilities (`snapshot`, `cache`, `render`) and different words can describe the same responsibility at different surfaces (`projection replay`, `event replay`, `full projection rebuild`). Normalizing words first would erase implementation boundaries; recovering owner/boundary/consumer relationships preserves the evidence needed for any later vocabulary work.

## Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '!**/.git/**' && git status --short`
- `cat AGENTS.md && git status --short`
- `rg -n "projection|ProjectionBuildDiagnostics|state-build|current-facts|knowledge reachability|observation ingestion|runtime trace|execution status|snapshot policy|snapshot comparison|projection store|execution timing|load_state|rendering|render" . --glob '!**/.git/**'`
- `sed -n '1,120p' seed_runtime/state.py; sed -n '720,840p' seed_runtime/state.py; sed -n '1,220p' seed_runtime/projection_store.py; sed -n '533,720p' seed_runtime/projection_store.py`
- `sed -n '3090,3335p' scripts/seed_local.py; sed -n '5020,5190p' scripts/seed_local.py; sed -n '160,245p' seed_runtime/knowledge_reachability.py; sed -n '420,500p' seed_runtime/knowledge_reachability.py; sed -n '7370,7430p' scripts/seed_local.py`
- `rg -n "ObservationIngestionDiagnostics|format_observation_ingestion|snapshot policy|snapshot comparison|runtime trace|execution status|class CliExecutionStatus|runtime_trace|execution-status|execution status" seed_runtime scripts docs tests -S`
- `sed -n '90,130p' seed_runtime/observation_sources.py; sed -n '3170,3235p' seed_runtime/observation_sources.py; sed -n '690,735p' scripts/seed_local.py; sed -n '1,120p' seed_runtime/runtime_trace.py; sed -n '1,80p' seed_runtime/execution_status.py; sed -n '1,120p' seed_runtime/snapshot_policy_audit.py`

## Files inspected

- `AGENTS.md`
- `seed_runtime/state.py`
- `seed_runtime/projection_store.py`
- `scripts/seed_local.py`
- `seed_runtime/knowledge_reachability.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/runtime_trace.py`
- `seed_runtime/execution_status.py`
- `seed_runtime/snapshot_policy_audit.py`
- Related existing investigation documents found under `docs/`, especially `docs/execution_visibility_investigation.md` and `docs/execution_timing_adversarial_audit.md`.

## Files changed

- `docs/execution_concepts_implementation_investigation.md`

## LOC changed

One documentation file was added. It contains this investigation and no runtime code.

## Tests run

No tests were required because this investigation is documentation-only and does not change runtime code, diagnostic registry entries, CLI flags, recordable outputs, or tests.
