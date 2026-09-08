---
doc_type: pressure_test
status: exploratory
scope: documentation_only
domain: object role operation ontology
defines:
  - object role operation pressure test
  - evidence pressure test
  - support pressure test
  - authority pressure test
  - identity pressure test
  - frontier pressure test
  - working state pressure test
  - relationship pressure test
depends_on:
  - object_role_and_operation_frontier.md
  - object_role_operation_consistency_audit.md
  - foundational_ontology_reconciliation.md
  - knowledge_representation_reconciliation.md
  - relationship_promotion_reconciliation.md
  - corroboration_and_fact_promotion_reconciliation.md
  - evidence_trust_and_source_authority_reconciliation.md
  - entity_identity_derivation_reconciliation.md
  - inquiry_frontier.md
  - handoff_and_continuation_lineage_frontier.md
  - architectural_status_and_next_frontier.md
---

# Object, Role, and Operation Pressure Test

## Purpose

This document is a documentation-only architectural pressure test of a possible
organizing lens:

```text
Objects persist.
Roles describe participation.
Operations describe what happens.
```

It does not reconcile the ontology. It does not introduce canonical categories,
new schema, runtime behavior, tests, implementation direction, or a new modeling
system.

Repository authority wins over this document. The referenced reconciliations,
frontiers, and audits remain authoritative for their settled boundaries. This
pressure test only asks whether difficult concepts can be reasonably explained
through the object / role / operation lens or whether some other category appears
necessary.

The document deliberately attempts to falsify the lens. A finding that the lens
breaks is a useful result.

## Method

For each selected concept, this document evaluates:

1. object interpretation;
2. role interpretation;
3. operation interpretation;
4. relationship interpretation where necessary;
5. where the model succeeds;
6. where the model fails;
7. whether the concept appears overloaded.

The selected concepts are:

```text
evidence
support
authority
identity
frontier
working state
```

They were selected because repository usage repeatedly places them near category
boundaries and because each can cross between preserved knowledge, participation,
activity, and connection language.

## Baseline Under Pressure

The object / role / operation lens is attractive because it explains several
patterns already visible in the repository:

```text
claim persists
selected claim participates in a response
selection happens
```

```text
question persists
active question participates in working state
inquiry pursues it
```

```text
evidence persists
that evidence supports a claim
promotion or projection uses it
```

The pressure begins when the middle line in these examples is not clearly a role
and not clearly an operation. Many of the repository's most important verbs look
like durable represented edges:

```text
supports
contradicts
corroborates
identifies
belongs_to
runs_on
depends_on
```

If those are not objects, roles, or operations, then the lens may be missing a
relationship layer. This document treats that as the main falsification
candidate.

---

## Concept 1: Evidence

### Object Interpretation

Evidence has strong object behavior.

The foundational ontology describes evidence as preserved provenance and support
material. The evidence, trust, and source-authority reconciliation treats
evidence as something retained with source, payload, time, and context so later
participants can audit, explain, review contradiction, and reinterpret.

Under the object lens, evidence is a persisted represented thing:

```text
Observation O is preserved as evidence E.
Evidence E remains available after the acquisition event ends.
Evidence E can later be cited, challenged, reinterpreted, or excluded from a
particular projection without ceasing to exist.
```

This interpretation works well when evidence means preserved material:

```text
source payload
observation record
supporting artifact
measurement sample
operator statement
imported record
```

### Role Interpretation

Evidence also has role-like behavior.

An object can act as evidence for another object without changing its own stable
identity:

```text
Claim A
    acts as evidence for Claim B
```

In that example, Claim A does not stop being a claim. It participates in an
evidentiary position relative to Claim B. The phrase `acts as evidence for`
sounds less like a new object and more like a role occupied by Claim A in a
support context.

This role interpretation becomes especially strong when the same object can play
different roles in different episodes:

```text
Claim A supports Claim B in one inquiry.
Claim A is contradicted by Claim C in another inquiry.
Claim A is selected as handoff content in a continuation.
```

The object remains a claim; the evidentiary function is contextual.

### Operation Interpretation

Evidence is weak as an operation.

Operations can create, acquire, preserve, evaluate, select, promote, or project
evidence, but evidence itself is not what happens. Treating evidence as an
operation collapses provenance into acquisition or evaluation.

Possible operations around evidence include:

```text
observe
preserve
link
support
corroborate
promote
project
reinterpret
```

The operation lens is useful around evidence, not as evidence.

