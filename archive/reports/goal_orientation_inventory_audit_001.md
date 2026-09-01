# Goal Orientation Inventory Audit 001

## Scope

This audit determines the lawful read-only boundary for answering the operator-facing question:

```text
List all goals.
```

It investigates whether the following materials may be assembled without changing goal state:

```text
supported orthogonal goal dimensions
+
preserved goal pressures
+
BoundedOperatorGoalEstablishments
+
available inquiry references
→ GoalOrientationInventory
```

The inventory boundary must distinguish:

```text
dimension
!= pressure
!= bounded goal
!= active inquiry
```

This audit does not implement transitions, activation, prioritization, scheduling, authorization, execution, resource governance, planning, inquiry opening, event-ledger recording, or cluster mutation.

## Executive determination

A lawful `GoalOrientationInventory` may answer `List all goals` only as a read-only orientation inventory over distinct goal-adjacent materials. The answer may list:

1. supported orthogonal goal dimensions, including dimensions on Null;
2. preserved pressure evidence where an existing pressure-owning surface already emits pressure;
3. bounded operator goal establishments where a `BoundedOperatorGoalEstablishment` artifact exists;
4. available inquiry references where existing inquiry, handoff, or artifact-visibility surfaces preserve such references.

The inventory must not collapse those rows into one kind of goal. The lawful interpretation is:

```text
all goal-oriented dimensions
!= all established goals
!= all active work
```

A dimension on Null is visible as a known responsibility neighborhood with no established pressure or bounded goal. It is not a hidden task. A visible pressure is not an activated goal. A bounded goal establishment is not inquiry authority, work authorization, execution authority, or satisfaction judgment.

## Existing artifacts that can lawfully supply inventory material

### Dimensions

`orthogonal_goal_dimension_boundary_audit_001.md` is the current strongest source for supported dimension labels. It supports six dimensions named by the current goal-orientation context:

| Dimension | Lawful source status | Inventory boundary |
| --- | --- | --- |
| operator interaction | Supported as a weak responsibility neighborhood around admitted operator input and read-only orientation. | May appear even on Null; not a semantic intent parser or task queue. |
| operational continuity | Supported by execution visibility, diagnostics, inventory, and operational graph responsibilities. | May appear even on Null; not a scheduler or remediation loop. |
| resource stewardship | Cautiously supported by state-build/cache/performance/cost-adjacent diagnostic visibility. | May appear even on Null; not budget authority or automatic optimization. |
| capability recovery | Supported by capability candidates, verification, promotion readiness, capability inventory, operation contracts, and validation. | May appear even on Null; not automatic capability creation or provider/tool execution. |
| knowledge quality | Supported by observation/evidence/fact boundaries, reachability, support/conflict projection, Unknown preservation, and diagnostic-vs-cluster truth boundaries. | May appear even on Null; not automatic truth promotion or ontology expansion. |
| implementation maintenance | Supported by responsibility-family completion, readiness, slices, remaining compressed-boundary reports, and diagnostic-inventory discipline. | May appear even on Null; not roadmap, backlog, priority order, or obligation. |

The prior audit also tested an `Outstanding commitments` candidate, but the present inventory question names six supported dimensions. The lawful inventory can preserve `Outstanding commitments` only as adjacent or previously tested commitment-shaped material, not as one of the six current supported orthogonal goal dimensions unless a later authority re-admits it.

### Preserved goal pressures

Existing pressure material may be supplied by already implemented pressure surfaces, especially `pressure_audit`. The implementation defines `PressureItem` with category, score, evidence, reason, and recommended inspection command, and `PressureAudit` with a tuple of pressures. `build_pressure_audit` explicitly ranks operational pressure without planning, recording, or mutating state.

`inquiry_artifacts` also identifies `pressure` as only partially visible and states that implementation-backed operational pressure visibility does not infer inquiry pressure transformation. Therefore a `GoalOrientationInventory` may point to preserved pressure rows, but it must label them as pressure evidence rather than established goals.

