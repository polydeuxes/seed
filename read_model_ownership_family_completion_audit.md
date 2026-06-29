# Read-Model Ownership Family Completion Audit

## Scope

This is a bounded implementation audit of the Read-Model Ownership responsibility family. It does not implement another slice, add runtime surfaces, change CLI/JSON/events/ledger behavior, redesign caches, or perform architectural recovery.

The audit reviewed the slice reports, the implementation-local ownership module, state summary implementation, fact index implementation, projection/cache store implementation, projection publication callers, and existing read-model ownership tests.

## Implemented boundaries

Implementation now exposes the complete read-model lifecycle requested for this family:

```text
Projection Publication
↓
Read-Model Construction Inputs
↓
Read-Model Dependency Identity
↓
Read-Model Cache Lookup
↓
Read-Model Construction
↓
Read-Model Cache Publication
```

### Projection Publication → Read-Model Construction Inputs

`ReadModelConstructionInputs` wraps the already-visible projected `State` and explicitly states that the boundary does not own replay, finalization, publication, cache invalidation, rendering, scheduling, or persistence. The helper `read_model_construction_inputs(state)` returns that wrapper without changing the `State` object.

Implementation consumers preserve this handoff:

- compact state summary construction immediately recovers construction inputs and reads `inputs.visible_state`;
- fact-index construction does the same before building the derived subject/predicate index;
- state-summary cache miss paths recover construction inputs after projection state is obtained.

### Read-Model Construction Inputs → Read-Model Dependency Identity

`ReadModelDependencyIdentity` owns only the dependency evidence that already made dependent read-model caches valid: `state_projection_version` and `state_last_event_id`. `read_model_dependency_identity(...)` derives that evidence from construction inputs, while `read_model_dependency_identity_for_state_boundary(...)` supports lookup before a `State` object is rebuilt when the ledger last-event boundary is already known.

The identity boundary remains separate from construction contents and from cache lookup: fact-index construction copies the identity values into the returned `DerivedFactIndex`, while cache lookup passes those same fields into projection-store lookup methods.

### Read-Model Dependency Identity → Read-Model Cache Lookup

`ReadModelCacheLookupRequest` receives an already-derived dependency identity, and `resolve_read_model_cache_lookup(...)` delegates to the existing storage lookup function. `ReadModelCacheLookupResult.cache_hit` preserves the old `snapshot is not None` decision.

This means lookup answers only whether a reusable cached read model satisfies the dependency identity. It does not derive the identity, build a model, save a model, or own invalidation/storage policy.

### Read-Model Cache Lookup → Read-Model Construction

`ReadModelConstructionRequest` consumes construction inputs, dependency identity, and the optional already-resolved cache lookup result. `construct_read_model(...)` invokes the supplied existing builder with `ReadModelConstructionInputs` and returns `ReadModelConstructionResult`.

Fact-index and state-summary miss paths now make construction observable as a handoff after lookup rather than mixing miss handling with direct builder invocation.

### Read-Model Construction → Read-Model Cache Publication

`ReadModelCachePublicationRequest` consumes a completed construction result. `publish_read_model_cache(...)` creates a cache snapshot through caller-supplied existing snapshot-shaping logic and saves it through the existing store save operation.

The boundary is post-construction only. It does not own cache lookup, dependency identity, invalidation, storage mechanics, projection publication, rendering, CLI, or read-model semantics.

## Relationship to projection publication

Projection publication remains upstream of this responsibility family. The implementation-local read-model ownership module explicitly describes read models as consumers of already-published projected `State`; it does not publish projections or replay events.

The projection store still owns reusable projected-state snapshots, and `ProjectionStore` distinguishes state projection snapshots from dependent summary and derived-index snapshots. In state-summary execution, the projected `State` is obtained either from `project_state_with_cache(...)` or direct projector replay before read-model construction inputs are recovered.

Conclusion: read-model ownership now begins after projection publication and does not absorb projection publication authority.

## Relationship to cache publication

