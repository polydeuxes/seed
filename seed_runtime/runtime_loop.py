"""Small deterministic RuntimeLoop v1.

This module intentionally does not call LLMs, providers, shells, subprocesses,
network clients, or generated tools.  RuntimeLoop coordinates existing Seed
boundaries: EventLedger records events, ProjectionStore caches projected State,
ToolRegistry identifies registered tools, PolicyEngine evaluates registered tool
calls, and DecisionProvider proposes deterministic decisions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, Literal

from seed_runtime.context_views import DecisionContextView, build_decision_context_view
from seed_runtime.decision_journal import DecisionJournal, context_hash
from seed_runtime.events import EventLedger
from seed_runtime.fact_extraction import FactExtractionService
from seed_runtime.ids import new_id
from seed_runtime.models import PolicyDecision, ToolNeed, ToolSpec
from seed_runtime.policy import PolicyGate
from seed_runtime.projection_store import ProjectionStore, project_state_with_cache
from seed_runtime.registry import ToolRegistry
from seed_runtime.serialization import to_plain
from seed_runtime.state import State, StateProjector
from seed_runtime.tool_needs import slugify
from seed_runtime.tool_recommendations import ToolRecommendationService

DecisionKind = Literal["answer", "call_tool", "request_tool"]


@dataclass(frozen=True)
class RuntimeInput:
    workspace_id: str
    user_text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RuntimeResult:
    workspace_id: str
    run_id: str
    decision_kind: str | None
    response_text: str | None
    events_appended: list[str]
    tool_name: str | None = None
    tool_result: dict[str, Any] | None = None
    policy_allowed: bool | None = None
    error: str | None = None
    decision_id: str | None = None
    context_hash: str | None = None
    decision_reason: str | None = None
    decision_outcome: str | None = None
    recommendations: list[dict[str, object]] = field(default_factory=list)


@dataclass(frozen=True)
class Decision:
    kind: DecisionKind
    text: str | None = None
    tool_name: str | None = None
    tool_args: dict[str, Any] = field(default_factory=dict)
    tool_need: dict[str, Any] | None = None
    reason: str = ""


@dataclass(frozen=True)
class RuntimeContext:
    workspace_id: str
    run_id: str
    state: State
    current_input: dict[str, Any]
    tools: list[dict[str, Any]]
    decision_context: DecisionContextView = field(default_factory=DecisionContextView)


class DecisionProvider(Protocol):
    def decide(self, context: RuntimeContext) -> Decision: ...


class PolicyEngine(Protocol):
    def evaluate(
        self, tool: ToolSpec, state: State, *, scope: str | None = None
    ) -> PolicyDecision: ...


class RuntimeTool(Protocol):
    def execute(self, context: RuntimeContext, arguments: dict[str, Any]) -> dict[str, Any]: ...


class FakeDecisionProvider:
    """Deterministic DecisionProvider useful for tests."""

    def __init__(self, decision: object) -> None:
        self.decision = decision
        self.last_context: RuntimeContext | None = None

    def decide(self, context: RuntimeContext) -> object:
        self.last_context = context
        return self.decision


class EchoTool:
    """Deterministic in-memory echo tool useful for RuntimeLoop tests."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def execute(
        self, context: RuntimeContext, arguments: dict[str, Any]
    ) -> dict[str, Any]:
        self.calls.append(dict(arguments))
        return {
            "ok": True,
            "message": arguments.get("message"),
            "workspace_id": context.workspace_id,
        }


