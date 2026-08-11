"""Narrow read-only authority slice for local listener endpoint observation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from seed_runtime.observation_domains import build_observation_domains
from seed_runtime.observation_inventory import build_observation_inventory
from seed_runtime.state import State

CONSTRAINED_AUTHORITY_PROFILE = {
    "root": "unavailable",
    "docker_socket_read": "unavailable",
    "active_network_probe": "unauthorized",
    "local_passive": "available",
    "external_provider_query": "unknown",
}

DESIRED_OBSERVATION = "local listener endpoint inventory"
LISTENER_ENDPOINT_OBSERVATIONS = (
    "listening_protocol",
    "listening_address",
    "listening_port",
    "local_socket_table_evidence",
)
AUTHORITY_KEYS = (
    "root",
    "docker_socket_read",
    "active_network_probe",
    "local_passive",
    "external_provider_query",
)
OUT_OF_SCOPE = (
    "process ownership",
    "service ownership",
    "application ownership",
    "container ownership",
    "health",
    "responsiveness",
    "external accessibility",
    "DNS validity",
    "remote network reachability",
    "causality",
    "intent",
)


@dataclass(frozen=True)
class ListenerEndpointAuthoritySlice:
    desired_observation: str
    required_observations: tuple[str, ...]
    required_authority: dict[str, str]
    available_authority: dict[str, str]
    reachable_observations: tuple[str, ...]
    blocked_observations: tuple[str, ...]
    outcome: str
    uncertainty: tuple[str, ...]
    boundary: dict[str, object] = field(
        default_factory=lambda: {
            "read_only": True,
            "records": False,
            "writes_event_ledger": False,
            "mutates_cluster": False,
            "provider_acquisition": False,
            "permission_creation": False,
            "executes_observation": False,
            "scope": "local TCP/UDP endpoint inventory: protocol, address, port, local socket-table evidence",
            "excludes": list(OUT_OF_SCOPE),
        }
    )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "desired_observation": self.desired_observation,
            "required_observations": list(self.required_observations),
            "required_authority": dict(self.required_authority),
            "available_authority": dict(self.available_authority),
            "reachable_observations": list(self.reachable_observations),
            "blocked_observations": list(self.blocked_observations),
            "outcome": self.outcome,
            "uncertainty": list(self.uncertainty),
            "boundary": dict(self.boundary),
        }


def evaluate_listener_endpoint_authority_slice(
    state: State,
    profile: Mapping[str, str],
) -> ListenerEndpointAuthoritySlice:
    """Evaluate only the local listener endpoint authority slice.

    Existing repository surfaces are read as implementation evidence for local
    listener predicates/domains. The evaluator does not execute observations,
    acquire providers, grant permissions, record facts, or infer ownership.
    """

    available_authority = {key: str(profile.get(key, "unknown")) for key in AUTHORITY_KEYS}
    required_observations = LISTENER_ENDPOINT_OBSERVATIONS
    required_authority = {observation: "local_passive" for observation in required_observations}

    evidence = _listener_endpoint_evidence(state)
    implementation_supports_endpoint = all(
        evidence[key]
        for key in (
            "has_listener_family",
            "has_listening_endpoint",
            "has_listening_protocol",
            "has_listening_address",
            "has_listening_port",
            "has_local_listener_domain",
        )
    )
    local_passive_available = available_authority["local_passive"] == "available"

    if implementation_supports_endpoint and local_passive_available:
        reachable = required_observations
        blocked: tuple[str, ...] = ()
        outcome = "reachable"
    elif not local_passive_available:
        reachable = ()
        blocked = required_observations
        outcome = "blocked"
    else:
        reachable = ()
        blocked = ()
        outcome = "unknown"

    uncertainty = tuple(
        list(evidence["notes"])
        + [
            "does not establish process owner, service owner, container owner, or application owner",
            "does not establish health, responsiveness, external accessibility, DNS validity, or network reachability",
        ]
    )

    return ListenerEndpointAuthoritySlice(
        desired_observation=DESIRED_OBSERVATION,
        required_observations=required_observations,
        required_authority=required_authority,
        available_authority=available_authority,
        reachable_observations=reachable,
        blocked_observations=blocked,
        outcome=outcome,
        uncertainty=uncertainty,
    )


def _listener_endpoint_evidence(state: State) -> dict[str, Any]:
    inventory = build_observation_inventory()
    predicates = {predicate.predicate for predicate in inventory.predicates}
    families = {family.family for family in inventory.families}
    domains = build_observation_domains(state, domain_filter="local_listeners")
    domain = domains.domains[0] if domains.domains else None
    notes = []
    endpoint_predicates = {
        "listening_endpoint",
        "listening_protocol",
        "listening_address",
        "listening_port",
    }
    observed_endpoint_predicates = sorted(endpoint_predicates & predicates)
    if observed_endpoint_predicates:
        notes.append(
            "observation_inventory exposes listener endpoint predicates: "
            + ", ".join(observed_endpoint_predicates)
        )
    if domain is not None:
        notes.append(
            f"observation_domains reports local_listeners as {domain.classification} from implementation evidence"
        )
    notes.append(
        "local socket-table evidence is bounded to TCP/UDP protocol, address, and port"
    )
    return {
        "has_listener_family": "listening" in families or "listener" in families,
        "has_listening_endpoint": "listening_endpoint" in predicates,
        "has_listening_protocol": "listening_protocol" in predicates,
        "has_listening_address": "listening_address" in predicates,
        "has_listening_port": "listening_port" in predicates,
        "has_local_listener_domain": domain is not None and domain.domain == "local_listeners",
        "notes": tuple(notes),
    }


def listener_endpoint_authority_json(
    result: ListenerEndpointAuthoritySlice,
) -> dict[str, Any]:
    return result.to_json_dict()


def format_listener_endpoint_authority(result: ListenerEndpointAuthoritySlice) -> str:
    lines = [
        "Listener Endpoint Authority",
        "",
        f"Desired observation: {result.desired_observation}",
        "Required observations:",
    ]
    lines.extend(f"  - {item}" for item in result.required_observations)
    lines.append("Required authority:")
    lines.extend(
        f"  - {observation}: {authority}"
        for observation, authority in sorted(result.required_authority.items())
    )
    lines.append("Available authority:")
    lines.extend(
        f"  - {authority}: {status}"
        for authority, status in sorted(result.available_authority.items())
    )
    lines.append("Reachable observations:")
    lines.extend(f"  - {item}" for item in result.reachable_observations or ("none",))
    lines.append("Blocked observations:")
    lines.extend(f"  - {item}" for item in result.blocked_observations or ("none",))
    lines.extend([f"Outcome: {result.outcome}", "Uncertainty:"])
    lines.extend(f"  - {item}" for item in result.uncertainty)
    lines.append("Boundary:")
    for name, value in sorted(result.boundary.items()):
        rendered = ", ".join(value) if isinstance(value, list) else str(value).lower()
        lines.append(f"  - {name}: {rendered}")
    return "\n".join(lines)
