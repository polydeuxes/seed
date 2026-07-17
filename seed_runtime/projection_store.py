"""Projection snapshot stores for cached Seed state projections.

Event ledgers own append-only historical events. Projection stores own reusable
snapshots of projected state derived from those events.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import sqlite3
from typing import Any, Protocol

from seed_runtime.events import EventLedger
from seed_runtime.execution_status import (
    ExecutionStatusConsumer,
    ProgressCadence,
    emit_progress_if_due,
    emit_status,
)
from seed_runtime.evidence import Evidence
from seed_runtime.facts import Fact, FactConflict, FactSupport
from seed_runtime.models import (
    ActionPlan,
    Approval,
    Entity,
    ExecutionAuthorization,
    Goal,
    HandoffPlan,
    PendingAction,
    ToolNeed,
    ToolSpec,
)
from seed_runtime.observations import Observation
from seed_runtime.predicate_catalog import PredicateCatalog
from seed_runtime.serialization import to_plain
from seed_runtime.state import (
    AliasResolver,
    EntityAlias,
    EntityRelationship,
    EntityTypeAssertion,
    GraphValidationIssue,
    LegacyEntityRelationship,
    State,
    StateProjector,
    ProjectionBuildDiagnostics,
)

STATE_PROJECTION_NAME = "state"
STATE_PROJECTION_VERSION = "state-v2"
STATE_SUMMARY_PROJECTION_NAME = "state-summary"
STATE_SUMMARY_PROJECTION_VERSION = "state-summary-v1"
FACT_INDEX_NAME = "fact-index-by-subject-predicate"
FACT_INDEX_VERSION = "fact-index-by-subject-predicate-v1"


@dataclass(frozen=True)
class DerivedIndexSnapshot:
    workspace_id: str
    index_name: str
    index_version: str
    state_projection_version: str
    state_last_event_id: str | None
    index_payload: dict[str, Any]
    created_at: datetime


@dataclass(frozen=True)
class SummarySnapshotBoundary:
    artifact_standing: str = "derived_summary_snapshot"
    source_artifact_standing: str = "derived_projection_snapshot"
    source_producer_boundary: str = "python_state_projection"
    source_occurrence_evidence_kind: str = "snapshot_preservation_only"
    source_consumer_limit: str = "read_model_cache_only"
    consumer_limit: str = "operator_summary_cache_only"
    mutates_cluster: bool = False


@dataclass(frozen=True)
class SummaryProjectionSnapshot:
    workspace_id: str
    projection_name: str
    projection_version: str
    last_event_id: str | None
    state_projection_version: str
    state_last_event_id: str | None
    summary_payload: dict[str, Any]
    created_at: datetime
    boundary: SummarySnapshotBoundary = SummarySnapshotBoundary()


@dataclass(frozen=True)
class ProjectionSnapshotBoundary:
    artifact_standing: str = "derived_projection_snapshot"
    producer_boundary: str = "python_state_projection"
    occurrence_evidence_kind: str = "snapshot_preservation_only"
    consumer_limit: str = "read_model_cache_only"
    mutates_cluster: bool = False


@dataclass(frozen=True)
class ProjectionSnapshot:
    workspace_id: str
    projection_name: str
    projection_version: str
    last_event_id: str | None
    last_event_created_at: datetime | None
    state_payload: dict[str, Any]
    created_at: datetime
    boundary: ProjectionSnapshotBoundary = ProjectionSnapshotBoundary()


class ProjectionStore(Protocol):
    """Backend-independent store for projected-state snapshots."""

    __seed_arch__ = {
        "owner": "projection_cache",
        "layer": "state",
        "summary": "Stores reusable projected-state snapshots derived from the event ledger.",
        "edges": [
            {"to": "StateProjector", "label": "used when snapshot is stale"},
            {"to": "State", "label": "loads/saves projected snapshot"},
        ],
    }

    def load_snapshot(
        self, workspace_id: str, projection_name: str, projection_version: str
    ) -> ProjectionSnapshot | None:
        """Return a matching snapshot, if one exists for the exact version."""

    def save_snapshot(self, snapshot: ProjectionSnapshot) -> None:
        """Persist or replace a projection snapshot."""

    def clear_snapshot(
        self, workspace_id: str, projection_name: str | None = None
    ) -> None:
        """Remove snapshots for a workspace, optionally scoped to one projection."""

    def load_summary_snapshot(
        self,
        workspace_id: str,
        projection_name: str,
        projection_version: str,
        *,
        state_projection_version: str,
        state_last_event_id: str | None,
    ) -> SummaryProjectionSnapshot | None:
        """Return a summary read-model snapshot derived from a valid State snapshot."""

    def save_summary_snapshot(self, snapshot: SummaryProjectionSnapshot) -> None:
        """Persist or replace a dependent summary read-model snapshot."""

    def load_derived_index_snapshot(
        self,
        workspace_id: str,
        index_name: str,
        index_version: str,
        *,
        state_projection_version: str,
        state_last_event_id: str | None,
    ) -> DerivedIndexSnapshot | None:
        """Return a derived index snapshot for a matching State projection."""

    def save_derived_index_snapshot(self, snapshot: DerivedIndexSnapshot) -> None:
        """Persist or replace a derived index snapshot."""


class InMemoryProjectionStore:
    """Process-local ProjectionStore useful for tests and non-SQLite callers."""

    def __init__(self) -> None:
        self._snapshots: dict[tuple[str, str], ProjectionSnapshot] = {}
        self._summary_snapshots: dict[tuple[str, str], SummaryProjectionSnapshot] = {}
        self._derived_index_snapshots: dict[tuple[str, str], DerivedIndexSnapshot] = {}

    def load_snapshot(
        self, workspace_id: str, projection_name: str, projection_version: str
    ) -> ProjectionSnapshot | None:
        snapshot = self._snapshots.get((workspace_id, projection_name))
        if snapshot is None or snapshot.projection_version != projection_version:
            return None
        return snapshot

    def save_snapshot(self, snapshot: ProjectionSnapshot) -> None:
        self._snapshots[(snapshot.workspace_id, snapshot.projection_name)] = snapshot

    def clear_snapshot(
        self, workspace_id: str, projection_name: str | None = None
    ) -> None:
        if projection_name is not None:
            self._snapshots.pop((workspace_id, projection_name), None)
            for key in list(self._summary_snapshots):
                if key[0] == workspace_id:
                    self._summary_snapshots.pop(key, None)
            for key in list(self._derived_index_snapshots):
                if key[0] == workspace_id:
                    self._derived_index_snapshots.pop(key, None)
            return
        for key in list(self._snapshots):
            if key[0] == workspace_id:
                self._snapshots.pop(key, None)
        for key in list(self._summary_snapshots):
            if key[0] == workspace_id:
                self._summary_snapshots.pop(key, None)
        for key in list(self._derived_index_snapshots):
            if key[0] == workspace_id:
                self._derived_index_snapshots.pop(key, None)

    def load_summary_snapshot(
        self,
        workspace_id: str,
        projection_name: str,
        projection_version: str,
        *,
        state_projection_version: str,
        state_last_event_id: str | None,
    ) -> SummaryProjectionSnapshot | None:
        snapshot = self._summary_snapshots.get((workspace_id, projection_name))
        if snapshot is None or snapshot.projection_version != projection_version:
            return None
        if snapshot.state_projection_version != state_projection_version:
            return None
        if snapshot.state_last_event_id != state_last_event_id:
            return None
        if not summary_snapshot_is_eligible_for_operator_cache(snapshot):
            return None
        return snapshot

    def save_summary_snapshot(self, snapshot: SummaryProjectionSnapshot) -> None:
        self._summary_snapshots[(snapshot.workspace_id, snapshot.projection_name)] = (
            snapshot
        )

    def load_derived_index_snapshot(
        self,
        workspace_id: str,
        index_name: str,
        index_version: str,
        *,
        state_projection_version: str,
        state_last_event_id: str | None,
    ) -> DerivedIndexSnapshot | None:
        snapshot = self._derived_index_snapshots.get((workspace_id, index_name))
        if snapshot is None or snapshot.index_version != index_version:
            return None
        if snapshot.state_projection_version != state_projection_version:
            return None
        if snapshot.state_last_event_id != state_last_event_id:
            return None
        return snapshot

    def save_derived_index_snapshot(self, snapshot: DerivedIndexSnapshot) -> None:
        self._derived_index_snapshots[(snapshot.workspace_id, snapshot.index_name)] = (
            snapshot
        )


class SQLiteProjectionStore:
    """SQLite-backed ProjectionStore for local CLI state projection caching."""

    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self._connection = sqlite3.connect(database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS projection_snapshots (
                workspace_id TEXT NOT NULL,
                projection_name TEXT NOT NULL,
                projection_version TEXT NOT NULL,
                last_event_id TEXT,
                last_event_created_at TEXT,
                state_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                artifact_standing TEXT NOT NULL DEFAULT 'derived_projection_snapshot',
                producer_boundary TEXT NOT NULL DEFAULT 'python_state_projection',
                occurrence_evidence_kind TEXT NOT NULL DEFAULT 'snapshot_preservation_only',
                consumer_limit TEXT NOT NULL DEFAULT 'read_model_cache_only',
                mutates_cluster INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (workspace_id, projection_name)
            )
            """)
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS derived_index_snapshots (
                workspace_id TEXT NOT NULL,
                index_name TEXT NOT NULL,
                index_version TEXT NOT NULL,
                state_projection_version TEXT NOT NULL,
                state_last_event_id TEXT,
                index_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (workspace_id, index_name)
            )
            """)
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS state_summary_snapshots (
                workspace_id TEXT NOT NULL,
                projection_name TEXT NOT NULL,
                projection_version TEXT NOT NULL,
                last_event_id TEXT,
                state_projection_version TEXT NOT NULL,
                state_last_event_id TEXT,
                summary_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                artifact_standing TEXT NOT NULL DEFAULT 'derived_summary_snapshot',
                source_artifact_standing TEXT NOT NULL DEFAULT 'derived_projection_snapshot',
                source_producer_boundary TEXT NOT NULL DEFAULT 'python_state_projection',
                source_occurrence_evidence_kind TEXT NOT NULL DEFAULT 'snapshot_preservation_only',
                source_consumer_limit TEXT NOT NULL DEFAULT 'read_model_cache_only',
                consumer_limit TEXT NOT NULL DEFAULT 'operator_summary_cache_only',
                mutates_cluster INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (workspace_id, projection_name)
            )
            """)
        self._ensure_projection_snapshot_boundary_columns()
        self._ensure_state_summary_boundary_columns()
        self._connection.commit()

    def _ensure_projection_snapshot_boundary_columns(self) -> None:
        columns = {
            row[1]
            for row in self._connection.execute(
                "PRAGMA table_info(projection_snapshots)"
            )
        }
        additions = {
            "artifact_standing": "TEXT NOT NULL DEFAULT 'derived_projection_snapshot'",
            "producer_boundary": "TEXT NOT NULL DEFAULT 'python_state_projection'",
            "occurrence_evidence_kind": "TEXT NOT NULL DEFAULT 'snapshot_preservation_only'",
            "consumer_limit": "TEXT NOT NULL DEFAULT 'read_model_cache_only'",
            "mutates_cluster": "INTEGER NOT NULL DEFAULT 0",
        }
        for name, declaration in additions.items():
            if name not in columns:
                self._connection.execute(
                    f"ALTER TABLE projection_snapshots ADD COLUMN {name} {declaration}"
                )

    def _ensure_state_summary_boundary_columns(self) -> None:
        columns = {
            row[1]
            for row in self._connection.execute(
                "PRAGMA table_info(state_summary_snapshots)"
            )
        }
        additions = {
            "artifact_standing": "TEXT NOT NULL DEFAULT 'derived_summary_snapshot'",
            "source_artifact_standing": "TEXT NOT NULL DEFAULT 'derived_projection_snapshot'",
            "source_producer_boundary": "TEXT NOT NULL DEFAULT 'python_state_projection'",
            "source_occurrence_evidence_kind": "TEXT NOT NULL DEFAULT 'snapshot_preservation_only'",
            "source_consumer_limit": "TEXT NOT NULL DEFAULT 'read_model_cache_only'",
            "consumer_limit": "TEXT NOT NULL DEFAULT 'operator_summary_cache_only'",
            "mutates_cluster": "INTEGER NOT NULL DEFAULT 0",
        }
        for name, declaration in additions.items():
            if name not in columns:
                self._connection.execute(
                    f"ALTER TABLE state_summary_snapshots ADD COLUMN {name} {declaration}"
                )

    def load_snapshot(
        self, workspace_id: str, projection_name: str, projection_version: str
    ) -> ProjectionSnapshot | None:
        row = self._connection.execute(
            """
            SELECT * FROM projection_snapshots
            WHERE workspace_id = ? AND projection_name = ? AND projection_version = ?
            """,
            (workspace_id, projection_name, projection_version),
        ).fetchone()
        if row is None:
            return None
        return ProjectionSnapshot(
            workspace_id=row["workspace_id"],
            projection_name=row["projection_name"],
            projection_version=row["projection_version"],
            last_event_id=row["last_event_id"],
            last_event_created_at=_parse_datetime(row["last_event_created_at"]),
            state_payload=json.loads(row["state_json"]),
            created_at=_parse_datetime(row["created_at"]) or _utc_now(),
            boundary=ProjectionSnapshotBoundary(
                artifact_standing=row["artifact_standing"],
                producer_boundary=row["producer_boundary"],
                occurrence_evidence_kind=row["occurrence_evidence_kind"],
                consumer_limit=row["consumer_limit"],
                mutates_cluster=bool(row["mutates_cluster"]),
            ),
        )

    def save_snapshot(self, snapshot: ProjectionSnapshot) -> None:
        self._connection.execute(
            """
            INSERT INTO projection_snapshots (
                workspace_id, projection_name, projection_version, last_event_id,
                last_event_created_at, state_json, created_at, artifact_standing,
                producer_boundary, occurrence_evidence_kind, consumer_limit, mutates_cluster
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(workspace_id, projection_name) DO UPDATE SET
                projection_version = excluded.projection_version,
                last_event_id = excluded.last_event_id,
                last_event_created_at = excluded.last_event_created_at,
                state_json = excluded.state_json,
                created_at = excluded.created_at,
                artifact_standing = excluded.artifact_standing,
                producer_boundary = excluded.producer_boundary,
                occurrence_evidence_kind = excluded.occurrence_evidence_kind,
                consumer_limit = excluded.consumer_limit,
                mutates_cluster = excluded.mutates_cluster
            """,
            (
                snapshot.workspace_id,
                snapshot.projection_name,
                snapshot.projection_version,
                snapshot.last_event_id,
                _format_datetime(snapshot.last_event_created_at),
                json.dumps(snapshot.state_payload, sort_keys=True),
                _format_datetime(snapshot.created_at),
                snapshot.boundary.artifact_standing,
                snapshot.boundary.producer_boundary,
                snapshot.boundary.occurrence_evidence_kind,
                snapshot.boundary.consumer_limit,
                int(snapshot.boundary.mutates_cluster),
            ),
        )
        self._connection.commit()

    def clear_snapshot(
        self, workspace_id: str, projection_name: str | None = None
    ) -> None:
        if projection_name is None:
            self._connection.execute(
                "DELETE FROM projection_snapshots WHERE workspace_id = ?",
                (workspace_id,),
            )
        else:
            self._connection.execute(
                """
                DELETE FROM projection_snapshots
                WHERE workspace_id = ? AND projection_name = ?
                """,
                (workspace_id, projection_name),
            )
        self._connection.execute(
            "DELETE FROM state_summary_snapshots WHERE workspace_id = ?",
            (workspace_id,),
        )
        self._connection.execute(
            "DELETE FROM derived_index_snapshots WHERE workspace_id = ?",
            (workspace_id,),
        )
        self._connection.commit()

    def load_summary_snapshot(
        self,
        workspace_id: str,
        projection_name: str,
        projection_version: str,
        *,
        state_projection_version: str,
        state_last_event_id: str | None,
    ) -> SummaryProjectionSnapshot | None:
        row = self._connection.execute(
            """
            SELECT summary.* FROM state_summary_snapshots AS summary
            JOIN projection_snapshots AS state
              ON state.workspace_id = summary.workspace_id
             AND state.projection_name = ?
            WHERE summary.workspace_id = ?
              AND summary.projection_name = ?
              AND summary.projection_version = ?
              AND summary.state_projection_version = ?
              AND summary.state_last_event_id IS ?
              AND state.projection_version = summary.state_projection_version
              AND state.last_event_id IS summary.state_last_event_id
              AND state.artifact_standing = 'derived_projection_snapshot'
              AND state.producer_boundary = 'python_state_projection'
              AND state.occurrence_evidence_kind = 'snapshot_preservation_only'
              AND state.consumer_limit = 'read_model_cache_only'
              AND state.mutates_cluster = 0
              AND summary.artifact_standing = 'derived_summary_snapshot'
              AND summary.source_artifact_standing = state.artifact_standing
              AND summary.source_producer_boundary = state.producer_boundary
              AND summary.source_occurrence_evidence_kind = state.occurrence_evidence_kind
              AND summary.source_consumer_limit = state.consumer_limit
              AND summary.consumer_limit = 'operator_summary_cache_only'
              AND summary.mutates_cluster = 0
            """,
            (
                STATE_PROJECTION_NAME,
                workspace_id,
                projection_name,
                projection_version,
                state_projection_version,
                state_last_event_id,
            ),
        ).fetchone()
        if row is None:
            return None
        return SummaryProjectionSnapshot(
            workspace_id=row["workspace_id"],
            projection_name=row["projection_name"],
            projection_version=row["projection_version"],
            last_event_id=row["last_event_id"],
            state_projection_version=row["state_projection_version"],
            state_last_event_id=row["state_last_event_id"],
            summary_payload=json.loads(row["summary_json"]),
            created_at=_parse_datetime(row["created_at"]) or _utc_now(),
            boundary=SummarySnapshotBoundary(
                artifact_standing=row["artifact_standing"],
                source_artifact_standing=row["source_artifact_standing"],
                source_producer_boundary=row["source_producer_boundary"],
                source_occurrence_evidence_kind=row["source_occurrence_evidence_kind"],
                source_consumer_limit=row["source_consumer_limit"],
                consumer_limit=row["consumer_limit"],
                mutates_cluster=bool(row["mutates_cluster"]),
            ),
        )

    def save_summary_snapshot(self, snapshot: SummaryProjectionSnapshot) -> None:
        self._connection.execute(
            """
            INSERT INTO state_summary_snapshots (
                workspace_id, projection_name, projection_version, last_event_id,
                state_projection_version, state_last_event_id, summary_json, created_at,
                artifact_standing, source_artifact_standing, source_producer_boundary,
                source_occurrence_evidence_kind, source_consumer_limit, consumer_limit,
                mutates_cluster
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(workspace_id, projection_name) DO UPDATE SET
                projection_version = excluded.projection_version,
                last_event_id = excluded.last_event_id,
                state_projection_version = excluded.state_projection_version,
                state_last_event_id = excluded.state_last_event_id,
                summary_json = excluded.summary_json,
                created_at = excluded.created_at,
                artifact_standing = excluded.artifact_standing,
                source_artifact_standing = excluded.source_artifact_standing,
                source_producer_boundary = excluded.source_producer_boundary,
                source_occurrence_evidence_kind = excluded.source_occurrence_evidence_kind,
                source_consumer_limit = excluded.source_consumer_limit,
                consumer_limit = excluded.consumer_limit,
                mutates_cluster = excluded.mutates_cluster
            """,
            (
                snapshot.workspace_id,
                snapshot.projection_name,
                snapshot.projection_version,
                snapshot.last_event_id,
                snapshot.state_projection_version,
                snapshot.state_last_event_id,
                json.dumps(snapshot.summary_payload, sort_keys=True),
                _format_datetime(snapshot.created_at),
                snapshot.boundary.artifact_standing,
                snapshot.boundary.source_artifact_standing,
                snapshot.boundary.source_producer_boundary,
                snapshot.boundary.source_occurrence_evidence_kind,
                snapshot.boundary.source_consumer_limit,
                snapshot.boundary.consumer_limit,
                int(snapshot.boundary.mutates_cluster),
            ),
        )
        self._connection.commit()

    def load_derived_index_snapshot(
        self,
        workspace_id: str,
        index_name: str,
        index_version: str,
        *,
        state_projection_version: str,
        state_last_event_id: str | None,
    ) -> DerivedIndexSnapshot | None:
        row = self._connection.execute(
            """
            SELECT derived.* FROM derived_index_snapshots AS derived
            JOIN projection_snapshots AS state
              ON state.workspace_id = derived.workspace_id
             AND state.projection_name = ?
            WHERE derived.workspace_id = ?
              AND derived.index_name = ?
              AND derived.index_version = ?
              AND derived.state_projection_version = ?
              AND derived.state_last_event_id IS ?
              AND state.projection_version = derived.state_projection_version
              AND state.last_event_id IS derived.state_last_event_id
            """,
            (
                STATE_PROJECTION_NAME,
                workspace_id,
                index_name,
                index_version,
                state_projection_version,
                state_last_event_id,
            ),
        ).fetchone()
        if row is None:
            return None
        return DerivedIndexSnapshot(
            workspace_id=row["workspace_id"],
            index_name=row["index_name"],
            index_version=row["index_version"],
            state_projection_version=row["state_projection_version"],
            state_last_event_id=row["state_last_event_id"],
            index_payload=json.loads(row["index_json"]),
            created_at=_parse_datetime(row["created_at"]) or _utc_now(),
        )

    def save_derived_index_snapshot(self, snapshot: DerivedIndexSnapshot) -> None:
        self._connection.execute(
            """
            INSERT INTO derived_index_snapshots (
                workspace_id, index_name, index_version, state_projection_version,
                state_last_event_id, index_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(workspace_id, index_name) DO UPDATE SET
                index_version = excluded.index_version,
                state_projection_version = excluded.state_projection_version,
                state_last_event_id = excluded.state_last_event_id,
                index_json = excluded.index_json,
                created_at = excluded.created_at
            """,
            (
                snapshot.workspace_id,
                snapshot.index_name,
                snapshot.index_version,
                snapshot.state_projection_version,
                snapshot.state_last_event_id,
                json.dumps(snapshot.index_payload, sort_keys=True),
                _format_datetime(snapshot.created_at),
            ),
        )
        self._connection.commit()

    def close(self) -> None:
        self._connection.close()


