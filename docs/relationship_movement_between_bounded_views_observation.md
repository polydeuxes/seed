---
doc_type: observation
status: exploratory
domain: relationship movement between bounded views
introduced_by: relationship movement between bounded views observation
related_documents:
  - relation_cluster_observation.md
  - relation_of_use_observation.md
  - relation_of_use_decomposition_observation.md
  - relation_preservation_observation.md
  - relationship_frontier.md
  - relationship_fact_reconciliation.md
  - relationship_observation_v0_reconciliation.md
  - relationship_promotion_reconciliation.md
  - object_role_operation_relation_cluster_observation.md
  - defines_relationship_reconciliation_audit.md
  - stable_orientation_multiple_lenses_probe.md
---

# Relationship Movement Between Bounded Views Observation

## Purpose

This exploratory observation investigates which relationships repeatedly make
another bounded view relevant.

It does not implement lens traversal, orientation selection, relationship
routing, active-edge machinery, continuation machinery, runtime behavior, schema,
or ontology. It does not assume relationships are primary. It records only what
repository evidence appears to support about movement between bounded views.

The starting question is:

```text
Which relationships repeatedly make
another bounded view relevant?
```

The non-goals are:

```text
How does orientation select a lens?
How should traversal work?
How should a runtime move between lenses?
```

## Files Inspected

Required files inspected:

- `docs/relation_cluster_observation.md`
- `docs/relation_of_use_observation.md`
- `docs/relation_of_use_decomposition_observation.md`
- `docs/relation_preservation_observation.md`
- `docs/relationship_frontier.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/relationship_observation_v0_reconciliation.md`
- `docs/relationship_promotion_reconciliation.md`
- `docs/object_role_operation_relation_cluster_observation.md`
- `docs/defines_relationship_reconciliation_audit.md`
- `docs/stable_orientation_multiple_lenses_probe.md`

Repository commands used for this observation included targeted `sed`, `rg`, and
`nl -ba` reads over the required files, plus `git status --short` to confirm the
working tree state before documentation was added.

## High-Level Finding

Repository evidence fits a relationship-centered explanation better than a
purely lens-centered explanation for why another bounded view becomes relevant.

The evidence does not show lens selectors, orientation engines, active lens
controllers, traversal algorithms, or runtime movement rules. It more often shows
stable concern, pressure, inquiry, or continuation posture encountering a
relationship that makes another bounded view relevant.

A cautious summary is:

```text
lenses bound what is viewed
relationships often explain why another bounded view matters now
```

This does not prove that relationships are canonical ontology or primary runtime
entities. The strongest documents repeatedly warn against over-materializing
relationship language into implementation, runtime machinery, or settled
ontology.

## Relationship Families Compared

The reviewed repository evidence supports comparison of these families:

- reachability / source navigation;
- relation-of-use;
- support / evidence-support;
- identity / scope / alias;
- ownership / authority / owning context;
- boundary;
- continuation;
- selection;
- ambiguity;
- current concern;
- pressure;
- activation;
- consequence / relevance / significance;
- safe move;
- discovery path / lineage.

The relation-of-use decomposition inventory remains the strongest single source
for candidate families. It treats these as observational labels only, not
ontology, schema, or runtime objects.

## Family Analysis

### Reachability / Source Navigation

Repository-supported meaning: reachability relates an inquiry, note, term,
source fact, concept, or architectural concern to reachable evidence, owning
documents, source artifacts, documentation families, or navigation routes.

Persistence: reachability can survive while the bounded view changes. In the
stable-orientation probe, Inquiry Orientation remains stable while Source /
Knowledge Navigation becomes relevant because the same inquiry needs a route to
owning evidence.

Load bearing: reachability carries navigation, evidence routing, source/document
ownership context, and safe movement from question-shaped material to supporting
surfaces.

Lens interaction: reachability appears inside Inquiry Orientation, between
Inquiry Orientation and Source / Knowledge Navigation, and across continuation
boundaries where discovery path or source route prevents rediscovery.

Failure mode: without reachability, the inquiry can remain visible but lack a
route to evidence or authority. Work then risks unsupported interpretation or
full rediscovery.

### Relation-Of-Use

Repository-supported meaning: relation-of-use is a cautious observational phrase
for the middle position between available knowledge and present use, concern,
consequence, or continuation point. Decomposition evidence suggests this phrase
compresses multiple support relations rather than naming one undivided relation.

