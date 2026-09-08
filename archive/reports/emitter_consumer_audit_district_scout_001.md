# Emitter/Consumer Audit District Scout 001

## Scout scope

This scout reviewed the current Emitter/Consumer Audit district after Slice 003. It was read-only with respect to implementation and tests: no implementation files and no test files were intentionally changed. The only deliverable file for this scout is this report.

Recently consumed Emitter/Consumer Audit boundaries treated as unavailable:

- Slice 001: scan-result collection via `EmitterConsumerScanResult` and `_collect_emitter_consumer_scan_result(...)`.
- Slice 002: emitted-output relationship-status derivation via `_derive_emitted_output_relationship_status(...)`.
- Slice 003: unknown-emitter row production via `_unknown_emitter_rows(...)`.

Prior stopped/exhausted neighborhoods respected:

- Slice 035: `selection_path_audit` neighborhood exhausted.
- Slice 051: immediate diagnostic-shape pressure candidate-construction pocket exhausted.
- District Scout 004: immediate post-Slice-062 pressure-audit neighborhood exhausted for safe local recovery.
- Outward Scout 005: Frontier Pressure Admission pressure-audit district has zero immediate recoverable candidates.
- Consumer Dependency Audit District Scout 003: local consumer dependency audit district has zero immediate recoverable candidates after Slice 003.

Prior Consumer Dependency Audit boundaries avoided:

- observation-predicate audit item-family production;
- diagnostic audit item-family production;
- matched consumer group construction.

Prior Frontier Pressure Admission boundaries avoided:

- pressure-audit candidate admission;
- consumer-predicate source fan-out from pressure-audit;
- orphaned/fragile-predicate pressure evidence payload ownership;
- orphaned/fragile-predicate pressure score production;
- orphaned/fragile-predicate positive-finding refusal;
- orphaned/fragile-predicate item-set selection.

## Current app evidence

Commands used for the scout:

```bash
python scripts/seed_local.py --emitter-consumer-audit --json
python scripts/seed_local.py --diagnostic-inventory
python scripts/seed_local.py --diagnostic-shape-audit --json
rg -n "emitter_consumer|EmitterConsumer|build_emitter_consumer|unknown_emitter|relationship_status" -S .
sed -n '1,390p' seed_runtime/emitter_consumer_audit.py
sed -n '7608,7624p' scripts/seed_local.py
sed -n '155,188p' seed_runtime/operational_graph.py
```

Observed current app output from `python scripts/seed_local.py --emitter-consumer-audit --json`:

- Summary: `items_scanned=25`, `consumed=9`, `orphaned=1`, `partially_consumed=3`, `unknown=12`.
- Metadata: discovery is an AST scan of event-ledger append literals, `Event(...)` kind literals, and `event.kind` comparisons; rendered strings are excluded unless `include_rendered` is true; scope is `seed_runtime` and `scripts`.
- Example rows show public schema fields `emitter`, `emits`, `consumers`, `status`, `evidence`, and `emission_type`.

Diagnostic visibility evidence:

- `python scripts/seed_local.py --diagnostic-inventory` reports `emitter_consumer_audit` as `--emitter-consumer-audit, --include-rendered`, using repo files, JSON-supported, not recordable, `record_scope=none`, not writing event-ledger facts, and not mutating the cluster.
- `scripts/seed_local.py` dispatches `--emitter-consumer-audit` by building the audit with `include_rendered`, then printing either JSON through `emitter_consumer_audit_json(...)` or human text through `format_emitter_consumer_audit(...)`.
- `operational_graph` consumes completed audit items as outward evidence by turning item evidence into `emits` edges and item consumers into `consumes` edges.

## Inspected neighborhoods

### 1. `build_emitter_consumer_audit(...)` emitted scanned-item construction

Implementation evidence:

- `build_emitter_consumer_audit(...)` consumes the scan result, then still directly owns the loop over `(emitter, emission_type)` emitted groups.
- Inside that loop it derives the visible consumer tuple from `consumed`, delegates status to `_derive_emitted_output_relationship_status(...)`, aggregates evidence from `evidence`, constructs `EmitterConsumerItem`, and appends it to the item list.
- This is distinct from Slice 001 because scan-result collection is already complete before this loop.
- This is distinct from Slice 002 because status derivation is already delegated and the remaining responsibility is row construction around that status.
- This is distinct from Slice 003 because unknown-emitter rows are already delegated after the emitted scanned-item loop.

