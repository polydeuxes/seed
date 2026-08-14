# Projection Influence Lineage Family Completion Audit

## Scope

This is a bounded implementation audit of the projection influence lineage responsibility family. It does not add another implementation slice, architectural recovery, CLI surface, renderer, projection redesign, cache redesign, replay optimization, read-model redesign, or vocabulary migration.

The audit reviews current implementation evidence for the chain:

```text
Projection Influence Lineage
    ↓
Replay Scope Assessment
    ↓
Replay Selection Justification
    ↓
Replay Selection
    ↓
Replay Execution
    ↓
Projection Finalization
    ↓
Projection Publication
```

Repository authority wins over architectural preference.

## Supported conclusion

Projection Influence Lineage has become a completed implementation responsibility family for the current conservative replay/projection implementation.

The implementation now exposes a complete decision and handoff chain from event-derived projection influence evidence through replay assessment, target justification, target selection, execution, finalization, and publication. The chain is implementation-local and behavior-preserving: it does not narrow replay, does not optimize finalization, does not alter cache invalidation, and does not publish a new runtime or diagnostic surface.

Completion here means the family has reached a natural stopping point as an ownership-recovery family, not that Seed now has selective replay, dirty projection invalidation, or read-model partial refresh.

## Implemented boundaries

### Projection Influence Lineage

Implemented owner:

```python
_ProjectionInfluenceLineage
_recover_projection_influence_lineage(...)
```

Implementation evidence:

- `_ProjectionInfluenceLineage` preserves source event ids, affected scopes, and affected projection surfaces.
- Its docstring explicitly excludes replay plans, cache dependency graphs, invalidation policy, projection results, and read models.
- `_recover_projection_influence_lineage(...)` composes affected-scope and affected-projection recovery for a materialized event sequence and returns a lineage value.

This boundary answers: which event-derived projected-state scopes and downstream projection surfaces explain why projection work may be required?

### Replay Scope Assessment

Implemented owner:

```python
_ReplayScopeAssessment
_assess_replay_scope(...)
```

Implementation evidence:

- `_ReplayScopeAssessment` carries lineage plus `replay_required`.
- `_assess_replay_scope(...)` consumes lineage and returns `replay_required=True` for the compatible projector, including empty lineage.
- The helper explicitly does not select compatible targets.

This boundary answers: given the recovered lineage, does the current compatible projector require replay work?

### Replay Selection Justification

Implemented owner:

```python
_ReplaySelectionJustification
_justify_replay_selection(...)
```

Implementation evidence:

- `_ReplaySelectionJustification` carries the scope assessment and the compatible replay target tuple.
- `_justify_replay_selection(...)` preserves `("event_replay", "projection_finalization")` as the compatible full replay/finalization target set.
- It justifies the target tuple without executing it.

This boundary answers: why is the selected compatible target set still full event replay plus projection finalization?

### Replay Selection

Implemented owner:

```python
_ReplaySelection
_select_replay_targets(...)
```

Implementation evidence:

- `_ReplaySelection` carries the justification plus selected `replay_targets`.
- `_select_replay_targets(...)` consumes `_ReplaySelectionJustification` and returns the compatible target tuple unchanged.
- Selection remains conservative and does not narrow replay.

This boundary answers: what replay work will this projector execute?

### Replay Execution

Implemented owner:

```python
_ReplayExecutionRequest
_execute_replay_selection(...)
```

Implementation evidence:

- `_ReplayExecutionRequest` wraps an already selected replay.
- `_execute_replay_selection(...)` validates the selected target tuple, executes the replay callback, and then invokes finalization.
- Unsupported target tuples raise `ValueError`.

This boundary answers: how is an already selected compatible replay request executed?

### Projection Finalization

Implemented owner:

```python
StateProjector.finalize(...)
```

Implementation evidence:

- `finalize(...)` owns all current derived projection index rebuilding.
- It rebuilds alias resolution, measurement retention, inferred facts, fact partitions, fact supports, legacy and catalog relationships, entity type assertions, graph issues, entity aliases, and fact conflicts.
- Finalization remains global after replay or suffix replay.

This boundary answers: how are derived projection indexes rebuilt after event application?

### Projection Publication

Implemented owner:

```python
_ProjectionPublicationRequest
_ProjectionPublication
_publish_finalized_projection(...)
```

Implementation evidence:

- `_ProjectionPublicationRequest` carries a finalized `State`.
- `_ProjectionPublication` carries the consumer-visible `State`.
- `_publish_finalized_projection(...)` is intentionally identity-preserving: `visible_state` is the same finalized state object.

This boundary answers: how is finalized projection state handed to consumers as the visible projected state?

## Directly observable chain

`StateProjector.project_from_state(...)` now executes the full chain in order:

```text
materialize events
recover projection influence lineage
assess replay scope
justify replay selection
select replay targets
wrap replay execution request
execute selected replay
finalize projection
publish finalized projection
return visible state
```

The implementation sequence is direct evidence that the family is now observable as a complete chain rather than a compressed owner hidden inside `project_from_state(...)`.

## Counterexample review

### Projection influence and replay assessment

No remaining counterexample found inside this family.

The code separates lineage recovery from replay assessment. `_recover_projection_influence_lineage(...)` returns descriptive event/scope/projection evidence. `_assess_replay_scope(...)` then consumes that lineage and returns replay necessity. The two concepts are adjacent, but not mixed.

Remaining limitation: the assessment always returns `replay_required=True`. That is a conservative compatibility rule, not evidence that influence lineage and replay assessment remain compressed.

### Replay justification and replay selection

No remaining counterexample found inside this family.

The code separates `_justify_replay_selection(...)` from `_select_replay_targets(...)`. Justification owns the compatible target tuple and its replay-necessity context. Selection owns the actual selected target value consumed by execution.

