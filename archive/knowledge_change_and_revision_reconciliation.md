# Knowledge Change, Revision, And Derivation Reconciliation

## Purpose

This reconciliation defines the ontology boundary for what changes when Seed's
knowledge changes, and it revises the earlier framing that treated many cases as
undifferentiated "knowledge change."

It is documentation only. It does not implement code, modify schemas, modify
runtime behavior, design persistence, design claim versioning, design event
schemas, design databases, design graph storage, design conflict algorithms,
design reasoning engines, design inference engines, design planners, or add
tests.

The central questions are now two related questions:

```text
What changes when knowledge changes?
When is the change actually derivation of new knowledge from existing knowledge?
```

Not:

```text
What changes when reality changes?
How should an inference engine be designed?
```

This document is subordinate to the repository's existing learning, lifecycle,
integrity, contradiction, observation/evidence/change/event, forecasting,
temporal, ontology, and architectural-status documents. Repository authority
wins over prompt language.

## Authoritative Context

This reconciliation builds on these existing findings:

- Observation, evidence, claim formation, change, and event are distinct
  architectural concepts.
- A repeated observation may add support while producing no new domain change.
- Learning changes Seed's represented understanding without erasing the history
  of how that understanding arose.
- Occurrence time is usually a supported temporal claim, not a directly observed
  primitive.
- The world may change once while Seed's understanding of when it changed
  improves many times.
- Contradictions may exist latently before Seed discovers or exposes them.
- Contradiction discovery is not contradiction creation.
- Prediction is primarily a future claim, not an observation, recommendation,
  decision, command, or action.
- Visibility is not truth.
- Cross-Seed sharing transfers evidence or testimony, not truth.
- Ontology should not be dictated by storage, runtime, projection, or schema
  convenience.

## Executive Summary

The earlier document was directionally correct that knowledge can change without
reality changing. It was not precise enough because it placed several distinct
operations under one broad phrase: "knowledge change."

The revised finding is:

```text
Knowledge change is the umbrella.
Acquisition, support expansion, revision, refinement, correction, replacement,
and derivation are not the same operation.
```

Some knowledge changes require or usually begin with new observations. Other new
knowledge arises from reasoning over existing observations, evidence, claims,
relationships, comparisons, assumptions, and projections. The most important
boundary is therefore not only:

```text
Reality change != knowledge change
```

but also:

```text
Acquisition != derivation != revision
```

The safest ontology is:

```text
Reality / occurrence
        distinct from
Observation / evidence acquisition
        distinct from
Support relation
        distinct from
Claim content
        distinct from
Derived claim or derived relationship
        distinct from
Revision of an earlier claim
        distinct from
Knowledge state
        distinct from
Projection / selection / visibility
```

The statement from the earlier framing:

```text
Knowledge change does not require a new observation.
```

is **partially true but ambiguous**. It is true for derivation, reinterpretation,
identity reconciliation, contradiction discovery, confidence recalculation, and
selection changes over already-preserved knowledge. It is false or misleading if
read as a description of new support arriving, because new support often enters
Seed through a new observation, imported report, operator assertion, or evidence
preservation step.

The sharper formulation is:

```text
Knowledge change does not always require a new observation.
Support expansion usually does.
Derivation can produce new knowledge from existing preserved support.
Revision may be triggered by either new support or reanalysis of old support.
```

## Boundary Summary

