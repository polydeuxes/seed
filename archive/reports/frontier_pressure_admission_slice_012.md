# Frontier Pressure Admission Slice 012

## Selected boundary

Recovered implementation-local ownership boundary: **supported pressure-selection supporting-evidence payload preparation inside `selection_path_audit`**.

The selected boundary is the local handoff where `_from_pressure_selection(...)` stops owning the inline construction of the supporting-evidence payload for the selected pressure item. That responsibility is now carried by `_pressure_selection_supporting_evidence_payload(...)` before the existing selection-path compatibility handoff runs.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` around `selection_path_audit` and the implementation immediately adjacent to the recent `_pressure_selection_reason_payload(...)` slice. The current implementation already separated selected pressure item lookup, supported pressure-selection reason payload preparation, candidate-set preparation, selection-factor preparation, non-selected candidate preparation, typed unknown preparation, target matching, and unsupported-target selection preparation.

The adjacent supported-selection implementation still prepared supporting evidence inline inside `_from_pressure_selection(...)`:

- `_from_pressure_selection(...)` obtained the selected pressure item.
- `_from_pressure_selection(...)` converted that item into evidence with `_evidence(selected_item)`.
- `_from_pressure_selection(...)` wrapped the result in `_SelectionSupportingEvidencePayload(...)` using the same inline empty-evidence fallback when there was no selected item.

That made supported pressure-selection supporting-evidence payload preparation observable only as an inline expression in the broader supported pressure-selection assembly path.

## Before

`_from_pressure_selection(...)` directly constructed `_SelectionSupportingEvidencePayload(evidence=[_evidence(selected_item)] if selected_item else [])` while also assembling result, reason, lineage, candidate, factor, non-selected, and unknown payloads.

## After

`_from_pressure_selection(...)` delegates exactly that supporting-evidence payload preparation to `_pressure_selection_supporting_evidence_payload(selected_item)`. The helper owns only the conversion from a selected pressure item to `_SelectionSupportingEvidencePayload`, including the existing empty-evidence fallback for no selected item. It does not select candidates, match targets, produce reasons, mutate state, record facts, write events, or alter public output.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

Producer: `_pressure_selection_supporting_evidence_payload(...)`, called by `_from_pressure_selection(...)` while preparing supported pressure-selection audit output.

## Recovered artifact/helper

Artifact/helper: `_pressure_selection_supporting_evidence_payload(...)`, returning `_SelectionSupportingEvidencePayload`.

## Recovered consumer

Consumer: `_from_pressure_selection(...)` consumes the supporting-evidence payload and passes it unchanged into `_selection_path_from_payloads(...)`, which preserves the existing public `SelectionPathAudit.evidence` output.

## Compatibility preserved

No.

No compatibility boundary changed. Public CLI behavior, JSON shape, human-readable output, schema, diagnostic inventory behavior, diagnostic shape-audit behavior, event-ledger behavior, and read-only mutation boundary are preserved.

## LOC changed

- `seed_runtime/selection_path_audit.py`: 9 insertions, 3 deletions.
- `tests/test_selection_path_audit.py`: 31 insertions, 0 deletions.
- Total: 40 insertions, 3 deletions.

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 124 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   Supported pressure-selection assembly, selected-item evidence conversion, supporting-evidence payload construction, empty-evidence fallback, reason payload construction, candidate lineage construction, selection factors, non-selected candidates, and typed unknown transport were adjacent in `_from_pressure_selection(...)`. The selected compressed responsibility was only the supported-selection supporting-evidence payload preparation.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary between supported pressure-selection assembly and supported pressure-selection supporting-evidence payload preparation became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   `_from_pressure_selection(...)` now calls `_pressure_selection_supporting_evidence_payload(selected_item)`, and `tests/test_selection_path_audit.py` directly exercises populated and empty supporting-evidence payload production while proving it does not own outcome, candidate, or selection-factor fields.

4. **What producer now owns the recovered responsibility?**

   `_pressure_selection_supporting_evidence_payload(...)` owns the recovered responsibility.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_pressure_selection_supporting_evidence_payload(...)` carries the boundary and returns `_SelectionSupportingEvidencePayload`.

6. **Who consumes it?**

   `_from_pressure_selection(...)` consumes the helper result before handing the payload to `_selection_path_from_payloads(...)`.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining compression should be evaluated from current implementation evidence rather than campaign history, naming symmetry, or architectural preference. After this slice, nearby implementation responsibilities still include target-route ordering between focus and pressure-category paths, selected-name fallback preparation through `_selected_name(...)`, and the broader supported-selection orchestration in `_from_pressure_selection(...)`. They are not recovered here because this slice recovers exactly one implementation-local boundary supported by direct code pressure.
