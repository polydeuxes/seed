# Emitter/Consumer Audit District Scout 002

## District consistency verification

- Active district verified: **Emitter/Consumer Audit**.
- Latest relevant completed Emitter/Consumer Audit slice verified: **`emitter_consumer_audit_slice_004.md`**.
- Repository-local Emitter/Consumer Audit files present and reviewed:
  - `seed_runtime/emitter_consumer_audit.py`
  - `tests/test_emitter_consumer_audit.py`
  - `emitter_consumer_audit_slice_001.md`
  - `emitter_consumer_audit_slice_002.md`
  - `emitter_consumer_audit_slice_003.md`
  - `emitter_consumer_audit_slice_004.md`
  - `emitter_consumer_audit_district_scout_001.md`
- The available Emitter/Consumer Audit slice chain points to Slice 004 as the latest completed local slice. Nearby Competency Interrogation, DiagnosticSurface, Frontier Pressure Admission, Consumer Dependency Audit, and Pressure Audit reports are present in the repository but were treated as unrelated district material and were not used as authority for this district.
- No district mismatch was found. This scout proceeded inside Emitter/Consumer Audit.

## Scout scope and read-only boundary

This scout was read-only with respect to implementation and tests. It changed no implementation files and no test files. It created only this scout report file: `emitter_consumer_audit_district_scout_002.md`.

This is not a slice report and does not create PR metadata.

## Current app evidence

Commands used as app/repository evidence during scouting:

```text
python scripts/seed_local.py --emitter-consumer-audit --json
python scripts/seed_local.py --diagnostic-inventory
python scripts/seed_local.py --diagnostic-shape-audit --json
rg -n "emitter_consumer|EmitterConsumer|emitter-consumer|Emitter/Consumer" seed_runtime tests *.md --glob '!competency*' --glob '!frontier*' --glob '!consumer_dependency*'
nl -ba seed_runtime/emitter_consumer_audit.py | sed -n '1,420p'
nl -ba tests/test_emitter_consumer_audit.py | sed -n '1,340p'
nl -ba seed_runtime/diagnostic_inventory.py | sed -n '790,815p'
nl -ba seed_runtime/diagnostic_shape_audit.py | sed -n '300,330p'
nl -ba scripts/seed_local.py | rg -n "emitter-consumer|format_emitter_consumer|build_emitter_consumer" -C 3
```

Observed implementation/app facts:

- `build_emitter_consumer_audit(...)` now delegates scan-result collection to `_collect_emitter_consumer_scan_result(...)`, delegates scanned emitted-item row production to `_scanned_emitted_item_rows(...)`, delegates unknown-emitter row production to `_unknown_emitter_rows(...)`, then still performs final item merge/sort and metadata construction before returning `EmitterConsumerAudit`.
- `_scanned_emitted_item_rows(...)` owns scanned-emitter row production from `EmitterConsumerScanResult`. It intentionally keeps visible consumer tuple derivation, relationship-status helper consumption, and evidence aggregation inside the same row-production responsibility.
- `_unknown_emitter_rows(...)` owns rows for consumed outputs with no visible scanned emitter.
- `_derive_emitted_output_relationship_status(...)` owns relationship-status derivation for scanned emitted-output groups.
- `_collect_emitter_consumer_scan_result(...)` owns source scanning, AST parsing, discovery, rendered-string gating, classification, emitter naming, consumer naming, emitted collection, consumed collection, and evidence collection.
- `EmitterConsumerItem.to_json_dict(...)`, `EmitterConsumerAudit.summary`, `EmitterConsumerAudit.to_json_dict(...)`, and `emitter_consumer_audit_json(...)` already own JSON/public shape boundaries.
- `format_emitter_consumer_audit(...)` already owns human-readable Emitter/Consumer Audit output.
- Diagnostic inventory registers `emitter_consumer_audit` with `--emitter-consumer-audit` and `--include-rendered`, repo-file use, JSON support, no record support, `record_scope=none`, `writes_event_ledger=false`, and `mutates_cluster=false`.
- Diagnostic shape audit registers the Emitter/Consumer Audit implementation with module path `seed_runtime/emitter_consumer_audit.py`, build function `build_emitter_consumer_audit`, format function `format_emitter_consumer_audit`, JSON function `emitter_consumer_audit_json`, CLI flags `--emitter-consumer-audit` and `--include-rendered`, and repo markers `SCAN_PATHS` and `_python_files`.
- CLI dispatch builds the audit with `include_rendered`, then prints either `emitter_consumer_audit_json(...)` or `format_emitter_consumer_audit(...)`.

