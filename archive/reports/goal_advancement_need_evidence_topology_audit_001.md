# Goal Advancement Need Evidence Topology Audit 001

## Question

Determine what existing stage-owned artifacts may lawfully testify to each advancement-need family for one selected bounded goal:

```text
GoalInquiryConsiderationSelection
+
BoundedAdvancementHorizon
+
stage-owned need evidence
→ GoalAdvancementNeedSet
```

The candidate need families are:

```text
clarification
inquiry
authority
operational realization
```

This audit also determines what bounded coverage evidence would be required before absence of unresolved needs may support:

```text
sufficient_for_now
```

Repository authority wins. This audit does not implement need resolution, sufficiency judgment, inquiry creation, authority requests, realization selection, scheduling, authorization, or execution.

## Guardrails preserved

The lawful topology must preserve these separations:

```text
need kind
!= epistemic standing
!= blocked/reachable state

clarification need
!= inquiry need
!= authority need
!= operational-realization need

no visible need
!= sufficient_for_now

GoalAdvancementNeedSet
!= planner
!= router
!= priority order
!= next-action selection
```

A generic assembler may preserve and assemble need records only when stage owners have already established the evidence. It must not infer needs from goal wording, absent fields, missing downstream artifacts, topic similarity, labels, inventory uniqueness, or downstream silence.

## Evidence reviewed

- `seed_runtime/goal_inquiry_consideration_selection.py`
- `goal_inquiry_consideration_selection_slice_001.md`
- `goal_inquiry_consideration_selection_audit_001.md`
- `seed_runtime/bounded_operator_goal_establishment.py`
- `goal_advancement_need_audit_001.md`
- `seed_runtime/operational_realization_selection.py`
- `seed_runtime/operational_realization_warrant.py`

## Selected bounded goal boundary

`GoalInquiryConsiderationSelection` is the lawful selector for this audit's bounded target, but only in the narrow sense of selecting one visible bounded goal for inquiry consideration. It consumes explicit focus evidence naming exact bounded-goal identities. Its boundary notes refuse priority, activation, inquiry opening, frontier movement, work authorization, execution, recording, and mutation.

The selected goal's stage-owned state remains `BoundedOperatorGoalEstablishment`. That artifact owns the selected goal's identity, establishment state, intended outcome, known scope, unresolved scope, sufficiency conditions, sufficiency state, stop conditions, operator acceptance provenance, operator constraints, unknowns, ambiguities, conflicts, known loss, upstream lineage, and non-authority flags. Its boundary notes preserve that a goal being established is not inquiry opened, resources observed, constraints satisfied, work authorized, or goal satisfied.

Therefore a lawful `GoalAdvancementNeedSet` cannot start from goal wording alone. It must be anchored by:

1. one `GoalInquiryConsiderationSelection` in `selected` state;
2. exactly one matching `BoundedOperatorGoalEstablishment.goal_establishment_id`;
3. an explicit bounded advancement horizon describing which present movement boundary is being considered;
4. zero or more need records established by the stage owners of clarification, inquiry, authority, and operational-realization evidence.

## BoundedAdvancementHorizon responsibility

No reviewed implementation already provides a `BoundedAdvancementHorizon` artifact by that name. The responsibility is nevertheless required if absence of unresolved needs is to mean anything bounded rather than global.

A lawful horizon would preserve:

- `horizon_id`;
- `selected_goal_establishment_id`;
- `selection_ref`;
- `goal_establishment_ref`;
- `movement_boundary_ref` or equivalent statement of the exact present advancement boundary under review;
- scope limits, time/current-state limits, and evidence-snapshot references;
- included need families, excluded need families, and exclusion reasons;
- stale, unavailable, or out-of-scope evidence markers;
- non-authority flags: `read_only=true`, `selects_next_action=false`, `prioritizes=false`, `opens_inquiry=false`, `requests_authority=false`, `selects_operational_realization=false`, `authorizes_transition=false`, `starts_execution=false`, `judges_goal_satisfaction=false`, `writes_event_ledger=false`, `mutates_cluster=false`.

