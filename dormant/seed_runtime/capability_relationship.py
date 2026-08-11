"""Read-only capability relationship visibility from existing capability surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.capability_needs import build_capability_needs
from seed_runtime.privilege_discovery import _guidance_for
from seed_runtime.state import State


@dataclass(frozen=True)
class CapabilityRelationship:
    capability: str
    current_access: str
    operational_benefit: str
    pressure: int
    attainability: str
    expectation: str
    reasoning: tuple[str, ...]
    known_limitations: tuple[str, ...]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "capability": self.capability,
            "current_access": self.current_access,
            "operational_benefit": self.operational_benefit,
            "pressure": self.pressure,
            "attainability": self.attainability,
            "expectation": self.expectation,
            "reasoning": list(self.reasoning),
            "known_limitations": list(self.known_limitations),
        }


@dataclass(frozen=True)
class CapabilityRelationshipAudit:
    capabilities: tuple[CapabilityRelationship, ...]
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "capabilities": [cap.to_json_dict() for cap in self.capabilities],
            "boundary": {
                "read_only": self.read_only,
                "writes_event_ledger": self.writes_event_ledger,
                "mutates_cluster": self.mutates_cluster,
            },
        }


def build_capability_relationship(
    state: State, *, capability_filter: str | None = None
) -> CapabilityRelationshipAudit:
    """Explain capability/access/pressure relationships without acquisition logic."""

    relationships: list[CapabilityRelationship] = []
    for need in build_capability_needs(state):
        if capability_filter and need.capability != capability_filter:
            continue
        access, benefit, _next_step, _notes = _guidance_for(need.capability)
        relationships.append(
            CapabilityRelationship(
                capability=need.capability,
                current_access=access,
                operational_benefit=benefit,
                pressure=len(need.subjects),
                attainability="unknown",
                expectation="unknown",
                reasoning=(
                    "repository evidence shows operational benefit and current access context",
                    "repository evidence does not establish deployment expectation or operator intent",
                    "capability pressure is reported as visibility context, not acquisition guidance",
                ),
                known_limitations=(
                    "deployment intent not observed",
                    "capability acquisition is outside this read-only surface",
                ),
            )
        )
    return CapabilityRelationshipAudit(capabilities=tuple(relationships))


def capability_relationship_json(audit: CapabilityRelationshipAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_capability_relationship(audit: CapabilityRelationshipAudit) -> str:
    lines = ["Capability Relationship", ""]
    if not audit.capabilities:
        lines.extend(
            [
                "No capability pressure identified by the current audit inputs.",
                "",
                "Boundary:",
                "  read only; no recording, event ledger writes, cluster mutation, acquisition, policy, or planning",
            ]
        )
        return "\n".join(lines)

    for capability in audit.capabilities:
        lines.append("Capability:")
        lines.append(f"  {capability.capability}")
        lines.append("")
        lines.append("Current Access:")
        lines.append(f"  {capability.current_access}")
        lines.append("")
        lines.append("Operational Benefit:")
        lines.append(f"  {capability.operational_benefit}")
        lines.append("")
        lines.append("Pressure:")
        lines.append(f"  {capability.pressure} affected subjects")
        lines.append("")
        lines.append("Attainability:")
        lines.append(f"  {capability.attainability}")
        lines.append("")
        lines.append("Expectation:")
        lines.append(f"  {capability.expectation}")
        lines.append("")
        lines.append("Reasoning:")
        for item in capability.reasoning:
            lines.append(f"  - {item}")
        lines.append("")
        lines.append("Known Limitations:")
        for item in capability.known_limitations:
            lines.append(f"  - {item}")
        lines.append("")

    lines.append("Boundary:")
    lines.append(
        "  read only; no recording, event ledger writes, cluster mutation, acquisition, policy, or planning"
    )
    return "\n".join(lines).rstrip()
