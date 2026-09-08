# Constitutional Relationship Reasoning Path Implementation Slice 008

## Selected boundary

Recovered exactly one implementation-local ownership boundary: story-impact preservation for Reasoning Path.

The boundary is intentionally narrow. It owns only the preservation of existing `operational_story` impact entries and the matching `operational_story` consumer lineage for a requested reasoning-path subject and domain. It does not collect upstream surfaces, select relevant ownership rows, project supporting evidence, derive intermediate ownership conclusions, produce selected-row derived capability conclusions, preserve capability-needs consumers, preserve capability-needs derived-conclusion compatibility fallback, preserve pressure or privilege consumers, preserve typed Unknowns, assemble payloads, invoke the compatibility handoff, render output, record facts, write the event ledger, mutate cluster state, or redesign the Reasoning Path.

## Implementation evidence

Implementation evidence selected this boundary:

- Slice 007 recovered pressure and privilege consumer preservation and left the immediately adjacent `operational_story` conditional in `build_reasoning_path_audit(...)`.
- The remaining adjacent behavior did not produce source evidence or derived conclusions. It preserved story impact and an associated `operational_story` consumer entry for lineage.
- The story branch matched the requested subject against the operational story JSON and the requested domain against the story focus.
- When matched, it preserved the existing story-impact dictionary shape and the existing operational-story consumer dictionary shape.
- The recovered helper returns the same story-impact and consumer dictionaries that the builder previously appended inline, leaving typed Unknown handling, payload assembly, deduplication of final consumers, and compatibility handoff unchanged.

## Before

`build_reasoning_path_audit(...)` still compressed these responsibilities after Slice 007:

1. Collect upstream diagnostic surfaces.
2. Hand selected rows to supporting-evidence projection.
3. Hand selected rows to intermediate ownership-conclusion derivation.
4. Hand selected rows to derived capability-conclusion production.
5. Hand capability needs to capability-needs consumer preservation.
6. Hand capability needs to capability-needs derived-conclusion compatibility fallback.
7. Hand pressure and privilege surfaces to pressure and privilege consumer preservation.
8. Preserve story impact.
9. Preserve typed Unknowns for evidence gaps.
10. Assemble implementation-local payloads.
11. Hand payloads to `_reasoning_path_from_payloads(...)` for public compatibility.

## After

`build_reasoning_path_audit(...)` still performs the existing orchestration and preserves public behavior, but story-impact preservation is now owned by `_reasoning_path_story_impact(...)`.

The helper returns matching story-impact dictionaries and matching `operational_story` consumer lineage dictionaries. Story impact continues to be carried by the existing `_DerivationLineagePayload`, and consumers continue through the existing deduplication and compatibility handoff unchanged.

## Recovered producer

`_reasoning_path_story_impact(...)` now owns the recovered responsibility.

It accepts the already-built operational story, requested domain, and requested subject, then produces matching `operational_story` story-impact entries and associated consumer lineage entries when the story references the reasoning-path subject or domain.

## Recovered artifact/helper

Recovered helper:

- `_reasoning_path_story_impact(...)`

No new payload artifact was required. The recovered boundary is carried by the returned story-impact and consumer lists and then by the existing `_DerivationLineagePayload`.

Existing artifacts preserved:

- `_DerivationSupportingEvidencePayload`
- `_DerivedConclusionPayload`
- `_DerivationLineagePayload`
- `ReasoningPathAudit`

No framework, engine, registry, workflow, planner, scheduler, universal builder, or orchestration system was introduced.

## Recovered consumer

The immediate consumer is still `build_reasoning_path_audit(...)`.

`build_reasoning_path_audit(...)` consumes the story-impact list by extending `story_impact` after pressure and privilege consumer preservation and before typed Unknown preservation. It consumes the returned consumer list by extending `consumers`; final consumers are still deduplicated before being placed in `_DerivationLineagePayload`.

`_reasoning_path_from_payloads(...)` then projects that existing lineage payload into `ReasoningPathAudit`.

Public downstream consumers remain unchanged:

- `ReasoningPathAudit`
- `reasoning_path_audit_json(...)`
- `format_reasoning_path_audit(...)`

## Required questions

### 1. What responsibilities were previously compressed?

The builder previously compressed upstream surface collection, relevant ownership-row selection, supporting-evidence projection, intermediate ownership-conclusion derivation, selected-row derived capability-conclusion production, capability-needs consumer preservation, capability-needs derived-conclusion compatibility fallback, pressure and privilege consumer preservation, story-impact preservation, typed Unknown preservation, payload assembly, and compatibility handoff invocation.

### 2. Which implementation-local ownership boundary became directly observable?

Story-impact preservation became directly observable immediately adjacent to `_reasoning_path_pressure_privilege_consumers(...)` and before typed Unknown preservation.

### 3. What producer now owns the recovered responsibility?

`_reasoning_path_story_impact(...)` owns story-impact preservation.

### 4. What artifact or helper carries the recovered boundary, if any?

The recovered helper is `_reasoning_path_story_impact(...)`. No new payload artifact was required; the returned story-impact and consumer lists carry the boundary until they are placed in the existing `_DerivationLineagePayload`.

### 5. Who consumes it?

`build_reasoning_path_audit(...)` consumes the returned story-impact and consumer lists and passes them into `_DerivationLineagePayload`; `_reasoning_path_from_payloads(...)` then projects that existing payload into `ReasoningPathAudit`.

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
- Slice 004 selected-row derived capability-conclusion production ownership unchanged.
- Slice 005 capability-needs consumer preservation ownership unchanged.
- Slice 006 capability-needs derived-conclusion compatibility fallback ownership unchanged.
- Slice 007 pressure and privilege consumer preservation ownership unchanged.
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
- `constitutional_relationship_reasoning_path_implementation_slice_008.md`

## LOC changed

Before adding this report, implementation and test diff was:

- `seed_runtime/reasoning_path_audit.py`: +30 / -18
- `tests/test_reasoning_path_audit.py`: +45 / -0

This report was then added as the required deliverable.

## Tests executed

- `pytest -q tests/test_reasoning_path_audit.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

The following responsibilities intentionally remain in `build_reasoning_path_audit(...)` because this slice recovered exactly one adjacent implementation-local ownership boundary:

- Upstream surface collection.
- Typed Unknown preservation.
- Payload assembly.
- Compatibility handoff invocation.
