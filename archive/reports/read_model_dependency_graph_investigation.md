# Read-Model Dependency Graph Investigation

## Scope

This is a bounded implementation investigation only. It does not implement ownership recovery, new abstractions, new runtime surfaces, cache redesign, partial refresh, dependency graphs, or vocabulary migration.

The question reviewed here is whether current implementation evidence supports a recurring **Read-Model Dependency Graph** responsibility: an owner for which read models consume other read models, their construction/dependency ordering, dependency reuse, derived relationships, consumer relationships, or invalidation relationships.

Repository authority wins over the candidate graph.

## Implementation evidence reviewed

### Projection and projected State publication

`StateProjector.project_from_state(...)` applies ledger events, finalizes derived projection indexes, then publishes a visible `State` through `_publish_finalized_projection(...)`. This shows projection publication as an already explicit responsibility and establishes `State` as the common read-model input boundary for later builders.

`StateProjector.finalize(...)` rebuilds projection-owned derived indexes inside `State`, including alias resolution, fact support construction, relationships, entity type assertions, graph issues, aliases, and fact conflicts. This is projection finalization evidence, not evidence of a separate read-model dependency graph among higher-level read models.

### Current facts and fact support

`State.get_current_facts(...)` derives current facts directly from `State` and `FactSupport` through `get_best_fact(...)` / `get_fact_supports(...)`, with predicate cardinality determining whether a best fact or multiple support representatives are returned. Current-facts selection is therefore a `State` method over projection-owned support data.

`build_fact_view(...)` also consumes `state.fact_supports` directly and has a raw-facts fallback for tests/callers that construct `State` manually. That fallback is a counterexample to a mandatory graph edge from a separately built Fact Index into Fact Views.

### Fact Index

`DerivedFactIndex` is explicitly described as a reusable facts-by-subject/predicate index derived from projected `State`. `build_fact_index(...)` receives `State`, calls `read_model_construction_inputs(state)`, iterates `visible_state.fact_supports`, and for each subject/predicate calls `visible_state.get_current_facts(...)` before storing fact ids. This is strong evidence for an internal construction dependency:

```text
Projected State / fact_supports / State.get_current_facts
  -> DerivedFactIndex
```

It is not evidence that Fact Index owns current facts. The index stores ids for faster lookup; `DerivedFactIndex.current_facts(...)` still requires the caller to pass `State` and filters by `state.facts`.

`load_or_build_fact_index(...)` shows the already-completed dependent cache pattern: derive dependency identity from the visible `State`, resolve a cache lookup, build on miss, and publish the snapshot. This is cache lookup/publication and construction evidence, not graph ownership evidence.

### State Summary

`projected_state_summary_from_args(...)` uses a dependent summary cache keyed by `STATE_PROJECTION_VERSION` and the current last event id. On cache miss it builds projected `State`, creates read-model construction inputs, and constructs a tuple of `build_state_summary(visible_state)` and `state_summary(visible_state)`.

This is evidence that both the compact `StateSummary` view and operator summary are sibling read models over the same projected `State` boundary:

```text
Projected State
  -> build_state_summary(...)
  -> state_summary(...)
```

The implementation does not show `state_summary(...)` consuming `DerivedFactIndex`, `current_facts`, or inquiry/diagnostic views. `state_summary(...)` directly scans `state.facts`, `state.observations`, stale facts, graph issues, and conflicts.

`_storage_projection(...)` is another sibling State-derived operator surface. It scans projected measurement facts from `state.facts`, performs projection-only filesystem grouping, derives shared-storage candidates, derives ambiguities from those candidates and cluster mount groups, and returns a storage-focused dictionary. This is a local derivation chain inside one read model, not a repository-level graph owner connecting named read models.

### Current Facts CLI and cache debug

`format_current_facts(...)` accepts an optional `fact_index`. When the index is present it calls `fact_index.current_facts(state, ...)`; otherwise it calls `state.get_current_facts(...)` directly. This is clear evidence of optional dependency reuse:

```text
Current Facts render path
  -> optional Fact Index reuse
  -> fallback direct State.get_current_facts
```

Because the direct fallback is first-class, the dependency is opportunistic rather than a required graph edge.

`_current_facts_timing_from_args(...)` labels phases such as projection build, fact-index build/load, read-model build, and render. This is diagnostic/timing visibility for a path; it does not own dependency ordering beyond the local command sequence.

### Capability candidates as a read-model consumer of Fact Index

`build_capability_candidates(...)` accepts an optional `DerivedFactIndex`. Its helper `_package_installed_facts(...)` scans `state.facts` directly when no index is supplied, or iterates the index's subject/predicate map and calls `fact_index.current_facts(...)` when an index is supplied. This repeats the optional reuse pattern seen in current facts:

```text
Capability candidates
  -> optional Fact Index reuse
  -> fallback direct State.facts scan
```

This is stronger evidence that Fact Index is a reusable helper for selected consumers. It is still not a centralized dependency graph, because the relationship is passed as an optional function argument and the fallback makes the consumer independent.

