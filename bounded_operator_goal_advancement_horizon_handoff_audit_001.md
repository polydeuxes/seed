# Bounded Operator Goal Advancement Horizon Handoff Audit 001

## Question

Determine how one `BoundedOperatorGoalEstablishment` lawfully becomes the exact selected goal consumed by `BoundedAdvancementHorizon`:

```text
BoundedOperatorGoalEstablishment
→ exact selected goal
→ BoundedAdvancementHorizon
```

Repository authority wins. This audit does not formulate a constitutional question, open inquiry, authorize execution, record, write the event ledger, or mutate state.

## Guardrails preserved

```text
goal established
!= goal selected for present advancement

goal orientation
!= active inquiry

provisional goal
!= selectable goal automatically

goal selection
!= advancement diagnosis
!= need selection
```

The handoff must not bypass `GoalOrientationInventory`, `GoalInquiryConsiderationSelection`, `BoundedAdvancementHorizon`, or the downstream need-family owners.

## Evidence reviewed

- `seed_runtime/bounded_operator_goal_establishment.py`
- `seed_runtime/goal_orientation_inventory.py`
- `seed_runtime/goal_inquiry_consideration_selection.py`
- `seed_runtime/bounded_advancement_horizon.py`
- `tests/test_goal_orientation_inventory.py`
- `tests/test_goal_inquiry_consideration_selection.py`
- `tests/test_bounded_advancement_horizon.py`
- `operator_authority_scope_bounded_goal_handoff_audit_001.md`
- `goal_advancement_need_evidence_topology_audit_001.md`
- `inquiry_need_projection_audit_001.md`
- `clarification_need_projection_audit_001.md`

## What exact selected-goal artifact does `BoundedAdvancementHorizon` currently require?

`BoundedAdvancementHorizon` currently requires two separate inputs that must agree:

1. one `GoalInquiryConsiderationSelection`; and
2. one matching `BoundedOperatorGoalEstablishment`.

The horizon constructor refuses unless:

- `selection.selection_state == "selected"`;
- `selection.selected_goal_establishment_id` is present;
- `selection.selected_goal_establishment_id == goal.goal_establishment_id`;
- `goal.artifact_type == "BoundedOperatorGoalEstablishment"`;
- `goal.establishment_state != "refused"`; and
- `present_movement_boundary` is non-empty.

Therefore the exact selected-goal artifact is not the `BoundedOperatorGoalEstablishment` alone. It is the selected-goal binding expressed by `GoalInquiryConsiderationSelection.selected_goal_establishment_id`, plus the matching stage-owned goal artifact supplied to the horizon.

The horizon preserves both identities:

```text
selection_id
selected_goal_establishment_id
selected_goal_source_ref
goal_establishment_id
goal_artifact_type
goal_ingress_artifact_ref
goal_ingress_lineage
```

This is a lawful two-part handoff: selection identity from the selector, goal state and lineage from the goal-establishment owner.

## Does `BoundedOperatorGoalEstablishment` already supply the necessary identity and lineage?

Yes, for identity and lineage. `BoundedOperatorGoalEstablishment` preserves:

- `goal_establishment_id`;
- `ingress_artifact_type`;
- `ingress_artifact_ref`;
- `ingress_lineage`;
- `establishment_state` and `establishment_reason`;
- intended outcome, known scope, unresolved scope, sufficiency and stop conditions;
- operator acceptance provenance and constraints;
- Unknowns, ambiguities, conflicts, known loss, and upstream source/warrant/selection/applicability/admission refs where applicable.

For the operator-ingress route in scope, `establish_bounded_operator_goal_from_authority_scope_binding(...)` verifies that the authority/scope binding, interpretation, and attributed expression identities match before it emits a goal. It then preserves the exact expression, interpretation, binding, authority source refs, supporting refs, unknowns, conflicts, excluded/unresolved scope material, and consumed ingress snapshot.

But this is still establishment, not present advancement selection. A goal's `goal_establishment_id` is sufficient for a selector to name it exactly; it is not itself proof that the goal has been selected for the current advancement horizon.

## How do ingress-derived goals enter `GoalOrientationInventory`?

Ingress-derived bounded goals enter the inventory only through explicit association evidence. The helper `association_from_bounded_goal(goal, dimension_refs=..., source_ref=...)` creates a `GoalOrientationAssociation` with:

```text
artifact_kind="bounded_goal"
artifact_ref=goal.goal_establishment_id
source_ref=source_ref or goal.ingress_artifact_ref
label=goal.intended_outcome
conflict_refs=goal.conflicts
association_state="associated" if dimension_refs else "Unknown"
```

`build_goal_orientation_inventory(...)` then places associated bounded-goal views into supported dimensions. It does not infer a dimension from goal wording, labels, topic similarity, or the mere existence of a goal. If a bounded goal lacks explicit dimension refs, it remains in `unknown_association_material`; if it cites unsupported dimensions, it remains in `unmatched_material`; if it carries conflicts, it remains in `conflicting_material`.