Remaining limitation: the selected target set is always `("event_replay", "projection_finalization")`. That is the current compatibility boundary, not an unrecovered ownership boundary.

### Projection finalization and publication

No remaining counterexample found inside this family.

The code separates `StateProjector.finalize(...)` from `_publish_finalized_projection(...)`. Finalization rebuilds derived indexes. Publication wraps the finalized state and returns it as visible state without mutation.

Remaining limitation: publication is identity-preserving and implementation-local. That is intentional behavior preservation, not evidence of finalization/publication compression.

## Remaining compressed boundaries

### Within this family

No recurring compressed owner remains that is clearly local to Projection Influence Lineage.

The remaining implementation constraints are conservative behavior boundaries rather than additional ownership slices:

- replay scope assessment is always replay-required;
- replay target compatibility remains full event replay plus full projection finalization;
- execution validates only that full replay/finalization target tuple;
- finalization still rebuilds all derived projection indexes;
- publication is an identity-preserving handoff.

These facts do not justify another ownership-recovery slice inside this family without new implementation evidence.

### Adjacent, not inside this family

The following pressure remains real, but belongs outside the completed Projection Influence Lineage family:

- projection builder dependency knowledge is still implicit in `finalize(...)` order and shared State reads/writes;
- affected projection recovery is descriptive and incomplete for dependency authority;
- cache validity is snapshot/tip based rather than affected-scope or affected-projection based;
- dependent read-model caches are keyed by projected State identity and rebuild globally on miss;
- fact-index and state-summary construction are read-model concerns, not projection lineage concerns.

These pressures are better understood as Read-Model Ownership, projection-builder dependency ownership, or behavior-changing incremental replay work. They should not be treated as a reason to keep slicing Projection Influence Lineage.

## Relationship to replay execution

Replay execution is now a consumer of selected replay work, not the owner of influence evidence, assessment, justification, or selection.

`_execute_replay_selection(...)` proves this by accepting a `_ReplayExecutionRequest`, validating the selected target tuple, running `replay_events()`, and returning `finalize()`. It does not inspect affected scopes, affected projections, lineage, cache state, or read-model dependency information.

Therefore replay execution is correctly positioned after selection and before projection finalization in this family.

## Relationship to projection publication

Projection publication is the terminal handoff of finalized projection state. It is not finalization itself and not read-model construction.

`_publish_finalized_projection(...)` returns `_ProjectionPublication(visible_state=request.finalized_state)`. That evidence supports the name `Projection Publication`: the implementation publishes a finalized `State` object unchanged. It does not construct a separate read model, render output, persist a cache entry, or alter consumer semantics.

Therefore projection publication closes the Projection Influence Lineage family at the projection-state handoff boundary.

## Relationship to Read-Model Ownership

Read-Model Ownership is the strongest next-family candidate.

Implementation evidence from existing investigations distinguishes projection from dependent read models:

- `StateProjector.finalize(...)` produces projected `State` and derived projection indexes.
- Dependent read models such as state summary and fact index consume already-projected State.
- Their caches depend on State projection version and `state_last_event_id`, so a projected State boundary change invalidates them coarsely.
- On dependent read-model misses, the read model is rebuilt globally rather than partially refreshed by affected subject, predicate, relationship, or section.

This pressure does not belong to Projection Influence Lineage because the completed lineage chain stops at publishing finalized projected State. Read-model construction, cache reuse, dependency keys, and partial refresh are downstream concerns.

## Supported conclusions

The audit supports these conclusions:

1. Projection Influence Lineage is complete as an implementation responsibility family for the current conservative replay/projection behavior.
2. The implementation exposes the chain from lineage recovery through publication with distinct local owners.
3. No additional recurring compressed owner remains inside this family based on current evidence.
4. Replay execution is separated from selection and remains behavior-preserving full replay plus full finalization.
5. Projection publication is separated from finalization and remains identity-preserving.
6. Remaining pressure around dependent summaries, fact indexes, and cache dependencies belongs naturally to Read-Model Ownership rather than to Projection Influence Lineage.
7. Implementation should now stop slicing Projection Influence Lineage until new implementation evidence demonstrates another recurring compressed owner.

## Unsupported conclusions

The audit does not support these conclusions:

1. Seed has selective replay.
2. Seed has dirty-scope projection invalidation.
3. Affected projection recovery is complete dependency tracking.
4. Empty affected projection recovery proves no derived projection is affected.
5. Projection finalization can safely skip individual builders.
6. Projection cache invalidation understands affected scopes or projection dependencies.
7. Projection publication constructs a separate read model.
8. Read-model partial refresh is implemented.
9. Beginning Read-Model Ownership implies immediate read-model redesign or optimization.

## Recommended next responsibility family

Begin Read-Model Ownership as the next responsibility family.

## Reason for recommendation

The completed family now reaches the terminal projection-state publication boundary. The strongest remaining implementation pressure is downstream of that boundary: consumers and caches that derive read models from projected State.

Read-Model Ownership is recommended because current evidence shows recurring downstream compression around:

- dependent read-model cache identity;
- global rebuild on read-model cache miss;
- fact-index and state-summary construction from projected State;
- coarse invalidation by State projection version and last event id;
- lack of partial refresh authority for read-model fragments.

That pressure is not solved by another Projection Influence Lineage slice. It requires investigating read-model construction and dependency ownership on their own implementation evidence.

## Confidence

High.

Confidence is high because the current code exposes each responsibility in the requested chain with named implementation-local owners and an ordered call sequence in `StateProjector.project_from_state(...)`. The remaining limitations are repeatedly described by the implementation as conservative compatibility behavior or downstream read-model/cache behavior, not as hidden projection-lineage ownership.

