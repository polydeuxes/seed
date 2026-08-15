"""A parallel edge-indexed store, for measuring against the ledger.

This establishes nothing. It records no Assertion, owns no Responsibility, and
is not a road any Act may consume.

It writes the same occurrences with their payload references lifted into an
indexed edge table, so both traversal directions can be timed on one material.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Iterable


class DagLedgerComparison:
    """The same occurrences, with their references lifted out of the payload."""

    def __init__(self, path: str = ":memory:") -> None:
        self._connection = sqlite3.connect(path)
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                locality_id TEXT,
                payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS edges (
                source_id TEXT NOT NULL,
                relation TEXT NOT NULL,
                destination_id TEXT NOT NULL,
                ordinal INTEGER NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_edges_source
                ON edges (source_id, relation, ordinal, destination_id);
            CREATE INDEX IF NOT EXISTS idx_edges_destination
                ON edges (destination_id, relation, source_id);
            """
        )

    def load(self, events: Iterable[Any]) -> int:
        """Write each occurrence once, and one edge per reference it carries.

        A reference is a payload string that names another occurrence present
        in the same material. Nothing infers a relation that the payload does
        not already carry: the edge's relation is the field name that carried
        it, and an unresolvable string is not an edge.
        """

        edge_count = 0
        earlier_ids: set[str] = set()
        for event in events:
            self._connection.execute(
                "INSERT OR REPLACE INTO nodes VALUES (?, ?, ?, ?)",
                (
                    event.id,
                    event.kind,
                    getattr(event, "locality_id", None),
                    json.dumps(event.payload, default=str),
                ),
            )
            references = dict.fromkeys(_references(event.payload, earlier_ids))
            for relation, destination, ordinal in references:
                self._connection.execute(
                    "INSERT INTO edges VALUES (?, ?, ?, ?)",
                    (event.id, relation, destination, ordinal),
                )
                edge_count += 1
            earlier_ids.add(event.id)
        self._connection.commit()
        return edge_count

    def references_from(self, node_id: str) -> list[tuple[str, str]]:
        """What this occurrence points at."""

        return [
            (relation, destination)
            for relation, destination in self._connection.execute(
                "SELECT relation, destination_id FROM edges WHERE source_id = ?"
                " ORDER BY relation, ordinal",
                (node_id,),
            )
        ]

    def references_to(self, node_id: str) -> list[tuple[str, str]]:
        """What points at this occurrence -- the direction the ledger cannot index."""

        return [
            (relation, source)
            for relation, source in self._connection.execute(
                "SELECT relation, source_id FROM edges WHERE destination_id = ?"
                " ORDER BY relation, source_id",
                (node_id,),
            )
        ]

    def byte_size(self) -> tuple[int, int]:
        """Payload bytes and edge-table rows, so cost is stated rather than guessed."""

        payload_bytes = sum(
            len(row[0].encode("utf-8"))
            for row in self._connection.execute("SELECT payload FROM nodes")
        )
        edges = self._connection.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
        return payload_bytes, edges


def _references(
    payload: Any, known_ids: set[str], relation: str = "", ordinal: int = 0
) -> list[tuple[str, str, int]]:
    found: list[tuple[str, str, int]] = []
    if isinstance(payload, dict):
        for key, nested in payload.items():
            found.extend(_references(nested, known_ids, key, 0))
    elif isinstance(payload, list):
        for position, nested in enumerate(payload):
            found.extend(_references(nested, known_ids, relation, position))
    elif isinstance(payload, str) and payload in known_ids:
        found.append((relation, payload, ordinal))
    return found
