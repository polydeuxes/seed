# Operational Graph District Scout 001

## District consistency verification

- Active district verified: **Operational Graph**.
- Latest relevant completed slice verified: **`operational_graph_slice_003.md`**.
- Completed handoff source verified: **`emitter_attribution_audit_outward_scout_004.md`**.
- Branch state did not point to another active district: `git status --short --branch` reported `## work` before this scout file was created.
- Local files support the same district sequence: `operational_graph_slice_001.md`, `operational_graph_slice_002.md`, and `operational_graph_slice_003.md` are present, and Slice 003 states that taxonomy, formatting, JSON pass-through, CLI dispatch, and diagnostic registration were left untouched rather than recovered.
- Unrelated district reports were ignored as authority. They were used only as avoidance constraints where they named prior recovered or exhausted boundaries.

## Current app evidence

Read-only app commands were run to verify the current surface:

- `python scripts/seed_local.py --operational-graph` reported 164 nodes, 284 edges, 29 high-confidence edges, 39 medium-confidence edges, and 216 low-confidence edges.
- `python scripts/seed_local.py --operational-graph-confidence --operational-graph-confidence-tier low` reported 216 low-confidence consumes edges, reference-only evidence, aggregate-target uncertainty, attribution uncertainty, and the current important low-confidence edge list.
- `python scripts/seed_local.py --operational-graph-taxonomy` reported 164 nodes, 8 aggregate nodes, 156 concrete nodes, and aggregate connectivity headed by `surface:state_build` and `surface:views`.

These commands were evidence of current behavior only. They were not treated as authority for promoting presentation vocabulary into knowledge.

## Inspected Operational Graph neighborhoods

### 1. `build_operational_graph(...)` graph node creation

Implementation evidence:

- `build_operational_graph(...)` owns a local `nodes` registry and a nested `node(kind, label)` factory.
- The nested factory constructs the stable node id from kind and label, inserts an `OperationalGraphNode` only if absent, applies `_node_classification(kind, label)`, and returns the id for downstream composition.
- Both already recovered composition helpers consume this callback rather than owning node registry semantics.

Scout finding: this is a still-compressed implementation-local ownership boundary. It is not emitter/consumer composition, consumer-dependency composition, confidence tier assembly, taxonomy reporting, JSON serialization, CLI dispatch, or diagnostic registration.

### 2. `build_operational_graph(...)` graph edge creation and duplicate-edge merging

Implementation evidence:

- `build_operational_graph(...)` owns a local `edges` registry and a nested `add_edge(...)` accumulator.
- The accumulator omits evidence-free edges, keys edges by `(source, target, edge_type)`, creates new `OperationalGraphEdge` values, merges duplicate evidence with order-preserving de-duplication, and preserves the stronger confidence via `_stronger(...)`.
- Prior Slices 001 and 002 recovered each composition helper's participation in duplicate-edge merging, but did not recover the merge owner itself.

Scout finding: this is a still-compressed implementation-local ownership boundary. It must be kept separate from audit item-to-graph composition already recovered in Slices 001 and 002.

### 3. Confidence analysis aggregate-edge filtering

Implementation evidence:

- `build_operational_graph_confidence(...)` builds the graph, maps nodes by id, and locally filters `graph.edges` when `exclude_aggregate` is true.
- The filter removes edges with aggregate source or target nodes before tier summary assembly, important low-confidence selection, and summary metadata construction.
- Slice 003 recovered `_confidence_tier_summary(...)`; it explicitly left graph construction, aggregate filtering, selected-tier orchestration, important low-confidence edge selection, taxonomy inclusion, metadata, and public analysis assembly in `build_operational_graph_confidence(...)`.

Scout finding: this is a possible implementation-local boundary, but it is narrower and riskier than the graph node and edge registry boundaries because it sits inside public confidence analysis assembly and is adjacent to filtering flags and summary totals.

### 4. Operational Graph taxonomy summary

Implementation evidence:

- `build_operational_graph_taxonomy(...)` already exists as a public build boundary for taxonomy analysis.
- Its remaining body counts classifications, counts node types, computes degree, selects aggregate nodes, builds aggregate connectivity rows, and returns summary metadata.

Scout finding: rejected for the next command. This is implementation-backed, but the currently visible seam is a public analysis assembly body rather than exactly one still-compressed local ownership boundary. It mixes count production, degree accounting, row projection, sorting, and metadata. Recovering it now risks extracting presentation/summary shape rather than a narrow ownership boundary.

### 5. Formatting, JSON pass-through, CLI dispatch, diagnostic inventory, and diagnostic-shape registration

Implementation evidence:

- JSON helpers are pass-through functions over existing data structures or analysis dictionaries.
- Formatting functions render public presentation text.
- CLI dispatch invokes the already registered builders and formatters.
- Diagnostic inventory and diagnostic-shape specs already register `operational_graph`, `operational_graph_taxonomy`, and `operational_graph_confidence` as read-only, JSON-capable, non-recording, non-mutating surfaces.

