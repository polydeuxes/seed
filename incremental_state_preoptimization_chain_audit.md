# Incremental State Pre-optimization Chain Audit

## Scope

This is a bounded implementation audit of the replay ownership chain around `StateProjector`, projection replay, projection execution, projection builders, and projection cache behavior.

This audit does not introduce incremental replay, dependency tracking, cache invalidation, projection optimization, CLI changes, schema changes, runtime behavior changes, or ledger changes. It characterizes the current implementation only.

## Executive answer

**Yes, the pre-optimization replay ownership chain has been recovered as implementation-visible architecture.** The implementation now exposes distinct local responsibilities for:

```text
State Event
↓
Affected Scope Recovery
↓
Affected Projection Recovery
↓
Replay Selection
↓
Replay Execution
```

The evidence supports beginning future behavior-changing incremental replay work **only if that work treats behavior change as the next kind of work**, not as more ownership recovery of this chain. However, safe optimization is still blocked by missing behavior-specific mechanisms: no dependency graph, no dirty projection state, no selective finalization contract, no projection-builder dependency declarations, and no cache invalidation model beyond snapshot version and latest event identity.

Therefore:

- **Ownership-chain recovery is complete enough to stop adding more pre-optimization chain slices.**
- **Behavior-changing incremental replay should not be implemented by reusing the current descriptive helpers as if they were a scheduler or dependency graph.**
- **The next implementation step should be a small behavior-enabling characterization or proof boundary, not another documentation-only architecture slice.**

## Recovered ownership chain

| Chain step | Implementation evidence | Owner | Responsibility | Inputs | Outputs | Remaining compression | Limitations |
|---|---|---|---|---|---|---|---|
| State Event | `StateProjector.project(...)` reads workspace events from the ledger and passes them to `project_from_state(...)`. `project_from_state(...)` iterates events in materialized ledger order, sets `state.last_event_id`, and applies each event. | `EventLedger` owns append-only event history; `StateProjector.project_from_state(...)` owns replay consumption of those events. | Provide ordered event input authority for projection replay. | Workspace id, ledger events. | Materialized event list; per-event application calls. | Event materialization, replay loop, progress cadence, and finalization are still coordinated inside `project_from_state(...)`. | No as-of/historical projection API is implied; replay order remains ledger order. |
| Affected Scope Recovery | `_AffectedScope` and `_recover_affected_scope(event)` return direct projected-state collection and identity for known event kinds before mutation. | `_recover_affected_scope(...)`. | Translate a state event into the direct projected collection/identity it may touch. | One `Event`. | `_AffectedScope(collection, identity, subject_id)` or `None`. | Scope recovery is called from `StateProjector.apply(...)`, which still also decodes payloads and mutates state. | This is descriptive visibility only; it does not drive event filtering, dirty state, scheduling, or cache invalidation. |
| Affected Projection Recovery | `_AffectedProjectionSet` and `_recover_affected_projections(scope)` map fact/evidence scopes to derived projection names that may read those scopes. | `_recover_affected_projections(...)`. | Translate direct affected state scope into candidate derived projection surfaces. | `_AffectedScope` or `None`. | `_AffectedProjectionSet(names=...)`. | Projection knowledge is a hard-coded descriptive mapping and is not derived from builder declarations. | It is not dependency tracking. Unknown scopes return an empty projection set rather than proving no dependency. |
| Replay Selection | `_ReplaySelection` and `_select_replay_targets(...)` preserve candidate affected projections as input evidence while selecting the compatible full replay target set. | `_select_replay_targets(...)`. | Decide what replay work this compatible projector will execute. | `_AffectedProjectionSet`. | `_ReplaySelection(affected_projections=..., replay_targets=("event_replay", "projection_finalization"))`. | Selection is invoked in `apply(...)` for event-local visibility and in `project_from_state(...)` with an empty candidate set for the full compatible replay path. | Selection intentionally never narrows replay and never chooses individual projection builders. |
| Replay Execution | `_ReplayExecutionRequest` and `_execute_replay_selection(...)` consume selection, validate the supported target tuple, execute replay callback, then finalization callback. | `_execute_replay_selection(...)`. | Execute an already selected compatible replay request. | `_ReplayExecutionRequest`, `replay_events` callback, `finalize` callback. | Finalized `State`. | Execution delegates replay details and finalization internals back to callbacks owned by `StateProjector.project_from_state(...)` and `StateProjector.finalize(...)`. | Only full event replay plus full projection finalization is supported. Unsupported target tuples raise `ValueError`. |

## Implementation evidence

### StateProjector replay and finalization

`StateProjector` is explicitly the state-projection owner: it reads append-only events, applies them, and produces projected `State`. `project(...)` creates a fresh `State` and passes ledger events into `project_from_state(...)`. `project_from_state(...)` materializes the event iterable, counts projection events, assigns `state.last_event_id`, calls `apply(...)` for every event, and then delegates compatible replay execution through `_execute_replay_selection(...)`.

