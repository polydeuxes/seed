# Constitutional Pipeline Public Surface Implementation 001

## Orientation verification

Verified the existing implementation contains `ConstitutionalPipelineRequest`, `ConstitutionalPipelineResult`, and `invoke_constitutional_pipeline(...)` in `seed_runtime/constitutional_pipeline.py`.

Verified the complete typed path is already implemented by the pipeline invocation:

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
ConstitutionalPipelineResult
```

The repository had public constitutional view surfaces and explicit view composition, but no public CLI/application surface invoking the complete pipeline end-to-end before this task.

## Public-surface evidence inspected

Inspected:

- `scripts/seed_local.py`
- existing constitutional CLI options: `--constitutional-process`, `--constitutional-governance`, `--constitutional-fidelity`, `--constitutional-view-composition`
- constitutional composition JSON and human formatters in `seed_runtime/constitutional_view_composition.py`
- diagnostic/output conventions in `seed_runtime/diagnostic_inventory.py` and `seed_runtime/diagnostic_shape_audit.py`
- argument validation conventions in `scripts/seed_local.py`
- constitutional CLI tests in `tests/test_constitutional_view_composition.py` and related view tests
- `seed_runtime/constitutional_pipeline.py`
- bounded question, question projection, capability projection, selection, and composition stage artifacts

## Command or application entrypoint

Added one narrow CLI public surface:

```text
seed --constitutional-pipeline
```

Implemented in `scripts/seed_local.py` using the repository's existing JSON flag convention (`--json`) and existing human-output convention.

## Accepted inputs

The public surface accepts only explicit operator-supplied bounded inputs:

- `--operator-inquiry`
- `--inquiry-provenance`
- `--bounded-question`
- `--constitutional-intent`
- `--scope-status`
- repeated `--pipeline-uncertainty`
- repeated `--pipeline-unknown`
- repeated exact `--selection-key`
- existing `--composition-purpose`
- existing `--json`

It does not parse unrestricted language into selection keys.

## Request construction

The CLI constructs a real `ConstitutionalPipelineRequest` from the explicit arguments. Exact caller selection keys are preserved as `caller_supplied_fields=(('selection_key', key), ...)` so the existing question projection stage remains the only owner of selection-key projection.

## Pipeline invocation

The public surface invokes `invoke_constitutional_pipeline(...)` exactly once per request.

The surface owns only:

- input parsing;
- request construction;
- invocation;
- result rendering.

It does not own bounded-question production, projection, capability registration, selection, composition, constitutional reasoning, provenance authority, persistence, mutation, planning, or recovery.

## JSON output

Added `constitutional_pipeline_result_json(...)`, which returns the deterministic typed pipeline result using the repository serialization convention. The JSON preserves the typed stage artifacts rather than flattening them into a competing schema.

JSON output exposes:

- bounded question identity and provenance;
- question projection;
- capability projection;
- selected constitutional views;
- selection uncertainty;
- composition request;
- composition result;
- read-only status;
- event-ledger behavior;
- cluster-mutation behavior.

## Human output

Added `format_constitutional_pipeline_result(...)`, a bounded human-readable rendering of the complete result. The formatter reports the operator inquiry as supplied testimony and includes the testimony boundary explicitly.

Human output exposes:

- operator inquiry as supplied testimony;
- inquiry provenance;
- bounded-question identity;
- question projection keys;
- capability projection keys;
- selected views;
- selection uncertainty;
- composition result;
- preserved Unknowns;
- preserved refusals;
- read-only/event-ledger/cluster-mutation status.

## Successful behavior

A request with `--selection-key process` selects `constitutional_process` by exact key and composes the existing registered Constitutional Process View.

## Insufficient-information behavior

A request with no `--selection-key` does not infer keys from operator text. It produces an empty selection, preserves selection uncertainty, and composes no views.

## Unknown and refusal preservation

Unknowns supplied to the bounded question remain visible in the bounded question and projection uncertainty. Unknowns and refusals from selected contributing views remain visible in composition output.

Unmatched exact keys remain visible as unsupported selection-key uncertainty.

## Provenance preservation

The operator inquiry and inquiry provenance are preserved in the bounded-question artifact and rendered in JSON and human output.

## Testimony/evidence/fact boundary

The public surface does not render the operator inquiry as established fact, verified claim, constitutional authority, repository truth, durable knowledge, or authoritative capability. It reports what the operator supplied and how the deterministic pipeline handled it.

## Compatibility preservation

Preserved:

- existing explicit constitutional view composition CLI;
- lower-level APIs;
- typed stage artifacts;
- exact-key selection behavior;
- diagnostic inventory and shape-audit conventions;
- event-ledger behavior;
- cluster-mutation behavior.

The full-pipeline public surface remains distinct from the explicit-view composition surface.

## Operational visibility determination

The new public surface is a public operational output surface. Under `AGENTS.md`, required public-surface inventory visibility was added to:

- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`

This is compatibility registration for public-surface visibility only. It is not full-pipeline diagnostic execution exposure.

## Files changed

- `scripts/seed_local.py`
- `seed_runtime/constitutional_pipeline.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_constitutional_pipeline_public_surface.py`
- `constitutional_pipeline_public_surface_implementation_001.md`

## Tests changed

Added `tests/test_constitutional_pipeline_public_surface.py` covering:

1. request construction and single pipeline invocation;
2. successful exact-key selection and composition;
3. operator inquiry/provenance visibility;
4. missing selection keys are not guessed;
5. unmatched keys remain uncertain;
6. refusals, Unknowns, and empty selections remain visible;
7. JSON determinism and human determinism;
8. testimony is not rendered as fact;
9. no event-ledger writes or cluster mutation in rendered artifacts;
10. existing explicit-view composition surface remains unchanged;
11. required public-surface inventory visibility.

## Tests executed

```text
pytest -q tests/test_constitutional_pipeline_public_surface.py
pytest -q tests/test_constitutional_pipeline_public_surface.py tests/test_constitutional_pipeline.py tests/test_constitutional_question_projection.py tests/test_constitutional_view_composition.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
pytest -q tests/test_bounded_constitutional_question.py tests/test_constitutional_question_projection.py tests/test_constitutional_capability_projection.py tests/test_constitutional_view_selection.py tests/test_constitutional_view_composition.py tests/test_constitutional_pipeline.py tests/test_constitutional_pipeline_public_surface.py tests/test_constitutional_process_view.py tests/test_constitutional_governance_view.py tests/test_constitutional_fidelity_view.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## LOC delta

+597 / -1

## Commit hash

efc3d39fca27d395a52d53b5e8ec57a4bfcb8034

## Explicit answers

```text
Did this task recover new architecture?

No.
```

```text
Does the public surface duplicate pipeline-stage logic?

No.
```

```text
Does it infer selection keys from unrestricted language?

No.
```

```text
Does it promote operator testimony into fact?

No.
```

```text
Does it write the event ledger or mutate cluster state?

No.
```

## Remaining next pressure

Full-pipeline diagnostic exposure.
