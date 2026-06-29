# Timing Visibility Slice 008

## Selected architectural boundary

`Timing Diagnostic Payload != Timing Presentation`

The recovered implementation-local owner is `_CurrentFactsTimingPresentation`. It preserves only the existing current-facts timing report rendering responsibility.

## Implementation evidence

The implementation pressure was at `_format_current_facts_timing_report(...)`.

Before this slice, `_CurrentFactsTimingDiagnosticPayload` preserved interpreted timing evidence for diagnostic consumers, and `_CurrentFactsDiagnosticPayload` carried that preserved evidence into `CurrentFactsTimingReport`. However, `_format_current_facts_timing_report(...)` immediately consumed `report.cache_status` and `report.timings` and rendered the operator-facing timing text inline.

That kept the final transition compressed:

- diagnostic payload data selected the cache status and timing tuples;
- the formatter decided how those preserved diagnostics were rendered for the operator;
- the formatting responsibility had no local owner distinct from the compatibility wrapper function.

The evidence did not support a broader timing framework, normalized timing structure, CLI output change, JSON behavior change, event behavior change, cache behavior change, or projection behavior change.

## Before

The current-facts timing path flowed as:

```text
_CurrentFactsTimingInterpretation

↓

_CurrentFactsTimingDiagnosticPayload

↓

_CurrentFactsDiagnosticPayload / CurrentFactsTimingReport

↓

_format_current_facts_timing_report directly renders cache status and timings
```

Diagnostic payload construction was explicit, but presentation remained embedded in the formatter function body.

## After

The current-facts timing path now flows as:

```text
_CurrentFactsTimingInterpretation

↓

_CurrentFactsTimingDiagnosticPayload

↓

_CurrentFactsDiagnosticPayload / CurrentFactsTimingReport

↓

_CurrentFactsTimingPresentation.from_report(...)

↓

_CurrentFactsTimingPresentation.format()
```

`_CurrentFactsTimingPresentation` consumes the already-preserved timing diagnostics from `CurrentFactsTimingReport` and renders the exact existing text. It does not own elapsed-time measurement, timing interpretation, diagnostic payload construction, cache behavior, projection behavior, CLI flag handling, JSON behavior, event recording, or ledger replay.

## Boundary made explicit

The explicit recovered boundary is:

```text
_CurrentFactsTimingDiagnosticPayload
        !=
_CurrentFactsTimingPresentation
```

The diagnostic payload answers:

```text
What interpreted timing evidence is preserved for downstream use?
```

The presentation owner answers:

```text
How is that preserved timing evidence rendered for the operator?
```

## Compatibility preserved

No compatibility boundary changed.

The slice intentionally preserved:

- timing labels;
- elapsed values;
- diagnostic contents;
- formatted CLI output;
- JSON behavior;
- cache behavior;
- projection behavior;
- event behavior;
- ledger replay behavior.

The compatibility wrapper `_format_current_facts_timing_report(...)` remains in place and delegates to `_CurrentFactsTimingPresentation`.

## Questions

### 1. Where were timing diagnostic payload and timing presentation previously mixed?

They were mixed in `_format_current_facts_timing_report(...)`. That function consumed `CurrentFactsTimingReport.cache_status` and `CurrentFactsTimingReport.timings`, then directly rendered the cache and timing text. The report diagnostics had already preserved the timing payload, but the presentation step had no implementation-local owner beyond the formatter body.

### 2. Which recovered architectural boundary became more explicit?

`Timing Diagnostic Payload != Timing Presentation` became explicit through `_CurrentFactsTimingPresentation`.

### 3. How does the implementation now better reflect the recovered architecture?

The implementation now separates the preserved timing diagnostic payload from the rendering responsibility:

1. `_CurrentFactsTimingDiagnosticPayload` preserves interpreted timing evidence.
2. `_CurrentFactsDiagnosticPayload` carries that evidence in `CurrentFactsTimingReport`.
3. `_CurrentFactsTimingPresentation` renders the preserved evidence into the existing operator-facing timing text.
4. `_format_current_facts_timing_report(...)` remains a compatibility wrapper and no longer owns the rendering body directly.

### 4. Did implementation evidence suggest a more precise responsibility name than "Timing Presentation"?

Yes. The evidence supports the more precise local responsibility name `Current-Facts Timing Presentation`, represented by `_CurrentFactsTimingPresentation`, because the recovered owner is scoped to the current-facts timing report and only renders its existing cache-status and timing tuples.

### 5. Did any compatibility boundary change?

No.

## Files changed

- `scripts/seed_local.py`
- `tests/test_seed_local_script.py`
- `timing_visibility_slice_008.md`

## LOC changed

Before adding this report, implementation and test changes were:

```text
scripts/seed_local.py            +30 / -10
tests/test_seed_local_script.py  +34 / -0
```

Total before this report: `64 insertions`, `10 deletions`.

## Tests executed

```text
pytest -q tests/test_seed_local_script.py -k "current_facts_timing_presentation or current_facts_timing_diagnostic_payload or current_facts_timing_interpretation or current_facts_cache_debug"
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed timing responsibilities

- `_current_facts_timing_from_args(...)` still owns current-facts orchestration and several local measurements.
- `_TimingProjectionStore` still owns projection-store timing wrapper instrumentation.
- The compatibility bridge from `_CurrentFactsTimingDiagnosticPayload` into `_CurrentFactsDiagnosticPayload` remains current-facts-local.
- `_format_current_facts_timing_report(...)` remains as a stable compatibility wrapper around the recovered presentation owner.

## Stop point

This slice recovered exactly one implementation-local ownership boundary and stopped. Remaining pressure belongs to measurement/orchestration and store-wrapper instrumentation owners, not to the newly recovered presentation owner.
