# Incremental State Evolution Architecture Investigation

## Scope and method

This is an implementation-backed architectural recovery, not a performance plan. It reviews the current Seed code paths for event preservation, state projection, projection caching, dependent read models, execution/status visibility, observation/fact/relationship projection, and answer/presentation composition. It does not propose distributed systems, CQRS redesign, stream processors, background workers, database replacement, or a pub/sub framework.

Repository authority wins: conclusions below are limited to what current implementation and tests already support.

## Executive answer

Yes. Seed already possesses the beginnings of an incremental state architecture, but only at the projection-cache replay boundary and dependent read-model cache boundary. It does not yet possess fully bounded dirty-scope evolution where a HostX event refreshes only HostX-derived projections.

Current implementation supports three meaningful incremental or bounded behaviors:

1. **Append-only event authority with replay order.** Events are preserved in order and can be listed by workspace.
2. **Snapshot-plus-tail replay.** A cached `State` snapshot can be materialized, then only ledger events after the snapshot's `last_event_id` are replayed before final projection indexes are rebuilt.
3. **Dependent read-model cache invalidation by state identity.** State summary and fact-index caches are keyed by projection version plus `state_last_event_id`, so they can be reused without recomputing when the underlying projected State boundary has not changed.

Current implementation still requires global recomputation in these places:

1. **Finalization after incremental replay is global.** Alias resolution, measurement retention, inference, fact supports, relationships, entity types, graph validation, aliases, and conflicts are rebuilt across the whole projected State after any replay.
2. **Read-model rebuilds are global within their model.** `state_summary(state)` and `build_fact_index(state)` derive from the whole projected State when their dependent cache misses.
3. **Answer/context composition selects from globally projected State.** Decision input composition orders and budgets all goals, entities, facts, evidence, and open tool needs from the current State rather than refreshing only affected answer fragments.

The smallest implementation-backed path toward incremental state evolution is not a new architecture. It is to expose and test the already-existing `event -> State.apply mutation -> State.finalize derived indexes -> dependent read model` boundary as affected-scope metadata, starting with the event kinds and State collections already modified by `StateProjector.apply`, then use that metadata only to report and audit scope before it controls recomputation.

## Evidence map

| Area reviewed | Implementation evidence | Recovery result |
|---|---|---|
| Event ledger | `EventLedger.append`, `append_many`, `_store`, and workspace indexes | Append-only, ordered event history exists and is workspace-scoped. |
| Projection stage | `StateProjector.project`, `project_from_state`, `apply`, `finalize` | Projection is separated into event application and derived-index finalization. |
| Projection cache | `project_state_with_cache`, `_events_after_snapshot`, `_save_state_snapshot` | Cached State snapshots support hit/miss and tail replay. |
| Current state build | `projected_state_summary_from_args` | State-build read model has a dependent cache keyed to current last event. |
| Read models | `build_state_summary`, `state_summary`, `build_fact_index`, `load_or_build_fact_index` | Read models are deterministic derivatives of State; fact index and state summary are cacheable. |
| Execution visibility and timing | `emit_status` phases in event persistence, projection cache, replay, incremental replay, summary cache, fact-index build/load | Operational timing/status surfaces separate cache load, replay, save, and read-model work. |
| Observation ownership | `StateProjector.apply` branches for observation/evidence/fact events and measurement provenance pruning | Observation/evidence/fact records have distinct projected collections; measurement retention prunes projection, not ledger authority. |
| Fact promotion and relationship projection | `_project_inferred_facts`, `_project_fact_supports`, `_project_catalog_relationships`, `_project_entity_type_assertions`, graph validation | Relationships, supports, type assertions, and conflicts are derived projection products rather than event authority. |
| Presentation and answer composition | `DecisionInputComposer.compose`, CLI summary path | Presentation/answer inputs consume projected State or cached read models; no partial answer refresh boundary is implemented. |

## 1. Existing incremental projection behavior

Seed already implements incremental projection in a narrow, concrete sense: when a projection snapshot exists but its `last_event_id` is stale, the cache path materializes the snapshot State, finds events after that snapshot, replays only those remaining events into the snapshot, finalizes derived indexes, saves a new snapshot, and reports `incremental_replay=True` with `events_applied` equal to the tail length.

This is not merely a performance hint. `StateProjector.project_from_state` explicitly documents applying ledger events to an existing projected State and then rebuilding derived indexes. Its docstring says the events must follow the snapshot's `last_event_id` in ledger order and that ledger history remains authority. That is an implementation-backed incremental boundary.

