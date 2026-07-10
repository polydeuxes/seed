# Emitter Attribution Audit Slice 001 — Unknown-emitter classification

## District consistency gate

- Active district verified: **Emitter Attribution Audit**.
- Handoff source verified: **`emitter_consumer_audit_outward_scout_004.md`**.
- Completed source district verified: **Emitter/Consumer Audit**.
- Latest completed Emitter/Consumer Audit slice verified: **`emitter_consumer_audit_slice_005.md`**.
- No available report, summary, branch state, or local file pointed to another active district. The Operational Graph outward candidate was not used in this batch.

## Selected boundary

Selected boundary: **Emitter Attribution unknown-emitter classification**.

The recovered responsibility classifies attribution for unknown base audit events and preserves the returned status, reason, emitter, confidence, attribution evidence, and supporting reference fields.

## Implementation evidence

- `build_emitter_attribution_audit(...)` consumes base Emitter/Consumer Audit rows and only invokes this boundary when the base row emitter is `unknown`.
- The classification logic distinguishes direct emitter evidence, workflow dynamic-only evidence, indirect emitter references, discovery gaps, dynamic workflow-only events, and missing emitter evidence.
- The returned fields are consumed by public `EmitterAttributionItem` construction and therefore by JSON and human-readable output.

## Before

Unknown-emitter classification returned an anonymous tuple. The branch owner was present but its field ownership was compressed into tuple position unpacking inside the build loop.

## After

Unknown-emitter classification is carried by `UnknownEmitterAttribution`, and `_classify_unknown_emitter_attribution(...)` returns that artifact. `build_emitter_attribution_audit(...)` consumes named fields while preserving the previous compatibility tuple wrapper `_unknown_attribution(...)`.

## Recovered producer

`_classify_unknown_emitter_attribution(...)` now owns unknown-emitter attribution classification.

## Recovered artifact/helper

`UnknownEmitterAttribution` carries the recovered boundary fields: status, reason, emitter, confidence, attribution evidence, and supporting references.

## Recovered consumer

`build_emitter_attribution_audit(...)` consumes the recovered artifact and constructs the same `EmitterAttributionItem` output as before.

## Compatibility preserved

No.

No compatibility boundary changed: public runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory behavior, diagnostic shape-audit behavior, schema, event-ledger behavior, and read-only mutation boundaries are preserved.

## Files changed

- `seed_runtime/emitter_attribution_audit.py`
- `tests/test_emitter_attribution_audit.py`
- `emitter_attribution_audit_slice_001.md`

## LOC changed

- `seed_runtime/emitter_attribution_audit.py`: added the recovered attribution artifact and changed the build loop to consume named fields while preserving the previous tuple wrapper.
- `tests/test_emitter_attribution_audit.py`: added focused classification assertions for the recovered boundary.
- `emitter_attribution_audit_slice_001.md`: added this slice report.

## Tests executed

- `pytest -q tests/test_emitter_attribution_audit.py` — passed.

## Required questions

1. Previously compressed responsibility: unknown-emitter attribution classification fields were compressed into tuple position ownership.
2. Directly observable ownership boundary: classification for unknown base audit events is now a named implementation-local producer.
3. Producer: `_classify_unknown_emitter_attribution(...)`.
4. Artifact/helper: `UnknownEmitterAttribution`.
5. Consumer: `build_emitter_attribution_audit(...)`, with `_unknown_attribution(...)` retained as compatibility wrapper.
6. Did any compatibility boundary change? No.
7. District containment: this only changes Emitter Attribution Audit classification after the base Emitter/Consumer Audit has produced unknown rows.
8. Distinct from Emitter/Consumer Audit slices: it does not collect scan results, derive relationship status, produce base unknown rows, produce scanned rows, or assemble the base audit.
9. Distinct from Consumer Dependency Audit slices: it does not produce observation-predicate items, diagnostic audit items, or matched consumer groups.
10. Distinct from Frontier Pressure Admission slices: it does not admit pressure candidates, select item sets, score pressure, or produce pressure evidence payloads.
11. Operational Graph avoided: no graph node, edge, confidence, taxonomy, or composition behavior changed.
12. Diagnostic visibility preserved: no diagnostic registration, inventory, or diagnostic-shape surface changed; the existing public surface remains visible as before.
13. Read-only/event-ledger behavior preserved: the audit still only reads implementation evidence and does not write the event ledger or mutate cluster state.
14. Distinct from earlier slices in this batch: this is the first slice in the batch.

## Remaining compressed responsibilities

Implementation-evidence collection remains directly evident in `_implementation_evidence(...)` and should be reassessed separately before any second slice.

## District boundary compliance

This slice remains inside Emitter Attribution Audit, preserves compatibility, and does not recover Operational Graph, diagnostic registration, shape-audit registration, formatting, CLI plumbing, metadata literals, or prior-district work.
