# Constitutional Capability Projection Implementation 001

Repository authority wins.

## Orientation verification

Verified prior implementation evidence before code changes:

- `constitutional_pipeline_implementation_scout_001.md`
- `bounded_constitutional_question_implementation_001.md`
- `constitutional_question_projection_implementation_001.md`
- `constitutional_capability_projection_characterization.md`

Verified current code contains:

- `BoundedConstitutionalQuestion`
- `produce_bounded_constitutional_question(...)`
- `project_constitutional_question(...)`
- `ConstitutionalQuestionProjection`
- `ConstitutionalCapabilityProjection`
- `select_constitutional_views(...)`

Verified implemented path remains:

```text
Operator Inquiry
        ↓
BoundedConstitutionalQuestion
        ↓
ConstitutionalQuestionProjection
```

Verified the missing seam was:

```text
ConstitutionalReadModelContract
+
ReadModelViewRegistration
+
Immutable Constitutional Views
        ↓
ConstitutionalCapabilityProjection
```

No newer repository evidence contradicted this orientation.

## Implementation evidence inspected

Implementation evidence inspected directly:

- `seed_runtime/constitutional_view_selection.py`
- `seed_runtime/read_model_ownership.py`
- `seed_runtime/constitutional_process_view.py`
- `seed_runtime/constitutional_governance_view.py`
- `seed_runtime/constitutional_fidelity_view.py`
- `tests/test_constitutional_view_selection.py`
- `tests/test_constitutional_question_projection.py`
- `tests/test_constitutional_view_composition.py`
- `tests/test_bounded_constitutional_question.py`
- `constitutional_pipeline_implementation_scout_001.md`
- `bounded_constitutional_question_implementation_001.md`
- `constitutional_question_projection_implementation_001.md`
- `constitutional_capability_projection_characterization.md`
- `constitutional_view_capability_characterization.md`

## Existing capability projection contract

The existing projection schema remains `ConstitutionalCapabilityProjection`:

- `registered_view_name: str`
- `capability_keys: tuple[str, ...]`
- `compatibility_answer: str = "No."`
- `read_only: bool = True`
- `mutates_cluster: bool = False`
- `writes_event_ledger: bool = False`

No competing projection type was introduced.

## Authoritative capability sources

The projection is regenerated from existing repository-owned sources:

1. `ConstitutionalReadModelContract` records constitutional read-model identity, operational metadata, and read-only / no-ledger / no-cluster-mutation flags.
2. `ReadModelViewRegistration` records consumable registration identity, CLI flag, builder, renderer, and read-only status.
3. Immutable constitutional views provide the existing contribution evidence and compatibility / boundary flags:
   - `ConstitutionalProcessView`
   - `ConstitutionalGovernanceView`
   - `ConstitutionalFidelityView`

## Implemented projection producer

Implemented one narrow helper:

```text
project_constitutional_capabilities(...)
```

The helper consumes constitutional read-model contracts, registrations, and immutable view builders. It returns a tuple of existing `ConstitutionalCapabilityProjection` records.

## Exact source artifacts consumed

The default source set is:

- `CONSTITUTIONAL_READ_MODEL_CONTRACTS`
- registrations produced by `constitutional_read_model_registration(contract)`
- `build_constitutional_process_view`
- `build_constitutional_governance_view`
- `build_constitutional_fidelity_view`

## Exact projected fields

For each projection:

- `registered_view_name` comes from `ReadModelViewRegistration.name`.
- `capability_keys` comes only from typed immutable view evidence.
- `compatibility_answer` comes from the immutable view's `compatibility_answer`, or `Unknown.` if no lawful view source is available.
- `read_only` combines the contract, registration, and view read-only flags.
- `writes_event_ledger` combines the contract and view ledger flags.
- `mutates_cluster` combines the contract and view mutation flags.

## Capability-key mapping

Exact capability keys are projected only from typed implementation evidence:

| Registered view | Immutable evidence required | Projected key |
| --- | --- | --- |
| `constitutional_process` | `ConstitutionalProcessView` with process `stages` | `process` |
| `constitutional_governance` | `ConstitutionalGovernanceView` with governance `relationships` | `governance` |
| `constitutional_fidelity` | `ConstitutionalFidelityView` with fidelity `classifications` | `fidelity` |

