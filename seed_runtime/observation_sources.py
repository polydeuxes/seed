"""Observation source adapters and collection service."""

from __future__ import annotations

import fcntl
import ipaddress
import json
import os
import re
import platform
import shutil
import socket
import struct
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


_IDENTITY_QUESTIONS = {
    "hostname": "What hostname is configured locally?",
    "machine_id": "What machine-id is recorded locally?",
    "boot_id": "What boot-id is recorded for the current local boot?",
    "fqdn": "What fully qualified hostname is explicitly configured locally?",
}

_MOUNT_QUESTIONS = {
    "mount_point": "What mount points currently exist?",
    "filesystem_type": "What filesystem type is mounted?",
    "mounted_device": "Which device backs the mount?",
    "mount_option": "What mount options are recorded for the mount?",
}

_HOST_DESCRIPTION_QUESTIONS = {
    "kernel_release": "What kernel release is this host running?",
    "kernel_version": "What kernel version string is reported locally?",
    "cpu_model": "What CPU model is reported locally?",
    "cpu_count": "How many CPUs are visible locally?",
    "memory_total_bytes": "How much total memory is reported locally?",
}

_PROC_MOUNT_ESCAPE_RE = re.compile(r"\\([0-7]{3})")


def _read_bounded_first_line(path: Path, *, max_bytes: int = 4096) -> str | None:
    try:
        with path.open("rb") as handle:
            raw = handle.read(max_bytes)
    except OSError:
        return None
    text = raw.decode("utf-8", errors="replace").splitlines()[0].strip() if raw else ""
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
        etc_hostname: str | Path = "/etc/hostname",
        machine_id: str | Path = "/etc/machine-id",
        resolv_conf: str | Path = "/etc/resolv.conf",
        systemd_resolv_conf: str | Path = "/run/systemd/resolve/resolv.conf",
        systemd_stub_resolv_conf: str | Path = "/run/systemd/resolve/stub-resolv.conf",
        systemd_resolved_conf: str | Path = "/etc/systemd/resolved.conf",
        systemd_lease_dir: str | Path = "/run/systemd/netif/leases",
    ) -> None:
        self.name = name
        self.proc_root = Path(proc_root)
        self.sys_class_net = Path(sys_class_net)
        self.etc_hostname = Path(etc_hostname)
        self.machine_id = Path(machine_id)
        self.resolv_conf = Path(resolv_conf)
        self.systemd_resolv_conf = Path(systemd_resolv_conf)
        self.systemd_stub_resolv_conf = Path(systemd_stub_resolv_conf)
        self.systemd_resolved_conf = Path(systemd_resolved_conf)
        self.systemd_lease_dir = Path(systemd_lease_dir)

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
        return observations

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

    def _read_text(self, path: Path) -> str | None:
        try:
            return path.read_text(encoding="utf-8")
        except OSError:
            return None

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
                "source_name": "prometheus",
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
                metadata["instance"] = instance
                nodename = metric.get("nodename")
                if isinstance(nodename, str) and nodename.strip():
                    metadata["nodename"] = nodename.strip()
            if query == "up":
                job = metric.get("job")
                if isinstance(job, str) and job.strip():
                    observations.append(
                        self._observation(
                            observed_at,
                            instance,
                            "endpoint_role",
                            job.strip(),
                            metadata,
                        )
                    )
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
            state = StateProjector(self.ingestor.ledger).project(workspace_id)
            normalized = self.normalization_pipeline.normalize(normalized, state=state)

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
