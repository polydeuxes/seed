import json
from datetime import datetime, timezone

import scripts.seed_local as seed_local
from seed_runtime.audit_snapshots import create_audit_snapshot
from seed_runtime.facts import Fact
from seed_runtime.models import Event
from seed_runtime.ops_brief import build_ops_brief, format_ops_brief
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.state import State


def _fact(fid, subject, predicate, value):
    return Fact(
        id=fid,
        subject_id=subject,
        predicate=predicate,
        value=value,
        observed_at=datetime(2026, 6, 20, tzinfo=timezone.utc),
    )


def _state_with_pressure():
    state = State(workspace_id="ws")
    state.facts = {
        "f_storage": _fact("f_storage", "fs1", "mountpoint", "/data"),
        "f_service": _fact("f_service", "svc1", "service_port", "8080"),
        "f_need": _fact(
            "f_need",
            "diagnostic_run:ops-test",
            "diagnostic_capability_need",
            {
                "diagnostic_name": "ownership_discrepancies",
                "diagnostic_subject": "svc1",
                "candidate_capability": "listener_process_inventory",
                "needed_evidence": "listener_process_inventory",
            },
        ),
    }
    return state


def test_ops_brief_renders_all_sections(tmp_path):
    brief = build_ops_brief(_state_with_pressure(), repo_root=tmp_path)
    rendered = format_ops_brief(brief)

    for section in [
        "Operational Brief",
        "Observations",
        "Ownership",
        "Capabilities",
        "Diagnostics",
        "Snapshots",
        "Recommended Next Actions",
    ]:
        assert section in rendered


def test_cli_ops_brief_json_emits_valid_json(capsys):
    assert seed_local.main(["--ops-brief", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert set(payload) == {
        "observations",
        "ownership",
        "capabilities",
        "diagnostics",
        "snapshots",
        "recommended_actions",
    }
    assert isinstance(payload["recommended_actions"], list)


def test_ops_brief_includes_observation_ownership_capability_diagnostic_and_snapshot_summaries(
    tmp_path,
):
    create_audit_snapshot(
        repo_root=tmp_path,
        kind="observation_inventory",
        payload={"summary": {"provider_count": 0}},
        command="seed --audit-snapshot observation_inventory",
        seed_db=None,
        events=[Event(id="evt1", kind="test", workspace_id="ws")],
        projection_version="test",
        snapshot_id="2026-06-20T164122Z",
    )

    brief = build_ops_brief(_state_with_pressure(), repo_root=tmp_path)

    assert {
        "providers": brief.observations["providers"],
        "predicates": brief.observations["predicates"],
        "unused_predicates": brief.observations["unused_predicates"],
        "orphaned_predicates": brief.observations["orphaned_predicates"],
        "fragile_predicates": brief.observations["fragile_predicates"],
    } == {
        "providers": 0,
        "predicates": 0,
        "unused_predicates": 0,
        "orphaned_predicates": 0,
        "fragile_predicates": 0,
    }
    assert brief.ownership["storage_ambiguities"] >= 1
    assert brief.ownership["service_ambiguities"] >= 1
    assert brief.capabilities["top_capability_needs"][0] == {
        "capability": "listener_process_inventory",
        "subject_count": 1,
    }
    assert brief.diagnostics["diagnostics"] >= 1
    assert brief.diagnostics["shape_mismatches"] >= 0
    assert brief.snapshots["latest_snapshot"] == "2026-06-20T164122Z"
    assert brief.snapshots["snapshot_count"] == 1


def test_ops_brief_summarizes_unrecorded_owner_not_observed_capability_needs(tmp_path):
    state = State(workspace_id="ws")
    state.facts = {
        "f_target": _fact("f_target", "api", "prometheus_target", "127.0.0.1:9100"),
        "f_listener": _fact(
            "f_listener", "node-a", "listening_socket", "tcp 127.0.0.1:9100"
        ),
    }

    brief = build_ops_brief(state, repo_root=tmp_path)
    rendered = format_ops_brief(brief)

    assert brief.ownership["conflicts"]["owner_not_observed"] == 1
    assert {
        "capability": "listener_process_inventory",
        "subject_count": 1,
    } in brief.capabilities["top_capability_needs"]
    assert "1. listener_process_inventory (1)" in rendered
    assert "container_inventory (1)" in rendered


def test_recommended_actions_are_generated_from_evidence():
    brief = build_ops_brief(_state_with_pressure())

    assert any(
        "listener_process_inventory" in action["action"]
        for action in brief.recommended_actions
    )
    assert all(action["reason"] for action in brief.recommended_actions)


def test_empty_state_behavior_is_sane(tmp_path):
    brief = build_ops_brief(State(workspace_id="ws"), repo_root=tmp_path)

    assert brief.observations["providers"] == 0
    assert brief.ownership["storage_ambiguities"] == 0
    assert brief.capabilities["top_capability_needs"] == []
    assert brief.snapshots["latest_snapshot"] is None
    assert brief.recommended_actions
    assert all(
        action["action"] and action["reason"] for action in brief.recommended_actions
    )


def test_ops_brief_does_not_mutate_cluster_or_write_event_ledger(tmp_path):
    db_path = tmp_path / "seed.sqlite"

    assert (
        seed_local.main(["--db", str(db_path), "--fact", "host1", "role", "web"]) == 0
    )
    ledger = SQLiteEventLedger(str(db_path))
    try:
        before = ledger.list_events("default")
    finally:
        ledger.close()
    assert seed_local.main(["--db", str(db_path), "--ops-brief", "--json"]) == 0
    ledger = SQLiteEventLedger(str(db_path))
    try:
        after = ledger.list_events("default")
    finally:
        ledger.close()

    assert [event.id for event in after] == [event.id for event in before]
