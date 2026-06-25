"""Narrow read-only authority slice for service ownership observation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from seed_runtime.capability_needs import build_capability_needs
from seed_runtime.observation_domains import CAPABILITY_TO_DOMAIN, build_observation_domains
from seed_runtime.observation_inventory import build_observation_inventory
from seed_runtime.observation_permission import SUPPORTED_OBSERVATION_CLASSES
from seed_runtime.privilege_discovery import _guidance_for
from seed_runtime.state import State

CONSTRAINED_AUTHORITY_PROFILE = {
    "root": "unavailable",
    "docker_socket_read": "unavailable",
    "active_network_probe": "unauthorized",
    "local_passive": "available",
    "external_provider_query": "unknown",
}

DESIRED_OBSERVATION = "service ownership"
SERVICE_OBSERVATIONS = (
    "tcp_listen_inventory",
    "listener_process_inventory",
    "systemd_unit_inventory",
    "container_inventory",
    "container_port_mapping",
)
AUTHORITY_KEYS = (
    "root",
    "docker_socket_read",
    "active_network_probe",
    "local_passive",
    "external_provider_query",
)
CURRENT_STRATEGY = "composite_local_service_attribution_observation"
BLOCKING_BOUNDARY = "docker_or_root_container_runtime_authority_unavailable"


@dataclass(frozen=True)
class ServiceOwnershipAuthoritySlice:
    desired_observation: str
    required_observations: tuple[str, ...]
    required_authority: dict[str, str]
    available_authority: dict[str, str]
    reachable_observations: tuple[str, ...]
    blocked_observations: tuple[str, ...]
    outcome: str
    current_strategy: str
    strategy_status: str
    remaining_observations: tuple[str, ...]
    uncertainty: tuple[str, ...]
    remaining_uncertainty: tuple[str, ...]
    blocking_boundary: str | None = None
    boundary: dict[str, bool] = field(
        default_factory=lambda: {
            "read_only": True,
            "records": False,
            "writes_event_ledger": False,
            "mutates_cluster": False,
            "provider_acquisition": False,
            "permission_creation": False,
            "executes_observation": False,
        }
    )

    def to_json_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "desired_observation": self.desired_observation,
            "required_observations": list(self.required_observations),
            "required_authority": dict(self.required_authority),
            "available_authority": dict(self.available_authority),
            "reachable_observations": list(self.reachable_observations),
            "blocked_observations": list(self.blocked_observations),
            "outcome": self.outcome,
            "current_strategy": self.current_strategy,
            "strategy_status": self.strategy_status,
            "remaining_observations": list(self.remaining_observations),
            "uncertainty": list(self.uncertainty),
            "remaining_uncertainty": list(self.remaining_uncertainty),
            "boundary": dict(self.boundary),
        }
        if self.blocking_boundary is not None:
            payload["blocking_boundary"] = self.blocking_boundary
        return payload


def evaluate_service_ownership_authority_slice(
    state: State,
    profile: Mapping[str, str],
) -> ServiceOwnershipAuthoritySlice:
    """Evaluate only the service-ownership authority slice.

    The supplied profile is authoritative for the constrained scenario. Existing
    repository surfaces are read only as implementation evidence for known
    capability names, observed listener/systemd support, and Docker/root limits.
    """

    available_authority = {key: str(profile.get(key, "unknown")) for key in AUTHORITY_KEYS}
    required_observations = _required_service_observations(state)
    required_authority = {
        observation: _authority_for_observation(observation)
        for observation in required_observations
    }

    reachable = tuple(
        observation
        for observation in required_observations
        if _is_reachable(observation, required_authority[observation], available_authority)
    )
    blocked = tuple(
        observation
        for observation in required_observations
        if _is_blocked(observation, required_authority[observation], available_authority)
    )

    if reachable and blocked:
        outcome = "partially_reachable"
    elif reachable:
        outcome = "reachable"
    elif blocked:
        outcome = "blocked"
    else:
        outcome = "unknown"

    uncertainty = list(_implementation_evidence_uncertainty(state, required_observations))
    uncertainty.append(
        "active_network_probe unauthorized and external_provider_query unknown are not used to promote service ownership beyond local passive evidence"
    )

    blocking_boundary = (
        BLOCKING_BOUNDARY
        if _docker_or_root_container_runtime_authority_blocked(
            blocked, required_authority, available_authority
        )
        else None
    )

    return ServiceOwnershipAuthoritySlice(
        desired_observation=DESIRED_OBSERVATION,
        required_observations=required_observations,
        required_authority=required_authority,
        available_authority=available_authority,
        reachable_observations=reachable,
        blocked_observations=blocked,
        outcome=outcome,
        current_strategy=CURRENT_STRATEGY,
        strategy_status=outcome,
        remaining_observations=blocked,
        uncertainty=tuple(uncertainty),
        remaining_uncertainty=tuple(uncertainty),
        blocking_boundary=blocking_boundary,
    )


def _required_service_observations(state: State) -> tuple[str, ...]:
    observed = []
    known = set(SERVICE_OBSERVATIONS)
    for need in build_capability_needs(state, diagnostic_filter="ownership_discrepancies"):
        if need.capability in known:
            observed.append(need.capability)
    for capability in SERVICE_OBSERVATIONS:
        if capability in observed:
            continue
        if capability in {"container_inventory", "container_port_mapping"}:
            if CAPABILITY_TO_DOMAIN.get(capability) == "container_runtime":
                observed.append(capability)
        else:
            observed.append(capability)
    return tuple(dict.fromkeys(observed))


def _authority_for_observation(observation: str) -> str:
    if observation == "tcp_listen_inventory":
        return "local_passive"
    if observation == "systemd_unit_inventory":
        access, *_ = _guidance_for("systemd_inventory")
        return "local_passive" if access == "available" else access
    access, *_ = _guidance_for(observation)
    return access


def _is_reachable(observation: str, authority: str, profile: Mapping[str, str]) -> bool:
    if observation in {"tcp_listen_inventory", "systemd_unit_inventory"}:
        return profile.get("local_passive") == "available"
    if observation == "listener_process_inventory":
        return authority == "partial_non_root" and profile.get("local_passive") == "available"
    return False


def _is_blocked(observation: str, authority: str, profile: Mapping[str, str]) -> bool:
    if authority == "docker_group_or_root":
        return (
            profile.get("root") == "unavailable"
            and profile.get("docker_socket_read") == "unavailable"
        )
    return False


def _docker_or_root_container_runtime_authority_blocked(
    blocked_observations: tuple[str, ...],
    required_authority: Mapping[str, str],
    available_authority: Mapping[str, str],
) -> bool:
    if not blocked_observations:
        return False
    return any(
        required_authority.get(observation) == "docker_group_or_root"
        for observation in blocked_observations
    ) and (
        available_authority.get("root") == "unavailable"
        and available_authority.get("docker_socket_read") == "unavailable"
    )


def _implementation_evidence_uncertainty(
    state: State, required_observations: tuple[str, ...]
) -> tuple[str, ...]:
    inventory = build_observation_inventory()
    families = {family.family for family in inventory.families}
    predicates = {predicate.predicate for predicate in inventory.predicates}
    domains = build_observation_domains(state)
    local_listener_domain = next(
        (domain for domain in domains.domains if domain.domain == "local_listeners"), None
    )
    notes = []
    if "listener" in families or "listening" in families or any(
        predicate.startswith(("listener_", "listening_")) for predicate in predicates
    ):
        notes.append("listener observation support exists in observation_inventory")
    else:
        notes.append("listener observation support was not found in observation_inventory")
    if any("systemd" in predicate for predicate in predicates):
        notes.append("systemd observation support exists in observation_inventory")
    else:
        notes.append("systemd support is limited to privilege guidance and current fact predicates, not a discovered systemd observation provider")
    if local_listener_domain is not None:
        notes.append(
            f"observation_domains reports local_listeners as {local_listener_domain.classification}"
        )
    if SUPPORTED_OBSERVATION_CLASSES.get("docker_socket_read") == "local_privileged":
        notes.append("docker_socket_read is recognized as local_privileged observation-permission activity")
    if {"container_inventory", "container_port_mapping"} & set(required_observations):
        notes.append("container observations remain Docker/root dependent under privilege_discovery guidance")
    return tuple(notes)


def service_ownership_authority_json(
    result: ServiceOwnershipAuthoritySlice,
) -> dict[str, Any]:
    return result.to_json_dict()


def format_service_ownership_authority(result: ServiceOwnershipAuthoritySlice) -> str:
    lines = [
        "Service Ownership Authority",
        "",
        "Goal",
        f"Desired observation: {result.desired_observation}",
        "",
        "Strategy",
        f"Current strategy: {result.current_strategy}",
        "Required observations:",
    ]
    lines.extend(f"  - {item}" for item in result.required_observations)
    lines.extend(["", "Observation state", "Reachable observations:"])
    lines.extend(f"  - {item}" for item in result.reachable_observations or ("none",))
    lines.append("Remaining observations:")
    lines.extend(f"  - {item}" for item in result.remaining_observations or ("none",))
    lines.extend(["", "Authority", "Required authority:"])
    lines.extend(
        f"  - {observation}: {authority}"
        for observation, authority in sorted(result.required_authority.items())
    )
    lines.append("Available authority:")
    lines.extend(
        f"  - {authority}: {status}"
        for authority, status in sorted(result.available_authority.items())
    )
    lines.extend(
        [
            "",
            "Execution",
            f"Strategy status: {result.strategy_status}",
            f"Outcome: {result.outcome}",
        ]
    )
    if result.blocking_boundary is not None:
        lines.append(f"Blocking boundary: {result.blocking_boundary}")
    lines.extend(["", "Uncertainty:"])
    lines.extend(f"  - {item}" for item in result.uncertainty)
    if result.remaining_uncertainty != result.uncertainty:
        lines.append("Remaining uncertainty:")
        lines.extend(f"  - {item}" for item in result.remaining_uncertainty)
    lines.extend(["", "Boundary"])
    lines.extend(
        f"  - {name}: {str(value).lower()}"
        for name, value in sorted(result.boundary.items())
    )
    return "\n".join(lines)
