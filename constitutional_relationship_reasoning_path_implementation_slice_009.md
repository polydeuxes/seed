# Constitutional Relationship Reasoning Path Implementation Slice 009

## Selected boundary

Recovered exactly one implementation-local ownership boundary: typed Unknown preservation for Reasoning Path evidence gaps.

The boundary is intentionally narrow. It owns only deciding whether the existing implementation-local derivation path has no observed evidence, conclusions, consumers, or story impact, and preserving the existing typed `Evidence Gap` Unknown in that case. It does not collect upstream surfaces, select relevant ownership rows, project supporting evidence, derive intermediate ownership conclusions, produce selected-row derived capability conclusions, preserve capability-needs consumers, preserve capability-needs derived-conclusion compatibility fallback, preserve pressure or privilege consumers, preserve story impact, assemble payloads, invoke the compatibility handoff, render output, record facts, write the event ledger, mutate cluster state, or redesign the Reasoning Path.

## Implementation evidence

Implementation evidence selected this boundary:

- Slice 008 recovered story-impact preservation and left the immediately adjacent typed Unknown block in `build_reasoning_path_audit(...)`.
- The remaining adjacent behavior was not payload assembly. It checked the already-produced implementation-local evidence, conclusion, consumer, and story-impact lists before payload construction.
- When every derivation path surface list was empty, it preserved a typed `Evidence Gap` Unknown with `area="derivation"` and reason `no derivation evidence currently available`.
- When any derivation path surface list was present, it preserved no Unknown.
- The recovered helper returns the same `TypedUnknownRecord` list that the builder previously populated inline, leaving `_DerivationLineagePayload`, payload assembly, public conversion through `typed_unknowns_to_public_dicts(...)`, and compatibility handoff unchanged.

## Before

`build_reasoning_path_audit(...)` still compressed these responsibilities after Slice 008:

1. Collect upstream diagnostic surfaces.
2. Hand selected rows to supporting-evidence projection.
3. Hand selected rows to intermediate ownership-conclusion derivation.
4. Hand selected rows to derived capability-conclusion production.
5. Hand capability needs to capability-needs consumer preservation.
6. Hand capability needs to capability-needs derived-conclusion compatibility fallback.
7. Hand pressure and privilege surfaces to pressure and privilege consumer preservation.
8. Hand operational story to story-impact preservation.
9. Preserve typed Unknowns for evidence gaps.
10. Assemble implementation-local payloads.
11. Hand payloads to `_reasoning_path_from_payloads(...)` for public compatibility.

## After

`build_reasoning_path_audit(...)` still performs the existing orchestration and preserves public behavior, but typed Unknown evidence-gap preservation is now owned by `_reasoning_path_typed_unknowns(...)`.

The helper receives the already-produced supporting-evidence payload, intermediate conclusions, derived conclusions, consumers, and story-impact entries. It returns either the existing typed `Evidence Gap` Unknown or an empty list. Typed Unknowns continue to be carried by the existing `_DerivationLineagePayload`, and public output conversion remains inside the existing compatibility handoff unchanged.

## Recovered producer

`_reasoning_path_typed_unknowns(...)` now owns the recovered responsibility.

It accepts the already-built implementation-local derivation path surfaces and produces typed Unknown records only when no derivation evidence is currently available.

## Recovered artifact/helper

Recovered helper:

- `_reasoning_path_typed_unknowns(...)`

No new payload artifact was required. The recovered boundary is carried by the returned `TypedUnknownRecord` list and then by the existing `_DerivationLineagePayload`.

Existing artifacts preserved:

- `_DerivationSupportingEvidencePayload`
- `_DerivedConclusionPayload`
- `_DerivationLineagePayload`
- `ReasoningPathAudit`

No framework, engine, registry, workflow, planner, scheduler, universal builder, or orchestration system was introduced.

## Recovered consumer

The immediate consumer is still `build_reasoning_path_audit(...)`.

`build_reasoning_path_audit(...)` consumes the returned typed Unknown list and passes it into `_DerivationLineagePayload`. `_reasoning_path_from_payloads(...)` then projects that existing lineage payload into `ReasoningPathAudit` by using the existing public typed Unknown conversion.

Public downstream consumers remain unchanged:

- `ReasoningPathAudit`
- `reasoning_path_audit_json(...)`
- `format_reasoning_path_audit(...)`

## Required questions

### 1. What responsibilities were previously compressed?

The builder previously compressed upstream surface collection, relevant ownership-row selection, supporting-evidence projection, intermediate ownership-conclusion derivation, selected-row derived capability-conclusion production, capability-needs consumer preservation, capability-needs derived-conclusion compatibility fallback, pressure and privilege consumer preservation, story-impact preservation, typed Unknown preservation, payload assembly, and compatibility handoff invocation.

### 2. Which implementation-local ownership boundary became directly observable?

Typed Unknown preservation became directly observable immediately adjacent to `_reasoning_path_story_impact(...)` and before lawful terminal payload assembly.

### 3. What producer now owns the recovered responsibility?

`_reasoning_path_typed_unknowns(...)` owns typed Unknown evidence-gap preservation.

### 4. What artifact or helper carries the recovered boundary, if any?

The recovered helper is `_reasoning_path_typed_unknowns(...)`. No new payload artifact was required; the returned `TypedUnknownRecord` list carries the boundary until it is placed in the existing `_DerivationLineagePayload`.

### 5. Who consumes it?

`build_reasoning_path_audit(...)` consumes the returned typed Unknown list and passes it into `_DerivationLineagePayload`; `_reasoning_path_from_payloads(...)` then projects that existing payload into `ReasoningPathAudit`.

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
- Slice 008 story-impact preservation ownership unchanged.
- `_DerivationSupportingEvidencePayload` unchanged.
- `_DerivedConclusionPayload` unchanged.
- `_DerivationLineagePayload` unchanged.
- Existing conclusion preservation unchanged.
- Existing lineage preservation unchanged.
- Typed Unknown public projection unchanged.
- Read-only behavior unchanged.
- No event-ledger writes added.
- No fact recording added.
- No cluster mutation added.

## Files changed

- `seed_runtime/reasoning_path_audit.py`
- `tests/test_reasoning_path_audit.py`
- `constitutional_relationship_reasoning_path_implementation_slice_009.md`

## LOC changed

Before adding this report, implementation and test diff was:

- `seed_runtime/reasoning_path_audit.py`: +33 / -15
- `tests/test_reasoning_path_audit.py`: +32 / -0

This report was then added as the required deliverable.

## Tests executed

- `pytest -q tests/test_reasoning_path_audit.py`

## Remaining compressed responsibilities

The following responsibilities intentionally remain in `build_reasoning_path_audit(...)` because this slice recovered exactly one adjacent implementation-local ownership boundary:

- Upstream surface collection.
- Payload assembly.
- Compatibility handoff invocation.