@dataclass(frozen=True)
class StateCacheStatus:
    cache_hit: bool
    projection_version: str
    snapshot_last_event_id: str | None
    current_last_event_id: str | None
    incremental_replay: bool = False
    events_applied: int | None = None


def _events_with_progress(
    events: list[Any],
    *,
    status_consumer: ExecutionStatusConsumer | None,
    phase: str,
    message: str,
):
    cadence = ProgressCadence()
    total = len(events)
    for index, event in enumerate(events, start=1):
        yield event
        emit_progress_if_due(
            status_consumer,
            cadence,
            phase,
            message,
            current=index,
            total=total,
        )


def projection_snapshot_is_eligible_for_state_cache(snapshot: ProjectionSnapshot) -> bool:
    expected = ProjectionSnapshotBoundary()
    return snapshot.boundary == expected


def summary_snapshot_is_eligible_for_operator_cache(snapshot: SummaryProjectionSnapshot) -> bool:
    expected = SummarySnapshotBoundary()
    return snapshot.boundary == expected


def project_state_with_cache(
    ledger: EventLedger,
    workspace_id: str,
    store: ProjectionStore | None,
    *,
    projector: StateProjector | None = None,
    projection_name: str = STATE_PROJECTION_NAME,
    projection_version: str = STATE_PROJECTION_VERSION,
    status_consumer: ExecutionStatusConsumer | None = None,
    diagnostics: ProjectionBuildDiagnostics | None = None,
) -> tuple[State, StateCacheStatus]:
    """Return projected State, reusing a valid ProjectionStore snapshot when possible."""

    projector = projector or StateProjector(ledger)
    events = ledger.list_events(workspace_id)
    latest_event = events[-1] if events else None
    current_last_event_id = latest_event.id if latest_event is not None else None
    snapshot_last_event_id: str | None = None
    if store is not None:
        emit_status(
            status_consumer, "projection_cache_load", "Loading projection cache..."
        )
        try:
            snapshot = store.load_snapshot(
                workspace_id, projection_name, projection_version
            )
        except Exception:
            snapshot = None
        if snapshot is not None:
            snapshot_last_event_id = snapshot.last_event_id
            if not projection_snapshot_is_eligible_for_state_cache(snapshot):
                snapshot = None
            else:
                try:
                    if diagnostics is not None:
                        snapshot_state = diagnostics.timed(
                            "cached projection load/materialize",
                            lambda: state_from_payload(snapshot.state_payload),
                        )
                    else:
                        snapshot_state = state_from_payload(snapshot.state_payload)
                except Exception:
                    snapshot_state = None
            if snapshot is not None and (
                snapshot_state is not None
                and snapshot.last_event_id == current_last_event_id
            ):
                emit_status(
                    status_consumer,
                    "projection_cache_load",
                    "Projection cache: hit",
                    completed=True,
                )
                return snapshot_state, StateCacheStatus(
                    cache_hit=True,
                    projection_version=projection_version,
                    snapshot_last_event_id=snapshot.last_event_id,
                    current_last_event_id=current_last_event_id,
                    events_applied=0,
                )
            if snapshot is not None and snapshot_state is not None and not snapshot_state.inferred_facts:
                remaining_events = _events_after_snapshot(
                    events, snapshot.last_event_id
                )
                if remaining_events is not None and hasattr(
                    projector, "project_from_state"
                ):
                    emit_status(
                        status_consumer,
                        "projection_cache_load",
                        "Projection cache: miss",
                        completed=True,
                    )
                    emit_status(
                        status_consumer,
                        "incremental_projection_replay",
                        "Incremental replay",
                        current=0,
                        total=len(remaining_events),
                    )
                    replay_events = _events_with_progress(
                        remaining_events,
                        status_consumer=status_consumer,
                        phase="incremental_projection_replay",
                        message="Incremental replay",
                    )
                    if diagnostics is not None and isinstance(
                        projector, StateProjector
                    ):
                        state = projector.project_from_state(
                            snapshot_state,
                            replay_events,
                            diagnostics=diagnostics,
                        )
                    else:
                        state = projector.project_from_state(
                            snapshot_state, replay_events
                        )
                    if not remaining_events:
                        emit_status(
                            status_consumer,
                            "incremental_projection_replay",
                            "Incremental replay",
                            current=0,
                            total=0,
                            completed=True,
                        )
                    _save_state_snapshot(
                        store,
                        state,
                        workspace_id,
                        projection_name,
                        projection_version,
                        latest_event,
                        current_last_event_id,
                        status_consumer,
                    )
                    return state, StateCacheStatus(
                        cache_hit=False,
                        projection_version=projection_version,
                        snapshot_last_event_id=snapshot.last_event_id,
                        current_last_event_id=current_last_event_id,
                        incremental_replay=True,
                        events_applied=len(remaining_events),
                    )

    if store is not None:
        emit_status(
            status_consumer,
            "projection_cache_load",
            "Projection cache: miss",
            completed=True,
        )
    emit_status(
        status_consumer,
        "projection_replay",
        "Projection replay",
        current=0,
        total=len(events),
    )
    if isinstance(projector, StateProjector):
        if diagnostics is not None:
            state = diagnostics.timed(
                "full projection rebuild",
                lambda: projector.project(
                    workspace_id,
                    status_consumer=status_consumer,
                    diagnostics=diagnostics,
                ),
            )
        else:
            state = projector.project(
                workspace_id, status_consumer=status_consumer, diagnostics=diagnostics
            )
    else:
        state = projector.project(workspace_id)
        emit_status(
            status_consumer,
            "projection_replay",
            "Projection replay",
            current=len(events),
            total=len(events),
            completed=True,
        )
    if store is not None:
        _save_state_snapshot(
            store,
            state,
            workspace_id,
            projection_name,
            projection_version,
            latest_event,
            current_last_event_id,
            status_consumer,
        )
    return state, StateCacheStatus(
        cache_hit=False,
        projection_version=projection_version,
        snapshot_last_event_id=snapshot_last_event_id,
        current_last_event_id=current_last_event_id,
        events_applied=len(events),
    )


