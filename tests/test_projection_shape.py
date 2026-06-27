import json

from scripts import seed_local
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.projection_shape import (
    build_projection_shape,
    format_projection_shape,
    format_projection_stage_definition,
    projection_shape_json,
    projection_stage_definition_json,
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
    assert stages["fact_conflict_handling"].authority_boundary == "explanatory-only"
    assert stages["measurement_evidence_scan"].authority_boundary == "projection-boundary"
    output = format_projection_shape()
    assert "Does Not Influence: unknown" not in output
    assert "unknown" not in output


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


def test_projection_stage_definition_json_includes_identity(capsys):
    assert (
        seed_local.main(
            ["--projection-stage-definition", "alias_projection", "--json"]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    definition = payload["projection_stage_definition"]

    assert definition == {
        "status": "known",
        "stage": "alias_projection",
        "stage_identifier": "alias_projection",
        "registered_stage": True,
        "evidence_source": "projection_shape_stage_registry",
        "implementation_reason": "identity recovered from the declared projection shape stage registration",
        "projection_stage_boundary": {
            "authority_boundary": "identity-resolution",
            "does_not_influence": ["event_ledger"],
        },
    }
    assert "consumes" not in definition
    assert "produces" not in definition
    assert "influences" not in definition
    assert definition["projection_stage_boundary"] == {
        "authority_boundary": "identity-resolution",
        "does_not_influence": ["event_ledger"],
    }


def test_projection_stage_definition_human_renders_same_identity(capsys):
    assert seed_local.main(["--projection-stage-definition", "alias_projection"]) == 0

    output = capsys.readouterr().out

    assert "ProjectionStage definition: alias_projection" in output
    assert "  status: known" in output
    assert "  stage_identifier: alias_projection" in output
    assert "  registered_stage: true" in output
    assert "  projection_stage_boundary:" in output
    assert "    authority_boundary: identity-resolution" in output
    assert "    does_not_influence: event_ledger" in output
    assert (
        "  implementation_reason: identity recovered from the declared projection shape stage registration"
        in output
    )
    assert "  evidence_source: projection_shape_stage_registry" in output
    assert "Consumes:" not in output
    assert "Produces:" not in output
    assert "Influences:" not in output
    assert "Authority Boundary:" not in output


def test_projection_stage_definition_unknown_is_bounded(capsys):
    assert (
        seed_local.main(["--projection-stage-definition", "missing_stage", "--json"])
        == 0
    )

    payload = json.loads(capsys.readouterr().out)

    assert payload["projection_stage_definition"] == {
        "status": "unknown",
        "stage": "missing_stage",
        "stage_identifier": "missing_stage",
        "registered_stage": False,
        "evidence_source": "projection_shape_stage_registry",
        "implementation_reason": "unknown projection stage; no projection shape stage declaration exists",
    }
    assert "projection_stage_boundary" not in payload["projection_stage_definition"]


def test_projection_stage_definition_does_not_change_projection_shape_json(capsys):
    expected = projection_shape_json()

    assert seed_local.main(["--projection-stage-definition", "alias_projection", "--json"]) == 0
    capsys.readouterr()
    assert seed_local.main(["--projection-shape", "--json"]) == 0

    assert json.loads(capsys.readouterr().out) == expected


def test_projection_stage_definition_does_not_change_projection_shape_human():
    output = format_projection_shape()

    assert "Projection Shape" in output
    assert "Stage: alias_projection" in output
    assert "ProjectionStage definition" not in output
    assert "stage_identifier" not in output


def test_projection_stage_definition_visibility_registration():
    entry = next(e for e in DIAGNOSTIC_INVENTORY if e.name == "projection_stage_definition")
    assert entry.cli_flags == ("--projection-stage-definition",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False


def test_projection_stage_definition_shape_registration_consistency():
    rows = [
        r
        for r in build_diagnostic_shape_audit()
        if r.diagnostic == "projection_stage_definition"
    ]
    assert rows
    assert {row.status for row in rows} == {"consistent"}


def test_projection_stage_definition_guardrails_exclude_execution_planning_and_inference(capsys):
    assert (
        seed_local.main(
            ["--projection-stage-definition", "alias_projection", "--json"]
        )
        == 0
    )

    rendered = json.dumps(json.loads(capsys.readouterr().out)).lower()

    for forbidden in [
        "runtime execution",
        "projection execution",
        "planner behavior",
        "semantic interpretation",
        "implementation inference",
        "future execution",
        "new projection concepts",
        "consumes",
        "produces",
        "influences",
    ]:
        assert forbidden not in rendered

    direct = projection_stage_definition_json("alias_projection")
    human = format_projection_stage_definition("alias_projection")
    assert direct["projection_stage_definition"]["stage"] in human


def test_projection_stage_explanation_json_composes_only_existing_fields(capsys):
    assert (
        seed_local.main(
            ["--projection-stage-explanation", "alias_projection", "--json"]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    explanation = payload["projection_stage_explanation"]
    definition = projection_stage_definition_json("alias_projection")[
        "projection_stage_definition"
    ]

    assert set(explanation) == {
        "projection_stage_definition",
        "projection_stage_boundary",
    }
    assert explanation["projection_stage_definition"] == definition
    assert explanation["projection_stage_boundary"] == definition[
        "projection_stage_boundary"
    ]
    assert "consumes" not in json.dumps(payload)
    assert "produces" not in json.dumps(payload)
    assert "influences" not in json.dumps(payload)


def test_projection_stage_explanation_human_composes_without_new_evidence(capsys):
    assert seed_local.main(["--projection-stage-explanation", "alias_projection"]) == 0

    output = capsys.readouterr().out

    assert "ProjectionStage explanation: alias_projection" in output
    assert "  projection_stage_definition:" in output
    assert "    status: known" in output
    assert "    stage_identifier: alias_projection" in output
    assert "  projection_stage_boundary:" in output
    assert "    authority_boundary: identity-resolution" in output
    assert "    does_not_influence: event_ledger" in output
    assert "projection_shape_stage_registry" in output
    assert "Consumes:" not in output
    assert "Produces:" not in output
    assert "Influences:" not in output
    assert "Authority Boundary:" not in output


def test_projection_stage_explanation_unknown_is_bounded(capsys):
    assert (
        seed_local.main(["--projection-stage-explanation", "missing_stage", "--json"])
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    explanation = payload["projection_stage_explanation"]

    assert set(explanation) == {"projection_stage_definition"}
    assert explanation["projection_stage_definition"] == {
        "status": "unknown",
        "stage": "missing_stage",
        "stage_identifier": "missing_stage",
        "registered_stage": False,
        "evidence_source": "projection_shape_stage_registry",
        "implementation_reason": "unknown projection stage; no projection shape stage declaration exists",
    }
    assert "projection_stage_boundary" not in explanation


def test_projection_stage_explanation_preserves_existing_definition_and_shape_behavior(capsys):
    expected_definition = projection_stage_definition_json("alias_projection")
    expected_shape = projection_shape_json()
    expected_human_shape = format_projection_shape()

    assert seed_local.main(["--projection-stage-explanation", "alias_projection"]) == 0
    capsys.readouterr()

    assert projection_stage_definition_json("alias_projection") == expected_definition
    assert projection_shape_json() == expected_shape
    assert format_projection_shape() == expected_human_shape


def test_projection_stage_explanation_visibility_registration():
    entry = next(e for e in DIAGNOSTIC_INVENTORY if e.name == "projection_stage_explanation")
    assert entry.cli_flags == ("--projection-stage-explanation",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False


def test_projection_stage_explanation_shape_registration_consistency():
    rows = [
        r
        for r in build_diagnostic_shape_audit()
        if r.diagnostic == "projection_stage_explanation"
    ]
    assert rows
    assert {row.status for row in rows} == {"consistent"}


def test_projection_stage_explanation_guardrails_exclude_presentation_framework_and_reasoning(capsys):
    assert (
        seed_local.main(
            ["--projection-stage-explanation", "alias_projection", "--json"]
        )
        == 0
    )

    rendered = json.dumps(json.loads(capsys.readouterr().out)).lower()

    for forbidden in [
        "infer",
        "reasoning",
        "normalize",
        "reinterpret",
        "recommend",
        "semantic meaning",
        "implementation not already present",
        "presentation framework",
        "explainablesubject",
        "ontology",
        "generic composition",
        "consumes",
        "produces",
        "influences",
    ]:
        assert forbidden not in rendered
