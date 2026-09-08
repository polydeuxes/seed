# Pressure Audit Slice 001

## Selected boundary

Recovered the implementation-local handoff between category-local pressure reduction and public `PressureItem` construction:

```text
category-local pressure reduction
!=
PressureItem construction
```

The slice introduces `_PressureItemCandidate` as the private owner of the repeated pre-item row fields before conversion to the public `PressureItem` shape.

## Implementation evidence

`seed_runtime/pressure_audit.py` previously had each category builder directly constructing `PressureItem` with the same set of fields: `category`, `score`, `evidence`, `reason`, and `recommended_command`.

The implementation now has:

- `PressureItem` as the unchanged public output row.
- `_PressureItemCandidate` as the private pre-item handoff row.
- `_PressureItemCandidate.to_pressure_item()` as the compatibility conversion point.
- Category builders still perform their local source query/filter/reduction, then return a `_PressureItemCandidate`.
- `build_pressure_audit(...)` converts candidates to public `PressureItem` instances before sorting and returning `PressureAudit`.

## Before

Each pressure category builder performed category-specific reduction and public item construction in the same function:

```text
source query/filter/reduction
score calculation
evidence assembly
category/reason/recommended command assignment
PressureItem construction
```

That repeated the pre-`PressureItem` assembly pattern across category builders.

## After

Each pressure category builder still owns only its category-local reduction and field values, but returns a `_PressureItemCandidate` instead of constructing the public `PressureItem` directly.

`build_pressure_audit(...)` performs the single public handoff by calling `candidate.to_pressure_item()` before preserving the existing score/category sort.

## Compatibility preservation

Preserved unchanged:

- `PressureItem` fields.
- `PressureAudit` JSON shape.
- `pressure_audit_json(...)` behavior.
- `format_pressure_audit(...)` output.
- Category names.
- Scores.
- Evidence keys and values.
- Reason text.
- Recommended commands.
- Empty-state behavior.
- Read-only behavior.

No diagnostic inventory, CLI, schema, formatter, event-ledger, cluster mutation, or broader Pressure Visibility behavior changed.

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `pressure_audit_slice_001.md`

## LOC changed

Before adding this report, implementation and test diff was:

```text
seed_runtime/pressure_audit.py | 44 +++++++++++++++++++++++++-----------
tests/test_pressure_audit.py   | 51 +++++++++++++++++++++++++++++++++++++++++-
2 files changed, 81 insertions(+), 14 deletions(-)
```

## Tests executed

```bash
pytest -q tests/test_pressure_audit.py
```

Result:

```text
5 passed in 0.67s
```

No pressure-audit-specific diagnostic inventory or diagnostic shape-audit test references were found in `tests/test_diagnostic_inventory.py` or `tests/test_diagnostic_shape_audit.py`.

## Remaining pressure-audit compression

The remaining compression is intentionally local and unsliced here:

- Consumer audit is called separately by orphaned and fragile predicate pressure builders.
- Category-specific scoring remains in each builder.
- Category-specific evidence assembly remains in each builder.
- No registry, generic pressure evidence, classification framework, scoring framework, or Pressure Visibility architecture was introduced.

## Questions

### 1. What responsibility was previously compressed inside each category builder?

Each category builder compressed category-local source reduction together with construction of the public `PressureItem` fields: category, score, evidence, reason, and recommended command.

### 2. Which implementation-local boundary became explicit?

The boundary between category-local pressure reduction and public `PressureItem` construction became explicit through `_PressureItemCandidate.to_pressure_item()`.

### 3. How does the implementation now better reflect Pressure Audit ownership?

Pressure Audit now has a private implementation-local row candidate that owns the repeated pre-public-item handoff, while each category builder continues to own only its local source query/filter/reduction and category-specific field values.

### 4. Did any compatibility boundary change?

No.
