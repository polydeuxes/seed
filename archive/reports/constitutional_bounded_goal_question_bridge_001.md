# Constitutional Bounded Goal Question Bridge Investigation 001

## Question

How, if at all, can the current constitutional condition of a bounded goal lawfully produce the next bounded constitutional question?

## Method and authority boundary

This is an evidence-only bridge investigation. It does not implement a bridge, create a universal inquiry engine, planner, semantic parser, question taxonomy, canonical goal object, or mandatory pipeline. Repository implementation, tests, and existing checked-in artifacts are treated as evidence. Existing reports are used as testimony and evidence locators, not as authority where implementation disagrees.

The investigation keeps these distinctions separate:

```text
goal-relative pressure
!= question-worthy uncertainty
!= bounded question standing
!= evidence demand
!= examination admission
!= caller-authored routing
```

## Side A: bounded goal condition

### A1. No single canonical bounded-goal owner is established

Repository evidence shows several bounded-goal-adjacent owners rather than one canonical goal object:

- The legacy projected runtime `Goal` model has `id`, `summary`, `status`, `facts`, `open_questions`, and `related_entities`. Its status vocabulary is `active`, `blocked`, `complete`, and `abandoned`.
- `StatePatchService` can append `goal.created` events from explicit state patches. This is mutating projected runtime state, not the newer read-only bounded-operator-goal family.
- `BoundedOperatorGoalEstablishment` is a read-only artifact for establishment, provisional establishment, or refusal from lawful ingress evidence.
- `GoalOrientationInventory` inventories explicitly associated pressures, bounded goals, inquiry references, and material across supported goal dimensions, but it is not a registry, planner, queue, or priority order.
- `GoalInquiryConsiderationSelection` can select one visible bounded goal for inquiry consideration only from exact focus evidence naming bounded-goal identity.
- `BoundedAdvancementHorizon` can preserve the current advancement boundary for one exact selected goal.
- `GoalAdvancementNeedSet` and `GoalAdvancementSufficiencyProjection` preserve and evaluate advancement-related need/coverage evidence for one selected goal and horizon without selecting a next action.

Therefore bounded-goal condition is family-local. There is no implementation-backed universal bounded-goal state object that contains every element listed in the prompt.

### A2. Bounded-goal identity establishment and preservation

`BoundedOperatorGoalEstablishment` preserves identity through `goal_establishment_id`, `ingress_artifact_type`, `ingress_artifact_ref`, and `ingress_lineage`. Its establishment functions compute stable ids from exact ingress, establishment state, intended outcome, scope, sufficiency conditions, stop conditions, Unknowns, conflicts, known loss, correction lineage, and convention.

Lawful ingress sources are explicitly limited to closed-choice selection binding, operator-expression interpretation, operator authority/scope binding, and downstream interpretation admission. The authority/scope path checks that binding, interpretation, and expression identities match before it can establish or refuse a goal. The admitted-interpretation path checks consumer and purpose refs for bounded-goal establishment and refuses mismatches. This means bounded-goal identity can be established from exact admitted or bound source records, not from later vocabulary similarity or caller assertion alone.

The runtime `Goal` model also has identity, summary, status, facts, open questions, and related entities, but this is projected state and not equivalent to the read-only bounded-operator-goal artifact.

### A3. Current position within a goal

Current constitutional position is not stored on the bounded-goal establishment artifact itself. It appears in later local artifacts:

- `GoalInquiryConsiderationSelection` records whether exact focus evidence selected a visible bounded goal, failed, conflicted, was ambiguous, or mismatched the inventory.
- `BoundedAdvancementHorizon` records `present_movement_boundary`, included/excluded scope, evidence snapshots, time/current-state bounds, relevant/excluded need families, Unknowns, conflicts, stale evidence, and unavailable evidence for one selected goal.
- `GoalAdvancementNeedSet` records supplied, absent, or excluded need-family projections and identity conflicts for one horizon.
- `GoalAdvancementSufficiencyProjection` records whether the horizon is `sufficient_for_now`, `insufficient_for_now`, `unknown`, or `conflicting` based on need and coverage evidence.

