---
doc_type: frontier
status: exploratory
domain: object role operation ontology
defines:
  - object role and operation frontier
  - object role operation boundary
  - object stability test
  - role stability test
  - operation interaction test
  - contextual role hypothesis
depends_on:
  - operations_frontier.md
  - attention_trigger_frontier.md
  - attention_target_frontier.md
  - inquiry_frontier.md
  - selection_and_attention_frontier.md
  - handoff_and_continuation_lineage_frontier.md
  - foundational_ontology_reconciliation.md
  - architectural_status_and_next_frontier.md
related:
  - continuation_context_and_working_state_reconciliation.md
  - handoff_consumption_activation_reconciliation.md
  - knowledge_change_and_revision_reconciliation.md
  - derivation_frontier.md
  - recommendation_selection_boundary.md
  - contradiction_discovery_and_visibility_reconciliation.md
---

# Object, Role, and Operation Frontier

## Purpose

This document investigates whether recent ontology frontiers have repeatedly
confused durable objects with contextual roles and operations.

It is documentation only. It does not implement code, modify schemas, modify
runtime behavior, add tests, design a role system, design a planner, design a
workflow engine, design a runtime operation executor, or define an implementation
architecture.

Repository authority wins over this document. The foundational ontology,
operations, inquiry, selection, attention trigger, attention target,
handoff-lineage, continuation, working-state, and architectural-status documents
remain authoritative for their own settled or partially settled boundaries.

The central question is exploratory:

```text
What is the difference between:

    object
    role
    operation
```

This document does not assume those are the correct categories. It tests whether
they explain a recurring pattern in recent investigations.

---

## Background Observation

Multiple recent frontiers and reconciliations follow a similar arc:

```text
Candidate concept discovered.
        ↓
Appears fundamental.
        ↓
Investigated.
        ↓
Behaves differently depending on context.
```

Examples include:

```text
Knowledge Change
    -> acquisition, derivation, revision, refinement

Derivation
    -> comparison, interpretation, calculation, extrapolation

Attention Trigger
    -> appears episode-relative

Attention Target
    -> appears episode-relative

Inquiry Object
    -> sometimes question, sometimes gap, sometimes tension, sometimes frontier

Working-State Content
    -> appears to depend on the active episode rather than on a new object kind
```

One possible explanation is:

```text
Some investigated concepts are not stable object types.
They may be roles occupied by existing objects during a particular episode.
```

This is only a hypothesis. The risk is symmetrical:

```text
If everything becomes an object, the ontology over-materializes temporary
participation.

If everything becomes a role, the ontology loses durable identity, evidence,
lineage, and citation.

If everything becomes an operation, the ontology collapses representation into
activity and loses what persists after activity ends.
```

---

## Existing Authority That Constrains This Frontier

### Foundational Ontology

The foundational ontology remains claim-centered and evidence-bounded. It gives
Seed durable knowledge vocabulary for observations, evidence, claims, facts,
relationships, projections, questions, goals, policy, operators, explanations,
capabilities, and handoffs.

This frontier must not demote those established objects merely because they can
also participate in episodes. A claim remains a claim whether or not it is
selected, targeted, revised, used as evidence, or included in a handoff.

### Operations Frontier

The operations frontier asks what happens to represented knowledge. It already
warns that not every verb should become a runtime operation, and not every
operation should become an object. That caution applies here. This document uses
`operation` as an ontology discovery term, not an executor, process step,
workflow stage, or implementation component.

### Attention Trigger Frontier

The attention trigger frontier found that triggers explain why attention moves,
but trigger candidates such as contradiction, ambiguity, risk, anomaly, repeated
failure, and operator burden may be episode-relative. A contradiction may trigger
attention in one episode, become evidence in another, and become handoff content
later.

### Attention Target Frontier

The attention target frontier asks what receives attention. Its candidate targets
include goals, needs, gaps, questions, tensions, contradictions, frontiers,
claims, relationships, assessments, and operator requests. The recurrence of
many object types in the same target position is a major reason to test whether
`target` is a role rather than a distinct object type.

### Selection and Attention Frontier

The selection and attention frontier distinguishes selection, relevance,
priority, active focus, frontier, gap, and tension. This document preserves that
boundary by treating `selected`, `active`, and `attended` as possible roles or
participation states, not as automatic evidence of object identity, truth,
priority, or authority.

