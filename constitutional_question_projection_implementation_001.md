# Constitutional Question Projection Implementation 001

Repository authority wins.

## Orientation verification

Verified before implementation:

- `constitutional_pipeline_implementation_scout_001.md` is present and identified deterministic `BoundedConstitutionalQuestion` production as the prior implementation-realization pressure.
- `bounded_constitutional_question_implementation_001.md` is present and reports the implemented `Operator Inquiry -> BoundedConstitutionalQuestion` producer.
- Current code contains `BoundedConstitutionalQuestion` and `produce_bounded_constitutional_question(...)` in `seed_runtime/bounded_constitutional_question.py`.
- Current code contains `ConstitutionalQuestionProjection` and `select_constitutional_views(...)` in `seed_runtime/constitutional_view_selection.py`.
- Recent commit history has `15a0417 Implement bounded constitutional question producer (#1603)` at HEAD before this work.
- The working tree was clean before implementation.

No newer repository evidence contradicted the orientation. The missing seam was confirmed as:

```text
BoundedConstitutionalQuestion
        ↓
ConstitutionalQuestionProjection
```

## Implementation evidence inspected

Inspected:

- `seed_runtime/bounded_constitutional_question.py`
- `seed_runtime/constitutional_view_selection.py`
- `tests/test_bounded_constitutional_question.py`
- `tests/test_constitutional_view_selection.py`
- `tests/test_constitutional_view_composition.py`
- `constitutional_question_projection_characterization.md`
- `bounded_constitutional_question_slice_001.md`
- `bounded_constitutional_question_implementation_001.md`
- `constitutional_pipeline_implementation_scout_001.md`
- `constitutional_view_selection_characterization.md`
- `constitutional_view_selection_slice_002.md`

## Existing projection contract

The existing `ConstitutionalQuestionProjection` schema is preserved exactly:

- `bounded_question_id: str`
- `selection_keys: tuple[str, ...]`
- `uncertainty: tuple[str, ...] = ()`
- `read_only: bool = True`
- `mutates_cluster: bool = False`
- `writes_event_ledger: bool = False`

It remains a deterministic Selection input. It does not carry the raw operator inquiry, bounded question text, provenance record, facts, verified claims, capability projection, selected views, composition request, or constitutional authority.

## Implemented projection producer

Implemented:

```text
seed_runtime.constitutional_view_selection.project_constitutional_question(...)
```

The helper accepts exactly one `BoundedConstitutionalQuestion` and returns the existing `ConstitutionalQuestionProjection` artifact.

## Exact source fields consumed

The producer consumes these source fields from `BoundedConstitutionalQuestion`:

- `bounded_question_id`
- `uncertainty`
- `unknowns`
- `caller_supplied_fields`
- `read_only`
- `writes_event_ledger`
- `mutates_cluster`

The helper does not consume unrestricted natural language for interpretation. It does not inspect `operator_inquiry`, `bounded_question`, `constitutional_intent`, or `scope_status` to infer selection keys.

## Exact projected fields produced

The helper produces:

- `bounded_question_id` from `BoundedConstitutionalQuestion.bounded_question_id`.
- `selection_keys` from exact explicit caller-supplied fields only.
- `uncertainty` from bounded-question uncertainty plus preserved unknowns in Selection's existing uncertainty channel.
- `read_only` from `BoundedConstitutionalQuestion.read_only`.
- `writes_event_ledger` from `BoundedConstitutionalQuestion.writes_event_ledger`.
- `mutates_cluster` from `BoundedConstitutionalQuestion.mutates_cluster`.

## Deterministic mapping

Selection keys are projected only from exact caller-declared selection-key fields in `caller_supplied_fields`:

- field name `selection_key` projects its field value as one exact key;
- field name prefix `selection_key:` projects the suffix as one exact key.

Duplicate keys are collapsed deterministically while preserving first occurrence after the bounded-question producer's deterministic field ordering.

No time, randomness, external service, model inference, mutable global state, repository mutation, event-ledger state, cluster state, hidden registration state, semantic similarity, fuzzy matching, or heuristic interpretation participates in projection.

## Identity preservation

`bounded_question_id` is preserved exactly.

