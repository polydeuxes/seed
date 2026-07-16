# Goal Advancement Need Audit 001

## Question

Determine the lawful read-only boundary:

```text
GoalInquiryConsiderationSelection
+
selected goal state
+
available sufficiency and boundary evidence
-> GoalAdvancementNeedProjection
```

The candidate outcome vocabulary under review is:

```text
sufficient_for_now
clarification_needed
inquiry_needed
authority_needed
operational_realization_needed
blocked
unknown
conflict
```

Repository authority wins. This audit does not implement clarification, inquiry-frontier establishment, authority requests, realization selection, execution, scheduling, prioritization, or goal satisfaction. It also preserves:

```text
goal selected != goal deficient
goal deficient != knowledge deficient
knowledge sufficient != movement authorized
inquiry unnecessary != goal permanently satisfied
need identified != next action selected != transition authorized
```

## Evidence reviewed

- `seed_runtime/goal_inquiry_consideration_selection.py`
- `goal_inquiry_consideration_selection_slice_001.md`
- `goal_inquiry_consideration_selection_audit_001.md`
- `seed_runtime/bounded_operator_goal_establishment.py`
- `seed_runtime/goal_orientation_inventory.py`
- `seed_runtime/operational_realization_selection.py`
- `seed_runtime/operational_realization_warrant.py`
- `minimum_lawful_advancement_explanation_recurrence_audit_001.md`
- `missing_constitutional_boundary_explanation_audit_001.md`

## Current implemented boundary before this projection

`GoalInquiryConsiderationSelection` is already narrower than advancement. It consumes a goal-orientation inventory candidate set plus explicit focus evidence, and selects only when one visible `bounded_goal` candidate has the named `goal_establishment_id`. Its boundary notes explicitly state that selection for inquiry consideration is not goal activation, inquiry required, inquiry opened, frontier moved, work authorized, execution, recording, or mutation.

The selected goal state comes from `BoundedOperatorGoalEstablishment`, not from selection. A bounded goal has `establishment_state`, `establishment_reason`, `intended_outcome`, `known_scope`, `unresolved_scope`, `sufficiency_conditions`, `sufficiency_state`, `stop_conditions`, operator constraints, unknowns, ambiguities, conflicts, known loss, lineage, and non-authority flags. Its own boundary notes say that goal establishment is not inquiry opened, resources observed, constraints satisfied, work authorized, or goal satisfied.

`GoalOrientationInventory` remains orientation only. It can expose dimensions, pressure, bounded goals, inquiry references, unknown association material, unmatched material, and conflicting material, but it is not a registry, planner, queue, priority order, activation surface, inquiry mover, scheduler, authorization surface, execution surface, recorder, event-ledger writer, or cluster mutator.

Operational-realization owners prove that realization-related movement is downstream and stage-owned. Selection of an operational realization selects zero or one supported realization but does not warrant reliance, construct invocation, translate representation, authorize, schedule, or execute. Warrant can warrant or refuse reliance on one exact selected realization, but it still does not authorize, schedule, emit, execute, or construct external representation.

Therefore the proposed `GoalAdvancementNeedProjection` may identify what kind of boundary appears missing or sufficient for present advancement, but it must not choose the next action, authorize movement, instantiate an inquiry frontier, request authority, select a realization, or judge satisfaction.

## Lawful read-only input set

The smallest lawful input set is:

```text
GoalInquiryConsiderationSelection(selection_state, selected_goal_establishment_id, unknowns, conflicts, boundary flags)
+
BoundedOperatorGoalEstablishment for that selected goal, when selection_state=selected
+
available evidence snapshots already produced by stage owners, such as sufficiency conditions, stop conditions, unresolved scope, unknowns, conflicts, operator constraints, known loss, inventory conflict visibility, authority standings, reachability/projection states, or operational-realization warrant states
```

The projection should reject or preserve mismatch when the selected goal identity and supplied goal artifact do not match. It should not repair by searching for another goal. It should not derive hidden goal state from labels, dimension names, topic similarity, or pressure visibility.

## Proposed output responsibility

A lawful `GoalAdvancementNeedProjection` would be a read-only classifier over already-available evidence. It answers:

```text
Given this exact selected goal and the already-visible sufficiency/boundary evidence, what kind of advancement need is presently visible, if any?
```

It does not answer:

- which question to ask;
- which clarification wording to send;
- whether to open an inquiry;
- which authority to request;
- which operational realization to select;
- whether to execute;
- whether the goal is permanently satisfied;
- how to prioritize coexisting needs.

Minimum fields, if implemented later:

```text
projection_id
selection_ref
selected_goal_establishment_id
input_goal_establishment_ref
projection_state: sufficient_for_now | clarification_needed | inquiry_needed | authority_needed | operational_realization_needed | blocked | unknown | conflict
coexisting_need_states: tuple[...]          # optional, unordered
primary_evidence_refs: tuple[...]
sufficiency_evidence_refs: tuple[...]
boundary_evidence_refs: tuple[...]
clarification_evidence_refs: tuple[...]
inquiry_evidence_refs: tuple[...]
authority_evidence_refs: tuple[...]
operational_realization_evidence_refs: tuple[...]
unknowns
conflicts
read_only=true
selects_next_action=false
authorizes_transition=false
opens_inquiry=false
requests_authority=false
selects_operational_realization=false
starts_execution=false
judges_goal_satisfaction=false
writes_event_ledger=false
mutates_cluster=false
```

The name should stay around **need projection**, not advancement manager, planner, router, scheduler, or satisfaction judge.

## Outcome vocabulary revised by repository evidence

The candidate outcomes are mostly lawful as need states, but only if they are read as present-tense projection states, not as commands. Repository evidence suggests these refinements:

| Candidate | Lawful? | Repository-revised meaning |
| --- | --- | --- |
| `sufficient_for_now` | Yes | Available evidence supports no additional clarification, inquiry, authority, or operational-realization need for this exact selected goal at the current boundary. It does not mean the goal is permanently satisfied. |
| `clarification_needed` | Yes | The selected goal evidence is deficient in operator meaning, scope, acceptance, stop/sufficiency condition, or ambiguous/conflicting intent such that the deficiency must be resolved by operator-facing clarification rather than by repository inquiry alone. |
| `inquiry_needed` | Yes | The selected goal is sufficiently identified, but available knowledge/evidence is insufficient or unresolved for bounded understanding. This points to an evidence-gathering or question frontier need, not to action authorization. |
| `authority_needed` | Yes | Available evidence indicates missing or unavailable authority/permission/scope for movement. This is distinct from knowledge sufficiency and from operational mechanism readiness. |
| `operational_realization_needed` | Yes | The selected goal has enough meaning and authority boundary for considering implementation mechanics, but no warranted operational realization or implementation-backed mechanism is available for the needed movement. It does not select a mechanism. |
| `blocked` | Yes, but narrow | Movement is visibly stopped because a required upstream boundary is refused, unsupported, unavailable, or non-resolvable within available evidence. It should preserve the blocking boundary and not invent a recovery plan. |
| `unknown` | Yes | Available evidence cannot lawfully classify the need because required evidence is absent, stale, outside scope, or owned by a missing stage. Unknown is not clarification, inquiry, or authority by default. |
| `conflict` | Yes | Available evidence contains incompatible selected-goal, sufficiency, boundary, authority, or realization facts. Conflict should dominate silent movement, but it still does not authorize resolution. |

No repository evidence requires splitting the vocabulary now. The main revision is semantic: these are projection states or unordered coexisting need states, not transitions.

## What evidence establishes sufficiency for now?

Sufficiency for now requires positive and negative evidence.

Positive evidence may include:

1. `GoalInquiryConsiderationSelection.selection_state == selected` with exactly one `selected_goal_establishment_id`.
2. The supplied `BoundedOperatorGoalEstablishment.goal_establishment_id` matches the selected identity.
3. The bounded goal is at least established or provisionally established in a way that the repository already treats as enough orientation for reversible continuation.
4. Existing `sufficiency_conditions` are present and are not contradicted by unresolved scope, unknowns, ambiguities, conflicts, or known loss relevant to present movement.
5. Existing `stop_conditions` do not identify a current stop for the movement under consideration.
6. Boundary evidence shows no authority, inquiry, or operational-realization gap at this exact present boundary.

Negative evidence is just as important:

- no conflicts on the selection or selected goal;
- no selected-goal identity mismatch;
- no unresolved operator-facing scope that must be clarified before any lawful movement;
- no knowledge/evidence gap that the repository already marks as necessary for understanding;
- no unavailable authority standing or scope boundary;
- no missing operational realization when the next movement would require one.

Because `BoundedOperatorGoalEstablishment` says goal establishment is not goal satisfaction, sufficiency for now must not be rendered as `satisfied`. The safer meaning is: no presently visible advancement need at the read-only projection boundary.

## What distinguishes clarification need from inquiry need?

Clarification need is operator-meaning deficient. Evidence includes missing/ambiguous/conflicting focus identity, unresolved goal scope, ambiguous intended outcome, missing acceptance provenance, missing or unclear sufficiency/stop conditions, or operator constraints that cannot be interpreted without asking the operator. It asks for disambiguation of the goal or operator intent.

Inquiry need is world/repository-evidence deficient after the selected goal is sufficiently identified. Evidence includes unknown facts, missing support, unresolved repository knowledge, absent observations, or unanswered bounded questions required to understand whether or how the selected goal may move. It asks for investigation, not for the operator to restate the goal.

The distinction is not whether information is missing in general. It is who owns the missing boundary:

```text
operator meaning / goal scope / acceptance boundary -> clarification_needed
repository evidence / knowledge / observation boundary -> inquiry_needed
```

This preserves `goal deficient != knowledge deficient`.

