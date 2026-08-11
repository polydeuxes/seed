"""Read-only investigation path audit for existing visibility surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.diagnostic_inventory import (
    DIAGNOSTIC_INVENTORY,
    DiagnosticInventoryEntry,
)


@dataclass(frozen=True)
class InvestigationPathStep:
    name: str
    reason: str
    order: int

    def to_json_dict(self) -> dict[str, Any]:
        return {"name": self.name, "reason": self.reason, "order": self.order}


@dataclass(frozen=True)
class InvestigationPathAudit:
    domain: str
    surfaces: tuple[InvestigationPathStep, ...]
    known_domains: tuple[str, ...]

    @property
    def found(self) -> bool:
        return bool(self.surfaces)

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "surfaces": [step.to_json_dict() for step in self.surfaces],
            "known_domains": list(self.known_domains),
        }


# Implementation-backed path declarations.  Surface names are validated against
# the diagnostic inventory so the audit exposes only registered visibility
# surfaces rather than free-form planning prose.
_INVESTIGATION_PATHS: dict[str, tuple[tuple[str, str], ...]] = {
    "ownership": (
        ("ownership_discrepancies", "primary ownership evidence"),
        ("capability_needs", "ownership gaps generate diagnostic capability needs"),
        ("privilege_discovery", "capability feasibility and access boundaries"),
        (
            "correlation_audit",
            "ownership/evidence disconnects across consumers and pressure",
        ),
        ("impact_audit", "validates whether visible outcomes improved over time"),
    ),
    "capability": (
        ("capability_needs", "primary recorded capability need visibility"),
        (
            "privilege_discovery",
            "explains whether access boundaries constrain the needed capability",
        ),
        (
            "pressure_audit",
            "shows operational pressure associated with missing capability",
        ),
        (
            "consumer_audit",
            "shows implementation consumers that depend on diagnostic evidence",
        ),
        (
            "impact_audit",
            "validates whether capability-related outcomes improved over time",
        ),
    ),
    "pressure": (
        ("pressure_audit", "primary pressure visibility"),
        ("capability_needs", "explains missing diagnostic capability behind pressure"),
        ("privilege_discovery", "explains access constraints for unmet capability"),
        ("correlation_audit", "checks pressure/evidence/consumer disconnects"),
        ("impact_audit", "validates pressure reduction over time"),
    ),
    "correlation": (
        (
            "correlation_audit",
            "primary evidence, consumer, and pressure disconnect visibility",
        ),
        (
            "consumer_audit",
            "identifies implementation-backed consumers of predicates and diagnostics",
        ),
        (
            "observation_utilization",
            "shows where observation predicates participate after collection",
        ),
        (
            "pressure_audit",
            "shows whether disconnects manifest as operational pressure",
        ),
        ("impact_audit", "validates whether correlated outcomes changed over time"),
    ),
    "observation": (
        ("observation_inventory", "primary provider and predicate visibility"),
        ("observation_utilization", "shows where collected observations are used"),
        (
            "consumer_audit",
            "shows implementation-backed consumers of observation predicates",
        ),
        (
            "visibility_coverage_audit",
            "checks whether operational surfaces are represented in diagnostic visibility",
        ),
    ),
    "consumer": (
        ("consumer_audit", "primary implementation-backed consumer visibility"),
        ("observation_utilization", "shows predicate participation after collection"),
        ("correlation_audit", "checks consumer/evidence/pressure disconnects"),
        (
            "operational_surface_inventory",
            "discovers CLI operational surfaces from argparse evidence",
        ),
    ),
    "performance": (
        ("ops_brief", "read-only operational triage summary"),
        ("pressure_audit", "shows performance-relevant operational pressure"),
        ("impact_audit", "compares observable outcomes over snapshots"),
        ("current_facts_cache_debug", "reports read-only cache and timing phases"),
    ),
}


def known_investigation_domains() -> tuple[str, ...]:
    return tuple(sorted(_INVESTIGATION_PATHS))


def build_investigation_path_audit(
    domain: str,
    entries: tuple[DiagnosticInventoryEntry, ...] = DIAGNOSTIC_INVENTORY,
) -> InvestigationPathAudit:
    normalized = domain.strip().lower()
    registered = {entry.name for entry in entries}
    steps = tuple(
        InvestigationPathStep(name=name, reason=reason, order=index)
        for index, (name, reason) in enumerate(
            _INVESTIGATION_PATHS.get(normalized, ()), start=1
        )
        if name in registered
    )
    return InvestigationPathAudit(normalized, steps, known_investigation_domains())


def investigation_path_audit_json(audit: InvestigationPathAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_investigation_path_audit(audit: InvestigationPathAudit) -> str:
    lines = ["Investigation Path", "", f"Domain: {audit.domain}", ""]
    if not audit.surfaces:
        lines.append("No investigation path is registered for this domain.")
        lines.append("Known Domains:")
        lines.extend(f"  {domain}" for domain in audit.known_domains)
        return "\n".join(lines)
    lines.append("Relevant Surfaces:")
    for step in audit.surfaces:
        lines.extend(
            [f"  {step.order}. {step.name}", "     Reason:", f"       {step.reason}"]
        )
    lines.append("")
    lines.append("Suggested Order:")
    lines.extend(f"  {step.order}. {step.name}" for step in audit.surfaces)
    return "\n".join(lines)
