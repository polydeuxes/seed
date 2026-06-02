"""Apply model-proposed state patches as append-only ledger events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.models import Event
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


@dataclass(frozen=True)
class StatePatchResult:
    """Result of applying a state patch."""

    events: list[Event]


class StatePatchError(ValueError):
    """Raised when a state patch cannot be applied."""


class StatePatchService:
    """Translate declarative state patch operations into ledger events."""

    def __init__(self, ledger: EventLedger, projector: StateProjector) -> None:
        self.ledger = ledger
        self.projector = projector

    def apply(
        self,
        workspace_id: str,
        state_patch: dict[str, Any],
        *,
        session_id: str | None = None,
        causation_id: str | None = None,
    ) -> StatePatchResult:
        """Apply a state patch and return the domain events that were appended."""
        events: list[Event] = []
        for operation in self._operations_from_patch(state_patch):
            event = self._apply_operation(
                workspace_id,
                operation,
                session_id=session_id,
                causation_id=causation_id,
            )
            events.append(event)
        return StatePatchResult(events=events)

    def _operations_from_patch(self, state_patch: dict[str, Any]) -> list[dict[str, Any]]:
        raw_operations = state_patch.get("ops", state_patch.get("operations"))
        if raw_operations is not None:
            if not isinstance(raw_operations, list):
                raise StatePatchError("state_patch.ops must be a list")
            return [
                self._require_mapping(item, "state_patch operation")
                for item in raw_operations
            ]

        operations: list[dict[str, Any]] = []
        for entity in state_patch.get("entities", []):
            operations.append({"op": "upsert_entity", "entity": entity})
        for evidence in state_patch.get("evidence", []):
            operations.append({"op": "observe_evidence", "evidence": evidence})
        for fact in state_patch.get("facts", []):
            operations.append({"op": "observe_fact", "fact": fact})
        for goal in state_patch.get("goals", []):
            operations.append({"op": "create_goal", "goal": goal})
        return operations

    def _apply_operation(
        self,
        workspace_id: str,
        operation: dict[str, Any],
        *,
        session_id: str | None,
        causation_id: str | None,
    ) -> Event:
        op = operation.get("op", operation.get("operation"))
        if op == "upsert_entity":
            entity = self._operation_payload(operation, "entity")
            entity.setdefault("id", new_id("ent"))
            self._require_fields(entity, "entity", "id", "kind", "name")
            return self.ledger.append(
                "entity.upserted",
                workspace_id,
                {"entity": to_plain(entity)},
                actor="system",
                session_id=session_id,
                causation_id=causation_id,
            )
        if op == "observe_evidence":
            evidence = self._operation_payload(operation, "evidence")
            evidence.setdefault("id", new_id("evd"))
            evidence.setdefault("workspace_id", workspace_id)
            self._require_fields(
                evidence, "evidence", "id", "workspace_id", "source", "kind"
            )
            evidence.setdefault("payload", {})
            evidence.setdefault("confidence", 1.0)
            return self.ledger.append(
                "evidence.observed",
                workspace_id,
                {"evidence": to_plain(evidence)},
                actor="system",
                session_id=session_id,
                causation_id=causation_id,
            )
        if op == "observe_fact":
            fact = self._operation_payload(operation, "fact")
            fact.setdefault("id", new_id("fact"))
            fact.setdefault("evidence_ids", [])
            self._require_fields(fact, "fact", "id", "subject_id", "predicate", "value")
            return self.ledger.append(
                "fact.observed",
                workspace_id,
                {"fact": to_plain(fact)},
                actor="system",
                session_id=session_id,
                causation_id=causation_id,
            )
        if op == "create_goal":
            goal = self._operation_payload(operation, "goal")
            goal.setdefault("id", new_id("goal"))
            goal.setdefault("workspace_id", workspace_id)
            goal.setdefault("status", "active")
            if causation_id is not None:
                goal.setdefault("created_from_event_id", causation_id)
            self._require_fields(goal, "goal", "id", "workspace_id", "summary")
            return self.ledger.append(
                "goal.created",
                workspace_id,
                {"goal": to_plain(goal)},
                actor="system",
                session_id=session_id,
                causation_id=causation_id,
            )
        raise StatePatchError(f"unsupported state patch op {op!r}")

    def _operation_payload(self, operation: dict[str, Any], key: str) -> dict[str, Any]:
        value = operation.get(key)
        if value is None:
            value = {k: v for k, v in operation.items() if k not in {"op", "operation"}}
        return self._require_mapping(value, key)

    def _require_mapping(self, value: Any, label: str) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise StatePatchError(f"{label} must be an object")
        return dict(value)

    def _require_fields(self, value: dict[str, Any], label: str, *fields: str) -> None:
        missing = [field for field in fields if field not in value or value[field] is None]
        if missing:
            raise StatePatchError(f"{label} missing required field(s): {', '.join(missing)}")