The horizon is not the need set and is not a sufficiency judgment. It bounds what coverage was checked, which evidence snapshots were in scope, and which present movement boundary the need records may speak about.

## Which existing artifacts can testify to each need family?

### Clarification need

Clarification need is operator-meaning, scope, acceptance, or goal-boundary deficient. Existing testimony may come from `BoundedOperatorGoalEstablishment` fields such as:

- `establishment_state` and `establishment_reason` when the goal is refused or only provisional because orientation is not resolved;
- `unresolved_scope` where the unresolved item concerns operator-facing goal scope;
- `intended_outcome` and `outcome_resolution` when the intended outcome is absent, unsupported, or only provisionally interpreted;
- `sufficiency_conditions`, `sufficiency_state`, and `stop_conditions` when acceptance or stop criteria are missing or unclear;
- `operator_acceptance_provenance` when acceptance provenance is absent or insufficient for the current boundary;
- `operator_constraints` when stated constraints cannot be interpreted;
- `ambiguities`, `conflicts`, `unknowns`, and `known_loss` where the unresolved matter belongs to operator meaning rather than repository investigation.

`GoalInquiryConsiderationSelection` may also testify to pre-goal-selection clarification-like defects through `missing_goal_identity_evidence_refs`, `ambiguous_goal_refs`, `unknowns`, and `conflicts`, but once the selected bounded goal exists these are selection-boundary evidence, not a license to rewrite the selected goal.

### Inquiry need

Inquiry need is repository/world/evidence deficient after the selected goal is sufficiently identified for the horizon. Existing testimony may come from:

- `BoundedOperatorGoalEstablishment.unknowns` when the unknown concerns repository facts or observations required for bounded understanding;
- `unresolved_scope` where the unresolved item is investigable repository evidence rather than operator intent;
- `conflicts` where incompatible repository evidence must be investigated rather than clarified with the operator;
- `known_loss` where loss of source detail prevents bounded understanding;
- inventory-visible inquiry references and conflicting or unknown association material when tied to the selected goal by an owning artifact;
- downstream reachability, projection, or support artifacts only when those stage owners explicitly preserve unknown, unsupported, or conflicting evidence for the selected boundary.

Inquiry need is not established merely because a goal exists, because an inquiry could be opened, or because no downstream realization has been produced.

### Authority need

Authority need is permission, scope, policy, or authority-standing deficient for movement. Existing testimony may come from:

- goal-owned `operator_constraints` when they establish a movement boundary requiring authority rather than clarification;
- explicit non-authority flags on `GoalInquiryConsiderationSelection` and `BoundedOperatorGoalEstablishment`, which prove that selection and establishment did not authorize work;
- operational-realization candidate, selection, or warrant evidence only where a stage owner preserves `authority_standing`, `allowed_authority_standings`, authority-related constraints, unavailable authority, or authority conflicts;
- separate repository authority or approval artifacts if tied to the exact selected goal and horizon.

Non-authority flags are negative boundary evidence: they prove no authorization occurred. They do not by themselves prove `authority_needed`; an owner must testify that authority is required for the bounded movement and is missing, unavailable, conflicted, or out of scope.

### Operational-realization need

Operational-realization need is mechanism, representation, dependency, or implementation-route deficient after goal meaning, evidence, and authority boundaries are sufficiently bounded for considering mechanics. Existing testimony may come from operational-realization stage owners:

- `OperationalRealizationSelection.selection_state`, `selection_reason`, `eligible_candidate_references`, `blocked_candidate_references`, `unsupported_candidate_references`, `unknown_candidate_references`, `conflicting_candidate_references`, `policy_unknowns`, and `policy_conflicts`;
- `OperationalRealizationWarrant.warrant_state`, `warrant_reason`, `grammar_support`, `behavioral_support`, `representation_support`, `methodological_support`, `mechanism_standing`, `dependency_standing`, `authority_standing`, `supporting_basis_references`, `known_limitations_or_loss`, `unknowns`, and `conflicts`;
- candidate-realization artifacts only when their own standing fields are explicitly bound to the exact demand and current horizon.

