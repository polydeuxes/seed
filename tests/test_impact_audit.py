import json

import scripts.seed_local as seed_local
from seed_runtime.audit_snapshots import create_audit_snapshot
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.impact_audit import (
    build_impact_audit,
    format_impact_audit,
    impact_audit_json,
)
from seed_runtime.state import State


def _snapshot_pair(tmp_path, before_rows, after_rows):
    create_audit_snapshot(
        repo_root=tmp_path,
        kind="ownership_discrepancies",
        payload=before_rows,
        command="seed --audit-snapshot ownership_discrepancies",
        seed_db=None,
        events=[],
        projection_version="v1",
        snapshot_id="2026-06-20T160000Z",
    )
    create_audit_snapshot(
        repo_root=tmp_path,
        kind="ownership_discrepancies",
        payload=after_rows,
        command="seed --audit-snapshot ownership_discrepancies",
        seed_db=None,
        events=[],
        projection_version="v1",
        snapshot_id="2026-06-20T170000Z",
    )


def _observation_pair(tmp_path, before_predicates, after_predicates):
    create_audit_snapshot(
        repo_root=tmp_path,
        kind="observation_inventory",
        payload={
            "predicates": [{"predicate": p} for p in before_predicates],
            "providers": [],
            "families": [],
            "summary": {"predicate_count": len(before_predicates)},
        },
        command="seed --audit-snapshot observation_inventory",
        seed_db=None,
        events=[],
        projection_version="v1",
        snapshot_id="2026-06-20T180000Z",
    )
    create_audit_snapshot(
        repo_root=tmp_path,
        kind="observation_inventory",
        payload={
            "predicates": [{"predicate": p} for p in after_predicates],
            "providers": [],
            "families": [],
            "summary": {"predicate_count": len(after_predicates)},
        },
        command="seed --audit-snapshot observation_inventory",
        seed_db=None,
        events=[],
        projection_version="v1",
        snapshot_id="2026-06-20T190000Z",
    )


def _row(subject, needs=None, conflict="missing_owner"):
    return {
        "kind": "service",
        "subject": subject,
        "conflict": conflict,
        "capability_needs": needs or [],
    }


def _metric(audit, name):
    return next(m for m in audit.metrics if m.metric == name)


def test_impact_audit_renders(tmp_path):
    _snapshot_pair(tmp_path, [_row("svc-a"), _row("svc-b")], [_row("svc-a")])
    rendered = format_impact_audit(build_impact_audit(tmp_path))
    assert "Operational Impact Audit" in rendered
    assert "Ownership / unresolved_ownership_rows" in rendered
    assert "Snapshot Coverage:" in rendered
    assert "result: improved" in rendered


def test_cli_impact_audit_json_is_valid(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)
    _snapshot_pair(tmp_path, [_row("svc-a")], [])
    assert seed_local.main(["--impact-audit", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["overall"] == "improved"
    assert payload["metrics"]
    assert payload["snapshot_coverage"]
    assert any(m["availability"] == "not_snapshotted" for m in payload["metrics"])


def test_impact_audit_detects_improvements(tmp_path):
    _snapshot_pair(tmp_path, [_row("svc-a"), _row("svc-b")], [_row("svc-a")])
    audit = build_impact_audit(tmp_path)
    assert audit.overall == "improved"
    assert _metric(audit, "unresolved_ownership_rows").delta == -1


def test_impact_audit_detects_regressions(tmp_path):
    _snapshot_pair(tmp_path, [_row("svc-a")], [_row("svc-a"), _row("svc-b")])
    audit = build_impact_audit(tmp_path)
    assert audit.overall == "regressed"
    assert _metric(audit, "unresolved_ownership_rows").result == "regressed"


def test_impact_audit_detects_no_change(tmp_path):
    _snapshot_pair(tmp_path, [_row("svc-a")], [_row("svc-a")])
    audit = build_impact_audit(tmp_path)
    assert audit.overall == "unchanged"
    assert _metric(audit, "capability_pressure").availability == "not_snapshotted"


def test_missing_comparison_data_is_not_reported_as_zero(tmp_path):
    audit = build_impact_audit(tmp_path)
    rendered = format_impact_audit(audit)
    assert audit.overall == "unknown"
    assert audit.missing
    assert _metric(audit, "unresolved_ownership_rows").before is None
    assert (
        _metric(audit, "unresolved_ownership_rows").availability == "no_comparison_data"
    )
    assert "before: no_comparison_data" in rendered
    assert "before: 0" not in rendered


def test_unavailable_metrics_are_reported_explicitly(tmp_path):
    _snapshot_pair(tmp_path, [_row("svc-a")], [_row("svc-a")])
    audit = build_impact_audit(tmp_path)
    capability = _metric(audit, "capability_pressure")
    assert capability.before is None
    assert capability.after is None
    assert capability.availability == "not_snapshotted"
    rendered = format_impact_audit(audit)
    assert "Capabilities / capability_pressure" in rendered
    assert "availability: not_snapshotted" in rendered


def test_real_zero_values_remain_distinguishable_from_unavailable_values(tmp_path):
    _snapshot_pair(tmp_path, [], [])
    audit = build_impact_audit(tmp_path)
    unresolved = _metric(audit, "unresolved_ownership_rows")
    capability = _metric(audit, "capability_pressure")
    assert unresolved.before == 0
    assert unresolved.after == 0
    assert unresolved.availability == "comparable"
    assert capability.before is None
    assert capability.availability == "not_snapshotted"
    rendered = format_impact_audit(audit)
    assert "before: 0" in rendered
    assert "before: not_snapshotted" in rendered


def test_impact_audit_remains_valid_when_only_some_snapshot_kinds_exist(tmp_path):
    _snapshot_pair(tmp_path, [_row("svc-a")], [])
    audit = build_impact_audit(tmp_path)
    assert audit.overall == "improved"
    assert _metric(audit, "observable_predicates").availability == "no_comparison_data"
    assert any(
        row.surface == "observation_inventory" and row.status == "no_comparison_data"
        for row in audit.coverage
    )


def test_ownership_comparisons_continue_to_work_with_unchanged_common_rows(tmp_path):
    _snapshot_pair(
        tmp_path, [_row("svc-a"), _row("svc-b")], [_row("svc-a"), _row("svc-b")]
    )
    audit = build_impact_audit(tmp_path)
    unresolved = _metric(audit, "unresolved_ownership_rows")
    assert unresolved.before == 2
    assert unresolved.after == 2
    assert unresolved.delta == 0


def test_observation_inventory_comparisons_continue_to_work(tmp_path):
    _observation_pair(tmp_path, ["a", "b"], ["a", "b", "c"])
    audit = build_impact_audit(tmp_path)
    observable = _metric(audit, "observable_predicates")
    assert observable.before == 2
    assert observable.after == 3
    assert observable.delta == 1
    assert observable.result == "improved"


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
