# Unavailable Evidence Territory Frontier Recovery 001

## Question

Does unavailable evidence territory still satisfy frontier identity, or does it only establish a blocking condition?

## Observed implementation behavior

The bounded inquiry frontier assembler treats `evidence_availability == "unavailable"` as coherent unless it is paired with a non-established standing, non-inquiry family disposition, or a conflicting value. The operative-clause predicate refuses clauses when `clause_standing != "established"`, `family_disposition != "inquiry"`, `evidence_currency == "conflicting"`, or `evidence_availability == "conflicting"`; it does not refuse `evidence_availability == "unavailable"`.

For the eligible/ineligible evidence-territory family, the implementation therefore permits this bounded case to satisfy the required clause family when the clause is otherwise established and inquiry-disposed:

```text
clause_family == "eligible_ineligible_evidence_territory"
clause_standing == "established"
family_disposition == "inquiry"
evidence_currency != "conflicting"
evidence_availability == "unavailable"
→ operative clause
```

Because frontier establishment is computed from coverage of all required clause families by operative clauses, an otherwise complete testimony set can be `frontier_state == "established"` even when the evidence-territory clause carries unavailable availability.

The assembler separately preserves `unavailable_clause_refs`. That means unavailability remains visible as a boundary quality and is not erased by establishment. However, in the current implementation, unavailability alone is not a material conflict, not a missing required family, and not a refusal reason.

## Book and adjacent warrant

The Book says frontier identity is conjunctive and must preserve available evidence territory, Unknowns, conflicts, and negative authority. It also says stale or unavailable evidence, by itself, does not establish the frontier, admit inquiry, select sources or observations, open examination, authorize access, determine the answer, write the event ledger, or mutate state.

Adjacent recovery artifacts distinguish available evidence territory from selected sources and observation plans. They also state that horizon stale and unavailable evidence refs may be part of lawfully available territory as constraints, while unavailable evidence does not authorize access and may establish that inquiry cannot be sufficiently resolved under current authority.

The implementation slice is more specific to the current assembler: unsupported, unknown, conflicting, mixed, adjacent-family, stale, unavailable, and out-of-scope clauses remain preserved and non-operative unless they independently satisfy the coherent operative rule. This supports the implementation rule that unavailable is not automatically non-operative; it is non-operative only when another coherent-operative requirement fails.

## Whether unavailable territory supplies frontier identity, blocking standing, both, or neither

Observed repository behavior supports **both, with different meanings**:

1. **Frontier identity / establishment:** unavailable eligible evidence territory can satisfy the evidence-territory clause family when the clause is otherwise established, inquiry-disposed, and non-conflicting. In this narrow implementation sense, unavailable territory can still be identified as lawful frontier territory and can contribute to required frontier establishment.
2. **Blocking standing:** unavailable evidence is preserved as `unavailable_clause_refs`, and adjacent warrant says unavailable evidence may establish that inquiry cannot be sufficiently resolved under current authority. That is a blocking or stopping-boundary quality, not evidence admission or access authorization.

The repository does **not** support treating unavailable as nonexistent. It also does **not** support treating eligible territory as presently accessible evidence, territory identification as evidence admission, blocking as frontier establishment, or frontier establishment as inquiry executable.

## Focused test evidence

Existing focused tests prove these boundaries indirectly:

- `tests/test_bounded_inquiry_frontier.py::test_unsupported_unknown_mixed_adjacent_stale_unavailable_and_out_of_scope_are_preserved_non_operative` constructs an otherwise established frontier and adds an established `eligible_ineligible_evidence_territory` clause with `evidence_availability="unavailable"`. The test expects the frontier to remain established and expects `unavailable_clause_refs == ("clause:unavailable",)`. It does not expect that clause to appear in `non_operative_clause_refs`.
- `tests/test_inquiry_frontier_boundary_testimony.py::test_all_clause_families_coexist_unordered_and_dispositions_remain_separate` proves a boundary testimony clause can simultaneously be an established eligible/ineligible evidence-territory clause and carry `evidence_availability == "unavailable"`.
- `tests/test_inquiry_frontier_boundary_testimony.py::test_stale_unavailable_out_of_scope_adjacent_and_mixed_do_not_replace_standing` proves unavailable availability does not overwrite clause standing; the unavailable example remains `clause_standing == "unknown"` because that standing was supplied independently.
- `tests/test_inquiry_frontier_boundary_testimony.py::test_visible_evidence_is_not_automatically_eligible_and_eligible_territory_selects_nothing` preserves the distinction between already-visible evidence and eligible evidence territory, and proves eligible territory does not select sources or observations.
- `tests/test_bounded_inquiry_frontier.py::test_no_scope_invention_question_opening_source_selection_authorization_execution_recording_ledger_or_mutation` proves an established frontier is still read-only and does not execute inquiry, authorize access, record, write the ledger, mutate cluster state, or know the result.

Focused command run:

```text
pytest -q tests/test_bounded_inquiry_frontier.py tests/test_inquiry_frontier_boundary_testimony.py
```

Result: all focused tests passed.

## Remaining Unknowns

- No focused test isolates the exact minimal case where the only eligible/ineligible evidence-territory clause is established and unavailable while the other three required families are coherent. The implementation plainly permits it, but the current focused test demonstrates that behavior as an additional clause beside an already available required evidence-territory clause.
- The Book's phrase "available evidence territory" can be read strictly, while adjacent artifacts allow unavailable evidence refs as constraints inside lawfully available territory. The implementation resolves this locally by admitting unavailable established inquiry clauses as operative unless conflicting, but the Book does not explicitly state that an unavailable evidence-territory clause alone satisfies the required evidence-territory family.
- No reviewed artifact shows whether another downstream owner should convert established-but-unavailable frontier territory into non-executable inquiry status. The current frontier assembler preserves unavailability but does not expose a separate `blocking_standing` field.

## Final fidelity judgment

The current implementation supports:

```text
unavailable territory
→ still identified as lawful frontier territory
```

and also supports:

```text
unavailable territory
→ blocking/stopping-boundary condition preserved separately
```

It does **not** support:

```text
unavailable territory
→ cannot satisfy required frontier establishment
```

as the current assembler rule.

Best characterization: **availability matters differently by clause family and by responsibility boundary**. For bounded inquiry frontier assembly, unavailable availability does not defeat an otherwise established eligible/ineligible evidence-territory clause. For inquiry execution, source selection, observation authorization, evidence admission, and sufficient resolution, unavailable remains a preserved blocker or stopping constraint rather than admitted evidence or executable access.

Fidelity status: **implementation is locally warranted by adjacent recovery artifacts and not plainly crossed by the Book, but the exact minimal unavailable-only required evidence-territory case remains under-tested and only locally conventional until a focused test or Book clause makes it explicit.**
