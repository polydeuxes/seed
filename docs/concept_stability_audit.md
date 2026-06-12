---
doc_type: audit
status: exploratory
domain: concept stability
defines:
  - concept stability audit
  - stable concept candidate
  - unstable concept candidate
  - recurring concept candidate
  - load-bearing concept candidate
  - concept under pressure
  - concept stability indicators
  - concept instability indicators
depends_on:
  - object_role_and_operation_frontier.md
  - object_role_operation_consistency_audit.md
  - object_role_operation_pressure_test.md
  - persistence_frontier.md
  - continuity_frontier.md
  - relationship_frontier.md
  - current_work_position_frontier.md
  - active_edge_frontier.md
  - inquiry_frontier.md
  - selection_and_attention_frontier.md
  - attention_trigger_frontier.md
  - attention_target_frontier.md
  - handoff_and_continuation_lineage_frontier.md
  - foundational_ontology_reconciliation.md
  - architectural_status_and_next_frontier.md
related:
  - operations_frontier.md
  - operation_attribution_frontier.md
  - derivation_frontier.md
  - knowledge_navigation_layers_frontier.md
  - architectural_findings_preservation.md
---

# Concept Stability Audit

## Purpose

This document audits whether concepts recurring across recent frontier work appear
stable, unstable, transformed, recurring, load-bearing, or still under pressure.

It is documentation only. It does not implement code, modify schemas, modify
runtime behavior, add tests, design an ontology registry, standardize vocabulary,
create taxonomy rules, or promote any concept to canonical architecture.

This is not a reconciliation. Repository authority remains with scoped
reconciliation documents, existing vocabulary documents, and the current
architectural status document. Frontier documents remain exploratory unless a
later reconciliation promotes specific findings.

The central question is:

```text
Which concepts appear stable, which repeatedly dissolve, which repeatedly
reappear, and which now appear load-bearing for explaining other findings?
```

Stability in this document does not mean correctness. Instability does not mean
failure. Recurrence does not mean importance by itself. Load-bearing use does not
create implementation authority.

---

## Evidence Base Reviewed

This audit reviewed the repository's recent frontier and audit work around:

- object, role, operation, and relationship pressure;
- persistence, continuity, current work position, active edge, and handoff
  lineage;
- inquiry, selection, attention trigger, and attention target;
- foundational ontology and current architectural status.

The most important authority constraint is that the current status document
classifies these recent documents as exploratory, characterized, or not
implementation-ready unless a later reconciliation promotes them. This audit
therefore evaluates stability evidence without standardizing terms.

---

## Method

The audit uses five non-exclusive labels:

| Label | Meaning in this audit | What it does not mean |
| --- | --- | --- |
| Stable candidate | A concept has repeated independent support, clearer boundaries, or survival through pressure. | Correct, canonical, reconciled, or implementation-ready. |
| Unstable candidate | A concept repeatedly changes meaning, is replaced, or depends on unresolved distinctions. | Useless, false, or failed. |
| Transformed candidate | Investigation changed the concept into a more precise neighboring concept. | The original concept was wrong. |
| Recurring candidate | A concept appears across unrelated investigations. | It is necessarily foundational or important. |
| Load-bearing candidate | Other findings currently rely on it for explanation. | It should become a top-level ontology category. |

The audit treats these as evidence labels, not taxonomy standards. A concept can
be stable and under pressure, recurring and unstable, or load-bearing without
being reconciled.

---

## Candidate Indicators

### Stability Indicators

Candidate stability indicators observed across the documents include:

1. repeated independent appearance in different investigations;
2. explanatory power over multiple problem families;
3. survival through pressure tests or audit follow-up;
4. resistance to reduction into a neighboring concept;
5. recurring repository usage in authoritative or exploratory documents;
6. ability to explain why other findings remain unresolved;
7. ability to preserve authority boundaries instead of erasing them.

These indicators are neither necessary nor sufficient. They are especially weak
when a recurring term is overloaded.

### Instability Indicators

Candidate instability indicators include:

1. repeated replacement by another concept;
2. repeated redefinition across documents;
3. drift between object, role, operation, relationship, state, lineage, and
   artifact meanings;
