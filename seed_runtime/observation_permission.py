"""Read-only observation-domain permission visibility."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from seed_runtime.state import State

ObservationClass = Literal[
    "local_passive",
    "network_passive",
    "network_active",
    "local_privileged",
    "external",
    "unknown",
]
PermissionState = Literal[
    "granted", "requires_operator_expression", "denied", "unknown"
]


@dataclass(frozen=True)
class ObservationPermissionDomain:
    domain: str
    observation_class: ObservationClass
    permission_state: PermissionState
    authority_evidence: tuple[str, ...] = ()
    reasoning: tuple[str, ...] = ()
    known_limitations: tuple[str, ...] = ()
    reusable_permission: str = "not_granted"
    future_autonomous_invocation: str = "requires_operator_expression"

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "observation_class": self.observation_class,
            "permission_state": self.permission_state,
            "authority_evidence": list(self.authority_evidence),
            "reasoning": list(self.reasoning),
            "known_limitations": list(self.known_limitations),
            "reusable_permission": self.reusable_permission,
            "future_autonomous_invocation": self.future_autonomous_invocation,
        }


@dataclass(frozen=True)
class ObservationPermissionReport:
    domains: tuple[ObservationPermissionDomain, ...]
    boundary: dict[str, bool] = field(
        default_factory=lambda: {
            "read_only": True,
            "writes_event_ledger": False,
            "mutates_cluster": False,
            "permission_enforcement": False,
            "approval_storage": False,
            "runtime_autonomy": False,
        }
    )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "domains": [domain.to_json_dict() for domain in self.domains],
            "boundary": dict(self.boundary),
        }


SUPPORTED_OBSERVATION_CLASSES: dict[str, ObservationClass] = {
    "neighbor_table_read": "local_passive",
    "traffic_capture": "network_passive",
    "active_network_probe": "network_active",
    "docker_socket_read": "local_privileged",
    "external_provider_query": "external",
}


def build_observation_permission(
    state: State, domain_filter: str | None = None
) -> ObservationPermissionReport:
    domains = sorted(SUPPORTED_OBSERVATION_CLASSES)
    if domain_filter:
        domains = [domain_filter]

    entries = tuple(_domain_entry(state, domain) for domain in domains)
    return ObservationPermissionReport(entries)


def observation_permission_json(report: ObservationPermissionReport) -> dict[str, Any]:
    return report.to_json_dict()


def format_observation_permission(report: ObservationPermissionReport) -> str:
    lines = ["Observation Permission", ""]
    if not report.domains:
        lines.append("(none)")
    for entry in report.domains:
        lines.extend(
            [
                "Domain:",
                f"  {entry.domain}",
                "",
                "Observation Class:",
                f"  {entry.observation_class}",
                "",
                "Permission State:",
                f"  {entry.permission_state}",
                "",
                "Authority Evidence:",
            ]
        )
        if entry.authority_evidence:
            lines.extend(f"  - {item}" for item in entry.authority_evidence)
        else:
            lines.append("  none observed")
        lines.extend(
            [
                "",
                "Reusable Permission:",
                f"  {entry.reusable_permission}",
                "",
                "Future Autonomous Invocation:",
                f"  {entry.future_autonomous_invocation}",
                "",
                "Reasoning:",
            ]
        )
        lines.extend(f"  - {item}" for item in entry.reasoning)
        lines.extend(["", "Known Limitations:"])
        lines.extend(f"  - {item}" for item in entry.known_limitations)
        lines.append("")
    lines.append("Boundary:")
    lines.append(
        "  read_only=true writes_event_ledger=false mutates_cluster=false no_recording=true no_permission_enforcement=true no_approval_storage=true no_runtime_autonomy=true"
    )
    return "\n".join(lines).rstrip()


def _domain_entry(state: State, domain: str) -> ObservationPermissionDomain:
    observation_class = SUPPORTED_OBSERVATION_CLASSES.get(domain, "unknown")
    approval = _approval_for_domain(state, domain)
    evidence: list[str] = []
    if approval is not None:
        evidence.append(
            f"Approval(action={approval.action}, scope={approval.scope}, approved_by={approval.approved_by})"
        )
    if approval is not None:
        permission_state: PermissionState = "granted"
        reusable_permission = "granted"
        future = "granted"
    elif observation_class == "unknown":
        permission_state = "unknown"
        reusable_permission = "unknown"
        future = "unknown"
    else:
        permission_state = "requires_operator_expression"
        reusable_permission = "not_granted"
        future = "requires_operator_expression"

    reasoning = [
        (
            "observation domain identified"
            if observation_class != "unknown"
            else "observation domain not recognized by implementation evidence"
        ),
        (
            "reusable approval observed"
            if approval is not None
            else "reusable approval not observed"
        ),
        "manual operator invocation may authorize only the current execution",
        "manual operator invocation does not create reusable Seed permission",
    ]
    if approval is None:
        reasoning.append(
            "future autonomous invocation requires operator expression unless reusable approval is observed"
        )
    return ObservationPermissionDomain(
        domain=domain,
        observation_class=observation_class,
        permission_state=permission_state,
        authority_evidence=tuple(evidence),
        reasoning=tuple(reasoning),
        known_limitations=(
            "visibility only",
            "no permission enforcement",
            "no approval record creation",
            "no autonomous runtime behavior",
        ),
        reusable_permission=reusable_permission,
        future_autonomous_invocation=future,
    )


def _approval_for_domain(state: State, domain: str):
    for approval in state.approvals.values():
        if approval.action == f"observation.{domain}":
            return approval
        if approval.constraints.get("observation_domain") == domain:
            return approval
    return None
