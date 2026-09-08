# External Orientation Slice 006 — Diagnostic Surface Intake != Diagnostic Inventory Composition

## Selected implementation boundary

Recovered exactly one implementation-local ownership boundary:

```text
Diagnostic Surface Intake
        !=
Diagnostic Inventory Composition
```

This slice keeps diagnostic inventory ownership local to `seed_runtime/diagnostic_inventory.py` and does not introduce generic Orientation, an orientation framework, a registry redesign, a taxonomy, or a source classifier.

## Implementation evidence

The implementation evidence is the existing diagnostic inventory path:

- `DiagnosticInventoryEntry` remains the public inventory declaration shape.
- `DIAGNOSTIC_INVENTORY` remains the existing tuple of implementation-local diagnostic declarations.
- `diagnostic_inventory_json(...)` and `format_diagnostic_inventory(...)` still expose the existing compatibility surfaces.
- A new private preparation helper converts incoming diagnostic declarations into a bounded private composition input before inventory JSON/table composition.
- Private composition consumers render JSON and human inventory output only from the prepared input.

## Before

Diagnostic declaration intake and diagnostic inventory composition were mixed in the public inventory functions:

- `diagnostic_inventory_json(...)` directly iterated over incoming entries and converted them to JSON dictionaries.
- `format_diagnostic_inventory(...)` directly iterated over incoming entries while building rendered inventory rows.

That meant the handoff from prepared diagnostic surface declarations to inventory composition existed only implicitly in the entry iteration inside the composition functions.

## After

Diagnostic surface declaration intake is now explicit and bounded:

```text
DiagnosticInventoryEntry declarations
        ↓
_prepare_diagnostic_inventory_composition(...)
        ↓
_DiagnosticInventoryCompositionInput
        ↓
_compose_diagnostic_inventory_json(...)
_compose_diagnostic_inventory(...)
```

The composition functions now consume only the prepared private input and preserve existing JSON and human rendering behavior.

## Recovered producer

`_prepare_diagnostic_inventory_composition(...)` is the recovered producer. It accepts prepared diagnostic surface declarations and returns the bounded composition input required for diagnostic inventory construction.

## Recovered artifact/helper

`_DiagnosticInventoryCompositionInput` is the private handoff artifact. It carries only:

```text
entries: tuple[DiagnosticInventoryEntry, ...]
```

No rendering state, shape-audit state, runtime behavior, ledger behavior, classification taxonomy, source classification, planner state, scheduler state, or generic orientation vocabulary is carried by this artifact.

## Consumer

The private consumers are:

- `_compose_diagnostic_inventory_json(...)`
- `_compose_diagnostic_inventory(...)`

The public compatibility functions remain wrappers:

- `diagnostic_inventory_json(...)`
- `format_diagnostic_inventory(...)`

## Required questions

### 1. Where were Diagnostic Surface Intake and Diagnostic Inventory Composition previously mixed?

They were mixed inside `diagnostic_inventory_json(...)` and `format_diagnostic_inventory(...)`, where incoming diagnostic declarations were accepted and immediately converted into JSON dictionaries or rendered inventory rows.

### 2. Which implementation-local boundary became directly observable?

The boundary between prepared diagnostic surface declaration intake and diagnostic inventory composition became directly observable.

### 3. What private artifact or helper now carries the handoff, if any?

`_DiagnosticInventoryCompositionInput` carries the private handoff, and `_prepare_diagnostic_inventory_composition(...)` produces it.

### 4. Who consumes that artifact/helper?

`_compose_diagnostic_inventory_json(...)` and `_compose_diagnostic_inventory(...)` consume `_DiagnosticInventoryCompositionInput`.

### 5. Did any compatibility boundary change?

No.

## Compatibility preserved

Compatibility is preserved:

- No public CLI flags changed.
- No diagnostic inventory JSON fields changed.
- No human inventory columns changed.
- No diagnostic shape-audit behavior changed.
- No event ledger behavior changed.
- No diagnostic recording boundary changed.
- No cluster mutation behavior changed.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `external_orientation_slice_006.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 32 ++++++++++++++++++--
tests/test_diagnostic_inventory.py   | 58 ++++++++++++++++++++++++++++++++++++
2 files changed, 87 insertions(+), 3 deletions(-)
```

Final repository diff also includes this report file.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
46 passed
```

## Remaining compressed External Orientation responsibilities

Remaining compressed responsibilities are intentionally not recovered in this slice. This slice leaves them unchanged, including:

- any generic External Orientation implementation;
- any orientation framework, registry, taxonomy, source classifier, engine, planner, or scheduler;
- diagnostic shape-audit ownership;
- public CLI, JSON, schema, event, ledger, inquiry orientation, source navigation, bounded ask, operational surface classification, pressure audit, and runtime behavior.
