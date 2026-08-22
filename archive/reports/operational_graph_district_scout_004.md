# Operational Graph District Scout 004

## District consistency verification

- Active district verified: **Operational Graph**.
- Latest relevant completed slice verified: **`operational_graph_slice_008.md`**.
- Latest local district scout verified: **`operational_graph_district_scout_003.md`**.
- Branch state did not point to another active district: `git status --short --branch` reported `## work` before this scout file was created.
- Local files support the requested sequence: `operational_graph_slice_008.md` is present and identifies the recovered Slice 008 boundary as Operational Graph confidence-analysis summary payload construction, and `operational_graph_district_scout_003.md` is present as the latest local scout before Slice 008.
- No available report, summary, branch state, or local file pointed this scout to another active district. No district mismatch was found.
- Unrelated district reports were ignored as authority. They were used only as explicit avoidance constraints where the prompt named prior recovered or exhausted boundaries.

## Current app evidence

Read-only app commands were run after Operational Graph Slice 008:

- `python scripts/seed_local.py --operational-graph | head -40` reported the active **Operational Graph** surface with 164 nodes, 284 edges, 255 `consumes` relationships, 29 `emits` relationships, and confidence counts of 29 high, 39 medium, and 216 low.
- `python scripts/seed_local.py --operational-graph-confidence --operational-graph-confidence-tier low --exclude-aggregate | head -100` reported the confidence view with low-confidence edges reduced to 0 after aggregate exclusion, no low-confidence relationship types, no common evidence, no uncertainty causes, no representative examples, and no operationally relevant low-confidence edges.
- `python scripts/seed_local.py --operational-graph-taxonomy | head -90` reported 164 nodes, 8 aggregate nodes, 156 concrete nodes, classification counts, and aggregate connectivity headed by `surface:state_build`, `surface:views`, and `surface:projection builders`.
- `python scripts/seed_local.py --diagnostic-inventory --json > /tmp/inv.json && python - <<'PY' ... PY` confirmed `operational_graph`, `operational_graph_taxonomy`, and `operational_graph_confidence` remain JSON-capable, non-recording, `record_scope=none`, non-event-ledger-writing, and non-mutating diagnostic surfaces.

These commands are evidence of current behavior only. They were not treated as authority for promoting presentation vocabulary into repository knowledge.

## Recently consumed Operational Graph boundaries respected

The following Operational Graph responsibilities are already recovered and unavailable:

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
- unfiltered confidence edge behavior;
- important low-confidence edge selection;
- already-filtered graph edge consumption;
- `_edge_sort_key` ordering for important-low selection;
- low-confidence-only important edge selection;
- `_importance(edge)` filtering;
- `_edge_example(edge, include_importance=True)` projection;
- ten-row `important_low_confidence_edges` limit;
- confidence-analysis summary payload construction;
- filtered edge count;
- filtered relationship-type counts;
- filtered confidence counts;
- total graph edge count;
- excluded aggregate edge count;
- `exclude_aggregate` summary flag;
- `read_only` summary flag;
- `writes_event_ledger` summary flag;
- `mutates_cluster` summary flag;
- selected confidence filter summary value.

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

This scout did not propose work in stopped or exhausted neighborhoods:

- Slice 035: `selection_path_audit` neighborhood exhausted.
- Slice 051: immediate diagnostic-shape pressure candidate-construction pocket exhausted.
- District Scout 004: immediate post-Slice-062 pressure-audit neighborhood exhausted for safe local recovery.
- Outward Scout 005: Frontier Pressure Admission pressure-audit district has zero immediate recoverable candidates.
- Consumer Dependency Audit District Scout 003: local Consumer Dependency Audit district has zero immediate recoverable candidates after Slice 003.
- Emitter/Consumer Audit District Scout 003: local Emitter/Consumer Audit district has zero immediate recoverable candidates after Slice 005.
- Emitter Attribution Audit District Scout 003: local Emitter Attribution Audit district has zero immediate recoverable candidates after Slice 004.

