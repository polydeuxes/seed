# Advancement Need Consideration Selection Audit 001

## Question

Determine the lawful bounded selection:

```text
GoalAdvancementNeedSet
+
explicit need-focus evidence
→ AdvancementNeedConsiderationSelection
```

for one exact selected goal and one exact bounded advancement horizon. The selection target is one exact already-established native advancement need record preserved inside the `GoalAdvancementNeedSet`.

Repository authority wins. This audit is documentary only. It does not implement a diagnostic surface, CLI flag, recordable output, inquiry opening, clarification request, authority request, operational-realization selection, route, priority, authorization, execution, event-ledger write, cluster mutation, or state mutation.

## Guardrails preserved

```text
need selected for consideration
!= highest-priority need
!= primary blocker
!= resolution selected
!= next action selected

unique established need
!= automatically selected

selected inquiry need
!= inquiry frontier opened
```

The selected need must already exist as an exact native need record in the `GoalAdvancementNeedSet`. Selection must not be inferred from family order, severity, uniqueness, sufficiency conclusion, labels, wording similarity, or display vocabulary.

## Evidence reviewed

- `seed_runtime/goal_advancement_need_set.py`
- `tests/test_goal_advancement_need_set.py`
- `seed_runtime/goal_advancement_sufficiency_projection.py`
- `tests/test_goal_advancement_sufficiency_projection.py`
- `seed_runtime/clarification_need_projection.py`
- `seed_runtime/inquiry_need_projection.py`
- `seed_runtime/authority_need_projection.py`
- `seed_runtime/operational_realization_need_projection.py`
- `seed_runtime/bounded_advancement_horizon.py`
- `seed_runtime/goal_inquiry_consideration_selection.py`
- `goal_inquiry_consideration_selection_audit_001.md`
- `goal_inquiry_consideration_selection_slice_001.md`
- `goal_advancement_need_evidence_topology_audit_001.md`
- `goal_advancement_need_set_slice_001.md`
- `goal_advancement_sufficiency_projection_audit_001.md`
- `goal_advancement_sufficiency_projection_slice_001.md`

## Current implemented boundary

### `GoalAdvancementNeedSet` preserves native need projections, not consideration selection

`GoalAdvancementNeedSet` preserves supplied, absent, and excluded family projections for one exact `BoundedAdvancementHorizon`. It records the selected goal identity, goal establishment identity, horizon identity, family records, horizon unknowns, horizon conflicts, exclusions, and projection identity conflicts.

Its boundary notes are decisive:

- supplied stage-owned need projections are preserved without reinterpretation;
- coexisting needs are an unordered set, not a priority order, overall blocker, route, or next action;
- supplied, absent, and explicitly excluded need families remain distinct;
- the need set is not a sufficiency judgment and does not open inquiry, request authority, select realization, authorize, execute, record, write the event ledger, or mutate cluster state.

Therefore `GoalAdvancementNeedSet` can provide the candidate universe for need consideration, but it does not select any need for consideration.

### Native family projections own need records

The native projections preserve family-owned need standing records:

- `ClarificationNeedProjection` has `established`, `unsupported`, `unknown`, `conflicting`, and `excluded_family` records.
- `InquiryNeedProjection` has `established`, `unsupported`, `unknown`, `conflicting`, and `excluded_family` records.
- `AuthorityNeedProjection` has `established`, `unsupported`, `unknown`, `conflicting`, `outside_current_scope`, and `unclassified` records.
- `OperationalRealizationNeedProjection` has `established`, `unsupported`, `unknown`, `conflicting`, `unclassified_here`, and `unclassified` records.

Only records in a supplied native projection can be selected by this boundary. A display summary, conclusion, family label, reason string, or coverage status is not itself a native need record.

### `GoalAdvancementSufficiencyProjection` is not a selector

