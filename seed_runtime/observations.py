"""Observation ingestion models and Fact conversion pipeline."""

from __future__ import annotations

from datetime import datetime
from importlib.util import find_spec
from typing import TYPE_CHECKING, Any, Iterable, Literal

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

ObservationSourceType = Literal["user", "discovery", "provider", "imported", "inferred"]


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
    dimensions: dict[str, str] = Field(default_factory=dict)
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
    ) -> Fact | None:
        """Record one observation through the batch ingestion path."""

        facts = self.ingest_many(
            [observation],
            workspace_id,
            actor=actor,
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        return facts[0] if facts else None

    def ingest_many(
        self,
        observations: Iterable[Observation],
        workspace_id: str = "default",
        *,
        actor: str = "system",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> list[Fact | None]:
        """Record observations and derived events in one ledger batch.

        This batches only the persistence transaction: each observation still
        produces its own observation event, evidence event, and optional fact
        event in the same order as repeated :meth:`ingest` calls.
        """

        from seed_runtime.models import Event

        events: list[Event] = []
        facts: list[Fact | None] = []
        for observation in observations:
            evidence = self.observation_to_evidence(observation, workspace_id)
            fact = (
                None
                if _should_suppress_fact_promotion(observation)
                else self.observation_to_fact(observation, evidence)
            )
            facts.append(fact)
            event_metadata = {
                "observation_id": observation.id,
                "source_type": observation.source_type,
            }

            observation_event = Event(
                id=new_id("evt"),
                kind="observation.observed",
                workspace_id=workspace_id,
                payload={"observation": to_plain(observation)},
                actor=actor,  # type: ignore[arg-type]
                session_id=session_id,
                causation_id=causation_id,
                correlation_id=correlation_id,
            )
            evidence_event = Event(
                id=new_id("evt"),
                kind="evidence.observed",
                workspace_id=workspace_id,
                payload={"evidence": to_plain(evidence), **event_metadata},
                actor=actor,  # type: ignore[arg-type]
                session_id=session_id,
                causation_id=causation_id or observation.id,
                correlation_id=correlation_id,
            )
            events.extend([observation_event, evidence_event])
            if fact is None:
                continue
            fact_event_kind = "fact.inferred" if fact.inferred else "fact.observed"
            events.append(
                Event(
                    id=new_id("evt"),
                    kind=fact_event_kind,
                    workspace_id=workspace_id,
                    payload={"fact": to_plain(fact), **event_metadata},
                    actor=actor,  # type: ignore[arg-type]
                    session_id=session_id,
                    causation_id=causation_id or evidence_event.id,
                    correlation_id=correlation_id,
                )
            )
        if events:
            self.ledger.append_many(events)
        return facts

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
                "dimensions": dict(observation.dimensions),
                "expires_at": (
                    observation.expires_at.isoformat()
                    if observation.expires_at is not None
                    else None
                ),
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
            dimensions=dict(observation.dimensions),
            evidence_ids=[evidence.id],
            source_type=source_type,
            confidence=observation.confidence,
            observed_at=observation.observed_at,
            expires_at=observation.expires_at,
            inferred=observation.source_type == "inferred",
        )


def _should_suppress_fact_promotion(observation: Observation) -> bool:
    return (
        observation.metadata.get("fact_promotion_suppressed") is True
        and observation.metadata.get("source_name") == "prometheus"
        and observation.metadata.get("prometheus_metric") == "node_uname_info"
        and observation.predicate == "os"
    )
