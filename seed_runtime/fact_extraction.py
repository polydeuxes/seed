"""Extract provenance evidence and optional facts from tool results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.events import EventLedger
from seed_runtime.evidence import Evidence
from seed_runtime.facts import Fact
from seed_runtime.ids import new_id
from seed_runtime.models import Event
from seed_runtime.serialization import to_plain


@dataclass(frozen=True)
class FactExtractionResult:
    """Events appended while extracting state observations from a source event."""

    events: list[Event]


class FactExtractionError(ValueError):
    """Raised when an event cannot be used for fact extraction."""


class ToolResultFactExtractor:
    """Turn completed tool calls into evidence, with hooks for tool-specific facts."""

    def __init__(self, ledger: EventLedger) -> None:
        self.ledger = ledger

    def observe_tool_result(self, event: Event) -> FactExtractionResult:
        """Append evidence and optional facts for a ``tool.call.completed`` event."""
        if event.kind != "tool.call.completed":
            raise FactExtractionError("can only extract facts from tool.call.completed")

        tool_name = self._tool_name(event.payload)
        evidence = Evidence(
            id=new_id("evd"),
            workspace_id=event.workspace_id,
            source=f"tool:{tool_name}",
            kind="tool.output",
            observed_at=event.timestamp,
            payload={
                "tool": tool_name,
                "output": event.payload.get("output", {}),
                "tool_call_event_id": event.id,
            },
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

        events = [evidence_event]
        for fact in self._facts_from_evidence(evidence):
            events.append(
                self.ledger.append(
                    "fact.observed",
                    event.workspace_id,
                    {"fact": to_plain(fact)},
                    actor="system",
                    session_id=event.session_id,
                    causation_id=evidence_event.id,
                    correlation_id=event.correlation_id,
                )
            )
        return FactExtractionResult(events=events)

    def _facts_from_evidence(self, evidence: Evidence) -> list[Fact]:
        """Return tool-specific facts supported by evidence.

        The generic extractor intentionally records evidence only. Individual tools can
        add deterministic, domain-specific fact extraction rules here without changing
        the tool execution path.
        """
        return []

    def _tool_name(self, payload: dict[str, Any]) -> str:
        tool_name = payload.get("tool")
        if not isinstance(tool_name, str) or not tool_name:
            raise FactExtractionError("tool.call.completed payload requires tool")
        return tool_name
