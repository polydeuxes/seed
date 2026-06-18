---
status: reconciliation
scope: view branch continuity across recent lens/orientation/inquiry investigations
created: 2026-06-18
---

# View Branch Continuity Reconciliation

## Status

This is a reconciliation and continuity review only. It does not implement View,
Lens, Orientation, Inquiry, State Summary, command structure, ontology, runtime
concepts, policy, dashboards, probes, or operator flows.

Repository authority wins over recent discussion. This report treats both older
View-focused work and newer Lens/Orientation/Inquiry observations as evidence to
be reconciled, not as automatic conclusions.

## Question

Central question:

```text
What did the repository already conclude about View?
What did recent Lens/Orientation/Inquiry work conclude?
Where do they agree?
Where do they differ?
Did recent investigations expose new pressure?
Or are we rediscovering established repository authority?
```

## Repository evidence reviewed

Required View-focused materials:

- `docs/lens_view_reconciliation.md`
- `docs/lens_view_architecture_audit.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`
- `docs/impact_overview_authority_reconciliation.md`
- `docs/state_summary_scope_review.md`

Required recent investigations:

- `docs/lens_vs_orientation_observation.md`
- `docs/inquiry_as_bridge_observation.md`
- `docs/inquiry_as_movement_observation.md`
- `docs/unresolvedness_observation.md`
- `docs/descriptive_language_vs_authority_observation.md`
- `docs/authority_owner_observation.md`
- `docs/repository_surface_inventory_observation.md`
- `docs/bounded_consequence_discipline_observation.md`

Additional implementation and documentation evidence was considered only through
claims cited by those required documents; this report did not re-audit runtime
code.

## Existing View authority

### Established findings

Older View-focused work already established the following with comparatively
strong authority:

1. **View authority is stronger than Lens authority.** Existing view modules and
   state-summary helpers provide implemented read-only surfaces, while Lens is
   mostly exploratory vocabulary.
2. **A View is read-only exposure of projected or lens-shaped material to a
   consumer.** It may render, package, group, or select material, but it does not
   add truth, action, probe, provider, policy, or mutation authority.
3. **Views are not presentation-only.** Rendering is part of some views, but
   consumer-specific authority, selection, summarization, and visibility rules
   are also View concerns.
4. **A View must preserve the authority boundaries of its inputs.** Evidence,
   interpretation, integrity, and navigation surfaces have different consumer
   questions and different rules for what may be summarized or hidden.
5. **State Summary is a combination, not a pure View category.** It includes a
   compact State View / projection and a richer operator-facing summary with
   embedded lens-like selections.
6. **Impact, current facts, fact support, integrity summary, and contradictions
   are different surface types.** Output disagreements are often authority
   disagreements rather than formatting disagreements.
7. **Future HomeOps and Seed Ops language is not current authority.** Older work
   classifies those as unresolved possible future view/surface families, not as
   implemented surfaces or canonical products.

### Unresolved findings

Older View-focused work deliberately left unresolved:

- where to draw a formal boundary between read projection, lens, and view if a
  Lens architecture is ever authorized;
- whether lenses should become runtime objects, helper functions, schema payloads,
  registry entries, or documentation-only authority boundaries;
- how one lens might participate in multiple views without losing caveats or
  provenance;
- which current State Summary sections should remain embedded selections and
  which, if any, should become separate surfaces;
- what sufficient repository authority would be needed before defining HomeOps or
  Seed Ops product surfaces.

### Explicit non-conclusions

Older View-focused work explicitly did not conclude that:

- `Lens` is canonical runtime architecture;
- every lens is a projection;
- every view is only presentation;
- State Summary should be redesigned now;
- Seed Ops or HomeOps should exist;
- Orientation is a first-class object;
- operator notes should be replaced immediately;
- command structure should change.

### Authority boundaries

Existing View authority is bounded by projected State, documented repository
knowledge, implementation-backed read models, and specific reconciliations. It
does not authorize new runtime behavior, live operational health claims, topology
truth, ownership truth, policy, probes, remediation, or command changes.

The safest existing View statement is:

