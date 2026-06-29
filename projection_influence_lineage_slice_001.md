# Projection Influence Lineage Slice 001

## Selected architectural boundary

Projection result is now separated from projection influence lineage inside the implementation-local state projection path.

The recovered owner is `_ProjectionInfluenceLineage`: a private evidence carrier for why projection work may be required. It preserves existing implementation evidence only:

- source event ids supplied to projection replay;
- direct projected-state scopes recovered from events;
- derived projection surfaces that may read those scopes.

It does not own replay execution, projection computation, cache invalidation, snapshot persistence, read-model construction, rendering, scheduling, or cluster mutation.

## Implementation evidence

Implementation evidence showed a recurring compression in `seed_runtime/state.py`:

- `_recover_affected_scope(event)` already identified direct projected-state scopes touched by event application.
- `_recover_affected_projections(scope)` already identified derived projection surfaces that may read those scopes.
- `_select_replay_targets(...)` preserved affected projection evidence while selecting the compatible replay target set.
- `StateProjector.project_from_state(...)` still executed full event replay followed by full projection finalization.

That meant the explanation evidence for "why was this projection rebuilt?" was partially carried by replay selection rather than by a dedicated influence-lineage owner.

## Before

Before this slice, replay selection directly owned the affected projection evidence:

```python
@dataclass(frozen=True)
class _ReplaySelection:
    affected_projections: _AffectedProjectionSet
    replay_targets: tuple[str, ...]
```

This mixed two implementation-local responsibilities:

1. describing projection influence evidence; and
2. selecting compatible replay targets.

## After

After this slice, `_ProjectionInfluenceLineage` owns the influence evidence:

```python
@dataclass(frozen=True)
class _ProjectionInfluenceLineage:
    source_event_ids: tuple[str, ...]
    affected_scopes: tuple[_AffectedScope, ...]
    affected_projections: _AffectedProjectionSet
```

Replay selection now consumes lineage evidence without interpreting it as replay scope:

```python
@dataclass(frozen=True)
class _ReplaySelection:
    influence_lineage: _ProjectionInfluenceLineage
    replay_targets: tuple[str, ...]
```

`_recover_projection_influence_lineage(events)` composes the existing affected-scope and affected-projection recovery evidence. It does not introduce a runtime surface or alter projection outputs.

## Boundary made explicit

The recovered boundary is:

```text
Projection Influence Lineage
        !=
Replay Target Selection
        !=
Projection Result
```

This makes the projection rebuild explanation more explicit while leaving the projection result path unchanged.

## Compatibility preserved

No compatibility boundary changed.

The implementation still performs the same compatible replay work:

```text
event_replay -> projection_finalization
```

No CLI, JSON, event, ledger, cache, schema, projection version, projection algorithm, read model, or storage behavior changed.

## Files changed

- `seed_runtime/state.py`
- `tests/test_state_projector.py`
- `docs/generated/architecture/architecture_graph.json`
- `projection_influence_lineage_slice_001.md`

## LOC changed

From `git diff --stat` before this report was added:

```text
.../generated/architecture/architecture_graph.json |  2 +-
seed_runtime/state.py                              | 68 ++++++++++++++++++----
tests/test_state_projector.py                      | 62 ++++++++++++++++----
3 files changed, 110 insertions(+), 22 deletions(-)
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
36 passed
38 passed
1587 passed
```

## Remaining compressed projection-lineage responsibilities

Remaining possible compression is intentionally left in place for future bounded slices:

- projection-store cache hit/miss reasons are still not modeled as influence lineage;
- dependent summary/index snapshot validity remains local to projection store methods;
- projection-shape diagnostic descriptions remain separate from runtime lineage evidence;
- no public diagnostic or runtime explanation surface was introduced.

## Observations about the emerging family vocabulary

The implementation vocabulary now distinguishes:

- affected scope: direct projected-state collection and identity touched by an event;
- affected projection set: derived projection surfaces that may read that scope;
- projection influence lineage: event-to-scope-to-derived-projection evidence explaining why projection work may be required;
- replay selection: the compatible execution target set, still full replay plus finalization;
- projection result: the `State` produced by replay and finalization.

The family vocabulary remains implementation-local and evidence-backed. It does not promote presentation vocabulary into repository knowledge or add a new operational surface.
