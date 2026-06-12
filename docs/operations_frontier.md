---
doc_type: frontier
status: exploratory
domain: operations ontology
defines:
  - operations frontier
  - knowledge operation
  - object operation boundary
  - derivation as candidate operation
  - learning operation relationship
depends_on:
  - derivation_frontier.md
  - knowledge_change_and_revision_reconciliation.md
  - foundational_ontology_reconciliation.md
  - knowledge_navigation_layers_frontier.md
  - learning_and_knowledge_change_reconciliation.md
  - observation_evidence_change_event_reconciliation.md
  - architectural_status_and_next_frontier.md
related:
  - contradiction_discovery_and_visibility_reconciliation.md
  - prediction_forecasting_and_future_claims_reconciliation.md
  - recommendation_selection_boundary.md
  - relationship_fact_reconciliation.md
  - operation_support_boundary_reconciliation.md
---

# Operations Frontier

## Purpose

This document characterizes a possible frontier in Seed's ontology:
represented knowledge may not only consist of objects such as observations,
evidence, claims, relationships, assessments, forecasts, recommendations, and
projections. It may also require names for things that happen to, between, or
over those objects.

It is documentation only. It does not implement code, modify schemas, modify
runtime behavior, add tests, define an executor, design a planner, introduce a
workflow, describe a pipeline, define a state machine, or prescribe runtime
stages.

Repository authority wins over this document. The existing observation,
evidence, change, event, learning, foundational ontology, derivation,
navigation, forecasting, contradiction, recommendation, projection, and
architectural-status documents remain authoritative for their own reconciled
boundaries.

The question here is exploratory:

```text
What are the fundamental operations over represented knowledge?
```

The document does not assume that the answer is known, that operations form a
pipeline, that operations correspond to implementation components, or that the
candidate vocabulary below is complete.

---

## Background Finding

Recent reconciliations repeatedly exposed a pattern:

```text
Seed has developed a rich ontology for what is represented.
Seed has less settled vocabulary for what happens to represented knowledge.
```

The object vocabulary is already substantial:

```text
observation
evidence
claim
relationship
support
projection
caveat
assessment
forecast
recommendation
```

Several recent frontier and reconciliation documents then encountered adjacent
verbs or event-like concepts:

```text
acquire
compare
interpret
derive
calculate
extrapolate
corroborate
revise
refine
correct
replace
select
project
reconcile
classify
qualify
navigate
```

The derivation frontier captured one version of the pattern: represented
knowledge may sometimes become support for additional represented knowledge.
That finding appears real. But the repeated tensions around derivation suggest
that derivation may not be primitive. It may be one member of a larger family of
knowledge operations.

---

## Central Hypothesis Under Test

The working hypothesis is:

```text
Seed may have discovered an Operations Frontier.
```

A tentative distinction is:

```text
Objects answer:    "What is represented?"
Operations answer: "What happened to represented knowledge?"
```

This distinction is useful, but not yet reconciled. It must be tested rather
than assumed. Some nouns in the current ontology, such as `change`, `event`,
`projection`, and `support`, already sit near the boundary between represented
object and operation. Some operations may leave no durable object of their own.
Some objects may preserve the result of an operation without representing the
operation itself.

A safer current formulation is:

```text
Knowledge objects are represented entities, propositions, relations, supports,
views, qualifications, and conclusions.

Knowledge operations are explainable acts, recognitions, transformations,
selections, or recharacterizations involving those represented objects.
```

This is not an implementation model. It is an ontology question.

---

## Object Versus Operation

### Candidate Knowledge Objects

Candidate knowledge objects include:

| Object | What it appears to represent |
| --- | --- |
| Observation | What was observed from a source or vantage point. |
| Evidence | Preserved support connecting observations, testimony, or sources to later understanding. |
| Claim | A supported proposition with scope, subject, predicate, value, time, modality, or qualification. |
| Relationship | A represented connection between represented things. |
| Support | The explainable connection by which one object justifies, backs, or contextualizes another. |
| Assessment | An evaluative characterization supported by evidence, claims, criteria, or context. |
| Forecast | A future-oriented claim or conclusion supported by present or historical knowledge and assumptions. |
| Recommendation | A suggested course of action or option, distinct from decision, command, and execution. |
| Projection | A selected, materialized, or presented view over preserved knowledge. |
| Caveat | A limitation, uncertainty, scope warning, or qualification attached to represented understanding. |

