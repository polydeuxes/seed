# Constitutional Read Model Contract Slice 001

## Scope

This is exactly one implementation ownership audit. It reviews the existing Constitutional Process View, Constitutional Governance View, `ReadModelViewRegistration`, diagnostic inventory participation, and diagnostic shape-audit participation. It does not redesign read models, diagnostics, CLI behavior, registration, JSON rendering, human rendering, or constitutional content.

## Implementation evidence

The repository already exposes two constitutional read models with the same implementation-local shape:

1. `seed_runtime/constitutional_process_view.py`
   - Producer: `build_constitutional_process_view()` returns a frozen `ConstitutionalProcessView` artifact.
   - Artifact: `ConstitutionalProcessView` preserves `name`, `compatibility_answer`, `composition`, staged content, preserved Unknowns, remaining candidate views, and read-only boundary flags.
   - JSON renderer: `constitutional_process_view_json(...)` delegates to `to_plain(...)`.
   - Human renderer: `format_constitutional_process_view(...)` renders compatibility, read-only flags, event-ledger and cluster-mutation boundaries, stages, preserved Unknowns, and remaining candidate views.
   - Boundary: `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`.

2. `seed_runtime/constitutional_governance_view.py`
   - Producer: `build_constitutional_governance_view()` returns a frozen `ConstitutionalGovernanceView` artifact.
   - Artifact: `ConstitutionalGovernanceView` preserves `name`, `compatibility_answer`, `composition`, governance relationships, preserved Unknowns, explicit refusals, remaining candidate views, and read-only boundary flags.
   - JSON renderer: `constitutional_governance_view_json(...)` delegates to `to_plain(...)`.
   - Human renderer: `format_constitutional_governance_view(...)` renders compatibility, read-only flags, event-ledger and cluster-mutation boundaries, relationships, preserved Unknowns, explicit refusals, and remaining candidate views.
   - Boundary: `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`.

Both views are registered through `ReadModelViewRegistration` in `seed_runtime/read_model_ownership.py`, participate in `DIAGNOSTIC_INVENTORY`, and have `DiagnosticImplementationSpec` entries in `seed_runtime/diagnostic_shape_audit.py`.

## Recurring implementation obligations

Repository evidence independently recovers the same obligations for both constitutional read models:

- a registration name;
- a CLI consumer flag;
- a producer function path;
- a read-model artifact returned by the producer;
- a human formatter function path;
- a JSON renderer function path;
- diagnostic inventory declaration by the same surface name;
- diagnostic shape-audit declaration by the same surface name;
- read-only behavior;
- JSON support;
- no record support;
- `record_scope="none"`;
- no event-ledger writes;
- no cluster mutation;
- preserved Unknowns in the produced artifact;
- compatibility answer preserved as:

```text id="92v8ki"
No.
```

## Selected ownership boundary

The selected immediately adjacent implementation-local boundary is:

```text
ConstitutionalReadModelContract
```

Repository evidence selects this boundary because the repeated implementation obligations are narrower than all read-model registration and broader than either individual constitutional view. The recurrence is not a new framework or view engine; it is a local contract for constitutional read models that are already independently implemented.

## Before

Before this slice, the recurring constitutional read-model obligations were compressed across:

- individual constitutional view modules;
- `READ_MODEL_VIEW_REGISTRATIONS` entries;
- diagnostic inventory entries;
- diagnostic shape-audit specs;
- tests for each individual view.

The pattern was recoverable only by comparing both implementations manually.

## After

This slice adds `ConstitutionalReadModelContract` and `CONSTITUTIONAL_READ_MODEL_CONTRACTS` in `seed_runtime/read_model_ownership.py`. The contract records the already-recurring obligations and produces the existing `ReadModelViewRegistration` entries for the two constitutional read models.

The diagnostic inventory and diagnostic shape-audit registries remain the authorities for their existing surfaces. Tests now prove the recovered contract matches those existing declarations.

## Recovered producer

`constitutional_read_model_registration(contract)` is the recovered producer. It consumes one `ConstitutionalReadModelContract` and produces the existing `ReadModelViewRegistration` artifact used by `READ_MODEL_VIEW_REGISTRATIONS`.

## Recovered artifact/helper

`ConstitutionalReadModelContract` is the recovered artifact/helper. It owns only the implementation-local contract fields shared by the existing constitutional read models:

- name;
- CLI flag;
- builder path;
- renderer path;
- JSON renderer path;
- inventory name;
- shape-audit name;
- read-only and mutation boundary declarations.

It does not own constitutional content, diagnostic registration, shape-audit implementation, CLI dispatch, rendering, JSON conversion, event-ledger behavior, cluster mutation, future view selection, or constitutional authority.

## Recovered consumer

`READ_MODEL_VIEW_REGISTRATIONS` is the recovered consumer. It now consumes `CONSTITUTIONAL_READ_MODEL_CONTRACTS` for the constitutional read-model registrations while preserving all other read-model registrations unchanged.

## Compatibility

No behavior changes are intended or accepted.

Expected compatibility answer:

```text id="92v8ki"
No.
```

Preserved behavior:

- Constitutional Process View remains implemented;
- Constitutional Governance View remains implemented;
- registration remains through `ReadModelViewRegistration`;
- CLI behavior remains unchanged;
- JSON output remains unchanged;
- human rendering remains unchanged;
- diagnostic inventory participation remains unchanged;
- diagnostic shape-audit participation remains unchanged;
- read-only boundaries remain unchanged;
- no recording is introduced;
- no event-ledger writes are introduced;
- no cluster mutation is introduced;
- no constitutional authority is created;
- no implementation authority beyond this local contract is created.

## Files changed

- `seed_runtime/read_model_ownership.py`
- `tests/test_read_model_ownership.py`
- `constitutional_read_model_contract_slice_001.md`

## LOC changed

Captured with `git diff --stat` during the slice.

## Tests executed

- `python -m black seed_runtime/read_model_ownership.py tests/test_read_model_ownership.py`
- `pytest -q tests/test_read_model_ownership.py tests/test_constitutional_process_view.py tests/test_constitutional_governance_view.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining candidate views

This slice did not implement any remaining candidate constitutional views. Remaining candidates stay as candidates only:

- Fidelity View;
- Observability Coverage View;
- Provenance Coverage View.
