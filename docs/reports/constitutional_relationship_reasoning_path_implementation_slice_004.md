# Constitutional Relationship Reasoning Path Implementation Slice 004

## Selected boundary

Recovered exactly one implementation-local ownership boundary: derived capability-conclusion production from selected ownership rows for Reasoning Path.

The boundary is intentionally narrow. It owns only the conversion of already-selected ownership discrepancy rows and their `diagnostic_capability_need_records(...)` into derived capability conclusion dictionaries that match the requested reasoning-path subject. It does not collect upstream surfaces, select relevant rows, project supporting evidence, derive intermediate ownership conclusions, preserve consumers, preserve story impact, preserve typed Unknowns, assemble payloads, invoke the compatibility handoff, render output, record facts, write the event ledger, mutate cluster state, or redesign the Reasoning Path.

## Implementation evidence

Implementation evidence selected this boundary:

- Slice 002 made relevant ownership-row selection explicit, and Slice 003 showed those selected rows feed intermediate ownership conclusions.
- Immediately downstream of `_reasoning_path_intermediate_conclusions(...)`, `build_reasoning_path_audit(...)` still contained a row-local loop over `diagnostic_capability_need_records(row)`.
- That loop produced only `derived_conclusions` entries for matching candidate capability or source conflict records.
- The later `build_capability_needs(...)` loop still preserves consumer discovery and compatibility fallback behavior separately, so consumer preservation and compatibility handoff remain compressed outside this slice.
- The recovered helper returns the same derived conclusion dictionaries that the builder previously appended inline.

## Before

`build_reasoning_path_audit(...)` still compressed these responsibilities after Slice 003:

1. Collect upstream diagnostic surfaces.
2. Hand selected rows to supporting-evidence projection.
3. Hand selected rows to intermediate ownership-conclusion derivation.
4. Produce derived capability conclusions from selected ownership rows.
5. Collect downstream consumers.
6. Preserve story impact.
7. Preserve typed Unknowns for evidence gaps.
8. Assemble implementation-local payloads.
9. Hand payloads to `_reasoning_path_from_payloads(...)` for public compatibility.

## After

`build_reasoning_path_audit(...)` still performs the existing orchestration and preserves public behavior, but selected-row derived capability-conclusion production is now owned by `_reasoning_path_derived_capability_conclusions(...)`.

The helper returns the same list of derived conclusion dictionaries that the builder previously appended inline. Those conclusions continue to be carried by the existing `_DerivedConclusionPayload` and projected through the existing compatibility handoff unchanged.

## Recovered producer

`_reasoning_path_derived_capability_conclusions(...)` now owns the recovered responsibility.

It accepts already-selected ownership rows and the requested reasoning-path subject, then produces only derived capability conclusion dictionaries supported by matching diagnostic capability-need records from those rows.

## Recovered artifact/helper

Recovered helper:

- `_reasoning_path_derived_capability_conclusions(...)`

No new payload artifact was required. The recovered boundary is carried by the returned derived-conclusion list and then by the existing `_DerivedConclusionPayload`.

Existing artifacts preserved:

- `_DerivationSupportingEvidencePayload`
- `_DerivedConclusionPayload`
- `_DerivationLineagePayload`
- `ReasoningPathAudit`

No framework, engine, registry, workflow, planner, scheduler, universal builder, or orchestration system was introduced.

## Recovered consumer

The immediate consumer is still `build_reasoning_path_audit(...)`.

`build_reasoning_path_audit(...)` consumes the derived capability-conclusion list by preserving it in `derived`, allowing the existing capability-needs consumer loop to append its compatibility fallback only when no capability-needs derived conclusion exists, and then passing the final derived list into `_DerivedConclusionPayload`.

`_reasoning_path_from_payloads(...)` then projects that existing payload into `ReasoningPathAudit`.

Public downstream consumers remain unchanged:

- `ReasoningPathAudit`
- `reasoning_path_audit_json(...)`
- `format_reasoning_path_audit(...)`

## Required questions

### 1. What responsibilities were previously compressed?

The builder previously compressed upstream surface collection, relevant ownership-row selection, supporting-evidence projection, intermediate ownership-conclusion derivation, derived capability-conclusion production, consumer preservation, story-impact preservation, typed Unknown preservation, payload assembly, and compatibility handoff invocation.

### 2. Which implementation-local ownership boundary became directly observable?

Derived capability-conclusion production from selected ownership rows became directly observable immediately downstream of `_reasoning_path_intermediate_conclusions(...)` and immediately upstream of the existing capability-needs consumer loop.

### 3. What producer now owns the recovered responsibility?

`_reasoning_path_derived_capability_conclusions(...)` owns selected-row derived capability-conclusion production.

### 4. What artifact or helper carries the recovered boundary, if any?

The recovered helper is `_reasoning_path_derived_capability_conclusions(...)`. No new payload artifact was required; the returned derived-conclusion list carries the boundary until it is placed in the existing `_DerivedConclusionPayload`.

### 5. Who consumes it?

`build_reasoning_path_audit(...)` consumes the derived-conclusion list and passes it into `_DerivedConclusionPayload`; `_reasoning_path_from_payloads(...)` then projects that existing payload into `ReasoningPathAudit`.

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
- Slice 003 intermediate ownership-conclusion derivation ownership unchanged.
- `_DerivationSupportingEvidencePayload` unchanged.
- `_DerivedConclusionPayload` unchanged.
- `_DerivationLineagePayload` unchanged.
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
- `constitutional_relationship_reasoning_path_implementation_slice_004.md`

## LOC changed

Before adding this report, implementation and test diff was:

- `seed_runtime/reasoning_path_audit.py`: +27 / -19
- `tests/test_reasoning_path_audit.py`: +43 / -0

This report was then added as the required deliverable.

## Tests executed

- `pytest -q tests/test_reasoning_path_audit.py`

## Remaining compressed responsibilities

The following responsibilities intentionally remain in `build_reasoning_path_audit(...)` because this slice recovered exactly one adjacent implementation-local ownership boundary:

- Upstream surface collection.
- Consumer preservation.
- Story-impact preservation.
- Typed Unknown preservation.
- Payload assembly.
- Compatibility handoff invocation.
