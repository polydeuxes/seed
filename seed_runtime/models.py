"""Pydantic domain models for the Seed runtime."""

from __future__ import annotations

from datetime import datetime, timezone
from importlib.util import find_spec
import json
from typing import Any, Literal

from seed_runtime.base import SeedModel
from seed_runtime.capabilities import normalize_capabilities
from seed_runtime.evidence import Evidence
from seed_runtime.observations import Observation
from seed_runtime.facts import (
    Fact,
    FactConflict,
    FactSupport,
    StaleFactRefreshRecommendation,
)
from seed_runtime.secrets import (
    SECRET_FIELD_NAMES,
    normalize_field_name,
    reject_secret_fields,
)

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field

Actor = Literal["user", "model", "system", "tool", "builder", "approver"]
GoalStatus = Literal["active", "blocked", "complete", "abandoned"]
RiskClass = Literal["L1", "L2", "L3", "L4"]
HandoffBackendType = Literal["ansible", "mcp", "temporal", "manual"]


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
    actor: Actor = "system"
    timestamp: datetime = Field(default_factory=utc_now)
    payload: dict[str, Any] = Field(default_factory=dict)
    session_id: str | None = None
    causation_id: str | None = None
    correlation_id: str | None = None


class Workspace(SeedModel):
    id: str
    name: str


class Session(SeedModel):
    id: str
    workspace_id: str
    title: str | None = None


class Goal(SeedModel):
    id: str
    workspace_id: str = "default"
    summary: str
    status: GoalStatus = "active"
    created_from_event_id: str | None = None
    facts: dict[str, Any] = Field(default_factory=dict)
    open_questions: list[str] = Field(default_factory=list)
    related_entities: list[str] = Field(default_factory=list)


class Entity(SeedModel):
    id: str
    kind: str
    name: str
    aliases: list[str] = Field(default_factory=list)
    attributes: dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0


class ToolSpec(SeedModel):
    def __init__(self, **data: Any) -> None:
        if "capabilities" in data:
            data["capabilities"] = normalize_capabilities(data["capabilities"])
        super().__init__(**data)

    name: str
    summary: str
    toolkit_id: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    policy_action: str
    implementation: str
    status: str = "registered"
    visibility: str = "model_visible"
    risk_class: RiskClass = "L1"
    capabilities: list[str] = Field(default_factory=list)
    examples: list[dict[str, Any]] = Field(default_factory=list)


class Toolkit(SeedModel):
    id: str
    name: str
    summary: str
    tools: list[ToolSpec]
    status: str = "registered"
    source: str = "core"


class Approval(SeedModel):
    id: str
    action: str
    scope: str
    approved_by: str
    expires_at: datetime | None = None
    constraints: dict[str, Any] = Field(default_factory=dict)
