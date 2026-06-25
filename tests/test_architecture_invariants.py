from __future__ import annotations

from pathlib import Path

from seed_runtime.capability_catalog import (
    CapabilityCatalog,
    CapabilityCatalogEntry,
    CapabilityRecommendation,
)
from seed_runtime.context import DecisionInputComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.models import Decision, RuntimeResponse, ToolNeed
from seed_runtime.projection_store import ProjectionStore
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import StaticDecisionProducer, Runtime
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService


class FailingToolExecutor:
    def execute(self, *args, **kwargs):  # pragma: no cover - invariant guard
        raise AssertionError("request_tool must not execute registered operations")


class RecordingToolExecutor:
    def __init__(self) -> None:
        self.calls: list[tuple[tuple[object, ...], dict[str, object]]] = []

    def execute(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return RuntimeResponse(kind="tool_result", message="executed", payload={})


def _runtime_for_decision(decision: Decision, tool_executor: object) -> Runtime:
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    projector = StateProjector(ledger)
    return Runtime(
        ledger,
        projector,
        DecisionInputComposer(registry),
        DecisionValidator(registry),
        tool_executor,  # type: ignore[arg-type]
        ToolNeedService(ledger, projector),
        StaticDecisionProducer(decision),
        capability_catalog=CapabilityCatalog.load("capability_catalog"),
    )


def test_runtime_loop_module_is_absent_from_seed_runtime():
    assert not Path("seed_runtime/runtime_loop.py").exists()
    assert not list(Path("seed_runtime").glob("**/runtime_loop.py"))


def test_request_tool_records_capability_need_without_calling_tool_executor():
    runtime = _runtime_for_decision(
        Decision(
            kind="request_tool",
            reason="missing weather capability",
            tool_need={
                "name": "weather_lookup",
                "summary": "Look up the current weather for a location",
                "capability": "weather_lookup",
            },
        ),
        FailingToolExecutor(),
    )

    response = runtime.handle_user_message("ws", "ses", "what is the weather?")

    assert response.kind == "tool_need"
    assert response.payload["tool_need"]["capability"] == "weather_lookup"


def test_call_tool_is_the_runtime_path_that_invokes_tool_executor():
    executor = RecordingToolExecutor()
    runtime = _runtime_for_decision(
        Decision(
            kind="call_tool",
            reason="user asked to echo",
            tool_name="echo",
            tool_arguments={"message": "hello"},
        ),
        executor,
    )

    response = runtime.handle_user_message("ws", "ses", "echo hello")

    assert response.kind == "tool_result"
    assert len(executor.calls) == 1
    args, kwargs = executor.calls[0]
    assert args[:4] == ("ws", "ses", "echo", {"message": "hello"})
    assert "causation_id" in kwargs


def test_capability_recommendation_operation_is_handoff_metadata_not_registered_operation():
    catalog = CapabilityCatalog(
        [
            CapabilityCatalogEntry(
                capability="ssh_access",
                summary="SSH access metadata",
                recommendations=[
                    CapabilityRecommendation(
                        provider="ops_handoff",
                        summary="Ask an operator to verify SSH reachability.",
                        backend_type="manual",
                        operation="verify_ssh_access",
                    )
                ],
            )
        ]
    )
    registry = ToolRegistry()
    ledger = EventLedger()
    service = ToolNeedService(ledger, StateProjector(ledger))
    need = ToolNeed(
        id="need_ssh",
        name="ssh_access",
        summary="Need SSH access",
        capability="ssh_access",
        reason="connectivity is unknown",
    )

    resolution = service.resolve_capability(
        need,
        capability_catalog=catalog,
        tool_registry=registry,
    )

    assert resolution["known_capability"] is True
    assert resolution["registered_operations"] == []
    assert resolution["handoff_candidates"] == [
        {
            "provider": "ops_handoff",
            "backend_type": "manual",
            "operation": "verify_ssh_access",
        }
    ]


def test_projection_store_protocol_does_not_own_event_methods():
    assert "append" not in ProjectionStore.__dict__
    assert "extend" not in ProjectionStore.__dict__
    assert "list" not in ProjectionStore.__dict__
    assert "list_events" not in ProjectionStore.__dict__
    assert "get" not in ProjectionStore.__dict__


def test_event_ledgers_do_not_own_projection_snapshot_methods():
    snapshot_methods = {"load_snapshot", "save_snapshot", "clear_snapshot"}

    assert snapshot_methods.isdisjoint(EventLedger.__dict__)
    assert snapshot_methods.isdisjoint(SQLiteEventLedger.__dict__)