Assessment: **A. Strong implementation-backed next slice**.

### 2. Emitted item consumer tuple derivation inside scanned-item construction

Implementation evidence:

- The visible consumer tuple for scanned emitted groups is still produced inline by a nested set comprehension over `outputs` and `consumed.get((output, emission_type), set())`.
- This has direct implementation evidence, but it is nested inside the broader emitted scanned-item row construction responsibility.

Assessment: **B. Possible but needs caution**.

This should not be recovered as a separate batch candidate before the broader emitted scanned-item row boundary is reassessed. If extracted independently, it risks becoming a micro-slice inside the same row-production boundary rather than an independently owned ownership artifact.

### 3. Emitted item evidence tuple aggregation inside scanned-item construction

Implementation evidence:

- The evidence tuple for scanned emitted groups is still produced inline by sorting all source locations for each output from the scan-result evidence mapping.
- The evidence is consumed by public JSON, human-visible item structure, and outward `operational_graph` edges.

Assessment: **B. Possible but needs caution**.

This is implementation-backed, but it is currently inseparable from scanned emitted-row construction without creating a too-small evidence-formatting helper. It should be reassessed only after an emitted scanned-item row producer exists.

### 4. Source discovery, discovered string classification, and emitter/consumer naming helpers

Implementation evidence:

- `_python_files(...)` already owns scan-path file discovery.
- `_discover_file(...)` already owns AST-walk discovery of emit/consume visitor items.
- `_event_emit_literal(...)`, `_event_consume_literals(...)`, `_is_event_ledger_append(...)`, `_is_render_append(...)`, `classify_emission_string(...)`, `_emitter_name(...)`, and `_consumer_name(...)` are already explicit helpers.
- Slice 001 already made `_collect_emitter_consumer_scan_result(...)` the owner of scan-result collection and the consumer of these helper outputs.

Assessment: **C. Already separated / likely re-slice**.

### 5. Public JSON, human-readable output, diagnostic registration, and operational graph consumers

Implementation evidence:

- `EmitterConsumerItem.to_json_dict(...)`, `EmitterConsumerAudit.to_json_dict(...)`, `emitter_consumer_audit_json(...)`, and `format_emitter_consumer_audit(...)` already provide public shape and formatting boundaries.
- Diagnostic inventory and diagnostic-shape registration already expose the read-only surface.
- `operational_graph` only consumes completed audit items as outward evidence.

Assessment: **C. Already separated / likely re-slice** for local Emitter/Consumer Audit; **move-out evidence only** if the local district becomes exhausted.

## Candidate boundary queue

How many recoverable candidates currently exist? **1**.

### Candidate 1: scanned emitted-item row production

- Rank: **A. Strong implementation-backed next slice**.
- Classification: **Independent**.
- Confidence: **High**.
- Recoverable boundary: a helper such as `_emitted_output_rows(...)` could own production of `EmitterConsumerItem` rows for scanned emitted groups.
- Producer/consumer relationship: the proposed helper would consume `scan_result.emitted`, `scan_result.consumed`, and `scan_result.evidence`; it would produce scanned-emitter `EmitterConsumerItem` rows; `build_emitter_consumer_audit(...)` would consume those rows and continue appending `_unknown_emitter_rows(...)` before final sorting and metadata construction.
- Why this is not a re-slice: it does not reclaim scan-result collection, status derivation, or unknown-emitter row production. It starts after `_collect_emitter_consumer_scan_result(...)`, uses `_derive_emitted_output_relationship_status(...)`, and remains separate from `_unknown_emitter_rows(...)`.
- Why this is not merely a name: the implementation currently has a concrete compressed row-production loop that combines consumer tuple derivation, status consumption, evidence tuple aggregation, `EmitterConsumerItem` construction, and append behavior for scanned emitters.
- Compatibility expectation: recovery should preserve schema, CLI behavior, JSON output, text output, diagnostic inventory/shape behavior, event-ledger behavior, and read-only boundaries if the helper returns the same rows and `build_emitter_consumer_audit(...)` keeps the same final sorting and metadata.
- Valid without other proposed candidates? **Yes**. It stands independently because it can be extracted without changing source discovery, scan collection, status derivation, unknown rows, public formatting, diagnostic registration, or operational graph consumers.

