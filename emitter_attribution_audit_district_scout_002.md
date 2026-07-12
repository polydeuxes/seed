# Emitter Attribution Audit District Scout 002

## District consistency verification

- Active district verified: **Emitter Attribution Audit**.
- Latest relevant completed slice verified: **`emitter_attribution_audit_slice_003.md`**.
- Latest local district scout verified: **`emitter_attribution_audit_district_scout_001.md`**.
- Branch state and local files did not point to a different active district during this scout.
- Unrelated district reports were ignored as authority. They were used only as explicit boundary constraints where the prompt named them.
- Repository authority was treated as decisive over prior scout evidence.

## Current app evidence

Read-only commands run from the repository root:

- `python scripts/seed_local.py --emitter-attribution-audit --json`
  - Summary observed: `items_scanned=41`, `attributed=34`, `dynamic=3`, `indirect=0`, `discovery_gap=4`, `missing=0`, `unknown=0`.
  - Metadata observed: `include_rendered=false`, scope `seed_runtime` and `scripts`, and discovery text describing refinement of Emitter/Consumer Audit rows with AST literal references, dynamic Event/append calls, and workflow-prefix visibility hints.
  - First JSON item observed an attributed action-plan event with direct-emitter attribution evidence, confidence `high`, domain emission type, and supporting evidence locations.
- `python scripts/seed_local.py --diagnostic-inventory --json`
  - Used as visibility context for the existing registered surface. The Emitter Attribution Audit remains a diagnostic/audit CLI surface and this scout made no registry change.
- `python scripts/seed_local.py --diagnostic-shape-audit --json`
  - Used as visibility context for existing shape coverage. The Emitter Attribution Audit remains registered with its build, format, JSON, and CLI implementation shape and this scout made no shape-audit change.

Implementation evidence inspected:

- `build_emitter_attribution_audit(...)` now delegates known-emitter attributed row construction to `_known_emitter_attributed_rows(...)`, consumes implementation evidence, maps unknown-emitter classification artifacts into `EmitterAttributionItem` rows, sorts final rows, and constructs metadata.
- `UnknownEmitterAttribution` and `_classify_unknown_emitter_attribution(...)` are already recovered by Slice 001 and remain classification owners, not new slice targets.
- `EmitterAttributionImplementationEvidence`, `_collect_emitter_attribution_implementation_evidence(...)`, and `_implementation_evidence(...)` are already recovered by Slice 002 and remain implementation-evidence owners, not new slice targets.
- `_known_emitter_attributed_rows(...)` is already recovered by Slice 003 and is unavailable.
- `_unknown_attribution(...)` is only a compatibility wrapper over `_classify_unknown_emitter_attribution(...)`.
- `EmitterAttributionItem.to_json_dict(...)`, `EmitterAttributionAudit.summary`, `EmitterAttributionAudit.to_json_dict(...)`, `emitter_attribution_audit_json(...)`, and `format_emitter_attribution_audit(...)` are already separated public schema/presentation surfaces.
- Diagnostic inventory registration, diagnostic-shape registration, and CLI dispatch are existing visibility/plumbing surfaces, not local emitter-attribution ownership boundaries for this scout.

## Recently consumed Emitter Attribution Audit boundaries treated as unavailable

The following were treated as already recovered and unavailable:

- unknown-emitter attribution classification;
- unknown-emitter status decision;
- unknown-emitter reason decision;
- unknown-emitter emitter decision;
- unknown-emitter confidence decision;
- unknown-emitter attribution evidence decision;
- unknown-emitter supporting-reference decision;
- implementation-evidence collection;
- literal reference collection;
- dynamic event-construction evidence collection;
- direct append literal evidence collection;
- deterministic implementation-evidence ordering;
- known-emitter attributed row construction;
- known-emitter event field preservation;
- known-emitter emitter field preservation;
- known-emitter status attribution;
- known-emitter reason preservation;
- known-emitter consumer preservation;
- known-emitter evidence preservation;
- known-emitter emission-type preservation;
- known-emitter confidence preservation;
- known-emitter direct-emitter attribution evidence construction.

