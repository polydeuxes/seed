"""Secret boundary helpers for Seed runtime payloads."""

from __future__ import annotations

from typing import Any, Iterable

SECRET_FIELD_NAMES = frozenset(
    {
        "password",
        "passphrase",
        "token",
        "private_key",
    }
)

SECRET_FREE_GRANT_METADATA_FIELDS = frozenset(
    {
        "interactive_prompt",
        "ssh_agent",
        "sudo_timestamp",
        "vault_token_reference",
    }
)


def secret_boundary_key(name: object) -> str:
    """The representation this boundary compares a payload key in.

    Three foldings: whitespace, case, and `-`/`_`. No input evidence says
    these spellings name one field; this boundary imposes that equality so a
    caller cannot slip `Token` past a check for `token`.

    Not the Book's Normalization (09.Assertion:15), which represents asserted
    content and source coordinates in another exact representation. No Assertion,
    asserted content, or source coordinate is involved here.
    """

    return str(name).strip().lower().replace("-", "_")


def reject_secret_fields(
    value: Any,
    path: str = "payload",
    *,
    allowed_fields: Iterable[str] = (),
) -> None:
    """Reject dictionaries containing raw-secret field names.

    The boundary is intentionally key based: Seed must not accept payload slots
    named like raw secret carriers. References to separate secret systems should
    use explicit ``*_reference`` fields such as ``vault_token_reference`` instead of
    raw ``token`` fields.
    """

    allowed = {secret_boundary_key(field) for field in allowed_fields}
    _reject_secret_fields(value, path, allowed)


def _reject_secret_fields(value: Any, path: str, allowed_fields: set[str]) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            boundary_key = secret_boundary_key(key)
            if (
                boundary_key in SECRET_FIELD_NAMES
                and boundary_key not in allowed_fields
            ):
                raise ValueError(f"secret field is not allowed in {path}: {key}")
            # Secret rejection is key based. Scalars cannot contain another
            # field name, so only containers can extend the search boundary.
            if isinstance(nested, (dict, list)):
                _reject_secret_fields(nested, f"{path}.{key}", allowed_fields)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            if isinstance(nested, (dict, list)):
                _reject_secret_fields(nested, f"{path}[{index}]", allowed_fields)
