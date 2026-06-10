# Foundational Ontology Reconciliation

## Purpose

This document performs a documentation-only reconciliation of Seed's
foundational ontology after the reconciliation chain completed.

It is an architectural vocabulary and boundary audit.

It does not implement code, modify schemas, modify runtime behavior, modify
projections, observations, evidence handling, claims, events, recommendations,
decisions, capabilities, execution paths, handoffs, or tests.

It does not introduce new runtime semantics.

Its role is to identify the minimal stable vocabulary already implied by prior
reconciliations, not to create new architecture.

## Central Finding

Seed's foundational ontology is the smallest implementation-independent set of
architectural concepts needed to preserve Seed's core distinctions:

```text
Observations report.
Evidence preserves provenance.
Claims are the central knowledge primitive.
Facts normalize claims.
Relationships normalize connection claims.
Events preserve occurrences.
Changes preserve transitions.
States describe conditions over time.
Projections communicate selected knowledge.
Assessments interpret selected knowledge.
Recommendations advise.
Decisions select.
Commands request execution.
Capabilities describe possible work.
Executions attempt work.
Actions mutate reality.
Operators own intent.
Goals preserve purpose.
Policy constrains behavior.
Authority gates boundary crossings.
Trust, corroboration, verification, contradiction, causality, and explanation
qualify reasoning without becoming truth.
Handoffs preserve continuation alignment.
```

Therefore:

```text
Seed is claim-centric.
```

It is not fact-centric, entity-centric, goal-centric, or action-centric. Facts,
relationships, events, assessments, recommendations, decisions, capabilities,
actions, explanations, and handoffs all matter, but none displaces the claim as
the central represented proposition.

## Files Reviewed

This reconciliation reviewed the major reconciliation surfaces that repeatedly
introduced or refined the candidate primitives:

