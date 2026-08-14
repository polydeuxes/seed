# Projection Influence Lineage Slice 004

## Selected architectural boundary

Projection publication is now directly observable as separate from projection finalization.

Recovered boundary:

```text
Projection Finalization
    !=
Projection Publication
```

The implementation-local owner is `_ProjectionPublication`. It preserves only the existing handoff from finalized projection state to the consumer-visible projected `State` returned by `StateProjector.project(...)` and `StateProjector.project_from_state(...)`.

## Implementation evidence

The relevant implementation path remains the private state projection path in `seed_runtime/state.py`:

1. `_recover_projection_influence_lineage(...)` recovers source event, affected scope, and affected projection evidence.
2. `_assess_replay_scope(...)` converts that lineage into replay necessity.
3. `_justify_replay_selection(...)` preserves the compatible target-set justification.
4. `_select_replay_targets(...)` selects the compatible replay targets.
5. `_execute_replay_selection(...)` executes full event replay followed by full projection finalization.
6. `_publish_finalized_projection(...)` now owns the identity-preserving handoff of finalized projection state to consumer-visible projected state.

The recovered owner is intentionally narrow:

```python
@dataclass(frozen=True)
class _ProjectionPublicationRequest:
    finalized_state: State


@dataclass(frozen=True)
class _ProjectionPublication:
    request: _ProjectionPublicationRequest
    visible_state: State
```

The publication helper preserves the same object identity that the previous code returned directly:

```python
return _ProjectionPublication(
    request=request,
    visible_state=request.finalized_state,
)
```

`StateProjector.project_from_state(...)` now names the two responsibilities separately:

```python
finalized_state = _execute_replay_selection(...)
publication = _publish_finalized_projection(
    _ProjectionPublicationRequest(finalized_state=finalized_state)
)
return publication.visible_state
```

Tests prove that publication preserves finalized-state identity and that the consumer-visible projection still contains the same projected state after `StateProjector.project(...)`.

## Before

Before this slice, `StateProjector.project_from_state(...)` returned the result of `_execute_replay_selection(...)` directly. Because `_execute_replay_selection(...)` invokes `finalize(...)` and returns its result, the method made projection finalization and publication to consumers appear as a single return boundary.

That compressed two responsibilities:

```text
finalize derived projection indexes
```

and:

```text
handoff finalized state as the consumer-visible projected state
```

No separate implementation-local owner represented the publication handoff.

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

Projection Finalization
    -> StateProjector.finalize(...)

Projection Publication
    -> _ProjectionPublication
```

`StateProjector.finalize(...)` still owns derived projection indexes. `_publish_finalized_projection(...)` owns only the subsequent publication handoff. It does not own replay execution, replay assessment, replay selection, projection computation, cache invalidation, rendering, CLI behavior, scheduling, storage, JSON, events, or ledger replay.

## Boundary made explicit

The recovered boundary is:

```text
Projection Finalization
    !=
Projection Publication
```

This boundary is implementation-backed because finalized projection state is now captured in `_ProjectionPublicationRequest`, and the consumer-visible state is carried by `_ProjectionPublication.visible_state`. The publication step is intentionally identity-preserving, making the owner observable without changing behavior.

## Compatibility preserved

No compatibility boundary changed.

The compatible replay target tuple remains exactly:

```text
event_replay
projection_finalization
```

Projection contents, read-model semantics, cache behavior, projection storage, projection versions, CLI behavior, JSON output, event semantics, and ledger replay semantics are unchanged. Consumers receive the same finalized `State` object that prior code returned directly.

## Files changed

- `seed_runtime/state.py`
- `tests/test_state_projector.py`
- `projection_influence_lineage_slice_004.md`

## LOC changed

At the time this report was written, `git diff --stat` reported:

```text
projection_influence_lineage_slice_004.md | 213 ++++++++++++++++++++++++++++++
seed_runtime/state.py                     |  45 ++++++-
tests/test_state_projector.py             |  24 ++++
3 files changed, 281 insertions(+), 1 deletion(-)
```

## Tests executed

```text
pytest -q tests/test_state_projector.py
```

Result:

```text
40 passed
```

## Remaining compressed projection-lineage responsibilities

This slice stops after one recovered owner. Remaining possible compressed responsibilities require fresh implementation evidence before naming or changing them.

Current evidence suggests these areas remain outside this slice:

- replay execution remains separate and unchanged;
- projection computation remains inside finalization and projection helpers;
- cache behavior and projection storage remain unchanged;
- read-model construction and rendering remain unchanged;
- compatibility remains the full replay plus full finalization target tuple;
- any further distinction between projection publication and concrete read-model construction remains unproven by this slice.

## Observations about the emerging family vocabulary

The implementation now supports the following local vocabulary with direct code evidence:

```text
Projection Influence Lineage
Replay Scope Assessment
Replay Selection Justification
Replay Selection
Replay Execution
Projection Finalization
Projection Publication
```

Implementation evidence suggested `Projection Publication` as the more precise local responsibility name for this slice. The code exposes a finalized `State` handoff, not a separate read-model construction step. Calling the recovered owner `Read-Model Publication` would overstate the evidence because the implementation change publishes the finalized projection state object unchanged.

## Questions answered with implementation evidence

### 1. Where were projection finalization and read-model publication previously mixed?

They were mixed at the return boundary in `StateProjector.project_from_state(...)`. The method previously returned `_execute_replay_selection(...)` directly, and `_execute_replay_selection(...)` returned the result of `finalize(...)`. That made finalization and the consumer-visible projection handoff indistinguishable in the implementation.

### 2. Which recovered architectural boundary became more explicit?

`Projection Finalization != Projection Publication` became explicit through `_ProjectionPublicationRequest`, `_ProjectionPublication`, and `_publish_finalized_projection(...)`.

### 3. How does the implementation now better reflect the recovered architecture?

The implementation now stores the result of replay execution and finalization as `finalized_state`, passes it through an implementation-local publication request, and returns `publication.visible_state`. This mirrors the recovered sequence without changing the state object, projection contents, cache behavior, or consumer semantics.

### 4. Did implementation evidence suggest a more precise responsibility name than "Read-Model Publication"?

Yes. `Projection Publication` is more precise. The implementation evidence shows publication of finalized projection `State`; it does not show a separate read-model construction or read-model transformation step at this boundary.

### 5. Did any compatibility boundary change?

No.