Scout finding: rejected. These are public surface, registry, or presentation responsibilities. They are not safe implementation-local ownership recovery candidates for this scout.

## Recently consumed Operational Graph boundaries respected

The following Operational Graph boundaries are treated as already recovered and unavailable:

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
- confidence tier important low-confidence edge participation, if recovered by Slice 003.

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

- selection path audit;
- immediate diagnostic-shape pressure candidate construction;
- post-Slice-062 pressure-audit neighborhood;
- Frontier Pressure Admission pressure-audit district;
- local Consumer Dependency Audit after Slice 003;
- local Emitter/Consumer Audit after Slice 005;
- local Emitter Attribution Audit after Slice 004.

## Candidate boundaries found

### Candidate 1 — A. Strong implementation-backed next slice: graph node registry / node creation

- Classification: **Independent**.
- Confidence: **High**.
- Recoverable candidate count contribution: **1**.
- Ownership boundary: node id construction, node de-duplication, `OperationalGraphNode` construction, classification application, and id return for graph composition.
- Direct implementation support: local `node(kind, label)` inside `build_operational_graph(...)`.
- Distinct from Operational Graph Slices 001-003: yes. Slices 001 and 002 recovered audit-specific composition through the callback; Slice 003 recovered confidence tier row assembly. This candidate recovers the shared node registry owner, not either audit composition or confidence summary rows.
- Distinct from prior Emitter Attribution, Emitter/Consumer, Consumer Dependency, and Frontier Pressure Admission slices: yes. It does not scan source evidence, build upstream audit rows, admit pressure candidates, or select pressure item sets.
- Compatibility preservation: a helper extraction can preserve node ids, classification, de-duplication, ordering, JSON shape, CLI output, diagnostic inventory behavior, event-ledger behavior, and read-only boundaries.
- Would still be valid if other proposed candidates were not recovered: **yes**.
- Why it is not a re-slice: prior slices used the node callback but did not recover the callback's registry ownership.
- Why it is not merely a name: implementation evidence includes concrete construction and de-duplication behavior, not just a label or taxonomy term.

### Candidate 2 — A. Strong implementation-backed next slice: graph edge registry / duplicate-edge merging

- Classification: **Independent**.
- Confidence: **High**.
- Recoverable candidate count contribution: **1**.
- Ownership boundary: evidence presence guard, edge key construction, edge insertion, duplicate evidence merge, and stronger-confidence selection.
- Direct implementation support: local `add_edge(...)` inside `build_operational_graph(...)` plus `_stronger(...)`.
- Distinct from Operational Graph Slices 001-003: yes. Slices 001 and 002 recovered audit-specific edge production and merge participation; they did not recover the shared duplicate-edge merge owner. Slice 003 is confidence tier analysis, not graph edge accumulation.
- Distinct from prior Emitter Attribution, Emitter/Consumer, Consumer Dependency, and Frontier Pressure Admission slices: yes. It operates only after upstream audits produce completed items and before public graph sorting/metadata.
- Compatibility preservation: a helper extraction can preserve omission of evidence-free edges, de-duplicated evidence ordering, confidence strengthening, graph JSON shape, CLI output, diagnostic inventory behavior, event-ledger behavior, and read-only boundaries.
- Would still be valid if other proposed candidates were not recovered: **yes**.
- Why it is not a re-slice: prior recovered boundaries feed `add_edge`; this candidate owns how duplicate graph edges are normalized.
- Why it is not merely a name: implementation evidence includes merge logic and confidence conflict resolution.

### Candidate 3 — B. Possible but needs caution: confidence aggregate-edge filtering

- Classification: **Independent**, but should be reassessed after any graph-builder slice that changes surrounding structure.
- Confidence: **Medium**.
- Recoverable candidate count contribution: **1**, with caution.
- Ownership boundary: filtering graph edges according to aggregate endpoint presence when `exclude_aggregate` is requested.
- Direct implementation support: local `nodes = {node.id: node for node in graph.nodes}` and `graph_edges = tuple(...)` in `build_operational_graph_confidence(...)`.
- Distinct from Operational Graph Slices 001-003: yes. Slice 003 moved tier row assembly into `_confidence_tier_summary(...)` and explicitly left aggregate filtering in the public confidence builder.
- Distinct from prior Emitter Attribution, Emitter/Consumer, Consumer Dependency, and Frontier Pressure Admission slices: yes. It analyzes completed Operational Graph edges and does not alter upstream audit evidence or pressure-admission behavior.
- Compatibility preservation: possible if extracted as a private helper that returns the same filtered edge tuple and keeps summary totals, filtered confidence, taxonomy inclusion, important low-confidence selection, JSON shape, CLI flags, diagnostics, and read-only metadata unchanged.
- Would still be valid if other proposed candidates were not recovered: **yes**. It only depends on the public `OperationalGraph` object and node aggregate classification.
- Why it is not a re-slice: it is not confidence tier row assembly; it determines the edge set before tier summaries are built.
- Why it is not merely a name: implementation evidence includes actual conditional filtering over graph edges and aggregate endpoint predicates.

