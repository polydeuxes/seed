"""Seed runtime input boundary without internal LLM decision authority."""

from __future__ import annotations

from typing import Protocol

from seed_runtime.events import EventLedger
from seed_runtime.models import RuntimeResponse
from seed_runtime.state import StateProjector


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
    ) -> None:
        self.ledger = ledger
        self.projector = projector

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
