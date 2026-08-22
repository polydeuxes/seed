---
doc_type: audit
status: exploratory
domain: object role operation consistency
defines:
  - object role operation consistency audit
  - object role operation category drift
  - persistence test
  - participation test
  - operation separation test
depends_on:
  - object_role_and_operation_frontier.md
  - operations_frontier.md
  - attention_trigger_frontier.md
  - attention_target_frontier.md
  - inquiry_frontier.md
  - selection_and_attention_frontier.md
  - foundational_ontology_reconciliation.md
  - knowledge_representation_reconciliation.md
  - architectural_status_and_next_frontier.md
related:
  - continuation_context_and_working_state_reconciliation.md
  - handoff_and_continuation_lineage_frontier.md
  - handoff_consumption_activation_reconciliation.md
  - knowledge_change_and_revision_reconciliation.md
  - derivation_frontier.md
  - recommendation_selection_boundary.md
  - contradiction_discovery_and_visibility_reconciliation.md
---

# Object / Role / Operation Consistency Audit

## Purpose

This document audits whether repository terminology consistently distinguishes
candidate objects, roles, and operations after the Object, Role, and Operation
Frontier raised a potentially unifying finding:

```text
Objects are what persist.
Roles are how objects participate.
Operations are what happen.
```

This audit does not reconcile that framing. It tests whether the current
repository evidence supports it, contradicts it, or shows category drift.

This is documentation only. It does not implement code, modify schemas, modify
runtime behavior, add tests, define new ontology, redesign existing ontology,
propose implementation, create a role system, create an operation system, create
working-state architecture, or settle any frontier.

Repository authority wins over this audit. Reconciled documents remain
authoritative for their settled boundaries, and frontier documents remain
exploratory.

---

## Method

The audit reviewed the required authoritative references and adjacent evidence
needed to avoid contradicting them. It evaluated usage rather than word forms.
For each concept family it asked:

```text
What appears to persist?
What appears to participate?
What appears to happen?
```

The audit uses five non-settling labels:

| Label | Meaning in this audit |
| --- | --- |
| Treated mostly as object | Repository language usually treats the concept as something preserved, cited, supported, revised, handed off, or revisited. |
| Treated mostly as role | Repository language usually treats the concept as a participation position occupied by different things in an episode, surface, handoff, frontier, or working state. |
| Treated mostly as operation | Repository language usually treats the concept as an act, recognition, transformation, selection, pursuit, or production involving other things. |
| Mixed usage | Repository language uses the concept across more than one category in ways that may be legitimate or drift-prone. |
| Unresolved | Repository evidence is too incomplete, frontier-bound, or ambiguous to classify even provisionally. |

These labels are audit findings, not ontology definitions.

---

## Evidence Base Reviewed

The required references expose a layered repository state:

- `foundational_ontology_reconciliation.md` establishes a claim-centered,
  evidence-bounded vocabulary for durable represented knowledge, including
  observations, evidence, claims, facts, relationships, projections, questions,
  goals, recommendations, decisions, capabilities, handoffs, events, changes,
  states, policy, authority, trust, contradiction, causality, and explanation.
- `knowledge_representation_reconciliation.md` treats Seed's knowledge model as
  representation-centered and boundary-preserving rather than schema-centered or
  runtime-centered.
- `operations_frontier.md` identifies a less-settled operation layer for what
  happens to represented knowledge, while warning that operations are not
  executors, pipelines, runtime stages, or implementation components.
- `selection_and_attention_frontier.md` distinguishes selected, prioritized,
  relevant, active, and attended states without turning selection into truth,
  authority, recommendation, or execution.
- `attention_trigger_frontier.md` investigates why attention moves, while
  repeatedly warning that trigger candidates can also be objects, inquiry
  targets, acquisition-relevant conditions, or handoff-relevant context.
- `attention_target_frontier.md` investigates what receives attention, and its
  strongest evidence is that many different preserved things can occupy the
  target position.
