# Shared Explanation Encounter Sequencing Topology Audit 001

## Bounded question

For already-admitted shared explanation projections in `SharedExplanationPresentationAdmission`, what owns operator encounter order while preserving constitutional derivation order?

This audit does not implement sequencing, composition, ranking, a view, a CLI, a diagnostic, or a recordable output. It inspects current repository evidence and preserves:

```text
constitutional derivation order
!= operator encounter order
```

```text
first displayed
!= first derived
```

```text
sequencing
!= constitutional ranking
```

```text
sequencing
!= composition
```

## Evidence reviewed

Primary repository evidence reviewed:

- `seed_runtime/shared_explanation_presentation_admission.py` and `tests/test_shared_explanation_presentation_admission.py` for the now-implemented admission boundary.
- `seed_runtime/shared_explanation_membership_evidence_projection.py` and `seed_runtime/shared_explanation_membership_evidence_set.py` for membership, Unknown, conflict, duplicate, and non-selection boundaries.
- `seed_runtime/shared_explanation_rendering_projection.py` for the single-explanation rendering boundary and stage-owned material preservation.
- `shared_explanation_presentation_contract_audit_001.md` for the shared rendering contract and stage-owned semantic fields.
- `shared_explanation_membership_to_presentation_admission_topology_audit_001.md` for the membership-to-admission topology and admission preconditions.
- `explanation_selection_sequencing_composition_topology_audit_001.md` for the prior four-responsibility topology separating membership, lineage preservation, encounter sequencing, and composition.
- `seed_runtime/reasoning_path_audit.py`, `seed_runtime/selection_path_audit.py`, and `seed_runtime/operational_story.py` for existing answer/reason/support/lineage/Unknown/composition precedents.

## Current implementation anchor

`SharedExplanationPresentationAdmission` now consumes one `SharedExplanationMembershipEvidenceSet`, one explicit requested-presentation boundary, and explicit admission evidence. It emits `admitted_to_sequencing_results` and `admitted_to_sequencing_projection_refs`, while preserving belonging-but-unadmitted projections, non-members, Unknowns, conflicts, duplicate identity occurrences, admission evidence references, and read-only/non-event/non-mutation flags.

The admission artifact expressly says admission to sequencing is not first encounter order, ranking, deduplication, view composition, membership reinterpretation, authorization, execution, event writing, or mutation. Tests preserve this by asserting that `admitted_to_sequencing` does not create `first_in_encounter_order`, `composed_view`, or `sequence_rank`.

Therefore the current repository has this topology:

```text
SharedExplanationRenderingProjection
  -> SharedExplanationMembershipEvidenceProjection
  -> SharedExplanationMembershipEvidenceSet
  -> SharedExplanationPresentationAdmission
  -> missing operator encounter sequencing owner
  -> later bounded composition owner, if implemented
```

Admission is now implemented. Encounter sequencing remains absent.

## What evidence may lawfully establish encounter order?

Lawful encounter-order evidence may only come from explicit presentation-local or repository-implemented ordering evidence over already-admitted projections. Based on current evidence, lawful sources include:

1. The requested presentation boundary and any explicit presentation-local sequencing policy supplied with it.
2. The operator's bounded question shape, such as whether the inquiry can advance now, when that question is already answered by admitted projections.
3. Stage-owned explanation role evidence already preserved in the projection: attempted movement, source state, source reason, prohibited downstream movement, explanation boundary, preserved Unknowns, preserved conflicts, and opaque `stage_owned_material`.
4. Explicit admission evidence references, if they state roles or display requirements for the requested presentation.
5. Source-stage lineage, handoff, provenance, and dependency references, but only to preserve derivation order or to label prerequisites; not to make display-first equal derivation-first.
6. Existing bounded answer-composition precedent that can display answer before support when the answer is already established.
7. Existing surface-specific ordering rules, but only for that specific implemented surface and only when tested.

Unsupported encounter-order evidence remains:

- tuple position in `admitted_to_sequencing_results` by itself;
- artifact ID or lexical order;
- creation timestamp;
- registry order;
- first returned result;
- implementation call order;
- severity normalization;
- global blocker ranking;
- source-stage constitutional order treated as display order;
- display prominence in another view;
- semantic inference from shared labels such as `blocked`, `unknown`, `permitted`, or `applicable`.

