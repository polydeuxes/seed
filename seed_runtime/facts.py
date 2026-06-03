"""Fact models for Seed state projection."""

from __future__ import annotations

from datetime import datetime
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
