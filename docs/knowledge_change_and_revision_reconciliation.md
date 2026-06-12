# Knowledge Change And Revision Reconciliation

## Purpose

This reconciliation defines the ontology boundary for what changes when Seed's
knowledge changes.

It is documentation only. It does not implement code, modify schemas, modify
runtime behavior, design persistence, design claim versioning, design event
schemas, design databases, design graph storage, design conflict algorithms, or
add tests.

The central question is:

```text
What changes when knowledge changes?
```

Not:

```text
What changes when reality changes?
```

This document is subordinate to the repository's existing learning, lifecycle,
integrity, contradiction, observation/evidence/change/event, temporal, ontology,
and architectural-status documents. Repository authority wins over prompt
language.

## Authoritative Context

This reconciliation builds on these existing findings:

- Observation, evidence, claim formation, change, and event are distinct
  architectural concepts.
- A repeated observation may add support while producing no new change.
- Learning changes Seed's represented understanding without erasing the history
  of how that understanding arose.
- Occurrence time is usually a supported temporal claim, not a directly observed
  primitive.
- The world may change once while Seed's understanding of when it changed
  improves many times.
- Contradictions may exist latently before Seed discovers or exposes them.
- Contradiction discovery is not contradiction creation.
- Visibility is not truth.
- Cross-Seed sharing transfers evidence or testimony, not truth.
- Ontology should not be dictated by storage, runtime, projection, or schema
  convenience.

## Executive Summary

Knowledge change is a change in Seed's represented epistemic state: what Seed
currently understands, how strongly it understands it, how that understanding is
supported, what caveats qualify it, what alternatives compete with it, and which
understanding is selected for a purpose.

Knowledge change is not necessarily reality change. Reality may remain exactly
as it was while Seed acquires new evidence, reinterprets existing support,
discovers a contradiction, resolves identity, narrows a temporal interval,
raises confidence, lowers confidence, supersedes an earlier claim, or explains
why an older claim remains historically justified but is no longer current.

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
Knowledge state
        distinct from
Projection / selection / visibility
```

When knowledge changes, the changed thing may be any one of several different
objects or relations. The architecture must therefore avoid treating every
knowledge change as a mutation of the claim itself.

Examples:

- New evidence may strengthen an unchanged claim.
- New evidence may require a revised claim.
- New interpretation may discover that two preserved claims contradict.
- New identity reconciliation may consolidate two subjects without changing the
  real-world entity.
- New temporal support may narrow a claim's occurrence-time interval without
  implying the occurrence happened again or the earlier claim was false.

The core finding is:

```text
Knowledge change is an explainable change in Seed's justified understanding,
selection, support, confidence, qualification, or comparison of preserved
knowledge, while reality change is a change in the world being represented.
```

## Boundary Summary

| Boundary | Reconciled distinction |
| --- | --- |
| Reality change vs knowledge change | Reality change concerns the world. Knowledge change concerns Seed's represented understanding of the world. |
| Support change vs claim change | Support may change without claim content changing. Claim content changes only when the asserted proposition, scope, subject, predicate, value, interval, modality, or qualification changes. |
| Learning vs occurrence | Learning is epistemic. Occurrence is worldly or domain-level. Learning may happen long after the occurrence. |
| Discovery vs creation | Discovery recognizes something already present or already true within a boundary. Creation introduces a new artifact, claim, support relation, projection, or preserved record. |
| Revision vs replacement | Revision creates a new understanding related to an earlier one. Replacement selects one understanding instead of another for a purpose. |
| Correction vs refinement | Correction marks earlier understanding as mistaken, mis-scoped, misidentified, or invalid for a use. Refinement makes understanding more precise without necessarily falsifying the earlier form. |
| Contradiction vs contradiction discovery | Contradiction is incompatibility among comparable claims. Discovery is Seed or an operator recognizing that incompatibility. |
| Contradiction discovery vs visibility | Discovery can exist without being shown. Visibility is surface-, audience-, and selection-dependent. |

## 1. What Is Knowledge Change?

Knowledge change is an epistemic transition in Seed's represented understanding.
It answers:

```text
What does Seed now know, believe, support, doubt, compare, select, or explain
differently than before?
```

Knowledge change may include changes to:

- available evidence;
- support relations between evidence and claims;
- support strength;
- confidence;
- claim content;
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

Knowledge change does not require:

- a new real-world occurrence;
- a changed entity;
- a changed historical fact;
- a new observation;
- a new claim;
- a contradiction;
- a correction;
- erasure of old knowledge.

The architectural question is therefore not merely:

```text
Did a claim change?
```

but:

```text
Which epistemic object, relation, selection, or qualification changed?
```

## 2. What Changes When New Evidence Arrives?

When new evidence arrives and a claim becomes stronger, several different
things may have changed.

The evidence set changed because Seed has additional support material.

The support graph changed because the new evidence may now support an existing
claim, weaken a competing claim, or connect previously separate claims.

The confidence may change if Seed's confidence model treats the new evidence as
corroborating, independent, authoritative, fresh, or otherwise relevant.

The knowledge state changed because Seed's represented understanding is now
better supported, differently qualified, or more selectable for a purpose.

The claim content changes only if the proposition itself changes.

Therefore:

```text
New evidence + stronger same claim
        = support change + confidence/knowledge-state change
        != necessary claim-content change
