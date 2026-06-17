---
doc_type: observation
status: exploratory
domain: lens catalog
related:
  - state_summary_scope_review.md
  - lens_as_observation_and_compression_pattern.md
  - architectural_knowledge_map.md
  - lens_orientation_and_dashboard_observation.md
  - read_model_inventory_and_authority_reconciliation.md
  - inquiry_note_orientation_surface_reachability_observation.md
---

# Lens Catalog Observation

## Purpose

This document catalogs candidate lenses already suggested by repository work.
It is exploratory only. It does not implement lenses, add commands, redesign
State Summary, redesign Inquiry Orientation, introduce dashboards, or promote a
canonical lens ontology.

The review question is:

```text
one deterministic State
    ->
many possible read-only views
```

Can those views usefully be described as lenses, and where do their boundaries
and authorities appear to sit?

## Method And Authority Boundary

Primary required reading:

- `docs/state_summary_scope_review.md`
- `docs/lens_as_observation_and_compression_pattern.md`
- `docs/architectural_knowledge_map.md`

Additional relationship/frontier and authority material inspected as needed:

- `docs/lens_orientation_and_dashboard_observation.md`
- `docs/read_model_inventory_and_authority_reconciliation.md`
- `docs/inquiry_note_orientation_probe_plan.md`
- `docs/inquiry_note_orientation_surface_reachability_observation.md`
- `docs/projection_integrity_summary_characterization.md`
- `docs/projection_integrity_drilldown_characterization.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/entity_impact_drilldown_reconciliation.md`
- `docs/storage_topology_observation.md`
- `docs/storage_topology_ambiguity_and_operator_clarification_reconciliation.md`
- `docs/operator_surface_family_observation.md`
- `seed_runtime/state_views.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/source_navigation.py`
- related tests located by file and term search

Existing documents retain authority for their scopes. This catalog records what
appears to be emerging from repository evidence; it does not authorize any new
runtime surface or vocabulary migration.

## Working Definition: What Is A Lens?

Repository evidence supports this cautious working definition:

```text
A lens is a deterministic, read-only way of viewing projected State for a
bounded question, attention pattern, or interpretive purpose.
```

A lens is not, by itself:

- State;
- a source of environmental truth;
- a mutation path;
- a live probe;
- a policy or goal authority;
- a replacement for evidence, provenance, or fact support;
- a sufficient explanation once its compressed distinctions matter.

This aligns with the prior lens-pattern observation: a lens helps finite
participants see a scattered family, but becomes dangerous if the compressed
term replaces support paths, evidence strength, derivation, caveats, or precise
boundaries.

## State Versus Lens

The distinction survives repository inspection.

### State Answers: What Exists?

Projected State is the deterministic read model that carries current entities,
facts, observations, requirements, capabilities, issues, relationships, support,
projection identity, and graph/integrity material. The compact state-view summary
is closest to this authority: it counts facts, observations, requirements,
capabilities, issues, and projection identity.

State-like questions include:

```text
What facts exist?
What observations exist?
What entities are represented?
What support exists for a fact?
What relationship records exist?
What projection identity produced this read model?
```

### Lens Answers: How Is It Being Viewed?

A lens selects, groups, ranks, suppresses, formats, scopes, or caveats parts of
State for a particular viewing question.

Lens-like questions include:

```text
Which integrity problems deserve investigation?
Which entities are prominent for navigation?
How is availability visible by scope?
How should storage facts be bounded for operator reading?
Which evidence paths help explain this entity?
What material is reachable from this inquiry note?
```

The State Summary scope review already found that counts and projection identity
are closer to State, while top entities, endpoint visibility, availability by
scope, and storage interpretation are view choices. Runtime code reinforces the
split: `seed_runtime/state_views.py` describes state views as deterministic
projections that do not read ledgers, append events, invoke providers, evaluate
policy, or execute runtime behavior; `seed_runtime/state_summary_views.py`
contains presentation taxonomies and explicit non-authority language for storage
and topology.

## Can Multiple Lenses View The Same Deterministic State?

Yes. Repository evidence strongly supports this.