### Bounded goals

`BoundedOperatorGoalEstablishment` can lawfully supply bounded-goal material only when such artifacts are available to the inventory caller. Its boundary is explicit: goal established is not inquiry opened, resources observed, constraints satisfied, work authorized, or goal satisfied. The dataclass preserves establishment state, intended outcome, scope, sufficiency and stop conditions, unknowns, ambiguities, conflicts, lineage, and read-only/no-ledger/no-mutation flags.

The existing legacy `Goal` model in `seed_runtime/models.py` is a cluster/runtime model with status, facts, open questions, and related entities. It may be relevant to existing application state, but it does not by itself satisfy the newer bounded-goal establishment boundary because it lacks the `BoundedOperatorGoalEstablishment` artifact's ingress lineage, sufficiency, stop-condition, and non-authority flags. Repository authority therefore favors bounded establishment artifacts for this audit's bounded-goal lane.

### Available inquiry references

Available inquiry references may be listed only when existing artifacts already preserve them. Lawful sources include:

- `BoundedOperatorGoalEstablishment.ingress_lineage`, `operator_acceptance_provenance`, and correction references, which can orient back to ingress evidence without opening an inquiry;
- inquiry or handoff artifacts that explicitly carry inquiry references, such as bounded constitutional question handoffs, authority-scope handoffs, examination-frontier or work-selection references, and membership evidence sets;
- `inquiry_artifacts`, which can state whether artifact kinds such as unknown, boundary, pressure, finding, supported/unsupported conclusion, open question, and gap are repository-visible, partially visible, document-visible, or unknown.

An inquiry reference is not an active inquiry unless the source artifact positively says so. A future handoff or open question is a reference or orientation affordance, not execution authority.

## Null and unsupported dimensions remain visible without becoming tasks

A supported dimension may remain on Null. In inventory output, Null should mean:

```text
known dimension + no established pressure + no bounded goal + no active inquiry reference available for that dimension
```

Null should not be rendered as omission if the question is `List all goals`, because omission would hide the distinction between unsupported material and a supported dimension with no current goal material. The row may say `state: Null` or equivalent, but it must also carry a boundary note such as:

```text
Null dimension is visible for orientation only; it is not a hidden task, pressure, bounded goal, active inquiry, queue item, or priority.
```

Unsupported dimensions should remain visible only when the inventory has an evidence-preserving lane for unsupported or adjacent material. For example, a rejected or not-currently-supported dimension label can be preserved as `unsupported_candidate_dimension` or `adjacent_not_in_dimension_set`, with source evidence and Unknowns/conflicts, instead of being silently converted into a seventh goal dimension.

## Cardinality: one inventory entry may contain zero or more pressures and goals

One inventory entry may lawfully contain zero or more pressures, zero or more bounded goal establishments, and zero or more inquiry references, because a dimension is a responsibility neighborhood, not the pressure or goal itself.

The cardinality rule is:

```text
GoalOrientationInventoryEntry
  dimension: exactly one supported dimension label
  pressures: zero or more preserved pressure references
  bounded_goals: zero or more BoundedOperatorGoalEstablishment references
  inquiry_references: zero or more available inquiry references
  unknowns/conflicts: zero or more preserved uncertainty records
```

This does not create priority order, queue order, work order, or activation state. Multiple pressures in one dimension remain multiple pressure rows. Multiple bounded goals in one dimension remain multiple bounded establishments. A dimension with zero pressures and zero goals remains visible on Null.

## Duplicate, conflicting, Unknown, and cross-dimensional material

### Duplicates

Duplicate pressure or goal material should be preserved by stable source identity rather than merged semantically. If two rows point to the same pressure item or establishment artifact, the inventory may de-duplicate by artifact identity while preserving all source references. If two rows share wording but lack identical source identity, they should not be merged merely because the wording is similar.

### Conflicts

Conflicts must remain conflicts on the material that owns them. For bounded goals, the establishment artifact has a `conflicts` lane. For pressure, the source pressure evidence can include conflict-shaped evidence such as ownership ambiguity or diagnostic-shape mismatches. The inventory may aggregate conflict visibility but must not resolve conflicts.

