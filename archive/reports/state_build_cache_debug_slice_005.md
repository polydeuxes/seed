# State-Build Cache Debug Slice 005

## Selected architectural boundary

Recovered boundary:

```text
State-Build Cache Debug Projection Evidence

↓

_StateBuildCacheDebugProjectionEvidence

↓

_StateBuildCacheDebugEvidenceAssembly
```

This slice remains inside **State-Build Cache Debug Evidence Collection** and recovers exactly one implementation-local ownership boundary. The selected stream is projection evidence, not read-model evidence, because the implementation already had a recurring projection diagnostic handoff in both cache-debug return paths while read-model construction still appears as build work feeding cache/debug visibility rather than a distinct recurring evidence artifact consumed by assembly.

## Implementation evidence

`_state_build_cache_debug_evidence_from_args(...)` already collected projection-related evidence before constructing evidence assembly:

- the warm summary-cache path set `state_cache_status="skipped"` and emitted empty projection timings/counters because projection replay was not needed;
- the cold projection/build path converted `ProjectionBuildDiagnostics.payload` through `_ProjectionDiagnosticSelection` and then shaped the selected timings and counters into `_ProjectionCacheDiagnosticPayload`;
- both paths immediately passed that projection diagnostic payload into `_StateBuildCacheDebugEvidenceAssembly` through cache-debug evidence construction.

The new `_StateBuildCacheDebugProjectionEvidence` artifact now owns only the implementation-local projection evidence shape needed by state-build cache debug. It consumes the already selected projection diagnostics and preserves the existing `_ProjectionCacheDiagnosticPayload` fields.

## Before

```text
_state_build_cache_debug_evidence_from_args(...)

↓

_StateBuildCacheDebugCacheEvidence(
    visibility=...,
    projection_diagnostics=_ProjectionCacheDiagnosticPayload(...)
)

↓

_StateBuildCacheDebugEvidenceAssembly.from_cache_evidence(...)
```

Projection evidence was mixed at the return sites in `_state_build_cache_debug_evidence_from_args(...)`. The function selected or synthesized projection diagnostic values and immediately embedded them in the cache-debug evidence consumed by evidence assembly.

## After

```text
_state_build_cache_debug_evidence_from_args(...)

↓

_StateBuildCacheDebugProjectionEvidence

↓

_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)
```

The summary-cache hit path now produces `_StateBuildCacheDebugProjectionEvidence` with skipped state-cache status and unchanged empty projection timings/counters. The projection/build path now produces `_StateBuildCacheDebugProjectionEvidence.from_diagnostic_selection(...)` from `_ProjectionDiagnosticSelection` before assembly consumes it.

## Recovered producer

`_state_build_cache_debug_evidence_from_args(...)` remains the broader State-Build Cache Debug Evidence Collection owner. For this slice, it is the producer of `_StateBuildCacheDebugProjectionEvidence` in both recurring paths:

- summary-cache hit path: direct projection evidence with `state_cache_status="skipped"`, no cached state id, no projection timings, and no counters;
- projection/build path: projection evidence from `_ProjectionDiagnosticSelection`, preserving selected projection timings and counters.

## Recovered artifact

`_StateBuildCacheDebugProjectionEvidence` is the recovered implementation-local artifact.

It preserves only the existing projection evidence stream:

- `state_cache_status`;
- `cached_state_last_event_id`;
- `projection_timings`;
- `projection_counters`.

It does not own projection execution, projection diagnostic production, cache semantics, read-model construction, report payload construction, presentation, JSON, events, or ledger replay.

## Consumer of the artifact

`_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)` consumes `_StateBuildCacheDebugProjectionEvidence` alongside the already recovered cache evidence and local timing evidence. `_StateBuildCacheDebugEvidenceAssembly.from_cache_evidence(...)` remains as an internal compatibility path that delegates to the stream-aware constructor without changing output shape.

## Questions

1. **Where was the selected evidence stream previously mixed with Evidence Assembly?**

   It was mixed inside `_state_build_cache_debug_evidence_from_args(...)` at both cache-debug return sites. The warm summary-cache return directly constructed `_ProjectionCacheDiagnosticPayload` with skipped projection values while calling `_StateBuildCacheDebugEvidenceAssembly.from_cache_evidence(...)`. The cold projection/build return converted `_ProjectionDiagnosticSelection` into `_ProjectionCacheDiagnosticPayload` inline while calling the same assembly path.

2. **Which recovered architectural boundary became more explicit?**

   `State-Build Cache Debug Projection Evidence != State-Build Cache Debug Evidence Assembly` became explicit.

3. **What implementation artifact is now produced, and who consumes it?**

   `_StateBuildCacheDebugProjectionEvidence` is now produced by `_state_build_cache_debug_evidence_from_args(...)` and consumed by `_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)`.

4. **Did implementation evidence suggest a more precise responsibility name?**

   Yes. The implementation evidence supports **State-Build Cache Debug Projection Evidence** because the artifact preserves state-cache projection status plus selected projection timings/counters after `_ProjectionDiagnosticSelection`, without owning projection execution or diagnostic production.

5. **Did any compatibility boundary change?**

   No.

## Compatibility preserved

No behavior, report contents, CLI output, JSON output, event behavior, ledger replay behavior, cache behavior, projection behavior, read-model behavior, timing labels, or timing values were intentionally changed. Existing report consumers still receive the same visibility payload, projection diagnostic payload, and timing list.

## Files changed

- `scripts/seed_local.py`
- `tests/test_seed_local_script.py`
- `state_build_cache_debug_slice_005.md`

## LOC changed

`git diff --stat` after the implementation and before this report showed:

```text
scripts/seed_local.py           | 75 ++++++++++++++++++++++++++++++++---------
tests/test_seed_local_script.py | 45 +++++++++++++++++++++++--
2 files changed, 103 insertions(+), 17 deletions(-)
```

This report adds the requested slice documentation.

## Tests executed

- `pytest -q tests/test_seed_local_script.py -q`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed State-Build Cache Debug responsibilities

Within **State-Build Cache Debug Evidence Collection**, the cache and projection streams now have explicit implementation-local artifacts before evidence assembly. Remaining compressed pressure appears to include:

- read-model evidence associated with compact `StateSummary` derivation, operator summary derivation, and summary snapshot publication evidence;
- local timing collection, which is still passed as a raw timing list into evidence assembly;
- broader orchestration in `_state_build_cache_debug_evidence_from_args(...)`, including store/ledger opening, current-event lookup, projector construction, projection execution dispatch, read-model construction, optional summary snapshot save, and resource cleanup.

Stop point: this slice recovers only projection evidence. Further recovery should continue inside Evidence Collection only if implementation evidence shows a distinct next owner, most likely read-model evidence or timing evidence, and should stop if pressure belongs to a different owner.