The tuple order currently visible in admission is preservation of admitted results from the membership set under explicit admission references, not a lawful operator encounter sequence. If a future sequencer consumes that tuple, it must still say why each encounter position is lawful for the requested presentation.

## How derivation order remains visible after reordering

Derivation order remains visible by carrying source-owned lineage alongside the encounter sequence. A lawful presentation sequence may lead with the answer or immediate reason, but it must preserve source references that show constitutional derivation order.

A future sequencing artifact would need to expose both dimensions, for example:

```text
constitutional_derivation_order:
1. ingress authority/scope binding -> permitted
2. representation grammar applicability -> applicable
3. reachability -> blocked

operator_encounter_order:
1. answer -> cannot currently advance
2. immediate_reason -> required realization unreachable
3. support -> ingress was permitted and grammar was applicable
4. limitations -> Unknowns/conflicts/non-authorization boundary
5. next_lawful_movement -> source-owned reconsideration or missing-boundary movement
```

The first list is not presentation ranking. The second list is not constitutional derivation. The lawful reordering condition is that every encounter item retains source explanation identity, source artifact owner, source explanation type, and stage-owned material or references sufficient to reconstruct the derivation path.

## Are answer, immediate reason, support, limitations, and next lawful movement already supported?

Partially, but not as a shared explanation sequencing artifact.

Existing repository support:

- `OperationalStory` separates answer material, reasoning payload, supporting evidence, boundary, and limitations. It is a bounded operational story view, not a shared explanation sequencer.
- `ReasoningPathAudit` separates evidence, intermediate conclusions, derived conclusions, consumers, story impact, Unknowns, and read-only boundary. It preserves derivation visibility, not encounter sequencing.
- `SelectionPathAudit` separates selected result, outcome/reason, supporting evidence, candidates, non-selected entries, factors, lineage, Unknowns, and read-only boundary. It proves selection explanation shape, not shared explanation encounter order.
- `SharedExplanationRenderingProjection` preserves source state, source reason, Unknowns, conflicts, prohibited downstream movement, explanation boundary, and stage-owned material for one explanation.
- `SharedExplanationPresentationAdmission` can identify projections admitted to later sequencing but intentionally does not assign roles or order.

Therefore roles such as answer, immediate reason, support, limitations, and next lawful movement are repository-supported as recurring presentation/answer concerns, but they are not yet assigned for admitted shared explanation projections. A future encounter sequencer would need explicit role-assignment evidence and must not derive roles solely from field labels or severity.

## Unknowns, conflicts, duplicates, and admitted supporting stages

Unknowns, conflicts, duplicates, and supporting stages must remain visible after sequencing.

Current evidence already preserves them before sequencing:

- Membership projection preserves membership `unknown`, `conflict`, missing lineage refs, incompatible refs, conflicting refs, and duplicate source identity refs.
- Membership set preserves all supplied results, partitions by state, duplicate occurrence records, collection partiality, and no completeness claim.
- Presentation admission preserves `unknown_results`, `conflict_results`, `duplicate_identity_occurrences`, `non_member_results`, and `belonging_but_unadmitted_results` while admitting only already-belonging projections.
- Rendering projection preserves per-explanation Unknowns and conflicts from the source stage.

A future sequencing owner may place Unknowns and conflicts near the relevant stage, in a limitations section, or before next lawful movement, but may not hide, resolve, downgrade, or convert them into non-membership. Duplicate handling may label exact duplicate occurrences if current identity evidence supports it, but deduplication is not sequencing unless an explicit separate duplicate policy preserves the collapsed occurrences. Admitted supporting stages may appear after the immediate answer for comprehension, but must remain visible as support rather than being discarded because they are not encounter-first.

## Is sequencing separate or already owned?

Sequencing is separate.

Current owners and limits:

| Owner | Owns | Does not own |
| --- | --- | --- |
| `SharedExplanationRenderingProjection` | one stage-owned explanation in a display-compatible projection | comparison, aggregation, ordering, composition |
| `SharedExplanationMembershipEvidenceProjection` | per-candidate membership evidence from explicit lineage | selection, ranking, sequencing, composition, deduplication |
| `SharedExplanationMembershipEvidenceSet` | supplied collection preservation, partitions, duplicate occurrence visibility | selecting, ranking, sequencing, composing, deduplicating |
| `SharedExplanationPresentationAdmission` | presentation-local admission of already-belonging projections into later sequencing eligibility | first encounter order, sequence rank, composition, deduplication |
| `ReasoningPathAudit` | derivation path visibility for operational conclusions | shared explanation presentation encounter order |
| `SelectionPathAudit` | selected target explanation and candidate visibility for operational conclusions | universal encounter sequencing for shared explanations |
| `OperationalStory` | one bounded operational story composition | ordering admitted shared explanation projections |

