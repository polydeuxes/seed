# Frontier required-family claim-relative warrant slice 001

## Selected family

The selected required frontier-clause family is `eligible_ineligible_evidence_territory`.

Repository evidence selected this family because the Book expectation is already reflected in implementation vocabulary: boundary testimony distinguishes visible evidence from eligible evidence territory, and the testimony artifact carries `eligible_evidence_territory_refs` separately from `already_visible_evidence_refs`, `source_lineage`, ownership fields, and positive clause coordinates. This gives one concrete family-relevant support dimension without requiring a universal warrant system.

This slice does not select the family because it is convenient. It selects it because existing repository construction already exposes a support/basis field for the exact assertion this family contributes.

## Exact family assertion

For this bounded frontier consumer, an `eligible_ineligible_evidence_territory` clause contributes only this family-local assertion:

> The selected inquiry frontier has at least one eligible evidence territory available as a boundary condition for the exact selected inquiry need.

It does not assert source selection, observation selection, admission, authority, inquiry opening, execution, recording, event-ledger writing, mutation, or result knowledge.

## Concrete claim-relative warrant recovered

The recovered concrete warrant is the preserved `eligible_evidence_territory_refs` relation on the clause testimony.

For this family only, positive operative contribution requires a non-empty `eligible_evidence_territory_refs` tuple in addition to the existing mechanical predicate coordinates:

- `clause_standing="established"`
- `family_disposition="inquiry"`
- no explicit currency or availability conflict
- the correct `clause_family` label

`already_visible_evidence_refs` remains transported material. It may show visible evidence but does not by itself establish eligible evidence territory. `source_lineage`, `producer_ref`, `producer_lineage`, `adapter_ref`, `adapter_lineage`, and `ownership_basis` remain attribution or preservation fields. They do not automatically supply family warrant.

## Producer and consumer responsibilities

The preservation owner remains `preserve_inquiry_frontier_boundary_testimony(...)`: it copies clause fields and lineage into `InquiryFrontierBoundaryClause`, classifies preservation-local ownership basis, and keeps the testimony read-only and non-mutating.

The frontier consumer remains `assemble_bounded_inquiry_frontier(...)`: it decides whether preserved clauses are operative for required-family coverage. The smallest lawful owner of refusing silent promotion is the frontier-local operative predicate, because the crossing occurred when the consumer counted a mechanically positive family label as operative coverage without validating the family-local territory support that was already preserved.

## Prior mechanical crossing

Previously, the consumer counted an `eligible_ineligible_evidence_territory` clause as operative when it had established standing, inquiry-local family disposition, no explicit currency or availability conflict, and the required family label. A clause with positive dispositions but no `eligible_evidence_territory_refs` could therefore satisfy the family and help establish the whole frontier.

What the consumer previously counted: positive coordinates plus family label.

What positive warrant was absent: the concrete eligible territory reference(s) needed for the selected inquiry need, frontier boundary, and reliance purpose.

## Corrected movement

After this slice, the frontier-local operative predicate treats an `eligible_ineligible_evidence_territory` clause as operative only when `eligible_evidence_territory_refs` is non-empty.

A mechanically positive clause that lacks that concrete warrant remains preserved exactly as testimony, but it is non-operative for this family. Required-family coverage remains incomplete, and the frontier state remains `missing_required_clause_family` rather than `established`.

## Preserved unsupported testimony

The correction does not discard unsupported testimony. The clause remains in:

- `preserved_clause_refs`
- `clauses`
- `non_operative_clause_refs`

It is not rewritten as unowned, unsupported, unknown, conflicting, stale, unavailable, out of scope, admitted, false, or mutated. The preservation road remains read-only.

## Resulting family and frontier standing

When the selected family carries `eligible_evidence_territory_refs`, it may contribute to operative required-family coverage for `eligible_ineligible_evidence_territory`.

When the selected family lacks `eligible_evidence_territory_refs`, that family remains missing even if the clause has established standing, inquiry-local disposition, current and available evidence coordinates, an included scope disposition, producer lineage, and the correct family label. The whole frontier cannot be established from that clause.

## Ownership asymmetry

Producer ownership is not a universal prerequisite for claim-relative warrant. This slice does not require recognized original producer ownership before a clause can be warranted.

Likewise, producer or adapter lineage is not sufficient family warrant. Ownership, attribution, source lineage, evidentiary support, family-specific basis, and consumer-local validation remain distinct. A producer-owned clause still needs the eligible territory support for this one family; an unowned limitation does not prove that no possible warrant exists.

## Tests

Focused tests cover:

1. Existing supported `eligible_ineligible_evidence_territory` testimony with `eligible_evidence_territory_refs` remains operative and can contribute to an established frontier.
2. The same mechanically positive family clause with `eligible_evidence_territory_refs` removed remains preserved but becomes non-operative.
3. Positive dispositions, absence of explicit conflict, visible evidence, copied lineage, producer lineage, and the correct family label do not repair the missing territory warrant.
4. Because the family is not positively supported, required-family coverage remains incomplete and the frontier does not become established.
5. The correction does not create inquiry opening, source selection, observation selection, authorization, execution, recording, ledger writing, or mutation.

## Compatibility

This slice preserves behavior outside the selected warrant boundary. It does not rename public artifacts or states, does not require every caller to construct a universal warrant artifact, and does not alter unrelated frontier families.

## Family-specific and cross-family Unknowns

Family-specific Unknown: this slice establishes only that `eligible_ineligible_evidence_territory` needs non-empty `eligible_evidence_territory_refs` to count as positive operative support in this consumer.

Cross-family Unknowns remain unresolved for:

- `included_excluded_inquiry_scope`
- `sufficient_resolution_conditions`
- `lawful_stopping_conditions`

This correction does not define their warrant because their concrete family-relative bases were not implemented in this slice. It also does not decide stale testimony, unavailable testimony, admission, source or observation selection, inquiry opening, authority, execution, recording, event-ledger writes, or mutation.
