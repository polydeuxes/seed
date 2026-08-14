"""Event occurrence model and durable reconstruction boundary."""

from __future__ import annotations

from datetime import datetime, timezone
from importlib.util import find_spec
import json
import math
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


def _require_preservable_payload(value: Any, path: str = "payload") -> None:
    """Refuse a payload a durable store could not return unchanged.

    JSON has no tuple and no non-string key, so a durable store silently
    returned `[1, 2]` for a tuple and `{"1": ...}` for an integer key while the
    in-memory ledger returned what the caller passed. The two share an API and
    are used interchangeably, so one append yielded two different occurrences
    depending on which ledger held it, with nothing recorded to say so.

    Refused rather than coerced, and rather than declared as known loss: the
    loss is avoidable, since a caller wanting a sequence can pass a list and one
    wanting a key can pass a string. The path is reported because a tuple nested
    four levels down is otherwise a long search.

    **The boundary is JSON value identity, held by exact type.** A durable store
    returns the JSON type, so a Python subclass does not survive it: an
    `IntEnum` came back as `int`, a `str` subclass as `str`, a `list` subclass
    as `list`. Those are the same divergence a tuple caused, so they are refused
    the same way rather than the rule being stated as one thing and enforced as
    another.
    """

    # `type(...) is` throughout, not `isinstance`. A durable store returns the
    # JSON type, so an `IntEnum` came back as `int`, a `str` subclass as `str`,
    # and a `list` subclass as `list`, while the in-memory ledger returned what
    # the caller passed. That is the same divergence a tuple caused, and an
    # `isinstance` gate admitted every one of them.
    if type(value) is dict:
        for key, nested in value.items():
            if type(key) is not str:
                raise ValueError(
                    f"{path} carries a {type(key).__name__} key {key!r}; a durable "
                    "store preserves only exact string keys"
                )
            _require_preservable_payload(nested, f"{path}[{key!r}]")
        return
    if type(value) is list:
        for index, nested in enumerate(value):
            _require_preservable_payload(nested, f"{path}[{index}]")
        return
    if type(value) is tuple:
        raise ValueError(
            f"{path} carries a tuple; a durable store returns it as a list, so "
            "pass a list to preserve it exactly"
        )
    if type(value) is float and not math.isfinite(value):
        # Refused for a stronger reason than round-tripping. `NaN` never equals
        # itself so it cannot round-trip at all, and `Infinity` does only under
        # Python's own permissive encoder — neither is valid JSON, so a store
        # holding one is readable by nothing else. `#2492` was this exact
        # lesson: a durable boundary must not depend on one runtime's leniency.
        raise ValueError(
            f"{path} carries {value!r}, which is not a JSON number; a durable "
            "store could hold it only under a permissive reader"
        )
    if value is None or type(value) in (str, int, float, bool):
        return
    raise ValueError(
        f"{path} carries {type(value).__name__}, which a durable store cannot "
        "preserve exactly"
    )


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
            # Refused here rather than at the store, so both ledgers refuse the
            # same payload identically and neither serializes first. A payload
            # reconstructed from durable JSON is already preservable by
            # construction, which is what the screened form marks.
            _require_preservable_payload(payload)
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
