# Projection Diagnostics Family Completion Audit

## Scope

This is a bounded implementation completion audit of the Projection Diagnostics producer family. It does not implement a new ownership slice, diagnostic framework, runtime surface, CLI behavior, schema, projection redesign, or cache redesign.

Reviewed implementation areas:

- `ProjectionBuildDiagnostics`
- `_ProjectionDiagnosticAggregation`
- `_ProjectionDiagnosticPayload`
- `_ProjectionDiagnosticSelection`
- `StateProjector.project(...)`
- `StateProjector.project_from_state(...)`
- `StateProjector.finalize(...)`
- state-build cache debug
- current-facts timing
- projection cache diagnostic pass-through

Repository authority wins over architectural preference.

## Executive conclusion

Yes: the implementation now exposes a completed Projection Diagnostics producer lifecycle for the current implementation-local responsibility family:

```text
Projection Measurement

↓

Projection Diagnostic Aggregation

↓

Projection Diagnostic Payload

↓

Projection Diagnostic Selection

↓

Consumers
```

The strongest remaining implementation pressure no longer appears to belong inside Projection Diagnostics. It appears downstream, primarily in **state-build cache debug** and **current-facts timing**, with additional consumer-side/cache-path pressure around projection cache debug/pass-through. Projection Diagnostics should not receive another ownership slice unless new implementation evidence shows recurring producer-side mixing that crosses measurement, aggregation, payload, or selection boundaries again.

Recommended next responsibility owner: **state-build cache debug**, with current-facts timing as the next most compelling adjacent owner.

## Recovered implementation boundaries

### 1. Projection Measurement != Projection Diagnostic Aggregation

`ProjectionBuildDiagnostics.timed(...)` owns the measurement moment: it calls `time.perf_counter()`, executes the supplied callable, computes elapsed time, and then delegates preservation of the elapsed value to `_ProjectionDiagnosticAggregation.add_timing(...)`.

`_ProjectionDiagnosticAggregation` owns the aggregation semantics for repeated timings and counters. Its docstring states that measurement remains with callers that know phase boundaries, while the aggregation owner preserves repeated measured values and counter updates in existing diagnostic shapes. The implementation adds elapsed values for repeated timing names and increments counters without measuring time itself.

Evidence:

- `_ProjectionDiagnosticAggregation.add_timing(...)` accumulates repeated timing names and appends new names.
- `_ProjectionDiagnosticAggregation.add_count(...)` increments counters.
- `ProjectionBuildDiagnostics.timed(...)` measures elapsed time and then calls `self._aggregation.add_timing(...)`.
- `ProjectionBuildDiagnostics.add_count(...)` delegates counter updates to aggregation.
- Tests preserve the repeated-measurement behavior and the public `ProjectionBuildDiagnostics` compatibility shape.

Conclusion: measurement and aggregation remain adjacent, but they are not implementation-compressed into one responsibility. Measurement captures elapsed values; aggregation preserves repeated values and counts.

### 2. Projection Diagnostic Aggregation != Projection Diagnostic Payload

`_ProjectionDiagnosticPayload` snapshots already aggregated diagnostic evidence for consumers. Its docstring explicitly excludes measuring phases, aggregating values, replaying events, rendering output, and changing compatibility surfaces. Its `from_aggregation(...)` classmethod copies timings into an immutable tuple and copies counters into a new dictionary.

Evidence:

- `_ProjectionDiagnosticPayload.from_aggregation(...)` only snapshots `aggregation.timings` and `aggregation.counters`.
- `ProjectionBuildDiagnostics.payload` builds a payload from `_aggregation` rather than exposing aggregation mechanics directly to consumers.
- Tests prove that mutating aggregation after payload construction does not change payload timings/counters.
- Tests prove that `ProjectionBuildDiagnostics.payload` preserves the compatible public lists/dicts on the diagnostics object while exposing a payload snapshot.

Conclusion: aggregation and payload are separated. Aggregation owns update rules; payload owns the consumer-facing snapshot of already aggregated evidence.

### 3. Projection Diagnostic Payload != Projection Diagnostic Selection

