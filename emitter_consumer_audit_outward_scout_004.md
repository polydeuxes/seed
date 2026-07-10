# Emitter/Consumer Audit Outward Scout 004

## District consistency verification

- Completed local district verified: **Emitter/Consumer Audit**.
- Latest relevant completed slice verified: **`emitter_consumer_audit_slice_005.md`**.
- Latest local district scout verified: **`emitter_consumer_audit_district_scout_003.md`**.
- The latest local scout reports **0 recoverable candidates**, **no efficiency batch**, **no protection batch**, **no single-slice target**, and **Stop/move-out**.
- No active-district mismatch was found. This scout proceeded outward and did not use unrelated district reports as authority.

## Current app evidence

Read-only commands run from the repository root:

- `python scripts/seed_local.py --emitter-consumer-audit --json`
  - Summary: `items_scanned=25`, `consumed=9`, `orphaned=1`, `partially_consumed=3`, `unknown=12`.
- `python scripts/seed_local.py --emitter-attribution-audit --json`
  - Summary: `items_scanned=41`, `attributed=34`, `dynamic=3`, `indirect=0`, `discovery_gap=4`, `missing=0`, `unknown=0`.
- `python scripts/seed_local.py --operational-graph --json`
  - Summary: `nodes=160`, `edges=276`, `relationship_types={consumes: 247, emits: 29}`, `confidence_counts={high: 29, medium: 39, low: 208}`.
- `python scripts/seed_local.py --operational-graph-confidence --json`
  - Summary matches operational graph edge counts and reports `read_only=true`, `writes_event_ledger=false`, `mutates_cluster=false`.
- `python scripts/seed_local.py --diagnostic-inventory --json`
  - `emitter_consumer_audit`, `emitter_attribution_audit`, `operational_graph`, `operational_graph_taxonomy`, and `operational_graph_confidence` are registered as JSON-capable, non-recording, non-event-ledger-writing, and non-cluster-mutating diagnostics.

## Exhausted neighborhoods respected

The scout did not propose work in these stopped or exhausted neighborhoods:

- Slice 035: `selection_path_audit` neighborhood exhausted.
- Slice 051: immediate diagnostic-shape pressure candidate-construction pocket exhausted.
- District Scout 004: immediate post-Slice-062 pressure-audit neighborhood exhausted for safe local recovery.
- Outward Scout 005: Frontier Pressure Admission pressure-audit district has zero immediate recoverable candidates.
- Consumer Dependency Audit District Scout 003: local consumer dependency audit district has zero immediate recoverable candidates after Slice 003.
- Emitter/Consumer Audit District Scout 003: local Emitter/Consumer Audit district has zero immediate recoverable candidates after Slice 005.

## Recently consumed boundaries treated as unavailable

Unavailable Emitter/Consumer Audit boundaries:

- scan-result collection;
- emitted-output relationship-status derivation;
- unknown-emitter row production;
- scanned emitted-item row production;
- consumer tuple derivation inside scanned emitted-row production;
- evidence aggregation inside scanned emitted-row production;
- relationship-status helper consumption inside scanned emitted-row production;
- final audit assembly;
- final row merging;
- deterministic final sorting;
- final metadata construction.

Unavailable Consumer Dependency Audit boundaries:

- observation-predicate audit item-family production;
- diagnostic audit item-family production;
- matched consumer group construction.

Unavailable Frontier Pressure Admission boundaries:

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

## Inspected outward neighborhoods

### 1. Emitter Attribution Audit build path

Implementation evidence:

- `build_emitter_attribution_audit(...)` consumes `build_emitter_consumer_audit(...)`, collects implementation evidence, iterates base audit items and emitted events, creates direct attributed rows for known emitters, delegates unknown-emitter classification to `_unknown_attribution(...)`, and returns sorted attribution items with metadata.
- This is outside the stopped local Emitter/Consumer Audit district because it consumes the completed audit as an input and produces a separate public diagnostic surface.

Assessment:

- Still-compressed ownership responsibility: **yes**, but broad if taken as the whole build function.
- Direct implementation evidence: **yes**.
- Distinct from prior Emitter/Consumer Audit slices: **yes**, if scoped only to Emitter Attribution row production and not to base scan/result assembly.
- Distinct from prior Consumer Dependency Audit and Frontier Pressure Admission slices: **yes**.
- Compatibility preservation: feasible if the slice extracts a helper without changing schema, CLI, JSON, rendering, inventory, shape-audit behavior, event-ledger behavior, or mutation boundaries.
- Classification: **Sequential / B. Possible but needs caution** if attempted after a stronger first attribution slice, because the whole builder includes multiple responsibilities and could be too broad.

### 2. Emitter Attribution unknown-emitter classification

Implementation evidence:

- `_unknown_attribution(...)` owns the status, reason, emitter, confidence, attribution-evidence, and supporting-reference decision for unknown base audit events.
- It distinguishes direct references, workflow dynamic references, indirect references, discovery gaps, dynamic workflow-only events, and missing emitter evidence.
- Current app evidence shows `dynamic=3` and `discovery_gap=4`, so the classification is active in the app output.

Assessment:

- Still-compressed ownership responsibility: **yes**, exactly one classification boundary is visible.
- Direct implementation evidence: **yes**.
- Distinct from prior Emitter/Consumer Audit slices: **yes**. It does not rescan emitted outputs, derive consumer relationship status, produce unknown-emitter rows for the base audit, produce scanned emitted rows, or assemble the base audit. It classifies attribution for events already surfaced by the completed base audit.
- Distinct from prior Consumer Dependency Audit and Frontier Pressure Admission slices: **yes**.
- Compatibility preservation: feasible through helper extraction or focused tests preserving returned tuple shape and public JSON/rendered summaries.
- Would still be valid without other proposed candidates: **yes**.
- Not a re-slice: it is downstream attribution classification, not base Emitter/Consumer row production.
- Not merely a name: it owns concrete branching behavior and returned data fields used by public Emitter Attribution Audit output.
- Classification: **Independent / High confidence / A. Strong implementation-backed next slice**.

### 3. Emitter Attribution implementation-evidence collection

Implementation evidence:

- `_implementation_evidence(...)` scans Python files, parses ASTs, classifies string literals containing dots, detects dynamic `Event(...)` calls without constant `kind`, detects dynamic `append`/`append_many` calls, performs a second pass for direct append literals, and returns sorted literal and dynamic evidence collections.
- `_reference_category(...)` classifies the provenance of literal references into test, inventory, diagnostic, projection, indirect-emitter, and string-reference categories.

Assessment:

- Still-compressed ownership responsibility: **yes**, but it contains at least two sub-responsibilities: AST evidence collection and reference category labeling.
- Direct implementation evidence: **yes**.
- Distinct from prior Emitter/Consumer Audit slices: **yes**, if scoped to Emitter Attribution evidence collection. It must not re-slice `_python_files(...)`, base scan-result collection, emitted-row evidence aggregation, or final base audit assembly.
- Distinct from prior Consumer Dependency Audit and Frontier Pressure Admission slices: **yes**.
- Compatibility preservation: feasible if behavior and ordering are preserved.
- Would still be valid without other proposed candidates: **yes**, but it should be scoped narrowly to avoid becoming a broad implementation-evidence rewrite.
- Not a re-slice: it gathers downstream attribution references and dynamic-construction hints, not base emitted-output scan results.
- Not merely a name: it owns AST parsing, evidence categorization, and returned data consumed by attribution classification.
- Classification: **Independent / Medium confidence / B. Possible but needs caution**.

### 4. Operational Graph composition from emitter/consumer and consumer audits

Implementation evidence:

- `build_operational_graph(...)` has local node and edge de-duplication helpers, consumes Emitter/Consumer Audit items to add high-confidence `emits` edges and medium-confidence event-to-surface `consumes` edges, consumes Consumer Dependency Audit items to add low-confidence reference-backed `consumes` edges, then returns sorted graph nodes, edges, and read-only metadata.
- Current app evidence shows this public surface is active with 276 edges.

Assessment:

