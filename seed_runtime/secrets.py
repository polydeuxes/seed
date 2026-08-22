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


def is_secret_boundary_key(name: object) -> bool:
    """Whether one key resolves to a refused secret-field name.

    The refused names begin with ``p`` or ``t`` after surrounding whitespace
    is removed. Keys that cannot acquire either initial need no allocation or
    case conversion. Potential spelling variants still take the complete
    normalization path.
    """

    if type(name) is str:
        if not name:
            return False
        first = name[0]
        # Every refused spelling begins with p or t after surrounding
        # whitespace is removed.  Other first characters cannot normalize to
        # one of those exact names, so their remaining characters need no
        # allocation or case conversion.
        if first not in ("p", "P", "t", "T") and not first.isspace():
            return False
    return secret_boundary_key(name) in SECRET_FIELD_NAMES
