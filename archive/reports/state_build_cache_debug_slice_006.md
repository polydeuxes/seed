# State-Build Cache Debug Slice 006

## Selected architectural boundary

State-Build Cache Debug Read-Model Evidence is now separated from State-Build Cache Debug Evidence Assembly.

```text
State-Build Cache Debug Read-Model Evidence

↓

_StateBuildCacheDebugReadModelEvidence

↓

_StateBuildCacheDebugEvidenceAssembly
```

The selected boundary remains inside **State-Build Cache Debug Evidence Collection** and recovers exactly one implementation-local ownership boundary.

## Implementation evidence

Implementation review showed the recurring read-model-related stream was mixed into the evidence assembly return sites inside `_state_build_cache_debug_evidence_from_args(...)`:

- Warm summary-cache hit path reconstructs the cached `StateSummary` payload, skips projection-cache work, then immediately assembled `_StateBuildCacheDebugEvidenceAssembly`.
- Cold projection/build path constructs compact `StateSummary`, constructs operator `state_summary`, optionally saves the state-summary snapshot, then immediately assembled `_StateBuildCacheDebugEvidenceAssembly`.
- Both paths already had cache evidence and projection evidence artifacts before assembly, but the read-model-related evidence was implicit in local variables and control flow.

The strongest implementation evidence supported the responsibility name **State-Build Cache Debug Read-Model Evidence** because the recurring stream is derived from read-model construction or read-model snapshot reuse, not from projection execution or report presentation.

## Before

```text
_state_build_cache_debug_evidence_from_args(...)

↓

read-model snapshot decode or read-model construction / optional summary snapshot save

↓

_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)
```

The read-model evidence stream was compressed into `_state_build_cache_debug_evidence_from_args(...)` at the same return sites that created evidence assembly.

## After

```text
_state_build_cache_debug_evidence_from_args(...)

↓

_StateBuildCacheDebugReadModelEvidence

↓

_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)
```

The read-model evidence stream now has an implementation-local artifact before assembly consumes it.

## Recovered producer

`_state_build_cache_debug_evidence_from_args(...)` remains the producer inside the broader Evidence Collection owner.

It now produces `_StateBuildCacheDebugReadModelEvidence` after the relevant read-model path has occurred:

- `summary_source="summary snapshot"` when the summary snapshot satisfies the request;
- `summary_source="constructed read model"` when the cold projection/build path derives the summaries;
- `summary_snapshot_published` records whether this debug run published a summary snapshot after constructing the read model.

## Recovered artifact

`_StateBuildCacheDebugReadModelEvidence` is the recovered implementation-local artifact.

It preserves only the existing read-model-related evidence stream:

- whether the summary came from a summary snapshot or constructed read model;
- whether the summary snapshot was published during the run.

It does not own read-model construction, read-model cache publication, projection execution, cache semantics, report payload construction, presentation, CLI behavior, JSON behavior, events, ledger replay, or timing behavior.

## Consumer of the artifact

`_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)` now consumes `_StateBuildCacheDebugReadModelEvidence` alongside the previously recovered cache evidence and projection evidence artifacts.

Downstream compatibility remains unchanged:

```text
_StateBuildCacheDebugEvidenceAssembly

↓

_StateBuildCacheDebugEvidence.from_assembly(...)

↓

_StateBuildCacheDebugReportPayload.from_evidence(...)

↓

StateSummaryCacheDebugReport.from_payload(...)
```

## Questions

### 1. Where was the selected read-model evidence stream previously mixed with Evidence Assembly?

It was mixed inside `_state_build_cache_debug_evidence_from_args(...)` at the warm summary-cache hit return and the cold projection/build return. The warm path decoded the cached summary snapshot and immediately assembled evidence. The cold path constructed the compact summary, constructed the operator summary, optionally saved a summary snapshot, and immediately assembled evidence.

### 2. Which recovered architectural boundary became more explicit?

The boundary between **State-Build Cache Debug Read-Model Evidence** and **State-Build Cache Debug Evidence Assembly** became explicit.

### 3. What implementation artifact is now produced, and who consumes it?

`_StateBuildCacheDebugReadModelEvidence` is now produced by `_state_build_cache_debug_evidence_from_args(...)` and consumed by `_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)`.

### 4. Did implementation evidence suggest a more precise responsibility name?

Yes. The implementation evidence suggested **State-Build Cache Debug Read-Model Evidence** because the recurring stream follows summary snapshot reuse, summary construction, operator summary construction, and summary snapshot publication evidence.

### 5. Did any compatibility boundary change?

No.

## Compatibility preserved

No public compatibility boundary changed:

- `state_summary_cache_debug_from_args(...)` still returns `StateSummaryCacheDebugReport`.
- `StateSummaryCacheDebugReport` public properties are unchanged.
- CLI output remains unchanged.
- JSON behavior remains unchanged.
- Event and ledger behavior remain unchanged.
- Projection behavior, cache behavior, read-model behavior, summary construction behavior, summary publication behavior, timing labels, and timing values remain unchanged.

## Files changed

- `scripts/seed_local.py`
- `tests/test_seed_local_script.py`
- `state_build_cache_debug_slice_006.md`

## LOC changed

```text
scripts/seed_local.py                  | 25 +++++++++++++++++++++++++
tests/test_seed_local_script.py        | 25 +++++++++++++++++++++++--
state_build_cache_debug_slice_006.md   | 176 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

## Tests executed

```text
pytest -q tests/test_seed_local_script.py -k 'state_summary_cache_debug'
```

Result: 9 passed, 156 deselected.

## Remaining compressed State-Build Cache Debug responsibilities

Remaining pressure inside State-Build Cache Debug Evidence Collection appears limited to earlier orchestration and evidence-producing activities:

- projection store and ledger opening;
- current-event lookup;
- summary-cache lookup;
- optional state-cache lookup and state snapshot decode;
- state projector construction;
- projection execution dispatch;
- read-model construction execution itself;
- summary snapshot publication execution itself;
- local timing collection;
- resource cleanup.

The recovered owner for this slice stops at read-model evidence production. Implementation evidence did not justify moving read-model construction, summary publication, cache semantics, projection execution, or report/presentation ownership into this recovered responsibility.
