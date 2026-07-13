from dataclasses import FrozenInstanceError, asdict
import json

import pytest

import seed_runtime.constitutional_pipeline as pipeline
from seed_runtime.constitutional_pipeline import (
    ConstitutionalPipelineProvenanceExplanation,
    ConstitutionalPipelineRequest,
    constitutional_pipeline_result_json,
    explain_constitutional_pipeline_provenance,
    format_constitutional_pipeline_result,
    invoke_constitutional_pipeline,
)
from seed_runtime.constitutional_pipeline_diagnostic import constitutional_pipeline_diagnostic_from_result
from seed_runtime.read_model_ownership import CONSTITUTIONAL_READ_MODEL_CONTRACTS


def _request(**overrides):
    values = {
        "operator_inquiry": "Operator says process should be visible; testimony only.",
        "inquiry_provenance": "operator:provenance-test",
        "bounded_question": "Explain explicitly selected constitutional process view.",
        "constitutional_intent": "caller supplied provenance inquiry",
        "scope_status": "caller-bounded; not independently verified",
        "uncertainty": ("caller uncertainty preserved",),
        "unknowns": (),
        "bounded_question_id": "bounded-question:provenance-test",
        "caller_supplied_fields": (("selection_key", "process"),),
        "composition_purpose": "compatibility",
        "output_format": "json",
    }
    values.update(overrides)
    return ConstitutionalPipelineRequest(**values)


def test_explanation_consumes_completed_result_without_running_pipeline_again(monkeypatch):
    result = invoke_constitutional_pipeline(_request())

    def fail(*args, **kwargs):
        raise AssertionError("stage should not run during provenance explanation")

    monkeypatch.setattr(pipeline, "produce_bounded_constitutional_question", fail)
    monkeypatch.setattr(pipeline, "project_constitutional_question", fail)
    monkeypatch.setattr(pipeline, "project_constitutional_capabilities", fail)
    monkeypatch.setattr(pipeline, "select_constitutional_views", fail)
    monkeypatch.setattr(pipeline, "build_constitutional_view_composition", fail)

    explanation = explain_constitutional_pipeline_provenance(result)

    assert isinstance(explanation, ConstitutionalPipelineProvenanceExplanation)
    assert explanation.bounded_question_id == "bounded-question:provenance-test"
    assert explanation.inquiry_provenance == "operator:provenance-test"
    assert explanation.operator_inquiry_testimony == _request().operator_inquiry
    assert explanation.question_selection_keys == ("process",)
    assert ("constitutional_process", ("process",)) in explanation.available_capability_keys
    assert explanation.matched_keys == ("process",)
    assert explanation.selected_views == ("constitutional_process",)
    assert explanation.composition_contributors == ("constitutional_process",)
    assert explanation.unsupported_question_keys == ()
    assert explanation.unselected_or_unavailable_views == ()
    assert explanation.read_only is True
    assert explanation.writes_event_ledger is False
    assert explanation.mutates_cluster is False
    with pytest.raises(FrozenInstanceError):
        explanation.read_only = False


def test_explanation_distinguishes_absent_unsupported_unknown_refused_and_selected():
    absent = explain_constitutional_pipeline_provenance(
        invoke_constitutional_pipeline(_request(caller_supplied_fields=()))
    )
    assert absent.question_selection_keys == ()
    assert absent.unsupported_question_keys == ()
    assert absent.selected_views == ()
    assert absent.unselected_or_unavailable_views == ("absent: no explicit question selection key was supplied",)
    assert "not verified irrelevance" in absent.empty_selection_explanation

    unsupported = explain_constitutional_pipeline_provenance(
        invoke_constitutional_pipeline(_request(caller_supplied_fields=(("selection_key", "missing"),)))
    )
    assert unsupported.question_selection_keys == ("missing",)
    assert unsupported.unsupported_question_keys == ("missing",)
    assert unsupported.matched_keys == ()
    assert unsupported.selected_views == ()
    assert "unsupported: missing did not match any projected capability key" in unsupported.unselected_or_unavailable_views
    assert "invalid" not in json.dumps(asdict(unsupported)).lower()

    missing_capability = explain_constitutional_pipeline_provenance(
        invoke_constitutional_pipeline(
            _request(
                capability_contracts=(CONSTITUTIONAL_READ_MODEL_CONTRACTS[0],),
                capability_registrations=(),
                capability_view_builders={},
            )
        )
    )
    assert missing_capability.question_selection_keys == ("process",)
    assert missing_capability.available_capability_keys == (("constitutional_process", ()),)
    assert missing_capability.unsupported_question_keys == ("process",)
    assert any(item.startswith("unknown: constitutional_process") for item in missing_capability.unselected_or_unavailable_views)

    unknown = explain_constitutional_pipeline_provenance(
        invoke_constitutional_pipeline(_request(unknowns=("operator assertion not verified",)))
    )
    assert "unknown: operator assertion not verified" in unknown.selection_uncertainty
    assert unknown.composition_unknowns

    refused = explain_constitutional_pipeline_provenance(
        invoke_constitutional_pipeline(_request(caller_supplied_fields=(("selection_key", "governance"),)))
    )
    assert refused.matched_keys == ("governance",)
    assert refused.selected_views == ("constitutional_governance",)
    assert refused.composition_contributors == ("constitutional_governance",)
    assert refused.composition_unknowns
    assert refused.composition_refusals


def test_explanation_boundaries_do_not_replace_stage_artifacts_or_diagnostic_status():
    result = invoke_constitutional_pipeline(_request(caller_supplied_fields=(("selection_key", "process"),)))
    explanation = explain_constitutional_pipeline_provenance(result)
    diagnostic = constitutional_pipeline_diagnostic_from_result(request=_request(), result=result)

    assert explanation != result.question_projection
    assert explanation != result.capability_projection
    assert explanation != result.selection
    assert explanation != result.composition
    assert not hasattr(explanation, "status")
    assert diagnostic.stages[3].status == "complete"
    assert explanation.selected_views == result.selection.selected_view_names


def test_explanation_is_deterministic_and_preserves_testimony_boundary():
    request = _request()
    first = explain_constitutional_pipeline_provenance(invoke_constitutional_pipeline(request))
    second = explain_constitutional_pipeline_provenance(invoke_constitutional_pipeline(request))

    assert first == second
    encoded = json.dumps(asdict(first), sort_keys=True)
    assert encoded == json.dumps(asdict(second), sort_keys=True)
    assert "established fact" in first.testimony_boundary
    assert "claim is true" not in encoded.lower()
    assert "proves a fact" not in encoded.lower()
    assert "selection" in first.explanation_boundary


def test_public_json_and_human_output_expose_deterministic_explanation():
    result = invoke_constitutional_pipeline(_request())
    first_json = constitutional_pipeline_result_json(result)
    second_json = constitutional_pipeline_result_json(result)
    first_human = format_constitutional_pipeline_result(result)
    second_human = format_constitutional_pipeline_result(result)

    assert first_json == second_json
    assert first_json["provenance_explanation"]["bounded_question_id"] == "bounded-question:provenance-test"
    assert first_json["provenance_explanation"]["matched_keys"] == ("process",)
    assert first_json["provenance_explanation"]["selected_views"] == ("constitutional_process",)
    assert first_json["provenance_explanation"]["writes_event_ledger"] is False
    assert first_json["provenance_explanation"]["mutates_cluster"] is False
    assert first_human == second_human
    assert "Provenance explanation" in first_human
    assert "Why these views were selected" in first_human
    assert "Why requested keys were unsupported" in first_human
    assert "Remaining uncertainty" in first_human
    assert "Composition contributors" in first_human
