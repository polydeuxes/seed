# Goal Orientation Association Ownership Audit 001

## Question

Determine the lawful producer boundary for the road:

```text
BoundedOperatorGoalEstablishment
→ stage-owned goal-orientation association testimony
→ GoalOrientationInventory
```

This audit does not implement. It asks whether the current `association_from_bounded_goal(...)` path is merely construction mechanics or an unrestricted ingress by which arbitrary callers can manufacture constitutional orientation through caller-supplied `dimension_refs`.

## Repository evidence reviewed

Implementation evidence:

- `seed_runtime/goal_orientation_inventory.py` defines `GoalOrientationAssociation`, `GoalOrientationInventory`, `association_from_bounded_goal(...)`, and `build_goal_orientation_inventory(...)`.
- `seed_runtime/bounded_operator_goal_establishment.py` defines `BoundedOperatorGoalEstablishment` and the lawful bounded-goal establishment producers.
- `tests/test_goal_orientation_inventory.py`, `tests/test_goal_inquiry_consideration_selection.py`, `tests/test_bounded_advancement_horizon.py`, `tests/test_clarification_need_projection.py`, `tests/test_inquiry_need_projection.py`, `tests/test_authority_need_projection.py`, and `tests/test_operational_realization_need_projection.py` exercise inventory, selection, horizon, and downstream projection paths.

Prior audit evidence:

- `goal_orientation_inventory_audit_001.md`
- `goal_orientation_inventory_slice_001.md`
- `bounded_operator_goal_advancement_horizon_handoff_audit_001.md`
- `goal_inquiry_consideration_selection_audit_001.md`
- `goal_advancement_need_audit_001.md`
- `clarification_need_projection_audit_001.md`
- `inquiry_need_projection_audit_001.md`
- `authority_need_projection_audit_001.md`
- `operational_realization_need_projection_audit_001.md`

## Current implementation shape

`GoalOrientationAssociation` is a frozen dataclass with these constitutional inputs:

```text
artifact_kind
artifact_ref
source_ref
dimension_refs
association_state
label
conflict_refs
```

The inventory builder consumes those associations as already-produced testimony. It does not derive membership from wording. It buckets a view under every supported dimension named in `dimension_refs`, preserves unknown material when association state is `Unknown` or no dimensions are supplied, preserves unmatched material when dimensions are unsupported, and preserves conflicting material when state or conflict refs indicate conflict.

`association_from_bounded_goal(...)` accepts a `BoundedOperatorGoalEstablishment`, accepts caller-supplied `dimension_refs`, and returns a `GoalOrientationAssociation` whose:

- `artifact_kind` is `bounded_goal`;
- `artifact_ref` is the goal establishment id;
- `source_ref` is caller-supplied or falls back to the goal ingress artifact ref;
- `dimension_refs` are exactly caller-supplied;
- `association_state` becomes `associated` whenever caller-supplied dimensions are non-empty, otherwise `Unknown`;
- `label` is the goal intended outcome;
- `conflict_refs` are the goal conflicts.

Therefore the helper does not infer dimensions from goal wording, but it also does not verify that the caller owns the dimensions it supplies.

## Every live producer of `GoalOrientationAssociation`

### Runtime production

The only runtime function that constructs a `GoalOrientationAssociation` from a bounded-goal artifact is:

```text
seed_runtime.goal_orientation_inventory.association_from_bounded_goal(...)
```

It produces only `artifact_kind="bounded_goal"` associations and accepts `dimension_refs` from its caller.

No reviewed runtime owner produces stage-owned bounded-goal orientation testimony by examining bounded-goal establishment evidence, responsibility-family evidence, goal-dimension projection evidence, or constitutional association evidence. No reviewed runtime owner validates an association producer identity.

### Direct dataclass construction in tests

The tests construct `GoalOrientationAssociation(...)` directly for pressures, bounded goals, inquiry references, and other material. These are fixture-level producers, not implemented constitutional owners. They prove that the inventory can consume explicit association evidence, preserve unknown/unmatched/conflicting/duplicate material, and keep inventory separate from selection. They do not prove who may lawfully produce association testimony in production.

### Downstream test fixtures using the helper

Several downstream projection tests call `association_from_bounded_goal(goal, dimension_refs=("knowledge_quality",), ...)` to build a minimal inventory fixture before selection/horizon/projection. Those calls are test scaffolding for downstream behavior. They currently also demonstrate the problem: a caller can make a bounded goal visible under a constitutional dimension by choosing `dimension_refs`.

### Prior audit prose

Prior audit prose describes an explicit association handoff from bounded goal to inventory. Prose is not a runtime producer. It can characterize the missing responsibility but cannot itself establish stage-owned association testimony.