- `inquiry_frontier.md` keeps inquiry unresolved because it appears partly like
  activity, partly like lineage, and partly like preserved unresolved context.
- `object_role_and_operation_frontier.md` explicitly tests the object / role /
  operation framing and finds it useful but unreconciled.
- `architectural_status_and_next_frontier.md` keeps operations, inquiry,
  derivation, attribution, handoff-lineage, and similar frontiers
  non-implementation-ready.

This evidence base is internally consistent about one constraint: audit language
must not become implementation language.

---

## Candidate Object Family Audit

The following table audits repository treatment of the requested candidate
objects without assuming that the candidate category is correct.

| Concept | Repository usage observed | Consistency evaluation |
| --- | --- | --- |
| observation | Usually preserved as source- or vantage-point report, used as support for evidence and claims, and protected from over-promotion into broader truth. | Treated mostly as object. |
| evidence | Preserved as provenance or support, but also used relationally as evidence-for a claim. | Mixed usage: object when preserved; role-like support function when relative to another object. |
| claim | Central represented proposition that can persist, be supported, selected, contradicted, revised, projected, explained, or handed off. | Treated mostly as object. |
| relationship | Represented connection between things; sometimes also result of relationship-generation or interpretation. | Treated mostly as object, with operation-result edge cases. |
| question | Foundational operator-facing bridge and recurring inquiry artifact; also appears as active question, inquiry target, attention target, or handoff content. | Mixed usage: object-like when preserved; role-like when active or targeted. |
| goal | Durable purpose when represented, but frequently works as criterion, driver, trigger, attention target, or acquisition-relevant condition. | Mixed usage. |
| gap | Preserved unresolved absence or missing support in many examples; also used as trigger, attention target, inquiry target, working-state content, and handoff content. | Mostly object-like when represented, with strong role participation. |
| need | Sometimes represented requirement or capability need; often used as rationale, trigger, attention target, or selection criterion. | Mixed usage. |
| contradiction | Can be represented incompatibility or finding; also frequently trigger, target, evidence of boundary failure, or handoff content. | Mixed usage, with strong object-like core when preserved. |
| ambiguity | Can be preserved unresolved interpretive condition; often appears as trigger or reason for inquiry rather than durable object. | Mixed usage leaning unresolved. |
| finding | Preserved conclusion or audit result produced by investigation, comparison, interpretation, or reconciliation; later selected, cited, revised, or handed off. | Treated mostly as object, often operation-produced. |
| recommendation | Represented suggested course of action, explicitly distinct from decision, command, execution, and recommendation generation. | Treated mostly as object. |
| frontier | Documentation artifact, unresolved investigation boundary, collection of questions and tensions, preservation structure, and sometimes target or content context. | Mixed usage and unresolved as a simple category. |

### Object Consistency Findings

The repository is most internally consistent when it discusses durable
represented knowledge:

```text
observation
evidence
claim
relationship
finding
recommendation
```

Even here, consistency is not absolute. Evidence can behave as both preserved
support object and evidentiary role. Relationship can be represented object and
operation result. Recommendation can be represented object while recommendation
generation is operation.

The strongest object consistency is claim-centered. The repository repeatedly
protects the distinction between claims and facts, observations and claims,
evidence and truth, recommendations and decisions, and commands and execution.
That discipline supports the conclusion that Seed's mature ontology is primarily
about preserved represented things and their authority boundaries.

Category drift appears when unresolved or continuation-facing concepts are
objectified too quickly:

```text
question
goal
gap
need
contradiction
ambiguity
frontier
```

Those concepts can persist, but repository usage also places them in trigger,
target, active, selected, inquiry, working-state, and handoff roles. The drift is
not necessarily an error. The risk is failing to say which usage is intended.

---

## Candidate Role Family Audit

The following table audits repository treatment of the requested candidate roles
without assuming that role is the correct category.

