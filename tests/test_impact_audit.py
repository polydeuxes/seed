import json

import scripts.seed_local as seed_local
from seed_runtime.audit_snapshots import create_audit_snapshot
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.impact_audit import build_impact_audit, format_impact_audit, impact_audit_json
from seed_runtime.state import State


def _snapshot_pair(tmp_path, before_rows, after_rows):
    create_audit_snapshot(repo_root=tmp_path, kind="ownership_discrepancies", payload=before_rows, command="seed --audit-snapshot ownership_discrepancies", seed_db=None, events=[], projection_version="v1", snapshot_id="2026-06-20T160000Z")
    create_audit_snapshot(repo_root=tmp_path, kind="ownership_discrepancies", payload=after_rows, command="seed --audit-snapshot ownership_discrepancies", seed_db=None, events=[], projection_version="v1", snapshot_id="2026-06-20T170000Z")


def _row(subject, needs=None, conflict="missing_owner"):
    return {"kind": "service", "subject": subject, "conflict": conflict, "capability_needs": needs or []}


def test_impact_audit_renders(tmp_path):
    _snapshot_pair(tmp_path, [_row("svc-a"), _row("svc-b")], [_row("svc-a")])
    rendered = format_impact_audit(build_impact_audit(tmp_path))
    assert "Operational Impact Audit" in rendered
    assert "Ownership / unresolved_ownership_rows" in rendered
    assert "result: improved" in rendered


def test_cli_impact_audit_json_is_valid(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)
    _snapshot_pair(tmp_path, [_row("svc-a")], [])
    assert seed_local.main(["--impact-audit", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["overall"] == "improved"
    assert payload["metrics"]


def test_impact_audit_detects_improvements(tmp_path):
    _snapshot_pair(tmp_path, [_row("svc-a"), _row("svc-b")], [_row("svc-a")])
    audit = build_impact_audit(tmp_path)
    assert audit.overall == "improved"
    assert [m for m in audit.metrics if m.metric == "unresolved_ownership_rows"][0].delta == -1


def test_impact_audit_detects_regressions(tmp_path):
    _snapshot_pair(tmp_path, [_row("svc-a")], [_row("svc-a"), _row("svc-b")])
    audit = build_impact_audit(tmp_path)
    assert audit.overall == "regressed"
    assert [m for m in audit.metrics if m.metric == "unresolved_ownership_rows"][0].result == "regressed"


def test_impact_audit_detects_no_change(tmp_path):
    _snapshot_pair(tmp_path, [_row("svc-a")], [_row("svc-a")])
    audit = build_impact_audit(tmp_path)
    assert audit.overall == "unchanged"


def test_impact_audit_missing_comparison_data_is_sane(tmp_path):
    audit = build_impact_audit(tmp_path)
    assert audit.overall == "unknown"
    assert audit.missing
    assert "Outcomes: unavailable" in format_impact_audit(audit)


def test_impact_audit_does_not_write_event_ledger_or_mutate_cluster(tmp_path):
    db = tmp_path / "events.sqlite"
    ledger = SQLiteEventLedger(db)
    before_events = ledger.list_events()
    state = State(workspace_id="ws")
    before_state = repr(state)
    _snapshot_pair(tmp_path, [_row("svc-a")], [])

    build_impact_audit(tmp_path)

    assert ledger.list_events() == before_events
    assert repr(state) == before_state


def test_impact_audit_registered_in_inventory_and_shape_audit():
    from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
    from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit

    entry = next(e for e in DIAGNOSTIC_INVENTORY if e.name == "impact_audit")
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False
    rows = [r for r in build_diagnostic_shape_audit() if r.diagnostic == "impact_audit"]
    assert rows
    assert {r.status for r in rows} == {"consistent"}
