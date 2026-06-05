"""Read-only RuntimeLoop trace reconstruction from append-only events."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Protocol

from seed_runtime.base import SeedModel
from seed_runtime.models import Event
from seed_runtime.serialization import to_plain


class EventReader(Protocol):
    """Minimal read-only event API required by runtime tracing."""

    def list(self, workspace_id: str | None = None) -> list[Event]: ...


class RuntimeTraceEvent(SeedModel):
    """A read-only event snapshot included in a runtime trace."""

    event_id: str
    event_type: str
    created_at: datetime
    payload: dict[str, Any]


class RuntimeTrace(SeedModel):
    """Read-only reconstruction of what happened during one runtime run."""

    run_id: str
    workspace_id: str
    user_input_event: RuntimeTraceEvent | None = None
    decision_record: dict[str, Any] | None = None
    policy_event: RuntimeTraceEvent | None = None
    tool_event: RuntimeTraceEvent | None = None
    assistant_event: RuntimeTraceEvent | None = None
    error_events: list[RuntimeTraceEvent]
    events: list[RuntimeTraceEvent]
    summary: dict[str, Any]


class RuntimeTraceReader:
    """Reconstruct a single RuntimeLoop run without replaying or mutating it."""

    def __init__(self, ledger: EventReader) -> None:
        self.ledger = ledger

    def trace(self, workspace_id: str, run_id: str) -> RuntimeTrace:
        """Return the ordered trace for ``run_id`` in ``workspace_id``."""
        events = [_snapshot(event) for event in self._matching_events(workspace_id, run_id)]
        user_input_event = _first_event(events, "input.user_message")
        decision_event = _first_event(events, "decision.recorded")
        decision_record = _decision_record(decision_event)
        policy_event = _first_event(events, "runtime.policy.denied")
        tool_event = _first_event(
            events,
            "tool.result",
            "tool.failure",
            "runtime.tool.unknown",
            "runtime.tool.handler_missing",
        )
        assistant_event = _first_event(events, "assistant.answer")
        error_events = [event for event in events if _is_error_event(event)]
        return RuntimeTrace(
            run_id=run_id,
            workspace_id=workspace_id,
            user_input_event=user_input_event,
            decision_record=decision_record,
            policy_event=policy_event,
            tool_event=tool_event,
            assistant_event=assistant_event,
            error_events=error_events,
            events=events,
            summary=_summary(
                run_id=run_id,
                user_input_event=user_input_event,
                decision_record=decision_record,
                policy_event=policy_event,
                tool_event=tool_event,
                assistant_event=assistant_event,
                error_events=error_events,
                found=bool(events),
            ),
        )

    def _matching_events(self, workspace_id: str, run_id: str) -> list[Event]:
        return [
            event
            for event in self.ledger.list(workspace_id)
            if _belongs_to_run(event, run_id)
        ]


def load_runtime_trace(ledger: EventReader, workspace_id: str, run_id: str) -> RuntimeTrace:
    """Load a read-only runtime trace from an EventLedger-like reader."""
    return RuntimeTraceReader(ledger).trace(workspace_id, run_id)


# Friendly aliases for tests and future callers.
build_runtime_trace = load_runtime_trace
get_runtime_trace = load_runtime_trace


def _belongs_to_run(event: Event, run_id: str) -> bool:
    if event.id == run_id:
        return True
    if event.causation_id == run_id or event.correlation_id == run_id:
        return True
    payload = event.payload
    if payload.get("run_id") == run_id:
        return True
    record = payload.get("record")
    return isinstance(record, dict) and record.get("run_id") == run_id


def _snapshot(event: Event) -> RuntimeTraceEvent:
    return RuntimeTraceEvent(
        event_id=event.id,
        event_type=event.kind,
        created_at=event.timestamp,
        payload=deepcopy(to_plain(event.payload)),
    )


def _first_event(
    events: list[RuntimeTraceEvent], *event_types: str
) -> RuntimeTraceEvent | None:
    event_type_set = set(event_types)
    for event in events:
        if event.event_type in event_type_set:
            return event
    return None


def _decision_record(decision_event: RuntimeTraceEvent | None) -> dict[str, Any] | None:
    if decision_event is None:
        return None
    record = decision_event.payload.get("record")
    if not isinstance(record, dict):
        return None
    return deepcopy(record)


def _is_error_event(event: RuntimeTraceEvent) -> bool:
    if event.event_type in {
        "runtime.decision.rejected",
        "runtime.policy.denied",
        "runtime.tool.unknown",
        "runtime.tool.handler_missing",
        "tool.failure",
    }:
        return True
    if "error" in event.payload and event.payload.get("error") is not None:
        return True
    record = event.payload.get("record")
    return isinstance(record, dict) and record.get("error") is not None


def _summary(
    *,
    run_id: str,
    user_input_event: RuntimeTraceEvent | None,
    decision_record: dict[str, Any] | None,
    policy_event: RuntimeTraceEvent | None,
    tool_event: RuntimeTraceEvent | None,
    assistant_event: RuntimeTraceEvent | None,
    error_events: list[RuntimeTraceEvent],
    found: bool,
) -> dict[str, Any]:
    selected_tool = None
    if decision_record is not None:
        selected_tool = decision_record.get("selected_tool_name")
    if selected_tool is None and tool_event is not None:
        selected_tool = tool_event.payload.get("tool_name")

    error = None
    if decision_record is not None:
        error = decision_record.get("error")
    if error is None and error_events:
        error = error_events[0].payload.get("error")
        if error is None:
            record = error_events[0].payload.get("record")
            if isinstance(record, dict):
                error = record.get("error")

    return {
        "found": found,
        "run_id": run_id,
        "input_text": _payload_value(user_input_event, "text"),
        "decision_kind": None if decision_record is None else decision_record.get("decision_kind"),
        "decision_reason": None if decision_record is None else decision_record.get("reason"),
        "outcome": None if decision_record is None else decision_record.get("outcome"),
        "selected_tool": selected_tool,
        "policy_allowed": None if decision_record is None else decision_record.get("policy_allowed"),
        "policy_denied": policy_event is not None,
        "final_response_text": _payload_value(assistant_event, "text"),
        "error": error,
    }


def _payload_value(event: RuntimeTraceEvent | None, key: str) -> Any:
    if event is None:
        return None
    return event.payload.get(key)