These are not all the same kind of object. Some are source-facing, some are
support-facing, some are conclusion-facing, and some are view-facing. The common
feature is that they can be represented, cited, selected, explained, or
preserved.

### Candidate Knowledge Operations

Candidate operations include:

| Operation | Candidate characterization | Status |
| --- | --- | --- |
| Acquisition | Bringing new observations, evidence, testimony, imports, or assertions into Seed. | Strongly supported by existing ontology. |
| Preservation | Retaining observations, evidence, claims, changes, events, or historical context for explainability. | Strong, but may be a lifecycle obligation rather than a knowledge operation. |
| Interpretation | Characterizing what an observation, source, claim, relationship, or pattern means within scope. | Strong candidate; boundary with derivation remains open. |
| Claim formation | Turning support into a represented claim or relationship. | Strong candidate; may be a specific form of interpretation or derivation. |
| Comparison | Examining represented objects together for sameness, difference, contradiction, ordering, or relation. | Strong candidate. |
| Contradiction discovery | Recognizing incompatibility among comparable represented claims. | Strong candidate; likely a specialized comparison or derivation. |
| Corroboration | Recognizing that additional independent or relevant support backs a claim, relationship, or assessment. | Strong candidate; may change support without changing claim content. |
| Derivation | Producing new represented knowledge from existing represented support through an explainable step. | Strong candidate, but probably not primitive. |
| Calculation | Applying explicit quantitative or formal computation over represented values. | Strong candidate; likely a subtype of derivation with stricter method. |
| Extrapolation | Extending a pattern, trend, rate, or model beyond directly represented observations. | Strong candidate; central to forecasting. |
| Projection | Selecting or materializing a view over preserved knowledge. | Ambiguous: both an object and an operation. |
| Selection | Choosing one represented object, value, interpretation, or view for a purpose without erasing alternatives. | Strong candidate; often projection-facing. |
| Revision | Relating later understanding to earlier understanding as changed, narrowed, corrected, superseded, or replaced. | Strong candidate; already reconciled as distinct from derivation. |
| Refinement | Increasing precision, scope clarity, or qualification without necessarily declaring prior understanding false. | Strong candidate; likely a form of revision. |
| Correction | Identifying prior understanding as mistaken, mis-scoped, misidentified, misinterpreted, or invalid for a use. | Strong candidate; likely a form of revision. |
| Replacement | Using one value, claim, model, or interpretation instead of another for a purpose. | Candidate; may be selection-level more often than knowledge-level. |
| Reconciliation | Bringing multiple represented objects, claims, authorities, or interpretations into an explainable relation. | Strong candidate; may be a family rather than an atomic operation. |
| Classification | Assigning a represented object to a type, category, role, severity, or domain. | Strong candidate; may be claim formation, interpretation, or selection depending on support. |
| Qualification | Adding scope, caveat, confidence, modality, authority, or limitation to represented knowledge. | Strong candidate; may modify usability without changing core claim content. |
| Navigation | Establishing or using paths among documents, concepts, architecture, repository artifacts, and knowledge. | Frontier candidate; may be both relationship generation and operator-facing selection. |
| Explanation | Exposing why represented knowledge exists, changed, was selected, or remains caveated. | Candidate but possibly a projection or communication operation rather than a knowledge operation. |
| Assessment | Evaluating represented knowledge against criteria. | Ambiguous: `assessment` is also an object. The operation may be better called evaluation. |
| Recommendation generation | Producing a recommendation from goals, assessments, constraints, claims, and caveats. | Candidate; must remain distinct from decision and command. |

This table intentionally preserves ambiguity. A future reconciliation may split,
merge, or reject several candidates.

---

## Findings From Critical Questions

