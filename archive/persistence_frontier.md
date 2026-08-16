---
doc_type: frontier
status: exploratory
domain: persistence ontology
defines:
  - persistence frontier
  - conceptual persistence
  - persistence storage boundary
  - persistence identity boundary
  - continuity of represented understanding
  - persistence pressure test
  - persistence participation boundary
depends_on:
  - object_role_and_operation_frontier.md
  - object_role_operation_consistency_audit.md
  - object_role_operation_pressure_test.md
  - foundational_ontology_reconciliation.md
  - knowledge_representation_reconciliation.md
  - inquiry_frontier.md
  - handoff_and_continuation_lineage_frontier.md
  - architectural_status_and_next_frontier.md
related:
  - continuation_context_and_working_state_reconciliation.md
  - handoff_consumption_activation_reconciliation.md
  - knowledge_change_and_revision_reconciliation.md
  - relationship_fact_reconciliation.md
  - contradiction_discovery_and_visibility_reconciliation.md
  - architectural_findings_preservation.md
---

# Persistence Frontier

## Purpose

This document investigates a premise that recent object, role, operation,
inquiry, and handoff work has used but not directly examined:

```text
Objects persist.
Roles describe participation.
Operations describe what happens.
```

The unexamined word is `persist`.

This is ontology discovery only. It does not design storage systems, schemas,
identifiers, databases, lifecycle implementations, runtimes, engines, canonical
object categories, or implementation architecture. It does not reconcile Seed's
ontology and does not supersede repository authority.

The central question is:

```text
What does it mean for a represented thing to persist?
```

More specifically:

```text
What survives across time, inquiry, revision, participation changes, and
continuation?
```

This frontier does not assume that persistence means durability, identity,
storage, implementation retention, or conceptual sameness. It tests those
possibilities against repository evidence.

---

## Existing Authority That Constrains This Frontier

### Foundational Ontology

The foundational ontology reconciliation names the stable claim-centered
vocabulary currently needed to preserve Seed's core distinctions. It states that
observations report, evidence preserves provenance, claims are central knowledge
primitives, facts normalize claims, relationships normalize connection claims,
events preserve occurrences, changes preserve transitions, states describe
conditions over time, goals preserve purpose, and handoffs preserve continuation
alignment.

That language already uses preservation-like terms. This document must not turn
that usage into a storage design. It can only ask what kind of survival is being
claimed by those concepts.

### Knowledge Representation

The knowledge representation reconciliation distinguishes observation,
evidence, fact, relationships, contradictions, projections, explanations, and a
claim-support branch. It also distinguishes evidence support from claim support:

```text
Evidence supports facts.
Facts support claims.
```

This matters because persistence may attach to different things at different
layers. An observation payload may remain available, a fact may remain projected,
a support relation may remain represented, and a claim may remain supported or
challenged. Those are not automatically the same persistence.

### Inquiry Frontier

The inquiry frontier characterizes inquiry as the active or preserved pursuit of
unresolved understanding. It treats questions, tensions, gaps, findings,
frontiers, working state, active context, selection rationale, and handoff
lineage as candidates whose status remains mixed.

This document therefore treats inquiry artifacts as persistence candidates, not
as settled persistent objects.

### Handoff And Continuation Lineage

The handoff-lineage frontier found that continuation can fail even when
information is preserved. Successful handoffs appear to preserve a selected
active edge: current frontier, active context, working state, constraints,
unresolved tensions, selection rationale, validation state, and next safe moves.

This frontier asks whether that continuation dependence is evidence about
persistence itself, or only evidence about handoff practice.

### Object / Role / Operation Pressure Test

The pressure test found that the object / role / operation lens is useful but
incomplete. It is strongest when it separates durable represented things,
contextual participation, and activity. It is weakest where the repository needs
relationship semantics such as supports, contradicts, identifies, belongs_to,
runs_on, depends_on, authority, lineage, and working-state connections.

This document accepts that pressure result as a constraint: persistence cannot be
understood only as object survival if some of what survives is relational,
contextual, or inquiry-shaped.