Read-model cache publication is now the terminal boundary inside this family: a constructed read model is converted to the existing summary or derived-index snapshot and passed to the existing save operation.

The lower-level store remains outside this family. `ProjectionStore` still owns the persistence API and exact-match snapshot load/save behavior for summary and derived-index snapshots. `publish_read_model_cache(...)` does not choose table keys, invalidation policy, snapshot retention, or storage backend behavior; it only names the publication handoff from construction result to existing save operation.

The state-summary debug path still contains a direct timed `store.save_summary_snapshot(...)` call. That is implementation evidence of debug/timing adjacency, not evidence that read-model construction and cache publication remain generally compressed in the primary family path. The direct call exists to preserve timing labels in a debug surface.

## Relationship to downstream read-model consumers

Downstream consumers still receive the same read models and payloads:

- `build_state_summary(...)` returns the same compact `StateSummary` fields;
- `state_summary(...)` returns the same operator summary dictionary from projected state;
- `load_or_build_fact_index(...)` returns the same `DerivedFactIndex` and uses the same `current_facts(...)` lookup semantics;
- cached state-summary hits reconstruct `StateSummary` and operator summary from the existing snapshot payload shape;
- fact-index cache hits reconstruct `DerivedFactIndex` from the existing derived-index payload shape.

No reviewed implementation evidence shows a downstream consumer needing an additional read-model ownership slice before it can consume these read models.

## Counterexample review

### Construction inputs and dependency identity mixed?

No recurring family-local compression remains. Construction inputs are recovered first, and dependency identity is derived separately from those inputs or from an already-known projected-state boundary. Remaining direct reads of `state.last_event_id` inside snapshot creation are payload population and debug accounting, not identity derivation mixed with construction inputs.

### Dependency identity and cache lookup mixed?

No. Cache lookup now takes `ReadModelCacheLookupRequest(dependency_identity)` and delegates to storage. The exact-match comparison remains in the projection store implementations, which is storage/cache policy rather than read-model ownership compression.

### Cache lookup and construction mixed?

No recurring primary-path compression remains. Miss paths carry the lookup result into `ReadModelConstructionRequest` before invoking builders. The cache-debug path constructs compact and operator summaries separately for timing, but each timed construction still uses the construction request boundary.

### Construction and cache publication mixed?

No recurring primary-path compression remains in the fact-index path or normal state-summary path. Both publish through `ReadModelCachePublicationRequest` and `publish_read_model_cache(...)`.

The state-summary cache-debug path still directly saves a `SummaryProjectionSnapshot` inside a timed block. This is remaining pressure in debug/timing instrumentation, not a reason to continue slicing Read-Model Ownership: the path is intentionally measuring individual operations and the direct save belongs more naturally to operational timing/visibility or cache-storage instrumentation than to another read-model lifecycle owner.

## Remaining compressed boundaries

No remaining recurring compressed boundary is supported inside Read-Model Ownership.

Remaining implementation pressure exists, but it points outside this family:

- `ProjectionStore` combines state projection snapshots, summary read-model snapshots, and derived-index snapshots behind one protocol. That is cache composition/storage ownership pressure, not read-model lifecycle pressure.
- Exact-match dependency checks are implemented by store load methods. That is cache invalidation/validity policy pressure, not read-model construction ownership.
- State-summary debug timing keeps direct timed save/decode operations to expose timings. That is operational visibility/timing ownership pressure, not a missing read-model lifecycle boundary.
- State summary has compact `StateSummary` construction and operator `state_summary(...)` construction adjacent in the same miss path. That is read-model selection/composition pressure, not another ownership slice in the completed lifecycle sequence.
- Projection builder dependency choices still live upstream of read-model construction inputs. That belongs to projection builder dependency ownership, not read-model ownership.

## Supported conclusions

