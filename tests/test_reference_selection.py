import json

import scripts.seed_local as seed_local
from seed_runtime.audit_snapshots import create_audit_snapshot
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.reference_selection import (
    build_reference_selection,
    format_reference_selection,
    reference_selection_json,
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


def _row(subject):
    return {"kind": "service", "subject": subject, "conflict": "missing_owner"}


def test_reference_selection_history_renders_json_selected_rationale_and_authority(
    tmp_path, monkeypatch, capsys
):
    _ownership_snapshot(tmp_path, "2026-06-20T160000Z", [_row("svc-a")])
    _ownership_snapshot(tmp_path, "2026-06-20T170000Z", [_row("svc-b")])
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    selection = build_reference_selection(tmp_path, "history")
    rendered = format_reference_selection(selection)

    assert "Reference Selection" in rendered
    assert "history" in rendered
    assert "previous comparable snapshot" in rendered
    assert "impact_audit compares the latest comparable snapshot pair" in rendered
    assert "implementation-selected reference" in rendered

    assert seed_local.main(["--reference-selection", "history", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["domain"] == "history"
    assert payload["question"] == "historical comparison"
    assert payload["selected_reference"]["reference"] == "previous comparable snapshot"
    assert payload["selected_reference"]["comparable_snapshot_pairs"]
    assert payload["selection_rationale"]
    assert (
        payload["authority_boundary"]["selected_authority"]
        == "implementation-selected reference"
    )
    assert payload["authority_boundary"]["accepted_reference"] is False
    assert payload["authority_boundary"]["expectation_bearing_reference"] is False
    assert payload["writes_event_ledger"] is False
    assert payload["mutates_cluster"] is False


def test_reference_selection_history_unknown_alternatives_remain_explicit(tmp_path):
    selection = build_reference_selection(tmp_path, "history")
    payload = reference_selection_json(selection)
    rendered = format_reference_selection(selection)

    assert payload["selected_reference"]["reference"] == "unknown"
    assert payload["alternative_references"] == [
        {
            "reference": "unknown",
            "reason": "implementation does not currently expose candidate alternatives",
        }
    ]
    assert "Alternative References:" in rendered
    assert "implementation does not currently expose candidate alternatives" in rendered


def test_reference_selection_choice_lineage_handoff_preserves_public_shape(tmp_path):
    _ownership_snapshot(tmp_path, "2026-06-20T160000Z", [_row("svc-a")])
    _ownership_snapshot(tmp_path, "2026-06-20T170000Z", [_row("svc-b")])

    payload = reference_selection_json(build_reference_selection(tmp_path, "history"))

    assert set(payload) == {
        "domain",
        "question",
        "selected_reference",
        "selection_rationale",
        "alternative_references",
        "authority_boundary",
        "limitations",
        "writes_event_ledger",
        "mutates_cluster",
    }
    assert payload["selected_reference"]["reference"] == "previous comparable snapshot"
    assert "selection_rationale" not in payload["selected_reference"]
    assert "alternative_references" not in payload["selected_reference"]
    assert payload["selection_rationale"]
    assert payload["alternative_references"]
    assert payload["limitations"]

def test_reference_selection_does_not_create_baselines_expectations_events_or_cluster_mutation(
    tmp_path,
):
    db = tmp_path / "events.sqlite"
    ledger = SQLiteEventLedger(db)
    before_events = ledger.list_events()
    state = State(workspace_id="ws")
    before_state = repr(state)
    before_paths = set(p.relative_to(tmp_path) for p in tmp_path.rglob("*"))

    selection = build_reference_selection(tmp_path, "history")

    after_paths = set(p.relative_to(tmp_path) for p in tmp_path.rglob("*"))
    created_paths = {str(p) for p in after_paths - before_paths}
    assert not any("baseline" in path for path in created_paths)
    assert not any("expectation" in path for path in created_paths)
    assert selection.authority_boundary["accepted_reference"] is False
    assert selection.authority_boundary["expectation_bearing_reference"] is False
    assert selection.writes_event_ledger is False
    assert selection.mutates_cluster is False
    assert ledger.list_events() == before_events
    assert repr(state) == before_state


def test_reference_selection_registered_in_visibility_contracts():
    from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
    from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
    from seed_runtime.operational_surface_inventory import (
        build_operational_surface_inventory,
    )

    entry = next(e for e in DIAGNOSTIC_INVENTORY if e.name == "reference_selection")
    assert entry.cli_flags == ("--reference-selection",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False

    rows = [
        r
        for r in build_diagnostic_shape_audit()
        if r.diagnostic == "reference_selection"
    ]
    assert rows
    assert {r.status for r in rows} == {"consistent"}

    surfaces = build_operational_surface_inventory(seed_local.build_parser())
    assert any(surface.name == "--reference-selection" for surface in surfaces)