---

## Method

For each candidate persistent concept, this document asks:

1. What might survive?
2. What clearly changes?
3. What would make a later participant recognize continuity?
4. What would falsify persistence?
5. Is the candidate better explained as object, role, operation, relationship,
   state, inquiry artifact, or compound context?

The candidates are:

```text
observation
evidence
claim
relationship
question
goal
gap
need
contradiction
ambiguity
finding
recommendation
frontier
```

The goal is not to classify them finally. The goal is to expose where the word
`persist` is doing architectural work and where it is hiding unresolved ontology.

---

## Working Distinction: Persistence Is Not Storage

A represented item can be stored without conceptually persisting.

Example:

```text
A stale projection row remains in a cache.
The repository no longer treats it as a live represented understanding.
```

The bytes or row survived, but the represented understanding may not have. It may
be obsolete, superseded, excluded from authority, or retained only as historical
material.

Conversely, a represented item may conceptually persist while its description
changes.

Example:

```text
Question Q is refined.
The wording changes.
The active unresolved pursuit remains recognizable.
```

The description did not survive unchanged, but something about the inquiry did.

Candidate distinction:

```text
storage = material retention of an artifact, record, projection, or text
persistence = recognizable continuity of represented understanding, unresolved
              pursuit, relation, commitment, or work-position across change
```

This distinction is useful, but dangerous if over-promoted. Some Seed concepts,
especially evidence, depend on retained source material and provenance. For those
concepts, storage-like preservation may be part of conceptual persistence. The
frontier finding is not that storage is irrelevant. It is that storage is not
sufficient.

---

## Working Distinction: Persistence Is Not Identity

Identity asks:

```text
Is this the same thing?
```

Persistence asks:

```text
What, if anything, survived through change?
```

They overlap but are not identical.

Persistence may require a weak continuity test without requiring strong identity:

```text
The endpoint-prominence tension becomes several narrower Prometheus questions.
The original tension may persist as lineage pressure even if no single refined
question is identical to the starting question.
```

Identity may require persistence when sameness is asserted across time:

```text
Host A today is the same represented host as Host A tomorrow.
```

But identity can also be an instantaneous relation:

```text
Alias A identifies Entity B in this source.
```

That relation can be represented without answering how either term persists
through future revision.

Candidate distinction:

```text
identity = sameness, identification, membership, belonging, or canonicalization
persistence = continuity through time, revision, role changes, inquiry movement,
              and handoff
```

The pressure test already warned that identity is strongest as a relationship or
claim family, not a simple object. This document adds that identity claims may be
one way of recognizing persistence, but they do not exhaust persistence.

---

## Candidate Persistent Concepts

### Observation

#### What Might Persist

An observation may persist as a reported encounter with a source at a time, with
payload, scope, source, and acquisition context. The foundational ontology says
observations report, and knowledge representation places observation before
evidence.

#### What Changes

Observation interpretation can change. Later work can reinterpret the payload,
exclude it from a projection, attach stronger caveats, or decide it supports a
different claim than first expected.

#### Continuity Test

An observation persists when later participants can still refer to the same
reported source encounter, even if the meaning extracted from it changes.

#### Falsifying Finding

If `observation` is used merely for the current projected view, it does not
persist as observation. Projection changes are not observation survival. The
observation's persistence depends on retaining the reported encounter or its
provenance, not on preserving a derived current-state surface.

### Evidence

#### What Might Persist

Evidence has the strongest persistence profile among the candidates. The pressure
test describes evidence as preserved provenance and support material that remains
after acquisition ends and can later be cited, challenged, reinterpreted, or
excluded from a projection.

#### What Changes

Evidentiary role can change. The same claim, fact, observation, or artifact can
support one claim, contradict another, become handoff content, or stop being
selected for a response.

#### Continuity Test

Evidence persists when the support material and provenance remain available for
later audit, explanation, reinterpretation, or challenge.

#### Falsifying Finding

`Evidence for X` is relational. A thing can persist while its evidentiary role
changes. Therefore evidence persistence cannot be reduced to the persistence of
an evidence-role assignment.

