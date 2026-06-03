"""Append-only in-memory event ledger."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
import json
import sqlite3
from typing import Any, Iterable

from seed_runtime.ids import new_id, reserve_id_prefix
from seed_runtime.models import Actor, Event, ExecutionAuthorization


class EventLedger:
    """Process-local append-only ledger for recording Seed runtime events."""

    def __init__(self) -> None:
        self._events: list[Event] = []
        self._by_id: dict[str, Event] = {}
        self._by_workspace: dict[str, list[Event]] = defaultdict(list)

    def append(
        self,
        kind: str,
        workspace_id: str = "default",
        payload: dict[str, Any] | None = None,
        *,
        actor: Actor = "system",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> Event:
        """Record an event and return the stored event."""
        event = Event(
            id=new_id("evt"),
            kind=kind,
            workspace_id=workspace_id,
            actor=actor,
            payload=payload or {},
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        self._store(event)
        return event

    def get(self, event_id: str) -> Event | None:
        """Return an event by id, if it exists."""
        return self._by_id.get(event_id)

    def list(self, workspace_id: str | None = None) -> list[Event]:
        """Return events in append order, optionally scoped to a workspace."""
        if workspace_id is None:
            return list(self._events)
        return list(self._by_workspace.get(workspace_id, []))

    def list_events(self, workspace_id: str | None = None) -> list[Event]:
        """Backward-compatible alias for :meth:`list`."""
        return self.list(workspace_id)

    def extend(self, events: Iterable[Event]) -> None:
        """Append externally constructed events while preserving order and IDs."""
        for event in events:
            self._store(event.model_copy(deep=True))

    def _store(self, event: Event) -> None:
        _validate_execution_authorization_event(event)
        if event.id in self._by_id:
            raise ValueError(f"event id already exists: {event.id}")
        self._events.append(event)
        self._by_id[event.id] = event
        self._by_workspace[event.workspace_id].append(event)


# Compatibility for older tests and callers; EventLedger itself remains in-memory.
class SQLiteEventLedger(EventLedger):
    """SQLite-backed ledger with the same public API as EventLedger."""

    _PERSISTED_ID_PREFIXES = (
        "plan",
        "handoff",
        "obs",
        "obs_local_host",
        "evd",
        "evd_obs",
        "fact",
        "fact_obs",
        "need",
        "auth",
    )

    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self._connection = sqlite3.connect(database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                workspace_id TEXT NOT NULL,
                actor TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                payload TEXT NOT NULL,
                session_id TEXT,
                causation_id TEXT,
                correlation_id TEXT
            )
            """)
        self._connection.commit()
        max_event_suffix = self._max_event_id_suffix()
        self._next_event_number = max_event_suffix + 1
        reserve_id_prefix("evt", max_event_suffix)
        self._reserve_persisted_payload_ids()

    def append(
        self,
        kind: str,
        workspace_id: str = "default",
        payload: dict[str, Any] | None = None,
        *,
        actor: Actor = "system",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> Event:
        event = Event(
            id=self._new_event_id(),
            kind=kind,
            workspace_id=workspace_id,
            actor=actor,
            payload=payload or {},
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        self._insert(event)
        return event

    def get(self, event_id: str) -> Event | None:
        row = self._connection.execute(
            "SELECT * FROM events WHERE id = ?",
            (event_id,),
        ).fetchone()
        return self._row_to_event(row) if row is not None else None

    def list(self, workspace_id: str | None = None) -> list[Event]:
        if workspace_id is None:
            rows = self._connection.execute(
                "SELECT * FROM events ORDER BY rowid"
            ).fetchall()
        else:
            rows = self._connection.execute(
                "SELECT * FROM events WHERE workspace_id = ? ORDER BY rowid",
                (workspace_id,),
            ).fetchall()
        return [self._row_to_event(row) for row in rows]

    def list_events(self, workspace_id: str | None = None) -> list[Event]:
        return self.list(workspace_id)

    def extend(self, events: Iterable[Event]) -> None:
        for event in events:
            self._insert(event)

    def close(self) -> None:
        self._connection.close()

    def _insert(self, event: Event) -> None:
        _validate_execution_authorization_event(event)
        self._connection.execute(
            """
            INSERT INTO events (id, kind, workspace_id, actor, timestamp, payload, session_id, causation_id, correlation_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.id,
                event.kind,
                event.workspace_id,
                event.actor,
                event.timestamp.isoformat(),
                json.dumps(event.payload),
                event.session_id,
                event.causation_id,
                event.correlation_id,
            ),
        )
        self._connection.commit()
        self._advance_event_counter(event.id)
        self._reserve_payload_ids(event.payload)

    def _row_to_event(self, row: sqlite3.Row) -> Event:
        return Event(
            id=row["id"],
            kind=row["kind"],
            workspace_id=row["workspace_id"],
            actor=row["actor"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
            payload=json.loads(row["payload"]),
            session_id=row["session_id"],
            causation_id=row["causation_id"],
            correlation_id=row["correlation_id"],
        )

    def _new_event_id(self) -> str:
        event_id = f"evt_{self._next_event_number:06d}"
        self._next_event_number += 1
        reserve_id_prefix("evt", self._next_event_number - 1)
        return event_id

    def _advance_event_counter(self, event_id: str) -> None:
        suffix = _numeric_suffix(event_id, "evt")
        if suffix is None:
            return
        self._next_event_number = max(self._next_event_number, suffix + 1)
        reserve_id_prefix("evt", suffix)

    def _max_event_id_suffix(self) -> int:
        row = self._connection.execute(
            """
            SELECT MAX(CAST(SUBSTR(id, 5) AS INTEGER)) AS max_suffix
            FROM events
            WHERE id LIKE 'evt_%'
              AND SUBSTR(id, 5) GLOB '[0-9]*'
              AND SUBSTR(id, 5) NOT GLOB '*[^0-9]*'
            """
        ).fetchone()
        return int(row["max_suffix"] or 0)

    def _reserve_persisted_payload_ids(self) -> None:
        rows = self._connection.execute(
            "SELECT payload FROM events ORDER BY rowid"
        ).fetchall()
        for row in rows:
            try:
                payload = json.loads(row["payload"])
            except (TypeError, json.JSONDecodeError):
                continue
            self._reserve_payload_ids(payload)

    def _reserve_payload_ids(self, payload: Any) -> None:
        max_suffixes = {prefix: 0 for prefix in self._PERSISTED_ID_PREFIXES}
        for value in _walk_values(payload):
            if not isinstance(value, str):
                continue
            for prefix in self._PERSISTED_ID_PREFIXES:
                suffix = _numeric_suffix(value, prefix)
                if suffix is not None:
                    max_suffixes[prefix] = max(max_suffixes[prefix], suffix)
        for prefix, max_suffix in max_suffixes.items():
            if max_suffix:
                reserve_id_prefix(prefix, max_suffix)


def _walk_values(value: Any) -> Iterable[Any]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from _walk_values(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_values(nested)
    else:
        yield value


def _validate_execution_authorization_event(event: Event) -> None:
    if event.kind != "execution_authorization.granted":
        return
    payload = event.payload.get("execution_authorization", event.payload)
    if not isinstance(payload, dict):
        raise ValueError("execution_authorization.granted requires an object payload")
    ExecutionAuthorization(**payload)


def _numeric_suffix(value: str, prefix: str) -> int | None:
    marker = f"{prefix}_"
    if not value.startswith(marker):
        return None
    suffix = value[len(marker) :]
    if not suffix.isdigit():
        return None
    return int(suffix)
