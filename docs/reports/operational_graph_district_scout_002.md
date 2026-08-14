# Operational Graph District Scout 002

## District consistency verification

- Active district verified: **Operational Graph**.
- Latest relevant completed slice verified: **`operational_graph_slice_006.md`**.
- Latest local district scout verified: **`operational_graph_district_scout_001.md`**.
- Branch state did not point to another active district: `git status --short --branch` reported `## work` before this scout file was created.
- Local files support the requested Operational Graph sequence: `operational_graph_slice_001.md` through `operational_graph_slice_006.md` are present, and Slice 006 identifies `operational_graph_district_scout_001.md` as the latest local scout before the batch.
- No available report, summary, branch state, or local file pointed this scout to another active district. No district mismatch was found.
- Unrelated district reports were ignored as authority. They were used only as avoidance constraints where they named prior recovered or exhausted boundaries.

## Current app evidence

Read-only app commands were run to verify the current Operational Graph surface after Slice 006:

- `python scripts/seed_local.py --operational-graph | head -40` reported 164 nodes, 284 edges, relationship counts of 255 `consumes` and 29 `emits`, and confidence counts of 29 high, 39 medium, and 216 low.
- `python scripts/seed_local.py --operational-graph-confidence --operational-graph-confidence-tier low | head -80` reported 216 low-confidence consumes edges, 698 reference evidence entries, aggregate-target uncertainty, attribution uncertainty, reference-only uncertainty, taxonomy uncertainty, representative examples, and the current operationally relevant low-confidence edge list.
- `python scripts/seed_local.py --operational-graph-taxonomy | head -60` reported 164 nodes, 8 aggregate nodes, 156 concrete nodes, aggregate-surface classifications, and aggregate connectivity headed by `surface:state_build` and `surface:views`.
- `python scripts/seed_local.py --diagnostic-inventory --json | python -c '...'` confirmed `operational_graph`, `operational_graph_taxonomy`, and `operational_graph_confidence` remain read-only, JSON-capable, non-recording, non-event-ledger-writing, and non-mutating diagnostic surfaces.

These commands are behavior evidence only. They were not treated as authority for promoting presentation vocabulary into repository knowledge.

## Recently consumed Operational Graph boundaries respected

The following Operational Graph boundaries are already recovered and unavailable for new slicing:

- emitter/consumer audit graph composition;
- Emitter/Consumer Audit item to graph node production;
- direct high-confidence emits edge production;
- indirect medium-confidence consumes edge production;
- emitter/consumer composition duplicate-edge merge participation;
- consumer-dependency audit graph composition;
- Consumer Dependency Audit item-kind node mapping;
- consumer surface node mapping;
- reference evidence construction;
- low-confidence consumes edge production;
- consumer-dependency composition duplicate-edge merge participation;
- confidence tier row assembly;
- confidence tier evidence counts;
- confidence tier relationship-type counts;
- confidence tier uncertainty causes;
- confidence tier uncertainty categories;
- confidence tier interpretation;
- confidence tier reasons;
- confidence tier improvement text;
- confidence tier representative examples;
- confidence tier important low-confidence edge participation, if recovered by Slice 003;
- graph node registry / node creation;
- stable node id construction;
- node de-duplication;
- `OperationalGraphNode` construction;
- node classification application;
- node id return to graph composition callbacks;
- graph edge registry / duplicate-edge merging;
- evidence-free edge omission;
- edge key construction;
- `OperationalGraphEdge` insertion;
- duplicate evidence merge ordering;
- stronger-confidence preservation;
- confidence aggregate-edge filtering;
- aggregate-edge exclusion;
- unfiltered confidence edge behavior.

## Prior district boundaries avoided

Avoided prior Emitter Attribution Audit boundaries:

- unknown-emitter attribution classification;
- implementation-evidence collection;
- known-emitter attributed row construction;
- unknown-emitter attribution item construction.

Avoided prior Emitter/Consumer Audit boundaries:

- scan-result collection;
- emitted-output relationship-status derivation;
- unknown-emitter row production;
- scanned emitted-item row production;
- final audit assembly.

