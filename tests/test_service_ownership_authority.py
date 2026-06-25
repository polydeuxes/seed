import json
from datetime import datetime, timezone

import scripts.seed_local as seed_local
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.service_ownership_authority import (
    CONSTRAINED_AUTHORITY_PROFILE,
    evaluate_service_ownership_authority_slice,
    format_service_ownership_authority,
)
from seed_runtime.models import Fact
from seed_runtime.state import State


def _state_with_service_endpoint_only() -> State:
    state = State(workspace_id="test")
    fact = Fact(
        id="fact_service_endpoint",
        subject_id="svc:web",
        predicate="prometheus_target",
        value="web:8080",
        evidence_ids=[],
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        source_type="user",
        confidence=1.0,
    )
    state.facts[fact.id] = fact
    state.observed_facts[fact.id] = fact
    return state


def test_service_ownership_slice_is_partially_reachable_under_constrained_profile():
    result = evaluate_service_ownership_authority_slice(
        State(workspace_id="test"), CONSTRAINED_AUTHORITY_PROFILE
    )

    assert result.desired_observation == "service ownership"
    assert result.outcome == "partially_reachable"
    assert result.current_strategy == "composite_local_service_attribution_observation"
    assert result.strategy_status == result.outcome
    assert result.remaining_observations == result.blocked_observations
    assert result.remaining_uncertainty == result.uncertainty
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
    assert (
        result.blocking_boundary
        == "docker_or_root_container_runtime_authority_unavailable"
    )


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
        "current_strategy",
        "strategy_status",
        "remaining_observations",
        "uncertainty",
        "remaining_uncertainty",
        "blocking_boundary",
        "boundary",
    ]:
        assert key in payload
    assert payload["desired_observation"] == "service ownership"
    assert payload["outcome"] == "partially_reachable"
    assert (
        payload["current_strategy"] == "composite_local_service_attribution_observation"
    )
    assert payload["strategy_status"] == payload["outcome"]
    assert payload["remaining_observations"] == payload["blocked_observations"]
    assert payload["remaining_uncertainty"] == payload["uncertainty"]
    assert (
        payload["blocking_boundary"]
        == "docker_or_root_container_runtime_authority_unavailable"
    )


def test_service_ownership_blocked_observations_include_privilege_explanation_fields():
    result = evaluate_service_ownership_authority_slice(
        State(workspace_id="test"), CONSTRAINED_AUTHORITY_PROFILE
    )

    by_observation = {
        item["observation"]: item for item in result.blocked_observation_details
    }

    assert set(by_observation) == {
        "container_inventory",
        "container_port_mapping",
    }
    for observation in ["container_inventory", "container_port_mapping"]:
        assert by_observation[observation]["guidance_status"] == "registered"
        assert by_observation[observation]["implementation_evidence"] == "registered"
        assert by_observation[observation]["limiting_reason"] == "missing_authority"