## Prior district boundaries avoided

The scout did not re-slice prior Emitter/Consumer Audit work:

- scan-result collection;
- emitted-output relationship-status derivation;
- unknown-emitter row production;
- scanned emitted-item row production;
- final audit assembly.

The scout did not re-slice prior Consumer Dependency Audit work:

- observation-predicate audit item-family production;
- diagnostic audit item-family production;
- matched consumer group construction.

The scout did not re-slice prior Frontier Pressure Admission work:

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

## Stopped and exhausted neighborhoods respected

The scout respected the stopped or exhausted neighborhoods named by the prompt:

- Slice 035: `selection_path_audit` neighborhood exhausted.
- Slice 051: immediate diagnostic-shape pressure candidate-construction pocket exhausted.
- District Scout 004: immediate post-Slice-062 pressure-audit neighborhood exhausted for safe local recovery.
- Outward Scout 005: Frontier Pressure Admission pressure-audit district has zero immediate recoverable candidates.
- Consumer Dependency Audit District Scout 003: local consumer dependency audit district has zero immediate recoverable candidates after Slice 003.
- Emitter/Consumer Audit District Scout 003: local Emitter/Consumer Audit district has zero immediate recoverable candidates after Slice 005.

No candidate was proposed in those neighborhoods.

## Inspected Emitter Attribution Audit neighborhoods

### 1. Unknown-attribution row mapping from recovered classification artifacts

- Evidence: `build_emitter_attribution_audit(...)` still performs the loop over unknown-emitter base events, obtains `refs`, calls `_classify_unknown_emitter_attribution(...)`, and constructs an `EmitterAttributionItem` by copying classification artifact fields plus base consumers and emission type.
- Still-compressed responsibility: yes. The remaining responsibility is not deciding classification; it is constructing the Emitter Attribution Audit item from a completed unknown-emitter attribution artifact and the base row context.
- Direct implementation support: yes. The item constructor fields are explicit implementation behavior.
- Existing helper status: not already separated. `_classify_unknown_emitter_attribution(...)` owns classification only, and `_known_emitter_attributed_rows(...)` owns the known-emitter side only.
- Compatibility risk: low if recovered as a pure helper that preserves event, classified emitter/status/reason/confidence/evidence/supporting references, base consumers, base emission type, combined evidence list, JSON output, human output, sorting input, diagnostics, and read-only behavior.
- Classification: **Independent**.
- Confidence: **High**.
- Ranking: **A. Strong implementation-backed next slice**.

### 2. Deterministic final sorting

- Evidence: `build_emitter_attribution_audit(...)` returns `items=tuple(sorted(items, key=lambda i: (i.status, i.event)))`.
- Still-compressed responsibility: no safe ownership boundary found. Sorting is a deterministic presentation/assembly expression, not an independently meaningful local emitter-attribution responsibility after row construction has been separated.
- Direct implementation support: the expression exists, but evidence supports only order preservation, not a recoverable ownership boundary.
- Compatibility risk: medium. Extracting it could preserve behavior, but would likely create a name around a one-line sorting expression.
- Classification: **Invalid**.
- Confidence: **Medium**.
- Ranking: **D. Cosmetic only**.

### 3. Metadata construction

- Evidence: `build_emitter_attribution_audit(...)` constructs metadata with discovery text, `include_rendered`, and `scope` copied from base audit metadata.
- Still-compressed responsibility: no. The metadata literal and copied scope are final audit assembly details and do not show an independent implementation-local ownership boundary.
- Direct implementation support: the fields exist, but the candidate would mostly name literals and final assembly.
- Compatibility risk: medium. Extraction would be behavior-preserving but likely cosmetic unless future implementation evidence creates richer metadata ownership.
- Classification: **Invalid**.
- Confidence: **Medium**.
- Ranking: **D. Cosmetic only**.

### 4. Audit summary and public JSON output