### Can An Operation Exist Without Creating A New Object?

Yes, at least in candidate form.

Examples:

- comparison may discover that two claims are compatible and create no new
  durable object;
- selection may choose a current-state value in a projection without creating a
  new claim;
- corroboration may increase support for an existing claim without changing the
  claim content;
- qualification may attach or expose a caveat using already-preserved support;
- navigation may traverse existing relationships without creating new
  relationships.

However, explainability may still require some durable trace when the operation
changes current understanding, authority, confidence, selection, caveat status,
or operator-facing answerability. The unresolved boundary is whether that trace
is an object representing the operation, a change event, an updated support
relationship, a projection state, or simply an explainable consequence of
existing objects.

### Can An Operation Modify Relationships Without Modifying Claims?

Yes.

A relationship may be added, removed, qualified, contradicted, selected, or
made visible without changing the content of the claims it connects. For
example, two claims may keep the same propositions while Seed later recognizes
that they contradict each other, corroborate each other, depend on the same
source, apply to different scopes, or should be navigated together.

This is one reason operations matter. If ontology only names claims, it cannot
explain knowledge changes that occur at the support, relationship, selection,
or visibility layer.

### Can Multiple Operations Produce The Same Object Type?

Yes.

A claim may result from acquisition, interpretation, derivation, calculation,
classification, extrapolation, correction, or reconciliation. A relationship may
result from direct observation, documentation observation, comparison,
identity reasoning, navigation analysis, or reconciliation. A forecast may
result from extrapolation, calculation, assessment, or a more complex derivation.

Therefore object type does not identify operation type. A `claim` alone does
not reveal whether it was acquired, derived, corrected, forecast, classified,
or selected. Provenance, support, assumptions, and operation characterization
are needed for explanation.

### Can The Same Object Participate In Different Operations?

Yes.

The same claim may be:

- acquired from testimony;
- used as evidence for a derived claim;
- compared against another claim;
- corroborated by a later observation;
- revised by a narrower claim;
- selected into a current-state projection;
- qualified by a caveat;
- used in a forecast;
- surfaced through navigation;
- excluded from a recommendation because of authority or freshness.

This suggests operations are not a pipeline. They are roles that represented
objects may participate in at different times, for different questions, and
under different authority boundaries.

---

## Critical Examples

### Example 1: Acquisition

Scenario:

```text
Package inventory arrives.

Observation preserved.
Evidence preserved.
```

The primary operation is acquisition. The source-facing result is an
observation; the support-facing result is evidence. If the inventory merely
repeats already-known package information, the operation may increase support
without creating a new claim, change, or event.

This example shows:

```text
Acquisition can occur without derivation.
Observation preservation can occur without knowledge-state change.
Support expansion can occur without claim-content change.
```

If the inventory contains a package not previously represented, acquisition may
also lead to claim formation. If the inventory is later compared against policy
or prior state, additional operations such as comparison, classification,
corroboration, contradiction discovery, or revision may occur.

### Example 2: Contradiction Discovery

Scenario:

```text
Claim A exists.
Claim B exists.

Later:

A contradicts B.
```

The operation appears to be comparison that yields contradiction discovery. It
may also be characterized as derivation if the contradiction relationship is new
represented knowledge produced from existing claims.

The important distinction is:

```text
The contradiction may have existed latently before Seed recognized it.
Discovery is not creation of the underlying incompatibility.
```

Possible results include:

- a contradiction relationship between A and B;
- a contradiction object, if the ontology chooses to represent contradictions
  as first-class objects;
- a caveat or confidence change;
- a change event preserving that Seed's understanding now includes the
  contradiction;
- no change to the content of either claim.

Knowledge changed if Seed can now responsibly represent, select, avoid,
explain, or caveat the incompatible claims differently. Support may change if
new support arrived or if existing support was reweighted or reinterpreted.
Support need not change merely because the contradiction relationship was
recognized.

### Example 3: Forecasting

Scenario:

```text
Disk usage exists.
Growth rate exists.

Later:

Disk fills in six months.
```