## Inspected Operational Graph neighborhoods

### 1. Confidence selected-tier orchestration

Implementation evidence:

- `build_operational_graph_confidence(...)` builds the graph, creates the node lookup, applies `_filter_aggregate_operational_graph_edges(...)`, computes `selected = ("high", "medium", "low") if confidence is None else (confidence,)`, then builds `tiers` by calling `_confidence_tier_summary(...)` for each selected tier.
- Tests already prove selected-tier public behavior through `--operational-graph-confidence low`, the `filtered_confidence` summary field, and the reduced `tiers` key set.

Scout finding: **D. Cosmetic only / C. likely re-slice**.

Candidate independence classification: **Invalid**.

Confidence: **High**.

Why it is rejected: the only remaining code is a small tuple-selection control-flow seam around the already recovered confidence tier row helper and the already recovered summary payload helper. Extracting it would mostly rename filter dispatch and would risk re-slicing Slice 003's tier assembly or Slice 008's selected-confidence summary value. It is not exactly one substantial implementation-local ownership boundary.

### 2. Taxonomy inclusion in confidence analysis

Implementation evidence:

- `build_operational_graph_confidence(...)` includes `"taxonomy": build_operational_graph_taxonomy(root)` in the public confidence-analysis payload.
- `build_operational_graph_taxonomy(...)` is already a public builder for taxonomy analysis, and `operational_graph_confidence_json(...)` returns the assembled analysis unchanged.
- Existing tests assert the confidence JSON contains `taxonomy`, that aggregate filtering leaves `filtered["taxonomy"] == full["taxonomy"]`, and that taxonomy summary node counts remain present in confidence analysis.

Scout finding: **D. Cosmetic only / C. already separated**.

Candidate independence classification: **Invalid**.

Confidence: **High**.

Why it is rejected: the taxonomy builder is already a distinct public Operational Graph surface. The confidence builder's remaining responsibility is only public payload inclusion. Extracting taxonomy inclusion would be JSON-shape or assembly churn, not recovery of a new implementation-local ownership boundary. It would also sit directly in a known risk area: taxonomy inclusion in confidence analysis.

### 3. Public confidence-analysis assembly and metadata pass-through

Implementation evidence:

- `build_operational_graph_confidence(...)` returns a dictionary containing `summary`, `tiers`, `taxonomy`, `important_low_confidence_edges`, and `metadata`.
- Four of those pieces are already delegated or public: `_operational_graph_confidence_summary_payload(...)`, `_confidence_tier_summary(...)`, `build_operational_graph_taxonomy(...)`, and `_important_low_confidence_edge_examples(...)`.
- `metadata` is copied directly from `graph.metadata`, and tests assert the public keys, read-only flags, event-ledger flags, mutation flags, and JSON round-trip behavior.

Scout finding: **D. Cosmetic only**.

Candidate independence classification: **Invalid**.

Confidence: **High**.

Why it is rejected: after Slice 008, this neighborhood is final result packaging and metadata pass-through. It is compatibility-sensitive public shape rather than a recoverable local algorithm or ownership boundary. A helper here would likely be named after the payload shape without owning new implementation logic.

### 4. Operational Graph taxonomy summary, aggregate connectivity, degree accounting, and node classification

Implementation evidence:

- `build_operational_graph_taxonomy(...)` counts classifications and node types, computes degree from graph edges, selects aggregate nodes, sorts aggregate connectivity by descending degree and id, projects public rows, and attaches `metadata`.
- `_node_classification(...)` and `_is_aggregate_surface(...)` already hold node classification decisions used during graph node creation.
- App evidence shows taxonomy output has real operational content: 8 aggregate nodes and aggregate connectivity headed by high-degree aggregate surfaces.

Scout finding: **B. Possible but needs caution**, not counted as currently recoverable.

