# Derivation Frontier

## Purpose

This document characterizes a recurring frontier in Seed's architecture:
represented knowledge may sometimes become support for additional represented
knowledge.

It is documentation only. It does not reconcile derivation, define a reasoning
engine, add runtime behavior, modify schemas, design graph execution, define a
planner, or add tests.

The goal is to record the frontier clearly enough that a future participant can
understand why derivation appears important, where it appears, which candidate
shape is emerging, and why implementation would be premature.

Repository authority wins over this document. In particular, the existing
knowledge-change, learning, foundational ontology, forecasting, contradiction,
identity, temporal, navigation, and architectural-status documents remain the
authoritative references for their own reconciled boundaries.

## Central Question

The frontier question is:

```text
Can knowledge produce new knowledge?
```

More precisely:

```text
Can represented knowledge become the support for additional represented
knowledge?
```

The answer appears to be "sometimes yes" in existing architectural language, but
that answer is not yet enough to settle an ontology named `derivation`.

Several reconciliations already permit or require this shape:

```text
Existing represented knowledge
        -> comparison / interpretation / calculation / reasoning / extrapolation
        -> new represented claim, relationship, assessment, forecast,
           contradiction, recommendation, or revision candidate
```

However, the architecture has not yet settled whether all of those cases are the
same operation, whether `derivation` is the right name, whether some are better
understood as interpretation, revision, projection, assessment, or selection, or
whether derivation is an operational layer above several object types.

## Candidate Shape Under Investigation

The candidate shape is:

```text
Existing observations, evidence, claims, relationships,
projections, caveats, and support

        ↓

comparison
interpretation
calculation
reasoning
extrapolation

        ↓

new represented claim
new relationship
new assessment
new forecast
new contradiction
new recommendation
```

This shape appears real enough to preserve as a frontier, but not settled enough
to promote into a complete ontology.

The safest current characterization is:

```text
Represented support may sometimes justify a newly represented proposition or
relationship, provided that provenance, assumptions, scope, caveats, and the
operation that transformed support into the new representation remain
explainable.
```

This does not mean arbitrary invention is allowed. It means a new represented
object may be justified by preserved support plus a declared interpretive,
comparative, calculative, or extrapolative step.

## Why This Appears Important

The pattern recurs across separate architectural areas:

- contradiction discovery;
- identity reconciliation;
- forecasting and future claims;
- temporal occurrence windows;
- assessment and recommendation generation;
- impact analysis and consequence reasoning;
- knowledge navigation relationships;
- learning and knowledge change;
- freshness, confidence, and selection changes over preserved support.

The repeated emergence matters because Seed is claim-centric. If claims,
relationships, assessments, recommendations, and forecasts can be newly
represented from preserved support, Seed needs a vocabulary for explaining:

```text
what was created
what supported it
what operation connected support to result
what assumptions or caveats constrained it
what changed in Seed's understanding
what did not change in reality
```

Without such vocabulary, several architectural errors become likely:

- treating a derived future claim as an observation of the future;
- treating contradiction discovery as contradiction creation;
- treating identity reconciliation as physical entity mutation;
- treating a narrowed occurrence window as a revised occurrence;
- treating a recommendation as a decision or command;
- treating navigation usefulness as repository topology;
- treating projection visibility as truth or existence.

## Current Evidence From Existing Reconciliations

### Knowledge Change

The knowledge-change reconciliation already distinguishes acquisition,
derivation, and revision. It states that knowledge change does not always require
a new observation, while support expansion usually does. It also says derivation
can produce new knowledge from existing preserved support.

That document is stronger than this frontier in one respect: it already uses the
term `derivation` in a boundary summary. This frontier does not repeal that
language. Instead, it asks whether the same operation extends across adjacent
areas that are not yet fully reconciled under one derivation ontology.

### Learning

The learning reconciliation defines learning as improvement or extension of
represented understanding, not erasure of history. It allows learning without a
new external observation, including contradiction discovery, reinterpreting old
evidence, identity clarification, and changes to confidence or caveats.

This suggests learning may be an umbrella that can include acquisition,
derivation, revision, and refinement. The exact relationship remains unsettled:
learning may name the broader epistemic outcome, while derivation may name one
operation that can contribute to that outcome.

### Foundational Ontology

The foundational ontology identifies observations, evidence, claims, facts, and
relationships as knowledge concepts, and assessments, recommendations, decisions,
commands, capabilities, executions, and actions as distinct architectural roles.
It also states that trust, corroboration, verification, contradiction, causality,
and explanation qualify reasoning without becoming truth.

This creates pressure to decide whether `derivation` is itself an object or an
operation over objects. The current evidence favors operation, but not enough to
settle implementation semantics.

### Prediction And Forecasting

