# Lowest-Sufficient-Layer Recalibration Audit 001

## Scope

This audit determines what currently owns the impact of a bounded operator intervention across the layered chain:

```text
communication
→ active question
→ inquiry frontier
→ bounded operator goal
→ constitutional orientation
```

It asks whether Seed needs a read-only projection shaped like:

```text
BoundOperatorIntervention
+
current communicated material
+
current inquiry state
+
current bounded operator goal
→ RecalibrationImpactProjection
```

This is an audit only. It does not implement communication, conversation-reference binding, active-question state, frontier transition, goal transition, planning, authorization, execution, recording, diagnostic inventory, CLI behavior, event-ledger behavior, cluster mutation, or constitutional revision.

## Evidence reviewed

Repository evidence reviewed:

- `seed_runtime/operator_expression_interpretation.py`
- `seed_runtime/bounded_constitutional_question.py`
- `seed_runtime/constitutional_pipeline.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/bounded_operator_goal_establishment.py`
- `bounded_operator_goal_establishment_slice_001.md`
- `step_wise_inquiry_frontier_transition_audit_001.md`
- `bounded_operator_goal_calibration_audit_001.md`
- `first_bounded_operator_goal_establishment_audit_001.md`
- `closed_choice_selection_binding_slice_001.md`
- `shared_explanation_bounded_composition_slice_001.md`

Commands used during this audit:

```bash
pwd && rg --files -g 'AGENTS.md' -g '!*venv*' -g '!node_modules' | xargs -r -I{} sh -c 'echo --- {}; cat {}' && rg --files | head -80
rg -n "bounded operator|operator goal|intervention|recalibration|active question|inquiry frontier|frontier|communicated|lineage|projection" -S . | head -200
rg -n "Bounded|Operator|Goal|Inquiry|Frontier|Question|Lineage|Intervention" seed_builder tests scripts -S | head -200
rg --files seed_runtime | head -100 && sed -n '1,220p' seed_runtime/operator_expression_interpretation.py && sed -n '1,180p' seed_runtime/bounded_constitutional_question.py && sed -n '1,160p' seed_runtime/constitutional_question_projection.py
sed -n '160,360p' seed_runtime/bounded_constitutional_question.py && sed -n '1,240p' seed_runtime/constitutional_pipeline.py && sed -n '1,220p' seed_runtime/inquiry_orientation.py
rg -n "bounded operator goal|operator goal|provisional bounded|bound operator|goal-level|bounded goal|operator intervention|intervention" . -S --glob '*.md' --glob '*.py' | head -200
sed -n '1,260p' seed_runtime/bounded_operator_goal_establishment.py && sed -n '1,220p' bounded_operator_goal_establishment_slice_001.md && sed -n '1,220p' step_wise_inquiry_frontier_transition_audit_001.md
sed -n '220,520p' step_wise_inquiry_frontier_transition_audit_001.md && sed -n '1,220p' bounded_operator_goal_calibration_audit_001.md && sed -n '220,360p' bounded_operator_goal_calibration_audit_001.md
```

One command intentionally exposed absence: `seed_runtime/constitutional_question_projection.py` does not exist as a standalone module. The constitutional question projection owner is imported and used through `seed_runtime/constitutional_pipeline.py` from `seed_runtime.constitutional_view_selection`.

## Executive determination

No existing owner currently classifies the impact of a bounded operator intervention across communication, active question, inquiry frontier, bounded operator goal, and constitutional orientation.

The repository now has a read-only bounded operator goal establishment owner, but it is not an intervention-impact owner. It establishes one bounded operator goal from lawful ingress evidence and explicitly refuses inquiry opening, authorization, execution, recording, satisfaction judgment, and lineage rewriting. Its boundary notes also preserve that corrections may establish a later bounded goal without rewriting exact ingress lineage.

