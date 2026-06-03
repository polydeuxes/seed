"""Pydantic domain models for the Seed runtime."""

from __future__ import annotations

from datetime import datetime, timezone
from importlib.util import find_spec
from typing import Any, Literal

from seed_runtime.base import SeedModel
from seed_runtime.evidence import Evidence
from seed_runtime.facts import Fact
from seed_runtime.secrets import (
    SECRET_FREE_GRANT_METADATA_FIELDS,
    reject_secret_fields,
)

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field

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
    "answer",
    "ask_question",
    "call_tool",
    "request_tool",
    "propose_state_patch",
    "refuse",
]
PolicyOutcome = Literal["allow", "block", "require_confirmation", "require_approval"]
RiskClass = Literal["L1", "L2", "L3", "L4"]
PendingActionStatus = Literal["pending", "approved", "completed", "cancelled"]
ActionPlanStatus = Literal["proposed", "accepted", "rejected", "superseded"]


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


class Event(SeedModel):
    def __init__(self, **data: Any) -> None:
        reject_secret_fields(data.get("payload", {}), "event.payload")
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


class ToolNeed(SeedModel):
    id: str
    workspace_id: str = "default"
    name: str
    summary: str
    capability: str
    reason: str
    requested_by_event_id: str | None = None
    risk_hint: str | None = None
    status: ToolNeedStatus = "proposed"
    desired_inputs: list[str] = Field(default_factory=list)
    desired_outputs: list[str] = Field(default_factory=list)


class ActionPlan(SeedModel):
    """Durable, text-only proposal for satisfying a tool need.

    Action plans are intentionally non-executable. They do not grant approval,
    register tools, or carry callable code.
    """

    id: str
    tool_need_id: str
    provider: str
    capability: str
    summary: str
    steps: list[str]
    risk_class: RiskClass
    requires_approval: bool
    status: ActionPlanStatus = "proposed"
    rejection_reason: str | None = None
    replacement_plan_id: str | None = None
    executable: Literal[False] = False


class Decision(SeedModel):
    kind: DecisionKind
    reason: str
    answer: str | None = None
    question: str | None = None
    tool_name: str | None = None
    tool_arguments: dict[str, Any] = Field(default_factory=dict)
    tool_need: dict[str, Any] | None = None
    state_patch: dict[str, Any] | None = None


class PolicyDecision(SeedModel):
    outcome: PolicyOutcome
    action: str
    reason: str
    risk_class: RiskClass
    approval_id: str | None = None


class PendingAction(SeedModel):
    id: str
    workspace_id: str = "default"
    action: str
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    scope: str | None = None
    status: PendingActionStatus = "pending"
    created_from_event_id: str | None = None
    causation_id: str | None = None


class ToolSpec(SeedModel):
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
    examples: list[dict[str, Any]] = Field(default_factory=list)


class Toolkit(SeedModel):
    id: str
    name: str
    summary: str
    tools: list[ToolSpec]
    status: str = "registered"
    source: str = "core"


class ToolkitCandidate(SeedModel):
    id: str
    tool_need_id: str
    workspace_id: str
    artifact_path: str
    generator: str = "seed-builder-v1"
    status: str = "generated"
    validation_report_id: str | None = None


class Approval(SeedModel):
    id: str
    action: str
    scope: str
    approved_by: str
    expires_at: datetime | None = None
    constraints: dict[str, Any] = Field(default_factory=dict)


class ExecutionAuthorization(SeedModel):
    """Just-in-time authorization for one concrete execution attempt.

    The authorization binds an accepted action plan to a proposed concrete tool
    call by fingerprint. It intentionally stores only secret-free grant metadata;
    raw passwords, passphrases, tokens, private keys, and credential/session
    material must be supplied just in time by the host environment and never
    enter Seed events, models, CLI arguments, or persistent storage.
    """

    def __init__(self, **data: Any) -> None:
        reject_secret_fields(
            data,
            "execution_authorization",
            allowed_fields=SECRET_FREE_GRANT_METADATA_FIELDS,
        )
        unknown_fields = set(data) - set(type(self).__annotations__)
        if unknown_fields:
            raise ValueError(
                "execution authorization may only store secret-free grant "
                f"metadata fields: {', '.join(sorted(unknown_fields))}"
            )
        if data.get("secret_seen_by_seed", False) is not False:
            raise ValueError("execution authorization secret_seen_by_seed must be false")
        super().__init__(**data)

    id: str
    action_plan_id: str
    tool_name: str
    arguments_fingerprint: str
    granted_by: str
    expires_at: datetime
    interactive_prompt: bool = False
    ssh_agent: str | None = None
    sudo_timestamp: str | None = None
    external_vault_token_ref: str | None = None
    secret_seen_by_seed: Literal[False] = False


class RuntimeResponse(SeedModel):
    kind: str
    message: str
    payload: dict[str, Any] = Field(default_factory=dict)
