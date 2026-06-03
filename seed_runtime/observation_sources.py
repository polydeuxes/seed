"""Observation source adapters and collection service."""

from __future__ import annotations

from typing import Any, Protocol

from seed_runtime.facts import Fact
from seed_runtime.models import Actor
from seed_runtime.observations import (
    Observation,
    ObservationIngestor,
    ObservationSourceType,
)


class ObservationSource(Protocol):
    """Adapter interface for external systems that emit Observations.

    Sources expose stable identity and provenance type while remaining unaware of
    Seed's event ledger, state projector, and fact-ingestion internals.
    """

    name: str
    source_type: ObservationSourceType

    def collect(self) -> list[Observation]:
        """Return the observations collected by this source."""


class FakeObservationSource:
    """Simple in-memory observation source for tests and development."""

    def __init__(
        self,
        observations: list[Observation] | None = None,
        *,
        name: str = "fake",
        source_type: ObservationSourceType = "provider",
    ) -> None:
        self.name = name
        self.source_type = source_type
        self._observations = list(observations or [])

    def collect(self) -> list[Observation]:
        """Return configured observations without mutating source state."""

        return list(self._observations)


class ObservationCollectionService:
    """Collect observations from a source and ingest them through Seed events."""

    def __init__(self, ingestor: ObservationIngestor) -> None:
        self.ingestor = ingestor

    def collect(
        self,
        source: ObservationSource,
        workspace_id: str = "default",
        *,
        actor: Actor = "system",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> list[Fact]:
        """Collect and ingest all observations from a source.

        Collection and validation complete before any events are appended so a
        failing or malformed source cannot partially modify runtime state.
        """

        observations = list(source.collect())
        normalized = [
            self._normalize_observation(source, observation)
            for observation in observations
        ]

        return [
            self.ingestor.ingest(
                observation,
                workspace_id,
                actor=actor,
                session_id=session_id,
                causation_id=causation_id,
                correlation_id=correlation_id,
            )
            for observation in normalized
        ]

    @staticmethod
    def _normalize_observation(
        source: ObservationSource, observation: Any
    ) -> Observation:
        if not isinstance(observation, Observation):
            raise TypeError("observation sources must collect Observation instances")
        if observation.source_type != source.source_type:
            raise ValueError(
                "observation source_type must match its ObservationSource source_type"
            )
        metadata = {
            **dict(observation.metadata),
            "observation_source": source.name,
        }
        return observation.model_copy(update={"metadata": metadata})
