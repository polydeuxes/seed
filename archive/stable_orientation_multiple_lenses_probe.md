# Stable Orientation / Multiple Lenses Probe

## Scope

This is a conceptual probe only. It does not implement a lens framework, store
orientation, define traversal behavior, introduce active-edge logic, create
continuation machinery, or add ontology.

The narrow question is:

```text
Can one orientation remain stable
while a participant naturally moves
between multiple lenses?
```

The probe does not ask what selected a lens. It asks the smaller question:

```text
What relationship made the second lens relevant?
```

## Files inspected

Required files inspected:

- `docs/same_lens_multiple_orientations_observation.md`
- `docs/lens_vs_orientation_observation.md`
- `docs/lens_catalog_observation.md`
- `docs/participant_orientation_view_selection_observation.md`
- `docs/relationship_frontier.md`
- `docs/relation_cluster_observation.md`
- `docs/relation_of_use_observation.md`
- `docs/relation_of_use_decomposition_observation.md`

Repository search was used only across the required files for terms including
`Orientation`, `Lens`, `Storage`, `Availability`, `Entity Navigation`,
`Inquiry Orientation`, `Source / Knowledge Navigation`, `Current Work Position`,
`Active Edge`, `relation of use`, `continuation`, and `relationship`.

## Boundary reminders from prior observations

Prior lens/orientation work supports this candidate boundary:

```text
Lens
    how projected State or preserved knowledge is viewed

Orientation
    where attention, relevance, pressure, activation, or continuation is directed
```

The boundary remains exploratory. Orientation should not be promoted into a
runtime primitive, stored object, lens selector, or canonical ontology.

The same prior work already permits the abstract pattern:

```text
different lenses
    same orientation
```

but that evidence was mostly conceptual. This probe tests small scenario
movements to see whether relationships between lenses can carry relevance while
the orientation remains stable.

## Scenario 1: Storage -> Availability

### Orientation

Storage ambiguity investigation.

The participant is trying to understand whether storage evidence supports a
safe reading of topology, mount visibility, or shared-storage ambiguity.

### Lens A

Storage Projection.

Storage Projection is repository-supported as a bounded view over filesystem,
mount, storage-candidate, topology-ambiguity, ownership-ambiguity, and
operator-reading material.

### Lens B

Operational Availability.

Operational Availability is repository-supported as a bounded view over
projected availability facts by host, service, endpoint, or unknown scope, with
freshness and scope caveats.

### Relationship making Lens B relevant

Evidence dependency / ambiguity dependency.

A storage ambiguity can make availability relevant when the storage question
turns on whether endpoint-visible evidence is absent, stale, scope-ambiguous, or
not observable from the expected entity boundary. The relationship is not a
traversal rule. It is a repository-supported dependency between ambiguous
storage interpretation and availability/freshness/scope evidence.

### What remained stable

The storage ambiguity investigation remained stable. The live concern was still
whether storage evidence could be safely read.

### What changed

The bounded viewing question changed from filesystem/mount/topology evidence to
availability visibility and scope caveats.

### Relationship type

- Evidential.
- Structural when endpoint, host, service, filesystem, or mount boundaries are
  involved.
- Ambiguity-related.

### Repository support

Supported. Storage Projection and Operational Availability are both established
candidate lenses, and prior observations allow multiple lenses to participate in
one incident or investigation orientation. The support is strongest if the move
is phrased as evidence/caveat preservation rather than as a lens traversal
mechanism.

### Naturalness

Natural. Availability does not solve the storage ambiguity, but it can expose
whether the storage evidence is absent because the endpoint/service/host view is
unavailable, stale, or scope-confused.

### Artificiality risk

Artificial if the move is described as Storage selecting Availability. The
repository supports relationship-based relevance, not a selector.

## Scenario 2: Availability -> Entity Navigation

### Orientation

Availability-scope investigation.

The participant is trying to understand a down, unknown, stale, or
scope-ambiguous availability signal without promoting it to live health truth.

### Lens A

Operational Availability.

### Lens B

Entity Navigation / Prominence.

