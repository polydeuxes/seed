# Emitter Attribution Audit Slice 003 — Known-emitter attributed row construction

## District consistency gate

- Active district verified: **Emitter Attribution Audit**.
- Latest relevant completed slice verified: **`emitter_attribution_audit_slice_002.md`**.
- Latest local district scout verified: **`emitter_attribution_audit_district_scout_001.md`**.
- No available report, summary, branch state, or local file pointed to a different active district.
- Unrelated district reports were not used as authority.

## Selected boundary

Selected boundary: **known-emitter attributed row construction**.

The recovered responsibility is: for base Emitter/Consumer Audit items whose emitter is known, produce Emitter Attribution Audit attributed rows while preserving event, emitter, status, reason, consumers, evidence, emission type, confidence, and direct-emitter attribution evidence.

## Implementation evidence

`build_emitter_attribution_audit(...)` consumed completed Emitter/Consumer Audit items and, for every base item whose `emitter != "unknown"`, directly constructed `EmitterAttributionItem` rows with:

- each emitted event copied into `event`;
- the base emitter copied into `emitter`;
- status fixed to `attributed`;
- reason fixed to `direct event emission evidence is attributed by the emitter/consumer audit`;
- consumers copied from the base item;
- non-empty base evidence copied into `evidence`;
- emission type copied from the base item;
- confidence fixed to `high`;
- attribution evidence converted from base evidence into `ClassifiedEvidence("direct_emitter", location)`.

This behavior was implementation-backed, local to Emitter Attribution Audit, and not already separated before this slice.

## Before

Known-emitter row construction was compressed inside `build_emitter_attribution_audit(...)` alongside high-level orchestration, unknown-emitter classification consumption, sorting, and metadata construction.

## After

Known-emitter row construction is owned by `_known_emitter_attributed_rows(...)`. `build_emitter_attribution_audit(...)` remains the high-level orchestrator: it obtains the base audit and implementation evidence, consumes known-emitter rows from the recovered helper, keeps unknown-emitter handling in the existing path, and preserves the existing sorted final audit assembly and metadata.

## Recovered producer

`_known_emitter_attributed_rows(...)` now produces known-emitter attributed rows for Emitter Attribution Audit.

## Recovered artifact/helper

Recovered helper: `_known_emitter_attributed_rows(...)`.

No new public schema artifact was added.

## Recovered consumer

`build_emitter_attribution_audit(...)` consumes the produced attributed rows unchanged.

## Compatibility preserved

No.

No compatibility boundary changed: public runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory behavior, diagnostic shape-audit behavior, schema, event-ledger behavior, and read-only mutation boundaries are preserved.

## Files changed

- `seed_runtime/emitter_attribution_audit.py`
- `tests/test_emitter_attribution_audit.py`
- `emitter_attribution_audit_slice_003.md`

## LOC changed

- `seed_runtime/emitter_attribution_audit.py`: extracted one helper and changed the builder call site to consume it.
- `tests/test_emitter_attribution_audit.py`: added focused known-emitter attributed-row tests and public-output/read-only coverage.
- `emitter_attribution_audit_slice_003.md`: added this slice report.

## Tests executed

- `pytest -q tests/test_emitter_attribution_audit.py` — passed.

## Required questions

1. **What responsibility was previously compressed?** Known-emitter attributed row construction for base audit items whose emitter was not `unknown`.
2. **Which implementation-local ownership boundary became directly observable?** The boundary that turns known-emitter base Emitter/Consumer Audit items into Emitter Attribution Audit `attributed` rows.
3. **What producer now owns the recovered responsibility?** `_known_emitter_attributed_rows(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** `_known_emitter_attributed_rows(...)` carries the boundary.
5. **Who consumes it?** `build_emitter_attribution_audit(...)`.
6. **Did any compatibility boundary change?** No.
7. **How does this stay inside the Emitter Attribution Audit district?** It only changes row construction after the base Emitter/Consumer Audit has already produced base items and before Emitter Attribution Audit returns its existing item schema.
8. **How is this distinct from Emitter Attribution Audit Slice 001 unknown-emitter classification?** It handles only base items whose emitter is already known; it does not classify unknown emitters, choose unknown-emitter statuses, derive unknown-emitter reasons, or modify `_classify_unknown_emitter_attribution(...)`.
9. **How is this distinct from Emitter Attribution Audit Slice 002 implementation-evidence collection?** It does not scan files, collect literal references, collect dynamic event-construction evidence, collect direct append literals, or modify `_collect_emitter_attribution_implementation_evidence(...)`.
10. **How is this distinct from prior Emitter/Consumer Audit slices?** It consumes completed base Emitter/Consumer Audit rows and does not collect scan results, derive relationship status, produce base unknown-emitter rows, produce scanned emitted-item rows, or assemble the base audit.
11. **How is this distinct from prior Consumer Dependency Audit slices?** It does not produce observation-predicate audit item families, diagnostic audit item families, or matched consumer groups.
12. **How is this distinct from prior Frontier Pressure Admission slices?** It does not admit pressure candidates, fan out consumer-predicate sources, build pressure evidence payloads, score pressure, refuse pressure findings, or select pressure item sets.
13. **How does this avoid Operational Graph work?** It creates no graph nodes, edges, graph confidence, graph taxonomy, graph storage, or Operational Graph audit behavior.
14. **How does this preserve diagnostic inventory and diagnostic-shape visibility?** It does not add or alter a diagnostic surface, CLI flag, recordable output, inventory registration, or shape-audit registration; the existing Emitter Attribution Audit surface remains unchanged.
15. **How does this preserve read-only and event-ledger behavior?** The helper only maps already-built in-memory audit rows into in-memory attribution rows. It does not write an event ledger, persist records, mutate cluster state, or change recording scope.

## Remaining compressed responsibilities

Without broad scouting, `build_emitter_attribution_audit(...)` still visibly owns high-level orchestration, unknown-attribution row mapping from the already recovered unknown classification artifact, deterministic sorting, and metadata construction. These were not recovered because the current slice was limited to the single Scout 001 candidate and the prompt forbade drifting into those areas.

## District boundary compliance

This slice stays inside the Emitter Attribution Audit district. It does not recover unknown-emitter classification, implementation-evidence collection, reference-category classification, sorting, metadata, summary calculation, JSON serialization, human-readable formatting, diagnostic registration, diagnostic-shape registration, CLI dispatch, Operational Graph behavior, Emitter/Consumer Audit behavior, Consumer Dependency Audit behavior, or Pressure Audit behavior.

## Operational Graph exclusion

Operational Graph remains excluded. The slice does not inspect, modify, or depend on Operational Graph implementation or reports.