These are current-position evidence, but each owner refuses to become a next-action selector or question originator.

### A4. Completed, fulfilled, blocked, refused, or deferred work visibility

Visibility is distributed:

- Runtime `Goal.status` can show `active`, `blocked`, `complete`, or `abandoned` for projected goals.
- `BoundedOperatorGoalEstablishment.establishment_state` can show `established`, `provisional`, or `refused` behavior through the establishment functions.
- `BoundedAdvancementHorizon` can be `bounded` or `refused` with specific refusal reasons.
- Need-family records preserve `supplied`, `absent`, and `excluded` dispositions.
- Sufficiency projection can conclude `sufficient_for_now`, `insufficient_for_now`, `unknown`, or `conflicting`.

No reviewed implementation converts these statuses into a new bounded constitutional question.

### A5. Unresolved pressure, conflicts, evidence gaps, and Unknowns

Unresolveds remain visible in several fields:

- `BoundedOperatorGoalEstablishment` preserves `unresolved_scope`, `unknowns`, `ambiguities`, `conflicts`, and `known_loss`.
- `GoalOrientationInventory` preserves Unknown, unmatched, and conflicting association material.
- `GoalInquiryConsiderationSelection` preserves missing identity evidence, ambiguous goal refs, inventory mismatches, Unknowns, and conflicts.
- `BoundedAdvancementHorizon` preserves Unknowns, conflicts, stale evidence, unavailable evidence, included/excluded scope, and excluded need families.
- `GoalAdvancementNeedSet` preserves horizon Unknowns/conflicts/exclusions and family-level identity conflicts.
- `GoalAdvancementSufficiencyProjection` converts unresolved native needs, conflicts, unknown native standing, absent projections, and coverage unknowns into read-only sufficiency reasons.

This proves unresolved pressure and gaps can be represented. It does not prove that any unresolved pressure is already question-worthy uncertainty or bounded question standing.

### A6. Available evidence territory

Evidence territory is explicit and bounded, not inferred universally:

- Bounded-goal establishment carries upstream source, warrant, selection, applicability, admission, and snapshot refs where relevant.
- Advancement horizon carries evidence snapshot refs, time bounds, current-state bounds, included/excluded scope, stale refs, and unavailable refs.
- Need-set and sufficiency artifacts are constrained to one selected goal and one horizon.
- Constitutional registered-view selection has its own separate territory: registered process, governance, and fidelity read-model views selected only by exact keys.

Available territory is therefore local to each artifact. No implementation-backed owner was found that reads the full bounded-goal condition and derives a question evidence territory from it.

### A7. Remaining authority, negative authority, and forbidden movement

The bounded-goal side has strong negative authority:

- Establishment says goal established is not inquiry opened, resources observed, constraints satisfied, work authorized, or goal satisfied.
- Orientation inventory says visible pressure does not activate a goal and bounded goals do not grant inquiry, authorization, execution, recording, or mutation authority.
- Inquiry-consideration selection says selected for inquiry consideration is not activation, inquiry required/opened, frontier movement, authorization, execution, recording, or mutation.
- Advancement horizon says it is not need classification or sufficiency judgment and does not open inquiry, authorize, execute, record, or mutate state.
- Need-set says needs are unordered and not priority, blocker, route, next action, inquiry opening, authority request, realization selection, authorization, execution, recording, ledger write, or cluster mutation.
- Sufficiency projection is read-only and does not rank, select, record, or mutate.

Movement forbidden by current evidence includes semantic free-text promotion, hidden priority selection, automatic inquiry opening, automatic question formulation, execution authorization, and cluster mutation.

### A8. Lawful stop or completion conditions

Lawful stopping is visible but local:

- Bounded-goal establishment carries supplied `sufficiency_conditions`, `sufficiency_state`, and `stop_conditions`.
- Advancement horizon refuses when selection is unresolved, identity mismatches, goal artifact is not established, present movement boundary is missing, or excluded need families lack reasons.
- Sufficiency projection can stop at `sufficient_for_now`, `insufficient_for_now`, `unknown`, or `conflicting` for the horizon.
- Existing constitutional question road standing audit says to stop when a caller asks the bounded-question road to treat supplied fields as constitutionally originated without a separate live producer.