### Unknown

Unknown must be preserved as Unknown rather than converted to no-goal or no-pressure. Missing inquiry reference evidence means `inquiry_reference_state: unknown` or `none_visible_from_available_sources`, depending on whether the source positively shows absence or merely lacks evidence. A missing dimension mapping for a pressure should remain `dimension_mapping: unknown` instead of being force-assigned.

### Cross-dimensional material

A pressure, bounded goal, or inquiry reference may be relevant to more than one dimension. Cross-dimensional material should be represented either by repeated references with the same source identity under each relevant dimension, or by a relation list such as `also_relevant_to`. It must not be treated as proof that the dimensions collapse, that one dimension owns another, or that a priority relation exists.

## Does an existing owner already assemble this view?

No existing owner appears to assemble the requested `GoalOrientationInventory` view.

Existing owners are local:

- `orthogonal_goal_dimension_boundary_audit_001.md` supplies audit-local dimension boundary vocabulary;
- `pressure_audit` supplies operational pressure rows only;
- `BoundedOperatorGoalEstablishment` supplies bounded operator-goal establishment artifacts only;
- `inquiry_artifacts` supplies artifact-visibility classifications and non-planning boundaries;
- question-surface inventory and bounded-ask dispatch own admitted question-family visibility and dispatch mechanics;
- diagnostic inventory and shape audit own operational diagnostic visibility governance.

No reviewed artifact currently joins the six supported dimensions to pressure rows, bounded establishment artifacts, and inquiry references while preserving the non-collapse boundaries.

## Is one read-only implementation slice warranted?

One read-only implementation slice is warranted only if the product requirement is to answer `List all goals` from live repository/runtime materials rather than from this audit prose. The warranted slice would be intentionally narrow:

```text
Build GoalOrientationInventory from supplied/available read-only sources,
render one entry per supported dimension,
attach references to existing pressure items, bounded-goal establishments,
and inquiry references when available,
and preserve Null/Unknown/conflict/non-authority notes.
```

That slice must not implement transitions, activation, prioritization, scheduling, authorization, execution, resource governance, or a planner. If exposed as a diagnostic or CLI surface, the repository's operational visibility contract would require diagnostic inventory and diagnostic shape-audit updates plus tests proving the new surface appears and is shape-checked.

If no live answer surface is needed, this audit-local characterization is sufficient and implementation should stop.

## Smallest missing responsibility

The smallest missing responsibility is a read-only assembler, not a registry or planner:

```text
Given the six supported goal dimensions and supplied existing artifacts,
assemble a non-authoritative inventory entry per dimension that preserves
pressure, bounded-goal, inquiry-reference, Null, Unknown, duplicate,
conflict, and cross-dimensional evidence without changing any state.
```

The missing responsibility is not goal establishment, not inquiry opening, not queue creation, not priority ranking, not work authorization, and not resource governance.

## Exact next bounded question

```text
Does Seed need an implemented read-only GoalOrientationInventory answer surface for `List all goals`, backed by existing dimension, pressure, bounded-goal establishment, and inquiry-reference artifacts, or should the lawful boundary remain audit-local until a concrete caller/consumer requires it?
```

This is a bounded preservation and consumer-need question. It is not a request to implement execution, transition, priority, scheduling, authorization, or resource governance.

## Conclusion

The lawful read-only boundary for answering `List all goals` is an orientation inventory, not a goal registry. It may list all six supported dimensions even when some are on Null; attach zero or more pressure references, bounded-goal establishments, and inquiry references to each dimension; and preserve duplicate, conflicting, Unknown, unsupported, and cross-dimensional material without resolving it.

No existing owner already assembles this exact view. A smallest implementation slice is warranted only if a live read-only answer surface is required. The missing responsibility is a non-authoritative assembler that preserves distinctions, not a planner or executor.

Goal orientation inventory audit complete.
