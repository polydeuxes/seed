# Knowledge Reachability District Scout 002

## District consistency verification

- Active district verified: **Knowledge Reachability**.
- Latest relevant completed slice verified: **`knowledge_reachability_slice_006.md`**.
- Latest local district scout verified: **`knowledge_reachability_district_scout_001.md`**.
- `knowledge_reachability_slice_006.md` identifies the active district as Knowledge Reachability, states that Slice 006 recovered table/human formatting through `_knowledge_reachability_table_output(...)`, and states that no further Knowledge Reachability implementation-local ownership boundary was directly evident without broad scouting after metadata assembly, JSON payload construction, and table/human formatting.
- `knowledge_reachability_district_scout_001.md` was treated as historical context only. Its three candidates have now been consumed by Slices 004, 005, and 006, so Scout 001 did not supply reusable target authority.
- Branch state and local files did not point to another active district. Unrelated district reports were ignored as authority and consulted only where the prompt named prior-district avoidance constraints.
- No district mismatch was found, so this scout proceeded.

## Commands and current app evidence

Read-only commands used during this scout:

```bash
pwd
find .. -name AGENTS.md -print
git status --short
rg -n "Knowledge Reachability|knowledge_reachability_slice_006|knowledge_reachability_district_scout_001|active district|latest" -S . --glob '!*.pyc'
cat AGENTS.md
sed -n '1,220p' knowledge_reachability_slice_006.md
sed -n '1,240p' knowledge_reachability_district_scout_001.md
sed -n '1,260p' seed_runtime/knowledge_reachability.py
sed -n '260,620p' seed_runtime/knowledge_reachability.py
sed -n '620,1040p' seed_runtime/knowledge_reachability.py
rg -n "knowledge_reachability|Knowledge Reachability" seed_runtime scripts tests -S | head -n 200
python scripts/seed_local.py --diagnostic-inventory --json | python -m json.tool | rg -n "knowledge_reachability|Knowledge Reachability|record_scope|mutates_cluster|writes_event_ledger" -C 3
python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-json --knowledge-reachability-audit-limit 20 | head -c 5000
nl -ba seed_runtime/knowledge_reachability.py | sed -n '210,720p'
python scripts/seed_local.py --question-surface-inventory --json | python -m json.tool | rg -n "knowledge reachability|knowledge_reachability|bounded" -C 4
python scripts/seed_local.py --diagnostic-shape-audit --json | python -m json.tool | rg -n "knowledge_reachability|consistent|format_function|json_function" -C 4
```

Observed app evidence:

- `--diagnostic-inventory --json` reported the `knowledge_reachability` surface as JSON-capable, read-only, `record_scope=none`, `supports_record=false`, `writes_event_ledger=false`, `mutates_cluster=false`, `uses_projected_state=true`, and `uses_repo_files=true`.
- `--knowledge-reachability-audit --knowledge-reachability-audit-json --knowledge-reachability-audit-limit 20` ran through load, discovery, index construction, evaluation, render, and counter emission. It reported 20 rows, `raw_seen=23`, `used=20`, `skipped=3`, `truncated=true`, `reason=limit`, metadata aliases `timing` and `candidates`, and index timing keys including `projected_entities`, `projected_facts`, `fact_support`, `source_navigation.index_from_fact_support`, `read_model`, and `inquiry_orientation`.
- `--question-surface-inventory --json` mapped the `knowledge reachability` family to `dispatch_surface=knowledge_reachability_audit`, `canonical_diagnostic_surface=knowledge_reachability`, `diagnostic_inventory_name=knowledge_reachability`, and `diagnostic_shape_spec_name=knowledge_reachability`. This was treated as outward compatibility evidence only.
- `--diagnostic-shape-audit --json` showed implementation-shape consistency for registered diagnostics, including the Knowledge Reachability surface through its declared builder, formatter, and JSON functions. This was treated as registry/shape compatibility evidence only.

## Recently consumed Knowledge Reachability boundaries respected

The following Knowledge Reachability responsibilities are treated as already recovered and unavailable:

- Candidate discovery and source-budget admission, including default seed admission, event-payload candidate admission, projected-state candidate admission, source-navigation-term candidate admission, docs candidate admission, seed_runtime candidate admission, source budget behavior, global limit behavior, subject bypass behavior, raw-seen counts, source counts, scan counts, effective limit, skipped count, truncation state, and the `_CandidateAdmission` handoff.
- Staged index construction, including preserved index construction, projected index construction, read-model index construction, source-navigation index construction, inquiry index construction, phase timing, index timing metadata, index counters, and the `_AuditIndexes` handoff.
- Candidate stage evaluation and first-loss row production, including candidate flag evaluation from indexes, candidate kind classification, first-loss classification, `KnowledgeReachabilityRow` construction, row fields, row order, progress handling, deadline handling, evaluation skipped count, evaluation truncation handling, and the `_EvaluationResult` handoff.
- Public result metadata assembly, including `KnowledgeReachabilityMetadata` construction, timing values, candidate counts, candidate-kind counts, loss-stage counts, algorithmic counters, candidate sources, scan counts, cache state, index timings, truncation reason, limit value, and max-seconds value.
- JSON payload construction, including row dictionary construction, metadata dictionary construction, the `timing` compatibility alias, the `candidates` compatibility alias, the row-only return shape, and the metadata-plus-rows return shape.
- Table/human formatting, including headers, stage-to-attribute mapping, yes/no rendering, column widths, timing metadata section, candidate metadata section, candidate-kind metadata section, loss-stage metadata section, truncation guard text, and final human-readable table composition.

## Prior district boundaries avoided

This scout did not propose re-slicing prior Operational Graph work: emitter/consumer audit graph composition, consumer-dependency audit graph composition, confidence tier row assembly, graph node registry/node creation, graph edge registry/duplicate-edge merging, confidence aggregate-edge filtering, important low-confidence edge selection, or confidence-analysis summary payload construction.

This scout did not propose re-slicing prior Emitter Attribution Audit work: unknown-emitter attribution classification, implementation-evidence collection, known-emitter attributed row construction, or unknown-emitter attribution item construction.

This scout did not propose re-slicing prior Emitter/Consumer Audit work: scan-result collection, emitted-output relationship-status derivation, unknown-emitter row production, scanned emitted-item row production, or final audit assembly.

This scout did not propose re-slicing prior Consumer Dependency Audit work: observation-predicate audit item-family production, diagnostic audit item-family production, or matched consumer group construction.

This scout did not propose re-slicing prior Frontier Pressure Admission work: pressure-audit candidate admission, consumer-predicate source fan-out from pressure-audit, orphaned-predicate pressure evidence payload ownership, fragile-predicate pressure evidence payload ownership, orphaned-predicate pressure score production, orphaned-predicate positive-finding refusal, fragile-predicate pressure score production, fragile-predicate positive-finding refusal, or orphaned-predicate item-set selection.

## Stopped and exhausted neighborhoods respected

The stopped and exhausted neighborhoods named by the prompt were respected:

- Slice 035: `selection_path_audit` neighborhood exhausted.
- Slice 051: immediate diagnostic-shape pressure candidate-construction pocket exhausted.
- District Scout 004: immediate post-Slice-062 pressure-audit neighborhood exhausted for safe local recovery.
- Outward Scout 005: Frontier Pressure Admission pressure-audit district has zero immediate recoverable candidates.
- Consumer Dependency Audit District Scout 003: local Consumer Dependency Audit district has zero immediate recoverable candidates after Slice 003.
- Emitter/Consumer Audit District Scout 003: local Emitter/Consumer Audit district has zero immediate recoverable candidates after Slice 005.
- Emitter Attribution Audit District Scout 003: local Emitter Attribution Audit district has zero immediate recoverable candidates after Slice 004.
- Operational Graph District Scout 004: local Operational Graph district has zero immediate recoverable candidates after Slice 008.

## Inspected Knowledge Reachability neighborhoods

### 1. Top-level result orchestration in `build_knowledge_reachability_audit_result(...)`

Implementation evidence: the builder now delegates candidate admission to `_admit_knowledge_reachability_candidates(...)`, index construction to `_construct_knowledge_reachability_indexes(...)`, candidate evaluation to `_evaluate_knowledge_reachability_candidates(...)`, public metadata assembly to `_assemble_knowledge_reachability_metadata(...)`, JSON rendering to `_knowledge_reachability_json_payload(...)`, and table rendering to `_knowledge_reachability_table_output(...)` through the public formatter.

Assessment: **C. Already separated / likely re-slice**.

Classification: **Invalid**. Confidence: **High**.

