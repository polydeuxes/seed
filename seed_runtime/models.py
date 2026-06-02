"""Domain models for the Seed runtime.

These dataclasses intentionally keep validation light and explicit. Runtime
services validate behavior at boundaries so the model layer stays portable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

Actor = Literal["user", "model", "system", "tool", "builder", "approver"]
GoalStatus = Literal["active", "blocked", "complete", "abandoned"]
ToolNeedStatus = Literal[
    "proposed",
    "accepted",
    "generating",
    "generated",
    "validating",
    "validated",
    "registered",
    "rejected",
]
DecisionKind = Literal[
    "answer", "ask_question", "call_tool", "request_tool", "propose_state_patch", "refuse"
]
PolicyOutcome = Literal["allow", "block", "require_confirmation", "require_approval"]
RiskClass = Literal["L1", "L2", "L3", "L4"]


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Event:
    id: str
    kind: str
    workspace_id: str
    actor: Actor
    timestamp: datetime
    payload: dict[str, Any] = field(default_factory=dict)
    session_id: str | None = None
    causation_id: str | None = None
    correlation_id: str | None = None


@dataclass(frozen=True)
class Workspace:
    id: str
    name: str


@dataclass(frozen=True)
class Session:
    id: str
    workspace_id: str
    title: str | None = None


@dataclass(frozen=True)
class Goal:
    id: str
    workspace_id: str
    summary: str
    status: GoalStatus = "active"
    created_from_event_id: str | None = None
    facts: dict[str, Any] = field(default_factory=dict)
    open_questions: list[str] = field(default_factory=list)
    related_entities: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Entity:
    id: str
    kind: str
    name: str
    aliases: list[str] = field(default_factory=list)
    attributes: dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0


@dataclass(frozen=True)
class Fact:
    id: str
    subject_id: str
    predicate: str
    value: Any
    source_event_id: str
    observed_at: datetime
    expires_at: datetime | None = None
    confidence: float = 1.0


@dataclass(frozen=True)
class ToolSpec:
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
    examples: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class Toolkit:
    id: str
    name: str
    summary: str
    tools: list[ToolSpec]
    status: str = "registered"
    source: str = "core"


@dataclass(frozen=True)
class ToolNeed:
    id: str
    workspace_id: str
    name: str
    summary: str
    capability: str
    reason: str
    requested_by_event_id: str | None = None
    risk_hint: str | None = None
    status: ToolNeedStatus = "proposed"
    desired_inputs: list[str] = field(default_factory=list)
    desired_outputs: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ToolkitCandidate:
    id: str
    tool_need_id: str
    workspace_id: str
    artifact_path: str
    generator: str = "seed-builder-v1"
    status: str = "generated"
    validation_report_id: str | None = None


@dataclass(frozen=True)
class Approval:
    id: str
    action: str
    scope: str
    approved_by: str
    expires_at: datetime | None = None
    constraints: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Decision:
    kind: DecisionKind
    reason: str
    answer: str | None = None
    question: str | None = None
    tool_name: str | None = None
    tool_arguments: dict[str, Any] = field(default_factory=dict)
    tool_need: dict[str, Any] | None = None
    state_patch: dict[str, Any] | None = None


@dataclass(frozen=True)
class PolicyDecision:
    outcome: PolicyOutcome
    action: str
    reason: str
    risk_class: RiskClass
    approval_id: str | None = None


@dataclass(frozen=True)
class RuntimeResponse:
    kind: str
    message: str
    payload: dict[str, Any] = field(default_factory=dict)
