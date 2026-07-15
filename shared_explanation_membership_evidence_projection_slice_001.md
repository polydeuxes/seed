# Shared Explanation Membership Evidence Projection Slice 001

## Recovered responsibility

This slice performs exactly one bounded **Shared Explanation Membership Evidence Projection Slice**.

Recovered responsibility:

```text
given:
  one explicit bounded inquiry
  one candidate SharedExplanationRenderingProjection
  preserved source-lineage evidence for that candidate

project:
  one per-candidate membership evidence result:
    belongs
    does_not_belong
    unknown
    conflict

without:
  selecting a set
  sequencing explanations
  composing a view
  ranking blockers
  comparing stage states
  inferring semantic relevance
  deduplicating duplicate identities
  inventing missing projections
  creating handoffs
  authorizing or executing movement
  writing events
  mutating cluster state
```

The projection answers only the core question:

```text
Given one explicit bounded inquiry,
one candidate shared explanation rendering projection,
and its preserved source-lineage evidence,

what lawful per-candidate membership result
can Seed establish?
```

Membership evidence remains distinct from membership selection. This slice produces one result for one candidate and does not produce a selected collection.

## Source inquiry and candidate boundaries

### Source inquiry boundary

The source inquiry must be explicit and bounded. Lawful inquiry references may include repository-supported identity forms such as:

- bounded question identity;
- bounded inquiry reference;
- source request identity;
- exact demand identity;
- exact work or probe identity;
- handoff identity connected to the bounded inquiry;
- provenance or derivation references connected to the bounded inquiry.

A natural-language resemblance to the operator's question is not enough. Operator wording is not promoted into membership truth without preserved identity or lineage evidence.

### Candidate boundary

The candidate is exactly one already-produced `SharedExplanationRenderingProjection`.

The candidate may preserve rendering-level identity and stage-owned material, including:

- candidate rendering projection identity;
- source explanation identity;
- source artifact owner;
- source explanation type;
- source state and source reason as rendering labels;
- preserved Unknowns;
- preserved conflicts;
- prohibited downstream movement;
- explanation boundary;
- opaque stage-owned material.

The candidate's rendering labels are not normalized into universal membership meaning. Same state, same stage, same source type, same wording, expected stage, or immediate blocker status does not establish membership.

### Source-lineage boundary

Membership may be established only through preserved evidence such as:

- bounded inquiry identity;
- source explanation identity;
- source artifact identity;
- exact demand identity;
- exact work or probe identity;
- handoff lineage;
- derivation references;
- provenance references;
- preserved Unknowns and conflicts.

If the rendering projection alone does not contain enough evidence, the lawful input is an explicit evidence handoff or source-lineage evidence bundle for this one candidate. The projection must not perform hidden lookup, semantic guessing, or stage-owned meaning normalization.

## Producer and output artifact

### Producer

The smallest producer is a read-only per-candidate projection producer:

```text
SharedExplanationMembershipEvidenceProjection
```

It consumes one explicit bounded inquiry reference, one candidate rendering projection reference, and the candidate's preserved source-lineage evidence.

### Output artifact

The output is exactly one per-candidate membership evidence result:

```text
SharedExplanationMembershipEvidenceResult
```

The result preserves enough evidence to explain its state:

```text
bounded_inquiry_reference
candidate_rendering_projection_identity
source_explanation_references
source_artifact_references
membership_state
membership_reason
positive_membership_evidence
positive_non_membership_evidence
missing_evidence
conflicting_references
duplicate_source_visibility
unknowns
conflicts
read_only_guarantees
```

These names are descriptive for this slice, not a mandate to rename existing repository-owned implementation fields. Repository-supported shapes should win if implementation later chooses different names.

## Evidence-input treatment

The producer treats evidence as preserved identity and lineage, not as semantic content.

Lawful positive membership evidence includes:

- the candidate lineage carries the same bounded inquiry identity;
- the candidate lineage carries a handoff descending from the bounded inquiry;
- the candidate lineage carries an exact demand, work, or probe identity connected to the bounded inquiry;
- the candidate's source explanation or source artifact is known through preserved lineage to be a stage-local result for the bounded inquiry;
- derivation or provenance references connect the candidate source to the bounded inquiry.

