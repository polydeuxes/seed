# Operator-Ingress Question Origination Deletion Audit 001

Repository authority wins. This audit is read-only with respect to implementation. It identifies the deletion boundary for the invalid path that mints a canonical `BoundedConstitutionalQuestion` directly from operator ingress authority/scope binding.

## Finding

The current live production path is invalid and must be deleted, not preserved as compatibility behavior:

```text
AttributedOperatorExpression
→ OperatorExpressionInterpretationProjection
→ OperatorAuthorityScopeBindingProjection
→ FutureBoundedConstitutionalQuestionHandoff
→ formulate_bounded_constitutional_question(...)
→ BoundedConstitutionalQuestion
```

The lawful replacement topology is:

```text
external grammar
→ interpretation
→ authority and scope
→ authorized constitutional intent / bounded goal
→ advancement diagnosis
```

Only an established inquiry frontier may normally originate the canonical internal question:

```text
BoundedInquiryFrontier
→ BoundedConstitutionalQuestion
```

The implementation must therefore stop treating permitted operator ingress as question origination. A permitted operator request may preserve expression, interpretation, authority, scope, provenance, uncertainty, presentation preference, and effect constraints, but it must terminate before canonical internal inquiry origination.

## Guardrail conclusions

- A permitted external request is not an inquiry need.
- Question-shaped external grammar is not an internal constitutional question.
- Authority/scope binding is not question origination.
- Operator ingress must not mint `BoundedConstitutionalQuestion`.
- No compatibility adapter, legacy peer producer, or dual ingress model should survive.
- Existing tests and public exports that encode the invalid path are deletion targets, not compatibility constraints.

## Complete deletion boundary

### Direct producer to delete

Delete `formulate_bounded_constitutional_question(...)` from `seed_runtime/bounded_constitutional_question.py`.

Current responsibilities compressed into that function:

- consumes `expression`, `interpretation`, `binding`, and `handoff`;
- requires permitted authority/scope binding;
- validates handoff identity against the binding, expression, and interpretation;
- derives focus, constitutional intent, bounded question text, scope status, provenance, uncertainty, unknowns, and caller fields;
- delegates final construction to `produce_bounded_constitutional_question(...)`.

The invalid part is not the preservation of ingress evidence. The invalid part is deriving a canonical `BoundedConstitutionalQuestion` from operator ingress before bounded-goal advancement, inquiry-need establishment, selected inquiry need, and `BoundedInquiryFrontier`.

### Handoff artifact to redirect or rename

`FutureBoundedConstitutionalQuestionHandoff` currently participates in the invalid edge. Its actual lawful responsibility is narrower than its name:

- preserve the permitted authority/scope binding boundary;
- preserve interpreted expression references;
- preserve requested activity class;
- preserve requested, bound/permitted, and excluded scope;
- preserve authority source references;
- preserve operator-stated effect constraints;
- preserve presentation preference;
- preserve source spans, grammar references, provenance, known loss, unknowns, and conflicts;
- remain read-only, no event-ledger write, no cluster mutation.

It does **not** own bounded-question formulation, selected inquiry need, inquiry frontier construction, constitutional question identity, authorization, execution, durable knowledge, or cluster truth.

Smallest lawful replacement name:

```text
FutureAuthorizedConstitutionalIntentHandoff
```

or, if the next implementation slice is deliberately diagnostic rather than intent-establishing:

```text
FutureAdvancementDiagnosisHandoff
```

The replacement should carry the same preserved boundary material but must not mention bounded questions or imply question production.

### Binding projection field to remove or rename

Remove or rename:

```text
OperatorAuthorityScopeBindingProjection.future_bounded_question_handoff
```

Replacement field options:

```text
future_authorized_constitutional_intent_handoff
```

or:

```text
future_advancement_diagnosis_handoff
```

The first is preferable if the next owner establishes authorized constitutional intent / bounded goal. The second is preferable if the next owner only diagnoses advancement. In either case, the field must not be consumed by a bounded-question producer.

### Binding boundary text to update

