"""Golden-case evaluation harness for model decision contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from seed_runtime.context import ContextComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.models import Decision, Event
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import DecisionModel
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


@dataclass(frozen=True)
class EvalExpectation:
    """Expected high-level decision properties for one eval case."""

    kind: str
    tool_name: str | None = None
    tool_need_name: str | None = None


@dataclass(frozen=True)
class EvalCase:
    name: str
    user_message: str
    expected: EvalExpectation
    workspace_id: str = "ws_eval"
    session_id: str = "ses_eval"
    seed_events: tuple[Event, ...] = ()


@dataclass(frozen=True)
class EvalResult:
    case_name: str
    passed: bool
    decision: Decision
    errors: list[str] = field(default_factory=list)
    validation_errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class EvalRun:
    results: list[EvalResult]

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results)

    @property
    def pass_rate(self) -> float:
        if not self.results:
            return 1.0
        passed = sum(1 for result in self.results if result.passed)
        return passed / len(self.results)


class DecisionEvaluator:
    """Evaluate a DecisionModel against deterministic golden cases."""

    def __init__(self, registry: ToolRegistry, model: DecisionModel) -> None:
        self.registry = registry
        self.model = model

    def evaluate(self, cases: Iterable[EvalCase]) -> EvalRun:
        return EvalRun([self.evaluate_case(case) for case in cases])

    def evaluate_case(self, case: EvalCase) -> EvalResult:
        ledger = EventLedger()
        ledger.extend(case.seed_events)
        projector = StateProjector(ledger)
        input_event = ledger.append(
            "input.user_message",
            case.workspace_id,
            {"text": case.user_message},
            actor="user",
            session_id=case.session_id,
        )
        state = projector.project(case.workspace_id)
        context = ContextComposer(self.registry).compose(case.workspace_id, case.session_id, input_event, state)
        decision = self.model.decide(context)
        validation = DecisionValidator(self.registry).validate(decision, state)
        errors = list(validation.errors)
        if decision.kind != case.expected.kind:
            errors.append(f"expected kind {case.expected.kind!r}, got {decision.kind!r}")
        if case.expected.tool_name is not None and decision.tool_name != case.expected.tool_name:
            errors.append(f"expected tool {case.expected.tool_name!r}, got {decision.tool_name!r}")
        if case.expected.tool_need_name is not None:
            actual = (decision.tool_need or {}).get("name")
            if actual != case.expected.tool_need_name:
                errors.append(f"expected tool need {case.expected.tool_need_name!r}, got {actual!r}")
        return EvalResult(
            case_name=case.name,
            passed=not errors,
            decision=decision,
            errors=errors,
            validation_errors=list(validation.errors),
        )

    def record_run(self, ledger: EventLedger, workspace_id: str, run: EvalRun) -> None:
        ledger.append(
            "eval.run.completed",
            workspace_id,
            {"passed": run.passed, "pass_rate": run.pass_rate, "results": to_plain(run.results)},
            actor="system",
        )
