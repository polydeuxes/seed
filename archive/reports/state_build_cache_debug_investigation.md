# State-Build Cache Debug Investigation

## Scope

This is a bounded implementation investigation of the existing `--state-build-cache-debug` path. It does not implement ownership recovery, redesign cache behavior, add a diagnostic framework, change CLI behavior, change schemas, change projections, or change read-model behavior.

The investigation asks whether the repository currently contains a recurring implementation responsibility suitable for bounded ownership recovery under the candidate name **State-Build Cache Debug**.

## Implementation evidence reviewed

### Primary implementation path

- `scripts/seed_local.py` registers `--state-build-cache-debug` as a CLI flag described as printing read-only state-build cache eligibility, hit/miss status, timing details, and projection build counters.
- `scripts/seed_local.py` dispatches that flag by calling `state_summary_cache_debug_from_args(args)` and then `format_state_summary_cache_debug_report(...)`.
- `StateSummaryCacheDebugReport` contains a separated `_StateBuildVisibilityPayload`, a `_ProjectionCacheDiagnosticPayload`, and top-level local timings.
- `state_summary_cache_debug_from_args(...)` opens projection-store and ledger resources, lists events, computes read-model dependency identity, looks up the state-summary cache, optionally short-circuits on summary-cache hit, looks up and decodes projection state cache, runs projection replay/build with `ProjectionBuildDiagnostics`, constructs state-summary read models, saves the state-summary snapshot, selects projection diagnostics, and returns one debug report.
- `format_state_summary_cache_debug_report(...)` renders cache eligibility, summary cache status, projection cache status, current/cached event ids, notes, projection counters, local timings, and projection subphase timings.

### Adjacent cache/read-model implementation

- `projected_state_summary_from_args(...)` is the normal state-build path. It uses the dependent state-summary read-model cache, resolves a summary cache lookup, short-circuits on hit, otherwise builds projected state, constructs `StateSummary` and operator summary read models, updates cache-status fields, and publishes a `SummaryProjectionSnapshot`.
- `seed_runtime/projection_store.py` defines `SummaryProjectionSnapshot` and `ProjectionStore.load_summary_snapshot(...)` / `save_summary_snapshot(...)`, including dependency fields `state_projection_version` and `state_last_event_id`.

### Tests reviewed

- `tests/test_seed_local_script.py` proves the cache-debug path is read-only with respect to ingestion and tool execution.
- `tests/test_seed_local_script.py` proves a cold run reports a state-build cache miss, a warm run reports a state-build cache hit, and the warm summary hit skips projection cache work and projection replay/build subphase timings.
- `tests/test_seed_local_script.py` proves `StateSummaryCacheDebugReport.visibility` is separated from `StateSummaryCacheDebugReport.projection_diagnostics` while legacy property accessors remain available.
- `tests/test_projection_store.py` proves the normal state-build CLI exposes state-build cache miss/hit behavior and that summary cache invalidation depends on full-state projection snapshot identity.

### Previously completed adjacent families reviewed

- `projection_diagnostics_family_completion_audit.md` concludes the Projection Diagnostics producer chain is complete: measurement, aggregation, payload, and selection are now separate from consumers.
- `read_model_ownership_family_completion_audit.md` concludes the Read-Model Ownership chain is complete and explicitly treats the remaining direct save in state-summary cache debug as timing/debug visibility pressure rather than another recurring read-model lifecycle boundary.
- `execution_visibility_slice_004.md` selected current-facts cache debug because visibility output and diagnostic evidence were flattened there, while naming `state_build_cache_debug` as a remaining pressure that constructs state-build visibility, projection cache diagnostics, timing, and counter details in one report path.

## Recurring implementation patterns

### 1. State-build orchestration recurs as a debug-local measurement path

The debug path repeats the same broad state-build lifecycle as the normal state-summary path, but with extra timing and cache-status instrumentation:

```text
open store / ledger
→ list events and recover current state boundary
→ lookup dependent summary read-model cache
→ maybe short-circuit on summary cache hit
→ inspect state projection cache
→ replay/build projected state when needed
→ build state-summary read models
→ publish dependent summary cache
→ assemble debug report
→ render presentation
```

This is implementation evidence for a coherent debug lifecycle, but it is also evidence that the lifecycle is orchestration-heavy. The path is not a new projection engine or a new read-model builder; it invokes existing projection, cache, diagnostics, and read-model owners.

### 2. Cache visibility and projection diagnostic consumption are compressed in one report-building function

`state_summary_cache_debug_from_args(...)` owns summary-cache status (`hit`, `miss`, `unavailable`), state/projection-cache status (`hit`, `miss`, `skipped`, `unavailable`), event-id visibility, debug notes, local timings, projection diagnostic selection, projection counters, and final report construction in one function.

The report data shape has a partial separation:

```text
_StateBuildVisibilityPayload
!=
_ProjectionCacheDiagnosticPayload
```

However, the producer function still constructs both payloads and owns the surrounding cache/read-model/report lifecycle.

