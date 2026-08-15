"""A parallel edge-indexed store, for measuring against the ledger.

This establishes nothing. It records no Assertion, owns no Responsibility, and
is not a witness any Act may consume.

It writes the same occurrences with their material references lifted into an
indexed edge table, so both traversal directions can be timed on one material.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Iterable


class DagLedgerComparison:
    """The same occurrences, with their references lifted out of the material."""

    def __init__(self, path: str = ":memory:") -> None:
        self._connection = sqlite3.connect(path)
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS nodes (
                identity TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                locality_identity TEXT,
                material TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS edges (
                source_identity TEXT NOT NULL,
                relation TEXT NOT NULL,
                destination_identity TEXT NOT NULL,
                ordinal INTEGER NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_edges_source
                ON edges (source_identity, relation, ordinal, destination_identity);
            CREATE INDEX IF NOT EXISTS idx_edges_destination
                ON edges (destination_identity, relation, source_identity);
            """
        )

    def load(self, events: Iterable[Any]) -> int:
        """Write each occurrence once, and one edge per reference it carries.

        A reference is a material string that names another occurrence present
        in the same material. Nothing infers a relation that the material does
        not already carry: the edge's relation is the field name that carried
        it, and an unresolvable string is not an edge.
        """

        edge_count = 0
        earlier_identities: set[str] = set()
        for event in events:
            self._connection.execute(
                "INSERT OR REPLACE INTO nodes VALUES (?, ?, ?, ?)",
                (
                    event.identity,
                    event.kind,
                    getattr(event, "locality_identity", None),
                    json.dumps(event.material, default=str),
                ),
            )
            references = dict.fromkeys(_references(event.material, earlier_identities))
            for relation, destination, ordinal in references:
                self._connection.execute(
                    "INSERT INTO edges VALUES (?, ?, ?, ?)",
                    (event.identity, relation, destination, ordinal),
                )
                edge_count += 1
            earlier_identities.add(event.identity)
        self._connection.commit()
        return edge_count

    def references_from(self, node_identity: str) -> list[tuple[str, str]]:
        """What this occurrence points at."""

        return [
            (relation, destination)
            for relation, destination in self._connection.execute(
                "SELECT relation, destination_identity FROM edges WHERE source_identity = ?"
                " ORDER BY relation, ordinal",
                (node_identity,),
            )
        ]

    def references_to(self, node_identity: str) -> list[tuple[str, str]]:
        """What points at this occurrence -- the direction the ledger cannot index."""

        return [
            (relation, source)
            for relation, source in self._connection.execute(
                "SELECT relation, source_identity FROM edges WHERE destination_identity = ?"
                " ORDER BY relation, source_identity",
                (node_identity,),
            )
        ]

    def byte_size(self) -> tuple[int, int]:
        """Material bytes and edge-table rows, so cost is stated rather than guessed."""

        material_bytes = sum(
            len(row[0].encode("utf-8"))
            for row in self._connection.execute("SELECT material FROM nodes")
        )
        edges = self._connection.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
        return material_bytes, edges


def _references(
    material: Any, known_identities: set[str], relation: str = "", ordinal: int = 0
) -> list[tuple[str, str, int]]:
    found: list[tuple[str, str, int]] = []
    if isinstance(material, dict):
        for key, nested in material.items():
            found.extend(_references(nested, known_identities, key, 0))
    elif isinstance(material, list):
        for position, nested in enumerate(material):
            found.extend(_references(nested, known_identities, relation, position))
    elif isinstance(material, str) and material in known_identities:
        found.append((relation, material, ordinal))
    return found