The same projected State can support:

- current fact inspection;
- fact support and best-fact justification;
- integrity summaries and drilldowns;
- State Summary accounting;
- availability-by-scope presentation;
- storage projection;
- source navigation;
- entity impact/detail views;
- inquiry orientation surfaces.

The `read_model_inventory_and_authority_reconciliation.md` finding that read
surfaces are not interchangeable is the strongest authority evidence. Different
surfaces answer different primary questions without requiring different States.

## Can Lenses Compose?

Composition appears meaningful when the output of one lens remains a bounded
read-only view that another view can further select, summarize, or place in an
operator surface.

Evidence supports weak composition, not implementation authority:

```text
Availability lens
    -> HomeOps Dashboard lens
```

The first lens would classify projected availability facts by host, service, and
endpoint scope. A HomeOps-oriented surface could then use those bounded results
as one panel among other attention signals. The dashboard would not thereby gain
live health authority.

```text
Storage Projection lens
    -> Node Detail lens
```

The storage lens can expose filesystem shape, cluster-mount candidates, and
ambiguity caveats. A node-detail surface can include the subset relevant to one
node while preserving the storage lens caveats that candidates are not ownership
or topology facts.

Composition is unsafe if a downstream lens hides the upstream caveat and presents
compressed output as stronger truth than its input authority permits.

## Can Lenses Overlap?

Yes. Overlap appears normal and should not by itself be treated as conflict.

Examples:

- Projection Health / Integrity and Observation / Provenance both touch support,
  confidence, source, stale facts, and unsupported facts.
- Knowledge Inventory and Entity Navigation / Prominence both count entities and
  may use alias/canonicalization material.
- Operational Availability and HomeOps Dashboard both view availability facts.
- Storage Projection and Node Detail both view filesystems and mounts.
- Inquiry Orientation and Knowledge Navigation both route a participant toward
  relevant preserved material.

Overlap becomes risky only when the same field is rendered without naming which
lens owns the interpretation.

## Can Lenses Disagree?

Yes, but disagreement should usually mean different viewing authority rather than
competing States.

Examples:

- A Knowledge Inventory lens may say an entity is prominent because it has many
  durable facts; an Operational Availability lens may say that same entity is
  unknown or down by projected availability facts.
- A Storage Projection lens may show many noisy filesystem rows while a Node
  Detail lens suppresses most of them to preserve readability.
- An Inquiry Orientation lens may surface a runtime entity because it is
  reachable through projected facts while a Knowledge Navigation lens routes the
  same phrase toward documentation concepts.
- A Projection Integrity lens may warn about stale facts while a HomeOps lens may
  not elevate them if no operator-action framing exists.

These are not contradictions unless the lenses claim the same authority over the
same question. The safe pattern is to preserve the question, input authority,
output authority, and caveat with each lens.

## Candidate Lens Inventory

### 1. Projection Health / Integrity

Purpose:

- Expose whether the projected State is internally supportable, current enough,
  structurally coherent, and worth trusting for downstream reading.

Input authority:

- Projected State, fact support, graph validation issues, conflicts,
  contradictions, stale facts, unsupported facts, projection/cache metadata.

Output authority:

- Integrity visibility, investigation routing, count-level and drilldown-level
  caveats.

What it may say:

- Which facts conflict.
- Which facts are stale or unsupported.
- Which graph issues exist.
- Where an operator may investigate next.

What it may not say:

- That the environment is healthy or unhealthy in live terms.
- That a remediation should be executed.
- That stale means false.
- That absence of integrity issues proves correctness.

Relationship to State:

- Reads integrity and support material from deterministic State and related
  projections; does not create new facts.

Relationship to operator attention:

- High. It routes attention to trust, support, and investigation risks.

Classification:

- Strong candidate lens. Existing projection integrity summary/drilldown work
  already owns much of this territory.

### 2. Knowledge Inventory

Purpose:

- Show what Seed currently represents: entity kinds, fact families, durable
  knowledge, measurement samples, capabilities, requirements, and aliases.

Input authority:

