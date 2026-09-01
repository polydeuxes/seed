# Constitutional Inquiry Origination Boundary Audit 001

## Question

Where does constitutional inquiry actually originate, and does the current operator-expression-to-`BoundedConstitutionalQuestion` path prematurely create an internal inquiry artifact before Seed has established inquiry need?

## Evidence reviewed

This audit reviewed implementation evidence rather than artifact names as authority:

- `seed_runtime/operator_expression_interpretation.py`
- `seed_runtime/operator_authority_scope_binding.py`
- `seed_runtime/bounded_constitutional_question.py`
- `seed_runtime/constitutional_pipeline.py`
- `seed_runtime/inquiry_need_projection.py`
- `seed_runtime/goal_advancement_need_set.py`
- `seed_runtime/bounded_inquiry_frontier.py`
- `bounded_inquiry_frontier_audit_001.md`
- `frontier_question_formulation_testimony_audit_001.md`
- `free_form_operator_interface_dynamic_view_topology_audit_001.md`

Repository authority wins over the names of the artifacts.

## Finding 1: what the current operator-ingress path actually owns

The current operator-ingress path owns a narrow external-expression handling road:

```text
AttributedOperatorExpression
→ OperatorExpressionInterpretationProjection
→ OperatorAuthorityScopeBindingProjection
→ FutureBoundedConstitutionalQuestionHandoff
→ formulate_bounded_constitutional_question(...)
→ BoundedConstitutionalQuestion
```

Its lawful responsibilities are:

1. preserve exact operator expression and attribution;
2. interpret one attributed expression under one recovered grammar;
3. preserve request kind, focus expressions, scope expressions, authority-bearing expressions, presentation preference, unresolved language, known loss, Unknowns, and conflicts;
4. bind authority and scope for the interpreted request;
5. when the binding is `permitted`, carry a future handoff that allows formulation of one bounded question;
6. formulate one deterministic question from explicit interpreted/bound ingress fields;
7. preserve read-only, non-ledger-writing, non-mutating boundaries.

The operator-ingress path does **not** own:

- goal establishment;
- bounded advancement horizon formation;
- advancement need diagnosis;
- inquiry need establishment;
- inquiry frontier assembly;
- source or observation selection;
- inquiry execution;
- result knowledge;
- repository truth creation.

The strongest implementation evidence is negative: operator interpretation explicitly states that it does not produce a bounded constitutional question, select a question family, authorize, schedule, emit, or execute. Authority/scope binding only creates a future bounded-question handoff when permitted. Bounded question formulation then consumes that handoff and preserves the resulting artifact as read-only testimony.

## Finding 2: where external grammar first becomes an internal inquiry artifact

The first conversion from external operator expression into the artifact named `BoundedConstitutionalQuestion` occurs in `formulate_bounded_constitutional_question(...)` in `seed_runtime/bounded_constitutional_question.py`.

That function consumes:

- the attributed external expression;
- the interpretation projection;
- the authority/scope binding;
- the future bounded-question handoff;
- optional formulation unknowns.

It then constructs:

- `operator_inquiry` from `expression.exact_text`;
- `bounded_question` from request kind, activity class, focus, scope, and constraints;
- `constitutional_intent` from request kind and activity class;
- `scope_status` from permitted/requested/excluded/unresolved scope;
- uncertainty and Unknowns from expression, interpretation, binding, and handoff material.

Therefore the first implemented conversion is not raw prose directly to question. It is:

```text
external grammar
→ attributed expression
→ recovered-grammar interpretation
→ authority/scope binding
→ permitted future handoff
→ BoundedConstitutionalQuestion
```

However, that is still an ingress road, not an advancement road.

## Finding 3: whether the conversion bypasses goal advancement and inquiry-need establishment

Yes. The existing operator-ingress formulation bypasses goal advancement and inquiry-need establishment as now recovered.

The bypass is not hidden in the code; it is structural:

- `formulate_bounded_constitutional_question(...)` has no input for `BoundedOperatorGoalEstablishment`, `BoundedAdvancementHorizon`, `GoalAdvancementNeedSet`, `InquiryNeedProjection`, `AdvancementNeedConsiderationSelection`, `InquiryFrontierBoundaryTestimony`, or `BoundedInquiryFrontier`.
- `ConstitutionalPipelineRequest` mirrors the explicit bounded-question fields and invokes `produce_bounded_constitutional_question(...)` directly before view projection, capability projection, selection, and composition.
- `InquiryNeedProjection` explicitly says an established inquiry need is not inquiry opened, question selected, observation authorized, action selected, sufficiency judged, execution, recording, ledger writing, or mutation.
- `GoalAdvancementNeedSet` explicitly preserves need projections without selecting route, next action, sufficiency, inquiry, authority, realization, execution, recording, ledger writing, or mutation.
- `BoundedInquiryFrontier` explicitly consumes one exact selected inquiry need plus boundary testimony and does not formulate a question, open inquiry, select sources or observations, authorize, execute, record, write the event ledger, or mutate state.

The operator-ingress path therefore predates or sits beside the recovered goal-advancement/inquiry-frontier road. It can lawfully preserve an ingress-formulated question-shaped artifact for compatibility, but it does not prove that Seed established an inquiry need.

## Finding 4: source-neutral constitutional responsibility of `BoundedConstitutionalQuestion`

Source-neutral responsibility should be smaller and later than the current module docstring suggests.

`BoundedConstitutionalQuestion` should own:

> One immutable, read-only, provenance-preserving internal constitutional question artifact whose question text, constitutional intent, scope status, uncertainty, Unknowns, ingress/provenance fields, and caller/stage-supplied fields have already been lawfully formulated by an upstream producer boundary.

It should not own:

- external grammar interpretation;
- authority establishment;
- scope permission;
- goal establishment;
- advancement sufficiency;
- inquiry need establishment;
- frontier assembly;
- question formulation from a frontier;
- source selection;
- observation authorization;
- inquiry opening or execution;
- repository truth creation.

In other words, `produce_bounded_constitutional_question(...)` is best understood as a deterministic artifact constructor/preserver, not the constitutional origin of inquiry.

## Finding 5: whether the existing question artifact combines external-ingress and inquiry ownership

Yes, in naming and module-level ownership language.

The dataclass itself is mostly neutral: it preserves strings, provenance, uncertainty, Unknowns, caller fields, and read-only boundaries. But the module docstring says it owns the `Operator Inquiry -> BoundedConstitutionalQuestion` boundary, and `formulate_bounded_constitutional_question(...)` performs ingress-derived formulation from operator expression / interpretation / binding.

That combines two responsibilities:

1. **artifact preservation**: a bounded internal question record;
2. **operator-ingress formulation**: converting one permitted interpreted external expression into that record.

The combination was lawful for the older pipeline because the artifact carefully refused authority, truth, capability discovery, view selection, event-ledger writes, and mutation. But after recovery of `BoundedInquiryFrontier`, the same combination is constitutionally misleading if treated as normal inquiry origination.

## Finding 6: which responsibilities should terminate at translated intent or bounded-goal establishment

External ingress should normally terminate before internal inquiry origination unless inquiry need is established.

The following responsibilities should terminate at translated intent, bounded request, or bounded goal establishment:

- exact external expression preservation;
- recovered-grammar interpretation;
- authority-bearing language preservation;
- requested scope preservation;
- requested activity classification;
- presentation preference preservation;
- unresolved language / unsupported residual preservation;
- operator-stated effect constraints;
- constitutional intent candidate;
- bounded goal candidate or established bounded goal, where the goal-establishment road applies;
- authority/scope binding sufficient to say what is permitted to consider, not sufficient to open inquiry.

They should not, by themselves, produce a normal internal constitutional question.

A lawful normal road is:

```text
external grammar
→ translation / interpretation
→ authority and scope preservation or binding
→ constitutional intent or bounded goal
→ bounded advancement horizon
→ advancement need projections
→ inquiry need establishment
→ selected inquiry need
→ frontier-boundary testimony
→ BoundedInquiryFrontier
→ frontier-question formulation testimony
→ BoundedConstitutionalQuestion
```