## Who currently supplies `dimension_refs`

Every live `dimension_refs` value is caller-supplied:

- direct `GoalOrientationAssociation(...)` construction supplies dimensions directly;
- `association_from_bounded_goal(...)` copies its `dimension_refs` parameter directly into the association;
- `build_goal_orientation_inventory(...)` trusts association inputs and does not re-authorize them.

No current implementation computes, validates, owns, or stage-binds the dimension references for bounded-goal association testimony.

## Do responsibility-family or goal-dimension projections already own this testimony?

No.

The existing supported dimensions are declared as a tuple in `goal_orientation_inventory.py`. That declaration is a vocabulary/listing of supported orientation dimensions. It is not a producer that binds a bounded goal to one or more dimensions.

The inventory owner consumes explicit association evidence and renders visibility. It refuses registry, planning, priority, scheduling, authorization, execution, recording, event-ledger, and mutation authority. That makes it an orientation view, not a constitutional association producer.

`BoundedOperatorGoalEstablishment` owns goal establishment from lawful ingress. It preserves intended outcome, scope, sufficiency conditions, stop conditions, operator acceptance provenance, constraints, unknowns, ambiguities, conflicts, known loss, lineage, and non-authority flags. It does not own orientation-dimension classification merely because it owns goal identity and wording.

The downstream selection, advancement horizon, clarification, inquiry, authority, and operational-realization projection owners consume already-visible or already-selected goal identity. They do not own the prior constitutional act of associating a bounded goal with an orientation dimension.

Therefore no existing responsibility-family projection or goal-dimension projection already owns this testimony.

## Constructor or unrestricted production ingress?

`association_from_bounded_goal(...)` is mechanically a constructor: it wraps an existing bounded-goal artifact in the `GoalOrientationAssociation` shape and avoids deriving dimensions from labels or intended-outcome wording.

Constitutionally, however, it currently acts as an unrestricted production ingress because any caller that can pass a bounded goal and non-empty `dimension_refs` can cause:

```text
association_state="associated"
```

and make that goal visible under supported dimensions in `GoalOrientationInventory`.

The helper therefore proves construction mechanics, not lawful ownership. As implemented, it permits arbitrary callers to manufacture orientation association testimony by supplying dimensions.

## What evidence warrants associating one bounded goal with one or more dimensions

A lawful association requires explicit stage-owned orientation testimony, not goal text, topic similarity, request kind, downstream need family, or inventory uniqueness.

Minimum warranted evidence:

1. **Exact bounded-goal identity.** The testimony must name exactly one `BoundedOperatorGoalEstablishment.goal_establishment_id` and preserve the source bounded-goal artifact ref.
2. **Producer boundary.** The testimony must be emitted by a stage owner whose sole responsibility is goal-orientation association testimony for already-established bounded goals.
3. **Explicit dimension assertion.** Each dimension must be asserted as an orientation association, not inferred from goal wording, intended outcome, label, or later projection family.
4. **Source and warrant refs.** The testimony must preserve the refs that justify the dimension assertion. If those refs are missing, unavailable, conflicting, or insufficient, the association state must not be `associated`.
5. **Goal establishment state preservation.** Established, provisional, and refused goal states must remain visible as goal establishment facts. Goal establishment must not automatically create an orientation association.
6. **Negative authority preservation.** Association testimony must be read-only and must not select the goal, diagnose advancement, open inquiry, request authority, schedule work, execute, record, write the event ledger, or mutate state.
7. **Failure-state preservation.** Unknown, conflicting, unmatched, duplicate, refused, and provisional testimony must be carried forward explicitly rather than silently converted into associated selectable material.

One bounded goal may be associated with multiple dimensions only when the stage-owned testimony independently names each dimension. Multi-dimension visibility is lawful only as multi-dimension testimony, not as a side effect of general goal wording.

## Visibility of established, provisional, refused, unknown, conflicting, unmatched, and duplicate goals

The lawful shape must preserve visibility without collapsing visibility into eligibility:

- **Established goals:** may become associated material only if stage-owned association testimony names dimensions. Establishment alone is insufficient.
- **Provisional goals:** may remain visible, but provisionality must be preserved and must not be upgraded by association. Whether they are eligible for later consideration requires explicit downstream rules.
- **Refused goals:** must remain visible as refused goal-establishment material or refused association material. They must not become selectable merely because a caller supplied dimensions.
- **Unknown association:** goals with no lawful dimension testimony remain in unknown association material.
- **Conflicting association:** conflicting dimension testimony remains in conflicting material and must not be normalized into an associated candidate.
- **Unmatched dimensions:** unsupported dimensions remain unmatched material.
- **Duplicate goals:** duplicate association records preserve source identity and become ambiguity for exact selection rather than being deduplicated into one clean candidate.