## Recently consumed Emitter/Consumer Audit boundaries treated as unavailable

The following boundaries are already recovered and unavailable for re-slicing:

- Slice 001: scan-result collection via `EmitterConsumerScanResult` and `_collect_emitter_consumer_scan_result(...)`.
- Slice 002: emitted-output relationship-status derivation via `_derive_emitted_output_relationship_status(...)`.
- Slice 003: unknown-emitter row production via `_unknown_emitter_rows(...)`.
- Slice 004: scanned emitted-item row production via `_scanned_emitted_item_rows(...)`.
- Consumer tuple derivation inside scanned emitted-row production.
- Evidence aggregation inside scanned emitted-row production.
- Relationship-status helper consumption inside scanned emitted-row production.

This scout did not re-slice those subparts under new names.

## Prior district boundaries avoided

This scout avoided prior Consumer Dependency Audit boundaries:

- observation-predicate audit item-family production;
- diagnostic audit item-family production;
- matched consumer group construction.

This scout avoided prior Frontier Pressure Admission boundaries:

- pressure-audit candidate admission;
- consumer-predicate source fan-out from pressure-audit;
- orphaned-predicate pressure evidence payload ownership;
- fragile-predicate pressure evidence payload ownership;
- orphaned-predicate pressure score production;
- orphaned-predicate positive-finding refusal;
- fragile-predicate pressure score production;
- fragile-predicate positive-finding refusal;
- orphaned-predicate item-set selection;
- fragile-predicate item-set selection.

This scout also respected stopped and exhausted neighborhoods:

- Slice 035: selection_path_audit neighborhood exhausted.
- Slice 051: immediate diagnostic-shape pressure candidate-construction pocket exhausted.
- District Scout 004: immediate post-Slice-062 pressure-audit neighborhood exhausted for safe local recovery.
- Outward Scout 005: Frontier Pressure Admission pressure-audit district has zero immediate recoverable candidates.
- Consumer Dependency Audit District Scout 003: local consumer dependency audit district has zero immediate recoverable candidates after Slice 003.

## Inspected Emitter/Consumer Audit neighborhoods

### 1. `build_emitter_consumer_audit(...)` final audit assembly

Evidence:

- After all recovered row helpers run, `build_emitter_consumer_audit(...)` still owns the final merge of scanned rows and unknown rows, the public sort key `(status, emitter, emits)`, and the metadata payload containing `discovery`, `include_rendered`, and `scope`.
- This responsibility begins after Slice 004's scanned emitted-item rows are produced and after Slice 003's unknown-emitter rows are produced.
- The responsibility ends at construction of the public `EmitterConsumerAudit` object.

Assessment: **A. Strong implementation-backed next slice**.

This is a narrow remaining implementation-local boundary: final audit assembly from already-produced row collections plus metadata. It has a clear producer/consumer relationship if recovered as a helper: `build_emitter_consumer_audit(...)` would produce/collect row inputs and consume the assembled `EmitterConsumerAudit`, while the helper would own only the existing sort and metadata construction.

### 2. `EmitterConsumerAudit.summary` and JSON serialization

Evidence:

- `EmitterConsumerAudit.summary` already owns summary count derivation from final items.
- `EmitterConsumerAudit.to_json_dict(...)` already owns public JSON object assembly.
- `EmitterConsumerItem.to_json_dict(...)` already owns item JSON shape.
- `emitter_consumer_audit_json(...)` is already a public wrapper around `audit.to_json_dict()`.

Assessment: **C. Already separated / likely re-slice**.

No still-compressed local ownership boundary is visible here. A new slice would likely rename or wrap existing JSON/summary ownership without changing producer/consumer separation.

### 3. Human-readable audit output

Evidence:

- `format_emitter_consumer_audit(...)` already owns the human-readable Emitter/Consumer Audit rendering surface.
- It renders heading/summary lines, an empty-state line, and per-item blocks.
- There is no separate implementation consumer of a per-item rendered block artifact; the function directly produces final human text for CLI dispatch.

Assessment: **D. Cosmetic only**.

A helper for item-block lines or summary-header lines could be named, but current evidence does not show a separate implementation consumer or a compatibility-relevant ownership boundary. The existing formatter is already the public human-output boundary.

### 4. Diagnostic inventory and diagnostic-shape registration

Evidence:

- Diagnostic inventory already registers `emitter_consumer_audit` as read-only, JSON-supported, not recordable, `record_scope=none`, no event-ledger writes, and no cluster mutation.
- Diagnostic shape audit already names the Emitter/Consumer Audit module, build function, format function, JSON function, CLI flags, and repo-file markers.

Assessment: **C. Already separated / likely re-slice**.

The registration surfaces are already owned by their registries and tests. No Emitter/Consumer Audit implementation-local boundary remains here unless the diagnostic surface itself changes, which this scout must not do.

### 5. Operational graph and emitter attribution consumers

Evidence:

- `seed_runtime/operational_graph.py` consumes `build_emitter_consumer_audit(repo_root)` outwardly when constructing operational graph evidence.
- `seed_runtime/emitter_attribution_audit.py` consumes `build_emitter_consumer_audit(...)` outwardly for emitter attribution evidence.

Assessment: **C. Already separated / likely re-slice** for this district; outward evidence only.

These consumers confirm compatibility constraints for the public audit object, but they do not expose an implementation-local Emitter/Consumer Audit boundary after Slice 004. They should not be used to reopen Consumer Dependency Audit, Pressure Audit, Frontier Pressure Admission, or unrelated diagnostic-surface work.

## Candidate boundaries found

### Candidate 1: Final Emitter/Consumer Audit assembly from produced row collections

- Rank: **A. Strong implementation-backed next slice**.
- Classification: **Independent**.
- Confidence: **High**.
- Recoverable boundary: final audit assembly after row production, specifically consuming already-produced scanned rows and unknown rows, preserving the public item sort key, and constructing `EmitterConsumerAudit` metadata.
- Producer/consumer relationship:
  - Existing producers: `_scanned_emitted_item_rows(...)` and `_unknown_emitter_rows(...)` produce row collections.
  - Proposed recovered producer: a narrow final-assembly helper could consume rows and `include_rendered`, then produce the final `EmitterConsumerAudit` with unchanged sorted items and metadata.
  - Existing consumer: `build_emitter_consumer_audit(...)` would consume the assembled audit result as its return value.
- Why exactly one ownership boundary remains compressed: the remaining local work in `build_emitter_consumer_audit(...)` after Slice 004 is not scanning, status derivation, unknown row production, scanned row production, JSON serialization, or human formatting. It is final assembly of public audit state.
- Why it is not a re-slice: it starts after the recovered row-production helpers have returned. It does not re-own scan-result collection, relationship-status derivation, unknown-emitter row production, scanned emitted-item row production, consumer tuple derivation, relationship-status helper consumption, or evidence aggregation.
- Why it is not merely a name: the implementation still performs concrete behavior at this point: extends the row list, applies a public deterministic sort key, and builds metadata fields consumed by JSON/human/CLI/outward callers.
- Compatibility expectation: a helper that returns the same `EmitterConsumerAudit` should preserve behavior, schema, CLI, JSON, diagnostics, event-ledger behavior, and read-only boundaries.
- Valid without other proposed candidates: **Yes**. It stands alone because no other safe candidate is required before final assembly can be recovered.

## Rejected candidates and why

### Candidate 2: Summary count extraction

- Rank: **C. Already separated / likely re-slice**.
- Classification: **Invalid**.
- Confidence: **High**.
- Reason rejected: `EmitterConsumerAudit.summary` already owns summary counts. A new helper would likely wrap already-separated dataclass behavior.
- Why it would be a re-slice: it would re-open existing summary ownership rather than recover a still-compressed boundary.
- Why it is merely a name: no distinct producer/consumer handoff is missing.
- Valid without other candidates: **No**, because it is invalid.

### Candidate 3: Public JSON output shaping

- Rank: **C. Already separated / likely re-slice**.
- Classification: **Invalid**.
- Confidence: **High**.
- Reason rejected: item JSON, audit JSON, and the public JSON wrapper are already separated.
- Why it would be a re-slice: it would rename existing `to_json_dict(...)` ownership.
- Why it is merely a name: no still-compressed local responsibility remains between audit object and JSON output.
- Valid without other candidates: **No**, because it is invalid.

### Candidate 4: Human per-item rendering helper

- Rank: **D. Cosmetic only**.
- Classification: **Invalid**.
- Confidence: **Medium**.
- Reason rejected: `format_emitter_consumer_audit(...)` already owns human-readable output. Although per-item block rendering is visible as repeated line assembly, the repository evidence does not show a separate consumer of a per-item line artifact or a compatibility-driven ownership boundary.
- Why it would risk a re-slice: it could re-slice the existing formatter's public formatting authority.
- Why it is merely a name: absent a distinct produced artifact consumed elsewhere, a helper would mostly rename line-list construction.
- Valid without other candidates: **No**, because it is invalid.