- Still-compressed ownership responsibility: **yes**, but it is a different district and depends on both completed Emitter/Consumer Audit and Consumer Dependency Audit outputs.
- Direct implementation evidence: **yes**.
- Distinct from prior Emitter/Consumer Audit slices: **yes**, provided it only recovers graph composition and does not alter base audit rows.
- Distinct from prior Consumer Dependency Audit slices: **yes**, provided it does not alter item-family production or matched consumer groups.
- Distinct from prior Frontier Pressure Admission slices: **yes**.
- Compatibility preservation: feasible but riskier because the graph public JSON includes nodes, edges, evidence, confidence, and metadata.
- Would still be valid without other proposed candidates: **yes**.
- Not a re-slice: it transforms completed audits into graph edges rather than discovering emitted outputs or consumer groups.
- Not merely a name: it owns concrete node/edge construction, de-duplication, confidence merging, sorting, and read-only metadata.
- Classification: **Independent / Medium confidence / B. Possible but needs caution**.

### 5. Diagnostic inventory / diagnostic-shape visibility around adjacent surfaces

Implementation evidence:

- Diagnostic inventory registers `emitter_consumer_audit`, `emitter_attribution_audit`, `operational_graph`, `operational_graph_taxonomy`, and `operational_graph_confidence` as read-only, non-recording operational surfaces.
- These rows are compatibility constraints for any future adjacent diagnostic change.

Assessment:

- Still-compressed ownership responsibility: **no safe candidate for this scout**.
- Direct implementation evidence: **yes**, but the rows already exist.
- Classification: **Invalid / High confidence / C. Already separated / likely re-slice**.
- Reason rejected: changing registration or shape-audit specs would create or alter operational visibility surfaces, which this read-only scout must not do. Existing registry rows constrain future slices but do not by themselves expose a fresh implementation-local recovery boundary.

## Candidate boundaries found

How many recoverable candidates currently exist?

**3**

### Candidate 1 — Emitter Attribution unknown-emitter classification

- Rank: **A. Strong implementation-backed next slice**.
- Classification: **Independent**.
- Confidence: **High**.
- Boundary: recover `_unknown_attribution(...)` decision ownership as a focused Emitter Attribution Audit slice.
- Why it is not a re-slice: it classifies attribution status for unknown base audit events after the base Emitter/Consumer Audit has already completed. It does not own base scan-result collection, relationship-status derivation, unknown-emitter base-row production, scanned emitted-item row production, or final base audit assembly.
- Why it is not merely a name: it owns concrete branching decisions and returned status/reason/emitter/confidence/evidence fields used in Emitter Attribution Audit output.
- Valid without other candidates: **yes**.

### Candidate 2 — Emitter Attribution implementation-evidence collection

- Rank: **B. Possible but needs caution**.
- Classification: **Independent**.
- Confidence: **Medium**.
- Boundary: recover `_implementation_evidence(...)` collection of literal references, dynamic event-construction evidence, and direct append literal evidence.
- Why it is not a re-slice: it scans for attribution references and dynamic construction hints for the downstream attribution audit, not for base Emitter/Consumer Audit row production.
- Why it is not merely a name: it owns AST traversal, evidence category assignment, dynamic evidence detection, direct append evidence detection, and deterministic return ordering.
- Valid without other candidates: **yes**.
- Caution: the candidate must avoid reopening shared `_python_files(...)` behavior and should not bundle `_reference_category(...)` unless the implementation evidence requires it.

### Candidate 3 — Operational Graph audit-composition edge production

- Rank: **B. Possible but needs caution**.
- Classification: **Independent**.
- Confidence: **Medium**.
- Boundary: recover `build_operational_graph(...)` conversion of completed audit items into graph nodes, evidence, confidence, and sorted graph output.
- Why it is not a re-slice: it consumes completed Emitter/Consumer Audit and Consumer Dependency Audit outputs to build graph relationships. It does not rediscover events, consumers, or pressure candidates.
- Why it is not merely a name: it owns executable graph construction behavior, including node IDs, edge de-duplication, evidence construction, confidence merging, sorting, and read-only metadata.
- Valid without other candidates: **yes**.
- Caution: it is a different-district handoff and should not be batched with Emitter Attribution slices unless the next command explicitly chooses an outward mixed-district batch.

