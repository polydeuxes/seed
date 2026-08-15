from __future__ import annotations

import json
import sqlite3
from typing import Any, Iterable


class ReferencePairComparison:
    def __init__(self, path: str = ":memory:") -> None:
        self._connection = sqlite3.connect(path)
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS occurrences (
                identity TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                locality_identity TEXT,
                material TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS reference_pairs (
                source_identity TEXT NOT NULL,
                relation TEXT NOT NULL,
                destination_identity TEXT NOT NULL,
                position INTEGER NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_reference_pairs_source
                ON reference_pairs (source_identity, relation, position, destination_identity);
            CREATE INDEX IF NOT EXISTS idx_reference_pairs_destination
                ON reference_pairs (destination_identity, relation, source_identity);
            """
        )

    def load(self, events: Iterable[Any]) -> int:
        pair_count = 0
        earlier_identities: set[str] = set()
        for event in events:
            self._connection.execute(
                "INSERT OR REPLACE INTO occurrences VALUES (?, ?, ?, ?)",
                (
                    event.identity,
                    event.kind,
                    getattr(event, "locality_identity", None),
                    json.dumps(event.material, default=str),
                ),
            )
            references = dict.fromkeys(_references(event.material, earlier_identities))
            for relation, destination, position in references:
                self._connection.execute(
                    "INSERT INTO reference_pairs VALUES (?, ?, ?, ?)",
                    (event.identity, relation, destination, position),
                )
                pair_count += 1
            earlier_identities.add(event.identity)
        self._connection.commit()
        return pair_count

    def references_from(self, occurrence_identity: str) -> list[tuple[str, str]]:
        return [
            (relation, destination)
            for relation, destination in self._connection.execute(
                "SELECT relation, destination_identity FROM reference_pairs WHERE source_identity = ?"
                " ORDER BY relation, position",
                (occurrence_identity,),
            )
        ]

    def references_to(self, occurrence_identity: str) -> list[tuple[str, str]]:
        return [
            (relation, source)
            for relation, source in self._connection.execute(
                "SELECT relation, source_identity FROM reference_pairs WHERE destination_identity = ?"
                " ORDER BY relation, source_identity",
                (occurrence_identity,),
            )
        ]


def _references(
    material: Any, known_identities: set[str], relation: str = "", position: int = 0
) -> list[tuple[str, str, int]]:
    found: list[tuple[str, str, int]] = []
    if isinstance(material, dict):
        for key, nested in material.items():
            found.extend(_references(nested, known_identities, key, 0))
    elif isinstance(material, list):
        for position, nested in enumerate(material):
            found.extend(_references(nested, known_identities, relation, position))
    elif isinstance(material, str) and material in known_identities:
        found.append((relation, material, position))
    return found
