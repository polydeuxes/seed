# Consumer Dependency Audit District Scout 003

## Scout scope and read-only statement

This scout reassessed the current Consumer Dependency Audit district after Consumer Dependency Audit Slice 003. It was read-only with respect to implementation and tests: no implementation files were changed, no test files were changed, and no slice report was created. The only intended repository change is this scout report: `consumer_dependency_audit_district_scout_003.md`.

Commit hash for this scout report commit: `b372aa5656ec0d0f5a8f28f43238fbaab32255be`.

## Commands and current app evidence

Commands used during the scout:

- `pwd && rg --files -g 'AGENTS.md' -g '!*.pyc' -g '!__pycache__' | xargs -r -I{} sh -c 'echo --- {}; cat {}' && git status --short`
- `rg -n "consumer_dependency|consumer-audit|ConsumerAudit|_audit_item|_matched_consumer_groups|_consumer_lookup_terms|_mentions_any_item|_read_sources|def _read\(" -S .`
- `sed -n '1,360p' seed_runtime/consumer_dependency_audit.py`
- `sed -n '1,360p' tests/test_consumer_dependency_audit.py`
- `sed -n '1425,1465p;2545,2580p;2720,2775p' scripts/seed_local.py`
- `sed -n '360,520p' tests/test_consumer_dependency_audit.py`
- `rg -n "consumer_audit|build_consumer_audit|consumer_audit_json|format_consumer_audit" scripts/seed_local.py seed_runtime tests -S`
- `sed -n '7588,7612p' scripts/seed_local.py`
- `python scripts/seed_local.py --consumer-audit --json | python -m json.tool | head -160`
- `python scripts/seed_local.py --consumer-audit --predicate filesystem_avail_bytes --json | python -m json.tool`
- `python scripts/seed_local.py --consumer-audit --diagnostic ownership_discrepancies --json | python -m json.tool`
- `nl -ba seed_runtime/consumer_dependency_audit.py | sed -n '1,260p'`
- `nl -ba tests/test_consumer_dependency_audit.py | sed -n '95,245p'`
- `nl -ba scripts/seed_local.py | sed -n '1435,1450p;2550,2568p;7600,7610p'`
- `nl -ba seed_runtime/consumer_dependency_audit.py | sed -n '260,275p'`
- `nl -ba tests/test_consumer_dependency_audit.py | sed -n '245,430p'`

Current app evidence from `python scripts/seed_local.py --consumer-audit --json | python -m json.tool | head -160`:

- The public JSON envelope still contains `items`, `metadata`, and `summary`.
- Rows are sorted by public kind/item order: the first visible rows are diagnostic rows beginning with `architecture_conformance_audit`, `audit_compare`, `audit_snapshot`, and `audit_snapshots`.
- Item rows expose `item`, `kind`, `consumers`, `consumer_count`, `orphaned`, and `highlight`.
- The default run is read-only from this command path; no record flag is involved.

Current focused diagnostic-filter evidence from `python scripts/seed_local.py --consumer-audit --diagnostic ownership_discrepancies --json | python -m json.tool`:

- Exactly one item is emitted: `ownership_discrepancies` with `kind` `diagnostic`.
- The item has consumers `diagnostics`, `state_build`, and `views`, `consumer_count` `3`, `highlight` `widely used`, and `orphaned` `false`.
- Metadata remains the same discovery/evidence envelope used by the unfiltered audit.

Current focused predicate-filter evidence from `python scripts/seed_local.py --consumer-audit --predicate filesystem_avail_bytes --json | python -m json.tool`:

- In the current repository state this exact filter emitted zero items. That means this scout did not use that predicate output as candidate evidence.
- Existing tests still document the intended fixture/storage predicate behavior, but a scout candidate must rely on current implementation boundaries rather than this absent app row.

## Recently consumed Consumer Dependency Audit boundaries respected

These boundaries are treated as already recovered and unavailable:

1. Observation-predicate audit item-family production via `_observation_predicate_audit_items(...)`.
2. Diagnostic audit item-family production via `_diagnostic_audit_items(...)`.
3. Matched consumer group construction via `_matched_consumer_groups(...)`.

