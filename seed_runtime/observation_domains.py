"""Read-only observation-domain visibility derived from existing evidence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from seed_runtime.capability_needs import build_capability_needs
from seed_runtime.observation_inventory import build_observation_inventory
from seed_runtime.observation_utilization import build_observation_utilization_audit
from seed_runtime.operational_story import build_operational_story
from seed_runtime.state import State


@dataclass(frozen=True)
class ObservationDomainEntry:
    domain: str
    classification: str
    gap_type: str
    pressure: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "classification": self.classification,
            "gap_type": self.gap_type,
            "pressure": list(self.pressure),
            "evidence": list(self.evidence),
        }


@dataclass(frozen=True)
class ObservationDomainReport:
    domains: tuple[ObservationDomainEntry, ...]
    boundary: dict[str, bool] = field(
        default_factory=lambda: {
            "read_only": True,
            "writes_event_ledger": False,
            "mutates_cluster": False,
        }
    )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "domains": [domain.to_json_dict() for domain in self.domains],
            "boundary": dict(self.boundary),
        }


CAPABILITY_TO_DOMAIN = {
    "listener_process_inventory": "local_listeners",
    "container_inventory": "container_runtime",
    "container_port_mapping": "container_runtime",
}


def build_observation_domains(
    state: State,
    domain_filter: str | None = None,
) -> ObservationDomainReport:
    inventory = build_observation_inventory()
    utilization = build_observation_utilization_audit()
    needs = build_capability_needs(state)
    story = build_operational_story(state)

    families = {family.family for family in inventory.families}
    predicates = {predicate.predicate for predicate in inventory.predicates}
    diagnostic_predicates = {
        row.predicate for row in utilization.predicates if row.diagnostic_consumed
    }
    pressure_by_domain: dict[str, set[str]] = {}
    for capability, domain in CAPABILITY_TO_DOMAIN.items():
        # Repository authority: capability_needs.py names these capability pressures.
        # Recorded/current diagnostic facts can add to the same implementation-backed map.
        pressure_by_domain.setdefault(domain, set()).add(capability)
    for need in needs:
        domain = CAPABILITY_TO_DOMAIN.get(need.capability)
        if domain:
            pressure_by_domain.setdefault(domain, set()).add(need.capability)

    domains: dict[str, ObservationDomainEntry] = {}
    listener_observed = "listener" in families or any(
        predicate.startswith("listener_") for predicate in predicates
    )
    if listener_observed or "local_listeners" in pressure_by_domain:
        pressure = tuple(sorted(pressure_by_domain.get("local_listeners", set())))
        classification = "partially_observed" if pressure else "observed"
        gap_type = "missing_evidence_inside_observed_domain" if pressure else "unknown"
        evidence = ["listener predicates observed"]
        if diagnostic_predicates & {p for p in predicates if p.startswith("listener_")}:
            evidence.append("listener predicates consumed by diagnostics")
        if pressure:
            evidence.append("listener ownership pressure observed")
        domains["local_listeners"] = ObservationDomainEntry(
            "local_listeners", classification, gap_type, pressure, tuple(evidence)
        )

    container_pressure = tuple(sorted(pressure_by_domain.get("container_runtime", set())))
    container_observed = "container" in families or any(
        predicate.startswith("container_") for predicate in predicates
    )
    if container_observed or container_pressure:
        if container_observed and container_pressure:
            classification = "partially_observed"
            gap_type = "missing_evidence_inside_observed_domain"
        elif container_observed:
            classification = "observed"
            gap_type = "unknown"
        else:
            classification = "unobserved"
            gap_type = "missing_observation_domain"
        evidence = []
        if container_pressure:
            evidence.append("capability pressure observed")
        if not container_observed:
            evidence.append("no container observation family observed")
        else:
            evidence.append("container observation family observed")
        domains["container_runtime"] = ObservationDomainEntry(
            "container_runtime", classification, gap_type, container_pressure, tuple(evidence)
        )

    for family in sorted(families - {"listener", "listening", "container"}):
        name = f"{family}_observations"
        domains.setdefault(
            name,
            ObservationDomainEntry(
                name,
                "observed",
                "unknown",
                (),
                (f"{family} observation family observed",),
            ),
        )

    if domain_filter:
        domains = {
            domain_filter: domains.get(
                domain_filter,
                ObservationDomainEntry(
                    domain_filter,
                    "unknown",
                    "unknown",
                    (),
                    ("insufficient repository evidence for requested observation domain",),
                ),
            )
        }

    return ObservationDomainReport(tuple(domains[name] for name in sorted(domains)))


def observation_domains_json(report: ObservationDomainReport) -> dict[str, Any]:
    return report.to_json_dict()


def format_observation_domains(report: ObservationDomainReport) -> str:
    lines = ["Observation Domains", ""]
    if not report.domains:
        lines.append("(none)")
    for entry in report.domains:
        lines.extend(
            [
                "Observation Domain",
                "",
                f"Domain: {entry.domain}",
                f"Classification: {entry.classification}",
                "Pressure: " + (", ".join(entry.pressure) if entry.pressure else "(none)"),
                f"Gap Type: {entry.gap_type}",
                "Evidence:",
            ]
        )
        lines.extend(f"  - {item}" for item in entry.evidence)
        lines.extend(["Boundary: read only", ""])
    lines.append(
        "Boundary: read_only=true writes_event_ledger=false mutates_cluster=false"
    )
    return "\n".join(lines).rstrip()