Reason rejected: the remaining builder body is orchestration and compatibility handoff. Extracting another local boundary here would either re-slice Slices 001 through 006 or create a broad final-assembly wrapper with no independently compressed responsibility. It is not merely a name because the implementation evidence shows concrete phase calls, but those phase responsibilities are already owned by the recovered helpers.

### 2. `_ReachabilityTimer`, progress messages, phase timing, and algorithmic counters

Implementation evidence: `_ReachabilityTimer` owns phase start/end/progress message emission, while the builder records total time and emits sorted counters after evaluation. The current app run shows load/discovery/index/evaluate/render progress and counter messages.

Assessment: **C. Already separated / likely re-slice**.

Classification: **Invalid**. Confidence: **High**.

Reason rejected: timing metadata, index timing metadata, progress handling, deadline handling, and algorithmic counters were consumed by Slices 002, 003, and 004. Reopening this area would risk progress wording and timing-literal churn rather than recovering a new Knowledge Reachability ownership boundary.

### 3. Public compatibility entry points and data classes

Implementation evidence: `build_knowledge_reachability_audit(...)` remains a row-only compatibility wrapper over `build_knowledge_reachability_audit_result(...)`; `format_knowledge_reachability_table(...)` delegates to `_knowledge_reachability_table_output(...)`; `knowledge_reachability_json(...)` delegates to `_knowledge_reachability_json_payload(...)`; `KnowledgeReachabilityRow`, `KnowledgeReachabilityMetadata`, and `KnowledgeReachabilityAuditResult` define public result shapes.

Assessment: **C. Already separated / likely re-slice**.

Classification: **Invalid**. Confidence: **High**.

Reason rejected: these are public API and schema compatibility seams, not still-compressed implementation-local ownership. Changing them would risk schema movement after Slice 005 and table/public formatting after Slice 006.

### 4. CLI dispatch, diagnostic inventory registration, and diagnostic-shape registration

Implementation evidence: CLI dispatch imports the existing builder, formatter, and JSON function; the diagnostic inventory declares Knowledge Reachability as read-only and non-recording; diagnostic-shape specs point to the existing module and public functions; app inventory and shape-audit output confirm the surface is visible and consistent.

Assessment: **C. Already separated / likely re-slice**.

Classification: **Invalid**. Confidence: **High**.

Reason rejected: this is operational surface plumbing and compatibility evidence. No new diagnostic, audit, probe, CLI flag, recordable output, or diagnostic shape is being added by this scout. A slice here would violate the constraint against using diagnostic registration or CLI dispatch as an automatic candidate.

### 5. Source Navigation, Question Surface Inventory, bounded ask, and inquiry orientation adjacency

Implementation evidence: Knowledge Reachability candidate admission and index construction include source-navigation-shaped evidence, and Question Surface Inventory maps the `knowledge reachability` question family to the Knowledge Reachability diagnostic surface. The inventory also lists Source Navigation and Inquiry Orientation as separate question families/surfaces with their own boundaries.

Assessment: **C. Already separated / likely re-slice for this district**.

Classification: **Invalid**. Confidence: **High**.

Reason rejected: these are outward compatibility surfaces, not remaining local Knowledge Reachability ownership. Direct work there would risk re-slicing Source Navigation, Question Surface Inventory, bounded ask dispatch, or inquiry orientation work.

## Candidate boundaries found

How many recoverable candidates currently exist? **0**.

No implementation-backed Knowledge Reachability slice candidate remains safe in the nearby post-Slice-006 district. Fewer than three implementation-backed candidates are supported; in fact, none are supported.

Candidate detail:

1. **No candidate — local Knowledge Reachability district exhausted after Slice 006**
   - Rank: **E. Stop**.
   - Classification: **Invalid for slicing / exhausted**.
   - Confidence: **High**.
   - Independent / Sequential / Invalid: **Invalid** because no still-compressed single ownership boundary remains.
   - Why it is not a re-slice: no slice is proposed. The scout avoids reusing Scout 001 targets that were consumed by Slices 004 through 006 and avoids reopening Slices 001 through 006 under new names.
   - Why it is not merely a name: the conclusion is based on implementation evidence showing the candidate-admission, index-construction, evaluation, metadata, JSON, and table responsibilities already have explicit helpers and public compatibility callers.
   - Valid without the others: **Not applicable**; there are no other candidates.

## Rejected candidates and why

