import pytest

from seed_runtime.context import DecisionInputComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.models import Decision
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import Runtime, StaticDecisionProducer
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService


def _runtime(decision_producer=None):
    ledger = EventLedger()
    registry = ToolRegistry()
    projector = StateProjector(ledger)
    runtime = Runtime(
        ledger,
        projector,
        DecisionInputComposer(registry),
        DecisionValidator(registry),
        ToolExecutor(ledger, registry, projector),
        ToolNeedService(ledger, projector),
        decision_producer=decision_producer,
    )
    return runtime, ledger


@pytest.mark.parametrize(
    "decision",
    [
        Decision(kind="answer", reason="model said", answer="authoritative answer"),
        Decision(kind="ask_question", reason="model said", question="what next?"),
        Decision(kind="refuse", reason="model refuses"),
        Decision(
            kind="request_tool",
            reason="model wants a tool",
            tool_need={
                "name": "need_shell",
                "summary": "Need shell execution",
                "capability": "shell_access",
            },
        ),
        Decision(
            kind="call_tool",
            reason="model calls",
            tool_name="echo",
            tool_arguments={"message": "hi"},
        ),
        Decision(
            kind="propose_state_patch",
            reason="model patch",
            state_patch={"ops": [{"op": "add_entity", "kind": "host", "name": "h"}]},
        ),
    ],
)
def test_model_shaped_decisions_are_inert_at_runtime_boundary(decision):
    runtime, ledger = _runtime(StaticDecisionProducer(decision))

    response = runtime.handle_user_message("ws", "ses", "free text")

    assert response.kind == "unsupported"
    assert runtime.decision_producer is None
    event_kinds = [event.kind for event in ledger.list("ws")]
    assert event_kinds == [
        "input.user_message",
        "runtime.decision_authority_unsupported",
    ]
    forbidden = {
        "model.decision.proposed",
        "response.answer",
        "response.question",
        "response.refusal",
        "tool_need.created",
        "tool.call.started",
        "tool.call.completed",
        "state.patch.rejected",
        "entity.discovered",
        "fact.observed",
        "relationship.observed",
    }
    assert forbidden.isdisjoint(event_kinds)


def test_static_decision_producer_alias_cannot_restore_decide_corridor():
    producer = StaticDecisionProducer(Decision(kind="answer", reason="r", answer="a"))
    runtime, _ledger = _runtime(producer)

    assert runtime.decision_producer is None
    with pytest.raises(RuntimeError, match="unsupported"):
        producer.decide(None)  # type: ignore[arg-type]
