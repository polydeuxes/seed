# Bounded Goal Advancement Road Evidence Audit 001

## Scope and method

This audit examines only repository-observable evidence on the current road between `BoundedOperatorGoalEstablishment` and `BoundedAdvancementHorizon`. It reviews these live implementation files and directly related tests:

- `seed_runtime/bounded_operator_goal_establishment.py`
- `seed_runtime/goal_orientation_inventory.py`
- `seed_runtime/goal_inquiry_consideration_selection.py`
- `seed_runtime/bounded_advancement_horizon.py`
- `seed_runtime/__init__.py`
- `tests/test_goal_orientation_inventory.py`
- `tests/test_goal_inquiry_consideration_selection.py`
- `tests/test_bounded_advancement_horizon.py`
- downstream projection tests that construct horizons: `tests/test_clarification_need_projection.py`, `tests/test_inquiry_need_projection.py`, `tests/test_authority_need_projection.py`, `tests/test_operational_realization_need_projection.py`, `tests/test_goal_advancement_need_set.py`, `tests/test_advancement_need_family_coverage_set.py`, and `tests/test_goal_advancement_sufficiency_projection.py`

The audit treats code, public exports, and tests as evidence of current behavior only. It does not treat prior audit documents, helper names, dataclass names, or repeated vocabulary as proof of constitutional ownership.

## Exact live call and data paths reviewed

### Path A: bounded goal to orientation inventory candidate visibility

```text
BoundedOperatorGoalEstablishment
→ association_from_bounded_goal(goal, dimension_refs=..., source_ref=...)
→ GoalOrientationAssociation(...)
→ build_goal_orientation_inventory([...])
→ GoalOrientationInventory.dimensions[*].bounded_goals
```

Implementation evidence:

- `association_from_bounded_goal(...)` accepts a `BoundedOperatorGoalEstablishment`, caller-supplied `dimension_refs`, and optional `source_ref`.
- It returns `GoalOrientationAssociation(artifact_kind="bounded_goal", artifact_ref=goal.goal_establishment_id, source_ref=source_ref or goal.ingress_artifact_ref, dimension_refs=tuple(dimension_refs), association_state="associated" if dimensions else "Unknown", label=goal.intended_outcome, conflict_refs=goal.conflicts)`.
- `build_goal_orientation_inventory(...)` creates dimension buckets from supported dimensions, converts each association into a view, adds views with `association_state == "Unknown"` or no dimensions to `unknown_association_material`, adds views with conflicts to `conflicting_material`, and appends associated views into supported dimension buckets by each supplied dimension ref.
- A bounded goal is visible to selection only when its association view lands in `GoalOrientationInventory.dimensions[*].bounded_goals`.

### Path B: orientation inventory to inquiry-consideration selection

```text
GoalOrientationInventory
→ visible_bounded_goals(inventory)
→ goal_inventory_candidate_set_id(inventory)
→ select_goal_for_inquiry_consideration(inventory, focus_evidence)
→ GoalInquiryConsiderationSelection
```

Implementation evidence:

- `visible_bounded_goals(...)` iterates over `inventory.dimensions` and returns only `dimension.bounded_goals` whose `artifact_kind == "bounded_goal"`.
- `goal_inventory_candidate_set_id(...)` hashes `artifact_ref`, `source_ref`, and `association_state` for visible bounded goals.
- `select_goal_for_inquiry_consideration(...)` consumes the inventory and iterable `GoalFocusEvidence`.
- Selection returns `selected` only when exactly one focus identity is supplied, exactly one visible bounded-goal candidate has matching `artifact_ref`, and no missing, Unknown, ambiguous, or conflicting focus state precedes it.
- Selection returns unresolved states for no focus evidence, missing/Unknown evidence, ambiguous focus evidence, conflicting focus identities, duplicate visible matches, or inventory mismatch.

### Path C: selection plus bounded goal to bounded advancement horizon

```text
GoalInquiryConsiderationSelection
+ BoundedOperatorGoalEstablishment
+ caller keyword inputs
→ establish_bounded_advancement_horizon(...)
→ BoundedAdvancementHorizon
```

