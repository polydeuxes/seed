# Execution Timing Adversarial Audit

## Implementation summary

This audit reviewed Seed's existing timing, debug-timing, cache, snapshot, and execution-status visibility as implementation evidence only. The implementation contains several useful read-only timing surfaces, but they are not yet a coherent self-observation system. The healthiest surfaces are narrow and local: current-facts timing, state-build cache debug, observation ingestion timings, and knowledge reachability metadata. The adversarial finding is that these surfaces cannot reliably be compared as one execution model because phase names, timing boundaries, output parity, cache vocabulary, persistence behavior, and snapshot/run participation evidence differ by surface.

This is not an optimization proposal. No timers, code refactors, or implementation fixes were added.

## Files inspected

- `scripts/seed_local.py`
- `seed_runtime/state.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/knowledge_reachability.py`
- `seed_runtime/observations.py`
- `seed_runtime/execution_status.py`
- `seed_runtime/audit_snapshots.py`
- `seed_runtime/snapshot_policy_audit.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_knowledge_reachability.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

## Timing surfaces audited

| Surface | Implementation evidence | Timing / debug form | Persistence / JSON status |
| --- | --- | --- | --- |
| State-build cache debug | `state_summary_cache_debug_from_args()` and `StateSummaryCacheDebugReport` in `scripts/seed_local.py` | Timed phase list, projection subphase timings, cache statuses, event ids, counters | Human-rendered only; no JSON function in the inspected implementation path |
| Current-facts cache debug | `_current_facts_timing_from_args()` and `CurrentFactsTimingReport` in `scripts/seed_local.py` | Timed phase list, cache status, store wrapper timings, projection diagnostics | Human-rendered only; diagnostic inventory says `supports_json=False` |
| Knowledge reachability audit | `_ReachabilityTimer` and `KnowledgeReachabilityMetadata` in `seed_runtime/knowledge_reachability.py` | Named phases, metadata timings, counters, indexes, progress debug | JSON parity exists through `knowledge_reachability_json()` |
| Projection build diagnostics | `ProjectionBuildDiagnostics` in `seed_runtime/state.py` | Optional additive subphase timings and counters | Returned to callers that pass diagnostics; not itself persisted |
| Projection cache status | `format_state_cache_status_from_args()` and `project_state_with_cache()` paths | Hit/miss and event id status; build path can emit transient status | Mostly rendered/status-only; snapshot payload persists state, not timing |
| Snapshot creation/reuse/comparison/policy | `audit_snapshots.py` and `snapshot_policy_audit.py` | Snapshot metadata, latest event id, comparison availability, age seconds | Snapshot metadata and payload persisted for audit snapshots; policy has JSON output |
| Observation ingestion timings | `format_observation_ingestion_diagnostics()` and collection diagnostics | Source collection, normalization, event generation + ledger write, throughput counters | Rendered when `--observe-timings`; diagnostics are in-memory list passed by caller |
| Runtime trace / execution status | `runtime_trace_from_args()`, `format_runtime_trace()`, and `execution_status.py` | Historical runtime trace from ledger plus transient status events | Runtime trace is ledger-backed; execution status is transient/non-authoritative |
| Diagnostic inventory / shape audit | `DIAGNOSTIC_INVENTORY` and `IMPLEMENTATION_SPECS` | Registration of diagnostic surfaces and implementation-shape checks | Inventory/shape surfaces expose JSON; timing debug surfaces are not all registered equally |

## Healthy findings

1. **State-build cache debug exposes enough local evidence to explain a narrow cache path.** It reports cache eligibility, summary-cache status, projection-cache status, current/cached last-event ids, notes, structure counters, top-level timings, and projection replay/build subphase timings.
2. **Current-facts cache debug separates some important paths.** It distinguishes cache hit, incremental replay miss, full projection rebuild miss, read-model build, query/filter, render, fact-index build/load, and projection-store load/save calls.
3. **Knowledge reachability has the best JSON timing parity.** Its metadata includes rounded phase timings, candidate counts, candidate-kind counts, loss-stage counts, algorithmic counters, source counts, scan counts, index timings, truncation reason, limit, and max-seconds.
4. **Projection build diagnostics are reusable by multiple callers.** `ProjectionBuildDiagnostics` provides an optional common object for state projection subphase timings and counters.
5. **Observation ingestion diagnostics are operator-useful for source comparison.** The output separates source collection, normalization, event generation + ledger write, totals, promoted facts, and throughput.
6. **Execution status is deliberately non-authoritative.** `ExecutionStatus` is explicitly transient and renderer-independent, which avoids silently turning progress rendering into state truth.
7. **Snapshot policy has durable comparison metadata for supported audit snapshot kinds.** Audit snapshot metadata records snapshot id, kind, command, db, latest event id, event count, projection version, and git metadata; snapshot policy can render and return JSON readiness/comparison evidence.
8. **Some diagnostic visibility is registered.** `current_facts_cache_debug`, `knowledge_reachability`, `snapshot_policy_audit`, `projection_shape`, and `diagnostic_shape_audit` are present in the diagnostic inventory/shape-audit code.

## Adversarial findings

### 1. Reliable enough surfaces are local, not system-comparable

The reliable surfaces are reliable only within their own boundary:

- `--current-facts-cache-debug` is useful for one current-facts command path.
- `--state-build-cache-debug` is useful for one state-summary/cache boundary.
- `--knowledge-reachability-audit` is useful for that audit's own candidate pipeline.
- `--observe-timings` is useful for one observation collection/normalization/ingestion pipeline.

They do not share a stable phase vocabulary, a run id, a common schema, or shared persistence. This makes them weak evidence for comparing Seed command execution across surfaces.

### 2. Timing names are inconsistent across surfaces

Examples of non-aligned vocabulary:

- State-build uses `projection replay / build`, `compact StateSummary derivation`, `operator state_summary derivation`, and `rendering`.
- Current-facts uses `full projection rebuild (event replay)`, `read-model build`, `render`, `query/filter + render`, and `stdout/output time`.
- Knowledge reachability uses `load_state`, `discover_candidates`, `build_indexes`, `evaluate`, `render`, and `total`.
- Observation ingestion uses `source collection`, `normalization`, `event generation + ledger write`, and `total`.
- Projection-store wrapping in current-facts labels load as `cache metadata lookup + cached projection row load`, while state-build labels a similar thing `state cache lookup` or `state summary snapshot lookup`.

These are understandable to a human reading each implementation, but they are not stable enough for Seed to compare execution phases across commands.

### 3. Phase boundaries are inconsistent

- Current-facts includes `stdout/output time` but hard-codes it to `0.0`, so output cost is named but not measured.
- State-build measures a placeholder `rendering` function rather than the real formatter; that phase is structurally present but misleading as command-render cost.
- Knowledge reachability includes a `render` phase in the build result before actual CLI formatting/JSON serialization, so its render timing is not equivalent to current-facts or state-build output timing.
- Observation ingestion combines event generation and ledger write into one phase, while `ObservationIngestor.ingest_many()` separately emits transient statuses for generating events and passes ledger append progress through the ledger only if a status consumer exists.

### 4. Cache/snapshot paths are visible but incomplete for slow-command explanation

Visible:

- State-build cache debug reports summary cache hit/miss, projection cache hit/miss, current last-event id, cached summary last-event id, and cached projection last-event id.
- Current-facts cache debug wraps projection store snapshot/index load and save calls.
- Projection cache status reports state snapshot hit/miss and last-event ids.
- Snapshot policy reports snapshot counts, latest snapshot age, comparison availability, and recommendation status.

Missing or weak:

- There is no single cache-path schema across state cache, state summary cache, fact-index cache, and audit snapshots.
- Current-facts reports `state cache: hit|miss|unavailable`, but fact-index cache status is only inferable through timing names, not a structured status field.
- Knowledge reachability metadata initializes `cache = {"state": "miss", "summary": "miss", "projection": "miss"}` but does not actually use the projection cache path in `StateProjector(ledger).project(workspace_id)`, making cache metadata look more meaningful than it is.
- Audit snapshots record command and event/projection metadata, but not execution phase timings or command-run timing participation.

### 5. Important phases are missing timing entirely

Supported by inspected implementation gaps:

- CLI argument parsing and command dispatch are not timed by these surfaces.
- Database connection close/finalization is generally outside timing reports.
- Actual final `print()`/stdout write is not measured; current-facts reports a zero output time and state-build times a placeholder.
- Runtime command handling has historical trace views, but the inspected runtime trace/status path does not provide a unified phase-timing record for model classification, policy, tool execution, state projection, rendering, and ledger append in one comparable schema.
- Snapshot creation persists metadata and payload, but not the time spent creating payloads, writing files, collecting git metadata, or comparing snapshots.

### 6. Timing persistence is fragmented

- Knowledge reachability timings can be returned in JSON metadata.
- Snapshot metadata is persisted, but execution timings are not part of the audit snapshot schema.
- State-build and current-facts debug timings are rendered only.
- Projection build diagnostics are in-memory and optional.
- Observation ingestion diagnostics are in-memory and formatted only when requested.
- Execution status updates are transient and explicitly non-authoritative.
- Runtime trace is persisted through events, but transient execution status is not a timing record.

### 7. Debug surfaces do not expose enough evidence for run comparison

A run comparison would need stable identity, shared timing fields, consistent phase names, command arguments, cache/snapshot participation, input event high-water mark, projection versions, rendered output mode, and environment/db path. Current implementation has pieces of this, but not together:

- State-build has event ids and cache statuses but no JSON/run schema.
- Current-facts has detailed local timings but no structured event-id fields in the report dataclass.
- Knowledge reachability has JSON timings/counters but no projection-cache participation beyond a fixed cache metadata dict.
- Audit snapshots preserve command/git/event metadata but not timings.
- Runtime trace can show historical run events, but it is not integrated with the timing debug reports.

### 8. Duplicated timing concepts are implemented differently

- Local `timed()` closures appear separately in state-build cache debug and current-facts timing.
- `_ReachabilityTimer` uses context-manager phases and structured progress emission.
- `ProjectionBuildDiagnostics.timed()` accumulates repeated phase names, unlike local timing lists that append repeated names.
- `_TimingProjectionStore` measures store calls by wrapping methods, while state-build measures store calls by wrapping caller lambdas.
- Observation ingestion diagnostics are collected by the collection service and rendered in a separate formatter, rather than sharing `ProjectionBuildDiagnostics`-style semantics.

The duplication is not a code-quality complaint by itself; the adversarial issue is that the same conceptual evidence (`timing a phase`) has different accumulation, naming, rendering, and JSON behavior depending on which surface produced it.

## Missing evidence

- A stable cross-command phase vocabulary.
- A shared timing schema for rendered output, JSON output, persisted snapshots, and in-memory diagnostics.
- Explicit timing-boundary declarations that say what each phase includes and excludes.
- Per-run identifiers tying timing/debug reports to runtime traces, event-ledger high-water marks, cache participation, and command arguments.
- Structured cache participation fields for summary cache, state cache, fact-index cache, and audit snapshots.
- Snapshot participation fields in normal timing reports: whether a command created, reused, skipped, or compared snapshots.
- JSON timing parity for state-build cache debug and current-facts cache debug.
- Real output/render timing parity; current placeholder/zero output timings are not comparable evidence.
- Evidence that diagnostic inventory/shape audit covers `state_build_cache_debug` specifically. The inspected registry covers `current_facts_cache_debug` but not an equivalent entry for `--state-build-cache-debug`.

## Inconsistent terminology

| Concept | Term variants found |
| --- | --- |
| State projection work | `projection replay / build`, `full projection rebuild (event replay)`, `load_state`, `project_state_with_cache`, `StateProjector.project` |
| Cache lookup | `state summary snapshot lookup`, `state cache lookup`, `cache metadata lookup + cached projection row load`, `fact-index cache lookup/load` |
| Cache outcome | `summary_cache_status`, `state_cache_status`, `projection_cache_status`, `cache_status`, `state cache: hit`, `cache: hit` |
| Output/render | `rendering`, `render`, `query/filter + render`, `stdout/output time` |
| Total runtime | `total runtime`, `total`, observation `total`, reachability `total` |
| Snapshot/cache storage | `projection cache`, `state cache`, `state-build cache`, `summary snapshot`, `derived index snapshot`, `audit snapshot` |

## Fragile implementation areas

- **Misleading placeholder timing:** state-build records `rendering` by timing an empty placeholder function, not the final format call.
- **Hard-coded output timing:** current-facts appends `stdout/output time` as `0.0`, creating apparent precision without measurement.
- **Cache metadata that appears more active than it is:** knowledge reachability metadata exposes cache fields initialized to miss while using direct `StateProjector` projection.
- **Surface-specific local timers:** repeated local timing implementations make naming/accumulation drift likely.
- **Diagnostic registration gap:** `current_facts_cache_debug` is registered and shape-audited, but `state_build_cache_debug` does not appear as a peer diagnostic inventory entry in inspected registry searches.
- **Snapshot timing absence:** audit snapshots preserve useful metadata, but snapshot creation/comparison cost is not timing evidence.
- **Boundary ambiguity:** subphase timings from `ProjectionBuildDiagnostics` are appended into caller-specific reports, but callers use different outer labels for similar projection paths.

## Required questions answered

### 1. Which timing surfaces are reliable enough to support Seed self-observation?

Reliable enough for local self-observation:

- Current-facts cache debug for current-facts path timing.
- State-build cache debug for state-summary/cache path timing.
- Knowledge reachability timings for that audit's own candidate evaluation pipeline.
- Observation ingestion timings for source collection/normalization/ledger-write throughput.
- Projection cache status for narrow state snapshot hit/miss explanation.

Not reliable enough as a whole-system execution model because they lack shared identity, schema, vocabulary, JSON parity, and persistence.

### 2. Which timings are isolated, non-comparable, or misleading?

- Isolated: state-build, current-facts, reachability, observation ingestion, snapshot policy, and runtime trace/status each describe different command-local boundaries.
- Non-comparable: `rendering`, `render`, `query/filter + render`, and `stdout/output time`; `projection replay / build` versus `full projection rebuild (event replay)` versus `load_state`.
- Misleading: state-build placeholder rendering timing; current-facts zero stdout timing; knowledge reachability cache metadata initialized to miss without cache participation.

### 3. Are timing names consistent across surfaces?

No. Similar phases use different names, and identical-looking names do not always share boundaries.

### 4. Are phase boundaries consistent?

No. Render/output, projection build, cache lookup, event generation, ledger write, and total runtime boundaries vary by surface.

### 5. Are cache/snapshot paths visible enough to explain slow commands?

Partially. Cache hit/miss and last-event ids are visible for some state paths, and snapshots expose policy/comparison metadata. They are not sufficient to explain slow commands across all surfaces because fact-index status, snapshot participation, final rendering, db close, and command dispatch are missing or unstructured.

### 6. Are important phases missing timing entirely?

Yes: CLI parse/dispatch, final stdout write, database close/finalization, runtime/model/policy/tool phases as one timing schema, snapshot create/write/compare costs, and some cache/index participation fields.

### 7. Are timings persisted, rendered only, returned in JSON, or discarded?

All four patterns exist:

- Persisted: audit snapshot metadata, but not timing phases.
- JSON: knowledge reachability timings; snapshot policy fields; diagnostic inventory/shape output.
- Rendered only: state-build cache debug, current-facts cache debug, observation ingestion timings.
- Discarded/in-memory only: projection build diagnostics unless a caller renders them; transient execution status.

### 8. Do debug surfaces expose enough evidence for Seed to compare runs?

No. They expose useful fragments but lack a shared run id, schema, phase vocabulary, cache/snapshot participation fields, timing boundary declarations, and JSON parity.

### 9. Are there duplicated timing concepts implemented differently?

Yes. There are local closures, a reachability context-manager timer, projection diagnostics with additive phase accumulation, store wrapper timings, observation ingestion diagnostics, and transient status progress. These implement overlapping timing/debug concepts differently.

### 10. If this were truly Seed observing his own execution, what would be expected but absent?

See the next section.

## If this were Seed, it would have...

- stable phase vocabulary across state-build, current-facts, reachability, observation ingestion, snapshots, and runtime trace;
- per-surface execution path visibility that uses the same schema for command path, cache path, snapshot path, render path, and ledger path;
- cache path normalization for state cache, summary cache, fact-index cache, and projection cache status;
- snapshot participation fields in timing/debug reports, not only separate audit snapshot metadata;
- JSON timing parity for human-only timing surfaces;
- run comparison evidence tying timings to command args, workspace, db path, last-event id, projection version, cache status, and run id;
- timing boundary declarations for every phase name;
- real render/output timing instead of placeholder or hard-coded zero output timing;
- a diagnostic inventory entry and shape-audit spec for every timing/debug operational surface, including `--state-build-cache-debug` as a peer of `--current-facts-cache-debug`.

## Commands executed

```text
pwd && rg --files -g 'AGENTS.md' -g '!README*' -g '!*.pyc' | xargs -r -I{} sh -c 'echo --- {}; cat {}' && git status --short
rg -n "timing|timer|elapsed|duration|debug|snapshot|projection cache|diagnostic-inventory|diagnostic-shape|knowledge-reachability|runtime trace|execution status|state-build|current-facts|observation" . --glob '!*.pyc' --glob '!htmlcov/**' --glob '!node_modules/**'
sed -n '2880,3260p' scripts/seed_local.py
sed -n '3260,3520p' scripts/seed_local.py
sed -n '1470,1538p' scripts/seed_local.py
sed -n '1848,1995p' scripts/seed_local.py
rg -n "CurrentFactsCache|current_facts_cache|ProjectionBuildDiagnostics|class ProjectionBuildDiagnostics|timings|elapsed_seconds|observe_timings|format_observation_ingestion_diagnostics|trace-run|ExecutionStatus|runtime" scripts seed_runtime tests --glob '!*.pyc'
sed -n '5000,5190p' scripts/seed_local.py
sed -n '1,220p' seed_runtime/state.py
sed -n '1,220p' seed_runtime/knowledge_reachability.py
sed -n '1,220p' seed_runtime/projection_store.py
sed -n '1,180p' seed_runtime/execution_status.py
sed -n '220,520p' seed_runtime/knowledge_reachability.py
sed -n '220,520p' seed_runtime/projection_store.py
sed -n '180,320p' seed_runtime/execution_status.py
sed -n '1,220p' seed_runtime/observations.py
sed -n '320,460p' seed_runtime/projection_store.py
sed -n '680,770p' scripts/seed_local.py
sed -n '1,220p' seed_runtime/audit_snapshots.py
sed -n '1,220p' seed_runtime/snapshot_policy_audit.py
sed -n '1,160p' seed_runtime/diagnostic_inventory.py
sed -n '1,120p' seed_runtime/diagnostic_shape_audit.py
rg -n "state_build_cache_debug|current_facts_cache_debug|snapshot_policy|observation_inventory|diagnostic_shape|projection_shape|knowledge_reachability" seed_runtime/diagnostic_inventory.py seed_runtime/diagnostic_shape_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
sed -n '500,560p' seed_runtime/diagnostic_shape_audit.py
sed -n '535,565p' seed_runtime/diagnostic_inventory.py
sed -n '660,680p' seed_runtime/diagnostic_inventory.py
sed -n '615,640p' seed_runtime/diagnostic_inventory.py
```

## Files changed

- `docs/execution_timing_adversarial_audit.md`

## LOC changed

- Added approximately 259 lines.
- Modified 0 implementation lines.
- Deleted 0 lines.

## Tests run

No automated tests were run because this change only adds an adversarial audit document and intentionally does not modify implementation, diagnostic registry entries, shape-audit specs, or tests.
