"""Shared normalization pipeline for observations emitted by source adapters."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from typing import Any, Protocol

from seed_runtime.observations import Observation
from seed_runtime.serialization import to_plain


class ObservationNormalizer(Protocol):
    """Derive normalized observations without mutating source observations."""

    name: str

    def normalize(self, observations: list[Observation]) -> list[Observation]:
        """Return observations derived from the supplied observations."""


class ObservationNormalizationPipeline:
    """Run normalizers in order and retain originals plus unique derivations."""

    def __init__(self, normalizers: list[ObservationNormalizer] | None = None) -> None:
        self.normalizers = list(normalizers or [])

    def normalize(self, observations: list[Observation]) -> list[Observation]:
        """Return originals followed by unique observations derived in pipeline order."""

        normalized = list(observations)
        original_ids = {observation.id for observation in observations}
        derived_keys: set[str] = set()
        for normalizer in self.normalizers:
            for derived in normalizer.normalize(list(normalized)):
                if not isinstance(derived, Observation):
                    raise TypeError(
                        "observation normalizers must return Observation instances"
                    )
                if derived.id in original_ids:
                    continue
                key = _derived_observation_key(derived)
                if key in derived_keys:
                    continue
                derived_keys.add(key)
                normalized.append(derived)
        return normalized


class EndpointAliasNormalizer:
    """Derive stable hostname-to-endpoint aliases from generic source metadata."""

    name = "endpoint_alias"

    def normalize(self, observations: list[Observation]) -> list[Observation]:
        """Return one derived alias for each unique hostname and endpoint pair."""

        aliases: dict[tuple[str, str, str, str], list[Observation]] = {}
        for observation in observations:
            metadata = observation.metadata
            stable_name = _metadata_string(metadata.get("hostname")) or _metadata_string(
                metadata.get("nodename")
            )
            endpoint = _metadata_string(metadata.get("instance")) or _metadata_string(
                metadata.get("endpoint")
            )
            if stable_name is None or endpoint is None or stable_name == endpoint:
                continue
            source_name = _metadata_string(metadata.get("source_name"))
            # Accept the earlier metadata spelling while source adapters migrate to
            # the shared source_name contract.
            source_name = source_name or _metadata_string(metadata.get("source"))
            predicate = (
                f"{_normalize_source_name(source_name)}_instance"
                if source_name
                else "alias"
            )
            key = (observation.source_type, stable_name, predicate, endpoint)
            aliases.setdefault(key, []).append(observation)

        return [
            self._derive_alias(key, source_observations)
            for key, source_observations in aliases.items()
        ]

    def _derive_alias(
        self,
        key: tuple[str, str, str, str],
        source_observations: list[Observation],
    ) -> Observation:
        source_type, stable_name, predicate, endpoint = key
        first = source_observations[0]
        source_ids = list(dict.fromkeys(obs.id for obs in source_observations))
        metadata = {
            **dict(first.metadata),
            "derived": True,
            "derived_from_observation_id": first.id,
            "normalizer": self.name,
            "original_subject": first.subject,
        }
        if len(source_ids) > 1:
            metadata["derived_from_observation_ids"] = source_ids

        return Observation(
            id=_derived_observation_id(
                self.name, source_type, stable_name, predicate, endpoint
            ),
            source_type=source_type,
            observed_at=max(obs.observed_at for obs in source_observations),
            subject=stable_name,
            predicate=predicate,
            value=endpoint,
            confidence=min(obs.confidence for obs in source_observations),
            metadata=metadata,
            expires_at=_earliest_expiration(source_observations),
        )


DEFAULT_OBSERVATION_NORMALIZATION_PIPELINE = ObservationNormalizationPipeline(
    [EndpointAliasNormalizer()]
)


def _metadata_string(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


def _normalize_source_name(source_name: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", source_name.strip().lower()).strip("_")
    return normalized or "source"


def _derived_observation_id(prefix: str, *parts: Any) -> str:
    payload = "\x1f".join(str(part) for part in parts)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"obs_{prefix}_{digest}"


def _derived_observation_key(observation: Observation) -> str:
    payload = {
        "source_type": observation.source_type,
        "subject": observation.subject,
        "predicate": observation.predicate,
        "value": to_plain(observation.value),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)


def _earliest_expiration(observations: list[Observation]) -> datetime | None:
    expirations = [obs.expires_at for obs in observations if obs.expires_at is not None]
    return min(expirations) if expirations else None
