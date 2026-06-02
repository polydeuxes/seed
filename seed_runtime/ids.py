"""Identifier helpers for Seed domain objects."""

from __future__ import annotations

from itertools import count
from threading import Lock

_counters: dict[str, count] = {}
_lock = Lock()


def new_id(prefix: str) -> str:
    """Return a compact deterministic-process unique identifier."""
    with _lock:
        if prefix not in _counters:
            _counters[prefix] = count(1)
        return f"{prefix}_{next(_counters[prefix]):06d}"
