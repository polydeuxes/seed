---
doc_type: observation
status: exploratory
domain: participant orientation and view selection
related:
  - view_branch_continuity_reconciliation.md
  - lens_view_reconciliation.md
  - lens_view_architecture_audit.md
  - lens_vs_orientation_observation.md
  - inquiry_as_bridge_observation.md
  - inquiry_as_movement_observation.md
  - unresolvedness_observation.md
---

# Participant Orientation View Selection Observation

## Status

Exploratory observation only.

This document investigates a pressure left unresolved after View continuity
reconciliation:

```text
If View authority is largely reconciled,
where does participant pressure actually enter?
```

It does not modify implementation, State Summary, Inquiry Orientation, command
structure, ontology, runtime concepts, or policy. It does not conclude that a
participant layer exists, that View selection should be implemented, that
Orientation should become ontology, that Inquiry should become runtime state, or
that State Summary should be redesigned.

Repository authority remains with implementation, tests, catalogs, and more
specific reconciliations in their own scopes.

## Question

The central exploratory questions are:

```text
Where does participant pressure enter?
How does a participant arrive at a View?
What role do Inquiry, Orientation, Current Work Position, Active Edge, Concern,
and Continuation play?
Are they participating in View selection, View use, View interpretation, or
something else entirely?
```

The candidate chain tested was:

```text
participant
    -> concern
    -> inquiry
    -> orientation
    -> view selection
    -> view
    -> lens
    -> State
```

The investigation does not assume that any step exists, that the order is
correct, or that the chain is real.

## Repository evidence reviewed

Required View authority materials reviewed:

- `docs/lens_view_reconciliation.md`
- `docs/lens_view_architecture_audit.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`
- `docs/impact_overview_authority_reconciliation.md`
- `docs/state_summary_scope_review.md`
- `docs/view_branch_continuity_reconciliation.md`

Required Inquiry / Orientation materials reviewed:

- `docs/lens_vs_orientation_observation.md`
- `docs/inquiry_as_bridge_observation.md`
- `docs/inquiry_as_movement_observation.md`
- `docs/unresolvedness_observation.md`
- `docs/descriptive_language_vs_authority_observation.md`
- `docs/authority_owner_observation.md`
- `docs/repository_surface_inventory_observation.md`
- `docs/bounded_consequence_discipline_observation.md`

Additional evidence sampled because the required materials pointed to it:

- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/relation_of_use_observation.md`
- `docs/operator_pressure_as_evidence_observation.md`
- `seed_runtime/inquiry_orientation.py`
- `tests/test_inquiry_orientation.py`

Search terms included `participant`, `operator`, `attention`, `activation`,
`selection`, `focus`, `current relevance`, `current work position`, `active
edge`, `concern`, `continuation`, `orientation`, `inquiry`, `view selection`,
`surface`, and `State Summary`.

## Participant investigation

Repository evidence contains participant-adjacent pressure, but not strong
evidence for `participant` as a current repository concept or layer.

The strongest participant-related patterns are indirect:

- View and surface documents ask who the consumer is and what authority the view
  owns. This introduces a consumer/operator side of the interaction without
  making that consumer an architectural object.
- Orientation documents repeatedly connect orientation to attention, relevance,
  pressure, activation, continuity, and the relationship between a participant
  and what Seed knows.
- Operator-pressure work treats operator pain as valuable evidence that can
  direct attention, while explicitly refusing to let that pressure become direct
  implementation authority.
- Relation-of-use work distinguishes knowledge that is merely available from
  knowledge that is governing present work, and describes usefulness as a
  relation to present concern, consequence, or continuation point.

Candidate participant-related vocabulary therefore appears as:

```text
operator / consumer / later participant
attention
activation
selection
focus
current concern
current relevance
continuation need
```

This differs from View, Lens, and State in the evidence reviewed:

- State is the projected read model derived from events.
- Lens is an exploratory bounded way of viewing projected State or repository
  knowledge for a question, attention pattern, or interpretive purpose.
- View is an implemented or operator-facing read surface that exposes selected
  material under a bounded authority.
- Participant pressure appears to explain why a view or surface matters now, not
  what State contains or what a View is authorized to expose.

This is only a pattern. No reviewed authority establishes a participant layer.

## Inquiry investigation

Inquiry evidence does not reduce cleanly to View selection.

`Inquiry As Bridge` found that inquiry behaves as a mixture of question, gap,
tension, pressure, unknown, investigation target, and comparison request. It
could be preserved as a note, made active by pressure, routed through knowledge
navigation, or carried forward as continuation context.

`Inquiry As Movement` weakens an object-like reading further: inquiry may be
movement through unresolvedness or a relationship to unresolvedness rather than
a stable object between Lens and Orientation. Implementation evidence supports
`InquiryNoteRecord` and `InquiryOrientationView`, not an `Inquiry` runtime
object. The authority boundary in `seed_runtime/inquiry_orientation.py` also
refuses promotion of a note into fact, claim, goal, tool need, requirement,
capability, decision, proposal, plan, authorization, command, runtime
instruction, intent, concern, recommended action, or next safe move.

Exploratory reading:

```text
Inquiry can participate before, during, or after View use.
```

It may shape why someone is looking, preserve unresolvedness, or supply lexical
material for an orientation view. It is not currently evidence of a formal View
selection mechanism.

## Orientation investigation

Orientation appears more naturally related to participant pressure and
continuation than to View alone, but the evidence remains mixed.

`Lens Vs Orientation` tested the distinction:

```text
State answers: What exists?
Lens answers: How is State being viewed?
Orientation answers: Where is attention currently directed?
```

That document treated the distinction as a candidate observation, not a
conclusion. It also observed that State Summary confusion may come from mixing
State description, Lens behavior, and Orientation behavior.

`Inquiry Orientation` implementation is especially ambiguous. It is a concrete
read-only view about a preserved inquiry note and related projected material, so
it behaves like a View. But its purpose is orientation around operator prose,
uncertainty, and authority boundaries, so it also carries participant-facing
pressure. The surface inventory describes Inquiry Orientation as accepting
preserved operator prose plus projected read models and returning a bounded
related-material view, while refusing promotion to action, plan, command, or
runtime instruction.

Exploratory reading:

```text
Orientation may be a relation between participant pressure and available
surfaces, sometimes rendered through a View.
```

This does not prove Orientation is a surface, nor that it is not a surface. It
suggests that Orientation can be view-shaped without being exhausted by View
authority.

## View selection investigation

Direct evidence for an implemented `View selection` mechanism was not found in
the required materials.

Evidence does support adjacent behaviors:

- View authority asks who the consumer is and what authority the view owns.
- Navigation surfaces ask where the operator should go next.
- Lens-like behavior selects, groups, ranks, suppresses, caveats, or classifies
  projected content for a bounded question.
- Current Work Position and Active Edge discuss what is active, why it is active,
  and what currently pulls work forward.
- Selection-and-attention evidence, cited from Active Edge materials, separates
  selection, priority, relevance, active attention, and working state.

Those patterns may explain how a participant arrives at a View descriptively:

```text
pressure / concern / unresolvedness
    -> attention or activation
    -> orientation or navigation
    -> use of a bounded surface
