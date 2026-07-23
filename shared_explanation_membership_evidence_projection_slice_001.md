# Shared Explanation Membership Evidence Projection Slice 001

## Implementation status

Implemented.

This slice is no longer a documentation-only account. The repository now contains a focused read-only implementation and tests for one per-candidate shared-explanation membership evidence projection.

## Recovered producer

Recovered producer:

```text
SharedExplanationMembershipEvidenceProjection
```

Implementation owner:

```text
seed_runtime/shared_explanation_membership_evidence_projection.py
```

The producer is intentionally local and bounded. It consumes exactly:

1. one `BoundedInquiryReference`;
2. one `SharedExplanationRenderingProjection` candidate;
3. one explicit `PreservedLineageEvidence` record.

It performs no hidden lookup, no source-explanation meaning changes, no CLI routing change, and no REPL routing change.

## Recovered artifact or payload

Recovered payload:

```text
SharedExplanationMembershipEvidenceProjection
```

The artifact preserves:

- bounded inquiry and demand references;
- candidate shared-rendering/source-explanation identity;
- candidate source artifact owner;
- membership state;
- membership reason;
- supporting references;
- incompatible references;
- missing lineage references;
- conflicting references;
- duplicate source identity visibility;
- evidence-input boundary;
- non-selection boundary;
- read-only, event-ledger, and cluster-mutation guarantees.

Supported membership states are exactly the repository-local equivalent of:

```text
belongs
does_not_belong
unknown
conflict
```

## Explicit evidence-input boundary

The evidence-input boundary is explicit in code:

```text
Consumes one bounded inquiry reference, one SharedExplanationRenderingProjection,
and explicit preserved lineage evidence; performs no lookup and no semantic guessing.
```

The projection uses only the caller-supplied `PreservedLineageEvidence` fields:

- `positive_inquiry_refs`;
- `positive_demand_refs`;
- `incompatible_inquiry_refs`;
- `incompatible_demand_refs`;
- `missing_lineage_refs`;
- `supporting_references`;
- `incompatible_references`;
- `source_identity_refs`.

State discipline implemented:

```text
positive lineage to this inquiry
→ belongs
```

```text
positive lineage to another incompatible inquiry or demand
→ does_not_belong
```

```text
insufficient lineage evidence
→ unknown
```

```text
positive target lineage plus incompatible preserved lineage
→ conflict
```

Missing evidence is preserved as `unknown`; it is not converted to non-membership.

## Consumer/rendering boundary

Human rendering is implemented by:

```text
format_shared_explanation_membership_evidence(...)
```

JSON rendering is implemented by:

```text
shared_explanation_membership_evidence_json(...)
```

Both render the same membership meaning through the same artifact fields, including `membership_state`, references, duplicate source identity visibility, and read-only guarantees.

The rendering boundary remains per-candidate. It does not select candidates, produce a selected set, sequence results, rank blockers, compose a view, infer semantic relevance, deduplicate, invent missing stages, create handoffs, authorize, or execute.

## Proving cases

Focused tests were added in:

```text
tests/test_shared_explanation_membership_evidence_projection.py
```

They prove:

1. A grammar-applicability shared rendering projection with matching inquiry lineage `belongs`.
2. Positive lineage to another incompatible inquiry `does_not_belong`.
3. Missing lineage evidence remains `unknown`.
4. Matching target lineage plus incompatible demand lineage remains `conflict`.
5. Duplicate source identity remains visible and is not deduplicated.
6. Shared state, wording, or stage does not establish membership.
7. Human and JSON rendering preserve the same membership meaning.
8. The projection writes no events, mutates no cluster state, and does not select.

## Read-only guarantees

The artifact reports:

```text
read_only = true
writes_event_ledger = false
mutates_cluster = false
```

The focused tests assert these guarantees. The implementation constructs only an in-memory frozen dataclass result and contains no event-ledger write, cluster mutation, authorization, execution, handoff creation, selected-set production, or routing path.

## Files changed

```text
seed_runtime/shared_explanation_membership_evidence_projection.py
tests/test_shared_explanation_membership_evidence_projection.py
shared_explanation_membership_evidence_projection_slice_001.md
```

No source explanation meaning, CLI routing, REPL routing, diagnostic inventory, diagnostic shape-audit surface, event ledger writer, or cluster mutation path was changed.

## Tests executed

Focused and adjacent tests executed:

```text
```

Result:

```text
28 passed
```

## Compatibility answer

Did this slice change any existing compatibility boundary?

No.

The existing `SharedExplanationRenderingProjection` remains a one-source rendering projection. This slice adds a separate read-only per-candidate membership evidence projection that consumes the rendering projection and explicit lineage evidence. It does not change source explanation producers, source explanation meanings, rendering projection compatibility, CLI routing, or REPL routing.

## Remaining boundaries

This slice stops before:

- membership selection;
- selected-set production;
- sequencing;
- composition;
- blocker ranking;
- semantic relevance inference;
- deduplication;
- missing-stage invention;
- handoff creation;
- authorization;
- execution.

Duplicate source identity is visible but never used to collapse candidates.

## Exact next bounded question

Given several already-produced per-candidate `SharedExplanationMembershipEvidenceProjection` results for one bounded inquiry, what smallest read-only boundary, if any, may expose those results together without selecting, ranking, sequencing, composing, deduplicating, inventing missing stages, creating handoffs, authorizing, or executing?