4. dependency on concepts that are themselves unresolved;
5. category confusion between durable identity and episode-relative
   participation;
6. inability to explain handoff, authority, support, or continuation failures;
7. implementation temptation before the concept's boundary is settled.

---

## Concept Evaluations

### Object

`Object` appears relatively stable as a diagnostic contrast: some things must be
preserved as represented items with evidence, identity, support, or lineage.
Foundational ontology remains claim-centered and evidence-bounded, and the
object/role/operation work repeatedly warns against demoting established objects
just because they participate in episodes.

However, object is not stable as a universal answer. The pressure test found
that support, identity, authority, frontier, evidence, and working state become
overloaded if everything durable is treated as an object. Object is therefore a
stable contrast concept, not a complete ontology.

Audit label: stable candidate; load-bearing candidate; still under pressure.

### Role

`Role` became more stable through investigation because it explains why a claim,
question, contradiction, frontier, or relationship can function differently in a
particular episode without becoming a new object type. Attention target,
attention trigger, inquiry object, selected item, active item, and handoff
content all show role-like behavior.

Role remains unstable at its boundary with operation and relationship. Some roles
are momentary participation states; others have lineage or authority effects.
The repository has not reconciled role durability or role lineage.

Audit label: transformed/stabilizing candidate; recurring candidate; still under
pressure.

### Operation

`Operation` is stable as a warning that activity should not be confused with the
thing acted on. It helps separate observing from evidence, selecting from
selected content, handing off from a handoff artifact, and continuing from the
preserved context.

Operation is unstable as a target for implementation. The operations frontier and
object/role/operation audits repeatedly warn that not every verb should become a
runtime operation, executor, workflow step, or object. Operation remains useful
as an analytic lens but not as a settled runtime model.

Audit label: stable diagnostic candidate; unstable implementation candidate;
still under pressure.

### Relationship

`Relationship` is one of the strongest recurring and load-bearing concepts in
the evidence base. It appears in support, contradiction, corroboration, identity,
authority, dependency, trust, adoption, recommendation, continuation, active
edge, and working-state usefulness. The pressure test found relationship to be
the strongest falsification candidate for a pure object/role/operation lens.

That recurrence does not by itself prove that relationship is a canonical fourth
category. Relationship may be an object with edge semantics, a relationship
claim, a projection, a role-with-target, an operation result, or a distinct
modeling category. The important stability finding is narrower: the repository
cannot explain several core findings without edge semantics.

Audit label: strongest recurring candidate; strongest load-bearing candidate;
stable as pressure signal; still unresolved as ontology category.

### Continuity

`Continuity` appears to be the main transformation product of the persistence
investigation. Persistence started as a question about what survives. The later
continuity frontier sharpened that question by separating continuity from
identity, persistence, and lineage.

Continuity therefore looks more stable than persistence as an explanatory term
for recognizable survival through revision, inquiry movement, and handoff
resumption. It remains under pressure because the repository has not reconciled
whether continuity is a property of objects, relationships, inquiry lineage,
work positions, or future participant recognition.

Audit label: transformed/stabilizing candidate; load-bearing candidate; still
under pressure.

### Persistence

`Persistence` did not fail. It transformed. The persistence frontier rejected
naive equations such as persistence equals storage or persistence equals
identity. It exposed that what survives may be a represented item, relationship,
unresolved pressure, purpose, lineage, or compound working position.

Persistence is less stable than continuity because its boundary remains broad and
because multiple later concepts absorb parts of its explanatory load.
Nevertheless, it remains load-bearing as the question that revealed why storage,
identity, role participation, inquiry lineage, and continuation cannot be
collapsed.

Audit label: transformed candidate; unstable broad concept; load-bearing
question; still under pressure.

### Inquiry

`Inquiry` recurs wherever questions, gaps, tensions, findings, frontiers,
continuation, and attention are discussed. It appears necessary for explaining
unresolved pursuit and investigation lineage rather than only settled claims.

Inquiry remains unstable because the repository has not decided whether inquiry
has objects, state, lifecycle, branches, lineage, operations, or only processes
over existing objects. It is load-bearing for explaining why findings, gaps, and
frontiers can remain active without becoming implementation tasks.

