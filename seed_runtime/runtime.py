"""Runtime loop that routes validated fake-model decisions."""

from __future__ import annotations

from dataclasses import replace
from typing import Protocol

from seed_runtime.context import ContextComposer, ContextPacket
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.model_client import DecisionParseError
from seed_runtime.models import Decision, RuntimeResponse
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService


class DecisionModel(Protocol):
    def decide(self, context: ContextPacket) -> Decision: ...


class FakeDecisionModel:
    def __init__(self, decision: Decision) -> None:
        self.decision = decision
        self.last_context: ContextPacket | None = None

    def decide(self, context: ContextPacket) -> Decision:
        self.last_context = context
        return self.decision


class Runtime:
    def __init__(
        self,
        ledger: EventLedger,
        projector: StateProjector,
        context_composer: ContextComposer,
        decision_validator: DecisionValidator,
        tool_executor: ToolExecutor,
        tool_need_service: ToolNeedService,
        model: DecisionModel,
        max_decision_retries: int = 1,
    ) -> None:
        self.ledger = ledger
        self.projector = projector
        self.context_composer = context_composer
        self.decision_validator = decision_validator
        self.tool_executor = tool_executor
        self.tool_need_service = tool_need_service
        self.model = model
        self.max_decision_retries = max(0, max_decision_retries)

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
        state = self.projector.project(workspace_id)
        context = self.context_composer.compose(
            workspace_id, session_id, input_event, state
        )
        retry_context = context
        validation_errors: list[str] = []

        for attempt in range(self.max_decision_retries + 1):
            try:
                decision = self.model.decide(retry_context)
            except DecisionParseError as exc:
                invalid_event = self.ledger.append(
                    "model.decision.parse_failed",
                    workspace_id,
                    self._decision_parse_failed_payload(exc, attempt),
                    actor="system",
                    session_id=session_id,
                    causation_id=input_event.id,
                )
                if attempt >= self.max_decision_retries:
                    return RuntimeResponse(
                        "invalid_decision",
                        "Model decision failed parsing.",
                        {"errors": [str(exc)]},
                    )

                retry_context = self._decision_parse_retry_context(
                    context, exc, attempt + 1, invalid_event.id
                )
                continue

            decision_event = self.ledger.append(
                "model.decision.proposed",
                workspace_id,
                {"decision": to_plain(decision), "attempt": attempt},
                actor="model",
                session_id=session_id,
                causation_id=input_event.id,
            )
            validation = self.decision_validator.validate(decision, state)
            if validation.ok:
                return self._route(
                    workspace_id, session_id, decision, decision_event.id
                )

            validation_errors = validation.errors
            invalid_event = self.ledger.append(
                "model.decision.invalid",
                workspace_id,
                {"errors": validation.errors, "attempt": attempt},
                actor="system",
                session_id=session_id,
                causation_id=decision_event.id,
            )
            if attempt >= self.max_decision_retries:
                break

            retry_context = self._decision_retry_context(
                context, decision, validation.errors, attempt + 1, invalid_event.id
            )

        return RuntimeResponse(
            "invalid_decision",
            "Model decision failed validation.",
            {"errors": validation_errors},
        )

    def _decision_retry_context(
        self,
        context: ContextPacket,
        invalid_decision: Decision,
        errors: list[str],
        retry_number: int,
        invalid_event_id: str,
    ) -> ContextPacket:
        return replace(
            context,
            retry_prompt={
                "instruction": "Return exactly one corrected JSON decision that satisfies the decision_schema.",
                "retry_number": retry_number,
                "max_retries": self.max_decision_retries,
                "invalid_event_id": invalid_event_id,
                "validation_errors": list(errors),
                "invalid_decision": to_plain(invalid_decision),
            },
        )

    def _decision_parse_retry_context(
        self,
        context: ContextPacket,
        exc: DecisionParseError,
        retry_number: int,
        invalid_event_id: str,
    ) -> ContextPacket:
        retry_prompt = {
            "instruction": "Your previous output was not valid strict JSON. Return only one JSON decision object matching the decision_schema, with no prose, markdown, code fences, or extra text.",
            "retry_number": retry_number,
            "max_retries": self.max_decision_retries,
            "invalid_event_id": invalid_event_id,
            "parse_error": str(exc),
        }
        failure_classification = self._parse_failure_classification(exc)
        if failure_classification is not None:
            retry_prompt["raw_failure_classification"] = failure_classification
        return replace(context, retry_prompt=retry_prompt)

    def _decision_parse_failed_payload(
        self, exc: DecisionParseError, attempt: int
    ) -> dict[str, object]:
        payload: dict[str, object] = {"attempt": attempt, "parse_error": str(exc)}
        failure_classification = self._parse_failure_classification(exc)
        if failure_classification is not None:
            payload["raw_failure_classification"] = failure_classification
        return payload

    def _parse_failure_classification(self, exc: DecisionParseError) -> object | None:
        for attribute in (
            "raw_failure_classification",
            "failure_classification",
            "classification",
        ):
            value = getattr(exc, attribute, None)
            if value is not None:
                return value
        return None

    def _route(
        self, workspace_id: str, session_id: str, decision: Decision, causation_id: str
    ) -> RuntimeResponse:
        if decision.kind == "answer":
            self.ledger.append(
                "response.answer",
                workspace_id,
                {"answer": decision.answer},
                actor="system",
                session_id=session_id,
                causation_id=causation_id,
            )
            return RuntimeResponse("answer", decision.answer or "")
        if decision.kind == "ask_question":
            self.ledger.append(
                "response.question",
                workspace_id,
                {"question": decision.question},
                actor="system",
                session_id=session_id,
                causation_id=causation_id,
            )
            return RuntimeResponse("question", decision.question or "")
        if decision.kind == "request_tool":
            need = self.tool_need_service.create_from_decision(
                workspace_id, decision, causation_id
            )
            return RuntimeResponse(
                "tool_need",
                f"Recorded tool need {need.name}.",
                {"tool_need": to_plain(need)},
            )
        if decision.kind == "call_tool":
            return self.tool_executor.execute(
                workspace_id,
                session_id,
                decision.tool_name or "",
                decision.tool_arguments,
                causation_id=causation_id,
            )
        if decision.kind == "refuse":
            self.ledger.append(
                "response.refusal",
                workspace_id,
                {"reason": decision.reason},
                actor="system",
                session_id=session_id,
                causation_id=causation_id,
            )
            return RuntimeResponse("refusal", decision.reason)
        return RuntimeResponse("unsupported", "Unsupported valid decision kind.")
