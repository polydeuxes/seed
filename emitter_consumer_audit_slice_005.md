# Emitter/Consumer Audit Slice 005 — Final audit assembly

## District consistency gate

- Active district verified: **Emitter/Consumer Audit**.
- Latest relevant completed slice verified: **`emitter_consumer_audit_slice_004.md`**.
- The local slice chain and `emitter_consumer_audit_district_scout_002.md` point to final Emitter/Consumer Audit assembly as the next single-slice target. Nearby Competency Interrogation, DiagnosticSurface, Frontier Pressure Admission, Consumer Dependency Audit, and Pressure Audit files were not used as authority for this district.

## Selected boundary

Selected boundary: **final audit assembly from produced row collections**.

The recovered responsibility consumes already-produced scanned emitted-item rows and unknown-emitter rows, preserves the final public item sort key, and constructs the final `EmitterConsumerAudit` object with unchanged metadata.

## Implementation evidence

- `build_emitter_consumer_audit(...)` already delegated scan-result collection to `_collect_emitter_consumer_scan_result(...)`.
- `build_emitter_consumer_audit(...)` already delegated scanned emitted-item row production to `_scanned_emitted_item_rows(...)`.
- `build_emitter_consumer_audit(...)` already delegated unknown-emitter row production to `_unknown_emitter_rows(...)`.
- The remaining local work in `build_emitter_consumer_audit(...)` was combining those produced row collections, sorting with `(status, emitter, emits)`, and creating `EmitterConsumerAudit` metadata.

## Before

`build_emitter_consumer_audit(...)` compressed high-level orchestration with final audit object assembly:

1. collect scan result;
2. produce scanned emitted-item rows;
3. produce unknown-emitter rows;
4. merge row collections;
5. sort public items;
6. construct `EmitterConsumerAudit` metadata.

## After

`build_emitter_consumer_audit(...)` remains the high-level orchestrator. It now collects the scan result, produces the existing row collections, and delegates final audit object assembly to `_assemble_emitter_consumer_audit(...)`.

## Recovered producer

`_assemble_emitter_consumer_audit(...)` is the recovered producer for final audit assembly.

## Recovered artifact/helper

The recovered helper is `_assemble_emitter_consumer_audit(...)`. It carries no new public schema; it returns the existing `EmitterConsumerAudit` artifact.

## Recovered consumer

`build_emitter_consumer_audit(...)` consumes the assembled `EmitterConsumerAudit` result unchanged and continues to be the public build entry point for CLI, JSON, human-readable formatting, diagnostic inventory, diagnostic shape audit, and adjacent callers.

## Compatibility preserved

No.

No compatibility boundary changed: public runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory behavior, diagnostic shape-audit behavior, schema, event-ledger behavior, and read-only mutation boundaries are preserved.

## Files changed

- `seed_runtime/emitter_consumer_audit.py`
- `tests/test_emitter_consumer_audit.py`
- `emitter_consumer_audit_slice_005.md`

## LOC changed

Implementation and test diff before this report: 105 insertions and 3 deletions across 2 files. The report is additive documentation for this slice.

## Tests executed

- `pytest -q tests/test_emitter_consumer_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 127 tests.

## Focused test coverage

`test_final_audit_assembly_preserves_rows_sorting_metadata_public_outputs_and_visibility` proves:

- scanned emitted rows are consumed by final assembly;
- unknown-emitter rows are consumed by final assembly;
- deterministic item sorting preserves `(status, emitter, emits)` behavior;
- metadata fields are unchanged;
- public JSON output shape is unchanged;
- human-readable output behavior remains observable through the public formatter;
- diagnostic inventory visibility remains present for `emitter_consumer_audit`;
- diagnostic-shape visibility remains consistent;
- event-ledger/read-only behavior remains unchanged.

## Required questions

1. **What responsibility was previously compressed?**
   Final row collection merging, public item sorting, and `EmitterConsumerAudit` metadata construction were compressed inside `build_emitter_consumer_audit(...)` alongside orchestration.

2. **Which implementation-local ownership boundary became directly observable?**
   Final audit assembly from already-produced scanned rows and unknown-emitter rows.

3. **What producer now owns the recovered responsibility?**
   `_assemble_emitter_consumer_audit(...)`.

4. **What artifact or helper carries the recovered boundary, if any?**
   `_assemble_emitter_consumer_audit(...)` is the helper. It returns the existing `EmitterConsumerAudit` artifact.

5. **Who consumes it?**
   `build_emitter_consumer_audit(...)` consumes the assembled audit result and returns it as before.

6. **Did any compatibility boundary change?**
   No.

7. **How does this stay inside the Emitter/Consumer Audit district?**
   The change is limited to `seed_runtime/emitter_consumer_audit.py`, its focused tests, and this Emitter/Consumer Audit slice report. It does not alter other diagnostics or adjacent audit districts.

8. **How is this distinct from Emitter/Consumer Audit Slice 001 scan-result collection?**
   Slice 001 owns collection of emitted, consumed, and evidence scan data. This slice starts after row producers have consumed that scan result and only assembles final audit output from produced rows.

9. **How is this distinct from Emitter/Consumer Audit Slice 002 relationship-status derivation?**
   Slice 002 owns status derivation for emitted outputs. This slice does not derive statuses; it preserves whatever statuses are already present on row items.

10. **How is this distinct from Emitter/Consumer Audit Slice 003 unknown-emitter row production?**
    Slice 003 owns producing unknown-emitter rows. This slice only consumes unknown-emitter rows that have already been produced.

11. **How is this distinct from Emitter/Consumer Audit Slice 004 scanned emitted-item row production?**
    Slice 004 owns producing scanned emitted-item rows. This slice only consumes scanned emitted-item rows that have already been produced.

12. **How is this distinct from Consumer Dependency Audit Slices 001 through 003?**
    This slice does not inspect or change Consumer Dependency Audit item-family production or matched consumer group construction. It only assembles Emitter/Consumer Audit rows into the existing audit object.

13. **How is this distinct from prior Frontier Pressure Admission pressure-audit slices?**
    This slice does not admit candidates, score pressure, select item sets, generate evidence payloads, or implement pressure-audit behavior. It only preserves final Emitter/Consumer Audit object assembly.

14. **How does this preserve diagnostic inventory and diagnostic-shape visibility?**
    No diagnostic registry or shape spec changed. Focused tests assert that `emitter_consumer_audit` remains registered in diagnostic inventory and remains consistent in diagnostic shape audit for JSON support, repo-file use, event-ledger writes, and cluster mutation.

15. **How does this preserve read-only and event-ledger behavior?**
    The recovered helper only combines in-memory row objects and constructs metadata. Focused tests assert an `EventLedger` remains unchanged before and after assembly, and diagnostic inventory/shape assertions preserve `writes_event_ledger=false` and `mutates_cluster=false`.

## Remaining compressed responsibilities

Directly evident remaining work in `build_emitter_consumer_audit(...)` is high-level orchestration of scan collection and row producer calls. No additional implementation-local ownership boundary is recovered by this slice without broad scouting.

## District boundary compliance

This slice does not re-slice scan-result collection, relationship-status derivation, unknown-emitter row production, or scanned emitted-item row production. It does not touch summary count derivation, JSON serialization, human formatting internals, diagnostic registration, CLI dispatch, operational graph consumption, Consumer Dependency Audit, Pressure Audit, DiagnosticSurface behavior, Frontier Pressure Admission behavior, event-ledger mutation, schema, or read-only boundaries.
