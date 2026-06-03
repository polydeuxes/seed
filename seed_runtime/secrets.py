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
        "external_vault_token_ref",
    }
)


def normalize_field_name(name: object) -> str:
    """Normalize a payload key for secret-boundary comparisons."""

    return str(name).strip().lower().replace("-", "_")


def reject_secret_fields(
    value: Any,
    path: str = "payload",
    *,
    allowed_fields: Iterable[str] = (),
) -> None:
    """Reject dictionaries containing raw-secret field names.

    The boundary is intentionally key based: Seed must not accept payload slots
    named like raw secret carriers. References to external secret systems should
    use explicit ``*_ref`` fields such as ``external_vault_token_ref`` instead of
    raw ``token`` fields.
    """

    allowed = {normalize_field_name(field) for field in allowed_fields}
    _reject_secret_fields(value, path, allowed)


def _reject_secret_fields(value: Any, path: str, allowed_fields: set[str]) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized_key = normalize_field_name(key)
            child_path = f"{path}.{key}"
            if (
                normalized_key in SECRET_FIELD_NAMES
                and normalized_key not in allowed_fields
            ):
                raise ValueError(f"secret field is not allowed in {path}: {key}")
            _reject_secret_fields(nested, child_path, allowed_fields)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _reject_secret_fields(nested, f"{path}[{index}]", allowed_fields)
