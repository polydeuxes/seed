# State-Build Cache Debug Slice 007

## Selected architectural boundary

```text
State-Build Cache Debug Timing Evidence

↓

_StateBuildCacheDebugTimingEvidence

↓

_StateBuildCacheDebugEvidenceAssembly
```

This slice recovered exactly one implementation-local ownership boundary inside **State-Build Cache Debug Evidence Collection**. The selected boundary is the final recurring evidence stream consumed by `_StateBuildCacheDebugEvidenceAssembly`: timing evidence.

This completes the recurring evidence streams consumed by `_StateBuildCacheDebugEvidenceAssembly`; the next step can be a bounded family completion audit rather than another ownership slice.

## Implementation evidence

Evidence Assembly already consumed explicit evidence streams for cache, projection, and read-model evidence. Timing evidence was still compressed into the assembly call sites:

- Warm summary-cache hit path collected local timings, appended `("total runtime", ...)` inline, and immediately called `_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)`.
- Cold projection/build path collected local timings, appended `("total runtime", ...)` inline, and immediately called `_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)`.
- Existing timing labels were already recurring implementation facts: summary-cache timing, projection timing, build timing, rendering timing, and total runtime.

The implementation evidence supported `State-Build Cache Debug Timing Evidence` as the precise remaining stream. It did not support moving timing measurement, projection execution, cache semantics, read-model construction, report construction, presentation, JSON, events, or ledger behavior.

## Before

```text
_state_build_cache_debug_evidence_from_args(...)

↓

local timings list + inline total runtime append

↓

_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)
```

Timing evidence was mixed with Evidence Assembly at both return sites in `_state_build_cache_debug_evidence_from_args(...)`.

## After

```text
_state_build_cache_debug_evidence_from_args(...)

↓

_StateBuildCacheDebugTimingEvidence

↓

_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)
```

The same collected timing labels and values are preserved, but Evidence Assembly now consumes timing evidence as an explicit implementation-local artifact.

## Recovered producer

`_state_build_cache_debug_evidence_from_args(...)` remains the broader State-Build Cache Debug Evidence Collection owner. For this slice, it produces `_StateBuildCacheDebugTimingEvidence` after timing observations have already been collected.

## Recovered artifact

`_StateBuildCacheDebugTimingEvidence` is the recovered implementation-local artifact.

It owns only the existing timing evidence stream shape consumed by the assembly boundary:

- existing timing label/value pairs;
- the existing `total runtime` label/value append.

It does not own timing measurement. The local `timed(...)` helper still performs measurement, and the existing work phases still define their own labels.

## Consumer of the artifact

`_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)` now consumes `_StateBuildCacheDebugTimingEvidence` alongside:

- `_StateBuildCacheDebugCacheEvidence`;
- `_StateBuildCacheDebugProjectionEvidence`;
- `_StateBuildCacheDebugReadModelEvidence`.

## Compatibility preserved

No compatibility boundary changed.

Behavior, cache semantics, projection behavior, read-model behavior, report contents, CLI output, JSON, events, ledger behavior, timing labels, and compatibility remain unchanged.

## Explicit questions

### 1. Where was the selected timing evidence stream previously mixed with Evidence Assembly?

It was mixed inside `_state_build_cache_debug_evidence_from_args(...)` at the warm summary-cache hit return site and the cold projection/build return site. Both paths appended `("total runtime", time.perf_counter() - started)` inline while invoking `_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)`.

### 2. Which recovered architectural boundary became more explicit?

```text
State-Build Cache Debug Timing Evidence

↓

_StateBuildCacheDebugTimingEvidence

↓

State-Build Cache Debug Evidence Assembly
```

### 3. What implementation artifact is now produced, and who consumes it?

`_StateBuildCacheDebugTimingEvidence` is now produced by `_state_build_cache_debug_evidence_from_args(...)` and consumed by `_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)`.

### 4. Did implementation evidence suggest a more precise responsibility name?

Insufficient implementation evidence.

### 5. Did any compatibility boundary change?

No.

## Files changed

- `scripts/seed_local.py`
- `tests/test_seed_local_script.py`
- `state_build_cache_debug_slice_007.md`

## LOC changed

```text
scripts/seed_local.py                  | 34 ++++++++++++++++++++++++++--------
tests/test_seed_local_script.py        | 37 +++++++++++++++++++++++++++++++++++--
state_build_cache_debug_slice_007.md   | 156 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

## Tests executed

```text
python -m py_compile scripts/seed_local.py
pytest -q tests/test_seed_local_script.py -q
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed State-Build Cache Debug responsibilities

The recurring evidence streams consumed by `_StateBuildCacheDebugEvidenceAssembly` are now explicit:

```text
_StateBuildCacheDebugCacheEvidence
_StateBuildCacheDebugProjectionEvidence
_StateBuildCacheDebugReadModelEvidence
_StateBuildCacheDebugTimingEvidence
```

No further recurring evidence stream remains compressed into Evidence Assembly based on the current implementation evidence. Remaining State-Build Cache Debug responsibilities should be evaluated with a bounded family completion audit before selecting another ownership slice.
