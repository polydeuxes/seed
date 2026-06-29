"""Derived fact indexes for read-only State views.

The fact index is a cacheable derived read model. It is not event authority,
projection authority, fact mutation, observation creation, or a view cache.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from seed_runtime.execution_status import (
    ExecutionStatusConsumer,
    ProgressCadence,
    emit_progress_if_due,
    emit_status,
)
from seed_runtime.facts import Fact, is_fact_expired
from seed_runtime.read_model_ownership import (
    read_model_construction_inputs,
    read_model_cache_lookup_request,
    read_model_dependency_identity,
    resolve_read_model_cache_lookup,
)
from seed_runtime.projection_store import (
    FACT_INDEX_NAME,
    FACT_INDEX_VERSION,
    STATE_PROJECTION_VERSION,
    DerivedIndexSnapshot,
    ProjectionStore,
)
from seed_runtime.state import State, _fact_value_key


@dataclass(frozen=True)
class DerivedFactIndex:
    """Reusable facts-by-subject/predicate index derived from projected State."""

    workspace_id: str
    index_name: str
    index_version: str
    state_projection_version: str
    state_last_event_id: str | None
    created_at: datetime
    fact_ids_by_subject_predicate: dict[str, dict[str, list[str]]] = field(
        default_factory=dict
    )

    def current_facts(
        self, state: State, subject: str, predicate: str, *, include_expired: bool = False
    ) -> list[Fact]:
        """Return indexed facts for an exact subject/predicate lookup."""

        fact_ids = self.fact_ids_by_subject_predicate.get(subject, {}).get(predicate, [])
        facts = [
            state.facts[fact_id]
            for fact_id in fact_ids
            if fact_id in state.facts
            and (include_expired or not is_fact_expired(state.facts[fact_id]))
        ]
        return sorted(facts, key=lambda fact: _fact_value_key(fact.value))


def build_fact_index(
    state: State,
    *,
    workspace_id: str,
    state_projection_version: str = STATE_PROJECTION_VERSION,
    index_name: str = FACT_INDEX_NAME,
    index_version: str = FACT_INDEX_VERSION,
    status_consumer: ExecutionStatusConsumer | None = None,
) -> DerivedFactIndex:
    """Build the smallest reusable fact index from an already-projected State."""

    inputs = read_model_construction_inputs(state)
    visible_state = inputs.visible_state
    by_subject_predicate: dict[str, dict[str, list[str]]] = {}
    subjects = sorted({support.subject for support in visible_state.fact_supports})
    total = len(subjects)
    cadence = ProgressCadence()
    for index, subject in enumerate(subjects, start=1):
        predicates = sorted(
            {
                support.predicate
                for support in visible_state.fact_supports
                if support.subject == subject
            }
        )
        for predicate in predicates:
            facts = visible_state.get_current_facts(
                subject, predicate, resolve_aliases=False
            )
            if facts:
                by_subject_predicate.setdefault(subject, {})[predicate] = [
                    fact.id for fact in facts
                ]
        emit_progress_if_due(
            status_consumer,
            cadence,
            "fact_index_build",
            "Building fact index",
            current=index,
            total=total,
        )
    identity = read_model_dependency_identity(
        inputs, state_projection_version=state_projection_version
    )
    return DerivedFactIndex(
        workspace_id=workspace_id,
        index_name=index_name,
        index_version=index_version,
        state_projection_version=identity.state_projection_version,
        state_last_event_id=identity.state_last_event_id,
        created_at=_utc_now(),
        fact_ids_by_subject_predicate=by_subject_predicate,
    )


def load_or_build_fact_index(
    state: State,
    *,
    workspace_id: str,
    store: ProjectionStore | None,
    state_projection_version: str = STATE_PROJECTION_VERSION,
    status_consumer: ExecutionStatusConsumer | None = None,
) -> DerivedFactIndex:
    """Load a valid fact index cache or build and save one from projected State."""

    inputs = read_model_construction_inputs(state)

    identity = read_model_dependency_identity(
        inputs, state_projection_version=state_projection_version
    )

    if store is not None:
        emit_status(status_consumer, "fact_index_cache_load", "Loading fact index cache...")
        lookup = resolve_read_model_cache_lookup(
            read_model_cache_lookup_request(identity),
            lambda lookup_identity: store.load_derived_index_snapshot(
                workspace_id,
                FACT_INDEX_NAME,
                FACT_INDEX_VERSION,
                state_projection_version=lookup_identity.state_projection_version,
                state_last_event_id=lookup_identity.state_last_event_id,
            ),
        )
        if lookup.cache_hit:
            emit_status(
                status_consumer,
                "fact_index_cache_load",
                "Fact index cache: hit",
                completed=True,
            )
            snapshot = lookup.snapshot
            assert snapshot is not None
            return fact_index_from_payload(snapshot.index_payload, snapshot=snapshot)
        emit_status(
            status_consumer,
            "fact_index_cache_load",
            "Fact index cache: miss",
            completed=True,
        )
    emit_status(status_consumer, "fact_index_build", "Building fact index...")
    index = build_fact_index(
        state,
        workspace_id=workspace_id,
        state_projection_version=state_projection_version,
        status_consumer=status_consumer,
    )
    emit_status(status_consumer, "fact_index_build", "Building fact index...", completed=True)
    if store is not None:
        emit_status(status_consumer, "fact_index_cache_save", "Saving fact index cache...")
        store.save_derived_index_snapshot(
            DerivedIndexSnapshot(
                workspace_id=workspace_id,
                index_name=index.index_name,
                index_version=index.index_version,
                state_projection_version=index.state_projection_version,
                state_last_event_id=index.state_last_event_id,
                index_payload=fact_index_to_payload(index),
                created_at=index.created_at,
            )
        )
    return index


def fact_index_to_payload(index: DerivedFactIndex) -> dict[str, Any]:
    return {
        "fact_ids_by_subject_predicate": index.fact_ids_by_subject_predicate,
    }


def fact_index_from_payload(
    payload: dict[str, Any], *, snapshot: DerivedIndexSnapshot
) -> DerivedFactIndex:
    return DerivedFactIndex(
        workspace_id=snapshot.workspace_id,
        index_name=snapshot.index_name,
        index_version=snapshot.index_version,
        state_projection_version=snapshot.state_projection_version,
        state_last_event_id=snapshot.state_last_event_id,
        created_at=snapshot.created_at,
        fact_ids_by_subject_predicate={
            str(subject): {
                str(predicate): [str(fact_id) for fact_id in fact_ids]
                for predicate, fact_ids in predicates.items()
            }
            for subject, predicates in payload.get("fact_ids_by_subject_predicate", {}).items()
        },
    )


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)
