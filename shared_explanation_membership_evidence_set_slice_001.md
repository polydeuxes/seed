# Shared Explanation Membership Evidence Set Slice 001

## Recovered responsibility

This slice recovers exactly one bounded **Shared Explanation Membership Evidence Set**. Its only responsibility is to consume one explicit `BoundedInquiryReference` plus a caller-supplied tuple of already-produced `SharedExplanationMembershipEvidenceProjection` records and preserve that supplied collection as a read-only set artifact.

The set exists to enforce collection identity and preservation invariants. It does not reopen, reinterpret, normalize, compare, or promote per-candidate membership conclusions.

## Producer and set artifact

Implementation source adds `SharedExplanationMembershipEvidenceSet` and `build_shared_explanation_membership_evidence_set` in `seed_runtime/shared_explanation_membership_evidence_set.py`.

The producer is `SharedExplanationMembershipEvidenceSet`. The artifact preserves:

- bounded inquiry reference;
- bounded demand reference;
- supplied result count;
- empty/partial collection truth;
- every supplied `SharedExplanationMembershipEvidenceProjection` record in `belonging_results`;
- mechanical state partitions;
- duplicate identity occurrence visibility;
- read-only/no-event/no-mutation guarantees.

`belonging_results` remains a supplied membership-evidence collection and is not `selected_rendering_projections`.

## Same-inquiry validation

Construction accepts only results whose `bounded_inquiry_ref` and `bounded_demand_ref` exactly match the explicit bounded inquiry reference supplied to the builder.

Mixed inquiry input is refused with `ValueError`. Mixed demand input is refused with `ValueError`.

## Lossless preservation

The builder converts the supplied results to an immutable tuple and stores the exact records in order in `belonging_results`. It does not deduplicate, collapse, select, or rewrite the result records.

Focused tests prove that every supplied result is present exactly once in the set artifact.

## Duplicate visibility

The set exposes occurrence records for candidate projection identity, source explanation identity, and duplicate source identity references already exposed by per-candidate evidence records.

Duplicate candidate identities remain visible as multiple occurrence rows. Duplicate source identity references remain visible as multiple occurrence rows. No duplicate is removed.

## State partition treatment

The set computes mechanical partitions only across the existing membership states:

- `belongs`;
- `does_not_belong`;
- `unknown`;
- `conflict`.

Partitions contain candidate projection references from already-supplied results. The set does not re-evaluate state, infer relevance, normalize stage-owned meanings, or fabricate missing stage results.

## Empty and partial input treatment

An empty supplied tuple is lawful. Empty input produces:

- `collection_empty=True`;
- `supplied_result_count=0`;
- empty `belonging_results`;
- empty state partitions, including empty `unknown`;
- no fabricated candidate Unknowns.

The set defaults to `collection_partial=True` and preserves `completeness_claim="none; supplied collection only"`. This is an explicit refusal to claim that the supplied collection is complete.

## Human and JSON rendering

Human rendering is provided by `format_shared_explanation_membership_evidence_set`.

JSON rendering is provided by `shared_explanation_membership_evidence_set_json`.

Both renderings expose the same bounded meaning:

- bounded inquiry and demand;
- all supplied result identities;
- state partitions;
- duplicate identity occurrences;
- empty/partial collection status;
- no completeness claim;
- read-only, no-event-ledger, and no-cluster-mutation guarantees;
- non-selection boundary.

## Read-only guarantees

The artifact is read-only. It writes no event ledger and mutates no cluster state. It performs no handoff creation, authorization, or execution.

The non-selection boundary explicitly stops before membership selection, eligibility, selected-set production, ranking, sequencing, composition, deduplication, semantic relevance inference, missing-stage invention, handoff creation, authorization, and execution.

## Compatibility answer

Did this slice change any existing compatibility boundary?

No.

This slice adds a read-only preservation set after per-candidate membership evidence projection and before any future membership selection. It does not change existing projection, rendering, compatibility, handoff, authorization, execution, event-ledger, or cluster-mutation boundaries.

## Files changed

- `seed_runtime/shared_explanation_membership_evidence_set.py`
- `tests/test_shared_explanation_membership_evidence_set.py`
- `shared_explanation_membership_evidence_set_slice_001.md`

## Tests executed

- `pytest -q tests/test_shared_explanation_membership_evidence_set.py tests/test_shared_explanation_membership_evidence_projection.py tests/test_shared_explanation_rendering_projection.py`

## Remaining boundaries

This slice intentionally leaves unresolved and unimplemented:

- membership selection;
- eligibility;
- selected-set production;
- ranking;
- sequencing;
- composition;
- deduplication;
- semantic relevance inference;
- missing-stage invention;
- handoff creation;
- authorization;
- execution.

## Exact next bounded question

Given one lawful `SharedExplanationMembershipEvidenceSet`, what is the smallest future read-only membership selection artifact, if any, that may choose candidates for downstream use without changing the set's preservation guarantees, deduplicating supplied evidence, inventing missing candidates, authorizing execution, or mutating cluster truth?