Persistence: relation-of-use does not appear to persist as a single stable
thing. Different failures remove different relations: current concern,
consequence, continuation, safe movement, active question, or activation can
fail separately while knowledge, support, sources, or answers remain.

Load bearing: relation-of-use carries why-now, usefulness, governing status,
safe movement, significance, and continuation pressure.

Lens interaction: relation-of-use appears inside bounded views when knowledge is
shown in relation to present work, and between bounded views when current use
requires a different evidence or navigation surface.

Failure mode: facts, support, documents, questions, and answers may survive while
the reason they matter now disappears. The result is inert or non-governing
knowledge.

### Support / Evidence-Support

Repository-supported meaning: support relates evidence, corroborating material,
or claim-support material to the claim, conclusion, or confidence it supports.
It does not create truth by itself.

Persistence: support can survive while significance, consequence, current
concern, or activation disappears.

Load bearing: support carries evidence routing, claim warrant, confidence,
source trust boundaries, and preservation of why a claim may be held.

Lens interaction: support appears inside lenses as evidence counts or support
surfaces, between lenses when another bounded view is needed to inspect evidence,
and across continuation boundaries when successors need preserved warrant.

Failure mode: if support disappears, claims become unsupported. If support
survives but relation-to-use disappears, true or supported knowledge may still be
inert.

### Identity / Scope / Alias

Repository-supported meaning: identity includes same-as, identifies, alias,
endpoint, host, principal, service, projection-selected identity, and scoped
entity boundaries. Repository evidence treats identity errors as relation errors.

Persistence: identity or scope can persist while the bounded view changes. An
availability fact attached to endpoint, host, service, or unknown scope can make
Entity Navigation relevant without changing the underlying availability concern.

Load bearing: identity carries safe interpretation of scoped facts, canonical
entity routing, alias handling, and avoidance of false equivalence.

Lens interaction: identity appears inside Operational Availability as scope
classification and inside Entity Navigation as canonical entity, alias,
relationship, and drilldown visibility. It appears between those lenses when a
scoped availability fact is not intelligible on its own.

Failure mode: if identity or scope is removed, an availability fact may be read
against the wrong entity, alias, endpoint, host, or service.

### Ownership / Authority / Owning Context

Repository-supported meaning: ownership is safest when read as authority or
owning context, such as owning document, source artifact, or authority boundary.
It must not be generalized into runtime ownership without direct evidence.

Persistence: owning context can persist across source and knowledge navigation,
but runtime ownership does not follow from syntactic declaration, import,
defines, or navigation edges alone.

Load bearing: authority carries source/document ownership context, boundary
preservation, and protection against overclaiming from declaration to behavior.

Lens interaction: ownership appears inside Source / Knowledge Navigation and
between diagnostic views and source/document routes when constraints or authority
must be inspected.

Failure mode: if authority is removed, a bounded view may treat evidence as more
authoritative than it is. The `defines` audit shows this risk where one spelling
accumulates multiple meanings across documentation concept definition, source
declaration, existence claims, and structure claims.

### Boundary

Repository-supported meaning: boundary includes authority boundaries,
documentation/source boundaries, capability or execution boundaries, non-goals,
scope constraints, and constraints on safe movement.

Persistence: boundary can survive across lenses as the same constraint on
interpretation, authority, or movement. It can also disappear while facts remain.

Load bearing: boundary carries safe movement, non-crossing constraints,
authority preservation, and prevention of correct content being used in the wrong
context.

Lens interaction: boundary appears inside lenses as caveats, source boundaries,
authority limits, or scope constraints. It appears between lenses when boundary
ambiguity makes another bounded view relevant.

Failure mode: if boundary disappears, a fact may be used outside its authority
scope.

### Continuation

Repository-supported meaning: continuation is the relation by which preserved
work remains resumable, not merely archived. It includes preserved position,
rationale, pressure, safe next move, activation route, and handoff context.

Persistence: continuation can survive across multiple lenses while the work
position remains stable. Current Work Position is the clearest example: source
routes, availability caveats, storage ambiguity, and entity routes can each
preserve part of a continuable work position.

Load bearing: continuation carries safe resumption, handoff, activation path,
avoidance of rediscovery, and preservation of why routes and facts matter now.

