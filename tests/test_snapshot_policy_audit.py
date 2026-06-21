import json
from datetime import datetime, timezone

import scripts.seed_local as seed_local
from seed_runtime.audit_snapshots import create_audit_snapshot
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.snapshot_policy_audit import (
    build_snapshot_policy_audit,
    format_snapshot_policy_audit,
    snapshot_policy_audit_json,
)
from seed_runtime.state import State


def _ownership_snapshot(tmp_path, snapshot_id, rows=None):
    create_audit_snapshot(
        repo_root=tmp_path,
        kind="ownership_discrepancies",
        payload=rows or [],
        command="seed --audit-snapshot ownership_discrepancies",
        seed_db=None,
        events=[],
        projection_version="v1",
        snapshot_id=snapshot_id,
    )


def _observation_snapshot(tmp_path, snapshot_id, predicates=None):
    predicates = predicates or []
    create_audit_snapshot(
        repo_root=tmp_path,
        kind="observation_inventory",
        payload={
            "predicates": [{"predicate": p} for p in predicates],
            "providers": [],
            "families": [],
            "summary": {"predicate_count": len(predicates)},
        },
        command="seed --audit-snapshot observation_inventory",
        seed_db=None,
        events=[],
        projection_version="v1",
        snapshot_id=snapshot_id,
    )


def test_snapshot_policy_audit_renders_existing_missing_comparison_recommendations_and_story_dependency(
    tmp_path,
):
    _ownership_snapshot(tmp_path, "2026-06-20T160000Z")
    _ownership_snapshot(tmp_path, "2026-06-20T170000Z")
    _observation_snapshot(tmp_path, "2026-06-20T180000Z")

    audit = build_snapshot_policy_audit(
        tmp_path, now=datetime(2026, 6, 21, tzinfo=timezone.utc)
    )
    rendered = format_snapshot_policy_audit(audit)

    assert "Snapshot Policy Audit" in rendered
    assert "ownership_discrepancies" in rendered
    assert "observation_inventory" in rendered
    assert "capability_needs" in rendered
    assert "comparison available: yes" in rendered
    assert "snapshot_recommended" in rendered
    assert "operational_story" in rendered
    assert "snapshot health: partial" in rendered


def test_snapshot_policy_audit_json_is_valid_and_cli_supports_json(
    tmp_path, monkeypatch, capsys
):
    _ownership_snapshot(tmp_path, "2026-06-20T160000Z")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    code = seed_local.main(["--snapshot-policy-audit", "--json"])
    payload = json.loads(capsys.readouterr().out)

    assert code == 0
    assert payload["snapshot_kinds"]
    assert payload["comparison_availability"]
    assert payload["recommendations"]
    assert payload["writes_event_ledger"] is False
    assert payload["mutates_cluster"] is False


def test_snapshot_policy_audit_empty_state_is_sane(tmp_path):
    audit = build_snapshot_policy_audit(tmp_path)
    payload = snapshot_policy_audit_json(audit)

    assert {row["status"] for row in payload["snapshot_kinds"]} == {"unsnapshotted"}
    assert all(
        row["comparison_available"] is False for row in payload["snapshot_kinds"]
    )
    assert any(
        row["surface"] == "operational_story" for row in payload["operational_surfaces"]
    )
    assert "none" in format_snapshot_policy_audit(audit)


def test_snapshot_policy_audit_does_not_write_event_ledger_or_mutate_cluster(tmp_path):
    db = tmp_path / "events.sqlite"
    ledger = SQLiteEventLedger(db)
    before_events = ledger.list_events()
    state = State(workspace_id="ws")
    before_state = repr(state)

    build_snapshot_policy_audit(tmp_path)

    assert ledger.list_events() == before_events
    assert repr(state) == before_state


def test_snapshot_policy_audit_registered_in_inventory_shape_and_surface_inventory():
    from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
    from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
    from seed_runtime.operational_surface_inventory import (
        build_operational_surface_inventory,
    )

    entry = next(e for e in DIAGNOSTIC_INVENTORY if e.name == "snapshot_policy_audit")
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False

    rows = [
        r
        for r in build_diagnostic_shape_audit()
        if r.diagnostic == "snapshot_policy_audit"
    ]
    assert rows
    assert {r.status for r in rows} == {"consistent"}

    surfaces = build_operational_surface_inventory(seed_local.build_parser())
    assert any(surface.name == "--snapshot-policy-audit" for surface in surfaces)