Therefore the lawful ingress path is:

```text
BoundedOperatorGoalEstablishment
→ explicit GoalOrientationAssociation(artifact_kind="bounded_goal")
→ GoalOrientationInventory visible bounded-goal candidate, unknown material, unmatched material, or conflicting material
```

The current code already owns this transition at inventory level. It is explicit association intake, not goal selection.

## Is `GoalInquiryConsiderationSelection` truly the owner of present-goal selection?

Functionally, yes. The selector is the only reviewed implementation that consumes an inventory candidate snapshot plus explicit focus evidence and emits one selected bounded-goal identity.

It lawfully selects only when:

- the goal is visible in the inventory's associated dimensions as a bounded goal;
- focus evidence names exactly one `goal_establishment_id`;
- the named id appears exactly once in the visible bounded-goal candidate set; and
- the focus evidence is not missing, ambiguous, Unknown, or conflicting.

It preserves non-selected goals, provenance refs, missing identity evidence refs, ambiguous refs, inventory mismatch refs, Unknowns, and conflicts. Its boundary flags refuse priority, activation, inquiry requirement/opening, frontier movement, work authorization, execution, recording, event-ledger writing, and mutation.

However, its name is narrower than the responsibility now being used downstream. `BoundedAdvancementHorizon` consumes this selection as the selected goal for present advancement, not merely as a selected goal for an already-open or inevitable inquiry. The implementation does not open inquiry and explicitly says selection is not inquiry required. Thus the owner is a present bounded-goal selector in behavior, while its current name says `GoalInquiryConsiderationSelection`.

## Do established and provisionally established goals have different eligibility?

For `BoundedAdvancementHorizon`, no difference is currently enforced between `established` and `provisional` goals. The horizon refuses only when `goal.establishment_state == "refused"`; any non-refused goal artifact can pass the horizon's establishment-state gate if the selected id matches and a present movement boundary is supplied.

For `GoalOrientationInventory`, no eligibility difference is enforced either. `association_from_bounded_goal(...)` accepts a `BoundedOperatorGoalEstablishment` and does not inspect `establishment_state`. A refused goal can therefore be converted into association evidence if a caller supplies it. Whether it becomes visible then depends on the supplied association state and dimension refs, not on establishment state.

For `GoalInquiryConsiderationSelection`, eligibility is candidate visibility plus exact focus evidence. The selector sees `GoalOrientationArtifactView`, not the full `BoundedOperatorGoalEstablishment`, so it cannot distinguish `established`, `provisional`, and `refused` unless that state is encoded in association evidence outside the current schema.

The effective current eligibility is therefore:

| Stage | Established | Provisional | Refused |
| --- | --- | --- | --- |
| Association helper | accepted | accepted | accepted |
| Inventory visible candidate | visible if explicitly associated to supported dimension | visible if explicitly associated to supported dimension | visible if explicitly associated to supported dimension |
| Goal selection | selectable if visible and exactly focused | selectable if visible and exactly focused | selectable if visible and exactly focused |
| Horizon | accepted | accepted | refused |

This means provisional goals are not automatically selectable, because inventory association and exact focus evidence are still required. But once provisionally associated and exactly focused, they are horizon-eligible. Refused goals remain too visible before the horizon unless upstream association evidence excludes them or a smaller implementation slice adds an eligibility gate.

## How do refused, ambiguous, conflicting, duplicate, unmatched, or unselected goals remain visible?

Current visibility preservation is split across inventory, selection, and horizon:

- Unknown association material remains in `GoalOrientationInventory.unknown_association_material`.
- Unsupported-dimension material remains in `GoalOrientationInventory.unmatched_material`.
- Conflicting association material remains in `GoalOrientationInventory.conflicting_material`.
- Missing focus evidence becomes `GoalInquiryConsiderationSelection.selection_state == "no_focus_evidence"` or `"missing_goal_identity"` with `missing_identity_evidence_refs`.
- Ambiguous focus evidence becomes `selection_state == "ambiguous"` with `ambiguous_goal_refs`.
- Conflicting focus evidence or multiple exact named ids becomes `selection_state == "conflict"` with `ambiguous_goal_refs` and preserved conflicts.
- Duplicate visible candidate identity becomes `selection_state == "ambiguous"` because more than one visible inventory view matches the same id.
- Exact focus on a non-visible goal becomes `selection_state == "inventory_mismatch"` with `inventory_mismatch_goal_refs`.
- A selected goal leaves the remaining visible bounded-goal views in `non_selected_goals`.
- A non-selected, mismatched, refused, or unresolved selection causes `BoundedAdvancementHorizon` to refuse with `selection_not_resolved`, `goal_artifact_identity_mismatch`, or `goal_artifact_not_established`.

This is sufficient for visibility of bad or unresolved cases. It is not sufficient for clean pre-horizon eligibility because refused goal visibility is not filtered before selection.

## Does current naming incorrectly limit a general goal-selection responsibility to inquiry?

