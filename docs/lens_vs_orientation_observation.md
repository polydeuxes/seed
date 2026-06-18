---
doc_type: observation
status: exploratory
domain: lens versus orientation
related:
  - lens_catalog_observation.md
  - lens_view_reconciliation.md
  - lens_orientation_and_dashboard_observation.md
  - work_shape_and_orientation_observation.md
  - orientation_object_observation.md
  - current_work_position_frontier.md
  - active_edge_frontier.md
  - state_summary_authority_reconciliation.md
  - observation_visibility_continuity_baseline_expectation_concern_reconciliation.md
  - visibility_expectation_concern_branch_closure_reconciliation.md
---

# Lens Vs Orientation Observation

## Status

Exploratory observation only.

This document investigates whether `lens` and `orientation` are distinct
repository concepts. It does not implement lenses, redesign runtime behavior,
modify State Summary, modify Inquiry Orientation, introduce ontology, create
policy, or promote lens, orientation, or concern to canon.

The candidate distinction tested here is:

```text
State
    answers:
        What exists?

Lens
    answers:
        How is State being viewed?

Orientation
    answers:
        Where is attention currently directed?
```

This is treated as a candidate observation, not a conclusion.

## Question

The central question is:

```text
What is a Lens?
What is Orientation?
Are they different?
If they are different, what boundary separates them?
```

A secondary question is whether current State Summary confusion may come from
mixing:

```text
State description
Lens behavior
Orientation behavior
```

A third question is whether `concern` behaves more like State, lens,
orientation, or something else.

## Repository evidence reviewed

Repository materials reviewed for this observation:

- `docs/state.md`
- `docs/lens_catalog_observation.md`
- `docs/lens_view_reconciliation.md`
- `docs/lens_as_observation_and_compression_pattern.md`
- `docs/lens_orientation_and_dashboard_observation.md`
- `docs/lens_implementation_frontier_observation.md`
- `docs/lens_view_architecture_audit.md`
- `docs/state_summary_authority_reconciliation.md`
- `docs/state_summary_scope_review.md`
- `docs/work_shape_and_orientation_observation.md`
- `docs/orientation_object_observation.md`
- `docs/orientation_bundle_load_bearing_observation.md`
- `docs/orientation_non_convergence_audit.md`
- `docs/inquiry_note_orientation_probe_plan.md`
- `docs/inquiry_note_orientation_probe_work_order.md`
- `docs/inquiry_note_orientation_surface_reachability_observation.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/continuation_context_and_working_state_reconciliation.md`
- `docs/handoff_consumption_activation_reconciliation.md`
- `docs/knowledge_navigation_layers_frontier.md`
- `docs/knowledge_representation_map.md`
- `docs/visibility_expectation_concern_branch_closure_reconciliation.md`
- `docs/observation_visibility_continuity_baseline_expectation_concern_reconciliation.md`
- `docs/visibility_target_ownership_concern_reconciliation.md`
- `docs/purpose_and_concern_observation.md`
- `docs/reference_point_and_concern_subject_observation.md`
- `docs/pressure_precursor_and_work_activation_observation.md`
- `docs/pressure_visibility_and_preservation_observation.md`

Implementation evidence was consulted only to understand existing State and
read-view boundaries:

- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/context_views.py`
- `seed_runtime/projection_store.py`

## Candidate definitions

### State candidate

Repository evidence strongly supports State as the current deterministic
projected world/read model produced from event history. `docs/state.md` says the
State layer turns append-only EventLedger data into a current world model and
that projected State is the latest current world model after replaying all
events and building derived indexes.

Candidate shorthand:

```text
State answers: What exists in the projected world/read model?
```

This shorthand is safer if `exists` is read as `exists in projected State`, not
as unqualified real-world truth.

### Lens candidate

Recent lens documents converge on lens as a bounded, deterministic, read-only
way of viewing projected State or repository knowledge. The lens catalog's
working definition says a lens is a deterministic, read-only way of viewing
projected State for a bounded question, attention pattern, or interpretive
purpose. The lens/view reconciliation says lens is not yet a canonical runtime
primitive and is currently an architectural description for bounded
question-answering, attention shaping, compression, classification, or
interpretation over projected State.

Candidate shorthand:

```text
Lens answers: How is projected State or preserved knowledge being viewed?
```

This shorthand is supported only as exploratory vocabulary. It must not be read
as authorizing a lens registry, lens runtime API, or lens ontology.

### Orientation candidate

Orientation evidence is less implementation-backed and more continuation- and
participant-facing. `lens_orientation_and_dashboard_observation.md` says
orientation may be less about what Seed knows and more about the relationship
between a participant and what Seed knows. It also suggests orientation may be an
interaction, comparable to seeing rather than the thing seen. The orientation
object observation repeatedly ties orientation to attention, relevance,
pressure, activation, and continuity patterns rather than identity, agency, or
subjecthood.

Candidate shorthand:

```text
Orientation answers: Where is attention, relevance, pressure, or continuation currently directed?
```

This shorthand remains uncertain because repository work also treats Current
Work Position, Active Edge, activity context, inquiry, and working state as
adjacent unresolved surfaces.

## Lens investigation

The strongest lens evidence is about scoped viewing.

`docs/lens_catalog_observation.md` says State-like questions include what facts,
observations, entities, support, relationships, and projection identity exist.
It contrasts that with lens-like questions such as which integrity problems
deserve investigation, how availability is visible by scope, how storage facts
should be bounded for operator reading, and what material is reachable from an
inquiry note.

This supports a tentative boundary:

```text
State provides projected material.
Lens selects, groups, ranks, suppresses, formats, scopes, or caveats projected material.
```

Several named candidates behave this way:

### Availability Lens

Availability Lens appears to change scope of viewing. The lens catalog describes
it as viewing projected availability facts by host, service, endpoint, or
unknown scope, while reading availability facts from State and treating scope
grouping as lens interpretation.

That means Availability Lens does not appear to change which State exists. It
changes which availability facts are grouped together, which scope labels matter,
and how endpoint/host/service ambiguity is presented.

### Storage Lens

Storage Lens appears to change scope and caveat structure. Storage-related lens
work repeatedly distinguishes endpoint-visible filesystem measurements,
cluster-mount candidates, ownership ambiguity, topology ambiguity, and operator
reading. In this shape, Storage Lens is not the storage itself and is not a live
probe. It is a bounded read over projected filesystem/storage evidence with
caveats about what the evidence can and cannot mean.

### Knowledge Inventory Lens

Knowledge Inventory behaves lens-like because it counts, groups, and presents
repository/projected knowledge for overview. It may overlap with State Summary,
but it does not thereby become State. It seems to answer `what knowledge is
represented and how complete/visible is it for inventory purposes?`, which is a
viewing question over State and documentation surfaces.

### Entity Navigation Lens

Entity Navigation / Prominence behaves lens-like because it narrows global State
or repository knowledge to navigable subjects, aliases, relationships,
prominence, and drilldown paths. It changes the route through State, not the
State itself.

### Inquiry Orientation as a special lens candidate

The lens catalog classifies Inquiry Orientation as a relation-sensitive lens,
not a simple State-only lens. That classification is important evidence against
a clean binary. Inquiry Orientation uses inquiry-note evidence, projected facts,
fact support, State Summary material, repository knowledge, and reachability
signals to orient a participant around a question. It may therefore have both:

```text
lens-like behavior:
    selected reachable material

orientation-like behavior:
    participant-facing direction of attention
