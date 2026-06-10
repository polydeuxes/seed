# Learning and Knowledge Change Reconciliation

## Purpose

This reconciliation defines the architectural boundary for how Seed changes what
it knows over time without destroying history, provenance, support paths, or
explainability.

It is documentation only. It does not implement code, modify schemas, modify
runtime behavior, modify observations, modify evidence handling, modify claims,
modify events, modify projections, modify federation behavior, modify trust
models, modify authority systems, modify identity models, or add tests. It does
not introduce new runtime semantics.

## Executive Summary

Seed evolves by adding, interpreting, qualifying, selecting, and explaining
preserved knowledge. It should not evolve by silently overwriting the record of
what it previously observed, imported, claimed, projected, trusted, doubted, or
explained.

The central finding is:

```text
Learning changes Seed's current understanding; it must not erase Seed's
historical record of how that understanding arose.
```

A later observation that `nginx stopped` does not delete the earlier observation
that `nginx running` was reported. It changes the current-state selection for the
service when the later observation has the appropriate temporal scope and
support. An operator correction that `host115 is not production` does not make
the earlier production classification disappear. It creates an explainable
correction path that distinguishes the earlier mistaken or obsolete claim from
later corrected understanding. A foreign Seed correction does not become a local
observation; it remains an imported revision or withdrawal with foreign
provenance and optional local promotion.

The safest architectural model is:

```text
Preserved history + preserved support + preserved qualifications
    -> projection and selection rules
    -> current understanding for a purpose
```

Knowledge change is therefore not the same thing as event occurrence, state
change, contradiction, or projection refresh. Those may contribute to knowledge
change, but knowledge change is the explainable evolution of Seed's represented
understanding across time, scope, support, and authority.

## Files Considered

This reconciliation builds on the existing architecture and adjacent
reconciliations, especially:

- `docs/knowledge_acquisition_and_selection.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `docs/knowledge_maintenance_reconciliation.md`
- `docs/contradiction_handling_audit.md`
- `docs/event_and_change_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/fact_confidence_and_corroboration_reconciliation.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/cross_seed_provenance_and_federation_reconciliation.md`
- `docs/natural_language_observation_and_intent_derivation_reconciliation.md`
- `docs/read_model_inventory_and_authority_reconciliation.md`
- `docs/state.md`
- `docs/invariants.md`

## Boundary Summary

| Concept | Architectural definition | Preserves history? | Common confusion to avoid |
| --- | --- | --- | --- |
| Learning | Seed's acquisition or improvement of represented understanding through preserved observations, evidence, claims, qualifications, projections, and explanations. | Yes | Learning is not replacement or erasure. |
| Knowledge change | An explainable change in Seed's represented understanding, confidence, qualification, or selected current view. | Yes | Knowledge change is not merely an event or projection refresh. |
| Correction | An explicit or inferable update that marks prior understanding as mistaken, mis-scoped, misidentified, misinterpreted, stale, or otherwise not valid for the asserted use. | Yes | Correction is not mere disagreement. |
| Contradiction | Coexistence of incompatible or tensioned claims within a relevant scope. | Yes | Contradiction does not automatically mean error. |
| Revision | A new version, interpretation, or qualification of an earlier claim, import, projection export, or understanding. | Yes | Revision is not always correction. |
| Supersession | A later item becomes preferred for a selection purpose while the earlier item remains preserved. | Yes | Supersession is not deletion or historical invalidation. |
| Retraction | A source or authority withdraws a claim, assertion, import, or endorsement. | Yes | Retraction is not erasure. |
| Replacement | A selection or modeling relationship in which one value is used instead of another for a purpose. | Usually | Replacement is often projection-level, not knowledge-level. |
| Forgetting | Deliberate loss, non-selection, archival, or inability to use knowledge depending on policy and representation boundary. | Depends | Forgetting must not be conflated with ordinary projection omission. |
| Historical preservation | Retention of prior observations, support, claims, projections, contradictions, and authority decisions as explainable history. | Yes | Historical preservation does not mean current endorsement. |
| Current-state selection | Projection choice of the currently applicable value or interpretation for a purpose. | Yes | Current state is not entire history. |

## 1. What Is Learning?

Learning is the process by which Seed improves or extends its represented
understanding while preserving the support path that made the improvement
possible.

Learning may include:

- acquiring observations;
- preserving evidence;
- interpreting observations into candidate claims;
- normalizing or promoting claims within explicit support and authority bounds;
- accumulating corroboration or conflict signals;
- changing confidence, caveats, or freshness characterization;
- updating projections or selected context from preserved support;
- discovering that prior understanding was wrong, stale, too broad, or
  insufficiently supported;
- preserving foreign revisions, withdrawals, or corrected imports with foreign
  provenance.

Learning is not limited to one layer. It is not only observation ingestion, not
only claim creation, not only confidence change, and not only projection update.
Architecturally, learning is a cross-layer effect over preserved knowledge:

```text
new or reinterpreted support changes what Seed can responsibly understand,
select, explain, or qualify.
```

Learning can occur without a new external observation. Examples include:

- a projection is re-run over existing events and exposes a previously hidden
  contradiction;
- an operator clarifies identity scope for an existing entity;
- an imported foreign claim is reclassified as testimony rather than local
  evidence;
- confidence changes because support was re-evaluated;
- a stale observation becomes less usable for current-state selection.

Learning can also occur without changing current state. For example, receiving a
second independent report that `nginx is running` may improve corroboration and
explainability while leaving the selected state unchanged.

### Learning Is Not Erasure

Learning should preserve explainability. If Seed previously selected `host115 is
production` and later learns that `host115 is not production`, an explanation
should be able to distinguish:

```text
previous support for production classification
later correction or reclassification
authority or source behind the correction
current selected classification
reason the earlier classification is not currently selected
```

The earlier claim may become wrong for current use, but its existence remains
part of Seed's learning history.

## 2. What Is Knowledge Change?

Knowledge change is an explainable change in Seed's represented understanding or
selected use of represented understanding.

It answers:

```text
What does Seed understand differently now, and why?
```

Knowledge change may involve changes in:

- available observations;
- evidence support;
- claim set;
- claim scope;
- confidence or strength;
- freshness and staleness characterization;
- contradiction status;
- authority status;
- provenance interpretation;
- current-state projection;
- selected context or answerability;
- explanation path.

Knowledge change differs from adjacent concepts:

| Adjacent concept | Difference from knowledge change |
| --- | --- |
| Event occurrence | An event happens in the world or operational domain. Knowledge change occurs when Seed's represented understanding changes because of preserved information about the event. |
| State change | A state transition can be represented as knowledge, but knowledge change is the change in Seed's understanding of the state, not necessarily the state transition itself. |
| Contradiction | Contradiction is tension between claims. Knowledge change may detect, preserve, explain, or resolve that tension, but the contradiction itself is not automatically a correction. |
| Projection change | Projection change is a read-model or selection change over preserved support. Knowledge change may be expressed through projection, but projection refresh is not knowledge replacement. |

Example:

```text
Yesterday observation: nginx running at T1
Today observation:     nginx stopped at T2
```

If `T1` and `T2` are distinct temporal scopes, the knowledge change is not that
`running` became false historically. The change is that Seed now understands the
service state history as including a transition or later current state. The
current-state projection may select `stopped`; the historical record still
contains `running at T1`.

## 3. What Is Correction?

Correction is an explicit or inferable change that identifies prior
understanding as mistaken, mis-scoped, misidentified, misinterpreted,
misattributed, stale for a purpose, or otherwise not valid under its previous
use.

Correction answers:

```text
What was wrong or inappropriate about the prior understanding, and what support
or authority explains the change?
```

Examples:

```text
Operator correction: host115 is not production.
Foreign Seed correction: previously imported claim C was wrong.
Identity correction: host115 and host151 are different hosts, not aliases.
Scope correction: nginx running was true only inside container X, not host H.
```

Correction differs from contradiction because contradiction only records tension.
Correction adds a relationship of error, withdrawal, mis-scope, or revised
authority between earlier and later understanding.

A correction should preserve:

- the corrected item;
- the correction assertion;
- the source or authority of the correction;
- the support path for both the original and corrective understanding;
- the reason the correction changes current selection or explanation;
- any remaining historical value of the corrected item.

A corrected claim may remain useful as evidence of what was believed, imported,
reported, projected, or operationally acted upon at a prior time.

## 4. What Is Contradiction?

Contradiction is the coexistence of claims, values, interpretations, or
projections that cannot all be accepted as simultaneously valid within the same
relevant scope.

Contradiction answers:

```text
What cannot all be true, selected, or applied together under the same scope?
```

Contradiction may indicate:

- disagreement between sources;
- temporal ambiguity;
- identity confusion;
- scope mismatch;
- stale data;
- source error;
- projection bug or modeling limitation;
- authority conflict;
- genuine uncertainty.

Contradiction implies disagreement when incompatible claims are preserved but no
architectural authority or support path has established that one is a correction
of the other.

Contradiction implies actual correction only when additional support,
authority, or explicit withdrawal identifies one side as mistaken,
mis-scoped, superseded for the asserted use, or no longer endorsed.

Examples:

```text
Source A: host115 is production.
Source B: host115 is not production.
```

This is contradiction or disagreement until Seed can explain why one source's
statement corrects the other, or why scope separates them.

```text
At T1: nginx running.
At T2: nginx stopped.
```

This is not a contradiction if the temporal scopes are distinct. It is a state
history or change.

## 5. What Is Revision?

Revision is a newer version, interpretation, qualification, or statement about a
previously represented item.

Revision answers:

```text
How has this represented item or its interpretation changed across versions or
statements?
```

Revision differs from related concepts:

| Concept | Difference |
| --- | --- |
| Correction | A correction is a revision that identifies prior understanding as wrong, mis-scoped, or inappropriate for its prior use. Not every revision says the prior version was wrong. |
| Replacement | Replacement selects or uses one item instead of another. A revision may cause replacement, but revision itself is versioned change. |
| Supersession | Supersession means a later item becomes preferred for a selection purpose. A revision may supersede an earlier revision without invalidating it historically. |
| Retraction | Retraction withdraws an assertion or endorsement. A revision may narrow or update a claim without withdrawing it. |

Examples:

```text
Inventory export v2 includes newer package list than v1.
Foreign Seed sends revised claim C2 derived from earlier claim C1.
Operator narrows claim from "host115 is production" to "host115 was production before migration M".
```

Revision should preserve lineage: what was revised, by whom or what source, at
what time, under what authority, and with what support.

## 6. What Is Supersession?

Supersession is a relationship in which a later or stronger item becomes the
preferred item for a selection purpose while the earlier item remains preserved.

Supersession answers:

```text
Which item should be used now for this purpose, and what earlier item did it
supersede?
```

Examples:

```text
newer inventory snapshot supersedes older inventory snapshot for current package state
new service observation supersedes prior service observation for current-state selection
operator-approved identity classification supersedes imported tentative classification
```

Supersession differs from deletion because the superseded item remains available
for history, provenance, audit, trend analysis, and explanation.

Supersession differs from contradiction because two temporally ordered inventory
snapshots may disagree in values without being contradictory. The later snapshot
may simply be the current selector.

Supersession differs from historical invalidation because the earlier item may
still have been true, useful, or correctly reported at its time.

Supersession is often a projection or selection relationship:

```text
preserved earlier support + preserved later support -> current selector chooses later support
```

It should not be modeled as if the later item destroyed the earlier knowledge.

## 7. What Is Retraction?

Retraction is a withdrawal of a claim, assertion, endorsement, import,
projection export, or authority statement by a source or authority.

Retraction answers:

```text
What is no longer asserted or endorsed by this source, and what record of that
withdrawal exists?
```

Examples:

```text
operator withdraws the claim that host115 is production
foreign Seed withdraws an exported assertion
source system retracts a previously published inventory record
```

After retraction, the following should survive:

- the original claim or imported assertion;
- the original support and provenance;
- the retraction event or assertion;
- the retracting source and authority scope;
- the time of retraction;
- any reason or evidence attached to the retraction;
- the fact that the item was once asserted, imported, selected, or acted upon;
- any downstream explanation that depends on historical assertion.

Retraction should usually remove or reduce current endorsement. It should not
erase the fact that the assertion existed.

Retraction differs from correction because a source may retract without stating
the earlier assertion was false. It may retract because of uncertainty, lost
authority, policy, expiration, redaction, or changed scope.

## 8. What Is Replacement?

Replacement is the use of one item instead of another for a particular purpose.

Replacement may appear at several levels, but its safest architectural home is
often projection or selection rather than preserved knowledge itself.

| Level | Replacement interpretation |
| --- | --- |
| Observation | Raw observations should rarely be replaced. A later observation may supersede a prior one for current selection, but the prior report remains preserved. |
| Evidence | Evidence should not be silently replaced. New evidence may be added, support may be reweighted, and unusable evidence may be marked withdrawn or invalid for a purpose. |
| Claim | Claims may be revised, corrected, retracted, or superseded. The older claim should remain explainable. |
| Projection | Projections commonly replace selected current values because they are views over preserved support. |
| Context/response | Selected context or response text may replace an earlier answer for the current interaction without rewriting knowledge history. |

Replacement becomes dangerous when it is treated as destructive mutation of
history. Safer terminology is often:

```text
superseded for current-state selection
corrected by later authority
retracted by source
revised by later version
not selected because stale or unsupported
```

## 9. What Is Forgetting?

Forgetting is loss of usable access to knowledge, support, or selection
eligibility. It must be defined explicitly because several different operations
can look like forgetting.

Possible forms:

| Form | Meaning | Architectural consequence |
| --- | --- | --- |
| Deletion | Data is removed from preserved history. | Strongest form; threatens explainability unless explicitly authorized and recorded elsewhere. |
| Archival | Data is retained but moved out of normal selection or fast access. | History survives; selection may need archive-aware explanation. |
| Projection omission | Data is preserved but not selected into a projection or response. | Not true forgetting; current view is narrower than history. |
| Support loss | Seed can no longer explain or verify why a claim was held. | Severe explainability degradation even if claim text remains. |
| Authority expiry | A claim is retained but no longer usable under current authority or policy. | Historical assertion survives; current endorsement changes. |
| Privacy or retention redaction | Some payload is intentionally removed or obscured. | Remaining metadata should explain that redaction occurred if policy allows. |

Architecturally, ordinary learning should not require forgetting. Projection
omission and supersession are not forgetting. Retraction is not forgetting.
Correction is not forgetting. Forgetting should be reserved for explicit
retention, privacy, archival, or support-loss semantics.

## 10. What Survives Knowledge Change?

The following should survive ordinary learning, correction, revision,
supersession, retraction, and projection change:

- provenance;
- source identity and source class;
- local versus foreign origin;
- import path and foreign provenance where applicable;
- observation records;
- evidence records or evidence summaries sufficient for explanation;
- claim identity and claim lineage;
- support relationships;
- contradiction records and conflict signals;
- correction assertions and corrective authority;
- revision lineage;
- supersession relationships;
- retraction records;
- historical state and temporal scope;
- confidence, strength, caveat, and freshness history when represented;
- authority decisions and authority scope;
- trust context and trust limitations;
- projection rationale or traceability to underlying support;
- explanation paths used for prior or current answers.

Survival does not mean current endorsement. A preserved claim may be stale,
wrong, retracted, superseded, contradicted, foreign, weakly supported, or outside
current authority. Its preservation means Seed can explain its history and why it
is or is not currently selected.

## 11. Relationship Between Learning and History

Learning and history must be complementary.

Learning should preserve prior understanding because Seed's answers depend not
only on what it currently selects but also on why earlier selections were made,
why they changed, and what evidence caused the change.

Learning cannot safely erase history as an ordinary architectural operation.
There may be explicit retention or privacy policies that remove data, but those
are separate from learning itself.

Historical claims after later evidence arrives should be represented as
historical, qualified, or superseded rather than silently invalidated.

Examples:

```text
Claim at T1: nginx running.
Claim at T2: nginx stopped.
Current-state selection at T2: nginx stopped.
Historical state remains: nginx was reported running at T1.
```

```text
Imported claim at I1: Foreign Seed A reports host115 is production.
Foreign revision at I2: Seed A reports prior classification was wrong.
Local current selection: host115 not production, if local authority accepts or promotes the revision.
Historical import remains: Seed A previously reported production classification.
```

```text
Operator correction at C1: host115 and host151 are distinct hosts.
Current identity model: distinct entities.
Historical understanding remains: earlier aliasing or conflation occurred and can be explained.
```

## 12. What Should Not Be Collapsed Together?

### Correction != Contradiction

Contradiction preserves tension. Correction identifies an error, mis-scope, or
withdrawn use. Collapsing them would let any disagreement erase one side before
Seed can explain why.

### Supersession != Deletion

Supersession selects a later or stronger item for a purpose. Deletion removes
history. Collapsing them would destroy auditability and temporal reasoning.

### Learning != Replacement

Learning may add support, improve confidence, expose contradictions, or qualify
claims without replacing anything. Collapsing learning into replacement makes
Seed look like a mutable current-state store rather than an explainable
knowledge system.

### Historical Claim != Invalid Claim

A claim may be historically true, historically asserted, or historically useful
even if it is not currently selected. Collapsing historical with invalid would
make state transitions and prior decisions unexplainable.

### New Evidence != New Truth

New evidence changes support. It may corroborate, contradict, weaken, correct,
or leave current understanding unchanged. Collapsing evidence with truth would
bypass trust, authority, confidence, and contradiction handling.

### Projection Change != Knowledge Change

A projection change may be a view refresh, selector change, or current-state
update over the same preserved support. It can express knowledge change, but it
is not the whole of knowledge change.

### Retraction != Erasure

Retraction withdraws assertion or endorsement. Erasure removes the record.
Collapsing them would make it impossible to explain that a claim was once made
and later withdrawn.

### Current State != Entire History

Current-state selection answers what should be used now for a purpose. History
answers what was observed, claimed, believed, contradicted, corrected, and
selected over time.

### Import Revision != Local Observation

A foreign revision is local evidence that a foreign source revised something. It
is not the receiving Seed's local observation of the underlying world. Collapsing
these would destroy federation provenance and local authority boundaries.

## Current-State Selection Boundary

Current-state selection is a projection responsibility over preserved knowledge.
It answers:

```text
Given time, scope, support, confidence, authority, and freshness, which value or
interpretation should be used now for this purpose?
```

Current-state selection may choose:

- the most recent observation in a temporal sequence;
- the strongest supported claim;
- the locally authoritative correction;
- the non-retracted version;
- the least stale value;
- a conflicted state with caveats rather than a single value.

Current-state selection should remain traceable to underlying support and should
not imply that non-selected historical items disappeared.

## Support Preservation Boundary

Support preservation is the requirement that Seed retain enough provenance,
evidence, source, scope, and lineage information to explain why knowledge was
created, changed, selected, or rejected.

Support preservation applies especially to:

- corrections, because the corrective authority must be explainable;
- contradictions, because disagreement should survive before resolution;
- supersession, because current selection should explain what it superseded;
- retractions, because withdrawal must be distinguishable from erasure;
- federation, because foreign revisions must preserve foreign provenance;
- projection changes, because selected state should trace to support changes or
  selector rules.

A claim without support may remain textually present, but it loses much of its
architectural value because Seed cannot explain why it was known, believed,
challenged, corrected, or selected.

## Example Reconciliations

### Yesterday `nginx running`, Today `nginx stopped`

What changed:

- the service's represented state history gained a later state;
- current-state selection may move from `running` to `stopped`;
- the prior `running` claim remains historically useful if scoped to yesterday;
- contradiction exists only if both states are asserted for the same temporal
  scope without a transition model.

### Operator Correction: `host115 is not production`

What changed:

- Seed gained a corrective claim from an operator source;
- current classification may change if the operator has authority for that
  classification;
- the prior production classification remains preserved as prior understanding;
- explanation should show why the correction overrides or qualifies the prior
  classification.

### Foreign Seed Correction: Previously Imported Claim Was Wrong

What changed:

- the receiving Seed gained local evidence that the foreign Seed revised or
  corrected a foreign claim;
- the original import remains foreign-origin knowledge;
- the correction remains foreign-origin revision unless locally promoted;
- local projection may change only under local trust and authority boundaries;
- provenance should show both the original foreign assertion and the later
  foreign correction.

### New Observation: Service Recovered

What changed:

- the state history gained a recovery observation;
- current-state selection may move from `stopped` to `running` or `healthy`;
- the outage state remains historically true for its interval;
- impact, consequence, or recommendation explanations may still cite the outage
  period.

## Non-Goals

This reconciliation does not define or require:

- a new `LearningEngine`;
- a new `KnowledgeChangeEngine`;
- new schema fields;
- new runtime mutation paths;
- new projection algorithms;
- new contradiction resolution behavior;
- new trust, authority, or identity systems;
- new federation protocols;
- destructive replacement semantics;
- automatic correction from contradiction;
- automatic truth transfer from imports;
- automatic deletion after retraction;
- any test changes.

## Implementation Implications

The established findings imply architectural guardrails rather than immediate
implementation work:

- documentation and future designs should describe learning as explainable
  evolution over preserved support;
- future correction features should preserve corrected items and corrective
  support instead of overwriting claims;
- future projection work should distinguish current-state selection from
  historical replacement;
- future federation work should treat foreign revisions as imported foreign
  provenance, not local observations;
- future retention or privacy work should explicitly distinguish forgetting from
  ordinary non-selection, supersession, correction, or retraction;
- future explanation surfaces should be able to show why a current selection
  changed without implying that earlier history was deleted.

These are not implementation recommendations beyond preserving the boundaries
already established by existing architecture documentation.

## Architectural Invariants

The findings support the following invariants:

1. Learning changes understanding, not history.
2. Knowledge evolution should preserve provenance.
3. Corrections should remain explainable.
4. Contradictions should survive long enough to be explained.
5. Contradiction does not automatically imply error.
6. Supersession does not imply deletion.
7. Retraction does not imply erasure.
8. Historical claims remain historical even when not currently selected.
9. Current-state selection is not historical replacement.
10. Projection changes should remain traceable to underlying support changes or
    selector rules.
11. Imported knowledge revisions should preserve foreign provenance.
12. New evidence is not automatically new truth.
13. Support loss is an explainability loss.
14. Learning should preserve the ability to answer `what changed and why?`.
