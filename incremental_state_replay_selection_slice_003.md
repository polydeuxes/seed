# Incremental State Replay Selection Slice 003

## Selected architectural boundary

This slice recovers exactly one implementation-visible ownership boundary:

```text
Affected Projection Recovery != Replay Selection
```

The slice does not implement incremental replay, replay optimization, dependency scheduling, cache invalidation, schema changes, CLI changes, or ledger changes.

## Implementation evidence

Implementation evidence was recovered from `seed_runtime/state.py` and `tests/test_state_projector.py`.

`StateProjector.apply(...)` already recovered an `_AffectedScope` for each event and then recovered an `_AffectedProjectionSet` before applying the event payload. That showed affected projection recovery existed, but replay selection had no separate owner.

`StateProjector.project_from_state(...)` still materializes the supplied events, replays every event, and calls `finalize(...)` after replay. `finalize(...)` still rebuilds the existing derived projection indexes. Replay behavior therefore remains full replay plus full finalization.

## Before

Affected projection recovery and replay selection were compressed at the `StateProjector.apply(...)` call site:

```text
_recover_affected_scope(event)
  -> _recover_affected_projections(scope)
  -> event payload application
  -> project_from_state(...).finalize(...)
```

The `_AffectedProjectionSet` represented candidate derived projections that may read the affected scope, but there was no explicit implementation-local object or function distinguishing those candidates from selected replay work.

## After

The slice adds an implementation-local `_ReplaySelection` value object and `_select_replay_targets(...)` helper.

`StateProjector.apply(...)` now performs:

```text
_recover_affected_scope(event)
  -> _recover_affected_projections(scope)
  -> _select_replay_targets(affected_projections)
  -> event payload application
```

The selected replay targets intentionally remain:

```text
event_replay
projection_finalization
```

The recovered affected projections are preserved as input evidence on `_ReplaySelection`; they are not used to narrow, skip, schedule, invalidate, or optimize replay.

## Boundary made explicit

`_AffectedProjectionSet` answers:

```text
Which derived projections may depend upon this affected scope?
```

`_ReplaySelection` answers:

```text
What replay work will this compatible projector execute?
```

The current answer is still full event replay and full projection finalization, regardless of affected projection candidates. This makes the ownership boundary directly observable without changing runtime behavior.

## Compatibility preserved

No compatibility boundary changed.

Replay execution remains unchanged:

- no incremental replay;
- no projection scheduler;
- no dependency graph;
- no dirty-state engine;
- no cache invalidation change;
- no projection optimization;
- no CLI, schema, or ledger change.

Expected answer to the compatibility question: **No.**

## Files changed

- `seed_runtime/state.py`
  - Added `_ReplaySelection`.
  - Added `_select_replay_targets(...)`.
  - Updated `StateProjector.apply(...)` to make replay selection explicit after affected projection recovery.
- `tests/test_state_projector.py`
  - Added tests proving replay selection is separate from affected projection recovery.
  - Added tests proving empty candidate sets still select full replay/finalization.

## LOC changed

```text
seed_runtime/state.py          +32 / -1
tests/test_state_projector.py  +21 / -0
```

Total:

```text
53 insertions, 1 deletion
```

## Tests executed

```text
pytest -q tests/test_state_projector.py
```

Result:

```text
34 passed
```

## Remaining compressed incremental-state boundaries

This slice stops after one recovered boundary. Remaining compressed or deliberately unimplemented incremental-state areas include:

- replay selection is explicit but not used for incremental replay;
- replay execution remains full replay;
- projection finalization remains full finalization;
- no dependency graph exists between affected scopes and projection builders;
- no dirty projection set exists;
- projection cache invalidation remains unchanged;
- dependent read-model refresh remains outside this slice;
- candidate projection knowledge remains descriptive, not scheduling authority.

## Acceptance summary

Exactly one recovered architectural boundary is now implementation-visible:

```text
Affected Projection Recovery != Replay Selection
```

Replay behavior is unchanged, compatibility is preserved, and Incremental State Evolution gains the next implementation-visible ownership boundary without replay optimization or dependency scheduling.
