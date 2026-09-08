---
doc_type: frontier
status: exploratory
domain: relationship ontology
defines:
  - relationship frontier
  - relationship ontology pressure signal
  - relationship object boundary
  - relationship role boundary
  - relationship operation boundary
  - relationship persistence question
  - relationship continuity question
depends_on:
  - object_role_and_operation_frontier.md
  - object_role_operation_consistency_audit.md
  - object_role_operation_pressure_test.md
  - persistence_frontier.md
  - continuity_frontier.md
  - relationship_fact_reconciliation.md
  - relationship_promotion_reconciliation.md
  - entity_identity_derivation_reconciliation.md
  - corroboration_and_fact_promotion_reconciliation.md
  - evidence_trust_and_source_authority_reconciliation.md
  - foundational_ontology_reconciliation.md
  - architectural_status_and_next_frontier.md
related:
  - claim_support_frontier.md
  - operations_frontier.md
  - operation_attribution_frontier.md
  - inquiry_frontier.md
  - handoff_and_continuation_lineage_frontier.md
  - contradiction_discovery_and_visibility_reconciliation.md
  - knowledge_change_and_revision_reconciliation.md
---

# Relationship Frontier

## Purpose

This document investigates relationship directly.

It exists because recent repository investigations repeatedly produced pressure
toward relationship semantics. The strongest examples include:

```text
support
evidence-for
corroborates
contradicts
same-as
belongs-to
runs-on
authority relations
```

The object / role / operation pressure test found that relationship is the
strongest candidate for a missing explanatory category. This frontier asks what
that pressure means without resolving it.

This is ontology discovery only. It does not reconcile Seed's ontology, introduce
canonical categories, design schemas, design graph models, design storage,
design runtime relationship engines, modify code, modify projections, modify
runtime behavior, or create implementation direction.

Repository authority wins over this document. The foundational ontology,
relationship fact, relationship promotion, identity derivation, corroboration,
evidence trust, persistence, continuity, operations, and architectural-status
documents remain authoritative for their settled boundaries.

The central question is:

```text
What is a relationship?
```

More specifically:

```text
What kind of thing is a relationship?
```

This document does not assume relationship is primitive, object, role, operation,
state, or missing top-level category. It evaluates repository evidence.

---

## Existing Authority That Constrains This Frontier

### Foundational Ontology

The foundational ontology already names relationships as normalized connection
claims between things. That creates important evidence that Seed already needs
relationship-shaped knowledge.

This frontier must not replace that authority. It asks what kind of thing such a
connection claim might be, not whether settled relationship vocabulary should be
removed or redefined.

### Relationship Fact Reconciliation

The relationship fact reconciliation found that artifact facts describe things
and relationship facts describe connections between things. It introduced the
architectural need for behavior-oriented relationship evidence such as calls,
routes, stores, emits, validates, imports, depends on, implements, contains, and
other observed connections.

This frontier accepts that as repository evidence. It does not decide whether the
existing `RelationshipFact` concept is the final ontology for all relationship
kinds.

### Relationship Promotion Reconciliation

The relationship promotion reconciliation treats promoted relationships as
bounded, evidence-supported, source-scoped knowledge. It preserves that promoted
relations remain limited by source authority, confidence, conflict, and
projection humility.

This frontier must not turn promotion rules into a universal relationship model.
Promotion is evidence handling; relationship ontology is the topic under
investigation.

### Entity Identity Derivation

The identity reconciliation warns against collapsing endpoint, host, alias,
principal, service, and projection-selected identities. It treats same-as,
belongs-to, identifies, and runs-on language as high-risk because identity errors
are often relation errors.

This frontier uses identity examples as pressure cases, not as settled equality
semantics.

### Corroboration And Evidence Trust

Corroboration documents distinguish compatible support from truth creation, and
evidence-trust documents distinguish source, authority, support, confidence,
review, and promotion. These documents repeatedly require relationship language:
evidence supports claims, sources are authoritative for scopes, and independent
items corroborate a target under constraints.

This frontier preserves that support and authority are bounded and do not become
truth merely because a relationship is represented.

### Persistence And Continuity

The persistence frontier found that relationships may persist as recognizable
edges while their support, scope, confidence, projection visibility, or endpoints
change. It also warned that some relationships are episodic participation edges
that should not be over-materialized.

The continuity frontier found that support, contradiction, authority,
dependency, and working-state usefulness can survive as edges, but relationship
continuity remains unresolved.

