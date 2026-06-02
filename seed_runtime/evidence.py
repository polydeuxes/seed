"""Evidence models for provenance-backed Seed facts."""

from __future__ import annotations

from datetime import datetime
from importlib.util import find_spec
from typing import Any

from seed_runtime.base import SeedModel

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field


class Evidence(SeedModel):
    """An observed source payload that can support one or more facts."""

    id: str
    workspace_id: str
    source: str
    kind: str
    observed_at: datetime
    payload: dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
