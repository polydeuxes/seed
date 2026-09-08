# Consumer Dependency Audit Slice 002

## Selected boundary
Diagnostic audit item production inside `build_consumer_audit(...)`.

## Implementation evidence
After slice 001, `build_consumer_audit(...)` still had an adjacent compressed diagnostic item-family loop: it collected diagnostic inventory names, applied `diagnostic_filter`, and produced `ConsumerAuditItem(kind="diagnostic")` rows before the existing final audit sort.

## Before
Diagnostic item-family production was compressed into `build_consumer_audit(...)` next to orchestration, filter gating, final sorting, and metadata construction.

## After
Diagnostic row production is owned by `_diagnostic_audit_items(...)`, while `build_consumer_audit(...)` still owns source loading, observation-vs-diagnostic top-level filter gating, final sorting, and metadata.

## Recovered producer
`_diagnostic_audit_items(...)`.

## Recovered artifact/helper
A tuple of `ConsumerAuditItem` rows with `kind="diagnostic"`.

## Recovered consumer
`build_consumer_audit(...)` consumes the tuple and extends the audit item list before final sorting.

## Compatibility preserved
No.

## Required questions
1. The compressed responsibility was production of diagnostic audit rows from diagnostic inventory names.
2. The implementation-local ownership boundary now directly observable is the diagnostic item-family producer.
3. `_diagnostic_audit_items(...)` now owns the recovered responsibility.
4. The helper `_diagnostic_audit_items(...)` carries the recovered boundary.
5. `build_consumer_audit(...)` consumes it.
6. Did any compatibility boundary change? No.
7. This stays inside the consumer dependency audit district because it only changes local consumer-audit diagnostic item-family production.
8. This is distinct from Frontier Pressure Admission Slice 037 because it does not use consumer audit output to admit or fan out pressure candidates.
9. This is distinct from orphaned/fragile pressure item selection, score, refusal, and evidence slices because it does not touch pressure audit item selection, scoring, refusal, or evidence payloads.
10. This avoids per-item source-consumer matching because `_audit_item(...)` still owns lookup terms and consumer matching.
11. This is distinct from slice 001 because slice 001 recovered observation-predicate row production, while this slice recovers diagnostic row production.

## Files changed
- `seed_runtime/consumer_dependency_audit.py`
- `tests/test_consumer_dependency_audit.py`

## LOC changed
- Implementation: diagnostic helper added and diagnostic loop replaced with helper consumption.
- Tests: focused diagnostic item-family producer test added.

## Tests executed
- `pytest -q tests/test_consumer_dependency_audit.py::test_diagnostic_item_producer_preserves_boundary_behavior`
- `pytest -q tests/test_consumer_dependency_audit.py::test_observation_predicate_item_producer_preserves_boundary_behavior tests/test_consumer_dependency_audit.py::test_diagnostic_item_producer_preserves_boundary_behavior`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities
Per-item source-consumer matching and lookup-term construction remain directly evident in `_audit_item(...)` and `_consumer_lookup_terms(...)`, but both are explicitly out of scope for this batch. No further safe candidate was taken.

## District boundary compliance
The change is local to consumer dependency audit implementation and tests. It does not change CLI flags, JSON schema, diagnostic inventory, diagnostic shape audit, event-ledger behavior, read-only behavior, or pressure-audit code.

## Distinction from prior Frontier Pressure Admission slices
This slice only recovers diagnostic row production before the consumer audit exists. It does not create, select, score, admit, refuse, or explain pressure candidates.

## Distinction from earlier slices in this batch
Slice 001 recovered observation-predicate item-family production. Slice 002 recovers the separate diagnostic item-family production boundary and does not re-slice observation-predicate production.