### Claim

#### What Might Persist

A claim may persist as a represented proposition, even as support changes,
confidence changes, contradiction visibility changes, or projection selection
changes.

#### What Changes

Claim wording may be refined, scope narrowed, strength adjusted, evidence added,
or contradiction discovered. If refinement changes the proposition too far, the
original claim may no longer be the same claim; it may have generated a successor
claim.

#### Continuity Test

A claim persists when later participants can recognize the represented
proposition under revision history, support evolution, and scope clarification.

#### Falsifying Finding

If every wording refinement is treated as the same claim, Seed risks hiding real
knowledge change. If every wording refinement is treated as a new claim, Seed
loses lineage. Claim persistence therefore appears to require both proposition
continuity and revision humility.

### Relationship

#### What Might Persist

A relationship may persist as a represented connection claim between terms:

```text
Claim A supports Claim B.
Claim A contradicts Claim B.
Endpoint A belongs_to Host B.
Module M depends_on Module N.
```

The foundational ontology already names relationships as normalized connection
claims, and the pressure test found relationship semantics to be the strongest
falsification candidate for a three-part object / role / operation lens.

#### What Changes

Relationship support, scope, confidence, active role, projection visibility, and
contradiction state can change. The related terms may also change or be
reidentified.

#### Continuity Test

A relationship persists when the represented edge remains recognizable across
support changes, inquiry movement, or projection changes.

#### Falsifying Finding

Some relationships are episodic participation edges rather than durable
connection claims:

```text
Question Q is target of this inquiry.
Finding F is active in this working state.
Claim C is selected for this response.
```

Those may persist only within the episode or handoff context. Treating all
relationships as durable would over-materialize participation.

### Question

#### What Might Persist

A question may persist as the directed pursuit of an unresolved issue. The
inquiry frontier treats questions as strong inquiry-adjacent objects and asks
whether they have lineage.

#### What Changes

Questions refine. A broad question can split into narrower questions, merge with
another tension, become inactive, become a handoff item, or produce findings.

#### Continuity Test

A question persists when the unresolved pursuit remains recognizable despite
wording, scope, or target refinement.

#### Critical Example

```text
Question Q becomes refined.
```

Possible readings:

1. same question, refined description;
2. successor question in the same inquiry lineage;
3. old question closed and new question opened;
4. underlying tension persisted while the question changed.

The strongest repository-aligned reading is usually not simple identity. Inquiry
lineage can persist even when the question object changes.

#### Falsifying Finding

A question does not persist merely because similar words recur. If the unresolved
pursuit, scope, or selection rationale changes completely, recurrence of phrasing
is storage or textual similarity, not conceptual persistence.

### Goal

#### What Might Persist

A goal may persist as preserved purpose or operator intent. The foundational
ontology names goals as preserving purpose, and goal/policy/authority documents
make goals relevant to recommendations, decisions, and authority.

#### What Changes

A goal can be refined, decomposed, subordinated, paused, superseded, or rejected.
Its role can change from active driver to background constraint to historical
reason for a decision.

#### Continuity Test

A goal persists when the purpose remains recognizable across plan changes,
inquiry movement, recommendation changes, or continuation handoff.

#### Falsifying Finding

A plan step, next safe move, or recommendation can be mistaken for a goal. If the
supposed goal disappears when one recommended action is replaced, it may have
been an operational proposal rather than persistent purpose.

### Gap

#### What Might Persist

A gap may persist as a missing answer, missing evidence path, missing visibility,
missing implementation, or missing understanding. The inquiry frontier
characterizes gap as absence and frontier as active or preservable exploratory
edge.

#### What Changes

A gap's role can change:

```text
today:     attention target
tomorrow:  inquiry target
later:     handoff content
```

The description may sharpen, the evidence path may improve, and the gap may move
from passive absence to active frontier.

#### Critical Example

```text
Gap G

today:
    attention target

tomorrow:
    inquiry target

later:
    handoff content
```

Possible survivors:

1. the same missing understanding;
2. the description of that missing understanding;
3. the relationship between a goal and the missing prerequisite;
4. the inquiry opened to close the gap;
5. only a lineage marker connecting distinct episodes.

The best current finding is that `gap` persistence is often persistence of an
absence-under-description plus its relevance relation. The role changes do not
by themselves create new gaps, but a refined gap can become a successor if the
missing object changes.

#### Falsifying Finding

Some gaps are merely projection or attention artifacts. If a later participant
finds that the underlying knowledge existed but was not selected or visible, the
`gap` may not have persisted as missing understanding. What persisted was a
visibility or selection problem.

### Need

#### What Might Persist

A need may persist as a requirement, operator need, capability need, information
need, or continuation need. It often connects a goal to a missing condition.

#### What Changes

The object needed can change as understanding improves. A need may be satisfied,
deferred, invalidated, reframed as a policy constraint, or decomposed into
multiple needs.

#### Continuity Test

A need persists when the requirement pressure remains recognizable even while
candidate satisfiers change.

#### Falsifying Finding

A need is often relational: some actor, goal, inquiry, or system needs something
for some purpose. If the relation is not preserved, the `need` becomes a vague
object detached from why it mattered.

### Contradiction

#### What Might Persist

A contradiction may persist as a represented relation between claims, evidence,
facts, or projections:

```text
Claim A contradicts Claim B.
```

The knowledge representation reconciliation includes contradictions among
projected knowledge structures, and the pressure test treats `contradicts` as a
relationship-like term.

#### What Changes

New evidence can change support, confidence, interpretation, scope, or whether
the apparent conflict is real. It can reveal that one claim was too broad, that
both claims are source-scoped, or that the contradiction was actually ambiguity.

#### Critical Example

```text
Claim A contradicts Claim B.

Later:
    New evidence arrives.
```

Possible outcomes:

1. contradiction persists with stronger support;
2. contradiction persists but scope narrows;
3. contradiction is resolved because one claim is revised;
4. contradiction is reclassified as ambiguity or source disagreement;
5. only the history of contradiction persists.

#### Falsifying Finding

Contradiction persistence is not the same as claim persistence. Claim A and Claim
B can persist while the contradiction relation between them does not. Conversely,
the contradiction can persist while the active attention role changes.

### Ambiguity

#### What Might Persist

Ambiguity may persist as unresolved multiple interpretation, unclear scope,
uncertain reference, or underspecified meaning.

#### What Changes

Ambiguity can be clarified, split into questions, become a contradiction, become
a gap, or be accepted as a caveat. It can move from attention trigger to inquiry
target to handoff warning.

#### Continuity Test

Ambiguity persists when the unresolved interpretive multiplicity remains
recognizable across descriptions and episodes.

#### Falsifying Finding

Ambiguity may be a state of another object rather than an object. Treating it as
a durable thing can hide that the persistent item is a claim, relationship,
question, or term whose interpretation remains unstable.

### Finding

#### What Might Persist

A finding may persist as an inquiry result that contains claims, method, scope,
support, rejected collapses, and implications. The inquiry frontier treats
finding as a bridge between inquiry and knowledge.

#### What Changes

A finding can be expanded, narrowed, superseded, cited, preserved as rejected,
carried forward, or promoted into a reconciliation.

#### Critical Example

```text
Finding F

Later:
    Finding F is expanded.
```

Possible readings:

1. same finding with more support or explanation;
2. refined finding with altered scope;
3. successor finding in the same inquiry lineage;
4. new finding that cites the old one;
5. old finding preserved historically but no longer active.

#### Continuity Test

A finding persists when its inquiry result remains recognizable across support
expansion, scope clarification, and later use.

#### Falsifying Finding

If expansion changes the question answered, the method, or the conclusion, the
original finding may not persist as the same finding. What persists may instead
be lineage from old finding to new finding.

### Recommendation

#### What Might Persist

A recommendation may persist as advice tied to goal, evidence, context,
constraints, risk, and decision boundary.

#### What Changes

