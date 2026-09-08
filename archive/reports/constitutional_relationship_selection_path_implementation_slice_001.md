# Constitutional Relationship Selection Path Implementation Slice 001

## Selected boundary

Selection-target resolution is now an implementation-local ownership boundary. The recovered boundary decides whether a normalized Selection Path target is handled as:

- `focus`
- `pressure_category`
- `unsupported`

This slice recovers only that responsibility. It does not redesign Selection Path, add a framework, add a registry, introduce an engine, or change public behavior.

## Implementation evidence

Repository implementation evidence selected this boundary:

- `build_selection_path_audit(...)` already normalized the target, collected `_SelectionPathInputs`, and directly owned all target-dispatch decisions.
- Existing adjacent helpers already exposed separate evidence for focus target matching and pressure-category target matching.
- Existing target-specific producers already consumed the result of target dispatch:
  - `_from_focus_selection(...)`
  - `_from_pressure_category_selection(...)`
  - `_unsupported_target_selection(...)`

The directly observable compressed responsibility was therefore the local decision that classifies a target before those target-specific producers run.

## Before

`build_selection_path_audit(...)` compressed these responsibilities together:

1. repository-root preparation;
2. target normalization;
3. input gathering;
4. implemented target resolution;
5. focus selection production;
6. pressure-category selection production;
7. unsupported-target production;
8. public compatibility handoff through the existing audit shape.

## After

`build_selection_path_audit(...)` still prepares the root, normalizes the target, gathers inputs, and returns the same public `SelectionPathAudit` shape.

The target-resolution responsibility is now owned by `_selection_target_selection(...)`, which returns `_SelectionTargetSelection` with the original target, normalized target, and local `selection_kind`.

## Recovered producer

`_selection_target_selection(...)` now owns the recovered implementation-local responsibility: classifying the normalized target against implemented Selection Path target evidence.

## Recovered artifact/helper

`_SelectionTargetSelection` carries the recovered boundary. It intentionally carries only target-resolution material:

- `target`
- `normalized_target`
- `selection_kind`

It does not carry pressure inputs, focus inputs, selected result material, outcome material, evidence material, Unknowns, or public audit fields.

## Recovered consumer

`build_selection_path_audit(...)` consumes `_SelectionTargetSelection` and delegates to the already-existing target-specific producers without changing their public output:

- `focus` -> `_from_focus_selection(...)`
- `pressure_category` -> `_from_pressure_category_selection(...)`
- `unsupported` -> `_unsupported_target_selection(...)`

## Compatibility preserved

No compatibility boundary changed.

Preserved boundaries:

- public CLI behavior;
- JSON output shape;
- text rendering;
- `SelectionPathAudit` compatibility shape;
- existing payload artifacts;
- existing helper artifacts;
- read-only behavior;
- typed Unknown behavior;
- lineage behavior;
- candidate behavior;
- evidence behavior;
- no fact recording;
- no event-ledger writes;
- no cluster mutation.

## Files changed

- `seed_runtime/selection_path_audit.py`
- `tests/test_selection_path_audit.py`
- `constitutional_relationship_selection_path_implementation_slice_001.md`

## LOC changed

Implementation and test diff before this report:

- `seed_runtime/selection_path_audit.py`: 50 changed lines in diff context, including 92 total insertions and 5 deletions across implementation and tests.
- `tests/test_selection_path_audit.py`: 47 changed lines in diff context.

Including this report, the final repository diff also adds this markdown deliverable.

## Tests executed

- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 156 tests.
- `git diff --check` — passed.

## Required questions

1. **What responsibilities were previously compressed?** Target normalization, implemented-target resolution, target-specific selection producer dispatch, unsupported-target dispatch, and final public audit production were compressed inside `build_selection_path_audit(...)`.
2. **Which implementation-local ownership boundary became directly observable?** Implemented Selection Path target resolution became directly observable as a local boundary between gathered inputs and target-specific producers.
3. **What producer now owns the recovered responsibility?** `_selection_target_selection(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** `_SelectionTargetSelection` carries the target, normalized target, and `selection_kind`.
5. **Who consumes it?** `build_selection_path_audit(...)` consumes it and dispatches to the existing target-specific producers.
6. **Did any compatibility boundary change?** No.

## Remaining compressed responsibilities

The following responsibilities remain intentionally compressed or only partially separated for future repository-evidence-driven recovery slices:

- public audit construction and compatibility handoff;
- focus selected-name production versus pressure-category selected-name production;
- pressure-selection payload bundle composition;
- unsupported-target payload bundle composition;
- candidate, factor, non-selected, evidence, lineage, and Unknown material integration into the final compatibility artifact.