`operator_authority_scope_binding.py` already contains one correct boundary note saying the artifact does not produce a bounded constitutional question. However, the module still creates `FutureBoundedConstitutionalQuestionHandoff`, so the naming and field contradict the boundary note. Update names and downstream tests so the note is implementation-truth rather than aspirational.

### Minimum lawful advancement explanation to update

`explain_minimum_lawful_advancement(...)` currently describes the attempted movement as advancing from authority/scope binding to bounded constitutional question formulation and includes `formulate_bounded_constitutional_question` in prohibited downstream movement for non-permitted bindings. That wording preserves the obsolete edge. It must be rewritten to the lawful replacement boundary:

```text
advance one interpreted operator request from authority/scope binding to authorized constitutional intent / bounded-goal establishment or advancement diagnosis
```

For permitted bindings, the explanation may say movement can advance only to the replacement owner, not to question formulation.

## Public exports participating in invalid behavior

Remove public exports for deleted/renamed symbols from `seed_runtime/__init__.py`:

- `FutureBoundedConstitutionalQuestionHandoff`;
- `formulate_bounded_constitutional_question`.

Add replacement exports only after the replacement artifact exists. Do not export aliases with the old names.

## Request artifacts and pipeline edges to delete or rewrite

### `ConstitutionalPipelineRequest`

`ConstitutionalPipelineRequest` currently mirrors direct bounded-question producer inputs. That makes the public pipeline able to construct a canonical bounded question from caller-supplied fields, bypassing inquiry frontier establishment. Remove from this request:

- `operator_inquiry` as a bounded-question-originating field;
- `inquiry_provenance` as a bounded-question-originating field;
- `bounded_question`;
- `constitutional_intent`;
- `scope_status`;
- `uncertainty` if it is attached directly to a minted question;
- `unknowns` if it is attached directly to a minted question;
- `bounded_question_id`;
- `caller_supplied_fields`.

The pipeline request should instead receive an already-established `BoundedConstitutionalQuestion` produced by the lawful upstream frontier, or receive a lawful upstream artifact such as `BoundedInquiryFrontier` once that producer owns question origination. The pipeline may still accept capability contracts, registrations, view builders, composition purpose, and output format because those are downstream deterministic projection/composition inputs.

### `invoke_constitutional_pipeline(...)`

Delete the call to `produce_bounded_constitutional_question(...)` inside `invoke_constitutional_pipeline(...)`. The function should not mint a bounded question. It should consume an already-established bounded question and then project/select/compose views.

### Diagnostic and CLI surfaces

Any diagnostic, CLI, JSON formatter, or integration helper that accepts explicit question fields and internally builds `ConstitutionalPipelineRequest` must be rewritten. The current explicit-field diagnostic surface is a direct/manual question-construction path and should be removed or made to require an existing lawful upstream question/frontier artifact.

Because this changes diagnostic surfaces, the diagnostic inventory and shape-audit registries/tests must be updated when implementation begins.

## Does `operator_inquiry` belong in canonical `BoundedConstitutionalQuestion`?

Not as an originating or authority-bearing field.

If preserved at all, `operator_inquiry` should be demoted to provenance/testimony material with a name that cannot be mistaken for internal question ownership, for example:

```text
source_operator_expression_text
operator_expression_testimony
external_request_text
```

Canonical `BoundedConstitutionalQuestion` should prove that an established inquiry frontier selected and bounded an inquiry. It should not prove that an operator asked a question-shaped request. Therefore `operator_inquiry` should not remain a required canonical field in its current name and position. A lawful question may carry external expression provenance, but the question identity and bounded question text must derive from `BoundedInquiryFrontier`, not from the external grammar.

## What remains of `produce_bounded_constitutional_question(...)`

`produce_bounded_constitutional_question(...)` should not remain as a public/manual constructor from explicit caller fields.

Smallest lawful remainder:

