# Observation-Derived Capability Slice 001

## selected architectural boundary

`Observed Evidence != Executable Operation Contract`

This slice makes one implementation-local boundary directly observable in capability inventory construction: capability names derived from observed verification facts are collected separately from capability names declared by registered executable operation contracts.

## implementation evidence

- `seed_runtime/capability_candidates.py` already preserves capability candidates from projected evidence and states that candidates are not capabilities, execution authority, execution decisions, policy evaluation, or tool invocation.
- `seed_runtime/verification_evidence.py` already acquires local binary-path evidence for candidates and states that the evidence is not capability verification, selection, execution authority, policy approval, planning, or tool invocation.
- `seed_runtime/registry.py` and `seed_runtime/models.py` define `ToolRegistry` / `ToolSpec` as the registered operation contract side: manifest-loaded operation metadata, implementation reference, policy action, visibility, status, and capability labels.
- `seed_runtime/capability_inventory.py` was the smallest confirmed compression point: `_inventory_capabilities()` built one capability universe by directly mixing capability names from registered `ToolSpec` records, requested `ToolNeed`s, and observed `capability_verified` facts.

## before

`_inventory_capabilities()` directly accumulated all capability names in one function body:

1. registered operation contract capability labels from `state.tools.values()`;
2. requested capability names from `state.tool_needs.values()`;
3. observed verification fact subjects from `state.facts.values()` where `predicate == "capability_verified"`.

That behavior was correct, but the architectural ownership boundary was implicit.

## after

`_inventory_capabilities()` remains the same compatibility-preserving union point, but its sources are separated into implementation-local helpers:

- `_registered_operation_contract_capabilities(state)` for `ToolSpec`-declared operation-contract metadata;
- `_observed_verification_capability_subjects(state)` for observation/evidence-derived verification fact subjects;
- `_requested_capabilities(state)` for requested capability needs.

The union behavior is unchanged.

## boundary made explicit

Observed verification facts are now represented by a separate implementation path from registered operation contracts:

```text
_observed_verification_capability_subjects
    !=
_registered_operation_contract_capabilities
```

This makes the recovered boundary directly visible without vocabulary migration or public rename.

## compatibility preserved

No.

No compatibility boundary changed. The slice did not change CLI behavior, JSON output, event payloads, ledger writes, schemas, manifests, capability promotion, operation registration, manifest loading, executable operation behavior, policy behavior, or capability inventory semantics.

## files changed

- `seed_runtime/capability_inventory.py`
- `observation_derived_capability_slice_001.md`

## LOC changed

`git diff --stat` reported:

```text
seed_runtime/capability_inventory.py | 39 ++++++++++++++++++++++++++++++++----
1 file changed, 35 insertions(+), 4 deletions(-)
```

This report file is additive documentation for the required deliverable.

## tests executed

```text
python -m pytest -q tests/test_capability_inventory.py
```

Result:

```text
8 passed in 1.79s
```

## remaining compressed observation-derived capability boundaries

- Capability inventory still intentionally unions registered operation contracts, requested capabilities, and observed verification subjects into one read model universe after collecting them separately.
- `CapabilityCandidate` remains package-observation oriented; binary-path verification evidence is still acquired in a separate module and not promoted.
- Capability verification state still depends on projected `capability_verified` facts; provider-reported, observed, verified, and stale states may need further responsibility slicing in future work.
- Provider recommendations in `CapabilityCatalog` remain capability metadata, not observation evidence and not executable operation contracts.
- Registered operation capability labels remain metadata on `ToolSpec`; they are still not capability proof, observed availability, or promotion authority.