The repository also has audits that characterize inquiry-frontier and goal-calibration transitions, but those documents conclude that active frontier transition and multi-inquiry bounded-goal calibration are not implementation-owned. Therefore the present owner map is distributed and intentionally incomplete:

| Layer | Existing owner evidence | Current ownership limit |
| --- | --- | --- |
| Communication / exact material | `AttributedOperatorExpression`, `InquiryNoteRecord`, bounded-question `operator_inquiry` | Preserves exact operator material; does not decide intervention impact. |
| Response-local correction | No dedicated owner | Can be characterized by audit discipline only; no implementation classifies a correction as response-local. |
| Active question | Bounded constitutional question and question-surface invocation paths | Produce or invoke bounded questions from explicit inputs; no current active-question revision owner. |
| Inquiry frontier | `step_wise_inquiry_frontier_transition_audit_001.md` | Finds no active inquiry-frontier owner or executable transition algebra. |
| Bounded operator goal | `BoundedOperatorGoalEstablishment` | Establishes a goal from lawful ingress; does not classify later intervention impact across layers. |
| Constitutional orientation | Constitutional discipline and pipeline boundary notes | Preserves lawful movement constraints; misinterpretation is not automatically constitutional failure. |

Supported conclusion:

```text
Seed can preserve intervention evidence and bounded goal establishment lineage;
Seed cannot yet classify the lowest sufficient impact layer of an intervention as an implementation-owned projection.
```

Unsupported conclusion:

```text
Any correction, clarification, or redirection automatically rewrites the active question, frontier, goal, or constitutional orientation.
```

## What evidence binds an operator intervention to prior communicated material

Current repository evidence supports binding only when explicit identity, exact text, or provenance survives the handoff.

### Existing binding evidence

1. **Exact operator expression identity.** `attribute_operator_expression(...)` preserves `exact_text`, `normalized_text`, `source_channel`, workspace/session/operator refs, provenance, received scope context, uncertainty, unknowns, and a stable `expression_id`. This binds a later interpretation to exact communicated material.
2. **Source spans.** `OperatorExpressionInterpretationProjection` carries `source_span_bindings`, unsupported residual spans, unresolved references, and alternative interpretations. This binds interpreted components to exact spans but does not prove the effect of an intervention on prior state.
3. **Bounded constitutional question testimony.** `BoundedConstitutionalQuestion` preserves `operator_inquiry`, `inquiry_provenance`, caller-supplied fields, uncertainty, unknowns, and read-only boundaries. It explicitly treats operator testimony as evidence, not established fact.
4. **Inquiry note records.** `InquiryNoteRecord` preserves raw inquiry note prose, timestamp, source, workspace, and session. `InquiryOrientationView` can orient by lexical overlap only and refuses semantic interpretation, planning, workflow movement, and next-safe-move authority.
5. **Bounded operator goal ingress lineage.** `BoundedOperatorGoalEstablishment` preserves `ingress_artifact_type`, `ingress_artifact_ref`, `ingress_lineage`, `operator_acceptance_provenance`, unknowns, ambiguities, conflicts, known loss, and optional `correction_of_goal_ref`.

### Missing binding evidence

The repository does not currently bind an intervention to:

- a durable current communication object;
- a durable active response object;
- a durable active question object;
- a durable active inquiry-frontier object;
- a durable current bounded-goal frame across multiple interventions;
- a current constitutional-orientation revision target.

Therefore the current binding is ingress- and artifact-local, not layer-impact-complete.

## Whether an existing owner already classifies intervention impact

No.

Adjacent owners classify narrower things:

| Candidate owner | Classifies | Does not classify |
| --- | --- | --- |
| Operator expression interpretation | one attributed expression as interpreted, ambiguous, unsupported, unknown, or conflict | response-local vs question vs frontier vs goal impact |
| Bounded constitutional question formulation | one bounded question from permitted upstream artifacts | whether later operator material recalibrates that question or a higher layer |
| Inquiry orientation | deterministic lexical relatedness for preserved note prose | semantic intervention impact or transition effect |
| Question surface inventory / bounded ask | exact registered question-family eligibility and dispatch | current active-question refinement from arbitrary intervention |
| Inquiry-frontier audit | characterization-level continue/constrain/expand/fork/supersede/close distinctions | implementation-owned frontier transitions |
| Bounded operator goal establishment | initial bounded-goal establishment or provisional/refused state from lawful ingress | multi-layer intervention impact or actual transition |
| Bounded operator goal calibration audit | warranted future transition vocabulary | implementation-owned classifier |

The closest new implementation owner is `BoundedOperatorGoalEstablishment`, because it can reference `correction_of_goal_ref`. But that field only preserves a later establishment relation. It does not decide whether the correction should have stopped at response material, active question, inquiry frontier, bounded goal, or constitutional orientation.

## Layer identities and lineage that must be preserved

A lawful recalibration projection would need to preserve distinct identities rather than collapsing the chain:

1. **Intervention identity**
   - exact intervention material;
   - attribution/provenance;
   - source channel;
   - workspace/session/operator refs where available;
   - uncertainty, unknowns, and conflicts.
2. **Prior communicated material identity**
   - the exact prior response or communicated material reference if one exists;
   - local claim/span/section identity if only part of the response is corrected;
   - the boundary that communication content is not automatically inquiry state.
3. **Active question identity**
   - bounded question id or exact registered question-family invocation identity;
   - current question text/selection keys/required args if available;
   - question lineage and non-selected alternatives where preserved.
4. **Inquiry-frontier identity**
   - frontier pressure, open question, selected bounded work, or document-visible question identity if available;
   - explicit unknown when no active frontier owner exists;
   - no fabricated branch, closure, or continuation object.
5. **Bounded operator goal identity**
   - goal establishment id;
   - ingress artifact ref and lineage;
   - intended outcome, known/unresolved scope, sufficiency and stop conditions;
   - `correction_of_goal_ref` when a later goal corrects an earlier goal.
6. **Constitutional orientation identity**
   - constitutional rule/orientation references if the intervention alleges a movement-law problem;
   - explicit separation between misinterpretation, ordinary layer correction, and constitutional failure.

The preserved lineage rule is:

```text
recalibration appends or projects impact over preserved lineage;
recalibration does not rewrite prior lineage.
```

## How repository evidence distinguishes impact classes

The following distinctions are currently evidence-backed as audit-level classifications, not implemented states.

### 1. Response-local correction

A response-local correction is supported when the intervention points only at communicated material and does not supply evidence that the active question, frontier, or goal must change.

Evidence shape:

```text
intervention exact material
+ prior communicated material/span target
+ no changed question boundary
+ no changed frontier pressure
+ no changed goal outcome/scope/sufficiency/stop criteria
+ no constitutional movement failure
→ response-local correction
```

Repository support:

- exact text and source spans can be preserved;
- operator testimony remains evidence, not truth;
- inquiry orientation refuses intent and next-safe-move inference.

Repository gap:

- no active response/communication object is currently preserved as the target of correction.

Guardrail preserved:

```text
local correction must not automatically propagate upward
```

### 2. Active-question refinement

An active-question refinement is supported when the intervention changes the current bounded question's wording, required args, selection key, scope, or unresolved reference, but does not require a new frontier branch or goal recalibration.

Evidence shape:

```text
intervention exact material
+ active question identity
+ changed question boundary or argument
+ same bounded goal outcome/sufficiency frame
+ prior question lineage preserved
→ active-question refinement
```

Repository support:

- bounded constitutional question and question-surface paths preserve question identity and explicit inputs;
- bounded ask requires exact registered identity rather than implicit routing.

Repository gap:

- no current owner records an active question as refined by intervention.

### 3. Inquiry-frontier constraint, expansion, fork, or closure

