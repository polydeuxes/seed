# Bounded Constitutional Question Implementation 001

Repository authority wins.

## Orientation verification

Verified `constitutional_pipeline_implementation_scout_001.md` is present and concludes:

```text
Current pressure classification:
Implementation Realization — deterministic `BoundedConstitutionalQuestion` producer.

Lawful Architectural Stopping:
Still applies. Remain in implementation mode.

Recoverable ownership candidates:
None.

Recommended exact target:
Implement the deterministic `BoundedConstitutionalQuestion` producer as an immutable provenance-preserving, read-only, non-mutating artifact/helper from explicit operator-inquiry inputs.
```

Selection and Composition remain implemented:

- `seed_runtime/constitutional_view_selection.py` still defines `ConstitutionalQuestionProjection`, `ConstitutionalCapabilityProjection`, `SelectedConstitutionalViews`, and `select_constitutional_views(...)`.
- `seed_runtime/constitutional_view_composition.py` still defines `ConstitutionalViewCompositionRequest`, `ConstitutionalViewCompositionArtifact`, and `build_constitutional_view_composition(...)`.

No newer repository evidence inspected during this implementation contradicted the scout conclusion. The work remained implementation realization, not architecture recovery.

## Implementation evidence inspected

Implementation evidence inspected before and during the change:

- `constitutional_pipeline_implementation_scout_001.md`
- `seed_runtime/constitutional_view_selection.py`
- `seed_runtime/constitutional_view_composition.py`
- `seed_runtime/serialization.py`
- `tests/test_constitutional_view_selection.py`
- `tests/test_constitutional_view_composition.py`

## Implemented artifact

Implemented immutable dataclass:

```text
seed_runtime.bounded_constitutional_question.BoundedConstitutionalQuestion
```

The artifact owns only the Operator Inquiry -> BoundedConstitutionalQuestion production boundary.

## Implemented producer

Implemented deterministic helper:

```text
seed_runtime.bounded_constitutional_question.produce_bounded_constitutional_question(...)
```

Implemented JSON-ready helper:

```text
seed_runtime.bounded_constitutional_question.bounded_constitutional_question_json(...)
```

## Exact producer inputs

The producer accepts only explicit caller inputs:

- `operator_inquiry: str`
- `inquiry_provenance: str`
- `bounded_question: str`
- `constitutional_intent: str`
- `scope_status: str`
- `uncertainty: Iterable[str] = ()`
- `unknowns: Iterable[str] = ()`
- `bounded_question_id: str | None = None`
- `caller_supplied_fields: dict[str, Any] | None = None`

## Exact produced fields

The produced artifact contains:

- `bounded_question_id`
- `operator_inquiry`
- `inquiry_provenance`
- `bounded_question`
- `constitutional_intent`
- `scope_status`
- `uncertainty`
- `unknowns`
- `caller_supplied_fields`
- `testimony_status`
- `read_only_boundaries`
- `read_only`
- `writes_event_ledger`
- `mutates_cluster`

## Deterministic identity behavior

If `bounded_question_id` is supplied, the producer preserves it exactly.

If `bounded_question_id` is not supplied, the producer derives a stable identifier by SHA-256 hashing canonical JSON built only from explicit producer inputs other than the identifier. The generated identifier is prefixed with:

```text
bounded-constitutional-question:
```

No time, randomness, event-ledger state, cluster state, external service, model inference, view-registration state, or mutable global state participates in identity generation.

## Provenance preservation

The producer preserves `operator_inquiry` exactly as received and preserves `inquiry_provenance` exactly as supplied by the caller.

## Testimony / evidence / fact distinction

The artifact marks operator testimony as evidence, not established fact:

```text
operator testimony preserved as evidence, not established fact
```

The artifact and tests avoid fields that would represent the inquiry as established fact, verified claim, constitutional authority, repository truth, durable knowledge, authoritative capability, selected constitutional view, or lawful action.

## Immutability

`BoundedConstitutionalQuestion` is a frozen dataclass.

Caller-owned mutable input collections are copied into immutable tuples before artifact construction.

## Read-only behavior

The artifact sets:

```text
read_only=True
```

Read-only boundaries explicitly include no natural-language classification, no fact promotion, no authority creation, no capability creation, no view selection, and no QuestionProjection production.

## Event-ledger behavior

The artifact sets:

```text
writes_event_ledger=False
```

The producer does not write the event ledger.

## Cluster mutation behavior

The artifact sets:

```text
mutates_cluster=False
```

The producer does not mutate cluster state.

## Producer / projection boundary

The producer does not perform `QuestionProjection`.

It does not emit selection keys, capability projections, selected views, composition requests, or explanations. Deterministic QuestionProjection remains the next implementation pressure.

## Compatibility preservation

No Selection inputs or outputs were changed.

No Composition inputs or outputs were changed.

No CLI behavior was changed.

No diagnostic inventory or diagnostic-shape registration was changed.

No event-ledger or cluster mutation behavior was changed.

No synthetic projection fixtures were changed.

## Files changed

- Added `seed_runtime/bounded_constitutional_question.py`
- Added `tests/test_bounded_constitutional_question.py`
- Added `bounded_constitutional_question_implementation_001.md`

## Tests added or changed

Added focused producer tests in `tests/test_bounded_constitutional_question.py` proving:

1. The artifact is immutable.
2. Production is deterministic from explicit inputs.
3. The operator inquiry is preserved exactly.
4. Provenance/source is preserved.
5. Explicit bounded fields are preserved.
6. Uncertainty and unknowns are preserved.
7. Operator testimony is not represented as established fact.
8. No authoritative capability is created.
9. No constitutional views are selected.
10. `read_only` remains true.
11. `writes_event_ledger` remains false.
12. `mutates_cluster` remains false.
13. Production does not mutate caller-owned input collections.

Existing Selection and Composition tests were not changed.

## Tests executed

```bash
pytest -q tests/test_bounded_constitutional_question.py tests/test_constitutional_view_selection.py tests/test_constitutional_view_composition.py
```

Result:

```text
17 passed
```

## LOC delta

Committed task line delta is:

```text
+489 / -0
```

## Remaining next pressure

Deterministic QuestionProjection production.

## Commit hash

To be assigned by git at commit time. The final implementation response reports the exact commit hash.

## Required explicit answers

Did this task recover new architecture?

No.

Does the producer perform QuestionProjection?

No.

Does the producer promote operator testimony into fact?

No.

Does the producer write the event ledger or mutate cluster state?

No.
