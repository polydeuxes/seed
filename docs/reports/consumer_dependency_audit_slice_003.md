# Consumer Dependency Audit Slice 003

## Selected boundary

Recovered exactly one implementation-local ownership boundary: matched consumer group construction for a single consumer dependency audit item.

## Implementation evidence

`_audit_item(...)` already resolved lookup terms with `_consumer_lookup_terms(...)`, iterated the provided source groups, delegated low-level mention checks to `_mentions_any_item(...)`, accumulated matching consumer group names, and constructed `ConsumerAuditItem`. The still-inline responsibility was the middle group-level matching step: consume source groups plus resolved lookup terms and produce ordered consumer group names that mention the item.

## Before

`_audit_item(...)` owned all of these steps together:

1. resolve lookup terms;
2. iterate source groups in source mapping order;
3. check each group's file contents with `_mentions_any_item(...)`;
4. accumulate matching group names;
5. construct `ConsumerAuditItem`.

## After

`_audit_item(...)` still owns lookup-term resolution and `ConsumerAuditItem` construction. `_matched_consumer_groups(...)` now owns only source group iteration plus matched consumer group name production.

## Recovered producer

`_matched_consumer_groups(...)` produces the ordered tuple of consumer group names matching the already-resolved lookup terms.

## Recovered artifact/helper

`_matched_consumer_groups(sources, lookup_terms) -> tuple[str, ...]` carries the recovered boundary.

## Recovered consumer

`_audit_item(...)` consumes the tuple unchanged when constructing `ConsumerAuditItem`.

## Compatibility preserved

No compatibility boundary changed.

Preserved behavior includes source group ordering, exact matched consumer group names, orphan behavior, lookup-term behavior, low-level mention behavior, `ConsumerAuditItem` construction, JSON shape, human-readable output, CLI behavior, diagnostic visibility, event-ledger non-mutation, and read-only behavior.

## Files changed

- `seed_runtime/consumer_dependency_audit.py`
- `tests/test_consumer_dependency_audit.py`
- `consumer_dependency_audit_slice_003.md`

## LOC changed

Implementation change is limited to extracting the existing group-matching loop from `_audit_item(...)` into `_matched_consumer_groups(...)`. Test and report LOC document and preserve the recovered behavior.

## Tests executed

- `pytest -q tests/test_consumer_dependency_audit.py::test_matched_consumer_groups_preserves_order_exact_matches_and_orphans tests/test_consumer_dependency_audit.py::test_audit_item_delegates_lookup_terms_and_low_level_mention_matching`
- `pytest -q tests/test_consumer_dependency_audit.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

Directly evident remaining responsibilities inside `_audit_item(...)` are lookup-term resolution and final `ConsumerAuditItem` construction. They were intentionally not recovered in this slice.

## Required questions

1. What responsibility was previously compressed?
   - Source group iteration and matched consumer group name production for one audit item were compressed inside `_audit_item(...)`.

2. Which implementation-local ownership boundary became directly observable?
   - The boundary between resolved lookup terms plus source groups and the ordered matched consumer group names became directly observable.

3. What producer now owns the recovered responsibility?
   - `_matched_consumer_groups(...)`.

4. What artifact or helper carries the recovered boundary, if any?
   - `_matched_consumer_groups(sources, lookup_terms) -> tuple[str, ...]`.

5. Who consumes it?
   - `_audit_item(...)` consumes the returned tuple unchanged while constructing `ConsumerAuditItem`.

6. Did any compatibility boundary change?
   - No.

7. How does this stay inside the consumer dependency audit district?
   - The change is confined to `seed_runtime/consumer_dependency_audit.py` and focused tests for consumer dependency audit behavior.

8. How is this distinct from Consumer Dependency Audit Slice 001?
   - Slice 001 recovered observation-predicate audit item-family production. This slice does not produce item families and only matches consumer groups for one already-selected item.

9. How is this distinct from Consumer Dependency Audit Slice 002?
   - Slice 002 recovered diagnostic audit item-family production. This slice does not filter or produce diagnostic item families and only matches consumer groups for one already-selected item.

10. How is this distinct from `_consumer_lookup_terms(...)` ownership?
    - `_consumer_lookup_terms(...)` still owns lookup-term construction. `_matched_consumer_groups(...)` accepts lookup terms that are already resolved and does not alter their semantics.

11. How is this distinct from `_mentions_any_item(...)` ownership?
    - `_mentions_any_item(...)` still owns low-level string-form expansion and mention detection. `_matched_consumer_groups(...)` only decides which source groups match by delegating each group to `_mentions_any_item(...)`.

12. How is this distinct from Frontier Pressure Admission Slice 037?
    - Frontier Pressure Admission Slice 037 concerned pressure-audit use of consumer audits and fan-out into pressure candidates. This slice stays inside consumer dependency audit per-item matching and does not touch pressure-audit code.

## District boundary compliance

This slice does not implement Frontier Pressure Admission, lawful acceptance, action, mutation, planning, prioritization, readiness evaluation, inquiry generation, route authority, autonomous next-step selection, a framework, an engine, a registry, a methodology owner, a scheduler, an ontology, or an architectural redesign.