Lens interaction: continuation appears inside Current Work Position, between
multiple bounded views needed for safe resumption, and directly across
continuation boundaries.

Failure mode: if continuation is removed, sources, lineage, or discovery paths
may survive while the successor still must rediscover why the path matters now.

### Selection

Repository-supported meaning: selection is narrowing into selected work,
selected pressure, selected branch, or active question. It is distinguishable
from activation because material can be selected or read without becoming usable
in working state.

Persistence: selection can survive across lenses as the same selected concern,
or disappear while pressure remains recorded.

Load bearing: selection carries which concern is live among alternatives, why one
pressure is current work, and preservation of non-selected remainder.

Lens interaction: selection appears inside Current Work Position and Active Edge
clusters. It appears between lenses when the selected concern requires a
different evidence surface.

Failure mode: if selection disappears, pressure may remain visible without being
current work, or a preserved inquiry may be mistaken for a live inquiry.

### Ambiguity

Repository-supported meaning: ambiguity is a pressure source. It may concern
scope, topology, ownership, evidence absence, stale availability, boundary
uncertainty, contradiction, or failed activation.

Persistence: ambiguity can persist across lenses as the same unresolved concern.
Storage ambiguity can remain stable while availability becomes relevant to test
absence, staleness, or scope confusion.

Load bearing: ambiguity carries relevance pressure, caveat preservation,
safe-reading constraints, and prompts for additional evidence surfaces.

Lens interaction: ambiguity appears inside Storage Projection and Operational
Availability, and between them when storage interpretation depends on
availability, freshness, or scope caveats.

Failure mode: if ambiguity is flattened, uncertain evidence may be promoted into
a clear finding, or absence/staleness/scope confusion may be misread as a direct
truth.

### Current Concern / Pressure

Repository-supported meaning: current concern is what has become operative for
present work or interpretation. Pressure is broader and can arise from gaps,
ambiguity, contradiction, consequence, boundary uncertainty, navigation failure,
preservation failure, or activation failure.

Persistence: current concern can persist while lenses change. Pressure can
persist without being selected as current concern.

Load bearing: current concern and pressure carry why-now, active attention,
selection into current work, and the reason another bounded view becomes
relevant.

Lens interaction: pressure appears inside lenses as caveat or unresolved pull,
between lenses when another evidence surface is needed, and across continuation
boundaries when preserved pressure must transition into successor work.

Failure mode: if current concern disappears, knowledge can remain available but
become inert or non-governing. If pressure is recorded without active question or
selection relation, pressure remains visible but not current work.

### Activation

Repository-supported meaning: activation is uptake into operative working state,
not merely availability, selection, or reading.

Persistence: activation may or may not survive lens changes. It is often visible
as a cross-cutting failure mode where artifacts exist but do not start the right
work.

Load bearing: activation carries live uptake, resumption, and conversion from
available material into governing work.

Lens interaction: activation appears inside working-state and handoff surfaces,
between lenses when route or evidence must become live work, and across
continuation boundaries when handoff content must activate successor work.

Failure mode: if activation disappears, an answer and source can survive while
work does not resume correctly.

### Consequence / Relevance / Significance

Repository-supported meaning: consequence is future effect, risk, downstream
change, or impact. Significance is not reducible to consequence because it also
depends on reference point, current concern, continuity need, operator context,
or active edge.

Persistence: consequence can survive while significance varies. Relevance can
vary by concern, reference point, and continuation need.

Load bearing: consequence and significance carry why a condition matters, why a
view matters now, and pressure on attention, continuation, or boundary.

Lens interaction: this family appears inside lenses as caveats, impact, or
why-this explanation, and between lenses when downstream consequence requires
another evidence surface.

Failure mode: support without significance leaves true knowledge inert.

## Relationship Persistence Observations

Repository evidence repeatedly shows that relationship persistence is not the
same as artifact persistence.

Relations appear to survive terminology changes when documents preserve:

- the current concern or reference point that makes knowledge matter now;
- the consequence or impact that explains why a known condition matters;
- the boundary that constrains legitimate use;
- the continuation point or safe next movement;
- the selected branch and active question;
- the activation path from preserved artifact to live work.

Relations appear lost when:

- knowledge remains available but no longer selects current work;
- support remains visible but significance disappears;
- pressure remains recorded but is not attached to an active question;
- continuation artifacts remain but no safe movement survives;
- facts survive but boundary relations disappear.

## Lens-Centered Explanation Compared With Relationship-Centered Explanation

### Lens-Centered Explanation

A lens-centered explanation says:

```text
The participant moved from Lens A to Lens B because Lens B is the next relevant view.
```

This usually requires additional assumptions:

- a selector;
- a traversal order;
- a controller;
- a lens transition rule;
- runtime or conceptual machinery deciding movement.

The required corpus does not show such machinery as repository-supported.

### Relationship-Centered Explanation

A relationship-centered explanation says:

```text
The participant remained oriented around the same concern,
but a relationship made another bounded view relevant.
```

This explanation can use already-supported relationships:

- evidence dependency;
- ambiguity dependency;
- identity or scope relation;
- reachability route;
- boundary constraint;
- continuation need;
- source or document authority.

### Storage -> Availability

Lens-centered explanation:

```text
Storage Projection selected Operational Availability.
```

This implies selector behavior that the repository does not support.

Relationship-centered explanation:

```text
A storage ambiguity depends on availability, freshness, and scope evidence.
```

This requires fewer assumptions because the stable-orientation probe already
supports the move as evidence dependency and ambiguity dependency, not traversal.

### Availability -> Entity Navigation

Lens-centered explanation:

```text
Operational Availability hands off to Entity Navigation.
```

This implies routing or handoff machinery.

Relationship-centered explanation:

```text
A scoped availability fact requires canonical entity, alias boundary,
relationship route, or drilldown target to be intelligible.
```

This requires fewer assumptions because identity and scope relationships already
explain why Entity Navigation becomes relevant.

### Inquiry Orientation -> Source / Knowledge Navigation

Lens-centered explanation:

```text
Inquiry Orientation transitions into Source Navigation.
```

This implies traversal.

Relationship-centered explanation:

```text
The same inquiry needs a reachability route to owning documents,
source artifacts, documentation families, or evidence surfaces.
```

This requires fewer assumptions because reachability and source-navigation
relations already explain the bounded-view change.

### Current Work Position -> Multiple Lenses

Lens-centered explanation:

```text
Current Work Position selects several lenses.
```

This implies active selection machinery.

Relationship-centered explanation:

```text
Current Work Position is a relation bundle whose continuation,
boundary, route, evidence, identity, and ambiguity needs make several
bounded views relevant.
```

This fits repository evidence better, provided Current Work Position remains a
cluster-bearing observation rather than a selector.

## Which Explanation Better Fits

The relationship-centered explanation better fits repository evidence because it
requires fewer unsupported assumptions.

The evidence shows:

- things and connections are distinct evidence shapes;
- behavior-oriented claims require relationship evidence, not artifact existence
  alone;
- preservation failures often leave objects in place while losing relations to
  concern, pressure, boundary, discovery path, activation, or next move;
- stable-orientation examples repeatedly name relationship types as what makes
  another bounded view relevant.

This finding remains limited. It does not promote relationships into canonical
ontology or runtime machinery.

## Candidate Observations

- Bounded views expose relationship pressure more than they cause movement.
- The same orientation can persist while relationship pressure changes the
  bounded viewing question.
- Movement is often evidence preservation, caveat preservation, identity repair,
  reachability routing, or continuation preservation rather than traversal.
- Identity and scope relationships are especially load-bearing for safe
  interpretation.
- Continuation is a relation bundle, not artifact survival.
- Support is necessary but not sufficient for live usefulness.
- Relationship vocabulary is already overloaded and must be handled cautiously.

## Remaining Uncertainties

- Relationship persistence remains unresolved, especially where endpoints,
  support, scope, confidence, and projection visibility can change.
- Relation-of-use may be a useful compression rather than one relation.
- Lens concepts still matter as bounded views; the evidence only weakens a
  lens-centered explanation of movement.
- Relationship-centered reading must not be over-promoted into runtime design.
- Ownership and authority remain risky because terms such as `defines` already
  accumulate multiple meanings across current repository evidence.

## Files Changed

This observation adds one documentation file:

- `docs/relationship_movement_between_bounded_views_observation.md`

## LOC Changed

One new Markdown file was added. No runtime files, tests, schemas, projections,
or implementation files were changed.
