# Constitutional Pipeline Diagnostic Implementation 001

## Orientation verification

Verified the repository already contained `ConstitutionalPipelineRequest`, `ConstitutionalPipelineResult`, `invoke_constitutional_pipeline(...)`, `constitutional_pipeline_result_json(...)`, and `format_constitutional_pipeline_result(...)` in `seed_runtime/constitutional_pipeline.py`.

Verified the public surface `seed --constitutional-pipeline` existed in `scripts/seed_local.py`.

Verified `constitutional_pipeline` was already registered as a public surface in `seed_runtime/diagnostic_inventory.py` and `seed_runtime/diagnostic_shape_audit.py`.

No existing diagnostic executed the complete constitutional pipeline and exposed deterministic stage-level condition. The missing seam was `ConstitutionalPipelineResult -> full-pipeline diagnostic result -> diagnostic JSON / human rendering`.

## Diagnostic evidence inspected

Inspected the pipeline invocation module, CLI dispatch, diagnostic inventory, diagnostic shape audit, constitutional selection, constitutional view composition, and existing tests around public pipeline and diagnostic conventions.

## Diagnostic name

`constitutional_pipeline_diagnostic`, exposed as `seed --constitutional-pipeline-diagnostic`.

## Diagnostic request or input artifact

The CLI consumes the same explicit bounded input fields as `seed --constitutional-pipeline` and constructs a `ConstitutionalPipelineRequest`.

The implementation provides both:

- `build_constitutional_pipeline_diagnostic(request)`, which invokes the existing pipeline exactly once.
- `constitutional_pipeline_diagnostic_from_result(request=..., result=...)`, which consumes an already completed `ConstitutionalPipelineResult` without re-running stages.

## Diagnostic result artifact

Implemented immutable `ConstitutionalPipelineDiagnosticResult` and immutable per-stage `ConstitutionalPipelineStageDiagnostic` artifacts.

The result preserves the request, the complete pipeline result, deterministic stage order, selected views, no-view reasons, composition compatibility answer, read-only status, event-ledger status, cluster-mutation status, recordability, testimony boundary, and diagnostic boundary.

## Stage status model

Typed deterministic statuses are: `complete`, `empty`, `unsupported`, `unknown`, and `refused`.

The diagnostic classifies only from typed artifacts and does not rerun or reproduce stage algorithms.

## Pipeline invocation or result-consumption path

CLI execution calls `build_constitutional_pipeline_diagnostic(request)`, which calls `invoke_constitutional_pipeline(request)` from the existing pipeline module exactly once.

Existing-result consumption is available via `constitutional_pipeline_diagnostic_from_result(...)` for callers that already own a completed pipeline result.

## Successful-path findings

Successful exact-key selection reports selected view names, complete selection status, composition contributing-view counts, and preserved read-only boundaries.

## Empty-path findings

Missing question selection keys are reported as `question_projection=empty`, selection is `empty`, composition request is `empty`, and composition is `empty`. Empty composition is not reported as verified constitutional success.

## Unsupported-path findings

Unmatched exact keys are reported separately as `selection=unsupported` with explicit `unsupported_keys`.

## Unknown propagation

Bounded-question Unknowns, capability-projection Unknowns, selection uncertainty derived from Unknowns, and composition preserved Unknowns remain visible as distinct fields.

## Refusal propagation

Composition preserved refusals are counted and surfaced, and the composition stage reports `refused` when refusals are present.

## Provenance handling

The diagnostic preserves the original `ConstitutionalPipelineRequest` and the complete `ConstitutionalPipelineResult`, including bounded-question provenance and identity.

## Testimony/evidence/fact boundary

The diagnostic reports that operator testimony entered the pipeline as evidence and explicitly preserves that it is not established fact.

## JSON output

`constitutional_pipeline_diagnostic_json(...)` emits deterministic typed fields using the repository serialization convention.

## Human output

`format_constitutional_pipeline_diagnostic(...)` renders boundary lines and a deterministic stage table with stage, status, artifact/counts, uncertainty/Unknown/refusal summary, and read-only/ledger/mutation status.

## Recordability decision

The diagnostic is read-only and non-recording. It has `record_scope=none`.

## Event-ledger behavior

The diagnostic does not write the event ledger. Tests prove CLI diagnostic execution with `--db` does not create or append an event-ledger database.

## Cluster mutation behavior

The diagnostic does not mutate cluster state. The result and inventory declare `mutates_cluster=false`.

## Inventory registration

Added `constitutional_pipeline_diagnostic` to the diagnostic inventory with JSON support, no record support, no event-ledger writes, and no cluster mutation.

## Shape-audit registration

Added `constitutional_pipeline_diagnostic` to diagnostic shape audit specs with build, JSON, format, and CLI flag entries.

## Compatibility preservation

Preserved `seed --constitutional-pipeline`, constitutional view composition, pipeline schemas, pipeline invocation behavior, public pipeline JSON/human output, exact-key selection, composition behavior, and existing diagnostic registrations.

## Files changed

- `scripts/seed_local.py`
- `seed_runtime/constitutional_pipeline_diagnostic.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_constitutional_pipeline_diagnostic.py`
- `constitutional_pipeline_diagnostic_implementation_001.md`

## Tests changed

Added focused full-pipeline diagnostic tests covering successful path, empty keys, unsupported keys, missing capability evidence, Unknown propagation, refusal propagation, deterministic JSON/human output, non-recording behavior, inventory visibility, and shape-audit visibility.

## Tests executed

- `pytest -q tests/test_constitutional_pipeline_diagnostic.py`
- `pytest -q tests/test_constitutional_pipeline_diagnostic.py tests/test_constitutional_pipeline.py tests/test_constitutional_pipeline_public_surface.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## LOC delta

`+725 / -18`

## Commit hash

`b9198d86f0ca6316a2f512e1fc4ce944d5d9ddc5`

## Remaining next pressure

End-to-end constitutional provenance explanation.

## Explicit answers

Did this task recover new architecture?

No.

Does the diagnostic duplicate pipeline-stage ownership?

No.

Does the diagnostic interpret unrestricted natural language?

No.

Does the diagnostic promote operator testimony into fact?

No.

Does the diagnostic distinguish empty, unsupported, Unknown, and refused outcomes?

Yes.

Does the diagnostic mutate cluster state?

No.
