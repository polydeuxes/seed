import json

import scripts.seed_local as seed_local
from seed_runtime.constitutional_fidelity_view import (
    build_constitutional_fidelity_view,
    constitutional_fidelity_view_json,
    format_constitutional_fidelity_view,
)
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit


def test_constitutional_fidelity_view_composes_completed_fidelity_evidence_only():
    view = build_constitutional_fidelity_view()

    assert view.compatibility_answer == "No."
    assert view.composition == ("constitutional_fidelity_characterization.md",)
    assert [classification.name for classification in view.classifications] == [
        "constitutional authority",
        "lawful implementation realization",
        "implementation freedom",
        "compatibility-only structures",
        "orchestration-only structures",
        "constitutional boundary preservation",
        "explicit refusals",
        "preserved Unknowns",
    ]
    assert all(classification.status == "known" for classification in view.classifications)
    assert view.remaining_candidate_views == (
        "Observability Coverage View",
        "Provenance Coverage View",
    )
    assert view.read_only is True
    assert view.writes_event_ledger is False
    assert view.mutates_cluster is False


def test_constitutional_fidelity_view_preserves_unknowns_and_required_refusals():
    view = build_constitutional_fidelity_view()

    assert any("Projection Grammar" in item for item in view.unknowns)
    assert any("implementation-backed public surface" in item for item in view.unknowns)
    assert view.explicit_refusals == (
        "constitutional recovery",
        "implementation recovery",
        "ownership recovery",
        "implementation mutation",
        "repository mutation",
        "runtime evaluation",
        "fidelity enforcement",
        "architectural redesign",
        "projection recovery",
    )
    assert "no event-ledger writes" in view.read_only_boundaries
    assert "no cluster mutation" in view.read_only_boundaries


def test_constitutional_fidelity_view_json_and_human_rendering():
    view = build_constitutional_fidelity_view()

    payload = constitutional_fidelity_view_json(view)
    rendered = format_constitutional_fidelity_view(view)

    assert payload["name"] == "Constitutional Fidelity View"
    assert payload["compatibility_answer"] == "No."
    assert payload["mutates_cluster"] is False
    assert "Constitutional Fidelity View" in rendered
    assert "constitutional authority: known" in rendered
    assert "Recurring constitutional discipline" in rendered
    assert "Explicit refusals" in rendered
    assert "Read-only boundaries" in rendered


def test_cli_constitutional_fidelity_supports_human_and_json(capsys):
    assert seed_local.main(["--constitutional-fidelity"]) == 0
    human = capsys.readouterr().out
    assert "Constitutional Fidelity View" in human

    assert seed_local.main(["--constitutional-fidelity", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["compatibility_answer"] == "No."
    assert payload["writes_event_ledger"] is False


def test_constitutional_fidelity_view_appears_in_diagnostic_inventory_and_shape_audit():
    entry = next(entry for entry in DIAGNOSTIC_INVENTORY if entry.name == "constitutional_fidelity")
    rows = [
        row
        for row in build_diagnostic_shape_audit()
        if row.diagnostic == "constitutional_fidelity"
    ]

    assert entry.cli_flags == ("--constitutional-fidelity",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False
    assert rows
    assert all(row.status == "consistent" for row in rows)