### Candidate 2: scanned emitted-item consumer tuple derivation

- Rank: **B. Possible but needs caution**.
- Classification: **Sequential**.
- Confidence: **Medium**.
- Recoverable boundary: derivation of sorted consumer names for a scanned emitted group from outputs, emission type, and consumed mapping.
- Why this is not currently a safe independent slice: it is part of the broader scanned emitted-item row production loop. Extracting this first could produce a very small helper without a durable ownership artifact.
- Why this is not merely a name: the nested comprehension is concrete implementation behavior, but its ownership is probably subordinate to row production.
- Valid without Candidate 1? **No**. Reassess only after Candidate 1 lands or is rejected.

### Candidate 3: scanned emitted-item evidence tuple aggregation

- Rank: **B. Possible but needs caution**.
- Classification: **Sequential**.
- Confidence: **Medium-Low**.
- Recoverable boundary: aggregation of sorted source evidence strings for scanned emitted rows.
- Why this is not currently a safe independent slice: it is public and operationally consumed, but it remains tightly coupled to the scanned emitted-item row construction boundary.
- Why this is not merely a name: current implementation directly aggregates evidence from `evidence.get((emitter, output), set())`, and operational graph consumes item evidence as direct emission evidence; however, that support is not enough to justify a separate immediate slice before row production is separated.
- Valid without Candidate 1? **No**. Reassess only after Candidate 1 lands or is rejected.

## Rejected candidates

- Scan-result collection: rejected as already recovered by Slice 001.
- Emitted-output relationship-status derivation: rejected as already recovered by Slice 002.
- Unknown-emitter row production: rejected as already recovered by Slice 003.
- Source file discovery: rejected as already owned by `_python_files(...)` and consumed through `_collect_emitter_consumer_scan_result(...)`.
- AST discovered item production: rejected as already owned by `_discover_file(...)` and literal helper functions.
- Discovered string classification: rejected as already owned by `classify_emission_string(...)`.
- Emitter naming and consumer group naming: rejected as already owned by `_emitter_name(...)` and `_consumer_name(...)`.
- Public JSON output: rejected as already owned by dataclass `to_json_dict(...)` methods and `emitter_consumer_audit_json(...)`.
- Human-readable output: rejected as already owned by `format_emitter_consumer_audit(...)`.
- Diagnostic inventory and shape registration: rejected because the surface is already registered and no new diagnostic, CLI flag, recordable output, or shape is being proposed by this scout.
- Operational graph consumers: rejected for local recovery; they are outward evidence only and should not be used to re-slice Emitter/Consumer Audit internals.

## Batch efficiency gate

- Recoverable candidates currently safe: **1**.
- Queue classification: **Single-slice target**.
- Recommended next command: perform one guarded Emitter/Consumer Audit slice for scanned emitted-item row production.
- Recommended batch size: **1**.
- Efficiency batch? **No**. Three safe recoverable candidates do not exist.
- Protection batch? **No**. Only one safe candidate exists. Running a batch is not worth it for speed or process protection because the remaining possible boundaries are sequential and need reassessment after the first slice.
- Stop/move-out? **Not yet**. One local implementation-backed slice remains. If that slice lands and no new local compression appears, the next scout should consider stopping or moving outward.
- Different-district handoff? **Not recommended now**. Local Emitter/Consumer Audit still has one strong implementation-backed boundary.

## Risk of re-slicing prior work

Risk is **medium** if the next command targets consumer tuple derivation, evidence aggregation, source scanning, classification, naming helpers, public formatting, diagnostic registration, or operational graph consumption before separating scanned emitted-item row production. Risk is **low** if the next command stays narrowly on scanned emitted-item row production and preserves existing helpers from Slices 001 through 003.

## Read-only statement

No implementation files were changed. No test files were changed. This scout created only `emitter_consumer_audit_district_scout_001.md`.

## Scout report commit

Commit hash: 2843430c81f5713de94864b9726a4c346a2d2144