An inquiry-frontier impact is supported when the intervention changes what inquiries remain open, constrained, added, branched, superseded, or closed while preserving prior lineage.

Evidence shape:

```text
intervention exact material
+ current inquiry/frontier evidence
+ transition effect limited to constrain | expand | fork | close | preserve | unresolved
+ prior lineage retained
+ no goal-frame rewrite unless goal evidence separately supports it
→ inquiry-frontier impact
```

Repository support:

- `step_wise_inquiry_frontier_transition_audit_001.md` distinguishes continue, constrain, expand, fork, supersede, and close as lawful audit descriptions;
- it explicitly preserves interrupted != completed, constrained != answered, expanded != replaced, new branch != rewritten history, and communication turn != inquiry step.

Repository gap:

- the same audit finds no active frontier owner and no executable transition algebra.

### 4. Bounded-goal recalibration

A bounded-goal recalibration is supported when the intervention changes the intended outcome, known or unresolved scope, sufficiency conditions, stop conditions, closure criteria, or corrects a prior bounded-goal establishment.

Evidence shape:

```text
intervention exact material
+ current bounded operator goal establishment id
+ changed goal outcome/scope/sufficiency/stop criteria or correction_of_goal_ref
+ prior goal ingress lineage preserved
+ future inquiries affected prospectively
→ bounded-goal recalibration
```

Repository support:

- `BoundedOperatorGoalEstablishment` preserves intended outcome, outcome resolution, known and unresolved scope, sufficiency conditions, stop conditions, constraints, unknowns, ambiguities, conflicts, known loss, and `correction_of_goal_ref`;
- its boundary notes state that corrections may establish a later bounded goal without rewriting exact ingress lineage;
- `bounded_operator_goal_calibration_audit_001.md` distinguishes preservation, constraint, expansion, correction, and closure of a goal frame.

Repository gap:

- no implementation owner classifies an intervention as requiring bounded-goal recalibration before any later goal establishment is produced.

Guardrail preserved:

```text
goal-level redirection must not be trapped as response-local correction
```

### 5. Unresolved or conflicting intervention

An unresolved or conflicting intervention is supported when reference binding, target layer, semantic interpretation, authority, or evidence conflicts remain unresolved.

Evidence shape:

```text
intervention exact material
+ missing target identity or conflicting layer evidence
+ unknowns/conflicts preserved
+ no hidden promotion
+ no irreversible movement
→ unresolved_or_conflicting_intervention
```

Repository support:

- operator expression interpretation has `unknown`, `ambiguous`, `unsupported`, and `conflict` states;
- bounded goal establishment can produce `refused` and preserve unknowns/conflicts;
- inquiry orientation states that lexical overlap does not establish intent.

Repository gap:

- no cross-layer projection preserves target-layer uncertainty as a first-class intervention-impact answer.

## Impact classification and actual state transition are separate responsibilities

Repository evidence strongly supports separation.

Impact classification would be read-only:

```text
intervention + current material + current inquiry/goal evidence
→ projected impact class + evidence + unknowns + conflicts + non-transition boundary
```

Actual state transition would be a different responsibility:

```text
approved/authorized transition request + current state owner
→ changed communication/question/frontier/goal state, if such a state owner exists
```

The current repository repeatedly separates projection from mutation, interpretation from authority, inquiry from execution, and goal establishment from work authorization. `BoundedOperatorGoalEstablishment` is explicitly read-only and says goal established is not inquiry opened, resources observed, constraints satisfied, work authorized, execution started, recording started, or satisfaction judged. The inquiry-frontier audit likewise says current transition labels are characterization-only, not executable state changes.

Therefore a `RecalibrationImpactProjection` would be lawful only if it remains a read-only classifier and explicitly refuses to perform the transition it classifies.

## What Seed currently owns

Seed currently owns these adjacent responsibilities:

```text
exact operator material preservation
one-expression interpretation under recovered grammar
bounded constitutional question production from explicit fields or permitted handoff
exact registered question-family invocation
read-only inquiry-note orientation
bounded operator goal establishment from lawful ingress
constitutional non-promotion and lineage-preservation discipline
```

Seed does not currently own:

```text
current communicated-material target binding
active question mutation
active inquiry-frontier state
multi-intervention bounded goal frame calibration
lowest-sufficient-layer impact classification
actual state transition after classification
constitutional revision from intervention
```

## The smallest missing owner

The smallest missing owner is not a planner, transition engine, goal mutator, conversation memory, or constitutional authority mechanism.

The smallest missing owner is:

```text
Bounded Operator Intervention Impact Projection
```

Its minimal responsibility would be to consume already-preserved evidence and produce a read-only projection:

```text
BoundedOperatorInterventionImpactProjection
- intervention_ref / exact intervention material ref
- prior_communicated_material_ref or unknown
- active_question_ref or unknown
- inquiry_frontier_ref or explicit no-owner/unknown
- bounded_operator_goal_ref or unknown
- constitutional_orientation_refs, if implicated
- impact_class:
  response_local_correction
  | active_question_refinement
  | inquiry_frontier_constraint
  | inquiry_frontier_expansion
  | inquiry_frontier_fork
  | inquiry_frontier_closure
  | bounded_goal_recalibration
  | unresolved
  | conflict
- impact_reason
- evidence_refs
- lineage_preservation_notes
- non_transition_boundary
- unknowns
- conflicts
- read_only=true
- writes_event_ledger=false
- mutates_cluster=false
```

Non-responsibilities:

- interpreting arbitrary prose beyond existing interpretation evidence;
- binding vague conversation references such as “that” without an upstream binding artifact;
- mutating active question, frontier, or goal state;
- creating a goal, plan, authorization, execution, record, or constitutional revision;
- rewriting prior lineage;
- treating a misinterpretation as constitutional failure;
- hiding promotion or making irreversible movement.

## Whether one implementation slice is warranted

Yes, one implementation slice is warranted, but not the full transition system and not in this audit.

The warranted slice is a narrow read-only projection over existing artifacts that makes the absence of state transition ownership explicit. It should probably start with only cases that can be proven without conversation inference:

1. bounded-goal recalibration candidate when an intervention references a current `BoundedOperatorGoalEstablishment` and changes goal fields or supplies `correction_of_goal_ref` evidence;
2. unresolved impact when the target layer is absent or ambiguous;
3. response-local candidate only when an explicit communicated-material target artifact exists, which may require a separate prior owner if no such artifact exists.

A larger slice would be premature if it adds active frontier state, active-question mutation, natural-language conversation targeting, or executable transition effects.

Because this job explicitly forbids implementation, this audit stops at the projection warrant.

## Exact next bounded question

```text
What minimal read-only intervention-impact projection can classify one preserved operator intervention against one existing BoundedOperatorGoalEstablishment and explicit target references, while returning unresolved when communication, active-question, or inquiry-frontier target identity is missing?
```

## Final conclusion

- Evidence binds an operator intervention to prior material only through exact text, stable artifact refs, source spans, provenance, and preserved lineage; no general current-communication or active-frontier target binding exists.
- No existing owner classifies intervention impact across response, active question, inquiry frontier, bounded goal, and constitutional orientation.
- Layer identities that must be preserved are intervention, communicated material, active question, inquiry frontier, bounded operator goal, constitutional orientation, and each layer's lineage.
- Impact classification and actual state transition must remain separate responsibilities.
- The smallest missing owner is a read-only `BoundedOperatorInterventionImpactProjection` / `RecalibrationImpactProjection` owner.
- One implementation slice is warranted later, but only as a narrow non-mutating projection that returns unresolved when target evidence is missing.
- The next bounded question is the minimal projection question stated above.

Lowest-sufficient-layer recalibration audit complete.