The operation is not observation of the future. It is likely extrapolation,
possibly calculation, under assumptions and caveats. It may also be a
specialized derivation because existing represented measurements and growth
rates support a new future-oriented claim.

The resulting object is best characterized as a forecast or future claim, with
preserved support, assumptions, scope, confidence, and caveats. If the forecast
is used to advise action, recommendation generation is a later and distinct
operation. If an operator decides to act, decision and command remain separate
from both forecast and recommendation.

### Example 4: Navigation

Scenario:

```text
Document metadata exists.

Documentation observation produces:

depends_on
related_to
defines
```

Navigation may be an operation, but the example splits into several operations:

- acquisition of document metadata;
- interpretation of metadata and prose into concepts and references;
- relationship generation or claim formation for `depends_on`, `related_to`,
  and `defines`;
- selection of useful paths for a question;
- projection of a navigation view.

Documentation observation can be both acquisition and a source of later
derivation. The acquired document metadata is not itself navigation. Navigation
emerges when represented document, concept, authority, and relationship
knowledge is used to answer:

```text
Where should I look?
```

Relationship generation is likely an operation when it creates represented
relationships from observations, metadata, or existing knowledge. Traversing an
already-represented relationship may instead be navigation use, not new
knowledge creation.

---

## Relationship To Existing Ontology

The proposed distinction:

```text
Observation / Evidence / Claim / Relationship describe what exists.
Operations describe what happens.
```

is partially useful and partially misleading.

It is useful because observations, evidence, claims, and relationships are
represented artifacts or structures that can be preserved, supported, cited,
selected, and explained. Operations such as acquisition, comparison,
corroboration, derivation, revision, and selection explain why those artifacts
appear, change, become related, or become usable.

It is misleading because some existing concepts are already event-like or
operation-adjacent:

- `change` records what became different;
- `event` preserves meaningful history;
- `support` can be a represented relation and the result of support expansion;
- `projection` can mean both a view and the act of selecting or materializing a
  view;
- `assessment` can mean both an evaluative object and the act of evaluating;
- `recommendation` can mean a represented suggestion, while recommendation
  generation is the operation that produced it.

Therefore the safer distinction is not noun versus verb. It is:

```text
Represented objects are things Seed can preserve as part of knowledge.
Operations are explainable happenings, recognitions, selections, or
transformations involving represented objects.
```

An operation may produce an object, update a relationship, alter support,
change selection, expose a caveat, or merely explain why no new durable object
was needed.

---

## Derivation Findings

The derivation frontier expanded because many separate areas had the same rough
shape:

```text
existing represented support
        -> explainable operation
        -> additional represented knowledge
```

But the examples do not all look like one primitive operation.

Derivation remains a strong candidate when:

- the inputs are already represented knowledge;
- an explainable step connects inputs to result;
- the result is a new claim, relationship, assessment, forecast,
  contradiction, caveat, or recommendation;
- the support, assumptions, scope, and caveats remain visible.

Derivation may be too broad or too narrow when:

- the operation merely acquires new observations;
- the result is support expansion without new claim content;
- the operation is selection among existing alternatives;
- the operation revises, corrects, or replaces prior understanding;
- the operation is calculation with strict formal method;
- the operation is extrapolation into future claims;
- the operation is interpretation of ambiguous observations;
- the operation is navigation across existing relationships.

The emerging finding is:

```text
Derivation may be real.
Derivation may not be primitive.
Derivation may name one family member within a broader operations ontology.
```

A future reconciliation should avoid making `derivation` a catch-all for every
knowledge change that does not begin with a new observation.

---

## Learning Connection

Learning is not cleanly identical to any one operation.

Existing learning language suggests learning is an improvement or extension of
represented understanding while preserving the support path that made the
improvement possible. That can involve many operations:

```text
acquisition
interpretation
claim formation
corroboration
comparison
contradiction discovery
derivation
revision
refinement
correction
classification
qualification
selection
projection
```

The best current characterization is:

```text
Learning is a cross-layer epistemic outcome or family effect produced by one or
more operations over preserved knowledge.
```