Avoided prior Consumer Dependency Audit boundaries:

- observation-predicate audit item-family production;
- diagnostic audit item-family production;
- matched consumer group construction.

Avoided prior Frontier Pressure Admission boundaries:

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

This scout did not propose work in the stopped or exhausted neighborhoods named by the prompt:

- Slice 035: `selection_path_audit` neighborhood exhausted.
- Slice 051: immediate diagnostic-shape pressure candidate-construction pocket exhausted.
- District Scout 004: immediate post-Slice-062 pressure-audit neighborhood exhausted for safe local recovery.
- Outward Scout 005: Frontier Pressure Admission pressure-audit district has zero immediate recoverable candidates.
- Consumer Dependency Audit District Scout 003: local Consumer Dependency Audit district has zero immediate recoverable candidates after Slice 003.
- Emitter/Consumer Audit District Scout 003: local Emitter/Consumer Audit district has zero immediate recoverable candidates after Slice 005.
- Emitter Attribution Audit District Scout 003: local Emitter Attribution Audit district has zero immediate recoverable candidates after Slice 004.

## Inspected Operational Graph neighborhoods

### 1. Confidence analysis important low-confidence edge selection

Implementation evidence:

- `build_operational_graph_confidence(...)` now builds the graph, maps nodes, delegates aggregate-edge filtering, selects confidence tiers, builds tier summaries, and still locally assembles `important_low_confidence_edges`.
- The remaining important-edge code sorts the filtered graph edges by `_edge_sort_key`, selects only low-confidence edges, requires `_importance(edge)`, converts each surviving edge through `_edge_example(edge, include_importance=True)`, and truncates the public result to ten rows.
- `_importance(...)` is already a separate predicate over `IMPORTANT_SURFACES`, and `_edge_example(...)` is already a separate row projector. The still-compressed responsibility is the orchestration that selects the important low-confidence edge list from filtered graph edges.

Scout finding: **A. Strong implementation-backed next slice**.

Candidate independence classification: **Independent**.

Confidence: **High**.

Why it is one ownership boundary: the candidate owns one list-selection responsibility: sorted filtered-edge traversal, low-confidence selection, importance filtering, row projection with importance, and result limit for the `important_low_confidence_edges` section.

Why it is not a re-slice: it does not recover confidence tier row assembly from Slice 003, graph node registration from Slice 004, graph edge registration from Slice 005, aggregate-edge filtering from Slice 006, or any upstream audit row construction. It starts after graph-edge filtering and tier-summary assembly inputs already exist.

Why it is not merely a name: app output exposes a concrete "Operationally relevant low-confidence edges" section, tests assert `important_low_confidence_edges` exists and is non-empty, and implementation evidence shows selection conditions and output projection, not just vocabulary.

Would it remain valid without other proposed candidates? **Yes**. It can be recovered as a helper without any taxonomy, summary, sorting, CLI, JSON, or diagnostic-registration change.

Compatibility expectation: recovery should preserve behavior, schema, CLI output, JSON keys, diagnostics, event-ledger behavior, and read-only boundaries if it is limited to extracting the current selection into a private helper and keeping the same top-ten output.

### 2. Confidence selected-tier orchestration

Implementation evidence:

- `build_operational_graph_confidence(...)` computes `selected = ("high", "medium", "low") if confidence is None else (confidence,)` and creates the `tiers` dictionary by calling `_confidence_tier_summary(...)` for each selected tier.

Scout finding: **D. Cosmetic only**.

Candidate independence classification: **Invalid**.

Confidence: **Low**.

Why it is rejected: this is a tiny control-flow expression and dictionary comprehension around an already recovered tier summary helper. Extracting it would mostly name a public filtering parameter rather than recover an implementation-local ownership boundary. It also risks re-slicing Slice 003's confidence tier row assembly under a new orchestration name.

### 3. Confidence analysis summary construction

Implementation evidence:

- `build_operational_graph_confidence(...)` constructs the public summary by combining graph summary values with filtered edge counts, filtered relationship-type counts, filtered confidence counts, total graph edge count, excluded aggregate edge count, the aggregate-exclusion flag, read-only flags, event-ledger flags, mutation flags, and the selected confidence filter.

Scout finding: **B. Possible but needs caution**, but **not recommended as a current recoverable batch candidate**.

Candidate independence classification: **Sequential / needs reassessment after the important-low slice**.

Confidence: **Medium-Low**.

Why it is not currently safe enough: the implementation is real, but it is adjacent to public JSON shape, diagnostic-shape expectations, read-only metadata, and aggregate-filter accounting. The seam mixes count production with public compatibility metadata. It should be reassessed after the important-low slice rather than batched now.

Why it is not a re-slice if later recovered: a future helper would have to own only confidence-analysis summary construction from already-filtered graph edges and the existing graph, not tier assembly, aggregate filtering, graph summary, or diagnostic registration.

Why it is not merely a name: current JSON and tests exercise these keys and counts. However, because the boundary is public-shape-adjacent, evidence of behavior is not enough to make it safe for the next batch.

Would it remain valid without the important-low slice? **Possibly**, but not with enough confidence for this scout. It should be reassessed after any prior confidence-analysis extraction because the remaining local compression may change.

### 4. Operational Graph taxonomy summary and aggregate connectivity

Implementation evidence:

- `build_operational_graph_taxonomy(...)` already exists as a public taxonomy build boundary.
- Its body counts node classifications, counts node types, computes node degree from edges, selects aggregate nodes, sorts aggregate connectivity by degree and id, constructs public rows, and attaches summary metadata.

Scout finding: **C. Already separated / likely re-slice** for the builder as a whole, and **B/C with caution** for any smaller degree or row helper.

Candidate independence classification: **Invalid for the next command**.

Confidence: **Medium**.

Why it is rejected: this neighborhood is implementation-backed, but the visible seams are taxonomy naming, degree accounting, aggregate/concrete summary counts, public row projection, sorting, and metadata. The prompt identifies taxonomy classification, aggregate naming, degree accounting, aggregate connectivity rows, and presentation extraction as known risk areas. A slice here would likely extract public taxonomy shape or sorting rather than one implementation-local ownership boundary.

Why it is not used as authority: taxonomy app output is evidence of current behavior only. It does not prove a safe local recovery target after the existing public taxonomy builder.

### 5. Graph sorting, metadata, JSON output, CLI dispatch, and diagnostic registration

Implementation evidence:

- `build_operational_graph(...)` sorts final nodes and edges and attaches metadata.
- `OperationalGraph.to_json_dict(...)`, `operational_graph_json(...)`, `operational_graph_confidence_json(...)`, and `operational_graph_taxonomy_json(...)` preserve public JSON shapes.
- CLI dispatch calls the existing builders and formatters.
- Diagnostic inventory and diagnostic-shape registration already expose Operational Graph surfaces as read-only, JSON-capable, non-recording, non-event-ledger-writing, and non-mutating.

Scout finding: **D. Cosmetic only / C. Already separated**.

Candidate independence classification: **Invalid**.

Confidence: **High**.

Why it is rejected: these are public surface, registry, presentation, sorting, and metadata responsibilities. They are not safe implementation-local ownership recovery candidates. Extracting them would create naming churn or public-shape churn rather than a meaningful implementation boundary.

## Candidate boundaries found

How many recoverable candidates currently exist? **1**.

### Candidate 1: Important low-confidence edge selection