No candidate below reclaims those responsibilities under a new name.

## Prior Frontier Pressure Admission boundaries avoided

The scout avoided pressure-audit fan-out and pressure candidate work, including:

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

Especially, nothing here re-slices Slice 037. Slice 037 recovered pressure-audit's use of one consumer audit and fan-out into pressure candidates. This scout inspected only the consumer dependency audit surface and rejected any move that would depend on `seed_runtime/pressure_audit.py`.

## Stopped and exhausted neighborhoods respected

The scout respected the stopped/exhausted neighborhoods:

- Slice 035: `selection_path_audit` neighborhood exhausted.
- Slice 051: immediate diagnostic-shape pressure candidate-construction pocket exhausted.
- District Scout 004: immediate post-Slice-062 pressure-audit neighborhood exhausted for safe local recovery.
- Outward Scout 005: Frontier Pressure Admission pressure-audit district has zero immediate recoverable candidates.

No proposed work touches those neighborhoods.

## Implementation evidence baseline

The current consumer dependency audit implementation already has narrow helpers for the previously recovered or existing responsibilities:

- `build_consumer_audit(...)` reads sources once, conditionally invokes observation-predicate item-family production when no diagnostic filter is present, conditionally invokes diagnostic item-family production when no predicate filter is present, sorts final rows by `(kind, item)`, and constructs metadata.
- `_observation_predicate_audit_items(...)` owns observation-predicate row production and delegates per item to `_audit_item(...)`.
- `_diagnostic_audit_items(...)` owns diagnostic row production and filtering, then delegates per item to `_audit_item(...)`.
- `_audit_item(...)` now only composes lookup terms, matched groups, and `ConsumerAuditItem` construction.
- `_matched_consumer_groups(...)` owns group-order-preserving source matching.
- `_read_sources(...)` and `_read(...)` own consumer source file loading.
- `_consumer_lookup_terms(...)` owns canonical lookup-term expansion from `predicate_catalog/core.json`.
- `_mentions_any_item(...)` owns low-level string-form expansion and membership checks.
- `ConsumerAuditItem` owns per-item derived fields and per-item JSON.
- `ConsumerAudit` owns summary calculation and top-level JSON envelope.
- `format_consumer_audit(...)` owns human-readable output.
- `scripts/seed_local.py` owns CLI flag declaration, validation, dispatch, and JSON/human formatter selection.

## Inspected consumer-audit neighborhoods

### 1. `_audit_item(...)` after Slice 003

Evidence:

- `_audit_item(...)` obtains aliases from `_consumer_lookup_terms(...)`, obtains consumers from `_matched_consumer_groups(...)`, and returns `ConsumerAuditItem(item=item, kind=kind, consumers=consumers)`.
- `_matched_consumer_groups(...)` is already a helper and is directly tested for ordered exact matches and orphan behavior.
- Tests also prove `_audit_item(...)` delegates lookup terms and low-level mention matching while preserving public JSON order and no event-ledger write.

Assessment: **Already separated / likely re-slice (Rank C).**

There is no longer an implementation-local ownership boundary compressed inside `_audit_item(...)`. Extracting the remaining three-line composition would only rename orchestration between already recovered helpers and the dataclass constructor. It would likely re-slice Slice 003 or existing `_consumer_lookup_terms(...)` / `_mentions_any_item(...)` responsibilities.

### 2. Final audit item sorting in `build_consumer_audit(...)`

Evidence:

- `build_consumer_audit(...)` combines item families and returns `ConsumerAudit(items=tuple(sorted(items, key=lambda item: (item.kind, item.item))), metadata=...)`.
- Tests for observation-predicate item production verify producer-local order before the final audit sort and then verify final audit rows sort by `(kind, item)`.
- The public app output also demonstrates the sorted public row order.

Assessment: **Cosmetic only (Rank D).**

Sorting is behaviorally important, but it is a single compatibility-preserving expression at the assembly point. There is no recurring producer/consumer handoff, no second consumer of a sorted item set, and no independent owner beyond final audit assembly. Extracting `_sorted_consumer_audit_items(...)` would be a name-first refactor unless future implementation evidence introduces another sorted-row consumer.