### Inquiry Frontier

The inquiry frontier asks whether inquiry has an object family, lineage, state,
relationships, and lifecycle, or whether it is better explained as a process over
existing objects. This document re-tests that question with the object / role /
operation distinction in mind.

### Handoff and Continuation Lineage Frontier

The handoff-lineage frontier strengthens the idea that later work may preserve
not only claims, but also unresolved investigation context, active branches,
working-state commitments, and continuation lineage. That evidence matters
because roles may need preservation without becoming independent object types.

### Architectural Status

The architectural-status document cautions against implementing operation,
inquiry, derivation, attribution, continuation-lineage, planner, workflow, or
runtime systems before frontiers are reconciled. This frontier therefore remains
non-implementation discovery.

---

## Method

This investigation uses three tests.

### 1. Object Stability Test

```text
If the thing remains the same while its participation changes,
it is behaving more like an object.
```

Example:

```text
Gap
    -> attention target today
    -> inquiry object tomorrow
    -> handoff content later
```

The test asks:

```text
What changed?

The gap?
Or the role the gap occupied?
```

A candidate passes the object stability test when it can be cited, preserved,
revisited, related, supported, contradicted, refined, or handed off even after a
specific episode ends.

### 2. Role Stability Test

```text
If multiple object types can occupy the same participation position,
that participation position is behaving more like a role.
```

Example:

```text
question
gap
contradiction
need
claim
relationship
```

may all appear as:

```text
attention target
```

The test asks whether `target` names a stable object type or a contextual role
occupied by different objects.

### 3. Operation Interaction Test

```text
Does an operation happen to objects?
Does an operation assign roles?
Does an operation consume roles?
Does an operation create new objects?
```

The test does not assume a single answer. Acquisition may create observations or
evidence. Selection may assign a selected role without creating a new object.
Revision may modify or supersede claims. Interpretation may produce findings.
Inquiry may consume a question-like role while producing evidence, claims,
findings, or new gaps.

---

## Provisional Vocabulary Under Test

The potential framing is:

```text
Objects are what persist.
Roles are how objects participate.
Operations are what happen.
```

This framing is useful only if it survives scrutiny.

A more cautious version is:

```text
Object
    A represented thing with identity or continuity across episodes.

Role
    A contextual participation position occupied by an object during an episode,
    handoff, inquiry, attention movement, selection, or working state.

Operation
    An act, recognition, transformation, pursuit, comparison, preservation,
    revision, or production involving objects and possibly roles.
```

None of these definitions is reconciled. They are working distinctions for the
investigation.

---

## Candidate Object Evaluation

The following table evaluates the requested candidate objects without assuming
that each belongs in the object category.

| Candidate | Evaluation | Current finding |
| --- | --- | --- |
| claim | Strong object candidate. A claim can persist across episodes, be supported, contradicted, revised, selected, targeted, or handed off. Its participation changes without erasing claim identity. | Object, with possible contextual roles. |
| relationship | Strong object candidate when it represents a durable connection between represented things. A relationship can be observed, claimed, supported, challenged, selected, or projected. | Object, though relationship-discovery may be an operation. |
| observation | Strong object candidate. It preserves what was observed from a source or vantage point and can later support evidence or claims. | Object. |
| evidence | Strong object candidate, though sometimes also a role-like support function. A preserved artifact can be evidence for one claim and irrelevant to another. | Object when preserved; evidentiary function can be role-like. |
| question | Mixed. A question can persist as a represented inquiry artifact, be reopened, refined, answered, or handed off. But `active question` appears role-like. | Object or interface artifact; active-question is role-like. |
| goal | Mixed. A goal can be a durable operator or system-intent object, but can also act as trigger, target, selection criterion, or inquiry driver. | Object when represented; many uses are roles. |
| gap | Strong candidate for object-like unresolved absence when preserved, named, tracked, or handed off. It may occupy attention-target, inquiry-target, or handoff-content roles. | Likely object-like unresolved condition plus roles. |
| need | Mixed. A need may be a durable represented requirement or an episode-relative rationale. It often acts as trigger, target, or criterion. | Object when represented; role/rationale in many episodes. |
| contradiction | Mixed but object-like when represented as an incompatibility between claims or relationships. It can trigger attention, become a target, or be evidence of boundary failure. | Object-like finding/tension; trigger is role-like. |
| ambiguity | Mixed. Ambiguity may be a represented unresolved interpretive condition, but often names why inquiry is needed rather than a durable object. | Possible object when preserved; often trigger/condition role. |
| frontier | Ambiguous. A frontier may be a documentation artifact, an unresolved investigation boundary, a collection of tensions, or a preservation structure. | Not a simple object; likely composite/preservation structure and sometimes role. |
| finding | Strong object candidate when preserved as a conclusion or result with support. A finding can be selected, used, revised, or handed off. | Object produced by operations. |
| recommendation | Strong object candidate under existing boundaries when represented as a suggested course of action distinct from decision or execution. Recommendation generation is an operation. | Object; generation is operation. |

