import json

import scripts.seed_local as seed_local
from seed_runtime.constitutional_governance_view import (
    build_constitutional_governance_view,
    constitutional_governance_view_json,
    format_constitutional_governance_view,
)
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY


def test_constitutional_governance_view_composes_existing_governance_evidence_only():
    view = build_constitutional_governance_view()

    assert view.compatibility_answer == "No."
    assert [relationship.name for relationship in view.relationships] == [
        "Question Grammar governs later Process movement",
        "Relationship Grammar governs connective use",
        "External Grammar governs representation intake",
        "Constitutional Process governs bounded movement",
        "Constitutional Fidelity governs lawful realization",
    ]
    assert all(relationship.status == "known" for relationship in view.relationships)
    assert "Fidelity View" in view.remaining_candidate_views
    assert "Observability Coverage View" in view.remaining_candidate_views
    assert "Provenance Coverage View" in view.remaining_candidate_views
    assert view.read_only is True
    assert view.writes_event_ledger is False
    assert view.mutates_cluster is False


def test_constitutional_governance_view_preserves_unknowns_and_refusals_without_inference():
    view = build_constitutional_governance_view()

    assert any("distinct constitutional governance owner" in item for item in view.unknowns)
    assert any("implementation topology" in item for item in view.unknowns)
    assert "runtime governance" in view.explicit_refusals
    assert "repository mutation" in view.explicit_refusals
    assert "ownership" not in " ".join(
        relationship.name.lower() for relationship in view.relationships
    )


def test_constitutional_governance_view_json_and_human_rendering():
    view = build_constitutional_governance_view()

    payload = constitutional_governance_view_json(view)
    rendered = format_constitutional_governance_view(view)

    assert payload["name"] == "Constitutional Governance View"
    assert payload["compatibility_answer"] == "No."
    assert payload["mutates_cluster"] is False
    assert "Constitutional Governance View" in rendered
    assert "Question Grammar governs later Process movement: known" in rendered
    assert "Explicit refusals" in rendered
    assert "Remaining candidate views" in rendered


def test_cli_constitutional_governance_supports_human_and_json(capsys):
    assert seed_local.main(["--constitutional-governance"]) == 0
    human = capsys.readouterr().out
    assert "Constitutional Governance View" in human

    assert seed_local.main(["--constitutional-governance", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["compatibility_answer"] == "No."
    assert payload["writes_event_ledger"] is False


def test_constitutional_governance_view_appears_in_diagnostic_inventory_and_shape_audit():
    entry = next(
        entry for entry in DIAGNOSTIC_INVENTORY if entry.name == "constitutional_governance"
    )
    rows = [
        row
        for row in build_diagnostic_shape_audit()
        if row.diagnostic == "constitutional_governance"
    ]

    assert entry.cli_flags == ("--constitutional-governance",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False
    assert rows
    assert all(row.status == "consistent" for row in rows)
