# Execution-Status Producer Contract Reconciliation

## Scope

This is a documentation-only reconciliation of Seed execution-status production. It reviews the shared consumer surface, the CLI renderer, progress cadence, local-host and repository-source observation paths, projection replay, dependent read-model caches, fact-index construction, and recent execution-status audits.

This document does not implement emitters, change execution status, change projection behavior, change cache behavior, change observation behavior, add status messages, add progress cadence, or modify runtime code.

## Evidence reviewed

Runtime surfaces reviewed:

- `seed_runtime/execution_status.py`, including `ExecutionStatus`, `ExecutionStatusConsumer`, `CliExecutionStatusConsumer`, `ProgressCadence`, `emit_progress_if_due`, and `emit_status`.
- `seed_runtime/observation_sources.py`, especially `ObservationCollectionService.collect` and source collection dispatch.
- `seed_runtime/observations.py`, especially `ObservationIngestor.ingest_many`.
- `seed_runtime/events.py`, including in-memory and SQLite `append_many` status emission.
- `seed_runtime/projection_store.py`, including state projection cache load, full replay, incremental replay, and cache save.
- `seed_runtime/state.py`, including `StateProjector.project` and `project_from_state` replay progress.
- `seed_runtime/fact_index.py`, including fact-index cache load, build, and save status.
- `scripts/seed_local.py`, including `--observe-local-host`, `--observe-repository-source`, `--state-summary`, current-facts, candidate, verification, and promotion-readiness read-model inspection paths.

Recent documentation reviewed:

- `docs/execution_status_and_operator_feedback_reconciliation.md`.
- `docs/execution_status_emission_and_consumption_reconciliation.md`.
- `docs/execution_boundary_inventory_and_status_emission_audit.md`.
- `docs/execution_status_and_projection_pipeline_gap_audit.md`.
- `docs/execution_status_measurement_implementation_audit.md`.

## Shared consumer surface

Seed has a shared execution-status consumer surface. `ExecutionStatus` is renderer-independent and non-authoritative activity visibility. The protocol exposes a single `consume(status)` method, with null, recording, and CLI consumers. The CLI consumer renders status without owning execution state, and it suppresses some progress updates according to a renderer-side interval.

The shared consumer model is therefore real and explicit:

- status has `phase`, `message`, optional `current`, optional `total`, and `completed`;
- consumers observe status;
- consumers do not define, authorize, replay, persist, or mutate work;
- CLI progress rendering is a consumption policy, not producer authority.

## Progress cadence implementation

Seed also has a reusable producer-side cadence helper. `ProgressCadence` bounds loop progress by first item, final item, item interval, and elapsed time. `emit_progress_if_due` applies that cadence and emits an `ExecutionStatus` only when useful.

However, this cadence is a helper, not a complete producer contract. It standardizes when bounded loop updates may be emitted for producers that opt in. It does not define which operations must report, which phase names must be used, which messages must be used, or where phase boundaries begin and end.

## Producer-path findings

