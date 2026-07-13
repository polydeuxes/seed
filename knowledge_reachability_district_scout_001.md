# Knowledge Reachability District Scout 001

## District consistency verification

- Active district verified: **Knowledge Reachability**.
- Latest relevant completed slice verified: **`knowledge_reachability_slice_003.md`**.
- Completed handoff source verified: **`operational_graph_outward_scout_005.md`**.
- `knowledge_reachability_slice_003.md` identifies the active district as Knowledge Reachability, verifies `operational_graph_outward_scout_005.md` as the handoff source, and says Slice 003 recovered candidate stage evaluation and first-loss row production.
- `operational_graph_outward_scout_005.md` identifies Knowledge Reachability as the outward adjacent district after Operational Graph exhaustion.
- Branch and local files did not point this scout to another active district. Unrelated district reports were ignored as authority and used only where the prompt named them as avoidance constraints.
- No district mismatch was found, so the scout proceeded.

## Commands and current app evidence

Read-only commands used during the scout:

```bash
git status --short
sed -n '1,220p' knowledge_reachability_slice_003.md
sed -n '1,120p' operational_graph_outward_scout_005.md
sed -n '1,260p' seed_runtime/knowledge_reachability.py
sed -n '260,620p' seed_runtime/knowledge_reachability.py
sed -n '620,980p' seed_runtime/knowledge_reachability.py
sed -n '980,1320p' seed_runtime/knowledge_reachability.py
rg -n "knowledge_reachability|Knowledge Reachability" seed_runtime tests scripts -S
python scripts/seed_local.py --diagnostic-inventory --json
python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-json --knowledge-reachability-audit-limit 20
python scripts/seed_local.py --question-surface-inventory --json
```

Observed app evidence:

- `--diagnostic-inventory --json` reported **56** entries. The `knowledge_reachability` entry is JSON-capable, read-only, `record_scope=none`, `writes_event_ledger=false`, `mutates_cluster=false`, `uses_projected_state=true`, and `uses_repo_files=true`.
- `--knowledge-reachability-audit --knowledge-reachability-audit-json --knowledge-reachability-audit-limit 20` reported **20** rows, candidate counts including `raw_seen=22`, `used=20`, `skipped=2`, `truncated=true`, `reason=limit`, and candidate/loss counts flowing through metadata.
- The same Knowledge Reachability app run reported index timing keys including `projected_entities`, `projected_facts`, `fact_support`, `source_navigation.index_from_fact_support`, `read_model`, and `inquiry_orientation`.
- The same run emitted progress/counter messages for load, discovery, index construction, evaluation, render, and algorithmic counters. This is behavioral evidence only, not authority for a new progress or counter slice.
- `--question-surface-inventory --json` reported **17** rows and mapped the `knowledge reachability` question family to `dispatch_surface=knowledge_reachability_audit`, `canonical_diagnostic_surface=knowledge_reachability`, and the existing diagnostic inventory/shape entries. This was treated as compatibility evidence only.

## Recently consumed Knowledge Reachability boundaries respected

The following Knowledge Reachability responsibilities are treated as already recovered and unavailable:

- Candidate discovery and source-budget admission, including default seeds, event payloads, projected state, source-navigation terms, docs, seed_runtime scanning, source budget behavior, global limit behavior, subject bypass behavior, raw-seen/source/scan counts, effective limit, skipped count, truncation state, and the `_CandidateAdmission` handoff.
- Staged index construction, including preserved, projected, read-model, source-navigation, and inquiry index construction, phase timing, index timing metadata, index counters, and the `_AuditIndexes` handoff.
- Candidate stage evaluation and first-loss row production, including candidate flag evaluation, candidate-kind classification, first-loss classification, `KnowledgeReachabilityRow` construction, row fields/order, progress and deadline behavior, evaluation skipped count, truncation handling, and the `_EvaluationResult` handoff.

## Prior district boundaries avoided

