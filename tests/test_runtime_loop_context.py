import pytest

pytestmark = pytest.mark.experimental_runtime_loop

from seed_runtime.decision_journal import context_hash
from seed_runtime.events import EventLedger
from seed_runtime.evidence import Evidence
from seed_runtime.models import Fact, ToolSpec, Toolkit, utc_now
from seed_runtime.policy import PolicyGate
from seed_runtime.projection_store import InMemoryProjectionStore
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime_loop import (
    Decision as LoopDecision,
    EchoTool,
    FakeDecisionProvider,
    RuntimeInput,
    RuntimeLoop,
)
from seed_runtime.runtime_loop_context import RuntimeLoopContextComposer
from seed_runtime.state import State
from seed_runtime.serialization import to_plain


def make_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register_toolkit(
        Toolkit(
            id="tk_context",
            name="context tools",
            summary="RuntimeLoop context tools.",
            tools=[
                ToolSpec(
                    toolkit_id="tk_context",
                    name="echo",
                    summary="Echo a message deterministically.",
                    input_schema={},
                    output_schema={},
                    policy_action="echo.run",
                    implementation="tests:echo",
                    risk_class="L1",
                ),
                ToolSpec(
                    toolkit_id="tk_context",
                    name="internal_notes",
                    summary="Internal hidden tool.",
                    input_schema={},
                    output_schema={},
                    policy_action="internal.read",
                    implementation="tests:hidden",
                    risk_class="L2",
                    visibility="internal",
                ),
            ],
        )
    )
    return registry


def make_state() -> State:
    evidence = Evidence(
        id="evd_context",
        workspace_id="ws_context",
        source="test",
        kind="user_input",
        observed_at=utc_now(),
        payload={"summary": "service-a is active"},
        confidence=1.0,
    )
    fact = Fact(
        id="fact_context",
        subject_id="service-a",
        predicate="status",
        value="active",
        evidence_ids=["evd_context"],
        observed_at=utc_now(),
        confidence=0.95,
    )
    return State(
        workspace_id="ws_context",
        last_event_id="evt_context_last",
        facts={fact.id: fact},
        observed_facts={fact.id: fact},
        evidence={evidence.id: evidence},
    )


def test_composer_preserves_current_input_shape_and_metadata_copy():
    runtime_input = RuntimeInput(
        workspace_id="ws_context",
        user_text="hello",
        metadata={"request_id": "req-1", "nested": {"trace": "abc"}},
    )
    context = RuntimeLoopContextComposer(make_registry()).compose(
        workspace_id="ws_context",
        run_id="run_context",
        runtime_input=runtime_input,
        state=make_state(),
    )

    assert context.current_input == {
        "text": "hello",
        "metadata": {"request_id": "req-1", "nested": {"trace": "abc"}},
    }
    assert list(context.current_input) == ["text", "metadata"]
    assert context.current_input["metadata"] is not runtime_input.metadata


def test_composer_visible_tool_list_shape_and_hidden_tools_excluded():
    context = RuntimeLoopContextComposer(make_registry()).compose(
        workspace_id="ws_context",
        run_id="run_context",
        runtime_input=RuntimeInput(workspace_id="ws_context", user_text="hello"),
        state=make_state(),
    )

    assert context.tools == [
        {
            "name": "echo",
            "summary": "Echo a message deterministically.",
            "policy_action": "echo.run",
            "risk_class": "L1",
        }
    ]
    assert [list(tool) for tool in context.tools] == [
        ["name", "summary", "policy_action", "risk_class"]
    ]
    assert "internal_notes" not in [tool["name"] for tool in context.tools]


def test_composer_builds_decision_context_view_from_provided_state():
    state = make_state()

    context = RuntimeLoopContextComposer(make_registry()).compose(
        workspace_id="ws_context",
        run_id="run_context",
        runtime_input=RuntimeInput(workspace_id="ws_context", user_text="status?"),
        state=state,
    )

    assert context.state is state
    assert context.decision_context.last_event_id == "evt_context_last"
    assert context.decision_context.projection_version == "v1"
    assert [fact.fact_id for fact in context.decision_context.facts] == [
        "fact_context"
    ]
    assert context.decision_context.summary.facts_count == 1


def test_runtime_loop_context_hash_remains_stable_for_unchanged_inputs():
    composer = RuntimeLoopContextComposer(make_registry())
    runtime_input = RuntimeInput(
        workspace_id="ws_context",
        user_text="hello",
        metadata={"request_id": "req-1"},
    )
    state = make_state()

    first = composer.compose(
        workspace_id="ws_context",
        run_id="run_context",
        runtime_input=runtime_input,
        state=state,
    )
    second = composer.compose(
        workspace_id="ws_context",
        run_id="run_context",
        runtime_input=runtime_input,
        state=state,
    )

    assert context_hash(first) == context_hash(second)


def test_runtime_loop_provider_receives_same_context_fields_from_composer():
    ledger = EventLedger()
    evidence = Evidence(
        id="evd_loop_context",
        workspace_id="ws_context",
        source="test",
        kind="user_input",
        observed_at=utc_now(),
        payload={"summary": "service-a is active"},
        confidence=1.0,
    )
    fact = Fact(
        id="fact_loop_context",
        subject_id="service-a",
        predicate="status",
        value="active",
        evidence_ids=["evd_loop_context"],
        observed_at=utc_now(),
        confidence=0.95,
    )
    ledger.append("evidence.observed", "ws_context", {"evidence": to_plain(evidence)})
    ledger.append("fact.observed", "ws_context", {"fact": to_plain(fact)})
    provider = FakeDecisionProvider(
        LoopDecision(kind="answer", text="done", reason="context")
    )
    runtime = RuntimeLoop(
        ledger,
        InMemoryProjectionStore(),
        make_registry(),
        PolicyGate(),
        provider,
        {"echo": EchoTool()},
    )

    result = runtime.run(
        RuntimeInput(
            workspace_id="ws_context",
            user_text="hello",
            metadata={"request_id": "req-1"},
        )
    )

    assert result.error is None
    assert provider.last_context.workspace_id == "ws_context"
    assert provider.last_context.run_id == result.run_id
    assert provider.last_context.current_input == {
        "text": "hello",
        "metadata": {"request_id": "req-1"},
    }
    assert provider.last_context.tools == [
        {
            "name": "echo",
            "summary": "Echo a message deterministically.",
            "policy_action": "echo.run",
            "risk_class": "L1",
        }
    ]
    assert provider.last_context.state.workspace_id == "ws_context"
    assert [fact.fact_id for fact in provider.last_context.decision_context.facts] == [
        "fact_loop_context"
    ]
