"""Shared normalization pipeline for observations emitted by source adapters."""

from __future__ import annotations

import hashlib
import inspect
import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any, Protocol

from seed_runtime.facts import is_fact_expired
from seed_runtime.observations import Observation
from seed_runtime.predicate_normalizers import PredicateNormalizer
from seed_runtime.serialization import to_plain

if TYPE_CHECKING:
    from seed_runtime.state import State


class ObservationNormalizer(Protocol):
    """Derive normalized observations without mutating source observations."""

    name: str

    def normalize(
        self, observations: list[Observation], *, state: "State | None" = None
    ) -> list[Observation]:
        """Return observations derived from the supplied observations and state."""


class ObservationNormalizationPipeline:
    """Run normalizers in order and retain originals plus unique derivations."""

    def __init__(self, normalizers: list[ObservationNormalizer] | None = None) -> None:
        self.normalizers = list(normalizers or [])

    def normalize(
        self, observations: list[Observation], *, state: "State | None" = None
    ) -> list[Observation]:
        """Return originals plus unique derivations using optional projected state."""

        normalized = list(observations)
        original_ids = {observation.id for observation in observations}
        derived_keys: set[str] = set()
        for normalizer in self.normalizers:
            for derived in _normalize_with_state(normalizer, list(normalized), state):
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


_ENDPOINT_IDENTITY_PREDICATES = {"ip_address", "alias", "ansible_host"}
_ENDPOINT_HOST_PATTERN = re.compile(
    r"(?:[A-Za-z0-9_](?:[A-Za-z0-9_.-]*[A-Za-z0-9_])?)"
)


class EndpointAliasNormalizer:
    """Derive stable hostname-to-endpoint aliases from generic source metadata."""

    name = "endpoint_alias"

    def normalize(
        self, observations: list[Observation], *, state: "State | None" = None
    ) -> list[Observation]:
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


class EndpointIdentityNormalizer:
    """Link explicitly known base identities to observed endpoint subjects."""

    name = "endpoint_identity"

    def normalize(
        self, observations: list[Observation], *, state: "State | None" = None
    ) -> list[Observation]:
        """Derive one alias per identity subject and matching endpoint."""

        identities: dict[str, list[_IdentityMatch]] = {}
        endpoints: dict[str, list[Observation]] = {}
        endpoint_bases: dict[str, str] = {}
        existing_aliases: set[tuple[str, str]] = set()

        for observation in observations:
            self._add_identity(observation, identities, existing_aliases)

            endpoint = observation.subject
            base_identity = _endpoint_base_identity(endpoint)
            if base_identity is not None:
                endpoints.setdefault(endpoint, []).append(observation)
                endpoint_bases[endpoint] = base_identity

        if state is not None:
            for fact in state.facts.values():
                if is_fact_expired(fact):
                    continue
                self._add_identity(fact, identities, existing_aliases)

        derived: list[Observation] = []
        seen: set[tuple[str, str]] = set()
        for endpoint, endpoint_observations in endpoints.items():
            matching_identities = identities.get(endpoint_bases[endpoint], [])
            for identity in sorted(matching_identities, key=_identity_match_sort_key):
                key = (identity.subject, endpoint)
                if key in seen or key in existing_aliases or identity.subject == endpoint:
                    continue
                seen.add(key)
                derived.append(self._derive_alias(identity, endpoint, endpoint_observations))

        return derived

    @staticmethod
    def _add_identity(
        source: Any,
        identities: dict[str, list["_IdentityMatch"]],
        existing_aliases: set[tuple[str, str]],
    ) -> None:
        predicate = source.predicate
        if predicate not in _ENDPOINT_IDENTITY_PREDICATES:
            return
        identity = _observation_string_value(source.value)
        if identity is None:
            return
        subject = getattr(source, "subject", None)
        if subject is None:
            subject = source.subject_id
        match = _IdentityMatch(
            id=source.id,
            subject=subject,
            predicate=predicate,
            observed_at=source.observed_at,
            confidence=source.confidence,
            expires_at=source.expires_at,
        )
        identities.setdefault(identity, []).append(match)
        if predicate == "alias":
            existing_aliases.add((subject, identity))

    def _derive_alias(
        self,
        identity: "_IdentityMatch",
        endpoint: str,
        endpoint_observations: list[Observation],
    ) -> Observation:
        first_endpoint = endpoint_observations[0]
        source_ids = list(
            dict.fromkeys(
                [identity.id, *(observation.id for observation in endpoint_observations)]
            )
        )
        metadata = {
            **dict(first_endpoint.metadata),
            "derived": True,
            "derived_from_observation_id": first_endpoint.id,
            "derived_from_observation_ids": source_ids,
            "normalizer": self.name,
            "original_endpoint_subject": endpoint,
            "matched_identity_subject": identity.subject,
            "matched_identity_predicate": identity.predicate,
        }
        return Observation(
            id=_derived_observation_id(self.name, identity.subject, "alias", endpoint),
            source_type=first_endpoint.source_type,
            observed_at=max(
                identity.observed_at,
                *(observation.observed_at for observation in endpoint_observations),
            ),
            subject=identity.subject,
            predicate="alias",
            value=endpoint,
            confidence=min(
                identity.confidence,
                *(observation.confidence for observation in endpoint_observations),
            ),
            metadata=metadata,
            expires_at=_earliest_expiration_values(
                [
                    identity.expires_at,
                    *(observation.expires_at for observation in endpoint_observations),
                ]
            ),
        )


@dataclass(frozen=True)
class _IdentityMatch:
    """Identity evidence from either the current batch or projected state."""

    id: str
    subject: str
    predicate: str
    observed_at: datetime
    confidence: float
    expires_at: datetime | None


# Identity normalization runs first so canonical observations inherit the same raw
# endpoint subjects and participate in the aliases derived earlier in the batch.
DEFAULT_OBSERVATION_NORMALIZATION_PIPELINE = ObservationNormalizationPipeline(
    [EndpointAliasNormalizer(), EndpointIdentityNormalizer(), PredicateNormalizer()]
)


def _observation_string_value(value: Any) -> str | None:
    return _metadata_string(value)


def _normalize_with_state(
    normalizer: ObservationNormalizer,
    observations: list[Observation],
    state: "State | None",
) -> list[Observation]:
    """Pass state to context-aware normalizers without breaking older extensions."""

    parameters = inspect.signature(normalizer.normalize).parameters.values()
    accepts_state = any(
        parameter.name == "state" or parameter.kind == inspect.Parameter.VAR_KEYWORD
        for parameter in parameters
    )
    if accepts_state:
        return normalizer.normalize(observations, state=state)
    return normalizer.normalize(observations)  # type: ignore[call-arg]


def _endpoint_base_identity(subject: str) -> str | None:
    base, separator, port = subject.rpartition(":")
    if not separator or not base or not port.isdigit():
        return None
    if not 1 <= int(port) <= 65535:
        return None
    if _ENDPOINT_HOST_PATTERN.fullmatch(base) is None:
        return None
    return base


def _identity_match_sort_key(identity: _IdentityMatch) -> tuple[int, str]:
    predicate_priority = {"ip_address": 0, "ansible_host": 1, "alias": 2}
    return (predicate_priority[identity.predicate], identity.id)


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
    return _earliest_expiration_values([obs.expires_at for obs in observations])


def _earliest_expiration_values(values: list[datetime | None]) -> datetime | None:
    expirations = [value for value in values if value is not None]
    return min(expirations) if expirations else None