```text
A View exposes selected projected or lens-shaped material to a consumer while
preserving the authority and non-authority boundaries of its inputs.
```

## Recent findings summary

This section summarizes recent investigations without promoting them.

### Lens and Orientation

`docs/lens_vs_orientation_observation.md` investigates whether Lens and
Orientation are distinct. Its safest statement is exploratory: scoped viewing and
directed attention appear distinguishable, but the boundary is porous and not
canonical. It does not authorize a formal State / Lens / Orientation ontology,
State Summary redesign, Inquiry Orientation modification, or runtime behavior.

Relevant pressure introduced or sharpened:

- Lens may be a bounded viewing/interpretive shape.
- Orientation may involve participant relation, focus, continuation, activation,
  or current work position rather than only read-model selection.
- Inquiry Orientation can look lens-like, but may also be orientation-like because
  it relates a participant question to existing material.

### Inquiry as bridge

`docs/inquiry_as_bridge_observation.md` asks whether Inquiry bridges Lens,
Orientation, Concern, and Inquiry Note. Its safest position is that Inquiry may
act as a relation or pressure between a question, view, and activation, but this
is not canon. A conservative alternative remains that Inquiry Orientation is just
a compound surface.

Relevant pressure:

- Inquiry might not be a normal View output, but it can shape what material a
  surface relates to and why.
- Inquiry notes are preserved prose, not facts, goals, plans, commands, or
  runtime instructions.

### Inquiry as movement

`docs/inquiry_as_movement_observation.md` explores whether Inquiry is better read
as movement than as an object. It explicitly refuses to make Inquiry ontology,
runtime state, or a first-class primitive. The movement framing is exploratory and
could be revised.

Relevant pressure:

- Some newer work treats Inquiry as a process of moving among question, gap,
  concern, active edge, and orientation rather than a stored object.
- That movement can affect how views are used, without changing View authority.

### Unresolvedness

`docs/unresolvedness_observation.md` investigates whether recent inquiry work
exposed a broader pattern of unresolved material. It explicitly considers that no
separate concept exists and that existing terms may be sufficient.

Relevant pressure:

- Uncertainty is not the whole phenomenon; unresolvedness may include known
  differences, missing authority, incomplete relations, continuation positions,
  and active-edge terrain.
- Preserving unresolvedness can be an intended repository status, not merely a
  failure to decide.

### Description vs authority

`docs/descriptive_language_vs_authority_observation.md` records a recurring
separation between useful explanatory language and authority-bearing repository
structures. Its safest reading is narrow: repository work benefits from
separating words that explain evidence from structures allowed to govern behavior.

Relevant pressure:

- Shared terms do not imply shared authority.
- Descriptive vocabulary can help investigate without authorizing runtime or
  model consequences.

### Authority owner

`docs/authority_owner_observation.md` finds scoped authority boundaries more
strongly than a single repository-wide authority-owner model. It treats
authority-owner patterns as hypotheses only.

Relevant pressure:

- Meaning becomes authority-bearing only when accepted by scoped models,
  catalogs, projections, reconciliations, or tests.
- Visibility, aliases, lookup convenience, or shared wording do not fill missing
  ownership authority.

### Surface inventory

`docs/repository_surface_inventory_observation.md` inventories candidate
surfaces and explicitly refuses to make `Surface` a repository concept or formal
taxonomy. It nevertheless observes preservation-oriented, projection-oriented,
vocabulary/catalog, operator-facing, and boundary surfaces.

Relevant pressure:

- Many repository surfaces accept bounded input and refuse over-promotion.
- Inquiry Orientation and State Summary can be treated as operator-facing read
  surfaces for comparison, but the inventory does not promote that to ontology.

### Bounded consequence discipline

`docs/bounded_consequence_discipline_observation.md` observes a repeated pattern:
accepting, preserving, projecting, validating, navigating, orienting, or
summarizing often stops short of ownership, truth, execution, repair, promotion,
or authority. It leaves unresolved whether this is a deeper architecture or just
careful documentation style.

Relevant pressure:

- The pattern generalizes View boundary concerns beyond View-specific documents.
- It may explain why recent branches repeatedly rediscover refusal of
  over-promotion.

