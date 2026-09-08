# Bounded-ask constitutional-pipeline ingress cleanup 001

## Bounded implementation result

PR 1611 created a bounded-ask adapter that classified the implementation `QuestionFamily` named `constitutional pipeline` as `eligible_with_parameters`. It accepted six raw operator-provided fields, selected the `constitutional_pipeline` dispatch surface, and mutated the CLI namespace with `constitutional_pipeline=True` plus the raw payload.

PR 1734 removed raw constitutional-question origination from the consumer. `ConstitutionalPipelineRequest` now requires an already-formed `BoundedConstitutionalQuestion`, while both direct CLI flags unconditionally refuse raw question fields. The surviving pre-change topology therefore advertised a permitted producer/dispatch road whose only produced representation was categorically refused by its selected consumer.

This change removes that stale producer road. It removes `constitutional pipeline` from `BOUNDED_ASK_DISPATCH_SURFACES`, `BOUNDED_ASK_REQUIRED_SURFACE_ARGS`, the QuestionFamily inventory and examples, and the selected-value six-field special adapter. Disposition A was selected because the row's declared responsibility, examples, surface, notes, and relationship existed solely to advertise the deleted dispatch entrance; no independent active inventory responsibility warranted preserving it.

No replacement entrance, question interpretation, semantic routing, selection-key inference, automatic admission, inquiry-admission implementation, JSON reconstruction, or API object injection through the CLI was added.

## Verification changes

`tests/test_question_surface_inventory.py` now proves the family is absent from inventory and JSON, exact lookup and bounded-work eligibility reject it, both dispatch maps omit it, bounded ask cannot mutate `constitutional_pipeline`, and selected-value, selected-surface, and selection helpers reject a non-permitted representation. Existing tests continue to cover unrelated immediate, parameterized, diagnostic-only, and non-dispatchable roads and inventory consistency.

No tests protecting the old adapter remained in the merged test suite, so none were deleted. The focused constitutional-pipeline tests continue to prove that raw `ConstitutionalPipelineRequest` fields are rejected, direct raw CLI ingress refuses, and API invocation succeeds with a supplied `BoundedConstitutionalQuestion`.

The active operator guide `constitutional_pipeline_operations.md` was corrected. Earlier numbered implementation and campaign reports are intentionally preserved as historical testimony about their former implementation state, not as current operator guidance or constitutional authority.

The typed question producer, typed request/result, projections, view selection and composition, pipeline invocation, diagnostic, provenance explanation, and JSON/human renderers are unchanged. Direct CLI refusal is unchanged. API behavior is unchanged. How a responsible question-formation occurrence will eventually establish a `BoundedConstitutionalQuestion` remains Unknown and was not decided here.

## Active Book constraints

| Recovered claim | Exact active Book path and clause | Scope supported | What is not inferred |
| --------------- | --------------------------------- | --------------- | -------------------- |
| Operator question-shaped material is not an internal bounded question; question formation remains Seed-owned. | `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`, **04.Question.B — Inquiry origination requires bounded translation** and **04.Question.E — Normal internal questioning is Seed-owned** | Raw operator fields cannot stand in for a responsibly formed internal question. | No missing question-forming implementation or automatic translation is invented. |
| Implementation `QuestionFamily` is not constitutional question taxonomy. | `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`, **04.Question.C — Question relations are local and non-collapsing** | Removing an implementation inventory/dispatch row does not amend constitutional taxonomy. | Inventory membership does not establish constitutional applicability or standing. |
| Question surface is not inquiry standing. | `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`, **Important distinctions** | Public presentation and compatibility dispatch cannot establish inquiry standing. | CLI reachability does not admit an inquiry. |
| Compatibility routing is not constitutional applicability. | `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`, **04.Question.C** and **04.Question.E** | An `ask` map may witness bounded implementation routing only. | A dispatch label does not establish goal applicability or question formation. |
| Constructibility is not responsible production occurrence. | `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md`, opening clause and **Important distinctions** | A mechanically constructible question-shaped object does not prove its responsible producer occurred. | Consumer-local type satisfaction does not establish producer standing. |
| Consumer-local uptake must match producer standing. | `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`, opening uptake clause and **Material applicable to a consumer...** | Producer warrant, preserved representation, applicability, admission, and consumer use remain distinct at the crossing. | Mechanical compatibility or call adjacency does not establish a constitutional road. |
| Absence of a lawful entrance does not authorize inventing one. | `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`, **04.Question.E** | The incomplete executable dialogue loop preserves Seed ownership and permits lawful stopping. | Missing realization does not transfer origination to the operator or warrant a shortcut. |

PR history above is implementation testimony only. The cited active Book clauses constrain this cleanup; reports, tests, implementation names, and PR descriptions are not used as Book authority.