| Concept | Repository usage observed | Consistency evaluation |
| --- | --- | --- |
| trigger | Explains why attention moved; many objects can trigger attention, and the same object may later become target or handoff content. | Treated mostly as role. |
| target | Explains what attention or inquiry is directed toward; occupied by gaps, questions, needs, contradictions, claims, relationships, frontiers, goals, and recommendations. | Treated mostly as role. |
| selected | Indicates participation in a projection, context, response, working state, or handoff without proving truth, priority, authority, or action. | Treated mostly as role/state assigned by selection. |
| active | Indicates current focus or continuation relevance without changing object identity. | Treated mostly as role/state. |
| unresolved | Describes condition of questions, gaps, contradictions, frontiers, and tensions; sometimes behaves as inquiry participation. | Mixed usage: state adjective and role-like filter. |
| frontier-content | Describes content included in a frontier document or unresolved investigation boundary. | Treated mostly as role within preservation structure. |
| working-state-content | Describes objects selected into current continuation context. | Treated mostly as role. |
| handoff-content | Describes objects selected for continuation transfer without becoming the handoff itself. | Treated mostly as role. |
| inquiry-target | Describes the object being pursued by inquiry. | Treated mostly as role. |
| attention-target | Describes what receives attention. | Treated mostly as role. |

### Role Consistency Findings

The repository is increasingly consistent when it uses these terms as
participation language rather than object identity:

```text
trigger
target
selected
active
frontier-content
working-state-content
handoff-content
inquiry-target
attention-target
```

The strongest evidence is substitutability. Many different things can occupy the
same position:

```text
gap
question
need
contradiction
claim
relationship
frontier
recommendation
```

all can appear as:

```text
attention target
inquiry target
working-state content
handoff content
```

This supports, but does not settle, the idea that recent attention, inquiry,
working-state, and handoff frontiers have exposed roles rather than a new object
family for every position.

The main role drift is durability. A role may be temporary, but continuation may
need to preserve that it occurred. For example, a contradiction may no longer be
active, yet a handoff may need to remember that it was the active attention
target. Repository language has not settled whether such preservation is object
lineage, role lineage, operation lineage, handoff context, working-state history,
or documentation prose.

---

## Candidate Operation Family Audit

The following table audits repository treatment of the requested candidate
operations without assuming that operation is the correct category.

| Concept | Repository usage observed | Consistency evaluation |
| --- | --- | --- |
| attention | Described as actual focus or movement into active exploration; consumes or assigns trigger and target roles. | Mostly operation/episode, with state-preservation edge cases. |
| selection | Described as choosing or including for a surface, context, projection, response, focus, or continuation without erasing alternatives. | Treated mostly as operation. |
| inquiry | Described as pursuit of unresolved understanding, but also as possible lineage, artifact family, and handoff-resumable context. | Mixed usage: operation-like but not reducible to operation. |
| acquisition | Described as bringing observations, evidence, testimony, imports, or assertions into represented knowledge. | Treated mostly as operation that creates or preserves objects. |
| derivation | Described as knowledge from knowledge, but likely family-level rather than primitive; overlaps with comparison, interpretation, calculation, extrapolation. | Treated mostly as operation family. |
| revision | Described as relating later understanding to earlier understanding as changed, narrowed, corrected, superseded, or replaced. | Treated mostly as operation with lineage. |
| refinement | Described as narrowing, qualifying, or improving precision without necessarily declaring prior understanding false. | Treated mostly as operation. |
| correction | Described as marking prior understanding mistaken, mis-scoped, misidentified, or invalid. | Treated mostly as operation with lineage. |
| comparison | Described as examining represented objects together for sameness, difference, contradiction, ordering, or relation. | Treated mostly as operation. |
| interpretation | Described as characterizing meaning within scope, with explicit warnings not to treat interpretation as verification. | Treated mostly as operation. |
| calculation | Described as applying formal or quantitative computation over represented values. | Treated mostly as operation. |
| extrapolation | Described as extending from existing evidence or patterns toward future or unobserved claims, forecasts, or projections. | Treated mostly as operation. |
| recommendation generation | Described as producing a recommendation object and kept distinct from recommendation, decision, command, and execution. | Treated mostly as operation. |

