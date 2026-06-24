from datetime import datetime, timedelta, timezone

from seed_runtime.container_ownership_authority import (
    evaluate_container_ownership_authority_slice,
)
from seed_runtime.models import Approval
from seed_runtime.state import State


PROFILE = {
    "root": "unavailable",
    "docker_socket_read": "unavailable",
    "active_network_probe": "unauthorized",
    "local_passive": "available",
    "external_provider_query": "unknown",
}


def test_container_ownership_slice_blocks_without_root_or_docker_socket():
    result = evaluate_container_ownership_authority_slice(
        State(workspace_id="test"), PROFILE
    )

    assert result.desired_observation == "container ownership"
    assert result.outcome == "blocked"
    assert "container_inventory" in result.required_observations
    assert "container_port_mapping" in result.required_observations
    assert result.required_authority["container_inventory"] == "docker_group_or_root"
    assert result.required_authority["container_port_mapping"] == "docker_group_or_root"
    assert set(result.remaining_observations) == {
        "container_inventory",
        "container_port_mapping",
    }
    assert result.boundary["read_only"] is True
    assert result.boundary["records"] is False
    assert result.boundary["writes_event_ledger"] is False
    assert result.boundary["mutates_cluster"] is False


def test_supplied_profile_overrides_unrelated_current_approval_state():
    state = State(workspace_id="test")
    state.approvals["appr_docker"] = Approval(
        id="appr_docker",
        action="observation.docker_socket_read",
        scope="local",
        approved_by="operator@example.com",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
        constraints={"observation_domain": "docker_socket_read"},
    )

    result = evaluate_container_ownership_authority_slice(state, PROFILE)

    assert result.available_authority["docker_socket_read"] == "unavailable"
    assert result.outcome == "blocked"
    assert any(
        "supplied profile remains authoritative" in item for item in result.uncertainty
    )


def test_container_ownership_slice_has_no_writes_or_acquisition_behavior():
    state = State(workspace_id="test")
    before = (
        len(state.facts),
        len(state.observed_facts),
        len(state.inferred_facts),
        len(state.approvals),
        len(state.events) if hasattr(state, "events") else 0,
    )

    result = evaluate_container_ownership_authority_slice(state, PROFILE)

    after = (
        len(state.facts),
        len(state.observed_facts),
        len(state.inferred_facts),
        len(state.approvals),
        len(state.events) if hasattr(state, "events") else 0,
    )
    assert after == before
    assert result.boundary == {
        "read_only": True,
        "records": False,
        "writes_event_ledger": False,
        "mutates_cluster": False,
        "provider_acquisition": False,
        "permission_creation": False,
        "executes_observation": False,
    }


def test_absent_subject_pressure_still_reports_domain_requirements_and_uncertainty():
    result = evaluate_container_ownership_authority_slice(
        State(workspace_id="test"), PROFILE
    )

    assert result.required_observations == (
        "container_inventory",
        "container_port_mapping",
    )
    assert any(
        item
        == "subject-specific ownership pressure exists only when ownership_discrepancies emits matching service conflicts"
        for item in result.uncertainty
    )