Implementation evidence:

- `establish_bounded_advancement_horizon(...)` consumes a `GoalInquiryConsiderationSelection`, a `BoundedOperatorGoalEstablishment`, and keyword inputs for the present boundary, scope, evidence snapshots, time/current-state bounds, need-family visibility/exclusion, unknowns, conflicts, stale refs, and unavailable refs.
- It refuses when selection is not `selected`, when the selected goal id does not match the supplied goal, when the supplied goal is not a `BoundedOperatorGoalEstablishment` or has `establishment_state == "refused"`, when `present_movement_boundary` is empty, or when an excluded need family lacks a reason.
- On success it preserves selection identity, selected goal identity/source, goal identity/type/ingress lineage, caller-supplied horizon boundary and bounds, caller-supplied evidence refs, caller-supplied need-family fields, and merged selection/goal/caller unknowns and conflicts.

### Public exports reviewed

`seed_runtime/__init__.py` publicly exports `BoundedAdvancementHorizon`, `EvidenceSnapshotReference`, `NeedFamilyExclusion`, `establish_bounded_advancement_horizon`, `GoalFocusEvidence`, `GoalInquiryConsiderationSelection`, `goal_inventory_candidate_set_id`, `select_goal_for_inquiry_consideration`, `visible_bounded_goals`, `GoalOrientationAssociation`, `GoalOrientationInventory`, `association_from_bounded_goal`, and `build_goal_orientation_inventory`. Public export evidence proves external availability, not constitutional ownership.

## Field-provenance table

