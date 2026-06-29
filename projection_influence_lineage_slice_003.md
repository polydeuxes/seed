# Projection Influence Lineage Slice 003

## Selected architectural boundary

Replay selection justification is now directly observable as separate from replay selection.

Recovered boundary:

```text
Replay Scope Assessment
    !=
Replay Selection Justification
    !=
Replay Selection
```

The implementation-local owner is `_ReplaySelectionJustification`. It preserves the existing reason that the compatible replay target set remains full event replay plus full projection finalization after replay has been assessed as required.

## Implementation evidence

The relevant implementation path is still the private state projection path in `seed_runtime/state.py`:

1. `_recover_projection_influence_lineage(...)` recovers source event, affected scope, and affected projection evidence.
2. `_assess_replay_scope(...)` converts that lineage into replay necessity.
3. `_justify_replay_selection(...)` preserves the compatible target-set justification.
4. `_select_replay_targets(...)` consumes that justification and returns the selected target set.
5. `_execute_replay_selection(...)` executes only the already selected compatible target tuple.

The recovered owner is intentionally narrow:

```python
@dataclass(frozen=True)
class _ReplaySelectionJustification:
    scope_assessment: _ReplayScopeAssessment
    compatible_replay_targets: tuple[str, ...]
```

Its helper preserves the previous target tuple exactly:

```python
return _ReplaySelectionJustification(
    scope_assessment=scope_assessment,
    compatible_replay_targets=("event_replay", "projection_finalization"),
)
```

Replay selection now consumes that justification:

```python
return _ReplaySelection(
    justification=justification,
    replay_targets=justification.compatible_replay_targets,
)
```

Tests prove the new owner is separate from replay scope assessment and that replay selection consumes it without changing the target tuple.

## Before

Before this slice, `_select_replay_targets(...)` consumed `_ReplayScopeAssessment` directly and returned `_ReplaySelection` with the compatible target tuple. That made one function and one return object own both:

```text
why the compatible full replay target set is the preserved answer
```

and:

```text
the selected target set itself
```

The target selection behavior was already compatible and intentionally non-narrowing, but the justification boundary was compressed into selection.

## After

After this slice, the projection path is explicit:

```text
Projection Influence Lineage
    -> _ProjectionInfluenceLineage

Replay Scope Assessment
    -> _ReplayScopeAssessment

Replay Selection Justification
    -> _ReplaySelectionJustification

Replay Selection
    -> _ReplaySelection

Replay Execution
    -> _ReplayExecutionRequest
```

`_justify_replay_selection(...)` owns only the existing justification for the compatible target set. `_select_replay_targets(...)` owns only the selection value consumed by execution.

## Boundary made explicit

The recovered boundary is:

```text
Replay Selection Justification
    !=
Replay Selection
```

This boundary is implementation-backed because `_ReplaySelectionJustification` carries replay-necessity evidence and the compatible target tuple before `_ReplaySelection` is created. Replay selection no longer has to be inspected to discover both the target set and the implementation-local reason that this projector remains compatible only with full replay plus finalization.

## Compatibility preserved

No compatibility boundary changed.

The compatible target tuple remains exactly:

```text
event_replay
projection_finalization
```

The execution guard in `_execute_replay_selection(...)` remains unchanged and still rejects any unsupported target tuple. Replay execution, projection computation, cache behavior, projection storage, read-model construction, CLI behavior, JSON output, event semantics, and ledger replay semantics are unchanged.

## Files changed

- `seed_runtime/state.py`
- `tests/test_state_projector.py`
- `projection_influence_lineage_slice_003.md`

## LOC changed

At the time this report was written, `git diff --stat` reported:

```text
projection_influence_lineage_slice_003.md | 199 +++++++++++++++++++++++++++++++++
seed_runtime/state.py                    |  62 ++++++++++++----
tests/test_state_projector.py            |  48 ++++++++++--
3 files changed, 288 insertions(+), 21 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_state_projector.py
```

Result:

```text
38 passed
```

## Remaining compressed projection-lineage responsibilities

This slice stops after one recovered owner. Remaining possible compressed responsibilities should be treated as future investigation only and require fresh implementation evidence before naming or changing them.

Current evidence suggests these areas remain outside this slice:

- replay execution remains separate and unchanged;
- projection computation remains inside finalization and projection helpers;
- cache behavior and projection storage remain unchanged;
- read-model construction and rendering remain unchanged;
- compatibility remains the full replay plus full finalization target tuple.

Potential future pressure may exist around how finalization stages explain their own local influence, but this slice does not promote that vocabulary or create a new owner for it.

## Observations about the emerging family vocabulary

The implementation now supports the following local vocabulary with direct code evidence:

```text
Projection Influence Lineage
Replay Scope Assessment
Replay Selection Justification
Replay Selection
Replay Execution
```

The term `Replay Selection Justification` is precise enough for this slice because the new owner preserves why the current compatible replay target tuple is carried forward. Implementation evidence did not suggest a more precise responsibility name than `Replay Selection Justification`.

## Questions answered with implementation evidence

### 1. Where were replay selection justification and replay selection previously mixed?

They were mixed in `_select_replay_targets(...)` and `_ReplaySelection`. `_select_replay_targets(...)` directly consumed `_ReplayScopeAssessment`, embedded the compatible full replay target tuple, and returned `_ReplaySelection`. That compressed the justification for the compatible target set with the selected target set itself.

### 2. Which recovered architectural boundary became more explicit?

`Replay Selection Justification != Replay Selection` became explicit through `_ReplaySelectionJustification` and `_justify_replay_selection(...)`.

### 3. How does the implementation now better reflect the recovered architecture?

The implementation now passes through a distinct private value object before selection. `_ReplaySelectionJustification` preserves the replay assessment and compatible target tuple; `_ReplaySelection` consumes that justification and exposes the selected targets for execution. The call sequence now mirrors the recovered ownership sequence instead of skipping from replay scope assessment directly into replay selection.

### 4. Did implementation evidence suggest a more precise responsibility name than "Replay Selection Justification"?

Insufficient implementation evidence.

### 5. Did any compatibility boundary change?

No.
