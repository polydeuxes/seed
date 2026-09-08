# Structure Probe Architectural Relation Observation

## Forms added

The documentation structure probe now observes the following explicit relation-line forms as raw structure only:

- `A != B`
- `A owns B`
- `A produces B`
- `A consumes B`
- `A hands off to B`
- `A preserves B`
- `A bounds B`
- `A derives B`
- `A selects B`
- `A explains B`
- `A observes B`
- `A does not own B`

Each observation captures the left term, relation text, right term, source path, line number, and evidence line.

## Implementation evidence

- Added `DocumentationArchitecturalRelationRecord` to the existing documentation structure observer model.
- Added bounded explicit-line matching in the structure observer, excluding Markdown headings, list items, block quotes, table rows, and fenced-code content.
- Added optional detail expansion output with `--architectural-relations` under the existing `--documentation-structure` surface.
- Added JSON and human rendering for architectural relation observations only when the detail expansion is requested.
- Updated diagnostic inventory and diagnostic shape-audit declarations so the extended probe surface remains visible.

## Files changed

- `seed_runtime/documentation_structure.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_documentation_structure.py`
- `tests/test_diagnostic_inventory.py`
- `structure_probe_architectural_relation_observation.md`

## LOC changed

Current diff before commit:

```text
scripts/seed_local.py                    +8  -1
seed_runtime/diagnostic_inventory.py     +2  -1
seed_runtime/diagnostic_shape_audit.py   +4  -0
seed_runtime/documentation_structure.py +99  -1
tests/test_diagnostic_inventory.py       +1  -0
tests/test_documentation_structure.py  +105  -0
```

Tracked implementation/test LOC delta excluding this report: `+219/-3`.

## Tests executed

- `pytest -q tests/test_documentation_structure.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`
- `pytest -q tests/test_documentation_structure.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Compatibility preserved

- The existing `--documentation-structure` command remains read-only.
- Existing JSON output remains bounded by detail expansions; relation observations are only emitted in document JSON when `--architectural-relations` is requested.
- Existing diagnostic inventory semantics remain `supports_record=false`, `record_scope=none`, `writes_event_ledger=false`, and `mutates_cluster=false`.
- No event ledger writes were added.
- No runtime cluster mutation was added.

## Explicit non-goals

- No grammar interpretation.
- No responsibility recovery.
- No lexicon stabilization.
- No architectural inference.
- No claim extraction or promotion.
- No priority, importance, next-work, or truth conclusions.

## Remaining gaps

- The observation grammar is intentionally bounded to explicit standalone lines with capitalized left and right terms.
- The probe does not interpret relation meaning beyond copying the explicit relation token/string.
- The probe does not connect observations to any responsibility family, grammar category, lexicon entry, or projected knowledge object.
