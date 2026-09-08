# Incremental State Replay Execution Slice 004

## selected architectural boundary

Recovered exactly one compatibility-preserving ownership boundary:

```text
Replay Selection
!=
Replay Execution
```

This slice does not implement incremental replay, projection narrowing, dependency scheduling, dirty propagation, cache invalidation changes, projection optimization, runtime behavior changes, CLI changes, schema changes, or ledger changes.

## implementation evidence

Implementation review showed the pre-existing replay ownership chain in `seed_runtime/state.py`:

```text
StateProjector.project_from_state(...)
  materializes events
  defines replay_events()
  executes replay_events()
  executes finalize(...)
```

Before this slice, `_ReplaySelection` and `_select_replay_targets(...)` existed, but `project_from_state(...)` still directly owned replay execution and projection finalization. Selection could answer what the compatible replay target set was, but there was no implementation-local replay execution owner consuming that selection.

This slice adds implementation-local replay execution evidence:

```text
_ReplayExecutionRequest(selection=_ReplaySelection(...))
_execute_replay_selection(request, replay_events=..., finalize=...)
```

`_execute_replay_selection(...)` consumes `_ReplayExecutionRequest`, checks that the compatible selected targets remain exactly:

```text
event_replay
projection_finalization
```

and then executes the same full replay callback followed by the same full finalization callback.

## before

Replay execution was compressed into `StateProjector.project_from_state(...)`:

```text
if diagnostics is not None:
    diagnostics.timed("event replay", replay_events)
else:
    replay_events()
return self.finalize(state, diagnostics=diagnostics)
```

That made replay selection observable as a value object, but execution of the selected replay remained owned by the projector method body that also materialized events, tracked progress cadence, and finalized projections.

## after

`StateProjector.project_from_state(...)` now builds a compatible replay selection, wraps it in `_ReplayExecutionRequest`, and delegates execution to `_execute_replay_selection(...)`:

```text
replay_selection = _select_replay_targets(_AffectedProjectionSet(()))
replay_request = _ReplayExecutionRequest(selection=replay_selection)
return _execute_replay_selection(
    replay_request,
    replay_events=...,
    finalize=...,
)
```

Replay execution is now an implementation-local adapter that consumes replay selection and performs the same full replay plus full finalization.

## boundary made explicit

The recovered boundary is now directly observable in code and tests:

```text
Replay Selection
  -> _ReplaySelection

Replay Execution Request
  -> _ReplayExecutionRequest(selection=_ReplaySelection)

Replay Execution
  -> _execute_replay_selection(request, replay_events, finalize)
```

Execution consumes selection. Selection is not used to narrow replay. Execution still performs full event replay and full projection finalization.

## compatibility preserved

No compatibility boundary changed.

The selected target set remains:

```text
("event_replay", "projection_finalization")
```

The execution order remains:

```text
full event replay
full projection finalization
```

The existing projection behavior, scheduling, cache behavior, finalization builders, CLI surface, schema, and ledger behavior are unchanged.

## files changed

- `seed_runtime/state.py`
  - Added `_ReplayExecutionRequest`.
  - Added `_execute_replay_selection(...)`.
  - Updated `StateProjector.project_from_state(...)` to delegate full replay plus finalization through replay execution.
- `tests/test_state_projector.py`
  - Added a test proving replay execution consumes replay selection without narrowing.

## LOC changed

`git diff --stat` after the implementation slice reported:

```text
 seed_runtime/state.py         | 46 ++++++++++++++++++++++++++++++++++++++-----
 tests/test_state_projector.py | 17 ++++++++++++++++
 2 files changed, 58 insertions(+), 5 deletions(-)
```

## tests executed

```text
pytest -q tests/test_state_projector.py
```

Result:

```text
35 passed
```

## remaining compressed incremental-state boundaries

Known remaining boundaries are intentionally not recovered in this slice.

Potential future implementation-visible boundaries may still exist around:

- durable cache lookup versus cache validity decision;
- cache validity decision versus full rebuild fallback;
- replay execution versus projection finalization internals;
- projection finalization ordering versus individual projection builder ownership;
- diagnostics timing collection versus projection execution.

Those are not changed here. This slice stops after recovering exactly one boundary:

```text
Replay Selection
!=
Replay Execution
```
