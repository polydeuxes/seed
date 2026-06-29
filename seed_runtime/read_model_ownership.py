"""Implementation-local read-model construction ownership boundaries.

Read models consume already-published projected State. This module preserves that
handoff as a local construction input boundary; it does not publish projections,
replay events, invalidate caches, render output, persist snapshots, or change
read-model semantics.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

from seed_runtime.state import State

TReadModelSnapshot = TypeVar("TReadModelSnapshot")
TReadModel = TypeVar("TReadModel")


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
class ReadModelCacheLookupRequest:
    """Request to resolve a read-model cache entry for a dependency identity.

    The boundary owns only the existing lookup question: whether a dependent
    read-model cache has an entry satisfying the already-derived dependency
    identity. It does not derive identity, own cache storage, invalidate caches,
    construct read models, publish projections, render output, or change lookup
    semantics.
    """

    dependency_identity: ReadModelDependencyIdentity


@dataclass(frozen=True)
class ReadModelCacheLookupResult(Generic[TReadModelSnapshot]):
    """Result of resolving an existing read-model cache lookup request."""

    request: ReadModelCacheLookupRequest
    snapshot: TReadModelSnapshot | None

    @property
    def cache_hit(self) -> bool:
        return self.snapshot is not None


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


@dataclass(frozen=True)
class ReadModelConstructionRequest(Generic[TReadModelSnapshot]):
    """Request to construct a read model after cache lookup did not reuse one.

    The boundary owns only the handoff into existing construction. It consumes
    the already-visible State inputs, the already-derived dependency identity,
    and the already-resolved cache lookup result. It does not perform cache
    lookup, own cache storage, save snapshots, invalidate caches, publish
    projections, render output, schedule work, or alter read-model contents.
    """

    inputs: ReadModelConstructionInputs
    dependency_identity: ReadModelDependencyIdentity
    cache_lookup: ReadModelCacheLookupResult[TReadModelSnapshot] | None = None


@dataclass(frozen=True)
class ReadModelConstructionResult(Generic[TReadModel]):
    """Constructed read model returned by the existing read-model builder."""

    request: ReadModelConstructionRequest[object]
    read_model: TReadModel


def read_model_construction_inputs(state: State) -> ReadModelConstructionInputs:
    """Return read-model construction inputs for an already-published State."""

    return ReadModelConstructionInputs(visible_state=state)


def read_model_construction_request(
    inputs: ReadModelConstructionInputs,
    dependency_identity: ReadModelDependencyIdentity,
    *,
    cache_lookup: ReadModelCacheLookupResult[TReadModelSnapshot] | None = None,
) -> ReadModelConstructionRequest[TReadModelSnapshot]:
    """Return a construction request from existing read-model handoff evidence."""

    return ReadModelConstructionRequest(
        inputs=inputs,
        dependency_identity=dependency_identity,
        cache_lookup=cache_lookup,
    )


def construct_read_model(
    request: ReadModelConstructionRequest[TReadModelSnapshot],
    build_read_model: Callable[[ReadModelConstructionInputs], TReadModel],
) -> ReadModelConstructionResult[TReadModel]:
    """Construct a read model by invoking the existing builder unchanged."""

    return ReadModelConstructionResult(
        request=request,
        read_model=build_read_model(request.inputs),
    )


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


def read_model_cache_lookup_request(
    dependency_identity: ReadModelDependencyIdentity,
) -> ReadModelCacheLookupRequest:
    """Return the cache lookup request for an already-derived dependency identity."""

    return ReadModelCacheLookupRequest(dependency_identity=dependency_identity)


def resolve_read_model_cache_lookup(
    request: ReadModelCacheLookupRequest,
    load_snapshot: Callable[[ReadModelDependencyIdentity], TReadModelSnapshot | None],
) -> ReadModelCacheLookupResult[TReadModelSnapshot]:
    """Resolve a read-model cache lookup using the existing storage operation."""

    return ReadModelCacheLookupResult(
        request=request,
        snapshot=load_snapshot(request.dependency_identity),
    )
