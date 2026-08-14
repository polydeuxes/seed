# Emitter/Consumer Audit Slice 004 — Scanned emitted-item row production

## Selected boundary
Recovered the implementation-local scanned emitted-item row production boundary.

## Implementation evidence
After Slices 001 through 003, `build_emitter_consumer_audit(...)` still directly consumed scan-result `emitted`, `consumed`, and `evidence` collections to construct `EmitterConsumerItem` rows for scanned emitters before appending unknown-emitter rows and applying the final public sort.

## Before
Scanned emitted-item row production was compressed into `build_emitter_consumer_audit(...)`. The builder directly iterated scanned emitter/emission-type groups, derived the visible consumer tuple, consumed `_derive_emitted_output_relationship_status(...)`, aggregated evidence, and constructed scanned-emitter `EmitterConsumerItem` rows.

## After
`_scanned_emitted_item_rows(...)` owns scanned-emitter row production from the existing `EmitterConsumerScanResult`. `build_emitter_consumer_audit(...)` consumes those rows unchanged, then appends `_unknown_emitter_rows(...)` output and preserves the final public sort and metadata.

## Recovered producer
`_scanned_emitted_item_rows(...)`.

## Recovered artifact/helper
The helper returns `EmitterConsumerItem` rows for scanned emitters. It carries the recovered boundary while keeping consumer tuple derivation, relationship-status consumption, and evidence aggregation inside the same row-production responsibility.

## Recovered consumer
`build_emitter_consumer_audit(...)` consumes the returned scanned rows before appending unknown-emitter rows and constructing the final `EmitterConsumerAudit`.

## Compatibility preserved
No compatibility boundary changed.

## Required questions
1. Previously compressed responsibility: producing scanned-emitter `EmitterConsumerItem` rows from scan-result emitted, consumed, and evidence collections.
2. Observable boundary: scanned emitted-item row production is now directly observable as `_scanned_emitted_item_rows(...)`.
3. Producer: `_scanned_emitted_item_rows(...)`.
4. Artifact/helper: returned scanned-emitter `EmitterConsumerItem` rows.
5. Consumer: `build_emitter_consumer_audit(...)`.
6. Did any compatibility boundary change? No.
7. District: the slice only changes Emitter/Consumer Audit row production and focused Emitter/Consumer Audit tests.
8. Slice 001 distinction: this does not collect scan results, discover files, parse AST, classify strings, name emitters, name consumers, or gate rendered strings; it consumes the already-collected `EmitterConsumerScanResult`.
9. Slice 002 distinction: this does not own status derivation rules; it only calls `_derive_emitted_output_relationship_status(...)` while constructing scanned rows.
10. Slice 003 distinction: this does not produce unknown-emitter rows; `build_emitter_consumer_audit(...)` still appends `_unknown_emitter_rows(...)` after scanned rows are produced.
11. Consumer Dependency Audit distinction: this does not modify observation-predicate audit item-family production, diagnostic audit item-family production, or matched consumer group construction.
12. Frontier Pressure distinction: this does not modify pressure-audit admission, source fan-out, evidence payloads, scores, refusals, or item-set selection.
13. Diagnostic visibility: no diagnostic registration, inventory surface, shape-audit contract, public JSON shape, or human-readable format changed; focused tests preserve public scanned-row shape and diagnostic inventory/shape-audit tests were run.
14. Read-only/event-ledger: the recovered helper derives rows from in-memory scan collections only; tests prove the audit still does not write the event ledger or mutate cluster state.

## Files changed
- `seed_runtime/emitter_consumer_audit.py`
- `tests/test_emitter_consumer_audit.py`
- `emitter_consumer_audit_slice_004.md`

## LOC changed
Implementation: one row-production helper extraction. Tests: one focused scanned emitted-item row production preservation test. Report: this file.

## Tests executed
- `python -m pytest -q tests/test_emitter_consumer_audit.py`
- `python -m pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities
No additional adjacent responsibility was recovered in this slice. Consumer tuple derivation and evidence tuple aggregation remain intentionally inside the scanned emitted-row producer, as part of this single-slice boundary. Formatting, JSON conversion, metadata, CLI dispatch, diagnostic registration, source scanning, string classification, status derivation, unknown-row production, Consumer Dependency Audit, and Pressure Audit behavior were intentionally left untouched.

## District boundary compliance
This slice remains inside the Emitter/Consumer Audit district and preserves public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory behavior, diagnostic shape-audit behavior, schema, event-ledger behavior, and read-only mutation boundaries.
