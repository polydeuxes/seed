# Constitutional Relationship Reasoning Path Implementation Slice 005

## Selected boundary

Recovered exactly one implementation-local ownership boundary: capability-needs consumer preservation for Reasoning Path.

The boundary is intentionally narrow. It owns only preservation of `capability_needs` consumer lineage entries for capability need surfaces that match the requested reasoning-path subject. It does not collect upstream surfaces, select relevant ownership rows, project supporting evidence, derive intermediate ownership conclusions, produce selected-row derived capability conclusions, preserve pressure or privilege consumers, preserve story impact, preserve typed Unknowns, assemble payloads, invoke the compatibility handoff, render output, record facts, write the event ledger, mutate cluster state, or redesign the Reasoning Path.

## Implementation evidence

Implementation evidence selected this boundary:

- Slice 004 made selected-row derived capability-conclusion production explicit and left the immediately adjacent `build_capability_needs(...)` loop in `build_reasoning_path_audit(...)`.
- That adjacent loop had two distinct responsibilities: preserving `capability_needs` consumer lineage and preserving the existing compatibility fallback that appends a capability-needs derived conclusion only when selected ownership rows did not already produce one.
- The consumer append was a local, recurring lineage-preservation responsibility: it matched the requested subject against capability name, subjects, and diagnostics, then projected matching needs into `consumers` entries.
- The compatibility fallback remains in `build_reasoning_path_audit(...)`, so this slice does not recover payload assembly, compatibility handoff invocation, or derived conclusion fallback behavior.

## Before

`build_reasoning_path_audit(...)` still compressed these responsibilities after Slice 004:

1. Collect upstream diagnostic surfaces.
2. Hand selected rows to supporting-evidence projection.
3. Hand selected rows to intermediate ownership-conclusion derivation.
4. Hand selected rows to derived capability-conclusion production.
5. Preserve capability-needs consumer lineage.
6. Preserve capability-needs derived-conclusion compatibility fallback.
7. Preserve pressure and privilege consumers.
8. Preserve story impact.
9. Preserve typed Unknowns for evidence gaps.
10. Assemble implementation-local payloads.
11. Hand payloads to `_reasoning_path_from_payloads(...)` for public compatibility.

## After

`build_reasoning_path_audit(...)` still performs the existing orchestration and preserves public behavior, but capability-needs consumer preservation is now owned by `_reasoning_path_capability_need_consumers(...)`.

The helper returns the same consumer dictionaries that the builder previously appended inline. Those consumers continue to be deduplicated into the existing `_DerivationLineagePayload` and projected through the existing compatibility handoff unchanged.

## Recovered producer

`_reasoning_path_capability_need_consumers(...)` now owns the recovered responsibility.

It accepts capability need records and the requested reasoning-path subject, then produces only matching `capability_needs` consumer lineage dictionaries.

## Recovered artifact/helper

Recovered helper:

- `_reasoning_path_capability_need_consumers(...)`

No new payload artifact was required. The recovered boundary is carried by the returned consumer list and then by the existing `_DerivationLineagePayload`.

Existing artifacts preserved:

- `_DerivationSupportingEvidencePayload`
- `_DerivedConclusionPayload`
- `_DerivationLineagePayload`
- `ReasoningPathAudit`

No framework, engine, registry, workflow, planner, scheduler, universal builder, or orchestration system was introduced.

## Recovered consumer

The immediate consumer is still `build_reasoning_path_audit(...)`.

`build_reasoning_path_audit(...)` consumes the capability-needs consumer list by extending `consumers`, preserving the existing capability-needs derived-conclusion compatibility fallback separately, and then passing deduplicated consumers into `_DerivationLineagePayload`.

`_reasoning_path_from_payloads(...)` then projects that existing payload into `ReasoningPathAudit`.

Public downstream consumers remain unchanged:

- `ReasoningPathAudit`
- `reasoning_path_audit_json(...)`
- `format_reasoning_path_audit(...)`

## Required questions

### 1. What responsibilities were previously compressed?

The builder previously compressed upstream surface collection, relevant ownership-row selection, supporting-evidence projection, intermediate ownership-conclusion derivation, selected-row derived capability-conclusion production, capability-needs consumer preservation, capability-needs derived-conclusion compatibility fallback, pressure and privilege consumer preservation, story-impact preservation, typed Unknown preservation, payload assembly, and compatibility handoff invocation.

### 2. Which implementation-local ownership boundary became directly observable?

Capability-needs consumer preservation became directly observable immediately downstream of `_reasoning_path_derived_capability_conclusions(...)` and immediately adjacent to the existing capability-needs fallback loop.

### 3. What producer now owns the recovered responsibility?

`_reasoning_path_capability_need_consumers(...)` owns capability-needs consumer preservation.

### 4. What artifact or helper carries the recovered boundary, if any?

The recovered helper is `_reasoning_path_capability_need_consumers(...)`. No new payload artifact was required; the returned consumer list carries the boundary until it is placed in the existing `_DerivationLineagePayload`.

### 5. Who consumes it?

`build_reasoning_path_audit(...)` consumes the consumer list and passes deduplicated consumers into `_DerivationLineagePayload`; `_reasoning_path_from_payloads(...)` then projects that existing payload into `ReasoningPathAudit`.

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
- `constitutional_relationship_reasoning_path_implementation_slice_005.md`

## LOC changed

Before adding this report, implementation and test diff was:

- `seed_runtime/reasoning_path_audit.py`: +18 / -8
- `tests/test_reasoning_path_audit.py`: +44 / -0

This report was then added as the required deliverable.

## Tests executed

- `pytest -q tests/test_reasoning_path_audit.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

The following responsibilities intentionally remain in `build_reasoning_path_audit(...)` because this slice recovered exactly one adjacent implementation-local ownership boundary:

- Upstream surface collection.
- Capability-needs derived-conclusion compatibility fallback.
- Pressure and privilege consumer preservation.
- Story-impact preservation.
- Typed Unknown preservation.
- Payload assembly.
- Compatibility handoff invocation.
