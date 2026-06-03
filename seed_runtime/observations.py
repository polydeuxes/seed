"""Observation ingestion models and Fact conversion pipeline."""

from __future__ import annotations

from datetime import datetime
from importlib.util import find_spec
from typing import TYPE_CHECKING, Any, Literal

from seed_runtime.base import SeedModel
from seed_runtime.evidence import Evidence
from seed_runtime.facts import Fact, FactSourceType
from seed_runtime.ids import new_id
from seed_runtime.secrets import reject_secret_fields
from seed_runtime.serialization import to_plain

if TYPE_CHECKING:
    from seed_runtime.events import EventLedger

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field

ObservationSourceType = Literal[
    "user", "discovery", "provider", "imported", "inferred"
]


class Observation(SeedModel):
    """Canonical external observation that can be converted into a Fact."""

    def __init__(self, **data: Any) -> None:
        reject_secret_fields(data, "observation")
        data.setdefault("metadata", {})
        confidence = float(data.get("confidence", 1.0))
        if confidence < 0.0 or confidence > 1.0:
            raise ValueError("observation.confidence must be between 0.0 and 1.0")
        data["confidence"] = confidence
        super().__init__(**data)

    id: str
    source_type: ObservationSourceType
    observed_at: datetime
    subject: str
    predicate: str
    value: Any
    confidence: float = 1.0
    metadata: dict[str, Any] = Field(default_factory=dict)
    expires_at: datetime | None = None


class ObservationIngestor:
    """Append observations and derived facts while preserving provenance."""

    def __init__(self, ledger: "EventLedger") -> None:
        self.ledger = ledger

    def ingest(
        self,
        observation: Observation,
        workspace_id: str = "default",
        *,
        actor: str = "system",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> Fact:
        """Record an observation, evidence, and the derived observed Fact."""

        evidence = self.observation_to_evidence(observation, workspace_id)
        fact = self.observation_to_fact(observation, evidence)
        event_metadata = {
            "observation_id": observation.id,
            "source_type": observation.source_type,
        }
        self.ledger.append(
            "observation.observed",
            workspace_id,
            {"observation": to_plain(observation)},
            actor=actor,  # type: ignore[arg-type]
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        evidence_event = self.ledger.append(
            "evidence.observed",
            workspace_id,
            {"evidence": to_plain(evidence), **event_metadata},
            actor=actor,  # type: ignore[arg-type]
            session_id=session_id,
            causation_id=causation_id or observation.id,
            correlation_id=correlation_id,
        )
        fact_event_kind = "fact.inferred" if fact.inferred else "fact.observed"
        self.ledger.append(
            fact_event_kind,
            workspace_id,
            {"fact": to_plain(fact), **event_metadata},
            actor=actor,  # type: ignore[arg-type]
            session_id=session_id,
            causation_id=causation_id or evidence_event.id,
            correlation_id=correlation_id,
        )
        return fact

    @staticmethod
    def observation_to_evidence(
        observation: Observation, workspace_id: str = "default"
    ) -> Evidence:
        """Convert an Observation into provenance Evidence."""

        return Evidence(
            id=new_id("evd_obs"),
            workspace_id=workspace_id,
            source=f"observation:{observation.source_type}",
            kind="observation",
            observed_at=observation.observed_at,
            payload={
                "observation_id": observation.id,
                "source_type": observation.source_type,
                "subject": observation.subject,
                "predicate": observation.predicate,
                "value": observation.value,
                "metadata": dict(observation.metadata),
                "expires_at": observation.expires_at.isoformat()
                if observation.expires_at is not None
                else None,
            },
            confidence=observation.confidence,
        )

    @staticmethod
    def observation_to_fact(observation: Observation, evidence: Evidence) -> Fact:
        """Convert an Observation and its Evidence into an observed Fact."""

        source_type: FactSourceType = observation.source_type
        return Fact(
            id=new_id("fact_obs"),
            subject_id=observation.subject,
            predicate=observation.predicate,
            value=observation.value,
            evidence_ids=[evidence.id],
            source_type=source_type,
            confidence=observation.confidence,
            observed_at=observation.observed_at,
            expires_at=observation.expires_at,
            inferred=observation.source_type == "inferred",
        )
