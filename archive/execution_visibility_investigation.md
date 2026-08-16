# Execution Visibility Investigation

This investigation is documentation-only. It does not add CLI flags, runtime instrumentation, projection behavior, cache behavior, diagnostic inventory entries, shape-audit specs, or tests. It records implementation-backed execution evidence that already exists in the repository.

## Implementation summary

Seed already preserves several execution-characterization observations, but they are distributed across projection/cache helpers, selected inquiry surfaces, observation ingestion, and diagnostic metadata. The strongest existing evidence is:

- projection construction can record non-authoritative subphase timings and event-kind counters through `ProjectionBuildDiagnostics`;
- projection-cache execution returns a structured `StateCacheStatus` that distinguishes cache hit, full rebuild, and incremental replay, including snapshot/current event ids and events applied;
- state-build cache debug and current-facts cache debug render phase timings for cache lookup, projection build/replay, read-model work, rendering, and total runtime;
- knowledge reachability preserves timing metadata for load-state/cache, discovery/evaluation/read-model/index phases, render, and total runtime;
- observation ingestion can optionally render source collection, normalization, event generation plus ledger-write time, total time, and observation/event counters;
- audit snapshots preserve local snapshot metadata, and snapshot policy/impact/reference-selection surfaces expose snapshot count, latest snapshot, comparison availability, and comparison pairs.

Seed does not currently have a single universal execution trace for every inquiry command. Existing evidence can explain selected surfaces and projection/cache paths, but it stops at isolated phase measurements and cache/status metadata rather than a full causal profile for arbitrary commands.

## Execution evidence recovered

### Projection construction diagnostics

`ProjectionBuildDiagnostics` is the repository's built-in projection timing container. It records named timings using `time.perf_counter`, accumulates repeated phase names, and records integer counters. Its own docstring explicitly marks the timings as optional and non-authoritative, so these timings are implementation-backed observations but not semantic projection authority.

Implementation-backed observations include:

- projection input event materialization;
- projection event count;
- per-event-kind counters;
- event replay timing;
- finalization subphase timings;
- full projection rebuild timing when routed through `project_state_with_cache`.

### Projection-cache status

`project_state_with_cache` exposes execution-path evidence through `StateCacheStatus` and status phases. It loads the current event list, checks the projection snapshot, returns immediately on exact cache hits with `events_applied=0`, attempts incremental replay from a compatible snapshot, and otherwise performs a full projection replay and saves a new snapshot. The status includes cache hit/miss, projection version, snapshot last event id, current last event id, incremental replay flag, and events applied.

### State-build cache debug

The state-build cache debug path measures cache eligibility and phase timings without ingesting observations or executing tools. It separately measures projection-store open, ledger open, event listing/current last-event lookup, summary snapshot lookup, state cache lookup, snapshot decode, projector construction, projection replay/build, summary derivation, summary snapshot save, rendering, and total runtime. It also renders projection subphase timings and projection counters when a build occurs.

### Current-facts cache debug

The current-facts cache debug path is a read-only timing report for the current-facts State path. It wraps projection-store operations to time cache metadata and cached projection row load, snapshot save, fact-index cache lookup/load, and fact-index cache save. It then reports whether the state path was a cache hit, incremental replay miss, full rebuild miss, or unavailable, and measures read-model build or query/filter plus render.

### Knowledge reachability timing metadata

Knowledge reachability has an internal timer that records named phase timings with `time.monotonic`, emits optional progress messages, preserves total time, and returns metadata containing rounded phase timings, cache metadata, and index timings. The formatted table prints a timing section when metadata is supplied.

### Observation ingestion timings

Observation ingestion can render comparable source-inspection timings for source collection, normalization, event generation plus ledger write, total time, total observations, and total events. The CLI only prints these diagnostics when `--observe-timings` is supplied for observation-ingestion paths.

### Runtime/tool execution phase evidence

Tool execution records phase names for failures such as input validation, policy denial, confirmation/approval pending, and execution/output validation. This is execution-path evidence for tool calls, but it is not a duration profile.

