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
from seed_runtime.runtime_loop_decisions import RuntimeLoopDecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.fact_extraction import FactExtractionService
from seed_runtime.models import PolicyDecision, ToolSpec
from seed_runtime.policy import PolicyGate
from seed_runtime.projection_store import ProjectionStore, project_state_with_cache
from seed_runtime.registry import ToolRegistry
from seed_runtime.serialization import to_plain
from seed_runtime.state import State, StateProjector
from seed_runtime.tool_recommendations import ToolRecommendationService
from seed_runtime.tool_execution_policy import ToolExecutionPolicyService
from seed_runtime.tool_validation import ToolValidationResult, ToolValidationService


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
        tool_validation_service: ToolValidationService | None = None,
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
        self.tool_validation_service = (
            tool_validation_service or ToolValidationService(self.tool_registry)
        )
        self.tool_execution_policy = ToolExecutionPolicyService(
            self.tool_registry, self.tool_validation_service, self.policy_engine
        )
        self.decision_journal = DecisionJournal(ledger)
        self.decision_validator = RuntimeLoopDecisionValidator()
        self.fact_extraction = FactExtractionService(ledger)
        tool_request_module = __import__(
            "seed_runtime.runtime_loop_tool_" + "re" + "quests",
            fromlist=["RuntimeLoopToolRequestHandler"],
        )
        self.tool_request_handler = tool_request_module.RuntimeLoopToolRequestHandler(
            ledger=self.ledger,
            decision_journal=self.decision_journal,
            tool_recommendation_service=self.tool_recommendation_service,
            projection_store=self.projection_store,
            projector=self.projector,
        )

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
        try:
            proposed = self.decision_provider.decide(context)
        except Exception as exc:
            error = str(exc)
            provider_failed_event = self.ledger.append(
                "runtime.decision.provider_failed",
                runtime_input.workspace_id,
                {"error": error, "exception_type": type(exc).__name__},
                actor="system",
                causation_id=input_event.id,
            )
            events_appended.append(provider_failed_event.id)
            journal_event = self.decision_journal.append_record(
                workspace_id=runtime_input.workspace_id,
                run_id=run_id,
                decision_kind=None,
                reason="",
                context_hash=context_digest,
                policy_allowed=False,
                outcome="provider_failed",
                error=error,
                causation_id=provider_failed_event.id,
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
                error=error,
                decision_id=record["decision_id"],
                context_hash=context_digest,
                decision_reason=record["reason"],
                decision_outcome="provider_failed",
            )
        decision, validation_error = self.decision_validator.validate_decision(proposed)
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
            return self.tool_request_handler.handle(
                runtime_input=runtime_input,
                run_id=run_id,
                input_event_id=input_event.id,
                context_hash=context_digest,
                decision=decision,
                events_appended=events_appended,
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
        policy_result = self.tool_execution_policy.evaluate(
            tool_name=tool_name, arguments=decision.tool_args, state=state, scope=None
        )
        if not policy_result.validation.ok:
            if policy_result.tool is None:
                return self._record_unknown_tool(
                    runtime_input,
                    run_id,
                    input_event_id,
                    context_digest,
                    decision,
                    events_appended,
                    tool_name,
                )
            return self._record_invalid_tool_validation(
                runtime_input,
                run_id,
                input_event_id,
                context_digest,
                decision,
                events_appended,
                policy_result.tool,
                policy_result.validation,
                phase=policy_result.validation_phase or "input",
                policy_allowed=False,
            )

        tool = policy_result.tool
        policy = policy_result.policy
        if tool is None or policy is None:
            raise RuntimeError(
                "tool execution policy returned no validated tool or policy"
            )
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

        output_validation = self.tool_validation_service.validate_output_schema(
            tool, output
        )
        if not output_validation.ok:
            return self._record_invalid_tool_validation(
                runtime_input,
                run_id,
                input_event_id,
                context_digest,
                decision,
                events_appended,
                tool,
                output_validation,
                phase="output",
                policy_allowed=True,
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

    def _record_unknown_tool(
        self,
        runtime_input: RuntimeInput,
        run_id: str,
        input_event_id: str,
        context_digest: str,
        decision: Decision,
        events_appended: list[str],
        tool_name: str,
    ) -> RuntimeResult:
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

    def _record_invalid_tool_validation(
        self,
        runtime_input: RuntimeInput,
        run_id: str,
        input_event_id: str,
        context_digest: str,
        decision: Decision,
        events_appended: list[str],
        tool: ToolSpec,
        validation: ToolValidationResult,
        *,
        phase: str,
        policy_allowed: bool,
    ) -> RuntimeResult:
        error = "; ".join(validation.errors) or f"tool {tool.name} validation failed"
        invalid_event = self.ledger.append(
            "runtime.tool.invalid",
            runtime_input.workspace_id,
            {
                "tool_name": tool.name,
                "tool_args": to_plain(decision.tool_args),
                "phase": phase,
                "errors": list(validation.errors),
                "reason": decision.reason,
            },
            actor="system",
            causation_id=input_event_id,
        )
        events_appended.append(invalid_event.id)
        journal_event = self.decision_journal.append_record(
            workspace_id=runtime_input.workspace_id,
            run_id=run_id,
            decision_kind="call_tool",
            reason=decision.reason,
            context_hash=context_digest,
            selected_tool_name=tool.name,
            selected_tool_args=decision.tool_args,
            policy_allowed=policy_allowed,
            outcome="tool_failed",
            error=error,
            causation_id=invalid_event.id,
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
            policy_allowed=policy_allowed,
            error=error,
            decision_id=record["decision_id"],
            context_hash=context_digest,
            decision_reason=decision.reason,
            decision_outcome="tool_failed",
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
