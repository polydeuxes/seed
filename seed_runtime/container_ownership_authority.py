"""Narrow read-only authority slice for container ownership observation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from seed_runtime.capability_needs import build_capability_needs
from seed_runtime.observation_domains import CAPABILITY_TO_DOMAIN
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

DESIRED_OBSERVATION = "container ownership"
CONTAINER_RUNTIME_DOMAIN = "container_runtime"
CONTAINER_OBSERVATIONS = ("container_inventory", "container_port_mapping")
AUTHORITY_KEYS = (
    "root",
    "docker_socket_read",
    "active_network_probe",
    "local_passive",
    "external_provider_query",
)
CURRENT_STRATEGY = "container_runtime_observation"
BLOCKING_BOUNDARY = "docker_or_root_container_runtime_authority_unavailable"


@dataclass(frozen=True)
class ContainerOwnershipAuthoritySlice:
    desired_observation: str
    required_observations: tuple[str, ...]
    required_authority: dict[str, str]
    available_authority: dict[str, str]
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


def evaluate_container_ownership_authority_slice(
    state: State,
    profile: Mapping[str, str],
) -> ContainerOwnershipAuthoritySlice:
    """Evaluate only the container-ownership/root-Docker authority slice.

    The supplied profile is the authority decision source. Existing repository
    concepts are consulted only to prove recognized names and domain/privilege
    mappings; approvals in state never grant authority for this evaluator.
    """

    available_authority = {key: str(profile.get(key, "unknown")) for key in AUTHORITY_KEYS}

    required_observations = tuple(
        capability
        for capability in CONTAINER_OBSERVATIONS
        if CAPABILITY_TO_DOMAIN.get(capability) == CONTAINER_RUNTIME_DOMAIN
    )
    required_authority = {
        capability: _guidance_for(capability)[0] for capability in required_observations
    }

    subject_specific_pressure = _has_subject_specific_container_ownership_pressure(
        state, set(required_observations)
    )
    docker_socket_read_recognized = (
        SUPPORTED_OBSERVATION_CLASSES.get("docker_socket_read") == "local_privileged"
    )

    docker_or_root_blocked = (
        available_authority["root"] == "unavailable"
        and available_authority["docker_socket_read"] == "unavailable"
    )
    outcome = (
        "blocked"
        if required_observations
        and all(
            required_authority[capability] == "docker_group_or_root"
            for capability in required_observations
        )
        and docker_or_root_blocked
        else "unknown"
    )
    remaining_observations = required_observations if outcome == "blocked" else ()
    blocking_boundary = BLOCKING_BOUNDARY if outcome == "blocked" else None

    uncertainty = [
        "external_provider_query unknown and not mapped to this first slice",
        "local_passive available but not sufficient for docker/root container runtime evidence",
    ]
    if docker_socket_read_recognized:
        uncertainty.append(
            "docker_socket_read is recognized as local_privileged observation-permission activity but supplied profile remains authoritative"
        )
    else:
        uncertainty.append(
            "docker_socket_read recognition not found in observation_permission implementation evidence"
        )
    if subject_specific_pressure:
        uncertainty.append(
            "subject-specific ownership pressure exists from ownership_discrepancies matching service conflicts"
        )
    else:
        uncertainty.append(
            "subject-specific ownership pressure exists only when ownership_discrepancies emits matching service conflicts"
        )

    return ContainerOwnershipAuthoritySlice(
        desired_observation=DESIRED_OBSERVATION,
        required_observations=required_observations,
        required_authority=required_authority,
        available_authority=available_authority,
        outcome=outcome,
        current_strategy=CURRENT_STRATEGY,
        strategy_status=outcome,
        remaining_observations=remaining_observations,
        uncertainty=tuple(uncertainty),
        remaining_uncertainty=tuple(uncertainty),
        blocking_boundary=blocking_boundary,
    )


def _has_subject_specific_container_ownership_pressure(
    state: State, required_observations: set[str]
) -> bool:
    for need in build_capability_needs(
        state, diagnostic_filter="ownership_discrepancies"
    ):
        if need.capability in required_observations and need.subjects:
            return True
    return False


def container_ownership_authority_json(
    result: ContainerOwnershipAuthoritySlice,
) -> dict[str, Any]:
    return result.to_json_dict()


def format_container_ownership_authority(
    result: ContainerOwnershipAuthoritySlice,
) -> str:
    lines = [
        "Container Ownership Authority",
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
    lines.extend(
        [
            f"Outcome: {result.outcome}",
            f"Current strategy: {result.current_strategy}",
            f"Strategy status: {result.strategy_status}",
        ]
    )
    if result.blocking_boundary is not None:
        lines.append(f"Blocking boundary: {result.blocking_boundary}")
    lines.append("Remaining observations:")
    if result.remaining_observations:
        lines.extend(f"  - {item}" for item in result.remaining_observations)
    else:
        lines.append("  - none")
    lines.append("Uncertainty:")
    lines.extend(f"  - {item}" for item in result.uncertainty)
    lines.append("Remaining uncertainty:")
    lines.extend(f"  - {item}" for item in result.remaining_uncertainty)
    lines.append("Boundary:")
    lines.extend(
        f"  - {name}: {str(value).lower()}"
        for name, value in sorted(result.boundary.items())
    )
    return "\n".join(lines)
