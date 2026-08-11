import json

import scripts.seed_local as seed_local
from seed_runtime.audit_snapshots import create_audit_snapshot
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.history_brief import (
    build_history_brief,
    format_history_brief,
    history_brief_json,
)
from seed_runtime.state import State


def _ownership_snapshot(tmp_path, snapshot_id, rows):
    create_audit_snapshot(
        repo_root=tmp_path,
        kind="ownership_discrepancies",
        payload=rows,
        command="seed --audit-snapshot ownership_discrepancies",
        seed_db=None,
        events=[],
        projection_version="v1",
        snapshot_id=snapshot_id,
    )


def _observation_snapshot(tmp_path, snapshot_id, predicates):
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


def _row(subject):
    return {"kind": "service", "subject": subject, "conflict": "missing_owner"}


def test_history_brief_renders_and_json_is_valid(tmp_path, monkeypatch, capsys):
    _ownership_snapshot(tmp_path, "2026-06-20T160000Z", [_row("svc-a")])
    _ownership_snapshot(tmp_path, "2026-06-20T170000Z", [])
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert "History Brief" in format_history_brief(build_history_brief(tmp_path))
    assert seed_local.main(["--history-brief", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert set(payload) >= {
        "changes",
        "stable",
        "repository_context",
        "historical_confidence",
        "unsupported_conclusions",
    }


def test_history_brief_surfaces_changes_stability_repository_confidence_and_unsupported(tmp_path):
    _ownership_snapshot(tmp_path, "2026-06-20T160000Z", [_row("svc-a")])
    _ownership_snapshot(tmp_path, "2026-06-20T170000Z", [_row("svc-a"), _row("svc-b")])
    _observation_snapshot(tmp_path, "2026-06-20T180000Z", ["host.name"])
    _observation_snapshot(tmp_path, "2026-06-20T190000Z", ["host.name"])

    brief = build_history_brief(tmp_path)
    payload = history_brief_json(brief)
    rendered = format_history_brief(brief)

    assert any(row["metric"] == "unresolved_ownership_rows" for row in payload["changes"])
    assert any(row["metric"] == "observable_predicates" for row in payload["stable"])
    assert payload["repository_context"]["state"] == "repository context unavailable"
    assert payload["historical_confidence"]["level"] in {"snapshot_constrained", "partial"}
    assert payload["historical_confidence"]["causation"] == "not proven"
    assert any("capability_pressure" in row["conclusion"] for row in payload["unsupported_conclusions"])
    assert "correlation may be visible" in rendered
    assert "causation is not proven" in rendered


def test_history_brief_empty_state_is_sane(tmp_path):
    brief = build_history_brief(tmp_path)
    payload = history_brief_json(brief)

    assert payload["changes"] == []
    assert payload["stable"] == []
    assert payload["historical_confidence"]["comparison"] == "insufficient comparison history"
    assert payload["unsupported_conclusions"]
    assert "none" in format_history_brief(brief)


def test_history_brief_does_not_write_events_or_mutate_cluster(tmp_path):
    db = tmp_path / "events.sqlite"
    ledger = SQLiteEventLedger(db)
    before_events = ledger.list_events()
    state = State(workspace_id="ws")
    before_state = repr(state)

    brief = build_history_brief(tmp_path)

    assert brief.writes_event_ledger is False
    assert brief.mutates_cluster is False
    assert ledger.list_events() == before_events
    assert repr(state) == before_state


def test_history_brief_registered_in_inventory_shape_and_surface_inventory():
    from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
    from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
    from seed_runtime.operational_surface_inventory import build_operational_surface_inventory

    entry = next(e for e in DIAGNOSTIC_INVENTORY if e.name == "history_brief")
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False

    rows = [r for r in build_diagnostic_shape_audit() if r.diagnostic == "history_brief"]
    assert rows
    assert {r.status for r in rows} == {"consistent"}

    surfaces = build_operational_surface_inventory(seed_local.build_parser())
    assert any(surface.name == "--history-brief" for surface in surfaces)