## Rejected candidates

### Rejected: Emitter Attribution full build orchestration

- Rank: **B/C depending scope**.
- Classification: **Sequential** if narrowed after Candidate 1, otherwise **Invalid** as too broad.
- Reason: `build_emitter_attribution_audit(...)` includes direct attributed item creation, unknown classification delegation, evidence collection, sorting, and metadata. Recovering the entire builder in one slice risks bundling multiple ownership boundaries.

### Rejected: Emitter Attribution formatter

- Rank: **C. Already separated / likely re-slice**.
- Classification: **Invalid**.
- Reason: `format_emitter_attribution_audit(...)` is already a discrete formatting owner. No evidence showed a still-compressed implementation-local responsibility beyond presentation line assembly.

### Rejected: Operational Graph confidence analysis

- Rank: **B/C**.
- Classification: **Sequential** after a graph-composition slice, otherwise **Invalid for immediate batch**.
- Reason: `build_operational_graph_confidence(...)` is implementation-backed and active, but it depends on graph composition and contains multiple analysis subparts. It should be reassessed after any graph-composition slice rather than bundled now.

### Rejected: Operational Graph taxonomy analysis

- Rank: **C. Already separated / likely re-slice**.
- Classification: **Invalid for this scout**.
- Reason: it is a separate registered surface and not directly needed to move outward from exhausted Emitter/Consumer Audit. It risks expanding into operational graph taxonomy rather than adjacent emitter/consumer consumption.

### Rejected: Diagnostic inventory or diagnostic-shape registration rows

- Rank: **C. Already separated / likely re-slice**.
- Classification: **Invalid**.
- Reason: registry rows are already present and should be treated as compatibility constraints, not fresh recovery candidates.

## Batch Efficiency Gate

- Recoverable candidates currently exist: **3**.
- Efficiency batch: **conditionally yes**, because three implementation-backed candidates exist.
- Protection batch: **not the primary recommendation**, because three candidates exist; however, if the next command wants lower risk, a two-candidate protection batch inside Emitter Attribution Audit is safer than a mixed-district batch.
- Single-slice target: **also safe**, with Candidate 1 as the strongest first slice.
- Stop/move-out: **no local Emitter/Consumer Audit work remains**, but the outward scout found adjacent recoverable work.
- Different-district handoff: **yes**. The next work should move out of Emitter/Consumer Audit into Emitter Attribution Audit, or explicitly into Operational Graph if that district is selected.

## Recommended next command

Recommended next command: **different-district handoff to Emitter Attribution Audit with an efficiency batch of up to 2 Emitter Attribution candidates, starting with unknown-emitter classification, then implementation-evidence collection only if the first slice preserves behavior cleanly**.

Recommended batch size:

- **2** for safest same-district process protection: Candidate 1 and Candidate 2.
- **3** only if the process explicitly accepts a mixed outward batch that includes Operational Graph as a separate district candidate. Because Candidate 3 belongs to Operational Graph, not Emitter Attribution Audit, a three-candidate batch saves command count but increases coordination and re-slice risk.

The safest single-slice target is Candidate 1: **Emitter Attribution unknown-emitter classification**.

## Risk of re-slicing prior work

- Risk is **low** for Candidate 1 if scoped strictly to `_unknown_attribution(...)` return decisions.
- Risk is **medium** for Candidate 2 because it scans implementation evidence and imports `_python_files(...)` from the base audit module; the slice must not reopen base Emitter/Consumer scan-result collection.
- Risk is **medium** for Candidate 3 because it composes both Emitter/Consumer Audit and Consumer Dependency Audit output; the slice must not reopen either source audit district.
- Risk is **high** if any next command continues mining local Emitter/Consumer Audit internals after District Scout 003.

## Read-only and file-change statement

This scout was read-only with respect to implementation and tests. No implementation files were changed. No test files were changed. No slice report was created. No PR metadata was created by this scout report. The only intended repository change is `emitter_consumer_audit_outward_scout_004.md`.

## Scout report commit

Commit hash for the scout report commit: pending until commit creation; record the final committed hash from `git rev-parse HEAD` after committing this file.