### 3. Summary-cache consumption and publication are adjacent to read-model construction

The debug path both consumes and publishes the dependent state-summary cache. It loads `SummaryProjectionSnapshot` through the read-model cache lookup boundary, reconstructs `StateSummary` on hit, builds `StateSummary` and operator summary on miss, and saves a new `SummaryProjectionSnapshot` when eligible.

This is recurring with the normal `projected_state_summary_from_args(...)` path. The difference is that the debug path wraps those steps in timing labels and uses their results as visibility/report evidence.

### 4. Report payload construction and presentation are still local to the state-build cache-debug surface

The report constructor and formatter are specific to state-build cache debug. The formatter consumes report properties and renders sections for cache eligibility, state-build cache status, projection cache status, event ids, notes, projection/build structure counts, timings, and projection replay/build subphase timings.

This supports a consumer-specific interpretation boundary: the same projection and read-model evidence is interpreted for the cache-debug operator surface rather than for normal `--state-build` output.

## Counterexamples and limiting evidence

### Counterexample 1: State-Build Cache Debug may be orchestration, not a durable owner

The strongest implementation function primarily coordinates already-owned mechanisms:

- projection store and event ledger access;
- read-model dependency identity and cache lookup;
- projection replay/build and projection cache;
- projection diagnostics payload/selection;
- state-summary read-model construction;
- summary cache publication;
- debug report formatting.

This means the candidate family is not clearly an independent domain owner. It may instead be a consumer-specific orchestration surface whose pressure should be reduced only where existing completed owners expose better handoffs.

### Counterexample 2: Several pressures already belong to completed owners

The evidence does not support reopening adjacent completed families:

- Projection measurement, diagnostic aggregation, payload production, and diagnostic selection are already explicitly owned by Projection Diagnostics.
- Read-model construction inputs, dependency identity, cache lookup, construction, and cache publication are already explicitly owned by Read-Model Ownership.
- Execution/status/timing/cache visibility has an established Execution Visibility family, including previous work separating state-build visibility from projection-cache diagnostics.
- Projection cache storage and publication are not owned by the state-build cache-debug report; the debug path only observes/uses them.

### Counterexample 3: `--state-build-cache-debug` is not registered as a diagnostic inventory surface

Repository searches show `current_facts_cache_debug` in `seed_runtime/diagnostic_inventory.py`, `seed_runtime/diagnostic_shape_audit.py`, and their tests, but do not show a corresponding `state_build_cache_debug` entry. The CLI flag exists and is operationally diagnostic-like, but the existing diagnostic governance implementation does not currently treat it as a registered diagnostic surface.

Because this investigation must not add runtime surfaces or inventory entries, this is missing evidence for treating State-Build Cache Debug as a mature diagnostic ownership family today.

### Counterexample 4: Existing tests preserve behavior, but not a full owner lifecycle

The tests prove read-only behavior, warm/cold cache behavior, normal summary-output preservation, and visibility-vs-projection-diagnostics separation. They do not yet prove a complete bounded State-Build Cache Debug lifecycle with named owner boundaries for orchestration, report payload construction, report presentation, and consumer-specific interpretation.

## Answers to central questions

### 1. Does a recurring State-Build Cache Debug responsibility currently exist?

**Yes, but only as a candidate consumer/orchestration responsibility.**

Implementation evidence shows a recurring state-build cache-debug lifecycle: cache eligibility, summary-cache lookup, projection-cache inspection, projection execution when needed, projection diagnostics consumption, read-model construction, summary-cache publication, report assembly, and presentation. The strongest evidence is that these steps are not merely prose; they are implemented in `state_summary_cache_debug_from_args(...)`, preserved by `StateSummaryCacheDebugReport`, and rendered by `format_state_summary_cache_debug_report(...)`.

However, the current evidence is not strong enough to say it is already a mature independent owner. Much of the function coordinates completed owners rather than owning a new core behavior.

### 2. If yes, where is the strongest implementation evidence?

The strongest implementation evidence is the `state_summary_cache_debug_from_args(...)` path in `scripts/seed_local.py`, because it contains the whole implemented chain:

- cache eligibility and ineligibility reason selection;
- current event boundary lookup;
- summary read-model cache lookup;
- warm summary-cache short-circuit;
- state projection cache lookup and snapshot decode;
- projection replay/build with `ProjectionBuildDiagnostics`;
- read-model construction for compact and operator state summaries;
- summary snapshot save;
- projection diagnostic selection;
- construction of `_StateBuildVisibilityPayload`, `_ProjectionCacheDiagnosticPayload`, and `StateSummaryCacheDebugReport`.

The strongest test evidence is `test_state_summary_cache_debug_separates_visibility_from_projection_diagnostics(...)`, which proves a recovered local boundary already exists inside the report shape, and `test_cli_state_summary_cache_debug_reports_warm_summary_hit(...)`, which proves the cache-debug lifecycle has observable warm/cold behavior.

### 3. What implementation responsibilities currently appear compressed?

