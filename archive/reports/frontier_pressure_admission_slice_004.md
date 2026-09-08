# Frontier Pressure Admission Slice 004

## Selected boundary

Recovered implementation-local ownership boundary: **non-selected candidate explanation ownership inside `selection_path_audit`**.

The selected boundary is the handoff where pressure-backed selection stops constructing the selected candidate set and separately prepares the public `SelectionPathAudit.non_selected` explanations through `_SelectionNonSelectedPayload` and `_non_selected_from_pressures(...)`.

This is not Frontier Pressure Admission. It is not readiness evaluation, planning, prioritization, scheduling, or a new framework. It only recovers one already-evidenced local responsibility in the selection-path audit implementation.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` adjacent to the previously documented selected supporting-evidence slice.

Evidence found:

1. `_SelectionResultPayload`, `_SelectionReasonPayload`, `_SelectionSupportingEvidencePayload`, and `_SelectionCandidateSetPayload` already made neighboring ownership boundaries observable.
2. `_SelectionLineagePayload` still carried `non_selected` as a raw `list[dict[str, Any]]`, while candidate-set ownership had a named payload.
3. `_from_pressure_selection(...)` still prepared non-selected explanations inline with a list comprehension over `pressures[1:]`.
4. `_non_selected(...)` already encoded the explanation rules for non-selected candidates, showing an implementation-local responsibility separate from candidate construction, selected result, selected reason, supporting evidence, and typed Unknown production.
5. `_selection_path_from_payloads(...)` was already the compatibility handoff into public `SelectionPathAudit`, so the recovery could make the local producer/payload boundary visible without changing JSON, text output, CLI behavior, diagnostics, schema, event-ledger behavior, or cluster mutation behavior.

## Before

The non-selected candidate explanation responsibility was compressed in implementation:

- `_from_pressure_selection(...)` constructed the non-selected explanation list inline.
- `_SelectionLineagePayload` carried that list directly as `list[dict[str, Any]]`.
- `_selection_path_from_payloads(...)` copied the raw list into `SelectionPathAudit.non_selected`.
- Tests observed public non-selected output as a list, but did not prove a named implementation-local artifact owned non-selected explanation preparation separately from candidate-set preparation.

## After

Exactly one implementation-local boundary is now directly observable:

- `_SelectionNonSelectedPayload` carries only non-selected candidate explanations.
- `_non_selected_from_pressures(...)` prepares that payload from pressure order and the selected pressure item.
- `_SelectionLineagePayload` now carries the named non-selected payload instead of a raw list.
- `_selection_path_from_payloads(...)` performs the unchanged public handoff by assigning `lineage.non_selected.non_selected` to `SelectionPathAudit.non_selected`.
- `test_selection_non_selected_payload_is_separate_from_candidate_set` proves the payload is separate from candidate-set, factor, and unknown ownership.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

Producer: `_non_selected_from_pressures(...)`, called by `_from_pressure_selection(...)` after the selected pressure item is known.

The existing `_non_selected(...)` helper continues to own the individual explanation rule for lower-score and same-score alternatives. The newly recovered producer owns preparation of the non-selected explanation payload for the selection-path lineage handoff.

## Recovered artifact/helper

Recovered artifact/helper: `_SelectionNonSelectedPayload`.

Carrying helper: `_non_selected_from_pressures(...)`.

The artifact carries only `non_selected: list[dict[str, Any]]`; it does not carry candidates, selection factors, selected value, outcome reason, supporting evidence, or typed Unknown records.

## Recovered consumer

Consumers:

- `_SelectionLineagePayload`, which carries the non-selected payload alongside candidate-set, selection-factor, and typed Unknown lineage material;
- `_selection_path_from_payloads(...)`, which performs the compatibility handoff;
- `SelectionPathAudit.non_selected`;
- `selection_path_audit_json(...)` through `SelectionPathAudit.to_json_dict()`;
- `format_selection_path_audit(...)`, which renders the non-selected candidates section;
- the CLI path behind `seed --selection-path`.

## Compatibility preserved

No.

No compatibility boundary changed.

Preserved surfaces:

- public CLI behavior;
- JSON shape;
- human-readable output;
- diagnostics;
- schema;
- event-ledger behavior;
- cluster mutation behavior;
- read-only selection-path boundary;
- unsupported-target refusal behavior;
- typed Unknown public shape.

## Required questions

### 1. What responsibilities were previously compressed?

Non-selected candidate explanation preparation was compressed with pressure-backed selection lineage construction. `_from_pressure_selection(...)` prepared the non-selected list inline while `_SelectionLineagePayload` carried it as a raw list next to candidate-set, factor, and typed Unknown material.

### 2. Which implementation-local ownership boundary became directly observable?

The non-selected candidate explanation ownership boundary became directly observable.

### 3. What implementation and/or test change made the boundary observable?

Implementation now has `_SelectionNonSelectedPayload` and `_non_selected_from_pressures(...)`, and `_SelectionLineagePayload` carries that payload instead of a raw list. Tests now instantiate the payload at lineage handoffs and assert that the non-selected payload is separate from candidate-set, selection-factor, and unknown ownership.

### 4. What producer now owns the recovered responsibility?

`_non_selected_from_pressures(...)` owns non-selected payload preparation for pressure-backed selection lineage.

### 5. What artifact or helper carries the recovered boundary, if any?

`_SelectionNonSelectedPayload` carries the recovered boundary, with `_non_selected_from_pressures(...)` preparing it.

### 6. Who consumes it?

`_SelectionLineagePayload` and `_selection_path_from_payloads(...)` consume it internally. Public consumers continue to consume unchanged `SelectionPathAudit.non_selected`, JSON output, human-readable output, and CLI output.

### 7. Did any compatibility boundary change?

No.

## LOC changed

Implementation/test change before this report:

- `seed_runtime/selection_path_audit.py`: 20 insertions, 6 deletions.
- `tests/test_selection_path_audit.py`: 44 insertions, 4 deletions.

## Tests executed

- `python scripts/seed_local.py --selection-path current_focus --json`
- `python scripts/seed_local.py --selection-path unknown-frontier-candidate --json`
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

Remaining compressed responsibilities were intentionally not recovered in this slice:

- implemented-target admission ownership beyond existing local target matching;
- selection-factor payload ownership;
- typed Unknown production beyond the existing lineage handoff;
- unsupported-target lawful refusal beyond the existing unsupported branch;
- target normalization and matching ownership;
- public rendering ownership;
- Frontier Pressure Admission;
- readiness evaluation;
- prioritization;
- investigation planning;
- scheduler or planner behavior.