### Object Findings

The object stability test suggests that many candidate objects are valid objects
because they can outlive a specific episode:

```text
claim
relationship
observation
evidence
question
gap
contradiction
finding
recommendation
```

However, several candidates are object-like only when represented and preserved:

```text
goal
need
ambiguity
frontier
```

The important discovery is not that the object list is wrong. It is that object
identity and contextual participation are different questions. A gap can remain
the same gap while moving through attention, inquiry, working-state, and handoff
roles.

---

## Candidate Role Evaluation

The following table evaluates the requested candidate roles without assuming
that each belongs in the role category.

| Candidate | Evaluation | Current finding |
| --- | --- | --- |
| trigger | Strong role candidate. Many object types can trigger attention: contradiction, risk, anomaly, operator request, ambiguity, gap, repeated failure. Trigger explains why attention moved in an episode. | Role-like participation; not a stable object type by itself. |
| target | Strong role candidate. Questions, gaps, claims, relationships, needs, contradictions, and frontiers can all receive attention. | Role-like participation. |
| active | Strong role/state candidate. An object can become active and later inactive without changing identity. | Role or episode state, not object. |
| selected | Strong role candidate. Selection confers participation in a view, response, handoff, or focus episode without proving truth or priority. | Role-like participation assigned by selection. |
| unresolved | Mixed. Unresolved can describe an object state, such as an unanswered question or unreconciled contradiction, but can also operate as a role in inquiry. | State/role adjective, not standalone object. |
| frontier-content | Strong role candidate. Many objects can be included in a frontier as content. The content role depends on the frontier document or investigation boundary. | Role within a preservation structure. |
| working-state-content | Strong role candidate. Objects included in current working state may later be removed, archived, or handed off without changing object identity. | Role within active context. |
| handoff-content | Strong role candidate. Objects selected for continuation occupy a handoff role without becoming a separate handoff object. | Role within handoff preservation. |
| attention-target | Strong role candidate. It names what attention is directed toward, not what the object fundamentally is. | Role. |
| inquiry-target | Strong role candidate. A question, gap, contradiction, need, or frontier can be pursued by inquiry. | Role, unless later evidence supports a durable inquiry object subtype. |

### Role Findings

The role stability test strongly supports `trigger`, `target`, `active`,
`selected`, `working-state-content`, `frontier-content`, `handoff-content`,
`attention-target`, and `inquiry-target` as roles or role-like participation
positions.

The strongest evidence is substitutability:

```text
question
gap
contradiction
need
claim
relationship
frontier
```

can each occupy:

```text
attention target
inquiry target
working-state content
handoff content
```

This suggests that recent frontiers may sometimes have been investigating role
positions rather than new ontology objects.

The finding is not that roles are unimportant. Role preservation may be critical
to continuation. If a future participant receives a handoff, knowing that a gap
was the active attention target may matter even though `attention target` is not
itself a new durable object type.

---

## Candidate Operation Evaluation

The following table evaluates the requested candidate operations without
assuming that each belongs in the operation category.

