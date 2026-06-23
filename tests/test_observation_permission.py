import json
from datetime import datetime, timedelta, timezone

import scripts.seed_local as seed_local
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.models import Approval
from seed_runtime.observation_permission import build_observation_permission
from seed_runtime.state import State


def _domain(report, name):
    return next(domain for domain in report.domains if domain.domain == name)


def test_cli_observation_permission_renders_human_readable(capsys):
    assert seed_local.main(["--observation-permission", "neighbor_table_read"]) == 0

    output = capsys.readouterr().out

    assert "Observation Permission" in output
    assert "Domain:" in output
    assert "neighbor_table_read" in output
    assert "Observation Class:" in output
    assert "local_passive" in output
    assert "Permission State:" in output
    assert "requires_operator_expression" in output


def test_cli_observation_permission_json_is_valid(capsys):
    assert seed_local.main(["--observation-permission", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert payload["boundary"]["read_only"] is True
    assert payload["boundary"]["writes_event_ledger"] is False
    assert payload["boundary"]["mutates_cluster"] is False
    assert {entry["domain"] for entry in payload["domains"]} >= {
        "neighbor_table_read",
        "traffic_capture",
        "active_network_probe",
        "docker_socket_read",
    }


def test_domain_class_permission_and_authority_visibility():
    report = build_observation_permission(State(workspace_id="test"), "traffic_capture")
    entry = _domain(report, "traffic_capture")

    assert entry.observation_class == "network_passive"
    assert entry.permission_state == "requires_operator_expression"
    assert entry.authority_evidence == ()
    assert "reusable approval not observed" in entry.reasoning


def test_unknown_domain_uses_unknown_state():
    report = build_observation_permission(State(workspace_id="test"), "unmapped_domain")
    entry = _domain(report, "unmapped_domain")

    assert entry.observation_class == "unknown"
    assert entry.permission_state == "unknown"
    assert entry.reusable_permission == "unknown"


def test_approval_evidence_uses_existing_approval_model_without_new_authority_system():
    state = State(workspace_id="test")
    state.approvals["appr_1"] = Approval(
        id="appr_1",
        action="observation.neighbor_table_read",
        scope="local",
        approved_by="operator@example.com",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
        constraints={"observation_domain": "neighbor_table_read"},
    )

    entry = _domain(
        build_observation_permission(state, "neighbor_table_read"),
        "neighbor_table_read",
    )

    assert entry.permission_state == "granted"
    assert entry.reusable_permission == "granted"
    assert entry.authority_evidence
    assert (
        "Approval(action=observation.neighbor_table_read" in entry.authority_evidence[0]
    )


def test_manual_invocation_reasoning_visibility():
    entry = _domain(
        build_observation_permission(
            State(workspace_id="test"), "active_network_probe"
        ),
        "active_network_probe",
    )

    assert (
        "manual operator invocation may authorize only the current execution"
        in entry.reasoning
    )
    assert (
        "manual operator invocation does not create reusable Seed permission"
        in entry.reasoning
    )
    assert entry.future_autonomous_invocation == "requires_operator_expression"


def test_observation_permission_boundary_is_read_only():
    report = build_observation_permission(State(workspace_id="test"))

    assert report.boundary["read_only"] is True
    assert report.boundary["writes_event_ledger"] is False
    assert report.boundary["mutates_cluster"] is False
    assert report.boundary["permission_enforcement"] is False
    assert report.boundary["approval_storage"] is False
    assert report.boundary["runtime_autonomy"] is False


def test_observation_permission_visibility_registration():
    entry = next(e for e in DIAGNOSTIC_INVENTORY if e.name == "observation_permission")

    assert entry.cli_flags == ("--observation-permission",)
    assert entry.supports_json
    assert not entry.supports_record
    assert entry.record_scope == "none"
    assert not entry.writes_event_ledger
    assert not entry.mutates_cluster


def test_observation_permission_shape_registration_consistency():
    rows = [
        r
        for r in build_diagnostic_shape_audit()
        if r.diagnostic == "observation_permission"
    ]

    assert rows
    fields = {row.field: row for row in rows}
    assert fields["supports_json"].status == "consistent"
    assert fields["writes_event_ledger"].status == "consistent"
    assert fields["mutates_cluster"].status == "consistent"
    assert fields["supports_record"].status == "consistent"