- keep an internal helper only if it is renamed and scoped to frontier-owned construction, for example `_produce_bounded_constitutional_question_from_frontier(...)`;
- require `BoundedInquiryFrontier` or an equivalent established frontier-owned input;
- derive identity from frontier references and frontier-owned question material;
- preserve external operator expression only as provenance/testimony if available;
- refuse direct `operator_inquiry`, `bounded_question`, `constitutional_intent`, and `scope_status` kwargs supplied by arbitrary callers.

If no lawful frontier producer exists yet, the first implementation slice should delete the operator-ingress formulation path first and leave frontier-owned production as future work rather than preserving the invalid manual producer.

## Direct/manual question construction elimination

Live production paths to eliminate:

1. `formulate_bounded_constitutional_question(...)` from ingress binding artifacts.
2. `invoke_constitutional_pipeline(...)` constructing a bounded question from `ConstitutionalPipelineRequest` fields.
3. CLI/diagnostic surfaces that accept `operator_inquiry`, `bounded_question`, `constitutional_intent`, and `scope_status` and produce the pipeline result.
4. Test fixtures that call `produce_bounded_constitutional_question(...)` as if any caller may create canonical questions.
5. Public exports that allow downstream code to preserve the old edge.

Permitted test-only construction, if needed after deletion, should use a clearly named fixture helper that creates an already-established frontier-owned question artifact or a minimal fake with explicit test provenance. It must not be a production export.

## Downstream consumers and what they currently assume

Downstream consumers currently treat `BoundedConstitutionalQuestion` as proof that these fields are already available and bounded:

- `project_constitutional_question(...)` assumes `bounded_question`, `constitutional_intent`, `scope_status`, `uncertainty`, `unknowns`, read-only flags, and caller-supplied fields exist and may be deterministically projected into selection keys.
- `project_constitutional_capabilities(...)` is adjacent and does not need operator ingress; it projects registered capability evidence.
- `select_constitutional_views(...)` assumes question projection keys are legitimate selection keys from an already-bounded question, not arbitrary external grammar.
- `selected_constitutional_views_to_composition_request(...)` assumes selected views came from a lawful question/capability selection boundary.
- `build_constitutional_view_composition(...)` assumes selected views are legitimate inputs to composition.
- `explain_constitutional_pipeline_provenance(...)` reports operator inquiry testimony and bounded-question identity as already completed pipeline artifacts.
- pipeline JSON and human renderers assume a bounded question exists before projection and selection.

After deletion, those consumers should assume a bounded question proves an established inquiry frontier, not operator ingress permission.

## Tests to delete or rewrite

### Delete or completely rewrite

- `tests/test_bounded_constitutional_question_formulation.py`: this file exists to prove the invalid ingress-binding-to-question formulation path.
- Any assertions in `tests/test_operator_authority_scope_binding.py` that require `future_bounded_question_handoff` on permitted bindings.
- Any assertions in `tests/test_operator_authority_scope_binding.py` that preserve `formulate_bounded_constitutional_question` as a valid permitted downstream movement.
- Public surface tests asserting `formulate_bounded_constitutional_question` or `FutureBoundedConstitutionalQuestionHandoff` exports.

### Rewrite to consume lawful upstream artifact

- `tests/test_constitutional_pipeline.py`: rewrite request fixtures to pass an already-established bounded question or frontier-owned question, not direct fields.
- `tests/test_constitutional_pipeline_public_surface.py`: remove public direct producer/export expectations; assert no legacy formulation export exists.
- `tests/test_constitutional_pipeline_provenance_explanation.py`: rewrite to preserve external expression as provenance/testimony from a lawful question, not `operator_inquiry` request fields.
- `tests/test_constitutional_pipeline_diagnostic.py`: rewrite diagnostic request shape and update diagnostic inventory / shape audit tests if a CLI/diagnostic surface remains.
- `tests/test_constitutional_pipeline_integration_wiring.py`: rewrite integration wiring so pipeline invocation receives lawful bounded-question input.
- `tests/test_constitutional_question_projection.py`: rewrite fixture construction to use frontier-owned test artifact or a non-production fixture builder.
- `tests/test_constitutional_capability_projection.py`, `tests/test_examination_method_applicability.py`, `tests/test_examination_policy_projection.py`, `tests/test_examination_frontier.py`, and `tests/test_candidate_examination_work.py`: replace direct calls to `produce_bounded_constitutional_question(...)` with lawful test fixtures.

