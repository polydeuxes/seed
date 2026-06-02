"""Identifier helpers for Seed domain objects."""

from __future__ import annotations

from threading import Lock

_next_values: dict[str, int] = {}
_lock = Lock()


def new_id(prefix: str) -> str:
    """Return a compact deterministic-process unique identifier."""
    with _lock:
        next_value = _next_values.get(prefix, 1)
        _next_values[prefix] = next_value + 1
        return f"{prefix}_{next_value:06d}"


def reserve_id_prefix(prefix: str, max_numeric_suffix: int) -> None:
    """Ensure future IDs for ``prefix`` are greater than an observed suffix."""
    if max_numeric_suffix < 0:
        raise ValueError("max_numeric_suffix must be non-negative")
    with _lock:
        _next_values[prefix] = max(_next_values.get(prefix, 1), max_numeric_suffix + 1)