| Path | Phases/status observed | Missing or uneven status | Shared wording/cadence finding |
| --- | --- | --- | --- |
| Observation collection | `observation_collection`: `Collecting {source.name} observations...`; `Collected N observations.` | The actual source-specific `collect()` implementation may perform substantial discovery silently before returning. | Phase name is shared by collection service, but message includes source name and cadence is absent because the service receives a completed list. |
| Observation normalization | No explicit status phase found. | Normalization pipeline can run between collection and ingestion without status. | No shared producer behavior for normalization. |
| Observation ingestion event generation | `observation_ingestion`: `Generating events...`, per-observation `Generating events`, final `Generated events`. | Per-observation generation uses direct `emit_status`, not bounded cadence; CLI may suppress many progress rows, but producer still emits every observation. | Phase is operation-specific and wording is not shared with event persistence. |
| Event writing | `event_persistence`: `Writing events` with bounded cadence. | No distinct commit/finalization wording beyond completed progress. | In-memory and SQLite ledgers share the same phase/message/cadence. This is one of the strongest standardized producer areas. |
| Local-host observation | Routed through `ObservationCollectionService.collect`, then ingestion and event writing. | Source-local discovery internals are only visible if they emit independently; otherwise collection is silent until the list returns. | Operator-visible progress mostly comes from ingestion and event persistence after collection, not necessarily from every discovery subphase. |
| Repository-source observation | Routed through the same high-level collection service, but source scanning may be long before observations are returned. | Repository-source discovery can emit little or no progress during collection if its source internals do not report. | It shares the consumer surface but not a source-level producer contract for discovery cadence or phases. |
| Projection cache load | `projection_cache_load`: `Loading projection cache...`, `State cache: hit`, `State cache: miss`. | Cache deserialization/validation substeps are not separately phased. | Wording is local to projection cache and not shared with state-summary or fact-index cache except by informal hit/miss shape. |
| Full projection replay | `projection_replay`: starts at `0 / total`; `StateProjector.project` applies events and emits bounded progress from `project_from_state`. | `finalize` has no status; derived index rebuild inside finalization is silent. | Uses shared cadence helper, but phase wording is projection-specific. |
| Incremental projection replay | `incremental_projection_replay`: starts at `0 / remaining`; `_events_with_progress` can emit bounded progress while yielding events. | `project_from_state` materializes the iterable before applying events, so generator-layer progress may describe event-list consumption rather than event application. The current documentation treats this as a tension, not a runtime change request. | Incremental replay has its own phase rather than sharing full replay vocabulary. |
| Projection cache save | `projection_cache_save`: `Saving projection snapshot...`. | No completion status found for save. | Operation-specific one-shot status. |
| State-summary cache | `state_summary_cache_load`: `Loading state-summary cache...`, `State-summary cache: hit`, `State-summary cache: miss`. | Building `StateSummary`, building operator summary payload, and saving summary snapshot are silent. | Mirrors cache hit/miss structure but uses its own phase and wording. |
| Fact-index cache | `fact_index_cache_load`: `Loading fact index cache...`, `Fact index cache: hit`, `Fact index cache: miss`; `fact_index_cache_save`: `Saving fact index cache...`. | Cache save has no completion status. | Similar cache lifecycle shape, but phase names and messages remain subsystem-specific. |
| Fact-index build | `fact_index_build`: `Building fact index...`, bounded progress `Building fact index`, final completed `Building fact index...`. | Start/final message includes ellipsis, progress message omits it. | Uses shared cadence helper, but wording is local and not a common build/read-model vocabulary. |
| Read-model inspection paths | Many CLI branches create `CliExecutionStatusConsumer` and pass it into projection/cache/fact-index helpers. | Read-model-specific derivation after projected state is often silent; not every inspection path passes a consumer to every helper. | Consumers are reused, but producer coverage depends on each called helper. |

## Is execution status operation-specific or shared phase-oriented?

Repository evidence currently supports this answer:

Seed models execution status as a shared transient status shape consumed by shared consumers, while production is mostly operation-specific messages with a few reusable helpers and repeated informal patterns.

It is not yet governed by a shared phase-oriented producer contract. There are recurring phase-like ideas, but they are not centralized as an authoritative vocabulary and are not applied uniformly across observers, projectors, caches, and read-model builders.

## Do subsystems share a common phase vocabulary?

Not formally.

They share a common status object and some common structural motifs:

- load cache;
- cache hit;
- cache miss;
- replay;
- build;
- save;
- write events;
- collect observations;
- generate events.

But the exact phase identifiers are subsystem-specific:

- `projection_cache_load`;
- `state_summary_cache_load`;
- `fact_index_cache_load`;
- `projection_replay`;
- `incremental_projection_replay`;
- `fact_index_build`;
- `observation_collection`;
- `observation_ingestion`;
- `event_persistence`.

The vocabulary is descriptive, but not shared in the sense of a repository-wide producer contract. There is no evidence of a canonical phase enum, lifecycle table, required status sequence, or required producer obligations for long-running work.

## Recurring phases that repository evidence supports

The evidence supports these recurring phase families, without proving that they are formal phases:

1. Cache access
   - loading projection cache;
   - loading state-summary cache;
   - loading fact-index cache.
2. Cache result
   - state cache hit/miss;
   - state-summary cache hit/miss;
   - fact-index cache hit/miss.
3. Replay
   - full projection replay;
   - incremental projection replay.
4. Build/read-model derivation
   - fact-index build is visible;
   - state-summary build exists but is silent;
   - read-model inspection derivation often happens after projection without its own status.
5. Persistence/save
   - writing events;
   - saving projection snapshot;
   - saving fact-index cache;
   - state-summary snapshot save exists but is silent.
6. Observation intake
   - collecting observations;
   - generating observation/evidence/fact events;
   - writing generated events.

These families resemble a possible future common vocabulary, but the repository currently treats them as local producer choices.

## What is shared

- The status data shape is shared.
- The consumer protocol is shared.
- CLI rendering is shared by consumers that receive status.
- Recording/null consumers provide shared test and no-op behavior.
- Producer-side bounded progress cadence is shared where producers opt in.
- Event-writing producers are relatively standardized across in-memory and SQLite ledgers.
- Cache paths share an informal load/hit/miss pattern.
- Projection replay and fact-index build share the cadence helper for bounded progress.

## What is duplicated

- Cache lifecycle wording is duplicated separately for projection, state-summary, and fact-index caches.
- Build/replay loops independently choose phase identifiers and messages.
- CLI branches independently decide whether to instantiate and pass `CliExecutionStatusConsumer`.
- Observation-related paths share high-level service status but leave source-specific discovery behavior to independent source implementations.

## What is inconsistent

- Some long-running loops use `ProgressCadence`; observation event generation emits every item directly.
- Some cache saves announce start only; state-summary cache save is silent.
- Projection replay has start and bounded progress; state-summary build has no explicit build status.
- Fact-index build has visible start/progress/final status; other read-model builds can be silent.
- Full replay and incremental replay use different phase names and may report progress from different layers.
- Cache hit/miss messages are structurally similar but not governed by a common cache-status contract.
- CLI consumption is common, but producer behavior varies substantially by subsystem.

## Boundary findings

The reviewed implementation preserves the intended boundaries:

- execution status is not an event;
- execution status is not an observation;
- execution status is not a fact;
- execution status is not projection authority;
- execution status is not cache authority;
- execution status does not define runtime semantics;
- execution status communicates work while the underlying work remains defined by observations, events, projection, caches, and read-model builders.

Tests and prior audits reinforce that status is transient and should not enter ledgers, observations, facts, or projection cache payloads.

## Unresolved tensions preserved

- Status phase vs implementation detail: a phase can help the operator, but too many phases may expose internals as implied semantics.
- Generic status vs subsystem-specific status: common vocabulary improves consistency, while local wording can be more useful for the current operation.
- Phase consistency vs operator usefulness: uniform labels may be less informative than source-specific messages during collection or replay.
- Progress reporting vs work semantics: progress communicates work but must not become the definition of work.
- Consumer standardization vs producer standardization: Seed has standardized consumption more clearly than production.
- Cache lifecycle visibility vs cache authority: cache hit/miss messages help operators, but the cache remains an optimization, not authority.
- Replay visibility vs projection authority: replay status can describe application progress, but event history remains the source of truth.

## Final conclusion

Repository evidence supports the central question:

Seed currently has a shared execution-status consumer surface and shared helper primitives, but it does not yet have a shared execution-status producer contract.

The current architectural shape is best described as:

```text
shared consumer
+
shared status data shape
+
shared optional cadence helper
+
independent producer behavior
```

The repository evidence also supports a possible future direction where long-running work could report through a common phase vocabulary, because cache load/hit/miss, replay, build, save, collect, generate, and write patterns recur across subsystems. However, the current architecture does not prove that such a direction is already intentional or authoritative. Today, production remains operation-specific, with informal recurring patterns rather than a formal common phase model.

## Direct answer

Did this task implement a status framework?

No.

This task created a documentation-only reconciliation.