Entity Navigation is repository-supported as a bounded view over canonical
entities, aliases, fact counts, entity kinds, relationships, supported evidence
counts, route targets, and drilldown paths.

### Relationship making Lens B relevant

Navigational relationship / structural identity relationship.

An availability fact may be attached to an endpoint, host, service, or unknown
scope. Entity Navigation becomes relevant when the participant needs to find the
canonical entity, alias boundary, relationship route, or drilldown target that
makes the scoped availability fact intelligible.

### What remained stable

The availability-scope investigation remained stable. The live concern was still
understanding the availability signal and its caveats.

### What changed

The bounded viewing question changed from availability grouping by scope to
entity route, identity, alias, relationship, and drilldown visibility.

### Relationship type

- Navigational.
- Structural.
- Evidential when fact support and supported evidence counts affect the route.

### Repository support

Supported. Operational Availability explicitly reads entity scope
classification and endpoint identity boundaries. Entity Navigation explicitly
routes through canonical entities, aliases, relationships, evidence counts, and
drilldown targets.

### Naturalness

Natural. An ambiguous availability fact often requires entity navigation before
it can be read safely.

### Artificiality risk

Artificial if prominence is treated as importance or if the navigation route is
treated as authority to remediate.

## Scenario 3: Inquiry Orientation -> Source / Knowledge Navigation

### Orientation

Inquiry orientation around a participant note.

The participant is not issuing a command, claim, goal, or selected work item.
The note is evidence of what the participant is looking at.

### Lens A

Inquiry Orientation.

Inquiry Orientation is repository-supported as a relation-sensitive lens-like
surface over participant inquiry evidence in relation to preserved State,
documentation, navigation surfaces, and reachable material.

### Lens B

Source / Knowledge Navigation.

Source / Knowledge Navigation is repository-supported as a route from questions,
terms, source facts, concepts, and architectural concerns to evidence and owning
documents.

### Relationship making Lens B relevant

Reachability relationship / source-navigation relationship.

Inquiry Orientation can surface related material and reachability boundaries.
Source / Knowledge Navigation becomes relevant when the same inquiry needs a
route to the owning document, source artifact, documentation family, or evidence
surface.

### What remained stable

The participant inquiry remained stable. The stable orientation was the
question-shaped relation between the note and preserved knowledge.

### What changed

The bounded viewing question changed from related-material orientation to route
finding through source/document knowledge.

### Relationship type

- Navigational.
- Evidential.
- Relation-sensitive.

### Repository support

Strongly supported. The lens catalog explicitly lists the composition shape:

```text
State + inquiry note evidence
    -> Inquiry Orientation
    -> Knowledge Navigation route
```

### Naturalness

Very natural. Inquiry Orientation already depends on reachable material, and
Source / Knowledge Navigation owns routes to source and document evidence.

### Artificiality risk

Artificial if the move is treated as proof that the inquiry note is intent,
selected work, or a runtime instruction.

## Scenario 4: Current Work Position -> multiple lenses

### Orientation

Current Work Position as a continuation-relevant work position.

The participant is preserving or resuming what is active, why it is active, what
boundaries constrain it, what validation status matters, what non-goals remain,
and what movement remains safe.

### Lens A

Source / Knowledge Navigation.

### Lens B

Operational Availability.

### Lens C

Storage Projection.

### Lens D

Entity Navigation / Prominence.

### Relationship making additional lenses relevant

Relation bundle: reference point, current concern, boundary, continuation,
safe-move, and selection relations.

Current Work Position appears in repository evidence as a cluster-bearing
surface rather than a single lens. When current work needs safe continuation,
multiple bounded views can become relevant because each preserves a different
part of the work position:

- Source / Knowledge Navigation preserves route and ownership context.
- Operational Availability preserves scoped availability caveats.
- Storage Projection preserves filesystem, mount, and topology ambiguity.
- Entity Navigation preserves identity, alias, relationship, and drilldown
  routes.

### What remained stable

The continuation-relevant work position remained stable. The participant was
still oriented around preserving or resuming current work safely.

