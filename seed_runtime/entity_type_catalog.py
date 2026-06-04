"""Read-only vocabulary for entity classifications."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from seed_runtime.base import SeedModel


class EntityTypeDefinition(SeedModel):
    """Definition of one entity type Seed can reason about."""

    entity_type: str
    description: str = ""


class EntityTypeCatalog:
    """Read-only vocabulary for entity classifications."""

    def __init__(self, entity_types: Iterable[EntityTypeDefinition] = ()) -> None:
        entries = list(entity_types)
        self._entity_types = {entry.entity_type: entry for entry in entries}
        if len(self._entity_types) != len(entries):
            raise ValueError("entity type names must be unique")
        if "unknown" not in self._entity_types:
            raise ValueError("entity type catalog must define 'unknown'")

    @classmethod
    def load(cls, path: str | Path | None = None) -> "EntityTypeCatalog":
        """Load a catalog file, defaulting to Seed's built-in core catalog."""

        catalog_path = Path(path) if path is not None else _builtin_catalog_path()
        if catalog_path.is_dir():
            catalog_path = catalog_path / "core.json"
        data = json.loads(catalog_path.read_text())
        if not isinstance(data, dict) or not isinstance(data.get("entity_types"), list):
            raise ValueError(f"{catalog_path} must contain an entity_types array")
        return cls(EntityTypeDefinition(**entry) for entry in data["entity_types"])

    def get(self, entity_type: str) -> EntityTypeDefinition | None:
        """Return an entity type definition by canonical name, if present."""

        return self._entity_types.get(entity_type)

    def list_entity_types(self) -> list[EntityTypeDefinition]:
        """Return entity type definitions in stable name order."""

        return [self._entity_types[name] for name in sorted(self._entity_types)]


def _builtin_catalog_path() -> Path:
    return Path(__file__).resolve().parents[1] / "entity_type_catalog" / "core.json"
