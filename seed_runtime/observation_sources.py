"""Observation source adapters and collection service."""

from __future__ import annotations

import fcntl
import ipaddress
import json
import math
import os
import platform
import re
import shutil
import socket
import subprocess
import stat
import struct
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen

from seed_runtime.base import SeedModel
from seed_runtime.facts import Fact, FactConflict, is_fact_expired
from seed_runtime.ids import new_id
from seed_runtime.knowledge.relationship_observation import (
    extract_python_definition_relationship_facts,
    extract_python_import_relationship_facts,
)
from seed_runtime.models import Actor
from seed_runtime.local_packages import (
    package_records_to_observations,
    parse_dpkg_status,
)
from seed_runtime.execution_status import (
    ExecutionStatusConsumer,
    ObservationProducerLifecycle,
)
from seed_runtime.serialization import to_plain
from seed_runtime.observation_normalizers import (
    DEFAULT_OBSERVATION_NORMALIZATION_PIPELINE,
    ObservationNormalizationPipeline,
    is_endpoint_subject,
)
from seed_runtime.observations import (
    Observation,
    ObservationIngestor,
    ObservationSourceType,
)
from seed_runtime.state import StateProjector

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


@dataclass
class ObservationIngestionDiagnostics:
    """Comparable timing counters for observation collection and ingestion."""

    source_name: str
    source_collection_seconds: float = 0.0
    normalization_seconds: float = 0.0
    event_generation_and_ledger_write_seconds: float = 0.0
    total_seconds: float = 0.0
    total_observations: int = 0
    total_events: int = 0
    facts_promoted: int = 0
    source_counters: dict[str, Any] = field(default_factory=dict)

    @property
    def observations_per_second(self) -> float:
        if not self.total_seconds:
            return 0.0
        return self.total_observations / self.total_seconds

    @property
    def events_per_second(self) -> float:
        if not self.event_generation_and_ledger_write_seconds:
            return 0.0
        return self.total_events / self.event_generation_and_ledger_write_seconds


class RepositorySourceObservationSource:
    """Read-only repository source adapter for imports/defines observations."""

    name = "repository_source"
    source_type: ObservationSourceType = "discovery"

    def __init__(
        self,
        repository_root: str | Path,
        *,
        observed_at: datetime | None = None,
        include_roots: tuple[str, ...] = ("seed_runtime", "tests"),
    ) -> None:
        self.repository_root = Path(repository_root).resolve()
        self.observed_at = observed_at or datetime.now(timezone.utc)
        self.include_roots = include_roots
        self.last_collection_counters: dict[str, Any] = {}

    def collect(self) -> list[Observation]:
        observations: list[Observation] = []
        files_scanned = 0
        definitions_imports_extracted = 0
        for source_path in self.discover_source_files():
            files_scanned += 1
            text = (self.repository_root / source_path).read_text(encoding="utf-8")
            relationship_facts = [
                *extract_python_import_relationship_facts(source_path, text),
                *extract_python_definition_relationship_facts(source_path, text),
            ]
            definitions_imports_extracted += len(relationship_facts)
            observations.extend(
                self._relationship_observation(relationship)
                for relationship in relationship_facts
            )
        self.last_collection_counters = {
            "files_scanned": files_scanned,
            "files_skipped": 0,
            "definitions_imports_extracted": definitions_imports_extracted,
        }
        return observations

    def discover_source_files(self) -> list[str]:
        """Return allowlisted Python source paths without shelling out to grep."""

        source_paths: list[str] = []
        for include_root in self.include_roots:
            root = (self.repository_root / include_root).resolve()
            if not root.exists():
                continue
            if not root.is_dir() or not root.is_relative_to(self.repository_root):
                raise ValueError(f"repository observation root is not allowed: {root}")
            source_paths.extend(
                path.relative_to(self.repository_root).as_posix()
                for path in root.rglob("*.py")
                if _is_observable_repository_source(path)
            )
        return sorted(source_paths)

    def _relationship_observation(self, relationship: Any) -> Observation:
        return Observation(
            id=new_id("obs_repo"),
            source_type=self.source_type,
            observed_at=self.observed_at,
            subject=relationship.subject,
            predicate=relationship.relationship_kind,
            value=relationship.object,
            confidence=1.0,
            metadata={
                "source_name": self.name,
                "source_path": relationship.path,
                "evidence": relationship.evidence,
                "relationship_family": relationship.relationship_kind,
                "repository_root": str(self.repository_root),
            },
            dimensions={"path": relationship.path},
        )


def _is_observable_repository_source(path: Path) -> bool:
    return "__pycache__" not in path.parts


_IDENTITY_QUESTIONS = {
    "hostname": "What hostname is configured locally?",
    "machine_id": "What machine-id is recorded locally?",
    "boot_id": "What boot-id is recorded for the current local boot?",
    "fqdn": "What fully qualified hostname is explicitly configured locally?",
}

_HOSTS_FILE_QUESTION = "What local hosts-file name/address mappings are configured?"
_HOSTS_FILE_SOURCE = "/etc/hosts"

_MOUNT_QUESTIONS = {
    "mount_point": "What mount points currently exist?",
    "filesystem_type": "What filesystem type is mounted?",
    "mounted_device": "Which device backs the mount?",
    "mount_option": "What mount options are recorded for the mount?",
}

_STORAGE_QUESTIONS = {
    "block_device": "What block devices are visible locally?",
    "partition": "What partitions are visible locally?",
    "block_device_size_bytes": "How large is this observed block device or partition?",
    "block_device_rotational": "Does local sysfs mark this storage device as rotational?",
    "block_device_removable": "Does local sysfs mark this storage device as removable?",
    "block_device_model": "What model string is exposed locally for this block device?",
    "block_device_vendor": "What vendor string is exposed locally for this block device?",
    "block_device_parent": "What parent block device is exposed locally for this partition?",
}

_LISTENER_QUESTIONS = {
    "listening_port": "What TCP/UDP ports are bound locally?",
    "listening_protocol": "What local listener protocol is exposed by kernel state?",
    "listening_address": "What local addresses are bound by listeners?",
    "listening_endpoint": "What protocol/address/port endpoints are bound locally?",
    "listening_socket_family": "What socket address families are bound by listeners?",
    "listening_process_id": "What process IDs are directly linked to listener socket inodes?",
    "listening_process_name": "What process names are directly linked to listener socket inodes?",
}

_LOCAL_USER_QUESTIONS = {
    "user_account": "Which local user accounts are declared on this host?",
    "user_uid": "What UID is declared for this local user account?",
    "user_primary_gid": "What primary GID is declared for this local user account?",
    "user_home_directory": "What home directory is declared for this local user account?",
    "user_shell": "What shell is declared for this local user account?",
    "group_account": "Which local group accounts are declared on this host?",
    "group_gid": "What GID is declared for this local group account?",
    "group_member": "Which supplementary group members are declared locally?",
}

_HOST_DESCRIPTION_QUESTIONS = {
    "kernel_release": "What kernel release is this host running?",
    "kernel_version": "What kernel version string is reported locally?",
    "cpu_model": "What CPU model is reported locally?",
    "cpu_count": "How many CPUs are visible locally?",
    "memory_total_bytes": "How much total memory is reported locally?",
}

_PROC_MOUNT_ESCAPE_RE = re.compile(r"\\([0-7]{3})")
_LOCAL_READ_MAX_BYTES = 1024 * 1024


def _read_bounded_first_line(path: Path, *, max_bytes: int = 4096) -> str | None:
    if max_bytes <= 0:
        return None
    try:
        path_stat = path.stat()
    except OSError:
        stat_size_known = False
        stat_size = 0
    else:
        stat_size_known = stat.S_ISREG(path_stat.st_mode)
        stat_size = path_stat.st_size
        if stat_size_known and stat_size > max_bytes:
            return None
    try:
        with path.open("rb") as handle:
            raw = handle.read(max_bytes)
    except OSError:
        return None
    if not raw or (not stat_size_known and len(raw) == max_bytes):
        return None
    text = raw.decode("utf-8", errors="replace").splitlines()[0].strip()
    return text or None