Yes, partially. The implementation name and type name say `GoalInquiryConsiderationSelection`, but its behavior and downstream use are broader:

```text
GoalOrientationInventory
→ exact bounded-goal focus selection
→ BoundedAdvancementHorizon
```

The selector does not open inquiry, require inquiry, move a frontier, classify inquiry need, or select an advancement need. It selects one visible bounded goal for consideration from exact focus evidence. Downstream horizon and need-family projections use it as the selected-goal identity for present advancement.

The current name therefore risks preserving an obsolete road: it suggests inquiry owns the selected goal handoff even when the next lawful stage is clarification, authority, operational realization, sufficiency coverage, or no need at all. The responsibility is not an inquiry owner; it is a bounded goal consideration selector.

A rename or compatibility-breaking replacement should not preserve bad names solely for compatibility if an implementation slice is taken.

## Smallest lawful connection

No new general advancement-diagnosis owner is needed for this junction.

The smallest lawful connection is:

```text
BoundedOperatorGoalEstablishment(non-refused, including provisional)
→ explicit GoalOrientationAssociation(artifact_kind="bounded_goal", eligibility visible or withheld by association evidence)
→ GoalOrientationInventory
→ exact GoalFocusEvidence(goal_establishment_id=...)
→ GoalInquiryConsiderationSelection(selection_state="selected")
→ BoundedAdvancementHorizon(selection + matching BoundedOperatorGoalEstablishment + present_movement_boundary)
```

The implementation already has the mechanics for this path. The missing conceptual connection is not a new stage between goal establishment and horizon. It is the explicit recognition that the selection artifact consumed by `BoundedAdvancementHorizon` is produced by the goal-selection owner after inventory visibility and exact focus evidence, not by `BoundedOperatorGoalEstablishment` itself.

The smallest code-level correction, if one is warranted, is narrower than advancement diagnosis:

1. introduce a neutrally named selected-goal owner or alias, such as `BoundedGoalConsiderationSelection`, with the same no-action boundaries; or
2. rename `GoalInquiryConsiderationSelection` to a general bounded-goal consideration selector and update horizon consumers accordingly; and
3. add an eligibility rule so refused goals do not become visible/selectable bounded-goal candidates merely because association evidence was supplied.

That slice must not select needs, diagnose advancement, open inquiry, authorize, execute, record, write the event ledger, or mutate state.

## Is one implementation slice warranted?

Yes, one small implementation slice is warranted if the repository is advancing this junction beyond audit form.

The slice should not implement a new advancement-diagnosis owner. It should only make the existing handoff explicit and correctly named:

- make present bounded-goal selection neutral rather than inquiry-named;
- preserve exact selected `goal_establishment_id`, candidate-set identity, focus evidence refs, provenance refs, non-selected candidates, missing/ambiguous/conflicting/mismatched cases, and no-action flags;
- consume `GoalOrientationInventory`, not raw goal wording;
- require exact focus evidence, not inventory uniqueness or topic similarity;
- ensure refused `BoundedOperatorGoalEstablishment` records remain visible as refused/unselectable material rather than selected goals;
- preserve provisional goals as eligible only when explicitly associated and exactly focused;
- keep `BoundedAdvancementHorizon` consuming one selected-goal artifact plus the matching goal artifact;
- avoid compatibility aliases if they preserve the false implication that inquiry owns all present-goal selection.

If the repository chooses not to take a slice yet, the current path is still lawful for non-refused goals because `BoundedAdvancementHorizon` enforces the final selected-id and goal-artifact match.

## Exact next bounded question

What is the minimal read-only `BoundedGoalConsiderationSelection` implementation that consumes one `GoalOrientationInventory` and exact focus evidence, selects at most one non-refused visible `BoundedOperatorGoalEstablishment.goal_establishment_id` for present advancement consideration, preserves provisional eligibility only through explicit association and exact focus, preserves refused/ambiguous/conflicting/duplicate/unmatched/unselected goals as visible non-selection evidence, and supplies the selected-goal identity required by `BoundedAdvancementHorizon` without diagnosing advancement needs, opening inquiry, authorizing, recording, writing the event ledger, or mutating state?

## Conclusion

`BoundedAdvancementHorizon` currently requires a selected `GoalInquiryConsiderationSelection` plus a matching non-refused `BoundedOperatorGoalEstablishment`. `BoundedOperatorGoalEstablishment` already supplies exact goal identity and ingress lineage, including the operator-ingress authority/scope-binding route, but it does not itself select the goal for present advancement. Ingress-derived goals enter `GoalOrientationInventory` through explicit `GoalOrientationAssociation` evidence. The current selector truly owns present selected-goal identity in behavior, but its inquiry-specific name is too narrow for the downstream horizon handoff. The smallest lawful connection is inventory visibility plus exact focus selection plus horizon identity match; one small implementation slice is warranted only to neutralize naming and refuse pre-horizon selection of refused goals, not to introduce a general advancement-diagnosis owner.

Bounded goal to advancement horizon audit complete.