### Inquiry views

`build_inquiry_orientation(...)` consumes `State` and an `InquiryNoteRecord`, then collects orientation evidence from projected fact supports and source-navigation matches. The public view is produced by answer composition and rendering, not by consuming State Summary, Current Facts, Fact Index, or diagnostic views.

The inquiry code's uncertainty text says absence of matches means no deterministic related material was found in already projected read models, but implementation evidence shows concrete calls into projected `State` and source navigation rather than a registered dependency graph of read-model-to-read-model edges.

### Diagnostic and projected-state consumer views

`build_projected_state_consumers(...)` builds rows from `DIAGNOSTIC_INVENTORY` and static classification sets. It declares source classes such as projected-state, repository-file, static-inventory, live-observation, event-ledger, and runtime-input use. It explicitly says the surface classifies existing registry evidence only and does not infer consumers.

This is useful consumer characterization, but it is not an implementation-owned dependency graph among read models. It classifies surfaces by evidence-source classes and boundary metadata rather than preserving ordered read-model edges or invalidation relationships.

### Cache dependency identity and read-model cache publication

`ReadModelDependencyIdentity` preserves `state_projection_version` and `state_last_event_id`. `ReadModelCacheLookupRequest`, `ReadModelConstructionRequest`, and `ReadModelCachePublicationRequest` make lookup, construction, and cache publication handoffs explicit. Their docstrings repeatedly exclude cache invalidation, storage, projection publication, rendering, events, and read-model semantics from the boundary.

This is strong evidence that dependency identity and cache publication are sufficiently explicit already. The identity is about validity of a cached read model against projected `State`, not about a graph of read models consuming each other.

`ProjectionStore` persists three cache families: projected state snapshots, summary snapshots, and derived index snapshots. Summary and derived index loads validate against `state_projection_version` and `state_last_event_id`; clearing a state snapshot removes dependent summary and derived index snapshots for the workspace. This is invalidation/coupling at cache storage granularity, not a generalized dependency graph among all read-model consumers.

## Recurring dependency patterns recovered

### Pattern 1: Projected State is the dominant shared input boundary

Most reviewed read models consume projected `State` directly:

```text
Projected State
  -> State.get_current_facts(...)
  -> build_fact_view(...)
  -> build_fact_index(...)
  -> build_state_summary(...)
  -> state_summary(...)
  -> storage_state_projection(...)
  -> build_inquiry_orientation(...)
  -> many diagnostics declared as uses_projected_state
```

This pattern is recurring and explicit, but it is already owned by read-model construction inputs and projection publication rather than by a separate graph owner.

### Pattern 2: Fact Index is an optional reusable accelerator/helper

The Fact Index is reused in at least two places:

```text
Current Facts formatting
  -> optional DerivedFactIndex.current_facts(...)

Capability candidate inspection
  -> optional DerivedFactIndex.current_facts(...)
```

Both consumers have direct `State` fallbacks. This supports a narrower conclusion: the repository has optional dependency reuse around Fact Index, not mandatory dependency ordering for all read models.

### Pattern 3: Dependent cache validity is keyed to projected State identity

Fact Index and State Summary snapshots are valid only when their stored `state_projection_version` and `state_last_event_id` match the current projected State boundary. This is a recurring dependent-cache relationship:

```text
Projected State identity
  -> dependent summary snapshot validity
  -> dependent fact-index snapshot validity
```

This belongs to dependency identity/cache lookup/cache publication/storage, which the repository already made explicit.

### Pattern 4: Local derivation chains exist inside individual read models

`_storage_projection(...)` derives complete filesystems, operator-relevant filesystems, filesystem summaries, mount groups, shared-storage candidates, storage ambiguities, and storage topology summary. These are meaningful local derivation steps but they are implementation-internal to one read model, not registry-level dependency edges among read models.

## Counterexamples and limits

1. **Current Facts does not require Fact Index.** `format_current_facts(...)` falls back to `state.get_current_facts(...)` when no index is supplied.
2. **Capability candidates do not require Fact Index.** `_package_installed_facts(...)` scans `state.facts` directly when no index is supplied.
3. **State Summary does not consume Fact Index or Current Facts.** It scans projected `State` directly.
4. **Inquiry Orientation does not consume State Summary, Current Facts, Fact Index, or diagnostics.** It consumes `State`, inquiry note input, fact matches, and source navigation evidence.
5. **Projected State Consumers does not infer a dependency graph.** It classifies registered evidence-source consumption and states that it does not infer consumers.
6. **Cache invalidation exists at store/cache granularity.** Clearing a projected-state snapshot also clears dependent summary and derived-index snapshots, but this is storage coupling, not an owned graph of semantic read-model dependencies.

## Supported conclusions

### 1. Does a recurring Read-Model Dependency Graph responsibility currently exist?

**Partially, but not maturely enough as a repository-owned responsibility family.**

The implementation contains recurring dependency relationships, especially:

- read models consuming projected `State`;
- dependent caches keyed by projected-State identity;
- optional Fact Index reuse by Current Facts and Capability Candidates;
- local derivation chains inside specific read models.