| Control area | Field or input | Live producer / immediate source | Caller-controlled? | Validation observed | Effect |
|---|---|---:|---:|---|---|
| Inventory visibility | `GoalOrientationAssociation.artifact_kind` | Direct association constructor or `association_from_bounded_goal(...)` | Yes for direct constructor; fixed to `bounded_goal` by helper | Inventory buckets by literal kind; selection later filters `artifact_kind == "bounded_goal"` | Determines whether material can appear as bounded-goal candidate |
| Inventory visibility | `GoalOrientationAssociation.artifact_ref` | Direct constructor or `goal.goal_establishment_id` in helper | Yes indirectly by supplied goal/direct association | No inventory validation that ref is a live established goal | Becomes candidate identity and possible selected id |
| Inventory visibility | `GoalOrientationAssociation.source_ref` | Direct constructor or caller `source_ref` fallback to goal ingress ref | Yes | No authorization validation | Preserved as selected goal source if selected |
| Inventory visibility | `dimension_refs` | Direct constructor or `association_from_bounded_goal(..., dimension_refs=...)` | Yes | Only membership against supported dimensions during inventory bucketing | Non-empty supported refs make a bounded-goal view visible under dimensions |
| Inventory visibility | `association_state` | Direct constructor or helper sets `associated` if dimensions else `Unknown` | Yes for direct constructor; derived from caller dimensions in helper | Unknown/no-dimension views are sent to unknown material; still may be bucketed if dimensions exist | Preserves association state and affects candidate-set identity |
| Inventory visibility | `conflict_refs` | Direct constructor or `goal.conflicts` in helper | Yes directly or from supplied goal | Conflicted views are preserved in `conflicting_material`; not excluded from dimension buckets | Conflict visibility does not by itself prevent candidate visibility |
| Selection candidate acquisition | `inventory.dimensions[*].bounded_goals` | `build_goal_orientation_inventory(...)` or any supplied `GoalOrientationInventory` | Yes if caller supplies inventory | `visible_bounded_goals(...)` filters only by location and `artifact_kind` | Defines candidate set |
| Selection candidate identity | Candidate `artifact_ref` | Inventory view | Yes via association/inventory | Exact equality against focus goal id | Matching ref can be selected |
| Selection candidate uniqueness | Count of candidate matches | Inventory contents | Yes via inventory/associations | `len(matches) == 1` required; duplicates become ambiguous | Prevents duplicate visible identity from selecting |
| Selection focus | `GoalFocusEvidence.evidence_ref` | Caller | Yes | Preserved; not authorized | Selection provenance/id input |
| Selection focus | `GoalFocusEvidence.source_ref` | Caller | Yes | Preserved; not authorized | Selection provenance/id input |
| Selection focus | `GoalFocusEvidence.goal_establishment_id` | Caller | Yes | Requires exactly one named id after state checks; then must match a visible candidate | Decisive selected-goal identity input |
| Selection focus | `GoalFocusEvidence.evidence_state` | Caller | Yes | `conflict`, `missing_goal_identity`, `Unknown`, and `ambiguous` block selected state | Controls eligibility for selection |
| Selection focus | `candidate_goal_refs` | Caller | Yes | Preserved for ambiguity/conflict outputs | Unresolved diagnosis only |
| Selection focus | `unknowns`, `conflicts` | Caller | Yes | Deduped into selection outputs | Later merged into horizon unknowns/conflicts |
| Horizon construction | `selection.selection_state` | Selection object supplied by caller | Yes by supplying object | Must be `selected` | Required for bounded horizon |
| Horizon construction | `selection.selected_goal_establishment_id` | Selection result or constructed object | Yes by supplying object | Must be non-empty and equal `goal.goal_establishment_id` | Binds selected id to goal artifact |
| Horizon construction | `selection.selected_goal_source_ref` | Candidate source ref | Yes via inventory/selection object | No independent validation | Preserved on horizon |
| Horizon construction | `goal.artifact_type` | Bounded goal producer or constructed object | Caller controls supplied object | Must equal `BoundedOperatorGoalEstablishment` | Refuses non-goal artifact type |
| Horizon construction | `goal.establishment_state` | Bounded goal producer | Caller controls supplied object | Refuses only `refused`; provisional is not refused by this check | Refused goals cannot produce bounded horizon here |
| Horizon construction | `goal.goal_establishment_id` | Bounded goal producer | Caller controls supplied object | Must match selection id | Horizon goal identity |
| Horizon construction | `present_movement_boundary` | Horizon caller keyword | Yes | Must be non-empty | Required horizon boundary |
| Horizon construction | `included_scope`, `excluded_scope` | Horizon caller keywords | Yes | String coercion/dedupe only | Preserved horizon scope |
| Horizon construction | `evidence_snapshot_refs` | Horizon caller keyword | Yes | Tuple conversion only | Preserved evidence snapshot refs |
| Horizon construction | `time_bounds`, `current_state_bounds` | Horizon caller keywords | Yes | String coercion/dedupe only | Preserved horizon bounds |
| Horizon construction | `potentially_relevant_need_families` | Horizon caller keyword | Yes | String coercion/dedupe only | Preserved as potentially relevant, not classified |
| Horizon construction | `explicitly_excluded_need_families` | Horizon caller keyword | Yes | Each item must have non-empty `reason` | Preserved exclusions or refusal |
| Horizon construction | `unknowns`, `conflicts` | Selection, goal, horizon caller | Yes | Deduped | Preserved on horizon |
| Horizon construction | `stale_evidence_refs`, `unavailable_evidence_refs` | Horizon caller keywords | Yes | String coercion/dedupe only | Preserved evidence-quality refs |

## Answers to the asymmetrical investigation questions

### 1. What exact artifact and fields must `BoundedAdvancementHorizon` consume?

The live producer function consumes:

```python
establish_bounded_advancement_horizon(
    selection: GoalInquiryConsiderationSelection,
    goal: BoundedOperatorGoalEstablishment,
    *,
    present_movement_boundary: str,
    included_scope: Iterable[str] = (),
    excluded_scope: Iterable[str] = (),
    evidence_snapshot_refs: Iterable[EvidenceSnapshotReference] = (),
    time_bounds: Iterable[str] = (),
    current_state_bounds: Iterable[str] = (),
    potentially_relevant_need_families: Iterable[str] = (),
    explicitly_excluded_need_families: Iterable[NeedFamilyExclusion] = (),
    unknowns: Iterable[str] = (),
    conflicts: Iterable[str] = (),
    stale_evidence_refs: Iterable[str] = (),
    unavailable_evidence_refs: Iterable[str] = (),
)
```

