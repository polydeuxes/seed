# Operational Graph Outward Scout 005

## District consistency verification

- Completed local district verified: **Operational Graph**.
- Latest relevant completed slice verified: **`operational_graph_slice_008.md`**.
- Latest local district scout verified: **`operational_graph_district_scout_004.md`**.
- `git status --short --branch` reported branch `work` with no local implementation or test changes before this report was created.
- `operational_graph_slice_008.md` identifies Slice 008 as Operational Graph confidence-analysis summary payload construction.
- `operational_graph_district_scout_004.md` reports 0 recoverable Operational Graph candidates, no efficiency batch, no protection batch, no single-slice target, stop/move-out, and recommended batch size 0.
- No available report, summary, branch state, or local file pointed to another active district. No mismatch was found.
- Unrelated district reports were not used as authority. They were used only as explicit avoidance constraints where the prompt named stopped, exhausted, or recently consumed boundaries.

## Current app evidence

Read-only app evidence gathered after Operational Graph Slice 008 and Operational Graph District Scout 004:

- `python scripts/seed_local.py --diagnostic-inventory --json` reported 56 diagnostic inventory entries. The adjacent entries include `knowledge_reachability`, `operational_graph`, `operational_graph_taxonomy`, `operational_graph_confidence`, `question_surface_inventory`, `diagnostic_shape_audit`, `projection_shape`, and `implementation_trait_characterization`.
- The same inventory reports `operational_graph`, `operational_graph_taxonomy`, and `operational_graph_confidence` as JSON-capable, non-recording, `record_scope=none`, non-event-ledger-writing, and non-mutating.
- `python scripts/seed_local.py --operational-graph --json` reported 164 nodes, 284 edges, 255 `consumes` relationships, 29 `emits` relationships, and confidence counts of 29 high, 39 medium, and 216 low.
- `python scripts/seed_local.py --operational-graph-confidence --exclude-aggregate --json` reported 29 filtered edges, 255 excluded aggregate edges, relationship types limited to `emits`, `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`.
- `python scripts/seed_local.py --operational-graph-taxonomy --json` reported 164 nodes, 8 aggregate nodes, 156 concrete nodes, 284 edges, and the same read-only/no-ledger/no-mutation flags.
- `python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-json --knowledge-reachability-audit-limit 20` reported candidate discovery, index construction, evaluation, timing, source counts, scan counts, candidate-kind counts, loss-stage counts, and a source-navigation-derived index phase. With the current empty projected state it evaluated 20 candidates, saw default seed and docs sources, and reported `source_navigation.index_from_fact_support` as an index phase with 0 source-navigation terms.
- `python scripts/seed_local.py --question-surface-inventory --json` reported 17 question-family inventory rows, including the `knowledge reachability` bounded question family mapped to the `knowledge_reachability` diagnostic surface.

This app evidence is behavioral evidence only. It is not authority for promoting presentation vocabulary into repository knowledge.

## Exhausted neighborhoods respected

This scout respected and did not propose work in these stopped or exhausted neighborhoods:

- Slice 035: `selection_path_audit` neighborhood exhausted.
- Slice 051: immediate diagnostic-shape pressure candidate-construction pocket exhausted.
- District Scout 004: immediate post-Slice-062 pressure-audit neighborhood exhausted for safe local recovery.
- Outward Scout 005: Frontier Pressure Admission pressure-audit district has zero immediate recoverable candidates.
- Consumer Dependency Audit District Scout 003: local Consumer Dependency Audit district has zero immediate recoverable candidates after Slice 003.
- Emitter/Consumer Audit District Scout 003: local Emitter/Consumer Audit district has zero immediate recoverable candidates after Slice 005.
- Emitter Attribution Audit District Scout 003: local Emitter Attribution Audit district has zero immediate recoverable candidates after Slice 004.
- Operational Graph District Scout 004: local Operational Graph district has zero immediate recoverable candidates after Slice 008.

## Recently consumed boundaries respected

Unavailable Operational Graph boundaries were treated as consumed: emitter/consumer audit graph composition, consumer-dependency audit graph composition, confidence tier row assembly, graph node registry and node creation, graph edge registry and duplicate-edge merging, confidence aggregate-edge filtering, important low-confidence edge selection, confidence-analysis summary payload construction, graph node id construction, node de-duplication, node classification application, edge evidence-free omission, duplicate evidence merge ordering, stronger-confidence preservation, aggregate-edge exclusion, important-low edge ordering/projection/limit, filtered edge count summary, relationship-type count summary, confidence count summary, excluded aggregate edge count summary, read-only/event-ledger/mutation summary flags, and selected confidence filter summary value.

