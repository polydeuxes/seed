# Frontier Pressure Admission Slice 003

## Selected boundary

Recovered implementation-local ownership boundary: **selection supporting-evidence ownership inside `selection_path_audit`**.

The selected boundary is the handoff where supported pressure-backed selection stops choosing the selected value and explaining that value, then carries only the selected candidate's audit evidence to the public `SelectionPathAudit.evidence` view through `_SelectionSupportingEvidencePayload` and `_selection_path_from_payloads(...)`.

This is not Frontier Pressure Admission. It is not readiness evaluation. It is not investigation planning, scheduling, prioritization, question generation, or a new evidence framework. It is only the already-present local responsibility for transporting the support for an implemented pressure-backed selection after the implementation has determined that the target is an implemented selection surface.

## Implementation evidence

The app and adjacent implementation were used to inspect the next local responsibility after selected-result and selected-reason ownership:

- `python scripts/seed_local.py --selection-path current_focus --json`
- `python scripts/seed_local.py --selection-path unknown-frontier-candidate --json`
- `python scripts/seed_local.py --diagnostic-inventory --json`
- `python scripts/seed_local.py --diagnostic-shape-audit --json`

Evidence found:

1. `selection_path_audit` already separates selected value, selected-value explanation, selected supporting evidence, and lineage into separate implementation-local payloads.
2. `_SelectionSupportingEvidencePayload` carries only `evidence: list[dict[str, Any]]`.
3. `_selection_path_from_payloads(...)` performs the compatibility handoff by placing `support.evidence` in the public `SelectionPathAudit.evidence` field without altering any public field names or shapes.
4. Supported targets produce supporting evidence only from the selected pressure item: `_from_pressure_selection(...)` passes `evidence=[_evidence(selected_item)] if selected_item else []`.
5. `_evidence(...)` preserves the pressure audit support shape as `surface`, `category`, `score`, `reason`, and nested `evidence`.
6. Unsupported targets preserve empty supporting evidence while still exposing candidate lineage and typed Unknown refusal separately, which shows that supporting evidence ownership is not candidate-lineage ownership and not unknown-production ownership.
7. Diagnostic inventory and diagnostic shape audit still describe the existing `selection_path` diagnostic as read-only, non-recording, non-ledger-writing, and non-mutating.

## Before

After Slice 002, the immediately adjacent responsibilities still compressed around public `SelectionPathAudit` construction were:

- selected supporting-evidence transport;
- candidate lineage transport;
- candidate ranking/factor transport;
- non-selected candidate explanation transport;
- implemented target recognition;
- unsupported target refusal;
- typed Unknown production;
- public JSON and human rendering.

The selected result and selected-outcome reason boundaries had already been named. Implementation evidence then made selected supporting-evidence ownership directly observable because evidence is transported by its own payload and recomposed into the unchanged public audit object separately from result, reason, and lineage.

## After

Exactly one additional implementation-local ownership boundary is now documented:

- `_SelectionSupportingEvidencePayload` owns selected supporting-evidence transport inside `selection_path_audit`.
- `_from_pressure_selection(...)` produces that payload only from the selected pressure item.
- `_selection_path_from_payloads(...)` keeps the compatibility handoff explicit by assigning that payload to `SelectionPathAudit.evidence` without changing public shape.
- `_SelectionSupportingEvidencePayload` does not own selected value transport, selected reason transport, candidate lineage, ranking factors, non-selected explanations, typed Unknown records, target admission, readiness, investigation planning, or Frontier Pressure Admission.

No runtime behavior, diagnostic surface, schema, event-ledger behavior, CLI behavior, JSON shape, or human-readable output was changed.

## Recovered producer

Producer: `_from_pressure_selection(...)`.

The producer already identifies `selected_item = pressures[0] if pressures else None` and creates `_SelectionSupportingEvidencePayload(evidence=[_evidence(selected_item)] if selected_item else [])` before the public audit is composed. Unsupported-target production in `build_selection_path_audit(...)` produces `_SelectionSupportingEvidencePayload(evidence=[])`, preserving the absence of selected supporting evidence when the target is not an implemented selection surface.

## Recovered artifact/helper

Recovered artifact/helper: `_SelectionSupportingEvidencePayload`.

Carrying helpers: `_evidence(...)` and `_selection_path_from_payloads(...)`.

`_evidence(...)` shapes the selected pressure item's support record. `_SelectionSupportingEvidencePayload` carries the selected supporting-evidence list. `_selection_path_from_payloads(...)` performs the implementation-local compatibility handoff into `SelectionPathAudit.evidence`.

## Recovered consumer

Consumers:

- `SelectionPathAudit.evidence`;
- `selection_path_audit_json(...)` through `SelectionPathAudit.to_json_dict()`;
- `format_selection_path_audit(...)`, which renders the evidence section;
- the CLI path behind `seed --selection-path`.

## Compatibility preserved

No.

No compatibility boundary changed.

Preserved surfaces:

- public CLI behavior;
- JSON shape;
- human-readable output;
- diagnostics;
- schemas;
- event-ledger behavior;
- read-only selection-path boundary;
- typed Unknown public shape;
- unsupported-target refusal behavior.

## Required questions

### 1. What responsibilities were previously compressed?

Selected supporting-evidence transport, candidate lineage transport, candidate ranking/factor transport, non-selected candidate explanation transport, implemented target recognition, unsupported target refusal, typed Unknown production, and public rendering remained compressed around the public `SelectionPathAudit` construction boundary.

### 2. Which implementation-local ownership boundary became directly observable?

The selected supporting-evidence ownership boundary became directly observable: `_SelectionSupportingEvidencePayload` owns the support list that becomes `SelectionPathAudit.evidence` before the public audit is composed.

### 3. What producer now owns the recovered responsibility?

`_from_pressure_selection(...)` owns production of the selected supporting-evidence payload for implemented pressure-backed selections. `build_selection_path_audit(...)` preserves the same boundary for unsupported targets by producing an empty supporting-evidence payload.

### 4. What artifact or helper carries the recovered boundary, if any?

`_SelectionSupportingEvidencePayload` carries the selected supporting evidence, `_evidence(...)` shapes the selected pressure item evidence record, and `_selection_path_from_payloads(...)` carries the implementation-local handoff into `SelectionPathAudit.evidence`.

### 5. Who consumes it?

`SelectionPathAudit`, `selection_path_audit_json(...)`, `format_selection_path_audit(...)`, and the CLI `--selection-path` surface consume it.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `frontier_pressure_admission_slice_003.md`

## LOC changed

- Added: 158 lines
- Removed: 0 lines

## Tests executed

- `python scripts/seed_local.py --selection-path current_focus --json`
- `python scripts/seed_local.py --selection-path unknown-frontier-candidate --json`
- `python scripts/seed_local.py --diagnostic-inventory --json`
- `python scripts/seed_local.py --diagnostic-shape-audit --json`
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

Remaining compressed responsibilities were intentionally not recovered in this slice:

- inquiry pressure transformation;
- constitutional frontier pressure admission;
- readiness evaluation;
- prioritization;
- investigation planning;
- question generation;
- planner or scheduler behavior;
- implemented-target admission ownership beyond existing local target matching;
- typed Unknown ownership;
- candidate lineage ownership;
- candidate ranking/factor ownership;
- non-selected candidate explanation ownership;
- generalized lawful-refusal framework.

Unsupported conceptual pressure remains pressure.