Current inventory behavior already preserves unknown, unmatched, conflicting, and duplicate association material once it receives explicit associations. The missing boundary is lawful production and state-preserving association testimony before inventory consumption.

## Association visibility remains separate from consideration eligibility

`GoalOrientationInventory` visibility is orientation only. It does not select, prioritize, authorize, schedule, execute, record, or mutate. Current selection behavior is separate: `GoalInquiryConsiderationSelection` consumes an inventory and explicit focus evidence, then selects at most one visible bounded-goal identity or preserves no-focus, missing, ambiguous, conflict, duplicate, and mismatch states.

That separation must remain. A lawful association producer may make bounded-goal orientation testimony visible, but it must not make the goal selected for consideration. Selection remains a later exact-focus owner. Advancement diagnosis remains later still.

## Must arbitrary caller-supplied associations be deleted?

Yes, for bounded-goal constitutional orientation production.

The arbitrary path should not remain as a compatibility route for real production, because it gives callers authority to create `associated` bounded-goal orientation testimony by passing dimensions. Compatibility with tests or fixtures should not preserve a bad constitutional ingress.

The smallest deletion is not necessarily deletion of the dataclass or inventory builder. Direct explicit associations are still the inventory's input shape, and tests may need fixtures. The path that must be removed or demoted is the public bounded-goal helper accepting arbitrary `dimension_refs` and returning `associated` testimony without a stage-owned producer/warrant boundary.

A safe future implementation can keep low-level construction internal to the new producer or expose a constructor that cannot mark a bounded goal `associated` from raw caller dimensions without explicit producer/warrant evidence.

## Is one implementation slice warranted?

Yes, one narrow implementation slice is warranted if the repository needs executable support for the candidate road.

The slice should be smaller than a general goal selector, responsibility-family classifier, or advancement-diagnosis owner. It should recover only:

```text
stage-owned goal-orientation association testimony for bounded goals
```

It should consume already-produced `BoundedOperatorGoalEstablishment` artifacts and explicit association evidence records, then emit bounded-goal `GoalOrientationAssociation` records or refusal/unknown/conflict/unmatched records for inventory consumption.

It should not infer dimensions from labels, intended outcome wording, topic similarity, request kind, downstream need kind, or inventory uniqueness.

## Smallest lawful connection

The smallest lawful connection is:

```text
BoundedOperatorGoalEstablishment
→ BoundedGoalOrientationAssociationTestimony
→ GoalOrientationAssociation(artifact_kind="bounded_goal", state-preserving)
→ GoalOrientationInventory
```

Where `BoundedGoalOrientationAssociationTestimony` is a read-only producer boundary that:

- requires one exact bounded-goal identity;
- requires explicit dimension testimony and warrant refs;
- preserves the bounded goal's establishment state;
- emits `associated` only for supported dimensions with sufficient non-conflicting testimony;
- emits `Unknown` when dimension testimony is absent or insufficient;
- emits `conflicting` when testimony conflicts;
- emits unmatched material for unsupported dimensions;
- preserves duplicate source identity;
- does not select goals;
- does not diagnose advancement need;
- does not open inquiry;
- does not authorize, schedule, execute, record, write the event ledger, or mutate state.

`association_from_bounded_goal(...)` should not be the lawful producer unless it is replaced by or restricted behind this stage-owned boundary.

## Exact next bounded question

What is the minimal read-only `BoundedGoalOrientationAssociationTestimony` artifact that consumes one `BoundedOperatorGoalEstablishment` plus explicit dimension-assertion evidence refs, emits or refuses bounded-goal `GoalOrientationAssociation` records for `GoalOrientationInventory`, preserves established, provisional, refused, unknown, conflicting, unmatched, and duplicate states, and proves that it did not infer dimensions from wording, select the goal for consideration, diagnose advancement needs, authorize work, record output, write the event ledger, or mutate cluster state?

## Conclusion

The existing implementation has an inventory consumer and a bounded-goal association constructor, but no lawful stage-owned producer of bounded-goal orientation association testimony. All current `dimension_refs` are caller-supplied. `association_from_bounded_goal(...)` is mechanically a constructor but constitutionally functions as an unrestricted production ingress because non-empty caller dimensions become associated inventory visibility. No existing responsibility-family or goal-dimension projection owns this testimony. Arbitrary caller-supplied bounded-goal associations should be deleted or demoted from production ingress, and one narrow implementation slice is warranted to introduce a read-only stage-owned association testimony boundary between bounded-goal establishment and inventory.

Goal orientation association ownership audit complete.
