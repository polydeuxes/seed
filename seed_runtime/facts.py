"""Fact models for Seed state projection."""

from __future__ import annotations

from datetime import datetime
from importlib.util import find_spec
from typing import Any

from seed_runtime.base import SeedModel

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field


class Fact(SeedModel):
    """A state fact with provenance links to evidence observations."""

    id: str
    subject_id: str
    predicate: str
    value: Any
    evidence_ids: list[str] = Field(default_factory=list)
    observed_at: datetime
    expires_at: datetime | None = None
    confidence: float = 1.0
