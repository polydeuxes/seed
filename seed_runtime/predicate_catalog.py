"""Canonical predicate vocabulary and provider-to-canonical mappings."""

from __future__ import annotations

import json
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Iterable, Literal

from seed_runtime.base import SeedModel

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field


class PredicateDefinition(SeedModel):
    """Definition of one canonical thing Seed can know."""

    predicate: str
    kind: Literal["measurement", "durable_fact"]
    value_type: Literal["enum", "integer", "string"]
    cardinality: Literal["single", "multi"] = "single"
    allowed_values: list[Any] = Field(default_factory=list)


class PredicateMapping(SeedModel):
    """Mapping from a provider predicate into the canonical vocabulary."""

    predicate: str
    canonical_predicate: str
    source_name: str | None = None
    value_map: dict[str, Any] = Field(default_factory=dict)

    def map_value(self, value: Any) -> Any:
        """Return the mapped value, preserving values not named in the map."""

        return self.value_map.get(_value_map_key(value), value)


class PredicateCatalog:
    """Read-only vocabulary for what Seed can know."""

    def __init__(
        self,
        predicates: Iterable[PredicateDefinition] = (),
        mappings: Iterable[PredicateMapping] = (),
    ) -> None:
        self._predicates = {entry.predicate: entry for entry in predicates}
        self._mappings = list(mappings)
        for mapping in self._mappings:
            if mapping.canonical_predicate not in self._predicates:
                raise ValueError(
                    f"mapping for {mapping.predicate!r} references unknown canonical "
                    f"predicate {mapping.canonical_predicate!r}"
                )

    @classmethod
    def load(cls, path: str | Path | None = None) -> "PredicateCatalog":
        """Load a catalog file, defaulting to Seed's built-in core catalog."""

        catalog_path = Path(path) if path is not None else _builtin_catalog_path()
        if catalog_path.is_dir():
            catalog_path = catalog_path / "core.json"
        data = json.loads(catalog_path.read_text())
        if not isinstance(data, dict):
            raise ValueError(f"{catalog_path} must contain a JSON object")
        predicates = data.get("predicates", [])
        mappings = data.get("mappings", [])
        if not isinstance(predicates, list) or not isinstance(mappings, list):
            raise ValueError(f"{catalog_path} predicates and mappings must be arrays")
        return cls(
            predicates=[PredicateDefinition(**entry) for entry in predicates],
            mappings=[PredicateMapping(**entry) for entry in mappings],
        )

    def get(self, predicate: str) -> PredicateDefinition | None:
        """Return a canonical predicate definition, if present."""

        return self._predicates.get(predicate)

    def find_mapping(
        self, predicate: str, *, source_name: str | None = None
    ) -> PredicateMapping | None:
        """Return the most specific mapping matching a raw observation."""

        generic: PredicateMapping | None = None
        for mapping in self._mappings:
            if mapping.predicate != predicate:
                continue
            if mapping.source_name is None:
                generic = mapping
            elif source_name == mapping.source_name:
                return mapping
        return generic

    def cardinality(self, predicate: str) -> Literal["single", "multi"]:
        """Return predicate cardinality, defaulting unknown predicates to single."""

        definition = self.get(predicate)
        return definition.cardinality if definition is not None else "single"

    def is_multi(self, predicate: str) -> bool:
        """Return whether multiple values may be current simultaneously."""

        return self.cardinality(predicate) == "multi"

    def is_measurement(self, predicate: str) -> bool:
        """Return whether a canonical predicate has measurement semantics."""

        definition = self.get(predicate)
        return definition is not None and definition.kind == "measurement"

    def list_predicates(self) -> list[PredicateDefinition]:
        """Return canonical predicates in name order."""

        return [self._predicates[key] for key in sorted(self._predicates)]

    def list_mappings(self) -> list[PredicateMapping]:
        """Return mappings in stable provider/predicate order."""

        return sorted(
            self._mappings,
            key=lambda item: (
                item.source_name or "", item.predicate, item.canonical_predicate
            ),
        )


def _builtin_catalog_path() -> Path:
    return Path(__file__).resolve().parents[1] / "predicate_catalog" / "core.json"


def _value_map_key(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    return str(value)