A recommendation can be accepted, rejected, superseded, invalidated by new
evidence, narrowed by policy, or transformed into a decision. Its active role can
change without erasing the fact that the advice was once given.

#### Continuity Test

A recommendation persists conceptually when the advice and its rationale remain
available for explanation, audit, or later reconsideration.

#### Falsifying Finding

A recommendation should not be treated as persistent command, decision, or goal.
If its purpose was only to support a transient response and no rationale or
selection context survives, it may be stored text but not a persistent
recommendation in the architectural sense.

### Frontier

#### What Might Persist

A frontier may persist as an unresolved boundary, document artifact, collection
of questions and tensions, active edge, handoff content, or preservation
structure. The object / role / operation pressure test found frontier to be
strongly overloaded.

#### What Changes

Frontiers evolve. An attention frontier can expose an object / role / operation
frontier. A frontier can be refined into a reconciliation, split into multiple
frontiers, become dormant, or remain as a warning that implementation is
premature.

#### Critical Example

```text
Attention Frontier

Weeks later:
    Object / Role / Operation Frontier
```

Possible survivors:

1. the same frontier persisted under a new name;
2. inquiry persisted while frontier object changed;
3. tension persisted while the investigation target changed;
4. selected unresolved pressure persisted as lineage;
5. no frontier persisted; only a historical path connects them.

The strongest current reading is usually lineage persistence, not simple frontier
identity. A frontier document persists as artifact; the unresolved pressure may
persist through successor frontiers; the active boundary may move.

#### Falsifying Finding

If every later frontier is treated as the same persistent frontier, Seed loses
the ability to recognize real inquiry movement. If no continuity is recognized,
Seed loses the ability to explain why later frontiers inherit unresolved pressure
from earlier work.

---

## Relationship To Inquiry

The inquiry sequence can be described as:

```text
Question
    ↓
Inquiry
    ↓
Finding
```

A simplistic persistence reading would say:

```text
Question persists until finding answers it.
```

Repository evidence is more complex.

Questions refine, branch, merge, and sometimes disappear into broader tensions.
Inquiry can continue after one question is answered because the finding exposes a
new gap or frontier. Findings can preserve inquiry result and also carry
unresolved implications forward.

What appears to persist through inquiry is often not one object but a structured
continuity:

```text
unresolved pressure
selected question or tension
active pursuit
support and method
finding or rejected collapse
remaining gap or next frontier
```

This supports the inquiry frontier's characterization: inquiry is process-like,
but the repository also preserves inquiry-shaped state and lineage. Persistence
may therefore be one reason inquiry cannot be dismissed as mere workflow.

However, this does not justify an inquiry runtime or formal inquiry object graph.
It only shows that conceptual continuity through inquiry matters.

---

## Relationship To Handoffs And Continuation

Continuation depends on persistence, but persistence is broader than
continuation.

A handoff can preserve all major conclusions and still fail if it does not
preserve:

```text
active position
selection rationale
working state
unresolved tensions
navigation context
validation state
next safe move
unsafe next move
```

This means continuation requires a particular kind of persistence: the survival
of enough active work-position for a future participant to resume safely.

Persistence is broader because many things can persist without being selected
for continuation:

```text
stored evidence
historical finding
superseded recommendation
inactive question
resolved contradiction history
dormant frontier
```

Continuation persistence is therefore selection-sensitive. It asks not merely
what survived, but what must remain active and why.

---

## Relationship To Working State

One candidate explanation is:

```text
working state = persistent objects
              + current roles
              + operation context
```

This is attractive because it matches the object / role / operation lens:

```text
question persists
question is active now
inquiry or continuation operates over it
```

But the pressure test found working state to be more compound than that.
Working state also depends on relationships and selection rationale:

```text
finding supports next move
tension blocks reconciliation
question depends_on unresolved evidence
frontier references settled authority
selection rationale explains active subset
```

A stronger current explanation is:

```text
working state preserves a bounded current work-position composed of selected
persistent candidates, current participation roles, relationship context,
operation context, validation state, and selection rationale.
```