However, the repository does not currently show a centralized owner for:

- which read models consume other read models;
- dependency ordering across read models;
- graph-level dependency reuse;
- semantic dependency invalidation beyond cache identity/storage;
- a maintained edge inventory among named read models.

### 2. If yes, where is the strongest implementation evidence?

The strongest evidence for a recoverable dependency-graph pressure is the repeated optional Fact Index reuse pattern:

```text
DerivedFactIndex built from State.get_current_facts(...)
Current Facts optionally uses DerivedFactIndex.current_facts(...)
Capability Candidates optionally uses DerivedFactIndex.current_facts(...)
```

The strongest evidence for dependent identity is the shared `ReadModelDependencyIdentity` used by fact-index and state-summary cache lookup/publication.

Neither is yet enough to prove an implementation-owned Read-Model Dependency Graph family, because both are either optional caller-supplied reuse or already-completed cache identity/lookup/publication behavior.

### 3. What implementation responsibilities currently appear compressed?

The following responsibilities still appear compressed or only local:

- optional read-model reuse versus direct projected-State scanning;
- read-model consumer relationships passed as optional arguments rather than preserved as relationships;
- local derivation chains inside read-model builders versus cross-read-model dependency relationships;
- cache invalidation coupling in `ProjectionStore.clear_snapshot(...)` versus semantic dependency invalidation;
- diagnostic surface evidence-source classification versus read-model dependency ownership.

### 4. What implementation responsibilities are already sufficiently explicit?

The following responsibilities are already explicit enough and should not be re-owned by a dependency graph investigation:

- projected-State construction, finalization, and publication;
- read-model construction handoff through `ReadModelConstructionInputs` / `ReadModelConstructionRequest`;
- dependency identity for cached read models through `ReadModelDependencyIdentity`;
- cache lookup through `ReadModelCacheLookupRequest` / `ReadModelCacheLookupResult`;
- cache publication through `ReadModelCachePublicationRequest` / `publish_read_model_cache(...)`;
- projection-store persistence for state snapshots, summary snapshots, and derived index snapshots;
- diagnostic inventory and shape-audit visibility for operational surfaces.

### 5. Should Read-Model Dependency Graph become the next responsibility family?

**Not yet.**

The repository contains dependency pressure, but current implementation evidence is not mature enough for bounded ownership recovery of a Read-Model Dependency Graph responsibility family. The strongest recoverable fact is narrower: selected consumers optionally reuse `DerivedFactIndex`, while most read models remain direct consumers of projected `State`.

Starting a full responsibility family now would risk promoting presentation vocabulary or architectural preference ahead of implementation evidence.

## Unsupported conclusions

The current implementation evidence does **not** support concluding that:

- the candidate chain `Projected State -> Current Facts -> Fact Index -> State Summary -> Inquiry Views -> Diagnostic Views` is the repository's actual dependency graph;
- State Summary depends on Fact Index or Current Facts;
- Inquiry Views depend on State Summary, Fact Index, Current Facts, or Diagnostic Views;
- Diagnostic Views depend on Inquiry Views as read models;
- every read model participates in a common dependency graph;
- invalidation is modeled semantically across read-model relationships rather than through cache keys and projection-store clearing;
- a graph abstraction should be implemented now.

## Confidence

**Medium-high confidence** that a full Read-Model Dependency Graph responsibility is not yet recoverable.

Rationale:

- The reviewed implementation repeatedly shows direct projected-State consumption.
- Optional Fact Index reuse is real and repeated, but fallback paths make it opportunistic rather than governing dependency order.
- Cache dependency identity is explicit already and should not be mistaken for semantic graph ownership.
- Diagnostic consumer classification exists, but it explicitly classifies registry evidence and does not infer consumers.

**Medium confidence** that a narrower future responsibility may emerge around reusable read-model dependency declarations if more consumers begin requiring Fact Index or other derived read models without direct fallbacks.

## Recommended next action

Do not begin a Read-Model Dependency Graph ownership family yet.

Recommended next action is continued observation only:

1. Preserve the current explicit ownership boundaries for projection publication, construction, dependency identity, cache lookup, and cache publication.
2. Watch for future implementation evidence where a read model must consume another read model without a direct projected-State fallback.
3. If such evidence appears in at least two independent consumers, perform a narrower investigation around **read-model dependency declaration** or **read-model reuse relationship** before naming a full dependency graph family.
4. Do not implement graph abstractions, dependency registries, invalidation redesign, partial refresh, or vocabulary migration from this investigation alone.

## Acceptance answer

The repository **does contain recoverable read-model dependency pressure**, especially optional Fact Index reuse and projected-State-keyed dependent caches.

The repository **does not yet contain enough implementation evidence for a mature Read-Model Dependency Graph responsibility family**. The missing evidence is an implementation-owned place that preserves semantic relationships among named read models: which read models consume which others, required construction ordering, graph-level dependency reuse, and graph-level invalidation beyond cache identity and projection-store clearing.
