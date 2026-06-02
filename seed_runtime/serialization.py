"""Small serialization helpers for Seed model payloads."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any

from importlib.util import find_spec

if find_spec("pydantic") is not None:
    from pydantic import BaseModel
else:
    from seed_runtime._pydantic_compat import BaseModel


def to_plain(value: Any) -> Any:
    """Convert Seed models and datetimes into JSON-like values."""
    if isinstance(value, BaseModel):
        return to_plain(value.model_dump(mode="json"))
    if is_dataclass(value):
        return to_plain(asdict(value))
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): to_plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    return value
