# Advancement Need Family Coverage Audit 001

## Question

Determine the lawful boundary:

```text
BoundedAdvancementHorizon
+
stage-owned need projections
+
stage-owned coverage testimony
→ AdvancementNeedFamilyCoverageSet
```

The question is not whether Seed can assemble `GoalAdvancementNeedSet`; current implementation already preserves supplied, absent, and excluded stage-owned need projections. The question is what additional evidence proves that the clarification, inquiry, authority, and operational-realization families have completely examined their horizon-relevant candidate space for one exact bounded horizon.

Repository authority wins. This audit is documentary only. It does not implement a diagnostic surface, CLI flag, recordable output, sufficiency judgment, inquiry opening, authority request, realization selection, authorization, execution, event-ledger writing, cluster mutation, or state mutation.

## Guardrails preserved

```text
projection supplied
!= family coverage complete

no established need
!= no unresolved need

absent testimony
!= complete coverage

excluded family
requires explicit horizon reason

coverage complete
!= sufficient_for_now
```

Completeness must not be inferred from empty projections, successful tests, absence of evidence, the presence of all four native family projections, horizon inclusion, or a `GoalAdvancementNeedSet` record with disposition `supplied`.

## Evidence reviewed

- `seed_runtime/bounded_advancement_horizon.py`
- `seed_runtime/goal_advancement_need_set.py`
- `seed_runtime/clarification_need_projection.py`
- `seed_runtime/inquiry_need_projection.py`
- `seed_runtime/authority_need_projection.py`
- `seed_runtime/operational_realization_need_projection.py`
- `tests/test_bounded_advancement_horizon.py`
- `tests/test_goal_advancement_need_set.py`
- `tests/test_clarification_need_projection.py`
- `tests/test_inquiry_need_projection.py`
- `tests/test_authority_need_projection.py`
- `tests/test_operational_realization_need_projection.py`
- `goal_advancement_need_evidence_topology_audit_001.md`

## Current implemented boundary

### Bounded advancement horizon

`BoundedAdvancementHorizon` is the selected-goal and evidence-snapshot boundary for the current movement question. It preserves `selection_id`, `selected_goal_establishment_id`, `goal_establishment_id`, a required `present_movement_boundary`, included and excluded scope, evidence snapshot references, time and current-state bounds, potentially relevant need families, explicitly excluded need families, unknowns, conflicts, stale evidence, unavailable evidence, and negative authority/mutation flags.

The horizon implementation refuses unresolved selection, goal identity mismatch, refused goal artifacts, missing movement boundary, and excluded need families lacking reasons. Its boundary notes explicitly say it is not the goal, not need classification, not sufficiency judgment, and that included need family means potentially relevant to preserve rather than that a need exists.

Therefore the horizon is necessary for family coverage, but not itself coverage testimony. It binds the candidate space and evidence snapshot for later family testimony.

### Native need projections

The four family projections are already stage-owned need projections, not family-coverage artifacts.

| Family | Native projection | What it consumes | What it refuses |
| --- | --- | --- | --- |
| Clarification | `ClarificationNeedProjection` | explicit component-bounded operator-meaning uncertainty testimony | generic unresolved material, family hints, mixed prose, unresolved goal fields, question wording, inquiry opening, action selection, authorization, execution, recording, mutation |
| Inquiry | `InquiryNeedProjection` | explicit component-bounded repository/world uncertainty testimony | generic unknowns, absent artifacts, stale evidence by itself, observation authorization, inquiry opening, sufficiency judgment, execution, recording, mutation |
| Authority | `AuthorityNeedProjection` | explicit component-bounded authority requirement testimony joined to authority standing testimony | generic blockers, denied execution, absent observations, candidate-local authority blockers by themselves, authority request, permission grant, scope expansion, authorization, execution, recording, mutation |
| Operational realization | `OperationalRealizationNeedProjection` | explicit requirement and standing testimony for operational-realization components | missing selection, no candidate, one blocked candidate, authority failure, downstream silence, realization selection, warrant, representation translation, invocation preparation, authority request, authorization, execution, recording, mutation |

A native projection may contain zero established items and still not prove coverage. It only classifies the testimony it received.

### Goal advancement need set

`GoalAdvancementNeedSet` assembles supplied native projections for the exact horizon and preserves absent and excluded families. It detects projection identity mismatch against the horizon and can refuse mismatched projections. Its boundary notes preserve supplied, absent, and excluded families as distinct and deny priority, route, next action, sufficiency judgment, inquiry opening, authority request, realization selection, authorization, execution, recording, event-ledger writing, and cluster mutation.

