# Bounded constitutional question duplicate producer deletion 001

## Result

The unused named producer `produce_bounded_constitutional_question(...)` was
deleted. Repository-wide reference inspection confirmed zero non-test calls.
The producer's exclusive `_tuple_of_strings(...)`, `_field_items(...)`, and
`_stable_question_id(...)` helpers were deleted with it, and the now-exclusive
`hashlib`, `json`, and `Iterable` imports were removed. No replacement producer,
adapter, alias, classmethod, validation path, or stable-ID implementation was
introduced.

## Complete current reference inventory

Before deletion, the complete executable inventory was:

- production calls: zero;
- production definition: one, in
  `seed_runtime/bounded_constitutional_question.py`;
- test fixture calls: two fixture definitions, in
  `tests/test_bounded_constitutional_question.py` and
  `tests/test_examination_frontier.py`;
- active exports/imports outside those tests: zero; and
- textual documentation occurrences: historical implementation, recovery,
  topology, audit, survey, and deletion reports only.

After deletion, remaining textual occurrences are historical reports and this
deletion report. There is no stale active reference, production import or call,
test import or fixture call, public export, operator instruction, or API
instruction. No active documentation correction or public-export removal was
required. Historical reports, including the six named preservation holdouts,
remain unchanged.

## Topology before deletion

```text
test/API construction:
    produce_bounded_constitutional_question(...)
    → BoundedConstitutionalQuestion

operator-reachable construction:
    examination_frontier.input_from_json_dict(...)
    → BoundedConstitutionalQuestion(**qd)
    → ExaminationFrontier
```

## Topology after deletion

```text
test fixtures:
    explicit BoundedConstitutionalQuestion construction

operator-reachable construction:
    examination_frontier.input_from_json_dict(...)
    → BoundedConstitutionalQuestion(**qd)
    → ExaminationFrontier

named producer helper:
    deleted
```

> Deleting the unused named producer does not establish the surviving raw JSON constructor as a lawful question-origination boundary. It removes one unconsumed duplicate construction surface so that the remaining operator-reachable boundary can be recovered independently.

> Direct dataclass construction in tests demonstrates artifact constructibility and consumer compatibility only. It does not prove responsible production, inquiry admission, or constitutional-question standing.

## Preserved behavior and tests

The bounded-question tests now directly construct an artifact with an explicit,
stable test identifier. Producer-specific coverage for hash-derived identity,
ID override, normalization, sorting/stringification, and producer input
non-mutation was deleted. Focused artifact coverage remains for frozen and tuple
immutability, negative-authority defaults, read-only/no-ledger/no-mutation
defaults, JSON-ready serialization, and human formatting. The examination
frontier fixture likewise directly constructs the artifact with an explicit
test identifier while retaining its existing values and assertions.

The `BoundedConstitutionalQuestion` schema, field order, field types, defaults,
testimony status, boundaries, and operational flags are unchanged. Its JSON
serializer and human formatter are unchanged. The frontier module is unchanged
byte-for-byte; therefore `input_from_json_dict(...)`, raw
`BoundedConstitutionalQuestion(**qd)` JSON construction, projection,
classification, exceptions, and JSON/human CLI rendering remain unchanged.

Validation results:

- focused suite: 125 passed;
- full suite: 1874 passed;
- `tests/test_public_exports.py`: not present, so no path was invented;
- artifact import: succeeded;
- deleted-producer import: failed with `ImportError`, as required;
- examination-frontier human and JSON CLI smoke coverage: passed in the focused
  frontier test; and
- compile and diff checks: passed.

No Book file, historical report, diagnostic inventory, diagnostic shape audit,
or frontier implementation was changed.
