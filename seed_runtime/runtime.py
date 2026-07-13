"""Seed runtime input boundary without internal LLM decision authority."""

from __future__ import annotations

from typing import Protocol

from seed_runtime.capability_catalog import CapabilityCatalog
from seed_runtime.context import DecisionInputComposer, DecisionInputPacket
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.models import Decision, RuntimeResponse
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService


class DecisionProducer(Protocol):
    """Legacy import-only protocol for pre-excision callers.

    Runtime no longer consumes this protocol. Implementations may still exist as
    external adapters, but passing one to Runtime cannot restore movement.
    """

    def decide(self, decision_input: DecisionInputPacket) -> Decision: ...


class StaticDecisionProducer:
    """Legacy inert test helper retained only as compatibility residue.

    Calling ``decide`` is unsupported because model-shaped Decisions no longer
    have internal runtime authority.
    """

    def __init__(self, decision: Decision) -> None:
        self.decision = decision
        self.last_decision_input: DecisionInputPacket | None = None

    def decide(self, decision_input: DecisionInputPacket) -> Decision:
        self.last_decision_input = decision_input
        raise RuntimeError(
            "DecisionProducer.decide is unsupported: model-shaped Decisions are not Seed authority"
        )


class Runtime:
    __seed_arch__ = {
        "owner": "runtime_input_boundary",
        "layer": "runtime",
        "summary": "Records user input and refuses to route model-produced Decisions as Seed authority.",
        "routes": [],
        "edges": [
            {
                "to": "StateProjector",
                "label": "projects current state for deterministic callers",
            }
        ],
        "events": ["input.user_message", "runtime.decision_authority_unsupported"],
    }

    def __init__(
        self,
        ledger: EventLedger,
        projector: StateProjector,
        decision_input_composer: DecisionInputComposer,
        decision_validator: DecisionValidator,
        tool_executor: ToolExecutor,
        tool_need_service: ToolNeedService,
        decision_producer: DecisionProducer | None = None,
        capability_catalog: CapabilityCatalog | None = None,
        max_decision_retries: int = 0,
    ) -> None:
        self.ledger = ledger
        self.projector = projector
        self.decision_input_composer = decision_input_composer
        self.decision_validator = decision_validator
        self.tool_executor = tool_executor
        self.tool_need_service = tool_need_service
        self.capability_catalog = capability_catalog or CapabilityCatalog.load()
        self.decision_producer = None
        self.max_decision_retries = 0

    def handle_user_message(
        self, workspace_id: str, session_id: str, text: str
    ) -> RuntimeResponse:
        input_event = self.ledger.append(
            "input.user_message",
            workspace_id,
            {"text": text},
            actor="user",
            session_id=session_id,
        )
        self.ledger.append(
            "runtime.decision_authority_unsupported",
            workspace_id,
            {
                "reason": "LLM/model-produced Decisions are external grammar and cannot route Seed runtime movement.",
                "removed_boundary": "DecisionProducer.decide -> Runtime._route",
            },
            actor="system",
            session_id=session_id,
            causation_id=input_event.id,
        )
        return RuntimeResponse(
            kind="unsupported",
            message="No Seed-owned runtime decision authority is configured for free-text input.",
            payload={
                "reason": "model_decision_authority_excised",
                "input_event_id": input_event.id,
            },
        )
