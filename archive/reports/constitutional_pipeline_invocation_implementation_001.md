# Constitutional Pipeline Invocation Implementation 001

## Orientation verification

Verified current repository implementation contains the required stage artifacts and functions:

- `BoundedConstitutionalQuestion`
- `produce_bounded_constitutional_question(...)`
- `ConstitutionalQuestionProjection`
- `project_constitutional_question(...)`
- `ConstitutionalCapabilityProjection`
- `project_constitutional_capabilities(...)`
- `ConstitutionalViewSelection` as implemented by `SelectedConstitutionalViews` and `select_constitutional_views(...)`
- `SelectedConstitutionalViews`
- `selected_constitutional_views_to_composition_request(...)`
- `ConstitutionalViewComposition` as implemented by `ConstitutionalViewCompositionArtifact`
- `build_constitutional_view_composition(...)`

Verified implemented topology:

```text
Operator Inquiry
        ↓
BoundedConstitutionalQuestion
        ↓
QuestionProjection
        +
CapabilityProjection
        ↓
ConstitutionalViewSelection
        ↓
SelectedConstitutionalViews
        ↓
ConstitutionalViewComposition
        ↓
ConstitutionalViewCompositionArtifact
```

The missing seam was deterministic invocation of these already implemented responsibilities as one typed pipeline.

## Implementation evidence inspected

Inspected implementation evidence in:

- `seed_runtime/bounded_constitutional_question.py`
- `seed_runtime/constitutional_view_selection.py`
- `seed_runtime/constitutional_view_composition.py`
- `tests/test_bounded_constitutional_question.py`
- `tests/test_constitutional_question_projection.py`
- `tests/test_constitutional_capability_projection.py`
- `tests/test_constitutional_view_selection.py`
- `tests/test_constitutional_view_composition.py`

## Implemented request artifact

Implemented `ConstitutionalPipelineRequest` in `seed_runtime/constitutional_pipeline.py`.

The request is immutable and contains the explicit bounded-question producer inputs, composition adapter inputs, and optional immutable capability-source inputs for deterministic invocation and tests. It does not require unrestricted language interpretation. It preserves explicit caller input and provenance. It does not infer selection keys from inquiry prose.

## Implemented result artifact

Implemented `ConstitutionalPipelineResult` in `seed_runtime/constitutional_pipeline.py`.

The result is immutable and preserves existing typed stage artifacts:

- `bounded_question`
- `question_projection`
- `capability_projection`
- `selection`
- `composition_request`
- `composition`

It does not flatten or replace existing schemas.

## Implemented invocation function

Implemented `invoke_constitutional_pipeline(...)` in `seed_runtime/constitutional_pipeline.py`.

## Exact stage order

The invocation order is:

1. `produce_bounded_constitutional_question(...)`
2. `project_constitutional_question(...)`
3. `project_constitutional_capabilities(...)`
4. `select_constitutional_views(...)`
5. `selected_constitutional_views_to_composition_request(...)`
6. `build_constitutional_view_composition(...)`
7. return `ConstitutionalPipelineResult`

## Typed handoffs

- Bounded-question producer returns `BoundedConstitutionalQuestion`.
- Question Projection consumes `BoundedConstitutionalQuestion` and returns `ConstitutionalQuestionProjection`.
- Capability Projection returns `tuple[ConstitutionalCapabilityProjection, ...]`.
- Selection consumes the question projection and capability projections and returns `SelectedConstitutionalViews`.
- The adapter consumes `SelectedConstitutionalViews` and returns `ConstitutionalViewCompositionRequest`.
- Composition consumes `ConstitutionalViewCompositionRequest` and returns `ConstitutionalViewCompositionArtifact`.

## Bounded-question production

The invocation calls the existing bounded-question producer and does not produce bounded-question semantics itself.

## Question Projection invocation

The invocation calls the existing Question Projection producer and does not derive selection keys itself.

## Capability Projection invocation

The invocation calls the existing Capability Projection producer and does not discover, repair, or register capabilities.

## Selection invocation

The invocation calls existing Selection and does not match keys itself.

## Selection-to-Composition adaptation

The invocation calls the existing `selected_constitutional_views_to_composition_request(...)` adapter.

## Composition invocation

The invocation calls existing Composition and does not build view explanations itself.

## Successful-path behavior

A focused success-path test proves a real operator inquiry flows through every implemented stage, exact caller-supplied selection key `process` selects `constitutional_process`, and every stage artifact is observable in the final result.

## Insufficient-information behavior

Focused insufficient-information tests prove missing question keys are not guessed, missing capability evidence is not guessed, unmatched exact keys preserve Selection uncertainty, and empty selections compose through the existing Composition path without invented success.

## Unknown propagation

Unknowns supplied to bounded-question production flow through Question Projection into Selection uncertainty using existing projection behavior.

## Refusal propagation

The invocation does not alter Composition refusal propagation. Composition remains responsible for preserved contributing view refusals.

## Provenance preservation

The result exposes the real `BoundedConstitutionalQuestion`, preserving `operator_inquiry`, `inquiry_provenance`, caller-supplied fields, and the bounded-question identity.

## Testimony/evidence/fact boundary

The invocation preserves `testimony_status="operator testimony preserved as evidence, not established fact"` and does not introduce `established_fact` or `verified_claim` fields.

## Determinism

Equivalent requests and equivalent capability sources produce equivalent results. The invocation uses no current time, randomness, model inference, external service, event-ledger state, cluster mutation, semantic matching, fuzzy matching, recovery, or heuristic fallback.

## Read-only behavior

Tests assert all stage artifacts in the result preserve read-only behavior.

## Event-ledger behavior

Tests assert all stage artifacts in the result preserve `writes_event_ledger=False`.

## Cluster mutation behavior

Tests assert all stage artifacts in the result preserve `mutates_cluster=False`.

## Compatibility preservation

Existing bounded-question, Question Projection, Capability Projection, Selection, and Composition tests remain green. No CLI surface, diagnostic registration, event type, mutation path, registry, scheduler, or generalized pipeline engine was added.

## Files changed

- `seed_runtime/constitutional_pipeline.py`
- `tests/test_constitutional_pipeline.py`
- `constitutional_pipeline_invocation_implementation_001.md`

## Tests added or changed

Added `tests/test_constitutional_pipeline.py` with focused success, determinism, insufficiency, unmatched-key, read-only, non-mutating, and boundary-call tests.

## Tests executed

```text
pytest -q tests/test_constitutional_pipeline.py
pytest -q tests/test_constitutional_pipeline.py tests/test_bounded_constitutional_question.py tests/test_constitutional_question_projection.py tests/test_constitutional_capability_projection.py tests/test_constitutional_view_selection.py tests/test_constitutional_view_composition.py
```

## LOC delta

Final committed delta:

```text
+556 / -0
```

## Remaining next pressure

Public constitutional pipeline surface or full-pipeline diagnostic exposure, chosen from repository evidence after invocation is complete.

## Commit hash

Commit containing this report. Exact final commit hash is reported in the completion response because embedding the final self-hash would change the commit identity.

## Explicit answers

```text
Did this task recover new architecture?

No.
```

```text
Does the invocation duplicate stage ownership?

No.
```

```text
Does the invocation interpret unrestricted natural language?

No.
```

```text
Does the invocation invent question or capability keys?

No.
```

```text
Does the invocation promote operator testimony into fact?

No.
```

```text
Does the invocation write the event ledger or mutate cluster state?

No.
```
