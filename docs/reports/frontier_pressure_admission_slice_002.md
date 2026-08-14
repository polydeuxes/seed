# Frontier Pressure Admission Slice 002

## Selected boundary

Recovered implementation-local ownership boundary: **selected-outcome reason ownership inside `selection_path_audit`**.

The selected boundary is the handoff where `build_selection_path_audit(...)` and `_from_pressure_selection(...)` stop determining the selected value itself and separately hand the explanation for that selected value to the public `SelectionPathAudit` view through `_SelectionReasonPayload` and `_selection_path_from_payloads(...)`.

This is not constitutional frontier pressure admission. It is not readiness evaluation. It is not investigation planning, prioritization, question generation, scheduler behavior, or planner behavior. It is only the already-present local responsibility for carrying the selected outcome reason after the implementation has either matched an implemented selection surface or preserved an unsupported target as Unknown.

## Implementation evidence

The app was used to inspect implementation-adjacent behavior:

- `python scripts/seed_local.py --inquiry-artifacts --json`
- `python scripts/seed_local.py --selection-path unknown-frontier-candidate --json`
- `python scripts/seed_local.py --selection-path current_focus --json`
- `python scripts/seed_local.py --reasoning-path derivation unknown-frontier-candidate --json`
- `python scripts/seed_local.py --diagnostic-inventory --json`
- `python scripts/seed_local.py --diagnostic-shape-audit --json`

Evidence found:

1. `selection_path_audit` already separates the selected value from the selected-value explanation. `_SelectionResultPayload` carries only `selected`, while `_SelectionReasonPayload` carries only `outcome`.
2. `_selection_path_from_payloads(...)` performs the compatibility handoff by placing `result.selected` in the public `selected` field and `reason.outcome` in the public `outcome` field.
3. Supported targets produce a reason payload containing `selected`, `focus`, and a human summary such as `<selected> selected`.
4. Unsupported targets produce a reason payload containing `selected="unknown"` and `reason="target is not an implemented selection surface"`.
5. Unsupported targets also preserve typed Unknown production separately in `_SelectionLineagePayload.unknowns`, with `area="selection_logic"` and a reason that no implementation-backed selection evidence was discovered for the target.
6. Inquiry artifacts keep pressure only partially visible and do not infer inquiry pressure transformation from prose.
7. Reasoning-path diagnostics independently preserve missing derivation as Unknown, confirming that this slice is local to selection-path reason transport rather than a generalized frontier, readiness, or planning engine.
8. Diagnostic inventory and diagnostic shape audit still describe the existing `selection_path` diagnostic as read-only, non-recording, non-ledger-writing, and non-mutating.

## Before

The nearby responsibilities were compressed around the public `SelectionPathAudit` construction boundary:

- selected outcome transport;
- selected outcome reason transport;
- supporting evidence transport;
- implemented target recognition;
- unsupported target refusal;
- typed Unknown production;
- candidate lineage transport;
- public JSON and human rendering.

Slice 001 recovered selected outcome ownership. After that recovery, implementation evidence made the adjacent reason ownership boundary directly observable because the selected value and its explanation are transported by different implementation-local payloads before being recomposed into the unchanged public audit object.

## After

Exactly one additional implementation-local ownership boundary is now documented:

- `_SelectionReasonPayload` owns the selected-outcome explanation inside `selection_path_audit`.
- `_selection_path_from_payloads(...)` keeps the compatibility handoff explicit by assigning that explanation to `SelectionPathAudit.outcome` without changing public shape.
- `_SelectionReasonPayload` does not own selected value transport, supporting evidence, candidate lineage, typed Unknown records, target admission, readiness, planning, or frontier pressure admission.

No runtime behavior, diagnostic surface, schema, event-ledger behavior, CLI behavior, JSON shape, or human-readable output was changed.

## Recovered producer

Producer: `build_selection_path_audit(...)`, with the supported-target branch delegated through `_from_pressure_selection(...)`.

The producer already decides whether the target is implemented. For supported targets, `_from_pressure_selection(...)` produces `_SelectionReasonPayload(outcome={"selected": selected, "focus": focus, "summary": f"{selected} selected"})`. For unsupported targets, `build_selection_path_audit(...)` produces `_SelectionReasonPayload(outcome={"selected": "unknown", "reason": "target is not an implemented selection surface"})`.

## Recovered artifact/helper

Recovered artifact/helper: `_SelectionReasonPayload`.

Carrying helper: `_selection_path_from_payloads(...)`.

The helper is implementation-local. It transports the already-produced reason payload into the public `SelectionPathAudit.outcome` field while keeping selected result, supporting evidence, and lineage payloads separate until the compatibility handoff.

## Recovered consumer

Consumers:

- `SelectionPathAudit.outcome`;
- `selection_path_audit_json(...)` through `SelectionPathAudit.to_json_dict()`;
- `format_selection_path_audit(...)`, which renders the outcome summary or reason;
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

Selected outcome transport, selected outcome reason transport, supporting evidence transport, implemented target recognition, unsupported target refusal, typed Unknown production, candidate lineage transport, and public rendering were compressed around the public `SelectionPathAudit` construction boundary.

### 2. Which implementation-local ownership boundary became directly observable?

The selected-outcome reason ownership boundary became directly observable: `_SelectionReasonPayload` owns the public outcome explanation before `SelectionPathAudit` is composed.

### 3. What producer now owns the recovered responsibility?

`build_selection_path_audit(...)` owns production of the selected-outcome reason payload, with `_from_pressure_selection(...)` producing the supported-target reason payload for pressure-backed selections.

### 4. What artifact or helper carries the recovered boundary, if any?

`_SelectionReasonPayload` carries the selected-outcome explanation, and `_selection_path_from_payloads(...)` carries the implementation-local compatibility handoff into `SelectionPathAudit.outcome`.

### 5. Who consumes it?

`SelectionPathAudit`, `selection_path_audit_json(...)`, `format_selection_path_audit(...)`, and the CLI `--selection-path` surface consume it.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `frontier_pressure_admission_slice_002.md`

## LOC changed

- Added: 161 lines
- Removed: 0 lines

## Tests executed

- `python scripts/seed_local.py --inquiry-artifacts --json`
- `python scripts/seed_local.py --selection-path unknown-frontier-candidate --json`
- `python scripts/seed_local.py --selection-path current_focus --json`
- `python scripts/seed_local.py --reasoning-path derivation unknown-frontier-candidate --json`
- `python scripts/seed_local.py --diagnostic-inventory --json`
- `python scripts/seed_local.py --diagnostic-shape-audit --json`
- `pytest -q tests/test_selection_path_audit.py tests/test_inquiry_artifacts.py tests/test_reasoning_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

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
- typed Unknown ownership beyond observing its separate lineage transport;
- supporting evidence ownership;
- candidate lineage ownership;
- generalized lawful-refusal framework.

Unsupported conceptual pressure remains pressure.
