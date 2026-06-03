"""Observation source adapters and collection service."""

from __future__ import annotations

import json
import os
import platform
import shutil
from datetime import datetime, timezone
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen

from seed_runtime.ansible_inventory_source import AnsibleInventoryObservationSource
from seed_runtime.base import SeedModel
from seed_runtime.facts import Fact, FactConflict, is_fact_expired
from seed_runtime.ids import new_id
from seed_runtime.models import Actor
from seed_runtime.serialization import to_plain
from seed_runtime.observation_normalizers import (
    DEFAULT_OBSERVATION_NORMALIZATION_PIPELINE,
    ObservationNormalizationPipeline,
)
from seed_runtime.observations import Observation, ObservationIngestor, ObservationSourceType

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field

DEFAULT_JSON_OBSERVED_AT = datetime(1970, 1, 1)


class ObservationInventoryDiffEntry(SeedModel):
    """One incoming observation and the projected state it would affect."""

    observation: dict[str, Any]
    current_fact_ids: list[str] = Field(default_factory=list)
    current_values: list[Any] = Field(default_factory=list)
    reason: str


class ObservationInventoryDiff(SeedModel):
    """Dry-run diff for a JSON observation inventory against projected state."""

    new_facts: list[ObservationInventoryDiffEntry] = Field(default_factory=list)
    matching_facts: list[ObservationInventoryDiffEntry] = Field(default_factory=list)
    changed_facts: list[ObservationInventoryDiffEntry] = Field(default_factory=list)
    expired_incoming: list[ObservationInventoryDiffEntry] = Field(default_factory=list)
    conflicts_introduced: list[FactConflict] = Field(default_factory=list)


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


class LocalHostObservationSource:
    """Read-only local host observation source using Python stdlib APIs only.

    This source intentionally does not execute shells or subprocesses. It reads
    process-local platform and disk metadata via Python standard library calls.
    """

    source_type: ObservationSourceType = "discovery"

    def __init__(self, *, name: str = "local-host") -> None:
        self.name = name

    def collect(self) -> list[Observation]:
        """Return local host facts without executing or mutating the host."""

        observed_at = datetime.now(timezone.utc)
        hostname = platform.node() or "localhost"
        system = (platform.system() or "unknown").lower()
        architecture = platform.machine() or "unknown"
        uname_metadata: dict[str, Any] = {}
        if hasattr(os, "uname"):
            uname = os.uname()
            uname_metadata = {
                "sysname": uname.sysname,
                "nodename": uname.nodename,
                "release": uname.release,
                "version": uname.version,
                "machine": uname.machine,
            }
        disk_usage = shutil.disk_usage("/")
        metadata = {
            "collector": "LocalHostObservationSource",
            "read_only": True,
            "shell_execution": False,
            **uname_metadata,
        }
        return [
            self._observation(
                observed_at, hostname, "os", system, metadata={**metadata}
            ),
            self._observation(
                observed_at,
                hostname,
                "architecture",
                architecture,
                metadata={**metadata},
            ),
            self._observation(
                observed_at,
                hostname,
                "disk_total_bytes",
                int(disk_usage.total),
                metadata={**metadata, "path": "/"},
            ),
            self._observation(
                observed_at,
                hostname,
                "disk_free_bytes",
                int(disk_usage.free),
                metadata={**metadata, "path": "/"},
            ),
        ]

    def _observation(
        self,
        observed_at: datetime,
        subject: str,
        predicate: str,
        value: Any,
        *,
        metadata: dict[str, Any],
    ) -> Observation:
        return Observation(
            id=new_id("obs_local_host"),
            source_type=self.source_type,
            observed_at=observed_at,
            subject=subject,
            predicate=predicate,
            value=value,
            confidence=1.0,
            metadata=metadata,
        )


