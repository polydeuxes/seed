"""Fact models for Seed state projection."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from importlib.util import find_spec

if find_spec("pydantic") is not None:
    from pydantic import BaseModel, ConfigDict, Field
else:
    from seed_runtime._pydantic_compat import BaseModel, ConfigDict, Field


class Fact(BaseModel):
    """A state fact with provenance links to evidence observations."""

    model_config = ConfigDict(frozen=True)

    id: str
    subject_id: str
    predicate: str
    value: Any
    evidence_ids: list[str] = Field(default_factory=list)
    observed_at: datetime
    expires_at: datetime | None = None
    confidence: float = 1.0