| Boundary | Reconciled distinction |
| --- | --- |
| Reality change vs knowledge change | Reality change concerns the world. Knowledge change concerns Seed's represented understanding of the world. |
| Acquisition vs derivation | Acquisition brings new observations, evidence, testimony, or imports into Seed. Derivation creates a new supported claim, relationship, assessment, or comparison from existing represented knowledge. |
| Support expansion vs derivation | Support expansion adds or reweights support for a claim. Derivation produces new claim content or a new relationship from support that may already exist. |
| Support change vs claim change | Support may change without claim content changing. Claim content changes only when the asserted proposition, scope, subject, predicate, value, interval, modality, or qualification changes. |
| Derivation vs revision | Derivation may produce a new claim without changing an older claim. Revision explicitly relates a later understanding to an earlier understanding as changed, narrowed, corrected, superseded, or replaced. |
| Refinement vs correction | Refinement improves precision without necessarily falsifying the earlier claim. Correction marks earlier understanding as mistaken, mis-scoped, misidentified, or invalid for a use. |
| Replacement vs revision | Replacement is a selection relation in which one understanding is used instead of another for a purpose. Revision is a knowledge relationship between earlier and later understandings. |
| Contradiction vs contradiction discovery | Contradiction is incompatibility among comparable claims. Discovery is recognition or derivation of that incompatibility relationship. |
| Forecasting vs observation | Forecasting derives future-oriented claims from current or historical support. It is not observation of the future. |
| Identity derivation vs entity change | Deriving `A == B` changes Seed's represented identity relation. It does not by itself merge or split reality. |

## 1. What Is Knowledge Change?

Knowledge change is an epistemic transition in Seed's represented understanding.
It answers:

```text
What does Seed now know, believe, support, doubt, compare, select, derive, or
explain differently than before?
```

Knowledge change may include changes to:

- available observations;
- available evidence;
- support relations between evidence and claims;
- support strength;
- confidence;
- derived claim content;
- non-derived claim content;
- claim scope;
- claim precision;
- claim lifecycle status;
- selected current understanding;
- contradiction discovery status;
- contradiction visibility;
- identity resolution;
- provenance interpretation;
- caveats;
- freshness assessment;
- authority weighting;
- explanation paths.

Knowledge change does not always require:

- a new real-world occurrence;
- a changed entity;
- a changed historical fact;
- a new observation;
- a changed existing claim;
- a contradiction;
- a correction;
- erasure of old knowledge.

However, the phrase "does not require a new observation" must not be used to
collapse acquisition and derivation. If the changed thing is added support from a
source, there is usually an acquisition path:

```text
Source report / operator assertion / import / sample
        -> observation or testimony preservation
        -> evidence
        -> support relation
        -> possible knowledge-state change
```

If the changed thing is a derived relationship or claim, there may be no new
observation:

```text
Existing observations, evidence, claims, and relationships
        -> reasoning, comparison, extrapolation, or interpretation
        -> derived claim or derived relationship
        -> possible knowledge-state change
```

The architectural question is therefore not merely:

```text
Did knowledge change?
```

but:

```text
Which epistemic operation occurred, and which plane changed?
```

## 2. Two Candidate Mechanisms: Acquisition And Derivation

The investigation supports a real architectural distinction between acquisition
and derivation, with a caveat: this document names the ontology boundary, not a
runtime pipeline or engine design.

### Acquisition

Acquisition is the path by which Seed receives or preserves new source material.
A compact shape is:

```text
Observation
    -> Evidence
    -> Claim or support relation
    -> Knowledge state
```

Acquisition may include sensor samples, logs, tool outputs, operator assertions,
foreign Seed testimony, imported files, source reports, or explicit corrections.
Acquisition changes what support material Seed has available.

Acquisition does not guarantee claim revision. A new observation may merely
corroborate an existing claim or leave current selection unchanged.

### Derivation

Derivation is the path by which Seed produces new represented knowledge from
already-preserved knowledge. A compact shape is:

```text
Existing observations, evidence, claims, relationships, projections, and caveats
    -> reasoning, comparison, interpretation, calculation, or extrapolation
    -> new derived claim, relationship, assessment, contradiction, or forecast
```

Derivation is a real architectural operation when it creates a support-preserving
representation that Seed can later select, explain, challenge, revise, or expose.
It is not merely a metaphor if the result becomes part of Seed's represented
knowledge rather than an ephemeral wording choice.

Derivation is not a license to invent truth. A derived item must preserve:

- the source claims, observations, or evidence it depended on;
- the comparison, interpretation, calculation, assumption, or extrapolation path;
- the time or context of derivation;
- the uncertainty, caveat, or authority boundary of the result;
- whether the result is a claim, relationship, assessment, forecast, visibility
  decision, or selection effect.

### Evaluation Of The Proposed Distinction

The distinction is supported, but not as two isolated systems. Acquisition and
derivation are intertwined concerns over preserved knowledge:

```text
Acquisition can provide inputs for derivation.
Derivation can create claims that later receive new acquired support.
Revision can be triggered by either acquisition or derivation.
Selection can consume both acquired and derived knowledge.
```

The repository's claim-centric ontology makes this distinction important because
both acquired and derived material can become claims or support-bearing
relationships, but they answer different provenance questions:

```text
Acquired: What did a source report, and when did Seed preserve it?
Derived: What did Seed infer or compute from preserved support, and how?
```

## 3. Operation Comparison

The required terms are not the same operation.

| Operation | Primary question | Typical input | Typical output | Changes an existing claim? |
| --- | --- | --- | --- | --- |
| Knowledge revision | How does later understanding relate to earlier understanding? | New support or reanalysis of old support | Later understanding explicitly related to an earlier one | Sometimes |
| Knowledge refinement | How did understanding become more precise or better qualified? | Broader claim plus support for narrowing or qualification | Narrower or better-qualified understanding | Often, but may preserve compatibility |
| Knowledge correction | What was wrong, mis-scoped, misidentified, or invalid about prior understanding? | Corrective support, authority, or reanalysis | Corrective claim plus relationship to earlier item | Yes in evaluative status; not erasure |
| Knowledge replacement | Which understanding should be used for this purpose now? | Competing or superseding understandings | Selection relation or current-view choice | Not necessarily |
| Knowledge derivation | What new claim, relationship, or assessment follows from existing represented knowledge? | Existing observations, evidence, claims, relationships, assumptions | New derived claim, relationship, contradiction, forecast, or assessment | Not necessarily |

### Knowledge Revision

Knowledge revision is the creation or recognition of a later understanding that
is explicitly related to an earlier understanding.

Revision says:

```text
Seed now understands this differently from an earlier understanding.
```

Revision may be a correction, refinement, narrowing, expansion, consolidation,
supersession, or replacement. It should not imply erasure.

Revision can be caused by acquisition:

```text
new log evidence -> narrower outage interval
```

Revision can also be caused by derivation:

```text
existing observations reinterpreted -> previous identity assignment was wrong
```

### Knowledge Refinement

Knowledge refinement is a revision that improves precision, specificity,
qualification, or explanatory fit without necessarily making the earlier claim
false.

Example:

```text
Earlier: outage occurred between 10:49:45 and 10:50:15.
Later:   outage occurred between 10:49:59.500 and 10:50:15.
```

The later claim is narrower. If the earlier interval was an honest supported
bounds claim, it may remain historically justified and compatible with the later
claim.

Refinement can be derived from existing support if the support was already
preserved but not previously interpreted precisely. It can also be acquired from
new support if a new observation supplies a tighter bound.

### Knowledge Correction

Knowledge correction is a revision that indicates an earlier understanding was
wrong, mis-scoped, misidentified, misinterpreted, stale for its asserted use, or
otherwise invalid under the relevant authority and comparison boundary.

Example:

```text
Earlier: host115 is production.
Later:   host115 is staging; the earlier source mapped the wrong inventory row.
```

Correction is stronger than refinement. It changes how the earlier claim should
be evaluated, not just how precise the current claim is.

Correction is not the same as contradiction discovery. Contradiction discovery
may reveal tension. Correction adds a directional evaluative relationship that
one earlier understanding should no longer be used as asserted.

### Knowledge Replacement

Knowledge replacement is a selection relation in which one understanding is used
instead of another for a purpose.

Replacement says:

```text
Use this claim for this view now.
```

It does not by itself say:

```text
Delete the older claim.
The older claim was never justified.
Reality changed.
```

Replacement may be projection-level, response-level, or selection-level rather
than ontology-level. Replacement can be downstream of revision, correction, or
refinement, but it is not identical to any of them.

### Knowledge Derivation

Knowledge derivation creates a new supported claim, relationship, assessment,
comparison, contradiction record, forecast, or explanation-relevant relation from
existing represented knowledge.

Derivation says:

```text
Given preserved support and an explicit interpretation path, Seed can now
represent this additional claim or relationship.
```

Derivation does not necessarily say:

```text
An older claim changed.
New external evidence arrived.
Reality changed.
A final answer is selected.
```

Derived knowledge may later become the subject of revision, refinement,
correction, replacement, contradiction, or new acquired support.

## 4. Support Expansion Versus Derivation

The prior framing accidentally grouped support expansion and derivation too
closely. Both can change knowledge state, but they change different things.

### Support Expansion

Support expansion changes the support basis for a claim or relationship.

Examples:

- a second package database reports `nginx installed`;
- a host log provides an additional timestamp bound;
- a foreign Seed contributes testimony;
- an operator assertion supplies a corrected environment classification;
- a source is reweighted after authority clarification.

Support expansion usually implies an acquisition path because new support must
come from somewhere. That does not always mean a new domain occurrence happened,
but it usually means Seed received, imported, preserved, or reclassified source
material.

```text
New support arriving
        usually means
new observation, testimony, import, source report, or authority input
        -> new or reclassified evidence
        -> support relation change
```

### Derivation

Derivation changes represented knowledge by creating a new epistemic artifact or
relationship from support that may already be present.

Examples:

- Seed compares Claim A and Claim B and derives that they contradict.
- Seed extrapolates disk usage and derives a future disk-full claim.
- Seed compares identifiers, aliases, and source context and derives `A == B`.
- Seed recalculates that an observation is stale for current-state selection.
- Seed derives a narrower occurrence-time interval from already-preserved sample
  timestamps.

```text
Existing support already present
        -> comparison / interpretation / extrapolation
        -> new derived relationship or claim
```

Derivation may add support to another claim after the derived item exists, but
that downstream support effect should not be confused with the operation that
created the derived item.

## 5. Critical Example: Contradiction Discovery

Existing state:

```text
Claim A exists.
Claim B exists.
No new observations arrive.
Later Seed identifies that A and B contradict.
```

What changed?

The claims did not necessarily change. Their text, scope, support, and
preservation history may be identical before and after discovery.

The support for the individual claims did not necessarily change. Claim A may
have the same evidence after discovery that it had before discovery. Claim B may
also have the same evidence.

The changed object is best characterized as a derived contradiction relationship
or integrity comparison over preserved claims:

```text
Claim A + Claim B + comparison semantics
        -> derived contradiction relationship
```

Additional downstream changes may follow:

- an integrity view may include a contradiction record;
- confidence or selection may be caveated;
- a response may disclose tension;
- an explanation path may show incompatible support paths;
- visibility may change for a particular operator or surface.

The earlier phrase:

```text
the knowledge model changed
```

is directionally true but not precise enough. More precise language is:

```text
Seed derived or recognized a contradiction relationship among preserved claims,
and the knowledge state changed because that relationship became represented,
selectable, explainable, or visible.
```

Contradiction discovery is therefore a knowledge change by derivation, not
necessarily a claim change, support expansion, or reality change.

There are different cases that must not be collapsed:

```text
A and B already comparable and incompatible -> latent contradiction discovered.
A new incompatible claim arrives -> contradiction created by acquisition.
A new semantic rule makes A and B comparable -> comparability changed.
A view starts showing the contradiction -> visibility changed.
A resolution chooses A over B -> selection or replacement changed.
```

## 6. Critical Example: Forecasting

Existing state:

```text
Disk usage observations exist.
Growth-rate observations exist.
Later Seed derives: disk will fill in six months.
```

