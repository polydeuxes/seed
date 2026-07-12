import json

import scripts.seed_local as seed_local
from seed_runtime.constitutional_process_view import (
    build_constitutional_process_view,
    constitutional_process_view_json,
    format_constitutional_process_view,
)
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY


def test_constitutional_process_view_composes_existing_process_evidence_only():
    view = build_constitutional_process_view()

    assert view.compatibility_answer == "No."
    assert [stage.name for stage in view.stages] == [
        "Pressure",
        "Lawful Question",
        "Orientation",
        "Recovery",
        "Cross-Examination",
        "Completion Audit",
        "Lawful Stop",
    ]
    assert all(stage.status == "known" for stage in view.stages)
    assert "Governance View" in view.remaining_candidate_views
    assert view.read_only is True
    assert view.writes_event_ledger is False
    assert view.mutates_cluster is False


def test_constitutional_process_view_preserves_unknowns_without_inference():
    view = build_constitutional_process_view()

    assert any("single named constitutional process owner" in item for item in view.unknowns)
    assert any("Orientation-to-Recovery handoff" in item for item in view.unknowns)
    assert "runtime" not in " ".join(stage.summary.lower() for stage in view.stages)


def test_constitutional_process_view_json_and_human_rendering():
    view = build_constitutional_process_view()

    payload = constitutional_process_view_json(view)
    rendered = format_constitutional_process_view(view)

    assert payload["name"] == "Constitutional Process View"
    assert payload["compatibility_answer"] == "No."
    assert payload["mutates_cluster"] is False
    assert "Constitutional Process View" in rendered
    assert "Pressure: known" in rendered
    assert "Remaining candidate views" in rendered


def test_cli_constitutional_process_supports_human_and_json(capsys):
    assert seed_local.main(["--constitutional-process"]) == 0
    human = capsys.readouterr().out
    assert "Constitutional Process View" in human

    assert seed_local.main(["--constitutional-process", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["compatibility_answer"] == "No."
    assert payload["writes_event_ledger"] is False


def test_constitutional_process_view_appears_in_diagnostic_inventory_and_shape_audit():
    entry = next(entry for entry in DIAGNOSTIC_INVENTORY if entry.name == "constitutional_process")
    rows = [row for row in build_diagnostic_shape_audit() if row.diagnostic == "constitutional_process"]

    assert entry.cli_flags == ("--constitutional-process",)
    assert entry.supports_json is True
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False
    assert rows
    assert all(row.status == "consistent" for row in rows)