### Relationship Interpretation

The relationship interpretation is necessary in the critical examples:

```text
Observation O
    supports Claim C
```

```text
Claim A
    acts as evidence for Claim B
```

These are not exactly the same meaning of evidence.

In the first example, an observation is preserved as source-attributed material
that supports a claim. Evidence has a strong object core: it is the retained
provenance explaining why Seed may consider Claim C.

In the second example, Claim A is already a claim. Its use as evidence for Claim
B is a relative support relation. Calling Claim A `evidence` risks hiding that it
remains a claim and that its evidentiary force depends on the relationship to
Claim B.

The strongest formulation under pressure is:

```text
evidence-as-material = object-like
evidence-for = relationship / role-like participation
using evidence = operation-adjacent
```

### Where the Lens Succeeds

The lens successfully protects preserved evidence from being reduced to the act
of observing or projecting. It also explains why a claim can occupy an
evidentiary role without becoming a different object kind.

### Where the Lens Fails

The lens struggles because `evidence for` has relational force. Object / role /
operation can say that Claim A occupies an evidence role, but it does not fully
represent the directed support edge from Claim A to Claim B.

### Overload Finding

Evidence is overloaded.

It means at least:

```text
preserved provenance object
support material
relative evidentiary role
source of a support relationship
possible input to promotion or projection operations
```

This does not falsify the object / role / operation lens by itself, but it does
expose relationship as a likely missing category.

---

## Concept 2: Support

### Object Interpretation

Support is weak as a standalone object.

Repository language sometimes names support records, fact support, claim
support, support groups, and support-aware views. Those can be represented
objects or projection artifacts. However, the general concept `support` does not
behave like a stable domain object in the same way that observation, evidence,
claim, fact, relationship, or recommendation does.

When support is object-like, it is usually a record of a connection:

```text
support record
support group
support explanation
support view
```

That suggests the object is a representation of support, not support itself.

### Role Interpretation

Support has some role behavior.

An observation, evidence item, fact, or claim can occupy a supporting position:

```text
Observation O supports Claim C.
Claim A supports Claim B.
Fact F supports Claim C.
```

The supporting item remains what it was. Its support function is relative to the
supported item.

Role language helps avoid promoting every supporting object into a new type.

### Operation Interpretation

Support is also weak as an operation if treated as the durable result.

There are support-related operations:

```text
link evidence to fact
assess support strength
promote evidence-backed claim
select support for explanation
project support-aware view
```

But `supports` in repository examples often describes a standing relation, not
only the act of creating that relation.

### Relationship Interpretation

Support is strongest as a relationship.

The knowledge representation reconciliation explicitly distinguishes evidence
support and claim justification support and notes that support relationships may
be represented as specialized relationship types in future work. The examples
also behave relationally:

```text
Observation O supports Claim C
Claim A supports Claim B
Evidence E supports Fact F
Fact F supports Claim C
```

Each example has a directed shape:

```text
supporter -> supported
```

The relation may carry scope, strength, source, freshness, contradiction state,
and promotion eligibility. Those properties are hard to express if support is
only a role assigned to the supporter.

### Where the Lens Succeeds

The lens succeeds by separating supporting objects from support-related
operations. It prevents `support` from swallowing observation, evidence, fact,
claim, promotion, confidence, and truth.

### Where the Lens Fails

The lens fails if it has no place for a durable directed edge. `Supporter has
support role` does not fully answer:

```text
supporting what?
under what scope?
with what strength?
through what evidence?
against what contradictions?
```

Those questions are relational.

### Overload Finding

Support is overloaded.

It can mean:

```text
a relationship between represented things
a role occupied by supporting material
a record representing that relationship
a projection of support state
a family of operations that evaluate or expose support
```

Support is one of the strongest falsifying cases against an object / role /
operation-only lens.

---

## Concept 3: Authority

### Object Interpretation

Authority has object-like pressure because the foundational ontology names it as
scoped power to decide, approve, request, execute, override, or communicate. The
repository also needs to preserve policy, operator, source, capability, command,
and execution boundaries.

Authority may be represented as something that exists in a scope:

```text
operator authority
source authority
execution authority
adoption authority
communication authority
```

A preserved authority record, policy grant, approval, or decision can behave as
an object.

### Role Interpretation

Authority also behaves like a participation role.

Examples:

```text
Operator may adopt capability.
Operator may execute action.
```

