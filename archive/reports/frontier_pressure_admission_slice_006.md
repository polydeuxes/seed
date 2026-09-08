# Frontier Pressure Admission Slice 006

Recovered implementation-local ownership boundary: **typed unknown payload ownership inside `selection_path_audit`**.

## Selected boundary

The selected boundary is the handoff where pressure-backed selection stops preparing candidate-set evidence-gap unknowns inline and carries typed unknown records through a named implementation-local payload before the unchanged public compatibility handoff into `SelectionPathAudit.unknowns`.

Expected compatibility answer: **No.**

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` around `_from_pressure_selection(...)`, `_SelectionLineagePayload`, `_candidate_set_from_pressures(...)`, `_non_selected_from_pressures(...)`, `_selection_factors_from_pressures(...)`, typed unknown preparation, selected-result preparation, selected-reason preparation, supporting-evidence preparation, and `_selection_path_from_payloads(...)`.

Implementation evidence showed that result, reason, supporting evidence, candidate set, non-selected candidates, and selection factors already had named implementation-local payloads or helpers. The remaining adjacent compressed responsibility was typed unknown transport:

1. `_SelectionLineagePayload` carried typed unknown records as a raw `list[TypedUnknownRecord]` beside named candidate-set, factor, and non-selected payloads.
2. `_from_pressure_selection(...)` prepared the pressure-backed evidence-gap unknown inline before constructing lineage.
3. The unsupported-target branch prepared its implementation unknown inline and handed a raw typed-unknown list into lineage.
4. `_selection_path_from_payloads(...)` converted lineage unknowns directly into the public `SelectionPathAudit.unknowns` list.

## Before

Typed unknown preparation and lineage assembly were compressed:

- `_from_pressure_selection(...)` created an inline `list[TypedUnknownRecord]` for missing pressure candidates.
- The unsupported-target path created an inline raw typed-unknown list for unimplemented targets.
- `_SelectionLineagePayload` carried `unknowns` as a raw list rather than a named ownership artifact.
- `_selection_path_from_payloads(...)` consumed the raw list and converted it to the public unknown shape.

## After

Typed unknown payload ownership is directly observable:

- `_SelectionUnknownPayload` owns implementation-local typed unknown transport.
- `_selection_unknowns_from_pressures(...)` prepares the pressure-backed evidence-gap unknown payload.
- `_SelectionLineagePayload` now carries `_SelectionUnknownPayload` rather than a raw typed-unknown list.
- `_selection_path_from_payloads(...)` performs the unchanged public compatibility handoff by converting `lineage.unknowns.unknowns` into public `SelectionPathAudit.unknowns`.
- Tests now instantiate and assert the unknown payload independently from candidate set, selection factors, and non-selected candidate ownership.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

Producer: `_selection_unknowns_from_pressures(...)`, called by `_from_pressure_selection(...)` when preparing pressure-backed selection lineage.

The unsupported-target path also now constructs `_SelectionUnknownPayload` explicitly before the existing lineage and public compatibility handoff.

## Recovered artifact/helper

- Artifact: `_SelectionUnknownPayload`
- Helper: `_selection_unknowns_from_pressures(...)`

## Recovered consumer

Internal consumers:

- `_SelectionLineagePayload`, which carries the typed unknown payload beside candidate-set, factor, and non-selected payloads.
- `_selection_path_from_payloads(...)`, which converts the typed unknown records to the unchanged public unknown dictionaries.

Public consumers remain unchanged:

- `SelectionPathAudit.unknowns`
- `selection_path_audit_json(...)`
- `format_selection_path_audit(...)`
- CLI `--selection-path` JSON and human-readable output

## Compatibility preserved

No compatibility boundary changed. The public `SelectionPathAudit` dataclass fields, JSON keys, human-readable sections, CLI behavior, diagnostic inventory registration, diagnostic shape-audit behavior, event-ledger behavior, and read-only mutation boundary remain unchanged.

## LOC changed

```text
seed_runtime/selection_path_audit.py | 50 +++++++++++++++++++++++-------------
tests/test_selection_path_audit.py   | 37 ++++++++++++++++++++++----
2 files changed, 64 insertions(+), 23 deletions(-)
```

## Tests executed

- `python -m pytest -q tests/test_selection_path_audit.py`
- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py`
- `python -m pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Required questions

### 1. What responsibilities were previously compressed?

Typed unknown preparation, typed unknown transport through lineage, and public unknown compatibility conversion were compressed around `_from_pressure_selection(...)`, unsupported-target lineage construction, `_SelectionLineagePayload`, and `_selection_path_from_payloads(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

Typed unknown payload ownership became directly observable before public `SelectionPathAudit.unknowns` compatibility conversion.

### 3. What implementation and/or test change made the boundary observable?

Implementation now has `_SelectionUnknownPayload`, `_selection_unknowns_from_pressures(...)`, and `_SelectionLineagePayload.unknowns` typed as `_SelectionUnknownPayload`. Tests now construct lineage with `_SelectionUnknownPayload` and assert `_selection_unknowns_from_pressures(...)` is separate from candidate-set, selection-factor, and non-selected ownership.

### 4. What producer now owns the recovered responsibility?

`_selection_unknowns_from_pressures(...)` owns pressure-backed typed unknown payload preparation.

### 5. What artifact or helper carries the recovered boundary, if any?

`_SelectionUnknownPayload` carries the recovered boundary, with `_selection_unknowns_from_pressures(...)` producing the pressure-backed instance.

### 6. Who consumes it?

`_SelectionLineagePayload` consumes it internally, and `_selection_path_from_payloads(...)` consumes it to populate unchanged public `SelectionPathAudit.unknowns`.

### 7. Did any compatibility boundary change?

No.

## Remaining compressed responsibilities

Directly adjacent responsibilities that may still warrant future implementation-evidence investigation include unsupported-target refusal preparation, selected-result compatibility handoff details, pressure-backed selection admission preparation, diagnostic read-only handoff preparation, and broader lineage assembly. This slice does not claim any of those boundaries; it recovers only typed unknown payload ownership.
