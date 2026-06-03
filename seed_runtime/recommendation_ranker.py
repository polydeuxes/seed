"""Rank CapabilityCatalog recommendations against observed Seed state."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from datetime import datetime, timezone
from typing import Any

from seed_runtime.base import SeedModel
from seed_runtime.capability_catalog import CapabilityRecommendation
from seed_runtime.facts import is_fact_expired
from seed_runtime.models import Entity, Fact
from seed_runtime.state import State
from seed_runtime.tool_needs import slugify

_TOKEN_RE = re.compile(r"[a-z0-9]+")
_RISK_LEVELS = {"L1": 1, "L2": 2, "L3": 3, "L4": 4}
_CONTEXT_PREDICATES = ("runtime", "platform")


class RankedRecommendation(SeedModel):
    """A catalog recommendation annotated with ranker score and reasoning."""

    provider: str
    summary: str
    kind: str = "provider"
    source: str | None = None
    risk_class: str | None = None
    notes: str | None = None
    score: int
    reasons: list[str]
    reasoning: list[str]


class RecommendationRanker:
    """Score catalog recommendations using state and environment facts.

    The ranker is intentionally read-only: it only inspects the supplied state,
    entities, and facts. It never executes providers, installs providers, or
    mutates tool registration.
    """

    def rank(
        self,
        capability: str,
        recommendations: Iterable[CapabilityRecommendation],
        state: State | None,
        *,
        registered_tools: (
            Iterable[Any] | Mapping[str, Any] | Mapping[str, Iterable[Any]] | None
        ) = None,
        entities: (
            Iterable[Entity | Mapping[str, Any]]
            | Mapping[str, Entity | Mapping[str, Any]]
            | Mapping[str, Iterable[Entity | Mapping[str, Any]]]
            | None
        ) = None,
        facts: (
            Iterable[Fact | Mapping[str, Any]]
            | Mapping[str, Fact | Mapping[str, Any]]
            | Mapping[str, Iterable[Fact | Mapping[str, Any]]]
            | None
        ) = None,
    ) -> list[RankedRecommendation]:
        """Return recommendations ordered by score, with score reasoning.

        Args:
            capability: Normalized or human-readable capability name.
            recommendations: Catalog recommendations for the capability.
            state: Current Seed state snapshot.
            registered_tools: Optional supplemental registered-tool inventory, such
                as the payload returned by environment_inventory.list_registered_tools.
            entities: Optional supplemental entities or environment entities, such
                as the payload returned by environment_inventory.list_known_entities.
            facts: Optional supplemental state/environment facts, such as the
                payload returned by environment_inventory.list_known_facts.
        """
        recommendation_list = list(recommendations)
        registered_providers = self._registered_provider_names(state, registered_tools)
        known_runtime_values = self._known_context_values(
            "runtime", state, entities, facts
        )
        known_platform_values = self._known_context_values(
            "platform", state, entities, facts
        )

        ranked: list[tuple[int, RankedRecommendation]] = []
        lowest_risk_level = self._lowest_risk_level(recommendation_list)
        for index, recommendation in enumerate(recommendation_list):
            score = 0
            reasons: list[str] = []
            reasoning: list[str] = []
            provider_key = slugify(recommendation.provider)
            recommendation_tokens = self._recommendation_tokens(recommendation)

            if provider_key in registered_providers:
                score += 1000
                reasons.append("provider already registered")
                reasoning.append("+1000 provider already registered")

            matched_runtime = self._matching_runtime_value(
                known_runtime_values, recommendation.provider, recommendation_tokens
            )
            if matched_runtime is not None:
                runtime_boost = self._runtime_provider_boost(
                    matched_runtime, recommendation.provider
                )
                score += runtime_boost
                reasons.append(f"provider matches known runtime: {matched_runtime}")
                reasoning.append(
                    f"+{runtime_boost} provider matches known runtime: "
                    f"{matched_runtime}"
                )

            matched_platform = self._matching_value(
                known_platform_values, recommendation_tokens
            )
            if matched_platform is not None:
                score += 25
                reasons.append(f"provider matches known platform: {matched_platform}")
                reasoning.append(
                    f"+25 provider matches known platform: {matched_platform}"
                )

            risk_level = self._risk_level(recommendation.risk_class)
            if risk_level is not None and risk_level == lowest_risk_level:
                score += 10
                reasons.append(
                    f"lower risk class: {recommendation.risk_class or 'unknown'}"
                )
                reasoning.append(
                    f"+10 lower risk class: {recommendation.risk_class or 'unknown'}"
                )

            if index == 0:
                score += 5
                reasons.append("catalog default")
                reasoning.append("+5 catalog default priority")

            if not reasoning:
                reasons.append("no ranking signals matched")
                reasoning.append("0 no ranking signals matched")

            ranked.append(
                (
                    index,
                    RankedRecommendation(
                        **recommendation.model_dump(mode="python"),
                        score=score,
                        reasons=reasons,
                        reasoning=reasoning,
                    ),
                )
            )

        ranked.sort(key=lambda item: (-item[1].score, item[0]))
        return [recommendation for _, recommendation in ranked]

    def _registered_provider_names(
        self,
        state: State | None,
        registered_tools: (
            Iterable[Any] | Mapping[str, Any] | Mapping[str, Iterable[Any]] | None
        ) = None,
    ) -> set[str]:
        tools = list(self._mapping_or_iterable_values(state.tools if state else None))
        tools.extend(self._inventory_items(registered_tools, "tools"))

        names: set[str] = set()
        if state is not None:
            names.update(slugify(name) for name in state.tools)

        for tool in tools:
            for field in ("name", "toolkit_id"):
                value = self._get(tool, field)
                if value:
                    names.add(slugify(str(value)))
            for field in ("policy_action", "implementation"):
                value = self._get(tool, field)
                if isinstance(value, str):
                    names.update(
                        slugify(part) for part in re.split(r"[.:]", value) if part
                    )

        return names

    def _known_context_values(
        self,
        key: str,
        state: State | None,
        entities: (
            Iterable[Entity | Mapping[str, Any]]
            | Mapping[str, Entity | Mapping[str, Any]]
            | None
        ),
        facts: (
            Iterable[Fact | Mapping[str, Any]]
            | Mapping[str, Fact | Mapping[str, Any]]
            | None
        ),
    ) -> list[str]:
        values: list[str] = []
        all_entities = list(
            self._mapping_or_iterable_values(state.entities if state else None)
        )
        all_entities.extend(self._inventory_items(entities, "entities"))
        all_facts = list(
            self._mapping_or_iterable_values(state.facts if state else None)
        )
        all_facts.extend(self._inventory_items(facts, "facts"))

        for entity in all_entities:
            attributes = self._get(entity, "attributes") or {}
            if isinstance(attributes, Mapping):
                values.extend(self._extract_context_values(attributes.get(key)))

        for fact in all_facts:
            if self._is_expired_fact(fact):
                continue
            predicate = str(self._get(fact, "predicate") or "").lower()
            value = self._get(fact, "value")
            if self._predicate_mentions(predicate, key):
                values.extend(self._extract_context_values(value))
            elif isinstance(value, Mapping):
                values.extend(self._extract_context_values(value.get(key)))

        return self._dedupe(values)

    def _is_expired_fact(self, fact: Any) -> bool:
        if isinstance(fact, Fact):
            return is_fact_expired(fact)
        expires_at = self._get(fact, "expires_at")
        if expires_at is None:
            return False
        if isinstance(expires_at, str):
            try:
                expires_at = datetime.fromisoformat(expires_at)
            except ValueError:
                return False
        if not isinstance(expires_at, datetime):
            return False
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        return expires_at <= datetime.now(timezone.utc)

    def _predicate_mentions(self, predicate: str, key: str) -> bool:
        parts = {part for part in re.split(r"[^a-z0-9]+", predicate) if part}
        return key in parts or predicate.endswith(key)

    def _extract_context_values(self, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        if isinstance(value, bool | int | float):
            return [str(value)]
        if isinstance(value, Mapping):
            values: list[str] = []
            for context_key in _CONTEXT_PREDICATES:
                values.extend(self._extract_context_values(value.get(context_key)))
            return values
        if isinstance(value, Iterable) and not isinstance(value, bytes):
            values: list[str] = []
            for item in value:
                values.extend(self._extract_context_values(item))
            return values
        return []

    def _matching_runtime_value(
        self, values: list[str], provider: str, tokens: set[str]
    ) -> str | None:
        provider_key = slugify(provider)
        for value in values:
            runtime_key = slugify(value)
            if runtime_key == "docker" and provider_key == "docker_container_lifecycle":
                return value
            if runtime_key == "systemd" and provider_key == "systemctl_cli":
                return value
        return self._matching_value(values, tokens)

    def _runtime_provider_boost(self, runtime: str, provider: str) -> int:
        runtime_key = slugify(runtime)
        provider_key = slugify(provider)
        if runtime_key == "docker" and provider_key == "docker_container_lifecycle":
            return 200
        if runtime_key == "systemd" and provider_key == "systemctl_cli":
            return 200
        return 50

    def _recommendation_tokens(self, recommendation: CapabilityRecommendation) -> set[str]:
        text = " ".join(
            part
            for part in (
                recommendation.provider,
                recommendation.summary,
                recommendation.kind,
                recommendation.source,
                recommendation.notes,
            )
            if part
        )
        return set(_TOKEN_RE.findall(text.lower()))

    def _matching_value(self, values: list[str], tokens: set[str]) -> str | None:
        for value in values:
            value_tokens = set(_TOKEN_RE.findall(value.lower()))
            if value_tokens and value_tokens.issubset(tokens):
                return value
        return None

    def _lowest_risk_level(
        self, recommendations: list[CapabilityRecommendation]
    ) -> int | None:
        levels = [
            level
            for level in (
                self._risk_level(recommendation.risk_class)
                for recommendation in recommendations
            )
            if level is not None
        ]
        return min(levels) if levels else None

    def _risk_level(self, risk_class: str | None) -> int | None:
        return _RISK_LEVELS.get((risk_class or "").upper())

    def _inventory_items(self, value: Any, collection_key: str) -> list[Any]:
        if isinstance(value, Mapping) and collection_key in value:
            return self._mapping_or_iterable_values(value.get(collection_key))
        return self._mapping_or_iterable_values(value)

    def _mapping_or_iterable_values(self, value: Any) -> list[Any]:
        if value is None:
            return []
        if isinstance(value, Mapping):
            return list(value.values())
        if isinstance(value, str | bytes):
            return [value]
        return list(value)

    def _get(self, value: Any, name: str) -> Any:
        if isinstance(value, Mapping):
            return value.get(name)
        return getattr(value, name, None)

    def _dedupe(self, values: list[str]) -> list[str]:
        seen: set[str] = set()
        deduped: list[str] = []
        for value in values:
            normalized = value.strip()
            key = normalized.lower()
            if normalized and key not in seen:
                seen.add(key)
                deduped.append(normalized)
        return deduped
