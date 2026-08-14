# Emitter Attribution Audit Slice 004 — Unknown-emitter attribution item construction

## District gate

- Active district verified: **Emitter Attribution Audit**.
- Latest relevant completed slice verified: **`emitter_attribution_audit_slice_003.md`**.
- Latest local district scout verified: **`emitter_attribution_audit_district_scout_002.md`**.
- The local files point to the same district and to Scout 002's single safe candidate: unknown-emitter attribution item construction from recovered attribution artifacts.

## Selected boundary

Recovered exactly one implementation-local ownership boundary: **unknown-emitter attribution item construction from recovered `UnknownEmitterAttribution` artifacts**.

The selected responsibility consumes a completed `UnknownEmitterAttribution` artifact plus base Emitter/Consumer Audit row context and the attributed event, then produces the corresponding `EmitterAttributionItem` row without changing classification decisions.

## Implementation evidence

Before this slice, `build_emitter_attribution_audit(...)` still directly:

- iterated unknown-emitter base rows after known-emitter row construction returned no rows;
- looked up literal references and called `_classify_unknown_emitter_attribution(...)`;
- copied `UnknownEmitterAttribution` fields into an `EmitterAttributionItem`;
- copied base consumers and base emission type;
- combined attribution-evidence locations and supporting-reference locations into the public `evidence` field.

This was implementation-backed row construction, not a classification decision, evidence collection pass, known-emitter row producer, sorting owner, metadata owner, formatter, JSON serializer, CLI surface, or registry change.

## Before

`build_emitter_attribution_audit(...)` owned both high-level orchestration and the unknown-emitter row construction mapping from the completed classification artifact into the final audit item.

## After

`build_emitter_attribution_audit(...)` remains the high-level orchestrator. It still builds the base audit, gathers implementation evidence, delegates known-emitter rows, calls `_classify_unknown_emitter_attribution(...)`, sorts final rows, and builds metadata.

Unknown-emitter row construction is now owned by `_unknown_emitter_attribution_item(...)`, which constructs the final `EmitterAttributionItem` from:

- the base `EmitterConsumerItem`;
- the event being attributed;
- the completed `UnknownEmitterAttribution` artifact.

## Recovered producer

`_unknown_emitter_attribution_item(...)` now produces the unknown-emitter attribution item row.

## Recovered artifact/helper

The recovered boundary is carried by the helper `_unknown_emitter_attribution_item(...)`. It consumes the already-recovered `UnknownEmitterAttribution` artifact and returns an `EmitterAttributionItem`.

## Recovered consumer

`build_emitter_attribution_audit(...)` consumes the produced unknown-emitter attribution item and appends it to the same final item list as before.

## Compatibility preserved

No compatibility boundary changed.

The implementation preserves:

- public Python compatibility for the existing build, JSON, and format functions;
- CLI behavior;
- JSON output shape;
- human-readable output shape;
- summary counts;
- deterministic final sorted output;
- schema;
- diagnostic inventory behavior;
- diagnostic shape-audit behavior;
- read-only behavior;
- event-ledger behavior.

Expected compatibility answer: **No.**

## Files changed

- `seed_runtime/emitter_attribution_audit.py`
- `tests/test_emitter_attribution_audit.py`
- `emitter_attribution_audit_slice_004.md`

## LOC changed

Measured with `git diff --stat` after implementation and tests:

- `seed_runtime/emitter_attribution_audit.py`: 36 changed lines in the final diff.
- `tests/test_emitter_attribution_audit.py`: 109 changed lines in the final diff.
- `emitter_attribution_audit_slice_004.md`: 143 report lines added.

## Tests executed

