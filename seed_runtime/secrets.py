"""Secret boundary helpers for Seed runtime materials."""

from __future__ import annotations

SECRET_FIELD_NAMES = frozenset(
    {
        "password",
        "passphrase",
        "token",
        "private_key",
    }
)


def secret_boundary_key(name: object) -> str:
    """Return the exact key representation used by this boundary."""
    return str(name).strip().lower().replace("-", "_")
