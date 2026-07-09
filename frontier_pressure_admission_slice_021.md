# Frontier Pressure Admission Slice 021

Recovered implementation-local ownership boundary: **unsupported-target supporting-evidence payload preparation inside `selection_path_audit`**.

## Selected boundary

The selected boundary is the local step where the unsupported-target selection path states that an unsupported selection target has no supporting evidence. Before this slice, `_unsupported_target_selection(...)` assembled the unsupported-target result, reason, empty supporting-evidence payload, candidate lineage, unknown factor, non-selected list, and typed unknown handoff in one body. Implementation evidence showed the still-compressed responsibility was the inline construction of `_SelectionSupportingEvidencePayload(evidence=[])` for unsupported targets.

## Implementation evidence

Investigation began in `seed_runtime/selection_path_audit.py` around `build_selection_path_audit(...)`, `_unsupported_target_selection(...)`, and the adjacent recent unsupported-target helpers. Current implementation showed:

1. `build_selection_path_audit(...)` routes unsupported targets to `_unsupported_target_selection(...)` after focus-selection and pressure-category checks fail.
2. `_unsupported_target_selection(...)` already consumes named producers for unsupported-target result, reason, and typed-unknown payloads.
3. The unsupported-target supporting-evidence payload remained inline as `_SelectionSupportingEvidencePayload(evidence=[])` inside `_unsupported_target_selection(...)`.
4. The inline supporting-evidence payload is a narrower responsibility than the whole unsupported-target assembly and does not own selected result, outcome reason, candidates, factors, non-selected alternatives, unknown preservation, rendering, recording, or mutation.

## Before

`_unsupported_target_selection(...)` directly constructed the unsupported-target `_SelectionSupportingEvidencePayload` inline while also coordinating unsupported-target selected result, refusal reason, candidate-set handoff, unknown factor, non-selected handoff, typed-unknown handoff, and final compatibility assembly.

## After

`_unsupported_target_selection(...)` delegates unsupported-target supporting-evidence payload construction to `_unsupported_target_supporting_evidence_payload()`. The helper returns the same empty `_SelectionSupportingEvidencePayload`, preserving public JSON output, human-readable output, CLI behavior, read-only boundary, and compatibility.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`
  - Replaced the inline unsupported-target supporting-evidence payload construction with `_unsupported_target_supporting_evidence_payload()`.
  - Added `_unsupported_target_supporting_evidence_payload()` as the local producer for the empty unsupported-target support payload.

## Test files changed

- `tests/test_selection_path_audit.py`
  - Added `test_unsupported_target_supporting_evidence_payload_is_owned_by_local_helper` to exercise the helper directly and prove it owns evidence only, not outcome, candidates, or selection factors.

## Recovered producer

`_unsupported_target_supporting_evidence_payload()` now owns unsupported-target supporting-evidence payload preparation.

## Recovered artifact/helper

The recovered helper is `_unsupported_target_supporting_evidence_payload()`, returning `_SelectionSupportingEvidencePayload(evidence=[])`.

## Recovered consumer

`_unsupported_target_selection(...)` consumes `_unsupported_target_supporting_evidence_payload()` when assembling the unchanged unsupported-target `SelectionPathAudit` compatibility object.

## Compatibility preserved

Yes. The selected value remains `unknown`, the unsupported-target outcome reason remains unchanged, the evidence list remains empty, and the read-only boundary remains unchanged.

Expected compatibility answer:

```text
No.
```

No compatibility boundary changed.

## LOC changed

```text
seed_runtime/selection_path_audit.py |  8 +++++++-
tests/test_selection_path_audit.py   | 13 +++++++++++++
2 files changed, 20 insertions(+), 1 deletion(-)
```

Numstat:

```text
7	1	seed_runtime/selection_path_audit.py
13	0	tests/test_selection_path_audit.py
```

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 134 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   Unsupported-target selection assembly and unsupported-target supporting-evidence payload construction were compressed together in `_unsupported_target_selection(...)`. The helper also still coordinates selected result, reason, candidate-set handoff, unknown factor, non-selected handoff, typed-unknown handoff, and final compatibility assembly, but this slice recovered only the narrower inline supporting-evidence payload preparation.

2. **Which implementation-local ownership boundary became directly observable?**

   Unsupported-target supporting-evidence payload preparation became directly observable as its own local producer.

3. **What implementation and/or test change made the boundary observable?**

   The inline `_SelectionSupportingEvidencePayload(evidence=[])` construction in `_unsupported_target_selection(...)` was replaced with `_unsupported_target_supporting_evidence_payload()`. `tests/test_selection_path_audit.py` now directly exercises that helper and proves it owns only the empty evidence payload fields, not outcome, candidates, or selection factors.

4. **What producer now owns the recovered responsibility?**

   `_unsupported_target_supporting_evidence_payload()`.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_unsupported_target_supporting_evidence_payload()` carries the recovered boundary and returns `_SelectionSupportingEvidencePayload(evidence=[])`.

6. **Who consumes it?**

   `_unsupported_target_selection(...)` consumes the helper while assembling the unsupported-target selection audit.

7. **Did any compatibility boundary change?**

   No. Runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, and read-only mutation boundary are preserved.

## Remaining compressed responsibilities

Remaining compression should be evaluated only from current implementation evidence. After this slice, `_unsupported_target_selection(...)` still constructs the unsupported-target lineage wrapper inline, including unknown factor and empty non-selected payloads. Those were not recovered here because this slice recovers exactly one narrower implementation-backed boundary: unsupported-target supporting-evidence payload preparation.
