"""Local package observation helpers.

This module keeps package observation emission generic while isolating dpkg status
parsing as the first narrow package adapter.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from seed_runtime.observations import Observation, ObservationSourceType
from seed_runtime.ids import new_id

_DPKG_INSTALLED_STATUS = "install ok installed"
_DPKG_MANAGER = "dpkg"
_PACKAGE_PREDICATES = (
    "package_installed",
    "package_version",
    "package_architecture",
    "package_manager",
)


@dataclass(frozen=True)
class PackageRecord:
    """Normalized package evidence independent of a package-manager wire format."""

    name: str
    manager: str
    installed: bool = True
    version: str | None = None
    architecture: str | None = None


def parse_dpkg_status(text: str) -> list[PackageRecord]:
    """Parse dpkg status database text into normalized installed package records.

    Only records with ``Status: install ok installed`` become PackageRecord
    instances. Malformed records and records missing Package or Status are
    skipped safely.
    """

    records: list[PackageRecord] = []
    for raw_record in _split_dpkg_records(text):
        fields = _parse_dpkg_record(raw_record)
        if fields is None:
            continue
        package_name = fields.get("Package")
        status = fields.get("Status")
        if not package_name or not status:
            continue
        if status != _DPKG_INSTALLED_STATUS:
            continue
        records.append(
            PackageRecord(
                name=package_name,
                manager=_DPKG_MANAGER,
                installed=True,
                version=fields.get("Version") or None,
                architecture=fields.get("Architecture") or None,
            )
        )
    return records


def package_records_to_observations(
    host: str,
    records: list[PackageRecord],
    observed_at: datetime,
    source_type: ObservationSourceType,
) -> list[Observation]:
    """Convert normalized installed package records into generic facts."""

    observations: list[Observation] = []
    for record in records:
        if not record.installed or not record.name or not record.manager:
            continue
        dimensions = {
            "package_name": record.name,
            "package_manager": record.manager,
        }
        metadata = {
            "collector": "LocalHostObservationSource",
            "source_adapter": "dpkg_status",
            "source_file": "/var/lib/dpkg/status",
            "read_only": True,
            "local_only": True,
            "shell_execution": False,
            "subprocess_execution": False,
            "privilege_escalation": False,
            "network_probe": False,
            "network_connection": False,
            "package_manager_cli_called": False,
            "repository_inspected": False,
            "lock_inspected": False,
            "service_inferred": False,
            "capability_inferred": False,
            "process_inferred": False,
            "port_inferred": False,
            "vulnerability_inferred": False,
            "patch_status_inferred": False,
        }
        values: list[tuple[str, Any]] = [("package_installed", record.name)]
        if record.version:
            values.append(("package_version", record.version))
        if record.architecture:
            values.append(("package_architecture", record.architecture))
        values.append(("package_manager", record.manager))
        for predicate, value in values:
            observations.append(
                Observation(
                    id=new_id("obs_local_package"),
                    source_type=source_type,
                    observed_at=observed_at,
                    subject=host,
                    predicate=predicate,
                    value=value,
                    confidence=1.0,
                    metadata={
                        **metadata,
                        "fact_produced": predicate,
                        "question_answered": _question_for_predicate(predicate),
                    },
                    dimensions=dimensions,
                )
            )
    return observations


def _split_dpkg_records(text: str) -> list[list[str]]:
    records: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.strip() == "":
            if current:
                records.append(current)
                current = []
            continue
        current.append(line)
    if current:
        records.append(current)
    return records


def _parse_dpkg_record(lines: list[str]) -> dict[str, str] | None:
    fields: dict[str, str] = {}
    current_field: str | None = None
    for line in lines:
        if line.startswith((" ", "\t")):
            if current_field is None:
                return None
            fields[current_field] = f"{fields[current_field]}\n{line[1:]}"
            continue
        if ":" not in line:
            return None
        field, value = line.split(":", 1)
        field = field.strip()
        if not field:
            return None
        fields[field] = value.strip()
        current_field = field
    return fields


def _question_for_predicate(predicate: str) -> str:
    if predicate == "package_installed":
        return "Which installed packages does the local dpkg status database declare?"
    if predicate == "package_version":
        return "Which package version does the local dpkg status database declare?"
    if predicate == "package_architecture":
        return "Which package architecture does the local dpkg status database declare?"
    if predicate == "package_manager":
        return "Which package manager declared this installed package record?"
    if predicate not in _PACKAGE_PREDICATES:
        return "Which installed packages does the local package adapter declare?"
    return "Which installed packages does the local package adapter declare?"