Lawful positive non-membership evidence includes:

- preserved lineage to another incompatible bounded inquiry;
- preserved lineage to another incompatible exact demand;
- preserved lineage to another incompatible work, probe, handoff, source explanation, or source artifact.

Missing evidence includes absent or insufficient:

- inquiry reference;
- demand reference;
- work or probe reference;
- handoff reference;
- source artifact reference;
- derivation reference;
- provenance reference.

Conflicting evidence includes preserved incompatible references inside the same candidate evidence boundary, such as:

- two incompatible inquiry references;
- incompatible demand references;
- incompatible handoff references;
- incompatible source artifact references;
- incompatible derivation or provenance references.

The producer must not infer non-membership from missing membership evidence.

## Membership state meanings

### `belongs`

`belongs` means the candidate has positive preserved identity or lineage evidence connecting it to the explicit bounded inquiry, and no preserved incompatible reference prevents that conclusion.

```text
positive connection to this inquiry
→ belongs
```

### `does_not_belong`

`does_not_belong` means the candidate has positive preserved identity or lineage evidence tying it to another incompatible inquiry, demand, work, handoff, source explanation, source artifact, derivation, or provenance boundary.

```text
positive connection to another incompatible inquiry or demand
→ does_not_belong
```

This state cannot be established from absence, display wording, same state, same stage, same source type, or expected-stage mismatch.

### `unknown`

`unknown` means preserved evidence is insufficient to establish either positive membership or positive non-membership.

```text
insufficient evidence for either conclusion
→ unknown
```

Missing evidence remains Unknown and is not silently converted into non-membership.

### `conflict`

`conflict` means preserved evidence contains incompatible inquiry, demand, handoff, source-lineage, derivation, or provenance references and the producer cannot lawfully choose among them.

```text
preserved incompatible inquiry, demand, handoff,
or source-lineage references
→ conflict
```

Conflict is preserved without source preference, timestamp preference, ordering, stage preference, severity, or display-position choice.

## Proving-case results

### Same Inquiry, Different Stage

Case:

```text
bounded inquiry: inquiry:A
candidate: ingress or grammar-applicability rendering projection
lineage: source explanation or stage-owned material preserves inquiry:A,
         a handoff from inquiry:A,
         or an exact demand/work/probe identity connected to inquiry:A
```

Result:

```json
{
  "membership_state": "belongs",
  "membership_reason": "preserved source-lineage evidence connects the candidate to the same bounded inquiry",
  "positive_membership_evidence": ["same bounded inquiry or lawful handoff/demand lineage"],
  "positive_non_membership_evidence": [],
  "missing_evidence": [],
  "conflicting_references": []
}
```

An ingress rendering projection and a grammar-applicability rendering projection can both belong when their source lineage lawfully connects to the same bounded inquiry. Different stage does not prevent membership. Immediate blocker status does not make a candidate the only relevant explanation.

### Same State, Different Inquiry

Case:

```text
bounded inquiry: inquiry:A
candidate: rendering projection with the same source_state, wording, source type, or stage as a known inquiry:A candidate
lineage: preserved positive connection to inquiry:B, incompatible with inquiry:A
```

Result:

```json
{
  "membership_state": "does_not_belong",
  "membership_reason": "preserved source-lineage evidence positively connects the candidate to another incompatible bounded inquiry",
  "positive_membership_evidence": [],
  "positive_non_membership_evidence": ["incompatible bounded inquiry lineage"],
  "missing_evidence": [],
  "conflicting_references": []
}
```

Same state does not establish same inquiry. Same stage does not establish same inquiry. Positive incompatible inquiry lineage establishes non-membership.

### Missing Lineage Evidence

Case:

```text
bounded inquiry: inquiry:A
candidate: rendering projection with source labels but no sufficient inquiry, demand, handoff, artifact, derivation, or provenance evidence
```

Result:

```json
{
  "membership_state": "unknown",
  "membership_reason": "lineage evidence is insufficient to establish membership or non-membership",
  "positive_membership_evidence": [],
  "positive_non_membership_evidence": [],
  "missing_evidence": ["bounded inquiry lineage", "exact demand or handoff lineage", "source artifact/provenance evidence"],
  "conflicting_references": []
}
```