| Candidate | Evaluation | Current finding |
| --- | --- | --- |
| selection | Strong operation candidate. It can assign selected, active, included, or handoff-content roles to existing objects. It may produce a projection or summary but need not create a new knowledge object. | Operation assigning roles and producing views. |
| attention | Strong operation or episode candidate. It focuses work on an object occupying target role and may be activated by another object occupying trigger role. | Operation/episode over role-bearing objects. |
| inquiry | Strong operation candidate, but not only an operation if inquiry lineage or question artifacts persist. Inquiry pursues unresolved understanding and may create findings, claims, or new gaps. | Operation with possible preserved objects/lineage. |
| acquisition | Strong operation candidate. It brings observations, evidence, assertions, or source material into represented knowledge. | Operation that can create objects. |
| derivation | Strong operation-family candidate, likely not primitive. It can include comparison, interpretation, calculation, and extrapolation. | Operation family. |
| revision | Strong operation candidate. It changes, supersedes, qualifies, or corrects represented knowledge. | Operation over objects, preserving lineage. |
| refinement | Strong operation candidate. It narrows, qualifies, clarifies, or improves an existing object without necessarily replacing it. | Operation. |
| correction | Strong operation candidate. It addresses error and may revise or supersede claims, relationships, projections, or findings. | Operation with lineage implications. |
| comparison | Strong operation candidate. It relates objects for similarity, difference, compatibility, or contradiction discovery. | Operation that may create findings or contradictions. |
| interpretation | Strong operation candidate, but risky if treated as verification. It may produce claims, assessments, findings, or caveats. | Operation, not truth by itself. |
| calculation | Strong operation candidate. It transforms inputs under explicit rules and may produce derived values or claims. | Operation that can produce objects. |
| extrapolation | Strong operation candidate. It extends from existing evidence or patterns toward future or unobserved claims, forecasts, or projections. | Operation with caveat needs. |
| recommendation generation | Strong operation candidate. It produces recommendation objects but is distinct from the recommendation itself, decision, command, or execution. | Operation producing objects. |

### Operation Findings

The operation interaction test suggests four different operation effects:

```text
1. Operations may consume objects.
   Example: comparison consumes two or more claims, observations, or
   relationships as inputs.

2. Operations may assign roles.
   Example: selection can make a claim selected, active, or handoff content.

3. Operations may consume roles.
   Example: inquiry may consume an inquiry-target role as the thing being
   pursued, while attention may consume trigger and target roles.

4. Operations may create new objects.
   Example: acquisition can create observations or evidence; comparison can
   produce a contradiction finding; recommendation generation can produce a
   recommendation.
```

The same operation may do several of these at once. That does not require a
runtime design. It only means that object, role, and operation boundaries are
interdependent.

---

## Critical Example 1: Gap

Questions:

```text
Is a gap an object?
Is attention target a role a gap can occupy?
Is inquiry an operation performed on a gap?
```

### Evaluation

A gap appears object-like when it is represented as a specific unresolved absence
or missing support:

```text
Gap A: no evidence yet supports whether claim C applies under condition K.
```

The same gap can participate in multiple episodes:

```text
Episode 1: Gap A triggers attention.
Episode 2: Gap A is the attention target.
Episode 3: Gap A is the inquiry target.
Episode 4: Gap A is working-state content.
Episode 5: Gap A is handoff content.
```

The object stability test asks what changed. The best current answer is:

```text
The gap remained the unresolved absence.
Its roles changed across episodes.
```

Inquiry appears to be an operation performed with respect to the gap, not the gap
itself. Inquiry may refine the gap, split it, close it, produce evidence, create
claims, or discover a different gap.

### Finding

Gap is a strong example of the object / role / operation distinction:

```text
gap = object-like unresolved condition when preserved
attention target = role the gap can occupy
inquiry = operation that may pursue, refine, or resolve the gap
```

This remains exploratory because some uses of `gap` may be shorthand for a role
or criterion rather than a preserved object.

---

## Critical Example 2: Contradiction

Questions:

```text
Is contradiction an object?
Is trigger a role contradiction may occupy?
Is contradiction discovery an operation?
```

### Evaluation

A contradiction appears object-like when it is represented as a specific
incompatibility among claims, relationships, observations, projections, or
authority boundaries. It can be cited, preserved, investigated, resolved,
reopened, or handed off.

But contradiction also frequently behaves as a trigger:

```text
Contradiction B caused attention to move.
```

In that sentence, `trigger` is not the contradiction's essence. It is the role
the contradiction occupied in an attention episode.

Contradiction discovery appears operation-like:

```text
compare claims
interpret incompatibility
recognize contradiction
preserve contradiction finding
```

The operation may produce a contradiction object or finding. The produced object
can later occupy trigger, target, evidence, working-state-content, or
handoff-content roles.

### Finding

Contradiction should not be collapsed into trigger. A contradiction may be:

```text
object-like represented incompatibility
finding produced by discovery or comparison
trigger role in an attention episode
target role in an inquiry episode
handoff content in continuation lineage
```