### Operation Consistency Findings

The repository is most consistent where an operation is clearly separated from
its result:

```text
acquisition -> observation / evidence
comparison -> contradiction finding or relationship
interpretation -> assessment / caveat / claim / finding
calculation -> derived value or claim
extrapolation -> forecast or future claim
recommendation generation -> recommendation
selection -> selected role, projection, or context inclusion
```

The repository is less consistent where an operation may also imply lineage or
state:

```text
inquiry
attention
revision
correction
refinement
```

The drift is not that these are wrongly named operations. The drift is that the
repository sometimes asks a single term to answer several questions:

```text
What happened?
What object resulted?
What role was assigned?
What state changed?
What lineage must be preserved?
```

The operations frontier handles this risk explicitly by refusing to treat
operations as runtime stages, engines, workflows, or schema classes. This audit
finds that caution consistent with the repository's current maturity level.

---

## Persistence Test

Test question:

```text
What survives participation changes?
```

Example path:

```text
Gap
    -> attention target
    -> inquiry target
    -> frontier content
```

Audit result:

```text
What persisted?
    The represented gap, if it was preserved as a specific unresolved absence,
    missing support condition, or known unknown.

What changed?
    Its participation changed: first as the thing attention moved toward, then
    as the thing inquiry pursued, then as content preserved in a frontier.
```

The same test applies to several families:

| Persisting thing | Participation changes observed |
| --- | --- |
| Question | active question, inquiry target, attention target, answered question, handoff content. |
| Contradiction | trigger, target, inquiry object, finding, handoff content, evidence of boundary failure. |
| Claim | selected claim, contradicted claim, evidence-supported claim, target of revision, projection content. |
| Finding | frontier content, working-state content, handoff content, support for later architectural status. |
| Recommendation | generated object, selected option, response content, not decision or command. |

The repository is fairly consistent in preserving durable objects across these
participation changes. Category drift appears when the participation label is
read back as object identity, such as treating `attention target` as a kind of
thing rather than a position a thing occupies.

---

## Participation Test

Test question:

```text
Can many different things occupy the same position?
```

The repository evidence strongly answers yes for `target`:

```text
Gap
Question
Need
Contradiction
Claim
Relationship
Frontier
Goal
Recommendation
```

can all appear as:

```text
attention target
```

Audit result:

```text
Is target behaving as a role?
    Yes, mostly. The target position is repeatedly occupied by different object
    candidates and does not appear to supply durable object identity by itself.
```

The same is broadly true for:

```text
trigger
selected
active
inquiry-target
working-state-content
handoff-content
frontier-content
```

The unresolved complication is role preservation. If a handoff must remember
that a gap was the attention target, the role has historical importance. That
does not prove the role is an object, but it does show that non-object
participation may still need durable explanation.

---

## Operation Test

Test questions:

```text
What appears to happen?
What appears to participate?
What appears to persist?
```

Repository language is most consistent when these are separated:

```text
What happens?
    selection, attention, inquiry, acquisition, derivation, revision,
    refinement, correction, comparison, interpretation, calculation,
    extrapolation, recommendation generation.

What participates?
    claims, observations, evidence, relationships, questions, gaps, needs,
    contradictions, findings, recommendations, frontiers, and role-bearing
    contexts such as target, trigger, selected, active, handoff content, and
    working-state content.

What persists?
    represented objects, support paths, findings, handoffs, frontier documents,
    and sometimes the context necessary to explain participation and continuation.
```

The repository is less consistent when the same word names an activity and the
artifact or state around that activity:

```text
projection
assessment
change
event
support
inquiry
attention
frontier
working state
```

The audit does not resolve these. It records that the repository already knows
these are boundary-sensitive terms.