Learning may include acquisition, but it is not merely acquisition. Learning may
include derivation, but it is not merely derivation. Learning may include
revision or correction, but it is not merely replacement or erasure. Learning
may appear as projection or selection change, but projection change is not
automatically knowledge replacement.

This preserves several invariants:

- learning should not erase the path by which previous understanding arose;
- learning can occur without a new external observation;
- learning can occur without changing current selected state;
- learning can result from reinterpreting already-preserved support;
- learning can improve explainability, caveats, confidence, or navigation
  without creating a new domain claim.

---

## Operation Tensions

### Operation Versus Process

An operation is an ontological category for what happened to represented
knowledge. A process is an organized sequence of activities. Operations should
not be assumed to form a process.

Example: comparison, selection, and qualification can occur in many orders or
independently. Treating them as a required process would over-design the
ontology.

### Operation Versus Capability

A capability is the ability to do something. An operation is the thing done or
recognized in knowledge terms. Seed may have a capability to observe packages,
but acquisition is the knowledge operation that occurs when package observations
are preserved.

### Operation Versus Runtime Stage

Operations are not runtime stages. A runtime may acquire, compare, project, or
select, but the ontology should not be dictated by runtime control flow.

### Operation Versus Implementation

An operation need not map to a class, function, table, queue, job, component, or
service. Multiple implementations may perform the same operation, and one
implementation may participate in multiple operations.

### Operation Versus Method

A method is how an operation is performed. Calculation, statistical estimation,
textual interpretation, operator assertion, and graph traversal may be methods
or subtypes depending on future reconciliation. The ontology should not confuse
method details with operation identity.

### Operation Versus Transformation

Some operations transform represented knowledge into new represented knowledge.
Others do not. Selection, navigation, corroboration, contradiction discovery,
and qualification may alter usability, support, relationship visibility, or
explainability without transforming claim content.

### Operation Versus Relationship

Some operations produce relationships, but relationships are not operations.
`A contradicts B` may be a relationship. Recognizing, deriving, preserving, or
surfacing that relationship is the operation. Likewise, `depends_on` may be a
relationship produced by documentation observation or navigation analysis, but
`depends_on` is not itself the act of navigating.

---

## Candidate Operation Grouping

The current candidates may be grouped without treating the grouping as final.

### Source And Support Operations

```text
acquisition
preservation
support expansion
corroboration
qualification
```

These operations concern what entered Seed, what support exists, how support is
preserved, and how that support is scoped or caveated.

### Interpretive And Relational Operations

```text
interpretation
claim formation
classification
comparison
contradiction discovery
relationship generation
reconciliation
```

These operations concern how represented objects become meaningful, comparable,
related, typed, or placed into tension.

### Generative And Projective Operations

```text
derivation
calculation
extrapolation
forecasting
assessment/evaluation
recommendation generation
```

These operations concern new conclusions, estimates, forecasts, assessments, or
recommendations based on existing represented support.

### Revision And Selection Operations

```text
revision
refinement
correction
replacement
selection
projection
```

These operations concern how later understanding relates to earlier
understanding, how precision changes, how mistakes are marked, and how a
current or purpose-specific view is selected without erasing preserved history.

### Navigation Operations

```text
navigation
path selection
relationship traversal
knowledge-location discovery
```

These operations concern how represented knowledge helps contributors or
operators find the concepts, documents, artifacts, or explanations needed for a
question.

This grouping is evidence of a frontier, not a taxonomy ready for schema or
runtime use.

---

## Candidate Rejections Or Merges

Some candidate names may not survive future reconciliation:

- `forecasting` may be an umbrella over extrapolation, calculation,
  assumptions, future claims, and caveats rather than a primitive operation.
- `assessment` should likely name an object; the operation may be `evaluation`.
- `projection` should be split between projection-as-object/view and
  projection-as-operation/selection.
- `replacement` may often be a selection relation rather than a knowledge
  operation, unless it explicitly relates later understanding to earlier
  understanding.
- `preservation` may be a lifecycle invariant rather than an operation over
  knowledge objects.