## Agreement analysis

Older View work and newer investigations converge in several places.

### Lens is not View

Older View work says Lens is bounded selection or interpretation and View exposes
projected/lens-shaped material to a consumer. Newer Lens/Orientation work again
separates scoped viewing from other roles. This is convergence, not novelty.

Continuity assessment: recent work did not overturn the older distinction; it
made the Lens boundary more pressured by comparing Lens to Orientation and
Inquiry.

### View is not Orientation

Older View work already rejected the claim that View is merely presentation, but
it did not make Orientation a View synonym. Newer work reinforces that
Orientation may involve attention, activation, participant relation, and
continuation. The branches agree that a consumer-facing surface and directed
orientation are not identical.

Continuity assessment: older View work implied this boundary; recent work made it
more explicit.

### View as composition

Older work concluded State Summary is a combination of compact State View,
operator summary, and embedded lens-like selections. Newer surface and bounded
consequence observations similarly describe operator-facing surfaces as composed
from preservation, projection, selection, and refusal boundaries.

Continuity assessment: recent work mostly rediscovered and generalized the
composition pattern.

### View as authority boundary

Older work explicitly says output disagreements are authority disagreements and
that views must not imply conclusions beyond their authority. Newer description,
authority-owner, surface-inventory, and bounded-consequence work independently
return to the same pattern: useful description, visibility, or acceptance does not
create authority.

Continuity assessment: this is the strongest continuity point. The newer work is
largely an extension and generalization of established View authority.

### State Summary boundary

Older State Summary work already distinguishes compact projected-State authority
from operator summary/lens-like selections and says State Summary is not a
dashboard, health checker, recommendation engine, or topology authority. Newer
work repeatedly confirms that accepting or summarizing material does not promote
it to ownership, truth, action, or runtime behavior.

Continuity assessment: recent State Summary concerns are mostly already
addressed by View and State Summary work, except where Inquiry/Orientation adds
participant-continuation pressure.

## Difference analysis

### Difference: Orientation pressure exceeds older View vocabulary

Older View documents mention Orientation but do not deeply analyze it. Newer
work treats Orientation as possibly involving participant relation, directed
attention, active edge, continuation, and activation.

Assessment: real scope expansion, not a contradiction. Older View authority can
still hold because Orientation pressure does not give View new powers. It exposes
a neighboring concern that View documents only partially covered.

### Difference: Inquiry pressure is not reducible to Lens/View

Older View work can classify Inquiry Orientation as a read-only surface, but
newer Inquiry work asks whether Inquiry is movement, bridge, relation, or
compound surface.

Assessment: real new pressure, but not a View contradiction. The pressure is
about what brings a participant to a surface and what unresolved relation is
preserved, not about changing View authority.

### Difference: Surface inventory broadens beyond View

Older View work uses surface categories for view responsibility. Newer surface
inventory applies surface language to EventLedger, ProjectionStore, Evidence,
Fact, catalogs, source navigation, Inquiry Orientation, Graph Validation, Context
Views, handoff metadata, and more.

Assessment: terminology drift and scope expansion. It is useful for comparison,
but the inventory itself refuses to make Surface canonical. It should not be read
as replacing View authority.

### Difference: Bounded consequence discipline generalizes View refusal

Older View work says views should not overclaim. Newer bounded-consequence work
finds similar refusal patterns across many repository mechanisms.

Assessment: extension, not contradiction. The newer work may reveal that View
boundaries are one instance of a broader repository habit, but that habit is not
yet established as architecture or policy.

### Difference: Unresolvedness adds preservation-of-not-yet-decided pressure

Older View work emphasizes evidence, interpretation, integrity, and navigation.
Newer unresolvedness work highlights material that should remain unresolved,
including missing authority and continuation positions.

Assessment: partial novelty. Integrity surfaces cover uncertainty and conflict,
but unresolvedness is broader than conflict/uncertainty. Still, the new label is
exploratory and may be unnecessary if existing terms suffice.

## New pressure analysis

Recent investigations exposed some pressure not fully visible in older View
work, but much of it extends existing authority boundaries rather than
contradicting them.

### Inquiry Orientation

