# Execution Status Measurement Implementation Audit

## Scope

This document is a measurement-focused implementation audit for slow repository-observation and projection/read-model workflows.

It preserves authority boundaries:

- execution status is transient operator visibility;
- event history remains durable authority;
- projection snapshots, state-summary snapshots, and fact indexes are caches/read models;
- repository observation is a read-only source scan until its observations are ingested as events.

This audit does not implement fixes, add status emissions, add caches, optimize replay, change schema, or change runtime behavior.

## Inputs Reviewed

- `docs/execution_status_and_projection_pipeline_gap_audit.md`
- `scripts/seed_local.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/state.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/observations.py`
- `seed_runtime/events.py`
- `seed_runtime/fact_index.py`
- `seed_runtime/execution_status.py`
- recent state-summary, projection-cache, fact-index, repository-observation, execution-status, and progress-cadence implementation paths in the repository

## Pull Latest Main

Attempted command:

```text
git fetch origin main && git pull --ff-only origin main
```

Result:

```text
fatal: 'origin' does not appear to be a git repository
fatal: Could not read from remote repository.
```

Measured repository state: no `origin` remote is configured, so there was no remote `main` available to pull from this checkout.

## Measurement Environment

Measurements were collected in the task container on 2026-06-15 UTC using temporary SQLite databases under `/tmp`.

The measurements are implementation evidence, not durable benchmark claims. They are useful for locating visible silent regions in the current code paths.

### Commands Run

Repository observation measurement:

```text
python scripts/seed_local.py --db "$db" --observe-repository-source .
```

Projection/read-model measurements after repository observation populated the temporary DB:

```text
python scripts/seed_local.py --db "$db" --state-summary
python scripts/seed_local.py --db "$db" --current-facts scripts/seed_local.py imports
python scripts/seed_local.py --db "$db" --capability-candidates python
python scripts/seed_local.py --db "$db" --capability-verification python
python scripts/seed_local.py --db "$db" --capability-promotion-readiness python
```

Long-running read-model commands were wrapped with `timeout 20` to preserve bounded evidence.

## Measured Findings

### Repository observation completed, but output volume is high

A repository-source observation against `.` completed successfully in 7.154 seconds.

Observed counts:

- return code: `0`
- elapsed wall time: `7.154s`
- collected observations: `3587`
- stdout lines: `32284`
- first visible status sequence:
  - `Collecting repository_source observations...`
  - `Collected 3587 observations.`
  - `Generating events...: 0 / 3587`
  - `Generating events: 100 / 3587`
  - `Generating events: 200 / 3587`

Measured conclusion: in this checkout, repository observation does emit top-level collection and ingestion/event-write status when invoked through the CLI path with a status consumer. The collection scan itself is still silent between the initial `Collecting ...` line and final `Collected ...` line.

### Cold projection/read-model commands timed out before first replay progress update

After repository-source observation created 10,761 events, multiple commands timed out after 20 seconds.

Each timed-out command showed the same final status region:

```text
Loading projection cache...
State cache: miss
Projection replay: 0 / 10761
```

For `--state-summary`, the preceding state-summary cache status was also visible:

```text
Loading state-summary cache...
State-summary cache: miss
Loading projection cache...
State cache: miss
Projection replay: 0 / 10761
```

Measured table:

| Command | Return code | Elapsed | Last observed status |
| --- | ---: | ---: | --- |
| `--state-summary` | 124 | 20.070s | `Projection replay: 0 / 10761` |
| `--current-facts scripts/seed_local.py imports` | 124 | 20.072s | `Projection replay: 0 / 10761` |
| `--capability-candidates python` | 124 | 20.068s | `Projection replay: 0 / 10761` |
| `--capability-verification python` | 124 | 20.067s | `Projection replay: 0 / 10761` |
| `--capability-promotion-readiness python` | 124 | 20.064s | `Projection replay: 0 / 10761` |

Measured conclusion: with a cold state cache after repository observation, time is spent before any rendered replay progress beyond `0 / 10761`. The command did not reach state-summary construction, fact-index loading/building, candidate derivation, capability-verification derivation, or promotion-readiness derivation during the 20-second windows.

This is stronger than a hypothesis that only post-replay work is slow for this measured case. The measured cold-cache path is slow during event projection before the first rendered loop update.

## Implementation Path Map

### Shared status infrastructure