That assembler is intentionally not a coverage owner. A `supplied` disposition means the projection artifact was present and identity-checked; it does not mean the family examined every relevant component.

## Lawful coverage artifact

A separate read-only artifact is warranted conceptually:

```text
AdvancementNeedFamilyCoverageSet
```

It would consume:

```text
BoundedAdvancementHorizon
+
zero or one native need projection per in-scope family
+
explicit coverage testimony from the owner of each family
```

It would emit one unordered coverage record per family, not one overall sufficiency result.

Minimum artifact identity:

```text
coverage_set_id
artifact_type = AdvancementNeedFamilyCoverageSet
selection_id
selected_goal_establishment_id / goal_establishment_id
horizon_id
present_movement_boundary
evidence_snapshot_refs
family_coverage_records
unknowns
conflicts
read_only=true
```

Minimum negative flags:

```text
judges_sufficiency=false
sufficient_for_now=None
classifies_need=false
selects_next_action=false
prioritizes=false
opens_inquiry=false
requests_authority=false
selects_realization=false
authorizes_work=false
starts_execution=false
starts_recording=false
writes_event_ledger=false
mutates_cluster=false
```

The artifact may preserve all four family coverage records together because co-preservation is not sufficiency judgment. It must not collapse them into `sufficient_for_now`, a blocker, a priority order, a route, or a selected next action.

## Which stage owns coverage testimony for each family?

Coverage testimony belongs to the same bounded stage that owns the family-specific candidate space, not to the generic need-set assembler.

| Family | Coverage owner | Reason |
| --- | --- | --- |
| Clarification | Operator-meaning / goal-establishment clarification owner | Only this owner can say it examined horizon-relevant operator meaning, scope, intended outcome, acceptance, stop, ambiguity, conflict, unknown, and known-loss components. |
| Inquiry | Repository/world uncertainty or inquiry-evidence owner | Only this owner can say it examined horizon-relevant repository/world subjects, observations, support gaps, evidence freshness, evidence availability, unknowns, conflicts, and known loss. |
| Authority | Authority requirement and authority standing owner | Only this owner can say it examined required authority classes, applicable scopes, requirement standing, authority standing, materiality, and authority conflicts for the movement boundary. |
| Operational realization | Operational-realization requirement and standing owner | Only this owner can say it examined required transformations, applicable scope, candidate/mechanism/representation/dependency/behavior/selection/warrant components, availability, coverage standing, and blocker-family ownership for the horizon. |

`BoundedAdvancementHorizon` owns horizon bounds and exclusion reasons. `GoalAdvancementNeedSet` owns preservation of projections. Neither owns family completeness.

## Component or candidate space each family must account for

### Clarification family

The clarification coverage record must account for all horizon-relevant operator-meaning components exposed by the selected bounded goal and selected movement boundary:

- goal identity and source binding already selected for the horizon;
- intended outcome and its resolution;
- operator-facing scope, unresolved scope, and excluded scope;
- sufficiency conditions, sufficiency state, and stop conditions where they affect current movement meaning;
- operator acceptance provenance;
- operator constraints that need interpretation rather than authority evaluation;
- ambiguities, conflicts, unknowns, and known loss that belong to operator meaning;
- any component explicitly excluded from clarification coverage, with horizon reason.

Completeness requires testimony that this finite component list, or an explicitly enumerated equivalent list, was examined for the exact horizon. No established clarification need means only that examined testimony did not establish one; it is not complete coverage unless the covered components are named.

### Inquiry family

The inquiry coverage record must account for all horizon-relevant repository/world subjects and evidence components:

- repository facts, observations, and source materials required for bounded understanding of the selected movement boundary;
- unresolved scope that is investigable rather than operator-facing;
- repository/world unknowns and conflicts;
- support gaps, stale evidence, unavailable evidence, and known loss;
- required evidence freshness and availability for the horizon;
- any relevant inquiry or observation subject explicitly excluded, with horizon reason.

Completeness requires explicit testimony that the inquiry owner examined the bounded subject set against the horizon evidence snapshots. It is not inferred from no unknowns, no conflicts, or current test success.

### Authority family

The authority coverage record must account for all horizon-relevant authority dimensions:

- every required authority class for the current movement boundary;
- applicable scope for each authority class;
- requirement standing: required, not required, unknown, or conflicting;
- authority standing: available, unavailable, unknown, conflicting, or outside current scope;
- scope applicability and horizon materiality;
- selected authority source, if any, without granting authority;
- authority conflicts and authority-related known loss;
- any authority class or scope explicitly excluded, with horizon reason.

Completeness requires paired coverage over requirement and standing candidate space. Negative non-authority flags on other artifacts prove lack of authorization, but they do not prove that all authority classes were examined.

### Operational-realization family

The operational-realization coverage record must account for all horizon-relevant realization components:

- required transformation for the movement boundary;
- applicable scope;
- requirement standing;
- candidate existence or candidate-space boundary;
- mechanism, representation, grammar, behavior, methodology, dependency, reachability, selection, and warrant components when material to the movement;
- availability standing;
- coverage standing over the realization candidate space;
- blocker-family ownership so authority, clarification, inquiry, generic, unknown, and conflicting blockers are not misclassified as realization need;
- any realization component explicitly excluded, with horizon reason.

The current operational-realization need projection already has a local `coverage_standing` on standing testimony. That is useful family-owned evidence, but it remains item-level need-projection input; complete family coverage still requires an artifact that accounts for the whole horizon-relevant realization candidate space and binds it to the native projection.

## Warrant for coverage standings

`AdvancementNeedFamilyCoverageSet` should preserve five coverage standings.

### `complete_for_horizon`

Warranted only when all are true:

1. the horizon is bounded and identity-matches the selected goal;
2. the family is included for this horizon and not excluded;
3. the family owner supplies explicit coverage testimony for the exact `selection_id`, `goal_establishment_id`, `horizon_id`, movement boundary, and evidence snapshot refs;
4. the testimony enumerates the horizon-relevant components or candidate-space rule used by that family;
5. every enumerated component is either examined or explicitly marked out of scope with a horizon reason;
6. coverage testimony cites, or is explicitly bound to, the native family need projection it covers;
7. no coverage testimony conflict, stale evidence conflict, or projection identity conflict remains for the family.

This standing does not imply no unresolved need and does not imply `sufficient_for_now`. It only says the family completed its examination for the bounded horizon.

### `partial`

Warranted when family-owned testimony identifies some examined components but also identifies remaining unexamined, stale, unavailable, unbounded, or out-of-scope-without-reason components.

`partial` may coexist with established, unknown, or conflicting needs in the native projection. It means coverage is incomplete, not that the family need is less severe.

### `unknown`

Warranted when the artifact cannot determine whether the family owner examined the relevant candidate space. Examples:

- no coverage testimony was supplied;
- testimony is not stage-owned;
- testimony is not bound to the horizon;
- testimony does not name components or a candidate-space rule;
- testimony does not bind to a native need projection;
- evidence snapshot binding is absent or not current enough to evaluate.

`unknown` is the lawful standing for absent testimony. It must not be upgraded to complete because a projection was supplied or empty.

### `conflicting`

Warranted when coverage testimony conflicts on material identity or scope, including:

- multiple owner testimonies disagree about whether coverage is complete;
- testimony binds to different selection, goal, horizon, or evidence snapshot IDs;
- coverage claims complete while listing unexamined required components;
- native projection identity conflicts with the horizon;
- the family owner and horizon disagree about whether a family is included or excluded;
- evidence freshness or availability conflicts prevent deciding coverage.

`conflicting` is a coverage standing, not a selected next action.

### `excluded`

Warranted only when `BoundedAdvancementHorizon.explicitly_excluded_need_families` contains the family, or its accepted alias, with a non-empty horizon reason. The excluded record should preserve:

```text
family
standing=excluded
exclusion_reason
horizon_id
selection_id
goal_establishment_id
native_projection_ref? if supplied anyway
conflict? if supplied projection asserts material in-scope coverage
```

Excluded does not mean complete and does not mean no unresolved need. It means the family is outside this bounded horizon for the explicit reason preserved by the horizon.

## Binding requirements

Each coverage record must bind to four anchors.

### Selected goal binding

The record must preserve the exact selected `selection_id` and `goal_establishment_id`. Mismatch yields `conflicting` or `unknown`; it cannot be repaired by textual similarity.

### Horizon binding

The record must preserve `horizon_id`, `present_movement_boundary`, included or excluded scope, time/current-state bounds, and evidence snapshot refs. Coverage is for one bounded horizon only and must not be reused globally.

### Evidence snapshot binding

The record must cite the same evidence snapshot refs as the horizon or explicitly preserve stale, unavailable, or extra evidence refs. Snapshot absence yields `unknown` unless the family is excluded with reason.

