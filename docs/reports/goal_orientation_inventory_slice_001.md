# Goal Orientation Inventory Slice 001

This slice adds one read-only `GoalOrientationInventory` implementation.

## Boundary

The inventory renders the supported orthogonal goal dimensions recovered by repository evidence:

- `operator_interaction`
- `operational_continuity`
- `resource_stewardship`
- `capability_recovery`
- `knowledge_quality`
- `implementation_maintenance`

A dimension remains visible with state `Null` when no explicit pressure, bounded goal, inquiry reference, or other material is associated with it.

## Association rule

Inventory membership is accepted only from explicit `GoalOrientationAssociation.dimension_refs` evidence. Artifact labels and wording are preserved as display material but are not used to infer dimension membership.

The inventory preserves:

- zero or more pressures per dimension;
- zero or more bounded goals per dimension;
- zero or more inquiry references per dimension;
- one artifact explicitly associated with several dimensions;
- unknown association material;
- unmatched dimension references;
- conflicting material;
- duplicate artifact references with separate source identity.

## Refusals

`GoalOrientationInventory` is not a registry, planner, queue, priority order, scheduler, authorization mechanism, execution mechanism, inquiry mover, recorder, event-ledger writer, or cluster mutator.

Visible pressure does not activate a goal. A bounded goal does not provide inquiry authority, execution authority, recording authority, or mutation authority.