This frontier investigates those findings without implementing persistence,
continuity, lineage, storage, or identifiers.

### Object / Role / Operation Pressure Test

The pressure test found that object / role / operation language is useful but
strained by edge-like examples:

```text
Observation O supports Claim C
Claim A contradicts Claim B
Host A same-as Host B
Endpoint A belongs-to Host B
Operator may execute Action X
Module M depends-on Module N
```

It left open whether relationship is a special kind of object with edge
semantics, a fourth category, or something else.

This frontier begins from that unresolved point.

---

## Method

For each candidate relationship, this document asks:

1. What appears to be connected?
2. Is the term object-like, role-like, operation-like, state-like, or edge-like?
3. What persists, if anything?
4. What can change without destroying the relationship?
5. What would falsify a simple relationship reading?
6. What repository boundary must be preserved?

The candidate terms are:

```text
supports
contradicts
corroborates
identifies
same-as
belongs-to
runs-on
depends-on
trusts
authorizes
adopts
recommends
```

The goal is not to classify all examples into one kind. The goal is to expose
what relationship language is doing.

---

## Working Hypothesis Under Test

A possible finding is:

```text
Objects explain represented things.
Roles explain participation.
Operations explain what happens.
Relationships explain connection.
```

This is not assumed. It is tested below.

The hypothesis is attractive because it separates four pressures:

| Pressure | Example | Risk if collapsed |
| --- | --- | --- |
| Object | `Claim C exists.` | Temporary participation becomes a durable thing. |
| Role | `Claim C is selected for this response.` | Contextual participation becomes global identity. |
| Operation | `Promotion produced Fact F.` | Activity is mistaken for what persists. |
| Relationship | `Evidence E supports Claim C.` | Connections become hidden inside endpoint roles or operations. |

The hypothesis is also dangerous. If every relation becomes a durable object,
Seed may over-materialize temporary, scoped, or projection-relative edges. If
relationship becomes a primitive too quickly, Seed may bypass existing claim,
evidence, promotion, source-authority, and projection humility boundaries.

---

## Candidate Relationship Evaluations

### Supports

Critical example:

```text
Observation O supports Claim C
```

`Supports` is the strongest relationship signal in the repository.

Object reading:

```text
A support record, support group, or support explanation can be represented as an
object.
```

Role reading:

```text
Observation O occupies a supporting-evidence role relative to Claim C.
```

Operation reading:

```text
An operation may assess, attach, promote, select, or project support.
```

Relationship reading:

```text
O is connected to C by a directed support edge.
```

The relationship reading is necessary because role language alone does not answer
`supporting what?`, and operation language alone does not preserve what remains
after support is assessed or attached.

What persists is not necessarily a separate support object. What may persist is
a represented edge:

```text
supporter -> supported
```

with evidence, scope, strength, freshness, contradiction state, and promotion
constraints.

Falsifying finding: support is overloaded. Sometimes `support` refers to the
supporting material, sometimes to the relation, sometimes to a record of the
relation, and sometimes to an operation or projection. Therefore `supports` is a
relationship pressure signal, not proof that relationship is a primitive.

### Contradicts

Critical example:

```text
Claim A contradicts Claim B
```

Contradiction has strong relationship behavior because it concerns incompatibility
between represented claims. Neither claim alone contains the whole contradiction.
The pressure appears between them.

Object reading:

```text
A contradiction finding or contradiction record may be preserved as an object.
```

Role reading:

```text
Claim A may occupy a contradicting role relative to Claim B.
```

Operation reading:

```text
Comparison, review, or integrity assessment may discover contradiction.
```

Relationship reading:

```text
A and B are connected by an incompatibility relation under a scope.
```

What persists?

The claims may persist. The contradiction record may persist. More importantly,
the incompatibility pressure may persist even when wording, scope, confidence, or
visibility changes.

Falsifying finding: contradiction can disappear when terms are clarified. If a
later review shows that A and B use different scopes or meanings, the perceived
contradiction may have been an interpretation error rather than a persistent
relationship.

### Corroborates

`Corroborates` is relationship-like but not identical to `supports`.
Corroboration concerns compatible, independent, or mutually reinforcing support
for a target. It can connect evidence to evidence, evidence to a claim, or facts
to a promotion candidate, depending on the source document and scope.

Object reading:

```text
A corroboration assessment can be recorded.
```

Role reading:

```text
An evidence item can occupy a corroborating role in a promotion review.
```

Operation reading:

```text
A promotion or review operation can evaluate corroboration.
```

Relationship reading:

```text
Evidence E1 corroborates Evidence E2 for Claim C under Scope S.
```

This may be ternary or scoped rather than a simple binary edge. The target of
corroboration matters. `E1 corroborates E2` is incomplete if the compatibility is
only relevant to a specific claim, fact, source scope, or promotion question.

Falsifying finding: corroboration does not create truth. Compatible support
strengthens an evaluation, but repository authority rejects collapsing
corroboration into verified fact, ownership, or source authority.

### Identifies

`Identifies` appears in identity derivation, endpoint/host boundaries, source
authority, principal identity, and projection display concerns.

Object reading:

```text
Identifier values, entity records, aliases, and identity claims can be objects.
```

Role reading:

```text
A name, endpoint, source string, or principal value may act as an identifier in a
specific source context.
```

Operation reading:

```text
Matching, normalization, derivation, or promotion may produce an identity claim.
```

Relationship reading:

```text
Identifier I identifies Entity E under Source S and Scope K.
```

The relationship reading is necessary because the identifier and identified
entity are distinct terms. The source and scope matter. An endpoint can identify
a scrape target without proving host identity. A label can identify a projection
representative without becoming authoritative identity.

Falsifying finding: `identifies` can be a weak source-scoped relation rather than
strong identity. Treating every identifying relation as same-as would reproduce
the identity-collapse errors that existing reconciliations warn against.

### Same-As

Critical example:

```text
Host A same-as Host B
```

`Same-as` is a symmetric identity relation candidate. It is stronger than
`identifies`, `belongs-to`, `observed-at`, or `runs-on`.

Object reading:

```text
A same-as claim can be preserved and cited.
```

Role reading:

```text
One entity can act as canonical representative for another in a projection.
```

Operation reading:

```text
Identity derivation or deduplication may produce the same-as assertion.
```

Relationship reading:

```text
A and B are asserted to be the same entity under evidence and scope.
```

The relationship reading is strong because identity here is fundamentally about
how two represented terms relate. The assertion can persist, be challenged,
revised, supported, contradicted, or demoted.

Falsifying finding: identity may not be purely relational. Entity records,
identifier histories, projection representatives, and source authority all matter.
Also, a same-as claim may be a claim object representing an equality relation,
which means relationship can be object-like in representation.

### Belongs-To

`Belongs-to` is a containment, membership, attachment, or association candidate.
It is weaker and more varied than same-as.

Examples:

```text
Endpoint A belongs-to Host H
Finding F belongs-to Frontier R
Capability C belongs-to Component X
```

Object reading:

```text
A membership or containment claim can be preserved.
```

Role reading:

```text
A participant can occupy member, contained item, child, or attached-resource role.
```

Operation reading:

```text
Observation, interpretation, or projection may attach one thing to another.
```

Relationship reading:

```text
A is associated with B by a scoped containment or membership relation.
```

Falsifying finding: `belongs-to` is dangerously overloaded. It may mean
ownership, containment, source attachment, projection grouping, topology,
membership, or display nesting. A relationship frontier should not promote
`belongs-to` without preserving which relation kind is actually meant.

### Runs-On

Critical example:

```text
Service S runs-on Host H
```

`Runs-on` is a runtime topology relation candidate. It relates a service,
process, endpoint, component, container, host, or environment to a substrate.

Object reading:

```text
A runtime topology claim or observation can be preserved.
```

Role reading:

```text
Host H may occupy execution substrate role for Service S in an observed context.
```

Operation reading:

```text
Observation, deployment, scheduling, startup, or monitoring may discover or
change the relation.
```

Relationship reading:

```text
Service S is executing on Host H during Scope/Time T according to Source V.
```

`Runs-on` is often stateful and temporal. A service may move. A host may be an
endpoint, container node, VM, physical host, or projection-selected entity.

Falsifying finding: `runs-on` may be a stateful observation rather than a durable
relationship. Treating it as globally persistent can overstate runtime evidence.
The safer reading is a scoped relation that may persist only while the observed
state remains valid.

### Depends-On

`Depends-on` appears in repository structure, runtime behavior, capability use,
knowledge justification, and frontier routing.

Object reading:

```text
A dependency fact or dependency record can be represented.
```

Role reading:

```text
One thing can occupy prerequisite, provider, import, blocker, or support role.
```