## Execution timing surfaces

The following existing surfaces expose timing evidence:

| Surface | Timing evidence currently exposed | Boundary |
| --- | --- | --- |
| `--state-build-cache-debug` | cache lookup/decode, projection replay/build, summary derivation, rendering, total runtime, projection subphases, projection counters | state-build/read-model cache debug |
| `--current-facts-cache-debug` | projection-store cache operations, state cache hit/miss path, projection subphases, read-model build, fact-index load/build, query/filter/render, total | current facts inquiry/debug |
| `--knowledge-reachability-audit` / JSON | load-state/cache, candidate discovery/evaluation, read-model/index timings, render, total | diagnostic/inquiry audit |
| observation ingestion with `--observe-timings` | source collection, normalization, event generation plus ledger write, total, observation/event counts | observation ingestion |
| projection helpers used by many projected-state consumers | optional `ProjectionBuildDiagnostics` timings and counters; `StateCacheStatus` path metadata | projection/cache implementation |
| execution status consumers | progress/status phases such as projection cache load, projection replay, incremental projection replay, and projection save | runtime/projection status, not duration |
| tool execution failure events | failure phase names | runtime/tool execution, not duration |

## Execution phase inventory

Only phases backed by implementation evidence are listed.

### Projection and cache phases

- projection cache load;
- cached projection load/materialize;
- full projection rebuild;
- projection input event materialization;
- event replay;
- incremental projection replay;
- projection save;
- finalization: initial alias projection;
- finalization relationship/entity/graph/inference subphases recorded by `StateProjector.finalize`;
- projection event-kind counters.

### State-build and read-model phases

- projection store open;
- ledger open;
- event listing/current last event lookup;
- state summary snapshot lookup;
- state summary snapshot decode/payload reconstruction;
- state cache lookup;
- state snapshot decode/State reconstruction;
- state projector construction;
- projection replay/build;
- fact-support construction if separable;
- compact `StateSummary` derivation;
- operator state summary derivation;
- state summary snapshot save;
- rendering;
- total runtime.

### Current-facts phases

- cache metadata lookup plus cached projection row load;
- snapshot save;
- fact-index cache lookup/load;
- fact-index cache save;
- state cache hit path;
- state cache miss path with incremental event replay;
- state cache miss path with full projection rebuild;
- full projection rebuild when no cache is available;
- read-model build;
- fact-index build/load;
- query/filter plus render;
- stdout/output time;
- total.

### Knowledge reachability phases

- load state/cache;
- projected entities, projected facts, fact support, source-navigation index, read-model, and inquiry-orientation index timings;
- candidate discovery and evaluation timings;
- render;
- total.

### Observation ingestion phases

- source collection;
- normalization;
- event generation plus ledger write;
- total.

### Runtime/tool phases without timing

- input validation;
- policy denial/confirmation/approval handling;
- execution/output validation failure;
- runtime trace event snapshots.

## Snapshot-related execution visibility

### Projection snapshots and cache reuse

Projection snapshots are explicitly derived, reusable projected-state snapshots owned by `ProjectionStore`, not the event ledger. Snapshot records preserve workspace, projection name/version, last event id, last event created time, state payload, and creation time. `project_state_with_cache` exposes exact-hit reuse, stale/miss behavior, safe full rebuild fallback after snapshot decode/load failures, and incremental replay from a compatible snapshot.

### Dependent read-model snapshots

State-summary snapshots and derived fact-index snapshots are dependent on the state projection version and state last event id. Loading those snapshots requires matching the associated state projection identity, so the implementation preserves whether the dependent read-model cache can be reused for the current state projection.

### Audit snapshots

Audit snapshot files preserve kind, command, seed database path, latest event id, event count, projection version, snapshot format version, creation time, git metadata, and payload. Supported local audit snapshot kinds are `observation_inventory` and `ownership_discrepancies`.

### Snapshot comparison and policy

