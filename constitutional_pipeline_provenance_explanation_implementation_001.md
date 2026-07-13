# Constitutional Pipeline Provenance Explanation Implementation 001

## Orientation verification

Verified repository authority before implementation:

- `ConstitutionalPipelineRequest`, `ConstitutionalPipelineResult`, and `invoke_constitutional_pipeline(...)` exist in `seed_runtime/constitutional_pipeline.py`.
- `ConstitutionalPipelineDiagnosticResult` and `build_constitutional_pipeline_diagnostic(...)` exist in `seed_runtime/constitutional_pipeline_diagnostic.py`.
- `constitutional_pipeline_result_json(...)` and `format_constitutional_pipeline_result(...)` exist in `seed_runtime/constitutional_pipeline.py`.
- The implemented path already ran: Operator Inquiry -> `BoundedConstitutionalQuestion` -> `ConstitutionalQuestionProjection` + `ConstitutionalCapabilityProjection` -> `SelectedConstitutionalViews` -> `ConstitutionalViewCompositionArtifact` -> `ConstitutionalPipelineResult` -> pipeline diagnostic.
- No existing artifact owned the complete deterministic answer to why exact selection keys produced selected views or did not produce views.

## Implementation evidence inspected

Inspected:

- `seed_runtime/constitutional_pipeline.py`
- `seed_runtime/constitutional_view_selection.py`
- `seed_runtime/constitutional_view_composition.py`
- `seed_runtime/constitutional_pipeline_diagnostic.py`
- constitutional pipeline, public-surface, diagnostic, inventory, and shape-audit tests.

## Explanation artifact

Implemented immutable `ConstitutionalPipelineProvenanceExplanation` in `seed_runtime/constitutional_pipeline.py`.

It preserves bounded typed evidence for:

- bounded question identity;
- inquiry provenance;
- operator inquiry as testimony;
- explicit question selection keys;
- projected capability keys by registered view;
- exact matched keys;
- unsupported question keys;
- selected views;
- absent / unsupported / unavailable explanations;
- selection uncertainty;
- empty-selection explanation;
- composition contributors;
- preserved composition Unknowns;
- preserved composition refusals;
- read-only, event-ledger, and cluster-mutation boundaries.

## Explanation producer

Implemented `explain_constitutional_pipeline_provenance(result)`.

The helper accepts one completed `ConstitutionalPipelineResult`, reads existing stage artifacts only, and returns one immutable explanation artifact.

It performs no pipeline stage again.
It performs no capability discovery.
It performs no selection.
It performs no composition.
It performs no event-ledger write or cluster mutation.

## Source pipeline artifacts consumed

The producer consumes:

- `result.bounded_question`
- `result.question_projection`
- `result.capability_projection`
- `result.selection`
- `result.composition_request` indirectly through composition identity preserved on the result
- `result.composition`

## Exact-key provenance chain

The explanation follows only this chain:

1. caller-supplied selection key already preserved by bounded question fields;
2. `ConstitutionalQuestionProjection.selection_keys`;
3. `ConstitutionalCapabilityProjection.capability_keys`;
4. exact set membership comparison over completed projection artifacts;
5. `SelectedConstitutionalViews.selected_view_names`;
6. composition request requested views;
7. `ConstitutionalViewCompositionArtifact.contributing_views`.

## Matched-key explanation

A key is reported as matched only when the exact question selection key appears in projected capability keys.

## Unsupported-key explanation

A key is reported as unsupported only when the exact question selection key does not appear in any projected capability key.

No semantic inference or relevance claim is made.

## Missing-key explanation

When no explicit question selection key was supplied, the explanation reports `absent: no explicit question selection key was supplied` and states that empty selection is not verified irrelevance.

## Missing-capability explanation

When capability projection evidence is Unknown and no capability keys are available, the explanation reports the unavailable projection separately from unsupported exact keys.

## Selected-view explanation

Selected views are reported from `SelectedConstitutionalViews.selected_view_names`; the explanation does not decide which views should be selected.

## Composition-contributor explanation

Composition contributors are reported from `ConstitutionalViewCompositionArtifact.contributing_views`; the explanation does not recompose views.

## Unknown preservation

Selection uncertainty and composition Unknowns are preserved distinctly.

## Refusal preservation

Composition refusals are preserved distinctly from Unknowns, unsupported keys, empty selection, and selected views.

## Testimony / evidence / fact boundary

The explanation preserves operator inquiry as testimony and includes the boundary: operator testimony is evidence, not established fact.

It does not state that the operator claim is true, that the inquiry proves a fact, or that composition verifies testimony.

## Public JSON exposure

`constitutional_pipeline_result_json(...)` now adds one nested `provenance_explanation` field while preserving existing top-level result fields.

## Public human exposure

`format_constitutional_pipeline_result(...)` now includes a bounded `Provenance explanation` section with:

- why these views were selected;
- why requested keys were unsupported;
- remaining uncertainty;
- composition contributors.

## Diagnostic relationship

The provenance explanation remains distinct from the pipeline diagnostic.

Diagnostic status classification remains owned by `seed_runtime/constitutional_pipeline_diagnostic.py`.

## Determinism

Tests prove equivalent completed pipeline results produce equivalent explanations, JSON output is deterministic, and human output is deterministic.

## Compatibility preservation

The implementation preserves existing stage artifacts, stage behavior, selected views, composition behavior, public pipeline command behavior, diagnostic behavior, event-ledger behavior, and cluster-mutation behavior.

## Event-ledger behavior

No event-ledger entry is written. The explanation computes `writes_event_ledger` from completed stage artifacts only.

## Cluster mutation behavior

No cluster state is mutated. The explanation computes `mutates_cluster` from completed stage artifacts only.

## Files changed

- `seed_runtime/constitutional_pipeline.py`
- `tests/test_constitutional_pipeline_provenance_explanation.py`
- `constitutional_pipeline_provenance_explanation_implementation_001.md`

## Tests changed

Added focused provenance explanation tests covering:

- successful exact-match path;
- no-selection-key path;
- unsupported-key path;
- missing-capability path;
- Unknown path;
- refusal path;
- boundary separation from projection, selection, composition, and diagnostic classification;
- no pipeline re-execution during explanation;
- public JSON and human exposure;
- event-ledger and cluster-mutation preservation.

## Tests executed

- `pytest -q tests/test_constitutional_pipeline_provenance_explanation.py`
- `pytest -q tests/test_constitutional_pipeline.py tests/test_constitutional_pipeline_public_surface.py tests/test_constitutional_pipeline_diagnostic.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## LOC delta

+543 / -1

## Commit hash

f4a8836

## Remaining next pressure

Integration wiring — Seed consuming its constitutional pipeline through an existing repository-supported inquiry path.

## Explicit answers

### Did this task recover new architecture?

No.

### Does provenance explanation perform Selection?

No.

### Does it infer why the operator supplied a selection key?

No.

### Does it promote operator testimony into fact?

No.

### Does it distinguish absent, unsupported, Unknown, refused, and selected outcomes?

Yes.

### Does it write the event ledger or mutate cluster state?

No.