## What distinguishes inquiry need from authority or operational need?

Inquiry need means evidence is insufficient to know. Authority need means evidence may be known, but movement is not permitted or scope/permission is unavailable. Operational-realization need means the repository may know enough and may have enough authority boundary to consider movement, but lacks a warranted means/mechanism/implementation path for the needed movement.

Practical distinction:

```text
Need to learn whether/what is true -> inquiry_needed
Need permission/scope/authority before movement -> authority_needed
Need a warranted mechanism or implementation route -> operational_realization_needed
```

Operational realization evidence must remain downstream-owned. Existing operational-realization selection and warrant surfaces show that selecting a candidate and warranting reliance are separate from authorization and execution. Therefore a need projection may say operational realization is needed or missing, but it may not select a realization, warrant it, authorize it, schedule it, or execute it.

## May several needs coexist without priority?

Yes. Several needs may coexist and should remain unordered unless a future owner lawfully establishes priority. Examples:

- unresolved goal scope and missing repository evidence can coexist as `clarification_needed` plus `inquiry_needed`;
- missing authority and missing operational realization can coexist, because authority and mechanism readiness are distinct;
- conflict can coexist with unknowns, but the projection should not hide either;
- sufficient evidence for understanding can coexist with lack of movement authority, preserving `knowledge sufficient != movement authorized`.

The projection can expose `coexisting_need_states` or evidence buckets without choosing a primary next action. If a single `projection_state` is required for compatibility, it should be a display classification only, with all coexisting needs preserved. Any priority order would be a separate responsibility.

## Does an existing owner already perform this projection?

No reviewed owner performs exactly this projection.

Adjacent owners are narrower:

- `GoalInquiryConsiderationSelection` selects one visible bounded goal for consideration and explicitly refuses inquiry opening, work authorization, execution, recording, or mutation.
- `BoundedOperatorGoalEstablishment` establishes goal identity, scope, sufficiency, stop conditions, unknowns, ambiguities, conflicts, lineage, and non-authority flags, but does not project present advancement need.
- `GoalOrientationInventory` shows dimensions and associated material without planning, priority, movement, authorization, or mutation.
- Minimum-lawful-advancement explanations explain already-known stage boundaries, but the recurrence audit warns against turning one explanation grammar into a universal owner across stages.
- Operational-realization selection and warrant own candidate selection and reliance warranting after capability/reachability stages, not selected-goal need classification.

Therefore the responsibility is currently missing if Seed needs an executable read-only answer to this exact question.

## Is one read-only implementation slice warranted?

Yes, but only one small slice is warranted, and only if the repository needs the answer to be executable rather than documented.

The slice should consume one already-produced `GoalInquiryConsiderationSelection`, one matching `BoundedOperatorGoalEstablishment`, and optional already-produced evidence snapshots. It should emit only a read-only need projection with explicit non-authority flags. It should not introduce a planner, priority queue, inquiry manager, authority-request manager, operational-realization selector, execution scheduler, or satisfaction judge.

A first implementation should probably avoid CLI exposure unless explicitly requested. If it becomes a diagnostic, audit, probe, view, operational CLI flag, or recordable output, the repository operational visibility contract requires diagnostic inventory registration, diagnostic shape-audit specs, and tests proving both surfaces.

## Smallest missing responsibility

The smallest missing responsibility is:

```text
Classify the presently visible advancement need, if any, for one exact selected bounded goal by reading the selected goal's existing sufficiency, unresolved-scope, unknown, conflict, authority, and operational-boundary evidence, while preserving that the classification does not select or authorize the next movement.
```

This is smaller than clarification generation, inquiry-frontier creation, authority request, operational-realization selection, scheduling, execution, or goal-satisfaction judgment.

## Exact next bounded question

```text
What is the minimal read-only `GoalAdvancementNeedProjection` artifact that consumes one `GoalInquiryConsiderationSelection` in `selected` state plus the matching `BoundedOperatorGoalEstablishment` and already-available sufficiency/boundary evidence, emits unordered need-state evidence for `sufficient_for_now`, `clarification_needed`, `inquiry_needed`, `authority_needed`, `operational_realization_needed`, `blocked`, `unknown`, and `conflict`, and proves that no clarification, inquiry frontier, authority request, realization selection, transition authorization, execution, scheduling, priority, or satisfaction judgment occurred?
```

## Conclusion

The lawful boundary is a read-only need projection over one exact selected bounded goal and already-available evidence. It may classify present visible needs, including sufficiency for now, clarification, inquiry, authority, operational realization, blocked, unknown, and conflict. Repository evidence does not support treating selection as deficiency, deficiency as knowledge deficiency, knowledge sufficiency as authorization, unnecessary inquiry as permanent satisfaction, or need identification as next-action selection. Multiple needs may coexist without priority. No existing owner performs this exact selected-goal advancement-need projection. One small read-only implementation slice is warranted if an executable surface is needed.

Goal advancement need audit complete.