### 3. Metadata construction in `build_consumer_audit(...)`

Evidence:

- Metadata is built inline with `discovery` and `consumer_evidence`, where `consumer_evidence` derives directly from `CONSUMER_PATHS`.
- `CONSUMER_PATHS` already owns the source groups that `_read_sources(...)` consumes.
- The app output shows metadata as a public JSON field, but no separate metadata consumer or alternate metadata producer is present.

Assessment: **Cosmetic only (Rank D).**

The metadata is public and useful, but this scout found no implementation-backed local ownership boundary distinct from source declaration and top-level JSON assembly. Pulling it out now would merely name an inline literal/comprehension pair. It would preserve behavior, but it would not recover a compressed responsibility.

### 4. `ConsumerAuditItem`, `ConsumerAudit`, public JSON, and human output

Evidence:

- `ConsumerAuditItem` owns `consumer_count`, `orphaned`, `highlight`, and `to_json_dict()`.
- `ConsumerAudit` owns summary and top-level `to_json_dict()`.
- `consumer_audit_json(...)` is a one-line adapter to `audit.to_json_dict()`.
- `format_consumer_audit(...)` owns human-readable rendering, including empty-output behavior.
- Tests cover JSON fields, human output, derived counts, orphan highlighting, and no event-ledger creation.

Assessment: **Already separated / likely re-slice (Rank C) for the dataclass JSON/summary owners; Cosmetic only (Rank D) for the one-line JSON adapter and formatter sub-pieces.**

The implementation already places per-item derived/public shape on `ConsumerAuditItem`, top-level summary/envelope shape on `ConsumerAudit`, and human presentation in `format_consumer_audit(...)`. Splitting count computation, highlight labels, consumer line rendering, or empty-output rendering would be presentation cleanup. It would not expose a new implementation-backed ownership boundary and could destabilize public schema without a real owner.

### 5. CLI filter behavior and source reading

Evidence:

- `scripts/seed_local.py` declares `--consumer-audit` and describes it as implementation-backed consumer auditing.
- CLI validation permits `--predicate` with `--consumer-audit` and permits `--diagnostic` with `--consumer-audit`.
- CLI dispatch passes those filters to `build_consumer_audit(...)` and chooses JSON or human formatting.
- `_read_sources(...)` maps `CONSUMER_PATHS` to file content via `_read(...)`; `_read(...)` is the missing-file tolerant text reader.
- Tests cover diagnostic filtering, empty predicate behavior, and source/consumer matching with fixture files.

Assessment: **Already separated / likely re-slice (Rank C) for source reading; Cosmetic only (Rank D) for CLI dispatch/filter extraction inside this district.**

Source reading is already a helper pair with a clear declaration-to-read relationship. CLI filtering is real public behavior, but its ownership lives in CLI argument validation/dispatch and existing item-family producers, not in a still-compressed consumer-audit implementation boundary. A consumer-audit slice that extracts CLI dispatch would cross from the audit implementation into app shell plumbing and would not be a district-local ownership recovery.

## Candidate boundaries found

How many recoverable candidates currently exist?

**0**

This scout found no nearby implementation-backed slice candidate after Slice 003. Fewer than three implementation-backed candidates are supported; in fact, no candidate meets the independence standard.

| Rank | Candidate / neighborhood | Classification | Confidence | Would it still be valid without others? | Why it is not a re-slice | Why it is not merely a name | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C | `_audit_item(...)` residual composition | Invalid | High | No | It would re-slice Slice 003 matched group construction or existing lookup/mention helpers. | The remaining operation only wires existing helpers into `ConsumerAuditItem`. | Reject. |
| D | Final item sorting | Invalid | Medium-High | No | It does not re-slice consumed item-family helpers, but it only sits at final assembly. | No recurring consumer or separate producer supports it beyond a single `sorted(...)` expression. | Reject. |
| D | Metadata construction | Invalid | Medium-High | No | It does not re-slice item production, but it overlaps source declaration evidence already owned by `CONSUMER_PATHS`. | Public field names alone are not enough; no separate metadata owner/consumer exists. | Reject. |
| C/D | JSON and human output shape | Invalid | High | No | Per-item/top-level JSON and human rendering are already separated into dataclass methods and formatter. | Splitting labels, counts, or lines would be presentation naming, not ownership recovery. | Reject. |
| C/D | CLI filter dispatch and source reading | Invalid | High for source reading; Medium for CLI dispatch | No | Source reading helpers already exist; CLI dispatch is outside a local audit ownership boundary. | The behavior is public, but the compressed responsibility is not in the district implementation. | Reject. |