Impact audit compares latest comparable snapshot pairs for supported snapshot kinds and reports coverage when a surface is not snapshotted or lacks comparison data. Snapshot policy audit reports latest snapshot id, latest snapshot age, snapshot count, comparison availability, comparison usefulness, status, recommendation, reason, repository context health, and operational surfaces constrained by snapshot health. Reference selection can choose a previous comparable snapshot when impact-audit evidence supplies a comparable pair.

### Snapshot debugging

Existing debug visibility includes state-cache status and state-build cache debug, which report cached/current last-event ids, cache eligibility, summary-cache and state-cache status, and timing for cache lookup/decode/replay/build. Current-facts cache debug reports the state cache path and fact-index cache load/build timings.

## Can Seed determine why one execution is slower than another?

For selected surfaces, Seed can compare implementation-backed phase timings and cache-path metadata:

- state-build cache debug can distinguish summary-cache hit, state-cache lookup/decode, projection replay/build, summary derivation, rendering, and total runtime;
- current-facts cache debug can distinguish state cache hit, incremental replay miss, full projection rebuild miss, fact-index cache/load, read-model build, query/filter/render, and total;
- knowledge reachability can compare load-state/cache, candidate discovery/evaluation, read-model/index, render, and total timings;
- observation ingestion can compare collection, normalization, event generation plus ledger write, total time, observation count, and event count.

Where implementation evidence stops:

- not every inquiry surface emits or preserves timing metadata;
- status phases are progress labels, not durations unless a timing/debug surface wraps them;
- runtime/tool execution failure phases identify where a failure occurred but do not provide elapsed time;
- projection timings are explicitly non-authoritative diagnostics;
- the repository does not currently preserve a universal per-command execution trace that causally attributes all elapsed wall time across every command.

## Ownership of execution visibility

Execution visibility belongs to a combination of layers:

- runtime/status infrastructure owns progress/status phase emission;
- projection owns optional projection build timings, counters, and projection replay/finalization phase names;
- projection cache owns snapshot reuse/miss/incremental/full rebuild status and snapshot persistence semantics;
- individual inquiry/debug surfaces own command-specific timing reports such as state-build cache debug, current-facts cache debug, and knowledge reachability metadata;
- observation ingestion owns source collection/normalization/event-write timing diagnostics;
- diagnostic infrastructure owns inventory/shape declarations stating whether debug/diagnostic surfaces write the event ledger, mutate the cluster, support record, or use projected state;
- audit snapshot infrastructure owns local snapshot creation, comparison, policy, and reference-selection evidence.

## Are execution timings implementation details or implementation-backed observations?

They are implementation-backed observations when exposed through existing reports or metadata, but they are not semantic authority. `ProjectionBuildDiagnostics` explicitly calls projected-State construction timings optional and non-authoritative. State-build/current-facts/knowledge-reachability/observation timing outputs are generated from real implementation timing calls and therefore are observations of that execution path. They remain diagnostic/read-only evidence rather than cluster truth or projection facts unless a separate existing diagnostic recording path records its own diagnostic findings.

## Can current implementation characterize where execution time was spent?

Current implementation can characterize where execution time was spent for the surfaces that expose phase timings. It cannot universally characterize every command. For supported surfaces, it can report a phase breakdown and cache path; for unsupported surfaces, it can often expose only isolated status labels, failure phases, or no timing evidence at all.

The current capability is therefore phase-local and surface-specific, not a repository-wide profiler or universal execution trace.

## Smallest truthful answer to “How did this command execute?”

Using existing evidence alone, the smallest truthful answer depends on the command:

- For state-build cache debug: Seed can say whether the summary cache or state projection cache was eligible/hit/missed, which snapshot/current event ids were involved, which projection path ran, how many projection events/kinds were seen, and how long cache lookup, projection, summary derivation, rendering, and total runtime took.
- For current-facts cache debug: Seed can say whether current facts used cached state, incremental replay, full rebuild, or no cache; whether a fact-index cache was loaded/built; and how long read-model/query/render and total execution took.
- For knowledge reachability: Seed can say how long state/cache loading, candidate discovery/evaluation, read-model/index work, render, and total execution took, with candidate and cache metadata.
- For observation ingestion with timings: Seed can say how long source collection, normalization, event generation plus ledger write, and total ingestion took, plus observation/event counts.
- For other inquiry surfaces without explicit timing metadata: Seed can only answer from implementation structure, cache/status metadata if invoked by shared helpers, and any recorded events/status/failure phases; it cannot truthfully provide a full elapsed phase breakdown.

## Implementation-backed gaps

- No universal per-command execution trace exists for every inquiry surface.
- Some execution evidence is rendered only on explicit debug/timing surfaces and is not persisted as cluster knowledge.
- Projection-build timings are intentionally non-authoritative diagnostics.
- Runtime/tool failure phases are preserved, but elapsed timing for those phases is not generally recorded.
- Snapshot policy/comparison visibility explains snapshot availability and reuse/comparison constraints, not the full runtime cost of snapshot creation or comparison.
- Cache status can identify hit/miss/incremental/full rebuild paths, but outside debug surfaces it does not automatically explain all downstream formatting/rendering costs.

## Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '!/.git' -g '!**/.git/**' && git status --short`
- `cat AGENTS.md && git status --short && rg -n "timing|duration|elapsed|snapshot|projection|read model|read-model|cache|phase|diagnostic|inventory|shape-audit|debug" -S .`
- `rg -n "perf_counter|time\\(|duration|elapsed|timing|phase|snapshot|cache_status|state_cache|debug" seed_runtime tests seed_cli.py pyproject.toml -S`
- `sed -n '1,120p' seed_runtime/state.py && sed -n '720,830p' seed_runtime/state.py && sed -n '1,220p' seed_runtime/projection_store.py && sed -n '1,180p' seed_runtime/diagnostic_inventory.py`
- `rg -n "current_facts_cache_debug|observe-timings|ProjectionCacheStatus|project_state_with_cache|cache_status|timings" seed_runtime scripts tests -S`
- `sed -n '533,620p' seed_runtime/projection_store.py && sed -n '3090,3335p' scripts/seed_local.py && sed -n '5020,5190p' scripts/seed_local.py && sed -n '160,245p' seed_runtime/knowledge_reachability.py && sed -n '420,500p' seed_runtime/knowledge_reachability.py`
- `sed -n '620,720p' seed_runtime/projection_store.py && sed -n '700,725p' scripts/seed_local.py && sed -n '7380,7420p' scripts/seed_local.py && sed -n '1,120p' seed_runtime/audit_snapshots.py && sed -n '1,80p' seed_runtime/snapshot_policy_audit.py`

## Files inspected

- `AGENTS.md`
- `seed_runtime/state.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/knowledge_reachability.py`
- `seed_runtime/audit_snapshots.py`
- `seed_runtime/snapshot_policy_audit.py`
- `seed_runtime/impact_audit.py`
- `seed_runtime/reference_selection.py`
- `seed_runtime/execution.py`
- `seed_runtime/runtime_trace.py`
- `scripts/seed_local.py`
- related tests surfaced by ripgrep under `tests/`

## Files changed

- `docs/execution_visibility_investigation.md`

## LOC changed

- Added 265 lines.

## Tests run

No tests were run because this investigation only adds a documentation artifact and does not change implementation, diagnostic inventory, diagnostic shape-audit specs, or CLI behavior.

## Conclusion

Seed already preserves enough implementation-backed execution evidence to begin understanding how selected inquiry surfaces execute, especially projection/cache-backed state build, current facts, knowledge reachability, and observation ingestion. Additional execution visibility would be required before Seed could answer “How did this command execute?” with a complete phase-by-phase explanation for every inquiry surface. Current evidence is meaningful but surface-specific: it provides cache-path status, phase timings, counters, snapshot metadata, and comparison/policy visibility where existing implementations expose them, but not a universal execution profile.