The required live inputs are an exact selected `GoalInquiryConsiderationSelection`, a matching non-refused `BoundedOperatorGoalEstablishment`, and non-empty `present_movement_boundary`. Other horizon fields are optional caller-supplied preservation inputs.

### 2. Which live production paths provide those inputs?

Observed tests provide the selection through:

```text
association_from_bounded_goal(goal, dimension_refs=("knowledge_quality",), source_ref=...)
→ build_goal_orientation_inventory([...])
→ select_goal_for_inquiry_consideration(inventory, [GoalFocusEvidence(..., goal.goal_establishment_id)])
```

Observed horizon tests then call `establish_bounded_advancement_horizon(selection, goal, present_movement_boundary=..., ...)`. Downstream projection tests use the same fixture pattern. The implementation itself does not require that `selection` was produced by this path; it accepts any `GoalInquiryConsiderationSelection` object with the expected fields.

### 3. Is any live path from an established bounded goal to the horizon possible without `GoalOrientationInventory`?

Yes, by implementation shape, because `establish_bounded_advancement_horizon(...)` accepts a `GoalInquiryConsiderationSelection` object directly and does not inspect or require a `GoalOrientationInventory`. A caller can construct `GoalInquiryConsiderationSelection(selection_state="selected", selected_goal_establishment_id=goal.goal_establishment_id, ...)` directly, then pass it with the goal and a non-empty boundary. This bypass path is possible through public dataclass construction.

No repository test was found that exercises this bypass as an intended production path. Therefore the bypass is implementation-possible, publicly available, and unproven as a lawful producer path.

### 4. What live consumer requires a bounded goal to possess dimension associations before present advancement?

`select_goal_for_inquiry_consideration(...)` requires visible bounded-goal candidates from `GoalOrientationInventory.dimensions[*].bounded_goals`. Those candidates are typically produced from dimension-associated bounded-goal associations. This is a requirement of the current selector path, not of `BoundedAdvancementHorizon` itself.

`BoundedAdvancementHorizon` requires selected goal identity and matching bounded goal artifact. It does not require or consume dimension associations.

### 5. Who controls every decisive input to `association_from_bounded_goal(...)`, especially `dimension_refs`?

The caller controls the supplied `goal`, `dimension_refs`, and `source_ref`. The helper copies `dimension_refs` into the association and sets association state to `associated` if the tuple is non-empty, otherwise `Unknown`. It does not derive dimension refs from goal text, validate a dimension-producing authority, inspect establishment state, or prove that the caller is allowed to associate the goal with those dimensions.

### 6. What validation prevents a caller from manufacturing orientation, eligibility, or selection?

Observed validation:

- Inventory only buckets supplied dimension refs that match supported dimensions; unsupported refs are preserved as unmatched.
- Inventory does not infer dimensions from wording.
- Selection ignores pressures and Null dimensions because it only considers `dimension.bounded_goals` views with `artifact_kind == "bounded_goal"`.
- Selection refuses missing, Unknown, ambiguous, conflicting, invisible, and duplicate visible identities.
- Horizon refuses unresolved selection, selected-goal/goal mismatch, refused goal artifact, empty movement boundary, and excluded need-family records without reasons.

Missing validation:

- No observed validation proves that a caller is authorized to supply `dimension_refs`.
- No observed validation proves that a direct `GoalOrientationAssociation` names a live established bounded goal.
- No observed validation prevents a caller from constructing `GoalInquiryConsiderationSelection` directly with `selection_state="selected"` and a matching id.
- No observed validation validates `GoalFocusEvidence.source_ref` or `evidence_ref` as constitutional testimony.
- No observed validation prevents a caller from presenting caller-chosen focus evidence as exact goal identity.

### 7. Does `GoalInquiryConsiderationSelection` own general bounded-goal selection, or only selection from one orientation-inventory representation?

Implementation evidence supports only selection from one orientation-inventory representation. The selector's candidate acquisition is hardwired to `visible_bounded_goals(inventory)`, which reads `GoalOrientationInventory.dimensions[*].bounded_goals`. No alternate candidate source is consumed by the selector. General bounded-goal selection outside that representation remains unproven.