```

Example:

```text
Initial claim:
nginx is installed on host115.

Later evidence:
A second independent package source reports nginx installed.

Result:
The claim content may remain identical while support and confidence improve.
```

In that case, Seed learned without changing the real host and without replacing
the claim. The changed object is the justified support state around the claim.

## 3. Support Change And Claim Change

Support and claim are independent architectural objects.

A claim answers:

```text
What is asserted, proposed, selected, or represented?
```

Support answers:

```text
Why is that claim justified, doubted, qualified, or selected?
```

Support can change without claim content changing:

- corroborating evidence arrives;
- evidence is reweighted;
- a source is reclassified as more or less authoritative;
- an observation is found to be stale;
- a support path is found to be indirect rather than direct;
- a remote Seed contributes testimony;
- a competing claim receives stronger support.

Claim content can change without new external support if existing preserved
support is reinterpreted:

- a parser bug is found in the interpretation layer;
- an identity boundary changes which subject a claim is about;
- a predicate is recognized as scoped rather than global;
- an earlier temporal interval is narrowed from the same observations;
- an authority rule changes which preserved claim is selected.

Claim content should be considered changed when Seed asserts a different
proposition, including changes to:

- subject identity;
- predicate;
- value;
- temporal interval;
- cardinality;
- modality;
- scope;
- caveat;
- negation;
- lifecycle status, when lifecycle status is part of the assertion being made.

Support change may cause claim change, but it does not entail claim change.

## 4. Revision, Replacement, Correction, And Refinement

The word "change" is too broad for knowledge. Seed needs finer ontology.

### Knowledge Revision

Knowledge revision is the creation or recognition of a later understanding that
is explicitly related to an earlier understanding.

Revision says:

```text
Seed now understands this differently.
```

Revision may be a correction, refinement, narrowing, expansion, consolidation,
or replacement. It should not imply erasure.

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
than ontology-level.

### Knowledge Supersession

Knowledge supersession is a lifecycle relation where a later understanding is
preferred over an earlier one while preserving the earlier understanding as
history.

Supersession may occur because the later claim is fresher, more authoritative,
more precise, better supported, or better scoped.

### Knowledge Consolidation

Knowledge consolidation merges or relates previously separate knowledge paths
into a shared understanding.

The most important case is identity consolidation:

```text
Earlier: entity A and entity B appear separate.
Later: corroboration indicates A and B are the same entity.
```

The real entity did not split or merge merely because Seed learned the identity
relation. The knowledge model changed.

### Knowledge Narrowing

Knowledge narrowing reduces the set of possible worlds compatible with Seed's
understanding.

Temporal refinement is a common narrowing:

```text
Outage occurred within a smaller interval than previously known.
```

Narrowing does not imply the earlier broader claim was false when the earlier
claim was explicitly a bounds claim.

### Knowledge Expansion

Knowledge expansion adds new scope, relations, support, or possibilities to
Seed's understanding.

Expansion may include discovering additional affected hosts, adding a new
support source, or recognizing that a claim applies across a larger dimension.
Expansion can be compatible with earlier narrower knowledge if the earlier
knowledge did not assert exclusivity.

## 5. Temporal Example: Outage Interval Revision

Consider:

```text
Initial support:
Prometheus evidence

Supported claim:
Outage occurred between
10:49:45 and 10:50:15

Later support:
Host logs

