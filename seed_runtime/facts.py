"""Fact models for Seed state projection."""

from __future__ import annotations

from datetime import datetime, timezone
from importlib.util import find_spec
from typing import Any, Literal

from seed_runtime.base import SeedModel

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field

FactSourceType = Literal["user", "discovery", "provider", "inferred", "imported"]

DEFAULT_CONFIDENCE_BY_SOURCE_TYPE: dict[str, float] = {
    "user": 0.90,
    "discovery": 0.95,
    "provider": 0.85,
    "inferred": 0.60,
    "imported": 0.70,
}


STALE_FACT_REFRESH_CAPABILITY_BY_PREDICATE: dict[str, str] = {
    "runtime": "service_inspection",
    "host": "environment_inventory",
    "container": "docker_inspection",
    "weather": "weather_lookup",
    "current_weather": "weather_lookup",
}

FALLBACK_STALE_FACT_REFRESH_CAPABILITY = "knowledge_lookup"


def recommended_capability_for_stale_fact(predicate: str) -> str:
    """Return the deterministic capability that can refresh a stale predicate."""

    return STALE_FACT_REFRESH_CAPABILITY_BY_PREDICATE.get(
        predicate, FALLBACK_STALE_FACT_REFRESH_CAPABILITY
    )


class FactSupport(SeedModel):
    """Aggregated support for one subject/predicate/value claim.

    FactSupport preserves the contributing fact IDs instead of turning support
    into a single verified flag. Confidence is a projection over the supporting
    facts and their provenance source types.
    """

    subject: str
    predicate: str
    value: Any
    supporting_fact_ids: list[str] = Field(default_factory=list)
    source_types: list[FactSourceType] = Field(default_factory=list)
    confidence: float
    observed_at: datetime
    latest_observed_at: datetime
    expired: bool = False
    expires_at: datetime | None = None


class FactConflict(SeedModel):
    """A detected disagreement among facts for one subject and predicate."""

    subject: str
    predicate: str
    values: list[Any]
    winning_value: Any | None = None
    best_fact_id: str | None = None
    conflicting_fact_ids: list[str] = Field(default_factory=list)
    reason: str


class StaleFactRefreshRecommendation(SeedModel):
    """A deterministic capability recommendation for refreshing a stale fact."""

    fact_id: str
    subject: str
    predicate: str
    value: Any
    recommended_capability: str
    reason: str


def is_fact_expired(fact: "Fact", *, now: datetime | None = None) -> bool:
    """Return whether a fact has passed its optional expiry timestamp."""

    if fact.expires_at is None:
        return False
    comparison_time = now or datetime.now(timezone.utc)
    expires_at = fact.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if comparison_time.tzinfo is None:
        comparison_time = comparison_time.replace(tzinfo=timezone.utc)
    return expires_at <= comparison_time


class Fact(SeedModel):
    """A state fact with provenance links to evidence observations."""

    def __init__(self, **data: Any) -> None:
        if data.get("inferred", False):
            data["source_type"] = "inferred"
        data.setdefault("source_type", "user")
        if data["source_type"] not in DEFAULT_CONFIDENCE_BY_SOURCE_TYPE:
            raise ValueError("fact.source_type must be a known provenance source")
        if "confidence" not in data or data["confidence"] is None:
            data["confidence"] = DEFAULT_CONFIDENCE_BY_SOURCE_TYPE[data["source_type"]]
        confidence = float(data["confidence"])
        if confidence < 0.0 or confidence > 1.0:
            raise ValueError("fact.confidence must be between 0.0 and 1.0")
        data["confidence"] = confidence
        super().__init__(**data)

    id: str
    subject_id: str
    predicate: str
    value: Any
    evidence_ids: list[str] = Field(default_factory=list)
    source_type: FactSourceType = "user"
    confidence: float = DEFAULT_CONFIDENCE_BY_SOURCE_TYPE["user"]
    observed_at: datetime
    expires_at: datetime | None = None
    inferred: bool = False