### 8. Which responsibilities are combined inside the current selector?

The current selector combines these implementation responsibilities:

1. **Candidate acquisition**: `visible_bounded_goals(inventory)` extracts bounded-goal views from inventory dimensions.
2. **Candidate-set identity**: `goal_inventory_candidate_set_id(inventory)` hashes visible candidate refs, source refs, and association states.
3. **Candidate eligibility by representation**: only visible dimension-bucketed bounded-goal views are candidates; unknown, unmatched, conflicting lists are not separately candidates unless also dimension-bucketed.
4. **Focus-evidence state handling**: missing, Unknown, ambiguous, and conflict focus states determine unresolved selection states.
5. **Exact focus binding**: exact focus evidence must supply one goal id.
6. **Goal selection**: exactly one visible candidate with matching artifact ref becomes selected.
7. **Inquiry-specific boundary vocabulary**: the artifact and boundary notes describe selection for inquiry consideration and explicitly refuse inquiry opening, frontier movement, work authorization, execution, recording, and mutation.

### 9. Are established, provisional, and refused goal states available to the inventory and selector? Where are they lost?

`BoundedOperatorGoalEstablishment` carries `establishment_state`. `association_from_bounded_goal(...)` does not copy `establishment_state` into `GoalOrientationAssociation` or `GoalOrientationArtifactView`. `GoalOrientationInventory` therefore does not preserve established/provisional/refused state for bounded goals. `GoalInquiryConsiderationSelection` sees only `GoalOrientationArtifactView` fields and likewise lacks establishment state. The state is reintroduced only when `establish_bounded_advancement_horizon(...)` receives the full `BoundedOperatorGoalEstablishment` and refuses `establishment_state == "refused"`.

Because the horizon check refuses only `refused`, the implementation does not show a horizon refusal for provisional states. Whether provisional goals are eligible for bounded horizons remains unproven by this road except that they are not rejected by the observed `establishment_state == "refused"` check.

### 10. What concrete behavior would fail if goal-dimension association were removed from the advancement road?

Concrete behavior that would fail in the current selector path:

- Tests and fixtures that build an inventory from `association_from_bounded_goal(goal, dimension_refs=("knowledge_quality",), ...)` and then select with exact `GoalFocusEvidence` would no longer produce visible bounded-goal candidates if no replacement candidate source were provided.
- `select_goal_for_inquiry_consideration(...)` would return `inventory_mismatch` for exact focus evidence naming a goal not present in visible inventory candidates.
- Horizon construction tests that obtain a selected state through that selector fixture would fail earlier because the selection would not be `selected`, causing `establish_bounded_advancement_horizon(...)` to refuse with `selection_not_resolved`.

Concrete behavior that would not necessarily fail:

- `BoundedAdvancementHorizon` construction itself does not consume dimensions. If supplied with a selected `GoalInquiryConsiderationSelection` and matching non-refused goal through another path, it can bound a horizon without orientation inventory.

### 11. What remains unproven about the proposed road?

Unproven claims:

- That `GoalOrientationInventory` is a constitutionally required stage between bounded goal establishment and bounded advancement horizon.
- That goal-dimension association is constitutionally necessary for present advancement.
- That `association_from_bounded_goal(...)` is a lawful producer rather than a convenience constructor or unrestricted ingress.
- That caller-supplied `dimension_refs` are constitutional testimony.
- That `GoalInquiryConsiderationSelection` owns general bounded-goal selection rather than inventory-specific inquiry-consideration selection.
- That exact focus evidence is produced by a validated constitutional testimony owner.
- That direct construction of `GoalInquiryConsiderationSelection` is lawful for production.
- That provisional goal states are eligible or ineligible for horizon construction as a constitutional matter.

## Alternate paths that bypass orientation inventory

### Direct selection dataclass construction

Because `GoalInquiryConsiderationSelection` is a public frozen dataclass and `establish_bounded_advancement_horizon(...)` only checks its fields, a caller can construct a selected selection object directly and pass it to the horizon producer. This path bypasses `GoalOrientationAssociation`, `GoalOrientationInventory`, `visible_bounded_goals(...)`, and `select_goal_for_inquiry_consideration(...)`.