```

This is one of the strongest reasons not to conclude too sharply.

## Orientation investigation

Orientation evidence is about directedness, continuation, activation, and work
shape more than about scoped read models.

### Inquiry Orientation

Inquiry Orientation appears to preserve or expose what a participant is looking
at in relation to preserved knowledge. Inquiry notes are explicitly not facts,
claims, goals, or tool needs in the lens/orientation observation. They are better
read as evidence about orientation than orientation itself.

This makes Inquiry Orientation different from a pure lens. A pure lens can be
applied to the same State without a participant's live question. Inquiry
Orientation appears to require a relation between:

```text
participant question / inquiry note
preserved knowledge
reachable evidence
current work need
```

### Current Work Position

Current Work Position appears broader than a lens. It is continuation-facing and
work-situating. The current-work frontier treats it as a candidate, not
established ontology, and asks whether it can be separated from working state or
whether it is a relationship bundle. Later orientation work says Current Work
Position preserves orientation as situated continuity.

This suggests Current Work Position is not primarily a way to view all State. It
is more like the preserved position from which continuation can safely resume:
what is live, bounded, relevant, risky, validated, or next.

### Active Edge

Active Edge is even more pressure- and attention-adjacent. The active-edge
frontier distinguishes attention as actual focus and Active Edge as the
candidate pressure that may make focus intelligible. It also says Active Edge may
be the currently activated unresolved pressure that explains why work is moving
forward.

This makes Active Edge less lens-like than Availability or Storage. It does not
primarily answer `how should State be grouped?` It asks what unresolved pressure
is pulling current work.

### Attention, activation, and continuation

Continuation documents strengthen the orientation side. `continuation_context`
work says activity context should preserve immediate objective, current object
of attention, live reasoning branch, blockers, active tensions, and next safe
moves. Work-shape observation says orientation reconfigures according to what
would make the current activity fail.

That evidence supports a candidate distinction:

```text
Lens controls the scope or method of viewing.
Orientation controls what is live for attention and continuation.
```

But this remains only a candidate distinction because some lens documents define
lenses partly through attention patterns, and some orientation surfaces use
lens-like selection.

## State / Lens / Orientation comparison

The candidate model mostly survives repository evidence if kept non-canonical:

```text
same State
    ->
different Lens
    ->
different view

same Lens
    ->
different Orientation
    ->
