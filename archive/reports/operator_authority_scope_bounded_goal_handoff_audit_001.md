# Operator authority/scope bounded goal handoff audit 001

Repository authority wins. This audit determines whether the existing `BoundedOperatorGoalEstablishment` owner can lawfully consume one permitted `OperatorAuthorityScopeBindingProjection` and its matching interpretation/expression material, and recovers only the smallest missing boundary proven necessary by implementation evidence.

## Current owner requirements

`BoundedOperatorGoalEstablishment` is the read-only owner for bounded operator goal establishment from lawful ingress evidence. Its artifact requires an ingress artifact type/ref, ingress lineage, establishment state/reason, intended outcome, outcome resolution, known and unresolved scope, sufficiency and stop conditions, operator acceptance provenance, constraints, Unknowns, ambiguities, conflicts, known loss, correction lineage, upstream refs, non-authority flags, read-only flags, and boundary notes.

Before this audit, implemented ingress roads were:

1. `ClosedChoiceSelectionBinding` via `establish_bounded_operator_goal_from_closed_choice(...)`.
2. `OperatorExpressionInterpretationProjection` via `establish_bounded_operator_goal_from_interpretation(...)`.
3. `DownstreamInterpretationAdmission` via `establish_bounded_operator_goal_from_admitted_interpretation(...)`.

The owner already refuses unsupported orientation, preserves unknown/conflicting material, and declares that goal establishment is not inquiry opening, resource observation, constraint satisfaction, work authorization, execution, recording, or satisfaction judging.

## Existing inputs in expression, interpretation, and authority/scope binding

### `AttributedOperatorExpression`

Already exists:

- exact external text;
- normalized text;
- input representation;
- source channel;
- workspace/session/operator references;
- provenance;
- received scope context;
- uncertainty and Unknowns;
- read-only, non-ledger, non-mutating boundary flags.

### `OperatorExpressionInterpretationProjection`

Already exists:

- matching attributed expression ref;
- interpretation state and reason;
- expression form and inquiry/request kind;
- focus, subject, object, and scope expressions;
- requested movement class;
- authority-bearing expressions;
- operator-stated effect constraints;
- evidence, limitation, and presentation preferences;
- source spans;
- alternatives;
- unresolved lexical/reference material;
- unsupported residual spans;
- known loss;
- supporting refs, provenance, Unknowns, conflicts;
- read-only, non-ledger, non-mutating boundary flags;
- a future authority/scope-binding handoff only for the authority/scope stage.

### `OperatorAuthorityScopeBindingProjection`

Already exists:

- matching interpretation and attributed expression refs;
- operator, workspace, and session identity;
- inquiry/request kind;
- requested activity class;
- requested scope expressions;
- resolved, permitted, excluded, and unresolved scope;
- authority-bearing expressions;
- authority source refs;
- required authority class;
- operator-stated effect constraints;
- presentation preference;
- binding state and reason;
- required additional authority;
- supporting refs, provenance, Unknowns, conflicts;
- boundary notes saying authority-bearing language is not itself authority, requested scope is not automatically permitted scope, permission to request movement is distinct from concrete-realization authorization, and the projection does not produce a bounded constitutional question.

## Can one permitted binding establish one bounded goal directly?

Yes, but only inside `BoundedOperatorGoalEstablishment`, and only when the exact binding, interpretation, and expression identities match.

The lawful connection is:

```text
AttributedOperatorExpression
→ OperatorExpressionInterpretationProjection
→ OperatorAuthorityScopeBindingProjection(binding_state="permitted")
→ BoundedOperatorGoalEstablishment
```

This is not automatic goal establishment by the authority/scope projection. The projection remains only preserved ingress authority/scope evidence. The goal owner must consume it explicitly and produce a separate bounded-goal artifact with its own state/reason and non-authority flags.

## Evidence distinguishing a goal from other material

A bounded goal is distinguished by these goal-owned fields:

- `goal_establishment_id`;
- `establishment_state` and `establishment_reason`;
- `intended_outcome`;
- `outcome_resolution`;
- `known_scope` and `unresolved_scope` as goal boundary material;
- `sufficiency_conditions` and `sufficiency_state`;
- `stop_conditions`;
- `operator_acceptance_provenance`;
- `correction_of_goal_ref` and correction lineage;
- read-only and no-effect flags.