- `navigation` may be a use of relationship knowledge rather than a producer of
  knowledge, except where it generates or qualifies navigation relationships.
- `reconciliation` may be too broad to be atomic; it may combine comparison,
  interpretation, qualification, revision, and selection.
- `reasoning` is intentionally not promoted here as a primitive because it may
  be broader than derivation, comparison, calculation, extrapolation,
  assessment, and reconciliation combined.

---

## Why Implementation Would Be Premature

Implementation would be premature because the ontology has not settled:

- whether operations are first-class represented objects;
- whether operations are labels on support edges, change events, provenance, or
  explanation paths;
- whether every operation needs a durable trace;
- whether operation names should be normalized or remain document-level
  vocabulary;
- whether projection and assessment should be split into object and operation
  terms;
- whether derivation is primitive, composite, or family-level;
- whether navigation generates knowledge or merely uses existing knowledge;
- whether learning is an operation, family of operations, result, or cross-layer
  effect;
- whether contradiction discovery should create contradiction objects,
  contradiction relationships, caveats, changes, events, or some combination.

The architecture already warns against treating ontology as dictated by schema,
runtime, projection, or implementation convenience. The operations frontier is
especially vulnerable to that error because verbs easily become imagined
engines, executors, planners, workflows, or pipelines.

No such implementation should be designed from this document.

---

## Frontier Finding

The repository has spent much of its recent effort discovering and stabilizing
objects:

```text
observation
evidence
claim
relationship
support
assessment
forecast
recommendation
projection
caveat
change
event
```

That work remains necessary and authoritative. But recent investigations also
show a recurring need to explain what happens over those objects:

```text
acquisition
interpretation
comparison
corroboration
derivation
calculation
extrapolation
revision
refinement
correction
selection
projection
reconciliation
classification
qualification
navigation
```

The operations frontier therefore appears real enough to preserve as a frontier
characterization. It is not yet reconciled enough to become a schema, runtime
layer, execution plan, or universal taxonomy.

The most conservative finding is:

```text
Seed's object ontology is more mature than its operation ontology.
Derivation exposed the gap because it described knowledge produced from
knowledge, but adjacent cases require additional operation names.
Future work should investigate operations without collapsing them into engines,
pipelines, stages, or implementation classes.
```

---

## Unresolved Questions

Future reconciliation should answer:

1. Are operations represented entities, provenance labels, support-edge roles,
   change-event causes, explanation categories, or non-durable descriptions?
2. Which operations are primitive and which are composites?
3. Is derivation a primitive, a family, or a relationship between support and
   result?
4. Is interpretation separate from derivation, or is interpretation a method of
   derivation?
5. Is calculation a subtype of derivation or a separate operation with stronger
   method constraints?
6. Is extrapolation a subtype of derivation, forecasting, or both?
7. Does corroboration change knowledge, support, confidence, or only
   explainability?
8. Does contradiction discovery create an object, a relationship, a caveat, a
   change event, or only a newly visible relation among existing claims?
9. Is projection primarily an object, operation, selection relation, or view?
10. Is navigation knowledge-producing, knowledge-using, or both?
11. Can operation identity be determined without reference to implementation
    method?
12. How should learning refer to operations without becoming a catch-all?
13. What minimum operation vocabulary is needed for explanation without
    overbuilding architecture?

---

## Final Finding

The operations frontier is a plausible next ontology frontier, but not a settled
architecture.

The document's strongest findings are:

- object type does not determine operation type;
- operations can occur without creating new claim content;
- operations can modify relationships, support, caveats, selection, or
  explainability without modifying claims;
- multiple operations can produce the same object type;
- the same object can participate in many operations;
- derivation is important but probably not primitive;
- learning is best understood for now as a cross-layer outcome or family effect
  of operations over preserved knowledge;
- implementation would be premature until the ontology can explain operation
  identity, durability, support, relationship to change/event, and interaction
  with projection and navigation.

A future participant should therefore treat this document as a map of questions
and candidate vocabulary, not as an implementation mandate.