The need set may preserve that operational realization is needed or missing. It may not select a realization, warrant reliance, construct invocation, translate representation, authorize, schedule, emit, or execute.

## Fields that distinguish kind, standing, and resolution state

A need record should keep these dimensions separate:

| Dimension | Meaning | Example field names |
| --- | --- | --- |
| Need kind | Which family owns the missing boundary. | `need_kind: clarification | inquiry | authority | operational_realization` |
| Epistemic standing | How strong the testimony is. | `standing: established | supported | provisional | unknown | conflict | unsupported` |
| Resolution state | Whether the need is still open for this horizon. | `resolution_state: unresolved | resolved_for_horizon | refused | superseded | out_of_scope | stale` |
| Blocking/reachability state | Whether movement is blocked or reachable under a separate owner. | `movement_state`, `reachability_state`, `blocked_by_refs` |
| Evidence ownership | Which stage produced the testimony. | `owner_stage`, `evidence_refs`, `source_artifact_refs` |
| Horizon binding | The selected goal and bounded movement for which it speaks. | `selected_goal_establishment_id`, `horizon_id`, `movement_boundary_ref` |

This prevents unsafe collapses such as:

```text
need_kind=inquiry + standing=unknown -> clarification_needed
need_kind=authority + resolution_state=unresolved -> blocked by default
reachable operational realization -> authorization granted
no operational-realization record -> operational-realization need
```

## May several need records coexist without priority?

Yes. Need families are not exclusive states. A single bounded goal may lawfully carry several unresolved need records for the same horizon, for example:

- clarification need plus inquiry need when goal scope is ambiguous and repository facts are also unknown;
- authority need plus operational-realization need when permission and mechanism readiness are both deficient;
- inquiry need plus authority need when the required observation is known but currently unauthorized;
- conflict standing on one family and unknown standing on another.

`GoalAdvancementNeedSet` must preserve coexistence as an unordered set. If a display layer later wants a headline state, that display headline must not erase the unordered records or become a priority, router, planner, or next-action selector.

## What bounded coverage is required before `sufficient_for_now`?

`no visible need` is not enough. `sufficient_for_now` requires positive bounded coverage evidence and negative unresolved-need evidence for the exact selected goal and horizon.

Minimum coverage evidence:

1. **Selection coverage:** one selected `GoalInquiryConsiderationSelection`, with exactly one selected goal identity and no selection mismatch, ambiguity, or conflict relevant to the horizon.
2. **Goal identity coverage:** one matching `BoundedOperatorGoalEstablishment`, with the selected `goal_establishment_id` matching the supplied goal artifact.
3. **Horizon coverage:** an explicit `BoundedAdvancementHorizon` naming the current movement boundary, evidence snapshots, included families, excluded families, stale evidence, and out-of-scope areas.
4. **Clarification-family coverage:** the clarification owner says no unresolved operator-meaning, scope, sufficiency, stop, acceptance, ambiguity, or conflict need remains for this horizon, or marks any remaining item out of scope with reason.
5. **Inquiry-family coverage:** the inquiry/evidence owner says no unresolved repository-evidence, observation, support, unknown, or conflict need remains for this horizon, or marks any remaining item out of scope with reason.
6. **Authority-family coverage:** the authority owner says required authority for this bounded movement is available or not required, and no unresolved authority conflict remains for this horizon.
7. **Operational-realization-family coverage:** the operational-realization owner says no mechanism, representation, dependency, candidate selection, or warrant gap remains for the movement boundary under review, or the horizon proves that operational realization is not in scope.
8. **Freshness and provenance coverage:** each family record cites current evidence snapshots or explicitly preserves staleness and non-coverage.
9. **Non-authority coverage:** the resulting need set preserves that `sufficient_for_now` is not goal satisfaction, transition authorization, scheduling, execution, or cluster mutation.

Only after those coverage records exist may absence of unresolved needs support `sufficient_for_now`. Even then, it means sufficient for the present bounded horizon, not permanently satisfied.

## Does an existing owner assemble these records?

No reviewed owner assembles `GoalAdvancementNeedSet` records in this topology.

Adjacent owners exist:

- `GoalInquiryConsiderationSelection` selects one visible bounded goal for consideration and refuses priority, activation, inquiry opening, authorization, execution, recording, and mutation.
- `BoundedOperatorGoalEstablishment` owns bounded goal identity and goal-state evidence but does not assemble advancement-need records.
- The prior `goal_advancement_need_audit_001.md` establishes a read-only projection boundary, but it treats the earlier vocabulary partly as projection states and does not implement a stage-owned, coexisting, unordered need-record topology.
- `OperationalRealizationSelection` and `OperationalRealizationWarrant` own downstream realization selection and warrant evidence, while refusing authorization, scheduling, and execution.

## Smallest missing responsibility

The smallest missing responsibility is a read-only assembler that consumes:

```text
GoalInquiryConsiderationSelection(selected)
+
matching BoundedOperatorGoalEstablishment
+
BoundedAdvancementHorizon
+
stage-owned need evidence records
```

and emits an unordered `GoalAdvancementNeedSet` that preserves:

- selected goal identity;
- horizon identity and coverage boundaries;
- each stage-owned need record without reclassification by wording or absence;
- need kind separately from epistemic standing and resolution state;
- coexisting needs without priority;
- coverage insufficiency when a family has not testified;
- explicit non-planning and non-authority flags.

The assembler's missing responsibility is preservation and bounded coverage accounting, not inference. It should be able to say `coverage_insufficient_for_sufficient_for_now` when a family has not testified.

## Is one implementation slice warranted?

One implementation slice is warranted only if Seed needs this answer to be executable rather than documented. The slice should be smaller than the prior proposed `GoalAdvancementNeedProjection`: it should implement records and coverage preservation, not a planner-like state classifier.

A minimal executable slice would introduce:

- `BoundedAdvancementHorizon` as a read-only evidence-scope artifact;
- `GoalAdvancementNeedRecord` with `need_kind`, `standing`, `resolution_state`, `owner_stage`, `evidence_refs`, and horizon binding;
- `GoalAdvancementNeedSet` as an unordered assembler over existing records;
- validation that `sufficient_for_now` cannot be emitted unless all in-scope families have current coverage and no unresolved need records;
- tests proving coexistence, no inference from missing records, no priority, and no authorization/execution side effects.

The implementation should not expose a CLI diagnostic unless explicitly requested. If exposed as a diagnostic, audit, probe, view, operational CLI flag, or recordable output, the repository operational visibility contract requires diagnostic inventory and shape-audit updates plus tests.

## Exact next bounded question

```text
What is the minimal read-only `BoundedAdvancementHorizon` and unordered `GoalAdvancementNeedSet` artifact pair that consumes one selected `GoalInquiryConsiderationSelection`, one matching `BoundedOperatorGoalEstablishment`, and stage-owned clarification, inquiry, authority, and operational-realization need records, preserves need kind separately from standing and resolution state, refuses to infer needs from absent evidence, and proves `sufficient_for_now` only when every in-scope need family has current bounded coverage with no unresolved records?
```

## Conclusion

Existing artifacts can lawfully testify to advancement-need families only within their owned boundaries. `BoundedOperatorGoalEstablishment` can testify to selected-goal meaning, scope, sufficiency, stop, unknown, ambiguity, conflict, and loss evidence. `GoalInquiryConsiderationSelection` can testify to exact selected-goal identity and selection-boundary defects. Operational-realization selection and warrant artifacts can testify to mechanism, representation, dependency, authority-standing, support, unknown, and conflict evidence for downstream realization boundaries. Authority need requires an authority owner or authority-specific fields; non-authority flags prove lack of authorization but do not alone establish an authority need.

The repository does not currently show an owner that assembles stage-owned need records into an unordered `GoalAdvancementNeedSet` under an explicit `BoundedAdvancementHorizon`. The smallest missing responsibility is bounded preservation and coverage accounting, not planning, routing, priority, next-action selection, resolution, sufficiency judgment, authorization, or execution. One narrow implementation slice is warranted only if this topology must become executable.

Goal advancement need evidence topology audit complete.