The implementation is incomplete for bounded state evolution because the event application is incremental, but finalization is global. Any tail replay still recomputes all alias resolution, measurement retention, inference, fact support, relationship projection, type assertion projection, graph validation, alias materialization, and conflict projection across the whole State.

## 2. Existing invalidation behavior

### Projection cache

Projection cache validity is exact-version and exact-last-event based. A snapshot is reusable only when:

- the workspace/projection name matches;
- the projection version matches;
- the snapshot materializes successfully; and
- the snapshot `last_event_id` equals the ledger's current last event id.

If that equality holds, projection returns a cache hit and applies zero events. If a usable snapshot exists but is stale and can be located in event order, the implementation applies only the remaining events. If no valid snapshot exists, the implementation performs a full projection replay.

The invalidation model is therefore **boundary invalidation**, not dirty-scope invalidation. It knows whether the cached projection is current relative to ledger order, but it does not know which subject, relationship, read model, or presentation section became dirty.

### Dependent state-summary cache

The state-build summary path first asks the projection store for a summary snapshot keyed by:

- workspace;
- state-summary projection name/version;
- State projection version; and
- `state_last_event_id` equal to the current ledger last event id.

A hit returns the compact `StateSummary` and operator summary payload without loading/building full State. A miss builds or loads State, computes summaries, and saves the dependent summary snapshot. This is stronger than a generic view cache because it records dependency on State projection identity.

### Derived fact-index cache

The fact index is explicitly described as a cacheable derived read model, not event authority or fact mutation. Its load path requires index name/version, State projection version, and exact `state_last_event_id`. A miss builds the index from already-projected State and stores only fact ids by subject/predicate.

### Warm and cold states

The implementation distinguishes:

- cold full replay: no usable projection snapshot;
- warm projection hit: snapshot `last_event_id` equals current ledger last event;
- warm-but-stale tail replay: snapshot exists and can be advanced by replaying events after snapshot;
- dependent read-model hit: summary or fact index matches State version and last-event boundary;
- dependent read-model miss: State may be cached or incrementally replayed, but the read model is rebuilt globally.

## 3. Existing affected-scope evidence

Current implementation does not expose a first-class `AffectedScope` type. However, recurring implementation evidence for affected scope exists in the data shapes and mutation targets.

### Event kind to State collection

`StateProjector.apply` already maps event kinds to bounded State collections:

- `entity.upserted` affects `state.entities[entity.id]`.
- `observation.observed` affects `state.observations[observation.id]`.
- `evidence.observed` affects `state.evidence[evidence.id]`.
- `fact.observed` and `fact.inferred` affect `state.facts[fact.id]`.
- `goal.created` affects `state.goals[goal.id]`.
- `tool_need.created` / `tool_need.status_changed` affect `state.tool_needs[need.id]`.
- approval and execution authorization events affect `state.approvals`, `state.execution_authorizations`, and possibly a matching execution proposal.
- execution proposal, handoff plan, pending action, action plan, and tool registration events each mutate their own State collection or status record.

That mapping is the strongest current evidence for affected scope. It is collection- and record-oriented, not yet projection-dependency-oriented.

### Subject and relationship scope

Facts carry subject, predicate, value, dimensions, evidence ids, observed time, expiry, confidence, and source type. Current belief selection uses subject/predicate/dimensions and predicate cardinality. Relationship projection derives edges from facts through the relationship catalog. Alias resolution may merge subject components, while endpoint-scoped predicates intentionally avoid host alias collapse.

This means subject/predicate/dimensions are already recoverable as affected knowledge scope for fact events, but aliases, inferred facts, relationships, graph issues, and conflicts can widen the downstream affected projection scope.

### Execution state scope

Execution authorization, execution proposals, pending actions, tool needs, action plans, and handoff plans are separate State collections. Their event branches update record-local status where possible. Execution status emission is operational visibility, not cached State authority, and tests explicitly cover that execution status is not included in projection cache.

### Documentation and capability scope

Documentation observation and capability modules are mostly separate operational/read surfaces, while projected State stores facts, evidence, observations, tool needs, tools, and related capability/verification artifacts through their events or derived views. Existing evidence supports bounded capability and documentation surfaces as read-model or diagnostic families, but not a unified dirty-scope engine.

## 4. Dirty scope, affected scope, projection dependency, incremental read model

The implementation naturally suggests these concepts, but does not yet implement them as authoritative abstractions.

Supported by current code:

- **Affected scope:** recoverable from event kind, record id, fact subject/predicate/dimensions, relationship endpoints, action/pending/execution ids, and tool/capability identifiers.
- **Projection dependency:** partially recoverable from function calls in `finalize` and dependent cache keys in summary/fact-index caches.
- **Incremental read model:** partially present as cache reuse and exact dependency invalidation. The read model can be skipped on hit, but on miss it rebuilds globally.
- **Dirty scope:** implied by stale snapshot boundaries and record-local event application, but not explicitly represented or consumed.