- Evidence: `EmitterAttributionAudit.summary`, `EmitterAttributionAudit.to_json_dict(...)`, `EmitterAttributionItem.to_json_dict(...)`, and `emitter_attribution_audit_json(...)` already exist as separated surfaces.
- Still-compressed responsibility: no. Summary calculation and JSON serialization are already owned by methods/functions outside the builder.
- Direct implementation support: yes, but it supports already-separated behavior, not a new recovery target.
- Compatibility risk: unnecessary churn. Any slice here would risk changing public schema or re-slicing already separated presentation/schema ownership.
- Classification: **Invalid**.
- Confidence: **High**.
- Ranking: **C. Already separated / likely re-slice**.

### 5. Human-readable output, diagnostic registration, shape registration, and CLI dispatch

- Evidence: `format_emitter_attribution_audit(...)` already owns rendering; diagnostic inventory and diagnostic-shape specs already register the surface; CLI dispatch already builds and prints JSON or human output.
- Still-compressed responsibility: no local Emitter Attribution Audit implementation ownership remains compressed here. These are public presentation, registry, and plumbing surfaces.
- Direct implementation support: yes, but not for a local ownership recovery slice in the Emitter Attribution Audit district.
- Compatibility risk: high relative to value, because changes could accidentally alter visibility contracts, CLI behavior, diagnostic inventory, shape-audit behavior, or schema.
- Classification: **Invalid**.
- Confidence: **High**.
- Ranking: **C. Already separated / likely re-slice**.

## Candidate boundaries found

### Candidate 1: unknown-emitter attribution item construction from recovered attribution artifacts

- Recoverable candidate count contribution: **1**.
- Boundary: map a base Emitter/Consumer Audit item with `emitter == "unknown"`, an event, implementation references, and dynamic references into an `EmitterAttributionItem` after `_classify_unknown_emitter_attribution(...)` has made the classification decision.
- Independent / Sequential / Invalid: **Independent**.
- Confidence: **High**.
- Would still be valid without other proposed candidates: **yes**. The candidate does not require sorting, metadata, JSON, rendering, diagnostic registration, or Operational Graph work to be recovered first.
- Why it is not a re-slice: it does not choose unknown-emitter status, reason, emitter, confidence, attribution evidence, or supporting references; those are already recovered by Slice 001. It does not collect implementation evidence; that is Slice 002. It does not construct known-emitter rows; that is Slice 003. It consumes completed base Emitter/Consumer Audit rows rather than producing base unknown-emitter rows or assembling the base audit.
- Why it is not merely a name: the builder still owns concrete field mapping into the public `EmitterAttributionItem` schema, including event, classified emitter, status, reason, consumers, combined evidence locations, emission type, confidence, attribution evidence, and supporting references. A helper could own a compatibility-preserving row construction boundary analogous to the already recovered known-emitter row helper while leaving classification untouched.
- Compatibility expectation: preserve CLI output, JSON output, human-readable output, row order after final sorting, diagnostic inventory behavior, diagnostic-shape behavior, event-ledger behavior, and read-only cluster boundaries.
- Rank: **A. Strong implementation-backed next slice**.

## Rejected candidates

### Rejected: unknown-emitter classification under a new name

- Classification: **Invalid**.
- Confidence: **High**.
- Rank: **C. Already separated / likely re-slice**.
- Reason rejected: `UnknownEmitterAttribution` and `_classify_unknown_emitter_attribution(...)` already own the decision fields from Slice 001.

### Rejected: implementation-evidence categorization or collection

- Classification: **Invalid**.
- Confidence: **High**.
- Rank: **C. Already separated / likely re-slice**.
- Reason rejected: Slice 002 already recovered implementation-evidence collection, literal references, dynamic event-construction evidence, direct append literal evidence, and deterministic implementation-evidence ordering.

### Rejected: known-emitter row construction follow-up

- Classification: **Invalid**.
- Confidence: **High**.
- Rank: **C. Already separated / likely re-slice**.
- Reason rejected: Slice 003 already recovered `_known_emitter_attributed_rows(...)` and the known-emitter field preservation boundaries.