No key is inferred from prose, display names, summaries, Unknowns, refusals, operator testimony, semantic similarity, or fuzzy matching.

## Deterministic ordering

Output order follows the supplied contract tuple order. With the default sources, output order is:

1. `constitutional_process`
2. `constitutional_governance`
3. `constitutional_fidelity`

Supplying a different explicit contract order deterministically changes the output order to that supplied order.

## Duplicate handling

Duplicate registered view names are deduplicated deterministically by first occurrence in the supplied contract order.

## Unknown or insufficient-source behavior

If a contract and registration exist but no immutable view builder is supplied for that contract name, the projection preserves insufficiency as:

- `capability_keys=()`
- `compatibility_answer="Unknown."`

It does not guess a key from the contract name, registration name, CLI flag, or display vocabulary.

An empty projection tuple is lawful when the supplied contract tuple is empty.

## Authority boundary

Capability Projection observes existing capability structure. It does not:

- invent capabilities;
- register views;
- modify contracts;
- create constitutional knowledge;
- create constitutional authority;
- repair missing registration;
- consume operator testimony as capability evidence.

## Read-only behavior

Projection is regenerated in memory from immutable inputs and builder outputs. It writes nothing back to source contracts, registrations, or views.

## Event-ledger behavior

Projection does not write the event ledger. Projected `writes_event_ledger` remains `False` for the default constitutional sources.

## Cluster mutation behavior

Projection does not mutate cluster state. Projected `mutates_cluster` remains `False` for the default constitutional sources.

## Registration/projection boundary

Registration remains owned by `ConstitutionalReadModelContract`, `ReadModelViewRegistration`, and `constitutional_read_model_registration(...)`. Projection consumes registration metadata only after it exists. It does not register, repair, or publish registration.

## Projection/Selection boundary

Projection does not perform Selection. Selection remains owned by `select_constitutional_views(...)`, which consumes `ConstitutionalQuestionProjection` and `ConstitutionalCapabilityProjection` records by exact-key comparison only.

## Compatibility preservation

Preserved:

- existing `ConstitutionalCapabilityProjection` schema;
- existing manually constructed projection fixtures;
- exact-key Selection behavior;
- Question Projection behavior;
- Composition behavior;
- CLI behavior;
- diagnostic inventory and diagnostic-shape behavior;
- event-ledger behavior;
- cluster mutation behavior;
- read-model contracts and registrations.

## Files changed

- `seed_runtime/constitutional_view_selection.py`
- `tests/test_constitutional_capability_projection.py`
- `constitutional_capability_projection_implementation_001.md`

## Tests added or changed

Added focused capability projection tests in `tests/test_constitutional_capability_projection.py` covering:

- real source consumption;
- equivalent source determinism;
- exact key preservation;
- deterministic duplicate handling;
- deterministic ordering;
- no display-name inference;
- missing evidence insufficiency;
- no source mutation;
- no Question Projection / Selection / Composition artifact production by the producer;
- read-only / no-ledger / no-cluster-mutation propagation;
- manual fixture compatibility;
- real Capability Projection paired with real Question Projection and consumed by existing Selection.

## Tests executed

```text
pytest -q tests/test_constitutional_capability_projection.py
pytest -q tests/test_constitutional_capability_projection.py tests/test_bounded_constitutional_question.py tests/test_constitutional_question_projection.py tests/test_constitutional_view_selection.py tests/test_constitutional_view_composition.py
```

## LOC delta

Pre-commit working-tree delta before this report and tests were added was `+114 / -0` for implementation. Final committed delta is recorded in git.

## Remaining next pressure

End-to-end constitutional pipeline invocation.

## Commit hash

To be filled after commit: `TBD`.

## Explicit answers

Did this task recover new architecture?

No.

Does CapabilityProjection invent or register capabilities?

No.

Does CapabilityProjection consume operator testimony as capability evidence?

No.

Does CapabilityProjection perform Selection?

No.

Does CapabilityProjection write the event ledger or mutate cluster state?

No.
