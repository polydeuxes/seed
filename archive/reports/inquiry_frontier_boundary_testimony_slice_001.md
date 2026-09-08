# Inquiry Frontier Boundary Testimony Slice 001

## Selected boundary

Recovered one read-only testimony artifact:

```text
selected inquiry need
+
explicit stage-owned frontier-boundary clauses
→ InquiryFrontierBoundaryTestimony
```

The artifact preserves unordered clauses for included/excluded inquiry scope, eligible/ineligible evidence territory, sufficient-resolution conditions, and lawful stopping conditions. It binds every preserved clause to the exact selected inquiry need, native inquiry item lineage, bounded uncertainty component, repository/world subject, selected goal, bounded advancement horizon, producer or adapter lineage, source lineage, evidence classes, provenance roles, and already-visible evidence references.

## Preserved separations

This slice preserves these dimensions independently rather than allowing one to replace another:

- clause standing: `established`, `unsupported`, `unknown`, `conflicting`, `unclassified`;
- scope disposition: `included`, `excluded`, `outside_current_scope`, `conflicting`, `not_applicable`;
- evidence currency: `current`, `stale`, `unknown`, `conflicting`;
- evidence availability: `available`, `unavailable`, `unknown`, `conflicting`;
- family disposition: `inquiry`, `adjacent_family`, `mixed`, `unclassified`.

Stale, unavailable, out-of-scope, adjacent-family, and mixed testimony remain testimony attributes; they do not rewrite clause standing.

## Ownership boundary

Ownership is derived only from stage producer lineage or adapter lineage. A caller payload flag cannot assert ownership. Clauses without producer lineage or adapter lineage are preserved as unowned rather than upgraded.

## Guardrail preservation

The artifact preserves these boundaries:

- goal-horizon scope is not inquiry scope;
- visible evidence is not eligible evidence territory and is not selected source evidence;
- eligible territory does not select concrete sources or observations;
- uncertainty subject is not sufficient-resolution condition;
- stale or unavailable evidence is not a stopping condition;
- boundary testimony is not frontier assembly, constitutional question formulation, inquiry opening, authorization, execution, recording, event-ledger write, or cluster mutation.

## Implementation

Implementation lives in `seed_runtime/inquiry_frontier_boundary_testimony.py`.

Focused tests live in `tests/test_inquiry_frontier_boundary_testimony.py` and cover exact identity binding, unordered family coexistence, separate dispositions, non-replacement of standing, lineage-derived ownership, visible evidence versus eligible territory, and read-only/no-side-effect boundaries.