Unsupported by current code:

- A per-subject dirty set that controls relationship/support/conflict recomputation.
- A dependency graph that lets a fact event refresh only affected relationships, graph issues, or summary sections.
- Partial answer refresh or answer-fragment caching.
- Projection-stage contracts that declare their inputs and outputs in machine-readable form.

## 5. Current global rebuild assumptions

Global rebuild assumptions appear at several levels:

1. `StateProjector.project` always starts from an empty State and projects all workspace events.
2. `project_from_state` can replay only a tail, but always calls global `finalize` afterward.
3. `finalize` computes derived indexes by scanning full State collections.
4. `state_summary(state)` builds operator summary from the whole State.
5. `build_fact_index(state)` iterates all subjects in `state.fact_supports`.
6. `DecisionInputComposer.compose` orders all goals, entities, facts, evidence, and open tool needs before budget selection.
7. Graph traversal methods scan relationship lists rather than using dependency-local indexes.

These are not bugs. They preserve deterministic projection and bounded responsibility. They are the current correctness-first architecture.

## 6. Projection stages and dependency graph evidence

Projection stages imply a dependency order, but not a declared dependency graph.

The strongest implicit order is in `StateProjector.finalize`:

```text
facts/evidence/observations after event replay
↓
initial alias projection
↓
measurement evidence scan and measurement retention
↓
inferred fact projection
↓
post-inference alias projection
↓
measurement retention after inference
↓
observed/inferred fact partitions
↓
measurement provenance pruning
↓
fact support construction
↓
legacy relationship projection
↓
catalog relationship projection
↓
entity type assertion projection
↓
graph issue construction
↓
alias list materialization
↓
fact conflict handling
```

This order is implementation evidence for dependencies. For example, relationship projection depends on projected facts and evidence; graph validation depends on relationships and entity type assertions; fact conflicts depend on projected facts and supports. However, these dependencies exist as call order and shared State reads/writes, not as an inspectable graph object.

Dependent read-model caches make another dependency explicit:

```text
Event ledger last_event_id
↓
State projection version + State last_event_id
↓
state-summary snapshot or fact-index snapshot
```

This is an existing dependency chain, but it is coarse: any State last-event change invalidates the dependent read model.

## 7. Partial answer refresh evidence

Current implementation does not support partial answer refresh. Answer and decision input surfaces compose from projected State at request time:

- `DecisionInputComposer.compose` orders State sections globally, then applies the context budget.
- Facts include attached evidence only when the evidence survived budget selection.
- CLI state summaries use either a whole dependent summary cache hit or a full summary rebuild.

There is partial **selection** through context budgeting and section ordering, but not partial **refresh**. The repository can avoid recomputing a cached whole summary, and it can avoid replaying old events through projection cache. It cannot refresh only the answer fragment for HostX, one relationship, or one documentation section.

## 8. Event to affected knowledge to affected projections to affected presentation

The recurring structure exists, but it is not fully surfaced:

```text
event
↓
StateProjector.apply mutates a bounded State collection or record
↓
StateProjector.finalize globally derives supports, aliases, relationships, types, graph issues, conflicts, inferred facts
↓
read models and presentation derive from State or cached State-derived snapshots
```

For fact events, the structure is especially visible:

```text
fact.observed / fact.inferred event
↓
state.facts[fact.id]
↓
current belief, support, conflict, relationship, type, inference, measurement retention, graph validation
↓
current facts, why/explanation, impact, relationships, state summary, context packet, answer inputs
```

For execution-related events:

```text
execution/tool/action event
↓
execution_proposals, execution_authorizations, pending_actions, action_plans, tool_needs, tools
↓
open needs, authorization/executable flags, runtime and policy read surfaces
↓
operator status, context packet, CLI/debug presentation
```

For observation events:

```text
observation/evidence/fact events
↓
observations, evidence, facts
↓
measurement retention, fact supports, relationships, graph issues, summaries
↓
state views, summaries, explanations, answer context
```

This supports explaining bounded state evolution using current implementation, but only descriptively. The code does not yet use this structure to limit finalization or read-model recomputation.

## Counterexamples and constraints

Evidence contradicting a mature incremental-evolution architecture:

- Global `finalize` after every projection or tail replay.
- Cache invalidation based on `last_event_id` rather than affected subject/stage/read-model scope.
- Relationship and graph validation recomputation over full lists.
- Fact support and conflict projection scanning all facts.
- State summary and fact-index rebuilds scanning whole State after cache miss.
- Decision input composition selecting from globally ordered State sections.
- No explicit machine-readable stage input/output/dependency registry.
- No first-class dirty-scope object, affected-scope audit, or partial presentation refresh.

Evidence preventing overreach:

- Projection cache is an optimization over ledger authority; it does not replace event history.
- Dependent read-model caches are valid only for exact State projection version and last-event boundary.
- Measurement history retention prunes projected State while preserving append-only ledger history.
- Execution status/progress emission is operational visibility, not State authority.

## Supported conclusions

1. Seed already has a real incremental projection beginning: cached State plus tail event replay.
2. Seed already separates event authority from projection cache authority.
3. Seed already has coarse projection dependencies through State projection version and `last_event_id`.
4. Seed already has dependent read-model caches for state summary and fact index.
5. Seed already has recoverable affected-scope signals in event kind, record id, fact subject/predicate/dimensions, relationship endpoints, and execution/action ids.
6. Seed can currently explain bounded state evolution as an architectural direction grounded in existing code.
7. Current implementation does not yet implement subject-local or projection-stage-local recomputation.

## Unsupported conclusions

1. Unsupported: Seed has a complete dirty-scope architecture.
2. Unsupported: Seed can currently recompute only HostX-related projections after a HostX fact changes.
3. Unsupported: Seed has a declared projection dependency graph.
4. Unsupported: read models are incrementally updated by affected scope.
5. Unsupported: answer composition supports partial refresh.
6. Unsupported: projection cache invalidation knows which knowledge changed; it knows only projection boundary freshness.
7. Unsupported: documentation, capability, execution, observation, relationship, and presentation scopes have one shared affected-scope model.

## Remaining implementation gaps

- No first-class affected-scope report for event kinds.
- No stage-level input/output/dependency spec for projection finalization.
- No tests proving affected scope can be recovered from events without changing recomputation behavior.
- No dirty-scope propagation from fact subject/predicate/dimensions to support, relationship, type, graph, summary, and answer surfaces.
- No read-model cache invalidation narrower than State `last_event_id`.
- No partial answer or presentation fragment cache.
- No operator-facing audit that says why a projection/read model was rebuilt globally instead of incrementally.

## Smallest implementation-backed next step

The smallest next step is an audit/reporting slice, not a recomputation rewrite:

1. Add an affected-scope recovery helper for existing event kinds handled by `StateProjector.apply`.
2. Return only descriptive metadata such as collection, record id, subject, predicate, dimensions, relationship endpoints when recoverable, and execution/action identifiers when recoverable.
3. Add tests that every current `StateProjector.apply` event family either maps to an affected scope or is explicitly marked unknown.
4. Optionally expose it through an existing diagnostic/audit pattern, following the repository's diagnostic inventory and shape-audit rules.
5. Do not use the metadata to skip finalization until tests prove it is complete enough for a bounded projection stage.

This path preserves repository authority because it first makes existing implementation scope visible. It avoids introducing a new architecture before the current event-to-State-to-read-model boundaries are recoverable and testable.

## Acceptance answers

### Does Seed already possess the beginnings of an incremental state architecture?

Yes. The beginning is cached State plus tail replay and dependent read-model caches keyed by State projection identity. It is coarse, but implementation-backed.

### What currently evolves incrementally?

Event application can evolve a cached State by replaying only events after the cached `last_event_id`. The projection snapshot then advances to the current ledger boundary. Dependent read models can be reused without recomputation when their State dependency matches exactly.

### What still requires global recomputation?

Projection finalization, fact supports, inferred facts, aliases, measurement retention, relationships, entity type assertions, graph validation, conflicts, state summary rebuild, fact-index rebuild, and answer/context composition still operate globally within their inputs after a cache miss or tail replay.

### Can affected scope be recovered?

Partially. It can be recovered from existing event kinds and payloads at the State collection/record and fact subject/predicate/dimension level. It cannot yet be recovered as a complete downstream projection dirty set.

### Can projection dependency be recovered?

Partially. It can be recovered as call order and cache dependency keys. It is not yet declared as a machine-readable dependency graph.

### Can bounded state evolution be explained using current implementation?

Yes, as an emerging architecture: append-only events affect bounded State records, which feed derived projections and read models. But current code uses that structure mostly for correctness, caching, and explanation, not yet for bounded recomputation.

### What is the smallest implementation-backed path toward incremental state evolution?

Recover affected scope explicitly and test it before changing projection behavior. The first implementation should report the scope implied by current event handlers and projection dependencies; only later should it control recomputation.
