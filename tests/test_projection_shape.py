import json

from scripts import seed_local
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.projection_shape import (
    build_projection_shape,
    format_projection_shape,
    projection_shape_json,
)


def _stages():
    return {stage.stage: stage for stage in build_projection_shape()["stages"]}


def test_projection_shape_human_readable_rendering(capsys):
    assert seed_local.main(["--projection-shape"]) == 0
    output = capsys.readouterr().out
    assert "Projection Shape" in output
    assert "Stage: fact_support_projection" in output
    assert "Consumes: facts" in output
    assert "Authority Boundary: selection-bearing" in output


def test_projection_shape_json_is_valid(capsys):
    assert seed_local.main(["--projection-shape", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["boundary"] == {
        "read_only": True,
        "writes_event_ledger": False,
        "mutates_cluster": False,
    }
    assert any(stage["stage"] == "event_replay" for stage in payload["stages"])


def test_projection_shape_stage_list_visibility():
    stages = _stages()
    for name in {
        "event_replay",
        "alias_projection",
        "measurement_retention",
        "inference",
        "fact_support_projection",
        "legacy_relationship_projection",
        "catalog_relationship_projection",
        "entity_type_assertion_projection",
        "graph_issue_construction",
        "fact_conflict_handling",
    }:
        assert name in stages


def test_projection_shape_consumes_and_produces_visibility():
    stages = _stages()
    assert "facts" in stages["fact_support_projection"].consumes
    assert "fact_supports" in stages["fact_support_projection"].produces
    assert "relationship_catalog" in stages["catalog_relationship_projection"].consumes
    assert "relationships" in stages["catalog_relationship_projection"].produces


def test_projection_shape_influence_and_non_influence_visibility():
    stages = _stages()
    assert "current_fact_selection" in stages["fact_support_projection"].influences
    assert (
        "relationship_projection"
        in stages["fact_support_projection"].does_not_influence
    )
    assert (
        "graph_issue_construction"
        in stages["catalog_relationship_projection"].influences
    )


def test_projection_shape_authority_boundary_and_unknown_handling():
    stages = _stages()
    assert stages["alias_projection"].authority_boundary == "identity-resolution"
    assert stages["graph_issue_construction"].authority_boundary == "validation-only"
    assert stages["measurement_evidence_scan"].authority_boundary == "unknown"
    assert "unknown" in format_projection_shape()


def test_projection_shape_read_only_no_event_ledger_writes_no_cluster_mutation():
    payload = projection_shape_json()
    assert payload["boundary"]["read_only"] is True
    assert payload["boundary"]["writes_event_ledger"] is False
    assert payload["boundary"]["mutates_cluster"] is False


def test_projection_shape_visibility_registration():
    entry = next(e for e in DIAGNOSTIC_INVENTORY if e.name == "projection_shape")
    assert entry.cli_flags == ("--projection-shape",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False


def test_projection_shape_shape_registration_consistency():
    rows = [
        r for r in build_diagnostic_shape_audit() if r.diagnostic == "projection_shape"
    ]
    assert rows
    assert {row.status for row in rows} == {"consistent"}