Candidate independence classification: **Invalid for the next command**.

Confidence: **Medium**.

Why it is rejected for now: this is the only nearby neighborhood with more implementation than final assembly, but the remaining seams are interleaved public taxonomy shape, aggregate/concrete vocabulary, degree accounting, aggregate connectivity row projection, sorting, and metadata. Node classification was already part of Slice 004 node creation, and taxonomy inclusion is already public-surface behavior. A safe slice would need a more precise implementation-backed seam than this scout can support without re-slicing node classification or extracting presentation row assembly.

### 5. Graph sorting, graph metadata construction, graph JSON output, CLI dispatch, and diagnostic registration

Implementation evidence:

- `build_operational_graph(...)` sorts final nodes and edges and attaches graph metadata.
- `OperationalGraph.to_json_dict(...)`, `operational_graph_json(...)`, `operational_graph_confidence_json(...)`, and `operational_graph_taxonomy_json(...)` preserve public JSON shapes.
- CLI dispatch calls existing builders and formatters for `--operational-graph`, `--operational-graph-taxonomy`, and `--operational-graph-confidence`.
- Diagnostic inventory and diagnostic-shape registration already expose Operational Graph surfaces as read-only, JSON-capable, non-recording, non-event-ledger-writing, and non-mutating.

Scout finding: **D. Cosmetic only / C. already separated**.

Candidate independence classification: **Invalid**.

Confidence: **High**.

Why it is rejected: these are stable ordering, metadata literal, JSON pass-through, registry, and CLI plumbing responsibilities. They are compatibility surfaces and visibility registration, not implementation-local recovery candidates. No new diagnostic, audit, probe, view, CLI flag, or recordable output is being added by this scout.

## Candidate boundaries found

How many recoverable candidates currently exist? **0**.

No implementation-backed candidate is safe enough to recommend as the next local Operational Graph slice after Slice 008.

Fewer than three implementation-backed candidates are supported. In fact, fewer than one implementation-backed candidate is supported.

## Candidate independence classification summary

No valid candidates were found. The inspected possible candidates classify as follows:

- Confidence selected-tier orchestration: **Invalid**, confidence **High**. It is not a safe candidate because it is small control flow around already recovered tier row assembly and selected-confidence summary behavior. It would not be a re-slice only if it owned a distinct selection artifact, but the current implementation does not show such an artifact. It is merely a name because no durable data construction exists beyond choosing a tuple of tiers.
- Taxonomy inclusion in confidence analysis: **Invalid**, confidence **High**. It is not a safe candidate because taxonomy construction is already separated as `build_operational_graph_taxonomy(...)`, while inclusion in confidence analysis is public payload assembly. It would be a re-slice of public taxonomy surface or confidence payload assembly. It is merely a name because the remaining code only places an existing taxonomy payload under an existing key.
- Public confidence-analysis assembly and metadata pass-through: **Invalid**, confidence **High**. It is not a safe candidate because it is final JSON-compatible result packaging. It would be a re-slice of Slice 008 summary payload construction or prior delegated confidence helpers. It is merely a name because no separate algorithm remains beyond assembling already produced values.
- Taxonomy summary / aggregate connectivity / degree accounting: **Invalid for the next command**, confidence **Medium**. It might contain future implementation evidence, but this scout cannot isolate exactly one safe ownership boundary distinct from Slice 004 node classification and public taxonomy shape. It is not safe without other candidates because any extraction would need reassessment from implementation evidence after a broader district move or a more focused scout. It is not merely a name in the broad sense because degree counts and aggregate rows are real data, but the currently visible boundary is too broad and too public-shape-adjacent.
- Graph sorting, metadata, JSON output, CLI dispatch, and diagnostic registration: **Invalid**, confidence **High**. These are already separated or cosmetic compatibility surfaces and not recoverable ownership boundaries.

## Rejected candidates and why