Novelty level: **partial**.

Older View work could classify Inquiry Orientation as a read-only surface or
operator-facing view over projected State and preserved prose. Newer work adds
pressure around whether the inquiry is a note, relation, movement, bridge,
activation path, or compound surface. Older View work did not fully answer that.

Boundary preserved: Inquiry Orientation remains non-promotional; it does not
turn prose into facts, goals, requirements, plans, commands, or runtime
instructions.

### Inquiry as movement

Novelty level: **moderate but exploratory**.

Older View work did not frame Inquiry as movement. Newer work suggests the useful
unit may be movement through question, gap, concern, active edge, and orientation,
not a stable object. This affects continuity and participant understanding more
than View implementation.

Boundary preserved: movement framing does not authorize runtime Inquiry objects
or command changes.

### Authority surfaces

Novelty level: **low-to-partial**.

Older View work already treated views as authority-bearing surfaces. Newer work
broadens authority-surface thinking across repository mechanisms. The broadening
is useful but not yet canonical.

Boundary preserved: localized authority remains stronger than a single global
surface or owner theory.

### Bounded consequence discipline

Novelty level: **partial**.

The specific phrase is newer, but the pattern was already visible in View, State
Summary, impact, source navigation, storage ambiguity, evidence/fact support, and
catalog boundaries. Recent work makes it easier to see that the View branch was
not isolated.

Boundary preserved: this is descriptive, not policy.

### Description vs authority

Novelty level: **low as principle, high as explicit framing**.

Older View work already refused to let presentation create truth or authority.
Newer work states the same as a general distinction between explanatory words and
governing structures. This is mostly a clearer vocabulary for an existing
repository discipline.

### Shared vocabulary vs shared authority

Novelty level: **partial**.

Older View work already warned against category collapse across evidence,
interpretation, integrity, navigation, State Summary, dashboard, and topology.
Newer work adds explicit examples where the same word can appear in multiple
authority domains without merging them.

Boundary preserved: shared language cannot create shared authority.

## State Summary relevance

Recent State Summary discussions are **mostly addressed, partially extended** by
older View work.

Already addressed:

- State Summary has a compact projected-State layer and a richer operator
  summary layer.
- Operator summary sections include lens-like selections.
- State Summary should not be read as a HomeOps dashboard, health checker,
  recommendation engine, topology authority, or only operator interface.
- Output changes should respect the authority of each surface.

Partially addressed:

- State Summary as a continuation/orientation aid. Older work covers operator
  summary and navigation but does not fully investigate participant relation,
  active edge, or inquiry movement.
- State Summary as a place where unresolvedness may be preserved. Older integrity
  language covers conflicts and uncertainty, but not all newer unresolvedness
  cases.

Not addressed by View work alone:

- Whether Inquiry should be read as movement rather than object.
- Whether Orientation is best understood as participant relation rather than a
  surface output.
- Whether bounded consequence discipline is a repository-wide tendency.

State Summary finding:

```text
Recent State Summary pressure does not justify redesign or command change. It
mostly confirms established View/State Summary boundaries while adding unresolved
participant-continuation questions for future reconciliation.
```

## Continuity assessment

### If a fresh participant read only older View documents

They would understand:

- View is read-only and authority-bounded.
- Lens is exploratory and bounded.
- View is not presentation-only.
- State Summary is a combination.
- HomeOps and Seed Ops are unresolved future surface candidates.
- Output disputes often reflect authority disputes.

They would likely miss:

- the sharper Lens vs Orientation distinction around directed attention,
  activation, participant relation, and continuation;
- Inquiry as possible bridge, movement, or relation rather than object;
- the unresolvedness framing for material that should remain preserved but not
  resolved;
- the generalized description-vs-authority pattern across branches;
- the broader surface inventory beyond View-like operator surfaces;
- bounded consequence discipline as a cross-repository descriptive pattern.

### If a fresh participant read only newer investigations

They would understand:

- recent work is cautious and exploratory;
- Inquiry, Orientation, unresolvedness, authority, and surfaces are not canon;
- acceptance, preservation, or visibility should not over-promote consequences;
- shared vocabulary does not imply shared authority.