The following remain non-goal evidence unless consumed and bounded by the goal owner:

- external expression text is testimony, not a bounded goal;
- interpretation focus/request/activity is interpreted meaning, not a bounded goal;
- requested activity class is a requested movement category, not intended outcome by itself;
- presentation preference is output-shape preference, not goal substance;
- requested/resolved/permitted/excluded/unresolved scope is scope testimony, not automatic goal establishment;
- authority source refs prove ingress permission only, not work authorization or execution authority.

## Refusal and preservation rules

The recovered implementation refuses or preserves material as follows:

- mismatched binding/interpretation/expression identities raise a boundary error;
- non-`permitted` bindings produce a refused goal with preserved unresolved/unknown/conflict material;
- non-interpreted matching interpretation produces a refused goal;
- conflicting interpretation or binding material produces a refused goal;
- unresolved scope on a permitted binding produces a refused goal;
- a scoped request with no permitted scope produces a refused goal;
- no supportable goal orientation produces a refused goal;
- mixed permitted/excluded material is not silently widened: permitted material may remain provisional while excluded material is preserved in unresolved goal scope;
- Unknowns prevent fully established state but may allow provisional orientation when permitted bounded material exists;
- exact expression, interpretation, authority, permitted/excluded/unresolved scope, requested activity, effect constraints, presentation preference, provenance, known loss, Unknowns, and conflicts are preserved in `consumed_ingress_material_snapshot` and goal-owned fields.

## Missing testimony or projection owner

No future handoff artifact is required.

Repository evidence already contains the needed upstream testimony in the three existing artifacts. The missing boundary was not a new projection owner between authority/scope binding and goal establishment. The missing boundary was one explicit goal-owner intake function that verifies identity, consumes one permitted authority/scope binding with matching expression/interpretation material, and emits one `BoundedOperatorGoalEstablishment` without reinterpreting, authorizing, diagnosing advancement, formulating a question, recording, writing the event ledger, or mutating state.

## Implementation slice warranted

Yes. One implementation slice was warranted because repository evidence showed:

- `BoundedOperatorGoalEstablishment` already owned bounded-goal establishment;
- `OperatorAuthorityScopeBindingProjection` already preserved ingress permission/scope evidence;
- the invalid direct operator-ingress-to-`BoundedConstitutionalQuestion` path had been deleted;
- the intended next road requires permitted interpreted external material to enter bounded goal establishment;
- no existing function consumed one permitted authority/scope binding plus its matching expression/interpretation material.

## Smallest lawful connection recovered

Recovered connection:

```text
establish_bounded_operator_goal_from_authority_scope_binding(
    binding: OperatorAuthorityScopeBindingProjection,
    interpretation: OperatorExpressionInterpretationProjection,
    expression: AttributedOperatorExpression,
    *,
    sufficiency_conditions=(),
    stop_conditions=(),
    correction_of_goal_ref="",
) -> BoundedOperatorGoalEstablishment
```

The connection:

- requires exact binding/interpretation/expression identity matching;
- requires `binding_state="permitted"` for non-refused establishment;
- uses permitted scope and interpreted focus/subject/object as goal orientation;
- preserves excluded/unresolved material rather than broadening scope;
- preserves constraints and presentation preference without enforcing or satisfying them;
- preserves exact source material in a snapshot;
- keeps `inquiry_opened=false`, `resources_observed=false`, `constraints_enforced=false`, `work_authorized=false`, `execution_started=false`, `recording_started=false`, `satisfaction_judged=false`, `writes_event_ledger=false`, and `mutates_cluster=false`.

## Exact next bounded question

What is the minimal read-only advancement diagnosis owner that consumes one matching `BoundedOperatorGoalEstablishment` established or provisionally established from permitted authority/scope-bound operator ingress, preserves goal identity, intended outcome, known scope, unresolved/excluded scope, sufficiency and stop conditions, constraints, Unknowns, conflicts, known loss, and ingress lineage, and determines only whether clarification, inquiry, authority, or operational-realization advancement need testimony is required without formulating a constitutional question, selecting inquiry, authorizing execution, recording, writing the event ledger, or mutating state?

Authority/scope binding to bounded goal audit complete.
