"""Append-only event ledgers."""

from __future__ import annotations

import json
import sqlite3
from collections import defaultdict
from dataclasses import replace
from datetime import datetime
from typing import Any, Iterable

from seed_runtime.ids import new_id
from seed_runtime.models import Actor, Event, utc_now


class EventLedger:
    """Process-local append-only ledger used by the prototype and tests."""

    def __init__(self) -> None:
        self._events: list[Event] = []
        self._by_workspace: dict[str, list[Event]] = defaultdict(list)

    def append(
        self,
        kind: str,
        workspace_id: str,
        payload: dict[str, Any] | None = None,
        *,
        actor: Actor = "system",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> Event:
        event = Event(
            id=new_id("evt"),
            kind=kind,
            workspace_id=workspace_id,
            actor=actor,
            timestamp=utc_now(),
            payload=payload or {},
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        self._store(event)
        return event

    def list_events(self, workspace_id: str | None = None) -> list[Event]:
        if workspace_id is None:
            return list(self._events)
        return list(self._by_workspace.get(workspace_id, []))

    def extend(self, events: Iterable[Event]) -> None:
        """Append externally constructed events while preserving order and IDs."""
        for event in events:
            self._store(replace(event))

    def _store(self, event: Event) -> None:
        self._events.append(event)
        self._by_workspace[event.workspace_id].append(event)


class SQLiteEventLedger(EventLedger):
    """SQLite-backed append-only ledger with the same public API."""

    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self._connection = sqlite3.connect(database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                id TEXT UNIQUE NOT NULL,
                kind TEXT NOT NULL,
                workspace_id TEXT NOT NULL,
                actor TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                payload TEXT NOT NULL,
                session_id TEXT,
                causation_id TEXT,
                correlation_id TEXT
            )
            """
        )
        self._connection.commit()

    def append(
        self,
        kind: str,
        workspace_id: str,
        payload: dict[str, Any] | None = None,
        *,
        actor: Actor = "system",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> Event:
        event = Event(
            id=new_id("evt"),
            kind=kind,
            workspace_id=workspace_id,
            actor=actor,
            timestamp=utc_now(),
            payload=payload or {},
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        self._store(event)
        return event

    def list_events(self, workspace_id: str | None = None) -> list[Event]:
        if workspace_id is None:
            rows = self._connection.execute("SELECT * FROM events ORDER BY sequence").fetchall()
        else:
            rows = self._connection.execute(
                "SELECT * FROM events WHERE workspace_id = ? ORDER BY sequence",
                (workspace_id,),
            ).fetchall()
        return [self._row_to_event(row) for row in rows]

    def close(self) -> None:
        self._connection.close()

    def _store(self, event: Event) -> None:
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