### Native need projection binding

Coverage must name the native projection it covers:

```text
clarification_projection_id
inquiry_projection_id
authority_projection_id
operational_realization_projection_id
```

or preserve that no native projection was supplied. This prevents a coverage artifact from becoming an alternate need classifier.

## Can one artifact preserve all four families without judging sufficiency?

Yes. One read-only `AdvancementNeedFamilyCoverageSet` can preserve four independent family coverage records because the act of co-preservation is not a sufficiency judgment.

The lawful shape is unordered and per-family:

```text
family
owner_stage
coverage_standing
covered_component_refs
unexamined_component_refs
excluded_component_refs + reasons
coverage_testimony_refs
native_need_projection_id
identity_conflicts
unknowns
conflicts
```

The artifact must not compute `sufficient_for_now`, select the next family to resolve, rank family urgency, route work, open inquiry, request authority, select realization, authorize, execute, record, or mutate state.

## Does an existing owner already perform this responsibility?

No.

Adjacent owners exist, but none performs complete family coverage accounting:

- `BoundedAdvancementHorizon` establishes the selected horizon, evidence snapshots, relevant families, and explicit family exclusions.
- Family need projections classify supplied family-owned need testimony.
- `OperationalRealizationNeedProjection` preserves item-level realization `coverage_standing`, but only as one dimension in realization need conclusion.
- `GoalAdvancementNeedSet` preserves supplied, absent, and excluded family projections and projection identity conflicts.

No existing implementation consumes separate coverage testimony for all four families and emits per-family `complete_for_horizon`, `partial`, `unknown`, `conflicting`, or `excluded` standings bound to both horizon and native projection.

## Smallest missing responsibility

The smallest missing responsibility is not another need projection and not a sufficiency gate. It is a read-only coverage accountant that:

1. accepts one bounded horizon;
2. accepts zero or one native projection per family;
3. accepts explicit coverage testimony from each family owner;
4. validates selection, goal, horizon, evidence snapshot, and native projection identity;
5. preserves one coverage standing per family;
6. preserves component/candidate-space accounting for complete and partial standings;
7. preserves absent testimony as `unknown`;
8. preserves horizon exclusions as `excluded` only with explicit reason;
9. refuses to classify needs or judge sufficiency.

## Is one read-only implementation slice warranted?

Yes, one narrow read-only implementation slice is warranted if Seed needs executable evidence that supplied projections are not being mistaken for family-complete coverage.

The slice should introduce only:

- `AdvancementNeedFamilyCoverageTestimony` records, stage-owned and family-specific;
- `AdvancementNeedFamilyCoverageRecord` records with the five coverage standings;
- `AdvancementNeedFamilyCoverageSet` assembler;
- tests proving supplied projection does not imply complete coverage;
- tests proving empty projection does not imply complete coverage;
- tests proving absent coverage testimony yields `unknown`;
- tests proving excluded family requires explicit horizon reason;
- tests proving complete coverage does not set `sufficient_for_now`;
- tests proving identity and native-projection mismatches produce conflicts or unknowns;
- tests proving all negative authority, execution, recording, event-ledger, and mutation flags remain false.

No public diagnostic CLI is warranted by this audit alone. If a future change exposes the artifact through a diagnostic, audit, probe, view, operational CLI flag, or recordable output, the repository operational visibility contract applies.

## Exact next bounded question

```text
What is the smallest read-only `AdvancementNeedFamilyCoverageSet` schema and assembler that consumes one `BoundedAdvancementHorizon`, zero or one native need projection for each family, and explicit stage-owned coverage testimony, then preserves per-family `complete_for_horizon`, `partial`, `unknown`, `conflicting`, or `excluded` standings without classifying needs, judging `sufficient_for_now`, selecting a next action, requesting authority, selecting realization, authorizing, executing, recording, writing the event ledger, or mutating state?
```

## Conclusion

The lawful boundary is a separate coverage layer after horizon establishment and native need projection assembly. The horizon owns exact bounded scope and exclusion reasons. Native projections own family need testimony classification. The coverage layer would own only whether each family owner has accounted for the complete horizon-relevant component or candidate space for that exact horizon and native projection.

Projection supplied is not coverage complete. No established need is not no unresolved need. Absent testimony is unknown coverage. Exclusion requires explicit horizon reason. Complete family coverage remains distinct from `sufficient_for_now`.

Advancement need family coverage audit complete.
