import json

import scripts.seed_local as seed_local
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.service_ownership_authority import (
    CONSTRAINED_AUTHORITY_PROFILE,
    evaluate_service_ownership_authority_slice,
)
from seed_runtime.state import State


def test_service_ownership_slice_is_partially_reachable_under_constrained_profile():
    result = evaluate_service_ownership_authority_slice(
        State(workspace_id="test"), CONSTRAINED_AUTHORITY_PROFILE
    )

    assert result.desired_observation == "service ownership"
    assert result.outcome == "partially_reachable"
    assert set(result.reachable_observations) >= {
        "tcp_listen_inventory",
        "listener_process_inventory",
        "systemd_unit_inventory",
    }
    assert set(result.blocked_observations) == {
        "container_inventory",
        "container_port_mapping",
    }


def test_service_ownership_reachable_observations_include_listener_and_systemd_evidence():
    result = evaluate_service_ownership_authority_slice(
        State(workspace_id="test"), CONSTRAINED_AUTHORITY_PROFILE
    )

    assert result.required_authority["tcp_listen_inventory"] == "local_passive"
    assert result.required_authority["systemd_unit_inventory"] == "local_passive"
    assert "tcp_listen_inventory" in result.reachable_observations
    assert "systemd_unit_inventory" in result.reachable_observations
    assert any("listener observation support" in item for item in result.uncertainty)
    assert any("systemd" in item for item in result.uncertainty)


def test_service_ownership_blocks_docker_root_dependent_observations():
    result = evaluate_service_ownership_authority_slice(
        State(workspace_id="test"), CONSTRAINED_AUTHORITY_PROFILE
    )

    assert result.required_authority["container_inventory"] == "docker_group_or_root"
    assert result.required_authority["container_port_mapping"] == "docker_group_or_root"
    assert result.available_authority["root"] == "unavailable"
    assert result.available_authority["docker_socket_read"] == "unavailable"
    assert "container_inventory" in result.blocked_observations
    assert "container_port_mapping" in result.blocked_observations


def test_cli_service_ownership_authority_json_contains_required_shape(capsys):
    assert seed_local.main(["--service-ownership-authority", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    for key in [
        "desired_observation",
        "required_observations",
        "required_authority",
        "reachable_observations",
        "blocked_observations",
        "available_authority",
        "outcome",
        "uncertainty",
        "boundary",
    ]:
        assert key in payload
    assert payload["desired_observation"] == "service ownership"
    assert payload["outcome"] == "partially_reachable"


def test_service_ownership_inventory_registration_is_correct():
    entry = next(e for e in DIAGNOSTIC_INVENTORY if e.name == "service_ownership_authority")

    assert entry.cli_flags == ("--service-ownership-authority",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.reads_diagnostic_facts is True
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False


def test_service_ownership_shape_audit_is_consistent():
    rows = [
        row
        for row in build_diagnostic_shape_audit()
        if row.diagnostic == "service_ownership_authority"
    ]

    assert rows
    assert [row for row in rows if row.status == "mismatch"] == []
    observed = {row.field: row.observed for row in rows}
    assert observed["supports_json"] is True
    assert observed["supports_record"] is False
    assert observed["writes_event_ledger"] is False
    assert observed["mutates_cluster"] is False
    assert observed["reads_diagnostic_facts"] is True


def test_service_ownership_slice_has_no_writes_permissions_or_acquisition_behavior():
    state = State(workspace_id="test")
    before = (
        len(state.facts),
        len(state.observed_facts),
        len(state.inferred_facts),
        len(state.approvals),
        len(state.events) if hasattr(state, "events") else 0,
    )

    result = evaluate_service_ownership_authority_slice(state, CONSTRAINED_AUTHORITY_PROFILE)

    after = (
        len(state.facts),
        len(state.observed_facts),
        len(state.inferred_facts),
        len(state.approvals),
        len(state.events) if hasattr(state, "events") else 0,
    )
    assert after == before
    assert result.boundary["writes_event_ledger"] is False
    assert result.boundary["mutates_cluster"] is False
    assert result.boundary["permission_creation"] is False
    assert result.boundary["provider_acquisition"] is False