In these cases, the operator participates as an authorized actor for a particular
transition. The operator is the object. `Authorized adopter` or `authorized
executor` is a role occupied in a scoped workflow.

Authority role language helps prevent the repository from treating every
operator, source, provider, or tool as globally authoritative.

### Operation Interpretation

Authority is not itself the operation.

Authority constrains operations such as:

```text
adopt capability
approve command
execute action
override decision
communicate recommendation
promote claim
```

Authority may be checked, granted, revoked, delegated, asserted, or consumed by
an operation, but it should not be collapsed into those operations.

### Relationship Interpretation

Authority is strongly relational.

The examples have a structure that is difficult to express as object or role
alone:

```text
operator -> may_adopt -> capability
operator -> may_execute -> action or command
source -> authoritative_for -> claim domain
policy -> permits/prohibits -> behavior
```

Authority asks who or what may make a transition in a scope. That is a relation
among actor, permitted action, object of action, policy, scope, and sometimes
workflow state.

### Something Else: Permission State

Authority may also be a state-like normative condition.

`Operator may execute action` is not just a relationship between operator and
action. It may depend on current policy, approval, time, environment, prior
verification, capability support, and command boundaries. A permission can be
valid, expired, conditional, overridden, or absent.

This suggests authority may require at least:

```text
object: operator, policy, command, capability, action
role: authorized actor, approving source, adopting operator
operation: approve, adopt, execute, revoke
relationship: may_execute, authoritative_for, permitted_by
state: currently permitted under scope
```

### Where the Lens Succeeds

The lens helps distinguish operator objects from authorized roles and from
operations that consume authority. It also preserves the repository's warning
that projection is not authority and recommendation is not decision.

### Where the Lens Fails

The lens becomes strained because authority is normative and scoped. A role can
say an operator is authorized, but it does not by itself encode the permitted
transition, target, condition, source of permission, or durability of the grant.

### Overload Finding

Authority is overloaded.

It can mean:

```text
scoped power
permission relation
authorized participation role
policy-derived state
approval or decision object
constraint on operations
source entitlement for declarations
```

Authority does not fit cleanly into any single object / role / operation bucket.
Relationship and state both appear necessary to describe it precisely.

---

## Concept 4: Identity

### Object Interpretation

Identity can appear object-like when the repository preserves identity records,
entity records, aliases, endpoint records, host records, or normalized entity
projections.

However, identity itself is risky as an object. Treating identity as a thing can
hide whether the repository means:

```text
an entity
a name
an alias
a claim of sameness
a derivation result
a membership or containment relationship
a projection-selected canonical representative
```

The entity identity derivation reconciliation warns against collapsing endpoint
identity into host identity and against over-promoting weak evidence into
stronger identity claims.

### Role Interpretation

Identity has limited role behavior.

An endpoint may participate as an alias candidate, host identifier, scrape
target, or evidence source. A name may participate as a canonical label in a
projection. But identity is not primarily explained by role language.

Role helps for cases like:

```text
Endpoint A acts as identifier for Host B in this source.
Name N acts as display label in this projection.
```

It does not fully explain equality or belonging.

### Operation Interpretation

Identity can be an operation result.

Identity derivation, matching, normalization, alias resolution, deduplication,
and promotion can produce identity claims:

```text
derive that Host A == Host B
infer that Endpoint A belongs to Host B
select canonical entity representative
```

The operation lens is useful for describing how an identity assertion came to be.
It is not enough to describe the assertion after it is preserved.

### Relationship Interpretation

Identity is strongest as a relationship or claim family.

Examples:

```text
Host A == Host B
Endpoint A belongs to Host B
Alias A identifies Entity B
Service S runs_on Host H
```

These are directed or symmetric relations with evidence, scope, and confidence.
Equality is not the same as containment. Identification is not the same as
ownership. Belonging is not the same as running on.

The relationship layer is critical because identity errors are often category
errors in the edge:

```text
endpoint observed at host address
    != endpoint is host

alias string matched host label
    != alias is authoritative identity

service observed through endpoint
    != service belongs to host globally
```

### Where the Lens Succeeds

The lens helps distinguish entities as objects from matching or derivation as
operations. It also explains that an endpoint can participate in an identifying
role without becoming the host.

### Where the Lens Fails

The lens cannot safely represent sameness, belonging, identifying, or running-on
without relationships. Identity is not merely a role of one object; it is a claim
about how objects relate.

### Overload Finding

Identity is overloaded.

It can mean:

```text
entity object
identifier value
alias role
same-as relationship
belongs-to relationship
identity claim
operation result of derivation or normalization
projection choice
```

Identity strongly falsifies a three-category-only lens unless relationship claims
are already counted as objects. Even then, the relationship form deserves explicit
attention.

---

## Concept 5: Frontier

### Object Interpretation

Frontier has real object behavior.

Repository frontiers are documents. They preserve unresolved investigation
boundaries, questions, tensions, candidate distinctions, and next-safe-work
signals. A future participant can cite a frontier, hand it off, revisit it,
supersede it, or reconcile it.

Under this interpretation, a frontier is a preservation object:

```text
an artifact that preserves an unresolved architectural edge
```

This object interpretation is especially strong for named frontiers:

```text
Inquiry Frontier
Selection Frontier
Attention Frontier
Object, Role, and Operation Frontier
```

### Role Interpretation

Frontier also behaves like a participation condition.

An object can be at the frontier of inquiry without being the frontier document:

```text
question at the inquiry frontier
tension at the selection frontier
relationship vocabulary at the attention frontier
```

Here, `frontier` indicates current boundary participation. The question, tension,
or relationship is active at the edge of unresolved work.

This role reading aligns with working-state and handoff documents that treat
frontiers as part of the selected active edge rather than as all preserved
knowledge.

### Operation Interpretation

Frontier is weak as an operation.

There are operations around frontiers:

```text
investigate frontier
preserve frontier
advance frontier
reopen frontier
reconcile frontier
handoff frontier
```

But the frontier itself is not the operation. It is the boundary or artifact
around which operations occur.

### Relationship Interpretation

Frontier may require relationships among unresolved objects:

```text
frontier contains question
frontier preserves tension
frontier depends_on reconciliation
frontier blocks implementation
frontier is superseded_by reconciliation
```

A frontier is not only a pile of objects. It often preserves why those objects
matter together and how they relate to settled authority, unsafe moves, and next
inquiry paths.

### Collection / Preservation Structure Interpretation

Frontier may be a collection or preservation structure rather than a simple
object.

The object lens says it persists. That is true of the document. But the
architectural meaning of frontier may be a structured unresolved boundary:

```text
selected unresolved questions
active tensions
settled constraints
unsafe promotions
candidate next moves
links to authority
```

That looks more like a preservation structure than a single atomic object.

### Where the Lens Succeeds

The lens explains why a frontier document can persist and why individual objects
can occupy frontier-content or inquiry-target roles.

### Where the Lens Fails

The lens strains when frontier means current boundary condition rather than
artifact. `Frontier as object` misses the participation aspect. `Frontier as
role` misses the preservation artifact and collection structure.

### Overload Finding

Frontier is overloaded.

It can mean:

```text
document artifact
unresolved investigation boundary
collection of questions and tensions
active edge of work
role-like condition occupied by objects
handoff content
preservation structure
```

Frontier does not break the lens completely, but it resists a clean single
classification.

---

## Concept 6: Working State

### Object Interpretation

Working state has object-like behavior when preserved in handoffs or
continuation artifacts. It can be referred to, transferred, consumed, updated,
and used to resume work.

Examples of preserved working-state content include:

```text
active questions
active tensions
active findings
selection rationale
next safe move
known unsafe move
validation status
```

A preserved working-state artifact can be an object.

### Role Interpretation

Working state strongly involves roles.

The objects inside working state do not become new object kinds merely because
they are active:

```text
question -> active question
finding -> active finding
tension -> active tension
reconciliation -> settled anchor
frontier -> active edge
```

`Working-state content` is a participation role assigned by selection and
activation.

### Operation Interpretation

Working state is closely tied to operations but is not reducible to them.

Operations around working state include:

```text
select
activate
preserve
handoff
consume
validate
resume
update
```

An operation can produce or modify working state, and continuation can consume
it. But working state is the current work-position preserved or made active, not
only the operation that produced it.

### Relationship Interpretation

Working state needs relationships because its value depends on how selected
items relate:

```text
finding supports next move
tension blocks reconciliation
question depends_on unresolved evidence
frontier references settled authority
handoff preserves working state
selection rationale explains active subset
```

Without relationships, a working state becomes a list. Successful continuation
requires more than a list; it needs the reason those items are active together.

### Collection / Context Interpretation

Working state may be a bounded context or collection rather than a simple object.

The handoff and continuation lineage frontier characterizes working state as a
current work-position that helps future participants avoid rediscovery. That
position includes active context, selection rationale, unresolved tensions, and
validation state. Those are not all the same kind of thing.

