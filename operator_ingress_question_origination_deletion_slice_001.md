# Operator Ingress Question Origination Deletion Slice 001

Repository authority wins. This slice deletes the operator-ingress authority/scope-binding-to-question-origination boundary.

## Deleted boundary

The operator-ingress path now stops at `OperatorAuthorityScopeBindingProjection`. A permitted authority/scope binding proves only that interpreted external material may be considered under the preserved authority and scope. It does not create, hand off, formulate, or imply a `BoundedConstitutionalQuestion`.

Deleted runtime surfaces:

- `FutureBoundedConstitutionalQuestionHandoff`
- `OperatorAuthorityScopeBindingProjection.future_bounded_question_handoff`
- `formulate_bounded_constitutional_question(...)`
- validation and formulation helpers used only by the ingress-binding-to-question path
- package-root exports for the deleted symbols

No compatibility aliases or replacement handoff artifacts were added.

## Preserved owners

`OperatorAuthorityScopeBindingProjection` continues to preserve authority/scope-binding material inside its existing owner:

- attributed expression reference and interpretation reference
- operator identity, workspace, and session authority testimony
- requested activity class
- requested, resolved, permitted, excluded, and unresolved scope
- authority-bearing expressions and authority source references
- operator-stated effect constraints
- presentation preference
- provenance
- Unknowns and conflicts
- read-only, no-event-ledger-write, and no-cluster-mutation flags

`BoundedConstitutionalQuestion` remains available only through explicit bounded-question production inputs. This slice does not repair `ConstitutionalPipelineRequest`, redesign the constitutional pipeline, or modify frontier-owned question construction.

## Minimum-lawful advancement wording

`MinimumLawfulAdvancementExplanation` no longer identifies bounded-question formulation as the next operator-ingress movement. For permitted bindings, its transition states that the permitted binding stops at authority/scope preservation in operator ingress. It continues to prohibit question origination, downstream selection, and authorization/execution.

## Tests

Focused tests prove that permitted and non-permitted bindings have no bounded-question handoff, that operator-ingress public surfaces cannot produce `BoundedConstitutionalQuestion`, that deleted symbols are absent from the package runtime surface, that preserved authority/scope/provenance/uncertainty/read-only fields remain intact, and that minimum-lawful advancement output no longer names bounded-question formulation as the next operator-ingress movement.
