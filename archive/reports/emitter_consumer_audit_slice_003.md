# Emitter/Consumer Audit Slice 003 — Unknown-emitter row production

## Selected boundary
Recovered the implementation-local unknown-emitter row production boundary.

## Implementation evidence
After Slices 001 and 002, `build_emitter_consumer_audit(...)` still directly compared consumed outputs against all visible scanned emissions and appended `unknown` emitter rows inline for consumed outputs that had visible consumers but no visible scanned emitter.

## Before
Unknown-emitter row production was compressed into `build_emitter_consumer_audit(...)` after scanned-emitter item construction.

## After
`_unknown_emitter_rows(...)` owns production of rows for consumed outputs with visible consumers but no scanned emitter. `build_emitter_consumer_audit(...)` extends its item list with those rows and preserves the final public sort.

## Recovered producer
`_unknown_emitter_rows(...)`.

## Recovered artifact/helper
The helper returns `EmitterConsumerItem` rows with `emitter="unknown"`, singleton emitted output, sorted consumers, `status="unknown"`, empty evidence, and the original emission type.

## Recovered consumer
`build_emitter_consumer_audit(...)` consumes the returned rows before final sorting and audit construction.

## Compatibility preserved
No.

## Required questions
1. Previously compressed responsibility: producing audit rows for consumed outputs that have visible consumers but no visible scanned emitter.
2. Observable boundary: `_unknown_emitter_rows(...)` is now the dedicated row producer.
3. Producer: `_unknown_emitter_rows(...)`.
4. Artifact/helper: returned `EmitterConsumerItem` rows.
5. Consumer: `build_emitter_consumer_audit(...)`.
6. Did any compatibility boundary change? No.
7. District: the slice only changes Emitter/Consumer Audit row production and focused emitter/consumer audit tests.
8. Consumer Dependency distinction: it does not modify observation-predicate audit item production, diagnostic audit item production, or matched consumer groups.
9. Frontier Pressure distinction: it does not modify pressure-audit admission, evidence payloads, scores, refusals, or item-set selection.
10. Diagnostic visibility: no diagnostic registration or shape contract changed; public JSON and human-readable unknown-row shape is preserved.
11. Read-only/event-ledger: the helper derives rows from in-memory scan collections only and does not write the event ledger or mutate cluster state.
12. Earlier batch distinction: Slice 001 recovered scan collection, Slice 002 recovered emitted-group status derivation, and this slice recovers only unknown-emitter row production.

## Files changed
- `seed_runtime/emitter_consumer_audit.py`
- `tests/test_emitter_consumer_audit.py`
- `emitter_consumer_audit_slice_003.md`

## LOC changed
Implementation: one row-production helper extraction. Tests: one focused unknown-emitter preservation test. Report: this file.

## Tests executed
- `python -m pytest -q tests/test_emitter_consumer_audit.py`

## Remaining compressed responsibilities
No further adjacent implementation-local ownership boundary was recovered in this batch. Formatting, JSON helpers, metadata, CLI, diagnostic registration, and presentation output were intentionally left untouched.

## District boundary compliance
This slice remains inside Emitter/Consumer Audit and preserves public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory behavior, diagnostic shape-audit behavior, schema, event-ledger behavior, and read-only mutation boundaries.