This scout did not propose re-slicing prior Operational Graph work: emitter/consumer audit graph composition, consumer-dependency audit graph composition, confidence tier row assembly, graph node registry/node creation, graph edge registry/duplicate-edge merging, confidence aggregate-edge filtering, important low-confidence edge selection, or confidence-analysis summary payload construction.

This scout did not propose re-slicing prior Emitter Attribution Audit work: unknown-emitter attribution classification, implementation-evidence collection, known-emitter attributed row construction, or unknown-emitter attribution item construction.

This scout did not propose re-slicing prior Emitter/Consumer Audit work: scan-result collection, emitted-output relationship-status derivation, unknown-emitter row production, scanned emitted-item row production, or final audit assembly.

This scout did not propose re-slicing prior Consumer Dependency Audit work: observation-predicate audit item-family production, diagnostic audit item-family production, or matched consumer group construction.

This scout did not propose re-slicing prior Frontier Pressure Admission work: pressure-audit candidate admission, consumer-predicate source fan-out, fragile/orphaned predicate evidence payload ownership, fragile/orphaned pressure score production, positive-finding refusal, or item-set selection.

## Stopped and exhausted neighborhoods respected

The stopped/exhausted neighborhoods named by the prompt were respected:

- Slice 035: `selection_path_audit` neighborhood exhausted.
- Slice 051: immediate diagnostic-shape pressure candidate-construction pocket exhausted.
- District Scout 004: immediate post-Slice-062 pressure-audit neighborhood exhausted for safe local recovery.
- Outward Scout 005: Frontier Pressure Admission pressure-audit district has zero immediate recoverable candidates.
- Consumer Dependency Audit District Scout 003: local Consumer Dependency Audit district has zero immediate recoverable candidates after Slice 003.
- Emitter/Consumer Audit District Scout 003: local Emitter/Consumer Audit district has zero immediate recoverable candidates after Slice 005.
- Emitter Attribution Audit District Scout 003: local Emitter Attribution Audit district has zero immediate recoverable candidates after Slice 004.
- Operational Graph District Scout 004: local Operational Graph district has zero immediate recoverable candidates after Slice 008.

## Inspected Knowledge Reachability neighborhoods

### 1. Public result metadata assembly after admission, index construction, and evaluation

Implementation evidence: `build_knowledge_reachability_audit_result(...)` still directly assembles `KnowledgeReachabilityMetadata` after consuming `_CandidateAdmission`, `_AuditIndexes`, and `_EvaluationResult`. The remaining inline assembly combines rounded timings, candidate counts, candidate-kind counts, loss-stage counts, algorithmic counters, candidate sources, scan counts, cache state, index timings, truncation/reason, limit, and max-seconds into the public metadata object.

Assessment: **A. Strong implementation-backed next slice**.

Classification: **Independent**. Confidence: **High**.

Why it is not a re-slice: the already consumed slices produced admission, indexes, and evaluation rows; they intentionally left broad metadata/result assembly unrecovered. A focused metadata assembly slice would consume those artifacts without reopening candidate discovery, index construction, row production, progress handling, or truncation mechanics.

Why it is not merely a name: the boundary is a concrete producer responsibility with many public metadata keys and derived count payloads assembled in one remaining block, not a label-only extraction.

Would it remain valid if other proposed candidates were not recovered? **Yes**. Metadata assembly can be recovered while JSON and table renderers remain unchanged consumers.

Compatibility expectation: preserve behavior, schema, CLI, JSON, table output, diagnostic inventory/shape visibility, event-ledger behavior, and read-only boundaries by keeping the same `KnowledgeReachabilityMetadata` values.

### 2. JSON payload construction for Knowledge Reachability audit output

Implementation evidence: `knowledge_reachability_json(...)` separately converts rows with `asdict(row)`, converts metadata with `asdict(metadata)`, adds compatibility aliases `timing` and `candidates`, and returns either row-only or metadata-plus-rows payloads.

Assessment: **B. Possible but needs caution**.

Classification: **Sequential**. Confidence: **Medium**.

Why it is not a re-slice: JSON payload construction was explicitly left unrecovered by Slice 003 and is separate from row evaluation. It owns public serialization aliases rather than producing rows or metadata values.

