"""Capability catalog for mapping tool needs to provider recommendations."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from seed_runtime.base import SeedModel
from seed_runtime.models import ToolNeed
from seed_runtime.tool_needs import slugify


class CapabilityRecommendation(SeedModel):
    """A suggested provider that could satisfy a missing capability."""

    provider: str
    summary: str
    kind: str = "provider"
    source: str | None = None
    risk_class: str | None = None
    notes: str | None = None


class CapabilityCatalogEntry(SeedModel):
    """Catalog entry for one normalized capability."""

    capability: str
    summary: str
    recommendations: list[CapabilityRecommendation]


class CapabilityCatalog:
    """Read-only catalog of known capability-to-provider recommendations."""

    def __init__(self, entries: Iterable[CapabilityCatalogEntry] = ()) -> None:
        self._entries = {slugify(entry.capability): entry for entry in entries}

    @classmethod
    def load(cls, catalog_dir: str | Path = "capability_catalog") -> "CapabilityCatalog":
        """Load all ``*.yml`` catalog entries from a directory."""
        root = Path(catalog_dir)
        if not root.exists():
            return cls()
        entries = [cls._load_entry(path) for path in sorted(root.glob("*.yml"))]
        return cls(entries)

    @classmethod
    def _load_entry(cls, path: Path) -> CapabilityCatalogEntry:
        data = _load_yaml_mapping(path)
        capability = data.get("capability")
        summary = data.get("summary")
        recommendations = data.get("recommendations", [])
        if not isinstance(capability, str) or not capability.strip():
            raise ValueError(f"{path} must define capability")
        if not isinstance(summary, str) or not summary.strip():
            raise ValueError(f"{path} must define summary")
        if not isinstance(recommendations, list):
            raise ValueError(f"{path} recommendations must be a list")
        normalized_recommendations: list[CapabilityRecommendation] = []
        for index, recommendation in enumerate(recommendations):
            if not isinstance(recommendation, dict):
                raise ValueError(f"{path} recommendation #{index + 1} must be a mapping")
            normalized_recommendations.append(CapabilityRecommendation(**recommendation))
        return CapabilityCatalogEntry(
            capability=slugify(capability),
            summary=summary,
            recommendations=normalized_recommendations,
        )

    def get(self, capability: str) -> CapabilityCatalogEntry | None:
        """Return the catalog entry for a capability, if present."""
        return self._entries.get(slugify(capability))

    def recommend_for(self, tool_need: ToolNeed) -> list[CapabilityRecommendation]:
        """Return provider recommendations matching a tool need's capability."""
        entry = self.get(tool_need.capability)
        if entry is None:
            return []
        return list(entry.recommendations)

    def list_entries(self) -> list[CapabilityCatalogEntry]:
        """Return catalog entries in capability order."""
        return [self._entries[key] for key in sorted(self._entries)]


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        return _parse_simple_yaml(path.read_text())

    loaded = yaml.safe_load(path.read_text())
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return loaded


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    """Parse the small YAML subset used by the checked-in catalog files.

    This fallback keeps the runtime dependency-light when PyYAML is unavailable.
    It supports a top-level mapping plus indented lists of mappings, which is all
    the catalog format needs.
    """
    result: dict[str, Any] = {}
    current_list_key: str | None = None
    current_item: dict[str, Any] | None = None

    for raw_line in text.splitlines():
        line = _strip_comment(raw_line).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if indent == 0:
            current_list_key = None
            current_item = None
            key, value = _split_key_value(stripped)
            if value == "":
                result[key] = []
                current_list_key = key
            else:
                result[key] = _parse_scalar(value)
            continue

        if current_list_key is None:
            raise ValueError(f"unsupported YAML indentation: {raw_line!r}")
        if stripped.startswith("- "):
            item_text = stripped[2:].strip()
            current_item = {}
            result[current_list_key].append(current_item)
            if item_text:
                key, value = _split_key_value(item_text)
                current_item[key] = _parse_scalar(value)
            continue
        if current_item is None:
            raise ValueError(f"unsupported YAML list item: {raw_line!r}")
        key, value = _split_key_value(stripped)
        current_item[key] = _parse_scalar(value)

    return result


def _split_key_value(text: str) -> tuple[str, str]:
    key, separator, value = text.partition(":")
    if not separator or not key.strip():
        raise ValueError(f"expected key/value YAML line: {text!r}")
    return key.strip(), value.strip()


def _parse_scalar(value: str) -> str | bool | int | float | None:
    if value in {"null", "None", "~"}:
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def _strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    for index, char in enumerate(line):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            return line[:index]
    return line
