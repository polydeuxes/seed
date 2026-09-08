# Constitutional Relationship Reasoning Path Implementation Slice 006

## Selected boundary

Recovered exactly one implementation-local ownership boundary: capability-needs derived-conclusion compatibility fallback for Reasoning Path.

The boundary is intentionally narrow. It owns only the preservation of the existing `capability_needs` derived-conclusion fallback when selected ownership rows did not already produce a `capability_needs` derived conclusion. It does not collect upstream surfaces, select relevant ownership rows, project supporting evidence, derive intermediate ownership conclusions, produce selected-row derived capability conclusions, preserve capability-needs consumers, preserve pressure or privilege consumers, preserve story impact, preserve typed Unknowns, assemble payloads, invoke the compatibility handoff, render output, record facts, write the event ledger, mutate cluster state, or redesign the Reasoning Path.

## Implementation evidence

Implementation evidence selected this boundary:

- Slice 005 made capability-needs consumer preservation explicit and left the immediately adjacent capability-needs loop behavior in `build_reasoning_path_audit(...)`.
- The remaining adjacent capability-needs behavior was distinct from consumer preservation: it appended a derived conclusion only when no `capability_needs` conclusion was already present in `derived`.
- The fallback uses the same matching evidence as the consumer path, but owns a different compatibility responsibility: preserving older `capability_needs` conclusion output when selected ownership-row derivation has not supplied it.
- The recovered helper returns the same derived-conclusion dictionaries that the builder previously appended inline and preserves the same suppression behavior when a `capability_needs` conclusion already exists.

## Before

`build_reasoning_path_audit(...)` still compressed these responsibilities after Slice 005:

1. Collect upstream diagnostic surfaces.
2. Hand selected rows to supporting-evidence projection.
3. Hand selected rows to intermediate ownership-conclusion derivation.
4. Hand selected rows to derived capability-conclusion production.
5. Hand capability needs to capability-needs consumer preservation.
6. Preserve capability-needs derived-conclusion compatibility fallback.
7. Preserve pressure and privilege consumers.
8. Preserve story impact.
9. Preserve typed Unknowns for evidence gaps.
10. Assemble implementation-local payloads.
11. Hand payloads to `_reasoning_path_from_payloads(...)` for public compatibility.

## After

`build_reasoning_path_audit(...)` still performs the existing orchestration and preserves public behavior, but capability-needs derived-conclusion compatibility fallback is now owned by `_reasoning_path_capability_need_compatibility_fallbacks(...)`.

The helper returns fallback derived-conclusion dictionaries only when the existing derived-conclusion list has no `capability_needs` surface. Those conclusions continue to be carried by the existing `_DerivedConclusionPayload` and projected through the existing compatibility handoff unchanged.

## Recovered producer

`_reasoning_path_capability_need_compatibility_fallbacks(...)` now owns the recovered responsibility.

It accepts capability need records, the requested reasoning-path subject, and the already-derived conclusions, then produces matching fallback `capability_needs` derived conclusions only when needed for compatibility.

## Recovered artifact/helper

Recovered helper:

- `_reasoning_path_capability_need_compatibility_fallbacks(...)`

No new payload artifact was required. The recovered boundary is carried by the returned fallback derived-conclusion list and then by the existing `_DerivedConclusionPayload`.

Existing artifacts preserved:

- `_DerivationSupportingEvidencePayload`
- `_DerivedConclusionPayload`
- `_DerivationLineagePayload`
- `ReasoningPathAudit`

No framework, engine, registry, workflow, planner, scheduler, universal builder, or orchestration system was introduced.

## Recovered consumer

The immediate consumer is still `build_reasoning_path_audit(...)`.

`build_reasoning_path_audit(...)` consumes the fallback derived-conclusion list by extending `derived` after capability-needs consumers are preserved and before passing the final derived list into `_DerivedConclusionPayload`.

`_reasoning_path_from_payloads(...)` then projects that existing payload into `ReasoningPathAudit`.

Public downstream consumers remain unchanged:

- `ReasoningPathAudit`
- `reasoning_path_audit_json(...)`
- `format_reasoning_path_audit(...)`

## Required questions

### 1. What responsibilities were previously compressed?

The builder previously compressed upstream surface collection, relevant ownership-row selection, supporting-evidence projection, intermediate ownership-conclusion derivation, selected-row derived capability-conclusion production, capability-needs consumer preservation, capability-needs derived-conclusion compatibility fallback, pressure and privilege consumer preservation, story-impact preservation, typed Unknown preservation, payload assembly, and compatibility handoff invocation.

### 2. Which implementation-local ownership boundary became directly observable?

Capability-needs derived-conclusion compatibility fallback became directly observable immediately adjacent to `_reasoning_path_capability_need_consumers(...)` and before pressure and privilege consumer preservation.

### 3. What producer now owns the recovered responsibility?

`_reasoning_path_capability_need_compatibility_fallbacks(...)` owns capability-needs derived-conclusion compatibility fallback.

### 4. What artifact or helper carries the recovered boundary, if any?

The recovered helper is `_reasoning_path_capability_need_compatibility_fallbacks(...)`. No new payload artifact was required; the returned fallback derived-conclusion list carries the boundary until it is placed in the existing `_DerivedConclusionPayload`.

### 5. Who consumes it?

`build_reasoning_path_audit(...)` consumes the fallback derived-conclusion list and passes the final derived conclusions into `_DerivedConclusionPayload`; `_reasoning_path_from_payloads(...)` then projects that existing payload into `ReasoningPathAudit`.

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
- `constitutional_relationship_reasoning_path_implementation_slice_006.md`

## LOC changed

Before adding this report, implementation and test diff was:

- `seed_runtime/reasoning_path_audit.py`: +25 / -11
- `tests/test_reasoning_path_audit.py`: +41 / -0

This report was then added as the required deliverable.

## Tests executed

- `pytest -q tests/test_reasoning_path_audit.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

The following responsibilities intentionally remain in `build_reasoning_path_audit(...)` because this slice recovered exactly one adjacent implementation-local ownership boundary:

- Upstream surface collection.
- Pressure and privilege consumer preservation.
- Story-impact preservation.
- Typed Unknown preservation.
- Payload assembly.
- Compatibility handoff invocation.