These stop conditions do not themselves produce a question.

### A9. Live implementation evidence versus reports, prose, and scaffolding

Live implementation evidence includes the runtime modules and tests for bounded-goal establishment, goal orientation inventory, inquiry consideration selection, advancement horizon, need-set assembly, sufficiency projection, bounded constitutional question production, constitutional view selection, and constitutional pipeline invocation.

Reports and audits are testimony and evidence locators. They help identify intended boundaries and history but do not override implementation. Tests that directly construct bounded questions or goals are implementation witnesses and scaffolding; they prove deterministic preservation and boundary behavior, not lawful origination from a live bounded-goal condition unless the production code does that same transformation.

### A10. Does any current consumer ask new questions from bounded-goal state?

No live consumer was found that consumes bounded-goal identity plus current constitutional position, fulfilled work, unresolved pressure, evidence territory, preserved Unknowns, remaining/negative authority, and stop conditions to produce a new `BoundedConstitutionalQuestion`.

The nearest consumers are weaker:

- `GoalInquiryConsiderationSelection` selects one visible bounded goal for inquiry consideration from exact focus evidence, but explicitly does not open inquiry.
- `BoundedAdvancementHorizon` preserves a current movement boundary for one selected goal, but explicitly does not classify needs or select next action.
- Need-set and sufficiency projection preserve and assess advancement needs/coverage, but do not select a route or next action.
- `ConstitutionalPipelineRequest` consumes an already-established `BoundedConstitutionalQuestion`; it does not originate one.

## Side B: constitutional question standing

### B1. Required identity and scope

The existing `BoundedConstitutionalQuestion` shape has useful identity and preservation fields: `bounded_question_id`, `operator_inquiry`, `inquiry_provenance`, `bounded_question`, `constitutional_intent`, `scope_status`, `uncertainty`, `unknowns`, and `caller_supplied_fields`. Its constructor can compute stable identity from explicit supplied inputs or preserve a supplied id.

However, for a constitutional question to lawfully direct examination or other movement, implementation evidence indicates that identity and scope would need to be established, not merely caller-authored. At minimum, standing would require evidence that the question belongs to an exact bounded goal or other lawful source, has bounded scope, has preserved uncertainty/Unknowns, and has a current unresolved need that warrants question treatment. The current constructor does not validate those conditions.

### B2. Required relation to the bounded goal

A goal-relative constitutional question would need a traceable relation to an exact bounded-goal identity and current position. The existing bounded-question road does not have fields or validation for selected goal identity, goal establishment id, horizon id, completed-work lineage, need-set id, sufficiency projection id, or authority/stop-condition lineage.

Therefore any relation to a bounded goal is currently caller testimony unless another artifact externally establishes it.

### B3. Present uncertainty or unresolved need

The existing bounded-question artifact preserves `uncertainty` and `unknowns`, and projection forwards them into selection uncertainty. That preservation is useful. It does not audit completeness, distinguish goal-relative pressure from question-worthy uncertainty, or prove that an unresolved need requires a constitutional question.

Need and sufficiency artifacts can expose unresolved needs, Unknowns, conflicts, absent projections, and insufficient-for-now states. But no current producer binds those reasons into bounded-question standing.

### B4. Evidence demand and evidence territory

The current constitutional question projection extracts only exact caller-declared `selection_key` fields. Those keys route to registered constitutional read-model views by exact matching. They do not recover evidence demand from the bounded question text, bounded-goal condition, pressure, work history, Unknowns, authority, or stop conditions.

Question standing would require an established evidence demand and available/excluded evidence territory. Today, registered-view routing can support caller-directed composition once keys are supplied, but it is not a recovered evidence demand.

### B5. Provenance and lineage requirements

`BoundedConstitutionalQuestion` preserves `inquiry_provenance` and caller fields, but the constructor does not validate provenance. The road-standing audit found that the caller asserts semantically important fields, including operator inquiry, provenance, bounded question, constitutional intent, scope status, uncertainty, Unknowns, selection keys, and any claim of bounded-goal origin.