- Rank: **A. Strong implementation-backed next slice**.
- Classification: **Independent**.
- Confidence: **High**.
- Still-compressed ownership boundary: yes, the local selection of `important_low_confidence_edges` from filtered graph edges.
- Direct implementation support: yes, the current builder contains the sorted low-confidence importance-filtered list assembly and ten-row limit.
- Distinct from Operational Graph Slices 001-006: yes. It does not compose audit graph edges, create nodes, merge graph edges, assemble tier rows, or filter aggregate endpoints.
- Distinct from prior Emitter Attribution Audit slices: yes. It does not classify or assemble emitter attribution rows.
- Distinct from prior Emitter/Consumer Audit slices: yes. It does not scan emitted outputs, derive relationship status, or assemble emitter/consumer audit rows.
- Distinct from prior Consumer Dependency Audit slices: yes. It does not create consumer dependency audit item families or matched consumer groups.
- Distinct from prior Frontier Pressure Admission slices: yes. It does not admit, score, or select pressure candidates.
- Compatibility preservation: expected, if implemented as a private helper called from `build_operational_graph_confidence(...)` with unchanged JSON and text output.
- Valid without other candidates: yes.
- Why it is not a re-slice: it starts after existing graph composition, node registry, edge registry, tier summary, and aggregate filtering boundaries.
- Why it is not merely a name: it is a concrete output list with explicit selection predicates, row projection, and a bounded public result.

Fewer than three implementation-backed candidates are supported. Only one candidate is safe enough to recommend now.

## Rejected candidates and why

- Selected confidence-tier orchestration: rejected as **D. Cosmetic only** and likely a re-slice of Slice 003 adjacency.
- Confidence summary construction: ranked **B. Possible but needs caution**, but not counted as currently recoverable because it is public JSON-shape and diagnostic metadata adjacent. Reassess after the important-low slice.
- Taxonomy summary / aggregate connectivity: rejected as **C. Already separated / likely re-slice** because the public builder already owns taxonomy output and the remaining seams mix counting, sorting, naming, row projection, and metadata.
- Graph sorting: rejected as **D. Cosmetic only** because stable ordering is final assembly behavior, not an ownership boundary.
- Graph metadata construction: rejected as **D. Cosmetic only** because it is public compatibility metadata.
- Graph JSON output: rejected as **C. Already separated** because JSON conversion helpers and dataclass `to_json_dict(...)` methods already exist.
- Diagnostic inventory and diagnostic-shape registration: rejected as **C. Already separated** because registrations already exist and no new diagnostic surface is being added.
- CLI dispatch and formatter extraction: rejected as **D. Cosmetic only** because these are presentation/plumbing surfaces rather than implementation-local ownership recovery.

## Batch efficiency gate

- Recoverable candidates currently existing: **1**.
- Queue classification: **Single-slice target**.
- Efficiency batch: **No**. Three safe recoverable candidates do not exist.
- Protection batch: **No**. Two safe recoverable candidates do not exist. Running a batch is not worth it for speed or process protection because the second candidate would be summary-shape-adjacent and should be reassessed after the first slice.
- Stop/move-out: **Not yet**. One strong local Operational Graph candidate remains.
- Recommended batch size: **1**.

## Recommended next command

Run a single Operational Graph slice for **important low-confidence edge selection**.

The next command should recover only the helper that selects the operationally relevant low-confidence edge examples from already-filtered graph edges. It should preserve current behavior, including sorting by `_edge_sort_key`, requiring low confidence, requiring `_importance(edge)`, projecting through `_edge_example(edge, include_importance=True)`, and limiting `important_low_confidence_edges` to ten entries.

After that slice lands, reassess confidence summary construction before attempting any additional Operational Graph work. Do not batch taxonomy, CLI, JSON, metadata, diagnostic registration, sorting, or selected-tier orchestration with the next slice.

## Risk of re-slicing prior work

Risk is **medium** if the next command is too broad, because `build_operational_graph_confidence(...)` is adjacent to already recovered confidence tier row assembly and aggregate-edge filtering. Risk is **low** if the next command extracts only important low-confidence edge selection and keeps tier summaries, aggregate filtering, graph construction, taxonomy inclusion, summary metadata, JSON shape, CLI behavior, and diagnostics unchanged.

## Read-only scout statement

This scout did not intentionally change implementation files or test files. The only intended repository change is this scout report, `operational_graph_district_scout_002.md`.

## Scout report commit

Commit hash: `e72c4d00bb33577958c215ce2b9b879e55e93bb7`.