Why it is not merely a name: it is implementation-backed by a dedicated public function with compatibility aliases and two return shapes.

Would it remain valid if other proposed candidates were not recovered? **Partly**. It is valid without table rendering, but it should be reassessed after metadata assembly because extracting JSON before metadata assembly risks moving public schema literals without first clarifying the producer of the metadata payload.

Compatibility expectation: any future slice must preserve row dictionaries, metadata dictionary keys, `timing` alias, `candidates` alias, JSON-capable CLI output, bounded ask compatibility, and diagnostic shape expectations.

### 3. Table/human formatting for Knowledge Reachability audit output

Implementation evidence: `format_knowledge_reachability_table(...)` separately owns headers, stage-to-attribute mapping, yes/no rendering, column widths, metadata sections for timing/candidates/kinds/losses, truncation guard text, and final human-readable table composition.

Assessment: **B. Possible but needs caution**.

Classification: **Sequential**. Confidence: **Medium**.

Why it is not a re-slice: table formatting was explicitly left unrecovered by Slice 003 and is separate from candidate admission, index construction, and row evaluation.

Why it is not merely a name: it is an existing public formatter with concrete rendering behavior, metadata sections, and compatibility-sensitive wording.

Would it remain valid if other proposed candidates were not recovered? **Partly**. It can stand apart from JSON, but it should be reassessed after metadata assembly because it consumes metadata sections and public wording; extracting it too early risks cosmetic formatting churn.

Compatibility expectation: any future slice must preserve exact human output semantics, stage headers, yes/no conversion, truncation guard behavior, CLI human output, and diagnostic shape declarations.

### 4. Diagnostic inventory and diagnostic-shape registration

Implementation evidence: `seed_runtime/diagnostic_inventory.py` and `seed_runtime/diagnostic_shape_audit.py` already declare Knowledge Reachability as a read-only JSON-capable diagnostic with repo-file and projected-state use. App inventory confirms the surface.

Assessment: **C. Already separated / likely re-slice**.

Classification: **Invalid**. Confidence: **High**.

Reason rejected: this is registry/spec plumbing, not a still-compressed Knowledge Reachability implementation-local ownership boundary. No new operational surface is being added by the scout.

### 5. Source Navigation, Question Surface Inventory, and bounded ask adjacency

Implementation evidence: Knowledge Reachability has source-navigation-shaped terms in candidate discovery/indexing, and Question Surface Inventory maps the question family to the Knowledge Reachability diagnostic surface. The app confirms this compatibility path.

Assessment: **C. Already separated / likely re-slice for this district**.

Classification: **Invalid**. Confidence: **High**.

Reason rejected: Source Navigation, Question Surface Inventory, and bounded ask are outward compatibility evidence only. Direct work there would risk re-slicing adjacent districts rather than recovering a remaining local Knowledge Reachability ownership boundary.

## Candidate boundaries found

How many recoverable candidates currently exist? **3**.

1. **Public result metadata assembly**
   - Rank: **A. Strong implementation-backed next slice**.
   - Classification: **Independent**.
   - Confidence: **High**.
   - Not a re-slice because it consumes the already recovered admission, index, and evaluation artifacts and owns only final public metadata/result assembly.
   - Not merely a name because concrete metadata keys and derived payloads are still assembled inline.
   - Valid without the others: **Yes**.

2. **JSON payload construction**
   - Rank: **B. Possible but needs caution**.
   - Classification: **Sequential**.
   - Confidence: **Medium**.
   - Not a re-slice because it owns public serialization aliases and return shapes, not candidate admission/index/evaluation.
   - Not merely a name because it has concrete JSON compatibility behavior.
   - Valid without the others: **Only after reassessment**; safer after metadata assembly.

3. **Table/human formatting**
   - Rank: **B. Possible but needs caution**.
   - Classification: **Sequential**.
   - Confidence: **Medium**.
   - Not a re-slice because it owns human presentation, not candidate admission/index/evaluation.
   - Not merely a name because it has concrete header, width, metadata-section, and truncation rendering behavior.
   - Valid without the others: **Only after reassessment**; safer after metadata assembly.