`_ProjectionDiagnosticSelection` owns consumer-requested handoff from payload. Its docstring says payload owns already aggregated evidence, while selection preserves the handoff where consumers request only existing payload portions they need. It does not measure, aggregate, construct payloads, format output, or change compatibility fields.

Evidence:

- `_ProjectionDiagnosticSelection.from_payload(...)` copies payload timings and counters into selection.
- `timings_list()` and `counters_dict()` return compatibility-shaped mutable copies for consumers.
- Tests prove that selection is isolated from later payload counter mutation and from mutations to returned counter dictionaries.

Conclusion: payload and selection are separated. Payload snapshots producer evidence; selection adapts that evidence for downstream consumer handoff.

### 4. Projection Diagnostic Selection != Consumers

Consumers now receive selected diagnostic evidence rather than reaching into producer aggregation details directly.

State-build cache debug creates `ProjectionBuildDiagnostics`, passes it into projection execution or cache-assisted projection, converts `projection_diagnostics.payload` into `_ProjectionDiagnosticSelection`, and then uses the selected timing/counter copies in `_ProjectionCacheDiagnosticPayload`.

Current-facts timing uses `_CurrentFactsTimingInterpretation.from_cache_evidence(...)` to convert a `StateCacheStatus` plus `ProjectionBuildDiagnostics` into cache visibility plus projection timing evidence. That interpretation uses `_ProjectionDiagnosticSelection.from_payload(...)` and preserves selection timings. `_CurrentFactsTimingDiagnosticPayload.from_timing_interpretation(...)` then combines the measured state-cache path elapsed time with projection timings for the current-facts timing report.

Projection cache code passes diagnostics through to projection paths and adds cache-path-specific measurements such as cached projection load/materialize and full projection rebuild, but it does not become the projection diagnostic payload or selection owner.

Conclusion: selection and consumer handoff are separated in the producer. Consumer-specific interpretation, cache labels, report payloads, and rendering remain outside the producer chain.

## Counterexample search results

### Measurement and aggregation mixed?

No recurring producer-side counterexample remains.

`ProjectionBuildDiagnostics.timed(...)` still contains measurement and calls aggregation, but aggregation semantics are isolated in `_ProjectionDiagnosticAggregation`. This is a local coordinating edge, not recurring compressed ownership, because repeated-name accumulation and counter increments live in aggregation methods and are covered by tests.

### Aggregation and payload mixed?

No recurring producer-side counterexample remains.

Payload construction only copies aggregated evidence. Aggregation mutation after payload construction does not affect payload. The implementation and tests support this as a completed boundary.

### Payload and selection mixed?

No recurring producer-side counterexample remains.

Selection is built from payload and returns compatibility-shaped copies. Tests prove selection isolation from payload and returned dict mutation.

### Selection and consumer handoff mixed?

No producer-side counterexample remains, but downstream consumers still contain pressure.

State-build cache debug and current-facts timing each interpret selected projection diagnostics alongside their own cache status, timing labels, report payloads, and rendering paths. That pressure is consumer-side because the producer selection boundary is already explicit and the remaining work concerns how each consumer combines projection diagnostics with cache/debug/report-specific evidence.

## Relationship to projection execution

Projection Diagnostics remains optional and non-authoritative for projected-state construction.

`StateProjector.project(...)` constructs a `State`, lists ledger events, and delegates to `project_from_state(...)` with the optional diagnostics object. It does not construct payloads or consumer selections.

`StateProjector.project_from_state(...)` uses diagnostics for implementation-local measurement and counters:

- materializes input events under the label `projection input event materialization` when diagnostics are supplied;
- records `projection events` count;
- records per-event-kind counters during replay;
- wraps event replay under the `event replay` timing label;
- calls `finalize(...)` with the same diagnostics object;
- publishes finalized projection state through the projection publication path.

`StateProjector.finalize(...)` uses the optional `diagnostics.timed` function to time finalization subphases and updates structural counters after finalization. The labels are still embedded near the projection work they measure, but this is measurement ownership: the producer chain now receives those measurements through `ProjectionBuildDiagnostics` and moves them through aggregation, payload, and selection before consumers use them.

