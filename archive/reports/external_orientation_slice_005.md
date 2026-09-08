# External Orientation Slice 005

## Selected implementation boundary

CLI Surface Intake != Operational Surface Classification.

This slice recovers the implementation-local owner that prepares bounded CLI/parser material for operational surface classification. It does not introduce generic Orientation, an orientation registry, a taxonomy, a source classifier, a planner, a scheduler, or CLI/runtime behavior changes.

## Implementation evidence

The operational surface classification entry point now delegates parser/registry intake to `_prepare_cli_surface_classification_inputs(...)`, then consumes prepared records in `build_operational_surface_classification_audit(...)`. The classification decision function `_classification_for(...)` now receives a `_CliSurfaceClassificationInput` instead of receiving raw argparse `Action` objects and flags.

Focused tests prove that the handoff artifact carries prepared parser material only and does not absorb public result/rendering ownership: it has no `classification`, `reason`, or `to_json_dict` surface, and classification consumes the prepared input directly.

## Before

`build_operational_surface_classification_audit(...)` mixed responsibilities by:

- reading registered diagnostic flags;
- iterating raw parser actions;
- selecting primary CLI flags;
- reading argparse help/action metadata;
- deriving category and registration state;
- invoking classification;
- constructing public `OperationalSurfaceClassification` result objects.

`_classification_for(...)` also reached into raw argparse `Action` objects to read help text, action type, and nargs while performing classification.

## After

`_prepare_cli_surface_classification_inputs(...)` owns CLI/parser surface intake for this classification path. It prepares the bounded input from existing parser and diagnostic inventory material.

`_classification_for(...)` owns only classification decisions over the prepared input.

`build_operational_surface_classification_audit(...)` remains the public builder that assembles the unchanged public audit result shape.

## Recovered producer

`_prepare_cli_surface_classification_inputs(...)` is the recovered producer for prepared CLI surface classification input.

## Recovered artifact/helper, if any

`_CliSurfaceClassificationInput` is the private implementation-local handoff artifact. It carries:

- selected primary flag;
- all long flags for registration matching;
- argparse help text;
- argparse action type name;
- argparse nargs value;
- prepared registration status;
- prepared operational category.

It intentionally does not carry public rendering, JSON serialization, final classification, or classification reason.

## Consumer

`build_operational_surface_classification_audit(...)` consumes `_CliSurfaceClassificationInput` records and passes each record to `_classification_for(...)`.

## Compatibility preserved

No.

No compatibility boundary changed. Public CLI flags, JSON shapes, schema, event ledger behavior, diagnostics behavior, inquiry orientation behavior, source navigation behavior, bounded ask behavior, pressure audit behavior, and runtime behavior were preserved.

## Required questions

### 1. Where were CLI Surface Intake and Operational Surface Classification previously mixed?

They were mixed in `build_operational_surface_classification_audit(...)`, which iterated raw parser actions, computed registration/category metadata, classified each option, and constructed public audit items in one loop. They were also mixed in `_classification_for(...)`, which read raw argparse action fields while deciding classifications.

### 2. Which implementation-local boundary became directly observable?

The boundary between preparing existing CLI/parser surface material and performing operational surface classification became directly observable.

### 3. What private artifact or helper now carries the handoff, if any?

`_CliSurfaceClassificationInput` carries the handoff, produced by `_prepare_cli_surface_classification_inputs(...)`.

### 4. Who consumes that artifact/helper?

`build_operational_surface_classification_audit(...)` consumes the prepared records and passes them to `_classification_for(...)`.

### 5. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/operational_surface_inventory.py`
- `tests/test_operational_surface_inventory.py`
- `external_orientation_slice_005.md`

## LOC changed

Final repository diff: 207 insertions, 17 deletions across 3 files.

## Tests executed

- `pytest -q tests/test_operational_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

Result: 64 passed.

## Remaining compressed External Orientation responsibilities

- Operational surface inventory discovery still uses raw argparse iteration for inventory construction.
- Visibility coverage still combines inventory and classification audit results in the coverage builder.
- Other committed External Orientation slices remain bounded to their implementation-local owners and are not generalized here.