No fourth nearby implementation-backed candidate is recommended. Diagnostic registration, CLI dispatch, Source Navigation, Question Surface Inventory, bounded ask, progress wording, timing literal movement, candidate-kind/loss counts, truncation behavior, and skipped-count mechanics are either already consumed, registry/plumbing, compatibility evidence, presentation/schema risk, or likely re-slices.

## Rejected candidates and reasons

- Candidate-kind counts and loss-stage counts alone: **C. Already separated / likely re-slice**. They are derived metadata consumers of rows already produced by Slice 003; separating only those counts would be too narrow and likely a re-slice of row evaluation.
- Source counts, scan counts, skipped count, effective limit, and truncation metadata alone: **C. Already separated / likely re-slice**. These were recovered through admission and evaluation handoffs; only their final public metadata assembly remains a valid broader boundary.
- Index timing metadata alone: **C. Already separated / likely re-slice**. Slice 002 consumed index timing metadata; moving its final assignment alone would be public metadata assembly at most.
- Progress and deadline behavior: **C. Already separated / likely re-slice**. Slice 003 consumed progress and deadline behavior.
- CLI dispatch: **D. Cosmetic only for this scout**. The CLI calls the existing builder and renderers; no direct local ownership boundary is compressed there for Knowledge Reachability after Slice 003.
- Diagnostic inventory/shape registration: **C. Already separated / likely re-slice**. Existing registry/spec declarations are compatibility surfaces, not a new local ownership boundary.
- Source Navigation query composition/formatting: **C. Already separated / likely re-slice for this district**. It is outward evidence only.
- Question Surface Inventory and bounded ask dispatch: **C. Already separated / likely re-slice for this district**. They are compatibility evidence only.

## Batch efficiency gate

The discovered queue is an **efficiency batch** by count because **three** recoverable candidates exist with enough evidence to attempt a guarded batch.

However, only the first candidate is high-confidence independent. The JSON and table candidates are sequential and should be reassessed after metadata assembly lands. A batch is safe only if guarded as:

1. Slice metadata assembly first.
2. Reassess JSON payload construction against the post-metadata code before changing it.
3. Reassess table/human formatting against the post-metadata code before changing it.

Recommended batch size: **3 maximum**, but **1 preferred if the next command cannot enforce reassessment between sequential slices**.

This is not a protection batch because three candidates exist. It is not a single-slice target because JSON and table rendering are implementation-backed candidates, though sequential. It is not stop/move-out because at least one strong local candidate remains.

## Recommended next command

Recommended next command: perform a **guarded Knowledge Reachability efficiency batch**, beginning with **public result metadata assembly** as the first slice. If the process cannot reassess after that slice, perform only the single metadata assembly slice and then run a fresh scout.

Next move classification: **efficiency batch with sequential gates**.

Different-district handoff: **No**. Stay in Knowledge Reachability for the next command unless metadata assembly is rejected by implementation evidence.

## Risk of re-slicing prior work

Risk is **medium** overall:

- Low for metadata assembly if it is bounded to final public metadata construction and does not alter admission, index construction, row evaluation, progress, deadline, or truncation behavior.
- Medium for JSON and table rendering because public schema keys and wording are compatibility-sensitive and can become cosmetic movement if not reassessed after metadata assembly.
- High if the next command attempts candidate counts, loss counts, source counts, index timings, progress wording, diagnostic registration, CLI dispatch, Source Navigation, Question Surface Inventory, or bounded ask work as separate local slices.

## Read-only statement

This scout was read-only with respect to implementation and tests. No implementation files were changed. No test files were changed. No slice report was created. No PR metadata file was created. The only intended repository change is this scout report: `knowledge_reachability_district_scout_001.md`.

## Commit hash

Final scout report commit hash: recorded in git history for the commit containing this file and reported in the assistant final response. A commit cannot reliably embed its own final object hash without changing that hash.