Audit label: recurring candidate; load-bearing candidate; unstable ontology
candidate; still under pressure.

### Current Work Position

`Current work position` is the strongest transformation of older working-state
language. What survived the working-state investigation was not a simple
persistent object but a compound position: selected active context, unresolved
pressure, safe next movement, authority constraints, validation state, and
continuation relevance.

The concept appears stable as a corrective to preserved-information thinking.
It remains under pressure because it depends on selection, attention, inquiry,
continuity, authority, and active edge, all of which remain partly unsettled.

Audit label: transformed/stabilizing candidate; load-bearing candidate; still
under pressure.

### Active Edge

`Active edge` appears useful for naming what currently pulls work forward among
preserved questions, gaps, contradictions, tensions, relationships, frontiers,
risks, ambiguities, findings, and recommendations. It explains why a repository
can contain many unresolved items while only some are presently pulling action.

Active edge is still dissolving at its boundaries. It may be a role, state,
selection result, attention condition, inquiry position, frontier condition,
current-work-position component, or relationship among pressures. Its strength is
that it exposes the boundary; its instability is that it has not survived enough
reduction tests to become settled.

Audit label: recurring/still-emerging candidate; strong concept under pressure;
not yet stable.

### Attention

`Attention` became more stable by splitting into trigger and target questions.
Attention trigger explains why attention moves. Attention target explains what
receives attention. This split prevented collapse among goals, needs, gaps,
tensions, questions, contradictions, frontiers, selection, priority, authority,
and inquiry.

Attention remains unstable as an architecture concept because attention movement
is not truth, priority, selection, authority, acquisition origin, or execution
permission. It is stable as a pressure family and unstable as a system boundary.

Audit label: transformed/stabilizing family; recurring candidate; still under
pressure.

### Selection

`Selection` is comparatively stable in existing repository authority as a
knowledge-selection concern and as a contrast with attention. Selection helps
explain chosen context and rationale without equating selection with truth,
priority, authority, or active attention.

Selection remains under pressure where it intersects with current work position,
active edge, attention target, handoff preservation, and continuation. Its
stability comes from existing reconciliation and vocabulary work; its frontier
pressure comes from newer attention and work-position questions.

Audit label: stable candidate in scoped authority; load-bearing contrast; still
under pressure at frontier boundaries.

### Frontier

`Frontier` is highly recurring and highly overloaded. It can mean a document,
an unresolved boundary, an active investigation edge, a collection of pressures,
a preserved non-final finding set, or a role-like condition around a concept.

Frontier appears stable as a repository document family and as a warning that an
area is not reconciled. It is unstable as an ontology concept because frontier
identity, continuity, active status, and relationship to inquiry are unresolved.

Audit label: recurring candidate; stable document-role candidate; unstable
ontology candidate; still under pressure.

### Contradiction

`Contradiction` is stable in reconciled authority as a distinction among
existence, discovery, visibility, explanation, and resolution. It repeatedly
appears as an attention trigger, active-edge pressure, persistence/continuity
candidate, inquiry driver, and relationship-like condition among claims.

Its remaining pressure is not whether contradictions matter, but which role they
play in a particular episode: object of inquiry, relationship between claims,
attention trigger, integrity issue, handoff content, or active edge.

Audit label: stable reconciled candidate; recurring candidate; load-bearing
integrity candidate; role boundary under pressure.

### Gap

`Gap` recurs across inquiry, persistence, continuity, attention, active edge, and
current work position. It explains absence or insufficiency that can pull work
forward without itself being a settled claim.

Gap is unstable because it can be passive, active, evidentiary, inquiry-forming,
attention-triggering, or frontier-preserving depending on context. A gap may
persist, transform into a question, dissolve after evidence appears, or become a
finding.

Audit label: recurring candidate; unstable/transformed candidate; still under
pressure.

### Finding

`Finding` appears stable as a documentation and audit outcome: something learned
or characterized during investigation. It is load-bearing because frontiers and
audits preserve findings without necessarily reconciling them.

Finding remains unstable at the boundary between observation, claim, conclusion,
recommendation, frontier pressure, and authority. A finding can be provisional,
scoped, falsifying, preserved, superseded, or later promoted by reconciliation.