What changed?

Reality did not change merely because the forecast was derived. The disk may
continue filling at the same rate, slow down, speed up, or be cleaned later.

No future observation occurred. Seed did not observe the disk six months from
now.

The historical observations did not necessarily change. The evidence for disk
usage and growth rate may be identical before and after the forecast.

The changed object is a new derived future claim:

```text
current disk usage claim
+ growth-rate claim
+ capacity claim
+ extrapolation method
+ time horizon / assumptions
        -> derived future claim: disk will fill in six months
```

That future claim may later support an assessment, consequence, recommendation,
decision, plan, or command, but it is not itself an action and not an observation
of the future.

The knowledge state changed because Seed now has an explainable future-oriented
claim with support and assumptions. That is derivation, not support expansion,
unless new observations were also acquired to compute the growth rate.

If later evidence shows the disk did not fill, Seed should preserve both the
forecast and the support path that justified it at the time. The later outcome
may calibrate, contradict, correct, or revise the forecast, but it does not erase
that the forecast existed as supported historical knowledge.

## 7. Critical Example: Identity

Existing state:

```text
Observations already exist.
Later Seed derives: Entity A == Entity B.
```

What changed?

Reality did not change merely because Seed derived the identity. The entity or
entities were already what they were.

The source observations did not necessarily change. Their support may be reused
under a new comparison.

The changed object is best characterized as a derived identity claim or identity
relationship:

```text
observations about A
+ observations about B
+ alias / identifier / source-scope interpretation
        -> derived identity claim: A == B
```

This may trigger downstream knowledge changes:

- support paths previously attached to separate subjects may now be considered
  together;
- claims may become comparable;
- latent contradictions may become discoverable;
- projections may consolidate nodes;
- current-state selection may change;
- historical aliases or provisional identities remain explainable.

Identity derivation may lead to revision if earlier knowledge asserted `A != B`
or if an earlier selected model depended on separateness. Without such an earlier
incompatible assertion, identity derivation is new knowledge, not correction of
old knowledge.

Therefore the precise answer is:

```text
Deriving A == B is primarily new identity knowledge derived from existing
support. It is revision only when it explicitly changes or invalidates an earlier
understanding of identity or scope.
```

## 8. Temporal Example: Outage Interval Revision

A temporal example shows the mixed case where acquisition, derivation, and
revision can all appear.

```text
Initial evidence:
Prometheus shows nginx up at 10:49:45 and down at 10:50:15.

Initial temporal claim:
outage began sometime in [10:49:45, 10:50:15].

Later source material:
host log last application entry at 10:49:59.500.

Later temporal claim:
outage began sometime in [10:49:59.500, 10:50:15].
```

The world did not change again. The outage occurrence did not move.

The later source material is acquisition if Seed newly receives or preserves the
host log.

The revised interval may be derivation if Seed computes the narrower bound from
Prometheus and log semantics.

The temporal claim changed if the asserted interval is claim content. The old
claim is not necessarily wrong. It depends on the claim shape:

```text
If the earlier claim meant:
The best supported bounds are [10:49:45, 10:50:15]
```

then the earlier claim is superseded by a narrower, better-supported bounds
claim.

```text
If the earlier claim meant:
The outage definitely began at 10:49:45
```

then the later claim may correct or contradict the earlier claim.

The distinction is ontological, not storage-specific:

```text
Broad interval as uncertainty bound
        can be refined.
Exact timestamp assertion
        may be corrected.
```

## 9. Relationship To Learning

Learning is better characterized as a combination of acquisition, derivation,
revision, selection improvement, and explanation improvement. It is not one
operation.

Learning includes acquisition when Seed receives observations, evidence,
testimony, operator input, or imports.

Learning includes derivation when Seed produces new claims, relationships,
assessments, contradictions, forecasts, or temporal interpretations from
preserved knowledge.

Learning includes revision when Seed changes how a later understanding relates to
an earlier understanding.

