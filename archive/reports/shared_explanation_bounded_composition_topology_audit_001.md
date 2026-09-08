# Shared Explanation Bounded Composition Topology Audit 001

## Question

Determine whether an existing composition owner already lawfully consumes one completed `SharedExplanationEncounterSequencing`, or whether Seed needs one new bounded shared-explanation composition responsibility.

## Repository evidence inspected

Implementation evidence shows a completed shared-explanation intake chain before composition:

```text
SharedExplanationRenderingProjection
→ SharedExplanationMembershipEvidenceProjection
→ SharedExplanationMembershipEvidenceSet
→ SharedExplanationPresentationAdmission
→ SharedExplanationEncounterSequencing
```

The completed sequencing owner consumes one `SharedExplanationPresentationAdmission` plus explicit presentation-local sequencing evidence. It preserves constitutional derivation order separately from operator encounter order and states that it is not composition, constitutional ranking, deduplication, membership, admission, authorization, execution, event writing, or cluster mutation.

Existing composition infrastructure found during this audit is the registered constitutional view composition surface. That surface consumes explicitly requested registered constitutional read-model views and composes them into one bounded explanation while preserving Unknowns and refusals. Its authority is tied to registered constitutional read models, not completed shared-explanation encounter sequencing.

The shared-explanation rendering projection explicitly rejects collections and preserves a single-explanation boundary. That is upstream projection, not downstream composition over one sequencing artifact.

## Determination

No existing composition owner found in the repository lawfully owns the boundary "consume one completed `SharedExplanationEncounterSequencing` and preserve it as one operator-facing shared-explanation view."

Seed therefore needs one new bounded shared-explanation composition responsibility if the product needs a final operator-facing shared-explanation view after encounter sequencing.

This is not because composition should repair sequencing. It is because sequencing intentionally stops before view composition. Existing constitutional view composition is a different bounded family, and existing shared-explanation rendering projection is single-source rendering projection rather than collection composition.

## Existing composition infrastructure ownership

### Constitutional view composition

`ConstitutionalViewCompositionArtifact` is lawful for registered constitutional read-model views only. It may correlate existing evidence, preserve contributing Unknowns and refusals, and render a compatibility answer inside its registered-view boundary.

It does not lawfully consume `SharedExplanationEncounterSequencing` because:

- its request shape is `requested_views`, `composition_purpose`, and `output_format`;
- its accepted inputs are names from the constitutional read-model contract registry;
- its contributing artifacts are constitutional process/governance/fidelity views;
- its summary and boundaries are explicitly about registered constitutional read models;
- it is not a shared-explanation presentation consumer.

### Shared-explanation rendering projection

`SharedExplanationRenderingProjection` is lawful for one ingress explanation at a time. Its tests preserve a single-explanation boundary and reject collections. It may not select, aggregate, order, compare, or compose multiple explanations.

It does not lawfully consume `SharedExplanationEncounterSequencing` because sequencing is a collection-bearing presentation artifact downstream of admission, while rendering projection is one-source upstream projection.

### Shared-explanation encounter sequencing

`SharedExplanationEncounterSequencing` is lawful for ordering admitted projections for operator encounter. It already preserves both:

```text
operator encounter order
!= constitutional derivation order
```

It does not lawfully produce a composed view. Its implementation and tests explicitly preserve:

```text
sequencing
!= composition
```

## What bounded shared-explanation composition may lawfully preserve

A new bounded shared-explanation composition responsibility may preserve exactly one completed `SharedExplanationEncounterSequencing` as one operator-facing view artifact.

It may preserve:

- the source `presentation_ref`, `bounded_inquiry_ref`, and `bounded_demand_ref`;
- the source sequencing convention and producer identity;
- the ordered `encounter_sequence_projection_refs` as operator encounter order;
- the separate `constitutional_derivation_projection_refs` as constitutional derivation order;
- the already-sequenced result payloads without reinterpretation;
- optional roles already supplied by sequencing evidence, without inventing roles;
- sequencing evidence references by projection ref;
- `unsequenced_admitted_projection_refs` as still admitted but not placed in operator encounter order;
- belonging-but-unadmitted, non-member, Unknown, conflict, and duplicate-identity surfaces as preserved visibility obligations;
- read-only operational boundaries: `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`.

