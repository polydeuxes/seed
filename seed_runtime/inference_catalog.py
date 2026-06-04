"""Catalog of deterministic, local fact projection rules."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from seed_runtime.base import SeedModel


class InferenceRule(SeedModel):
    """One deterministic predicate/value projection rule."""

    id: str
    name: str
    when_predicate: str
    when_value: Any | None = None
    then_predicate: str
    then_value: Any
    confidence: float
    reason: str

    def __init__(self, **data: Any) -> None:
        confidence = float(data.get("confidence", 0.0))
        if confidence < 0.0 or confidence > 1.0:
            raise ValueError("inference rule confidence must be between 0.0 and 1.0")
        data["confidence"] = confidence
        super().__init__(**data)

    def matches(self, predicate: str, value: Any) -> bool:
        """Return whether a fact activates this rule."""

        return self.when_predicate == predicate and (
            self.when_value is None or self.when_value == value
        )


class InferenceCatalog:
    """Read-only catalog defining Seed's deterministic reasoning rules."""

    def __init__(self, rules: Iterable[InferenceRule] = ()) -> None:
        entries = list(rules)
        self._rules = {rule.id: rule for rule in entries}
        if len(self._rules) != len(entries):
            raise ValueError("inference rule ids must be unique")

    @classmethod
    def load(cls, path: str | Path | None = None) -> "InferenceCatalog":
        """Load a catalog file, defaulting to Seed's built-in core catalog."""

        catalog_path = Path(path) if path is not None else _builtin_catalog_path()
        if catalog_path.is_dir():
            catalog_path = catalog_path / "core.json"
        data = json.loads(catalog_path.read_text())
        if not isinstance(data, dict) or not isinstance(data.get("rules"), list):
            raise ValueError(f"{catalog_path} must contain a rules array")
        return cls(InferenceRule(**entry) for entry in data["rules"])

    def get(self, rule_id: str) -> InferenceRule | None:
        """Return a rule by id, if present."""

        return self._rules.get(rule_id)

    def list_rules(self) -> list[InferenceRule]:
        """Return rules in stable id order."""

        return [self._rules[rule_id] for rule_id in sorted(self._rules)]

    def matching_rules(self, predicate: str, value: Any) -> list[InferenceRule]:
        """Return all rules activated by a predicate/value pair."""

        return [rule for rule in self.list_rules() if rule.matches(predicate, value)]


def _builtin_catalog_path() -> Path:
    return Path(__file__).resolve().parents[1] / "inference_catalog" / "core.json"
