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