A lawful bridge would need lineage from exact bounded-goal and current-position artifacts, including what was fulfilled, what remains unresolved, which evidence was available/excluded, and which movement is forbidden. That lineage is not present in the bounded-question constructor or projection.

### B6. Remaining and negative authority

The existing `BoundedConstitutionalQuestion` read-only boundaries are useful. They refuse fact promotion, verified claim promotion, constitutional authority creation, repository truth creation, durable knowledge creation, authoritative capability creation, view selection, projection, event-ledger writes, and cluster mutation.

But those boundaries are mostly constructor boundaries. They do not establish positive remaining authority to direct examination, nor do they carry bounded-goal-side forbidden movement. Registered-view selection and composition have independent authority only for exact-key read-model routing and composition.

### B7. Unknowns, conflicts, sufficiency, and lawful stop

The current shape preserves Unknowns and uncertainty. It lacks first-class conflicts, unresolved need reasons, sufficiency state, stop conditions, negative authority fields tied to a bounded goal, and refusal state for unsupported origination.

The road-standing audit's stop boundary is decisive: the current road must stop when asked to treat supplied question fields or selection keys as constitutionally originated without a separate implementation-backed live producer.

### B8. What must be established rather than caller-asserted

Before a question can lawfully direct examination or movement, the following cannot merely be caller asserted:

- exact question identity as arising from a lawful source;
- bounded scope and excluded territory;
- relation to an exact bounded goal/current position, if goal-relative standing is claimed;
- present uncertainty that is question-worthy rather than merely pressure;
- evidence demand and available evidence territory;
- provenance/lineage from fulfilled work, Unknowns, conflicts, and stop conditions;
- remaining authority and forbidden movement;
- admission into whatever examination or composition surface is requested.

### B9. Useful parts of `BoundedConstitutionalQuestion`

Useful surviving parts:

- immutable preservation;
- deterministic id for explicit payloads;
- exact preservation of operator inquiry/provenance and bounded-question text;
- uncertainty and Unknown preservation;
- testimony-status boundary;
- read-only/no-ledger/no-cluster flags;
- caller-supplied fields as testimony;
- explicit refusal to create authority, truth, durable knowledge, or view selection.

These parts are useful for preserving a candidate or supplied question artifact. They are not enough to establish goal-relative question standing.

### B10. Parts belonging only to caller-directed registered-view routing

`caller_supplied_fields` entries named `selection_key` or `selection_key:<key>` belong to caller-directed registered-view routing. Projection extracts them exactly; selection matches them exactly against registered capability keys; composition builds requested registered views. This is a legitimate registered-view route, not evidence demand recovery, question origination, or examination admission from bounded-goal state.

## Bridge comparison

### C1. Bounded-goal outputs that can lawfully supply question requirements

Some bounded-goal outputs could lawfully supply inputs to a future local question-standing act, if such an act were implemented:

| Question requirement | Bounded-goal-side evidence that could supply it | Current bridge status |
|---|---|---|
| Exact goal identity | `goal_establishment_id`, selected goal id, source refs | Available as evidence; no question producer consumes it |
| Current position | `present_movement_boundary`, horizon id, selected goal state | Available as evidence; no question producer consumes it |
| Fulfilled/blocked/deferred work visibility | establishment state, horizon refusal, need family dispositions, sufficiency conclusion | Available locally; no question-standing binding |
| Unresolved pressure/Unknowns/conflicts | unresolved scope, Unknowns, conflicts, need reasons, sufficiency reasons | Available locally; not distinguished as question-worthy uncertainty |
| Evidence territory | ingress lineage, snapshots, included/excluded scope, time/current-state bounds | Available locally; not transformed into evidence demand |
| Remaining/negative authority | read-only flags and boundary notes across owners | Available locally; not carried into question standing |
| Stop conditions | establishment stop conditions, horizon refusals, sufficiency conclusions, road stop boundary | Available locally; no origination stop/admission artifact |