Operation reading:

```text
Static analysis, interpretation, planning, or promotion may discover dependency.
```

Relationship reading:

```text
A depends-on B under dependency kind K and scope S.
```

Falsifying finding: dependency kinds differ. Import dependency, runtime call
dependency, policy prerequisite, evidentiary dependency, and inquiry-blocking
dependency are not one relationship kind. `Depends-on` is relationship pressure,
but it does not prove a uniform relation family.

### Trusts

`Trusts` is related to source authority, evidence quality, operator boundaries,
and promotion decisions, but it is not simply source authority.

Object reading:

```text
A trust policy, trust assessment, source record, or authority record can be an
object.
```

Role reading:

```text
A source can occupy trusted-source role for a limited context.
```

Operation reading:

```text
Review, validation, policy evaluation, or promotion may assess trust.
```

Relationship reading:

```text
Evaluator E trusts Source S for Claim Domain D under Policy P and Scope K.
```

Falsifying finding: trust can be normative, contextual, and policy-derived. It
may be closer to authority or confidence state than a simple connection. The
repository boundary is that trust must not erase provenance, caveats, or source
limitations.

### Authorizes

Critical authority example:

```text
Operator may adopt Capability C
```

`Authorizes` has especially strong relationship pressure, but it also strains a
simple relationship reading.

Object reading:

```text
A policy, approval, authority record, grant, or decision can be represented.
```

Role reading:

```text
The operator occupies authorized actor or authorized adopter role.
```

Operation reading:

```text
Approve, grant, revoke, adopt, execute, or check authority are operations.
```

Relationship reading:

```text
Authority Source A authorizes Operator O to adopt Capability C under Scope S.
```

State or constraint reading:

```text
O is currently permitted to perform adoption of C if policy and boundary
conditions hold.
```

Falsifying finding: authority is not just an edge. It is normative, scoped,
conditional, and often policy-derived. A relationship may represent the permission
connection, but role, object, operation, state, and constraint language all remain
necessary.

### Adopts

`Adopts` sits between authority and operation.

Object reading:

```text
An adoption decision or adoption record can persist.
```

Role reading:

```text
An operator can occupy adopting actor role; a capability can occupy adopted
capability role.
```

Operation reading:

```text
Adoption is something that happens.
```

Relationship reading:

```text
Operator O has adopted Capability C for Scope S.
```

Falsifying finding: `adopts` may primarily be an event or operation whose result
is a changed state or relationship. If the repository needs to know that adoption
occurred, the event matters. If it needs to know the current capability posture,
the resulting relationship or state matters. Relationship alone may be
insufficient.

### Recommends

`Recommends` links assessment, goal relevance, operator authority, decision, and
response boundaries.

Object reading:

```text
A recommendation is a represented object with support, caveats, and scope.
```

Role reading:

```text
A claim or action can occupy recommended option role.
```

Operation reading:

```text
Recommendation generation, ranking, selection, and communication are operations.
```

Relationship reading:

```text
Seed recommends Action A to Operator O for Goal G under Evidence E and Caveats C.
```

Falsifying finding: recommendation is not decision and is not authority. The
relationship reading captures directedness, but recommendation also has object
behavior as a preserved communicable artifact and operation behavior in how it is
generated.

---

## Critical Examples Revisited

### Example 1: Support

```text
Observation O supports Claim C
```

What is the support?

Current finding:

```text
The support is best read as a represented directed connection between O and C,
while recognizing that support records, support explanations, and support views
can be objects representing that connection.
```

Relationship is stronger than object, role, or operation here because the target
and edge kind are essential. But support remains overloaded, so this is not a
universal relationship primitive.

### Example 2: Contradiction

```text
Claim A contradicts Claim B
```

What persists?

Current finding:

```text
The claims may persist as objects. A contradiction record may persist as an
object. The contradiction itself appears to be incompatibility pressure between
claims under scope.
```

The relationship can be supported, challenged, revised, or dissolved. If scope
clarification removes incompatibility, the perceived relation may not persist.

### Example 3: Identity

```text
Host A same-as Host B
```

Is identity fundamentally relational?

Current finding:

```text
Same-as identity is strongly relational because it asserts how two represented
entities relate. But identity in the repository also includes entity objects,
identifier values, source-scoped aliases, derivation operations, and projection
choices.
```

Identity cannot be reduced to relation alone, but relation errors are central to
identity failures.