- Projected State entities, facts, requirements, capabilities, issue counts,
  aliases, entity types, fact lifecycle classification.

Output authority:

- Inventory and accounting over projected knowledge.

What it may say:

- Counts by entity type or fact family.
- Which canonical entities and aliases are represented.
- Durable fact count versus current measurement sample count.

What it may not say:

- Which entity is operationally most important.
- Whether inventory is complete relative to the external world.
- Which missing thing should be acquired next without a separate selection or
  capability lens.

Relationship to State:

- Very close to State; it is mostly shaped accounting over what State contains.

Relationship to operator attention:

- Medium. It helps operators know what is present but should not decide priority.

Classification:

- Strong candidate lens, possibly the narrowest future form of State Summary.

### 3. Observation / Provenance

Purpose:

- Explain where knowledge came from and how observations, evidence, and support
  attach to facts.

Input authority:

- Observations, source types, supporting event IDs, fact-support records,
  evidence chains, provenance metadata.

Output authority:

- Source visibility, support visibility, provenance routing.

What it may say:

- Which source types contributed observations.
- Which events support a fact.
- Whether a fact has multiple supporting observations.

What it may not say:

- That source presence equals truth.
- That a fact is operationally important.
- That an unsupported operator conclusion should be promoted.

Relationship to State:

- Reads observations and support paths that State preserves or projects.

Relationship to operator attention:

- Medium to high during audit, reconciliation, contradiction handling, and trust
  investigation.

Classification:

- Strong candidate lens. Existing fact-support, current-observations, and source
  navigation work already carry pieces of it.

### 4. Operational Availability

Purpose:

- View projected availability facts by appropriate scope without treating them as
  live health probes.

Input authority:

- Projected availability facts, entity scope classification, endpoint identity
  boundaries, observation timestamps and freshness caveats.

Output authority:

- Availability-fact visibility by scope: host, service, endpoint, or unknown.

What it may say:

- How many projected availability facts are up, down, or unknown by scope.
- Which availability observations are stale if integrity material supports that.
- That endpoint scrape availability differs from host or service availability.

What it may not say:

- That the system is currently healthy right now.
- That an endpoint result proves host status.
- That remediation should be performed.

Relationship to State:

- Reads availability facts from State; scope grouping is lens interpretation.

Relationship to operator attention:

- High. Availability naturally attracts operator attention and therefore needs
  explicit caveats.

Classification:

- Strong candidate lens. State Summary scope review found availability by scope
  useful but overloaded inside State Summary.

### 5. Entity Navigation / Prominence

Purpose:

- Help operators find meaningful entities without claiming that prominence is
  importance, ownership, or health.

Input authority:

- Canonical entities, aliases, fact counts, entity kinds, relationships,
  supported evidence counts, route/drilldown targets.

Output authority:

- Navigation ranking and compact prominence rows.

What it may say:

- Which entities have many durable facts.
- Which kind bucket an entity appears in for summary rendering.
- Which aliases are associated with a canonical entity.
- Where to drill down next.

What it may not say:

- That a top entity is the most important entity.
- That endpoints should be promoted as hosts.
- That ranking proves operator priority.

Relationship to State:

- Reads entities and facts; ranking, bucketing, and limits are view choices.

Relationship to operator attention:

- High. It directly shapes what a finite participant notices first.

Classification:

- Strong candidate lens. Endpoint prominence audits and State Summary scope work
  show this lens is already implicitly active.

### 6. Storage Projection

Purpose:

- Present filesystem, mount, storage-candidate, and topology-ambiguity material
  while preserving non-authority over ownership and topology truth.

Input authority:

- Projected filesystem facts, mount observations, storage entity types, cluster
  mount grouping, shared-storage candidates, ambiguity records.

Output authority:

- Bounded storage shape visibility and candidate/ambiguity reporting.

What it may say:

- Which filesystem rows are present.
- Which mount groups look candidate-like.
- Which shared-storage candidates or ambiguities were derived.
- Which rows are shown by presentation-only category.

What it may not say:

- That a candidate is shared storage fact.
- That a mount proves ownership.
- That topology identity is resolved.
- That noisy filesystem rows should be hidden from evidence inspection surfaces.

