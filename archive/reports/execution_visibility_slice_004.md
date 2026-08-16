# Execution Visibility Slice 004

## Selected architectural boundary

```text
Execution Visibility
    !=
Execution Diagnostics
```

This slice selected the `--current-facts-cache-debug` implementation because it already exposed both the current execution visibility output and diagnostic timing/cache evidence, while the returned report compressed those responsibilities into one data shape.

## Implementation evidence

- `--current-facts-cache-debug` is registered as an existing diagnostic surface with `supports_record=false`, `record_scope=none`, `writes_event_ledger=false`, and `mutates_cluster=false`.
- The CLI path still prints the current-facts output first and then prints the timing report.
- `_current_facts_timing_from_args` constructs both:
  - the operator-visible current-facts output; and
  - the cache/timing diagnostics used to inspect the execution path.
- `_format_current_facts_timing_report` consumes only cache status and timing details.

## Before

`CurrentFactsTimingReport` carried all fields directly:

```text
output
cache_status
timings
```

That meant the implementation returned visibility output and diagnostic evidence in one flattened report object even though the CLI behavior already treated them as different presentation sections.

## After

`CurrentFactsTimingReport` now has two implementation-local payloads:

```text
visibility: _CurrentFactsVisibilityPayload
    output

diagnostics: _CurrentFactsDiagnosticPayload
    cache_status
    timings
```

Compatibility properties preserve the previous access pattern:

```text
report.output
report.cache_status
report.timings
```

## Boundary made explicit

The recovered boundary is now directly observable in implementation:

```text
current-facts visibility payload
    !=
current-facts cache/timing diagnostic payload
```

The construction site still builds the same output, cache status, and timings, but it now returns them under separate implementation-local ownership.

## Compatibility preserved

No.

No compatibility boundary changed. The CLI flags, rendered output, diagnostic inventory declaration, shape-audit declaration, JSON behavior, recording behavior, event ledger behavior, and cluster mutation behavior remain unchanged.

## Files changed

- `scripts/seed_local.py`
  - Added `_CurrentFactsVisibilityPayload`.
  - Added `_CurrentFactsDiagnosticPayload`.
  - Changed `CurrentFactsTimingReport` to contain separated visibility and diagnostic payloads.
  - Preserved `output`, `cache_status`, and `timings` compatibility properties.
- `tests/test_seed_local_script.py`
  - Added a regression test proving the current-facts visibility output is separate from the cache/timing diagnostic payload while legacy report access still works.

## LOC changed

```text
scripts/seed_local.py            +27 -2
tests/test_seed_local_script.py  +25 -0
```

Total:

```text
+52 -2
```

## Tests executed

```text
pytest -q tests/test_seed_local_script.py -k 'current_facts_cache_debug'
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed execution visibility boundaries

Implementation evidence still suggests possible future slices, one boundary at a time:

- `state_build_cache_debug` still constructs state-build visibility, projection cache diagnostics, and timing/counter details in one report path.
- Projection build diagnostics are passed through cache-building paths and may still mix replay/build phase evidence with cache visibility labels at some call sites.
- Status-producing paths and diagnostic/audit surfaces remain separate in several modules, but additional implementation-local ownership boundaries may be recoverable where status output and later-inspection evidence share one return shape.