Prior Emitter Attribution Audit, Emitter/Consumer Audit, Consumer Dependency Audit, and Frontier Pressure Admission boundaries named by the prompt were also treated as unavailable.

## Inspected outward neighborhoods

### 1. Diagnostic inventory and diagnostic shape consumers of Operational Graph surfaces

Implementation evidence:

- `seed_runtime/diagnostic_inventory.py` registers `operational_graph`, `operational_graph_taxonomy`, and `operational_graph_confidence` with read-only/no-record/no-ledger/no-mutation shape.
- `seed_runtime/diagnostic_shape_audit.py` has implementation specs for those same surfaces.
- Tests already assert the inventory and shape-audit visibility for the Operational Graph surfaces.

Finding: **C. Already separated / likely re-slice**.

Classification: **Invalid**. Confidence: **High**.

Reason: registration/spec plumbing is already visible and was explicitly rejected by Operational Graph District Scout 004. No new operational surface is being added by this scout.

### 2. Question Surface Inventory as a downstream visibility consumer

Implementation evidence:

- `seed_runtime/question_surface_inventory.py` imports `DIAGNOSTIC_INVENTORY` and `IMPLEMENTATION_SPECS`.
- It maps `knowledge reachability` to `knowledge_reachability_audit`, canonicalizes that dispatch surface back to `knowledge_reachability`, and uses bounded ask maps/status to enrich question-family rows.
- It does not dispatch to Operational Graph surfaces as question families.

Finding: **C. Already separated / likely re-slice**.

Classification: **Invalid**. Confidence: **High**.

Reason: the implementation-backed seams here belong to the already active question-bounded-work district, where multiple slices already recovered exact lookup, eligibility, selected surface value, dispatch surface selection, presentation handoff, dispatch request, dispatch result, and knowledge-reachability JSON compatibility. Re-entering from Operational Graph would risk re-slicing bounded ask or inventory enrichment rather than finding a fresh adjacent Operational Graph consumer.

### 3. Knowledge Reachability audit as an outward adjacent district

Implementation evidence:

- Diagnostic inventory declares `knowledge_reachability` as a read-only audit across projected, repository, inquiry, and rendered surfaces, using both projected state and repository files.
- `seed_runtime/knowledge_reachability.py` implements a broad audit result builder that performs candidate discovery, index construction, candidate evaluation, metadata assembly, and table/JSON rendering.
- The audit has an implementation-backed source-navigation adjacency: `_build_indexes(...)` records `source_navigation.index_from_fact_support`, and `_discover_candidates(...)` scans `source-navigation terms` from fact support.
- The app run showed those phases and counts even when the current state had no fact support rows.

Finding: **A. Strong implementation-backed next slice district**, with three candidate boundaries below.

Classification: fresh **different-district handoff** to Knowledge Reachability. Confidence: **Medium-High**.

Reason: this is outside the exhausted Operational Graph district but still adjacent through the repository's visibility discipline: Operational Graph and Knowledge Reachability are both diagnostic inventory surfaces, and Knowledge Reachability is the explicit implementation evidence required by AGENTS.md before promoting presentation vocabulary. It is not local Operational Graph mining.

### 4. Source Navigation as a fact-support read-model adjacency

Implementation evidence:

- `seed_runtime/source_navigation.py` builds source navigation views from projected `defines` and `imports` fact support.
- `seed_runtime/knowledge_reachability.py` consumes source-navigation-shaped terms without calling `build_source_navigation(...)` in the current index path.
- Tests for `source_navigation` already cover private query preparation, composition, repository artifact definition/dependency/support/non-claims explanations, JSON, and formatting.

Finding: **B. Possible but needs caution**, not counted as the immediate next district queue.

Classification: **Sequential / invalid for this scout's next command**. Confidence: **Medium**.

Reason: Source Navigation is adjacent through Knowledge Reachability's source-navigation term index, but direct Source Navigation work risks re-slicing already tested query handoff, composition, explanation, and formatter responsibilities. It should be reassessed only after any Knowledge Reachability source-navigation-term boundary is recovered or rejected.

