import json

import pytest

import scripts.seed_local as seed_local
from seed_runtime import constitutional_view_composition as composition_module
from seed_runtime.constitutional_view_composition import (
    build_constitutional_view_composition,
    constitutional_view_composition_json,
    constitutional_view_composition_request,
    format_constitutional_view_composition,
)
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit


def test_constitutional_view_composition_request_shape_is_bounded():
    request = constitutional_view_composition_request(
        requested_views=("constitutional_process", "constitutional_governance"),
        composition_purpose="compatibility",
        output_format="json",
    )

    assert request.requested_views == ("constitutional_process", "constitutional_governance")
    assert request.composition_purpose == "compatibility"
    assert request.output_format == "json"


def test_constitutional_view_composition_preserves_unknowns_refusals_and_boundaries():
    artifact = build_constitutional_view_composition(
        constitutional_view_composition_request(
            requested_views=(
                "constitutional_process",
                "constitutional_governance",
                "constitutional_fidelity",
            )
        )
    )

    assert artifact.compatibility_answer == "No."
    assert [view.name for view in artifact.contributing_views] == [
        "constitutional_process",
        "constitutional_governance",
        "constitutional_fidelity",
    ]
    assert "constitutional_process_reconciliation.md" in artifact.correlated_existing_evidence
    assert "constitutional_governance_investigation.md" in artifact.correlated_existing_evidence
    assert "constitutional_fidelity_characterization.md" in artifact.correlated_existing_evidence
    assert any(item.startswith("constitutional_process:") for item in artifact.preserved_unknowns)
    assert any(item.startswith("constitutional_governance:") for item in artifact.preserved_unknowns)
    assert any(item.startswith("constitutional_fidelity:") for item in artifact.preserved_unknowns)
    assert "constitutional_governance: runtime governance" in artifact.preserved_refusals
    assert "constitutional_fidelity: runtime evaluation" in artifact.preserved_refusals
    assert "no runtime reasoning" in artifact.read_only_boundaries
    assert "no evidence discovery" in artifact.read_only_boundaries
    assert artifact.read_only is True
    assert artifact.writes_event_ledger is False
    assert artifact.mutates_cluster is False


def test_constitutional_view_composition_empty_requested_views_preserves_unknown_standing():
    artifact = build_constitutional_view_composition(
        constitutional_view_composition_request(requested_views=())
    )

    payload = constitutional_view_composition_json(artifact)
    rendered = format_constitutional_view_composition(artifact)

    assert artifact.request.requested_views == ()
    assert artifact.contributing_views == ()
    assert artifact.compatibility_answer == "Unknown."
    assert payload["compatibility_answer"] == "Unknown."
    assert payload["contributing_views"] == ()
    assert "Compatibility answer: Unknown." in rendered
    assert "Requested views: " in rendered
    assert artifact.read_only is True
    assert artifact.writes_event_ledger is False
    assert artifact.mutates_cluster is False


def test_constitutional_view_composition_unknown_contribution_preserves_non_no(monkeypatch):
    def build_view():
        return object()

    def render_view(_view):
        return {
            "name": "Constitutional Process View",
            "composition": ("constitutional_process_reconciliation.md",),
            "unknowns": ("compatibility testimony unavailable",),
            "explicit_refusals": (),
        }

    monkeypatch.setitem(
        composition_module._BUILDERS,
        "constitutional_process",
        (build_view, render_view),
    )

    artifact = build_constitutional_view_composition(
        constitutional_view_composition_request(requested_views=("constitutional_process",))
    )

    assert [view.name for view in artifact.contributing_views] == ["constitutional_process"]
    assert artifact.contributing_views[0].evidence == ("constitutional_process_reconciliation.md",)
    assert artifact.preserved_unknowns == (
        "constitutional_process: compatibility testimony unavailable",
    )
    assert artifact.preserved_refusals == ()
    assert artifact.compatibility_answer == "Unknown."
    assert artifact.read_only is True
    assert artifact.writes_event_ledger is False
    assert artifact.mutates_cluster is False

def test_constitutional_view_composition_refuses_unregistered_views():
    with pytest.raises(ValueError, match="registered constitutional views"):
        build_constitutional_view_composition(
            constitutional_view_composition_request(requested_views=("the_eye",))
        )


def test_constitutional_view_composition_json_and_human_rendering():
    artifact = build_constitutional_view_composition(
        constitutional_view_composition_request(
            requested_views=("constitutional_governance", "constitutional_fidelity")
        )
    )

    payload = constitutional_view_composition_json(artifact)
    rendered = format_constitutional_view_composition(artifact)

    assert payload["name"] == "Constitutional View Composition"
    assert payload["compatibility_answer"] == "No."
    assert payload["mutates_cluster"] is False
    assert payload["request"]["requested_views"] == (
        "constitutional_governance",
        "constitutional_fidelity",
    )
    assert "Constitutional View Composition" in rendered
    assert "Preserved Unknowns" in rendered
    assert "Preserved refusals" in rendered
    assert "no constitutional authority" in rendered


def test_cli_constitutional_view_composition_supports_human_and_json(capsys):
    assert seed_local.main([
        "--constitutional-view-composition",
        "constitutional_governance",
        "constitutional_fidelity",
    ]) == 0
    human = capsys.readouterr().out
    assert "Constitutional View Composition" in human
    assert "constitutional_governance" in human

    assert seed_local.main([
        "--constitutional-view-composition",
        "constitutional_governance",
        "constitutional_fidelity",
        "--json",
    ]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["compatibility_answer"] == "No."
    assert payload["writes_event_ledger"] is False


def test_constitutional_view_composition_appears_in_diagnostic_inventory_and_shape_audit():
    entry = next(
        entry for entry in DIAGNOSTIC_INVENTORY if entry.name == "constitutional_view_composition"
    )
    rows = [
        row
        for row in build_diagnostic_shape_audit()
        if row.diagnostic == "constitutional_view_composition"
    ]

    assert entry.cli_flags == ("--constitutional-view-composition",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False
    assert rows
    assert all(row.status == "consistent" for row in rows)