def _save_state_snapshot(
    store: ProjectionStore,
    state: State,
    workspace_id: str,
    projection_name: str,
    projection_version: str,
    latest_event: Any,
    current_last_event_id: str | None,
    status_consumer: ExecutionStatusConsumer | None = None,
) -> None:
    emit_status(
        status_consumer, "projection_cache_save", "Saving projection snapshot..."
    )
    store.save_snapshot(
        ProjectionSnapshot(
            workspace_id=workspace_id,
            projection_name=projection_name,
            projection_version=projection_version,
            last_event_id=current_last_event_id,
            last_event_created_at=(latest_event.timestamp if latest_event else None),
            state_payload=state_to_payload(state),
            created_at=_utc_now(),
        )
    )


def _events_after_snapshot(
    events: list[Any], snapshot_last_event_id: str | None
) -> list[Any] | None:
    if snapshot_last_event_id is None:
        return events
    for index, event in enumerate(events):
        if event.id == snapshot_last_event_id:
            return events[index + 1 :]
    return None


def rebuild_state_cache(
    ledger: EventLedger,
    workspace_id: str,
    store: ProjectionStore,
    *,
    projector: StateProjector | None = None,
    projection_name: str = STATE_PROJECTION_NAME,
    projection_version: str = STATE_PROJECTION_VERSION,
    status_consumer: ExecutionStatusConsumer | None = None,
    diagnostics: ProjectionBuildDiagnostics | None = None,
) -> tuple[State, StateCacheStatus]:
    """Clear and rebuild the cached state projection snapshot."""

    emit_status(
        status_consumer, "projection_cache_clear", "Clearing projection cache..."
    )
    store.clear_snapshot(workspace_id, projection_name)
    return project_state_with_cache(
        ledger,
        workspace_id,
        store,
        projector=projector,
        projection_name=projection_name,
        projection_version=projection_version,
        status_consumer=status_consumer,
        diagnostics=diagnostics,
    )