### Where the Lens Succeeds

The lens explains that working-state content is role-like and that preservation
or activation are operations. It prevents active questions, findings, and
tensions from becoming new object types solely because they are active.

### Where the Lens Fails

The lens struggles with working state as a compound context. It is persistent
enough to be object-like, role-heavy in its contents, operation-dependent in its
creation and consumption, and relationship-dependent in its usefulness.

### Overload Finding

Working state is overloaded.

It can mean:

```text
preserved artifact
current work-position
active context
collection of selected objects
role assignment over existing objects
operation context for continuation
relationship-bearing structure
```

Working state does not fit cleanly into object, role, or operation alone.

---

## Relationship Pressure Test

The object / role / operation lens currently lacks an explicit relationship
category. This section asks whether repository examples behave as relationships
rather than objects, roles, or operations.

### Candidate Relationship Terms

```text
supports
contradicts
corroborates
identifies
belongs_to
runs_on
depends_on
```

### Object Interpretation

Relationships can be represented as objects in a claim-centered ontology. The
foundational ontology names relationship as a normalized connection claim between
things. Relationship records can persist, carry support, be contradicted,
projected, and cited.

This means a repository could technically preserve the three-category lens by
saying:

```text
relationship record = object
```

That move is partially valid.

### Role Interpretation

Relationships are not well explained as roles.

A role describes participation by one object in a context. A relationship
connects at least two terms and often carries direction, kind, scope, support,
and durability.

For example:

```text
Observation O supports Claim C
```

Calling O `supporting` is useful, but it omits Claim C unless the relationship is
also represented. Role language describes one endpoint's participation; it does
not fully encode the edge.

### Operation Interpretation

Relationships are not simply operations.

An operation may create, discover, derive, promote, validate, or project a
relationship. But after that, the repository often needs the connection claim to
persist:

```text
Endpoint A belongs_to Host B
Service S runs_on Host H
Claim A contradicts Claim B
Evidence E corroborates Evidence F for Claim C
Module M depends_on Module N
```

The operation is how the relation was produced or used. The relation is what is
represented.

### Relationship Durability

Relationship durability is the hardest pressure point.

Some relationships are durable represented claims:

```text
Host A == Host B
Service S runs_on Host H
Module M depends_on Module N
```

Some relationships are episodic or projection-relative:

```text
Claim A is selected for this response
Finding F is active in this working state
Question Q is target of this inquiry
```

Some are stateful or conditional:

```text
Operator may execute Action X under Policy P during Scope S
Source S is authoritative_for Claim Domain D in Workflow W
```

The repository therefore appears to need distinctions among:

```text
durable relationship claim
episodic participation relation
conditional permission relation
operation-produced relationship
projection-selected relationship
```

The object / role / operation lens helps notice these differences but does not
fully classify them.

### Relationship vs Role

The tension is:

```text
role = how an object participates
relationship = how objects are connected
```

Role may be derivable from relationship in some cases:

```text
O supports C
therefore O occupies supporting-evidence role relative to C
```

But relationship is not reducible to role because the edge, target, kind, and
scope matter.

### Relationship vs Operation

The tension is:

```text
operation = what happens
relationship = what connection is represented before or after something happens
```

Operation can produce a relationship:

```text
identity derivation produces Host A == Host B
comparison produces Claim A contradicts Claim B
analysis produces Module M depends_on Module N
```

But once represented, the relationship can persist as a claim with evidence and
support. It should not be collapsed into the generating operation.

### Does The Repository Already Rely On A Relationship Layer?

Yes, descriptively.

The repository already relies on relationship language for support, identity,
dependency, authority, containment, execution, corroboration, contradiction,
lineage, and navigation. The foundational ontology already names relationships
as knowledge concepts. Several frontiers and reconciliations become hard to read
without relationship semantics.

This does not mean a new canonical category should be introduced here. It means
the pressure test finds that an object / role / operation-only lens is
insufficient unless `relationship` is explicitly handled as either:

```text
a special kind of object with edge semantics
```

or:

```text
a fourth modeling category
```

This document does not decide between those options.

---

## Cross-Concept Findings

### Where The Lens Is Strongest

The lens is strongest when a concept cleanly separates into:

```text
durable represented thing
contextual participation
activity that creates, selects, changes, or consumes represented things
```

Strong examples:

```text
claim persists
claim selected for response is role-like
selection is operation
```

