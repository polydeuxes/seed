# Current-Facts Timing Visibility Completion Audit

## Scope

This audit reviews the implementation-local current-facts timing path only. It does not propose or implement another ownership slice, timing framework, shared timing API, schema change, CLI change, cache redesign, projection redesign, or runtime surface.

Investigated implementation anchors:

- `_current_facts_timing_from_args(...)`
- `_CurrentFactsTimingInterpretation`
- `_CurrentFactsTimingDiagnosticPayload`
- `_CurrentFactsTimingPresentation`
- `_CurrentFactsCacheVisibility`
- `CurrentFactsTimingReport`
- `_format_current_facts_timing_report(...)`
- `ProjectionBuildDiagnostics`

## Recovered implementation boundaries

### Timing Measurement

The current-facts command path still owns direct measurement of the current-facts execution phases. `_current_facts_timing_from_args(...)` creates a local `timings` list, starts a total timer with `time.perf_counter()`, and defines a local `timed(name, func)` helper that appends phase durations after each measured operation.

Measured phases in this owner include ledger opening, projection store opening, projector construction, direct full projection rebuild when cache is unavailable, read-model build, render, fact-index build/load, query/filter/render, stdout/output placeholder, and total elapsed time.

The state-cache branch additionally measures the outer State path by capturing `state_path_started = time.perf_counter()` before `project_state_with_cache(...)` and passing the elapsed value into `_CurrentFactsTimingDiagnosticPayload.from_timing_interpretation(...)` after the cache path returns.

This is implementation evidence that measurement remains local orchestration, not a generic timing framework.

### Cache Visibility

`_CurrentFactsCacheVisibility` owns the current-facts-local explanation of State cache status. It converts `StateCacheStatus` into two values:

- `cache_status`, currently `hit` or `miss`;
- `state_path_label`, with separate labels for cached projection load, incremental event replay, and full projection rebuild.

This boundary is cache-path explanation only. It does not measure elapsed time, construct diagnostic payloads, format reports, or mutate projection/cache behavior.

### Timing Interpretation

`_CurrentFactsTimingInterpretation.from_cache_evidence(...)` consumes two pieces of already-produced evidence:

- `StateCacheStatus` from `project_state_with_cache(...)`;
- `ProjectionBuildDiagnostics` populated by the projector/cache path.

It returns interpreted cache visibility plus a tuple copy of projection diagnostic timings. Its docstring explicitly says it interprets measured State-cache evidence without owning measurement.

This separates timing interpretation from measurement: the measured State-path elapsed value is not produced inside `_CurrentFactsTimingInterpretation`, and the class does not call `time.perf_counter()`.

### Timing Diagnostic Payload

`_CurrentFactsTimingDiagnosticPayload.from_timing_interpretation(...)` consumes interpreted timing evidence plus the measured outer State-path elapsed value and preserves the timing data shape used by diagnostic consumers.

It constructs:

- `cache_status` from `interpretation.cache_visibility.cache_status`;
- a timing tuple beginning with the interpreted State-path label and measured elapsed State-path duration;
- projection diagnostic timings appended after that State-path timing.

This separates interpretation from diagnostic payload construction. The payload class does not decide cache-hit/miss labels and does not format text. It preserves already interpreted timing evidence in the report-compatible diagnostic shape.

### CurrentFactsTimingReport bridge

`CurrentFactsTimingReport` now carries two payloads:

- `visibility`, containing operator/read-model output;
- `diagnostics`, containing `cache_status` and `timings`.

Its `output`, `cache_status`, and `timings` properties are compatibility accessors over those payloads. This is a bridge shape, not a timing owner by itself.

### Timing Presentation

`_CurrentFactsTimingPresentation.from_report(...)` consumes only `CurrentFactsTimingReport.cache_status` and `CurrentFactsTimingReport.timings`, then `format()` renders the existing operator-facing text:

- title;
- cache section;
- timing lines with six decimal places.

`_format_current_facts_timing_report(...)` is now a compatibility wrapper that delegates to `_CurrentFactsTimingPresentation.from_report(report).format()`.