- `pytest -q tests/test_emitter_attribution_audit.py` — passed.
- `pytest -q tests/test_emitter_attribution_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed.

## Focused test coverage added

Added focused coverage proving that unknown-emitter attribution item construction preserves:

- unknown-emitter row construction;
- event field;
- classified emitter field;
- status from `UnknownEmitterAttribution`;
- reason from `UnknownEmitterAttribution`;
- consumers from the base row;
- combined evidence locations;
- emission type from the base row;
- confidence from `UnknownEmitterAttribution`;
- attribution evidence from `UnknownEmitterAttribution`;
- supporting references from `UnknownEmitterAttribution`;
- public JSON output behavior;
- human-readable output behavior;
- summary counts;
- final sorted output behavior;
- read-only event-ledger behavior.

## Required questions

1. **What responsibility was previously compressed?** Unknown-emitter `EmitterAttributionItem` construction from a completed `UnknownEmitterAttribution` artifact was compressed inside `build_emitter_attribution_audit(...)`.
2. **Which implementation-local ownership boundary became directly observable?** The boundary that maps base unknown-emitter audit row context plus an attributed event plus completed unknown-attribution artifact into the final Emitter Attribution Audit item row.
3. **What producer now owns the recovered responsibility?** `_unknown_emitter_attribution_item(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** The helper `_unknown_emitter_attribution_item(...)`; it consumes `UnknownEmitterAttribution` and returns `EmitterAttributionItem`.
5. **Who consumes it?** `build_emitter_attribution_audit(...)`.
6. **Did any compatibility boundary change?** No.
7. **How does this stay inside the Emitter Attribution Audit district?** It only changes local Emitter Attribution Audit row construction after the base Emitter/Consumer Audit exists and after unknown-emitter classification is complete.
8. **How is this distinct from Emitter Attribution Audit Slice 001 unknown-emitter classification?** Slice 001 owns status, reason, emitter, confidence, attribution evidence, and supporting-reference decisions. This slice only copies those completed decisions into an item row.
9. **How is this distinct from Emitter Attribution Audit Slice 002 implementation-evidence collection?** Slice 002 owns collection of literal references and dynamic construction evidence. This slice does not scan files or modify `_collect_emitter_attribution_implementation_evidence(...)` or `_implementation_evidence(...)`.
10. **How is this distinct from Emitter Attribution Audit Slice 003 known-emitter attributed row construction?** Slice 003 owns rows for base items whose emitter is already known. This slice only handles the unknown-emitter path after classification.
11. **How is this distinct from prior Emitter/Consumer Audit slices?** It does not collect scan results, derive emitted-output relationship status, produce base unknown-emitter rows, produce scanned emitted-item rows, or assemble the base Emitter/Consumer Audit.
12. **How is this distinct from prior Consumer Dependency Audit slices?** It does not produce observation-predicate audit item families, diagnostic audit item families, or matched consumer groups.
13. **How is this distinct from prior Frontier Pressure Admission slices?** It does not admit pressure candidates, select item sets, compute pressure scores, produce pressure evidence payloads, or make positive-finding/refusal decisions.
14. **How does this avoid Operational Graph work?** It does not read, modify, build, or register Operational Graph behavior; the change is confined to Emitter Attribution Audit item construction.
15. **How does this preserve diagnostic inventory and diagnostic-shape visibility?** It adds no diagnostic surface, CLI flag, recordable output, inventory registration, or shape-audit registration and preserves the existing Emitter Attribution Audit surface. The diagnostic inventory and shape-audit tests still pass.
16. **How does this preserve read-only and event-ledger behavior?** The helper is pure row construction from already available inputs and does not write the event ledger or mutate cluster state. Tests prove a build leaves a fresh `EventLedger` unchanged.

## Remaining compressed responsibilities

Without broad scouting, `build_emitter_attribution_audit(...)` still visibly owns high-level orchestration, deterministic sorting, and metadata construction. These were not recovered because this slice was limited to Scout 002's single target and the prompt explicitly forbade sorting, metadata, summary, formatting, JSON, diagnostic registration, and other ownership recovery.

## District boundary compliance

This slice stays inside the Emitter Attribution Audit district. It does not recover unknown-emitter classification, implementation-evidence collection, known-emitter row construction, reference-category classification, sorting, metadata, summary calculation, JSON serialization, human-readable formatting, diagnostic registration, diagnostic-shape registration, CLI dispatch, Operational Graph behavior, Emitter/Consumer Audit behavior, Consumer Dependency Audit behavior, Pressure Audit behavior, or Frontier Pressure Admission behavior.

## Operational Graph exclusion

Operational Graph was not modified, used as authority, or selected as a boundary. The recovered helper is local to `seed_runtime/emitter_attribution_audit.py` and only constructs an Emitter Attribution Audit row.