## Candidate independence classification

No recoverable candidates exist, so there are no Independent or Sequential candidates to queue.

For each rejected candidate:

- `_audit_item(...)` residual composition: **Invalid**, confidence **High**. It would not be valid without the already recovered Slice 003 boundary because it is now only helper composition. It is a re-slice risk and not a real new owner.
- Final item sorting: **Invalid**, confidence **Medium-High**. It would not be valid without other changes because it has no standalone producer/consumer recurrence. It is not a re-slice of prior item-family slices, but it is merely a name for one assembly expression.
- Metadata construction: **Invalid**, confidence **Medium-High**. It would not be valid without a future separate metadata consumer. It is not a direct re-slice, but current evidence is only a public field and a comprehension over `CONSUMER_PATHS`.
- JSON and human output shape: **Invalid**, confidence **High**. It would not be valid without changing presentation responsibilities. It risks re-slicing existing dataclass/formatter owners and is mostly presentation vocabulary.
- CLI filter dispatch and source reading: **Invalid**, confidence **High** for source reading and **Medium** for CLI dispatch. It would not be valid as a Consumer Dependency Audit district slice because source reading is already separated and CLI ownership is app-shell behavior.

## Batch efficiency gate

Discovered queue: **Stop/move-out**.

- Efficiency batch? **No.** Three recoverable candidates do not exist.
- Protection batch? **No.** Two recoverable candidates do not exist.
- Single-slice target? **No.** One implementation-backed slice candidate is not safe.
- Stop/move-out? **Yes.** No nearby implementation-backed slice candidate remains after Slice 003.

Recommended batch size: **0**.

Running a batch is not worth it for speed or process protection. A batch would create pressure to name cosmetic extractions and would increase the risk of re-slicing already recovered Consumer Dependency Audit or Frontier Pressure Admission work.

## Recommended next command

Recommended next command: **stop report or move outward to another district; do not run another local Consumer Dependency Audit slice from the inspected neighborhoods.**

Suggested prompt shape for the next command if work continues:

> Produce a stop report for the Consumer Dependency Audit district after Slice 003, or perform an outward scout from the current app pressure/visibility evidence to identify a different district. Do not re-slice observation-predicate item production, diagnostic item production, matched consumer group construction, lookup terms, mention matching, source reading, JSON formatting, human formatting, or pressure-audit fan-out.

Next move classification: **Stop/move-out**.

Different-district handoff: **Allowed only after a fresh outward scout.** This scout does not nominate a specific different district because the requested scope was the nearby Consumer Dependency Audit district.

## Risk of re-slicing prior work

Risk is **high** if another local Consumer Dependency Audit command proceeds without new implementation evidence. The nearby code is now mostly composed of explicit helpers and dataclass/formatter owners. The tempting names left in the district map directly onto already recovered or already separated responsibilities:

- `_observation_predicate_audit_items(...)`: consumed Slice 001.
- `_diagnostic_audit_items(...)`: consumed Slice 002.
- `_matched_consumer_groups(...)`: consumed Slice 003.
- `_consumer_lookup_terms(...)`: existing lookup-term helper.
- `_mentions_any_item(...)`: existing low-level mention helper.
- `_read_sources(...)` and `_read(...)`: existing source-loading helpers.
- `ConsumerAuditItem` and `ConsumerAudit`: existing schema/derived-field owners.
- `format_consumer_audit(...)` and `consumer_audit_json(...)`: existing presentation/adapter surfaces.
- CLI filter behavior: public app-shell behavior, not a newly compressed local consumer-audit ownership boundary.

## Final scout result

Rank: **E. Stop**.

No implementation or test files were changed. Only `consumer_dependency_audit_district_scout_003.md` was created and committed.
