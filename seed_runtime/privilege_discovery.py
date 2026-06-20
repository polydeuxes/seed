"""Read-only privilege discovery for missing operational capabilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.capability_needs import build_capability_needs
from seed_runtime.state import State


@dataclass(frozen=True)
class PrivilegeDiscoveryCapability:
    name: str
    access_level: str
    pressure: int
    operational_benefit: str
    suggested_next_step: str
    notes: str

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "access_level": self.access_level,
            "pressure": self.pressure,
            "operational_benefit": self.operational_benefit,
            "suggested_next_step": self.suggested_next_step,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class PrivilegeDiscoveryAudit:
    capabilities: tuple[PrivilegeDiscoveryCapability, ...]
    boundary: str = "privilege_discovery_visibility_only"
    mutates_cluster: bool = False
    writes_event_ledger: bool = False

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "boundary": self.boundary,
            "mutates_cluster": self.mutates_cluster,
            "writes_event_ledger": self.writes_event_ledger,
            "capabilities": [cap.to_json_dict() for cap in self.capabilities],
        }


_CAPABILITY_GUIDANCE: dict[str, tuple[str, str, str, str]] = {
    "listener_process_inventory": (
        "partial_non_root",
        "service ownership attribution",
        "attempt non-root attribution first",
        "Non-root listener views can identify ports, but process ownership may be incomplete without elevated process visibility.",
    ),
    "container_inventory": (
        "docker_group_or_root",
        "container ownership attribution",
        "requires docker-group or root visibility",
        "Docker inventory normally requires access to the Docker socket, docker group membership, or root-equivalent visibility.",
    ),
    "container_port_mapping": (
        "docker_group_or_root",
        "container port-to-service attribution",
        "requires docker-group or root visibility",
        "Container port mappings normally require Docker socket visibility, docker group membership, or root-equivalent visibility.",
    ),
    "systemd_inventory": (
        "available",
        "service unit attribution",
        "use non-root systemd inventory before requesting privilege",
        "Systemd unit metadata is commonly inspectable without privilege for read-only attribution.",
    ),
    "nfs_export_inventory": (
        "root",
        "storage export ownership attribution",
        "requires root visibility; do not collect until explicitly authorized",
        "NFS export details may require root-owned configuration visibility.",
    ),
}


def build_privilege_discovery(state: State) -> PrivilegeDiscoveryAudit:
    """Explain privilege boundaries for current capability needs without escalation."""

    capabilities = []
    for need in build_capability_needs(state):
        access, benefit, next_step, notes = _guidance_for(need.capability)
        pressure = len(need.subjects)
        capabilities.append(
            PrivilegeDiscoveryCapability(
                name=need.capability,
                access_level=access,
                pressure=pressure,
                operational_benefit=benefit,
                suggested_next_step=next_step,
                notes=notes,
            )
        )
    return PrivilegeDiscoveryAudit(capabilities=tuple(capabilities))


def privilege_discovery_json(audit: PrivilegeDiscoveryAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_privilege_discovery(audit: PrivilegeDiscoveryAudit) -> str:
    lines = ["Privilege Discovery", ""]
    if not audit.capabilities:
        lines.extend(
            [
                "No unavailable capability needs identified by the current audit inputs.",
                "",
                "Boundary:",
                "  visibility only; no sudo, privilege escalation, event ledger writes, or cluster mutation",
            ]
        )
        return "\n".join(lines)
    for capability in audit.capabilities:
        lines.append("Capability:")
        lines.append(f"  {capability.name}")
        lines.append("")
        lines.append("Current Access:")
        lines.append(f"  {capability.access_level}")
        lines.append("")
        lines.append("Pressure:")
        lines.append(f"  {capability.pressure} affected subjects")
        lines.append("")
        lines.append("Operational Benefit:")
        lines.append(f"  {capability.operational_benefit}")
        lines.append("")
        lines.append("Suggested Next Step:")
        lines.append(f"  {capability.suggested_next_step}")
        lines.append("")
        lines.append("Notes:")
        lines.append(f"  {capability.notes}")
        lines.append("")
    lines.append("Boundary:")
    lines.append("  visibility only; no sudo, privilege escalation, event ledger writes, or cluster mutation")
    return "\n".join(lines).rstrip()


def _guidance_for(capability: str) -> tuple[str, str, str, str]:
    if capability in _CAPABILITY_GUIDANCE:
        return _CAPABILITY_GUIDANCE[capability]
    normalized = capability.replace("_", " ")
    return (
        "unknown",
        f"{normalized} attribution",
        "inspect implementation evidence before requesting additional privileges",
        "No implementation-backed privilege guidance is registered for this capability yet.",
    )
