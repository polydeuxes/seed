"""Read-only catalog of deterministic fact inference rules."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from seed_runtime.base import SeedModel


class InferenceRule(SeedModel):
    """One deterministic source-fact to inferred-fact transformation."""

    def __init__(self, **data: Any) -> None:
        confidence_cap = float(data.get("confidence_cap", 0.6))
        if confidence_cap < 0.0 or confidence_cap > 1.0:
            raise ValueError("inference rule confidence_cap must be between 0.0 and 1.0")
        data["confidence_cap"] = confidence_cap
        super().__init__(**data)

    id: str
    source_predicate: str
    source_value: Any
    target_predicate: str
    target_value: Any
    confidence_cap: float = 0.6
    description: str = ""


class InferenceCatalog:
    """Read-only vocabulary of deterministic inference rules."""

    def __init__(self, rules: Iterable[InferenceRule] = ()) -> None:
        entries = list(rules)
        self._rules = {rule.id: rule for rule in entries}
        if len(self._rules) != len(entries):
            raise ValueError("inference rule IDs must be unique")
        self._by_source_predicate: dict[str, list[InferenceRule]] = {}
        for rule in entries:
            self._by_source_predicate.setdefault(rule.source_predicate, []).append(rule)

    @classmethod
    def load(cls, path: str | Path | None = None) -> "InferenceCatalog":
        """Load a catalog file, defaulting to Seed's built-in core catalog."""

        catalog_path = Path(path) if path is not None else _builtin_catalog_path()
        if catalog_path.is_dir():
            catalog_path = catalog_path / "core.json"
        data = json.loads(catalog_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("inference_rules"), list):
            raise ValueError(f"{catalog_path} inference_rules must be an array")
        return cls(InferenceRule(**entry) for entry in data["inference_rules"])

    def get(self, rule_id: str) -> InferenceRule | None:
        """Return an inference rule by ID, if present."""

        return self._rules.get(rule_id)

    def for_source_predicate(self, predicate: str) -> list[InferenceRule]:
        """Return rules matching a source predicate in stable ID order."""

        return sorted(
            self._by_source_predicate.get(predicate, ()), key=lambda rule: rule.id
        )

    def list_inference_rules(self) -> list[InferenceRule]:
        """Return all inference rules in stable ID order."""

        return [self._rules[rule_id] for rule_id in sorted(self._rules)]

    def list_rules(self) -> list[InferenceRule]:
        """Backward-compatible shorthand for :meth:`list_inference_rules`."""

        return self.list_inference_rules()

    @property
    def source_predicates(self) -> set[str]:
        """Return predicates that can trigger at least one inference rule."""

        return set(self._by_source_predicate)


def _builtin_catalog_path() -> Path:
    return Path(__file__).resolve().parents[1] / "inference_catalog" / "core.json"
