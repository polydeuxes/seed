# Orthogonal Goal Inventory Topology Audit 001

## Question

Determine whether Seed needs a read-only inventory of orthogonal goal pressures where one goal may have zero or more inquiries, and one inquiry may surface evidence relevant to several goals without activating those goals.

## Evidence reviewed

- `constitution.md` for Null persistence, pressure/inquiry boundaries, frontiers, responsibility ownership, and the explicit refusal to invent a total goal system.
- `seed_runtime/models.py` for the projected `Goal` artifact shape.
- `seed_runtime/state.py`, `seed_runtime/state_patches.py`, `seed_runtime/context.py`, and `seed_runtime/context_selection.py` for existing goal projection, creation, context selection, and active-goal ordering behavior.
- `seed_runtime/bounded_operator_goal_establishment.py` and `tests/test_bounded_operator_goal_establishment.py` for the newer read-only bounded operator goal establishment shape.
- `seed_runtime/inquiry_orientation.py` and `tests/test_inquiry_orientation.py` for evidence that inquiry notes and incidental related material do not create goals, plans, authorizations, or projected truth.
- `constitutional_conservation_characterization.md`, `constitutional_authority_characterization.md`, `architectural_frontier_characterization.md`, `inquiry_eligibility_characterization.md`, `operator_methodological_selection_characterization.md`, and `report_outcome_and_inquiry_selection_boundary_audit.md` for repository-level separation among pressure, visibility, bounded inquiry, selection, implementation readiness, authority, and stop states.

## Current goal-like responsibilities already present

Seed already preserves several goal-like or pressure-like responsibilities, but they are not one unified inventory:

| Responsibility | Current evidence | What it owns | What it refuses |
|---|---|---|---|
| Projected runtime `Goal` | `Goal` model plus event projection and context selection | A persisted projected goal with summary, status, facts, open questions, and related entities | Orthogonal goal categories, dormant pressures, constitutional meta-targets, Null preservation, inquiry mapping |
| Goal creation from state patches | `StatePatchApplier` creates `goal.created` events | Mutating projected state by explicit patch operation | Read-only inventory; dormant or Null goal pressure |
| Context active-goal selection | `order_goals(...)` and context packet composition | Deterministic active-first context presentation | Priority governance; orthogonal pressure topology; dormant pressure visibility |
| Bounded operator goal establishment | `BoundedOperatorGoalEstablishment` | Read-only establishment/provisional establishment/refusal from lawful ingress evidence | Inquiry opening, resource observation, constraint enforcement, authorization, execution, recording, satisfaction judging |
| Inquiry orientation | `InquiryOrientationView` | Read-only lexical orientation from preserved operator prose to already projected material | Goals, facts, requirements, capabilities, decisions, plans, authorizations, commands, recommended actions, next safe moves |
| Pressure/frontier reports | Constitution and characterization reports | Preserve visible pressure, insufficient evidence, frontier-only pressure, and stop results | Planner, priority order, schedule, roadmap mandate, autonomous obligation |
| Capability recovery / verification | Capability candidates, verification, inventory reports | Candidate/support/verification distinctions | Permission, tool invocation, execution, policy approval |
| Diagnostic/read-only inventories | Diagnostic inventory and shape audit conventions | Operational visibility of surfaces and non-mutation boundaries | Cluster mutation and automatic truth promotion |

This means Seed already has local goal-adjacent owners, but no owner that can list all preserved goal pressures across operator interaction, operational continuity, resource stewardship, capability recovery, knowledge quality, maintenance, and outstanding commitments.

## Do these responsibilities share one constitutional artifact shape?

No. Repository evidence supports a repeated constitutional discipline, not one shared artifact class.

The shared discipline is:

```text
Null / unknown / uncommitted
-> observation
-> bounded unknown
-> inquiry
-> evidence
-> supported transition or explicit stop
-> bounded handoff artifact
```

That discipline appears in goal establishment, inquiry orientation, pressure visibility, capability verification, diagnostics, and frontiers. However, the artifact shapes are family-local:

- projected `Goal` is mutable projected state;
- `BoundedOperatorGoalEstablishment` is read-only ingress establishment evidence;
- inquiry notes are probe-local preserved operator prose;
- frontiers are report-level pressure preservation;
- capability candidates and verification surfaces have their own candidate/support/admission boundaries;
- diagnostics have inventory and shape-audit boundaries.

Therefore the repository supports a cross-family constitutional rule, but not one constitutional artifact shape that all goal-like responsibilities already share.

## What it means for a goal to remain on Null

A goal pressure remains on Null when no repository evidence has justified even a bounded, provisional, active, dormant, blocked, sufficient-for-now, closed, or conflict state for that pressure.

Null means:

- no preserved goal artifact is claimed;
- no bounded inquiry is opened merely because the pressure is imaginable;
- no owner is assigned;
- no work is authorized;
- no priority order exists;
- no autonomous obligation is created;
- incidental evidence may be noticed later, but the pressure has not yet earned a state.

Null is not denial. It is the lawful preservation of unknown/uncommitted status until evidence justifies movement.

## Lawful visible states without becoming work

Repository authority supports visible states that do not become work, provided they are read-only and boundary-preserving:

| State | Lawful meaning for an inventory | Not allowed to imply |
|---|---|---|
| Null | No sufficient evidence to classify the pressure yet | Hidden backlog item, denied concern, task |
| Provisional | Some ingress or evidence orients the pressure but unresolved scope remains | Work authorization, sufficiency, execution |
| Bounded | The pressure has a scoped description or bounded question | Active inquiry, priority, scheduling |
| Active | Existing projected `Goal.status` may be active, or a bounded inquiry may be underway elsewhere | Global top priority or autonomous obligation |
| Blocked | Existing projected goal status may be blocked, or an audit may stop on missing evidence | Failure, retry mandate, escalation |
| Dormant | Preserved pressure has no active inquiry and no current authorization | Forgetting, closure, queued work |
| Sufficient-for-now | A bounded question or local surface has enough evidence for its role | Global satisfaction, no future relevance |
| Closed | A local goal/inquiry/report result is complete in its family | Adjacent pressure disappearance |
| Conflict | Evidence supports incompatible interpretations or boundaries | Automatic conflict resolution or priority arbitration |

The inventory may display these states only as descriptive preservation. It must not implement transitions among them.

## How incidental evidence may increase a dormant goal's resolution

Incidental evidence can increase a dormant goal's resolution when an authorized inquiry, diagnostic, or report produces evidence that is explicitly relevant to the dormant pressure's already-preserved boundary.

Example topology:

```text
Inquiry A investigates diagnostic visibility.
Evidence from Inquiry A also shows resource stewardship implications.
Resource stewardship pressure can gain a supporting evidence reference.
Resource stewardship does not become active unless separately bounded and authorized.
```

The lawful movement is not `evidence -> activation`. It is:

```text
incidental evidence
-> preserved relevance/reference/unknown reduction
-> optional later bounded question if an operator or repository-backed owner asks
```

This preserves the distinction:

```text
evidence relevant to a goal != activation of that goal
```

## How one inquiry may relate evidence to several goals without activating them

One inquiry can produce evidence with several relevance edges:

```text
one inquiry
-> evidence item E
-> relevant_to operator interaction
-> relevant_to operational continuity
-> relevant_to resource stewardship
-> relevant_to knowledge quality
```

The required boundary is that each edge is read-only and evidentiary. It says only: this evidence may bear on this preserved goal pressure. It does not say:

- the goal is bounded;
- the goal is active;
- an inquiry frontier moved;
- an operation is authorized;
- work should be scheduled;
- a planner has ranked the pressures.

The shape should be many-to-many evidence relevance, not inquiry ownership transfer.

## Can an existing owner list all preserved goals?

No existing implementation owner appears able to list all preserved goal pressures.

- Projected state can list persisted `Goal` objects, but that is only mutable runtime goal state.
- Context selection can choose an active goal for context, but it intentionally orders active goals first and truncates for decision input, not complete constitutional preservation.
- Bounded operator goal establishment can establish one bounded operator goal artifact from lawful ingress evidence, but it is not an inventory over all goal pressures.
- Inquiry orientation can relate one note to existing projected material, but it explicitly refuses to create goals, plans, authorizations, or next moves.
- Pressure/frontier reports preserve pressure, but they are report-local and do not provide a canonical read-only listing owner.

Thus the missing owner is not a planner or queue. The missing owner, if warranted, is a read-only lister of preserved goal-pressure records and their evidence relevance boundaries.

## Is a read-only `GoalInventory` or `GoalStateInventory` warranted?

A read-only inventory is warranted as a characterization-level missing responsibility, but implementation readiness is not yet established by this audit alone.

The repository has enough evidence to say the topology is real and currently fragmented:

```text
operator goal != operational goal != resource goal != constitutional meta-target
visible pressure != bounded goal != active inquiry != authorized operation
```

A lawful inventory would need to be explicitly constrained:

- read-only;
- no transitions;
- no scheduling;
- no priority order;
- no autonomous obligation;
- no resource governance;
- no activation;
- no inquiry-frontier movement;
- no execution authorization;
- no event-ledger write unless a separate recording boundary is explicitly designed;
- if diagnostic, visible in diagnostic inventory and shape audit under the repository operational visibility contract.

`GoalStateInventory` is the safer name if the surface lists states of preserved pressures. `GoalInventory` is shorter but risks sounding like a task queue. If implemented later, its boundary text should make the guardrails first-class.

## Smallest missing responsibility

The smallest missing responsibility is:

> Read-only enumeration of preserved orthogonal goal-pressure records, including category, current evidence-backed state, unresolveds, conflicts, and evidence relevance references, while refusing transition, priority, activation, authorization, planning, scheduling, resource governance, and execution.

This owner would not create the pressures it lists. It would only render already-preserved pressures and evidence links from bounded sources.

## Exact next bounded question

```text
Which existing repository artifact family can lawfully supply the source records for a read-only GoalStateInventory without converting pressure, inquiry notes, projected goals, or frontier observations into tasks, priorities, or authorized work?
```

## Conclusion

Seed needs the topology distinction: orthogonal goal pressures can be visible, Null, provisional, bounded, active, blocked, dormant, sufficient-for-now, closed, or conflict without becoming work. Existing artifacts preserve pieces of this distinction, but no existing owner can list all preserved goal pressures across families. A read-only `GoalStateInventory` is warranted as the smallest missing responsibility if and only if a later bounded implementation inquiry identifies lawful source records and preserves the guardrails above.

Orthogonal goal inventory topology audit complete.