### 5. Architecture Conformance Audit as an Operational Graph graph consumer

Implementation evidence:

- `seed_runtime/architecture_conformance_audit.py` imports `OperationalGraph` and `build_operational_graph`.
- It accepts an optional graph or builds an Operational Graph, then evaluates architecture conformance using graph evidence.
- This is a real downstream consumer of Operational Graph output, but it is a broader conformance district and not directly indicated by the latest Operational Graph district scout as the next local area.

Finding: **B. Possible but needs caution**.

Classification: **Sequential / different-district candidate, not part of this batch**. Confidence: **Medium-Low**.

Reason: the consumer relationship is implementation-backed, but this scout did not inspect enough of the conformance implementation to isolate a safe one-boundary slice without drifting into a new audit district. It should be the subject of a separate consistency gate if Knowledge Reachability is not pursued.

## Candidate boundaries found

How many recoverable candidates currently exist? **3**.

The recoverable queue is in the **Knowledge Reachability** district, not in the exhausted Operational Graph district.

### Candidate 1 — Knowledge Reachability candidate discovery and source-budget admission

Rank: **A. Strong implementation-backed next slice**.

- Boundary: `_discover_candidates(...)` owns candidate admission across default seeds, event payloads, projected state, source-navigation terms, `docs/`, and `seed_runtime/`, with source budgets, global limit handling, subject bypass, raw-seen counts, source counts, scan counts, and truncation state.
- Independent / Sequential / Invalid: **Independent**.
- Confidence: **High**.
- Still valid without the others: **Yes**. Candidate discovery can be recovered without changing index construction or row evaluation.
- Why it is not a re-slice: it does not compose Operational Graph nodes or edges, confidence rows, important-low examples, emitter/consumer rows, consumer dependency rows, emitter attribution rows, or Frontier Pressure Admission payloads. It owns candidate intake for a different audit surface.
- Why it is not merely a name: implementation evidence shows concrete loops, source budgets, counters, scan counts, truncation behavior, and source-count metadata feeding the public audit result.
- Compatibility preservation expected: a narrow extraction/test should preserve CLI flags, JSON metadata, table output, read-only behavior, event-ledger behavior, and mutation flags.

### Candidate 2 — Knowledge Reachability index construction across staged surfaces

Rank: **A. Strong implementation-backed next slice**.

- Boundary: `_build_indexes(...)` owns construction of preserved, projected, read-model, source-navigation, and inquiry term indexes, including phase timing and index-timing metadata.
- Independent / Sequential / Invalid: **Independent**, but should be reassessed after Candidate 1 if batched sequentially.
- Confidence: **High**.
- Still valid without the others: **Yes**. Index construction consumes events/state and returns `_AuditIndexes`; it does not require candidate discovery changes.
- Why it is not a re-slice: it does not recover graph metadata, graph taxonomy, graph confidence, diagnostic inventory registration, or bounded ask dispatch. It owns reachability stage indexes for a distinct diagnostic.
- Why it is not merely a name: implementation evidence shows multiple staged index producers, timing phases, counters, source-navigation term integration, and a returned `_AuditIndexes` artifact consumed by evaluation.
- Compatibility preservation expected: a narrow recovery can keep all row booleans, timing keys, JSON metadata, human output, and read-only/no-mutation boundaries unchanged.

### Candidate 3 — Knowledge Reachability candidate stage evaluation and first-loss row production

Rank: **B. Possible but needs caution**.

- Boundary: the evaluation loop in `build_knowledge_reachability_audit_result(...)` applies `_candidate_flags_from_indexes(...)`, `_candidate_kind(...)`, `_first_loss(...)`, deadline/progress checks, and row construction for each sorted candidate.
- Independent / Sequential / Invalid: **Sequential**. It is likely safe only after Candidate 1 or Candidate 2 is recovered, because its clean boundary depends on stable candidate and index handoffs.
- Confidence: **Medium**.
- Still valid without the others: **Probably yes as a concept, but not recommended first**. It should be reassessed after one earlier Knowledge Reachability slice lands.
- Why it is not a re-slice: it does not change candidate source discovery, index construction, Operational Graph confidence, taxonomy, edge filtering, or prior audit districts. It owns per-candidate reachability row production for Knowledge Reachability.
- Why it is not merely a name: implementation evidence shows concrete stage booleans, candidate kind classification, first-loss classification, progress/deadline handling, and `KnowledgeReachabilityRow` construction.
- Compatibility preservation expected: recovery must preserve row order, row fields, truncation behavior, progress messages, metadata counts, JSON/table shape, and read-only behavior.

