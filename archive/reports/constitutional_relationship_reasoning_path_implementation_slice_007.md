# Constitutional Relationship Reasoning Path Implementation Slice 007

## Selected boundary

Recovered exactly one implementation-local ownership boundary: pressure and privilege consumer preservation for Reasoning Path.

The boundary is intentionally narrow. It owns only the preservation of existing `pressure_audit` and `privilege_discovery` consumer lineage for a requested reasoning-path subject and domain. It does not collect upstream surfaces, select relevant ownership rows, project supporting evidence, derive intermediate ownership conclusions, produce selected-row derived capability conclusions, preserve capability-needs consumers, preserve capability-needs derived-conclusion compatibility fallback, preserve story impact, preserve typed Unknowns, assemble payloads, invoke the compatibility handoff, render output, record facts, write the event ledger, mutate cluster state, or redesign the Reasoning Path.

## Implementation evidence

Implementation evidence selected this boundary:

- Slice 006 recovered capability-needs derived-conclusion compatibility fallback and left the immediately adjacent consumer-preservation loops for pressure and privilege surfaces in `build_reasoning_path_audit(...)`.
- The remaining adjacent behavior did not produce conclusions or evidence. It appended lineage consumer dictionaries to the same `consumers` collection later carried by `_DerivationLineagePayload`.
- The pressure branch matched the requested subject against pressure text and the requested domain against pressure category, then preserved the existing `pressure_audit` consumer shape.
- The privilege branch matched the requested subject against capability names, then preserved the existing `privilege_discovery` consumer shape.
- The recovered helper returns the same consumer dictionaries that the builder previously appended inline, leaving deduplication, story impact, typed Unknown handling, payload assembly, and compatibility handoff unchanged.

## Before

`build_reasoning_path_audit(...)` still compressed these responsibilities after Slice 006:

1. Collect upstream diagnostic surfaces.
2. Hand selected rows to supporting-evidence projection.
3. Hand selected rows to intermediate ownership-conclusion derivation.
4. Hand selected rows to derived capability-conclusion production.
5. Hand capability needs to capability-needs consumer preservation.
6. Hand capability needs to capability-needs derived-conclusion compatibility fallback.
7. Preserve pressure and privilege consumers.
8. Preserve story impact.
9. Preserve typed Unknowns for evidence gaps.
10. Assemble implementation-local payloads.
11. Hand payloads to `_reasoning_path_from_payloads(...)` for public compatibility.

## After

`build_reasoning_path_audit(...)` still performs the existing orchestration and preserves public behavior, but pressure and privilege consumer preservation is now owned by `_reasoning_path_pressure_privilege_consumers(...)`.

The helper returns matching consumer lineage dictionaries for pressure and privilege surfaces. Those consumers continue to be deduplicated by the existing builder flow, carried by the existing `_DerivationLineagePayload`, and projected through the existing compatibility handoff unchanged.

## Recovered producer

`_reasoning_path_pressure_privilege_consumers(...)` now owns the recovered responsibility.

It accepts the already-built pressure audit, privilege discovery result, requested domain, and requested subject, then produces matching `pressure_audit` and `privilege_discovery` consumer lineage entries.

## Recovered artifact/helper

Recovered helper:

- `_reasoning_path_pressure_privilege_consumers(...)`

No new payload artifact was required. The recovered boundary is carried by the returned consumer list and then by the existing `_DerivationLineagePayload`.

Existing artifacts preserved:

- `_DerivationSupportingEvidencePayload`
- `_DerivedConclusionPayload`
- `_DerivationLineagePayload`
- `ReasoningPathAudit`

No framework, engine, registry, workflow, planner, scheduler, universal builder, or orchestration system was introduced.

## Recovered consumer

The immediate consumer is still `build_reasoning_path_audit(...)`.

`build_reasoning_path_audit(...)` consumes the pressure and privilege consumer list by extending `consumers` after capability-needs fallback preservation and before story-impact preservation. The final deduplicated consumer list is passed into `_DerivationLineagePayload`.

`_reasoning_path_from_payloads(...)` then projects that existing lineage payload into `ReasoningPathAudit`.

Public downstream consumers remain unchanged:

- `ReasoningPathAudit`
- `reasoning_path_audit_json(...)`
- `format_reasoning_path_audit(...)`

## Required questions

### 1. What responsibilities were previously compressed?

The builder previously compressed upstream surface collection, relevant ownership-row selection, supporting-evidence projection, intermediate ownership-conclusion derivation, selected-row derived capability-conclusion production, capability-needs consumer preservation, capability-needs derived-conclusion compatibility fallback, pressure and privilege consumer preservation, story-impact preservation, typed Unknown preservation, payload assembly, and compatibility handoff invocation.

### 2. Which implementation-local ownership boundary became directly observable?

Pressure and privilege consumer preservation became directly observable immediately adjacent to `_reasoning_path_capability_need_compatibility_fallbacks(...)` and before story-impact preservation.

### 3. What producer now owns the recovered responsibility?

`_reasoning_path_pressure_privilege_consumers(...)` owns pressure and privilege consumer preservation.

### 4. What artifact or helper carries the recovered boundary, if any?

The recovered helper is `_reasoning_path_pressure_privilege_consumers(...)`. No new payload artifact was required; the returned consumer list carries the boundary until it is placed in the existing `_DerivationLineagePayload`.

### 5. Who consumes it?

`build_reasoning_path_audit(...)` consumes the returned consumer list and passes the deduplicated final consumer lineage into `_DerivationLineagePayload`; `_reasoning_path_from_payloads(...)` then projects that existing payload into `ReasoningPathAudit`.

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
- `constitutional_relationship_reasoning_path_implementation_slice_007.md`

## LOC changed

Before adding this report, implementation and test diff was:

- `seed_runtime/reasoning_path_audit.py`: +35 / -21
- `tests/test_reasoning_path_audit.py`: +58 / -0

This report was then added as the required deliverable.

## Tests executed

- `pytest -q tests/test_reasoning_path_audit.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

The following responsibilities intentionally remain in `build_reasoning_path_audit(...)` because this slice recovered exactly one adjacent implementation-local ownership boundary:

- Upstream surface collection.
- Story-impact preservation.
- Typed Unknown preservation.
- Payload assembly.
- Compatibility handoff invocation.