`GoalAdvancementSufficiencyProjection` consumes the need set and family coverage set to emit one bounded sufficiency conclusion: `sufficient_for_now`, `insufficient_for_now`, `unknown`, or `conflicting`. It preserves family reasons as unordered and explicitly refuses ranking, priority, route selection, next-action selection, inquiry opening, authority request, realization selection, authorization, execution, recording, event-ledger writing, and cluster mutation.

Its reasons may mention native projection ids and item references, but the conclusion and reason dominance order do not lawfully select a need for consideration. In particular, `insufficient_for_now` does not identify the highest-priority need, primary blocker, resolution, or next action.

### `GoalInquiryConsiderationSelection` is adjacent precedent, not the same owner

`GoalInquiryConsiderationSelection` already shows the repository pattern for focus-bound read-only selection: explicit focus evidence naming exact identities can select one visible bounded goal, while missing identity, ambiguity, conflict, and inventory mismatch are preserved rather than repaired. It also proves that selection for consideration is not activation, inquiry opening, frontier movement, authorization, execution, recording, event-ledger writing, or mutation.

The same shape is appropriate here, but the target universe changes from visible bounded goals to exact native advancement need records already preserved by `GoalAdvancementNeedSet`.

## What evidence may lawfully identify one exact need record?

Lawful evidence must identify one exact native need record already present in a supplied family projection inside the exact `GoalAdvancementNeedSet`.

Minimum lawful evidence:

1. **Exact need-set binding.** The focus evidence must name or be bound to the current `need_set_id`, not merely to a goal label, family, or sufficiency conclusion.
2. **Exact selected-goal binding.** The evidence must bind to the same `selection_id` and `goal_establishment_id` carried by the need set.
3. **Exact horizon binding.** The evidence must bind to the same `horizon_id` carried by the need set.
4. **Exact family binding.** The evidence must name one supported in-scope family record: `clarification`, `inquiry`, `authority`, or `operational_realization`.
5. **Native projection binding.** The evidence must name the exact supplied native projection id from that family record.
6. **Native need identity.** The evidence must name one exact native need item identity. Existing native item schemas do not expose a universal `need_item_id`; therefore a first implementation slice would need either a stable native item identity or a precise native item selector such as family + projection id + standing bucket + exact testimony/component ref + exact item payload fingerprint.
7. **Established standing.** The selected item must be in the native projection's `established` bucket. This boundary selects an established advancement need for consideration; it does not select unsupported, unknown, conflicting, excluded, outside-current-scope, or unclassified records as needs.
8. **Explicit operator focus.** The evidence must be an operator-facing focus record, closed-choice binding, admitted interpretation, or preserved UI/reference event that carries the exact identity above. It cannot be inferred from uniqueness or presentation order.

Evidence that is not lawful by itself:

- only a need family name, such as `inquiry`;
- only a sufficiency conclusion, such as `insufficient_for_now`;
- only a reason string from the sufficiency projection;
- the only established need in the need set;
- family order, severity, count, or bucket order;
- label similarity, wording similarity, or shared terminology;
- `unknown`, `conflicting`, `unsupported`, `excluded_family`, `outside_current_scope`, `unclassified_here`, or `unclassified` records;
- an absent family record;
- a mismatched native projection that was refused by the need set;
- presentation vocabulary such as current work position, active edge, continuation, or source navigation unless another owner has already preserved exact need identity.

## How focus evidence binds to goal, horizon, family, native projection, and need identity

A lawful `AdvancementNeedConsiderationEvidence` shape should preserve all bindings explicitly:

```text
AdvancementNeedConsiderationEvidence
- evidence_ref
- source_ref
- need_set_id
- selection_id
- goal_establishment_id
- horizon_id
- family
- native_projection_id
- native_standing = established
- native_need_item_ref or native_need_item_fingerprint
- evidence_state:
    exact_need_identity
    missing_need_identity
    ambiguous
    conflict
    Unknown
```

A lawful `AdvancementNeedConsiderationSelection` output should then preserve:

```text
selection_id
artifact_type = AdvancementNeedConsiderationSelection
need_set_id
focus_evidence_refs
focus_provenance_refs
selection_state:
  selected
  no_focus_evidence
  missing_need_identity
  ambiguous
  conflict
  need_set_mismatch
  selection_identity_mismatch
  goal_identity_mismatch
  horizon_identity_mismatch
  family_mismatch
  projection_mismatch
  absent_need_record
  unsupported_standing
  excluded_family
selected_family: optional
selected_native_projection_id: optional
selected_native_need_item_ref: optional
selected_native_need_item_fingerprint: optional
non_selected_established_need_refs
ambiguous_need_refs
missing_identity_evidence_refs
unknowns
conflicts
read_only=true
orders_needs=false
prioritizes_needs=false
declares_primary_blocker=false
selects_resolution=false
selects_route=false
selects_next_action=false
opens_inquiry=false
requests_clarification=false
requests_authority=false
selects_authority_source=false
selects_realization=false
authorizes_work=false
starts_execution=false
starts_recording=false
writes_event_ledger=false
mutates_cluster=false
```

The binding check is conjunctive. A focus record that names the right item ref under the wrong `need_set_id`, selected goal, horizon, family, or projection must not be repaired by textual similarity. The output should preserve the mismatch state and leave every established need unselected.

## Preservation of missing identity, ambiguity, conflict, and absent need records

### Missing identity

Missing identity exists when focus evidence points to a topic, family, presentation label, sufficiency conclusion, reason kind, or unresolvedness generally, but not to one exact native established need item.

Required preservation:

```text
selection_state: missing_need_identity
selected_native_need_item_ref: none
missing_identity_evidence_refs: (...)
non_selected_established_need_refs: all established candidates unchanged
```

### Ambiguity

Ambiguity exists when focus evidence names multiple candidate records or an underspecified family/projection containing multiple established native needs.

Required preservation:

```text
selection_state: ambiguous
selected_native_need_item_ref: none
ambiguous_need_refs: (...)
non_selected_established_need_refs: all established candidates unchanged
```

A family with exactly one established need is still not selected unless the focus evidence identifies that exact need. Uniqueness may make an adapter easier to present, but it is not selection evidence at this boundary.

### Conflict

Conflict exists when explicit focus records name incompatible exact needs, bind the same native item to incompatible goal/horizon/projection identities, or inherit conflicting upstream selection evidence.

Required preservation:

```text
selection_state: conflict
selected_native_need_item_ref: none
conflicts: (...)
non_selected_established_need_refs: all established candidates unchanged
```

Conflict is not resolved by family order, sufficiency dominance, severity, or wording similarity.

### Absent need record

Absent record exists when focus evidence names a family, projection, standing bucket, or item identity that is not present as an established item in the supplied native projection preserved by the exact `GoalAdvancementNeedSet`.

Required preservation:

```text
selection_state: absent_need_record
selected_native_need_item_ref: none
missing_or_absent_need_ref: named identity
non_selected_established_need_refs: all established candidates unchanged
```

A need may be discussed by the operator, but it cannot be selected by this boundary unless the repository has already established and preserved it as an exact native need record in the current need set.

## May unsupported, unknown, conflicting, or excluded-family records be selected?

No, not as `AdvancementNeedConsiderationSelection` under this boundary.

The target is an exact established advancement need. Therefore:

- `unsupported` records are evidence that the family did not establish the need;
- `unknown` records are preserved uncertainty, not established need identity;
- `conflicting` records are preserved incoherence, not a selectable need to resolve;
- `excluded_family` and `outside_current_scope` records are out of the current bounded horizon;
- `unclassified_here` and `unclassified` records are not native established needs for this owner;
- absent family records are not selectable.

The selection artifact may preserve that the operator focused one of those records, but the lawful result is a non-selected state such as `unsupported_standing`, `unknown_standing`, `conflict`, `excluded_family`, or `absent_need_record`, not `selected`.

## Does an existing owner already perform this selection?

No.

Existing owners are adjacent but stop before this responsibility:

- Native need projections classify family-owned testimony into standing buckets, but do not select one established record for present consideration.
- `GoalAdvancementNeedSet` preserves supplied native projections as an unordered set and explicitly refuses priority, blocker, route, next action, inquiry opening, authority request, realization selection, authorization, execution, recording, event-ledger writing, and mutation.
- `GoalAdvancementSufficiencyProjection` combines need and coverage standings into a bounded sufficiency conclusion while preserving unordered reasons; it does not select, rank, route, authorize, or execute.
- `GoalInquiryConsiderationSelection` selects one bounded goal from exact focus evidence, but its target is a goal, not a native advancement need record.

No reviewed owner consumes one `GoalAdvancementNeedSet` plus explicit exact need-focus evidence and emits a read-only `AdvancementNeedConsiderationSelection` over exactly one established native need record.

## Smallest missing responsibility

The smallest missing responsibility is:

```text
Preserve explicit operator focus on one exact established native advancement need record already present in one exact `GoalAdvancementNeedSet`, while proving that no priority, primary blocker, resolution, route, next action, inquiry opening, clarification request, authority request, realization selection, authorization, execution, recording, event-ledger write, or mutation occurred.
```

This responsibility sits after native need projection and need-set assembly, and before any family-specific resolution, inquiry-frontier opening, authority request, realization selection, routing, or execution boundary.

## Is one read-only implementation slice warranted?

Yes, one narrow read-only implementation slice is warranted if Seed needs this boundary to become executable rather than only described.

The slice should be smaller than a planner, priority queue, inquiry opener, clarification requester, authority requester, realization selector, or movement authorizer. It should add only:

- a stable native need item identity or precise fingerprinting rule for the four native projection item types;
- `AdvancementNeedConsiderationEvidence` records that can carry exact item identity plus need-set, selected-goal, horizon, family, and native-projection binding;
- an `AdvancementNeedConsiderationSelection` artifact;
- a selector over one `GoalAdvancementNeedSet` and explicit focus evidence;
- tests proving exact established need selection;
- tests proving missing identity, ambiguity, conflict, absent records, unsupported/unknown/conflicting/excluded standings, mismatched goal/horizon/family/projection, uniqueness, family order, and sufficiency conclusion do not select;
- tests proving inquiry need selection does not open inquiry;
- tests proving authority and operational-realization need selection does not request authority, select realization, authorize, execute, record, write the event ledger, or mutate cluster state.

The implementation should not expose a CLI diagnostic unless explicitly requested. If exposed as a diagnostic, audit, probe, view, operational CLI flag, or recordable output, the repository operational visibility contract requires diagnostic inventory registration, diagnostic shape-audit specs, and tests for both surfaces.

## Exact next bounded question

```text
What is the minimal read-only `AdvancementNeedConsiderationSelection` schema and selector that consumes one exact `GoalAdvancementNeedSet` plus explicit exact need-focus evidence, selects exactly one established native need item already preserved in that need set, and preserves missing identity, ambiguity, conflict, absent records, unsupported/unknown/conflicting/excluded standings, and non-selected needs without ranking, resolving, routing, opening inquiry, requesting authority, selecting realization, authorizing, executing, recording, writing the event ledger, or mutating state?
```

## Conclusion

Lawful advancement-need consideration selection requires explicit focus evidence that identifies one exact established native need record already present in the exact `GoalAdvancementNeedSet`. The evidence must bind to the same need set, selected goal, bounded horizon, family, native projection, standing bucket, and need item identity. Selection for consideration is not priority, primary blocker designation, resolution selection, route selection, next-action selection, inquiry opening, clarification request, authority request, realization selection, authorization, execution, recording, event-ledger writing, or mutation. Unsupported, unknown, conflicting, excluded-family, outside-current-scope, unclassified, and absent records cannot be selected as established needs. Missing identity, ambiguity, conflict, mismatches, absent records, and non-selected established needs must remain visible and unchanged.

Advancement need consideration selection audit complete.
