from dataclasses import FrozenInstanceError, asdict, replace

import pytest

from seed_runtime.bounded_constitutional_question import BoundedConstitutionalQuestion
from seed_runtime.constitutional_pipeline import (
    ConstitutionalPipelineRequest,
    ConstitutionalPipelineResult,
    constitutional_pipeline_result_json,
    format_constitutional_pipeline_result,
    invoke_constitutional_pipeline,
)
from seed_runtime.constitutional_view_composition import ConstitutionalViewCompositionArtifact
from seed_runtime.constitutional_view_selection import ConstitutionalCapabilityProjection, ConstitutionalQuestionProjection, SelectedConstitutionalViews
from seed_runtime.read_model_ownership import CONSTITUTIONAL_READ_MODEL_CONTRACTS, constitutional_read_model_registration
from tests.constitutional_pipeline_test_support import bounded_question


def _request(**overrides):
    values = {
        "bounded_question": bounded_question(),
        "composition_purpose": "compatibility",
        "output_format": "json",
    }
    values.update(overrides)
    return ConstitutionalPipelineRequest(**values)


def test_request_requires_existing_bounded_question_and_rejects_raw_fields():
    supplied = bounded_question()
    request = ConstitutionalPipelineRequest(bounded_question=supplied)
    assert request.bounded_question is supplied
    with pytest.raises(TypeError):
        ConstitutionalPipelineRequest(
            operator_inquiry="raw",
            inquiry_provenance="raw",
            bounded_question="raw",
            constitutional_intent="raw",
            scope_status="raw",
        )
    assert "operator_inquiry" not in ConstitutionalPipelineRequest.__dataclass_fields__
    assert "bounded_question_id" not in ConstitutionalPipelineRequest.__dataclass_fields__


def test_pipeline_never_constructs_bounded_question(monkeypatch):
    import seed_runtime.constitutional_pipeline as pipeline
    assert not hasattr(pipeline, "produce_bounded_constitutional_question")
    supplied = bounded_question()
    result = invoke_constitutional_pipeline(_request(bounded_question=supplied))
    assert result.bounded_question is supplied


def test_supplied_identity_reaches_projection_selection_composition_provenance_and_rendering():
    supplied = bounded_question(bounded_question_id="bounded-question:exact-supplied")
    result = invoke_constitutional_pipeline(_request(bounded_question=supplied))
    payload = constitutional_pipeline_result_json(result)
    rendered = format_constitutional_pipeline_result(result)

    assert result.bounded_question is supplied
    assert result.question_projection.bounded_question_id == "bounded-question:exact-supplied"
    assert result.selection.bounded_question_id == "bounded-question:exact-supplied"
    assert result.composition.request is result.composition_request
    assert payload["provenance_explanation"]["bounded_question_id"] == "bounded-question:exact-supplied"
    assert "ID: bounded-question:exact-supplied" in rendered


def test_pipeline_success_path_preserves_downstream_output_and_read_only_boundaries():
    result = invoke_constitutional_pipeline(_request())

    assert isinstance(result, ConstitutionalPipelineResult)
    assert isinstance(result.bounded_question, BoundedConstitutionalQuestion)
    assert isinstance(result.question_projection, ConstitutionalQuestionProjection)
    assert all(isinstance(item, ConstitutionalCapabilityProjection) for item in result.capability_projection)
    assert isinstance(result.selection, SelectedConstitutionalViews)
    assert result.composition_request.requested_views == ("constitutional_process",)
    assert isinstance(result.composition, ConstitutionalViewCompositionArtifact)
    assert result.composition.request is result.composition_request
    assert result.question_projection.selection_keys == ("process",)
    assert result.selection.selected_view_names == ("constitutional_process",)
    assert [view.name for view in result.composition.contributing_views] == ["constitutional_process"]
    assert result.bounded_question.writes_event_ledger is False
    assert result.question_projection.writes_event_ledger is False
    assert not any(p.writes_event_ledger for p in result.capability_projection)
    assert result.selection.writes_event_ledger is False
    assert result.composition.writes_event_ledger is False
    assert result.bounded_question.mutates_cluster is False
    assert result.question_projection.mutates_cluster is False
    assert not any(p.mutates_cluster for p in result.capability_projection)
    assert result.selection.mutates_cluster is False
    assert result.composition.mutates_cluster is False
    assert "established_fact" not in asdict(result)
    assert "verified_claim" not in asdict(result)


def test_pipeline_is_deterministic_and_does_not_mutate_request_or_sources():
    contract = CONSTITUTIONAL_READ_MODEL_CONTRACTS[0]
    registration = constitutional_read_model_registration(contract)
    request = _request(capability_contracts=(contract,), capability_registrations=(registration,), capability_view_builders={})
    before = asdict(request)

    assert invoke_constitutional_pipeline(request) == invoke_constitutional_pipeline(request)
    assert asdict(request) == before
    with pytest.raises(FrozenInstanceError):
        request.bounded_question = bounded_question()


def test_pipeline_insufficient_information_does_not_guess_question_or_capability_keys():
    contract = replace(CONSTITUTIONAL_READ_MODEL_CONTRACTS[0], name="constitutional_display_only", cli_flag="--display-only")
    registration = constitutional_read_model_registration(contract)
    result = invoke_constitutional_pipeline(
        _request(
            bounded_question=bounded_question(caller_supplied_fields=(("note", "process words in testimony are not a key"),)),
            capability_contracts=(contract,),
            capability_registrations=(registration,),
            capability_view_builders={},
        )
    )

    assert result.question_projection.selection_keys == ()
    assert result.capability_projection == (ConstitutionalCapabilityProjection(registered_view_name="constitutional_display_only", capability_keys=(), compatibility_answer="Unknown."),)
    assert result.selection.selected_view_names == ()
    assert result.composition_request.requested_views == ()
    assert result.composition.compatibility_answer == "No."