The forecasting reconciliation already gives a chain from observations and
historical claims through current-state claims, trend or assumption support,
future claims, consequences, goal relevance, recommendation, decision, plan,
command, and action.

Forecasting therefore appears to depend on support-preserving transformation of
past and present knowledge into future-oriented claims. But forecasting is not
identical with derivation. A forecast may be one domain where derivation-like
operations occur, while the forecast itself remains a future claim or structured
aggregation of future claims.

### Contradiction Discovery

The contradiction reconciliation distinguishes contradiction existence,
discovery, projection, visibility, explanation, and resolution. A contradiction
can be latent in preserved claims before Seed discovers or exposes it.

This strongly resembles derivation:

```text
Claim A exists.
Claim B exists.
Comparison boundary becomes available or is applied.
A contradicts B is represented.
```

Yet the contradiction itself may be a property of preserved incompatible claims,
not a newly invented fact about the world. The open question is whether the new
represented relationship `A contradicts B` is best called derived, discovered,
classified, or projected.

### Identity Reconciliation

The identity reconciliation distinguishes identity merge from relationship. It
warns that related entities must not be collapsed into identical entities without
strong equivalence evidence.

Identity creates a difficult derivation frontier:

```text
Observations already exist.
Later, Seed represents A == B.
```

This may be a derived identity relationship, a reconciliation result, a claim
generation event, or a selection over candidate identities. Whatever it is, the
support must preserve why equivalence is justified and why weaker evidence only
supports relationship or candidate association.

### Temporal Occurrence Claims

The occurrence-time reconciliation treats occurrence time as a supported temporal
claim, not a directly observed primitive. Prometheus sample timestamps, log
timestamps, observation time, preservation time, and knowledge time can all
support temporal claims without becoming occurrence time.

Temporal narrowing therefore exposes a derivation-like pattern:

```text
Prometheus interval evidence exists.
Log interval evidence later exists or is reinterpreted.
Seed narrows the occurrence window.
```

The occurrence did not change. Seed's supported temporal claim changed. The open
question is whether the narrowed interval is a derived claim, a revised claim, a
refinement, or all three under different viewpoints.

### Knowledge Navigation

The knowledge-navigation frontier observes that documentation, architecture, and
repository artifacts may form separate but connectable navigation layers. A
future knowledge-navigation relation may be created from existing documentation
claims, references, dependencies, and concept boundaries.

This appears derivation-like because a useful navigation relationship might not
be directly observed as a source report. It may be interpreted from preserved
references and conceptual relationships. But navigation remains an active
frontier and must not be collapsed into graph unification or a new execution
system.

## Critical Examples

### Example 1: Contradiction Discovery

```text
Claim A exists.
Claim B exists.

Later:

A contradicts B.
```

Possible characterization:

- The world did not necessarily change.
- The preserved claims may not have changed.
- Seed's represented understanding changed by recognizing incompatibility under
  a comparison boundary.
- A new relationship or classification may have been represented.
- The contradiction may have existed latently before discovery.

Open questions:

- Is `A contradicts B` a derived relationship?
- Is contradiction discovery an operation that creates a represented relation
  while not creating the underlying incompatibility?
- Does discovery belong to assessment, integrity analysis, projection, or a
  broader derivation operation?
- When does contradiction discovery become revision or resolution?

### Example 2: Forecasting

```text
Disk usage observations exist.
Growth-rate observations or trend claims exist.

Later:

Disk predicted full in six months.
```

Possible characterization:

- The created object is likely a future claim or forecast.
- Support includes historical measurements, trend interpretation, assumptions,
  horizon, and uncertainty.
- The prediction is not an observation and not a future fact.
- If exposed as advice, a later recommendation remains distinct from the
  prediction.

Open questions:

- Is the forecast itself derived knowledge, or is only its support path
  derivational?
- How explicit must assumptions be to prevent invention?
- What distinguishes a calculated projection from speculative fabrication?
- When a later observation contradicts the forecast, is that revision,
  calibration, contradiction, or all of them?

### Example 3: Identity

```text
Observations already exist.

Later:

A == B.
```

Possible characterization:

- Seed may have created an identity claim or identity relationship.
- The external entity did not merge merely because Seed represented equivalence.
- Strong equivalence evidence is required; weak evidence should support
  relationship or candidate association instead.
- Existing observations may be reinterpreted under a clarified identity scope.

Open questions:

- Is identity equivalence derived, reconciled, selected, or asserted?
- Is `A == B` a claim, relationship, lifecycle operation, or selection over
  identifiers?
- What support threshold distinguishes identity collapse from relationship
  creation?
- How should prior projections be explained after identity clarification?

### Example 4: Temporal Claims

```text
Prometheus interval evidence exists.
Log interval evidence exists.

Later:

Occurrence window narrows.
```

Possible characterization:

- The event or occurrence did not change.
- Seed's temporal claim changed.
- The narrower interval may be a refined or revised temporal claim.
- The previous interval remains historically meaningful because it represented
  what was justified under earlier support.

Open questions:

- Is the narrowed window derived from combined support, revised from an earlier
  claim, or both?
- What exactly is new: claim content, support relation, confidence, selection,
  or projection?
- How should derivation method, clock trust, and source timestamp caveats remain
  inspectable?

## Acquisition Relationship

The emerging distinction is:

```text
Acquisition

Observation
        ↓
Evidence
        ↓
Knowledge
```

versus:

```text
Derivation

Knowledge
        ↓
Reasoning / comparison / interpretation / calculation
        ↓
Knowledge
```

Current findings:

- Acquisition introduces new observations, testimony, imports, samples, or
  source reports into Seed.
- Derivation-like operations can occur over already preserved observations,
  evidence, claims, relationships, projections, caveats, and support.
- The two are not mutually exclusive. New acquisition may trigger derivation,
  and derivation may reinterpret older acquired support.
- Support expansion usually has an acquisition path; new claim content or a new
  relationship may arise from derivation over existing support.
- Acquisition answers "what entered Seed?" Derivation answers "what additional
  represented understanding is justified by what Seed already preserves?"

Open questions:

- Can a single knowledge change contain both acquisition and derivation steps?
- Should derivation records point to observations directly, to evidence, to
  claims, or to a support graph?
- When a new observation causes a recalculation, is the result acquired,
  derived, revised, or all three?

## Relationship To Learning

Learning may include:

```text
acquisition
support expansion
derivation
revision
refinement
correction
selection changes
confidence changes
caveat changes
```

But that list is not yet a settled ontology.

Current findings:

- Learning names a change or improvement in represented understanding.
- Derivation may name one operation by which represented understanding changes.
- Revision may relate a later understanding to an earlier understanding as
  narrowed, corrected, superseded, expanded, or replaced.
- Refinement may improve precision without making the earlier claim false.
- Learning should preserve history and explainability regardless of whether the
  change came from acquisition, derivation, or revision.

Open questions:

- Is derivation a subtype of learning, a cause of learning, or an operation that
  sometimes produces learning?
- Can derivation occur without learning if it creates a candidate relation not
  selected into current understanding?
- Does learning require a knowledge-state change, or can it include preserved
  but not selected derived candidates?

## Object Versus Operation Findings

Recent ontology work suggests a possible distinction:

```text
Objects
```

Candidate objects:

```text
observation
evidence
claim
relationship
support
projection
assessment
forecast
recommendation
contradiction relation
revision relation
```

versus:

```text
Operations
```

Candidate operations:

```text
acquisition
derivation
revision
selection
projection
comparison
interpretation
calculation
extrapolation
assessment
recommendation generation
```

The current evidence favors treating derivation as an operation or operation
family rather than as a primary object. The result of derivation may be an
object, such as a claim, relationship, assessment, forecast, contradiction
relation, recommendation, or revision relation.

However, the operation itself may need to be represented enough to preserve:

- input support;
- transformation or method;
- assumptions;
- caveats;
- confidence or strength;
- scope and authority;
- creation time or knowledge time;
- lineage to prior claims or relationships;
- explanation path.

Open questions:

- Is a `derivation` itself a first-class represented object, or merely metadata
  on a derived claim or relationship?
- Is `support` enough to explain derivation, or must the transforming operation
  be separately preserved?
- Are comparison, interpretation, calculation, reasoning, and extrapolation
  sub-operations of derivation or sibling operations?
- Should recommendation generation be treated as derivation, assessment,
  selection, or advisory response construction?

## Provenance, Explainability, And Anti-Fabrication

If represented knowledge can support additional represented knowledge, the
architecture must preserve boundaries that prevent invention.

### Provenance Preservation

A derived or derivation-like result must be traceable to preserved support:

```text
result
        supported_by
observations / evidence / claims / relationships / assumptions / caveats
```

Provenance should answer:

- Which observations, evidence, claims, or relationships were used?
- Which sources and vantage points supplied them?
- What time horizon, scope, identity boundary, and authority boundary applied?
- What assumptions were necessary?
- Which caveats limit the result?

### Explainability Preservation

Explainability requires more than listing inputs. It should make the transforming
step inspectable:

```text
support + operation + assumptions + caveats -> represented result
```

A future explanation should be able to say why Seed represented the new claim or
relationship without implying that Seed directly observed it.

### Preventing Invention

The difference between derivation and fabrication is support discipline.

Derivation-like representation is constrained by:

- preserved support;
- explicit scope;
- declared assumptions;
- known uncertainty;
- caveats and confidence;
- method or comparison boundary;
- authority and source limitations;
- preservation of earlier claims rather than erasure.