## Rejected candidates

### C. Already separated / likely re-slice: emitter/consumer audit graph composition

Rejected because Slice 001 already recovered this boundary into `_compose_emitter_consumer_audit_graph(...)`.

### C. Already separated / likely re-slice: consumer-dependency audit graph composition

Rejected because Slice 002 already recovered this boundary into `_compose_consumer_dependency_audit_graph(...)`.

### C. Already separated / likely re-slice: confidence tier row assembly

Rejected because Slice 003 already recovered this boundary into `_confidence_tier_summary(...)`.

### B/C. Taxonomy summary sub-extraction

Rejected for the immediate next command. It is implementation-backed, but not currently narrow enough: count production, degree accounting, aggregate row creation, sorting, summary metadata, and public taxonomy shape are compressed together. A future scout could reassess it after safer builder-local boundaries are recovered, but using it now risks a presentation or summary-shape extraction.

### D. Cosmetic only: graph JSON output helpers

Rejected because `operational_graph_json(...)`, `operational_graph_confidence_json(...)`, and `operational_graph_taxonomy_json(...)` are pass-through public JSON surfaces, not compressed implementation-local ownership boundaries.

### D. Cosmetic / public surface only: formatters

Rejected because formatting owns presentation vocabulary and output layout. The prompt warns that presentation vocabulary is not automatically repository knowledge.

### D. Registry/plumbing only: CLI dispatch, diagnostic inventory, and diagnostic-shape registration

Rejected because the surfaces already exist as read-only diagnostics. Changing them would be operational visibility work, not recovery of a hidden implementation-local Operational Graph responsibility.

### D. Sorting and metadata literals

Rejected because final graph sorting and metadata construction are public output-shape stabilization, not currently a strong implementation-local ownership seam.

## Batch Efficiency Gate

How many recoverable candidates currently exist?

**3**, with two high-confidence independent candidates and one medium-confidence independent candidate that needs caution.

Candidate summary:

1. Graph node registry / node creation — **Independent**, **High confidence**, **A. Strong implementation-backed next slice**.
2. Graph edge registry / duplicate-edge merging — **Independent**, **High confidence**, **A. Strong implementation-backed next slice**.
3. Confidence aggregate-edge filtering — **Independent**, **Medium confidence**, **B. Possible but needs caution**.

Current queue classification: **Efficiency batch** is available because three recoverable candidates exist with enough implementation evidence to attempt a guarded batch.

Recommended batch size: **2 or 3 depending on risk tolerance**.

- Recommended safer guarded batch: **2 slices** for Candidate 1 and Candidate 2. This protects the graph builder's shared registry behavior while avoiding the higher-risk confidence filtering seam.
- Full efficiency batch: **3 slices** is possible if the next command explicitly supports reassessing Candidate 3 after the graph-builder slices land. Candidate 3 should be skipped if either builder-local slice changes confidence-builder assumptions.

If the process prioritizes correctness protection over command-count savings, a two-candidate protection batch is reasonable. If the process prioritizes command-count efficiency and supports reassessment between slices, a three-candidate efficiency batch is supportable.

## Recommended next command

Recommended next command: **Operational Graph guarded batch**.

Recommended order:

1. Recover graph edge registry / duplicate-edge merging or graph node registry / node creation from `build_operational_graph(...)` into a private compatibility-preserving helper.
2. Recover the remaining graph-builder registry helper.
3. Reassess confidence aggregate-edge filtering; recover it only if it remains a narrow helper after the graph-builder changes land.

Next move classification: **Efficiency batch available**, with a safer **protection batch** of the two high-confidence graph-builder candidates.

## Risk of re-slicing prior work

Overall risk: **medium**.

- Low risk for Candidate 1 if the slice stays strictly on node registry behavior and does not move audit-specific node mapping out of `_compose_emitter_consumer_audit_graph(...)` or `_compose_consumer_dependency_audit_graph(...)`.
- Low-to-medium risk for Candidate 2 if the slice stays strictly on edge normalization and does not rework direct emits, indirect consumes, reference evidence, or low-confidence edge production.
- Medium risk for Candidate 3 because confidence filtering is adjacent to summary totals, selected-tier orchestration, important low-confidence edge selection, taxonomy inclusion, and public JSON shape.

## Scout constraints observed

- No implementation files were changed.
- No test files were changed.
- No slice report was created.
- No PR metadata was created before commit.
- The only intended repository change is this scout report: `operational_graph_district_scout_001.md`.

## Commit

Scout report commit hash: `8438ae189b832595d2a42643bc8b9fa7bbf496c0`.
