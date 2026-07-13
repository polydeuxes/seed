# Operational Graph District Scout 003

## District consistency verification

- Active district verified: **Operational Graph**.
- Latest relevant completed slice verified: **`operational_graph_slice_007.md`**.
- Latest local district scout verified: **`operational_graph_district_scout_002.md`**.
- Branch state did not point to another active district: `git status --short --branch` reported `## work` before this scout file was created.
- Local files support the requested sequence: `operational_graph_slice_007.md` is present and names `operational_graph_district_scout_002.md` as the latest local district scout before Slice 007.
- No available report, summary, branch state, or local file pointed this scout to another active district. No district mismatch was found.
- Unrelated district reports were ignored as authority. They were used only as avoidance constraints where the prompt named prior recovered or exhausted boundaries.

## Current app evidence

Read-only app commands were run after Operational Graph Slice 007:

- `python scripts/seed_local.py --operational-graph | head -40` reported 164 nodes, 284 edges, 255 `consumes` relationships, 29 `emits` relationships, and confidence counts of 29 high, 39 medium, and 216 low.
- `python scripts/seed_local.py --operational-graph-confidence --operational-graph-confidence-tier low | head -90` reported 216 low-confidence edges, reference-only evidence, aggregate-target uncertainty, taxonomy uncertainty, representative examples, and the existing operationally relevant low-confidence edge section.
- `python scripts/seed_local.py --operational-graph-confidence --operational-graph-confidence-tier low --exclude-aggregate | head -80` reported zero low-confidence edges after aggregate exclusion, proving the confidence summary is currently built from already-filtered graph edges.
- `python scripts/seed_local.py --operational-graph-taxonomy | head -70` reported 164 nodes, 8 aggregate nodes, 156 concrete nodes, node classification counts, and aggregate connectivity headed by `surface:state_build` and `surface:views`.
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
- already-filtered graph edge consumption for important-low selection;
- `_edge_sort_key` ordering for important-low selection;
- low-confidence-only important edge selection;
- `_importance(edge)` filtering;
- `_edge_example(edge, include_importance=True)` projection;
- ten-row `important_low_confidence_edges` limit.

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

### 1. Confidence analysis summary construction

Implementation evidence:

- `build_operational_graph_confidence(...)` builds the graph, maps nodes, filters aggregate edges through `_filter_aggregate_operational_graph_edges(...)`, selects tiers, delegates tier row production to `_confidence_tier_summary(...)`, delegates important-low selection to `_important_low_confidence_edge_examples(...)`, and still locally constructs the public `summary` dictionary.
- The current local summary construction combines graph-level summary values with filtered-edge counts, filtered relationship-type counts, filtered confidence counts, total graph edge count, excluded aggregate edge count, the aggregate-exclusion flag, read-only flags, event-ledger flags, mutation flags, and the selected confidence filter.
- App evidence with `--exclude-aggregate` shows the summary is behaviorally tied to already-filtered graph edges rather than raw graph edges.

Scout finding: **A. Strong implementation-backed next slice**.

Candidate independence classification: **Independent**.

Confidence: **Medium**.

Exact narrow responsibility: build only the confidence-analysis `summary` payload from an already-built `OperationalGraph`, already-filtered graph edges, `exclude_aggregate`, and the selected confidence filter.

What it must not own: confidence tier row assembly, aggregate-edge filtering, important low-confidence edge selection, selected-tier orchestration, taxonomy inclusion, graph construction, JSON serialization, diagnostic registration, CLI plumbing, or formatting.

Why it is not a re-slice: it starts after graph construction and aggregate-edge filtering; it does not calculate tier rows from Slice 003, does not decide aggregate exclusion from Slice 006, and does not select important-low examples from Slice 007. It only assembles the top-level confidence summary counts and metadata from inputs that already exist.

Why it is not merely a name: tests and JSON output already depend on specific summary counts and flags such as `edges`, `relationship_types`, `confidence_counts`, `total_graph_edges`, `excluded_aggregate_edges`, `exclude_aggregate`, `read_only`, `writes_event_ledger`, `mutates_cluster`, and `filtered_confidence`. The boundary owns data construction, not vocabulary.

Would it remain valid without other proposed candidates? **Yes**. It can be recovered as a small private helper with unchanged public keys and values, while leaving taxonomy, selected-tier orchestration, important-low selection, formatting, CLI, JSON pass-through, diagnostics, and event-ledger behavior untouched.