### Rejected: deterministic sorting helper

- Classification: **Invalid**.
- Confidence: **Medium**.
- Rank: **D. Cosmetic only**.
- Reason rejected: the remaining sorting expression is deterministic and important to preserve, but no implementation evidence shows an independent ownership boundary beyond final assembly order.

### Rejected: metadata helper

- Classification: **Invalid**.
- Confidence: **Medium**.
- Rank: **D. Cosmetic only**.
- Reason rejected: metadata construction is a small final assembly literal/copy operation. Recovering it would likely name a literal rather than recover a boundary.

### Rejected: summary, JSON, human rendering, diagnostic inventory, diagnostic shape, and CLI dispatch

- Classification: **Invalid**.
- Confidence: **High**.
- Rank: **C. Already separated / likely re-slice**.
- Reason rejected: these are already separated public surfaces or registry/plumbing surfaces. They should be preserved by tests if a slice touches row mapping, not recovered as new local Emitter Attribution Audit ownership in this scout.

## Candidate independence answers

How many recoverable candidates currently exist?

**1**

For each candidate:

1. **Unknown-emitter attribution item construction from recovered attribution artifacts**
   - Classification: **Independent**.
   - Confidence: **High**.
   - Why it is not a re-slice: it consumes Slice 001's classification artifact rather than deciding classification, does not collect Slice 002 implementation evidence, does not construct Slice 003 known-emitter rows, and does not produce base Emitter/Consumer Audit rows.
   - Why it is not merely a name: it owns concrete public item field construction from classified attribution evidence and base row context.
   - Valid without other proposed candidates: **yes**.

No second or third implementation-backed candidate is currently supported. Sorting and metadata are visible but rejected as cosmetic/final-assembly pressure, and public output/diagnostic/CLI surfaces are already separated or plumbing.

## Batch efficiency gate

- Efficiency batch: **no**. Three recoverable candidates do not exist.
- Protection batch: **no**. Two recoverable candidates do not exist.
- Single-slice target: **yes**. One implementation-backed slice candidate is safe.
- Stop/move-out: **no for the immediate next command**, because one local Emitter Attribution Audit candidate remains.
- Recommended batch size: **1**.
- Is batching worth it for process protection rather than speed: **no**. With only one safe candidate, a batch would add re-slice risk without command-count savings or protection value.

## Operational Graph exclusion and outward-handoff status

Operational Graph was inspected only as an outward boundary constraint and was not selected. The local district is not exhausted because one implementation-backed Emitter Attribution Audit candidate remains. No different-district handoff is recommended until the unknown-attribution item construction candidate is either recovered or rejected by a focused slice attempt.

## Recommended next command

Recommended next command: **single Emitter Attribution Audit slice** recovering unknown-emitter attribution item construction from recovered `UnknownEmitterAttribution` artifacts into a compatibility-preserving implementation-local owner.

The next move is a **single-slice target** with batch size **1**.

## Risk of re-slicing prior work

- Main risk: accidentally moving classification decisions out of `_classify_unknown_emitter_attribution(...)` or renaming Slice 001 decisions as row mapping.
- Guardrail: the slice should accept the classification artifact as already authoritative and only map it into `EmitterAttributionItem` with base row context.
- Secondary risk: accidentally touching implementation-evidence collection or known-emitter row construction.
- Guardrail: preserve `_collect_emitter_attribution_implementation_evidence(...)`, `_implementation_evidence(...)`, `_known_emitter_attributed_rows(...)`, public JSON, human output, diagnostic inventory, diagnostic shape-audit registration, CLI dispatch, and read-only/event-ledger behavior.

## Scout write boundary

This scout was read-only with respect to implementation and tests. No implementation files were changed. No test files were changed. No slice report was created. No PR metadata was created by the scout report itself. The only intended repository change is `emitter_attribution_audit_district_scout_002.md`.

## Commit hash

The scout report commit hash is recorded in the final response after the commit is created. It cannot be embedded here as the final commit hash without changing the committed file content and therefore changing the hash.
