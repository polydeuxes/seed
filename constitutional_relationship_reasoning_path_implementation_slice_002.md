# Constitutional Relationship Reasoning Path Implementation Slice 002

## Selected boundary

Recovered exactly one implementation-local ownership boundary: relevant ownership-row selection for Reasoning Path.

The boundary is intentionally narrow. It owns only selection of ownership discrepancy rows relevant to a requested reasoning-path subject, including direct row subject/conflict matches and matches through diagnostic capability-need records implied by those rows. It does not project supporting evidence, derive intermediate conclusions, produce derived capability conclusions, preserve consumers, preserve story impact, preserve typed Unknowns, assemble payloads, render output, record facts, write the event ledger, mutate cluster state, or redesign the Reasoning Path.

## Implementation evidence

Implementation evidence selected this boundary:

- Slice 001 made supporting-evidence projection explicit and showed that projection receives already-selected rows.
- Immediately upstream of `_reasoning_path_supporting_evidence_payload(...)`, `build_reasoning_path_audit(...)` still contained the row-selection comprehension.
- That selection was recurring local responsibility: it matched the requested subject against row subject/conflict fields and against `diagnostic_capability_need_records(row)` candidate capability/conflict fields.
- The selected rows were consumed by both `_reasoning_path_supporting_evidence_payload(...)` and the existing conclusion derivation loop, making the selection boundary directly observable without changing compatibility output.

## Before

`build_reasoning_path_audit(...)` still compressed these responsibilities after Slice 001:

1. Collect upstream diagnostic surfaces.
2. Select relevant ownership discrepancy rows.
3. Hand selected rows to supporting-evidence projection.
4. Derive intermediate conclusions.
5. Derive capability need conclusions.
6. Collect downstream consumers.
7. Preserve story impact.
8. Preserve typed Unknowns for evidence gaps.
9. Assemble implementation-local payloads.
10. Hand payloads to `_reasoning_path_from_payloads(...)` for public compatibility.

## After

`build_reasoning_path_audit(...)` still performs the existing orchestration and preserves public behavior, but relevant ownership-row selection is now owned by `_reasoning_path_relevant_ownership_rows(...)`.

The helper returns the same selected row objects that the builder previously selected inline. Those rows continue to feed the Slice 001 supporting-evidence projection and the existing conclusion derivation logic unchanged.

## Recovered producer

`_reasoning_path_relevant_ownership_rows(...)` now owns the recovered responsibility.

It accepts ownership discrepancy rows and the requested reasoning-path subject, then returns only rows relevant by direct subject/conflict match or by implied diagnostic capability need match.

## Recovered artifact/helper

Recovered helper:

- `_reasoning_path_relevant_ownership_rows(...)`

No new artifact was required. The recovered boundary is carried by the selected row list returned from the helper.

Existing artifacts preserved:

- `_DerivationSupportingEvidencePayload`
- `_DerivedConclusionPayload`
- `_DerivationLineagePayload`
- `ReasoningPathAudit`

No framework, engine, registry, workflow, planner, scheduler, universal builder, or orchestration system was introduced.

## Recovered consumer

The immediate consumer is still `build_reasoning_path_audit(...)`.

`build_reasoning_path_audit(...)` consumes the selected rows by:

- passing them to `_reasoning_path_supporting_evidence_payload(...)`; and
- iterating them in the existing intermediate-conclusion and derived capability-conclusion logic.

Public downstream consumers remain unchanged:

- `ReasoningPathAudit`
- `reasoning_path_audit_json(...)`
- `format_reasoning_path_audit(...)`

## Required questions

### 1. What responsibilities were previously compressed?

The builder previously compressed upstream surface collection, relevant ownership-row selection, supporting-evidence projection, intermediate-conclusion derivation, derived capability-conclusion production, consumer preservation, story-impact preservation, typed Unknown preservation, payload assembly, and compatibility handoff invocation.

### 2. Which implementation-local ownership boundary became directly observable?

Relevant ownership-row selection became directly observable immediately upstream of Slice 001's supporting-evidence projection boundary.

### 3. What producer now owns the recovered responsibility?

`_reasoning_path_relevant_ownership_rows(...)` owns relevant ownership-row selection.

### 4. What artifact or helper carries the recovered boundary, if any?

The recovered helper is `_reasoning_path_relevant_ownership_rows(...)`. No new payload artifact was required; the returned selected row list carries the boundary.

### 5. Who consumes it?

`build_reasoning_path_audit(...)` consumes the selected rows, then passes them to `_reasoning_path_supporting_evidence_payload(...)` and the existing conclusion derivation loop.

### 6. Did any compatibility boundary change?

```text
No.
```

## Compatibility preserved

Did any compatibility boundary change?

```text
No.
```

Preserved behavior:

- Public CLI behavior unchanged.
- JSON output shape unchanged.
- Text rendering unchanged.
- `ReasoningPathAudit` compatibility shape unchanged.
- Slice 001 supporting-evidence projection ownership unchanged.
- `_DerivationSupportingEvidencePayload` unchanged.
- Existing conclusion preservation unchanged.
- Existing lineage preservation unchanged.
- Typed Unknown preservation unchanged.
- Story-impact preservation unchanged.
- Read-only behavior unchanged.
- No event-ledger writes added.
- No fact recording added.
- No cluster mutation added.

## Files changed

- `seed_runtime/reasoning_path_audit.py`
- `tests/test_reasoning_path_audit.py`
- `constitutional_relationship_reasoning_path_implementation_slice_002.md`

## LOC changed

Before adding this report, implementation and test diff was:

- `seed_runtime/reasoning_path_audit.py`: +19 / -11
- `tests/test_reasoning_path_audit.py`: +41 / -0

This report was then added as the required deliverable.

## Tests executed

- `pytest -q tests/test_reasoning_path_audit.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

The following responsibilities intentionally remain in `build_reasoning_path_audit(...)` because this slice recovered exactly one adjacent implementation-local ownership boundary:

- Upstream surface collection.
- Intermediate conclusion derivation.
- Derived capability conclusion production.
- Consumer preservation.
- Story-impact preservation.
- Typed Unknown preservation.
- Payload assembly.
- Compatibility handoff invocation.