`ExecutionStatusConsumer` is transient. `CliExecutionStatusConsumer` writes progress/status to stderr and renders progress only for boundaries, completion, and multiples of its `progress_interval` value, which defaults to `100`.

`ProgressCadence` emits on first item, final item, item intervals of `500`, or elapsed time of at least one second. Therefore a producer may generate a first-item status at `1 / total`, but the CLI consumer suppresses it unless the item count is a multiple of `100`, `0`, or final.

Measured implication: status can be emitted internally but not rendered by the CLI. In the measured cold projection path, the visible status stopped at `Projection replay: 0 / 10761`; a produced `1 / 10761` update would be suppressed by the CLI renderer.

### `--observe-local-host`

Path:

1. CLI detects observation-only mode.
2. Creates `CliExecutionStatusConsumer`.
3. Calls `ingest_observations_from_args`.
4. Constructs `LocalHostObservationSource`.
5. Calls `ingest_observation_source`.
6. `ObservationCollectionService.collect` emits collection start/end around `source.collect()`.
7. Normalization projects current state without threading the status consumer.
8. `ObservationIngestor.ingest_many` emits event-generation progress.
9. `SQLiteEventLedger.append_many` emits event-persistence progress when a DB is used.
10. CLI emits `Done.`.

Status coverage:

- collection boundary: yes;
- source-internal local-host loops: not generally itemized by execution status;
- normalization projection: silent;
- event generation: yes;
- event persistence: yes for SQLite batch writes;
- knowledge mutation: yes, via appended observation/evidence/fact events;
- cache mutation: no projection/read-model cache mutation in this path.

Long-running risk: local-host collection loops, normalization projection, event generation for large observation counts, and SQLite event persistence.

### `--observe-repository-source`

Path:

1. CLI detects observation-only mode.
2. Creates `CliExecutionStatusConsumer`.
3. Calls `ingest_observations_from_args`.
4. Constructs `RepositorySourceObservationSource(args.observe_repository_source)`.
5. Calls `ingest_observation_source`.
6. `ObservationCollectionService.collect` emits collection start/end around `source.collect()`.
7. `RepositorySourceObservationSource.collect` discovers Python files and loops over each file.
8. Each file is read, import relationship facts are extracted, definition relationship facts are extracted, and observations are created.
9. Normalization projects current state without status threading.
10. `ObservationIngestor.ingest_many` emits event-generation progress.
11. `SQLiteEventLedger.append_many` emits event-persistence progress when a DB is used.
12. CLI emits `Done.`.

Status coverage:

- collection boundary: yes;
- file discovery loop: silent;
- per-file read/parse/extract loop: silent;
- relationship-to-observation expansion: silent;
- normalization projection: silent;
- event generation: yes;
- event persistence: yes for SQLite batch writes;
- knowledge mutation: yes, via appended observation/evidence/fact events;
- cache mutation: no projection/read-model cache mutation in this path.

Measured finding: repository-source collection produced `3587` observations and completed in `7.154s` in the measured checkout. The collection phase had only boundary status, so an operator sees no per-file progress until all observations are collected.

Difference from local-host observation: both paths share collection boundary, normalization, ingestion, and persistence status. Repository observation has its own file-discovery and source-file extraction loops, and those repository-specific loops are silent.

### `--state-summary`

Path:

1. CLI calls `projected_state_summary_from_args` with `CliExecutionStatusConsumer`.
2. Opens SQLite event ledger and projection store.
3. Lists events to determine current last event id.
4. Emits state-summary cache load status.
5. Attempts `load_summary_snapshot`.
6. On miss, emits state-summary cache miss.
7. Creates `StateProjector`.
8. Calls `project_state_with_cache` when cache use is allowed.
9. Projection cache load emits status.
10. Snapshot load/deserialization may happen.
11. On cache miss, full projection replay begins and emits `Projection replay: 0 / total`.
12. `StateProjector.project` calls `project_from_state`.
13. `project_from_state` materializes the event iterable into a list, applies each event, emits cadence progress, then calls `finalize`.
14. `finalize` rebuilds aliases, inferred facts, measurement history retention, fact supports, entity relationships, catalog relationships, entity type assertions, graph issues, aliases, and conflicts.
15. State snapshot save emits only `Saving projection snapshot...` before serializing and saving state.
16. `build_state_summary(state)` runs silently.
17. `state_summary(state)` runs silently.
18. `save_summary_snapshot` runs silently.
19. CLI formats and prints summary.