`finalize(...)` remains the full projection-builder owner for derived indexes. It rebuilds alias resolution, measurement evidence scans, measurement retention, inferred facts, fact partitions, provenance pruning, fact supports, legacy relationships, catalog relationships, entity type assertions, graph issues, entity aliases, and fact conflicts.

### Affected scope and affected projection recovery

`StateProjector.apply(...)` begins by recovering direct affected scope, recovering candidate affected projections, and selecting replay targets before entering event-kind mutation branches. `_recover_affected_scope(...)` knows direct event-to-state-collection mappings such as entities, observations, evidence, facts, goals, tool needs, approvals, execution authorization/proposal state, handoff plans, pending actions, action plans, and registered tools.

`_recover_affected_projections(...)` is narrower. It maps fact scope to derived projections that read fact material and evidence scope to relationship/entity/graph surfaces that may read evidence. It returns an empty set for unsupported or unknown scope. This is important: empty means **no recovered projection knowledge in this helper**, not a proven absence of dependency.

### Replay selection and replay execution

`_select_replay_targets(...)` always returns the compatible full target set:

```text
("event_replay", "projection_finalization")
```

It stores affected projections as input evidence, but it does not narrow replay.

`_execute_replay_selection(...)` is now the execution boundary. It consumes `_ReplayExecutionRequest`, rejects unsupported target sets, runs the replay callback, and then runs finalization. This separates selection from execution without changing behavior.

### Projection cache behavior

`ProjectionStore` owns reusable projected-state snapshots, not event history and not replay ownership. `project_state_with_cache(...)` loads a matching projection snapshot by workspace, projection name, and projection version. A snapshot hit is valid when its last event id equals the current latest event id. If a materialized snapshot is valid, the function returns it without replay.

If a snapshot exists but is stale and materializes safely, `project_state_with_cache(...)` can call `projector.project_from_state(snapshot_state, remaining_events)` and then save a new snapshot. This is already behavior-visible as `incremental_replay=True` in `StateCacheStatus`, but it is **not** affected-projection optimization: remaining ledger events are still replayed in order and `StateProjector.project_from_state(...)` still performs full finalization.

The cache therefore remains tip-snapshot reuse plus suffix replay from a previously saved full state snapshot. It does not own dependency decisions, dirty-state propagation, projection-builder scheduling, or selective finalization.

## Ownership analysis

### Boundary 1: State Event != Affected Scope Recovery

This boundary is implementation-visible and adequately recovered. `Event` remains ledger input authority, while `_recover_affected_scope(...)` is a separate implementation-local translator from event kind/payload shape to projected collection identity.

The limitation is that `StateProjector.apply(...)` still owns both the call to scope recovery and the actual mutation branch. That is acceptable for pre-optimization ownership recovery because the responsibilities are visible and testable, but it is not a mutation-planning engine.

### Boundary 2: Affected Scope Recovery != Affected Projection Recovery

This boundary is implementation-visible and adequately recovered. `_AffectedScope` answers what direct state collection may change. `_AffectedProjectionSet` answers which named derived surfaces may read that scope.

The limitation is important: affected projection recovery is a hand-maintained descriptive list. Projection builders do not declare dependencies, and unsupported scopes returning an empty set must not be interpreted as proof that no derived projection is affected.

### Boundary 3: Affected Projection Recovery != Replay Selection

This boundary is implementation-visible and adequately recovered. `_AffectedProjectionSet` is candidate/read-side visibility. `_ReplaySelection` is selected work. The current selected work is always full event replay and full projection finalization.

The limitation is that selection is intentionally compatible and conservative. It cannot support optimization until a behavior-changing slice defines when and how selected targets may differ.

### Boundary 4: Replay Selection != Replay Execution

This boundary is implementation-visible and adequately recovered. `_execute_replay_selection(...)` consumes an explicit request and executes the selected compatible target set. It validates that only the current full replay/finalization target set is supported.

The limitation is that execution is still callback-based. It does not own per-builder execution bookkeeping, selective finalization, or cache mutation policy.

## Remaining compressed responsibilities

The chain itself is recovered, but several implementation responsibilities remain intentionally compressed outside the chain:

1. **Projection-builder dependency knowledge remains compressed in `finalize(...)`.** The builder order and read dependencies are visible only by reading the full finalization method and helper calls. There is no builder dependency declaration or builder-owned invalidation contract.
2. **Projection finalization remains all-or-nothing.** Even when affected projection names are recovered, `finalize(...)` rebuilds every derived projection surface.
3. **Projection cache validity remains snapshot/tip based.** Cache validity is based on projection version and latest event id equality, with suffix replay from a snapshot when possible. It is not based on affected scopes or affected projections.
4. **Cache mutation remains coupled to projection loading orchestration.** `project_state_with_cache(...)` owns load, hit/miss interpretation, suffix replay orchestration, snapshot save, status emission, and returned cache status.
5. **Projection execution bookkeeping remains split across status, diagnostics, and replay callbacks.** `ProjectionBuildDiagnostics` records timings/counters, while status consumers receive progress/status messages. Neither constitutes replay ownership.
6. **Affected projection recovery is descriptive, not authoritative.** It currently covers fact and evidence downstream surfaces but does not prove completeness for all scopes or future builders.
7. **Projection builders do not own replay decisions.** This is good for compatibility, but it means there is no implemented place yet where a builder can say it is clean, dirty, reusable, or selectively rebuildable.

## Blocking assumptions and counterexamples

The audit found no implementation counterexample that invalidates the recovered ownership chain itself. It did find assumptions that would block safe behavioral optimization if treated as already solved:

- **Implicit dependency assumptions remain.** The affected projection mapping names some fact/evidence readers, but dependency knowledge is not declared by builders.
- **Hidden projection coupling remains possible.** Finalization order encodes coupling among alias projection, measurement retention, inferred facts, relationship projection, entity type assertions, graph validation, and conflicts.
- **Projection builders do not own dependency contracts.** Builders are helper functions called by `finalize(...)`, not independently declared build nodes.
- **Cache state must not be treated as replay ownership.** `ProjectionStore` owns reusable snapshots. It does not own event authority or affected-projection truth.
- **Mutation and replay execution remain adjacent.** `StateProjector.apply(...)` mutates state per event; `_execute_replay_selection(...)` executes replay/finalization callbacks. There is separation now, but not a selective mutation protocol.
- **Existing suffix replay is not incremental projection optimization.** The cache path may apply only events after a snapshot, but the state snapshot is already a full projected state and finalization still runs globally after suffix events.

## Supported conclusions

Implementation evidence supports these conclusions:

1. The pre-optimization ownership chain is implementation-visible from event input through replay execution.
2. Each recovered step now has one named implementation responsibility.
3. Replay behavior remains conservative: full event replay for fresh projection and full projection finalization for both full and suffix replay paths.
4. Projection cache behavior remains compatibility-oriented snapshot reuse, not dependency-aware incremental replay.
5. The repository has reached the point where additional work should primarily define behavior-changing mechanisms rather than continue recovering this same ownership chain.

## Unsupported conclusions

Implementation evidence does **not** support these conclusions:

1. The repository already has dependency-aware incremental replay.
2. `_AffectedProjectionSet` is a complete dependency graph.
3. Empty affected projection recovery proves no derived projection is affected.
4. Replay selection can safely skip event replay or projection finalization today.
5. Projection builders can already be selectively scheduled.
6. Projection cache invalidation already understands affected scopes, affected projections, or dirty derived indexes.
7. Existing suffix replay from cache is the same as future incremental replay optimization.

## Recommended next implementation step

Do **not** implement another pre-optimization ownership slice for this chain. The chain is sufficiently recovered.

The next implementation step should be a small behavior-enabling characterization before optimization, for example:

1. Add tests that explicitly lock current compatibility semantics around cached suffix replay and full finalization.
2. Characterize which finalization outputs change for one or two concrete event kinds without introducing a dependency graph.
3. If behavior-changing incremental replay is selected next, start with one narrow projection builder and one explicit safety fallback to full finalization.

The safest immediate direction is **behavior characterization before behavior optimization**, not more architecture-only ownership recovery.

## Final answer to acceptance questions

### Is the replay ownership chain complete?

Yes, as a pre-optimization ownership chain. It is complete enough to distinguish event input, affected scope recovery, affected projection recovery, replay selection, and replay execution.

### What implementation evidence supports that conclusion?

The evidence is the set of implementation-local owners in `seed_runtime/state.py`: `_AffectedScope`, `_recover_affected_scope(...)`, `_AffectedProjectionSet`, `_recover_affected_projections(...)`, `_ReplaySelection`, `_select_replay_targets(...)`, `_ReplayExecutionRequest`, and `_execute_replay_selection(...)`, plus the `StateProjector.project_from_state(...)` call sequence that delegates selected compatible replay execution.

### What still blocks safe behavioral optimization?

Safe optimization is blocked by missing dependency declarations, missing dirty-state semantics, missing selective finalization contracts, descriptive-only affected projection knowledge, snapshot/tip-only cache validity, and hidden coupling in full finalization order.

### Should the repository continue recovering ownership, or has it reached behavior-changing work?

For this chain, ownership recovery should stop. Future work should primarily change behavior only after adding targeted characterization and safety tests. Additional ownership recovery may still be needed inside projection builders or cache invalidation if a specific optimization requires it, but not as another slice of the already recovered replay chain.