1. **Read-Model Ownership has become a completed implementation responsibility family.** The implementation exposes every boundary in the requested lifecycle and uses those boundaries in the recurring state-summary and fact-index cache/build paths.
2. **The family starts after projection publication.** It consumes visible projected `State` and does not own replay, finalization, publication, event ledger behavior, or projected-state cache behavior.
3. **The family ends at read-model cache publication.** It names the handoff from constructed read model to existing dependent cache save operations, but does not own lower-level storage mechanics or cache invalidation policy.
4. **No additional implementation slice is justified inside this family now.** Remaining pressure is either debug/timing instrumentation, cache policy/storage composition, read-model selection/composition, partial-refresh authority, dependency graph ownership, or upstream projection-builder dependency ownership.

## Unsupported conclusions

The implementation evidence does **not** support concluding that:

- cache invalidation policy has been fully separated or redesigned;
- partial refresh authority exists;
- read-model dependency graph ownership has been recovered;
- projection-store cache composition has been separated into independent stores;
- compact state summary and operator state summary are separate read-model selection authorities;
- projection publication has become part of Read-Model Ownership;
- downstream consumers have changed behavior, JSON shape, CLI behavior, event semantics, ledger behavior, or compatibility;
- another slice should be implemented merely because adjacent cache/debug code still exists.

## Recommended next responsibility family

Recommended next family: **Read-Model Dependency Graph**.

## Reason for recommendation

Among the remaining pressure examples, dependency graph ownership is the most implementation-backed next investigation because the current family has made the lifecycle of an individual dependent read model explicit, but dependencies are still represented as flat exact-match identity fields (`state_projection_version`, `state_last_event_id`) at each dependent cache. The implementation has at least two dependent read models (state summary and fact index), plus a lower-level projected-state cache, and the store API already distinguishes state snapshots from dependent summary and derived-index snapshots.

That evidence supports investigating how dependent read models relate to upstream projections and to each other. It does **not** support implementing partial refresh, invalidation redesign, or cache-store redesign yet. A bounded audit should first determine whether there is recurring compressed ownership around dependency relationships between projected state, summary read models, and derived indexes.

If repository evidence rejects dependency-graph ownership as recurring, the next alternatives should be investigated in this order:

1. **Cache invalidation policy** — because exact-match validity checks remain centralized in store load methods;
2. **Read-model selection** — because compact summary and operator summary are constructed together in state-summary paths;
3. **Projection builder dependency ownership** — because this is upstream of construction inputs and should not be folded back into Read-Model Ownership.

## Confidence

**High** that Read-Model Ownership is complete as an implementation responsibility family.

The confidence is high because both recurring dependent read-model paths reviewed in implementation—state summary and fact index—now traverse the same explicit lifecycle boundaries, and the ownership module itself names each boundary with negative ownership constraints. Confidence is not absolute because debug/timing paths intentionally preserve direct store operations for measurement, and because broader cache/dependency policy has not been audited as its own family.

## Acceptance answers

### Has Read-Model Ownership become a completed implementation responsibility family?

Yes. The recurring implementation paths now expose construction inputs, dependency identity, cache lookup, construction, and cache publication as separate implementation-local owners after projection publication.

### What implementation evidence supports that conclusion?

The ownership module defines all lifecycle boundary dataclasses and helpers. State summary and fact index construction recover construction inputs. Fact index and state-summary cached paths derive dependency identity, resolve cache lookup, construct on misses, and publish completed read models to existing cache stores without changing payload/cache semantics.

### Which remaining implementation pressure belongs inside this family?

None supported by current evidence. The one remaining direct save in state-summary cache debug is timing/debug visibility pressure rather than a recurring lifecycle boundary.

### Which remaining implementation pressure belongs elsewhere?

Dependency graph ownership, cache invalidation/validity policy, partial refresh authority, read-model selection/composition, projection-store cache composition, operational timing visibility, and projection builder dependency ownership belong elsewhere.

### Should implementation begin the next responsibility family?

Yes, but only as a bounded audit first, not implementation.

### If so, which one, and why?

Begin with a bounded **Read-Model Dependency Graph** audit because the individual read-model lifecycle is explicit while dependency relationships among projected state snapshots, state-summary snapshots, and derived-index snapshots remain represented as repeated flat exact-match identity fields.