These correspondences are potential evidence supply, not a live bridge.

### C2. Apparent correspondences that are only vocabulary similarity

The following are not enough:

- `open_questions` on runtime `Goal` is not a bounded constitutional question standing artifact.
- `inquiry` need family is not a `BoundedConstitutionalQuestion`.
- `selected for inquiry consideration` is not inquiry opened or question admitted.
- `present_movement_boundary` is not a bounded question.
- `unknowns` on a goal artifact are not automatically question-worthy uncertainty.
- `selection_key` is not evidence demand; it is caller-authored routing.
- `sufficient_for_now` is a local advancement sufficiency conclusion, not a universal stop/completion condition for constitutional questioning.

### C3. Required question standings with no producer

No current producer establishes:

- question-worthy uncertainty from goal-relative pressure;
- bounded constitutional question identity from exact bounded-goal/current-position artifacts;
- evidence demand from available/excluded evidence territory;
- relation between fulfilled work and the next constitutional question;
- complete provenance/lineage from bounded-goal ancestry after extended work;
- remaining authority and forbidden movement as question-standing fields;
- admission from bounded-goal condition into constitutional examination;
- refusal/Unknown state when the bridge lacks enough evidence.

### C4. Goal conditions with no lawful question-forming consumer

The following goal-side conditions are visible but have no lawful question-forming consumer:

- establishment/provisional/refused goal state;
- present advancement boundary;
- included/excluded scope and evidence snapshots;
- potentially relevant need families;
- unresolved native need projections;
- unknown/conflicting sufficiency projection;
- explicit stop conditions;
- negative authority declarations.

They can guide evidence-only human analysis but are not consumed by a live bridge artifact.

### C5. What act would be required?

Question origination cannot be reduced to construction. The missing act appears to be at least a recognition/evaluation/binding/admission sequence, or several local responsibilities, not one universal engine:

1. Recognize exact bounded-goal/current-position source artifacts.
2. Evaluate whether unresolved pressure is question-worthy uncertainty.
3. Bind the candidate question to goal identity, fulfilled work, evidence territory, Unknowns, conflicts, authority, and stop conditions.
4. Establish or refuse bounded question standing.
5. Admit any established question into a specific examination or registered-view route, if a lawful route exists.

Current repository evidence does not show this sequence as implemented. It may be one responsibility or several local responsibilities, but the current implementation does not settle that design.

### C6. Does a live handoff already exist?

No live handoff was found from bounded-goal condition to `BoundedConstitutionalQuestion`.

A handoff exists only after an already-established or caller-supplied `BoundedConstitutionalQuestion` is present: projection, capability projection, selection, adapter, and composition can proceed read-only. That is a downstream registered-view pipeline, not a bounded-goal-to-question bridge.

### C7. Missing evidence, refusal, Unknown, and stop

Because no implementation-backed live bridge exists, any claim that the current bounded-goal condition lawfully produces the next bounded constitutional question must be refused or preserved as Unknown.

The lawful stop boundary is exact:

> Stop before treating bounded-goal pressure, current position, unresolved work, Unknowns, sufficiency reasons, or caller-authored selection keys as a constitutionally established next bounded question. The repository currently supports preserving those materials as evidence and preserving a supplied bounded question as testimony, but not silently converting one shore into the other.

## Classification

**Disconnected implementation-backed shores.**

Both shores have implementation-backed artifacts:

- bounded-goal condition artifacts can preserve identity, current position, unresolved pressure, evidence territory, authority boundaries, and stop/sufficiency states;
- constitutional-question artifacts and pipeline stages can preserve supplied question testimony, exact caller routing keys, registered-view selection, and composition.

The bridge between them is not live. It is not a fully unsupported connection, because each shore is real. It is not a partially realized bridge, because no current owner performs even a minimal bounded-goal-to-question-standing production or admission. It is not missing constitutional realization in the abstract, because downstream question routing and bounded-goal current-position artifacts are realized separately. The missing realization is specifically the lawful bridge act from bounded-goal condition to next bounded constitutional question.

Bounded goal constitutional question bridge investigation 001 complete.