This separates diagnostic payload from presentation. Presentation no longer owns cache-status derivation, projection timing collection, State-path measurement, report payload construction, or read-model output.

### ProjectionBuildDiagnostics boundary

`ProjectionBuildDiagnostics` is a separate projection-owner diagnostic container. It is optional and explicitly non-authoritative for projected-State construction. It measures projection subphases through its own `timed(name, func)` helper, accumulates repeated timing names, and records counters.

The current-facts timing owner consumes `projection_diagnostics.timings` through `_CurrentFactsTimingInterpretation`; it does not own projection subphase measurement or projection diagnostic naming.

## Lifecycle conclusion

The implementation now exposes a complete current-facts timing lifecycle:

```text
Timing Measurement
↓
Timing Interpretation
↓
Timing Diagnostic Payload
↓
Timing Presentation
```

Implementation evidence:

1. Measurement is local to `_current_facts_timing_from_args(...)` and `_TimingProjectionStore` wrappers, with explicit `time.perf_counter()` calls and phase append behavior.
2. Interpretation is localized in `_CurrentFactsTimingInterpretation.from_cache_evidence(...)`, which consumes `StateCacheStatus` and `ProjectionBuildDiagnostics` without measuring elapsed time.
3. Diagnostic payload construction is localized in `_CurrentFactsTimingDiagnosticPayload.from_timing_interpretation(...)`, which combines interpreted labels and measured elapsed values into the report-compatible timing payload.
4. Presentation is localized in `_CurrentFactsTimingPresentation`, while `_format_current_facts_timing_report(...)` only delegates.
5. Tests preserve the recovered boundaries by checking that interpretation keeps projection measurements unchanged, diagnostic payload construction preserves interpreted evidence, presentation formats preserved diagnostics, and visibility remains separate from diagnostics.

Therefore, the current-facts timing owner has become a complete implementation responsibility chain for this path.

## Counterexample search

### Measurement and interpretation

No remaining current-facts cache-branch counterexample was found where measured State-cache evidence and interpretation remain materially mixed. `_current_facts_timing_from_args(...)` still measures the outer State path, but interpretation of `StateCacheStatus` and projection diagnostics occurs in `_CurrentFactsTimingInterpretation.from_cache_evidence(...)`.

The remaining local `timed(...)` helper labels non-cache branch and read-model/query/render phases directly. That is still measurement plus phase naming, but it is not the recovered cache-evidence interpretation boundary. The implementation does not expose a separate interpretation owner for every phase name such as `read-model build` or `render`, and this audit does not find evidence that such a generic timing-label owner exists or is required inside the current-facts owner.

### Interpretation and diagnostic payload

No remaining current-facts cache-branch counterexample was found where interpretation and diagnostic payload construction remain materially mixed. `_CurrentFactsTimingDiagnosticPayload` receives an interpretation object and measured elapsed value; it does not inspect `StateCacheStatus` directly.

### Diagnostic payload and presentation

No remaining counterexample was found where diagnostic payload construction and text presentation remain materially mixed. `_CurrentFactsTimingPresentation` consumes report diagnostics and formats text; `_CurrentFactsTimingDiagnosticPayload` does not format operator-facing output.

## Remaining compressed boundaries

The following implementation compression remains, but the evidence does not place it inside the completed current-facts timing owner as another necessary ownership slice:

1. **Local measurement orchestration remains in `_current_facts_timing_from_args(...)`.** The function still orchestrates CLI arguments, ledger/store/projector setup, cache eligibility, State projection, read-model or query output, resource cleanup, timing collection, and final report construction. This is broad command orchestration, but the recovered timing lifecycle boundaries are now explicit inside it.

2. **`_TimingProjectionStore` still records cache-wrapper timings by wrapping projection-store methods.** This is cache visibility/instrumentation pressure around projection-store operations, not evidence that current-facts timing interpretation, diagnostic payload, or presentation remain compressed.