Compatibility expectation: behavior, schema, CLI output, JSON output, diagnostic inventory, diagnostic-shape registration, event-ledger behavior, and read-only boundaries should be preserved if the slice only extracts the existing summary dict construction into a private helper and adds narrow preservation tests.

### 2. Confidence selected-tier orchestration

Implementation evidence:

- `build_operational_graph_confidence(...)` computes `selected = ("high", "medium", "low") if confidence is None else (confidence,)` and builds `tiers` by calling `_confidence_tier_summary(...)` for each selected tier.

Scout finding: **D. Cosmetic only**.

Candidate independence classification: **Invalid**.

Confidence: **Low**.

Why it is rejected: this is a very small control-flow expression around an already recovered tier-summary helper. Extracting it would mostly rename a public filter parameter and risks re-slicing Slice 003's confidence tier row assembly under an orchestration label. It is not enough implementation-local ownership to justify a slice.

### 3. Confidence reason and improvement text

Implementation evidence:

- `_confidence_reason(...)` and `_confidence_improvement(...)` already exist as separate helpers.
- `_confidence_tier_summary(...)` and `_edge_example(...)` consume those helpers to maintain consistent reason and improvement text across tier rows and edge examples.

Scout finding: **C. Already separated / likely re-slice**.

Candidate independence classification: **Invalid**.

Confidence: **High**.

Why it is rejected: the reason/improvement responsibility is already separated into helpers and was part of the consumed confidence tier row assembly boundary. Further work here would be wording or presentation churn, not recovery of a still-compressed implementation-local responsibility.

### 4. Operational Graph taxonomy summary and aggregate connectivity

Implementation evidence:

- `build_operational_graph_taxonomy(...)` already exists as the public taxonomy build boundary.
- It counts classifications and node types, computes node degree from graph edges, selects aggregate nodes, sorts aggregate connectivity by descending degree and id, projects public rows, and attaches summary metadata.

Scout finding: **B. Possible but needs caution**, not counted as currently recoverable.

Candidate independence classification: **Invalid for the next command**.

Confidence: **Medium-Low**.

Why it is rejected for now: this neighborhood is implementation-backed, but remaining seams mix public taxonomy shape, classification vocabulary, aggregate/concrete naming, degree accounting, aggregate connectivity rows, sorting, and metadata. Those are known risk areas. The existing builder is already an explicit taxonomy boundary, and a smaller extraction would likely recover public row projection or sorting rather than one clearly isolated ownership boundary.

### 5. Graph sorting, metadata, JSON output, CLI dispatch, and diagnostic registration

Implementation evidence:

- `build_operational_graph(...)` sorts final nodes and edges and attaches metadata.
- `OperationalGraph.to_json_dict(...)`, `operational_graph_json(...)`, `operational_graph_confidence_json(...)`, and `operational_graph_taxonomy_json(...)` preserve public JSON shapes.
- CLI dispatch calls existing builders and formatters.
- Diagnostic inventory and diagnostic-shape registration already expose Operational Graph surfaces as read-only, JSON-capable, non-recording, non-event-ledger-writing, and non-mutating.

Scout finding: **D. Cosmetic only / C. Already separated**.

Candidate independence classification: **Invalid**.

Confidence: **High**.

Why it is rejected: these are public surface, registry, presentation, sorting, and metadata responsibilities. They are not safe implementation-local recovery candidates. Extracting them would create naming churn or public-shape churn rather than a meaningful ownership boundary.

## Candidate boundaries found

How many recoverable candidates currently exist? **1**.

### Candidate 1: Confidence-analysis summary payload construction