### What changed

The bounded viewing question changed several times: route ownership, scoped
availability, storage ambiguity, and entity navigation.

### Relationship type

- Continuation-related.
- Boundary-related.
- Navigational.
- Evidential.
- Relation-of-use adjacent.

### Repository support

Supported, with caution. Relation-cluster and relation-of-use work support
Current Work Position as a bundle of current concern, reference point, boundary,
continuation, safe movement, and selection relations. The evidence does not
support turning that bundle into an interface, selector, or traversal system.

### Naturalness

Natural when the movement is described as preserving enough work position for
safe continuation. The stable item is not a lens; it is the work-position
relation bundle.

### Artificiality risk

Artificial if Current Work Position is treated as a super-lens, controller, or
canonical container for all participating views.

## Scenario 5: Incident investigation orientation -> multiple lenses

### Orientation

Incident investigation.

The participant is trying to diagnose a live or recently observed problem while
preserving authority boundaries: availability facts are not live health probes,
storage observations are not ownership truth, navigation routes are not priority,
and integrity caveats must survive use.

### Lens A

Operational Availability.

### Lens B

Storage Projection.

### Lens C

Entity Navigation / Prominence.

### Lens D

Source / Knowledge Navigation.

### Relationship making additional lenses relevant

Evidence dependency, structural dependency, support dependency, and navigation
relationship.

An incident investigation can move from an availability signal to storage
evidence if the symptom involves mount visibility, filesystem evidence, or
shared topology ambiguity. It can move to Entity Navigation if scope or identity
must be clarified. It can move to Source / Knowledge Navigation if the
participant needs owning documents or source evidence to understand constraints.

### What remained stable

The incident investigation remained stable. The live concern was still diagnosis
under repository authority boundaries.

### What changed

The bounded viewing question changed among availability state, storage evidence,
entity route, and source/document reachability.

### Relationship type

- Evidential.
- Structural.
- Navigational.
- Continuation-related when the incident state must be handed off.
- Relation-of-use adjacent when available facts become useful for the current
  diagnostic concern.

### Repository support

Supported. Prior same-lens/multiple-orientations work already names incident
investigation as an orientation in which Operational Availability, Storage
Projection, Projection Integrity, and Entity Navigation may participate. Source /
Knowledge Navigation is additionally supported when the incident requires routes
to owning documents or source artifacts.

### Naturalness

Natural. Incident diagnosis commonly needs several bounded views while the
participant's diagnostic concern stays stable.

### Artificiality risk

Artificial if the scenario implies runtime behavior, automatic lens traversal,
remediation, or active-edge machinery.

## Scenarios reviewed

| Scenario | Stable orientation | Lens transition observed | Repository support |
| --- | --- | --- | --- |
| Storage -> Availability | Storage ambiguity investigation | Storage Projection -> Operational Availability | Supported as evidential / ambiguity dependency |
| Availability -> Entity Navigation | Availability-scope investigation | Operational Availability -> Entity Navigation | Supported as navigation / identity dependency |
| Inquiry Orientation -> Source Navigation | Participant inquiry around note | Inquiry Orientation -> Source / Knowledge Navigation | Strongly supported as reachability / navigation dependency |
| Current Work Position -> multiple lenses | Continuation-relevant work position | Source, Availability, Storage, Entity Navigation | Supported with caution as relation bundle, not selector |
| Incident investigation -> multiple lenses | Diagnostic concern under caveats | Availability, Storage, Entity Navigation, Source Navigation | Supported as multi-view diagnostic use |

## Stable orientation examples

The strongest stable-orientation examples found in this probe are:

1. **Storage ambiguity investigation** remained stable across Storage Projection
   and Operational Availability.
2. **Availability-scope investigation** remained stable across Operational
   Availability and Entity Navigation.
3. **Participant inquiry around a note** remained stable across Inquiry
   Orientation and Source / Knowledge Navigation.
4. **Current Work Position** remained stable as a continuation-relevant relation
   bundle across multiple bounded views.