### Add new tests

- Permitted operator authority/scope binding does not expose a future bounded-question handoff.
- Permitted operator authority/scope binding exposes only the replacement authorized-intent/advancement-diagnosis handoff, if implemented.
- Importing `formulate_bounded_constitutional_question` from package public surface fails or is absent.
- `invoke_constitutional_pipeline(...)` does not call `produce_bounded_constitutional_question(...)`.
- Pipeline request cannot be constructed from raw `operator_inquiry` / `bounded_question` / `constitutional_intent` / `scope_status` fields.
- Only frontier-owned construction can produce canonical `BoundedConstitutionalQuestion` once implemented.
- Diagnostic inventory and diagnostic shape audit reflect any changed diagnostic/CLI surface.

## Destructive implementation sequence

1. Delete `formulate_bounded_constitutional_question(...)` and its validation/formulation helpers from `seed_runtime/bounded_constitutional_question.py`.
2. Rename or replace `FutureBoundedConstitutionalQuestionHandoff` with a non-question-originating handoff, or remove the handoff entirely if no immediate replacement owner exists.
3. Rename/remove `OperatorAuthorityScopeBindingProjection.future_bounded_question_handoff`.
4. Update `bind_operator_authority_scope(...)` so permitted bindings do not create bounded-question handoffs.
5. Rewrite `explain_minimum_lawful_advancement(...)` text and prohibited movement names to remove bounded-question formulation as a normal next step.
6. Remove old public exports from `seed_runtime/__init__.py` with no compatibility aliases.
7. Change `ConstitutionalPipelineRequest` to accept an already-established bounded question or frontier-owned artifact instead of raw direct question fields.
8. Remove `produce_bounded_constitutional_question(...)` from live pipeline invocation; make pipeline consume an already-established question.
9. Restrict or rename `produce_bounded_constitutional_question(...)` to frontier-owned internal construction, or delete it until frontier ownership is implemented.
10. Rewrite CLI/diagnostic surfaces and update diagnostic inventory / shape audit coverage.
11. Delete invalid formulation tests.
12. Rewrite downstream pipeline/projection tests with lawful fixtures.
13. Add negative tests proving operator ingress cannot mint `BoundedConstitutionalQuestion`.
14. Run targeted diagnostic tests required by repository instructions if any diagnostic surface changes:

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

15. Run the relevant pipeline, authority binding, question projection, and diagnostic test suites.

## Smallest first implementation slice

The smallest safe first slice is destructive and narrow:

1. Remove `formulate_bounded_constitutional_question(...)` from implementation and public exports.
2. Delete `tests/test_bounded_constitutional_question_formulation.py`.
3. Rename `FutureBoundedConstitutionalQuestionHandoff` / `future_bounded_question_handoff` to a non-question handoff, or remove it if replacement naming would over-claim ownership.
4. Update `tests/test_operator_authority_scope_binding.py` to assert that operator ingress does not produce a bounded-question handoff.
5. Update minimum lawful advancement explanation wording so it no longer normalizes question formulation as downstream ingress movement.

This first slice should not attempt full frontier-owned question construction. It should remove the invalid producer before adding a lawful one.

## Exact next bounded question

Given one permitted `OperatorAuthorityScopeBindingProjection` for one interpreted operator expression, what is the smallest read-only replacement artifact that preserves authority/scope-bound constitutional intent, requested movement class, permitted/excluded/unresolved scope, provenance, uncertainty, Unknowns, operator-stated constraints, and presentation preference for advancement diagnosis or bounded-goal establishment, without formulating a `BoundedConstitutionalQuestion`, selecting an inquiry need, assembling a `BoundedInquiryFrontier`, selecting capabilities or views, authorizing movement, executing tools, writing the event ledger, or mutating cluster state?

Operator-ingress question origination deletion audit complete.