Audit label: recurring candidate; stable preservation concept; authority
boundary under pressure.

### Authority

`Authority` is stable as a boundary-preserving concept. Many documents rely on
it to prevent collapse between documentation, handoff, selection, visibility,
triggering, recommendation, implementation, and truth. Repository authority is
especially load-bearing in keeping frontier work from becoming canonical by
accident.

Authority is also overloaded. It can mean source authority, policy permission,
operator authority, documentation authority, scope boundary, adoption authority,
execution permission, or evidence trust. The pressure test found authority to
require scoped relations among actor, action, object, policy, and state.

Audit label: strongest load-bearing boundary concept; stable as constraint;
unstable/overloaded internally; still under pressure.

---

## Critical Examples

### Example 1: Persistence Produced Continuity

Persistence did not fail. It exposed that survival is not storage and not strict
identity. Continuity then refined the question toward recognizable survival
through change, revision, and handoff resumption.

The transformation suggests that persistence was a productive frontier question,
while continuity is currently the more precise explanatory candidate. Both remain
unreconciled.

### Example 2: Working State Produced Current Work Position

Working state did not survive cleanly as a simple object. The stable residue is
current work position: what is selected, unresolved, safe to continue, bounded by
authority, and active now.

What survived was not all preserved information. What survived was a compound
orientation for continuation.

### Example 3: Attention Split Into Trigger And Target

Attention remained useful only after separating why attention moves from what
attention lands on. Trigger and target both behave partly like roles over
existing objects and partly like frontier pressures.

The stable finding is the separation. The unstable finding is whether attention
itself is an ontology object, state, operation, role, or explanatory lens.

### Example 4: Relationship Reappeared Across Investigations

Relationship reappeared in identity, support, authority, contradiction,
continuity, active edge, handoff lineage, and object/role/operation pressure
work. This recurrence is stronger than mere vocabulary repetition because many
findings became harder to explain without scoped edge semantics.

The audit does not infer that relationship is canonical. It infers that edge
semantics are load-bearing in current repository explanations.

### Example 5: Active Edge Remains Under Pressure

Active edge explains a real recurring problem: many things can be preserved, but
only some currently pull work forward. However, it is still unclear whether
active edge is a role, state, selection result, attention result, inquiry edge,
frontier condition, or current-work-position component.

Active edge is therefore one of the strongest concepts still under pressure.

---

## Required Findings

### Strongest Stability Candidates

1. `authority` as a boundary constraint;
2. `relationship` as recurring edge-semantics pressure;
3. `selection` as a scoped knowledge-selection concern and contrast with
   attention;
4. `contradiction` as a reconciled integrity concept with episode-relative roles;
5. `object` as a durable-representation contrast, not as universal ontology;
6. `continuity` as the refined survival-through-change concept;
7. `current work position` as the refined working-state concept.

### Strongest Instability Candidates

1. `persistence` as a broad concept when treated as storage, identity, or a
   single property;
2. `active edge` as a still-dissolving boundary among attention, inquiry,
   selection, frontier, and work position;
3. `frontier` as an ontology concept beyond its document/navigation role;
4. `gap` where it shifts among absence, question, trigger, active pressure, and
   finding input;
5. `authority` internally, because the same term spans source trust, policy,
   permission, adoption, execution, and documentation boundaries;
6. `operation` when prematurely interpreted as runtime machinery.

### Strongest Recurring Concepts

1. `relationship`;
2. `authority`;
3. `frontier`;
4. `inquiry`;
5. `gap`;
6. `contradiction`;
7. `attention`;
8. `selection`;
9. `finding`;
10. `continuity`.

### Strongest Load-Bearing Concepts

1. `authority`, because it keeps exploratory work, handoffs, selection,
   implementation, and truth claims from collapsing;
2. `relationship`, because support, contradiction, identity, dependency,
   lineage, working state, and authority need edge semantics;
3. `continuity`, because handoff, persistence, inquiry evolution, and work
   resumption need survival-through-change language;
4. `current work position`, because safe continuation requires more than
   preserved information;
5. `selection`, because context, attention, and continuation need a way to say
   what is chosen without asserting truth or priority;
