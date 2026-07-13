import json
from dataclasses import asdict

import pytest

import scripts.seed_local as seed_local
from seed_runtime.constitutional_pipeline import ConstitutionalPipelineRequest
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit


def _cli(*extra):
    return [
        "--constitutional-pipeline",
        "--operator-inquiry",
        "Operator says process should be visible; testimony only.",
        "--inquiry-provenance",
        "operator:public-surface-test",
        "--bounded-question",
        "Explain explicitly selected constitutional process view.",
        "--constitutional-intent",
        "caller supplied public pipeline inquiry",
        "--scope-status",
        "caller-bounded; not independently verified",
        *extra,
    ]


def test_constitutional_pipeline_modules_import_successfully():
    import seed_runtime.bounded_constitutional_question as bounded_question
    import seed_runtime.constitutional_pipeline as pipeline
    import seed_runtime.constitutional_pipeline_diagnostic as pipeline_diagnostic
    import seed_runtime.constitutional_view_selection as view_selection

    assert bounded_question.produce_bounded_constitutional_question
    assert pipeline.invoke_constitutional_pipeline
    assert pipeline_diagnostic.build_constitutional_pipeline_diagnostic
    assert view_selection.select_constitutional_views


def test_public_surface_constructs_request_and_invokes_complete_pipeline_once(monkeypatch, capsys):
    import scripts.seed_local as cli

    calls = []
    original = cli.invoke_constitutional_pipeline

    def spy(request):
        calls.append(request)
        return original(request)

    monkeypatch.setattr(cli, "invoke_constitutional_pipeline", spy)

    assert seed_local.main(_cli("--selection-key", "process", "--json")) == 0
    payload = json.loads(capsys.readouterr().out)

    assert len(calls) == 1
    assert isinstance(calls[0], ConstitutionalPipelineRequest)
    assert calls[0].caller_supplied_fields == (("selection_key", "process"),)
    assert payload["selection"]["selected_view_names"] == ["constitutional_process"]
    assert payload["composition"]["contributing_views"][0]["name"] == "constitutional_process"


def test_public_surface_json_preserves_operator_provenance_and_testimony_boundary(capsys):
    assert seed_local.main(
        _cli(
            "--selection-key",
            "process",
            "--pipeline-uncertainty",
            "caller uncertainty preserved",
            "--pipeline-unknown",
            "operator assertion not verified",
            "--json",
        )
    ) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["bounded_question"]["operator_inquiry"] == "Operator says process should be visible; testimony only."
    assert payload["bounded_question"]["inquiry_provenance"] == "operator:public-surface-test"
    assert payload["bounded_question"]["testimony_status"] == "operator testimony preserved as evidence, not established fact"
    assert "caller uncertainty preserved" in payload["bounded_question"]["uncertainty"]
    assert "operator assertion not verified" in payload["bounded_question"]["unknowns"]
    assert "established_fact" not in json.dumps(payload)
    assert payload["composition"]["writes_event_ledger"] is False
    assert payload["composition"]["mutates_cluster"] is False


def test_public_surface_human_output_is_deterministic_and_not_fact_rendering(capsys):
    args = _cli("--selection-key", "process")
    assert seed_local.main(args) == 0
    first = capsys.readouterr().out
    assert seed_local.main(args) == 0
    second = capsys.readouterr().out

    assert first == second
    assert "Constitutional Pipeline" in first
    assert "Operator inquiry supplied:" in first
    assert "Testimony status: operator testimony preserved as evidence, not established fact" in first
    assert "Selected views: constitutional_process" in first
    assert "Writes event ledger: false" in first
    assert "Mutates cluster: false" in first
    assert "Established fact" not in first


def test_public_surface_missing_selection_keys_are_not_guessed(capsys):
    assert seed_local.main(_cli("--json")) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["question_projection"]["selection_keys"] == []
    assert payload["selection"]["selected_view_names"] == []
    assert "no registered constitutional view matched deterministic projection keys" in payload["selection"]["selection_uncertainty"]
    assert payload["composition_request"]["requested_views"] == []


def test_public_surface_unmatched_keys_remain_uncertain(capsys):
    assert seed_local.main(_cli("--selection-key", "missing", "--json")) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["question_projection"]["selection_keys"] == ["missing"]
    assert payload["selection"]["selected_view_names"] == []
    assert "unsupported selection key: missing" in payload["selection"]["selection_uncertainty"]


def test_public_surface_refusals_unknowns_and_empty_selection_visible_in_human(capsys):
    assert seed_local.main(_cli("--selection-key", "governance")) == 0
    human = capsys.readouterr().out

    assert "Selected views: constitutional_governance" in human
    assert "Preserved Unknowns" in human
    assert "Preserved refusals" in human
    assert "constitutional_governance: runtime governance" in human

    assert seed_local.main(_cli()) == 0
    empty = capsys.readouterr().out
    assert "Selected views: none" in empty
    assert "Selection uncertainty: no registered constitutional view matched deterministic projection keys" in empty


def test_public_surface_requires_explicit_bounded_inputs():
    with pytest.raises(SystemExit):
        seed_local.main(["--constitutional-pipeline", "--operator-inquiry", "testimony"])


def test_public_surface_inventory_visibility_is_registered():
    entry = next(entry for entry in DIAGNOSTIC_INVENTORY if entry.name == "constitutional_pipeline")
    rows = [row for row in build_diagnostic_shape_audit() if row.diagnostic == "constitutional_pipeline"]

    assert entry.cli_flags == ("--constitutional-pipeline",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False
    assert rows
    assert all(row.status == "consistent" for row in rows)


def test_existing_explicit_view_composition_surface_remains_distinct(capsys):
    assert seed_local.main([
        "--constitutional-view-composition",
        "constitutional_process",
        "--json",
    ]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["name"] == "Constitutional View Composition"
    assert "bounded_question" not in payload
    assert payload["request"]["requested_views"] == ["constitutional_process"]