3. **Projection subphase measurement and labels remain in `ProjectionBuildDiagnostics` and projector/finalization code.** Current facts only consumes those timings after projection diagnostics have produced them. This points to projection diagnostics ownership, not to another current-facts timing slice.

4. **State-build/cache debug and current-facts cache debug may share conceptual timing vocabulary.** The implementation evidence shows separate caller-specific reports rather than a shared timing framework. The task explicitly forbids creating that framework, and the repository does not prove that current-facts should own other surfaces' timing grammar.

## Supported conclusions

- The current-facts timing path now has explicit implementation-local boundaries for measurement, interpretation, diagnostic payload construction, and presentation.
- The boundary between State-cache evidence interpretation and diagnostic payload construction is implemented and test-backed.
- The boundary between diagnostic payload and presentation is implemented and test-backed.
- `ProjectionBuildDiagnostics` remains a separate optional, non-authoritative projection diagnostics owner whose timings are consumed by current facts.
- Current-facts timing completion does not imply a repository-wide timing architecture or shared timing API.

## Unsupported conclusions

The implementation evidence does not support concluding that:

- all timing-producing owners in the repository share one lifecycle or should be merged;
- `ProjectionBuildDiagnostics` labels are semantic projection truth;
- current-facts timing owns state-build cache debug timing;
- current-facts timing owns projection diagnostics;
- current-facts timing owns knowledge reachability timing;
- current-facts timing owns observation ingestion timing;
- current-facts timing owns execution status cadence;
- presentation vocabulary such as cache/debug/timing labels should be promoted into preserved knowledge.

## Relationship to other timing-producing owners

### State-build cache debug

State-build cache debug remains a separate consumer/producer of cache and projection diagnostic visibility. It can share projection diagnostic inputs, but current-facts timing does not own its report shape or formatting.

### Projection diagnostics

`ProjectionBuildDiagnostics` is the strongest adjacent timing-producing owner in the investigated code. It owns optional projection subphase timings and counters. It is used by projection execution and then consumed by current-facts timing interpretation. If timing pressure remains around projection subphase labels, accumulation semantics, or finalization timing granularity, that pressure belongs to projection diagnostics rather than current-facts timing.

### Knowledge reachability

Knowledge reachability has its own audit/timing surface and should not be pulled under current-facts timing without implementation evidence. Presentation vocabulary alone is not enough.

### Observation ingestion

Observation ingestion timing/diagnostics are produced by ingestion-specific services and formatters. No evidence in this audit shows that current-facts timing should own ingestion timing semantics.

### Execution status cadence

Execution status cadence is status/progress visibility, not elapsed timing payload ownership. It remains a separate execution visibility owner.

## Confidence

Confidence is **high** that the current-facts timing path has become a completed implementation responsibility chain for the recovered lifecycle.

Confidence is **medium-high** that remaining recurring timing pressure belongs outside this owner, because the strongest remaining pressure visible in the investigated implementation is projection subphase diagnostics: `ProjectionBuildDiagnostics` owns optional projection timings/counters, accumulation behavior, and projector/finalization phase labels consumed by multiple callers.

Confidence is **not absolute** because `_current_facts_timing_from_args(...)` remains a broad orchestration function. However, the remaining breadth is command orchestration and local measurement collection, not evidence that measurement/interpretation/payload/presentation are still compressed in the current-facts timing owner.

## Recommended next responsibility owner

Stop this current-facts timing ownership family.

If more timing implementation pressure must be audited, the recommended next owner is **Projection Diagnostics**, centered on `ProjectionBuildDiagnostics` and its use in projection replay/finalization. That owner has the strongest implementation pressure because:

- it produces reusable projection subphase timings consumed by current-facts and other projection/cache debug surfaces;
- it accumulates repeated phase names while caller-local timing lists append phases;
- projector and finalization code embed diagnostic phase labels at the production site;
- it is explicitly optional and non-authoritative, so its boundaries matter for preventing diagnostic timing labels from becoming projection truth.

Do not continue with another current-facts timing ownership slice unless new implementation evidence shows that current-facts measurement, interpretation, diagnostic payload, or presentation have become compressed again.
