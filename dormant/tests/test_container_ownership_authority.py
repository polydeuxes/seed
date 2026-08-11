import json
from datetime import datetime, timedelta, timezone

import scripts.seed_local as seed_local
from seed_runtime.container_ownership_authority import (
    evaluate_container_ownership_authority_slice,
)
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
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
    assert result.current_strategy == "container_runtime_observation"
    assert result.strategy_status == result.outcome
    assert (
        result.blocking_boundary
        == "docker_or_root_container_runtime_authority_unavailable"
    )
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
    assert result.remaining_uncertainty == result.uncertainty


def test_container_ownership_blocking_boundary_only_when_docker_or_root_unavailable():
    profile = dict(PROFILE)
    profile["docker_socket_read"] = "available"

    result = evaluate_container_ownership_authority_slice(
        State(workspace_id="test"), profile
    )

    assert result.required_authority == {
        "container_inventory": "docker_group_or_root",
        "container_port_mapping": "docker_group_or_root",
    }
    assert result.available_authority["root"] == "unavailable"
    assert result.available_authority["docker_socket_read"] == "available"
    assert result.outcome == "unknown"
    assert result.strategy_status == result.outcome
    assert result.blocking_boundary is None
    assert "blocking_boundary" not in result.to_json_dict()


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


def test_cli_container_ownership_authority_renders_constrained_profile(capsys):
    assert seed_local.main(["--container-ownership-authority"]) == 0

    output = capsys.readouterr().out

    assert "container ownership" in output
    assert "blocked" in output
    assert "container_inventory" in output
    assert "container_port_mapping" in output
    assert "docker_group_or_root" in output
    assert "Current strategy: container_runtime_observation" in output
    assert "Strategy status: blocked" in output
    assert (
        "Blocking boundary: docker_or_root_container_runtime_authority_unavailable"
        in output
    )
    assert output.count("Uncertainty:") == 1
    assert "Remaining uncertainty:" not in output

    section_order = [
        "Goal",
        "Strategy",
        "Authority",
        "Execution",
        "Remaining work",
        "Boundary",
    ]
    positions = [output.index(f"\n{section}\n") for section in section_order]
    assert positions == sorted(positions)


def test_cli_container_ownership_authority_json_contains_required_shape(capsys):
    assert seed_local.main(["--container-ownership-authority", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert payload["desired_observation"] == "container ownership"
    for key in [
        "desired_observation",
        "required_observations",
        "required_authority",
        "available_authority",
        "outcome",
        "current_strategy",
        "strategy_status",
        "blocking_boundary",
        "uncertainty",
        "remaining_uncertainty",
        "boundary",
    ]:
        assert key in payload
    assert payload["outcome"] == "blocked"
    assert payload["current_strategy"] == "container_runtime_observation"
    assert payload["strategy_status"] == payload["outcome"]
    assert (
        payload["blocking_boundary"]
        == "docker_or_root_container_runtime_authority_unavailable"
    )
    assert payload["remaining_uncertainty"] == payload["uncertainty"]
    assert payload["boundary"]["writes_event_ledger"] is False
    assert payload["boundary"]["mutates_cluster"] is False


def test_container_ownership_authority_inventory_and_shape_audit_boundary():
    entry = next(
        e for e in DIAGNOSTIC_INVENTORY if e.name == "container_ownership_authority"
    )
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False

    rows = [
        row
        for row in build_diagnostic_shape_audit()
        if row.diagnostic == "container_ownership_authority"
    ]
    assert rows
    assert [row for row in rows if row.status == "mismatch"] == []
    assert {row.field: row.observed for row in rows}["writes_event_ledger"] is False
    assert {row.field: row.observed for row in rows}["mutates_cluster"] is False
    assert {row.field: row.observed for row in rows}["supports_record"] is False
