"""Evidence models for provenance-backed Seed facts."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from importlib.util import find_spec

if find_spec("pydantic") is not None:
    from pydantic import BaseModel, ConfigDict, Field
else:
    from seed_runtime._pydantic_compat import BaseModel, ConfigDict, Field


class Evidence(BaseModel):
    """An observed source payload that can support one or more facts."""

    model_config = ConfigDict(frozen=True)

    id: str
    workspace_id: str
    source: str
    kind: str
    observed_at: datetime
    payload: dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