## Rejected candidates and why

- Operational Graph diagnostic inventory registration: **C. Already separated / likely re-slice**. Existing registry/spec/tests already expose the surfaces; no new visibility surface is being added.
- Operational Graph diagnostic-shape registration: **C. Already separated / likely re-slice**. It is registration/spec plumbing, not a new implementation-local ownership boundary.
- Operational Graph taxonomy output, confidence inclusion, graph sorting, graph metadata, JSON pass-through, CLI dispatch, and formatter extraction: **C/D**. Operational Graph District Scout 004 already rejected these as invalid, cosmetic, already separated, public-shape-adjacent, or not narrow enough.
- Question Surface Inventory bounded ask surfaces: **C. Already separated / likely re-slice**. Prior question-bounded-work slices already recovered the local bounded ask handoffs most relevant to `knowledge reachability`.
- Direct Source Navigation query composition: **B with caution / invalid now**. Implementation-backed but already heavily covered by tests and not the safest immediate outward step from Operational Graph; reassess only after Knowledge Reachability source-navigation-term handling.
- Architecture Conformance Audit graph consumer: **B with caution / different district later**. It consumes Operational Graph but needs its own focused scout before proposing slice boundaries.

## Candidate independence classification summary

- Candidate 1: **Independent**, confidence **High**. Valid without Candidates 2 and 3.
- Candidate 2: **Independent**, confidence **High**. Valid without Candidates 1 and 3, though batching should reassess after each slice.
- Candidate 3: **Sequential**, confidence **Medium**. Reassess after Candidate 1 or 2; do not recover blindly if earlier changes alter handoffs.

Fewer than three fully independent candidates are supported. Three recoverable candidates exist only as a guarded Knowledge Reachability queue with two independent candidates and one sequential candidate.

## Batch efficiency gate

- Recoverable candidates currently existing: **3**.
- Queue classification: **Efficiency batch**, if and only if the next command explicitly moves to the Knowledge Reachability district and reassesses sequential Candidate 3 after each landed slice.
- Protection batch: also possible with Candidates 1 and 2 if the operator wants lower re-slice risk over speed.
- Single-slice target: Candidate 1 is the safest single-slice target if batching is not desired.
- Stop/move-out: local Operational Graph remains stopped; the next move is a **different-district handoff** to Knowledge Reachability.
- Recommended batch size: **2 or 3**. Use **2** for process protection and lower risk; use **3** only as a guarded efficiency batch with reassessment before Candidate 3.

## Recommended next command

Recommended next command: move outward to a **Knowledge Reachability** district consistency gate and recover either:

1. a single slice for Knowledge Reachability candidate discovery and source-budget admission; or
2. a guarded two-slice protection batch for candidate discovery plus staged index construction; or
3. a guarded three-slice efficiency batch only if Candidate 3 is reassessed after Candidates 1 and 2.

Do not continue mining local Operational Graph. Do not use Operational Graph reports as authority for Knowledge Reachability internals; use `seed_runtime/knowledge_reachability.py`, its tests, current app evidence, diagnostic inventory, and diagnostic shape-audit declarations.

## Risk of re-slicing prior work

Risk is **high** if the next command stays in Operational Graph or bounded ask. The safe movement is not to rename graph taxonomy, graph confidence packaging, diagnostic registration, question-family dispatch, or knowledge-reachability JSON compatibility. The lower-risk path is a fresh Knowledge Reachability district with strict boundaries around candidate discovery, staged index construction, and row evaluation.

Risk is **medium** inside Knowledge Reachability because the result builder is broad. The next command should isolate exactly one ownership boundary at a time, preserve public JSON/table shape, preserve read-only/no-ledger/no-mutation behavior, and run the Knowledge Reachability tests plus diagnostic inventory/shape checks if any operational visibility implementation changes are made.

## Read-only implementation/test statement

No implementation files were changed.

No test files were changed.

This scout created and committed only `operational_graph_outward_scout_005.md`.

## Scout report commit

Commit hash: `5178d1e281d7736c2f0fee13b498c2c3a014a4d4`.