Missing inquiry, demand, handoff, artifact, or provenance evidence remains `unknown`. Missing evidence is not non-membership.

### Conflicting Lineage

Case:

```text
bounded inquiry: inquiry:A
candidate: rendering projection whose preserved source lineage references inquiry:A and incompatible inquiry:B,
           or incompatible demands/handoffs/source artifacts
```

Result:

```json
{
  "membership_state": "conflict",
  "membership_reason": "preserved lineage contains incompatible references and the projection cannot lawfully choose among them",
  "positive_membership_evidence": ["bounded inquiry lineage to inquiry:A, if present"],
  "positive_non_membership_evidence": ["incompatible inquiry or demand lineage, if present"],
  "missing_evidence": [],
  "conflicting_references": ["inquiry:A", "inquiry:B"]
}
```

Incompatible preserved inquiry, demand, handoff, or source-lineage references remain `conflict`. The projection does not choose through ordering or source preference.

### Duplicate Source Identity

Case:

```text
bounded inquiry: inquiry:A
candidate: one rendering projection whose source explanation identity or source artifact identity duplicates another candidate
lineage: evaluated only for this one candidate
```

Result:

```json
{
  "membership_state": "belongs | does_not_belong | unknown | conflict",
  "membership_reason": "duplicate identity is visible but does not authorize deduplication",
  "duplicate_source_visibility": {
    "duplicate_source_explanation_identity": true,
    "duplicate_source_artifact_identity": true,
    "deduplicated": false
  }
}
```

Duplicate source-explanation or source-artifact identity remains visible. Duplicate identity is not authority to deduplicate.

### Unrelated Projection

Case:

```text
bounded inquiry: inquiry:A
candidate: rendering projection whose wording appears relevant
lineage: positive preserved connection to incompatible inquiry:B
```

Result:

```json
{
  "membership_state": "does_not_belong",
  "membership_reason": "positive preserved lineage ties the candidate to another incompatible inquiry despite apparent wording relevance",
  "positive_membership_evidence": [],
  "positive_non_membership_evidence": ["incompatible inquiry lineage"],
  "missing_evidence": [],
  "conflicting_references": []
}
```

Unrelated projection wording does not override preserved incompatible lineage.

## Duplicate treatment

The projection preserves duplicate visibility only as evidence:

```text
duplicate source explanation identity
→ visible duplicate source identity
→ no deduplication authority
```

```text
duplicate source artifact identity
→ visible duplicate source artifact identity
→ no deduplication authority
```

Duplicate candidates may each receive their own per-candidate membership result. This slice does not collapse, select, suppress, order, or merge duplicate results.

## Unknown and conflict preservation

Unknown preservation:

- missing bounded inquiry evidence remains Unknown;
- missing exact demand or work evidence remains Unknown;
- missing handoff evidence remains Unknown;
- missing source artifact evidence remains Unknown;
- missing derivation or provenance evidence remains Unknown;
- missing expected stage does not invent a projection;
- expected stage does not equal existing candidate.

Conflict preservation:

- incompatible inquiry references remain conflict;
- incompatible demand references remain conflict;
- incompatible handoff references remain conflict;
- incompatible source explanation or artifact references remain conflict;
- incompatible derivation or provenance references remain conflict;
- conflict is not resolved by order, preference, severity, source type, or stage.

## Human rendering

Bounded human rendering for one candidate:

```text
Shared explanation membership evidence result

Bounded inquiry: inquiry:A
Candidate rendering projection: rendering:123
Source explanation references: explanation:ingress:456
Source artifact references: binding:789

Membership state: belongs
Membership reason: preserved handoff lineage connects binding:789 to inquiry:A.

Supporting membership evidence:
- handoff handoff:A->ingress:456 descends from inquiry:A
- source explanation explanation:ingress:456 preserves source artifact binding:789

Supporting non-membership evidence:
- none

Missing evidence:
- none required for this result

Conflicting references:
- none

Duplicate source visibility:
- duplicate source explanation identity observed: false
- duplicate source artifact identity observed: false
- deduplicated: false

Unknowns preserved:
- none introduced by membership projection

Conflicts preserved:
- none introduced by membership projection

Read-only boundary:
- read_only: true
- writes_event_ledger: false
- mutates_cluster: false
- no sequencing, composition, ranking, semantic relevance inference, deduplication, handoff creation, authorization, execution, or event write occurred
```

