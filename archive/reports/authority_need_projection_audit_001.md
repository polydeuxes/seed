# Authority Need Projection Audit 001

## Bounded question

What evidence lawfully establishes that authority is required for the exact present movement and that the current authority standing creates an unresolved need, without requesting, choosing, granting, or exercising authority?

## Short answer

Seed does not currently have an implemented `AuthorityNeedProjection` owner parallel to `ClarificationNeedProjection` and `InquiryNeedProjection`. The lawful projection is recoverable from existing patterns, but only as a narrowly bounded read-only responsibility:

```text
BoundedAdvancementHorizon
+
component-bounded authority-requirement testimony
+
authority-standing testimony
→ AuthorityNeedProjection
```

The projection may establish an authority need only when both sides are explicit and bound to the same selected goal, bounded component, and advancement horizon:

1. **Requirement testimony** says the exact present movement requires a named authority class or authority source class.
2. **Standing testimony** says the current authority standing for that same authority class, component, scope, and horizon is unavailable, conflicted, unknown, or outside current scope.
3. **Horizon materiality** says that requirement matters to the present movement boundary, not merely to a later realization, possible inquiry, or unrelated downstream action.

No authorization occurs in this projection. Authority need established is not authority requested, not authority granted, not movement selected, not realization selected, not execution, not recording, and not state mutation.

## Existing artifacts that may testify to authority requirements

### BoundedAdvancementHorizon

`BoundedAdvancementHorizon` is the strongest existing boundary artifact for the present movement. It already binds a selected goal to one `present_movement_boundary`, included and excluded scope, evidence snapshots, potentially relevant need families, explicit exclusions, unknowns, conflicts, stale and unavailable evidence, and read-only/no-mutation flags.

Its authority-relevant contribution is **not** that authority is needed. Its contribution is the legal horizon against which a separate authority-requirement testimony can be tested. The horizon explicitly says it is not need classification, sufficiency judgment, action selection, authorization, execution, recording, or mutation.

Therefore the horizon may testify to:

- selected goal identity;
- current movement boundary;
- included and excluded scope;
- evidence snapshot membership;
- whether `authority` / `authority_need` is potentially relevant or explicitly excluded.

It may not testify by itself that authority is required.

### Component-bounded authority-requirement testimony

No current dedicated dataclass named `AuthorityRequirementTestimony` exists in the reviewed runtime. The closest implemented analogues are the testimony inputs used by clarification and inquiry projections:

- `OperatorMeaningUncertaintyTestimony` requires selection identity, goal identity, horizon identity, evidence identity, a bounded uncertainty component, an owning stage, a family discriminator, component boundedness, and materiality to the present movement.
- `RepositoryWorldUncertaintyTestimony` adds a repository/world subject and keeps inquiry standing separate from evidence freshness and evidence availability.

An authority-requirement testimony should follow this shape but should be its own family, not a reuse of clarification or inquiry testimony. It should require at least:

- `testimony_ref` and `source_ref`;
- `selection_id`;
- `goal_establishment_id`;
- `horizon_id`;
- `evidence_ref` present in the horizon snapshot set;
- `bounded_authority_component_ref`;
- `present_movement_ref` or equivalent component-to-horizon binding;
- `required_authority_ref` or `required_authority_class`;
- `requirement_standing` such as `required`, `not_required`, `unknown`, `conflicting`, or `outside_current_scope`;
- `owning_stage` and `stage_owns_authority_requirement`;
- `component_bounded=True`;
- `material_to_present_movement_boundary=True`;
- explicit notes/conflicts/unknowns.

This testimony is the only lawful source for **authority required**. Generic blockers, missing observations, denied execution, absent realizations, policy words, or downstream silence cannot substitute for it.

### Authority-standing testimony

No current dedicated dataclass named `AuthorityStandingTestimony` exists in the reviewed runtime. Existing authority-aware slices show nearby but insufficient evidence:

- candidate operational realizations carry `authority_standing` for realization candidates;
- capability reachability separately reports `authority_blockers` and `authority_reachability` while preserving that reachability is not realization selection or authorization;
- service/container ownership authority slices compare required observation authority with constrained available authority profiles.

These may be evidence sources only when transformed into explicit authority-standing testimony for the same selected goal, component, horizon, and required authority class. Candidate-level `authority_standing="unavailable"` by itself proves only candidate reachability standing, not a current authority need for the selected horizon.