- `docs/architectural_documentation_alignment_reconciliation.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/event_and_change_reconciliation.md`
- `docs/operator_intent_question_and_claim_interface_reconciliation.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/goal_relevance_and_recommendation_generation_reconciliation.md`
- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/causality_and_explanation_reconciliation.md`
- `docs/explainability_reconciliation.md`
- `docs/handoff_alignment_guardrails_reconciliation.md`
- `docs/handoff_document_boundary_reconciliation.md`
- `docs/typed_projection_handoff_reconciliation.md`
- `docs/boundary_preservation_as_architectural_principle.md`
- `docs/knowledge_representation_reconciliation.md`
- `docs/knowledge_lifecycle_reconciliation.md`

## 1. What Is A Foundational Ontology?

A foundational ontology is Seed's stable architectural vocabulary for naming the
kinds of things Seed reasons about and the boundaries between them.

It is not a schema catalog. It is not an implementation plan. It is not a list
of classes, tables, endpoints, providers, adapters, or UI labels. It is the
conceptual layer that lets future architecture work ask:

```text
What kind of thing is this?
What question does it answer?
What authority does it carry?
What must it not be collapsed into?
```

### What Makes A Concept Foundational?

A concept belongs in the foundational ontology when it satisfies most or all of
these tests:

1. **Repeated emergence:** multiple reconciliations depend on the concept, even
   when discussing different subsystems.
2. **Boundary pressure:** collapsing the concept into a neighbor creates an
   architectural error.
3. **Authority relevance:** the concept changes what Seed may preserve,
   communicate, advise, decide, request, execute, or mutate.
4. **Explanation value:** the concept is needed to explain why Seed says,
   selects, recommends, or does something.
5. **Implementation independence:** the concept remains meaningful if today's
   storage models, projection caches, tool names, provider APIs, or UI surfaces
   change.
6. **Reconciliation stability:** later reconciliations refine the concept rather
   than replace it.

A concept is not foundational merely because it appears in code, has a field, is
a model name, or appears in a document title.

### Foundational Vocabulary Versus Implementation Vocabulary

Foundational vocabulary names architectural roles. Implementation vocabulary
names concrete mechanisms.

| Foundational vocabulary | Implementation vocabulary |
| --- | --- |
| Claim | Fact model, support record, fixture field, projection row |
| Evidence | Payload, source path, observed timestamp, event payload |
| Projection | Projection store, cache snapshot, current view endpoint |
| Capability | Tool registry entry, adapter method, provider integration |
| Command | Pending action record, executor request, tool call envelope |
| Handoff | Markdown handoff document, typed handoff payload, session summary |

Implementation vocabulary may realize, serialize, cache, expose, or test
foundational concepts. It must not define them exhaustively.

## 2. Foundational Concepts

The minimal foundational ontology contains the following concepts.

### Knowledge Concepts

| Concept | Foundational role | Primary question |
| --- | --- | --- |
| Observation | Source-attributed report | What did a source report from a vantage point at a time? |
| Evidence | Preserved provenance and support material | Why may Seed consider this claim? |
| Claim | Scoped proposition available for preservation, support, interpretation, or communication | What is being said? |
| Fact | Normalized provenance-backed claim | What proposition has Seed represented in normalized form? |
| Relationship | Normalized connection claim between things | What connection has Seed represented? |

Knowledge is the center of Seed's ontology. The claim is the central proposition.
Observations and evidence support claims. Facts and relationships normalize
claims into useful shapes. Projections later communicate selected knowledge.

### Temporal Concepts

| Concept | Foundational role | Primary question |
| --- | --- | --- |
| Event | Occurrence in the world or operational domain | What happened? |
| Change | Transition between distinguishable states or values | What became different? |
| State | Condition or value at a time or interval | What condition held, holds, or is selected for a scope? |

Temporal vocabulary is foundational because Seed must distinguish preserved
history from selected current state. Events can remain historically true after
state changes. Changes describe transitions rather than mere disagreement.

### Interpretation Concepts

| Concept | Foundational role | Primary question |
| --- | --- | --- |
| Projection | Selected read view over preserved knowledge | What view should be communicated for this purpose? |
| Assessment | Evidence-backed interpretation under a scoped evaluative frame | What does this knowledge indicate? |
| Consequence | Outcome, impact, or risk arising from a condition or occurrence | What did, could, or may result? |
| Recommendation | Advisory suggestion related to knowledge, goals, gaps, or questions | What could be considered? |
| Decision | Accepted, rejected, deferred, escalated, or chosen option | What has been selected under authority and constraints? |

Interpretation vocabulary is foundational because Seed must separate knowledge
communication from judgment, advice, commitment, and mutation.

### Operator Concepts

| Concept | Foundational role | Primary question |
| --- | --- | --- |
| Operator | Human, organization, or delegated principal engaging Seed | Who is engaging or authorizing Seed? |
| Intent | Operator purpose, concern, task, or motivation | Why is the operator engaging Seed? |
| Question | Interface bridge from operator intent to Seed's knowledge | What is being asked or investigated? |
| Goal | Operator-owned desired outcome or target state | What outcome is desirable? |
| Policy | Governance constraints, permissions, prohibitions, requirements, and preferences | What behavior is allowed, required, disallowed, or preferred? |
| Authority | Scoped power to decide, approve, request, execute, override, or communicate | Who or what may make this transition? |

Operator vocabulary is foundational because Seed must not silently invent
purpose, authority, or approval. Goals remain operator-owned even when Seed
represents them for reasoning.

### Execution Concepts

| Concept | Foundational role | Primary question |
| --- | --- | --- |
| Capability | Possible class of work, with optional support and verification context | What kind of work could be done? |
| Command | Authorized bounded request for work through a selected or resolvable path | What should be attempted now? |
| Execution | Attempted performance of a command through an execution path | What work was attempted? |
| Action | Runtime mutation of external reality or durable operational state | What changed or attempted to change reality? |

Execution vocabulary is foundational because Seed's architecture depends on a
strict boundary between knowing, advising, deciding, requesting, attempting, and
mutating.

### Reasoning Concepts

| Concept | Foundational role | Primary question |
| --- | --- | --- |
| Trust | Belief about reliability of a source or path in a scope | How reliable is this source path for this domain? |
| Corroboration | Compatible support from multiple pieces of evidence | How much repeated or independent support exists? |
| Verification | Confirmation of a scoped question under a defined method | What has been checked, by what method, in what scope? |
| Contradiction | Incompatible claims or evidence under relevant scope | What cannot simultaneously hold under the same interpretation? |
| Causality | Claim that something produced or influenced something else | What caused or influenced what? |
| Explanation | Communication of why Seed presented, selected, assessed, recommended, or did something | Why is Seed saying this? |

Reasoning vocabulary is foundational because Seed needs to communicate support,
uncertainty, conflict, and rationale without turning every rationale into proof,
truth, or causation.

### Continuation Concept

| Concept | Foundational role | Primary question |
| --- | --- | --- |
| Handoff | Continuation artifact preserving alignment across sessions or actors | What must remain active so future work continues safely? |

Handoff is foundational at the continuation boundary, not because it defines
Seed's architecture, but because prior reconciliations showed that preserved
knowledge can be unsafe without preserved guardrails and working-set alignment.

## 3. Required Concept Boundaries

Seed's ontology is boundary-preserving. The following distinctions are
foundational because collapsing them has repeatedly produced or risked
architectural error.

### Claim != Fact

A claim is the proposition being represented or interpreted. A fact is a
normalized, provenance-backed claim form. Facts are important implementation and
knowledge-shape surfaces, but Seed is not fact-centric because the proposition
can also appear in observations, relationships, assessments, explanations, or
history.

### Fact != Truth

A fact is a normalized claim with support and scope. It is not universal truth,
current truth, live verification, or timeless reality. Facts may be stale,
contradicted, uncorroborated, historical, or selected differently by different
projections.

### Relationship != Identity

A relationship records a represented connection between things. It does not by
itself prove that the related things are the same entity, that one owns the
other, that one causes the other, or that one controls the other. Identity,
ownership, dependency, and causality require stronger or different support.

### Event != State

An event is an occurrence. State is a condition or value at a time or interval.
A service can stop as an event and later be running as current state. The event
remains part of history even when the selected state changes.

### Change != Contradiction

A change is a transition between before and after states or values. A
contradiction is incompatible support under a relevant scope. Different values at
different times may be a valid change rather than a conflict.

### Projection != Authority

A projection selects and communicates preserved knowledge. It does not create
operator approval, policy authorization, truth, execution permission, or
remediation choice. A projection may expose authority records; it is not the
authority merely by exposing them.

### Assessment != Recommendation

An assessment interprets knowledge: risk, sufficiency, drift, weakness,
contradiction, or significance. A recommendation suggests a possible response.
`Low disk space detected` is not the same as `investigate storage usage`.

### Recommendation != Decision

A recommendation is advisory. A decision accepts, rejects, defers, escalates, or
selects under authority. Recommendations can exist without authority to execute
and without an accepted choice.

### Decision != Command

A decision records selection or commitment. A command is a bounded request to
attempt work with target, arguments, scope, constraints, capability path, and
authority. A decision may approve investigation without yet forming an executable
request.

### Capability != Execution

A capability says work may be possible. Execution attempts work through a
concrete path. Capability availability is not a recommendation, decision,
command, provider adoption, trust assertion, or proof that anything happened.

### Explanation != Causality

Explanation communicates why Seed presented, selected, assessed, recommended,
or acted. Causality asserts production or influence between things. An
explanation may cite evidence, freshness, selection rationale, conflicts,
policy, or goals without making a causal claim.

### Handoff != Architecture

A handoff preserves continuation alignment. It is not architectural authority,
proof of correctness, implementation, or replacement for source documents. It
should carry enough active context and guardrails to prevent drift, but it must
not become the architecture itself.

## 4. Ontology Planes

Prior reconciliations justify organizing the foundational vocabulary into planes.
The planes are not runtime modules, schemas, services, or ownership claims. They
are conceptual regions that clarify which question a concept primarily answers.

### Knowledge Plane

```text
Observation -> Evidence -> Claim -> Fact / Relationship
```

The Knowledge Plane preserves what Seed may know or consider. It is centered on
claims, with observations as reports, evidence as provenance, facts as
normalized claims, and relationships as normalized connection claims.

### Temporal Plane

```text
Event -> Change -> State
```

The Temporal Plane preserves time-sensitive distinction: occurrences, transitions,
and conditions. It prevents history from being overwritten by current views and
prevents ordinary temporal succession from being mislabeled contradiction.

### Interpretation Plane

```text
Projection -> Assessment -> Consequence -> Recommendation -> Decision
```

The Interpretation Plane moves from selected knowledge toward meaning, impact,
advice, and selection. The plane is justified because prior reconciliations
repeatedly separated communication, interpretation, recommendation, and decision
authority.

### Operator Plane

```text
Operator -> Intent -> Question -> Goal -> Policy -> Authority
```

The Operator Plane preserves purpose and permission. It prevents Seed from
silently inventing objectives, treating questions as facts, treating goals as
commands, or treating policy text as execution authority by itself.

### Execution Plane

```text
Capability -> Command -> Execution -> Action
```

The Execution Plane preserves the distance between possible work and changed
reality. It is where advice becomes bounded work only after decision, policy,
capability support, approval, and execution-path constraints are satisfied.

### Reasoning Plane

```text
Trust / Corroboration / Verification / Contradiction / Causality / Explanation
```

The Reasoning Plane qualifies claims, selections, assessments, recommendations,
and actions. These concepts cut across the other planes: evidence can be
corroborated, sources can be trusted in scope, claims can be verified or
contradicted, events can participate in causal claims, and many surfaces require
explanation.

### Continuation Plane

```text
Handoff
```

The Continuation Plane preserves active alignment across time, sessions, and
actors. It exists because Seed work can fail when conclusions are preserved but
applicability guardrails are not.

## 5. The Center Of The Ontology

Seed is **claim-centric**.

It is not primarily:

- **fact-centric**, because facts are normalized claim forms rather than truth or
  final authority;
- **entity-centric**, because entity identity and relationships are important but
  not the root of knowledge representation;
- **goal-centric**, because goals preserve operator purpose but do not define
  what Seed knows;
- **action-centric**, because actions are tightly bounded mutation effects, not
  the source of knowledge authority;
- **projection-centric**, because projections communicate selected knowledge but
  do not own preserved history or authority;
- **LLM-centric**, because model output is neither the ontology nor the source of
  truth.

The claim is the center because it is the thing that can be reported, supported,
normalized, related, selected, assessed, contradicted, verified, explained, and
communicated.

## 6. What Should Not Be Included

The foundational ontology should exclude concepts that are implementation,
runtime, storage, provider, UI, or schema details unless they are being discussed
as examples of how foundational concepts are realized.

### Implementation Details

Do not include specific class names, function names, fixtures, serializers,
validators, ranking implementations, graph generators, or test helpers as
foundational concepts. They may implement or test the ontology; they are not the
ontology.

### Runtime Details

Do not include specific runtime loops, executor internals, scheduling mechanics,
cache refresh mechanics, subprocess mechanics, or dispatch strategies as
foundational concepts. Runtime behavior must respect concepts such as command,
execution, action, policy, and authority, but it does not define them.

### Storage Details

Do not include tables, event payload layouts, projection cache formats, file
paths, indexes, migrations, or database engines as foundational concepts.
Storage preserves architectural things; it does not decide what they are.

### Schema Details

Do not include individual fields, enum spellings, JSON shapes, or type names as
foundational concepts unless a separate reconciliation has already elevated the
underlying architectural distinction. Schema can encode ontology, but schema
should not be mistaken for ontology.

### Provider Details

Do not include specific providers, external APIs, package managers, Prometheus
servers, web search tools, local shell commands, or adapter libraries as
foundational concepts. Provider identity belongs below the capability, execution
path, trust, adoption, and authority boundaries.

### UI Details

Do not include screens, menus, labels, prompts, cards, forms, or visual layout as
foundational concepts. UI may communicate projections, assessments,
recommendations, explanations, decisions, commands, and handoffs, but it does not
make those concepts foundational.

## 7. Ontology And Implementation

### Does Ontology Dictate Implementation?

Ontology constrains implementation, but it does not dictate a single
implementation.

For example, the ontology says recommendation and decision must remain distinct.
It does not require a particular table, class hierarchy, service name, or UI
workflow for representing that distinction.

### Does Implementation Define Ontology?

Implementation can reveal missing distinctions, but it does not define the
ontology by accident.

If a current model named `Fact` stores normalized claims, that does not make Seed
fact-centric. If a projection cache exposes current state, that does not give the
cache authority over history. If a tool can execute work, that does not make
capability equivalent to execution or action.

### How Should Future Implementation Relate To Ontology?

Future implementation work should use the foundational ontology as a boundary
checklist:

1. Identify which foundational concept is being represented or crossed.
2. Preserve neighboring boundaries explicitly.
3. Avoid using implementation names to imply stronger authority than the concept
   carries.
4. Ensure provenance and explanation remain available where the concept requires
   them.
5. Treat new runtime behavior as an implementation of established boundaries,
   not as an implicit ontology change.
6. Create a new reconciliation before introducing a new foundational primitive.

## 8. Architectural Invariants Supported By This Reconciliation

This reconciliation supports the following stable invariants:

```text
Claims are the central knowledge primitive.
Facts are normalized claim forms.
Relationships are normalized connection claims.
Facts are not truth.
Relationships are not identity.
Events preserve history.
Changes preserve transitions.
State is selected or scoped condition, not the whole history.
Projections communicate selected knowledge.
Projection is not authority.
Assessments interpret knowledge.
Recommendations are advisory.
Decisions are distinct from recommendations.
Commands are distinct from decisions.
Capabilities preserve possibility.
Execution attempts work.
Actions change reality.
Goals preserve operator purpose.
Policy constrains acceptable behavior.
Authority gates boundary crossings.
Trust is not truth.
Corroboration is not authority.
Verification is scoped confirmation, not universal truth.
Contradiction is not ordinary change.
Causality is not explanation.
Explanations communicate understanding.
Handoffs preserve continuation alignment.
Foundational ontology remains implementation-independent.
```

## 9. Non-Goals

This document does not:

- add, remove, or rename runtime concepts;
- require schema changes;
- require projection changes;
- define a new storage model;
- define a new reasoning engine;
- authorize new execution behavior;
- introduce new provider, tool, or adapter semantics;
- prescribe UI behavior;
- rank implementation work;
- create a roadmap;
- supersede the detailed reconciliation documents that define each boundary in
  depth.

## 10. Summary

Seed's foundational ontology is a compact, boundary-preserving vocabulary for a
claim-centric architecture.

The ontology is stable because the same primitives recur across independent
reconciliations: knowledge preservation, temporal history, interpretation,
operator purpose, execution boundaries, reasoning support, and continuation
alignment.

The most important outcome is not the list itself. The most important outcome is
the discipline it encodes:

```text
Preserve architectural distinctions until evidence and authority justify crossing
them.
```
