import json

import pytest

from scripts import seed_local
from seed_runtime import question_surface_inventory as qsi
from seed_runtime.constitutional_pipeline import ConstitutionalPipelineRequest


def _surface_args(selection_key="process"):
    return [
        "Operator says process should be visible; testimony only.",
        "operator:bounded-ask-integration-test",
        "Which constitutional process surface is available?",
        "caller supplied bounded constitutional inquiry",
        "bounded",
        selection_key,
    ]


def test_bounded_ask_constitutional_pipeline_path_is_existing_inventory_backed():
    rows = qsi.build_question_surface_inventory()
    row = next(row for row in rows if row.question_family == "constitutional pipeline")

    assert row.bounded_status == "eligible_with_parameters"
    assert row.dispatch_surface == "constitutional_pipeline"
    assert row.required_surface_args == (
        "operator_inquiry",
        "inquiry_source",
        "bounded_question",
        "constitutional_intent",
        "scope_status",
        "selection_key",
    )
    assert row.surface_flag == "--constitutional-pipeline"


def test_bounded_ask_constructs_real_pipeline_request_invoked_once_and_preserves_provenance(monkeypatch, capsys):
    calls = []
    original = seed_local.invoke_constitutional_pipeline

    def spy(request: ConstitutionalPipelineRequest):
        calls.append(request)
        return original(request)

    monkeypatch.setattr(seed_local, "invoke_constitutional_pipeline", spy)

    assert seed_local.main([
        "ask",
        "--question-family", "constitutional pipeline",
        "--surface-args", *_surface_args("process"),
        "--json",
    ]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert len(calls) == 1
    request = calls[0]
    assert isinstance(request, ConstitutionalPipelineRequest)
    assert request.inquiry_provenance == "operator:bounded-ask-integration-test"
    assert request.caller_supplied_fields == (("selection_key", "process"),)
    assert payload["bounded_question"]["inquiry_provenance"] == request.inquiry_provenance
    assert payload["bounded_question"]["operator_inquiry"] == request.operator_inquiry
    assert payload["bounded_question"]["testimony_status"] == "operator testimony preserved as evidence, not established fact"
    assert payload["question_projection"]["selection_keys"] == ["process"]
    assert payload["selection"]["selected_view_names"] == ["constitutional_process"]
    assert payload["provenance_explanation"]["selected_views"] == ["constitutional_process"]
    assert payload["provenance_explanation"]["mutates_cluster"] is False
    assert payload["provenance_explanation"]["writes_event_ledger"] is False


def test_bounded_ask_constitutional_pipeline_missing_key_is_not_inferred(capsys):
    assert seed_local.main([
        "ask",
        "--question-family", "constitutional pipeline",
        "--surface-args", *_surface_args(""),
        "--json",
    ]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["question_projection"]["selection_keys"] == []
    assert payload["selection"]["selected_view_names"] == []
    assert "No explicit selection key" in payload["provenance_explanation"]["empty_selection_explanation"]
    assert payload["composition"]["preserved_unknowns"] == []


def test_bounded_ask_constitutional_pipeline_unsupported_key_preserves_unknown_selection(capsys):
    assert seed_local.main([
        "ask",
        "--question-family", "constitutional pipeline",
        "--surface-args", *_surface_args("unsupported-explicit-key"),
        "--json",
    ]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["question_projection"]["selection_keys"] == ["unsupported-explicit-key"]
    assert payload["selection"]["selected_view_names"] == []
    assert payload["provenance_explanation"]["unsupported_question_keys"] == ["unsupported-explicit-key"]
    assert "unsupported selection key: unsupported-explicit-key" in payload["selection"]["selection_uncertainty"]
    assert "no registered constitutional view matched deterministic projection keys" in payload["selection"]["selection_uncertainty"]


def test_bounded_ask_refusal_remains_owned_by_original_path(monkeypatch):
    calls = []
    monkeypatch.setattr(seed_local, "invoke_constitutional_pipeline", lambda request: calls.append(request))

    with pytest.raises(SystemExit):
        seed_local.main(["ask", "--question-family", "surface inventory"])

    assert calls == []


def test_unrelated_bounded_ask_path_is_not_redirected(monkeypatch, capsys):
    calls = []
    monkeypatch.setattr(seed_local, "invoke_constitutional_pipeline", lambda request: calls.append(request))

    assert seed_local.main(["ask", "--question-family", "projection shape visibility", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert calls == []
    assert "stages" in payload


def test_adapter_boundaries_do_not_own_admission_or_pipeline_stages():
    rows = qsi.build_question_surface_inventory()
    prepared = qsi._prepare_question_family_eligibility_input("constitutional pipeline", rows)
    eligibility = qsi._bounded_work_eligibility_for_prepared_question_family(prepared)
    surface_args = qsi.bounded_work_surface_args_for_eligibility(
        "constitutional pipeline", eligibility, tuple(_surface_args("process"))
    )
    selection = qsi.bounded_work_selection_for_question_family(
        "constitutional pipeline", eligibility, surface_args
    )
    request = qsi.bounded_work_dispatch_request_for_selection(selection)

    assert prepared.question_family == "constitutional pipeline"
    assert eligibility.permitted is True
    assert request.dispatch_surface == "constitutional_pipeline"
    assert request.surface_value["selection_key"] == ("process",)
    assert selection.reason == "selected bounded ask dispatch surface"