6. `inquiry`, because unresolved pursuit and frontier preservation cannot be
   explained only by settled claims;
7. `contradiction`, because integrity and active pressure depend on separating
   existence, discovery, visibility, and resolution.

### Strongest Concepts Still Under Pressure

1. `active edge`;
2. `persistence`;
3. `frontier` as ontology rather than document family;
4. `inquiry` as object/process/lineage/lifecycle;
5. `attention` as trigger/target/state/role/operation;
6. `role` durability and lineage;
7. `operation` outside analytic use;
8. `authority` as a scoped relation rather than overloaded label;
9. `relationship` as category, object subtype, claim, role, or projection.

---

## Unresolved Tensions

| Tension | Current audit characterization |
| --- | --- |
| Stability vs correctness | A term can be stable because it reliably preserves a boundary, even if its deeper ontology remains unsettled. |
| Recurrence vs importance | Relationship and frontier recur often, but recurrence becomes meaningful only when the concept explains otherwise unresolved findings. |
| Persistence vs continuity | Persistence was productive as a question; continuity is the stronger refinement for survival through change. |
| Work position vs active edge | Current work position is a compound orientation for continuation; active edge is the pull within or around that position. The boundary remains unsettled. |
| Relationship vs object/role/operation | Object/role/operation explains participation confusion; relationship explains scoped directed connections the three-part lens strains to express. |
| Inquiry vs active edge | Inquiry preserves unresolved pursuit; active edge marks what currently pulls pursuit forward. They overlap but are not identical. |
| Authority stability | Authority is stable as a constraint and unstable as a term spanning source trust, policy, permission, adoption, documentation, and execution. |
| Attention vs selection | Attention explains movement or focus; selection explains chosen context or rationale. Each can influence the other without containing the other. |
| Frontier as document vs frontier as pressure | Frontier documents are navigable artifacts; frontier pressure may continue, transform, become dormant, or be reconciled. |
| Finding vs reconciliation | Findings can be preserved without becoming authoritative reconciliations. |

---

## Why Implementation Remains Premature

Implementation remains premature because this audit found stability signals, not
settled ontology. The repository still lacks reconciled answers to questions
such as:

1. whether relationship is a distinct category or a claim/object pattern with
   edge semantics;
2. whether role assignments can persist or have lineage;
3. whether continuity attaches to objects, relationships, inquiry lineages,
   work-position structures, or future recognition;
4. whether active edge is a role, state, relation, selection result, attention
   result, or inquiry condition;
5. how authority should be scoped when source trust, permission, adoption,
   documentation authority, and execution authority all appear;
6. how findings move, if at all, from exploratory audit output to reconciled
   authority.

A schema, runtime, planner, workflow engine, attention engine, inquiry engine,
identifier system, or canonical vocabulary would freeze concepts that are still
being used to expose boundaries.

---

## Non-Goals

This audit does not:

- reconcile ontology;
- standardize vocabulary;
- create canonical concept categories;
- define schemas, identifiers, lifecycle states, registries, or graph models;
- propose runtime behavior, engines, workflows, planners, prioritizers, or
  schedulers;
- replace foundational ontology or scoped reconciliations;
- promote any frontier finding to implementation authority;
- decide whether relationship is a fourth top-level category;
- decide whether active edge, inquiry, continuity, attention, or current work
  position should become represented objects.

---

## Final Characterization

Recent frontier work shows a pattern:

```text
Some concepts stabilize as boundary protectors.
Some concepts transform into sharper neighboring concepts.
Some concepts recur because many findings need them.
Some concepts remain valuable precisely because they are still under pressure.
```

The strongest stability candidates are not necessarily the most finished
ontology. Authority, relationship, continuity, selection, contradiction, object,
and current work position appear stable enough to explain repeated findings, but
not stable enough to justify new implementation machinery.

The strongest instability candidates are not failures. Persistence, active edge,
frontier, gap, inquiry, attention, role durability, operation, and authority
scope are productive instability zones: they reveal where existing language is
still doing exploratory work.

The most important audit result is that implementation remains premature because
concept stability is uneven. Future participants should preserve these findings
as orientation, not as canonical vocabulary or architecture.
