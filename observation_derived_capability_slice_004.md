# Observation-Derived Capability Slice 004

## selected architectural boundary

Capability Promotion != Capability Inventory.

This slice makes the implementation-local handoff from admitted capability knowledge to capability inventory presentation directly observable, without changing public vocabulary, payloads, schemas, events, CLI behavior, ordering, promotion rules, or inventory semantics.

## implementation evidence

- `CapabilityPromotionReadinessInspection` is read-only and explicitly says it does not create `capability_verified` facts, select capabilities, evaluate policy, invoke tools, plan, or execute.
- `build_capability_inventory()` constructs inventory entries from projected `State` only and derives verification state from existing `capability_verified` facts and `FactSupport` records.
- Before this slice, `_inventory_capabilities()` directly merged registered operation-contract capabilities, requested capabilities, and observed verification fact subjects in one inventory construction function.
- The transition from promotion/admission to inventory presentation is the existing projected `capability_verified` fact boundary. Promotion/admission is represented as current projected knowledge; inventory presentation consumes that knowledge.

## before

`_inventory_capabilities()` directly accumulated every inventory source, including capability subjects from projected `capability_verified` facts:

```python
def _inventory_capabilities(state: State) -> set[str]:
    capabilities: set[str] = set()
    capabilities.update(_registered_operation_contract_capabilities(state))
    capabilities.update(_requested_capabilities(state))
    capabilities.update(_observed_verification_capability_subjects(state))
    return capabilities
```

That kept behavior correct, but the inventory construction function also owned the handoff from admitted capability knowledge into presentation.

## after

A private implementation-local `_AdmittedCapabilityState` now represents capability names admitted into projected knowledge before inventory presentation. `_inventory_capabilities()` still owns the compatibility-preserving inventory universe union, but it consumes admitted capability state instead of directly reaching through to verification fact subjects.

```python
@dataclass(frozen=True)
class _AdmittedCapabilityState:
    """Capability names admitted into projected knowledge before inventory presentation."""

    capabilities: set[str] = field(default_factory=set)
```

```python
def _inventory_capabilities(state: State) -> set[str]:
    capabilities: set[str] = set()
    capabilities.update(_registered_operation_contract_capabilities(state))
    capabilities.update(_requested_capabilities(state))
    capabilities.update(_admitted_capability_state(state).capabilities)
    return capabilities
```

```python
def _admitted_capability_state(state: State) -> _AdmittedCapabilityState:
    """Return capability knowledge admitted by projected promotion facts."""

    return _AdmittedCapabilityState(
        capabilities=_observed_verification_capability_subjects(state)
    )
```

## boundary made explicit

The recovered boundary is:

```text
Capability Promotion
    !=
Capability Inventory
```

Promotion/admission remains represented by existing projected `capability_verified` facts. Capability inventory remains a read-only presentation of current repository capability state. The new private helper makes that handoff explicit inside implementation while preserving the existing inventory output.

## compatibility preserved

No.

No compatibility boundary changed. This slice did not change CLI behavior, JSON output, public dataclasses, schemas, events, ledger writes, promotion semantics, inventory semantics, capability visibility, ordering, record behavior, or execution behavior.

## files changed

- `seed_runtime/capability_inventory.py`
- `observation_derived_capability_slice_004.md`

## LOC changed

Implementation LOC changed: `seed_runtime/capability_inventory.py` changed by 27 insertions and 1 deletion.

## tests executed

```text
pytest -q tests/test_capability_inventory.py tests/test_capability_promotion_readiness.py
```

Result:

```text
19 passed in 4.78s
```

## remaining compressed observation-derived capability boundaries

- Capability verification fact creation vs. promotion/admission remains represented by existing facts and read-only readiness inspection, but there is still no separate promotion writer in this slice.
- Capability inventory construction vs. inventory consumers remains distributed across inventory builders, integrity summary, verification inspection, and CLI formatters.
- Capability presentation vs. selection/routing remains mostly preserved by read-only inventory behavior, but inventory consumers still compose that state in separate modules.
- Provider-reported capability state vs. independently verified capability state remains encoded as inventory state values derived from fact values, not as a separate lifecycle abstraction.
