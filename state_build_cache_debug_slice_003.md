# State-Build Cache Debug Slice 003

## Selected architectural boundary

State-Build Cache Debug Evidence Assembly was recovered between state-build cache-debug evidence collection and the final `_StateBuildCacheDebugEvidence` artifact.

```text
State-Build Cache Debug Evidence Collection
    produces
_StateBuildCacheDebugEvidenceAssembly
    consumed by
_StateBuildCacheDebugEvidence
```

This slice remains inside State-Build Cache Debug Evidence Collection. It does not move projection execution, read-model construction, cache semantics, report construction, presentation, CLI behavior, JSON behavior, events, or ledger replay.

## Implementation evidence

- `_state_build_cache_debug_evidence_from_args(...)` still owns the broader evidence collection lifecycle: projection store opening, ledger opening, current event lookup, summary cache lookup, optional state cache lookup, projector construction, projection replay/build, read-model derivation, optional summary snapshot save, projection diagnostic selection, and local timing collection.
- The same function previously also performed final evidence assembly by directly constructing `_StateBuildCacheDebugEvidence` at each return site.
- Both final return paths assemble the same three already-collected implementation-local inputs: `_StateBuildVisibilityPayload`, `_ProjectionCacheDiagnosticPayload`, and local timings.
- The warm summary-cache hit path and cold projection/build path recur as separate collection paths but converge on the same assembly shape before producing `_StateBuildCacheDebugEvidence`.
- `_StateBuildCacheDebugEvidence` remains the artifact consumed by `_StateBuildCacheDebugReportPayload.from_evidence(...)`, preserving the previously recovered report-payload boundary.

## Before

```text
_state_build_cache_debug_evidence_from_args(...)
    collects cache lookup, projection, read-model, diagnostic, and timing evidence
    directly constructs
_StateBuildCacheDebugEvidence
    consumed by
_StateBuildCacheDebugReportPayload.from_evidence(...)
```

Evidence Collection and Evidence Assembly were mixed inside `_state_build_cache_debug_evidence_from_args(...)`. The collection path gathered evidence-producing inputs and also directly owned the final `_StateBuildCacheDebugEvidence` construction at both the summary-cache hit return and the projection/build return.

## After

```text
_state_build_cache_debug_evidence_from_args(...)
    collects cache lookup, projection, read-model, diagnostic, and timing evidence
    produces
_StateBuildCacheDebugEvidenceAssembly
    consumed by
_StateBuildCacheDebugEvidence.from_assembly(...)
    produces
_StateBuildCacheDebugEvidence
    consumed by
_StateBuildCacheDebugReportPayload.from_evidence(...)
```

The recovered assembly artifact is now directly observable at the convergence point between collected implementation-local payloads and final evidence.

## Recovered producer

`_state_build_cache_debug_evidence_from_args(...)` is still the broader State-Build Cache Debug Evidence Collection owner. For this slice, it now produces `_StateBuildCacheDebugEvidenceAssembly` after it has collected the visibility payload, projection diagnostic payload, and timing evidence.

It may consume or observe:

- cache lookup evidence;
- state-build visibility;
- projection diagnostic selection;
- read-model evidence;
- timing evidence.

It does not transfer ownership of projection execution, read-model construction, cache semantics, report payload construction, report construction, presentation, CLI behavior, JSON behavior, events, or ledger replay.

## Recovered artifact

`_StateBuildCacheDebugEvidenceAssembly` is the recovered implementation-local artifact.

It preserves only the final evidence assembly inputs:

- `_StateBuildVisibilityPayload`;
- `_ProjectionCacheDiagnosticPayload`;
- local state-build cache-debug timings.

## Consumer of the artifact

`_StateBuildCacheDebugEvidence.from_assembly(...)` consumes `_StateBuildCacheDebugEvidenceAssembly` and produces `_StateBuildCacheDebugEvidence`.

Downstream consumers remain unchanged: `_StateBuildCacheDebugReportPayload.from_evidence(...)` still consumes `_StateBuildCacheDebugEvidence`, and `StateSummaryCacheDebugReport.from_payload(...)` still consumes `_StateBuildCacheDebugReportPayload`.

## Compatibility preserved

No compatibility boundary changed.

- `state_summary_cache_debug_from_args(...)` still returns `StateSummaryCacheDebugReport`.
- `_state_build_cache_debug_evidence_from_args(...)` still returns `_StateBuildCacheDebugEvidence`.
- `_StateBuildCacheDebugReportPayload.from_evidence(...)` still consumes `_StateBuildCacheDebugEvidence`.
- Existing report properties remain unchanged.
- CLI output, format text, JSON behavior, events, ledger replay, cache behavior, projection behavior, read-model behavior, diagnostic contents, report contents, and timing labels are unchanged.

## Answers to required questions

1. **Where were Evidence Collection and Evidence Assembly previously mixed?**

   They were mixed inside `_state_build_cache_debug_evidence_from_args(...)`, where the function collected cache lookup evidence, projection diagnostic evidence, read-model evidence, state-build visibility, and local timings, then directly constructed `_StateBuildCacheDebugEvidence` at each return site.

2. **Which recovered architectural boundary became more explicit?**

   The boundary between State-Build Cache Debug Evidence Collection and State-Build Cache Debug Evidence Assembly became explicit through `_StateBuildCacheDebugEvidenceAssembly`.

3. **What implementation artifact is now produced, and who consumes it?**

   `_StateBuildCacheDebugEvidenceAssembly` is produced by `_state_build_cache_debug_evidence_from_args(...)` and consumed by `_StateBuildCacheDebugEvidence.from_assembly(...)`.

4. **Did implementation evidence suggest a more precise responsibility name than "Evidence Assembly"?**

   Insufficient implementation evidence.

5. **Did any compatibility boundary change?**

   No.

## Files changed

- `scripts/seed_local.py`
- `tests/test_seed_local_script.py`
- `state_build_cache_debug_slice_003.md`

## LOC changed

Final repository diff for this slice:

```text
scripts/seed_local.py: 54 insertions, 33 deletions
tests/test_seed_local_script.py: 30 insertions
state_build_cache_debug_slice_003.md: 152 insertions
```

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
pytest -q tests/test_seed_local_script.py -k 'state_summary_cache_debug'
```

Results:

- diagnostic inventory and shape-audit checks passed, 44 tests selected.
- state summary cache debug checks passed, 7 tests selected.

## Remaining compressed State-Build Cache Debug responsibilities

- Evidence Collection still owns cache-debug lifecycle measurement, projection store opening, ledger opening, event listing, cache lookup evidence gathering, projection invocation evidence, read-model derivation evidence, summary snapshot publication evidence, and projection diagnostic selection in one implementation path.
- Evidence Assembly is now explicit, but its inputs may still contain smaller implementation-local boundaries if future implementation evidence justifies recovering them.
- Report payload construction remains closed from slice 002.
- Report construction and presentation remain downstream and unchanged.

Stop point: the recovered assembly boundary now separates collected evidence inputs from final `_StateBuildCacheDebugEvidence` construction. Remaining pressure belongs to earlier evidence-producing activities inside Evidence Collection, not to this recovered owner.