It may not:

- reorder projections;
- assign new roles;
- reopen membership or admission;
- resolve Unknowns or conflicts;
- deduplicate;
- rank constitutional stages;
- re-derive source meaning;
- authorize, execute, write events, or mutate state.

Its composition authority is therefore view preservation, not meaning authority.

## Representation of unsequenced admitted projections

Unsequenced admitted projections remain represented as admitted-to-the-presentation but not placed in the operator encounter sequence.

A bounded composition view may show them in a separate section such as:

```text
Admitted but unsequenced
```

That section must not imply lower importance, later constitutional derivation, exclusion from membership, or conflict resolution. It represents missing or absent presentation-local sequencing evidence only.

The view should preserve the source projection refs and, where useful, the corresponding result payloads. It should not move those projections into encounter order unless a later sequencing responsibility emits a new completed sequencing artifact.

## Representation of unresolved visibility obligations

Unresolved visibility obligations remain visible as obligations, not as composition decisions.

The composed view may preserve separate sections for:

- belonging but unadmitted results;
- non-member results;
- Unknown results;
- conflict results;
- duplicate identity occurrences;
- sequencing evidence present or absent by projection ref.

These sections must carry the boundary:

```text
visibility obligation
!= composition authority to resolve it
```

Composition may display that unresolved material exists. It may not convert it into admission, exclusion, resolution, deduplication, ranking, or constitutional meaning.

## View artifact decision

Composition should produce a new view artifact, not adapt an existing one.

Recommended artifact family name:

```text
SharedExplanationBoundedComposition
```

Recommended producer boundary:

```text
compose_shared_explanation_bounded_view(sequencing: SharedExplanationEncounterSequencing) -> SharedExplanationBoundedComposition
```

Rationale:

- adapting constitutional view composition would cross from registered constitutional read models into shared-explanation presentation artifacts;
- adapting rendering projection would violate its single-explanation, non-composition boundary;
- adapting sequencing would collapse the preserved distinction between sequencing and composition;
- a new artifact can preserve one sequenced presentation as one operator-facing view without expanding upstream authorities.

The artifact should be read-only and should not support recording unless a later, explicit diagnostic/recording boundary is introduced with inventory and shape-audit coverage.

## Whether one implementation slice is warranted

Yes, one implementation slice is warranted if Seed needs the operator-facing view after sequencing.

The slice should be narrow:

1. Add a `SharedExplanationBoundedComposition` immutable artifact.
2. Add a pure composition function that consumes exactly one `SharedExplanationEncounterSequencing`.
3. Preserve sequenced, unsequenced, unresolved, duplicate, and boundary material without changing it.
4. Add JSON and human renderers if an operator-facing view is required.
5. Add tests proving:
   - composition consumes exactly one completed sequencing artifact;
   - encounter order is preserved and not recomputed;
   - constitutional derivation order remains separately preserved;
   - unsequenced admitted projections remain separate;
   - Unknowns, conflicts, duplicate identities, and visibility obligations remain unresolved;
   - no new roles are assigned;
   - read-only/event-ledger/cluster-mutation boundaries remain false.

No implementation should occur in this audit.

If a CLI diagnostic or recordable operational surface is later added for the composition view, the diagnostic inventory registry, shape-audit specs, and diagnostic tests must be updated in that same implementation slice.

## Exact next bounded question

Can Seed add `SharedExplanationBoundedComposition` as a read-only artifact that consumes exactly one `SharedExplanationEncounterSequencing` and renders one operator-facing shared-explanation view while preserving sequenced order, constitutional derivation order, unsequenced admitted projections, and unresolved visibility obligations without resolving or mutating them?

Shared explanation bounded composition topology audit complete.