Status coverage:

- state-summary cache load/hit/miss: yes;
- projection cache load/hit/miss: yes;
- replay start/progress: yes at producer level, rendered sparsely by CLI;
- finalize: silent;
- state serialization before save: covered only by pre-save boundary, no completion;
- projection snapshot SQLite save: covered only by pre-save boundary, no completion;
- state-summary build: silent;
- state-summary cache save: silent;
- cache mutation: yes, state projection snapshot and state-summary snapshot on miss;
- knowledge mutation: no.

Measured finding: in the cold-cache measured path, `--state-summary` timed out after `20.070s` with final status `Projection replay: 0 / 10761`, so it did not measurably reach post-replay state-summary phases during that bounded run.

### `--current-facts SUBJECT PREDICATE`

Path:

1. CLI creates `CliExecutionStatusConsumer`.
2. Calls `fact_query_state`.
3. Seeds dev-state inputs if provided.
4. Builds a `StateProjector`.
5. Uses `project_state_with_cache` when DB/cache conditions allow.
6. Optionally loads/builds fact index through `load_or_build_fact_index`.
7. Formats current facts.

Status coverage:

- projection cache load/hit/miss and replay: yes when state cache is used;
- non-cache projection fallback: silent in this helper because `projector.project(args.workspace)` is called without a status consumer;
- fact-index cache load/hit/miss: yes;
- fact-index build loop: yes at producer level, rendered sparsely by CLI;
- fact-index save: start status only;
- final fact filtering/formatting: silent;
- cache mutation: fact index may be saved; state cache may be saved on projection miss;
- knowledge mutation: only dev seed inputs, if supplied; the read query itself is read-only.

Measured finding: after repository observation, the cold-cache measured command timed out after `20.072s` at `Projection replay: 0 / 10761`, before fact-index phases.

### `--capability-candidates FILTER`

Path:

1. CLI creates `CliExecutionStatusConsumer`.
2. Calls `projected_state_from_args`.
3. Uses `project_state_with_cache` when DB/cache conditions allow.
4. Optionally loads/builds fact index.
5. Calls `build_capability_candidates` and renders JSON.

Status coverage:

- projection cache load/hit/miss and replay: yes when state cache is used;
- fallback projection: silent;
- fact-index cache/build/save: yes for load/build start/progress/save start;
- candidate derivation: silent;
- cache mutation: state cache and possibly fact-index cache;
- knowledge mutation: no.

Measured finding: timed out after `20.068s` at `Projection replay: 0 / 10761`, before fact-index or candidate derivation.

### `--capability-verification FILTER`

Path:

1. CLI creates `CliExecutionStatusConsumer`.
2. Calls `projected_state_from_args`.
3. Uses `project_state_with_cache` when DB/cache conditions allow.
4. Optionally loads/builds fact index.
5. Calls `build_capability_verification_inspection` and renders JSON.

Status coverage:

- projection cache load/hit/miss and replay: yes when state cache is used;
- fallback projection: silent;
- fact-index cache/build/save: yes for load/build start/progress/save start;
- verification derivation: silent;
- cache mutation: state cache and possibly fact-index cache;
- knowledge mutation: no.

Measured finding: timed out after `20.067s` at `Projection replay: 0 / 10761`, before fact-index or verification derivation.

### `--capability-promotion-readiness FILTER`

Path:

1. CLI creates `CliExecutionStatusConsumer`.
2. Calls `projected_state_from_args`.
3. Uses `project_state_with_cache` when DB/cache conditions allow.
4. Optionally loads/builds fact index.
5. Calls `build_capability_promotion_readiness_inspection` and renders JSON.

Status coverage:

- projection cache load/hit/miss and replay: yes when state cache is used;
- fallback projection: silent;
- fact-index cache/build/save: yes for load/build start/progress/save start;
- promotion-readiness derivation: silent;
- cache mutation: state cache and possibly fact-index cache;
- knowledge mutation: no.

Measured finding: timed out after `20.064s` at `Projection replay: 0 / 10761`, before fact-index or promotion-readiness derivation.

## Projection Pipeline Coverage