This example strongly supports separating object identity from episode role.

---

## Critical Example 3: Question

Questions:

```text
Is question an object?
Is active-question a role?
Is inquiry an operation involving a question?
```

### Evaluation

A question is already recognized as an operator-facing bridge in the foundational
ontology. It can also behave as a durable inquiry artifact when preserved,
refined, reopened, answered, split, or handed off.

However, `active-question` appears role-like:

```text
Question Q exists.
Question Q becomes active during an episode.
Question Q is no longer active after attention moves.
Question Q remains the same question.
```

Inquiry may involve a question in several ways:

```text
A question may initiate inquiry.
A question may be the inquiry target.
Inquiry may refine the question.
Inquiry may answer the question.
Inquiry may produce findings that generate new questions.
```

### Finding

Question is a plausible object or interface artifact. Active-question is better
understood as a role or episode state. Inquiry is operation-like, but inquiry may
also preserve lineage around questions and unresolved understanding.

The unresolved boundary is whether Seed needs a durable inquiry-object family or
whether question, gap, contradiction, and finding objects plus roles and
operations are sufficient.

---

## Critical Example 4: Frontier

Questions:

```text
Is frontier an object?
A role?
A collection?
A preservation structure?
```

### Evaluation

`Frontier` is the most ambiguous candidate. In repository practice, a frontier
can mean:

```text
1. A documentation artifact that records exploratory investigation.
2. A boundary around unresolved architectural understanding.
3. A collection of questions, tensions, findings, candidates, and non-goals.
4. A preservation structure for future participants.
5. A role occupied by content that is not yet reconciled.
```

A frontier document is object-like as a repository artifact. The unresolved area
it names may also be object-like if it has durable identity across work. But
`frontier-content` is role-like because many kinds of objects can be included in
a frontier:

```text
question
gap
tension
finding
candidate object
candidate role
candidate operation
non-goal
unresolved tension
```

A frontier may also be produced by operations such as investigation,
reconciliation, preservation, or handoff.

### Finding

Frontier should not be treated as a simple object type. The current best
characterization is:

```text
frontier = documentation artifact plus unresolved-investigation boundary plus
preservation structure

frontier-content = role occupied by objects preserved inside that structure

frontier creation or update = operation-like documentation/preservation act
```

This is an important tension because frontiers can preserve roles without making
those roles independent objects.

---

## Critical Example 5: Working State

Questions:

```text
Does working state contain objects?
Roles?
Operation context?
```

### Evaluation

Working state appears to preserve what matters for continuation of an active
episode. That likely includes objects:

```text
claims
questions
gaps
contradictions
findings
recommendations
frontiers
```

But it also appears to preserve roles:

```text
active
selected
attention target
inquiry target
working-state content
blocked
unresolved
handoff relevant
```

And it may preserve operation context:

```text
what was being investigated
what operation was underway
what evidence had been consumed
what comparison or refinement remained incomplete
what assumptions constrained the next step
```

The mistake would be to say working state contains roles alone. Roles without
objects are empty participation slots. The opposite mistake would be to say it
contains only objects. Objects without their current participation context may be
insufficient for continuation.

### Finding

Working state is best investigated as preserving:

```text
objects
plus their current roles
plus enough operation context to resume safely
```

This does not imply a working-state schema or runtime. It only explains why
recent continuation and handoff documents repeatedly encounter both content and
participation language.

---

## Relationship to Attention

Attention strongly supports the role hypothesis.

The distinction appears to be:

```text
trigger = role explaining why attention moved
target = role explaining what attention moved toward
attention = operation or episode of focusing on a target, often activated by a trigger
```

Objects that may occupy trigger role include:

```text
contradiction
ambiguity
risk
anomaly
operator request
repeated failure
gap
need
```

Objects that may occupy target role include:

```text
question
gap
claim
relationship
contradiction
frontier
need
goal
recommendation
```

The same object can occupy both roles in the same or different episodes. A
contradiction may trigger attention and also become the target. A gap may be
noticed because it triggers attention, then become the target of inquiry.

This means attention target language is useful, but probably as role language,
not as a new object ontology.

---

## Relationship to Inquiry

Inquiry is difficult because it has evidence on both sides.

### Evidence for Inquiry as Operation

Inquiry often reads as activity:

```text
pursue a question
investigate a gap
resolve ambiguity
compare claims
interpret evidence
refine understanding
produce finding
```

Those verbs support treating inquiry as an operation or operation family.

### Evidence Against Reducing Inquiry to Operation Only

The inquiry frontier found that inquiry may have lineage:

```text
questions persist
gaps are reopened
findings preserve what was discovered
frontiers carry unresolved branches
handoffs continue investigations
```

If inquiry lineage persists, then inquiry cannot be described only as a momentary
operation. It may involve durable objects and preserved roles.

### Current Finding

The safest current formulation is:

```text
inquiry = operation-like pursuit of unresolved understanding

inquiry target = role occupied by an object being pursued

question / gap / contradiction / frontier / finding = possible objects involved
in inquiry lineage
```

This avoids prematurely designing an inquiry runtime while preserving the
possibility that later reconciliation may promote an inquiry-object family.

---

## Relationship to Operations

Operations interact with objects and roles in several patterns.

### Operation Over Object

```text
revision over claim
comparison over claims
interpretation over evidence
calculation over values
refinement over question
```

The object is the input or subject of the operation.

### Operation Assigning Role

```text
selection assigns selected
attention assigns active target
handoff selection assigns handoff content
frontier preservation assigns frontier content
```

The role explains participation in a context.

### Operation Consuming Role

```text
attention consumes trigger and target roles
inquiry consumes inquiry-target role
handoff consumes handoff-content role
selection consumes candidate role
```

The role helps explain how the operation proceeds.

### Operation Producing Object

```text
acquisition produces observation or evidence
comparison produces contradiction finding
interpretation produces assessment or caveat
recommendation generation produces recommendation
reconciliation produces finding or boundary
```

The result may then occupy roles in later episodes.

### Operation Producing Role Without New Object

Some operations may create no new object:

```text
selecting an existing claim for response
making an existing gap active
including an existing finding in working state
marking an existing question as handoff relevant
```

This is a key reason implementation would be premature. The repository needs
more reconciliation before deciding which operations warrant durable records and
which only explain contextual participation.

---

## Reclassification of Candidate Lists

The following reclassification is exploratory, not authoritative.

### Strong Object Candidates

```text
claim
relationship
observation
evidence
question
represented gap
represented contradiction
finding
recommendation
```

### Conditional or Composite Object Candidates

```text
goal
need
ambiguity
frontier
working state
```

These may be objects when represented and preserved, but often behave as
context, criteria, collections, or preservation structures.

### Strong Role Candidates

```text
trigger
target
active
selected
frontier-content
working-state-content
handoff-content
attention-target
inquiry-target
```

### Mixed State / Role Candidates

```text
unresolved
blocked
current
available
latent
handoff relevant
```

These describe participation or state of an object in an episode. They should
not be promoted to standalone object types without stronger evidence.

### Strong Operation Candidates

```text
selection
attention
acquisition
derivation
revision
refinement
correction
comparison
interpretation
calculation
extrapolation
recommendation generation
```

### Mixed Operation / Lineage Candidate

```text
inquiry
```

Inquiry appears operation-like, but may involve durable inquiry lineage or
preserved inquiry objects. It should remain under investigation.

---

## Unresolved Tensions

### Object vs Role

Some nouns are durable in one context and role-like in another. Evidence is a
preserved object, but `evidence for claim C` can also describe a role that a
source artifact occupies relative to a claim. A gap can be a represented object,
but `gap as attention target` is role participation.

### Role vs Operation

`Selected` appears role-like, while `selection` appears operation-like. But some
language blurs the boundary:

```text
active
attended
pursued
handoff relevant
```

These may name states caused by operations, roles consumed by operations, or
participant descriptions. The repository has not reconciled that boundary.

### Frontier vs Role

A frontier preserves unresolved objects and role assignments, but `frontier` can
also act as a target, content grouping, document type, investigation boundary, or
handoff artifact. It is not yet clear whether the unresolved boundary itself has
durable object identity apart from the document that preserves it.

### Contradiction vs Role

Contradiction may be a durable represented incompatibility, a finding produced by
comparison, a trigger for attention, a target of inquiry, or handoff content. The
same word crosses object, role, and operation-result boundaries.

### Question vs Role

Question is object-like when preserved. Active-question and inquiry-target are
role-like. The unresolved issue is whether a question is merely an interface
object or part of a broader inquiry-object family.

