# Constitutional Pipeline Integration Wiring 001

## Orientation verification

Verified current code contains `invoke_constitutional_pipeline(...)`, `explain_constitutional_pipeline_provenance(...)`, `constitutional_pipeline_result_json(...)`, and `format_constitutional_pipeline_result(...)` in `seed_runtime/constitutional_pipeline.py`.

Verified the completed pipeline stages remain ordered as:

```text
Operator Inquiry
        ↓
BoundedConstitutionalQuestion
        ↓
QuestionProjection
        +
CapabilityProjection
        ↓
Selection
        ↓
Composition
        ↓
Provenance Explanation
```

The remaining pressure was not recovery of those stages. It was compatibility-preserving integration with one existing inquiry path.

## Inquiry paths inspected

- `seed --constitutional-pipeline`: already invokes the complete pipeline from explicit CLI fields. It remains the existing producer/consumer used by this wiring.
- `seed --constitutional-pipeline-diagnostic`: already wraps the complete pipeline for diagnostic shape visibility; rejected because it is a diagnostic path, not the narrow inquiry consumer.
- `ask --question-family ...`: existing bounded ask inquiry path with exact Question Family admission, eligibility, surface-argument handling, dispatch selection, namespace handoff, and refusal behavior.
- `--inquiry-orientation`: rejected because it orients recorded inquiry notes and cannot supply explicit bounded constitutional request fields without semantic inference.
- Question Surface Inventory dispatch: inspected as the bounded ask inventory/eligibility authority; used only to expose the existing path and its dispatch mapping.

## Selected integration path

Selected path:

```text
ask --question-family "constitutional pipeline" --surface-args ...
        ↓
existing exact Question Family admission and bounded ask eligibility
        ↓
existing bounded ask dispatch namespace handoff
        ↓
ConstitutionalPipelineRequest construction in the existing --constitutional-pipeline consumer
        ↓
invoke_constitutional_pipeline(...)
        ↓
existing constitutional pipeline JSON/human response
```

This is the narrowest lawful consumer because bounded ask already receives operator inquiry input, already owns exact admission/refusal, and can carry explicit bounded fields as operator-provided surface args without prose inference.

## Rejected paths and reasons

- Inquiry Orientation: lacks explicit bounded constitutional fields and would require inference from recorded prose.
- Diagnostic pipeline: already diagnostic, not the inquiry-answer path requested.
- Broad application message dispatch: would create routing authority and alter admission.
- Any semantic matching from unrestricted prose: rejected by input-boundary constraints.

## Existing producer and consumer

- Producer: bounded ask exact Question Family path and its explicit `--surface-args` handling in `seed_runtime/question_surface_inventory.py` and `scripts/seed_local.py`.
- Consumer: existing `--constitutional-pipeline` CLI branch in `scripts/seed_local.py`, which constructs `ConstitutionalPipelineRequest`, invokes `invoke_constitutional_pipeline(...)`, and renders the existing result.

## Adapter inputs

The adapter accepts exactly six explicit surface args for the `constitutional pipeline` Question Family:

1. `operator_inquiry`
2. `inquiry_source`
3. `bounded_question`
4. `constitutional_intent`
5. `scope_status`
6. `selection_key`

An empty `selection_key` preserves absence and does not infer a key.

## Pipeline request mapping

The bounded ask adapter maps explicit positional values onto the existing CLI namespace fields:

- `constitutional_pipeline=True`
- `operator_inquiry=<arg 1>`
- `inquiry_provenance=<arg 2>`
- `bounded_question=<arg 3>`
- `constitutional_intent=<arg 4>`
- `scope_status=<arg 5>`
- `selection_key=(<arg 6>,)` when non-empty, otherwise `()`

The existing `--constitutional-pipeline` branch then constructs the real `ConstitutionalPipelineRequest` exactly as before.

## Pipeline invocation

The complete pipeline is invoked by the existing consumer with `invoke_constitutional_pipeline(request)`. The bounded ask adapter does not invoke pipeline stages directly and does not duplicate pipeline ownership.

## Result handoff

The result handoff is the existing constitutional pipeline response. JSON output preserves the nested `pipeline_result` equivalent as the existing full result shape plus nested `provenance_explanation`. Human output remains the existing formatter.

No broad schema replacement was introduced.

## Provenance preservation

The integration preserves the explicit inquiry source as `inquiry_provenance` and verifies it appears in the bounded question and provenance explanation.

## Unknown/refusal propagation

- Missing selection key is preserved as no key and produces empty selection without inferred irrelevance.
- Unsupported selection key remains explicit and produces existing selection uncertainty.
- Existing bounded ask refusal for diagnostic-only/non-answer surfaces remains owned by bounded ask and does not invoke the pipeline.

## Testimony/evidence/fact boundary

Operator inquiry text remains testimony. Passing through bounded ask and the constitutional pipeline does not verify testimony or promote it into cluster fact.

## Compatibility preservation

- Existing direct `--constitutional-pipeline` behavior is unchanged.
- Existing bounded ask admission/refusal behavior is unchanged.
- Unrelated bounded ask paths are not redirected to the pipeline.
- Exact-key Selection remains exact.
- Missing keys are not inferred.

## Event-ledger behavior

The selected path does not add event-ledger writes. Tests verify the provenance explanation reports `writes_event_ledger=false` for the successful path.

## Cluster mutation behavior

The selected path does not mutate cluster state. Tests verify the provenance explanation reports `mutates_cluster=false` for the successful path.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `tests/test_constitutional_pipeline_integration_wiring.py`
- `constitutional_pipeline_integration_wiring_001.md`

## Tests changed

Added `tests/test_constitutional_pipeline_integration_wiring.py` covering:

- successful exact-key path;
- no-selection-key path;
- unsupported-key path;
- existing bounded ask refusal path;
- unrelated bounded ask path not redirected;
- adapter/admission/pipeline ownership boundaries.

## Tests executed

```text
pytest -q tests/test_constitutional_pipeline_integration_wiring.py
pytest -q tests/test_question_surface_inventory.py tests/test_constitutional_pipeline_integration_wiring.py
pytest -q tests/test_constitutional_pipeline_integration_wiring.py tests/test_constitutional_pipeline.py tests/test_constitutional_pipeline_public_surface.py tests/test_constitutional_pipeline_diagnostic.py tests/test_constitutional_pipeline_provenance_explanation.py tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Final focused suite result: `208 passed`.

## LOC delta

`+397 / -11`

## Commit hash

Recorded in completion response for the final amended commit containing this report.

## Remaining pressure

Constitutional pipeline operational documentation or repository self-consumption demonstration, chosen from repository evidence.

## Explicit answers

```text
Did this task recover new architecture?

No.
```

```text
Did this task create a new inquiry path?

No.
```

```text
Does the adapter infer constitutional meaning from unrestricted language?

No.
```

```text
Does integration duplicate pipeline-stage ownership?

No.
```

```text
Does integration promote operator testimony into fact?

No.
```

```text
Does integration write the event ledger or mutate cluster state?

No, unless pre-existing repository authority explicitly requires otherwise.
```
