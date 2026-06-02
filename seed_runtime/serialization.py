"""Small serialization helpers for dataclass payloads."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any


def to_plain(value: Any) -> Any:
    """Convert Seed dataclasses and datetimes into JSON-like values."""
    if is_dataclass(value):
        return to_plain(asdict(value))
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): to_plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    return value