### Example 4: Authority

```text
Operator may adopt Capability C
```

Is authority a relationship, role, or constraint?

Current finding:

```text
Authority includes a permission relation among operator, action, capability,
policy, source, and scope; an authorized role for the actor; constraints on the
operation; and possibly a policy-derived state.
```

Authority is one of the strongest falsifying examples for a simple relationship
model.

### Example 5: Runtime Topology

```text
Service S runs-on Host H
```

What kind of thing is `runs-on`?

Current finding:

```text
Runs-on is a scoped runtime-topology relation that may be stateful, temporal,
source-relative, and identity-sensitive.
```

It is relationship-like, but its persistence depends on observed runtime state
and entity boundaries.

---

## Relationship Versus Object

Object-like evidence:

1. Relationship facts and relationship claims can be preserved.
2. A relationship record can carry evidence, source, scope, confidence, status,
   contradiction, freshness, and projection visibility.
3. Relationship records can be cited, reviewed, challenged, revised, promoted,
   demoted, superseded, or excluded.

Relationship-like evidence:

1. The architectural work is often done by the connection, not by an endpoint.
2. Role labels lose target, direction, kind, and scope.
3. Operation labels lose what persists after discovery, promotion, or evaluation.

Tension:

```text
A relationship may be represented by an object-like claim record, but the reason
that record matters is edge semantics.
```

Therefore, `relationship as object` is partially valid but incomplete. It
explains persistence and citation, but it risks hiding connection, direction,
scope, arity, and conditionality.

Current finding:

```text
Relationships can persist as represented claims, but their object-like record is
not the same as the relationship semantics it records.
```

---

## Relationship Versus Role

Role explains participation:

```text
Observation O is supporting evidence.
Operator O is authorized adopter.
Host H is execution substrate.
Source S is trusted source.
```

Relationship explains connection:

```text
O supports Claim C.
Policy P authorizes Operator O to adopt Capability C.
Service S runs-on Host H.
Evaluator E trusts Source S for Domain D.
```

Role language is useful but endpoint-local. It often describes one participant's
position inside a relationship. Relationship language preserves the edge.

Candidate rule of thumb:

```text
If the question is "how is this participant functioning here?", role language may
be primary.

If the question is "what is connected to what, under what kind and scope?",
relationship language is primary.
```

Falsifying concern:

Some role assignments are themselves relational or episodic:

```text
Claim C is selected for Response R.
Question Q is target of Inquiry I.
Finding F is active in Working State W.
```

Those should not automatically become durable relationships. Role and
relationship overlap at participation boundaries.

---

## Relationship Versus Operation

Operation explains what happens:

```text
observe
compare
derive
promote
corroborate
adopt
authorize
recommend
project
revise
```

Relationship explains what connection is represented before, during, or after an
operation:

```text
Observation O supports Claim C.
Claim A contradicts Claim B.
Host A same-as Host B.
Operator O has adopted Capability C.
```

An operation can create, discover, derive, validate, revise, promote, project,
consume, or dissolve a relationship. The operation and the represented
relationship are not the same.

Falsifying concern:

Some verbs name operations more strongly than relationships. `Adopts` may name an
event or action; the durable result may be an adopted-capability state or
operator-capability relation. `Authorizes` may name a granting act; the durable
result may be a permission relation or policy state.

Current finding:

```text
Relationship is often the result or target of operations, but some candidate
relationship terms remain operation-first or state-first.
```

---

## Relationship Persistence

The persistence frontier found that relationship persistence appears unavoidable
because some survivors are edges, not object cores.

What might it mean for a relationship to persist?

```text
A represented connection remains recognizable across changes in support, scope,
confidence, endpoint descriptions, projection visibility, or inquiry context.
```

Examples:

```text
Claim A continues to support Claim B after new evidence changes support strength.
Module M continues to depend-on Module N after the import path is refactored.
Source S remains authoritative-for Domain D after projection visibility changes.
```

What can change?

```text
support material
confidence
freshness
scope
source attribution
projection visibility
endpoint labels
contradiction status
active role in a response or handoff
```

What would falsify persistence?

```text
The edge kind changed.
The endpoint identity changed beyond recognition.
The scope changed so the old relation no longer applies.
The relation was only an episodic participation assignment.
The relation was an interpretation error corrected by later evidence.
```

Current finding:

```text
Relationship persistence is not storage of an edge record alone. It is
recognizable survival of the represented connection under bounded change.
```

