"""Implementation-local read-model construction ownership boundaries.

Read models consume already-published projected State. This module preserves that
handoff as a local construction input boundary; it does not publish projections,
replay events, invalidate caches, render output, persist snapshots, or change
read-model semantics.
"""

from __future__ import annotations

from dataclasses import dataclass

from seed_runtime.state import State


@dataclass(frozen=True)
class ReadModelDependencyIdentity:
    """Dependency identity proving a read model is valid for projected State.

    The boundary preserves only the already-existing identity evidence used by
    dependent read-model caches. It does not own cache invalidation, cache
    storage, lookup policy, read-model construction, projection publication,
    rendering, CLI, JSON, events, or ledger behavior.
    """

    state_projection_version: str
    state_last_event_id: str | None


@dataclass(frozen=True)
class ReadModelConstructionInputs:
    """Inputs handed from visible projected State into read-model builders.

    The boundary is identity-preserving: builders receive the same State object
    they previously accepted directly. The wrapper makes the post-publication
    handoff explicit without owning projection replay, projection finalization,
    projection publication, cache invalidation, rendering, scheduling, or
    persistence.
    """

    visible_state: State


def read_model_construction_inputs(state: State) -> ReadModelConstructionInputs:
    """Return read-model construction inputs for an already-published State."""

    return ReadModelConstructionInputs(visible_state=state)


def read_model_dependency_identity(
    inputs: ReadModelConstructionInputs, *, state_projection_version: str
) -> ReadModelDependencyIdentity:
    """Return the dependency identity for a read model built from inputs."""

    return ReadModelDependencyIdentity(
        state_projection_version=state_projection_version,
        state_last_event_id=inputs.visible_state.last_event_id,
    )


def read_model_dependency_identity_for_state_boundary(
    *, state_projection_version: str, state_last_event_id: str | None
) -> ReadModelDependencyIdentity:
    """Return dependency identity from an already-known projected State boundary."""

    return ReadModelDependencyIdentity(
        state_projection_version=state_projection_version,
        state_last_event_id=state_last_event_id,
    )