- Rank: **A. Strong implementation-backed next slice**.
- Classification: **Independent**.
- Confidence: **Medium**.
- Still-compressed ownership boundary: yes, construction of the top-level `summary` payload inside `build_operational_graph_confidence(...)`.
- Direct implementation support: yes, the current builder locally constructs filtered counts and read-only/ledger/mutation metadata for the confidence analysis summary.
- Distinct from Operational Graph Slices 001-007: yes. It does not compose audit graph nodes or edges, create graph nodes, merge graph edges, assemble tier rows, filter aggregate endpoints, or select important low-confidence examples.
- Distinct from prior Emitter Attribution Audit slices: yes. It does not classify emitters or build emitter attribution rows.
- Distinct from prior Emitter/Consumer Audit slices: yes. It does not scan emitted outputs, derive emitted-output relationship status, or assemble Emitter/Consumer Audit rows.
- Distinct from prior Consumer Dependency Audit slices: yes. It does not create consumer dependency audit item families or matched consumer groups.
- Distinct from prior Frontier Pressure Admission slices: yes. It does not admit, score, select, or construct pressure candidates.
- Compatibility preservation: expected if implemented as a private helper that returns the same summary keys and values from the same inputs.
- Valid without other candidates: yes.
- Why it is not a re-slice: it consumes results from prior boundaries rather than owning them; it only assembles the summary payload after graph construction and edge filtering and alongside already delegated tier and important-low helpers.
- Why it is not merely a name: the summary payload contains tested counts and operational boundary flags, including filtered edge counts, excluded aggregate edge counts, selected confidence, read-only status, event-ledger status, and mutation status.

Fewer than three implementation-backed candidates are supported. Only one candidate is safe enough to recommend now.

## Rejected candidates and why

- Selected confidence-tier orchestration: rejected as **D. Cosmetic only** and likely a re-slice of confidence tier assembly adjacency.
- Confidence reason and improvement text: rejected as **C. Already separated / likely re-slice** because `_confidence_reason(...)` and `_confidence_improvement(...)` already exist and are consumed by prior confidence-summary surfaces.
- Taxonomy summary / aggregate connectivity: rejected as **B/C with caution** because remaining seams are public taxonomy shape, aggregate naming, degree accounting, row projection, sorting, and metadata rather than one safe implementation-local boundary.
- Graph sorting: rejected as **D. Cosmetic only** because stable ordering is final assembly behavior, not a recoverable ownership boundary.
- Graph metadata construction: rejected as **D. Cosmetic only** because it is public compatibility metadata.
- Graph JSON output: rejected as **C. Already separated** because JSON conversion helpers and dataclass `to_json_dict(...)` methods already exist.
- Diagnostic inventory and diagnostic-shape registration: rejected as **C. Already separated** because registrations already exist and no new diagnostic surface is being added.
- CLI dispatch and formatter extraction: rejected as **D. Cosmetic only** because these are presentation/plumbing surfaces rather than implementation-local ownership recovery.

## Batch efficiency gate

- Recoverable candidates currently existing: **1**.
- Queue classification: **Single-slice target**.
- Efficiency batch: **No**. Three safe recoverable candidates do not exist.
- Protection batch: **No**. Two safe recoverable candidates do not exist. Running a batch is not worth it for speed or process protection because the second candidate would be taxonomy/public-shape-adjacent or a likely re-slice.
- Stop/move-out: **Not yet**. One local Operational Graph candidate remains.
- Recommended batch size: **1**.

If process protection is desired, it should come from tight slice wording and narrow tests, not batching. A batch would increase re-slice risk without saving command count.

## Recommended next command

Run a single Operational Graph slice for **confidence-analysis summary payload construction**.

The next command should recover only a helper that constructs the existing confidence-analysis `summary` dictionary from `graph`, already-filtered `graph_edges`, `exclude_aggregate`, and `confidence`. It should preserve all existing keys and values, including filtered edge counts, relationship counts, confidence counts, total graph edge count, excluded aggregate edge count, selected confidence, read-only status, event-ledger status, and mutation status.

Do not include confidence tier row assembly, aggregate-edge filtering, important low-confidence edge selection, selected-tier orchestration, taxonomy inclusion, graph construction, JSON serialization, diagnostic registration, CLI dispatch, formatting, taxonomy degree accounting, or graph metadata in the next slice.

## Risk of re-slicing prior work

Risk is **medium** because `build_operational_graph_confidence(...)` sits next to already recovered confidence tier assembly, aggregate filtering, and important-low selection. Risk is **low-to-medium** if the next slice is limited to the exact summary payload helper and tests assert unchanged summary behavior without touching tiers, taxonomy, important-low rows, CLI dispatch, diagnostic registration, or JSON pass-through.

## Scout write boundary

No implementation files were changed.

No test files were changed.

Only this scout report markdown file was created for commit.

## Scout report commit

Commit hash for the scout report commit: recorded by the git commit containing this file and reported in the final response. Embedding the final commit hash inside the committed file would change the commit hash itself.
