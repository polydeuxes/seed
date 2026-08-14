# State-Build Cache Debug Slice 001

## Selected architectural boundary

State-Build Cache Debug Orchestration now explicitly produces `_StateBuildCacheDebugEvidence`, and `StateSummaryCacheDebugReport` consumes that evidence to construct the consumer-specific report shape.

```text
State-Build Cache Debug Orchestration

↓

_StateBuildCacheDebugEvidence

↓

StateSummaryCacheDebugReport.from_evidence(...)
```

This recovers exactly one implementation-local ownership boundary. It does not reopen projection diagnostics, read-model ownership, projection publication, execution visibility, cache behavior, rendering, CLI dispatch, or JSON behavior.

## Implementation evidence

The implementation pressure was concentrated in `scripts/seed_local.py` around the state-build cache-debug path:

- `_StateBuildVisibilityPayload` already owned state-build-facing visibility fields: cache eligibility, summary-cache status, current/cached summary event ids, and notes.
- `_ProjectionCacheDiagnosticPayload` already owned projection-cache diagnostic fields: projection cache status, cached state event id, projection timings, and projection counters.
- `state_summary_cache_debug_from_args(...)` previously both orchestrated cache-debug evidence collection and directly constructed `StateSummaryCacheDebugReport` at each return boundary.
- `format_state_summary_cache_debug_report(...)` remains a downstream formatter that consumes only the public report compatibility properties.

The recurring compressed boundary was therefore not between the formatter and the report. The stronger evidence was inside report construction: orchestration produced an implementation artifact, but that artifact was implicit in inline `StateSummaryCacheDebugReport(...)` construction.

## Before

`state_summary_cache_debug_from_args(...)` mixed two responsibilities:

1. State-build cache-debug orchestration:
   - opening the projection store and event ledger;
   - listing current events;
   - resolving read-model dependency identity;
   - checking summary-cache and state-cache status;
   - invoking projection replay/build when needed;
   - consuming projection diagnostics;
   - constructing summary read models;
   - saving the summary snapshot;
   - collecting local timing evidence.
2. Consumer-specific report construction:
   - directly returning `StateSummaryCacheDebugReport(...)` from both the summary-cache-hit path and the rebuild/miss path.

## After

`_state_build_cache_debug_evidence_from_args(...)` now owns the orchestration lifecycle and returns `_StateBuildCacheDebugEvidence`.

`state_summary_cache_debug_from_args(...)` remains the public compatibility entry point and now only converts the recovered evidence into `StateSummaryCacheDebugReport` with `StateSummaryCacheDebugReport.from_evidence(...)`.

The formatter still consumes `StateSummaryCacheDebugReport`; no rendering ownership moved.

## Recovered producer

`_state_build_cache_debug_evidence_from_args(...)` is the recovered implementation-local producer.

It may consume existing state-build visibility, projection diagnostic selection, read-model cache results, summary cache status, and local timing evidence, because those were already part of the implemented orchestration path.

## Recovered artifact

`_StateBuildCacheDebugEvidence` is the recovered artifact.

It preserves only the existing artifact already produced by orchestration:

- `_StateBuildVisibilityPayload`;
- `_ProjectionCacheDiagnosticPayload`;
- local state-build cache-debug timings.

It does not own formatting, CLI behavior, projection execution semantics, projection diagnostics production, read-model construction semantics, cache semantics, JSON behavior, or rendering.

## Consumer of the artifact

`StateSummaryCacheDebugReport.from_evidence(...)` is the consumer-specific report construction boundary.

The report continues to expose the same compatibility properties, including `cache_eligible`, `summary_cache_status`, `state_cache_status`, event id accessors, `projection_timings`, `projection_counters`, and `notes`.

## Compatibility preserved

No compatibility boundary changed.

The public function `state_summary_cache_debug_from_args(...)` still returns `StateSummaryCacheDebugReport`, and `format_state_summary_cache_debug_report(...)` still renders the same report properties.

## Questions answered

1. **Where were State-Build Cache Debug orchestration and the produced implementation artifact previously mixed?**

   They were mixed inside `state_summary_cache_debug_from_args(...)`, which both executed the orchestration lifecycle and directly instantiated `StateSummaryCacheDebugReport(...)` at the cache-hit and miss/rebuild return points.

2. **Which recovered architectural boundary became more explicit?**

   The boundary between State-Build Cache Debug Orchestration and consumer-specific report construction became explicit.

3. **What implementation artifact is now explicitly produced for downstream consumption?**

   `_StateBuildCacheDebugEvidence`.

4. **Did implementation evidence suggest a more precise responsibility name than "State-Build Cache Debug Evidence"?**

   Insufficient implementation evidence.

5. **Did any compatibility boundary change?**

   No.

## Files changed

- `scripts/seed_local.py`
- `tests/test_seed_local_script.py`
- `state_build_cache_debug_slice_001.md`

## LOC changed

At the time of this report, the implementation/test diff and report file size were:

```text
scripts/seed_local.py                 | 32 insertions(+), 5 deletions(-)
tests/test_seed_local_script.py       | 30 insertions(+)
state_build_cache_debug_slice_001.md  | 134 lines added
```

## Tests executed

- `pytest -q tests/test_seed_local_script.py -k 'state_summary_cache_debug'`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed State-Build Cache Debug responsibilities

Stopped after recovering one owner.

Remaining pressure appears to stay in the state-build cache-debug lifecycle, including summary-cache lookup policy, state-cache lookup visibility, projection invocation choice, read-model derivation, summary snapshot publication, and timing-label selection. Those responsibilities remain compressed by design for this slice and belong to future owners only if implementation evidence supports them.
