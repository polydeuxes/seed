"""Observation normalizers backed by Seed's canonical PredicateCatalog."""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

from seed_runtime.observations import Observation
from seed_runtime.predicate_catalog import PredicateCatalog

if TYPE_CHECKING:
    from seed_runtime.state import State


class PredicateNormalizer:
    """Derive canonical observations from provider-specific observations."""

    name = "predicate"

    def __init__(self, catalog: PredicateCatalog | None = None) -> None:
        self.catalog = catalog or PredicateCatalog.load()

    def normalize(
        self, observations: list[Observation], *, state: "State | None" = None
    ) -> list[Observation]:
        """Return canonical derivations while leaving all raw observations intact."""

        derived: list[Observation] = []
        for observation in observations:
            source_name = observation.metadata.get(
                "source_name"
            ) or observation.metadata.get("source")
            mapping = self.catalog.find_mapping(
                observation.predicate,
                source_name=source_name if isinstance(source_name, str) else None,
            )
            if mapping is None:
                continue
            value = mapping.map_value(observation.value)
            metadata = {
                **dict(observation.metadata),
                "derived": True,
                "derived_from_observation_id": observation.id,
                "normalizer": self.name,
                "original_predicate": observation.predicate,
                "canonical_predicate": mapping.canonical_predicate,
                "original_value": observation.value,
            }
            derived.append(
                Observation(
                    id=_derived_observation_id(
                        self.name,
                        observation.id,
                        mapping.canonical_predicate,
                        value,
                    ),
                    source_type=observation.source_type,
                    observed_at=observation.observed_at,
                    subject=observation.subject,
                    predicate=mapping.canonical_predicate,
                    value=value,
                    confidence=observation.confidence,
                    metadata=metadata,
                    expires_at=observation.expires_at,
                )
            )
        return derived


def _derived_observation_id(prefix: str, *parts: object) -> str:
    payload = "\x1f".join(str(part) for part in parts)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"obs_{prefix}_{digest}"
