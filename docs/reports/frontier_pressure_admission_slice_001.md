# Frontier Pressure Admission Slice 001

## Selected boundary

Recovered implementation-local ownership boundary: **selection-result ownership inside `selection_path_audit`**.

The selected boundary is the handoff where `build_selection_path_audit(...)` stops collecting orientation pressure and candidate evidence, then hands exactly one selected value to the public `SelectionPathAudit` view through `_SelectionResultPayload` and `_selection_path_from_payloads(...)`.

This is not frontier pressure admission. It is not readiness evaluation. It is not prioritization. It is the already-present local responsibility for carrying the selected outcome string after the implementation has either matched an implemented selection surface or lawfully preserved `selected="unknown"`.

## Implementation evidence

The app was used to inspect the adjacent surfaces:

- `python scripts/seed_local.py --inquiry-artifacts --json`
- `python scripts/seed_local.py --selection-path unknown-frontier-candidate --json`
- `python scripts/seed_local.py --reasoning-path derivation unknown-frontier-candidate --json`
- `python scripts/seed_local.py --diagnostic-inventory --json`
- `python scripts/seed_local.py --diagnostic-shape-audit --json`

Evidence found:

1. Inquiry artifacts already distinguish pressure visibility from pressure transformation. The `pressure` artifact is only `partially_visible`, and its limitation says operational pressure visibility is implementation-backed while inquiry pressure transformation is not inferred.
2. Selection-path investigation already exposes a read-only boundary: `records_facts=false`, `writes_event_ledger=false`, and `mutates_cluster=false`.
3. When the target is not an implemented selection surface, `selection_path_audit` returns `selected="unknown"`, an outcome reason of `target is not an implemented selection surface`, and a typed Unknown for `selection_logic`.
4. Reasoning-path investigation independently preserves missing derivation as Unknown: `area="derivation"`, `reason="no derivation evidence currently available"`.
5. The implementation already separates candidate lineage, supporting evidence, reason/outcome, and the selected result with implementation-local payload helpers.

## Before

The implementation responsibility was compressed in the public selection-path behavior:

- orientation pressure came from `pressure_audit`;
- investigation candidates were rendered as `candidates`;
- admissible bounded investigation was recognized only when the target matched implemented selection surfaces;
- preserved Unknown was emitted for unsupported selection targets;
- lawful stop appeared as `selected="unknown"` plus a typed Unknown;
- already recovered work remained visible as pressure candidates from existing audit inputs;
- superseded work was not promoted by this surface;
- recommendation-like material remained limited to existing pressure-audit command fields and did not become a next action.

Those responsibilities were observable in output, but the ownership boundary for the selected result was not named in this slice artifact.

## After

Exactly one implementation-local ownership boundary is now directly observable in repository documentation:

- `_SelectionResultPayload` owns the selected outcome value inside `selection_path_audit`.
- `_selection_path_from_payloads(...)` is the handoff helper that composes the public `SelectionPathAudit` without changing its JSON shape or rendered text.
- `SelectionPathAudit`, `selection_path_audit_json(...)`, and `format_selection_path_audit(...)` consume the selected outcome after the local boundary has been crossed.

No new runtime behavior, diagnostic surface, schema, event-ledger behavior, or CLI behavior was introduced.

## Recovered producer

Producer: `build_selection_path_audit(...)`.

The producer already determines whether the requested target is an implemented selection surface. If it is not, the producer creates `_SelectionResultPayload(selected="unknown")` and pairs it with a reason, empty supporting evidence, candidate lineage, and a typed Unknown.

## Recovered artifact/helper

Recovered artifact/helper: `_SelectionResultPayload`.

Carrying helper: `_selection_path_from_payloads(...)`.

This helper is implementation-local. It does not alter public compatibility. It only preserves the existing public `SelectionPathAudit` construction boundary after local selection result ownership has been separated from reason, evidence, and lineage payloads.

## Recovered consumer

Consumers:

- `SelectionPathAudit` public dataclass;
- `selection_path_audit_json(...)`;
- `format_selection_path_audit(...)`;
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
- read-only selection-path boundary.

## Required questions

### 1. What responsibilities were previously compressed?

The compressed responsibilities were orientation pressure collection, candidate-set exposure, implemented-target admission, unknown-target refusal, selected-outcome transport, reason/outcome transport, supporting-evidence transport, candidate lineage transport, and public rendering.

### 2. Which implementation-local ownership boundary became directly observable?

The selected-outcome transport boundary became directly observable: `_SelectionResultPayload` owns only the selected result value before the public `SelectionPathAudit` is composed.

### 3. What producer now owns the recovered responsibility?

`build_selection_path_audit(...)` owns production of the selected result payload.

### 4. What artifact or helper carries the recovered boundary, if any?

`_SelectionResultPayload` carries the selected value, and `_selection_path_from_payloads(...)` carries the implementation-local handoff into the public audit object.

### 5. Who consumes it?

`SelectionPathAudit`, `selection_path_audit_json(...)`, `format_selection_path_audit(...)`, and the CLI `--selection-path` surface consume it.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `frontier_pressure_admission_slice_001.md`

## LOC changed

- Added: 151 lines
- Removed: 0 lines

## Tests executed

- `python scripts/seed_local.py --inquiry-artifacts --json`
- `python scripts/seed_local.py --selection-path unknown-frontier-candidate --json`
- `python scripts/seed_local.py --reasoning-path derivation unknown-frontier-candidate --json`
- `python scripts/seed_local.py --diagnostic-inventory --json`
- `python scripts/seed_local.py --diagnostic-shape-audit --json`
- `pytest -q tests/test_selection_path_audit.py tests/test_inquiry_artifacts.py tests/test_reasoning_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

Remaining compressed responsibilities were intentionally not recovered in this slice:

- inquiry pressure transformation;
- frontier pressure admission;
- readiness evaluation;
- prioritization;
- next-action recommendation;
- question generation;
- planner or scheduler behavior;
- supersession policy beyond existing plan lifecycle surfaces;
- generalized lawful-refusal framework.

Unsupported conceptual pressure remains pressure.
