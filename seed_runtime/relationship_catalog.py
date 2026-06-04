"""Read-only vocabulary for topology relationships derived from facts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from seed_runtime.base import SeedModel


class RelationshipDefinition(SeedModel):
    """Definition of one directed relationship Seed can project from facts."""

    relationship: str
    subject_type: str
    object_type: str
    derived_from_predicates: list[str]
    object: str | None = None


class RelationshipCatalog:
    """Read-only vocabulary for how entities connect to each other."""

    def __init__(self, relationships: Iterable[RelationshipDefinition] = ()) -> None:
        entries = list(relationships)
        self._relationships = {entry.relationship: entry for entry in entries}
        if len(self._relationships) != len(entries):
            raise ValueError("relationship names must be unique")

        self._by_predicate: dict[str, list[RelationshipDefinition]] = {}
        for entry in entries:
            for predicate in entry.derived_from_predicates:
                self._by_predicate.setdefault(predicate, []).append(entry)

    @classmethod
    def load(cls, path: str | Path | None = None) -> "RelationshipCatalog":
        """Load a catalog file, defaulting to Seed's built-in core catalog."""

        catalog_path = Path(path) if path is not None else _builtin_catalog_path()
        if catalog_path.is_dir():
            catalog_path = catalog_path / "core.json"
        data = json.loads(catalog_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("relationships"), list):
            raise ValueError(f"{catalog_path} relationships must be an array")
        return cls(RelationshipDefinition(**entry) for entry in data["relationships"])

    def get(self, relationship: str) -> RelationshipDefinition | None:
        """Return a relationship definition by canonical name, if present."""

        return self._relationships.get(relationship)

    def for_predicate(self, predicate: str) -> list[RelationshipDefinition]:
        """Return definitions derived from a fact predicate in stable name order."""

        return sorted(
            self._by_predicate.get(predicate, ()), key=lambda entry: entry.relationship
        )

    def list_relationships(self) -> list[RelationshipDefinition]:
        """Return relationship definitions in stable name order."""

        return [self._relationships[name] for name in sorted(self._relationships)]


def _builtin_catalog_path() -> Path:
    return Path(__file__).resolve().parents[1] / "relationship_catalog" / "core.json"