def _is_locally_configured_fqdn(value: str) -> bool:
    candidate = value.strip().rstrip(".")
    if "." not in candidate or candidate.lower() == "localhost.localdomain":
        return False
    labels = candidate.split(".")
    return all(label and not label.isspace() for label in labels)


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
    process-local platform, disk, local network, and mount metadata via
    Python standard library calls and local read-only files.
    """

    source_type: ObservationSourceType = "discovery"

    def __init__(
        self,
        *,
        name: str = "local-host",
        proc_root: str | Path = "/proc",
        sys_class_net: str | Path = "/sys/class/net",
        sys_block: str | Path = "/sys/block",
        sys_class_block: str | Path = "/sys/class/block",
        etc_hostname: str | Path = "/etc/hostname",
        machine_id: str | Path = "/etc/machine-id",
        etc_hosts: str | Path = "/etc/hosts",
        resolv_conf: str | Path = "/etc/resolv.conf",
        systemd_resolv_conf: str | Path = "/run/systemd/resolve/resolv.conf",
        systemd_stub_resolv_conf: str | Path = "/run/systemd/resolve/stub-resolv.conf",
        systemd_resolved_conf: str | Path = "/etc/systemd/resolved.conf",
        systemd_lease_dir: str | Path = "/run/systemd/netif/leases",
        etc_passwd: str | Path = "/etc/passwd",
        etc_group: str | Path = "/etc/group",
        dpkg_status: str | Path = "/var/lib/dpkg/status",
        systemd_source: Any | None = None,
    ) -> None:
        self.name = name
        self.proc_root = Path(proc_root)
        self.sys_class_net = Path(sys_class_net)
        self.sys_block = Path(sys_block)
        self.sys_class_block = Path(sys_class_block)
        self.etc_hostname = Path(etc_hostname)
        self.machine_id = Path(machine_id)
        self.etc_hosts = Path(etc_hosts)
        self.resolv_conf = Path(resolv_conf)
        self.systemd_resolv_conf = Path(systemd_resolv_conf)
        self.systemd_stub_resolv_conf = Path(systemd_stub_resolv_conf)
        self.systemd_resolved_conf = Path(systemd_resolved_conf)
        self.systemd_lease_dir = Path(systemd_lease_dir)
        self.etc_passwd = Path(etc_passwd)
        self.etc_group = Path(etc_group)
        self.dpkg_status = Path(dpkg_status)
        self.systemd_source = systemd_source

    def collect(self) -> list[Observation]:
        """Return local host facts without executing or mutating the host."""

        observed_at = datetime.now(timezone.utc)
        identity = self._collect_local_identity()
        hostname_entry = identity.get("hostname")
        hostname = platform.node() or (
            hostname_entry["value"] if isinstance(hostname_entry, dict) else "localhost"
        )
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
            "local_only": True,
            "shell_execution": False,
            "subprocess_execution": False,
            "privilege_escalation": False,
            "network_probe": False,
            "network_connection": False,
            **uname_metadata,
        }
        observations = self._collect_identity_observations(
            observed_at, hostname, metadata, identity
        )
        observations.extend(
            self._collect_hosts_file_observations(observed_at, hostname, metadata)
        )
        observations.extend(
            [
                self._observation(
                    observed_at,
                    hostname,
                    "local_observation_status",
                    "observed",
                    metadata={
                        **metadata,
                        "meaning": "Seed inspected this host through local read-only APIs",
                        "network_reachability_asserted": False,
                        "provider_visibility_asserted": False,
                        "availability_asserted": False,
                    },
                ),
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
        )
        observations.extend(
            self._collect_host_description_observations(observed_at, hostname, metadata)
        )
        observations.extend(
            self._collect_network_observations(observed_at, hostname, metadata)
        )
        observations.extend(
            self._collect_mount_observations(observed_at, hostname, metadata)
        )
        observations.extend(
            self._collect_storage_observations(observed_at, hostname, metadata)
        )
        observations.extend(
            self._collect_listener_observations(observed_at, hostname, metadata)
        )
        observations.extend(
            self._collect_local_user_observations(observed_at, hostname, metadata)
        )
        observations.extend(
            self._collect_local_package_observations(observed_at, hostname)
        )
        observations.extend(self._collect_systemd_observations(observed_at, hostname))
        return observations

    def _collect_systemd_observations(
        self, observed_at: datetime, hostname: str
    ) -> list[Observation]:
        """Collect systemd unit facts through the dedicated systemd source."""

        source = self.systemd_source
        if source is None:
            source = SystemdObservationSource(observed_at=observed_at, hostname=hostname)
        try:
            return source.collect()
        except Exception:
            return []

    def _collect_local_package_observations(
        self, observed_at: datetime, hostname: str
    ) -> list[Observation]:
        """Collect installed package facts from the local dpkg status database.

        LocalHostObservationSource only orchestrates the read-only collection.
        Dpkg parsing and generic package observation emission live in
        seed_runtime.local_packages so dpkg remains the first adapter rather
        than the package observation architecture.
        """

        status_text = self._read_text(self.dpkg_status, max_bytes=16 * 1024 * 1024)
        if status_text is None:
            return []
        records = parse_dpkg_status(status_text)
        return package_records_to_observations(
            hostname, records, observed_at, self.source_type
        )

    def _collect_local_identity(self) -> dict[str, dict[str, str]]:
        """Read bounded local identity files without DNS, network, or execution."""

        identity: dict[str, dict[str, str]] = {}
        hostname = self._first_local_value(
            (
                ("/etc/hostname", self.etc_hostname),
                ("/proc/sys/kernel/hostname", self.proc_root / "sys/kernel/hostname"),
            )
        )
        if hostname is not None:
            identity["hostname"] = hostname
        machine_id = self._first_local_value((("/etc/machine-id", self.machine_id),))
        if machine_id is not None:
            identity["machine_id"] = machine_id
        boot_id = self._first_local_value(
            (
                (
                    "/proc/sys/kernel/random/boot_id",
                    self.proc_root / "sys/kernel/random/boot_id",
                ),
            )
        )
        if boot_id is not None:
            identity["boot_id"] = boot_id
        if hostname is not None and _is_locally_configured_fqdn(hostname["value"]):
            identity["fqdn"] = {
                "value": hostname["value"],
                "source": hostname["source"],
            }
        return identity

    def _first_local_value(
        self, candidates: tuple[tuple[str, Path], ...]
    ) -> dict[str, str] | None:
        for source_name, path in candidates:
            value = _read_bounded_first_line(path)
            if value:
                return {"value": value, "source": source_name}
        return None

    def _collect_identity_observations(
        self,
        observed_at: datetime,
        subject: str,
        metadata: dict[str, Any],
        identity: dict[str, dict[str, str]],
    ) -> list[Observation]:
        observations: list[Observation] = []
        for predicate in ("hostname", "machine_id", "boot_id", "fqdn"):
            entry = identity.get(predicate)
            if not isinstance(entry, dict):
                continue
            observations.append(
                self._observation(
                    observed_at,
                    subject,
                    predicate,
                    entry["value"],
                    metadata={
                        **metadata,
                        "source": entry["source"],
                        "question_answered": _IDENTITY_QUESTIONS[predicate],
                        "fact_produced": predicate,
                        "dns_validity_asserted": False,
                        "dns_resolution_asserted": False,
                        "network_reachability_asserted": False,
                        "availability_asserted": False,
                        "provider_visibility_asserted": False,
                        "host_ownership_asserted": False,
                        "host_uniqueness_asserted": False,
                    },
                )
            )
        return observations

    def _collect_hosts_file_observations(
        self, observed_at: datetime, subject: str, metadata: dict[str, Any]
    ) -> list[Observation]:
        """Collect local /etc/hosts configured mapping evidence only.

        Hosts-file lines are source-scoped local configuration evidence. They do
        not assert DNS truth, resolution, reachability, host uniqueness, alias
        equivalence, ownership, endpoint identity, or host identity.
        """

        entries = self._hosts_file_entries()
        observations: list[Observation] = []
        hosts_metadata = {
            **metadata,
            "source": _HOSTS_FILE_SOURCE,
            "source_path": str(self.etc_hosts),
            "question_answered": _HOSTS_FILE_QUESTION,
            "dns_validity_asserted": False,
            "dns_resolution_asserted": False,
            "network_reachability_asserted": False,
            "availability_asserted": False,
            "host_ownership_asserted": False,
            "host_uniqueness_asserted": False,
            "alias_equivalence_asserted": False,
            "endpoint_identity_asserted": False,
            "host_identity_asserted": False,
        }
        for entry in entries:
            line_number = str(entry["line_number"])
            address = entry["address"]
            canonical_name = entry["names"][0]
            names = entry["names"]
            observations.append(
                self._observation(
                    observed_at,
                    subject,
                    "hosts_file_address_mapping",
                    address,
                    metadata={
                        **hosts_metadata,
                        "fact_produced": "hosts_file_address_mapping",
                    },
                    dimensions={
                        "source": _HOSTS_FILE_SOURCE,
                        "line_number": line_number,
                        "address": address,
                        "canonical_name": canonical_name,
                        "names": " ".join(names),
                    },
                )
            )
            observations.append(
                self._observation(
                    observed_at,
                    subject,
                    "hosts_file_name",
                    canonical_name,
                    metadata={**hosts_metadata, "fact_produced": "hosts_file_name"},
                    dimensions={
                        "source": _HOSTS_FILE_SOURCE,
                        "line_number": line_number,
                        "address": address,
                        "name_index": "0",
                        "name_role": "canonical",
                    },
                )
            )
            for index, alias in enumerate(names[1:], start=1):
                observations.append(
                    self._observation(
                        observed_at,
                        subject,
                        "hosts_file_alias",
                        alias,
                        metadata={
                            **hosts_metadata,
                            "fact_produced": "hosts_file_alias",
                        },
                        dimensions={
                            "source": _HOSTS_FILE_SOURCE,
                            "line_number": line_number,
                            "address": address,
                            "canonical_name": canonical_name,
                            "name_index": str(index),
                            "name_role": "alias",
                        },
                    )
                )
        return observations

    def _hosts_file_entries(self) -> list[dict[str, Any]]:
        text = self._read_text(self.etc_hosts)
        if text is None:
            return []
        entries: list[dict[str, Any]] = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            content = line.split("#", 1)[0].strip()
            if not content:
                continue
            fields = content.split()
            if len(fields) < 2:
                continue
            address = fields[0]
            try:
                ipaddress.ip_address(address)
            except ValueError:
                continue
            entries.append(
                {
                    "line_number": line_number,
                    "address": address,
                    "names": fields[1:],
                }
            )
        return entries

    def _collect_host_description_observations(
        self, observed_at: datetime, hostname: str, metadata: dict[str, Any]
    ) -> list[Observation]:
        """Collect kernel, CPU, and memory description facts from local evidence.

        These observations describe locally reported host substrate values only.
        They do not infer host health, performance adequacy, workload status,
        availability, reachability, supportability, or provider visibility.
        """

        observations: list[Observation] = []
        description_metadata = {
            **metadata,
            "health_asserted": False,
            "performance_asserted": False,
            "performance_adequacy_asserted": False,
            "memory_pressure_asserted": False,
            "workload_status_asserted": False,
            "availability_asserted": False,
            "reachability_asserted": False,
            "network_reachability_asserted": False,
            "supportability_asserted": False,
            "provider_visibility_asserted": False,
        }
        for predicate, value, source_name in self._host_description_values():
            observations.append(
                self._observation(
                    observed_at,
                    hostname,
                    predicate,
                    value,
                    metadata={
                        **description_metadata,
                        "source": source_name,
                        "question_answered": _HOST_DESCRIPTION_QUESTIONS[predicate],
                        "fact_produced": predicate,
                    },
                )
            )
        return observations

    def _host_description_values(self) -> list[tuple[str, Any, str]]:
        """Return directly evidenced kernel, CPU, and memory values."""

        values: list[tuple[str, Any, str]] = []
        kernel_release = _read_bounded_first_line(
            self.proc_root / "sys" / "kernel" / "osrelease"
        )
        if kernel_release is not None:
            values.append(
                ("kernel_release", kernel_release, "/proc/sys/kernel/osrelease")
            )

        kernel_version = _read_bounded_first_line(self.proc_root / "version")
        if kernel_version is not None:
            values.append(("kernel_version", kernel_version, "/proc/version"))

        cpuinfo = self._read_text(self.proc_root / "cpuinfo")
        if cpuinfo:
            cpu_model = self._cpu_model_from_cpuinfo(cpuinfo)
            if cpu_model is not None:
                values.append(("cpu_model", cpu_model, "/proc/cpuinfo"))
            cpu_count = self._cpu_count_from_cpuinfo(cpuinfo)
            if cpu_count is not None:
                values.append(("cpu_count", cpu_count, "/proc/cpuinfo"))
        elif (cpu_count := os.cpu_count()) is not None and cpu_count > 0:
            values.append(("cpu_count", int(cpu_count), "os.cpu_count"))

        meminfo = self._read_text(self.proc_root / "meminfo")
        if meminfo:
            memory_total = self._memory_total_bytes_from_meminfo(meminfo)
            if memory_total is not None:
                values.append(("memory_total_bytes", memory_total, "/proc/meminfo"))
        return values

    @staticmethod
    def _cpu_model_from_cpuinfo(text: str) -> str | None:
        for key in ("model name", "Hardware", "Processor"):
            for line in text.splitlines():
                if ":" not in line:
                    continue
                name, value = line.split(":", 1)
                if name.strip() == key and value.strip():
                    return value.strip()
        return None

    @staticmethod
    def _cpu_count_from_cpuinfo(text: str) -> int | None:
        processor_ids = {
            line.split(":", 1)[1].strip()
            for line in text.splitlines()
            if ":" in line and line.split(":", 1)[0].strip() == "processor"
        }
        if processor_ids:
            return len(processor_ids)
        return None

    @staticmethod
    def _memory_total_bytes_from_meminfo(text: str) -> int | None:
        for line in text.splitlines():
            if not line.startswith("MemTotal:"):
                continue
            fields = line.split()
            if len(fields) < 2 or not fields[1].isdigit():
                return None
            unit = fields[2].lower() if len(fields) > 2 else "kb"
            multiplier = {"kb": 1024, "b": 1}.get(unit)
            if multiplier is None:
                return None
            return int(fields[1]) * multiplier
        return None

    def _collect_network_observations(
        self, observed_at: datetime, hostname: str, metadata: dict[str, Any]
    ) -> list[Observation]:
        observations: list[Observation] = []
        interfaces = self._interface_names()
        ipv4_addresses = self._ipv4_addresses(interfaces)
        ipv6_addresses = self._ipv6_addresses()
        default_gateways = self._default_gateways()
        default_route_interfaces = {route["interface"] for route in default_gateways}
        assignment_methods = self._address_assignment_methods(ipv4_addresses)

        for interface in interfaces:
            dimensions = {"interface": interface}
            observations.append(
                self._observation(
                    observed_at,
                    hostname,
                    "network_interface",
                    interface,
                    metadata={**metadata, "source": "socket.if_nameindex/proc_net_dev"},
                    dimensions=dimensions,
                )
            )
            observations.append(
                self._observation(
                    observed_at,
                    hostname,
                    "interface_role",
                    self._interface_role(interface, default_route_interfaces),
                    metadata={
                        **metadata,
                        "source": "interface_name/proc_net_route",
                        "interface": interface,
                        "default_route": interface in default_route_interfaces,
                        "classification_only": True,
                        "network_reachability_asserted": False,
                        "availability_asserted": False,
                    },
                    dimensions=dimensions,
                )
            )
            operstate = self._read_sys_net_value(interface, "operstate")
            if operstate:
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        "interface_operstate",
                        operstate,
                        metadata={
                            **metadata,
                            "source": "sysfs",
                            "interface": interface,
                        },
                        dimensions=dimensions,
                    )
                )
            mac_address = self._read_sys_net_value(interface, "address")
            if mac_address:
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        "interface_mac_address",
                        mac_address.lower(),
                        metadata={
                            **metadata,
                            "source": "sysfs",
                            "interface": interface,
                        },
                        dimensions=dimensions,
                    )
                )
            mtu = self._read_sys_net_value(interface, "mtu")
            if mtu and mtu.isdigit():
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        "interface_mtu",
                        int(mtu),
                        metadata={
                            **metadata,
                            "source": "sysfs",
                            "interface": interface,
                        },
                        dimensions=dimensions,
                    )
                )
            for address in ipv4_addresses.get(interface, []):
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        "ip_address",
                        address,
                        metadata={
                            **metadata,
                            "source": "SIOCGIFADDR",
                            "interface": interface,
                        },
                        dimensions={**dimensions, "address_family": "ipv4"},
                    )
                )
            assignment_method = assignment_methods.get(interface)
            if assignment_method:
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        "address_assignment_method",
                        assignment_method,
                        metadata={
                            **metadata,
                            "source": "systemd_netif_lease",
                            "interface": interface,
                            "evidence": "matching systemd-networkd DHCP lease",
                        },
                        dimensions={**dimensions, "address_family": "ipv4"},
                    )
                )
            for address in ipv6_addresses.get(interface, []):
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        "ip_address",
                        address,
                        metadata={
                            **metadata,
                            "source": "proc_net_if_inet6",
                            "interface": interface,
                        },
                        dimensions={**dimensions, "address_family": "ipv6"},
                    )
                )

        for route in default_gateways:
            observations.append(
                self._observation(
                    observed_at,
                    hostname,
                    "default_gateway",
                    route["gateway"],
                    metadata={
                        **metadata,
                        "source": "proc_net_route",
                        "interface": route["interface"],
                    },
                    dimensions={
                        "interface": route["interface"],
                        "address_family": "ipv4",
                    },
                )
            )

        for resolver in self._dns_resolvers():
            observations.append(
                self._observation(
                    observed_at,
                    hostname,
                    "dns_resolver",
                    resolver,
                    metadata={**metadata, "source": "resolv_conf"},
                    dimensions={"source": str(self.resolv_conf)},
                )
            )
        for resolver in self._dns_resolver_stubs():
            observations.append(
                self._observation(
                    observed_at,
                    hostname,
                    "dns_resolver_stub",
                    resolver,
                    metadata={
                        **metadata,
                        "source": "resolv_conf",
                        "stub_resolver": True,
                        "upstream_reachability_asserted": False,
                        "dns_resolution_asserted": False,
                    },
                    dimensions={"source": str(self.resolv_conf)},
                )
            )
        for resolver in self._dns_resolver_upstreams():
            observations.append(
                self._observation(
                    observed_at,
                    hostname,
                    "dns_resolver_upstream",
                    resolver,
                    metadata={
                        **metadata,
                        "source": "systemd_resolved_resolv_conf",
                        "stub_resolver": False,
                        "upstream_reachability_asserted": False,
                        "dns_resolution_asserted": False,
                    },
                    dimensions={"source": str(self.systemd_resolv_conf)},
                )
            )

        return observations

    def _collect_storage_observations(
        self, observed_at: datetime, hostname: str, metadata: dict[str, Any]
    ) -> list[Observation]:
        """Collect local block storage topology without managing storage.

        Storage topology facts describe names, parent-child shape, and sysfs
        attributes visible through read-only local files. They do not assert
        device availability, filesystem health, storage health, repairability,
        data safety, redundancy, backup status, or performance adequacy.
        """

        observations: list[Observation] = []
        storage_metadata = {
            **metadata,
            "source": "sysfs_proc_partitions",
            "management_asserted": False,
            "storage_management_asserted": False,
            "filesystem_management_asserted": False,
            "availability_asserted": False,
            "reachability_asserted": False,
            "health_asserted": False,
            "storage_health_asserted": False,
            "filesystem_health_asserted": False,
            "repairability_asserted": False,
            "backup_status_asserted": False,
            "redundancy_asserted": False,
            "data_safety_asserted": False,
            "performance_asserted": False,
            "performance_adequacy_asserted": False,
        }
        for device in self._storage_topology_entries():
            name = device["name"]
            dimensions = {"device": name}
            observations.append(
                self._observation(
                    observed_at,
                    hostname,
                    "block_device",
                    name,
                    metadata={
                        **storage_metadata,
                        "source": device["source"],
                        "question_answered": _STORAGE_QUESTIONS["block_device"],
                        "fact_produced": "block_device",
                    },
                    dimensions=dimensions,
                )
            )
            for predicate in (
                "block_device_size_bytes",
                "block_device_rotational",
                "block_device_removable",
                "block_device_model",
                "block_device_vendor",
            ):
                if predicate not in device:
                    continue
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        predicate,
                        device[predicate],
                        metadata={
                            **storage_metadata,
                            "source": device.get(
                                f"{predicate}_source", device["source"]
                            ),
                            "question_answered": _STORAGE_QUESTIONS[predicate],
                            "fact_produced": predicate,
                        },
                        dimensions=dimensions,
                    )
                )
            for partition in device["partitions"]:
                partition_name = partition["name"]
                partition_dimensions = {"device": partition_name, "parent": name}
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        "partition",
                        partition_name,
                        metadata={
                            **storage_metadata,
                            "source": partition["source"],
                            "question_answered": _STORAGE_QUESTIONS["partition"],
                            "fact_produced": "partition",
                        },
                        dimensions=partition_dimensions,
                    )
                )
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        "block_device_parent",
                        name,
                        metadata={
                            **storage_metadata,
                            "source": partition["source"],
                            "question_answered": _STORAGE_QUESTIONS[
                                "block_device_parent"
                            ],
                            "fact_produced": "block_device_parent",
                            "child_device": partition_name,
                        },
                        dimensions=partition_dimensions,
                    )
                )
                if "block_device_size_bytes" in partition:
                    observations.append(
                        self._observation(
                            observed_at,
                            hostname,
                            "block_device_size_bytes",
                            partition["block_device_size_bytes"],
                            metadata={
                                **storage_metadata,
                                "source": partition.get(
                                    "block_device_size_bytes_source",
                                    partition["source"],
                                ),
                                "question_answered": _STORAGE_QUESTIONS[
                                    "block_device_size_bytes"
                                ],
                                "fact_produced": "block_device_size_bytes",
                            },
                            dimensions=partition_dimensions,
                        )
                    )
        return observations

    def _storage_topology_entries(self) -> list[dict[str, Any]]:
        """Return deterministic block-device topology from sysfs/procfs only."""

        proc_partitions = self._proc_partition_names()
        device_names: set[str] = set()
        try:
            for entry in self.sys_block.iterdir():
                if entry.name:
                    device_names.add(entry.name)
        except OSError:
            device_names.update(self._top_level_proc_partition_names(proc_partitions))

        entries: list[dict[str, Any]] = []
        for name in sorted(device_names):
            sys_path = self.sys_block / name
            entry: dict[str, Any] = {
                "name": name,
                "source": f"/sys/block/{name}",
                "partitions": [],
            }
            self._add_storage_attributes(entry, sys_path, name)
            partitions = self._storage_partitions_for_device(name, sys_path)
            entry["partitions"] = partitions
            entries.append(entry)
        return entries

    def _add_storage_attributes(
        self, entry: dict[str, Any], sys_path: Path, name: str
    ) -> None:
        size_bytes = self._sector_size_bytes(sys_path / "size")
        if size_bytes is not None:
            entry["block_device_size_bytes"] = size_bytes
            entry["block_device_size_bytes_source"] = f"/sys/block/{name}/size"
        rotational = self._sysfs_bool_marker(sys_path / "queue" / "rotational")
        if rotational is not None:
            entry["block_device_rotational"] = rotational
            entry["block_device_rotational_source"] = (
                f"/sys/block/{name}/queue/rotational"
            )
        removable = self._sysfs_bool_marker(sys_path / "removable")
        if removable is not None:
            entry["block_device_removable"] = removable
            entry["block_device_removable_source"] = f"/sys/block/{name}/removable"
        for predicate, filename in (
            ("block_device_model", "model"),
            ("block_device_vendor", "vendor"),
        ):
            value = _read_bounded_first_line(sys_path / "device" / filename)
            if value is not None:
                entry[predicate] = value
                entry[f"{predicate}_source"] = f"/sys/block/{name}/device/{filename}"

    def _storage_partitions_for_device(
        self, device: str, sys_path: Path
    ) -> list[dict[str, Any]]:
        partitions: dict[str, dict[str, Any]] = {}
        try:
            children = list(sys_path.iterdir())
        except OSError:
            children = []
        for child in children:
            if not (child / "partition").exists():
                continue
            partitions[child.name] = {
                "name": child.name,
                "source": f"/sys/block/{device}/{child.name}/partition",
            }
        for name in self._proc_partition_names():
            if self._partition_parent_from_name(name, device) == device:
                partitions.setdefault(
                    name,
                    {"name": name, "source": "/proc/partitions"},
                )
        for name, partition in partitions.items():
            size_bytes = self._sector_size_bytes(self.sys_class_block / name / "size")
            if size_bytes is not None:
                partition["block_device_size_bytes"] = size_bytes
                partition["block_device_size_bytes_source"] = (
                    f"/sys/class/block/{name}/size"
                )
        return [partitions[name] for name in sorted(partitions)]

    def _proc_partition_names(self) -> list[str]:
        text = self._read_text(self.proc_root / "partitions")
        if not text:
            return []
        names: list[str] = []
        for line in text.splitlines():
            fields = line.split()
            if len(fields) != 4 or not all(field.isdigit() for field in fields[:3]):
                continue
            names.append(fields[3])
        return sorted(dict.fromkeys(names))

    def _top_level_proc_partition_names(self, names: list[str]) -> list[str]:
        """Best-effort top-level block device names when sysfs is unavailable."""

        top_level: list[str] = []
        for candidate in names:
            if any(
                self._partition_parent_from_name(candidate, other) == other
                for other in names
                if other != candidate
            ):
                continue
            top_level.append(candidate)
        return sorted(top_level)

    @staticmethod
    def _partition_parent_from_name(name: str, parent: str) -> str | None:
        if name == parent:
            return None
        if parent.startswith("nvme") or parent.startswith("mmcblk"):
            return parent if name.startswith(parent + "p") else None
        return parent if name.startswith(parent) else None

    @staticmethod
    def _sector_size_bytes(path: Path) -> int | None:
        value = _read_bounded_first_line(path)
        if value is None or not value.isdigit():
            return None
        return int(value) * 512

    @staticmethod
    def _sysfs_bool_marker(path: Path) -> str | None:
        value = _read_bounded_first_line(path)
        if value == "0":
            return "false"
        if value == "1":
            return "true"
        return None

    def _collect_listener_observations(
        self, observed_at: datetime, hostname: str, metadata: dict[str, Any]
    ) -> list[Observation]:
        """Collect locally bound TCP/UDP endpoints from procfs only.

        Listener observations describe host topology visible from local kernel
        socket tables. They do not infer reachability, availability,
        responsiveness, endpoint health, process ownership, service ownership,
        application ownership, or external accessibility.
        """

        observations: list[Observation] = []
        listener_metadata = {
            **metadata,
            "source": "/proc/net/{tcp,tcp6,udp,udp6}",
            "availability_asserted": False,
            "reachability_asserted": False,
            "network_reachability_asserted": False,
            "external_accessibility_asserted": False,
            "health_asserted": False,
            "endpoint_health_asserted": False,
            "service_health_asserted": False,
            "responsiveness_asserted": False,
            "traffic_asserted": False,
            "managed_asserted": False,
            "application_owner_asserted": False,
            "process_owner_asserted": False,
            "service_owner_asserted": False,
        }
        for listener in self._listening_socket_entries():
            protocol = listener["protocol"]
            address = listener["address"]
            port = listener["port"]
            endpoint = f"{protocol} {self._format_listener_address(address)}:{port}"
            dimensions = {
                "protocol": protocol,
                "address": address,
                "port": str(port),
                "address_family": listener["address_family"],
            }
            per_listener_metadata = {
                **listener_metadata,
                "source": listener["source"],
                "kernel_state": listener["state"],
                "protocol": protocol,
                "address": address,
                "port": str(port),
            }
            for predicate, value in (
                ("listening_endpoint", endpoint),
                ("listening_protocol", protocol),
                ("listening_address", address),
                ("listening_port", port),
                ("listening_socket_family", listener["address_family"]),
            ):
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        predicate,
                        value,
                        metadata={
                            **per_listener_metadata,
                            "question_answered": _LISTENER_QUESTIONS[predicate],
                            "fact_produced": predicate,
                        },
                        dimensions=dimensions,
                    )
                )
            process = listener.get("process")
            if process is not None:
                for predicate, value in (
                    ("listening_process_id", process["pid"]),
                    ("listening_process_name", process["name"]),
                ):
                    observations.append(
                        self._observation(
                            observed_at,
                            hostname,
                            predicate,
                            value,
                            metadata={
                                **per_listener_metadata,
                                "process_inode": listener["inode"],
                                "process_source": process["source"],
                                "question_answered": _LISTENER_QUESTIONS[predicate],
                                "fact_produced": predicate,
                            },
                            dimensions=dimensions,
                        )
                    )
        return observations

    @staticmethod
    def _format_listener_address(address: str) -> str:
        return f"[{address}]" if ":" in address else address

    def _listening_socket_entries(self) -> list[dict[str, Any]]:
        entries: list[dict[str, Any]] = []
        sources = (
            ("tcp", "ipv4", self.proc_root / "net" / "tcp", "/proc/net/tcp"),
            ("tcp", "ipv6", self.proc_root / "net" / "tcp6", "/proc/net/tcp6"),
            ("udp", "ipv4", self.proc_root / "net" / "udp", "/proc/net/udp"),
            ("udp", "ipv6", self.proc_root / "net" / "udp6", "/proc/net/udp6"),
        )
        inode_processes = self._socket_inode_processes()
        for protocol, family, path, source_name in sources:
            entries.extend(
                self._parse_proc_net_socket_table(
                    protocol, family, path, source_name, inode_processes
                )
            )
        return sorted(
            entries,
            key=lambda item: (
                item["protocol"],
                item["address_family"],
                ipaddress.ip_address(item["address"]),
                item["port"],
                item["source"],
            ),
        )

    def _parse_proc_net_socket_table(
        self,
        protocol: str,
        family: str,
        path: Path,
        source_name: str,
        inode_processes: dict[str, dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        text = self._read_text(path)
        if not text:
            return []
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines or "local_address" not in lines[0]:
            return []
        entries: list[dict[str, Any]] = []
        for line in lines[1:]:
            fields = line.split()
            if len(fields) < 10 or ":" not in fields[1]:
                return []
            local_address, local_port = fields[1].split(":", 1)
            state = fields[3].upper()
            if protocol == "tcp" and state != "0A":
                continue
            try:
                port = int(local_port, 16)
            except ValueError:
                return []
            if port <= 0:
                continue
            address = self._decode_proc_net_address(local_address, family)
            if address is None:
                return []
            inode = fields[9]
            entry = {
                "protocol": protocol,
                "address_family": family,
                "address": address,
                "port": port,
                "state": state,
                "inode": inode,
                "source": source_name,
            }
            process = (inode_processes or {}).get(inode)
            if process is not None:
                entry["process"] = process
            entries.append(entry)
        return entries

    def _socket_inode_processes(self) -> dict[str, dict[str, Any]]:
        """Return directly observable process metadata keyed by socket inode.

        This links only procfs fd symlinks of the form ``socket:[inode]`` to
        numeric /proc process directories and their ``comm`` names. Missing or
        unreadable process information is preserved as absence.
        """

        processes: dict[str, dict[str, Any]] = {}
        if not self.proc_root.exists():
            return processes
        try:
            process_dirs = list(self.proc_root.iterdir())
        except OSError:
            return processes
        for process_dir in process_dirs:
            if not process_dir.name.isdigit() or not process_dir.is_dir():
                continue
            try:
                pid = int(process_dir.name)
            except ValueError:
                continue
            name = self._read_text(process_dir / "comm", max_bytes=4096)
            if not name:
                continue
            process = {
                "pid": pid,
                "name": name.splitlines()[0],
                "source": f"/proc/{pid}/fd and /proc/{pid}/comm",
            }
            fd_dir = process_dir / "fd"
            if not fd_dir.is_dir():
                continue
            try:
                fd_paths = list(fd_dir.iterdir())
            except OSError:
                continue
            for fd_path in fd_paths:
                try:
                    target = os.readlink(fd_path)
                except OSError:
                    continue
                match = re.fullmatch(r"socket:\[(\d+)\]", target)
                if match:
                    processes.setdefault(match.group(1), process)
        return processes

    @staticmethod
    def _decode_proc_net_address(value: str, family: str) -> str | None:
        try:
            raw = bytes.fromhex(value)
        except ValueError:
            return None
        if family == "ipv4":
            if len(raw) != 4:
                return None
            return str(ipaddress.IPv4Address(raw[::-1]))
        if family == "ipv6":
            if len(raw) != 16:
                return None
            network_order = b"".join(
                raw[index : index + 4][::-1] for index in range(0, 16, 4)
            )
            return str(ipaddress.IPv6Address(network_order))
        return None

    def _collect_local_user_observations(
        self, observed_at: datetime, hostname: str, metadata: dict[str, Any]
    ) -> list[Observation]:
        """Collect declared local user and group records from passwd/group only.

        These observations describe local account and group configuration records.
        They do not infer login activity, SSH access, sudo authorization, account
        safety, password status, account enablement, human/system classification,
        service ownership, privilege, reachability, or availability.
        """

        observations: list[Observation] = []
        boundary_metadata = {
            **metadata,
            "read_only": True,
            "local_only": True,
            "shell_execution": False,
            "subprocess_execution": False,
            "privilege_escalation": False,
            "network_probe": False,
            "network_connection": False,
            "login_activity_asserted": False,
            "active_session_asserted": False,
            "ssh_access_asserted": False,
            "sudo_access_asserted": False,
            "sudoers_policy_asserted": False,
            "privilege_asserted": False,
            "account_safety_asserted": False,
            "account_enabled_asserted": False,
            "password_status_asserted": False,
            "availability_asserted": False,
            "human_user_asserted": False,
            "system_user_asserted": False,
            "service_account_asserted": False,
            "shadow_inspected": False,
            "sudoers_inspected": False,
            "authorized_keys_inspected": False,
            "pam_inspected": False,
            "utmp_wtmp_inspected": False,
            "loginctl_inspected": False,
        }
        for user in self._local_passwd_entries():
            username = user["username"]
            uid = user["uid"]
            gid = user["gid"]
            dimensions = {"username": username, "uid": str(uid)}
            user_metadata = {
                **boundary_metadata,
                "source": user["source"],
                "source_file": "/etc/passwd",
                "username": username,
                "uid": str(uid),
                "gid": str(gid),
            }
            for predicate, value in (
                ("user_account", username),
                ("user_uid", uid),
                ("user_primary_gid", gid),
                ("user_home_directory", user["home_directory"]),
                ("user_shell", user["shell"]),
            ):
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        predicate,
                        value,
                        metadata={
                            **user_metadata,
                            "question_answered": _LOCAL_USER_QUESTIONS[predicate],
                            "fact_produced": predicate,
                        },
                        dimensions=dimensions,
                    )
                )
        for group in self._local_group_entries():
            groupname = group["groupname"]
            gid = group["gid"]
            dimensions = {"groupname": groupname, "gid": str(gid)}
            group_metadata = {
                **boundary_metadata,
                "source": group["source"],
                "source_file": "/etc/group",
                "groupname": groupname,
                "gid": str(gid),
            }
            for predicate, value in (
                ("group_account", groupname),
                ("group_gid", gid),
            ):
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        predicate,
                        value,
                        metadata={
                            **group_metadata,
                            "question_answered": _LOCAL_USER_QUESTIONS[predicate],
                            "fact_produced": predicate,
                        },
                        dimensions=dimensions,
                    )
                )
            for username in group["members"]:
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        "group_member",
                        username,
                        metadata={
                            **group_metadata,
                            "username": username,
                            "question_answered": _LOCAL_USER_QUESTIONS["group_member"],
                            "fact_produced": "group_member",
                        },
                        dimensions={**dimensions, "username": username},
                    )
                )
        return observations

    def _local_passwd_entries(self) -> list[dict[str, Any]]:
        return self._parse_passwd_text(self._read_text(self.etc_passwd), "/etc/passwd")

    def _local_group_entries(self) -> list[dict[str, Any]]:
        return self._parse_group_text(self._read_text(self.etc_group), "/etc/group")

    @staticmethod
    def _parse_passwd_text(text: str | None, source_name: str) -> list[dict[str, Any]]:
        if not text:
            return []
        entries: list[dict[str, Any]] = []
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            fields = stripped.split(":")
            if len(fields) < 7:
                continue
            username, _password, uid_text, gid_text, _gecos, home_directory, shell = (
                fields[:7]
            )
            if not username:
                continue
            try:
                uid = int(uid_text)
                gid = int(gid_text)
            except ValueError:
                continue
            entries.append(
                {
                    "username": username,
                    "uid": uid,
                    "gid": gid,
                    "home_directory": home_directory,
                    "shell": shell,
                    "source": source_name,
                }
            )
        return sorted(
            entries, key=lambda item: (item["username"], item["uid"], item["gid"])
        )

    @staticmethod
    def _parse_group_text(text: str | None, source_name: str) -> list[dict[str, Any]]:
        if not text:
            return []
        entries: list[dict[str, Any]] = []
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            fields = stripped.split(":")
            if len(fields) < 4:
                continue
            groupname, _password, gid_text, members_text = fields[:4]
            if not groupname:
                continue
            try:
                gid = int(gid_text)
            except ValueError:
                continue
            members = sorted(
                member.strip() for member in members_text.split(",") if member.strip()
            )
            entries.append(
                {
                    "groupname": groupname,
                    "gid": gid,
                    "members": members,
                    "source": source_name,
                }
            )
        return sorted(entries, key=lambda item: (item["groupname"], item["gid"]))

    def _collect_mount_observations(
        self, observed_at: datetime, hostname: str, metadata: dict[str, Any]
    ) -> list[Observation]:
        """Collect mounted filesystem facts from /proc/mounts only.

        Mount facts describe local kernel mount-table entries. They do not
        assert health, writability, reachability, storage availability, or
        device accessibility.
        """

        observations: list[Observation] = []
        for mount in self._mount_entries():
            mount_point = mount["mount_point"]
            dimensions = {"mount_point": mount_point}
            mount_metadata = {
                **metadata,
                "source": mount["source"],
                "mount_point": mount_point,
                "health_asserted": False,
                "writability_asserted": False,
                "reachability_asserted": False,
                "network_reachability_asserted": False,
                "availability_asserted": False,
                "device_health_asserted": False,
                "device_accessibility_asserted": False,
            }
            for predicate, value in (
                ("mount_point", mount_point),
                ("filesystem_type", mount["filesystem_type"]),
                ("mounted_device", mount["mounted_device"]),
            ):
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        predicate,
                        value,
                        metadata={
                            **mount_metadata,
                            "question_answered": _MOUNT_QUESTIONS[predicate],
                            "fact_produced": predicate,
                        },
                        dimensions=dimensions,
                    )
                )
            for option in mount["mount_options"]:
                observations.append(
                    self._observation(
                        observed_at,
                        hostname,
                        "mount_option",
                        option,
                        metadata={
                            **mount_metadata,
                            "question_answered": _MOUNT_QUESTIONS["mount_option"],
                            "fact_produced": "mount_option",
                        },
                        dimensions={**dimensions, "mount_option": option},
                    )
                )
        return observations

    def _mount_entries(self) -> list[dict[str, Any]]:
        """Parse /proc/mounts without invoking mount/findmnt or other commands."""

        text = self._read_text(self.proc_root / "mounts")
        if not text:
            return []
        entries: list[dict[str, Any]] = []
        for line in text.splitlines():
            fields = line.split()
            if len(fields) < 4:
                continue
            device, mount_point, filesystem_type, options = fields[:4]
            decoded_options = sorted(
                dict.fromkeys(
                    self._decode_proc_mount_field(option)
                    for option in options.split(",")
                    if option
                )
            )
            entries.append(
                {
                    "mounted_device": self._decode_proc_mount_field(device),
                    "mount_point": self._decode_proc_mount_field(mount_point),
                    "filesystem_type": self._decode_proc_mount_field(filesystem_type),
                    "mount_options": decoded_options,
                    "source": "/proc/mounts",
                }
            )
        return sorted(
            entries,
            key=lambda item: (
                item["mount_point"],
                item["mounted_device"],
                item["filesystem_type"],
            ),
        )

    @staticmethod
    def _decode_proc_mount_field(value: str) -> str:
        """Decode procfs octal escapes such as \040 for spaces."""

        return _PROC_MOUNT_ESCAPE_RE.sub(
            lambda match: chr(int(match.group(1), 8)), value
        )

    def _interface_role(
        self, interface: str, default_route_interfaces: set[str]
    ) -> str:
        """Classify a local interface without implying reachability."""

        lowered = interface.lower()
        if interface in default_route_interfaces:
            return "primary"
        if lowered == "lo":
            return "loopback"
        if lowered.startswith(("tailscale", "wg")):
            return "vpn"
        if lowered.startswith(("docker", "br-", "veth")):
            return "container"
        if lowered.startswith("virbr"):
            return "virtual"
        return "secondary"

    def _address_assignment_methods(
        self, ipv4_addresses: dict[str, list[str]]
    ) -> dict[str, str]:
        """Return assignment methods only when read-only evidence is explicit.

        DHCP is identified from systemd-networkd lease files under
        /run/systemd/netif/leases by matching a lease ADDRESS to an observed
        IPv4 address for the interface with the same sysfs ifindex. Static
        assignment generally requires manager-specific config interpretation, so
        it is intentionally left unknown unless a future explicit evidence source
        is added.
        """

        methods: dict[str, str] = {}
        for interface, addresses in ipv4_addresses.items():
            if not addresses:
                continue
            ifindex = self._read_sys_net_value(interface, "ifindex")
            if not ifindex:
                continue
            lease_text = self._read_text(self.systemd_lease_dir / ifindex)
            if not lease_text:
                continue
            lease_values = self._parse_key_value_lines(lease_text)
            if lease_values.get("ADDRESS") in set(addresses):
                methods[interface] = "dhcp"
        return methods

    @staticmethod
    def _parse_key_value_lines(text: str) -> dict[str, str]:
        values: dict[str, str] = {}
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            values[key.strip()] = value.strip()
        return values

    def _interface_names(self) -> list[str]:
        names = {name for _, name in socket.if_nameindex()}
        proc_net_dev = self._read_text(self.proc_root / "net" / "dev")
        if proc_net_dev:
            for line in proc_net_dev.splitlines()[2:]:
                if ":" not in line:
                    continue
                names.add(line.split(":", 1)[0].strip())
        return sorted(name for name in names if name)

    def _ipv4_addresses(self, interfaces: list[str]) -> dict[str, list[str]]:
        addresses: dict[str, list[str]] = {}
        for interface in interfaces:
            address = self._ipv4_address_for_interface(interface)
            if address:
                addresses[interface] = [address]
        return addresses

    def _ipv4_address_for_interface(self, interface: str) -> str | None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            request = struct.pack("256s", interface.encode("utf-8")[:15])
            result = fcntl.ioctl(sock.fileno(), 0x8915, request)  # SIOCGIFADDR
            return socket.inet_ntoa(result[20:24])
        except OSError:
            return None
        finally:
            sock.close()

    def _ipv6_addresses(self) -> dict[str, list[str]]:
        addresses: dict[str, list[str]] = {}
        text = self._read_text(self.proc_root / "net" / "if_inet6")
        if not text:
            return addresses
        for line in text.splitlines():
            fields = line.split()
            if len(fields) < 6:
                continue
            raw_address, _idx, _prefix, _scope, _flags, interface = fields[:6]
            if len(raw_address) != 32:
                continue
            try:
                address = str(ipaddress.IPv6Address(int(raw_address, 16)))
            except ValueError:
                continue
            addresses.setdefault(interface, []).append(address)
        return {interface: sorted(values) for interface, values in addresses.items()}

    def _default_gateways(self) -> list[dict[str, str]]:
        routes: list[dict[str, str]] = []
        text = self._read_text(self.proc_root / "net" / "route")
        if not text:
            return routes
        for line in text.splitlines()[1:]:
            fields = line.split()
            if len(fields) < 3:
                continue
            interface, destination, gateway = fields[:3]
            if destination != "00000000" or gateway == "00000000":
                continue
            try:
                gateway_address = socket.inet_ntoa(bytes.fromhex(gateway)[::-1])
            except (OSError, ValueError):
                continue
            routes.append({"interface": interface, "gateway": gateway_address})
        return sorted(routes, key=lambda item: (item["interface"], item["gateway"]))

    def _dns_resolvers(self) -> list[str]:
        return self._nameservers_from_file(self.resolv_conf)

    def _dns_resolver_stubs(self) -> list[str]:
        return [
            resolver
            for resolver in self._nameservers_from_file(self.resolv_conf)
            if self._is_loopback_address(resolver)
        ]

    def _dns_resolver_upstreams(self) -> list[str]:
        upstreams = [
            resolver
            for resolver in self._nameservers_from_file(self.systemd_resolv_conf)
            if not self._is_loopback_address(resolver)
        ]
        return sorted(dict.fromkeys(upstreams))

    def _nameservers_from_file(self, path: Path) -> list[str]:
        resolvers: list[str] = []
        text = self._read_text(path)
        if not text:
            return resolvers
        for line in text.splitlines():
            stripped = line.split("#", 1)[0].strip()
            if not stripped:
                continue
            fields = stripped.split()
            if len(fields) >= 2 and fields[0] == "nameserver":
                resolvers.append(fields[1])
        return sorted(dict.fromkeys(resolvers))

    @staticmethod
    def _is_loopback_address(value: str) -> bool:
        try:
            return ipaddress.ip_address(value).is_loopback
        except ValueError:
            return False

    def _read_sys_net_value(self, interface: str, filename: str) -> str | None:
        text = self._read_text(self.sys_class_net / interface / filename)
        return text.strip() if text is not None else None

    def _read_text(
        self, path: Path, *, max_bytes: int = _LOCAL_READ_MAX_BYTES
    ) -> str | None:
        if max_bytes <= 0:
            return None
        try:
            path_stat = path.stat()
        except OSError:
            stat_size_known = False
            stat_size = 0
        else:
            stat_size_known = stat.S_ISREG(path_stat.st_mode)
            stat_size = path_stat.st_size
            if stat_size_known and stat_size > max_bytes:
                return None
        try:
            with path.open("rb") as handle:
                raw = handle.read(max_bytes)
        except OSError:
            return None
        if not raw:
            return None
        if not stat_size_known and len(raw) == max_bytes:
            return None
        return raw.decode("utf-8", errors="replace")

    def _observation(
        self,
        observed_at: datetime,
        subject: str,
        predicate: str,
        value: Any,
        *,
        metadata: dict[str, Any],
        dimensions: dict[str, str] | None = None,
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
            dimensions=dimensions or {},
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
        self.last_collection_counters: dict[str, Any] = {}

    def collect(self) -> list[Observation]:
        """Collect safe Prometheus metrics, returning [] if unreachable."""

        seed_collected_at = datetime.now(timezone.utc)
        observations: list[Observation] = []
        self.last_error = None
        api_fetch_seconds = 0.0
        metric_families = 0
        samples_processed = 0
        for query in self.SAFE_QUERIES:
            try:
                query_started = time.perf_counter()
                payload = self._query(query)
                api_fetch_seconds += time.perf_counter() - query_started
            except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
                self.last_error = f"{type(exc).__name__}: {exc}"
                return []
            metric_families += 1
            result = payload["data"]["result"]
            samples_processed += len(result) if isinstance(result, list) else 0
            observations.extend(
                self._observations_from_query(query, payload, seed_collected_at)
            )
        self.last_collection_counters = {
            "http_api_fetch_seconds": api_fetch_seconds,
            "metric_families_processed": metric_families,
            "samples_processed": samples_processed,
            "observations_generated": len(observations),
        }
        return observations

    def _query(self, query: str) -> dict[str, Any]:
        if query not in self.SAFE_QUERIES:
            raise ValueError(f"Prometheus query is not allowlisted: {query}")
        url = urljoin(self.base_url, "api/v1/query") + "?" + urlencode({"query": query})
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
        self, query: str, payload: dict[str, Any], seed_collected_at: datetime
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
            sample_timestamp_raw = value[0]
            sample_timestamp = _prometheus_sample_timestamp(sample_timestamp_raw)
            if sample_timestamp is None:
                continue
            sample_value = value[1]
            metadata = {
                "collector": "PrometheusObservationSource",
                "source_name": "prometheus",
                "prometheus_base_url": self.base_url.rstrip("/"),
                "prometheus_metric": query,
                "metric_labels": dict(metric),
                "read_only": True,
                "http_method": "GET",
                "prometheus_sample_timestamp": sample_timestamp.isoformat(),
                "prometheus_sample_timestamp_raw": sample_timestamp_raw,
                "source_observed_at": sample_timestamp.isoformat(),
                "source_time_kind": "sample_time",
                "source_time_authority": "prometheus",
                "seed_collected_at": seed_collected_at.isoformat(),
                "seed_collection_time_authority": "seed_local_clock",
                "query_temporal_intent": "current_instant",
            }
            # Only node_uname_info is authoritative for stable host identity.
            # Other metrics remain endpoint-scoped and do not participate in
            # endpoint alias normalization.
            if query == "node_uname_info":
                metadata["instance"] = instance
                nodename = metric.get("nodename")
                if isinstance(nodename, str) and nodename.strip():
                    metadata["nodename"] = nodename.strip()
            if query == "up":
                job = metric.get("job")
                if isinstance(job, str) and job.strip():
                    observations.append(
                        self._observation(
                            sample_timestamp,
                            instance,
                            "endpoint_role",
                            job.strip(),
                            metadata,
                        )
                    )
                observations.append(
                    self._observation(
                        sample_timestamp,
                        instance,
                        "up",
                        _prometheus_int(sample_value),
                        metadata,
                    )
                )
            elif query == "node_uname_info":
                os_value = _prometheus_os_from_uname(metric)
                if os_value is not None:
                    os_metadata = dict(metadata)
                    if is_endpoint_subject(instance):
                        os_metadata.update(
                            {
                                "fact_promotion_suppressed": True,
                                "fact_promotion_suppressed_reason": (
                                    "prometheus_node_uname_os_endpoint_subject"
                                ),
                            }
                        )
                    observations.append(
                        self._observation(
                            sample_timestamp, instance, "os", os_value, os_metadata
                        )
                    )
            elif query == "node_filesystem_avail_bytes":
                observations.append(
                    self._observation(
                        sample_timestamp,
                        instance,
                        "filesystem_avail_bytes",
                        _prometheus_int(sample_value),
                        metadata,
                    )
                )
            elif query == "node_filesystem_size_bytes":
                observations.append(
                    self._observation(
                        sample_timestamp,
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
            dimensions=_filesystem_dimensions(predicate, metadata),
        )


def _filesystem_dimensions(predicate: str, metadata: dict[str, Any]) -> dict[str, str]:
    """Return the stable identity labels for one filesystem measurement series."""

    if predicate not in {"filesystem_avail_bytes", "filesystem_size_bytes"}:
        return {}
    labels = metadata.get("metric_labels", {})
    if not isinstance(labels, dict):
        return {}
    return {
        key: value
        for key in ("mountpoint", "device", "fstype")
        if isinstance((value := labels.get(key)), str) and value
    }


def _prometheus_sample_timestamp(value: Any) -> datetime | None:
    """Parse a Prometheus vector sample timestamp as UTC, or skip if malformed."""

    try:
        timestamp = float(str(value))
    except (TypeError, ValueError):
        return None
    if not math.isfinite(timestamp):
        return None
    try:
        return datetime.fromtimestamp(timestamp, timezone.utc)
    except (OverflowError, OSError, ValueError):
        return None


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


class SystemdObservationSource:
    """Read-only systemd observation source using systemctl machine output.

    The source records only systemd-reported unit identity, runtime state,
    substate, and unit-file enablement state. It does not interpret health,
    ownership, intent, dependencies, or desired state.
    """

    name = "systemd"
    source_type: ObservationSourceType = "discovery"

    def __init__(
        self,
        *,
        observed_at: datetime | None = None,
        command_runner: Any | None = None,
        hostname: str | None = None,
    ) -> None:
        self.observed_at = observed_at
        self.command_runner = command_runner or self._run_command
        self.hostname = hostname
        self.last_collection_counters: dict[str, Any] = {}

    def collect(self) -> list[Observation]:
        """Return observations for units reported by systemd."""

        observed_at = self.observed_at or datetime.now(timezone.utc)
        subject_host = self.hostname or platform.node() or "localhost"
        try:
            runtime_units = self._collect_runtime_units()
            unit_file_states = self._collect_unit_file_states()
        except (OSError, subprocess.CalledProcessError):
            self.last_collection_counters = {
                "units_observed": 0,
                "runtime_units_observed": 0,
                "unit_files_observed": 0,
                "collection_error": True,
            }
            return []
        unit_names = sorted(set(runtime_units) | set(unit_file_states))
        observations: list[Observation] = []
        metadata = {
            "source_name": self.name,
            "collector": "SystemdObservationSource",
            "read_only": True,
            "local_only": True,
            "observation_surface": "systemd",
            "shell_execution": False,
            "privilege_escalation": False,
            "service_health_asserted": False,
            "desired_state_asserted": False,
            "operator_intent_asserted": False,
            "ownership_asserted": False,
        }
        for unit_name in unit_names:
            dimensions = {"unit": unit_name}
            unit_metadata = {**metadata, "unit": unit_name}
            observations.append(
                self._observation(
                    observed_at,
                    subject_host,
                    "systemd_unit",
                    unit_name,
                    unit_metadata,
                    dimensions,
                )
            )
            runtime = runtime_units.get(unit_name, {})
            for source_key, predicate in (
                ("active", "systemd_active_state"),
                ("sub", "systemd_sub_state"),
            ):
                value = _systemd_string(runtime.get(source_key))
                if value is not None:
                    observations.append(
                        self._observation(
                            observed_at,
                            subject_host,
                            predicate,
                            value,
                            unit_metadata,
                            dimensions,
                        )
                    )
            unit_file_state = _systemd_string(unit_file_states.get(unit_name))
            if unit_file_state is not None:
                observations.append(
                    self._observation(
                        observed_at,
                        subject_host,
                        "systemd_unit_file_state",
                        unit_file_state,
                        unit_metadata,
                        dimensions,
                    )
                )
        self.last_collection_counters = {
            "units_observed": len(unit_names),
            "runtime_units_observed": len(runtime_units),
            "unit_files_observed": len(unit_file_states),
        }
        return observations

    def _collect_runtime_units(self) -> dict[str, dict[str, Any]]:
        output = self.command_runner(
            [
                "systemctl",
                "list-units",
                "--all",
                "--output=json",
                "--no-pager",
                "--plain",
            ]
        )
        units: dict[str, dict[str, Any]] = {}
        for entry in _systemd_json_rows(output):
            unit = _systemd_string(entry.get("unit") or entry.get("UNIT"))
            if unit is None:
                continue
            units[unit] = {
                "active": entry.get("active") or entry.get("ACTIVE"),
                "sub": entry.get("sub") or entry.get("SUB"),
            }
        return units

    def _collect_unit_file_states(self) -> dict[str, str]:
        output = self.command_runner(
            [
                "systemctl",
                "list-unit-files",
                "--output=json",
                "--no-pager",
                "--plain",
            ]
        )
        states: dict[str, str] = {}
        for entry in _systemd_json_rows(output):
            unit = _systemd_string(entry.get("unit_file") or entry.get("UNIT FILE"))
            state = _systemd_string(entry.get("state") or entry.get("STATE"))
            if unit is not None and state is not None:
                states[unit] = state
        return states

    @staticmethod
    def _run_command(command: list[str]) -> str:
        completed = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return completed.stdout

    def _observation(
        self,
        observed_at: datetime,
        subject: str,
        predicate: str,
        value: Any,
        metadata: dict[str, Any],
        dimensions: dict[str, str],
    ) -> Observation:
        return Observation(
            id=new_id("obs_systemd"),
            source_type=self.source_type,
            observed_at=observed_at,
            subject=subject,
            predicate=predicate,
            value=value,
            confidence=1.0,
            metadata=metadata,
            dimensions=dimensions,
        )


def _systemd_json_rows(output: str) -> list[dict[str, Any]]:
    try:
        payload = json.loads(output or "[]")
    except json.JSONDecodeError:
        return []
    if not isinstance(payload, list):
        return []
    return [entry for entry in payload if isinstance(entry, dict)]


def _systemd_string(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


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
        status_consumer: ExecutionStatusConsumer | None = None,
        diagnostics: list[ObservationIngestionDiagnostics] | None = None,
    ) -> list[Fact]:
        """Collect and ingest all observations from a source.

        Collection and validation complete before any events are appended so a
        failing or malformed source cannot partially modify runtime state.
        """

        lifecycle = ObservationProducerLifecycle(status_consumer, source.name)
        total_started = time.perf_counter()
        lifecycle.collecting()
        collect_started = time.perf_counter()
        observations = list(source.collect())
        collect_seconds = time.perf_counter() - collect_started
        lifecycle.collected(len(observations))
        lifecycle.normalizing(len(observations))
        normalize_started = time.perf_counter()
        normalized = [
            self._normalize_observation(source, observation)
            for observation in observations
        ]
        if self.normalization_pipeline is not None:
            state = StateProjector(self.ingestor.ledger).project(workspace_id)
            normalized = self.normalization_pipeline.normalize(normalized, state=state)
        normalize_seconds = time.perf_counter() - normalize_started
        lifecycle.normalized(len(normalized))

        lifecycle.ingesting(len(normalized))
        ingest_started = time.perf_counter()
        facts = self.ingestor.ingest_many(
            normalized,
            workspace_id,
            actor=actor,
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
            status_consumer=status_consumer,
        )
        ingest_seconds = time.perf_counter() - ingest_started
        lifecycle.completed(len(normalized))
        promoted_count = sum(1 for fact in facts if fact is not None)
        if diagnostics is not None:
            diagnostics.append(
                ObservationIngestionDiagnostics(
                    source_name=source.name,
                    source_collection_seconds=collect_seconds,
                    normalization_seconds=normalize_seconds,
                    event_generation_and_ledger_write_seconds=ingest_seconds,
                    total_seconds=time.perf_counter() - total_started,
                    total_observations=len(normalized),
                    total_events=(2 * len(normalized)) + promoted_count,
                    facts_promoted=promoted_count,
                    source_counters=dict(
                        getattr(source, "last_collection_counters", {})
                    ),
                )
            )
        return [fact for fact in facts if fact is not None]

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