Authority-standing testimony should require at least:

- `testimony_ref` and `source_ref`;
- `selection_id`;
- `goal_establishment_id`;
- `horizon_id`;
- `evidence_ref` present in the horizon snapshot set;
- `bounded_authority_component_ref` matching or lawfully joining the requirement component;
- `authority_ref` / `authority_class` matching the requirement testimony;
- `scope_ref` or `scope_applicability`;
- `authority_standing` such as `available`, `unavailable`, `conflicted`, `unknown`, or `outside_current_scope`;
- `standing_basis_refs`;
- `component_bounded=True`;
- `material_to_present_movement_boundary=True`.

This testimony is the only lawful source for **authority available / unavailable / conflicted / outside current scope**.

## What binds both testimonies to the selected goal, bounded component, and horizon

The lawful binding contract should be stricter than lexical similarity:

1. **Selection identity**: testimony `selection_id` must equal the current `GoalInquiryConsiderationSelection.selection_id`.
2. **Goal identity**: testimony `goal_establishment_id` must equal the selected `BoundedOperatorGoalEstablishment.goal_establishment_id`.
3. **Horizon identity**: testimony `horizon_id` must equal the active `BoundedAdvancementHorizon.horizon_id`.
4. **Evidence identity**: each testimony `evidence_ref` must be present in `horizon.evidence_snapshot_refs`.
5. **Component binding**: requirement and standing testimony must share the same `bounded_authority_component_ref`, or a declared relation must explicitly bind them.
6. **Authority-class binding**: the required authority class/source in the requirement testimony must match the class/source whose standing is testified.
7. **Scope applicability**: the standing testimony must be applicable to the horizon's included scope and not merely to excluded scope.
8. **Horizon materiality**: both testimonies must say they are material to the exact present movement boundary.
9. **Stage ownership**: the producing stage must explicitly own the authority-requirement or authority-standing testimony family.

Without these joins, the item should be unclassified, not promoted to authority need.

## Distinctions recovered

| Distinction | Lawful meaning | Not enough by itself |
| --- | --- | --- |
| `authority required` | Explicit requirement testimony says the present movement requires a bounded authority class/source. | No authorization occurred; a tool would need approval later; movement failed; execution was denied. |
| `authority available` | Explicit standing testimony says the required authority is currently available for the same component, scope, and horizon. | A mechanism is reachable; a policy allows another action; a credential exists somewhere. |
| `authority unavailable` | Explicit standing testimony says the required authority is unavailable for the same component, scope, and horizon. | Movement requires authority; no one has requested authority; observation is missing. |
| `authority conflicted` | Explicit standing testimony preserves incompatible standing evidence for the same authority class/component/scope/horizon. | Mixed generic blockers; disagreement about realization feasibility; unclear vocabulary. |
| `authority outside current scope` | Requirement or standing testimony says the authority question belongs outside the current horizon scope. | Authority is globally unavailable; movement is globally blocked; authority should be requested. |

The projection should be able to output, for example:

- `established`: requirement is required and standing is unavailable/conflicted/unknown in a way material to the horizon;
- `unsupported`: requirement testimony says not required, or standing says available for the required class and scope;
- `unknown`: requirement or standing is explicit but insufficient to decide;
- `conflicting`: requirement or standing evidence conflicts;
- `outside_current_scope`: requirement or standing is explicitly outside the current horizon;
- `excluded_family`: the horizon explicitly excludes authority need;
- `unclassified`: joins or family tests fail.

## Keeping requirement standing, authority standing, scope applicability, and horizon materiality separate

The projection must not collapse four independent questions:

1. **Requirement standing**: does the present movement require authority?
2. **Authority standing**: is that authority available, unavailable, conflicted, unknown, or outside scope?
3. **Scope applicability**: does the standing apply to the horizon's included scope and bounded component?
4. **Horizon materiality**: does the requirement matter to the exact present movement, not merely to a later step?

A lawful `AuthorityNeedProjectionItem` should carry these as separate fields. The need conclusion should be derived only after all four have been preserved. This prevents the forbidden collapses:

```text
no authorization occurred
!= authority need

movement requires authority
!= authority unavailable

authority unavailable
!= movement globally blocked

authority need established
!= authority requested
!= authority granted
```

## Exclusions

### Clarification components