5. **Incident investigation** remained stable across diagnostic lenses when
   authority caveats survived movement.

## Lens transitions observed

Observed conceptual transitions:

```text
Storage Projection
    -> Operational Availability
```

```text
Operational Availability
    -> Entity Navigation / Prominence
```

```text
Inquiry Orientation
    -> Source / Knowledge Navigation
```

```text
Current Work Position
    -> Source / Knowledge Navigation
    -> Operational Availability
    -> Storage Projection
    -> Entity Navigation / Prominence
```

```text
Incident investigation
    -> Operational Availability
    -> Storage Projection
    -> Entity Navigation / Prominence
    -> Source / Knowledge Navigation
```

These are not traversal rules. They are observed relevance movements supported
by relationships between evidence, scope, identity, route, caveat, and
continuation need.

## Relationships involved

Relationships appearing in the scenarios:

- evidence dependency;
- support dependency;
- ambiguity dependency;
- visibility dependency;
- structural identity / scope relationship;
- navigation / reachability relationship;
- continuation relationship;
- boundary relationship;
- selection relation;
- relation-of-use adjacent current-concern relationship.

## Load-bearing relationships

The most load-bearing relationships were:

1. **Reachability / navigation.** This is load-bearing for Inquiry Orientation
   -> Source / Knowledge Navigation and Availability -> Entity Navigation.
2. **Scope / identity boundary.** This is load-bearing for Availability -> Entity
   Navigation and Storage -> Availability.
3. **Evidence / support dependency.** This is load-bearing whenever a second lens
   is needed to preserve caveats or inspect support.
4. **Ambiguity dependency.** This is load-bearing for Storage -> Availability.
5. **Continuation / current-concern relation.** This is load-bearing for Current
   Work Position and incident handoff shapes.

## Places where movement feels natural

Movement feels repository-consistent when:

- the orientation is phrased as a live concern, pressure, inquiry, or
  continuation need rather than as a selecting object;
- the second lens answers a bounded question the first lens does not own;
- upstream caveats survive downstream use;
- the relationship is evidence, reachability, identity, boundary, ambiguity, or
  continuation rather than control flow;
- no lens claims authority outside its bounded viewing question.

## Places where movement feels artificial

Movement feels artificial when:

- a lens is said to select or activate another lens;
- orientation is treated as stored runtime state;
- Current Work Position is promoted into a super-lens or controller;
- Entity Navigation prominence is mistaken for operational importance;
- Availability is treated as live health truth;
- Storage Projection is treated as ownership or topology truth;
- Inquiry Orientation is treated as command, goal, intent, or selected work.

## Candidate observations

1. Repository evidence supports the phenomenon that one orientation can remain
   stable while a participant naturally moves between multiple lenses.
2. The movement is best explained by relationships between lenses' input and
   output authority, not by lens traversal rules.
3. The strongest connecting relationships are reachability, evidence/support,
   scope/identity, ambiguity, boundary, continuation, and current concern.
4. Inquiry Orientation -> Source / Knowledge Navigation is the cleanest
   repository-supported movement because prior lens work already names that
   composition shape.
5. Current Work Position and incident investigation are broader and riskier, but
   they still support stable orientation across multiple lenses if treated as
   relation bundles or diagnostic concerns rather than controllers.
6. The probe strengthens the earlier conceptual claim:

```text
different lenses
    -> same orientation
```

without implementing or designing architecture.

## Remaining uncertainties

- Whether `orientation` is the best name for every stable concern in these
  scenarios remains unresolved.
- Whether some scenarios are better described as Current Work Position, Active
  Edge, current concern, relation of use, or navigation pressure remains open.
- The probe does not establish how participants arrive at the second lens.
- The probe does not establish whether any future surface should render these
  movements.
- The probe does not decide whether relationship vocabulary should be made more
  formal.
- The probe does not decide whether incident investigation is an orientation, a
  work position, a workflow pressure, or an operator entrypoint.

## Files changed

- `docs/stable_orientation_multiple_lenses_probe.md`

## LOC changed

- Added 584 lines of conceptual documentation.
