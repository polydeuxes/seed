# Frontier Pressure Admission Slice 028

Recovered implementation-local ownership boundary: **unsupported-target lineage payload preparation inside `selection_path_audit`**.

## Selected boundary

The selected boundary is the unsupported-target branch's local lineage payload preparation: the step that groups preserved pressure candidates, unsupported-target selection factors, unsupported-target non-selected payload, and unsupported-target typed unknowns into `_SelectionLineagePayload` before the unchanged public `SelectionPathAudit` compatibility handoff.

This boundary was selected from current implementation evidence in `seed_runtime/selection_path_audit.py`, beginning at `build_selection_path_audit(...)`, `_unsupported_target_selection(...)`, and the adjacent helpers recovered in previous slices. The unsupported-target branch already had named producers for result, reason, supporting evidence, factor payload, non-selected payload, typed-unknown payload, and generic pressure candidate-set preparation. No narrower inline unsupported-target payload construction remained inside the branch. The still-compressed responsibility was the branch-local assembly of those already-separated lineage pieces into the lineage payload consumed by the compatibility handoff.

## Implementation evidence

Before this slice, `_unsupported_target_selection(...)` still constructed `_SelectionLineagePayload(...)` inline while also owning unsupported-target audit assembly and the public compatibility handoff. The inline lineage construction called:

- `_candidate_set_from_pressures(pressures)`;
- `_unsupported_target_factor_payload()`;
- `_unsupported_target_non_selected_payload()`;
- `_unsupported_target_unknown_payload()`.

Those producers were already separated, so recovering a narrower individual payload would have re-sliced existing ownership. The implementation evidence therefore supported exactly one adjacent boundary: unsupported-target lineage payload preparation.

## Before

`_unsupported_target_selection(...)` directly grouped candidate-set, factor, non-selected, and unknown payloads into `_SelectionLineagePayload(...)` at the same site that prepared result, reason, support, and public audit compatibility output.

## After

`_unsupported_target_selection(...)` now delegates lineage payload assembly to `_unsupported_target_lineage_payload(pressures)` and passes the returned `_SelectionLineagePayload` to the existing `_selection_path_from_payloads(...)` compatibility handoff.

`_unsupported_target_lineage_payload(...)` owns only the implementation-local assembly of unsupported-target lineage payload pieces. It does not select targets, accept pressure, mutate state, write the event ledger, record facts, plan, prioritize, generate inquiries, or alter runtime/CLI/JSON/human output.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`
  - Added `_unsupported_target_lineage_payload(...)`.
  - Replaced inline `_SelectionLineagePayload(...)` construction in `_unsupported_target_selection(...)` with a call to the new helper.

## Test files changed

- `tests/test_selection_path_audit.py`
  - Added `test_unsupported_target_lineage_payload_is_owned_by_local_helper` to directly exercise the recovered helper and prove it carries candidate-set, unsupported factor, empty non-selected, and unsupported typed-unknown payloads without owning selected result, outcome, or evidence fields.

## Recovered producer

`_unsupported_target_lineage_payload(pressures)`.

## Recovered artifact/helper

- Helper: `_unsupported_target_lineage_payload(...)`.
- Artifact: `_SelectionLineagePayload` carrying `_SelectionCandidateSetPayload`, `_SelectionFactorPayload`, `_SelectionNonSelectedPayload`, and `_SelectionUnknownPayload`.

## Recovered consumer

`_unsupported_target_selection(...)` consumes `_unsupported_target_lineage_payload(...)` and passes the returned `_SelectionLineagePayload` to `_selection_path_from_payloads(...)`.

## Compatibility preserved

No compatibility boundary changed.

Expected compatibility answer:

```text
No.
```

The public `SelectionPathAudit` dataclass, JSON keys, human-readable formatter, CLI behavior, diagnostics, schema, event-ledger behavior, and read-only mutation boundary remain unchanged. The helper only names an existing implementation-local assembly step.

## LOC changed

```text
seed_runtime/selection_path_audit.py | 18 ++++++++++++------
tests/test_selection_path_audit.py   | 32 ++++++++++++++++++++++++++++++++
2 files changed, 44 insertions(+), 6 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 141 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   Unsupported-target audit assembly and unsupported-target lineage payload preparation were compressed inside `_unsupported_target_selection(...)`. The function prepared result, reason, support, lineage grouping, and compatibility handoff while the lineage grouping still assembled candidate-set, unsupported factor, unsupported non-selected, and unsupported typed-unknown payloads inline.

2. **Which implementation-local ownership boundary became directly observable?**

   Unsupported-target lineage payload preparation became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   `_unsupported_target_selection(...)` now calls `_unsupported_target_lineage_payload(pressures)`, and `tests/test_selection_path_audit.py` directly exercises that helper in `test_unsupported_target_lineage_payload_is_owned_by_local_helper`.

4. **What producer now owns the recovered responsibility?**

   `_unsupported_target_lineage_payload(...)` owns the recovered responsibility.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_unsupported_target_lineage_payload(...)` carries the helper boundary and returns `_SelectionLineagePayload`.

6. **Who consumes it?**

   `_unsupported_target_selection(...)` consumes it and passes the returned lineage payload to `_selection_path_from_payloads(...)`.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

The immediate unsupported-target lineage grouping is now separated after its narrower payload pieces had already been separated. Remaining candidates should continue to be selected only from current implementation evidence. Broader route dispatch in `build_selection_path_audit(...)`, public compatibility construction in `_selection_path_from_payloads(...)` / `_selection_path_from_payload_bundle(...)`, formatting helpers, target normalization, and generic candidate row rendering remain unchanged and should not be sliced unless future implementation evidence exposes a concrete still-compressed ownership boundary. This slice does not introduce acceptance, action, mutation, execution, planning, prioritization, inquiry generation, route authority, readiness evaluation, event-ledger writes, or cluster mutation.
