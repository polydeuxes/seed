# Incremental State Scope Visibility Slice 001

## Selected architectural boundary

`State Event != Affected Scope Recovery`.

This slice makes one implementation-visible boundary explicit inside state projection: a ledger event is the input authority, while affected-scope recovery is an implementation-local report describing which projected-state collection and identity the event application may touch.

## Implementation evidence

The reviewed implementation showed the boundary was compressed in `StateProjector.apply(...)`:

- `StateProjector.project_from_state(...)` replays every ledger event, assigns `state.last_event_id`, and calls `self.apply(state, event, diagnostics=diagnostics)` before full finalization.
- `StateProjector.apply(...)` branches on `event.kind`, extracts payload identity fields, decodes event payloads, and mutates the corresponding `State` collection in the same method.
- Finalization still rebuilds derived indexes globally after replay, including alias projection, inferred facts, measurement retention, fact supports, relationships, graph issues, and conflicts.

The event application code therefore already knew what direct state scope each event affected, but that knowledge was only implicit in each mutation branch.

## Before

Before this slice, affected-scope knowledge was embedded in mutation branches:

- `entity.upserted` extracted an entity ID and wrote `state.entities[entity.id]`.
- `fact.observed` / `fact.inferred` decoded a fact and wrote `state.facts[fact.id]`.
- update events such as `tool_need.status_changed`, `action_plan.accepted`, and `pending_action.completed` read IDs from payload fields and conditionally updated the matching projected object.

There was no implementation-local value object or helper that represented the affected scope separately from applying the event.

## After

This slice adds a private implementation-local `_AffectedScope` value object and a private `_recover_affected_scope(event)` helper. The helper reports the direct projected-state collection and identity that event application may touch.

`StateProjector.apply(...)` now calls `_recover_affected_scope(event)` before executing the existing event-kind mutation branches. The recovered scope is not used to alter replay, scheduling, caching, finalization, invalidation, or mutation behavior.

## Boundary made explicit

The newly visible ownership boundary is:

```text
State Event
    !=
Affected Scope Recovery
```

A state event remains the ledger input. Affected scope recovery is now a separate implementation-local responsibility that can be tested independently from state mutation.

## Compatibility preserved

No compatibility boundary changed.

The change does not introduce or modify:

- CLI behavior;
- schema behavior;
- event kinds or payload shapes;
- event ledger writes;
- projection cache behavior;
- dirty tracking;
- incremental replay;
- dependency planning;
- finalization behavior;
- runtime behavior.

## Files changed

- `seed_runtime/state.py`
  - Added `_AffectedScope`.
  - Added `_recover_affected_scope(event)`.
  - Added a call to affected-scope recovery at the start of `StateProjector.apply(...)` without using it to change execution.
- `tests/test_state_projector.py`
  - Added tests proving affected-scope recovery is directly observable before state mutation.
  - Added tests proving update-event scope can be recovered without applying the update.
- `incremental_state_scope_visibility_slice_001.md`
  - Added this implementation slice report.

## LOC changed

Pre-report implementation/test diff:

```text
78 insertions, 0 deletions: seed_runtime/state.py
51 insertions, 0 deletions: tests/test_state_projector.py
```

## Tests executed

```text
pytest -q tests/test_state_projector.py
```

Result:

```text
30 passed
```

## Remaining compressed incremental-state boundaries

This slice intentionally stops after making affected-scope recovery visible. Remaining compressed boundaries include:

- replay still applies all events rather than selecting events by recovered scope;
- finalization still rebuilds all derived projection indexes globally;
- projection cache reuse remains snapshot/tip based rather than affected-scope based;
- no dependency graph declares which derived indexes depend on which recovered scopes;
- no dirty set, scheduler, priority engine, projection planner, or cache invalidation boundary exists;
- diagnostics timing still reports replay/finalization phases, not per-scope incremental work.

Those are not implemented by this slice.