```text
BoundedOperatorGoalEstablishment
→ caller-constructed GoalInquiryConsiderationSelection(selection_state="selected", selected_goal_establishment_id=goal.goal_establishment_id)
→ establish_bounded_advancement_horizon(...)
→ BoundedAdvancementHorizon
```

Repository evidence shows this is possible from public constructors and function checks. Repository evidence does not show it is an intended lawful production path.

### Direct horizon refusal path

A caller can also pass unresolved selection objects to `establish_bounded_advancement_horizon(...)`. The horizon artifact is still produced, but with `horizon_state="refused"` and refusal reason such as `selection_not_resolved`. This path bypasses inventory for refused horizon construction.

## Actual downstream assumptions

Downstream projection implementations import and consume `BoundedAdvancementHorizon` directly with `GoalInquiryConsiderationSelection` and `BoundedOperatorGoalEstablishment`. Their tests generally construct the horizon through the inventory/selection fixture path, but the downstream projection boundary is the horizon plus selected goal inputs, not the orientation inventory.

Observed downstream assumptions include:

- The selection is selected and matches the goal.
- The horizon is bounded and matches the selected goal.
- The horizon carries evidence refs, stale/unavailable refs, potentially relevant need families, explicit exclusions, unknowns, conflicts, and read-only/no-mutation flags.
- Need-family projection code uses horizon family fields and evidence-quality fields; it does not consume `GoalOrientationInventory` dimension refs as its horizon input.

## Claims supported by implementation evidence

- `BoundedAdvancementHorizon` consumes `GoalInquiryConsiderationSelection`, `BoundedOperatorGoalEstablishment`, and caller-supplied horizon boundary/scope/evidence/need-family fields.
- The inventory selector path depends on visible bounded-goal views in `GoalOrientationInventory.dimensions[*].bounded_goals`.
- `association_from_bounded_goal(...)` copies caller-supplied `dimension_refs` and makes non-empty dimensions associated.
- `build_goal_orientation_inventory(...)` does not infer dimensions from goal wording.
- `select_goal_for_inquiry_consideration(...)` selects only when exact focus evidence names exactly one visible bounded-goal candidate.
- `BoundedAdvancementHorizon` does not consume dimension refs and does not inspect orientation inventory.
- Established/provisional/refused goal state is not preserved in `GoalOrientationAssociation`, `GoalOrientationArtifactView`, `GoalOrientationInventory`, or `GoalInquiryConsiderationSelection`.
- The horizon producer refuses refused goal artifacts but does not reject non-refused provisional state by the observed check.

## Claims contradicted by implementation evidence

- Claim: `GoalOrientationInventory` is mechanically required by `BoundedAdvancementHorizon`.
  - Contradiction: the horizon producer signature accepts selection and goal, not inventory.
- Claim: Dimension association is required by the horizon artifact.
  - Contradiction: the horizon artifact has no dimension-ref input and preserves no orientation dimension refs.
- Claim: The selector performs general bounded-goal selection.
  - Contradiction: candidates come only from one orientation-inventory representation.
- Claim: Existing helper status proves lawful producer status.
  - Contradiction: the helper accepts caller-supplied dimensions and contains no validation of producer authority.
- Claim: Inventory or selector preserves established/provisional/refused bounded-goal states.
  - Contradiction: their view and selection fields omit establishment state.

## Claims that remain unproven

- Whether an orientation inventory stage belongs on the constitutional advancement road.
- Whether bounded goals must be dimension-associated before present advancement.
- Who may lawfully produce goal-orientation association testimony.
- Who may lawfully produce exact goal-focus evidence.
- Whether direct selected `GoalInquiryConsiderationSelection` construction is forbidden, tolerated, or a valid alternate producer.
- Whether provisional bounded goals may advance to a bounded horizon.
- Whether the current inquiry-consideration selector should be the selector immediately before every bounded advancement horizon.

Bounded goal advancement road evidence audit complete.