Fabrication appears when a result lacks an inspectable support path, hides its
assumptions, overstates its authority, collapses distinct objects, treats
possibility as fact, or presents projection visibility as truth.

This frontier does not design enforcement machinery. It only records that any
future derivation ontology must preserve this boundary.

## Required Tensions

### Derived Claim vs Revised Claim

A derived claim may be new without changing an older claim. A revised claim
explicitly relates later understanding to earlier understanding. The same result
may be both derived from support and a revision of an earlier claim, but those
roles should not be collapsed.

### Derived Relationship vs Discovered Relationship

A relationship may be represented only after comparison or interpretation, but
that does not mean the underlying relation began to exist at discovery time.
`Discovered` emphasizes Seed's recognition. `Derived` emphasizes the support and
operation that justified representation.

### Derivation vs Interpretation

Interpretation may be the act of assigning meaning to preserved support.
Derivation may be the broader transformation from support to a new represented
object. But some interpretation results may themselves be represented claims or
relationships.

### Derivation vs Reasoning

Reasoning is broader and less ontologically precise. It may include comparison,
selection, planning, explanation, and recommendation. Derivation may be the
subset that produces a represented knowledge result, but this remains unsettled.

### Derivation vs Prediction

Prediction is a future-oriented claim. It may be produced by a derivation-like
operation from historical and current support, but prediction should not be
renamed derivation or treated as observed fact.

### Derivation vs Recommendation

A recommendation may rely on derived assessments, future claims, consequences,
or goal relevance. But recommendation is advisory and remains distinct from
decision, command, and action.

### Derivation vs Assessment

Assessment interprets selected knowledge for an evaluative purpose. Some
assessments may be derived from support, but assessment includes stance,
criteria, and purpose that may not apply to all derived claims or relationships.

### Derivation vs Projection

Projection selects, formats, summarizes, or exposes preserved knowledge.
Projection may compute or expose derivation-like relationships, but visibility
is not existence and projection should not become truth authority.

## Frontier Constraints

This document intentionally does not create:

- runtime designs;
- reasoning engines;
- planning engines;
- inference engines;
- graph execution systems;
- schema changes;
- persistence models;
- projection mutation rules;
- automatic contradiction detection;
- automatic identity merging;
- forecasting algorithms;
- recommendation engines.

Implementation would be premature because the ontology questions are still open.
The recurring pattern is visible, but the architecture has not yet decided:

- whether `derivation` is the correct umbrella term;
- whether derivation is one operation or a family of operations;
- which outputs count as derived knowledge;
- how derivation relates to learning, revision, assessment, and projection;
- how much of the operation must be represented for explainability;
- what authority boundaries govern derived results.

## Open Questions

1. Can represented knowledge become support for additional represented knowledge
   in all of the listed domains, or only in some?
2. Is derivation the right architectural name for the pattern?
3. Is derivation an operation, an object, metadata, lineage, or a relation
   between support and result?
4. Which output types can be derivation results: claims, relationships,
   assessments, forecasts, contradictions, recommendations, revisions, or
   navigation links?
5. What minimum provenance must every derivation-like result preserve?
6. What minimum explanation must be available to distinguish derivation from
   fabrication?
7. How should assumptions be represented without designing a new inference
   system?
8. Can derivation be unselected, provisional, disputed, superseded, or retracted?
9. How does derivation interact with contradiction discovery without making
   discovery look like creation?
10. How does derivation interact with identity without encouraging unsafe entity
    collapse?
11. How does derivation interact with forecasting without making future claims
    look observed?
12. How does derivation interact with temporal claim revision without making
    knowledge change look like reality change?
13. How does derivation interact with navigation without prematurely unifying
    repository, architecture, and knowledge graphs?
14. Does learning include acquisition, derivation, revision, refinement,
    correction, and selection, or is learning narrower?
15. What future document should reconcile this frontier, and what evidence would
    justify moving from characterization to reconciliation?

## Final Characterization

Derivation appears important because many parts of Seed do more than acquire
observations. They compare, interpret, calculate, extrapolate, assess, and relate
already represented knowledge in ways that may justify additional represented
knowledge.

The candidate shape is real enough to preserve:

```text
Existing represented support
        -> bounded operation
        -> new represented result
```

But implementation is premature because the architecture has not settled whether
this is one operation, several operations, metadata on support, a lineage object,
or a vocabulary shared by forecasting, contradiction discovery, identity,
temporal refinement, assessment, recommendation, and navigation.

Until that reconciliation happens, the durable guidance is boundary discipline:

```text
Preserve support.
Expose assumptions.
Name the operation cautiously.
Keep claims, relationships, assessments, forecasts, recommendations, revisions,
projections, and reality distinct.
Do not treat derived representation as observation.
Do not treat discovery as creation.
Do not treat explanation as proof.
Do not implement an engine before the ontology is settled.
```