| Phase | Status? | Can be expensive? | Measured or inferred? | Notes |
| --- | --- | --- | --- | --- |
| List events from ledger | No dedicated phase status | Yes for large ledgers | Inferred | Happens before projection-cache status in `project_state_with_cache`. |
| Load projection snapshot | Yes, start plus hit/miss | Yes if snapshot JSON is large | Inferred | Deserialization through `state_from_payload` is inside load/hit path and has no subphase. |
| Load remaining events | No dedicated phase status | Yes | Inferred | Remaining-event slicing happens before incremental replay status. |
| Full replay start | Yes | N/A | Measured | Visible as `Projection replay: 0 / 10761`. |
| Apply replay events | Producer emits cadence progress | Yes | Measured for cold path as slow before next visible CLI update | CLI suppresses non-boundary/non-100-multiple progress. Per-event `apply` recomputes relationship projections for fact events. |
| Incremental replay start | Yes | N/A | Inferred from implementation and prior operator output | Visible as `Incremental replay: 0 / N`. |
| Apply incremental events | Producer emits cadence progress via `_events_with_progress` and `project_from_state` may also emit if parameters are supplied | Yes | Inferred | Incremental path passes a generator that emits progress, but `project_from_state` materializes it with `list(events)` before its own apply loop. |
| Finalize projected state | No | Yes | Inferred | Rebuilds support structures and validation outputs. |
| Serialize state payload | Only preceded by `Saving projection snapshot...` | Yes | Inferred | `state_to_payload` and JSON serialization are inside snapshot save path. |
| Save projection snapshot | Start only | Yes | Inferred | No completion status. |
| Build `StateSummary` view | No | Yes | Inferred | Runs after state projection in state-summary path. |
| Build operator state-summary | No | Yes | Inferred | Runs after `build_state_summary`. |
| Save state-summary cache | No | Yes | Inferred | Direct call to `save_summary_snapshot`. |
| Load/build fact index | Yes for load/hit/miss/build/save start; build loop has cadence | Yes | Inferred for post-projection; not reached in measured timed-out runs | Used by filtered fact/capability read paths. |
| Candidate/verification/readiness derivation | No | Possibly | Inferred; not reached in measured timed-out runs | Read-only derivation after state and optional index. |

## Identified Silent Phases

Measured silent or sparsely visible phases:

- repository-source file discovery and per-file source extraction between collection start and collection completion;
- projection event application before the first CLI-rendered replay progress update;
- state-summary, current-facts, capability-candidates, capability-verification, and capability-promotion-readiness all share the same cold projection bottleneck after repository observation.

Implementation-inferred silent phases that were not reached by bounded measurements:

- state finalization after replay;
- projection snapshot serialization and save completion;
- state-summary construction;
- state-summary cache save;
- read-model derivation after projection;
- fallback non-cache projection paths that call `projector.project` without a status consumer;
- normalization projection during observation ingestion.

## Hypotheses Preserved Separately

These are hypotheses, not measured findings in this audit:

1. Per-event projection may be expensive because `StateProjector.apply` recomputes entity/catalog relationships on each fact event, before finalization recomputes derived structures again.
2. Incremental replay may duplicate progress-production layers because `_events_with_progress` emits while `project_from_state` also supports status emission, but the current incremental call relies on the generator layer.
3. Post-replay finalization and serialization may still be expensive on a machine/run where replay completes; this remains plausible from the prior operator observation showing a hold after `Incremental replay: 10761 / 10761`, but it was not reached by the cold-cache timeout measurements in this audit.
4. Large stdout formatting may contribute to perceived slowness for repository observation because the measured observation command produced 32,284 stdout lines.

## Open Questions

- On a warmed cache with a valid projection snapshot, how much time is spent loading/deserializing the snapshot versus using dependent state-summary/fact-index caches?
- In the operator's incremental-replay case, what phase followed `Incremental replay: 10761 / 10761` before the long hold: `finalize`, `state_to_payload`, SQLite snapshot save, summary build, or summary save?
- Should future measurement use phase-level profiling outside production behavior to time `apply`, `finalize`, `state_to_payload`, `save_snapshot`, `build_state_summary`, `state_summary`, and `save_summary_snapshot` separately?
- Should CLI rendering cadence be considered separately from producer cadence, since internal status may be emitted but not rendered?

## Direct Answer

Did this task implement fixes?

No.

This task produced a measurement-focused implementation audit only.