## Provenance preservation

Operator inquiry provenance remains traceable through the preserved bounded-question identity. Projection does not duplicate raw operator testimony or provenance text into the Selection input because the existing projection schema has no provenance field.

## Uncertainty propagation

`BoundedConstitutionalQuestion.uncertainty` is copied into `ConstitutionalQuestionProjection.uncertainty` without rewriting.

## Unknown propagation

`BoundedConstitutionalQuestion.unknowns` are preserved in Selection's existing uncertainty channel as deterministic `unknown: ...` entries because the existing projection schema has no separate `unknowns` field.

## Insufficient-input behavior

If the bounded question lacks exact explicit selection-key fields, projection emits an empty `selection_keys` tuple. It does not guess from operator inquiry wording, bounded question text, constitutional intent, scope status, or presentation vocabulary.

## Selection-key behavior

Selection keys are explicit caller-supplied data. The projection helper only re-exposes those exact keys in the existing projection artifact. It does not introduce semantic matching, synonyms, token scoring, embeddings, model classification, inferred intent, fuzzy keys, fallback guesses, or heuristic capability demands.

## Testimony / evidence / fact boundary

Operator testimony remains evidence, not fact. Projection does not promote testimony into established fact, verified claim, constitutional authority, repository truth, durable knowledge, authoritative capability, selected constitutional view, lawful action, or implementation instruction.

## Read-only behavior

Projection is read-only and carries forward the bounded-question read-only flag.

## Event-ledger behavior

Projection writes no event ledger entries and carries forward `writes_event_ledger=False` for the implemented producer path.

## Cluster mutation behavior

Projection mutates no cluster state and carries forward `mutates_cluster=False` for the implemented producer path.

## Producer / projection boundary

The bounded-question producer remains responsible for `Operator Inquiry -> BoundedConstitutionalQuestion`. Question Projection only derives Selection-facing projection from the immutable bounded artifact.

## Projection / Selection boundary

Question Projection does not select constitutional views. Existing Selection remains the only owner of exact-key comparison between `ConstitutionalQuestionProjection` and `ConstitutionalCapabilityProjection`.

## Compatibility preservation

Preserved:

- existing `ConstitutionalQuestionProjection` schema;
- existing Selection input and output behavior;
- exact-key matching;
- manually constructed projection fixtures;
- Selection JSON behavior;
- Composition behavior;
- CLI behavior;
- diagnostic inventory;
- diagnostic-shape registration;
- event-ledger behavior;
- cluster mutation behavior;
- public schemas.

## Required explicit answers

Did this task recover new architecture?

No.

Does QuestionProjection interpret unrestricted natural language?

No.

Does QuestionProjection produce CapabilityProjection?

No.

Does QuestionProjection select constitutional views?

No.

Does QuestionProjection promote operator testimony into fact?

No.

Does QuestionProjection write the event ledger or mutate cluster state?

No.

## Files changed

- `seed_runtime/constitutional_view_selection.py`
- `tests/test_constitutional_question_projection.py`
- `constitutional_question_projection_implementation_001.md`

## Tests added or changed

Added `tests/test_constitutional_question_projection.py` covering:

- real bounded-question input;
- deterministic equivalent projections;
- exact bounded-question identity preservation;
- authorized field projection only;
- provenance traceability through the source bounded question and preserved identity;
- no testimony-to-fact promotion;
- uncertainty propagation;
- unknown propagation;
- no guessed selection keys when explicit projection information is absent;
- no capability projection;
- no selected views;
- no composition request;
- read-only / no-ledger / no-cluster-mutation flags;
- source bounded-question immutability;
- manual projection fixture compatibility;
- consumption by existing Selection with explicit capability projection.

## Tests executed

```text
pytest -q tests/test_constitutional_question_projection.py tests/test_bounded_constitutional_question.py tests/test_constitutional_view_selection.py tests/test_constitutional_view_composition.py
```

Result: 23 passed.

## LOC delta

+394 / -0

## Remaining next pressure

Deterministic CapabilityProjection production.

## Commit hash

Final commit hash is reported in the completion response; embedding the final Git object hash inside the committed file would change that hash.
