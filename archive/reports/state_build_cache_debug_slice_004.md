# State-Build Cache Debug Slice 004

## Selected architectural boundary

State-Build Cache Debug Cache Evidence is now explicit as an implementation-local boundary before State-Build Cache Debug Evidence Assembly.

Recovered chain:

```text
State-Build Cache Debug Cache Evidence Collection

↓

_StateBuildCacheDebugCacheEvidence

↓

_StateBuildCacheDebugEvidenceAssembly

↓

_StateBuildCacheDebugEvidence

↓

_StateBuildCacheDebugReportPayload

↓

StateSummaryCacheDebugReport
```

## Implementation evidence

The compressed pressure was in `_state_build_cache_debug_evidence_from_args(...)`, where the same return sites collected cache-related visibility and projection-cache diagnostics, then immediately shaped `_StateBuildCacheDebugEvidenceAssembly`.

The implementation evidence is the repeated pairing of:

- `_StateBuildVisibilityPayload`, containing cache eligibility, summary cache status, current and cached summary event ids, and cache notes;
- `_ProjectionCacheDiagnosticPayload`, containing projection/state cache status, cached state event id, projection timings, and projection counters;
- local timing evidence added separately when producing `_StateBuildCacheDebugEvidenceAssembly`.

The summary-cache hit path already has cache evidence without projection replay subphase timings or counters. The cold projection/build path has the same cache evidence shape after projection diagnostic selection. Both paths now converge by producing `_StateBuildCacheDebugCacheEvidence`, and assembly consumes that artifact with the local timing list.

## Before

```text
_state_build_cache_debug_evidence_from_args(...)

↓

_StateBuildCacheDebugEvidenceAssembly

↓

_StateBuildCacheDebugEvidence
```

The evidence collection function mixed cache-evidence ownership with assembly ownership at both the summary-cache hit return and projection/build return.

## After

```text
_state_build_cache_debug_evidence_from_args(...)

↓

_StateBuildCacheDebugCacheEvidence

↓

_StateBuildCacheDebugEvidenceAssembly.from_cache_evidence(...)

↓

_StateBuildCacheDebugEvidence
```

The evidence collection function still owns the broader state-build cache-debug evidence collection lifecycle, but cache evidence is now a directly observable implementation-local artifact before assembly adds local timing evidence.

## Recovered producer

`_state_build_cache_debug_evidence_from_args(...)` is the recovered producer for this slice.

It produces `_StateBuildCacheDebugCacheEvidence` after the relevant cache evidence has been collected:

- summary cache eligibility/status;
- current and cached summary event ids;
- state/projection cache status;
- cached state event id;
- cache notes;
- projection diagnostic selection output when the projection/build path runs.

## Recovered artifact

`_StateBuildCacheDebugCacheEvidence` is the recovered implementation-local artifact.

It preserves existing evidence only:

- `visibility: _StateBuildVisibilityPayload`
- `projection_diagnostics: _ProjectionCacheDiagnosticPayload`

It does not own projection execution, read-model construction, summary publication, report construction, CLI formatting, JSON behavior, events, or ledger replay.

## Consumer of the artifact

`_StateBuildCacheDebugEvidenceAssembly.from_cache_evidence(...)` consumes `_StateBuildCacheDebugCacheEvidence` and combines it with local timing evidence to produce `_StateBuildCacheDebugEvidenceAssembly`.

Downstream consumers remain unchanged:

- `_StateBuildCacheDebugEvidence.from_assembly(...)` still consumes `_StateBuildCacheDebugEvidenceAssembly`.
- `_StateBuildCacheDebugReportPayload.from_evidence(...)` still consumes `_StateBuildCacheDebugEvidence`.
- `StateSummaryCacheDebugReport.from_payload(...)` still consumes `_StateBuildCacheDebugReportPayload`.

## Compatibility preserved

No compatibility boundary changed.

Preserved behavior includes:

- cache behavior;
- projection behavior;
- read-model behavior;
- summary cache hit/miss behavior;
- projection cache hit/miss behavior;
- diagnostic contents;
- report contents;
- CLI output;
- JSON behavior;
- events;
- ledger replay;
- timing labels;
- timing values.

## Questions

### 1. Where was the selected evidence-collection responsibility previously mixed?

It was mixed inside `_state_build_cache_debug_evidence_from_args(...)`, specifically at the summary-cache hit return and the projection/build return. Those return sites built `_StateBuildVisibilityPayload` and `_ProjectionCacheDiagnosticPayload` while directly constructing `_StateBuildCacheDebugEvidenceAssembly`.

### 2. Which recovered architectural boundary became more explicit?

The boundary between State-Build Cache Debug Cache Evidence and State-Build Cache Debug Evidence Assembly became explicit.

### 3. What implementation artifact is now produced, and who consumes it?

`_StateBuildCacheDebugCacheEvidence` is now produced by `_state_build_cache_debug_evidence_from_args(...)` and consumed by `_StateBuildCacheDebugEvidenceAssembly.from_cache_evidence(...)`.

### 4. Did implementation evidence suggest a more precise responsibility name than the prompt examples?

No. The implementation evidence matched the prompt example `State-Build Cache Debug Cache Evidence`: the recovered artifact carries cache eligibility/status, cache notes, state/projection cache status, cached event ids, and projection-cache diagnostic selections.

### 5. Did any compatibility boundary change?

No.

## Files changed

- `scripts/seed_local.py`
- `tests/test_seed_local_script.py`
- `state_build_cache_debug_slice_004.md`

## LOC changed

Measured with `git diff --stat` before commit:

```text
scripts/seed_local.py                    | 79 ++++++++++++++++++++++++++---------------
tests/test_seed_local_script.py          | 31 ++++++++++++++++
state_build_cache_debug_slice_004.md     | 192 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
3 files changed, 274 insertions(+), 28 deletions(-)
```

## Tests executed

```text
python -m py_compile scripts/seed_local.py
pytest -q tests/test_seed_local_script.py -q
pytest -q tests/test_seed_local_script.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py -q
```

## Remaining compressed State-Build Cache Debug responsibilities

The recovered cache-evidence boundary stops before responsibilities that still belong to different owners. Remaining compressed pressure includes:

1. Summary cache lookup mechanics versus state/projection cache lookup mechanics.
2. Projection diagnostic selection versus projection diagnostic production.
3. Local timing collection versus cache-evidence production.
4. Read-model construction inputs versus summary cache publication.
5. Projection/build execution versus diagnostic report evidence collection.

Stop point: this slice made exactly one implementation-local cache-evidence owner directly observable. Remaining pressure belongs to different owners inside the broader State-Build Cache Debug Evidence Collection lifecycle.