def test_service_ownership_json_extends_blocked_observations_without_replacing_old_fields(
    capsys,
):
    assert seed_local.main(["--service-ownership-authority", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert payload["blocked_observations"] == [
        "container_inventory",
        "container_port_mapping",
    ]
    assert payload["remaining_observations"] == payload["blocked_observations"]
    assert payload["blocked_observation_details"] == [
        {
            "observation": "container_inventory",
            "guidance_status": "registered",
            "implementation_evidence": "registered",
            "limiting_reason": "missing_authority",
        },
        {
            "observation": "container_port_mapping",
            "guidance_status": "registered",
            "implementation_evidence": "registered",
            "limiting_reason": "missing_authority",
        },
    ]


def test_service_ownership_human_output_renders_blocked_observation_explanations(
    capsys,
):
    assert seed_local.main(["--service-ownership-authority"]) == 0

    output = capsys.readouterr().out

    assert "  - container_inventory\n    Guidance: registered" in output
    assert "    Implementation evidence: registered" in output
    assert "    Limiting reason: missing_authority" in output
    assert "  - container_port_mapping\n    Guidance: registered" in output


def test_service_ownership_blocking_boundary_only_when_docker_root_blocks_runtime():
    profile = dict(CONSTRAINED_AUTHORITY_PROFILE)
    profile["docker_socket_read"] = "available"

    result = evaluate_service_ownership_authority_slice(
        State(workspace_id="test"), profile
    )

    assert result.blocked_observations == ()
    assert result.remaining_observations == ()
    assert result.blocking_boundary is None
    assert "blocking_boundary" not in result.to_json_dict()


def test_cli_service_ownership_authority_renders_composite_inquiry_flow(capsys):
    assert seed_local.main(["--service-ownership-authority"]) == 0

    output = capsys.readouterr().out

    expected_order = [
        "Goal",
        "Desired observation: service ownership",
        "Strategy",
        "Current strategy: composite_local_service_attribution_observation",
        "Observation state",
        "Reachable observations:",
        "Remaining observations:",
        "Authority",
        "Required authority:",
        "Available authority:",
        "Execution",
        "Strategy status: partially_reachable",
        "Outcome: partially_reachable",
        "Blocking boundary: docker_or_root_container_runtime_authority_unavailable",
        "Uncertainty:",
        "Boundary",
    ]
    cursor = -1
    for text in expected_order:
        next_index = output.find(text, cursor + 1)
        assert next_index > cursor
        cursor = next_index


def test_service_ownership_available_docker_socket_does_not_change_observation_semantics():
    result = evaluate_service_ownership_authority_slice(
        State(workspace_id="test"),
        {**CONSTRAINED_AUTHORITY_PROFILE, "docker_socket_read": "available"},
    )

    assert result.outcome == "reachable"
    assert set(result.reachable_observations) == {
        "tcp_listen_inventory",
        "listener_process_inventory",
        "systemd_unit_inventory",
    }
    assert set(result.blocked_observations) == set()


def test_service_ownership_inventory_registration_is_correct():
    entry = next(
        e for e in DIAGNOSTIC_INVENTORY if e.name == "service_ownership_authority"
    )

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

    result = evaluate_service_ownership_authority_slice(
        state, CONSTRAINED_AUTHORITY_PROFILE
    )

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


def test_service_ownership_consumes_existing_ownership_discrepancy_summary():
    result = evaluate_service_ownership_authority_slice(
        _state_with_service_endpoint_only(), CONSTRAINED_AUTHORITY_PROFILE
    )

    by_observation = {
        item["observation"]: item for item in result.blocked_observation_details
    }

    summary = by_observation["container_inventory"]["ownership_discrepancy"]
    assert summary == {
        "conflict": "insufficient_evidence",
        "reason": "Only endpoint/target evidence exists; no host, process, container, or local listener evidence was observed.",
        "needed_evidence": "container_inventory",
        "candidate_capability": "container_inventory",
    }


def test_service_ownership_discrepancy_summary_uses_existing_capability_join_only():
    result = evaluate_service_ownership_authority_slice(
        _state_with_service_endpoint_only(), CONSTRAINED_AUTHORITY_PROFILE
    )

    by_observation = {
        item["observation"]: item for item in result.blocked_observation_details
    }

    assert "ownership_discrepancy" in by_observation["container_inventory"]
    assert "ownership_discrepancy" not in by_observation["container_port_mapping"]


def test_service_ownership_json_preserves_schema_while_nesting_discrepancy_summary():
    result = evaluate_service_ownership_authority_slice(
        _state_with_service_endpoint_only(), CONSTRAINED_AUTHORITY_PROFILE
    )

    payload = result.to_json_dict()

    assert payload["blocked_observations"] == [
        "container_inventory",
        "container_port_mapping",
    ]
    container = payload["blocked_observation_details"][0]
    assert container["observation"] == "container_inventory"
    assert container["guidance_status"] == "registered"
    assert container["implementation_evidence"] == "registered"
    assert container["limiting_reason"] == "missing_authority"
    assert container["ownership_discrepancy"]["conflict"] == "insufficient_evidence"


def test_service_ownership_human_output_renders_related_discrepancy_summary():
    result = evaluate_service_ownership_authority_slice(
        _state_with_service_endpoint_only(), CONSTRAINED_AUTHORITY_PROFILE
    )

    output = format_service_ownership_authority(result)

    assert "Related ownership discrepancy" in output
    assert "      Conflict: insufficient_evidence" in output
    assert "      Needed evidence: container_inventory" in output
    assert "      Candidate capability: container_inventory" in output
