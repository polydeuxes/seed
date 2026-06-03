"""Observation source adapters and collection service."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol

from seed_runtime.facts import Fact
from seed_runtime.ids import new_id
from seed_runtime.serialization import to_plain
from seed_runtime.models import Actor
from seed_runtime.observations import (
    Observation,
    ObservationIngestor,
    ObservationSourceType,
)

DEFAULT_JSON_OBSERVED_AT = datetime(1970, 1, 1)


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


class JsonObservationSource:
    """Observation source backed by a local JSON inventory file.

    The file must contain an object with an ``observations`` array. Every entry
    is validated and converted into an :class:`Observation` before any entries
    are returned, allowing callers to fail the whole ingest when one entry is
    malformed.
    """

    def __init__(
        self,
        path: str | Path,
        *,
        name: str | None = None,
        source_type: ObservationSourceType = "imported",
    ) -> None:
        self.path = Path(path)
        self.name = name or f"json:{self.path}"
        self.source_type = source_type
        self.allow_mixed_source_types = True

    def collect(self) -> list[Observation]:
        """Read, validate, and return all observations from the JSON file."""

        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"invalid JSON observation file {self.path}: {exc}"
            ) from exc
        if not isinstance(payload, dict):
            raise ValueError("JSON observation file must contain a top-level object")

        entries = payload.get("observations")
        if not isinstance(entries, list):
            raise ValueError("JSON observation file must contain an observations array")

        observations: list[Observation] = []
        for index, entry in enumerate(entries):
            observations.append(self._observation_from_entry(entry, index))
        return observations

    def _observation_from_entry(self, entry: Any, index: int) -> Observation:
        if not isinstance(entry, dict):
            raise ValueError(f"observations[{index}] must be an object")

        required_fields = ("subject", "predicate", "value")
        missing = [field for field in required_fields if field not in entry]
        if missing:
            raise ValueError(
                f"observations[{index}] missing required field(s): "
                + ", ".join(missing)
            )
        for field in ("subject", "predicate"):
            if not isinstance(entry[field], str) or not entry[field].strip():
                raise ValueError(
                    f"observations[{index}].{field} must be a non-empty string"
                )

        metadata = entry.get("metadata", {})
        if metadata is None:
            metadata = {}
        if not isinstance(metadata, dict):
            raise ValueError(f"observations[{index}].metadata must be an object")
        metadata = {**metadata, "json_path": str(self.path)}

        observed_at = (
            self._parse_datetime_field(entry, index, "observed_at")
            or DEFAULT_JSON_OBSERVED_AT
        )
        expires_at = self._parse_datetime_field(entry, index, "expires_at")

        data = {
            "id": entry.get("id") or new_id("obs_json"),
            "source_type": entry.get("source_type", self.source_type),
            "observed_at": observed_at,
            "subject": entry["subject"],
            "predicate": entry["predicate"],
            "value": entry["value"],
            "confidence": entry.get("confidence", 1.0),
            "metadata": metadata,
            "expires_at": expires_at,
        }
        if not isinstance(data["id"], str) or not data["id"].strip():
            raise ValueError(f"observations[{index}].id must be a non-empty string")
        try:
            return Observation(**data)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"observations[{index}] is malformed: {exc}") from exc

    @staticmethod
    def _parse_datetime_field(
        entry: dict[str, Any], index: int, field: str
    ) -> datetime | None:
        value = entry.get(field)
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"observations[{index}].{field} must be an ISO timestamp")
        try:
            return datetime.fromisoformat(value)
        except ValueError as exc:
            raise ValueError(
                f"observations[{index}].{field} must be an ISO timestamp"
            ) from exc


def export_observations_json(
    state: Any, *, include_inferred: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Export projected facts as a JSON observation inventory payload.

    The returned dictionary matches the ``JsonObservationSource`` input shape:
    ``{"observations": [...]}``. Each fact is represented as one observation
    entry so re-importing the payload preserves independent fact support rather
    than collapsing support into one aggregate claim. Inferred facts are omitted
    by default because they are derivable from observed facts.
    """

    facts = sorted(
        state.facts.values(),
        key=lambda fact: (
            fact.inferred,
            fact.observed_at,
            fact.subject_id,
            fact.predicate,
            fact.id,
        ),
    )
    observations: list[dict[str, Any]] = []
    for fact in facts:
        if fact.inferred and not include_inferred:
            continue
        entry = {
            "subject": fact.subject_id,
            "predicate": fact.predicate,
            "value": to_plain(fact.value),
            "source_type": fact.source_type,
            "confidence": fact.confidence,
            "observed_at": fact.observed_at.isoformat(),
        }
        if fact.expires_at is not None:
            entry["expires_at"] = fact.expires_at.isoformat()
        observations.append(entry)
    return {"observations": observations}


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
        if observation.source_type != source.source_type and not getattr(
            source, "allow_mixed_source_types", False
        ):
            raise ValueError(
                "observation source_type must match its ObservationSource source_type"
            )
        metadata = {
            **dict(observation.metadata),
            "observation_source": source.name,
        }
        return observation.model_copy(update={"metadata": metadata})
