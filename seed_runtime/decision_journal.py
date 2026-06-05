"""Append-only decision journal events for RuntimeLoop v1.

DecisionJournal does not own a mutable store.  It formats decision audit records
and appends them to EventLedger so the ledger remains the source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime
import hashlib
import json
from typing import Any, Literal

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.models import Event, utc_now
from seed_runtime.serialization import to_plain
from seed_runtime.state import State

DecisionOutcome = Literal[
    "answered",
    "tool_succeeded",
    "tool_failed",
    "tool_unknown",
    "policy_denied",
    "malformed_decision",
    "tool_requested",
]


@dataclass(frozen=True)
class DecisionRecord:
    decision_id: str
    run_id: str
    workspace_id: str
    decision_kind: str | None
    reason: str
    context_hash: str
    selected_tool_name: str | None
    selected_tool_args: dict[str, Any]
    policy_allowed: bool
    outcome: DecisionOutcome
    error: str | None
    created_at: datetime


class DecisionJournal:
    """Append decision reasoning and outcome records to the EventLedger."""

    event_kind = "decision.recorded"

    def __init__(self, ledger: EventLedger) -> None:
        self.ledger = ledger

    def append_record(
        self,
        *,
        workspace_id: str,
        run_id: str,
        decision_kind: str | None,
        reason: str = "",
        context_hash: str,
        selected_tool_name: str | None = None,
        selected_tool_args: dict[str, Any] | None = None,
        policy_allowed: bool,
        outcome: DecisionOutcome,
        error: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> Event:
        record = DecisionRecord(
            decision_id=new_id("dec"),
            run_id=run_id,
            workspace_id=workspace_id,
            decision_kind=decision_kind,
            reason=reason,
            context_hash=context_hash,
            selected_tool_name=selected_tool_name,
            selected_tool_args=to_plain(selected_tool_args or {}),
            policy_allowed=policy_allowed,
            outcome=outcome,
            error=error,
            created_at=utc_now(),
        )
        return self.ledger.append(
            self.event_kind,
            workspace_id,
            {"record": to_plain(record)},
            actor="system",
            causation_id=causation_id,
            correlation_id=correlation_id,
        )


def context_hash(context: object) -> str:
    """Return a deterministic hash of RuntimeContext-like content."""
    payload = context_hash_payload(context)
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def context_hash_payload(context: object) -> dict[str, Any]:
    """Build JSON-stable context content representing what the provider saw."""
    return {
        "workspace_id": getattr(context, "workspace_id", None),
        "run_id": getattr(context, "run_id", None),
        "current_input": _json_stable(getattr(context, "current_input", None)),
        "tools": _json_stable(getattr(context, "tools", None)),
        "state": _state_hash_payload(getattr(context, "state", None)),
    }


def _state_hash_payload(state: object) -> Any:
    if not isinstance(state, State):
        return _json_stable(state)

    skipped = {"predicate_catalog", "alias_resolver"}
    payload: dict[str, Any] = {"workspace_id": state.workspace_id}
    for field_info in fields(state):
        name = field_info.name
        if name in skipped or name == "workspace_id":
            continue
        payload[name] = _json_stable(getattr(state, name))
    return payload


def _json_stable(value: Any) -> Any:
    plain = to_plain(value)
    if plain is None or isinstance(plain, str | int | float | bool):
        return plain
    if isinstance(plain, datetime):
        return plain.isoformat()
    if isinstance(plain, dict):
        return {str(key): _json_stable(plain[key]) for key in sorted(plain, key=str)}
    if isinstance(plain, tuple | list):
        return [_json_stable(item) for item in plain]
    if is_dataclass(plain):
        return _json_stable(to_plain(plain))
    return repr(plain)