### Inquiry vs Operation

Inquiry has operation-like behavior, but inquiry lineage suggests persistence.
The unresolved boundary is whether inquiry itself is an operation, an object
family, a lineage structure, or a name for coordinated operations over unresolved
objects.

### Attention vs Operation

Attention appears operation-like or episode-like. But attention may also be a
state of focus represented in working state. The unresolved issue is whether
attention should be named as an operation, a role assignment, an episode, or only
a participant description.

### Working State vs Role Preservation

Working state likely preserves objects plus roles plus operation context. The
unresolved issue is how much role context is necessary for continuation without
creating a role engine or working-state schema.

### Role Durability

Roles may be temporary, but some roles matter after the episode ends. A handoff
may need to preserve that a contradiction was the active attention target, even
if the contradiction later stops being active. This raises the possibility of
role history without implying roles are durable objects.

### Role Lineage

If an object moves from trigger to target to inquiry target to handoff content,
that path may matter. The repository has not reconciled whether this is lineage
of the object, lineage of roles, lineage of operations, or all three.

---

## Findings

### Object Findings

Objects appear to be represented things with enough continuity to be cited,
supported, revised, related, selected, targeted, handed off, or revisited. The
object category remains useful, especially for claims, relationships,
observations, evidence, findings, recommendations, represented gaps, represented
questions, and represented contradictions.

The object category becomes unsafe when temporary participation is mistaken for
identity. `Attention target` should not become an object merely because attention
needs something to point at.

### Role Findings

Roles appear to be contextual participation positions. The same object can
occupy different roles over time, and multiple object types can occupy the same
role. This strongly explains why recent frontiers repeatedly discovered concepts
that appeared fundamental but became context-dependent under scrutiny.

Roles may still require preservation in handoff, frontier, and working-state
contexts. The fact that a role is not a stable object type does not make it
unimportant.

### Operation Findings

Operations appear to be what happens to, with, or over represented objects and
role-bearing contexts. Operations may assign roles, consume roles, create
objects, revise objects, or produce findings. Some operations leave durable
results; others may only change participation context.

No operation runtime follows from this finding.

### Attention Findings

Attention trigger and attention target are best treated as role-like concepts at
this stage:

```text
trigger = why attention moved
target = what attention moved toward
attention = focusing episode or operation involving those roles
```

Contradictions, gaps, questions, needs, risks, claims, relationships, and
frontiers may occupy attention roles without becoming attention-specific object
types.

### Inquiry Findings

Inquiry is better understood as operation-like than object-like in many examples,
but it should not be collapsed into operation only. Inquiry may preserve lineage
through questions, gaps, findings, frontiers, handoffs, and working-state
context.

The safer current boundary is:

```text
inquiry operation pursues an inquiry-target role occupied by some object,
and may produce or transform durable objects.
```

### Working-State Findings

Working state likely preserves objects plus current roles plus operation context.
This explains why working-state content and handoff content feel role-like while
still requiring durable objects underneath them.

---

## Why Implementation Would Be Premature

Implementation would be premature because the repository has not reconciled:

```text
whether roles require durable records;
whether role history is object lineage, operation lineage, or separate lineage;
whether inquiry is an operation, object family, lineage structure, or hybrid;
whether attention is an operation, episode, role assignment, or focus state;
whether frontier is an object, collection, document artifact, or preservation structure;
whether working state preserves roles as current context or historical facts.
```

Designing schemas, runtimes, planners, role engines, workflow systems, or
operation executors now would risk hard-coding distinctions that this frontier
only begins to discover.

---

## Conclusion

The object / role / operation distinction is useful, but not yet reconciled.

The strongest current framing is:

```text
Objects are what persist.
Roles are how objects participate.
Operations are what happen.
```

The framing survives initial scrutiny for gaps, contradictions, questions,
attention, inquiry, working state, and handoff content. It explains why recent
frontiers often found candidate concepts that seemed fundamental but became
context-dependent: they may have been studying roles occupied by existing objects
inside attention, inquiry, selection, working-state, frontier, and handoff
episodes.

The framing does not settle every boundary. Frontier, inquiry, working state,
contradiction, evidence, goal, need, and ambiguity remain mixed or context-sensitive.
Future reconciliation should preserve the distinction without implementing it
prematurely.
