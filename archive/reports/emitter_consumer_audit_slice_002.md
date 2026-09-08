# Emitter/Consumer Audit Slice 002 — Relationship-status derivation

## Selected boundary
Recovered the implementation-local relationship-status derivation boundary for emitted output groups.

## Implementation evidence
After Slice 001, `build_emitter_consumer_audit(...)` still directly counted which outputs in each emitted group had visible consumers and translated that coverage into `consumed`, `orphaned`, `partially_consumed`, or `unknown` statuses inline.

## Before
Consumer coverage and status derivation were embedded in emitted-output row construction.

## After
`_derive_emitted_output_relationship_status(...)` owns the status derivation. Item construction consumes the resulting status without changing public fields, summary counts, JSON, or text output.

## Recovered producer
`_derive_emitted_output_relationship_status(...)`.

## Recovered artifact/helper
The helper returns a `RelationshipStatus` value for one emitted output group.

## Recovered consumer
The emitted-output item construction loop in `build_emitter_consumer_audit(...)`.

## Compatibility preserved
No.

## Required questions
1. Previously compressed responsibility: deriving relationship status from emitted output visibility and consumed-output coverage.
2. Observable boundary: `_derive_emitted_output_relationship_status(...)` is now the dedicated producer of relationship status.
3. Producer: `_derive_emitted_output_relationship_status(...)`.
4. Artifact/helper: the helper-returned `RelationshipStatus` value.
5. Consumer: `build_emitter_consumer_audit(...)` while constructing `EmitterConsumerItem` rows for scanned emitters.
6. Did any compatibility boundary change? No.
7. District: the slice only changes Emitter/Consumer Audit status derivation and focused emitter/consumer audit tests.
8. Consumer Dependency distinction: it does not modify observation-predicate audit items, diagnostic audit items, or matched consumer group construction.
9. Frontier Pressure distinction: it does not modify pressure-audit candidate admission, score production, evidence payload ownership, refusal, or item-set selection.
10. Diagnostic visibility: public diagnostic inventory and shape-audit registration remain unchanged; public status fields and summary counts are preserved.
11. Read-only/event-ledger: the helper computes from in-memory scan collections only and does not write the event ledger or mutate cluster state.
12. Earlier batch distinction: Slice 001 recovered scan-result collection; this slice recovers only status derivation after scan data already exists.

## Files changed
- `seed_runtime/emitter_consumer_audit.py`
- `tests/test_emitter_consumer_audit.py`
- `emitter_consumer_audit_slice_002.md`

## LOC changed
Implementation: one status helper extraction. Tests: one focused status preservation test. Report: this file.

## Tests executed
- `python -m pytest -q tests/test_emitter_consumer_audit.py`

## Remaining compressed responsibilities
Unknown-emitter row production remains directly adjacent after emitted-output row construction and is eligible for reassessment as Slice 003.

## District boundary compliance
This slice remains inside Emitter/Consumer Audit and preserves public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory behavior, diagnostic shape-audit behavior, schema, event-ledger behavior, and read-only mutation boundaries.