Relationship to State:

- Reads storage-related facts and produces bounded presentation summaries.

Relationship to operator attention:

- Medium to high when diagnosing nodes or topology. Caveats are load-bearing.

Classification:

- Strong candidate lens. Runtime helper names and boundary strings explicitly
  describe candidate and ambiguity limits.

### 7. HomeOps Dashboard

Purpose:

- Gather operator-attention signals for a home-operations context: broken,
  changed, unhealthy, degraded, at risk, or needing investigation.

Input authority:

- Likely composed from availability, integrity, inventory, storage, entity
  navigation, observation/provenance, and relationship lenses.

Output authority:

- Operator-attention overview, if ever authorized separately.

What it may say:

- Which bounded signals deserve attention in a HomeOps context.
- Which upstream lenses produced those signals.
- Which caveats constrain those signals.

What it may not say:

- That it is State Summary.
- That it is live operational truth.
- That it can execute remediation or decide operator goals.
- That upstream caveats disappear because the dashboard is convenient.

Relationship to State:

- Indirect. It would likely be a composition over other lenses reading State.

Relationship to operator attention:

- Very high. Its whole purpose is attention shaping, which makes authority
  boundaries especially important.

Classification:

- Plausible but not yet an implemented lens. Existing dashboard discussion is
  explicitly exploratory.

### 8. Node Detail

Purpose:

- Present a bounded detail view for one host/node/entity without turning the
  detail page into a topology, health, or ownership authority.

Input authority:

- Entity facts, aliases, availability facts, storage projection output,
  relationships, fact support, observations, integrity caveats.

Output authority:

- Entity-scoped detail and drilldown organization.

What it may say:

- What projected facts are attached to a node.
- What availability observations and storage rows are relevant.
- Which relationships or source paths can be inspected.

What it may not say:

- That selected detail is complete environmental truth.
- That omitted facts do not exist.
- That storage mounts prove cluster topology or ownership.
- That availability facts are live health checks.

Relationship to State:

- Reads a subset of State scoped by entity identity and related facts.

Relationship to operator attention:

- High for investigation; it narrows attention from global State to one subject.

Classification:

- Plausible candidate lens. It is more implied by entity impact/detail and
  storage/node discussion than directly present as a named surface.

### 9. Inquiry Orientation

Purpose:

- Preserve an operator inquiry note as evidence of what a participant is looking
  at, then render bounded related material from existing knowledge surfaces.

Input authority:

- Raw inquiry note evidence, projected facts, fact support, State Summary
  material, observations, source/navigation surfaces, documentation/frontier
  material if participating surfaces allow it.

Output authority:

- Orientation around an inquiry: related material, reachability, tentative
  relevance, and boundaries.

What it may say:

- Which existing material appears related to the note.
- Which surfaces were reachable or not reachable.
- That a note is evidence about orientation, not orientation itself.
- That available knowledge is not necessarily recognized or activated work.

What it may not say:

- That the note is an intent, goal, command, claim, or selected work.
- That V1/V2 should be redesigned.
- That match quality alone explains reachability boundaries.
- That related material is activated work.

Relationship to State:

- Partly direct and partly compositional. It can read projected State and other
  read-only surfaces, but the inquiry note itself is evidence about participant
  orientation rather than a State fact about the world.

Relationship to operator attention:

- Very high. It exists to shape a participant's attention relative to preserved
  knowledge.

Classification:

- Strong lens-like candidate, with a special boundary: it may be less a lens over
  State alone than a lens over the relation between a participant's current
  inquiry and preserved State/documentation surfaces.

### 10. Source / Knowledge Navigation

Purpose:

- Route readers from questions, terms, source facts, concepts, and architectural
  concerns to relevant evidence and owning documents.

Input authority:

- Preserved `imports`/`defines` facts, documentation maps, source-navigation
  facts, architectural maps, frontiers, reconciliation documents.

Output authority:

- Navigation, routing, discovery, and source/document surface reachability.

What it may say:

- Where a concept or source artifact is documented.
- Which file or document family owns a question.
- Which route is useful for further inspection.

