# Constitutional Relationship Reasoning Path Implementation Slice 001

## Selected boundary

Recovered exactly one implementation-local ownership boundary: supporting-evidence row projection for Reasoning Path.

The boundary is intentionally narrow. It owns only the conversion of already-selected ownership discrepancy rows into `_DerivationSupportingEvidencePayload` evidence rows. It does not select relevant rows, derive conclusions, preserve lineage, preserve typed Unknowns, render output, record facts, write the event ledger, mutate cluster state, or redesign the Reasoning Path.

## Implementation evidence

Implementation evidence selected this boundary:

- `build_reasoning_path_audit(...)` already selected `relevant_rows` from `build_ownership_discrepancies(...)` and `diagnostic_capability_need_records(...)`.
- `_DerivationSupportingEvidencePayload` already existed as the implementation-local payload artifact for supporting evidence.
- `_reasoning_path_from_payloads(...)` already consumed `_DerivationSupportingEvidencePayload` and projected its `evidence` into the public `ReasoningPathAudit` compatibility shape.
- The compressed builder body previously projected each selected source row directly into public evidence dictionaries before passing the dictionaries through the existing payload handoff.

## Before

`build_reasoning_path_audit(...)` compressed these responsibilities in one producer-sized body:

1. Collect upstream diagnostic surfaces.
2. Select relevant ownership discrepancy rows.
3. Project selected rows into supporting evidence dictionaries.
4. Derive intermediate conclusions.
5. Derive capability need conclusions.
6. Collect downstream consumers.
7. Preserve story impact.
8. Preserve typed Unknowns for evidence gaps.
9. Assemble implementation-local payloads.
10. Hand payloads to `_reasoning_path_from_payloads(...)` for public compatibility.

## After

`build_reasoning_path_audit(...)` still performs the existing orchestration and preserves public behavior, but the selected-row-to-supporting-evidence projection is now owned by `_reasoning_path_supporting_evidence_payload(...)`.

The helper returns the existing `_DerivationSupportingEvidencePayload` artifact and is consumed by the existing compatibility handoff unchanged.

## Recovered producer

`_reasoning_path_supporting_evidence_payload(...)` now owns the recovered responsibility.

It accepts already-selected source rows and produces the implementation-local supporting evidence payload.

## Recovered artifact/helper

Recovered helper:

- `_reasoning_path_supporting_evidence_payload(...)`

Existing artifact preserved:

- `_DerivationSupportingEvidencePayload`

No new framework, engine, registry, workflow, planner, scheduler, universal builder, or orchestration system was introduced.

## Recovered consumer

The immediate consumer is still `build_reasoning_path_audit(...)`, which passes the payload to `_reasoning_path_from_payloads(...)`.

The public downstream consumers remain unchanged:

- `ReasoningPathAudit`
- `reasoning_path_audit_json(...)`
- `format_reasoning_path_audit(...)`

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
- Existing payload artifacts unchanged.
- Read-only behavior unchanged.
- Evidence preservation unchanged.
- Conclusion preservation unchanged.
- Lineage preservation unchanged.
- Typed Unknown preservation unchanged.
- Story-impact preservation unchanged.
- No event-ledger writes added.
- No fact recording added.
- No cluster mutation added.

## Files changed

- `seed_runtime/reasoning_path_audit.py`
- `tests/test_reasoning_path_audit.py`
- `constitutional_relationship_reasoning_path_implementation_slice_001.md`

## LOC changed

Before adding this report, implementation and test diff was:

- `seed_runtime/reasoning_path_audit.py`: +30 / -14
- `tests/test_reasoning_path_audit.py`: +44 / -0

This report was then added as the required deliverable.

## Tests executed

- `pytest -q tests/test_reasoning_path_audit.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

The following responsibilities intentionally remain in `build_reasoning_path_audit(...)` because this slice recovered exactly one boundary:

- Upstream surface collection.
- Relevant row selection.
- Intermediate conclusion derivation.
- Derived capability conclusion production.
- Consumer preservation.
- Story-impact preservation.
- Typed Unknown preservation.
- Payload assembly.
- Compatibility handoff invocation.
