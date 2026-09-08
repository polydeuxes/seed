# Operational Realization Need Projection Audit 001

## Scope

This audit asks whether Seed already has lawful evidence and ownership for an `OperationalRealizationNeedProjection` over the family:

```text
BoundedAdvancementHorizon
+
operational-realization requirement testimony
+
operational-realization standing testimony
→ OperationalRealizationNeedProjection
```

The audit is read-only. It does not select, warrant, translate, invoke, authorize, execute, record, or mutate operational state.

## Repository evidence reviewed

The relevant present implementation evidence is:

- `BoundedAdvancementHorizon`, which preserves a present movement boundary and explicitly declares that it is not need classification, sufficiency judgment, next-action selection, authorization, execution, recording, or mutation.
- `ClarificationNeedProjection`, which consumes only explicit component-bounded operator-meaning uncertainty testimony and refuses to request clarification or execute work.
- `InquiryNeedProjection`, which consumes only explicit component-bounded repository/world uncertainty testimony and keeps freshness and availability separate from inquiry standing.
- `AuthorityNeedProjection`, which already models a two-testimony join between authority requirement testimony and authority standing testimony.
- `CandidateOperationalRealizationSet`, which projects candidate realizations but does not project overall capability reachability, rank, or select candidates.
- `CapabilityReachabilityProjection`, which consumes candidate-realization projections and concludes demand-level reachability without selecting a realization, authorizing, scheduling, executing, or creating pending action.
- `OperationalRealizationSelection`, which can select an eligible supported candidate only after reachability handoff and policy, while preserving no-selection and non-selected alternatives.

## What may testify that realization is required

A lawful requirement witness must be an explicit, component-bounded operational-realization requirement testimony for the exact selected goal and horizon. By analogy with authority need, it must carry at least:

- `selection_id`, `goal_establishment_id`, and `horizon_id` matching the present movement artifacts.
- An `evidence_ref` included in `horizon.evidence_snapshot_refs`.
- A bounded component reference for the required operational realization component.
- A required capability or transformation reference for one exact bounded transformation.
- An owning stage.
- Requirement standing such as `required`, `not_required`, `unknown`, or `conflicting`.
- Horizon materiality proving that the requirement is material to the exact present movement boundary.

The horizon alone cannot testify that a realization is required. Its own boundary notes say included need families are only potentially relevant and do not establish that a need exists. Therefore `potentially_relevant_need_families=("operational_realization_need", ...)` may preserve scope for later classification, but it is not requirement testimony.

Candidate and reachability artifacts also cannot testify that the movement requires realization. They can show candidate or demand standing for a capability demand once such a demand has been handed off, but they do not prove that the present movement must be advanced by operational realization rather than clarification, inquiry, authority work, sufficiency, or lawful stop.

## What may testify to realization-family standing

A lawful standing witness must be an explicit, component-bounded operational-realization standing testimony for the same exact selected goal, horizon, bounded realization component, and required transformation. It may be derived from, or reference, existing candidate and reachability evidence, but it must not collapse those evidence layers.

Existing artifacts that can supply inputs to such testimony are:

- `CandidateOperationalRealizationSet`: candidate existence, no-known-realization observation, candidate-local mechanism availability, grammar standing, behavior standing, representation compatibility, methodological compatibility, dependency standing, authority standing, and candidate standing.
- `CapabilityReachabilityProjection`: demand-level reachability state and family partitions such as supporting, blocked, unsupported, unknown, and conflicting candidates.
- `OperationalRealizationSelection`: selected or no-selection state, but only as selection evidence, not as realization-family availability evidence.

Standing testimony should therefore reference these artifacts as evidence, not replace them. A single unsupported candidate is evidence about that candidate. It is not evidence that the realization family is unavailable. A missing selection is evidence about selection state. It is not evidence that no realization is available.

## Two-testimony join requirement

Repository evidence strongly supports a two-testimony join.

`AuthorityNeedProjection` already separates requirement testimony from standing testimony, validates both against the same selection, goal, horizon, evidence snapshot, component, class, scope, owner, applicability, and materiality, then concludes need only after joining matching requirement and standing witnesses. The operational-realization boundary has the same shape: need is established only when the present movement requires a realization and the realization family is presently insufficient.

Therefore the lawful operational-realization need rule should be:

```text
requirement_standing=required
+
realization_family_standing=unavailable
+
matching selection/goal/horizon/evidence/component/transformation/owner/materiality
→ operational_realization_need=established
```

Other combinations should preserve separate outcomes:

- `required + available → unsupported` for need, because the family is sufficient at this boundary.
- `required + unknown → unknown`.
- `required + conflicting → conflicting`.
- `required + outside_current_scope → outside_current_scope`.
- `not_required + any standing → unsupported`, unless scope/materiality validation excludes it first.
- Missing matching standing testimony → unclassified, not established.
- Standing testimony without matching requirement testimony → unclassified, not established.

## What “available” lawfully means here

At this boundary, `available` cannot mean merely “a candidate exists,” “a candidate is supported,” “a candidate was selected,” or “reliance is warranted.” It should mean only:

> For the exact present movement and bounded transformation, current evidence establishes at least one realization family path sufficient for the family-standing boundary, without selecting or warranting a candidate and without authorizing movement.

