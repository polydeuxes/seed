# Constitutional Relationship Reasoning Path Implementation Slice 003

## Selected boundary

Recovered exactly one implementation-local ownership boundary: intermediate ownership-conclusion derivation for Reasoning Path.

The boundary is intentionally narrow. It owns only the derivation of intermediate `ownership attribution incomplete` conclusions from already-selected ownership discrepancy rows that still carry a conflict. It does not select relevant rows, project supporting evidence, produce derived capability conclusions, preserve consumers, preserve story impact, preserve typed Unknowns, assemble payloads, render output, record facts, write the event ledger, mutate cluster state, or redesign the Reasoning Path.

## Implementation evidence

Implementation evidence selected this boundary:

- Slice 002 made relevant ownership-row selection explicit and showed that selected rows feed multiple downstream responsibilities.
- Slice 001 made supporting-evidence projection explicit and showed that selected rows already have a separate evidence-projection consumer.
- Immediately adjacent to those recovered row boundaries, `build_reasoning_path_audit(...)` still contained a local `if row.conflict` block that projected selected ownership rows into intermediate conclusions.
- That block produced only `intermediate_conclusions` entries and did not own derived capability production, consumer preservation, story-impact preservation, typed Unknown preservation, payload assembly, or compatibility handoff.
- The derived capability loop remains in `build_reasoning_path_audit(...)`, preserving the distinction between intermediate ownership conclusions and derived capability conclusions.

## Before

`build_reasoning_path_audit(...)` still compressed these responsibilities after Slice 002:

1. Collect upstream diagnostic surfaces.
2. Hand selected rows to supporting-evidence projection.
3. Derive intermediate ownership conclusions from selected conflict rows.
4. Derive capability need conclusions.
5. Collect downstream consumers.
6. Preserve story impact.
7. Preserve typed Unknowns for evidence gaps.
8. Assemble implementation-local payloads.
9. Hand payloads to `_reasoning_path_from_payloads(...)` for public compatibility.

## After

`build_reasoning_path_audit(...)` still performs the existing orchestration and preserves public behavior, but intermediate ownership-conclusion derivation is now owned by `_reasoning_path_intermediate_conclusions(...)`.

The helper returns the same list of intermediate conclusion dictionaries that the builder previously appended inline. Those conclusions continue to be carried by the existing `_DerivedConclusionPayload` and projected through the existing compatibility handoff unchanged.

## Recovered producer

`_reasoning_path_intermediate_conclusions(...)` now owns the recovered responsibility.

It accepts already-selected ownership rows and produces only intermediate conclusion dictionaries for rows whose `conflict` field is present.

## Recovered artifact/helper

Recovered helper:

- `_reasoning_path_intermediate_conclusions(...)`

No new payload artifact was required. The recovered boundary is carried by the returned intermediate-conclusion list and then by the existing `_DerivedConclusionPayload`.

Existing artifacts preserved:

- `_DerivationSupportingEvidencePayload`
- `_DerivedConclusionPayload`
- `_DerivationLineagePayload`
- `ReasoningPathAudit`

No framework, engine, registry, workflow, planner, scheduler, universal builder, or orchestration system was introduced.

## Recovered consumer

The immediate consumer is still `build_reasoning_path_audit(...)`.

`build_reasoning_path_audit(...)` consumes the intermediate conclusions by passing them into `_DerivedConclusionPayload`, which is then consumed by `_reasoning_path_from_payloads(...)`.

Public downstream consumers remain unchanged:

- `ReasoningPathAudit`
- `reasoning_path_audit_json(...)`
- `format_reasoning_path_audit(...)`

## Required questions

### 1. What responsibilities were previously compressed?

The builder previously compressed upstream surface collection, relevant ownership-row selection, supporting-evidence projection, intermediate ownership-conclusion derivation, derived capability-conclusion production, consumer preservation, story-impact preservation, typed Unknown preservation, payload assembly, and compatibility handoff invocation.

### 2. Which implementation-local ownership boundary became directly observable?

Intermediate ownership-conclusion derivation became directly observable immediately downstream of relevant ownership-row selection and adjacent to supporting-evidence projection.

### 3. What producer now owns the recovered responsibility?

`_reasoning_path_intermediate_conclusions(...)` owns intermediate ownership-conclusion derivation.

### 4. What artifact or helper carries the recovered boundary, if any?

The recovered helper is `_reasoning_path_intermediate_conclusions(...)`. No new payload artifact was required; the returned intermediate-conclusion list carries the boundary until it is placed in the existing `_DerivedConclusionPayload`.

### 5. Who consumes it?

`build_reasoning_path_audit(...)` consumes the intermediate-conclusion list and passes it into `_DerivedConclusionPayload`; `_reasoning_path_from_payloads(...)` then projects that existing payload into `ReasoningPathAudit`.

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
- Slice 002 relevant ownership-row selection ownership unchanged.
- `_DerivationSupportingEvidencePayload` unchanged.
- `_DerivedConclusionPayload` unchanged.
- `_DerivationLineagePayload` unchanged.
- Existing derived conclusion preservation unchanged.
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
- `constitutional_relationship_reasoning_path_implementation_slice_003.md`

## LOC changed

Before adding this report, implementation and test diff was:

- `seed_runtime/reasoning_path_audit.py`: +19 / -10
- `tests/test_reasoning_path_audit.py`: +30 / -0

This report was then added as the required deliverable.

## Tests executed

- `pytest -q tests/test_reasoning_path_audit.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

The following responsibilities intentionally remain in `build_reasoning_path_audit(...)` because this slice recovered exactly one adjacent implementation-local ownership boundary:

- Upstream surface collection.
- Derived capability-conclusion production.
- Consumer preservation.
- Story-impact preservation.
- Typed Unknown preservation.
- Payload assembly.
- Compatibility handoff invocation.
