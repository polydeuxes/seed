"""First-class service for missing capability requests."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.capability_catalog import CapabilityCatalog
from seed_runtime.models import Decision, ToolNeed, ToolSpec
from seed_runtime.registry import ToolRegistry
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector
from seed_runtime.capabilities import slugify


class ToolNeedService:
    def __init__(self, ledger: EventLedger, projector: StateProjector) -> None:
        self.ledger = ledger
        self.projector = projector

    def create_from_decision(
        self, workspace_id: str, decision: Decision, causation_id: str | None = None
    ) -> ToolNeed:
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

    def resolve_capability(
        self,
        tool_need: ToolNeed,
        *,
        capability_catalog: CapabilityCatalog,
        tool_registry: ToolRegistry,
        provider_recommendations: list[Any] | None = None,
    ) -> dict[str, object]:
        """Return read-only capability resolution metadata for a ToolNeed.

        Capability resolution keeps Seed's boundaries explicit: catalog entries
        describe known capabilities and non-executable provider/handoff
        suggestions, while registered operation candidates come only from the
        ToolRegistry capability lookup. This method does not execute tools,
        authorize actions, create pending actions, or mutate registry/catalog
        state.
        """
        catalog_entry = capability_catalog.get(tool_need.capability)
        recommendations = provider_recommendations
        if recommendations is None:
            recommendations = []
        catalog_recommendations = (
            list(catalog_entry.recommendations) if catalog_entry is not None else []
        )
        return {
            "known_capability": catalog_entry is not None,
            "registered_operations": [
                _registered_operation_candidate(tool)
                for tool in tool_registry.list_tools_for_capability(
                    tool_need.capability, visible_only=True
                )
            ],
            "provider_recommendations": [
                {
                    "provider": recommendation.provider,
                    "score": recommendation.score,
                    "reasons": list(recommendation.reasons),
                }
                for recommendation in recommendations
            ],
            "handoff_candidates": [
                _handoff_candidate(recommendation)
                for recommendation in catalog_recommendations
                if recommendation.backend_type is not None or recommendation.operation
            ],
        }

    def set_status(
        self,
        workspace_id: str,
        need: ToolNeed,
        status: str,
        causation_id: str | None = None,
    ) -> ToolNeed:
        updated = replace(need, status=status)  # type: ignore[arg-type]
        self.ledger.append(
            "tool_need.status_changed",
            workspace_id,
            {"tool_need_id": need.id, "status": status},
            actor="system",
            causation_id=causation_id,
        )
        return updated


def _registered_operation_candidate(tool: ToolSpec) -> dict[str, object]:
    return {
        "name": tool.name,
        "summary": tool.summary,
        "toolkit_id": tool.toolkit_id,
        "policy_action": tool.policy_action,
        "risk_class": tool.risk_class,
        "visibility": tool.visibility,
        "status": tool.status,
        "capabilities": list(tool.capabilities),
    }


def _handoff_candidate(recommendation: object) -> dict[str, object]:
    provider = getattr(recommendation, "provider")
    candidate: dict[str, object] = {"provider": provider}
    backend_type = getattr(recommendation, "backend_type", None)
    operation = getattr(recommendation, "operation", None)
    if backend_type is not None:
        candidate["backend_type"] = backend_type
    if operation:
        candidate["operation"] = operation
    return candidate