- **Top-level result assembly**: **C. Already separated / likely re-slice**. The remaining builder body is coordination among already recovered helpers plus public result return. It is too broad as a new boundary and too likely to re-slice metadata, admission, index, or evaluation work.
- **Metadata pass-through**: **C. Already separated / likely re-slice**. Slice 004 consumed metadata construction; later pass-through is public compatibility, not a new local owner.
- **JSON serialization**: **C. Already separated / likely re-slice**. Slice 005 consumed row dictionaries, metadata dictionaries, aliases, and return shapes.
- **Table formatting and human-readable rendering**: **C. Already separated / likely re-slice**. Slice 006 consumed headers, widths, yes/no rendering, metadata sections, guard text, and final table composition.
- **Diagnostic inventory registration and diagnostic-shape registration**: **C. Already separated / likely re-slice**. Current app evidence confirms the surface is visible and consistent; no new operational surface exists to register.
- **CLI dispatch**: **D. Cosmetic only**. The CLI calls the already recovered builder/JSON/formatter paths and does not own a Knowledge Reachability implementation-local responsibility.
- **Progress message wording and timing metadata literals**: **C. Already separated / likely re-slice**. Progress/deadline behavior and timing metadata were already consumed by Slices 002 through 004; changing wording would be compatibility-risky and cosmetic.
- **Source Navigation query composition or formatting**: **C. Already separated / likely re-slice for this district**. It is outward evidence only.
- **Question Surface Inventory and bounded ask dispatch**: **C. Already separated / likely re-slice for this district**. They are compatibility evidence only and belong outside the local Knowledge Reachability district.
- **KnowledgeReachabilityRow / KnowledgeReachabilityMetadata shape movement**: **C. Already separated / likely re-slice**. The shapes are public schema boundaries already exercised by metadata, JSON, and table slices.
- **Candidate-kind counts, loss-stage counts, source counts, scan counts, limit, reason, and skipped count as separate targets**: **C. Already separated / likely re-slice**. These were consumed by admission, evaluation, and metadata assembly slices; splitting them now would rename old work.

## Candidate independence classification

Because there are zero recoverable candidates, no candidate is independent or sequential.

- Independent candidates: **0**.
- Sequential candidates: **0**.
- Invalid or exhausted inspected neighborhoods: **5**.
- Confidence in exhaustion of the immediate local district: **High**.

Each rejected neighborhood would remain invalid even if all other rejected neighborhoods were ignored, because each rejection rests on direct implementation evidence and prior-slice consumption rather than dependency on another proposed candidate.

## Batch efficiency gate

The discovered queue is a **stop/move-out result**.

How many recoverable candidates currently exist?

**0**

This is not an efficiency batch because three recoverable candidates do not exist. It is not a protection batch because two recoverable candidates do not exist. It is not a single-slice target because one safe implementation-backed candidate does not exist.

Recommended batch size: **0**.

Running a batch is not worth it for speed or process protection. A batch would increase the risk of re-slicing prior Knowledge Reachability work or drifting into diagnostic registration, CLI dispatch, Source Navigation, Question Surface Inventory, bounded ask, or other adjacent districts.

## Recommended next command

Recommended next command: **stop local Knowledge Reachability slicing and move outward to another district only if repository authority provides a new handoff**.

Next move classification: **stop/move-out**.

Different-district handoff: **Do not invent one from this scout**. If the next command must continue ownership recovery, it should begin with a fresh outward scout or explicit repository-backed district handoff rather than continuing from stale Knowledge Reachability candidate names.

## Risk of re-slicing prior work

Risk is **high** if future work remains inside the immediate Knowledge Reachability district without new evidence. The remaining tempting areas are known risk zones: top-level result assembly, metadata pass-through, JSON serialization, table formatting, human-readable rendering, diagnostic inventory registration, diagnostic-shape registration, CLI dispatch, Source Navigation adjacency, Question Surface Inventory, bounded ask dispatch, progress wording, timing literals, and public schema keys. Each is now either already recovered, a public compatibility seam, registry plumbing, outward evidence, or cosmetic pressure.

## Read-only statement

This scout was read-only with respect to implementation and tests. No implementation files were changed. No test files were changed. No slice report was created. The only intended repository change is this scout report: `knowledge_reachability_district_scout_002.md`.

## Commit hash

Final scout report commit hash: recorded in git history for the commit containing this file and reported in the assistant final response. A commit cannot reliably embed its own final object hash inside its tracked content without changing that hash.
