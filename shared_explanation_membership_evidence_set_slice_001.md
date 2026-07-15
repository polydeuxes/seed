# Shared Explanation Membership Evidence Set Slice 001

## Corrected recovered responsibility

This correction preserves exactly one bounded **Shared Explanation Membership Evidence Set** responsibility. The set consumes one explicit `BoundedInquiryReference` plus a caller-supplied tuple of already-produced `SharedExplanationMembershipEvidenceProjection` records and preserves that supplied collection as a read-only set artifact.

The set remains a collection-preservation artifact. It does not reopen, reinterpret, normalize, compare, select, sequence, rank, deduplicate, or promote per-candidate membership conclusions.

## Producer versus artifact distinction

The actual construction boundary is the producer function `build_shared_explanation_membership_evidence_set(...)` in `seed_runtime/shared_explanation_membership_evidence_set.py`.

The produced artifact is `SharedExplanationMembershipEvidenceSet`.

The artifact preserves:

- bounded inquiry reference;
- bounded demand reference;
- supplied result count;
- empty/partial collection truth;
- every supplied `SharedExplanationMembershipEvidenceProjection` record in `membership_results`;
- mechanical positive partition in `belongs_results`;
- independent mechanical non-positive partitions in `does_not_belong_results`, `unknown_results`, and `conflict_results`;
- legacy `belonging_results` compatibility alias documented as the complete supplied collection, not the positive partition;
- mechanical state identity partitions;
- duplicate identity occurrence visibility;
- read-only/no-event/no-mutation guarantees.

## Corrected general collection boundary

`membership_results` is the general supplied membership-evidence collection boundary.

It preserves every supplied `SharedExplanationMembershipEvidenceProjection` exactly once, in supplied order, including records whose state is:

- `belongs`;
- `does_not_belong`;
- `unknown`;
- `conflict`.

The general collection is not a selector and is not the positive membership partition.

## Mechanical partition boundaries

The mechanical positive partition is `belongs_results`.

The other independently visible mechanical partitions are:

- `does_not_belong_results`;
- `unknown_results`;
- `conflict_results`.

Each partition is computed only from already-supplied `membership_state` values. The set does not derive new membership states, select eligible projections, rank, sequence, deduplicate, reinterpret Unknowns, reinterpret conflicts, invent missing candidates, compose a view, create handoffs, authorize, execute, write events, or mutate cluster state.

The existing `state_partitions` identity map remains as a candidate-reference summary of the same mechanical state partitions.

## Same-inquiry validation

Construction accepts only results whose `bounded_inquiry_ref` and `bounded_demand_ref` exactly match the explicit bounded inquiry reference supplied to the builder.

Mixed inquiry input is refused with `ValueError`. Mixed demand input is refused with `ValueError`.

## Lossless preservation and duplicate visibility

The builder converts the supplied results to an immutable tuple and stores the exact records in order in `membership_results`. It does not deduplicate, collapse, select, or rewrite result records.

The set exposes occurrence records for candidate projection identity, source explanation identity, and duplicate source identity references already exposed by per-candidate evidence records.

Duplicate candidate identities remain visible as multiple occurrence rows. Duplicate source identity references remain visible as multiple occurrence rows. No duplicate is removed.

## Empty and partial input treatment

An empty supplied tuple is lawful. Empty input produces:

- `collection_empty=True`;
- `supplied_result_count=0`;
- empty `membership_results`;
- empty `belongs_results`;
- empty `does_not_belong_results`;
- empty `unknown_results`;
- empty `conflict_results`;
- empty state partitions, including empty `unknown`;
- no fabricated candidate Unknowns.

The set defaults to `collection_partial=True` and preserves `completeness_claim="none; supplied collection only"`. This is an explicit refusal to claim that the supplied collection is complete.

## Human and JSON equivalence

Human rendering is provided by `format_shared_explanation_membership_evidence_set`.

JSON rendering is provided by `shared_explanation_membership_evidence_set_json`.

Both renderings expose the same bounded meaning:

- bounded inquiry and demand;
- all supplied result identities;
- positive belongs identities;
- state partitions;
- duplicate identity occurrences;
- empty/partial collection status;
- no completeness claim;
- read-only, no-event-ledger, and no-cluster-mutation guarantees;
- non-selection boundary.

JSON also includes `belonging_results` only as a deprecated compatibility alias for `membership_results`, accompanied by an explicit compatibility note that it is not the `belongs_results` partition.

## Read-only guarantees

The artifact is read-only. It writes no event ledger and mutates no cluster state. It performs no handoff creation, authorization, or execution.

The non-selection boundary explicitly stops before membership selection, eligibility, selected-set production, ranking, sequencing, composition, deduplication, semantic relevance inference, missing-stage invention, handoff creation, authorization, and execution.

## Compatibility treatment

Did this correction change an existing compatibility boundary?

No existing behavior outside this newly introduced set boundary was changed. Within the set boundary, the misleading general collection name was corrected to `membership_results` and the mechanical positive partition was exposed as `belongs_results`.

Because `belonging_results` had already been exposed on the set artifact and JSON shape, it is retained only as a deprecated compatibility alias for the complete supplied collection. Its documented meaning is `membership_results`, not the positive `belongs_results` partition. This prevents silently maintaining two ambiguous meanings.

## Proving-case evidence

Focused tests prove a supplied four-result collection containing one result in each state:

- preserves all four results exactly once and in supplied order in `membership_results`;
- exposes only the `belongs` result in `belongs_results`;
- exposes only the `does_not_belong` result in `does_not_belong_results`;
- exposes only the `unknown` result in `unknown_results`;
- exposes only the `conflict` result in `conflict_results`;
- keeps `state_partitions` as a mechanical candidate-reference summary.

The same focused test file also preserves:

- duplicate occurrence visibility;
- same-inquiry and same-demand validation;
- empty collection behavior;
- partial/no-completeness claim;
- read-only/no-event/no-mutation guarantees;
- human/JSON equivalence.

## Files changed

- `seed_runtime/shared_explanation_membership_evidence_set.py`
- `tests/test_shared_explanation_membership_evidence_set.py`
- `shared_explanation_membership_evidence_set_slice_001.md`

## Tests executed

- `pytest -q tests/test_shared_explanation_membership_evidence_set.py tests/test_shared_explanation_membership_evidence_projection.py`

## Remaining boundaries

This correction intentionally leaves unresolved and unimplemented:

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

Given one lawful
SharedExplanationMembershipEvidenceSet,

what smallest membership-selection
responsibility may identify projections
eligible for later sequencing

while preserving non-members,
Unknowns, conflicts, and duplicates

without ranking blockers,
deduplicating evidence,
or composing the view?
