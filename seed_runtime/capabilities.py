"""Capability normalization helpers."""

from __future__ import annotations

import re

_SLUG_CHARS = re.compile(r"[^a-z0-9_]+")


def slugify(value: str) -> str:
    """Normalize names using Seed's existing capability slugging behavior."""
    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    normalized = _SLUG_CHARS.sub("_", normalized).strip("_")
    return normalized or "unnamed_tool"


def normalize_capability(value: str) -> str:
    """Return the normalized capability slug for a non-blank string."""
    if not isinstance(value, str):
        raise ValueError("capability must be a string")
    if not value.strip():
        raise ValueError("capability must be a non-empty string")
    normalized = slugify(value)
    if not normalized:
        raise ValueError("capability must normalize to a non-empty string")
    return normalized


def normalize_capabilities(values: list[str]) -> list[str]:
    """Normalize a sequence of operation capability slugs."""
    if not isinstance(values, list):
        raise ValueError("capabilities must be a list of strings")
    return [normalize_capability(value) for value in values]