class RuntimeLoop:
    """Coordinate one deterministic user-request run through Seed boundaries."""

    def __init__(
        self,
        ledger: EventLedger,
        projection_store: ProjectionStore | None,
        tool_registry: ToolRegistry,
        policy_engine: PolicyEngine | None,
        decision_provider: DecisionProvider,
        tool_handlers: Mapping[str, RuntimeTool] | None = None,
        *,
        projector: StateProjector | None = None,
        tool_recommendation_service: ToolRecommendationService | None = None,
    ) -> None:
        self.ledger = ledger
        self.projection_store = projection_store
        self.tool_registry = tool_registry
        self.policy_engine = policy_engine or PolicyGate()
        self.decision_provider = decision_provider
        self.tool_handlers = dict(tool_handlers or {})
        self.projector = projector or StateProjector(ledger)
        self.tool_recommendation_service = (
            tool_recommendation_service or ToolRecommendationService()
        )
        self.decision_journal = DecisionJournal(ledger)
        self.fact_extraction = FactExtractionService(ledger)

    def run(self, runtime_input: RuntimeInput) -> RuntimeResult:
        events_appended: list[str] = []
        input_event = self.ledger.append(
            "input.user_message",
            runtime_input.workspace_id,
            {"text": runtime_input.user_text, "metadata": dict(runtime_input.metadata)},
            actor="user",
        )
        events_appended.append(input_event.id)
        run_id = input_event.id

        state, _cache_status = project_state_with_cache(
            self.ledger,
            runtime_input.workspace_id,
            self.projection_store,
            projector=self.projector,
        )
        context = self._compose_context(runtime_input, run_id, state)
        context_digest = context_hash(context)
        proposed = self.decision_provider.decide(context)
        decision, validation_error = self._validate_decision(proposed)
        if validation_error is not None or decision is None:
            rejected_event = self.ledger.append(
                "runtime.decision.rejected",
                runtime_input.workspace_id,
                {"error": validation_error, "decision": self._safe_decision_payload(proposed)},
                actor="system",
                causation_id=input_event.id,
            )
            events_appended.append(rejected_event.id)
            journal_event = self.decision_journal.append_record(
                workspace_id=runtime_input.workspace_id,
                run_id=run_id,
                decision_kind=self._safe_decision_payload(proposed).get("kind"),
                reason=self._safe_decision_payload(proposed).get("reason", ""),
                context_hash=context_digest,
                selected_tool_name=self._safe_decision_payload(proposed).get("tool_name"),
                selected_tool_args=self._safe_decision_payload(proposed).get("tool_args", {}),
                policy_allowed=False,
                outcome="malformed_decision",
                error=validation_error,
                causation_id=rejected_event.id,
                correlation_id=input_event.id,
            )
            events_appended.append(journal_event.id)
            record = journal_event.payload["record"]
            return RuntimeResult(
                workspace_id=runtime_input.workspace_id,
                run_id=run_id,
                decision_kind=None,
                response_text=None,
                events_appended=events_appended,
                policy_allowed=False,
                error=validation_error,
                decision_id=record["decision_id"],
                context_hash=context_digest,
                decision_reason=record["reason"],
                decision_outcome="malformed_decision",
            )

        if decision.kind == "answer":
            answer_event = self.ledger.append(
                "assistant.answer",
                runtime_input.workspace_id,
                {"text": decision.text, "reason": decision.reason},
                actor="system",
                causation_id=input_event.id,
            )
            events_appended.append(answer_event.id)
            journal_event = self.decision_journal.append_record(
                workspace_id=runtime_input.workspace_id,
                run_id=run_id,
                decision_kind="answer",
                reason=decision.reason,
                context_hash=context_digest,
                policy_allowed=True,
                outcome="answered",
                causation_id=answer_event.id,
                correlation_id=input_event.id,
            )
            events_appended.append(journal_event.id)
            record = journal_event.payload["record"]
            return RuntimeResult(
                workspace_id=runtime_input.workspace_id,
                run_id=run_id,
                decision_kind="answer",
                response_text=decision.text,
                events_appended=events_appended,
                policy_allowed=True,
                decision_id=record["decision_id"],
                context_hash=context_digest,
                decision_reason=decision.reason,
                decision_outcome="answered",
            )

        if decision.kind == "request_tool":
            return self._run_request_tool_decision(
                runtime_input,
                run_id,
                input_event.id,
                context_digest,
                decision,
                events_appended,
            )

        return self._run_tool_decision(
            runtime_input,
            run_id,
            input_event.id,
            state,
            context,
            context_digest,
            decision,
            events_appended,
        )

    def _run_request_tool_decision(
        self,
        runtime_input: RuntimeInput,
        run_id: str,
        input_event_id: str,
        context_digest: str,
        decision: Decision,
        events_appended: list[str],
    ) -> RuntimeResult:
        tool_need = self._build_tool_need(
            runtime_input.workspace_id, decision, input_event_id
        )
        need_event = self.ledger.append(
            "tool_need.created",
            runtime_input.workspace_id,
            {"tool_need": to_plain(tool_need)},
            actor="system",
            causation_id=input_event_id,
        )
        events_appended.append(need_event.id)
        recommendation_state, _cache_status = project_state_with_cache(
            self.ledger,
            runtime_input.workspace_id,
            self.projection_store,
            projector=self.projector,
        )
        recommendations = [
            {
                "provider": recommendation.provider,
                "score": recommendation.score,
                "reasons": list(recommendation.reasons),
            }
            for recommendation in self.tool_recommendation_service.recommend_for(
                tool_need, recommendation_state
            )
        ]
        journal_event = self.decision_journal.append_record(
            workspace_id=runtime_input.workspace_id,
            run_id=run_id,
            decision_kind="request_tool",
            reason=decision.reason,
            context_hash=context_digest,
            policy_allowed=True,
            outcome="tool_requested",
            causation_id=need_event.id,
            correlation_id=input_event_id,
        )
        events_appended.append(journal_event.id)
        record = journal_event.payload["record"]
        return RuntimeResult(
            workspace_id=runtime_input.workspace_id,
            run_id=run_id,
            decision_kind="request_tool",
            response_text=f"Recorded tool need {tool_need.name}.",
            events_appended=events_appended,
            policy_allowed=True,
            error=None,
            decision_id=record["decision_id"],
            context_hash=context_digest,
            decision_reason=decision.reason,
            decision_outcome="tool_requested",
            recommendations=recommendations,
        )

    def _build_tool_need(
        self, workspace_id: str, decision: Decision, requested_by_event_id: str
    ) -> ToolNeed:
        payload = decision.tool_need or {}
        name = slugify(str(payload["name"]))
        capability = slugify(str(payload["capability"]))
        return ToolNeed(
            id=new_id("need"),
            workspace_id=workspace_id,
            name=name,
            summary=str(payload["summary"]),
            capability=capability,
            reason=decision.reason,
            requested_by_event_id=requested_by_event_id,
            risk_hint=payload.get("risk_hint"),
            desired_inputs=list(payload.get("desired_inputs", [])),
            desired_outputs=list(payload.get("desired_outputs", [])),
        )

    def _run_tool_decision(
        self,
        runtime_input: RuntimeInput,
        run_id: str,
        input_event_id: str,
        state: State,
        context: RuntimeContext,
        context_digest: str,
        decision: Decision,
        events_appended: list[str],
    ) -> RuntimeResult:
        tool_name = decision.tool_name or ""
        tool = self.tool_registry.get(tool_name)
        if tool is None:
            unknown_event = self.ledger.append(
                "runtime.tool.unknown",
                runtime_input.workspace_id,
                {"tool_name": tool_name, "reason": decision.reason},
                actor="system",
                causation_id=input_event_id,
            )
            events_appended.append(unknown_event.id)
            error = f"unknown tool: {tool_name}"
            journal_event = self.decision_journal.append_record(
                workspace_id=runtime_input.workspace_id,
                run_id=run_id,
                decision_kind="call_tool",
                reason=decision.reason,
                context_hash=context_digest,
                selected_tool_name=tool_name,
                selected_tool_args=decision.tool_args,
                policy_allowed=False,
                outcome="tool_unknown",
                error=error,
                causation_id=unknown_event.id,
                correlation_id=input_event_id,
            )
            events_appended.append(journal_event.id)
            record = journal_event.payload["record"]
            return RuntimeResult(
                workspace_id=runtime_input.workspace_id,
                run_id=run_id,
                decision_kind="call_tool",
                response_text=None,
                events_appended=events_appended,
                tool_name=tool_name,
                policy_allowed=False,
                error=error,
                decision_id=record["decision_id"],
                context_hash=context_digest,
                decision_reason=decision.reason,
                decision_outcome="tool_unknown",
            )

        policy = self.policy_engine.evaluate(tool, state, scope=None)
        if policy.outcome != "allow":
            denied_event = self.ledger.append(
                "runtime.policy.denied",
                runtime_input.workspace_id,
                {
                    "tool_name": tool.name,
                    "tool_args": to_plain(decision.tool_args),
                    "policy": to_plain(policy),
                    "reason": decision.reason,
                },
                actor="system",
                causation_id=input_event_id,
            )
            events_appended.append(denied_event.id)
            error = f"policy denied tool {tool.name}: {policy.outcome}"
            journal_event = self.decision_journal.append_record(
                workspace_id=runtime_input.workspace_id,
                run_id=run_id,
                decision_kind="call_tool",
                reason=decision.reason,
                context_hash=context_digest,
                selected_tool_name=tool.name,
                selected_tool_args=decision.tool_args,
                policy_allowed=False,
                outcome="policy_denied",
                error=error,
                causation_id=denied_event.id,
                correlation_id=input_event_id,
            )
            events_appended.append(journal_event.id)
            record = journal_event.payload["record"]
            return RuntimeResult(
                workspace_id=runtime_input.workspace_id,
                run_id=run_id,
                decision_kind="call_tool",
                response_text=None,
                events_appended=events_appended,
                tool_name=tool.name,
                policy_allowed=False,
                error=error,
                decision_id=record["decision_id"],
                context_hash=context_digest,
                decision_reason=decision.reason,
                decision_outcome="policy_denied",
            )

        handler = self.tool_handlers.get(tool.name)
        if handler is None:
            missing_event = self.ledger.append(
                "runtime.tool.handler_missing",
                runtime_input.workspace_id,
                {"tool_name": tool.name},
                actor="system",
                causation_id=input_event_id,
            )
            events_appended.append(missing_event.id)
            error = f"no runtime handler registered for tool: {tool.name}"
            journal_event = self.decision_journal.append_record(
                workspace_id=runtime_input.workspace_id,
                run_id=run_id,
                decision_kind="call_tool",
                reason=decision.reason,
                context_hash=context_digest,
                selected_tool_name=tool.name,
                selected_tool_args=decision.tool_args,
                policy_allowed=True,
                outcome="tool_failed",
                error=error,
                causation_id=missing_event.id,
                correlation_id=input_event_id,
            )
            events_appended.append(journal_event.id)
            record = journal_event.payload["record"]
            return RuntimeResult(
                workspace_id=runtime_input.workspace_id,
                run_id=run_id,
                decision_kind="call_tool",
                response_text=None,
                events_appended=events_appended,
                tool_name=tool.name,
                policy_allowed=True,
                error=error,
                decision_id=record["decision_id"],
                context_hash=context_digest,
                decision_reason=decision.reason,
                decision_outcome="tool_failed",
            )

        try:
            output = handler.execute(context, dict(decision.tool_args))
        except Exception as exc:
            error = f"tool {tool.name} failed: {exc}"
            failure_event = self.ledger.append(
                "tool.failure",
                runtime_input.workspace_id,
                {"tool_name": tool.name, "error": error, "reason": decision.reason},
                actor="tool",
                causation_id=input_event_id,
            )
            events_appended.append(failure_event.id)
            journal_event = self.decision_journal.append_record(
                workspace_id=runtime_input.workspace_id,
                run_id=run_id,
                decision_kind="call_tool",
                reason=decision.reason,
                context_hash=context_digest,
                selected_tool_name=tool.name,
                selected_tool_args=decision.tool_args,
                policy_allowed=True,
                outcome="tool_failed",
                error=error,
                causation_id=failure_event.id,
                correlation_id=input_event_id,
            )
            events_appended.append(journal_event.id)
            record = journal_event.payload["record"]
            return RuntimeResult(
                workspace_id=runtime_input.workspace_id,
                run_id=run_id,
                decision_kind="call_tool",
                response_text=None,
                events_appended=events_appended,
                tool_name=tool.name,
                policy_allowed=True,
                error=error,
                decision_id=record["decision_id"],
                context_hash=context_digest,
                decision_reason=decision.reason,
                decision_outcome="tool_failed",
            )

        result_event = self.ledger.append(
            "tool.result",
            runtime_input.workspace_id,
            {"tool_name": tool.name, "output": to_plain(output), "reason": decision.reason},
            actor="tool",
            causation_id=input_event_id,
        )
        events_appended.append(result_event.id)
        evidence_result = self.fact_extraction.observe_tool_result(result_event)
        events_appended.extend(event.id for event in evidence_result.events)
        journal_event = self.decision_journal.append_record(
            workspace_id=runtime_input.workspace_id,
            run_id=run_id,
            decision_kind="call_tool",
            reason=decision.reason,
            context_hash=context_digest,
            selected_tool_name=tool.name,
            selected_tool_args=decision.tool_args,
            policy_allowed=True,
            outcome="tool_succeeded",
            causation_id=result_event.id,
            correlation_id=input_event_id,
        )
        events_appended.append(journal_event.id)
        record = journal_event.payload["record"]
        return RuntimeResult(
            workspace_id=runtime_input.workspace_id,
            run_id=run_id,
            decision_kind="call_tool",
            response_text=None,
            events_appended=events_appended,
            tool_name=tool.name,
            tool_result=output,
            policy_allowed=True,
            decision_id=record["decision_id"],
            context_hash=context_digest,
            decision_reason=decision.reason,
            decision_outcome="tool_succeeded",
        )

    def _compose_context(
        self, runtime_input: RuntimeInput, run_id: str, state: State
    ) -> RuntimeContext:
        tools = [
            {
                "name": tool.name,
                "summary": tool.summary,
                "policy_action": tool.policy_action,
                "risk_class": tool.risk_class,
            }
            for tool in self.tool_registry.list_tools(visible_only=True)
        ]
        decision_context = build_decision_context_view(state)
        return RuntimeContext(
            workspace_id=runtime_input.workspace_id,
            run_id=run_id,
            state=state,
            current_input={
                "text": runtime_input.user_text,
                "metadata": dict(runtime_input.metadata),
            },
            tools=tools,
            decision_context=decision_context,
        )

    def _validate_decision(self, proposed: object) -> tuple[Decision | None, str | None]:
        if not isinstance(proposed, Decision):
            return None, "decision provider must return a runtime_loop.Decision"
        if proposed.kind not in {"answer", "call_tool", "request_tool"}:
            return None, "decision kind must be 'answer', 'call_tool', or 'request_tool'"
        if not isinstance(proposed.reason, str):
            return None, "decision reason must be a string"
        if proposed.kind == "answer":
            if not isinstance(proposed.text, str) or proposed.text == "":
                return None, "answer decisions require non-empty text"
            if proposed.tool_name is not None or proposed.tool_args:
                return None, "answer decisions may not include tool output fields"
            if proposed.tool_need is not None:
                return None, "answer decisions may not include tool_need"
        if proposed.kind == "call_tool":
            if not isinstance(proposed.tool_name, str) or proposed.tool_name == "":
                return None, "tool decisions require a non-empty tool_name"
            if not isinstance(proposed.tool_args, dict):
                return None, "tool decisions require tool_args to be a dict"
            if proposed.text is not None:
                return None, "tool decisions may not include answer text"
            if proposed.tool_need is not None:
                return None, "tool decisions may not include tool_need"
        if proposed.kind == "request_tool":
            if not isinstance(proposed.tool_need, dict):
                return None, "request_tool decisions require tool_need dict"
            for field_name in ("name", "summary", "capability"):
                value = proposed.tool_need.get(field_name)
                if not isinstance(value, str) or value.strip() == "":
                    return None, f"request_tool decisions require non-empty {field_name}"
            if proposed.tool_name is not None or proposed.tool_args or proposed.text is not None:
                return None, "request_tool decisions may not include tool_name, tool_args, or text"
        return proposed, None

    def _safe_decision_payload(self, proposed: object) -> dict[str, Any]:
        if isinstance(proposed, Decision):
            return {
                "kind": proposed.kind,
                "text": proposed.text,
                "tool_name": proposed.tool_name,
                "tool_args": to_plain(proposed.tool_args),
                "tool_need": to_plain(proposed.tool_need),
                "reason": proposed.reason,
            }
        if isinstance(proposed, dict):
            return to_plain(proposed)
        return {"type": type(proposed).__name__}
