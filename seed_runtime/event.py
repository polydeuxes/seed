"""Event occurrence model and durable reconstruction boundary."""

from __future__ import annotations

from datetime import datetime, timezone
from importlib.util import find_spec
import json
from typing import Any

from seed_runtime.base import SeedModel
from seed_runtime.secrets import (
    SECRET_FIELD_NAMES,
    normalize_field_name,
    reject_secret_fields,
)

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


_SCREENED_EVENT_PAYLOAD_TOKEN = object()


class _ScreenedEventPayload(dict[str, Any]):
    """Runtime-local evidence that durable JSON keys were screened."""

    def __init__(self, payload: dict[str, Any], token: object) -> None:
        if token is not _SCREENED_EVENT_PAYLOAD_TOKEN:
            raise TypeError("screened Event payloads come from the durable decoder")
        super().__init__(payload)


def _screen_durable_event_object(value: dict[str, Any]) -> dict[str, Any]:
    for key in value:
        if normalize_field_name(key) in SECRET_FIELD_NAMES:
            raise ValueError(
                f"secret field is not allowed in durable event payload: {key}"
            )
    return value


def _decode_screened_event_payload(raw_payload: str) -> Any:
    """Decode durable JSON while screening each dictionary as it is built."""

    payload = json.loads(raw_payload, object_hook=_screen_durable_event_object)
    if isinstance(payload, dict):
        return _ScreenedEventPayload(payload, _SCREENED_EVENT_PAYLOAD_TOKEN)
    return payload


class Event(SeedModel):
    def __init__(self, **data: Any) -> None:
        payload = data.get("payload", {})
        if not isinstance(payload, _ScreenedEventPayload):
            reject_secret_fields(payload, "event.payload")
        super().__init__(**data)

    id: str
    kind: str
    workspace_id: str = "default"
    # Retained durable occurrence field. No closed actor grammar is established.
    actor: str = "system"
    timestamp: datetime = Field(default_factory=utc_now)
    payload: dict[str, Any] = Field(default_factory=dict)
    session_id: str | None = None
    causation_id: str | None = None
    correlation_id: str | None = None
