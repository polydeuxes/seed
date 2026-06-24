import json

import scripts.seed_local as seed_local
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.listener_endpoint_authority import (
    CONSTRAINED_AUTHORITY_PROFILE,
    evaluate_listener_endpoint_authority_slice,
)
from seed_runtime.state import State


def test_listener_endpoint_slice_is_reachable_under_constrained_profile():
    result = evaluate_listener_endpoint_authority_slice(
        State(workspace_id="test"), CONSTRAINED_AUTHORITY_PROFILE
    )

    assert result.desired_observation == "local listener endpoint inventory"
    assert result.available_authority["local_passive"] == "available"
    assert result.available_authority["root"] == "unavailable"
    assert result.available_authority["docker_socket_read"] == "unavailable"
    assert result.available_authority["active_network_probe"] == "unauthorized"
    assert result.outcome == "reachable"


def test_reachable_observations_include_listener_endpoint_evidence():
    result = evaluate_listener_endpoint_authority_slice(
        State(workspace_id="test"), CONSTRAINED_AUTHORITY_PROFILE
    )

    assert set(result.reachable_observations) == {
        "listening_protocol",
        "listening_address",
        "listening_port",
        "local_socket_table_evidence",
    }
    assert all(authority == "local_passive" for authority in result.required_authority.values())
    assert any("listening_endpoint" in item for item in result.uncertainty)
    assert any("local socket-table evidence" in item for item in result.uncertainty)


def test_blocked_observations_are_empty_for_supported_local_passive_boundary():
    result = evaluate_listener_endpoint_authority_slice(
        State(workspace_id="test"), CONSTRAINED_AUTHORITY_PROFILE
    )

    assert result.blocked_observations == ()


def test_cli_listener_endpoint_authority_json_contains_required_shape(capsys):
    assert seed_local.main(["--listener-endpoint-authority", "--json"]) == 0

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
    assert payload["desired_observation"] == "local listener endpoint inventory"
    assert payload["outcome"] == "reachable"


def test_listener_endpoint_inventory_registration_is_correct():
    entry = next(e for e in DIAGNOSTIC_INVENTORY if e.name == "listener_endpoint_authority")

    assert entry.cli_flags == ("--listener-endpoint-authority",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.reads_diagnostic_facts is False
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False
    assert entry.uses_repo_files is True
    assert entry.uses_projected_state is True


def test_listener_endpoint_shape_audit_is_consistent():
    rows = [
        row
        for row in build_diagnostic_shape_audit()
        if row.diagnostic == "listener_endpoint_authority"
    ]

    assert rows
    assert [row for row in rows if row.status == "mismatch"] == []
    observed = {row.field: row.observed for row in rows}
    assert observed["supports_json"] is True
    assert observed["supports_record"] is False
    assert observed["writes_event_ledger"] is False
    assert observed["mutates_cluster"] is False
    assert observed["reads_diagnostic_facts"] is False


def test_listener_endpoint_slice_has_no_writes_permissions_or_acquisition_behavior():
    state = State(workspace_id="test")
    before = (
        len(state.facts),
        len(state.observed_facts),
        len(state.inferred_facts),
        len(state.approvals),
        len(state.events) if hasattr(state, "events") else 0,
    )

    result = evaluate_listener_endpoint_authority_slice(state, CONSTRAINED_AUTHORITY_PROFILE)

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
    assert result.boundary["executes_observation"] is False
