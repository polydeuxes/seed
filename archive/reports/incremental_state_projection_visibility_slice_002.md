# Incremental State Projection Visibility Slice 002

## Selected architectural boundary

This slice recovers exactly one implementation-visible boundary:

```text
Affected Scope
!=
Affected Projection Recovery
```

The boundary is recovered as implementation-local visibility only. It does not implement incremental replay, dependency tracking, dirty propagation, projection scheduling, cache invalidation, CLI behavior, schema behavior, ledger behavior, or projection behavior changes.

## Implementation evidence

The reviewed implementation already had a recovered affected-scope surface:

- `_AffectedScope` identifies the direct projected-state collection and identity an event application may touch.
- `_recover_affected_scope(event)` recovers that scope before `StateProjector.apply(...)` performs event-kind mutation.
- `StateProjector.project_from_state(...)` still replays ledger events in order and calls `finalize(...)` after replay.
- `StateProjector.finalize(...)` still rebuilds derived projection read models such as aliases, measurement history, inferred/observed fact partitions, fact supports, relationships, entity type assertions, graph issues, entity aliases, and fact conflicts.

That meant the first slice had made this question explicit:

```text
What projected state does this event touch?
```

But the implementation still had no separate local representation for the second question:

```text
Which derived projections may read from that affected scope?
```

## Before

Before this slice:

- `_recover_affected_scope(event)` returned direct state-scope knowledge.
- `StateProjector.apply(...)` recovered that scope and then executed the existing mutation branches.
- Derived projection knowledge remained only implicit in `finalize(...)` and its builder calls.
- There was no implementation-local value object representing affected projection recovery separately from affected scope recovery.

The compressed responsibility was not replay behavior; replay remained full replay plus full finalization. The compression was visibility ownership: direct affected state scope and downstream derived projection relevance had to be inferred together by reading both event mutation branches and finalization builders.

## After

This slice adds:

- `_AffectedProjectionSet`, an implementation-local value object for derived projection names that may read an affected scope.
- `_recover_affected_projections(affected_scope)`, a private implementation-local adapter from recovered affected scope to affected projection visibility.
- A `StateProjector.apply(...)` call sequence that now recovers affected scope first and affected projection visibility second, without using either to alter execution.
- Tests proving affected projection recovery is directly observable and remains separate from affected scope.

For fact scope, affected projection recovery names the existing derived projection surfaces currently rebuilt from fact material during finalization:

- `alias_resolver`
- `measurement_history`
- `observed_facts`
- `inferred_facts`
- `fact_supports`
- `entity_relationships`
- `relationships`
- `entity_type_assertions`
- `graph_issues`
- `entity_aliases`
- `fact_conflicts`

For evidence scope, affected projection recovery names existing derived surfaces that may read evidence during finalization:

- `relationships`
- `entity_type_assertions`
- `graph_issues`

For scopes without recovered projection knowledge in this slice, the helper returns an empty `_AffectedProjectionSet`. That is intentionally not dependency tracking.

## Boundary made explicit

The recovered boundary is:

```text
Affected Scope Recovery
  answers: what direct projected-state collection/identity did the event touch?

Affected Projection Recovery
  answers: which existing derived projection surfaces may read that affected scope?
```

The implementation now makes the sequence directly observable:

```text
State Event
↓
Affected Scope Recovery
↓
Affected Projection Recovery
↓
State Mutation
↓
Full Finalization (unchanged)
```

The recovered projection set is not used to schedule, skip, invalidate, cache, mutate, replay incrementally, or mark anything dirty.

## Compatibility preserved

No compatibility boundary changed.

No CLI behavior changed. No schema changed. No ledger behavior changed. No projection cache behavior changed. No replay behavior changed. No finalization behavior changed. No read model output changed.

Expected answer: No.

## Files changed

- `seed_runtime/state.py`
  - Added `_AffectedProjectionSet`.
  - Added `_recover_affected_projections(...)`.
  - Updated `StateProjector.apply(...)` to recover affected projections after affected scope recovery without using that recovery to change behavior.
- `tests/test_state_projector.py`
  - Added tests for affected projection recovery visibility.
  - Added tests proving unsupported/unknown projection recovery remains empty rather than becoming dependency tracking.
- `incremental_state_projection_visibility_slice_002.md`
  - Added this implementation slice report.

## LOC changed

Current diff stat at report time:

```text
seed_runtime/state.py                              | 49 +++++++++++++++++++++++++++++++++++--
tests/test_state_projector.py                     | 56 ++++++++++++++++++++++++++++++++++---------
incremental_state_projection_visibility_slice_002.md | added
```

## Tests executed

```text
python -m black seed_runtime/state.py tests/test_state_projector.py
pytest -q tests/test_state_projector.py
```

Result:

```text
32 passed
```

## Remaining compressed incremental-state boundaries

This slice intentionally stops after recovering exactly one boundary. Remaining compressed boundaries include:

- Affected projection visibility is not dependency tracking.
- Affected projection visibility is not dirty propagation.
- Projection finalization still rebuilds all derived projection surfaces.
- Projection cache reuse remains snapshot/tip based rather than affected-projection based.
- There is no projection scheduler.
- There is no incremental replay behavior.
- There is no cache invalidation change.