Supported conclusion: projection execution continues to own where projection phases begin and end. Projection Diagnostics owns preserving and handing off optional diagnostic evidence. The diagnostics chain does not execute projection, change replay, change publication, change cache behavior, or alter projected-state authority.

Unsupported conclusion: this audit does not prove that projection execution should be redesigned, that timing labels should move out of `finalize(...)`, or that a global timing framework should be introduced.

## Relationship to downstream consumers

### State-build cache debug

State-build cache debug remains the strongest downstream pressure. It opens/cache-checks state and summary caches, constructs a projector, creates projection diagnostics, invokes projection or cache-assisted projection, derives read models, saves summary snapshots, measures rendering, selects projection diagnostics, and assembles `StateSummaryCacheDebugReport`.

The projection diagnostic producer contribution is now bounded to:

```text
ProjectionBuildDiagnostics
→ payload
→ _ProjectionDiagnosticSelection
→ timing/counter copies
```

The remaining complexity belongs to the state-build cache debug consumer because it combines cache eligibility/status, state cache status, summary cache behavior, projection diagnostics, read-model construction, snapshot saving, and report payload assembly.

### Current-facts timing

Current-facts timing also retains downstream pressure. It opens ledgers/stores, wraps the projection store to time cache operations, constructs the projector, measures state-path elapsed time, interprets `StateCacheStatus`, selects projection diagnostics from payload, builds a timing diagnostic payload, runs read-model/fact-index work, and formats a timing report.

The projection diagnostic producer contribution is bounded by `_ProjectionDiagnosticSelection.from_payload(...)`; current-facts-specific cache labels, state-path timing, projection-store timing wrapper, report payload, and presentation remain current-facts timing ownership.

### Projection cache debug / pass-through

Projection cache pass-through remains adjacent. `project_state_with_cache(...)` receives optional diagnostics and passes them into cached materialization, incremental replay, or full projection rebuild paths. It also decides cache hit/miss/incremental replay and saves snapshots. This is not producer compression: it is cache-path execution and cache visibility pressure that consumes or augments projection measurements.

## Supported conclusions

1. **Projection Diagnostics has become a completed implementation responsibility chain for the current producer family.** The implementation has distinct owners for measurement coordination, aggregation update rules, payload snapshotting, and consumer selection.

2. **Remaining pressure is downstream.** State-build cache debug and current-facts timing still combine cache status, projection diagnostics, report payloads, local timings, and rendering/report assembly. They consume projection diagnostics; they do not prove producer compression.

3. **Projection execution remains separate from projection diagnostics.** Projection code supplies phase boundaries and optional measurement hooks. Diagnostic evidence is non-authoritative and does not change replay, publication, cache behavior, state content, counters' compatibility names, or JSON/CLI behavior.

4. **No new producer ownership slice is supported by current evidence.** Another slice inside Projection Diagnostics would likely chase consumer-specific cache/report pressure rather than producer responsibility compression.

## Unsupported conclusions

The implementation evidence does not support the following conclusions:

- that projection execution should be redesigned;
- that finalization labels should be moved into a global label registry;
- that cache debug needs a new framework;
- that CLI, JSON, schema, timing labels, counters, or compatibility behavior should change;
- that state-build cache debug and current-facts timing are complete;
- that projection cache debug/pass-through is free of future consumer-side ownership pressure;
- that presentation vocabulary such as `projection cache debug` is preserved knowledge beyond implemented cache/debug surfaces.

## Answers to the requested questions

### 1. Has the Projection Diagnostics producer become a completed implementation responsibility chain?

Yes. The current implementation exposes the complete chain:

```text
Projection Measurement
→ Projection Diagnostic Aggregation
→ Projection Diagnostic Payload
→ Projection Diagnostic Selection
→ Consumers
```

This is supported by the implementation-local classes and tests that separately preserve aggregation behavior, payload snapshotting, selection handoff, and consumer copy semantics.

### 2. What implementation evidence supports that conclusion?

Evidence includes:

