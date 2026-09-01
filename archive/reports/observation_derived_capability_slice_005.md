# Observation-Derived Capability Slice 005

## Selected architectural boundary

`Capability Inventory != Executable Operation Contract`.

This slice makes the final capability-admission transition directly observable inside the implementation: admitted repository capability knowledge is now collected separately from executable operation contract metadata before the unchanged capability inventory universe is presented.

## Implementation evidence

- `CapabilityInventoryEntry` remains the public read-only presentation model for capability inventory.
- `_admitted_capability_state()` continues to consume projected `capability_verified` facts as admitted repository capability knowledge.
- `_registered_operation_contract_capabilities()` continues to derive capability labels from registered `ToolSpec` records.
- New `_ExecutableOperationContractState` makes the executable contract side explicit without changing `ToolSpec`, `ToolRegistry`, registration semantics, schemas, JSON, CLI output, events, or ledger behavior.
- New `_CapabilityInventorySources` performs the implementation-local handoff from separated sources into the same inventory capability universe.
- `build_capability_inventory()` still sorts and presents the same union of registered operation capability labels, requested capabilities, and admitted capability subjects.

## Before

`_inventory_capabilities()` directly accumulated all inventory names in one function body:

1. registered executable operation contract capability labels;
2. requested capabilities from `ToolNeed`s;
3. admitted capability subjects from projected verification facts.

That meant inventory presentation and executable operation contract derivation were behaviorally correct but architecturally compressed at the inventory-universe construction point.

## After

`_inventory_capabilities()` delegates to `_capability_inventory_sources(state).capability_universe()`.

The source object keeps these responsibilities visible as separate implementation-local inputs:

- `admitted_capabilities`: repository capability knowledge admitted through projected `capability_verified` facts;
- `executable_operation_contracts`: operational affordance metadata derivable from registered `ToolSpec` records;
- `requested_capabilities`: unresolved capability needs.

The final union remains unchanged and deterministic.

## Boundary made explicit

The recovered boundary is now explicit at the implementation handoff:

```text
admitted repository capability knowledge
    !=
executable operation contract metadata
```

and the unchanged compatibility union remains:

```text
separated inventory sources
    -> capability inventory presentation universe
```

## Compatibility preserved

No compatibility boundary changed.

The slice intentionally avoided public renames, schema changes, manifest changes, event changes, CLI changes, JSON changes, ledger changes, operation registration changes, inventory behavior changes, contract behavior changes, executable behavior changes, and inventory ordering changes.

## Files changed

- `seed_runtime/capability_inventory.py`
- `tests/test_capability_inventory.py`
- `observation_derived_capability_slice_005.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/capability_inventory.py | 66 +++++++++++++++++++++++++++++++++---
tests/test_capability_inventory.py   | 31 +++++++++++++++--
2 files changed, 90 insertions(+), 7 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_capability_inventory.py
pytest -q tests/test_capability_verification_inspection.py tests/test_registry.py
```

Results:

```text
9 passed
20 passed
```

A mistyped exploratory command was also run before locating the correct verification inspection test file:

```text
pytest -q tests/test_capability_verification.py tests/test_registry.py
```

Result:

```text
ERROR: file or directory not found: tests/test_capability_verification.py
```

## Remaining compressed observation-derived capability boundaries

- Capability inventory still intentionally presents a compatibility union of registered operation contract labels, requested capabilities, and admitted verification fact subjects.
- Registered operation contract derivation remains represented by `ToolSpec` capability metadata in projected state; this slice only made the inventory handoff explicit and did not introduce a public contract-derivation API.
- Operation selection prerequisites remain outside this slice; selection and execution compatibility were intentionally unchanged.