What it may not say:

- That navigation proves implementation behavior.
- That a documented route is canonical architecture unless the routed document
  has that authority.
- That source proximity equals ownership.

Relationship to State:

- Can read projected source/navigation facts and documentation-derived material;
  also operates over repository documentation authority maps.

Relationship to operator attention:

- Medium to high. It reduces rediscovery and directs investigation.

Classification:

- Strong candidate lens, adjacent to but not identical with Inquiry Orientation.

## State-Vs-Lens Distinctions Found

The inspection preserves the proposed distinction:

```text
State answers: what exists?
Lens answers: how is it being viewed?
```

More specifically:

- State owns projected existence, current fact visibility, support records,
  observations, entities, and projection identity.
- Lenses own bounded selection, grouping, ranking, scope, caveat presentation,
  navigation, compression, and operator-attention shaping.
- Some surfaces are close to State, such as current-facts and compact State
  Summary counts.
- Some surfaces are clearly lenses, such as top entities, availability by scope,
  storage topology summaries, source navigation, and inquiry orientation.
- Some surfaces mix both, especially the current operator State Summary.

The distinction fails only if a lens silently claims State authority. Repository
boundary work repeatedly avoids that failure by adding non-authority language,
source/support links, freshness caveats, and explicit presentation-only labels.

## Composition Findings

Lens composition appears useful as a description of read-only view layering, not
as implementation instruction.

Supported composition shapes:

```text
State
    -> Projection Health / Integrity
    -> HomeOps attention surface
```

```text
State
    -> Operational Availability
    -> HomeOps attention surface
```

```text
State
    -> Storage Projection
    -> Node Detail
```

```text
State + inquiry note evidence
    -> Inquiry Orientation
    -> Knowledge Navigation route
```

Composition boundaries:

- upstream caveats must survive downstream use;
- downstream surfaces must not strengthen input authority;
- composed lenses should disclose which question they answer;
- composition is read-only unless separate repository authority introduces a
  mutation path;
- disagreement between composed lenses should be handled as question/authority
  difference before being treated as contradiction.

## Special Classification: Inquiry Orientation

Inquiry Orientation appears to be a lens, but not a simple State-only lens.

It views:

```text
participant inquiry evidence
    in relation to
preserved State / documentation / navigation surfaces
```

The inquiry note is not itself a fact, goal, command, claim, tool need, or work
selection. It is evidence about what a participant is looking at. The orientation
surface then asks how preserved knowledge becomes reachable from that note.

This makes Inquiry Orientation a relation-sensitive lens:

```text
not merely: what does State contain?

but: how does this participant-facing note view or reach preserved material?
```

The V1 reachability observation supports this classification because runtime
entities participated more strongly than repository concepts, suggesting a
surface-composition and reachability boundary rather than merely a matching
quality problem.

This section does not redesign V1 or V2.

## Non-Findings And Boundaries Preserved

This catalog does not conclude that:

- every read model must be renamed a lens;
- lenses require new commands or schemas;
- State Summary should be changed now;
- HomeOps Dashboard should be implemented;
- Inquiry Orientation should be redesigned;
- candidate lenses are complete or canonical;
- lens disagreement indicates State contradiction;
- operator attention surfaces can make live-health claims.

## Conclusion

Repository evidence supports a cautious lens catalog.

The strongest currently evidenced lenses are Projection Health / Integrity,
Knowledge Inventory, Observation / Provenance, Operational Availability, Entity
Navigation / Prominence, Storage Projection, Source / Knowledge Navigation, and
Inquiry Orientation. HomeOps Dashboard and Node Detail are plausible composed
operator lenses, but their current authority is weaker and more exploratory.

The most stable architectural distinction is:

```text
State
    answers what exists in the deterministic projected read model.

Lens
    answers how that State, or State plus participant evidence, is being viewed
    for a bounded question.
```

This distinction is useful precisely because several current surfaces are
valuable but overloaded. Cataloging them as candidate lenses preserves their
utility while keeping State authority, evidence authority, output authority, and
operator-attention authority separate.