def state_to_payload(state: State) -> dict[str, Any]:
    """Serialize enough State to faithfully serve read-only projection CLI output."""

    return to_plain(
        {
            "workspace_id": state.workspace_id,
            "last_event_id": state.last_event_id,
            "projection_version": state.projection_version,
            "entities": state.entities,
            "facts": state.facts,
            "observed_facts": state.observed_facts,
            "inferred_facts": state.inferred_facts,
            "relationships": state.relationships,
            "entity_relationships": state.entity_relationships,
            "entity_aliases": state.entity_aliases,
            "entity_type_assertions": state.entity_type_assertions,
            "graph_issues": state.graph_issues,
            "fact_supports": state.fact_supports,
            "fact_conflicts": state.fact_conflicts,
            "evidence": state.evidence,
            "observations": state.observations,
            "goals": state.goals,
            "tool_needs": state.tool_needs,
            "approvals": state.approvals,
            "action_plan_approvals": state.action_plan_approvals,
            "execution_authorizations": state.execution_authorizations,
            "execution_proposals": state.execution_proposals,
            "pending_actions": state.pending_actions,
            "action_plans": state.action_plans,
            "handoff_plans": state.handoff_plans,
            "tools": state.tools,
        }
    )


def state_from_payload(payload: dict[str, Any]) -> State:
    """Deserialize a State snapshot produced by :func:`state_to_payload`."""

    state = State(
        workspace_id=str(payload["workspace_id"]),
        predicate_catalog=PredicateCatalog.load(),
        last_event_id=payload.get("last_event_id"),
        projection_version=str(payload.get("projection_version", "v1")),
    )
    state.entities = _model_dict(payload, "entities", Entity)
    state.facts = _model_dict(payload, "facts", Fact)
    state.observed_facts = _model_dict(payload, "observed_facts", Fact)
    state.inferred_facts = _model_dict(payload, "inferred_facts", Fact)
    state.relationships = _dataclass_list(payload, "relationships", EntityRelationship)
    state.entity_relationships = _dataclass_list(
        payload, "entity_relationships", LegacyEntityRelationship
    )
    state.entity_aliases = _dataclass_list(payload, "entity_aliases", EntityAlias)
    state.entity_type_assertions = _dataclass_list(
        payload, "entity_type_assertions", EntityTypeAssertion
    )
    state.graph_issues = _dataclass_list(payload, "graph_issues", GraphValidationIssue)
    state.alias_resolver = AliasResolver(state.facts.values())
    state.fact_supports = _model_list(payload, "fact_supports", FactSupport)
    state.fact_conflicts = _model_list(payload, "fact_conflicts", FactConflict)
    state.evidence = _model_dict(payload, "evidence", Evidence)
    state.observations = _model_dict(payload, "observations", Observation)
    state.goals = _model_dict(payload, "goals", Goal)
    state.tool_needs = _model_dict(payload, "tool_needs", ToolNeed)
    state.approvals = _model_dict(payload, "approvals", Approval)
    state.action_plan_approvals = dict(payload.get("action_plan_approvals", {}))
    state.execution_authorizations = _model_dict(
        payload, "execution_authorizations", ExecutionAuthorization
    )
    state.execution_proposals = dict(payload.get("execution_proposals", {}))
    state.pending_actions = _model_dict(payload, "pending_actions", PendingAction)
    state.action_plans = _model_dict(payload, "action_plans", ActionPlan)
    state.handoff_plans = _model_dict(payload, "handoff_plans", HandoffPlan)
    state.tools = _model_dict(payload, "tools", ToolSpec)
    return state


def _latest_event(ledger: EventLedger, workspace_id: str):
    events = ledger.list_events(workspace_id)
    return events[-1] if events else None


def _model_dict(payload: dict[str, Any], key: str, model_type: type) -> dict[str, Any]:
    return {
        item_key: model_type(**item) for item_key, item in payload.get(key, {}).items()
    }


def _model_list(payload: dict[str, Any], key: str, model_type: type) -> list[Any]:
    return [model_type(**item) for item in payload.get(key, [])]


def _dataclass_list(payload: dict[str, Any], key: str, model_type: type) -> list[Any]:
    return [model_type(**item) for item in payload.get(key, [])]


def _parse_datetime(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


def _format_datetime(value: datetime | None) -> str | None:
    return value.isoformat() if value is not None else None


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)