## JSON rendering

Bounded JSON rendering with the same core meaning:

```json
{
  "bounded_inquiry_reference": "inquiry:A",
  "candidate_rendering_projection_identity": "rendering:123",
  "source_explanation_references": ["explanation:ingress:456"],
  "source_artifact_references": ["binding:789"],
  "membership_state": "belongs",
  "membership_reason": "preserved handoff lineage connects binding:789 to inquiry:A",
  "positive_membership_evidence": [
    {
      "evidence_type": "handoff_lineage",
      "reference": "handoff:A->ingress:456",
      "connects": ["inquiry:A", "explanation:ingress:456", "binding:789"]
    }
  ],
  "positive_non_membership_evidence": [],
  "missing_evidence": [],
  "conflicting_references": [],
  "duplicate_source_visibility": {
    "duplicate_source_explanation_identity_observed": false,
    "duplicate_source_artifact_identity_observed": false,
    "deduplicated": false
  },
  "unknowns": [],
  "conflicts": [],
  "read_only_guarantees": {
    "read_only": true,
    "writes_event_ledger": false,
    "mutates_cluster": false,
    "sequenced_explanations": false,
    "composed_view": false,
    "ranked_blockers": false,
    "compared_stage_states": false,
    "inferred_semantic_relevance": false,
    "deduplicated": false,
    "invented_missing_projection": false,
    "created_handoff": false,
    "authorized_or_executed": false
  }
}
```

The human and JSON renderings preserve candidate identity, bounded inquiry identity, membership state and reason, supporting evidence, missing evidence, conflicting evidence, duplicate visibility, Unknowns, conflicts, and read-only boundaries. They do not normalize stage-owned source meaning.

## Read-only guarantees

This projection is read-only:

```text
read_only = true
writes_event_ledger = false
mutates_cluster = false
```

It does not:

- sequence explanations;
- compose a view;
- rank blockers;
- compare stage states;
- infer semantic relevance;
- deduplicate;
- invent missing projections;
- create handoffs;
- authorize movement;
- execute movement;
- write events;
- mutate cluster state;
- modify existing source explanation producers;
- modify constitutional meanings;
- change CLI or REPL routing.

## Compatibility answer

Did this slice change any existing compatibility boundary?

No.

This slice preserves the existing boundary recovered by the prior audit: `SharedExplanationRenderingProjection` remains a one-source rendering projection, and membership evidence is a separate per-candidate read-only projection responsibility. Membership evidence is not membership selection, sequencing, or composition.

## Files changed

```text
shared_explanation_membership_evidence_projection_slice_001.md
```

No source explanation producer, CLI route, REPL route, diagnostic surface, event ledger writer, or cluster mutation path was changed.

## Tests executed

```text
python -m pytest -q tests/test_shared_explanation_rendering_projection.py
```

This documentation-only slice did not add a new operational diagnostic, audit, probe, view, CLI flag, or recordable output. Therefore the diagnostic inventory and diagnostic shape-audit surfaces were not changed.

## Remaining boundaries

This slice does not implement or investigate:

- membership selection;
- selected-set production;
- explanation sequencing;
- view composition;
- blocker ranking;
- severity selection;
- conversation planning;
- universal view registry;
- explanation relevance manager;
- global composition manager;
- source explanation producer changes;
- constitutional meaning changes;
- CLI routing changes;
- REPL routing changes;
- hidden semantic matching;
- deduplication policy;
- missing-stage invention.

Expected stage remains distinct from existing candidate. Immediate blocker remains distinct from only relevant explanation.

## Exact next bounded question

Given one bounded inquiry
and several independently produced
per-candidate membership evidence results,

what smallest membership-selection responsibility
may preserve every belonging, non-belonging,
Unknown, conflict, and duplicate result

while producing the set of rendering projections
eligible for later sequencing

without ranking blockers,
deduplicating by meaning,
or composing the view?