---

## Relationship Continuity

The continuity frontier found that continuity may survive change and that
relationship continuity may be central for support, contradiction, authority,
dependency, and working-state usefulness.

Can relationships exhibit continuity?

Current finding:

```text
Yes, but relationship continuity is not yet settled. It appears when a connection
or connection-pressure survives revision without requiring strict sameness of an
edge record.
```

Examples:

```text
A support relation weakens but remains support.
A contradiction narrows from broad claim conflict to scoped incompatibility.
A dependency moves from direct import to mediated dependency while the blocker
pressure remains.
An authority grant changes source but preserves the permitted action under a new
policy basis.
```

What survives?

Possible survivors include:

```text
edge kind
connection pressure
constraint
support direction
dependency need
permission boundary
incompatibility pressure
working-state usefulness
```

Falsifying findings:

1. Similar endpoints do not prove continuity.
2. Similar wording does not prove the same relationship continued.
3. Recorded lineage does not prove continuity if the connection pressure changed.
4. A revised relation may replace, not continue, the earlier relation.
5. Recognition can become subjective storytelling without preserved evidence,
   scope, support, or authority boundaries.

Current finding:

```text
Relationship continuity may be a judgment over relationship persistence,
lineage, support evolution, and endpoint continuity. It is not implementation-ready.
```

---

## Relationship Lineage

Can relationships evolve?

The repository evidence suggests they can, but `evolve` is ambiguous.

Possible lineage patterns:

| Pattern | Example | Caution |
| --- | --- | --- |
| Strength change | weak support becomes strong support | Same edge kind may persist, but support state changes. |
| Scope refinement | broad contradiction narrows to scoped contradiction | The original relation may be replaced rather than continued. |
| Endpoint reidentification | endpoint relation becomes host relation after stronger evidence | Risk of identity over-promotion. |
| Kind correction | belongs-to becomes runs-on | Earlier relation may have been wrong. |
| Permission transition | may-adopt becomes adopted | Operation/event/state distinction matters. |
| Evidence reversal | support becomes contradiction | This may be lineage of inquiry, not continuity of the same relationship. |

Can support become contradiction?

Current finding:

```text
A represented support relation should not simply mutate into contradiction as if
the same relation changed polarity. More likely, later work discovers a new
contradiction relation, demotes or rejects the support relation, and preserves a
lineage of interpretation or revision.
```

Can authority relationships change?

Current finding:

```text
Yes. Authority may be granted, revoked, narrowed, delegated, superseded, or
conditioned. But that change may be operation history plus permission state, not
simple relationship continuity.
```

Relationship lineage therefore appears important, but implementation remains
premature because the repository has not reconciled relationship identity,
relationship persistence, or relationship continuity.

---

## Strongest Relationship Findings

1. Relationship pressure is real and recurrent across support, contradiction,
   corroboration, identity, authority, dependency, runtime topology, trust,
   adoption, and recommendation.
2. The strongest relationship-shaped pattern is a scoped connection among
   represented terms with direction, kind, support, confidence, source, and
   possible contradiction.
3. Relationship cannot be reduced to endpoint role because target, edge kind,
   direction, and scope matter.
4. Relationship cannot be reduced to operation because operations may produce,
   discover, change, or consume a relation while the represented connection
   remains available for review.
5. Relationship can be object-like when preserved as a claim or fact record, but
   the record's objecthood does not exhaust the edge semantics.
6. Support, identity, authority, and dependency are the strongest pressure cases.
7. Relationship persistence appears unavoidable for some represented edges.
8. Relationship continuity appears possible but remains less settled than
   relationship persistence.
9. Implementation is premature because candidate relationships are heterogeneous:
   durable claims, episodic participation edges, conditional permissions,
   temporal topology states, operation results, and projection-relative
   associations are not one thing.

---

## Strongest Falsifying Findings

The strongest falsifications of a simple relationship ontology are:

```text
Some relationship candidates are better understood as operations.
Some are better understood as states or constraints.
Some are endpoint roles plus context rather than durable edges.
Some are projection-relative or episode-relative.
Some are records that represent relationships, not relationships themselves.
Some are ternary, scoped, conditional, temporal, or policy-derived rather than
simple binary edges.
Some apparent relationships disappear when identity, source, or scope is
corrected.
```

Specific falsifiers:

1. `Adopts` may be operation-first.
2. `Authorizes` may be permission-state and constraint-heavy.
3. `Runs-on` may be temporal state rather than durable topology.
4. `Belongs-to` is overloaded across containment, ownership, membership,
   projection grouping, and topology.
5. `Same-as` may be a claim object representing equality rather than proof that
   relationship is primitive.
6. `Corroborates` may require a target and scope, making simple binary relation
   language too weak.
7. `Trusts` may reflect policy and authority rather than a plain connection.

These falsifiers do not remove relationship pressure. They show that
relationship is not yet understood well enough to be reconciled or implemented.

---

## Required Tensions Preserved

| Tension | Current frontier finding |
| --- | --- |
| Relationship vs object | Relationship records can be objects, but connection semantics are doing distinct work. |
| Relationship vs role | Roles describe participant function; relationships preserve edge, target, direction, kind, and scope. |
| Relationship vs operation | Operations discover, create, revise, or consume relations; relationships may persist after operations. |
| Support vs relationship | Support is strongest as directed relationship, but support records, roles, views, and operations also exist. |
| Evidence vs relationship | Evidence can be object-like preserved material and role-like support participant; evidence-for requires a relation. |
| Identity vs relationship | Same-as, identifies, belongs-to, and runs-on are relationship-shaped, but identity also includes entity objects, identifiers, derivation, and projection choices. |
| Authority vs relationship | Authority includes permission relations, authorized roles, policy constraints, operations, and state. |
| Relationship persistence | Some edges persist through support, scope, confidence, and projection changes; episodic edges may not. |
| Relationship continuity | Some connection pressure may survive revision, but continuity is not proven by wording, records, or endpoint resemblance. |
| Relationship lineage | Relationships may be revised, superseded, demoted, or replaced; support becoming contradiction is probably revision lineage, not same-edge continuity. |

---

## Evaluation Of The Working Hypothesis

Hypothesis:

```text
Objects explain represented things.
Roles explain participation.
Operations explain what happens.
Relationships explain connection.
```

Repository evidence supports the hypothesis as an exploratory distinction.

It explains why:

```text
Claim C
Claim C selected for response
Promotion of Claim C
Evidence E supports Claim C
```

are not the same kind of statement.

It also explains why support, identity, authority, and dependency repeatedly
escaped object / role / operation-only classifications.

However, repository evidence does not support promoting the hypothesis to
canonical ontology. Relationship candidates are heterogeneous and often require
state, condition, temporality, source scope, confidence, authority, projection,
and operation history.

Current assessment:

```text
Relationship is a necessary explanatory pressure signal.
Relationship is not yet a reconciled top-level category.
Implementation remains premature.
```

---

## Non-Goals

This document does not:

- reconcile relationship ontology;
- redefine foundational ontology;
- replace relationship fact or relationship promotion reconciliations;
- define relationship schemas, identifiers, graph models, storage, query models,
  projections, engines, or runtimes;
- define canonical relationship kinds;
- define authority, identity, trust, support, corroboration, contradiction, or
  topology implementation rules;
- modify repository code, tests, runtime behavior, projections, generated
  artifacts, or acquisition paths;
- treat relationship as a primitive;
- decide whether relationship is a fourth top-level category;
- decide whether every relationship is an object;
- make relationship persistence, continuity, or lineage implementation-ready.

---

## Conclusion

A relationship might be a represented connection among terms, carrying kind,
direction, scope, support, confidence, source, authority limits, and possible
state or temporal conditions.

That is not the whole story. Some relationship candidates are records, roles,
operations, states, constraints, projection choices, or interpretation results.
The repository evidence therefore supports relationship as a pressure signal, not
as a reconciled primitive.

Relationship became a pressure signal because recent investigations repeatedly
needed to explain connections that were not safely reducible to objects, roles,
or operations:

```text
support
contradiction
corroboration
identity
authority
dependency
runtime topology
trust
adoption
recommendation
```

The strongest current distinction is:

```text
object = represented thing
role = contextual participation
operation = happening or transformation
relationship = represented connection or connection-pressure
```

But the distinction remains exploratory. Relationship persistence and continuity
appear unavoidable in some cases, especially support, contradiction, authority,
dependency, and working-state usefulness. Relationship lineage also appears
important, but it may often be revision history rather than same-edge survival.

Implementation remains premature because Seed has not reconciled whether
relationship is a special object subtype, a fourth category, a stateful/temporal
claim family, a compound of claim plus support plus scope, or something else.
