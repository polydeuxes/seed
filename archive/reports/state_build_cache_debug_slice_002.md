# State-Build Cache Debug Slice 002

## Selected architectural boundary

State-Build Cache Debug Report Payload was recovered between collected cache-debug evidence and the compatibility-preserving report object.

```text
State-Build Cache Debug Evidence
    produces
_StateBuildCacheDebugReportPayload
    consumed by
StateSummaryCacheDebugReport
```

This is the earliest still-compressed owner in the inspected chain. The formatter boundary remains downstream and unchanged.

## Implementation evidence

- `_StateBuildCacheDebugEvidence` already carries the implementation evidence observed for a state-build cache-debug run: state-build visibility payload, projection diagnostic payload, and local timings.
- `StateSummaryCacheDebugReport.from_evidence(...)` previously copied those evidence fields directly into `StateSummaryCacheDebugReport`, so evidence consumption and report payload shaping were mixed at the report construction boundary.
- `format_state_summary_cache_debug_report(...)` consumes only the compatibility report surface and its existing property names, which is stronger evidence that presentation was already separated enough for this slice.
- `_StateBuildVisibilityPayload` and `_ProjectionCacheDiagnosticPayload` remain implementation-local inputs to the report payload; they do not own evidence collection, projection behavior, read-model construction, cache semantics, events, or ledger replay.

## Before

```text
_StateBuildCacheDebugEvidence
    consumed directly by
StateSummaryCacheDebugReport.from_evidence(...)
    constructs
StateSummaryCacheDebugReport
    consumed by
format_state_summary_cache_debug_report(...)
```

The selected boundary was previously mixed inside `StateSummaryCacheDebugReport.from_evidence(...)`. That method both consumed evidence and performed the implementation-local report payload shaping step.

## After

```text
_StateBuildCacheDebugEvidence
    consumed by
_StateBuildCacheDebugReportPayload.from_evidence(...)
    produces
_StateBuildCacheDebugReportPayload
    consumed by
StateSummaryCacheDebugReport.from_payload(...)
    produces
StateSummaryCacheDebugReport
    consumed by
format_state_summary_cache_debug_report(...)
```

`StateSummaryCacheDebugReport.from_evidence(...)` remains as the compatibility-preserving entry point and delegates through the recovered payload boundary.

## Recovered producer

`_StateBuildCacheDebugReportPayload.from_evidence(...)` now owns the report-payload shaping step from collected state-build cache-debug evidence.

It consumes:

- `_StateBuildCacheDebugEvidence`;
- `_StateBuildVisibilityPayload` through the evidence object;
- `_ProjectionCacheDiagnosticPayload` through the evidence object;
- existing local timing evidence through the evidence object.

It does not own evidence collection, projection behavior, projection diagnostic production, read-model construction, cache lookup behavior, CLI handling, JSON behavior, events, or ledger replay.

## Recovered artifact

`_StateBuildCacheDebugReportPayload` is the recovered implementation-local artifact.

It preserves the existing report payload responsibility only:

- state-build visibility payload;
- projection diagnostic payload;
- state-build cache-debug local timings.

## Consumer of the artifact

`StateSummaryCacheDebugReport.from_payload(...)` consumes `_StateBuildCacheDebugReportPayload` and constructs the compatibility-preserving `StateSummaryCacheDebugReport` object.

`format_state_summary_cache_debug_report(...)` still consumes `StateSummaryCacheDebugReport`, not the implementation-local payload.

## Compatibility preserved

No compatibility boundary changed.

- `state_summary_cache_debug_from_args(...)` still returns `StateSummaryCacheDebugReport`.
- `StateSummaryCacheDebugReport.from_evidence(...)` remains available and preserves the previous construction path through delegation.
- Existing report properties remain unchanged.
- CLI output, format text, JSON behavior, events, ledger replay, cache behavior, projection behavior, and read-model behavior are unchanged.

## Answers to required questions

1. **Where was the selected boundary previously mixed?**

   It was mixed inside `StateSummaryCacheDebugReport.from_evidence(...)`, which directly consumed `_StateBuildCacheDebugEvidence` and instantiated the compatibility report object.

2. **Which recovered architectural boundary became more explicit?**

   The boundary between State-Build Cache Debug Evidence and State-Build Cache Debug Report became explicit through `_StateBuildCacheDebugReportPayload`.

3. **What implementation artifact is produced and who consumes it?**

   `_StateBuildCacheDebugReportPayload` is produced by `_StateBuildCacheDebugReportPayload.from_evidence(...)` and consumed by `StateSummaryCacheDebugReport.from_payload(...)`.

4. **Did implementation evidence suggest a more precise responsibility name than the prompt's expected name?**

   Insufficient implementation evidence.

5. **Did any compatibility boundary change?**

   No.

## Files changed

- `scripts/seed_local.py`
- `tests/test_seed_local_script.py`
- `state_build_cache_debug_slice_002.md`

## LOC changed

Final repository diff for this slice:

```text
scripts/seed_local.py: 27 insertions, 2 deletions
tests/test_seed_local_script.py: 13 insertions, 5 deletions
state_build_cache_debug_slice_002.md: 150 insertions
```

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
pytest -q tests/test_seed_local_script.py -k 'state_summary_cache_debug'
```

Results:

- diagnostic inventory and shape-audit checks passed, 44 tests selected.
- state summary cache debug checks passed, 6 tests selected.

## Remaining compressed State-Build Cache Debug responsibilities

- Evidence collection still owns cache-debug lifecycle measurement, cache lookup evidence gathering, projection invocation evidence, read-model derivation evidence, summary snapshot publication evidence, and final evidence assembly in one implementation path.
- Report construction still preserves compatibility accessors on `StateSummaryCacheDebugReport` while wrapping implementation-local payloads.
- Presentation remains in `format_state_summary_cache_debug_report(...)` and may be inspected separately in a later slice if implementation evidence shows report-to-presentation pressure.

Stop point: the recovered payload boundary now separates evidence from report payload shaping. Remaining pressure belongs to later or different owners.