Operator-meaning uncertainty remains owned by clarification testimony and `ClarificationNeedProjection`. Authority projection must reject testimony whose family is operator meaning, lexical ambiguity, ambiguous instruction, or clarification pressure, unless a separate authority-requirement testimony explicitly binds it.

### Inquiry components

Repository/world uncertainty remains owned by inquiry testimony and `InquiryNeedProjection`. Stale evidence, unavailable evidence, missing artifacts, unsupported facts, generic Unknowns, and absent observations do not become authority need. They may motivate inquiry only under inquiry rules.

### Realization components

Candidate realization and capability reachability may report authority standing for candidates, but they do not by themselves establish an authority need for the current horizon. Realization reachability is distinct from selection, policy authorization, and execution. A candidate authority blocker can feed authority-standing testimony only if explicitly rebound to the selected goal, bounded authority component, authority class, scope, and horizon.

### Generic blocking components

`blocked`, `failed`, denied execution, policy block, missing observation, downstream silence, or no known realization are not authority-need evidence unless an authority-requirement testimony and authority-standing testimony are both present and joined.

## Existing owner check

No reviewed implementation already performs this exact projection.

Existing owners cover adjacent boundaries:

- `BoundedAdvancementHorizon` preserves current movement horizon but explicitly does not classify needs.
- `ClarificationNeedProjection` projects operator-meaning clarification need from explicit component-bounded testimony.
- `InquiryNeedProjection` projects repository/world inquiry need from explicit component-bounded testimony and keeps freshness/availability separate.
- `CandidateOperationalRealization` and `CapabilityReachabilityProjection` preserve candidate and demand-level reachability, including authority blockers, but do not project current-horizon authority need.
- service/container ownership authority evaluators compare required observation authority with available authority profiles for their specific question families, not for the general present-movement need projection.

Therefore `AuthorityNeedProjection` is a missing sibling responsibility, not already owned by reachability, policy, execution, clarification, inquiry, or horizon construction.

## Smallest missing responsibility

The smallest missing responsibility is a read-only projector that:

1. consumes one selected goal, one bounded advancement horizon, explicit authority-requirement testimony, and explicit authority-standing testimony;
2. validates selection/goal/horizon/evidence/component/authority-class/scope/materiality joins;
3. preserves requirement standing separately from authority standing, scope applicability, and horizon materiality;
4. classifies items into established, unsupported, unknown, conflicting, outside-current-scope, excluded-family, and unclassified;
5. exposes no request/grant/authorization/execution/record/mutation behavior.

It should not select an authority source, request permission, open inquiry, select realization, invoke policy, execute, record, mutate state, or globally block movement.

## Is one read-only implementation slice warranted?

Yes. A narrow implementation slice is warranted because the repository already has two sibling implemented need projections and the horizon already names `authority_need` among need-classification fields. The missing slice can be kept small and testable by mirroring the clarification/inquiry projection pattern while adding the two-testimony join required for authority.

A safe first slice would add:

- `seed_runtime/authority_need_projection.py`;
- dataclasses for `AuthorityRequirementTestimony`, `AuthorityStandingTestimony`, `AuthorityNeedProjectionItem`, and `AuthorityNeedProjection`;
- `project_authority_need(...)` and JSON helper;
- tests proving identity matching, requirement/standing separation, scope/materiality gates, exclusion of clarification/inquiry/realization/generic blockers, and read-only/no-request/no-grant/no-authorization/no-record/no-mutation flags.

This slice is read-only and does not add a CLI diagnostic surface. If a future CLI diagnostic is added, the diagnostic inventory and shape-audit contract must be updated.

## Exact next bounded question

```text
Does Seed need a read-only AuthorityNeedProjection implementation that consumes one selected goal, one BoundedAdvancementHorizon, explicit component-bounded authority-requirement testimony, and explicit authority-standing testimony, and classifies unresolved authority need without requesting, granting, selecting, executing, recording, or mutating?
```

## Conclusion

Authority need is lawfully established only by the joined presence of explicit component-bounded authority-requirement testimony and explicit authority-standing testimony, both bound to the same selected goal, bounded authority component, evidence snapshot set, scope, and advancement horizon. The current implementation has adjacent authority-aware evidence and sibling need projectors, but no owner that performs this exact projection. The smallest missing responsibility is a read-only authority-need projector.

Authority need projection audit complete.