Learning includes refinement when Seed narrows, qualifies, or strengthens an
existing understanding.

Learning includes correction when Seed determines earlier understanding was
mistaken under a relevant boundary.

Learning includes replacement or supersession when Seed selects a different
understanding for current use while preserving the earlier one.

Therefore:

```text
Learning = acquisition and/or derivation and/or revision and/or selection change,
with preserved support and explainability.
```

Learning can occur without new external occurrences. Seed can learn by acquiring
late evidence about an old event, deriving a contradiction from existing claims,
resolving identity from already-preserved observations, applying a more precise
temporal interpretation, or changing which support is trusted for a scoped
purpose.

Learning must not mean:

```text
overwrite history
collapse support into truth
confuse discovery with creation
confuse derivation with acquisition
confuse support expansion with claim revision
confuse current selection with all preserved knowledge
confuse reality change with knowledge change
```

## 10. Is "Knowledge Begets Knowledge" Real?

The phrase "knowledge begets knowledge" is a metaphor if it merely means that
people can talk about old knowledge in new ways.

It is a real architectural operation when Seed creates a new preserved or
explainable epistemic artifact from existing represented knowledge.

Real architectural derivation has these boundaries:

```text
Input: existing represented knowledge and support.
Method: comparison, interpretation, calculation, extrapolation, aggregation, or
        rule application.
Output: a new claim, relationship, assessment, contradiction, forecast,
        temporal interpretation, identity relation, caveat, or explanation path.
Traceability: the output remains linked to its inputs, method, assumptions,
              time, authority, and uncertainty.
Non-collapse: the output is not treated as direct observation or unqualified
              truth.
```

If no new represented artifact, selection effect, explanation path, caveat, or
support relation is preserved or made available for use, then "knowledge begets
knowledge" is only a descriptive metaphor. If a derived result becomes something
Seed can preserve, select, explain, revise, contradict, or expose, then it is an
architectural operation.

## 11. Historical Knowledge

Old knowledge should not be classified with a single label such as "wrong." The
correct classification depends on support, claim shape, derivation path, and
later revision.

Old knowledge may be:

- historically justified, if it was reasonable under the evidence and authority
  available at the time;
- superseded, if a later understanding is preferred for current use;
- partially supported, if some but not all of its assertion remains justified;
- refined, if later knowledge narrows or qualifies it without falsifying it;
- corrected, if later support or derivation shows it was wrong, mis-scoped,
  misidentified, or invalid for its asserted use;
- contradicted, if an incompatible claim remains live in the relevant boundary;
- stale, if it may have been true but is no longer fresh enough for current
  selection;
- derived-from, if its status depends on an inference path rather than direct
  source observation;
- withdrawn, if its source retracts it;
- preserved but not selected, if it remains part of history but not current
  understanding.

Preserving this vocabulary prevents Seed from turning every update into deletion
or every derived claim into direct evidence.

## 12. Cross-Seed And Imported Knowledge

When a remote Seed sends a correction, forecast, contradiction finding, identity
claim, or other derived item, local Seed should treat the incoming material as
foreign testimony, imported support, or a foreign claim. It should not treat the
remote derivation as local direct observation.

What changed locally?

The local Seed acquired foreign support or testimony. Local support relations,
confidence, caveats, and selected claims may change if local authority rules
accept that support for the purpose at hand. Local Seed may also rederive the
claim locally from imported evidence if enough support is available.

Whose knowledge changed?

At minimum, local knowledge changed when local Seed incorporated or interpreted
the remote contribution. Remote knowledge may have changed earlier, when the
remote Seed formed the contribution. A third operator's knowledge may change
later, when a projection or response makes the revision visible.

The remote contribution is not truth transfer. It is support transfer, testimony
transfer, provenance transfer, or claim transfer. Local learning requires local
interpretation under local scope, trust, authority, and selection rules.

## 13. Review Questions

### Can reality remain unchanged while knowledge changes?