No existing owner can lawfully claim operator encounter order for already-admitted shared explanation projections. The admission boundary creates a handoff to sequencing; it does not fill the sequencing responsibility.

## Sequencing is not constitutional ranking

A sequencer would answer:

```text
what should the operator encounter first, second, third for this requested presentation?
```

It would not answer:

```text
which constitutional stage is more important?
which blocker outranks another blocker?
which source state has greater severity?
which projection is more true?
```

Constitutional ranking is not implemented here. Encounter order may lead with the current stopping point because that is the clearest answer for the operator, not because the stopping point outranks prior derivation stages constitutionally.

## Sequencing is not composition

Sequencing chooses or records encounter positions and role placement for already-admitted projections. Composition would later preserve those sequenced projections in one bounded view.

A composition owner may concatenate, nest, render, or package the sequence, but it must not invent encounter order if sequencing did not provide it. Conversely, a sequencing owner should not create the final view; it should emit enough ordered, source-referenced role placements for composition to preserve.

## Whether one implementation slice is warranted

One implementation slice is warranted only if Seed now needs to move admitted shared explanation projections into an operator-facing encounter order.

The warranted slice would be narrow and read-only, for example `SharedExplanationEncounterSequencing`, and would:

- consume exactly one `SharedExplanationPresentationAdmission`;
- consume explicit encounter-order evidence or policy for one requested presentation;
- sequence only `admitted_to_sequencing_projection_refs`;
- preserve `constitutional_derivation_order` separately from `operator_encounter_order`;
- preserve source explanation identity, source owner, source type, source state/reason, Unknowns, conflicts, duplicate visibility, admission evidence refs, and stage-owned material references;
- optionally assign presentation roles such as `answer`, `immediate_reason`, `support`, `limitations`, and `next_lawful_movement` only when explicit evidence supports the assignment;
- preserve non-members, Unknowns, conflicts, duplicates, and belonging-but-unadmitted projections as visibility sections without sequencing them as admitted encounters;
- not perform membership reinterpretation, admission, constitutional ranking, blocker severity normalization, deduplication by meaning, composition, authorization, execution, event-ledger writes, or cluster mutation.

No broader implementation is warranted. In particular, do not implement a composition view, conversation planner, severity ranker, universal explanation role classifier, or constitutional ranking system from this audit.

## Exact next bounded question

```text
Given one `SharedExplanationPresentationAdmission` and explicit requested-presentation sequencing evidence, what minimum read-only `SharedExplanationEncounterSequencing` artifact can assign operator encounter positions and optional roles to admitted projection refs while separately preserving constitutional derivation order, Unknown/conflict/duplicate visibility, belonging-but-unadmitted visibility, and non-mutation boundaries, without composing a final view or ranking constitutional stages?
```

## Preserved Unknowns

- No implemented encounter-sequencing owner exists for admitted shared explanation projections.
- No implemented role-assignment policy exists for `answer`, `immediate_reason`, `support`, `limitations`, or `next_lawful_movement` over admitted shared explanation projections.
- No implemented multi-explanation composition owner exists after sequencing.
- The exact source of presentation-local sequencing policy is not implemented.
- Whether future presentation requests will need budgets, grouping, audience modes, or conflict-placement rules remains unknown.
- Whether duplicate admitted projections should be preserved in sequence, grouped, or collapsed with occurrence visibility requires a future duplicate policy.

## Conclusion

Operator encounter order for already-admitted explanation projections is not owned by `SharedExplanationPresentationAdmission` and is not owned by rendering, membership, reasoning path, selection path, or operational story surfaces. Repository evidence supports a separate, read-only encounter-sequencing responsibility that consumes admission output and explicit sequencing evidence, preserves constitutional derivation order separately, and hands an ordered role-placement structure to any later composition owner.

Shared explanation encounter sequencing topology audit complete.
