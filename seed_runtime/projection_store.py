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
)

STATE_PROJECTION_NAME = "state"
STATE_PROJECTION_VERSION = "state-v1"
STATE_SUMMARY_PROJECTION_NAME = "state-summary"
STATE_SUMMARY_PROJECTION_VERSION = "state-summary-v1"


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


@dataclass(frozen=True)
class ProjectionSnapshot:
    workspace_id: str
    projection_name: str
    projection_version: str
    last_event_id: str | None
    last_event_created_at: datetime | None
    state_payload: dict[str, Any]
    created_at: datetime


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


class InMemoryProjectionStore:
    """Process-local ProjectionStore useful for tests and non-SQLite callers."""

    def __init__(self) -> None:
        self._snapshots: dict[tuple[str, str], ProjectionSnapshot] = {}
        self._summary_snapshots: dict[tuple[str, str], SummaryProjectionSnapshot] = {}

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
            return
        for key in list(self._snapshots):
            if key[0] == workspace_id:
                self._snapshots.pop(key, None)
        for key in list(self._summary_snapshots):
            if key[0] == workspace_id:
                self._summary_snapshots.pop(key, None)

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
        return snapshot

    def save_summary_snapshot(self, snapshot: SummaryProjectionSnapshot) -> None:
        self._summary_snapshots[(snapshot.workspace_id, snapshot.projection_name)] = snapshot


class SQLiteProjectionStore:
    """SQLite-backed ProjectionStore for local CLI state projection caching."""

    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self._connection = sqlite3.connect(database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS projection_snapshots (
                workspace_id TEXT NOT NULL,
                projection_name TEXT NOT NULL,
                projection_version TEXT NOT NULL,
                last_event_id TEXT,
                last_event_created_at TEXT,
                state_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (workspace_id, projection_name)
            )
            """
        )
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS state_summary_snapshots (
                workspace_id TEXT NOT NULL,
                projection_name TEXT NOT NULL,
                projection_version TEXT NOT NULL,
                last_event_id TEXT,
                state_projection_version TEXT NOT NULL,
                state_last_event_id TEXT,
                summary_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (workspace_id, projection_name)
            )
            """
        )
        self._connection.commit()

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
        )

    def save_snapshot(self, snapshot: ProjectionSnapshot) -> None:
        self._connection.execute(
            """
            INSERT INTO projection_snapshots (
                workspace_id, projection_name, projection_version, last_event_id,
                last_event_created_at, state_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(workspace_id, projection_name) DO UPDATE SET
                projection_version = excluded.projection_version,
                last_event_id = excluded.last_event_id,
                last_event_created_at = excluded.last_event_created_at,
                state_json = excluded.state_json,
                created_at = excluded.created_at
            """,
            (
                snapshot.workspace_id,
                snapshot.projection_name,
                snapshot.projection_version,
                snapshot.last_event_id,
                _format_datetime(snapshot.last_event_created_at),
                json.dumps(snapshot.state_payload, sort_keys=True),
                _format_datetime(snapshot.created_at),
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
        )

    def save_summary_snapshot(self, snapshot: SummaryProjectionSnapshot) -> None:
        self._connection.execute(
            """
            INSERT INTO state_summary_snapshots (
                workspace_id, projection_name, projection_version, last_event_id,
                state_projection_version, state_last_event_id, summary_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(workspace_id, projection_name) DO UPDATE SET
                projection_version = excluded.projection_version,
                last_event_id = excluded.last_event_id,
                state_projection_version = excluded.state_projection_version,
                state_last_event_id = excluded.state_last_event_id,
                summary_json = excluded.summary_json,
                created_at = excluded.created_at
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


def project_state_with_cache(
    ledger: EventLedger,
    workspace_id: str,
    store: ProjectionStore | None,
    *,
    projector: StateProjector | None = None,
    projection_name: str = STATE_PROJECTION_NAME,
    projection_version: str = STATE_PROJECTION_VERSION,
) -> tuple[State, StateCacheStatus]:
    """Return projected State, reusing a valid ProjectionStore snapshot when possible."""

    projector = projector or StateProjector(ledger)
    latest_event = _latest_event(ledger, workspace_id)
    current_last_event_id = latest_event.id if latest_event is not None else None
    snapshot_last_event_id: str | None = None
    if store is not None:
        snapshot = store.load_snapshot(workspace_id, projection_name, projection_version)
        if snapshot is not None:
            snapshot_last_event_id = snapshot.last_event_id
            if snapshot.last_event_id == current_last_event_id:
                return state_from_payload(snapshot.state_payload), StateCacheStatus(
                    cache_hit=True,
                    projection_version=projection_version,
                    snapshot_last_event_id=snapshot.last_event_id,
                    current_last_event_id=current_last_event_id,
                )

    state = projector.project(workspace_id)
    if store is not None:
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
    return state, StateCacheStatus(
        cache_hit=False,
        projection_version=projection_version,
        snapshot_last_event_id=snapshot_last_event_id,
        current_last_event_id=current_last_event_id,
    )


def rebuild_state_cache(
    ledger: EventLedger,
    workspace_id: str,
    store: ProjectionStore,
    *,
    projector: StateProjector | None = None,
    projection_name: str = STATE_PROJECTION_NAME,
    projection_version: str = STATE_PROJECTION_VERSION,
) -> tuple[State, StateCacheStatus]:
    """Clear and rebuild the cached state projection snapshot."""

    store.clear_snapshot(workspace_id, projection_name)
    return project_state_with_cache(
        ledger,
        workspace_id,
        store,
        projector=projector,
        projection_name=projection_name,
        projection_version=projection_version,
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
        item_key: model_type(**item)
        for item_key, item in payload.get(key, {}).items()
    }


def _model_list(payload: dict[str, Any], key: str, model_type: type) -> list[Any]:
    return [model_type(**item) for item in payload.get(key, [])]


def _dataclass_list(
    payload: dict[str, Any], key: str, model_type: type
) -> list[Any]:
    return [model_type(**item) for item in payload.get(key, [])]


def _parse_datetime(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


def _format_datetime(value: datetime | None) -> str | None:
    return value.isoformat() if value is not None else None


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)