Yes. Seed may receive new evidence, reinterpret existing evidence, derive a
contradiction relationship, derive a forecast, refine an occurrence-time
interval, consolidate identity, or change confidence without any new domain
occurrence.

### Can knowledge change without a new observation?

Yes, but the statement is ambiguous unless scoped. Derivation, reinterpretation,
comparison, identity reconciliation, contradiction discovery, stale-status
recalculation, and selection changes can occur over existing preserved knowledge.
Support expansion from a new source usually requires acquisition of a new
observation, testimony, import, or evidence item.

### Can support change without claim content changing?

Yes. Support can change because evidence arrives late, a source is reweighted,
provenance is clarified, corroboration is added, or a support relation is
reinterpreted. Those are epistemic changes.

### Can new knowledge arise without revising old knowledge?

Yes. A forecast, identity claim, contradiction relationship, consequence, or
assessment may be derived as additional knowledge while earlier source claims and
their support remain unchanged.

### Can claim precision improve without claim falsity?

Yes. A broad interval, scoped classification, or caveated claim can be refined
into a narrower or more precise claim while the earlier claim remains
historically justified. Falsity arises only if the earlier claim asserted
something incompatible with the later supported understanding under the relevant
boundary.

### Can contradiction discovery occur without contradiction creation?

Yes. If incompatible claims already existed but were not compared or surfaced,
later discovery derives or recognizes the incompatibility relationship. It
changes represented knowledge and possibly visibility, not necessarily the
claims, their support, or reality.

### Can learning occur without new external occurrences?

Yes. Learning can occur through acquisition of late evidence about old reality,
through derivation from existing support, through reinterpretation, comparison,
identity consolidation, confidence recalculation, support reclassification,
contradiction discovery, forecasting, or temporal refinement.

## 14. Required Distinctions Preserved

Seed should preserve these distinctions explicitly in ontology and future
architecture discussions:

```text
Reality change
Observation acquisition
Evidence preservation
Support expansion
Support reweighting
Claim-content change
Derived claim creation
Derived relationship creation
Knowledge-state change
Confidence change
Selection change
Visibility change
```

and:

```text
Learning
Acquisition
Derivation
Occurrence
Discovery
Creation
Revision
Replacement
Correction
Refinement
Contradiction
Contradiction discovery
Contradiction visibility
Forecasting
Identity derivation
```

The most important practical rule is:

```text
Do not ask only "did knowledge change?"
Ask "which operation occurred and which plane changed?"
```

The relevant planes are:

- domain reality;
- acquisition;
- observation;
- evidence;
- support;
- claim content;
- derived claim or relationship;
- knowledge state;
- integrity comparison;
- identity interpretation;
- temporal interpretation;
- forecasting or future-claim derivation;
- selection;
- projection;
- response visibility;
- historical preservation.

## 15. Original Assumptions Revised Or Rejected

This investigation revises these assumptions from the prior framing:

- **Revised:** "Knowledge change" remains useful, but only as an umbrella term.
  It should not be used when acquisition, derivation, revision, support
  expansion, or selection can be named more precisely.
- **Revised:** "Knowledge change does not require a new observation" should be
  replaced with "knowledge change does not always require a new observation."
- **Rejected:** Contradiction discovery is best described as a generic change to
  "the knowledge model." It is more precisely derivation or recognition of a
  contradiction relationship over preserved claims.
- **Rejected:** Forecasting is merely revision of current knowledge. It is more
  precisely derivation of a future claim from historical and current support,
  assumptions, and a horizon.
- **Rejected:** Identity consolidation always revises old knowledge. It revises
  old knowledge only when earlier identity assumptions are invalidated; otherwise
  it may be new derived identity knowledge.
- **Revised:** Learning is not just revision. It is a family that includes
  acquisition, derivation, revision, refinement, correction, selection, and
  explanation improvement.

## 16. Contradictions Discovered In Prior Framing

The prior framing contained a useful but overbroad pattern:

```text
knowledge changed although reality did not
```

The investigation discovered these tensions:

- It grouped support expansion and derivation under the same "knowledge change"
  language even though new support usually has an acquisition path and derivation
  may not.
- It treated contradiction discovery as knowledge-model change without naming the
  derived contradiction relationship as the changed object.
- It treated identity consolidation as knowledge-model change without separating
  new identity derivation from revision of earlier identity claims.
- It described forecasting-like cases as knowledge change without emphasizing
  that a forecast is a new future claim, not an observation of the future and not
  necessarily revision of an existing claim.
- It risked making "no new observation required" sound universal rather than
  limited to reanalysis, derivation, comparison, selection, or reinterpretation.

These contradictions do not invalidate the earlier reality/knowledge boundary.
They refine it.

## 17. Unresolved Tensions

This reconciliation intentionally does not settle storage, schema, runtime, or
algorithm design. It leaves several ontology-adjacent tensions for future bounded
work:

- when a derived item should be preserved as a first-class claim versus remain an
  explanation path or projection annotation;
- when a change in caveat or lifecycle status should be treated as claim-content
  revision rather than claim metadata revision;
- how much support reweighting is needed before Seed should describe a claim as
  revised rather than merely better supported;
- how to phrase derived contradictions in compact responses without implying that
  Seed created the underlying incompatibility;
- how to distinguish identity derivation from projection node merging in user
  explanations;
- how to distinguish derived forecasts from recommendations when both appear in
  the same operator-facing response;
- how federation should phrase imported derived knowledge when local authority
  accepts the testimony but cannot reproduce the derivation;
- how to explain old knowledge that was justified at the time but later shown to
  be false;
- how to avoid making every projection selection look like an ontological
  replacement;
- how to name derivation outputs consistently without designing a reasoning
  engine, inference engine, or graph system.

These tensions should not block the central boundary: knowledge can change
without reality changing, and new knowledge can arise from derivation without new
observation.

## Non-Goals

This document does not:

- design persistence;
- design claim versioning;
- design event schemas;
- design databases;
- design graph storage;
- design conflict algorithms;
- design reasoning engines;
- design inference engines;
- design planners;
- implement anything;
- modify tests;
- require a new runtime component;
- require a new schema object;
- require old knowledge to be deleted;
- define final UI language for revisions, derivations, contradictions, forecasts,
  or identity claims.

## Final Finding

Knowledge change is an explainable change in Seed's epistemic state: the
preserved and selected structure of observations, evidence, support, confidence,
claims, derived claims, derived relationships, qualifications, comparisons,
identity relations, temporal precision, forecasting outputs, contradiction
recognition, and visibility through which Seed understands the world.

Reality change is a change in the world being represented: an outage occurs, a
service restarts, a package is installed, an entity is renamed, a relationship
begins or ends, or another domain occurrence takes place.

Acquisition changes what source material Seed has preserved or accepted as
support.

Derivation changes what Seed can represent from existing preserved knowledge.

Revision changes how a later understanding relates to an earlier understanding.

Replacement changes which understanding is used for a purpose.

Seed learns without confusing these by preserving the support path and asking:

```text
Did the world change?
Did Seed acquire a new observation, testimony, import, or evidence item?
Did support expand or get reweighted?
Did Seed derive a new claim, relationship, contradiction, identity, forecast, or
assessment from existing knowledge?
Did claim content change?
Did confidence change?
Did selected current understanding change?
Did contradiction discovery or visibility change?
Did historical explanation change?
```

Only the first question is reality change. The rest are acquisition, evidence,
support, derivation, revision, selection, integrity, or visibility changes unless
independently tied to a worldly occurrence.

Therefore the reconciled answer to the central question is:

```text
When knowledge changes, reality need not change.
When new knowledge appears, an old claim need not have been revised.
Some knowledge changes require acquisition.
Some new knowledge arises by derivation from existing observations, evidence,
claims, relationships, assumptions, and support.
```
