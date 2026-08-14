# Frontier Pressure Admission Slice 007

Recovered implementation-local ownership boundary: **unsupported-target refusal preparation inside `selection_path_audit`**.

## Selected boundary

The selected boundary is the handoff where `build_selection_path_audit(...)` stops inlining the refusal audit for unimplemented selection targets and delegates that refusal preparation to `_unsupported_target_selection(...)` before the unchanged public `SelectionPathAudit` compatibility handoff.

Expected compatibility answer: `No.`

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` around `_from_pressure_selection(...)`, `_SelectionLineagePayload`, `_candidate_set_from_pressures(...)`, `_non_selected_from_pressures(...)`, `_selection_factors_from_pressures(...)`, `_selection_unknowns_from_pressures(...)`, selected-result preparation, selected-reason preparation, supporting-evidence preparation, lineage assembly, and `_selection_path_from_payloads(...)`.

Evidence found:

1. Pressure-backed selection admission was already routed through `_from_pressure_selection(...)`.
2. Candidate-set, non-selected, factor, and typed-unknown production already had named local artifacts or helpers.
3. The unsupported-target branch still assembled the complete refusal audit inline in `build_selection_path_audit(...)` after supported-target matching failed.
4. That inline branch mixed target-refusal outcome, empty supporting evidence, unknown factor, pressure candidate lineage preservation, and selection-logic typed Unknown construction at the outer builder level.
5. `_selection_path_from_payloads(...)` was already the unchanged compatibility handoff into the public `SelectionPathAudit` shape, so unsupported-target refusal preparation could be separated without changing public behavior.

## Before

Unsupported-target refusal preparation was compressed into `build_selection_path_audit(...)`:

- The builder selected the unsupported-target path.
- The builder directly constructed `_SelectionResultPayload(selected="unknown")`.
- The builder directly constructed the public refusal outcome reason.
- The builder directly constructed empty support, unknown factor, empty non-selected lineage, pressure candidate lineage, and the selection-logic typed Unknown.
- The builder immediately handed those pieces to `_selection_path_from_payloads(...)`.

## After

Unsupported-target refusal preparation is directly observable:

- `build_selection_path_audit(...)` now only selects the unsupported-target path and calls `_unsupported_target_selection(target, pressure.pressures)`.
- `_unsupported_target_selection(...)` owns the unsupported-target refusal audit preparation.
- The helper preserves pressure-backed candidate visibility while producing the same unknown selected result, refusal reason, unknown factor, empty support, empty non-selected list, and selection-logic typed Unknown.
- `_selection_path_from_payloads(...)` remains the public compatibility handoff.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`
  - Added `_unsupported_target_selection(...)`.
  - Replaced the inline unsupported-target refusal construction in `build_selection_path_audit(...)` with a call to that helper.

## Test files changed

- `tests/test_selection_path_audit.py`
  - Added `test_unsupported_target_selection_refusal_is_prepared_separately` to exercise the helper directly and prove the unsupported-target refusal surface remains unchanged.

## Recovered producer

Producer: `_unsupported_target_selection(...)`.

It now owns the implementation-local preparation of unsupported-target refusal material after `build_selection_path_audit(...)` determines that no implemented selection target matched.

## Recovered artifact/helper

Helper: `_unsupported_target_selection(target, pressures)`.

The helper carries the recovered boundary. It prepares the existing refusal payloads and delegates the unchanged public construction to `_selection_path_from_payloads(...)`.

## Recovered consumer

Consumers:

- `build_selection_path_audit(...)`, which calls the helper for unsupported targets.
- `_selection_path_from_payloads(...)`, which consumes the helper-prepared payloads and creates the public `SelectionPathAudit`.
- Public consumers continue to read unchanged `SelectionPathAudit` fields, JSON output, human-readable output, and CLI output.

## Compatibility preserved

No compatibility boundary changed.

The public `SelectionPathAudit` dataclass fields, JSON keys, human-readable sections, CLI behavior, diagnostic inventory registration, diagnostic shape-audit behavior, event-ledger behavior, and read-only mutation boundary remain unchanged.

## LOC changed

From `git diff --cached --stat` before commit:

```text
frontier_pressure_admission_slice_007.md | 132 +++++++++++++++++++++++++++++++
seed_runtime/selection_path_audit.py     |   8 +-
tests/test_selection_path_audit.py       |  41 ++++++++++
3 files changed, 180 insertions(+), 1 deletion(-)
```

## Tests executed

- `python -m pytest -q tests/test_selection_path_audit.py`
- `python -m pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Required questions

### 1. What responsibilities were previously compressed?

Unsupported-target selection-path refusal preparation was compressed with the outer selection target dispatcher in `build_selection_path_audit(...)`. The compressed responsibilities were unsupported-target result selection, refusal reason preparation, empty support preparation, unknown factor preparation, empty non-selected preparation, pressure candidate lineage preservation, selection-logic typed Unknown preparation, and public compatibility handoff.

### 2. Which implementation-local ownership boundary became directly observable?

The unsupported-target refusal preparation boundary became directly observable.

### 3. What implementation and/or test change made the boundary observable?

Implementation now routes unsupported targets through `_unsupported_target_selection(...)`. The new test `test_unsupported_target_selection_refusal_is_prepared_separately` calls that helper directly and asserts the unchanged refusal audit payload.

### 4. What producer now owns the recovered responsibility?

`_unsupported_target_selection(...)` owns unsupported-target refusal preparation.

### 5. What artifact or helper carries the recovered boundary, if any?

`_unsupported_target_selection(...)` carries the recovered boundary.

### 6. Who consumes it?

`build_selection_path_audit(...)` consumes the helper for unsupported targets, and `_selection_path_from_payloads(...)` consumes the helper-prepared payloads to produce the unchanged public audit.

### 7. Did any compatibility boundary change?

No.

## Remaining compressed responsibilities

Adjacent responsibilities that remain intentionally unchanged:

- Lineage assembly is still centralized in `_SelectionLineagePayload` construction.
- Public audit handoff remains centralized in `_selection_path_from_payloads(...)`.
- Pressure-backed target admission remains in `build_selection_path_audit(...)` and `_from_pressure_selection(...)`.
- Diagnostic read-only rendering handoff remains unchanged in `format_selection_path_audit(...)` and the CLI path.