```text
question persists
question as inquiry target is role-like
inquiry is operation-like
```

```text
evidence object persists
claim acting as evidence is role-like
promotion or projection is operation-like
```

### Where The Lens Becomes Strained

The lens becomes strained when the concept is directed, scoped, conditional, or
edge-like:

```text
Observation O supports Claim C
Claim A contradicts Claim B
Host A == Host B
Endpoint A belongs_to Host B
Operator may execute Action X
Module M depends_on Module N
```

These are not naturally objects, roles, or operations unless relationships are
absorbed into objects. Absorption may be possible, but it hides the fact that
edge semantics are doing the architectural work.

### Where Concepts Become Overloaded

All six pressure-tested concepts show overload:

| Concept | Overload pattern |
| --- | --- |
| Evidence | Preserved material, evidentiary role, support source, operation input. |
| Support | Relationship, role, support record, support view, support-evaluation operation. |
| Authority | Permission relation, scoped power, authorized role, policy state, operation constraint. |
| Identity | Entity object, identifier, alias role, equality relation, containment relation, derivation result. |
| Frontier | Document, unresolved boundary, collection, active edge, role-like condition, preservation structure. |
| Working state | Artifact, current work-position, active context, selected collection, operation context. |

Overload does not mean the repository is wrong. It means future work must avoid
promoting a term without specifying which meaning is being used.

### Strongest Supporting Findings

The strongest support for the lens is that it prevents category collapse:

```text
evidence is not the same as observing
claim is not the same as selected claim
question is not the same as inquiry target
recommendation is not the same as decision
capability is not the same as execution
handoff artifact is not the same as continuation behavior
```

It also explains why many recent concepts looked fundamental but later appeared
episode-relative.

### Strongest Falsifying Findings

The strongest falsifying finding is that support, identity, authority, and many
other core concepts require edge semantics.

The lens can say:

```text
object occupies role during operation
```

but many repository examples require:

```text
object has scoped directed connection to another object, with support,
authority, confidence, contradiction, or durability
```

That is relationship language.

### Does Relationship Appear Necessary?

Relationship appears necessary as an explicit pressure-test concern.

This document does not decide whether relationship is a fourth top-level
category or a special object subtype. It finds that relationship cannot be
ignored. The repository already relies on relationships to explain evidence,
support, identity, authority, dependency, contradiction, corroboration, lineage,
and working-state usefulness.

---

## Required Tensions Preserved

The following tensions remain unresolved:

| Tension | Pressure-test result |
| --- | --- |
| Evidence object vs evidence role | Evidence is object-like as preserved provenance, but role-like when another object acts as evidence for a claim. |
| Support relationship vs support object | Support is strongest as relationship; support records or views may be objects representing that relation. |
| Authority relationship vs authority role | Authority can be authorized participation, but permission needs scoped relation among actor, action, object, policy, and state. |
| Identity relationship vs identity object | Entity records are objects; same-as, belongs-to, identifies, and runs-on are relationship claims. |
| Frontier object vs frontier role | Frontier documents persist, but frontier can also mean active unresolved boundary or role-like participation condition. |
| Working state structure vs working state object | Preserved working state can be object-like, but its usefulness depends on selected contents, roles, operations, and relationships. |
| Relationship vs role | Role describes one participant's contextual function; relationship preserves the edge between participants. |
| Relationship vs operation | Operation may create or consume a relationship; the relationship may persist after the operation. |
| Relationship durability | Some relationships are durable claims, some are episodic participation edges, and some are conditional permission states. |

---

## Final Pressure-Test Assessment

The object / role / operation lens survives as a useful diagnostic lens, but not
as a complete explanation of the repository's difficult concepts.

It is strongest for preventing over-materialization of temporary participation
and for separating preserved things from activities. It is weakest when examples
require durable, scoped, directed, or conditional connections between things.

The most likely missing pressure category is:

```text
Relationship
```

This finding is not a reconciliation and does not introduce a canonical category.
It only records that relationship is the strongest falsification candidate for a
three-part lens.

A future participant should therefore treat object / role / operation as useful
but incomplete until the repository reconciles whether relationships are:

```text
objects with edge semantics
roles plus targets and scope
operation results
or a distinct modeling category
```

The pressure test did not protect the theory. It found that the theory explains
many participation and operation confusions, but it becomes strained exactly
where the repository depends on support, authority, identity, dependency,
corroboration, contradiction, lineage, and working-state connections.
