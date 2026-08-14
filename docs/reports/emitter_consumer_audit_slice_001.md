# Emitter/Consumer Audit Slice 001 — Scan-result collection

## Selected boundary
Recovered the implementation-local scan-result collection boundary in `build_emitter_consumer_audit(...)`.

## Implementation evidence
`build_emitter_consumer_audit(...)` previously scanned repository Python files, parsed ASTs, discovered emitted and consumed strings, classified emission strings, applied `include_rendered` gating, and populated `emitted`, `consumed`, and `evidence` collections inline before audit item construction.

## Before
Scan collection and audit item construction were compressed in one function body.

## After
`_collect_emitter_consumer_scan_result(...)` owns scanning and collection. `build_emitter_consumer_audit(...)` consumes the returned `EmitterConsumerScanResult` and continues constructing public audit items without changing output behavior.

## Recovered producer
`_collect_emitter_consumer_scan_result(...)`.

## Recovered artifact/helper
`EmitterConsumerScanResult` carries the emitted-output, consumed-output, and evidence collections.

## Recovered consumer
`build_emitter_consumer_audit(...)` consumes the scan result for item construction.

## Compatibility preserved
No.

## Required questions
1. Previously compressed responsibility: repository Python scanning, AST discovery, emission classification, include-rendered gating, and emitted/consumed/evidence collection production.
2. Observable boundary: the scan-result collection producer is directly represented by `_collect_emitter_consumer_scan_result(...)` and `EmitterConsumerScanResult`.
3. Producer: `_collect_emitter_consumer_scan_result(...)`.
4. Artifact/helper: `EmitterConsumerScanResult`.
5. Consumer: `build_emitter_consumer_audit(...)`.
6. Did any compatibility boundary change? No.
7. District: the slice only changes `seed_runtime/emitter_consumer_audit.py` and focused emitter/consumer audit tests.
8. Consumer Dependency distinction: it does not touch observation-predicate items, diagnostic items, or matched consumer groups.
9. Frontier Pressure distinction: it does not touch pressure admission, evidence payloads, scores, refusals, or item-set selection.
10. Diagnostic visibility: no diagnostic inventory or shape-audit surface changed; existing public audit shape is preserved.
11. Read-only/event-ledger: scanning still reads source files only and does not write the event ledger or mutate cluster state.
12. Earlier batch slice distinction: this is the first slice in the batch.

## Files changed
- `seed_runtime/emitter_consumer_audit.py`
- `tests/test_emitter_consumer_audit.py`
- `emitter_consumer_audit_slice_001.md`

## LOC changed
Implementation: helper/dataclass extraction only. Tests: one focused preservation test. Report: this file.

## Tests executed
- `python -m pytest -q tests/test_emitter_consumer_audit.py`

## Remaining compressed responsibilities
After this slice, relationship-status derivation remains directly adjacent inside emitted-output item construction and is eligible for reassessment as Slice 002.

## District boundary compliance
This slice remains entirely in the Emitter/Consumer Audit district and preserves public CLI, JSON, human-readable output, schema, diagnostic inventory behavior, diagnostic shape-audit behavior, event-ledger behavior, and read-only mutation boundaries.
