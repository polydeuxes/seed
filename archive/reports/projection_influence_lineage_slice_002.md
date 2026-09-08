# Projection Influence Lineage Slice 002

## Selected architectural boundary

Projection influence lineage is now separated from replay scope assessment inside the implementation-local state projection path.

The recovered owner is `_ReplayScopeAssessment`: a private assessment carrier for replay necessity derived from existing projection influence lineage. It preserves:

- the projection influence lineage being assessed;
- the compatible projector's answer that replay work is required.

It does not own replay execution, projection replay, cache invalidation, projection computation, projection storage, rendering, scheduling, CLI behavior, JSON shape, event shape, ledger replay, projection versions, or read-model behavior.

## Implementation evidence

Implementation evidence showed the transition point in `seed_runtime/state.py`:

- `_recover_projection_influence_lineage(events)` already recovers source event ids, affected scopes, and affected projection evidence without selecting replay targets.
- `_select_replay_targets(...)` previously accepted lineage directly and returned full compatible replay targets.
- `StateProjector.project_from_state(...)` immediately moved from recovered lineage into target selection.
- `_execute_replay_selection(...)` still only consumes selected targets and executes full event replay followed by full projection finalization.

That meant the answer to "given this lineage, is replay required?" was compressed into replay target selection.

## Before

Before this slice, the projection build path moved directly from lineage recovery to replay selection:

```python
influence_lineage = _recover_projection_influence_lineage(event_list)
replay_selection = _select_replay_targets(influence_lineage)
```

Replay selection therefore mixed two implementation-local responsibilities:

1. assessing replay necessity from projection influence lineage; and
2. selecting the compatible target set to execute.

## After

After this slice, `_ReplayScopeAssessment` owns replay-necessity assessment from lineage:

```python
@dataclass(frozen=True)
class _ReplayScopeAssessment:
    influence_lineage: _ProjectionInfluenceLineage
    replay_required: bool
```

The projection build path now makes the transition explicit:

```python
influence_lineage = _recover_projection_influence_lineage(event_list)
replay_assessment = _assess_replay_scope(influence_lineage)
replay_selection = _select_replay_targets(replay_assessment)
```

`_select_replay_targets(...)` now consumes `_ReplayScopeAssessment`, preserving selection as the compatible target-set owner rather than the replay-necessity owner.

## Boundary made explicit

The recovered boundary is:

```text
Projection Influence Lineage
        !=
Replay Scope Assessment
        !=
Replay Selection
```

This makes replay necessity directly observable in private implementation structure while leaving replay target compatibility and execution unchanged.

## Compatibility preserved

No compatibility boundary changed.

The implementation still assesses replay as required for every projection build, including empty lineage, and still selects the same compatible full replay target set:

```text
event_replay -> projection_finalization
```

No CLI, JSON, event, ledger, cache, schema, projection version, projection algorithm, read model, storage, or runtime diagnostic surface changed.

## Files changed

- `seed_runtime/state.py`
- `tests/test_state_projector.py`
- `projection_influence_lineage_slice_002.md`

## LOC changed

From `git diff --stat` before this report was added:

```text
seed_runtime/state.py                              | 52 +++++++++++++++++-----
tests/test_state_projector.py                      | 45 +++++++++++++++----
3 files changed, 79 insertions(+), 20 deletions(-)
```

This report adds the slice deliverable only. The generated architecture graph changed only because the private implementation-local additions shifted the recorded `StateProjector` line number.

## Tests executed

```text
pytest -q tests/test_state_projector.py
pytest -q tests/test_state_projector.py tests/test_architecture_generator.py
pytest -q
```

Results:

```text
37 passed
39 passed
1588 passed
```

## Remaining compressed projection-lineage responsibilities

Remaining possible compression is intentionally left in place for future bounded slices:

- replay target compatibility still remains a full replay/finalization selection and was not redesigned;
- projection-store cache hit/miss reasons are still not modeled as projection influence lineage or replay scope assessment;
- dependent summary/index snapshot validity remains local to projection store methods;
- projection-shape diagnostic descriptions remain separate from runtime lineage evidence;
- no public diagnostic or runtime explanation surface was introduced.

## Observations about emerging family vocabulary

The implementation vocabulary now distinguishes:

- affected scope: direct projected-state collection and identity touched by an event;
- affected projection set: derived projection surfaces that may read that scope;
- projection influence lineage: event-to-scope-to-derived-projection evidence explaining why projection work may be required;
- replay scope assessment: the implementation-local answer that replay is required from existing lineage evidence;
- replay selection: the compatible execution target set, still full replay plus finalization;
- replay execution: the consumer of selected targets that performs event replay and projection finalization.

`Replay Scope Assessment` is precise enough for the recovered implementation evidence in this slice: the owner assesses replay necessity from lineage while deliberately not owning target compatibility, execution, projection computation, or cache behavior.
