from dataclasses import FrozenInstanceError, asdict, replace

import pytest

from seed_runtime.bounded_constitutional_question import BoundedConstitutionalQuestion
from seed_runtime.constitutional_pipeline import (
    ConstitutionalPipelineRequest,
    ConstitutionalPipelineResult,
    invoke_constitutional_pipeline,
)
from seed_runtime.constitutional_view_composition import ConstitutionalViewCompositionArtifact
from seed_runtime.constitutional_view_selection import (
    ConstitutionalCapabilityProjection,
    ConstitutionalQuestionProjection,
    SelectedConstitutionalViews,
)
from seed_runtime.read_model_ownership import (
    CONSTITUTIONAL_READ_MODEL_CONTRACTS,
    constitutional_read_model_registration,
)


def _request(**overrides):
    values = {
        "operator_inquiry": "Operator says constitutional process should be inspected; this is testimony.",
        "inquiry_provenance": "operator:constitutional-pipeline-test",
        "bounded_question": "Explain the explicitly requested constitutional process view.",
        "constitutional_intent": "caller supplied compatibility inquiry",
        "scope_status": "caller-bounded; not independently verified",
        "uncertainty": ("caller scope preserved",),
        "unknowns": ("operator assertion not verified",),
        "bounded_question_id": "bounded-question:pipeline-test",
        "caller_supplied_fields": (("selection_key", "process"),),
        "composition_purpose": "compatibility",
        "output_format": "json",
    }
    values.update(overrides)
    return ConstitutionalPipelineRequest(**values)


def test_pipeline_success_path_observes_every_real_stage_artifact():
    result = invoke_constitutional_pipeline(_request())

    assert isinstance(result, ConstitutionalPipelineResult)
    assert isinstance(result.bounded_question, BoundedConstitutionalQuestion)
    assert isinstance(result.question_projection, ConstitutionalQuestionProjection)
    assert all(isinstance(item, ConstitutionalCapabilityProjection) for item in result.capability_projection)
    assert isinstance(result.selection, SelectedConstitutionalViews)
    assert result.composition_request.requested_views == ("constitutional_process",)
    assert isinstance(result.composition, ConstitutionalViewCompositionArtifact)
    assert result.composition.request is result.composition_request

    assert result.bounded_question.operator_inquiry == _request().operator_inquiry
    assert result.bounded_question.inquiry_provenance == "operator:constitutional-pipeline-test"
    assert result.bounded_question.testimony_status == "operator testimony preserved as evidence, not established fact"
    assert result.question_projection.selection_keys == ("process",)
    assert [p.registered_view_name for p in result.capability_projection] == [
        "constitutional_process",
        "constitutional_governance",
        "constitutional_fidelity",
    ]
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
    request = _request(
        capability_contracts=(contract,),
        capability_registrations=(registration,),
        capability_view_builders={},
        caller_supplied_fields=(("selection_key", "process"),),
    )
    before = asdict(request)

    first = invoke_constitutional_pipeline(request)
    second = invoke_constitutional_pipeline(request)

    assert first == second
    assert asdict(request) == before
    with pytest.raises(FrozenInstanceError):
        request.operator_inquiry = "changed"


def test_pipeline_insufficient_information_does_not_guess_question_or_capability_keys():
    contract = replace(
        CONSTITUTIONAL_READ_MODEL_CONTRACTS[0],
        name="constitutional_display_only",
        cli_flag="--display-only",
    )
    registration = constitutional_read_model_registration(contract)
    result = invoke_constitutional_pipeline(
        _request(
            caller_supplied_fields=(("note", "process words in testimony are not a key"),),
            capability_contracts=(contract,),
            capability_registrations=(registration,),
            capability_view_builders={},
        )
    )

    assert result.question_projection.selection_keys == ()
    assert result.capability_projection == (
        ConstitutionalCapabilityProjection(
            registered_view_name="constitutional_display_only",
            capability_keys=(),
            compatibility_answer="Unknown.",
        ),
    )
    assert result.selection.selected_view_names == ()
    assert "no registered constitutional view matched deterministic projection keys" in result.selection.selection_uncertainty
    assert result.composition_request.requested_views == ()
    assert result.composition.contributing_views == ()
    assert result.composition.compatibility_answer == "No."


def test_pipeline_preserves_unmatched_exact_keys_as_selection_uncertainty():
    result = invoke_constitutional_pipeline(
        _request(caller_supplied_fields=(("selection_key", "missing"),))
    )

    assert result.question_projection.selection_keys == ("missing",)
    assert result.selection.selected_view_names == ()
    assert "unsupported selection key: missing" in result.selection.selection_uncertainty
    assert result.composition_request.requested_views == ()


def test_pipeline_boundary_calls_existing_stage_functions(monkeypatch):
    import seed_runtime.constitutional_pipeline as pipeline

    calls = []
    original_produce = pipeline.produce_bounded_constitutional_question
    original_question = pipeline.project_constitutional_question
    original_capabilities = pipeline.project_constitutional_capabilities
    original_selection = pipeline.select_constitutional_views
    original_adapter = pipeline.selected_constitutional_views_to_composition_request
    original_composition = pipeline.build_constitutional_view_composition

    def produce_spy(**kwargs):
        calls.append("produce")
        return original_produce(**kwargs)

    def question_spy(bounded_question):
        calls.append(("question", isinstance(bounded_question, BoundedConstitutionalQuestion)))
        return original_question(bounded_question)

    def capabilities_spy(*args, **kwargs):
        calls.append("capabilities")
        return original_capabilities(*args, **kwargs)

    def selection_spy(**kwargs):
        calls.append(("selection", isinstance(kwargs["question_projection"], ConstitutionalQuestionProjection)))
        return original_selection(**kwargs)

    def adapter_spy(artifact, **kwargs):
        calls.append(("adapter", isinstance(artifact, SelectedConstitutionalViews)))
        return original_adapter(artifact, **kwargs)

    def composition_spy(request):
        calls.append("composition")
        return original_composition(request)

    monkeypatch.setattr(pipeline, "produce_bounded_constitutional_question", produce_spy)
    monkeypatch.setattr(pipeline, "project_constitutional_question", question_spy)
    monkeypatch.setattr(pipeline, "project_constitutional_capabilities", capabilities_spy)
    monkeypatch.setattr(pipeline, "select_constitutional_views", selection_spy)
    monkeypatch.setattr(pipeline, "selected_constitutional_views_to_composition_request", adapter_spy)
    monkeypatch.setattr(pipeline, "build_constitutional_view_composition", composition_spy)

    invoke_constitutional_pipeline(_request())

    assert calls == [
        "produce",
        ("question", True),
        "capabilities",
        ("selection", True),
        ("adapter", True),
        "composition",
    ]
