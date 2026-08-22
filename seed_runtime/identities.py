"""Exact identity minting for Seed occurrences and results."""

from __future__ import annotations

from threading import Lock

_next_values: dict[str, int] = {}
_lock = Lock()


def new_identity(prefix: str) -> str:
    """Return one process-unique identity."""
    with _lock:
        next_value = _next_values.get(prefix, 1)
        _next_values[prefix] = next_value + 1
        return f"{prefix}_{next_value:06d}"


def reserve_identity_prefix(prefix: str, max_numeric_number: int) -> None:
    """Ensure future identities for ``prefix`` exceed a carried number."""
    if max_numeric_number < 0:
        raise ValueError("max_numeric_number must be non-negative")
    with _lock:
        _next_values[prefix] = max(_next_values.get(prefix, 1), max_numeric_number + 1)