---

## Frontier Reinterpretation Evaluation

This section revisits recent frontier families and asks whether they revealed new
ontology or exposed object / role / operation confusion. The answer is mixed.

| Frontier family | Evidence for genuinely new ontology | Evidence for object / role / operation confusion | Audit finding |
| --- | --- | --- | --- |
| Inquiry | Inquiry may have lineage, branches, unresolved state, findings, handoff-resumable context, and question artifacts. | Inquiry targets can be questions, gaps, contradictions, needs, frontiers, or findings; inquiry also reads as activity. | Mixed: inquiry exposed operation and lineage questions more than a settled object family. |
| Attention | Attention names actual focus and activation, which is not identical to selection, priority, relevance, or knowledge existence. | Trigger and target are substitutable participation positions occupied by many objects. | Mostly role/operation clarification, with open state-preservation questions. |
| Attention triggers | Trigger vocabulary explains why attention moved. | Goal, need, gap, contradiction, operator request, repeated failure, risk, and ambiguity can also be objects, rationales, targets, or acquisition-relevant conditions. | Strong role finding; not a settled object ontology. |
| Attention targets | Target vocabulary explains what attention moved toward. | Many object types can occupy target; target does not appear durable by itself. | Strong role finding. |
| Working state | Continuation requires preserving active subset and current participation context. | Working state can be mistaken for a new object container, role set, active context, handoff artifact, or process state. | Mixed: likely composition of objects, roles, and operation context, but not settled. |
| Handoff lineage | Handoffs preserve more than final claims: unresolved work, active branches, next safe moves, rationale, and continuation context. | Handoff content, activation, and working-state preservation can be mistaken for new object types. | Mixed: exposes role and lineage preservation rather than only new objects. |
| Selection rationale | Selection rationale explains why known candidates had a selection outcome. | Selected status can be mistaken for truth, authority, priority, recommendation, decision, or execution. | Mostly role/operation clarification around selection. |

### Frontier Reinterpretation Finding

The potential finding under test is partially supported:

```text
Many recent frontiers were not discovering new objects.
They were discovering previously unnamed roles and operations.
```

The evidence supports this for attention target, attention trigger, selected,
active, working-state content, handoff content, frontier content, and parts of
selection rationale.

The evidence does not support reducing all recent frontiers to role and
operation confusion. Inquiry, frontier, working state, and handoff lineage also
raise genuine persistence questions:

```text
What unresolved context survives?
What lineage matters?
What must a future participant receive to continue safely?
Which findings, questions, gaps, and contradictions persist after an episode?
```

Therefore, the safest audit conclusion is:

```text
Recent frontiers likely exposed both things:
    genuinely missing preservation vocabulary,
    and object / role / operation category drift.
```

---

## Working State Evaluation

The Object, Role, and Operation Frontier suggested:

```text
working state
    =
objects
    +
roles
    +
operation context
```

Repository evidence supports this as an audit lens, not as a definition.

Working state appears to include objects:

```text
claims
questions
gaps
contradictions
findings
recommendations
frontiers
```

It also appears to include roles:

```text
active
selected
attention target
inquiry target
working-state content
handoff relevant
unresolved
blocked
```

And it appears to include operation context:

```text
what was being investigated
why this path was selected
what attention moved toward
what evidence had been consumed
what comparison, refinement, or correction remained incomplete
what next move would be safe
```

This lens explains why a handoff can preserve information but still lose
continuation alignment: the objects may survive while their roles and operation
context are missing.

The repository evidence contradicts a simpler view that working state is only a
bag of objects, only a set of roles, or only a process snapshot. It appears to be
composition-sensitive. However, implementation remains premature because the
repository has not settled which role or operation-context facts must be durable,
how long they last, or whether they belong to object lineage, role lineage,
operation lineage, handoff lineage, or documentation prose.

---

## Knowledge Representation Evaluation

The repository's knowledge model appears primarily object-centric in its mature
reconciled layer:

```text
observation
evidence
claim
fact
relationship
projection
assessment
recommendation
decision
command
capability
execution
action
handoff
```

This does not mean it ignores roles or operations. It means that the most stable
vocabulary has historically protected durable represented things and their
authority boundaries.

Role ontology appears less mature. The repository has strong recurring role
language, but it is mostly frontier or reconciliation-adjacent:

```text
selected
active
trigger
target
inquiry target
attention target
working-state content
handoff content
frontier content
handoff relevant
```

Operation ontology also appears less mature. The operations frontier gives a
strong candidate map, but it remains characterized rather than reconciled:

```text
acquisition
selection
attention
inquiry
derivation
comparison
interpretation
calculation
extrapolation
revision
refinement
correction
recommendation generation
```

Audit finding:

```text
The repository is more mature for object preservation and authority boundaries
than for role ontology or operation ontology.
```

This finding is consistent with the operations frontier and architectural-status
warnings. It should not be read as a request to create role or operation schemas.

---

## Category Drift Findings

The audit found several recurring category-drift patterns.

### 1. Object vs Role

An object's temporary participation is sometimes named as if it were identity.
Examples:

```text
question vs active question
gap vs attention target
contradiction vs trigger
claim vs selected claim
finding vs frontier content
```

The repository is increasingly careful about this, but older or neighboring
language can still blur it.

### 2. Role vs Operation

Roles and operations are frequently adjacent:

```text
selected vs selection
active vs attention
inquiry-target vs inquiry
handoff-content vs handoff selection
frontier-content vs frontier preservation
```

The drift occurs when a state caused by an operation is treated as the operation
itself, or when an operation's input role is treated as a durable object type.

### 3. Frontier Object vs Frontier Role

`Frontier` is the most category-dense term. It can mean:

```text
document artifact
unresolved investigation boundary
collection of questions, tensions, findings, candidates, and non-goals
preservation structure
target of attention
content role for unresolved material
```

The repository is not fully consistent here. It generally avoids implementation,
but it still relies on frontier language to preserve both objects and roles.

### 4. Question Object vs Inquiry Role

Questions can persist as represented artifacts, but they also occupy inquiry
roles. The repository has not settled whether questions are sufficient inquiry
objects or whether inquiry needs its own object family.

### 5. Contradiction Object vs Trigger Role

Contradictions can be represented incompatibilities or findings, but also strong
attention triggers and inquiry targets. The repository is careful to distinguish
contradiction discovery from contradiction existence, but trigger language still
creates drift risk.

### 6. Role Durability

Roles are contextual, yet some role assignments matter later. The repository has
not settled when role history should be preserved or what kind of lineage it is.

### 7. Role Lineage

An object may move through a path such as:

```text
trigger -> attention target -> inquiry target -> working-state content -> handoff content
```

The repository has not settled whether this is lineage of the object, lineage of
roles, lineage of operations, or handoff/continuation context.

### 8. Operation Lineage

Operations can produce objects, assign roles, revise objects, or expose
relationships. The repository has not settled whether operation history should be
durable as objects, provenance labels, support-edge roles, change events,
explanation categories, or prose.

### 9. Working State Composition

Working state language mixes object preservation, role preservation, and
operation context. This appears necessary for continuation but remains
unreconciled.

---

## Where The Repository Appears Internally Consistent

The repository appears most internally consistent in these areas:

1. **Claim-centered representation.** Claims remain central represented
   propositions, with observations, evidence, facts, relationships,
   projections, assessments, and explanations arranged around support and
   authority boundaries.
2. **Recommendation boundaries.** Recommendation objects remain distinct from
   recommendation generation, decision, command, execution, and action.
3. **Selection humility.** Selection does not mean truth, authority, priority,
   decision, recommendation, or execution.
4. **Attention role language.** Trigger and target increasingly behave as roles
   rather than standalone objects.