## Finding 7: whether `BoundedInquiryFrontier` should be the sole normal producer boundary

Yes, for normal internal constitutional questions that represent opened inquiry pressure after advancement diagnosis.

`BoundedInquiryFrontier` should be the sole normal producer boundary for internal constitutional questions because it is the recovered boundary that requires:

- one exact selected inquiry need;
- matching native inquiry item lineage;
- bounded uncertainty component;
- repository/world subject;
- selected goal;
- bounded advancement horizon;
- included/excluded inquiry scope;
- eligible/ineligible evidence territory;
- sufficient-resolution conditions;
- lawful-stopping conditions;
- explicit refusal on missing required families or material binding conflict.

But this does not mean `BoundedInquiryFrontier` should be the only compatibility source of a `BoundedConstitutionalQuestion` forever. The repository already has compatibility surfaces and tests that directly construct `BoundedConstitutionalQuestion` or invoke the constitutional pipeline from explicit fields. Those may remain as legacy/direct/manual/compatibility roads if they are named and bounded as not proving inquiry need.

Recommended ownership distinction:

| Producer road | Status | Meaning |
| --- | --- | --- |
| `BoundedInquiryFrontier` plus future frontier-question testimony | normal constitutional inquiry origination | inquiry need has been established and bounded into a frontier before question formulation |
| operator expression / interpretation / authority-scope binding formulation | compatibility / ingress-formulated bounded question | preserves a permitted interpreted request as a bounded question artifact, but does not prove advancement diagnosis or inquiry need |
| direct `produce_bounded_constitutional_question(...)` | manual/test/explicit artifact construction | constructs/preserves fields only; no origination claim |
| `ConstitutionalPipelineRequest` | compatibility pipeline invocation | invokes existing view pipeline from explicit fields; no goal-advancement or inquiry-need proof |

## Finding 8: smallest decomposition or redirection required

The smallest decomposition is documentation and naming-boundary correction first, then one small implementation redirection only if executable normal origination is needed.

### Smallest conceptual decomposition

1. Treat `BoundedConstitutionalQuestion` as the neutral internal question artifact.
2. Treat `produce_bounded_constitutional_question(...)` as an explicit-field constructor.
3. Treat `formulate_bounded_constitutional_question(...)` as `operator_ingress_formulate_bounded_constitutional_question` in constitutional responsibility, even if the public function name remains for compatibility.
4. Treat `ConstitutionalPipelineRequest` as compatibility/direct invocation, not proof of inquiry origination.
5. Treat `BoundedInquiryFrontier` as the normal upstream origin boundary once inquiry need has been established.
6. Require a future frontier-question formulation owner to map established frontier clauses into `BoundedConstitutionalQuestion` without opening inquiry or selecting evidence.

### Smallest implementation redirection if warranted

If implementation is pursued, the smallest slice should not replace the pipeline. It should add a new producer adjacent to existing code:

```text
Established BoundedInquiryFrontier
+ explicit FrontierQuestionFormulationTestimony
→ produce_bounded_constitutional_question(...)
→ BoundedConstitutionalQuestion
```

That slice should:

- refuse non-`established` frontiers;
- preserve frontier id, selected need reference, native projection id, horizon id, testimony id, uncertainty component, repository/world subject, operative clauses, missing/conflict refs, and lineage;
- distinguish `question_ingress_source=frontier` from `question_ingress_source=operator_ingress` or `explicit_fields`;
- delegate artifact construction to `produce_bounded_constitutional_question(...)`;
- not select sources, observations, capabilities, views, or execution;
- remain read-only, non-recording, non-ledger-writing, and non-mutating.

This matches the existing `frontier_question_formulation_testimony_audit_001.md` conclusion that no implemented owner currently expresses one established `BoundedInquiryFrontier` as one structurally equivalent `BoundedConstitutionalQuestion`, and that a small ingress-provenance extension is warranted before frontier-derived questions become executable.

## Finding 9: compatibility consequences

Compatibility consequences are real but manageable.

Do not remove or break:

- direct tests using `produce_bounded_constitutional_question(...)`;
- existing `ConstitutionalPipelineRequest` callers;
- current view selection and composition tests;
- existing operator-ingress formulation tests;
- public exports of `BoundedConstitutionalQuestion`.

Instead:

1. Reclassify direct construction as explicit-field/manual/compatibility construction.
2. Reclassify operator-ingress formulation as permitted-ingress formulation, not inquiry-need origination.
3. Add provenance fields or caller-supplied fields that make ingress source explicit.
4. Add frontier-derived formulation as the normal constitutional inquiry-origin road.
5. Keep existing artifacts read-only and non-mutating.

The compatibility danger is semantic, not primarily mechanical: downstream code may treat any `BoundedConstitutionalQuestion` as evidence that inquiry need was established. That should be corrected by provenance/source fields and tests once implementation occurs.

## Finding 10: whether implementation is warranted

Implementation is warranted only as a small follow-up slice, not inside this audit.

Warrant exists because:

- `BoundedInquiryFrontier` is implemented;
- `BoundedConstitutionalQuestion` is implemented;
- current source evidence shows no implemented bridge from established frontier to bounded question;
- current operator-ingress formulation can be mistaken for normal inquiry origination;
- `frontier_question_formulation_testimony_audit_001.md` already identifies the missing bridge and exact next shape.

Implementation should be limited to the bridge/provenance correction described above. It should not redesign external grammar, remove compatibility surfaces, replace the pipeline, or make `BoundedInquiryFrontier` execute inquiry.

## Recovered lawful relationship

The recovered lawful relationship is:

```text
external grammar
  owns expression form only; question-shaped grammar is not internal inquiry

translation / interpretation
  preserves bounded meaning candidates, focus/scope/activity/presentation/uncertainty;
  does not produce inquiry need

authority and scope
  binds what may be considered or preserved;
  authorized/permitted request is not inquiry opened

constitutional intent
  may express what the operator seeks constitutionally;
  intent is not inquiry need

bounded goal
  establishes the current bounded objective where the goal road applies;
  goal is not a question

advancement diagnosis
  evaluates needs against a horizon;
  coexisting needs are not priority or route

inquiry need
  arises only from explicit component-bounded repository/world uncertainty testimony
  material to the current horizon;
  need established is not question selected or inquiry opened

BoundedInquiryFrontier
  establishes the bounded frontier for one selected inquiry need using boundary testimony;
  normal producer boundary before internal question formulation

BoundedConstitutionalQuestion
  preserves one already-lawfully-formulated internal constitutional question;
  source-neutral artifact, not external-ingress owner and not inquiry-need establisher
```

## Determination

The existing operator-expression-to-`BoundedConstitutionalQuestion` path does prematurely create an internal question artifact **if** it is interpreted as normal constitutional inquiry origination. It does **not** itself claim to establish truth, authority, execution, ledger writes, mutation, or result knowledge, and it preserves useful interpretation, authority, scope, provenance, and uncertainty responsibilities. The defect is an origination-boundary compression: permitted external ingress currently can become the canonical internal question artifact without passing through goal advancement, inquiry-need establishment, selected inquiry need, and `BoundedInquiryFrontier`.

The lawful recovery is not to delete the current path. The lawful recovery is to demote it to compatibility / ingress-formulated bounded-question construction and make established `BoundedInquiryFrontier` plus explicit frontier-question formulation testimony the normal producer road for internal constitutional questions.

## Exact next bounded question

What is the minimal read-only frontier-question formulation implementation that consumes one `frontier_state="established"` `BoundedInquiryFrontier` plus explicit stage-owned formulation testimony, maps every operative frontier clause exactly once into existing `BoundedConstitutionalQuestion` fields, preserves frontier and selected-need lineage as distinct ingress provenance, refuses non-established, incomplete, ambiguous, conflicting, or nonequivalent formulations, delegates to `produce_bounded_constitutional_question(...)`, and leaves all existing operator-ingress and direct constitutional-pipeline compatibility surfaces intact without opening inquiry, selecting evidence, authorizing observation, executing, recording, writing the event ledger, or mutating state?

Constitutional inquiry origination boundary audit complete.
