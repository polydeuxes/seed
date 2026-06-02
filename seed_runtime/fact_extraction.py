"""Extract provenance evidence from completed tool calls."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.events import EventLedger
from seed_runtime.evidence import Evidence
from seed_runtime.ids import new_id
from seed_runtime.models import Event
from seed_runtime.serialization import to_plain


@dataclass(frozen=True)
class FactExtractionResult:
    """Events appended while extracting observations from a source event."""

    events: list[Event]


class FactExtractionError(ValueError):
    """Raised when an event cannot be used for fact extraction."""


class FactExtractionService:
    """Turn completed tool calls into evidence observations.

    The generic service records tool output as evidence only. It intentionally does
    not infer facts unless a future explicit mapping is added.
    """

    def __init__(self, ledger: EventLedger) -> None:
        self.ledger = ledger

    def observe_tool_result(self, event: Event) -> FactExtractionResult:
        """Append evidence for a ``tool.call.completed`` event."""
        if event.kind != "tool.call.completed":
            raise FactExtractionError("can only extract facts from tool.call.completed")

        tool_name = self._tool_name(event.payload)
        evidence = Evidence(
            id=new_id("evd"),
            workspace_id=event.workspace_id,
            source=f"tool:{tool_name}",
            kind="tool.output",
            observed_at=event.timestamp,
            payload=event.payload.get("output", {}),
            confidence=1.0,
        )
        evidence_event = self.ledger.append(
            "evidence.observed",
            event.workspace_id,
            {"evidence": to_plain(evidence)},
            actor="system",
            session_id=event.session_id,
            causation_id=event.id,
            correlation_id=event.correlation_id,
        )
        return FactExtractionResult(events=[evidence_event])

    def _tool_name(self, payload: dict[str, Any]) -> str:
        tool_name = payload.get("tool")
        if not isinstance(tool_name, str) or not tool_name:
            raise FactExtractionError("tool.call.completed payload requires tool")
        return tool_name


# Backward-compatible name for callers that used the earlier extractor class.
ToolResultFactExtractor = FactExtractionService