different attention / continuation use
```

Examples that appear supported:

1. The same projected availability facts can be viewed through an Availability
   Lens by endpoint, host, service, or unknown scope. That changes viewing scope,
   not necessarily current attention.
2. The same availability view can be used under different orientations: routine
   inventory, incident investigation, handoff continuation, or State Summary
   cleanup. That changes why the view matters now.
3. The same projected filesystem facts can be viewed through a Storage Lens for
   endpoint-visible mounts or cluster-mount ambiguity. Under a Current Work
   Position orientation, only the node116 mount-loss question may be live.
4. Entity Navigation can expose many routes through State. Active Edge may name
   which unresolved pressure makes one route the current pull.

A compact comparison:

| Candidate | Primary question | Strongest evidence | Risk if confused |
| --- | --- | --- | --- |
| State | What exists in projected State? | State docs and implementation projection model | Treating a view choice as truth authority |
| Lens | How is State or knowledge being viewed? | Lens catalog and lens/view reconciliation | Treating scoped grouping as ontology or runtime behavior |
| Orientation | Where is attention, relevance, pressure, or continuation directed? | Orientation, work-shape, Current Work Position, Active Edge, continuation docs | Treating live focus as State truth or policy priority |

## Concern investigation

Concern does not cleanly collapse into State, Lens, or Orientation.

The visibility/expectation/concern reconciliation says concern can arise from
visibility change, continuity break, baseline deviation, expectation violation,
ambiguity, staleness, degraded evidence quality, or operator investigation
context. It classifies concern as interpretive and operator-significant, possibly
authority-adjacent, requiring scoped significance but not necessarily should
authority.

That behavior is not State-like if State means deterministic projected world
model. Concern may depend on State evidence, but it adds significance.

Concern is partly lens-like because a concern surface can interpret evidence and
shape presentation. A Storage Lens or Availability Lens may expose concern-like
signals when visibility changes or evidence quality degrades.

Concern is also orientation-like because concern can direct attention. The
active-edge frontier says concern is broad mattering while Active Edge is current
pull; concern may be too vague unless sharpened into a question, gap, tension,
risk, or boundary.

Candidate observation:

```text
Concern may be operator-significant interpretation that can feed orientation.
```

This preserves uncertainty:

- Concern is not simply State.
- Concern is not simply Lens.
- Concern is not simply Orientation.
- Concern may become lens-visible, orientation-shaping, and sometimes
authority-adjacent without becoming ontology or policy.

## State Summary implications

Repository evidence supports the possibility that State Summary confusion comes
from mixing State description, lens behavior, and orientation behavior.

`state_summary_authority_reconciliation.md` begins from the observation that
State Summary contains inventory, integrity, operational, and knowledge
information. It finds State Summary is closest to a knowledge inventory and
overview surface, while also warning that future State Summary may need clearer
distinctions among inventory, integrity, availability, impact, and navigation.

`lens_view_reconciliation.md` goes further: State Summary is best understood as a
combination. One layer is compact State/accounting summary: counts, projection
identity, and current read-model inventory. Another layer is embedded view/lens
material such as top entities, entity-kind classification, availability by
scope, observation-source counts, and storage/topology caveats.

The current investigation adds a candidate third pressure:

```text
State Summary may also be asked to orient the operator.
```

That would explain why State Summary attracts dashboard, overview, attention,
availability, storage, topology, and issue-ranking pressure. Those pressures may
not all be State Summary responsibilities. Some may be lens responsibilities;
some may be orientation responsibilities; some may belong to future operator
surfaces if separately authorized.

This document does not recommend changing State Summary. It only records that
the confusion is plausibly caused by mixing:

```text
projected State inventory
bounded lens/view interpretation
operator orientation / attention shaping
```

## Uncertainties

1. Lens documents sometimes include `attention pattern` inside lens definition,
   which blurs the proposed lens/orientation boundary.
2. Inquiry Orientation is explicitly lens-like in the lens catalog, but
   participant-relation-like in the lens/orientation observation.
3. Current Work Position may collapse into working state, inquiry state,
   activity context, continuation context, or a relationship bundle.
4. Active Edge may collapse into Current Work Position, inquiry, selection,
   attention, priority, relationship semantics, or continuity.
5. Concern may be too broad unless attached to a subject, reference point,
   expectation, question, gap, risk, or active edge.
6. `Lens` is not yet canonical runtime vocabulary, and `Orientation` is even less
   settled as an architectural primitive.
7. The repository has strong read-view implementation evidence, but weaker
   implementation evidence for lens/orientation as separate layers.

## Possible distinctions

The following distinctions appear useful but remain non-conclusive:

### Scope of viewing vs focus of attention

```text
Lens changes scope of viewing.
Orientation changes focus of attention.
```

This fits Availability Lens, Storage Lens, Knowledge Inventory Lens, and Entity
Navigation better than it fits Inquiry Orientation.

### Read model interpretation vs participant relation

```text
Lens is an interpretation over projected State or preserved knowledge.
Orientation is a participant/work relation to that interpreted material.
```

This fits inquiry notes as evidence about orientation and explains why a
participant may possess knowledge without being oriented.

### Reusable view shape vs live continuation shape

```text
Lens can be reusable across contexts.
Orientation is live or continuation-specific.
```

Availability-by-scope can be reused in State Summary, HomeOps-like surfaces, and
Node Detail. Current Work Position and Active Edge are more dependent on what is
currently being continued or pulled forward.

### Compression vs activation

```text
Lens compresses scattered State into a bounded view.
Orientation activates some preserved material as currently relevant.
```

This fits continuation work: available documentation is not the same as consumed
or activated handoff content.

## Non-conclusions

This document does not conclude that:

- lens is canon;
- orientation is canon;
- concern is canon;
- State / Lens / Orientation should become a formal ontology;
- State Summary should be redesigned;
- Inquiry Orientation should be modified;
- concern should become a policy, alert, or runtime object;
- runtime behavior should change;
- a lens registry, orientation object, or concern object should be introduced.

The safest current statement is:

```text
Repository evidence supports an exploratory distinction between scoped viewing
and directed attention, but the boundary is porous and not yet canonical.
```
