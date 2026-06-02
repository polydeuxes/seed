"""First-class service for missing capability requests."""

from __future__ import annotations

import re
from dataclasses import replace

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.models import Decision, ToolNeed
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector

_SLUG_CHARS = re.compile(r"[^a-z0-9_]+")


def slugify(value: str) -> str:
    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    normalized = _SLUG_CHARS.sub("_", normalized).strip("_")
    return normalized or "unnamed_tool"


class ToolNeedService:
    def __init__(self, ledger: EventLedger, projector: StateProjector) -> None:
        self.ledger = ledger
        self.projector = projector

    def create_from_decision(self, workspace_id: str, decision: Decision, causation_id: str | None = None) -> ToolNeed:
        payload = decision.tool_need or {}
        name = slugify(payload["name"])
        capability = slugify(payload.get("capability", name))
        state = self.projector.project(workspace_id)
        for existing in state.open_tool_needs:
            if existing.name == name or existing.capability == capability:
                return existing
        need = ToolNeed(
            id=new_id("need"),
            workspace_id=workspace_id,
            name=name,
            capability=capability,
            summary=payload["summary"],
            reason=decision.reason,
            requested_by_event_id=causation_id,
            risk_hint=payload.get("risk_hint"),
            desired_inputs=payload.get("desired_inputs", []),
            desired_outputs=payload.get("desired_outputs", []),
        )
        self.ledger.append(
            "tool_need.created",
            workspace_id,
            {"tool_need": to_plain(need)},
            actor="system",
            causation_id=causation_id,
        )
        return need

    def set_status(self, workspace_id: str, need: ToolNeed, status: str, causation_id: str | None = None) -> ToolNeed:
        updated = replace(need, status=status)  # type: ignore[arg-type]
        self.ledger.append(
            "tool_need.status_changed",
            workspace_id,
            {"tool_need_id": need.id, "status": status},
            actor="system",
            causation_id=causation_id,
        )
        return updated