This explanation remains exploratory. It should not be turned into a schema,
state store, or runtime model.

---

## Object Pressure Test: Do Objects Persist?

The statement under test is:

```text
Objects persist.
```

### Supporting Evidence

The statement is useful when it prevents category collapse:

```text
claim is not the same as selected claim
evidence is not the same as observing
question is not the same as inquiry target
frontier document is not the same as frontier investigation
handoff artifact is not the same as continuation behavior
```

It helps explain why roles can change without replacing the underlying
represented thing.

### Falsifying Evidence

The statement becomes too broad if all candidate objects are assumed to persist
in the same way.

Some candidates are better explained as:

```text
relationships: support, contradiction, identity, need-for
states: ambiguity, active working state, unresolvedness
inquiry artifacts: question, gap, finding, frontier
participation roles: attention target, inquiry target, handoff content
operation results: recommendation, derived relationship, refined question
compound contexts: working state, frontier, handoff lineage
```

Some objects may persist only historically, not as active conceptual objects.
Some role assignments are temporary. Some relationships persist only within an
episode. Some inquiry artifacts survive as lineage rather than identity.

### Current Finding

`Objects persist` survives as a useful diagnostic slogan only if `persist` is
understood as variable and pressure-tested:

```text
objects may persist as represented propositions, evidence material, connection
claims, purposes, inquiry results, unresolved pressures, or continuation
positions.
```

The slogan fails if persistence is assumed to mean durable storage, unchanged
identity, active relevance, or implementation retention.

---

## Potential Finding Under Test

Candidate finding:

```text
Persistence is not storage.

Persistence is continuity of represented understanding across participation
changes.
```

### Evidence Supporting It

The repository repeatedly shows represented things changing roles:

```text
claim -> selected claim -> evidence for another claim -> handoff content
question -> active question -> refined question -> finding source
gap -> attention target -> inquiry target -> handoff content
frontier -> active edge -> successor frontier -> reconciliation input
```

In these cases, persistence appears to be recognized by continuity across
participation changes rather than by fixed role.

### Evidence Against It

The phrase `represented understanding` may be too narrow.

Evidence may persist as provenance material, not only understanding.
A contradiction may persist as a relationship, not an understanding.
A goal may persist as purpose.
A need may persist as requirement pressure.
A working state may persist as a current position rather than as an understood
claim.

A stronger but less elegant candidate is:

```text
Persistence is recognizable continuity of a represented item, relation,
unresolved pressure, purpose, or work-position across time, revision,
participation changes, inquiry movement, and continuation.
```

This is not a definition. It is the best exploratory formulation currently
supported by the reviewed documents.

---

## Persistence Tensions Preserved

| Tension | Frontier finding |
| --- | --- |
| Persistence vs storage | Storage can retain artifacts that no longer conceptually persist; conceptual persistence can survive description changes. Evidence remains the hard case because provenance retention matters. |
| Persistence vs identity | Identity asks sameness; persistence asks what survived through change. Persistence can be lineage-like without strict identity. |
| Persistence vs durability | Durability suggests long-lived retention. Persistence may be brief, episodic, historical, active, dormant, or lineage-based. |
| Persistence vs revision | Revision can preserve, refine, supersede, or replace the represented thing. Revision history is not automatically sameness. |
| Persistence vs refinement | Refinement may keep the same object, produce a successor, or preserve only underlying tension. |
| Persistence vs inquiry | Inquiry can preserve unresolved pursuit, not only knowledge products. But inquiry persistence is not yet a reconciled ontology. |
| Persistence vs continuation | Continuation requires selected active persistence, but many persistent items are not continuation-relevant. |
| Persistence vs relationship | Some survivors are edges, not object cores. Relationship persistence is central for support, contradiction, identity, need, and working state. |
| Persistence vs frontier | Frontier artifacts persist as documents, but frontier pressure may persist as inquiry lineage while the active boundary changes. |
| Persistence vs role | Role changes can reveal persistence, but role assignments may themselves be episodic. |
| Persistence vs active relevance | A thing can persist historically while no longer active; active state is participation, not proof of persistence. |

