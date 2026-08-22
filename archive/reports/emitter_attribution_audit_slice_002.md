# Emitter Attribution Audit Slice 002 — Implementation-evidence collection

## District consistency gate

- Active district verified: **Emitter Attribution Audit**.
- Handoff source verified: **`emitter_consumer_audit_outward_scout_004.md`**.
- Completed source district verified: **Emitter/Consumer Audit**.
- Latest completed Emitter/Consumer Audit slice verified: **`emitter_consumer_audit_slice_005.md`**.
- After Slice 001, implementation-evidence collection remained directly supported by local Emitter Attribution Audit implementation evidence and did not require Operational Graph work.

## Reassessment after Slice 001

Slice 002 remained justified because `_implementation_evidence(...)` still compressed literal reference collection, dynamic event-construction evidence collection, and direct append literal evidence collection into an anonymous tuple returned to the attribution builder. This did not reopen base Emitter/Consumer Audit scan-result collection, source file discovery ownership, emitted-row evidence aggregation, final base audit assembly, or the unknown-emitter attribution classification recovered in Slice 001. Reference-category classification remains owned by `_reference_category(...)` and was not recovered as a separate slice.

## Selected boundary

Selected boundary: **Emitter Attribution implementation-evidence collection**.

The recovered responsibility collects literal references, dynamic event-construction evidence, and direct append literal evidence used by Emitter Attribution Audit.

## Implementation evidence

- The implementation scans repository Python files, parses ASTs, collects dotted string literals as implementation references, records dynamic `Event(...)` or append/append_many calls without constant event kinds, and performs a direct append-literal pass for emitter evidence.
- The returned collections are consumed by the Emitter Attribution Audit builder and by unknown-emitter classification.
- Deterministic ordering is preserved by sorting literal evidence and dynamic evidence by category and location.

## Before

Implementation-evidence collection returned an anonymous `(literal_refs, dynamic_refs)` tuple. The boundary was present but compressed into tuple shape and local variable naming.

## After

Implementation-evidence collection is carried by `EmitterAttributionImplementationEvidence`, and `_collect_emitter_attribution_implementation_evidence(...)` returns that artifact. `_implementation_evidence(...)` remains as a compatibility wrapper for the prior tuple shape.

## Recovered producer

`_collect_emitter_attribution_implementation_evidence(...)` now owns implementation-evidence collection for Emitter Attribution Audit.

## Recovered artifact/helper

`EmitterAttributionImplementationEvidence` carries `literal_references` and `dynamic_event_construction` evidence collections.

## Recovered consumer

`build_emitter_attribution_audit(...)` consumes the recovered artifact. `_implementation_evidence(...)` continues to expose the previous tuple shape for compatibility.

## Compatibility preserved

No.

No compatibility boundary changed: public runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory behavior, diagnostic shape-audit behavior, schema, event-ledger behavior, and read-only mutation boundaries are preserved.

## Files changed

- `seed_runtime/emitter_attribution_audit.py`
- `tests/test_emitter_attribution_audit.py`
- `emitter_attribution_audit_slice_002.md`

## LOC changed

- `seed_runtime/emitter_attribution_audit.py`: added the recovered evidence artifact and producer while retaining the previous tuple wrapper.
- `tests/test_emitter_attribution_audit.py`: added focused implementation-evidence collection coverage.
- `emitter_attribution_audit_slice_002.md`: added this slice report.

## Tests executed

- `pytest -q tests/test_emitter_attribution_audit.py` — passed.

## Required questions

1. Previously compressed responsibility: Emitter Attribution implementation-evidence collection was compressed into an anonymous tuple return.
2. Directly observable ownership boundary: evidence collection for literal references, dynamic event construction, and direct append literals is now a named implementation-local producer.
3. Producer: `_collect_emitter_attribution_implementation_evidence(...)`.
4. Artifact/helper: `EmitterAttributionImplementationEvidence`.
5. Consumer: `build_emitter_attribution_audit(...)`, with `_implementation_evidence(...)` retained as compatibility wrapper.
6. Did any compatibility boundary change? No.
7. District containment: this only changes Emitter Attribution Audit evidence collection used by attribution, after the base audit exists.
8. Distinct from Emitter/Consumer Audit slices: it does not collect base scan results, derive relationship status, produce base unknown rows, produce scanned emitted rows, or assemble the base audit.
9. Distinct from Consumer Dependency Audit slices: it does not produce observation-predicate audit items, diagnostic audit items, or matched consumer groups.
10. Distinct from Frontier Pressure Admission slices: it does not admit pressure candidates, select pressure item sets, score pressure, or produce pressure evidence payloads.
11. Operational Graph avoided: no graph node, edge, confidence, taxonomy, or audit-composition behavior changed.
12. Diagnostic visibility preserved: no diagnostic inventory or diagnostic-shape registration changed; the existing audit surface remains visible unchanged.
13. Read-only/event-ledger behavior preserved: collection remains AST/file evidence only and does not write the event ledger or mutate cluster state.
14. Distinct from earlier slices in this batch: Slice 001 recovered unknown-emitter classification; this slice recovers upstream implementation-evidence collection and does not alter classification decisions.

## Remaining compressed responsibilities

No further same-district implementation-local boundary was directly evident without broad scouting. Reference-category classification remains a helper already separated from evidence collection.

## District boundary compliance

This slice remains inside Emitter Attribution Audit, preserves compatibility, and does not recover Operational Graph, diagnostic registration, shape-audit registration, formatting, CLI plumbing, metadata literals, or prior-district work.