```

However, this is not a repository mechanism. It is safer to say the repository
has evidence of view-use pressure and navigation pressure, not a defined View
selection layer.

## Current Work Position / Active Edge investigation

Current Work Position and Active Edge appear to describe a participant or work
relation more than State itself.

Current Work Position is described in adjacent frontier and relation-of-use work
as selected, bounded, continuation-relevant orientation: what is active, why it
is active, what unresolved pressure it occupies, what authority and validation
boundaries constrain it, and what movement is safe.

Active Edge asks what currently pulls work forward among preserved concerns,
questions, gaps, contradictions, relationships, or frontiers. It is explicitly
not assumed to be an object, role, operation, relationship, attention state,
selection result, priority, or inquiry object.

Exploratory distinction:

```text
State preserves projected knowledge.
View exposes bounded material.
Current Work Position / Active Edge describe why some preserved material is
currently live for continuation.
```

This supports participant-pressure language more than State or View authority,
but it does not authorize a new runtime concept.

## State Summary relevance

The recent State Summary pressure may not be State Summary-only pressure.

View authority materials already separate compact projected-state summary from
richer operator State Summary and treat top entities, endpoint visibility,
availability scope, and storage interpretation as lens/view choices rather than
State itself.

`Lens Vs Orientation` explicitly asks whether State Summary confusion comes from
mixing State description, Lens behavior, and Orientation behavior. The operator
pressure observation similarly shows that an operator-visible State Summary
symptom may direct attention while instrumentation and repository evidence are
needed to identify the actual cause.

Exploratory reading:

```text
Some State Summary pressure may be operator entrypoint, orientation, or
participant-relation pressure appearing at the State Summary surface.
```

This does not imply State Summary should be redesigned or command structure
changed. It only cautions against treating every State Summary discomfort as a
State Summary authority defect.

## Agreement and divergence

The older View work and newer Inquiry/Orientation work appear compatible at one
boundary:

```text
Older View work: what is exposed, under what authority, to which consumer.
Newer Inquiry/Orientation work: why attention is there, what unresolvedness is
active, and what continuation pressure makes the exposure useful now.
```

This agreement is partial. The distinction is not stable enough to treat as a
new architecture. Inquiry Orientation itself crosses the line: it is both a
view-shaped read surface and an orientation aid around participant prose.

The candidate chain is therefore too linear:

```text
participant -> concern -> inquiry -> orientation -> view selection -> view -> lens -> State
```

A less misleading exploratory shape is:

```text
projected State
    -> bounded lens/view surfaces

participant pressure / concern / unresolvedness / continuation
    -> orientation, navigation, activation, or use of one of those surfaces
```

Even this shape is only descriptive.

## Alternative explanations

The following alternatives remain viable:

### No participant layer exists

Supported. The evidence contains operator, consumer, later participant, and
attention language, but no reviewed authority defines a participant layer.

### View authority already explains everything

Partly supported. View authority explains what a surface exposes and what it
must refuse. It is weaker at explaining why a participant arrives at one surface
rather than another.

### Orientation is simply another View

Partly supported. Inquiry Orientation is implemented as a read-only orientation
view. But orientation documents also describe attention, relevance, pressure,
activation, and continuity, which may not be exhausted by a view payload.

### Inquiry is overloaded language

Supported. Inquiry is used for notes, questions, gaps, pressure, pursuit,
unresolvedness, movement, and frontier work. Existing documents repeatedly warn
against stabilizing it too quickly.

### Current Work Position already solves this

Possible but not settled. Current Work Position may already describe selected,
bounded, continuation-relevant orientation. It remains a frontier, not a settled
authority for View selection.

### Active Edge already solves this

Possible but not settled. Active Edge directly asks what pulls work forward, but
it also refuses to decide whether it is an object, role, operation,
relationship, attention state, selection result, priority, or inquiry object.

### The pressure is purely operator workflow, not repository architecture

Possible. Operator-pressure evidence shows that lived pressure can direct
attention without itself identifying implementation architecture. Some of the
observed pressure may be entrypoint or workflow friction rather than a missing
repository concept.

## Uncertainties

Open uncertainties preserved by this observation:

- Whether participant pressure should be modeled at all, or only described in
  documentation.
- Whether View selection is a useful name or an over-formalization of navigation,
  orientation, and current-work pressure.
- Whether Orientation is a relation, a surface, a process, a view payload, or
  overloaded vocabulary.
- Whether Inquiry is best understood as question, movement, unresolvedness,
  preserved note, or a family of related phenomena.
- Whether Current Work Position and Active Edge should remain separate from
  Orientation or explain it.
- Whether State Summary pressure is mostly view authority pressure, orientation
  pressure, entrypoint confusion, or operator workflow pressure.

## Non-conclusions

This document does not conclude that:

- Participant is a repository concept.
- A participant architecture should exist.
- View selection should be implemented.
- Orientation should become ontology.
- Inquiry should become runtime state.
- State Summary should be redesigned.
- Command structure should change.
- A new policy, runtime object, surface taxonomy, or ontology should be created.

The safest finding is narrower:

```text
Repository evidence strongly explains View authority as bounded exposure.
Repository evidence also preserves unresolved pressure around attention,
activation, concern, inquiry, orientation, current work, active edge, and
continuation.
Those pressures may explain why a participant uses or arrives at a View, but the
repository does not yet define View selection as a mechanism.
```