5. **Operation non-implementation.** Operation vocabulary is repeatedly kept
   separate from engines, workflows, runtime stages, schemas, and executors.
6. **Handoff caution.** Handoff documents preserve continuation alignment without
   becoming architecture authority.

---

## Where The Repository Appears Internally Mixed

The repository appears most mixed in these areas:

1. **Inquiry.** It is activity, possible lineage, possible object family,
   question pursuit, unresolved-state preservation, and handoff-resumable
   context.
2. **Frontier.** It is document, boundary, collection, preservation structure,
   target, and content context.
3. **Working state.** It contains objects, role assignments, active context,
   constraints, operation context, and next-safe-move information.
4. **Contradiction.** It is represented incompatibility, discovered finding,
   trigger, target, and handoff content.
5. **Evidence.** It is preserved support object and relative evidentiary role.
6. **Projection and assessment.** Each can name an object/view and a producing
   or evaluating operation.

These are the places where future reconciliation would need the most care.

---

## Required Tensions Preserved

The audit preserves the following tensions without resolving them:

| Tension | Current audit characterization |
| --- | --- |
| object vs role | Durable identity and contextual participation are different, but some concepts legitimately appear in both ways. |
| role vs operation | Roles are participation positions; operations assign, consume, or depend on them. The boundary is not always explicit. |
| frontier object vs frontier role | Frontier can be artifact, boundary, collection, preservation structure, target, or content role. |
| question object vs inquiry role | Question can persist, but active question and inquiry target are role-like. |
| contradiction object vs trigger role | Contradiction can persist as incompatibility or finding while also triggering attention. |
| role durability | Roles may be temporary but continuation can require preserving that they occurred. |
| role lineage | Movement among trigger, target, inquiry target, working-state content, and handoff content may matter. |
| operation lineage | Operation history may matter, but its representation form is unsettled. |
| working state composition | Working state appears to combine objects, roles, and operation context. |

---

## Why Implementation Remains Premature

Implementation remains premature because this audit found consistency signals,
not settled ontology.

The repository has not reconciled:

```text
whether object / role / operation is the final category set;
which roles require durable records;
whether role history is object lineage, role lineage, operation lineage, or handoff context;
whether operation history is represented object, provenance label, support-edge role, change event, explanation category, or prose;
whether inquiry is operation, object family, lineage structure, or hybrid;
whether attention is operation, episode, role assignment, or focus state;
whether frontier is object, role, collection, document artifact, or preservation structure;
whether working state should be modeled, documented, projected, or simply preserved in bounded handoffs.
```

A schema, runtime, role engine, workflow, operation executor, or universal
ontology would risk hard-coding distinctions that are still under audit.

---

## Audit Conclusion

The object / role / operation framing is useful as an architectural audit lens.
It explains several recurring repository patterns:

```text
Objects persist across episodes.
Roles explain contextual participation.
Operations explain what happens to, with, or over represented things.
```

Repository terminology is not uniformly consistent, but the inconsistency is
structured rather than random. Mature reconciled documents are mostly
object-centric and authority-boundary-centric. Recent frontiers appear to have
exposed less mature role and operation vocabulary, especially around attention,
selection, inquiry, working state, handoff lineage, and frontier preservation.

The strongest category-drift finding is that targets, triggers, selected status,
active status, working-state content, handoff content, and frontier content are
often participation roles occupied by existing objects, not independent object
families.

The strongest caution is that some recent frontiers also exposed genuine
persistence problems. Inquiry, working state, handoff lineage, frontier
preservation, contradiction, question, gap, and finding language cannot be
reduced to roles and operations only. Future participants need to know both what
persisted and how it participated.

Therefore the audit answer to the central question is:

```text
The repository has been most consistent about objects.
It has become increasingly aware of roles and operations.
It still mixes categories in inquiry, attention, frontier, working-state,
and handoff-lineage language.
The object / role / operation distinction is useful, but unreconciled.
Implementation remains premature.
```