The smallest lawful definition should be demand-level and family-level:

- The requirement and standing testimony refer to the same exact bounded operational-realization component and required transformation.
- The standing evidence is current within the `BoundedAdvancementHorizon` evidence snapshot.
- Candidate-space incompleteness is not being silently treated as availability or unavailability.
- Existing demand-level reachability evidence supports availability for the family, normally via `CapabilityReachabilityProjection.reachability_state == "reachable"` with at least one supporting candidate.
- The projection records that availability is not candidate selection, realization warrant, movement authorization, execution preparation, or execution.

`unavailable` should likewise be bounded. It may be established when demand-level evidence says the family is presently blocked or unsupported in a bounded way. It should not be inferred from no candidate selected, one candidate unavailable, absent candidates, failed implementations, generic blockers, authority failure in another boundary, or downstream silence.

## Required separation of layers

Repository evidence requires separate layers rather than a single flattened standing enum doing all work.

### Candidate existence

Candidate existence is preserved by `CandidateOperationalRealizationSet.candidates` and `no_known_realization_observations`. The candidate projection explicitly says no known realization does not mean impossible.

### Reachability

Demand-level reachability is owned by `CapabilityReachabilityProjection.reachability_state`. It consumes candidate sets and distinguishes `reachable`, `blocked`, `unsupported`, `unknown`, and `conflict` without selection.

### Selection

Selection is owned by `OperationalRealizationSelection.selection_state` and related policy. It can yield `selected`, `no_selection`, or `conflict`, and no-selection does not establish unavailability.

### Warrant

Warrant is downstream of selection handoff. A supported candidate and selected candidate are still not the same as reliance being warranted. Need projection must not issue or infer a warrant.

### Representation applicability

Representation applicability is owned by representation grammar applicability artifacts. Applicability may support future candidate realization, but repository boundary notes say it does not select or warrant a realization.

### Dependencies

Dependency standing is candidate-local and is summarized at reachability. Dependency unavailability can block otherwise sufficient candidates, but one candidate dependency blocker is not family unavailability.

### Behavior support

Behavior support is bounded to observed mechanism, version, invocation grammar, and probe conditions. Behavior support can contribute to candidate standing; it is not candidate selection, family need, or movement authorization.

## Exclusions: clarification, inquiry, authority, and generic blocking

Operational-realization need must exclude other need families and generic blockers:

- Clarification evidence remains operator-meaning uncertainty owned by `ClarificationNeedProjection`; unresolved operator meaning cannot be reclassified as realization need.
- Inquiry evidence remains repository/world uncertainty owned by `InquiryNeedProjection`; stale or unavailable evidence cannot silently become realization need.
- Authority evidence remains authority requirement plus authority standing owned by `AuthorityNeedProjection`; authority need established is not operational-realization need established.
- Generic blocking components, absent observations, denied execution, unsupported facts, missing selection, failed implementation attempts, and downstream silence are not operational-realization requirement or standing testimony unless an explicit component-bounded testimony artifact says so.

## Existing owner assessment

No existing owner performs the full operational-realization need projection.

- `BoundedAdvancementHorizon` preserves the boundary and possible need-family relevance, but explicitly refuses need classification.
- `CandidateOperationalRealizationSet` owns candidate evidence, not family need.
- `CapabilityReachabilityProjection` owns demand-level reachability, not present-movement requirement.
- `OperationalRealizationSelection` owns selection under policy, not need establishment.
- The existing clarification, inquiry, and authority need projections show the stage-owned projection pattern, but none owns operational-realization need.

## Smallest missing responsibility

The smallest missing responsibility is a read-only `OperationalRealizationNeedProjection` that:

1. Consumes `GoalInquiryConsiderationSelection`, `BoundedOperatorGoalEstablishment`, and `BoundedAdvancementHorizon`.
2. Consumes explicit `OperationalRealizationRequirementTestimony` and `OperationalRealizationStandingTestimony`.
3. Validates identity, evidence snapshot membership, bounded component identity, exact transformation identity, owning stage, family, scope/applicability if present, and horizon materiality.
4. Joins matching requirement and standing testimony.
5. Buckets results into `established`, `unsupported`, `unknown`, `conflicting`, `outside_current_scope`, and `unclassified`.
6. Preserves boundary flags: no realization selection, no warrant, no translation, no invocation preparation, no authorization, no execution, no recording, no event-ledger writing, and no cluster mutation.

## Whether one read-only implementation slice is warranted

Yes. One read-only implementation slice is warranted because repository patterns already exist and the missing responsibility is bounded. The slice should mirror `AuthorityNeedProjection` more closely than `InquiryNeedProjection` because operational-realization need requires both requirement testimony and standing testimony.

The slice should not add a CLI surface unless explicitly requested. If a diagnostic or recordable surface is later added, the diagnostic inventory and shape-audit obligations must be updated at that time.

## Exact next bounded question

```text
What is the minimal read-only OperationalRealizationNeedProjection API and test suite that joins explicit operational-realization requirement testimony with explicit operational-realization standing testimony for one BoundedAdvancementHorizon, while preserving candidate existence, reachability, selection, warrant, representation applicability, dependencies, and behavior support as separate layers?
```

Operational realization need projection audit complete.
