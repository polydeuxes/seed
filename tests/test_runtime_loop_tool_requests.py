from seed_runtime.decision_journal import DecisionJournal
from seed_runtime.events import EventLedger
from seed_runtime.models import ToolNeed
from seed_runtime.projection_store import InMemoryProjectionStore
from seed_runtime.recommendation_ranker import RankedRecommendation
from seed_runtime.runtime_loop import Decision, RuntimeInput
from seed_runtime.runtime_loop_tool_requests import RuntimeLoopToolRequestHandler
from seed_runtime.state import State, StateProjector


class RecordingToolRecommendationService:
    def __init__(self) -> None:
        self.calls: list[tuple[ToolNeed, State]] = []

    def recommend_for(
        self, tool_need: ToolNeed, state: State
    ) -> list[RankedRecommendation]:
        self.calls.append((tool_need, state))
        return [
            RankedRecommendation(
                provider="docker_container_lifecycle",
                summary="Use Docker container lifecycle operations.",
                kind="local_cli",
                source="docker",
                risk_class="L3",
                score=50,
                reasons=["provider matches known runtime: docker"],
                reasoning=["+50 provider matches known runtime: docker"],
            ),
            RankedRecommendation(
                provider="systemctl_cli",
                summary="Use systemctl on systemd hosts.",
                kind="local_cli",
                source="systemd",
                risk_class="L3",
                score=15,
                reasons=["catalog default"],
                reasoning=["+5 catalog default priority"],
            ),
        ]


def make_handler(
    ledger: EventLedger, recommendation_service: RecordingToolRecommendationService
) -> RuntimeLoopToolRequestHandler:
    return RuntimeLoopToolRequestHandler(
        ledger=ledger,
        decision_journal=DecisionJournal(ledger),
        tool_recommendation_service=recommendation_service,
        projection_store=InMemoryProjectionStore(),
        projector=StateProjector(ledger),
    )


def test_tool_request_handler_preserves_tool_need_created_payload_shape():
    ledger = EventLedger()
    recommendation_service = RecordingToolRecommendationService()
    handler = make_handler(ledger, recommendation_service)
    input_event = ledger.append(
        "input.user_message",
        "ws_loop",
        {"text": "check service", "metadata": {}},
        actor="user",
    )

    handler.handle(
        runtime_input=RuntimeInput(workspace_id="ws_loop", user_text="check service"),
        run_id=input_event.id,
        input_event_id=input_event.id,
        context_hash="context-digest",
        decision=Decision(
            kind="request_tool",
            reason="missing capability",
            tool_need={
                "name": "Lookup Service Status",
                "summary": "Look up service status from inventory",
                "capability": "Service Status Lookup",
                "risk_hint": "L3",
                "desired_inputs": ["service_name"],
                "desired_outputs": ["service_status"],
            },
        ),
        events_appended=[input_event.id],
    )

    events = ledger.list_events("ws_loop")
    assert [event.kind for event in events] == [
        "input.user_message",
        "tool_need.created",
        "decision.recorded",
    ]
    need_payload = events[1].payload["tool_need"]
    assert set(need_payload) == {
        "id",
        "workspace_id",
        "name",
        "summary",
        "capability",
        "reason",
        "requested_by_event_id",
        "risk_hint",
        "status",
        "desired_inputs",
        "desired_outputs",
    }
    assert need_payload["id"].startswith("need_")
    assert {key: value for key, value in need_payload.items() if key != "id"} == {
        "workspace_id": "ws_loop",
        "name": "lookup_service_status",
        "summary": "Look up service status from inventory",
        "capability": "service_status_lookup",
        "reason": "missing capability",
        "requested_by_event_id": input_event.id,
        "risk_hint": "L3",
        "status": "proposed",
        "desired_inputs": ["service_name"],
        "desired_outputs": ["service_status"],
    }
    assert events[1].actor == "system"
    assert events[1].causation_id == input_event.id
    assert set(events[1].payload) == {"tool_need"}


def test_tool_request_handler_preserves_result_journal_recommendations_and_event_count():
    ledger = EventLedger()
    recommendation_service = RecordingToolRecommendationService()
    handler = make_handler(ledger, recommendation_service)
    input_event = ledger.append(
        "input.user_message",
        "ws_loop",
        {"text": "check service", "metadata": {}},
        actor="user",
    )
    events_appended = [input_event.id]

    result = handler.handle(
        runtime_input=RuntimeInput(workspace_id="ws_loop", user_text="check service"),
        run_id=input_event.id,
        input_event_id=input_event.id,
        context_hash="context-digest",
        decision=Decision(
            kind="request_tool",
            reason="missing capability",
            tool_need={
                "name": "Lookup Service Status",
                "summary": "Look up service status from inventory",
                "capability": "Service Status Lookup",
            },
        ),
        events_appended=events_appended,
    )

    events = ledger.list_events("ws_loop")
    journal = events[-1].payload["record"]
    assert result.workspace_id == "ws_loop"
    assert result.run_id == input_event.id
    assert result.decision_kind == "request_tool"
    assert result.response_text == "Recorded tool need lookup_service_status."
    assert result.events_appended == [event.id for event in events]
    assert result.events_appended is events_appended
    assert result.tool_name is None
    assert result.tool_result is None
    assert result.policy_allowed is True
    assert result.error is None
    assert result.decision_id == journal["decision_id"]
    assert result.context_hash == "context-digest"
    assert result.decision_reason == "missing capability"
    assert result.decision_outcome == "tool_requested"
    assert result.recommendations == [
        {
            "provider": "docker_container_lifecycle",
            "score": 50,
            "reasons": ["provider matches known runtime: docker"],
        },
        {
            "provider": "systemctl_cli",
            "score": 15,
            "reasons": ["catalog default"],
        },
    ]
    assert journal["decision_kind"] == "request_tool"
    assert journal["outcome"] == "tool_requested"
    assert journal["policy_allowed"] is True
    assert journal["reason"] == "missing capability"
    assert journal["context_hash"] == "context-digest"
    assert events[-1].causation_id == events[1].id
    assert events[-1].correlation_id == input_event.id
    assert [event.kind for event in events] == [
        "input.user_message",
        "tool_need.created",
        "decision.recorded",
    ]
    assert len(events) == 3
    assert len(recommendation_service.calls) == 1
    service_tool_need, service_state = recommendation_service.calls[0]
    assert service_tool_need.name == "lookup_service_status"
    assert service_tool_need.capability == "service_status_lookup"
    assert service_state.open_tool_needs[0].name == "lookup_service_status"