- Selected confidence-tier orchestration: rejected as **D. Cosmetic only** and likely a re-slice of confidence tier assembly or selected-confidence summary behavior.
- Taxonomy inclusion in confidence analysis: rejected as **D/C** because taxonomy construction already exists and confidence inclusion is public assembly.
- Confidence metadata pass-through: rejected as **D. Cosmetic only** because it copies existing graph metadata into the public payload.
- Public confidence-analysis assembly: rejected as **D. Cosmetic only** because remaining work is final dictionary packaging from already delegated pieces.
- Taxonomy node classification: rejected as **C. Already separated / likely re-slice** because `_node_classification(...)` and `_is_aggregate_surface(...)` already support node creation and Slice 004 recovered node classification application.
- Taxonomy aggregate/concrete naming: rejected as **D. Cosmetic only** because it is presentation vocabulary and public taxonomy shape.
- Taxonomy degree accounting and aggregate connectivity: rejected as **B with caution but invalid now** because it is implementation-backed but too entangled with public taxonomy row projection, sorting, and metadata to identify exactly one safe local ownership boundary.
- Graph sorting: rejected as **D. Cosmetic only** because stable ordering is final assembly compatibility behavior.
- Graph metadata construction: rejected as **D. Cosmetic only** because it is a public compatibility literal.
- Graph JSON output: rejected as **C. Already separated** because JSON conversion methods and pass-through functions already exist.
- Diagnostic inventory and diagnostic-shape registration: rejected as **C. Already separated** because registrations already exist and no new operational surface is being added.
- CLI dispatch and formatter extraction: rejected as **D. Cosmetic only** because these are presentation/plumbing surfaces rather than implementation-local ownership recovery.

## Batch efficiency gate

- Recoverable candidates currently existing: **0**.
- Queue classification: **Stop/move-out**.
- Efficiency batch: **No**. Three safe recoverable candidates do not exist.
- Protection batch: **No**. Two safe recoverable candidates do not exist.
- Single-slice target: **No**. One safe candidate does not exist.
- Stop/move-out: **Yes**. No nearby implementation-backed Operational Graph slice candidate remains after Slice 008.
- Recommended batch size: **0**.

Running a batch is not worth it for speed or process protection. With zero safe candidates, a batch would only increase re-slice risk.

## Recommended next command

Recommended next move: **stop or move outward from the local Operational Graph district**.

The next command should not attempt an Operational Graph efficiency batch, protection batch, or single local slice from the neighborhoods inspected here. If work continues, it should either:

1. produce a stop report for the local Operational Graph district; or
2. move outward to a different district with fresh consistency gates and implementation evidence.

Do not use Operational Graph District Scout 003 candidate names as authority; Slice 008 consumed its only safe candidate.

## Risk of re-slicing prior work

Risk is **high** if the next command stays in the same local Operational Graph confidence neighborhood. The remaining nearby names mostly point to already recovered helpers, selected-filter control flow, public payload assembly, metadata pass-through, taxonomy presentation, or diagnostic/CLI plumbing. The specific re-slice risks are:

- re-slicing Slice 003 by renaming selected-tier orchestration around `_confidence_tier_summary(...)`;
- re-slicing Slice 004 by extracting taxonomy node classification or aggregate classification application;
- re-slicing Slice 006 by touching aggregate filtering behavior from taxonomy or confidence output;
- re-slicing Slice 007 by altering important-low-confidence examples or `_edge_example(...)` projection;
- re-slicing Slice 008 by extracting another public summary or result packaging helper;
- drifting into prior Emitter Attribution Audit, Emitter/Consumer Audit, Consumer Dependency Audit, or Frontier Pressure Admission districts through upstream audit inputs.

## Read-only implementation/test statement

No implementation files were changed.

No test files were changed.

This scout created and committed only `operational_graph_district_scout_004.md`.

## Scout report commit

Commit hash: `f360947bcae1ecbc24cb3fd09667f62fe16d624d`.
