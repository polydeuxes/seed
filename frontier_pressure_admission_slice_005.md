# Frontier Pressure Admission Slice 005

## Selected boundary

Recovered implementation-local ownership boundary: **selection-factor payload ownership inside `selection_path_audit`**.

The selected boundary is the handoff where pressure-backed selection stops deriving ordering factors inline and instead prepares the public `SelectionPathAudit.selection_factors` material through a named implementation-local payload.

This is not Frontier Pressure Admission. It is not readiness evaluation, planning, prioritization, scheduling, or a new framework. It only recovers one implementation-evidenced local responsibility in the selection-path audit implementation.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` and the adjacent tests around `_from_pressure_selection(...)`, `_candidate_set_from_pressures(...)`, `_non_selected_from_pressures(...)`, typed unknown preparation, selected-result handoff, lineage payload construction, and the public `SelectionPathAudit` compatibility handoff.

Evidence found:

1. `_SelectionResultPayload`, `_SelectionReasonPayload`, `_SelectionSupportingEvidencePayload`, `_SelectionCandidateSetPayload`, and `_SelectionNonSelectedPayload` already made neighboring ownership boundaries observable.
2. `_SelectionLineagePayload` still carried `selection_factors` as a raw `list[str]`, while candidate-set and non-selected material had named payload ownership.
3. `_from_pressure_selection(...)` still derived the pressure-ordering factor inline before constructing `_SelectionLineagePayload`.
4. The unsupported-target branch still supplied `selection_factors=["unknown"]` directly while constructing lineage.
5. `_selection_path_from_payloads(...)` was already the compatibility handoff into public `SelectionPathAudit`, so the recovery could make the local producer/payload boundary visible without changing JSON, text output, CLI behavior, diagnostics, schema, event-ledger behavior, or cluster mutation behavior.

## Before

Selection-factor preparation was compressed in implementation:

- `_from_pressure_selection(...)` constructed the pressure ordering explanation inline as a local `factors` list.
- The unsupported-target branch constructed the `unknown` factor directly inside `_SelectionLineagePayload` construction.
- `_SelectionLineagePayload` carried the raw factor list beside candidate-set, non-selected, and typed Unknown lineage material.
- `_selection_path_from_payloads(...)` copied the raw list into `SelectionPathAudit.selection_factors`.
- Tests observed public factor output, but did not prove a named implementation-local artifact owned factor preparation separately from candidate-set, non-selected, and unknown ownership.

## After

Exactly one implementation-local boundary is now directly observable:

- `_SelectionFactorPayload` carries only selection-factor explanations.
- `_selection_factors_from_pressures(...)` prepares that payload from pressure availability.
- `_SelectionLineagePayload` now carries the named factor payload instead of a raw `list[str]`.
- `_selection_path_from_payloads(...)` performs the unchanged public handoff by assigning `lineage.factors.selection_factors` to `SelectionPathAudit.selection_factors`.
- `test_selection_factor_payload_is_separate_from_candidate_set_and_unknowns` proves the payload is separate from candidate-set, non-selected, and unknown ownership while preserving both populated and empty-pressure factor values.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

Producer: `_selection_factors_from_pressures(...)`, called by `_from_pressure_selection(...)` when constructing pressure-backed selection lineage.

The unsupported-target branch also now hands an explicit `_SelectionFactorPayload(selection_factors=["unknown"])` to lineage rather than placing a raw factor list directly in lineage construction.

## Recovered artifact/helper

Recovered artifact/helper: `_SelectionFactorPayload`.

Carrying helper: `_selection_factors_from_pressures(...)`.

The artifact carries only `selection_factors: list[str]`; it does not carry candidates, non-selected alternatives, selected value, outcome reason, supporting evidence, or typed Unknown records.

## Recovered consumer

Consumers:

- `_SelectionLineagePayload`, which carries the factor payload alongside candidate-set, non-selected, and typed Unknown lineage material;
- `_selection_path_from_payloads(...)`, which performs the compatibility handoff;
- `SelectionPathAudit.selection_factors`;
- `selection_path_audit_json(...)` through `SelectionPathAudit.to_json_dict()`;
- `format_selection_path_audit(...)`, which renders the selection-factor section;
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

Selection-factor preparation was compressed with pressure-backed selection lineage construction. `_from_pressure_selection(...)` prepared the factor list inline, the unsupported-target branch placed the `unknown` factor directly into lineage construction, and `_SelectionLineagePayload` carried those factors as a raw list beside candidate-set, non-selected, and typed Unknown material.

### 2. Which implementation-local ownership boundary became directly observable?

The selection-factor payload ownership boundary became directly observable.

### 3. What implementation and/or test change made the boundary observable?

Implementation now has `_SelectionFactorPayload` and `_selection_factors_from_pressures(...)`, and `_SelectionLineagePayload` carries that payload instead of a raw list. Tests instantiate the factor payload at lineage handoffs and assert that the factor payload is separate from candidate-set, non-selected, and unknown ownership while preserving the same public factor values.

### 4. What producer now owns the recovered responsibility?

`_selection_factors_from_pressures(...)` owns pressure-backed selection-factor payload preparation.

### 5. What artifact or helper carries the recovered boundary, if any?

`_SelectionFactorPayload` carries the recovered boundary, with `_selection_factors_from_pressures(...)` preparing the pressure-backed instance.

### 6. Who consumes it?

`_SelectionLineagePayload` and `_selection_path_from_payloads(...)` consume it internally. Public consumers continue to consume unchanged `SelectionPathAudit.selection_factors`, JSON output, human-readable output, and CLI output.

### 7. Did any compatibility boundary change?

No.

## LOC changed

Implementation/test change before this report:

- `seed_runtime/selection_path_audit.py`: 23 insertions, 14 deletions.
- `tests/test_selection_path_audit.py`: 35 insertions, 6 deletions.

## Tests executed

- `python -m pytest -q tests/test_selection_path_audit.py`
- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py`
- `python -m pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

Remaining compressed responsibilities were intentionally not recovered in this slice:

- typed Unknown production beyond the existing lineage handoff;
- unsupported-target lawful refusal beyond the existing unsupported branch;
- implemented-target admission ownership beyond existing local target matching;
- target normalization and matching ownership;
- public rendering ownership;
- selected-result compatibility handoff details beyond the existing public handoff;
- lineage assembly beyond the now-separated candidate-set, factor, non-selected, and typed Unknown materials;
- Frontier Pressure Admission;
- readiness evaluation;
- prioritization;
- investigation planning;
- scheduler or planner behavior.