They would likely miss:

- the stronger implemented authority for concrete View modules and State Summary
  read projections;
- the older established distinction between read projection, Lens, and View;
- the classification of Evidence, Interpretation, Integrity, and Navigation
  surfaces as a View-responsibility aid;
- the specific State Summary split between compact State View and operator
  summary;
- the prior conclusion that View is authority-bearing but not execution,
  provider, policy, mutation, or probe authority;
- the explicit unresolved questions around formal Lens/View contracts and
  HomeOps/Seed Ops.

## Alternative explanations

### No reconciliation is needed

Partly plausible. The branches do not directly contradict each other, and most
recent documents preserve non-conclusions. However, reconciliation is useful
because newer investigations repeatedly touch View vocabulary and could otherwise
be mistaken for new authority over View or State Summary.

### The branches discuss different things

Partly true. Older work discusses View/Lens/State Summary authority. Newer work
discusses Inquiry, Orientation, unresolvedness, authority, surfaces, and bounded
consequences. But they overlap wherever read surfaces, consumer questions,
selection, summarization, authority boundaries, and State Summary are involved.

### Recent work merely renamed existing findings

Partly true. Description-vs-authority, surface refusal, and bounded consequences
largely rename or generalize older View boundary findings. But Inquiry movement,
participant relation, and unresolvedness pressure are not fully captured by older
View vocabulary.

### View work already resolved these questions

Partly true for View authority, State Summary boundaries, Lens non-canonicity,
and surface responsibility. Not true for Inquiry-as-movement, Orientation as
participant relation, or repository-wide bounded consequence discipline.

### Recent work exposed genuinely new concerns

Partly true. New concerns include Inquiry/Orientation continuity, active-edge
activation, preservation of unresolvedness beyond ordinary uncertainty, and the
possibility that View boundaries are one instance of a broader repository pattern.
They remain exploratory and do not override older View authority.

## Uncertainties

- Whether `Orientation` will remain descriptive vocabulary or receive a future
  formal boundary.
- Whether `Inquiry` is best treated as note, relation, movement, bridge, compound
  surface, overloaded term, or no separate concept.
- Whether `Unresolvedness` is necessary vocabulary or can be replaced by existing
  terms such as uncertainty, gap, concern, frontier, active edge, current work
  position, continuation, and handoff context.
- Whether bounded consequence discipline is a genuine architectural tendency or
  simply a documentation style.
- Whether a future Lens/View contract should be implemented at all.
- Whether State Summary should eventually separate embedded lens-like selections;
  no current implementation change is authorized by this reconciliation.

## Non-conclusions

This reconciliation does not conclude that:

- View should be implemented or redesigned.
- State Summary should be redesigned.
- Inquiry should be promoted.
- Inquiry should become ontology, runtime state, or a first-class primitive.
- Orientation should become ontology, runtime state, or a first-class primitive.
- Unresolvedness should become ontology, runtime state, or a first-class
  primitive.
- Surface should become a repository concept or taxonomy.
- Bounded consequence discipline should become policy.
- HomeOps or Seed Ops should be created.
- Command structure should change.
- Runtime architecture should change.

## Overall reconciliation

The recent Lens/Orientation/Inquiry investigations are mostly **rediscovering and
extending established repository authority** rather than contradicting it.

They rediscover established authority when they conclude that:

- visibility is not ownership;
- description is not authority;
- summarization is not truth;
- orientation is not execution;
- inquiry prose is not facts, goals, requirements, plans, or commands;
- View-like surfaces must preserve bounded authority.

They extend older View work by exposing pressure around:

- participant relation to a surface;
- activation and continuation;
- Inquiry as movement or bridge;
- unresolvedness as preserved, not-yet-promoted material;
- bounded consequence discipline across non-View mechanisms.

The continuity result is therefore:

```text
Older View work remains the repository authority for View boundaries.
Newer investigations add adjacent pressure around Orientation, Inquiry,
Unresolvedness, and cross-surface consequence discipline.
Those pressures may guide future reconciliation, but they do not authorize
implementation, State Summary redesign, command changes, ontology, runtime
concepts, or policy.
```