The following responsibilities are compressed in or around the state-build cache-debug path:

1. **State-build orchestration**: opening resources, deriving current event identity, deciding cache-eligible paths, and coordinating projection/read-model work.
2. **Cache visibility**: summary-cache status, state/projection-cache status, cached event ids, current event id, and debug notes.
3. **Projection diagnostic consumption**: converting `ProjectionBuildDiagnostics.payload` into selected timings and counters for this consumer.
4. **Summary-cache consumption**: dependent read-model cache lookup and warm-hit reconstruction.
5. **Read-model consumption/construction**: construction of compact `StateSummary` and operator summary when the summary cache misses.
6. **Summary-cache publication**: saving `SummaryProjectionSnapshot` from debug-path construction.
7. **Report payload construction**: assembling visibility payload, projection diagnostic payload, and top-level timings.
8. **Report presentation**: formatting the state-build cache-debug report sections and deciding which evidence appears as operator text.
9. **Consumer-specific interpretation**: interpreting summary-cache hits as projection-cache skip, interpreting state-cache snapshots as debug status, and exposing projection counters only as debug structure counts.

### 4. Which responsibilities are already sufficiently explicit because of previously completed families?

The following should not be treated as new State-Build Cache Debug ownership without contrary implementation evidence:

- **Projection Diagnostics** already owns producer-side measurement, aggregation, payload snapshotting, and diagnostic selection. State-build cache debug consumes selected projection diagnostics; it does not own producing them.
- **Read-Model Ownership** already owns construction inputs, dependency identity, cache lookup, construction, and cache publication boundaries. State-build cache debug uses those boundaries for the state-summary read model.
- **Execution Visibility** already owns the general visibility pattern around status/timing/cache diagnostics and has prior slices separating visibility output from diagnostic evidence.
- **Projection Publication / projection cache storage** owns projection snapshot storage behavior. State-build cache debug observes and uses projection cache state; it does not define projection cache validity or storage semantics.

### 5. Should State-Build Cache Debug become the next implementation responsibility family?

**Recommended answer: yes, but only after one bounded pre-slice or readiness check confirms that the target is the consumer/debug lifecycle rather than cache redesign or reopened upstream families.**

The candidate is mature enough for a bounded ownership-family investigation because the implementation contains a stable, tested, recurring chain and a partially recovered internal boundary. It is not mature enough for immediate broad recovery if the proposed owner is vague. The next family must be scoped narrowly around the consumer/debug surface, for example:

```text
State-Build Cache Debug Orchestration
!=
State-Build Cache Debug Report Payload
!=
State-Build Cache Debug Presentation
```

or another implementation-backed boundary discovered by the pre-slice.

It should not begin as cache redesign, read-model redesign, projection-diagnostics work, or diagnostic-framework work.

## Supported conclusions

1. The repository contains a recoverable candidate responsibility around the state-build cache-debug consumer lifecycle.
2. The candidate is strongest where `state_summary_cache_debug_from_args(...)` combines cache visibility, projection diagnostic consumption, read-model construction/consumption, summary-cache publication, report assembly, and presentation preparation.
3. Existing report dataclasses already show partial local boundary recovery between state-build visibility and projection-cache diagnostics.
4. Projection Diagnostics, Read-Model Ownership, Projection Publication, and Execution Visibility should remain closed unless new evidence shows compression inside their owned producer boundaries.
5. Any future recovery should be bounded to implementation-local cache-debug consumer/report responsibilities.

## Unsupported conclusions

1. Unsupported: State-Build Cache Debug is a new cache architecture owner.
2. Unsupported: State-Build Cache Debug owns projection execution or projection diagnostic production.
3. Unsupported: State-Build Cache Debug owns read-model construction semantics or dependency identity.
4. Unsupported: State-Build Cache Debug is currently a fully registered diagnostic inventory/shape-audit family.
5. Unsupported: The state-build cache-debug lifecycle should be changed, optimized, or redesigned as part of this investigation.

## Confidence

**Medium-high** that State-Build Cache Debug contains a recurring recoverable consumer/debug responsibility.

**Medium** that it should be the next ownership family, because the implementation pressure is real and localized, but its strongest evidence is still orchestration across completed owners. The family would need a narrow first slice to avoid reopening completed Projection Diagnostics, Read-Model Ownership, Projection Publication, or Execution Visibility work.

## Recommended next action

Begin a bounded readiness slice only if the next task can keep the owner narrow and implementation-local. The recommended first target is:

```text
State-Build Cache Debug Report Assembly
!=
State-Build Cache Debug Presentation
```

or, if implementation evidence during that slice points earlier in the chain:

```text
State-Build Cache Debug Orchestration
!=
State-Build Cache Debug Payload Construction
```

Before any runtime diagnostic registration or recordable output is added or changed, follow the repository diagnostic visibility contract: update diagnostic inventory, diagnostic shape-audit specs, and tests proving inventory and shape-audit coverage. This investigation itself does not add or modify such a surface.
