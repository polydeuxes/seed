# Consumer Dependency Audit Slice 001

## Selected boundary
Observation-predicate audit item production inside `build_consumer_audit(...)`.

## Implementation evidence
`build_consumer_audit(...)` already treated observation predicates as a distinct item family by loading observation inventory only when no diagnostic filter is selected, then producing `ConsumerAuditItem(kind="observation_predicate")` rows from `inventory.predicates` before the final audit sort.

## Before
Observation-predicate item-family production was compressed directly into `build_consumer_audit(...)` next to diagnostic item-family production.

## After
Observation-predicate row production is owned by `_observation_predicate_audit_items(...)`, while `build_consumer_audit(...)` still owns orchestration, source loading, filter gating, final sorting, and metadata.

## Recovered producer
`_observation_predicate_audit_items(...)`.

## Recovered artifact/helper
A tuple of `ConsumerAuditItem` rows with `kind="observation_predicate"`.

## Recovered consumer
`build_consumer_audit(...)` consumes the tuple and extends the audit item list before final sorting.

## Compatibility preserved
No.

## Required questions
1. The compressed responsibility was production of observation-predicate audit rows from observation inventory predicates.
2. The implementation-local ownership boundary now directly observable is the observation-predicate item-family producer.
3. `_observation_predicate_audit_items(...)` now owns the recovered responsibility.
4. The helper `_observation_predicate_audit_items(...)` carries the recovered boundary.
5. `build_consumer_audit(...)` consumes it.
6. Did any compatibility boundary change? No.
7. This stays inside the consumer dependency audit district because it only changes local consumer-audit item-family production.
8. This is distinct from Frontier Pressure Admission Slice 037 because it does not use consumer audit output to admit pressure candidates or fan out pressure candidates.
9. This is distinct from orphaned/fragile pressure item selection, score, refusal, and evidence slices because it does not touch pressure audit item selection, scoring, refusal, or evidence payloads.
10. This avoids per-item source-consumer matching because `_audit_item(...)` still owns lookup terms and consumer matching.
11. This is the first slice in this batch, so there is no earlier batch slice to distinguish from.

## Files changed
- `seed_runtime/consumer_dependency_audit.py`
- `tests/test_consumer_dependency_audit.py`

## LOC changed
- Implementation: 14 added helper lines and local orchestration replacement.
- Tests: 70 focused test lines added.

## Tests executed
- `pytest -q tests/test_consumer_dependency_audit.py::test_observation_predicate_item_producer_preserves_boundary_behavior`

## Remaining compressed responsibilities
Diagnostic audit item-family production remains adjacent and implementation-backed. Per-item source-consumer matching also remains compressed in `_audit_item(...)`, but it is explicitly out of scope for this batch.

## District boundary compliance
The change is local to consumer dependency audit implementation and tests. It does not change CLI flags, JSON schema, diagnostic inventory, diagnostic shape audit, event-ledger behavior, read-only behavior, or pressure-audit code.

## Distinction from prior Frontier Pressure Admission slices
This slice only recovers observation-predicate row production before the consumer audit exists. It does not create, select, score, admit, refuse, or explain pressure candidates.

## Distinction from earlier slices in this batch
Not applicable for slice 001.