Revised claim:
Outage occurred between
10:49:59.500 and 10:50:15
```

The outage did not change. The outage occurrence is the domain event being
represented. Unless there was another outage or a changed real-world state, the
worldly occurrence remains the same.

The support changed. Seed now has host logs in addition to Prometheus evidence,
and the support basis for the outage interval has improved.

The claim changed if the claim content is the asserted interval. The revised
claim asserts a narrower lower bound.

The knowledge changed because Seed's represented understanding became more
precise and better supported.

The old claim is not necessarily wrong. It depends on the claim shape:

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

## 6. Contradiction Example: Latent Incompatibility And Later Discovery

Consider:

```text
Two incompatible claims exist.
No one notices.
Later contradiction discovery occurs.
```

The contradiction did not necessarily appear at discovery time. If the claims
and the comparison semantics already made them incompatible, the contradiction
was latent in preserved knowledge.

What changed at discovery time was Seed's knowledge about its own preserved
knowledge:

- the incompatibility became recognized;
- an integrity view may have gained a contradiction record;
- an explanation path may now show competing support;
- a response may now disclose a caveat;
- selection may downgrade confidence or avoid a single-current answer.

Discovery changed knowledge and possibly visibility. It did not necessarily
change reality, and it did not necessarily create the contradiction.

However, contradiction creation can occur when a new incompatible claim is added
or when a newly adopted semantic rule makes previously incomparable claims
comparable. Seed should distinguish:

```text
Contradiction existed but was undiscovered.
Contradiction was created by adding an incompatible claim.
Contradiction became comparable because interpretation changed.
Contradiction became visible because a surface exposed it.
```

Those are different architectural transitions.

## 7. Identity Example: Consolidation Without Reality Change

Consider:

```text
Two entities appear separate.
Later corroboration indicates
they are the same entity.
```

Reality did not change merely because Seed learned an identity relation. The
real-world entity or entities were already what they were.

What changed was Seed's knowledge model:

- identity resolution changed;
- support paths may now attach to the same subject;
- previously separate claims may become comparable;
- latent contradictions may be discovered;
- projections may consolidate nodes;
- historical aliases or provisional identities remain explainable.

Identity consolidation is therefore a knowledge change with possible downstream
selection and contradiction effects. It is not an occurrence unless something in
the domain actually merged, split, was renamed, or reassigned.

## 8. Learning Connection

Learning is best understood as a family of knowledge changes, not a single
operation.

Learning can be:

```text
knowledge acquisition
knowledge revision
knowledge refinement
knowledge correction
knowledge consolidation
knowledge selection improvement
knowledge explanation improvement
```

Learning includes acquisition when Seed receives observations, evidence,
testimony, operator input, or imports.

Learning includes revision when Seed changes how it understands preserved
knowledge.

Learning includes refinement when Seed narrows, qualifies, or strengthens an
existing understanding.

Learning includes correction when Seed determines earlier understanding was
mistaken under a relevant boundary.

Learning may occur without new external occurrences. Seed can learn by
reanalyzing old evidence, discovering a contradiction, resolving identity,
applying a more precise temporal interpretation, or changing which support is
trusted for a scoped purpose.

Learning must not mean:

```text
overwrite history
collapse support into truth
confuse discovery with creation
confuse current selection with all preserved knowledge
confuse reality change with knowledge change
```

## 9. Historical Knowledge

Old knowledge should not be classified with a single label such as "wrong".
The correct classification depends on support, claim shape, and later revision.

Old knowledge may be:

- historically justified, if it was reasonable under the evidence and authority
  available at the time;
- superseded, if a later understanding is preferred for current use;
- partially supported, if some but not all of its assertion remains justified;
- refined, if later knowledge narrows or qualifies it without falsifying it;
- corrected, if later knowledge shows it was mistaken, mis-scoped, or
  misidentified;
- contradicted, if an incompatible claim remains live in the relevant boundary;
- retracted, if the source withdrew it;
- stale, if it may have been true but is not fresh enough for current selection;
- historical only, if preserved for explanation but not eligible as current
  knowledge.

The architecture should preserve the distinction between:

```text
This was once justified.
This is still true.
This is selected now.
This was later corrected.
This is incompatible with another claim.
```

## 10. Federation Implications

Consider:

```text
Remote Seed contributes new support.
Local claim changes.
```

What changed remotely?

The remote Seed's knowledge changed only if the remote Seed acquired, revised,
selected, or exposed something differently in its own knowledge state. Sending a
message does not by itself make the remote world change.

What changed locally?

The local Seed acquired foreign support or testimony. Local support relations,
confidence, caveats, and selected claims may change if local authority rules
accept that support for the purpose at hand.

Whose knowledge changed?

At minimum, local knowledge changed when the local Seed incorporated or
interpreted the remote contribution. Remote knowledge may have changed earlier,
when the remote Seed formed the contribution. A third operator's knowledge may
change later, when a projection or response makes the revision visible.

The remote contribution is not truth transfer. It is support transfer,
testimony transfer, provenance transfer, or claim transfer. Local learning
requires local interpretation under local scope, trust, authority, and selection
rules.

Therefore:

```text
Remote support arrives.
Local support graph changes.
Local confidence or claim selection may change.
Reality need not change.
Remote truth does not automatically become local truth.
```

## 11. Review Questions

### Can reality remain unchanged while knowledge changes?

Yes. Seed may receive new evidence, reinterpret existing evidence, discover a
contradiction, refine an occurrence-time interval, consolidate identity, or
change confidence without any new domain occurrence.

### Can support change without reality changing?

Yes. Support can change because evidence arrives late, a source is reweighted,
provenance is clarified, corroboration is added, or a support relation is
reinterpreted. Those are epistemic changes.

### Can claim precision improve without claim falsity?

Yes. A broad interval, scoped classification, or caveated claim can be refined
into a narrower or more precise claim while the earlier claim remains
historically justified. Falsity arises only if the earlier claim asserted
something incompatible with the later supported understanding under the relevant
boundary.

### Can contradiction discovery occur without contradiction creation?

Yes. If incompatible claims already existed but were not compared or surfaced,
later discovery changes recognition and possibly visibility, not the existence
of the incompatibility.

### Can learning occur without new external occurrences?

Yes. Learning can occur through reinterpretation, comparison, identity
consolidation, confidence recalculation, support reclassification, contradiction
discovery, or temporal refinement over preserved evidence.

## 12. Required Distinctions Preserved

Seed should preserve these distinctions explicitly in ontology and future
architecture discussions:

```text
Reality change
Knowledge change
Support change
Claim change
Confidence change
Selection change
Visibility change
```

and:

```text
Learning
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
```

The most important practical rule is:

```text
Do not ask only "what changed?"
Ask "which plane changed?"
```

The relevant planes are:

- domain reality;
- acquisition;
- evidence;
- support;
- claim content;
- knowledge state;
- integrity comparison;
- selection;
- projection;
- response visibility;
- historical preservation.

## 13. Unresolved Tensions

This reconciliation intentionally does not settle storage or algorithm design.
It leaves several ontology-adjacent tensions for future bounded work:

- when a change in caveat or lifecycle status should be treated as claim-content
  revision rather than claim metadata revision;
- how to name and expose historically justified but no-longer-selected claims in
  compact responses;
- how much support reweighting is needed before Seed should describe a claim as
  revised rather than merely better supported;
- how to distinguish identity consolidation from projection node merging in user
  explanations;
- how federation should phrase imported support when local authority rejects it;
- how to explain old knowledge that was justified at the time but later shown to
  be false;
- how to avoid making every projection selection look like an ontological
  replacement.

These tensions should not block the central boundary: knowledge can change
without reality changing.

## Non-Goals

This document does not:

- design persistence;
- design claim versioning;
- design event schemas;
- design databases;
- design graph storage;
- design conflict algorithms;
- implement anything;
- modify tests;
- require a new runtime component;
- require a new schema object;
- require old knowledge to be deleted;
- define final UI language for revisions.

## Final Finding

Knowledge change is an explainable change in Seed's epistemic state: the
preserved and selected structure of evidence, support, confidence, claims,
qualifications, comparisons, identity relations, temporal precision,
contradiction recognition, and visibility through which Seed understands the
world.

Reality change is a change in the world being represented: an outage occurs, a
service restarts, a package is installed, an entity is renamed, a relationship
begins or ends, or another domain occurrence takes place.

Seed learns without confusing the two by preserving the support path and asking
which plane changed:

```text
Did the world change?
Did Seed observe something?
Did evidence arrive?
Did support change?
Did confidence change?
Did claim content change?
Did selected current understanding change?
Did contradiction discovery or visibility change?
Did historical explanation change?
```

Only the first question is reality change. The rest are knowledge, support,
selection, integrity, or visibility changes unless independently tied to a
worldly occurrence.

Therefore the reconciled answer to the central question is:

```text
When knowledge changes, reality need not change.
What changes is Seed's justified, preserved, and explainable understanding of
reality.
```