### Candidate 5: Diagnostic inventory or shape-registration row for Emitter/Consumer Audit

- Rank: **C. Already separated / likely re-slice**.
- Classification: **Invalid**.
- Confidence: **High**.
- Reason rejected: registration is already represented in `diagnostic_inventory.py` and `diagnostic_shape_audit.py`. This scout does not add or modify a diagnostic surface, audit, probe, view, CLI flag, or recordable output.
- Why it would risk a re-slice: it would reopen diagnostic inventory/shape registry ownership rather than an Emitter/Consumer Audit implementation-local responsibility.
- Why it is merely a name: no current missing registration or shape-audit gap was observed.
- Valid without other candidates: **No**, because it is invalid.

## Candidate independence classification summary

How many recoverable candidates currently exist?

```text
1
```

For each candidate:

1. Final Emitter/Consumer Audit assembly from produced row collections
   - Classification: **Independent**
   - Confidence: **High**
   - Why it is not a re-slice: it operates after scan-result collection, relationship-status derivation, scanned row production, and unknown row production have already completed.
   - Why it is not merely a name: it preserves concrete final behavior: row merge, deterministic public ordering, and metadata construction.
   - Would still be valid if other proposed candidates were not recovered: **Yes**.

No second or third implementation-backed recoverable candidate is currently safe. The other nearby neighborhoods are already separated, likely re-slices, cosmetic, or outward-only evidence.

## Batch Efficiency Gate

- Discovered queue: **Single-slice target**.
- Recoverable candidates: **1**.
- Recommended batch size: **1**.
- Efficiency batch? **No**. Three recoverable candidates do not exist.
- Protection batch? **No**. Two recoverable candidates do not exist.
- Single-slice target? **Yes**. Only final Emitter/Consumer Audit assembly is safe.
- Stop/move-out? **Not yet**. One nearby implementation-backed slice candidate remains.
- Different-district handoff? **No**. Stay in Emitter/Consumer Audit for one guarded slice, then reassess.

Running a batch is not worth it for speed or process protection because only one safe candidate is currently implementation-backed. A batch would increase re-slicing risk by pulling in already-separated summary/JSON/formatting/registration work.

## Recommended next command

Perform one guarded Emitter/Consumer Audit slice recovering **final audit assembly from produced row collections**.

The slice should preserve behavior exactly:

- keep `_collect_emitter_consumer_scan_result(...)` as scan-result owner;
- keep `_scanned_emitted_item_rows(...)` as scanned row owner;
- keep `_unknown_emitter_rows(...)` as unknown row owner;
- keep `_derive_emitted_output_relationship_status(...)` as status owner;
- do not extract consumer tuple derivation, relationship-status helper consumption, or evidence aggregation from `_scanned_emitted_item_rows(...)`;
- preserve sorted item order, metadata fields, public JSON shape, human-readable output, diagnostic inventory registration, diagnostic-shape registration, event-ledger behavior, and `mutates_cluster=false` read-only behavior.

Suggested tests for that future slice should remain focused in `tests/test_emitter_consumer_audit.py` and prove final sorted items and metadata remain unchanged. Because the future slice would not add or modify a diagnostic surface, audit, probe, view, operational CLI flag, or recordable output, diagnostic inventory and shape-audit tests should only be needed if implementation evidence changes those surfaces.

## Risk of re-slicing prior work

Risk is **medium** if the next command tries to batch or names helpers before proving boundaries. The most likely re-slice traps are:

- extracting consumer tuple derivation from `_scanned_emitted_item_rows(...)` despite Slice 004 intentionally keeping it there;
- extracting evidence aggregation from `_scanned_emitted_item_rows(...)` despite Slice 004 intentionally keeping it there;
- reopening relationship-status helper consumption inside scanned emitted-row production;
- wrapping `EmitterConsumerAudit.summary` or JSON serialization even though those are already separated;
- splitting human formatting without a distinct implementation consumer;
- touching diagnostic inventory or diagnostic-shape registration without adding/modifying a diagnostic surface.

Risk is **low** if the next command recovers only final audit assembly after the existing row helpers and preserves all public outputs.

## Implementation/test change statement

No implementation files were changed. No test files were changed. No slice report was created. No PR metadata was created. The only repository change is this scout report markdown file.

## Scout report commit hash

Scout report commit hash: to be recorded by the committing agent after the report file is committed; the final response for this command must report the actual commit hash from git history.