class PrometheusObservationSource:
    """Read-only Prometheus HTTP API observation source.

    The source only performs HTTP GET requests against a fixed allowlist of safe
    metric names and does not accept arbitrary PromQL from users.
    """

    SAFE_QUERIES = (
        "up",
        "node_uname_info",
        "node_filesystem_avail_bytes",
        "node_filesystem_size_bytes",
    )

    def __init__(
        self,
        base_url: str,
        *,
        name: str | None = None,
        source_type: ObservationSourceType = "provider",
        timeout_seconds: float = 5.0,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError(
                "PrometheusObservationSource timeout_seconds must be positive"
            )
        self.base_url = base_url.rstrip("/") + "/"
        self.name = name or f"prometheus:{base_url.rstrip('/')}"
        self.source_type = source_type
        self.timeout_seconds = timeout_seconds
        self.last_error: str | None = None

    def collect(self) -> list[Observation]:
        """Collect safe Prometheus metrics, returning [] if unreachable."""

        observed_at = datetime.now(timezone.utc)
        observations: list[Observation] = []
        self.last_error = None
        for query in self.SAFE_QUERIES:
            try:
                payload = self._query(query)
            except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
                self.last_error = f"{type(exc).__name__}: {exc}"
                return []
            observations.extend(
                self._observations_from_query(query, payload, observed_at)
            )
        return observations

    def _query(self, query: str) -> dict[str, Any]:
        if query not in self.SAFE_QUERIES:
            raise ValueError(f"Prometheus query is not allowlisted: {query}")
        url = (
            urljoin(self.base_url, "api/v1/query")
            + "?"
            + urlencode({"query": query})
        )
        request = Request(url, method="GET", headers={"Accept": "application/json"})
        with urlopen(request, timeout=self.timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Prometheus response must be a JSON object")
        if payload.get("status") != "success":
            raise ValueError("Prometheus response status was not success")
        data = payload.get("data")
        if not isinstance(data, dict) or data.get("resultType") != "vector":
            raise ValueError("Prometheus response data must be a vector")
        result = data.get("result")
        if not isinstance(result, list):
            raise ValueError("Prometheus vector result must be a list")
        return payload

    def _observations_from_query(
        self, query: str, payload: dict[str, Any], observed_at: datetime
    ) -> list[Observation]:
        result = payload["data"]["result"]
        observations: list[Observation] = []
        for sample in result:
            if not isinstance(sample, dict):
                continue
            metric = sample.get("metric")
            value = sample.get("value")
            if (
                not isinstance(metric, dict)
                or not isinstance(value, list)
                or len(value) < 2
            ):
                continue
            instance = metric.get("instance")
            if not isinstance(instance, str) or not instance:
                continue
            sample_value = value[1]
            metadata = {
                "collector": "PrometheusObservationSource",
                "prometheus_base_url": self.base_url.rstrip("/"),
                "prometheus_metric": query,
                "metric_labels": dict(metric),
                "read_only": True,
                "http_method": "GET",
            }
            # Only node_uname_info is authoritative for stable host identity.
            # Other metrics remain endpoint-scoped and do not participate in
            # endpoint alias normalization.
            if query == "node_uname_info":
                metadata.update(
                    {
                        "source_name": "prometheus",
                        "instance": instance,
                    }
                )
                nodename = metric.get("nodename")
                if isinstance(nodename, str) and nodename.strip():
                    metadata["nodename"] = nodename.strip()
            if query == "up":
                observations.append(
                    self._observation(
                        observed_at,
                        instance,
                        "up",
                        _prometheus_int(sample_value),
                        metadata,
                    )
                )
            elif query == "node_uname_info":
                os_value = _prometheus_os_from_uname(metric)
                if os_value is not None:
                    observations.append(
                        self._observation(
                            observed_at, instance, "os", os_value, metadata
                        )
                    )
            elif query == "node_filesystem_avail_bytes":
                observations.append(
                    self._observation(
                        observed_at,
                        instance,
                        "filesystem_avail_bytes",
                        _prometheus_int(sample_value),
                        metadata,
                    )
                )
            elif query == "node_filesystem_size_bytes":
                observations.append(
                    self._observation(
                        observed_at,
                        instance,
                        "filesystem_size_bytes",
                        _prometheus_int(sample_value),
                        metadata,
                    )
                )
        return observations

    def _observation(
        self,
        observed_at: datetime,
        subject: str,
        predicate: str,
        value: Any,
        metadata: dict[str, Any],
    ) -> Observation:
        return Observation(
            id=new_id("obs_prometheus"),
            source_type=self.source_type,
            observed_at=observed_at,
            subject=subject,
            predicate=predicate,
            value=value,
            confidence=0.95,
            metadata=metadata,
        )


def _prometheus_int(value: Any) -> int:
    return int(float(str(value)))


def _prometheus_os_from_uname(metric: dict[str, Any]) -> str | None:
    sysname = metric.get("sysname") or metric.get("system")
    if not isinstance(sysname, str) or not sysname.strip():
        return None
    normalized = sysname.strip().lower()
    if normalized in {"linux", "darwin", "windows"}:
        return normalized
    return normalized


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


def diff_observations_json(state: Any, payload: Any) -> ObservationInventoryDiff:
    """Compare a JSON observation inventory with current projected state.

    This is a pure dry-run helper: it validates and normalizes the incoming JSON
    payload into Observation instances but does not append events, ingest
    observations, or mutate the supplied State.
    """

    observations = _observations_from_json_payload(payload)
    current_by_claim: dict[tuple[str, str], list[Fact]] = {}
    for fact in state.facts.values():
        if is_fact_expired(fact):
            continue
        current_by_claim.setdefault((fact.subject_id, fact.predicate), []).append(fact)

    new_facts: list[ObservationInventoryDiffEntry] = []
    matching_facts: list[ObservationInventoryDiffEntry] = []
    changed_facts: list[ObservationInventoryDiffEntry] = []
    expired_incoming: list[ObservationInventoryDiffEntry] = []
    conflicts_introduced: list[FactConflict] = []

    for observation in observations:
        incoming_entry = _diff_entry(observation)
        if _is_observation_expired(observation):
            expired_incoming.append(
                incoming_entry.model_copy(
                    update={"reason": "incoming observation is already expired"}
                )
            )
            continue

        current_facts = current_by_claim.get(
            (observation.subject, observation.predicate), []
        )
        current_value_keys = {_json_value_key(fact.value) for fact in current_facts}
        incoming_value_key = _json_value_key(observation.value)
        current_values = _dedupe_values(fact.value for fact in current_facts)
        current_fact_ids = [fact.id for fact in current_facts]

        if not current_facts:
            new_facts.append(
                incoming_entry.model_copy(
                    update={
                        "reason": "no current fact for subject and predicate",
                    }
                )
            )
            continue

        if incoming_value_key in current_value_keys:
            matching_facts.append(
                incoming_entry.model_copy(
                    update={
                        "current_fact_ids": current_fact_ids,
                        "current_values": current_values,
                        "reason": "incoming observation matches current projected fact value",
                    }
                )
            )
            continue

        changed_facts.append(
            incoming_entry.model_copy(
                update={
                    "current_fact_ids": current_fact_ids,
                    "current_values": current_values,
                    "reason": "incoming observation value differs from current projected fact value",
                }
            )
        )
        values = [*current_values, observation.value]
        conflicts_introduced.append(
            FactConflict(
                subject=observation.subject,
                predicate=observation.predicate,
                values=values,
                winning_value=None,
                best_fact_id=None,
                conflicting_fact_ids=current_fact_ids,
                reason=(
                    f"incoming observation would introduce multiple values for "
                    f"{observation.subject}/{observation.predicate}"
                ),
            )
        )

    return ObservationInventoryDiff(
        new_facts=new_facts,
        matching_facts=matching_facts,
        changed_facts=changed_facts,
        expired_incoming=expired_incoming,
        conflicts_introduced=conflicts_introduced,
    )


def _observations_from_json_payload(payload: Any) -> list[Observation]:
    if not isinstance(payload, dict):
        raise ValueError("JSON observation payload must contain a top-level object")
    entries = payload.get("observations")
    if not isinstance(entries, list):
        raise ValueError("JSON observation payload must contain an observations array")
    source = JsonObservationSource("<payload>")
    return [
        source._observation_from_entry(entry, index)
        for index, entry in enumerate(entries)
    ]


def _diff_entry(observation: Observation) -> ObservationInventoryDiffEntry:
    return ObservationInventoryDiffEntry(
        observation=to_plain(observation),
        reason="",
    )


def _is_observation_expired(observation: Observation) -> bool:
    if observation.expires_at is None:
        return False
    comparison_time = datetime.now(timezone.utc)
    expires_at = observation.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return expires_at <= comparison_time


def _json_value_key(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def _dedupe_values(values: Any) -> list[Any]:
    deduped: list[Any] = []
    seen: set[str] = set()
    for value in values:
        key = _json_value_key(value)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(value)
    return deduped


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

    def __init__(
        self,
        ingestor: ObservationIngestor,
        *,
        normalization_pipeline: ObservationNormalizationPipeline | None = (
            DEFAULT_OBSERVATION_NORMALIZATION_PIPELINE
        ),
    ) -> None:
        self.ingestor = ingestor
        self.normalization_pipeline = normalization_pipeline

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
        if self.normalization_pipeline is not None:
            normalized = self.normalization_pipeline.normalize(normalized)

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