---

## Strongest Findings

1. Persistence is not equivalent to storage.
2. Persistence is not equivalent to identity.
3. Persistence is not a single property shared uniformly by all objects.
4. Evidence has the strongest storage-adjacent persistence because provenance and
   support material must remain available for later audit.
5. Claims, relationships, questions, gaps, contradictions, findings, and
   frontiers can persist through refinement, but sometimes only as lineage rather
   than strict identity.
6. Relationship persistence is unavoidable because support, contradiction,
   identity, need, and working-state usefulness depend on edges.
7. Inquiry persistence appears real as continuity of unresolved pursuit, but it
   remains frontier material and not implementation direction.
8. Continuation requires selected active persistence: enough work-position,
   selection rationale, and validation state to resume safely.
9. Working state is better explained as compound current work-position than as a
   simple persistent object.
10. Implementation remains premature because the repository has not reconciled
    whether persistence attaches primarily to objects, relationships, states,
    inquiry artifacts, lineage, or compound contexts.

---

## Strongest Falsifying Findings

The strongest falsifications of naive persistence are:

```text
Stored does not mean persistent.
Same wording does not mean same question.
Same claims do not guarantee same contradiction.
Expanded finding may be a successor rather than the same finding.
Frontier lineage does not prove frontier identity.
Active role does not create durable object identity.
Relationship edges may persist or disappear independently of endpoint objects.
Continuation can fail despite preserved information.
```

These falsifications do not show that persistence is false. They show that
persistence is not yet understood well enough to carry implementation authority.

---

## Unresolved Questions

1. Is persistence a property of represented objects, a relationship among states,
   a lineage judgment, or a recognition practice by future participants?
2. Can Seed distinguish same object, refined object, successor object, historical
   predecessor, and inherited tension without designing identifiers?
3. Are relationship claims persistent objects with edge semantics, or does
   persistence require relationship as a distinct category?
4. Is inquiry persistence reducible to question lineage, or do gaps, tensions,
   findings, frontiers, and working state persist in their own ways?
5. Can a contradiction persist if both claims are revised?
6. Can a need persist after the goal that created it is superseded?
7. When a frontier becomes a reconciliation, what persists: frontier, inquiry,
   finding, tension, or authority boundary?
8. Does working state preserve persistent objects plus roles plus operation
   context, or does it preserve a distinct selected work-position?
9. How much persistence depends on future participant recognition rather than on
   intrinsic ontology?
10. What minimal vocabulary would let future documents discuss persistence
    without creating schema, identifiers, lifecycle machinery, or storage design?

---

## Non-Goals

This document does not:

- reconcile persistence ontology;
- define object identity rules;
- propose schemas, identifiers, storage systems, databases, state stores, or
  lifecycle implementation;
- introduce runtime behavior, engines, workflow systems, inquiry systems,
  continuation systems, or persistence services;
- modify code, projections, observations, evidence handling, claims,
  relationships, handoffs, recommendations, tests, or documentation authority;
- decide whether relationship is a fourth top-level category;
- decide whether inquiry objects are formal ontology objects;
- turn persistence into an implementation requirement.

---

## Final Characterization

Persistence matters because recent ontology work depends on a distinction between
what survives and what merely participates or happens.

The best current characterization is:

```text
Persistence is recognizable continuity of a represented item, relation,
unresolved pressure, purpose, or work-position across time, revision,
participation changes, inquiry movement, and continuation.
```

This characterization is intentionally tentative.

It supports the object / role / operation lens by explaining why roles can change
while something survives. It also limits that lens by showing that what survives
may be a relationship, inquiry lineage, unresolved tension, or compound working
state rather than a simple object.

Implementation remains premature. Before Seed can design any persistence-related
mechanism, future work would need to reconcile persistence versus storage,
identity, relationship, revision, inquiry, continuation, and working state. Until
then, persistence should remain an exploratory ontology frontier and a warning
against assuming that stored artifacts, stable names, active roles, or unchanged
text are the same as conceptual continuity.