- `_ProjectionDiagnosticAggregation` owns repeated timing accumulation and counter increments.
- `ProjectionBuildDiagnostics.timed(...)` measures elapsed time and delegates aggregation rather than owning repeated-value semantics inline.
- `_ProjectionDiagnosticPayload.from_aggregation(...)` snapshots already aggregated evidence.
- `ProjectionBuildDiagnostics.payload` exposes a payload snapshot without changing the compatible diagnostics lists/dicts.
- `_ProjectionDiagnosticSelection.from_payload(...)`, `timings_list()`, and `counters_dict()` preserve the consumer handoff boundary.
- State-build cache debug and current-facts timing use selection from payload before building consumer-specific diagnostic/report payloads.
- Tests cover aggregation, measurement-to-aggregation compatibility, payload snapshot isolation, and selection handoff isolation.

### 3. Does any remaining compression still belong to Projection Diagnostics?

No recurring compression currently belongs to Projection Diagnostics. Measurement and aggregation are connected, but aggregation semantics have an implementation-local owner. Aggregation and payload are separated by snapshot construction. Payload and selection are separated by consumer handoff. Selection and consumers are separated by selected copies, with consumer-specific report construction outside the producer.

### 4. If not, which implementation owner now contains the strongest remaining pressure?

The strongest remaining pressure is **state-build cache debug**.

It still combines cache eligibility/status, state cache lookup visibility, projector construction, projection/cache-assisted execution, read-model construction, summary snapshot saving, projection diagnostic selection, and report assembly. Current-facts timing is the next strongest owner because it combines cache-path timing, projection-store timing wrappers, projection diagnostic selection, current-facts read-model/fact-index work, and timing presentation.

### 5. Should Projection Diagnostics receive another ownership slice, or should the next work begin with a different responsibility owner?

Projection Diagnostics should not receive another ownership slice based on current evidence. The next work should begin with a different responsibility owner, preferably **state-build cache debug**, because the remaining recurring pressure is how downstream cache/debug consumers combine projection diagnostics with their own cache status, local timings, read models, and report payloads.

## Confidence

Confidence: **high** for the producer-family completion conclusion.

Reasons:

- The implementation now contains explicit classes for aggregation, payload, and selection.
- Tests cover each recovered boundary.
- Consumers use selection rather than directly owning producer aggregation mechanics.
- Remaining visible complexity is in consumer/report/cache paths, not in the projection diagnostic producer chain.

Confidence is not absolute because this audit is bounded to implementation evidence around the named classes, projection paths, state-build cache debug, current-facts timing, and projection cache pass-through. Future surfaces could introduce new producer-side compression, but no such counterexample was found in the reviewed implementation.

## Recommended next responsibility owner

Recommended next owner: **state-build cache debug**.

Why:

- It contains the broadest remaining consumer-side combination of cache visibility, projection execution, projection diagnostics consumption, summary read-model derivation, summary cache writes, and report assembly.
- It consumes Projection Diagnostics through the completed payload/selection handoff, so further work there would not require another Projection Diagnostics producer slice.
- It is more compressed than current-facts timing because it spans both state projection cache behavior and summary read-model cache/debug behavior in one report-building path.

Secondary candidate: **current-facts timing**, especially if the desired next boundary is narrower and focused on cache-path timing/report interpretation rather than state-build plus summary-cache behavior.

## Commands used

```bash
cat AGENTS.md
rg -n "ProjectionBuildDiagnostics|_ProjectionDiagnosticAggregation|_ProjectionDiagnosticPayload|_ProjectionDiagnosticSelection|class StateProjector|def project\(|def project_from_state|def finalize|state-build cache debug|current-facts timing|cache debug" seed_runtime scripts tests -g '!*.pyc'
sed -n '140,260p' seed_runtime/state.py
sed -n '893,1045p' seed_runtime/state.py
sed -n '1011,1165p' seed_runtime/state.py
sed -n '3380,3515p' scripts/seed_local.py
sed -n '5310,5365p' scripts/seed_local.py
sed -n '5365,5505p' scripts/seed_local.py
sed -n '542,820p' seed_runtime/projection_store.py
sed -n '1,90p' tests/test_state_projector.py
sed -n '2280,2335p' tests/test_seed_local_script.py
```
