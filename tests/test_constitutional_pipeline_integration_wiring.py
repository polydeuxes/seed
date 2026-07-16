import pytest

from scripts import seed_local
from seed_runtime.constitutional_pipeline import ConstitutionalPipelineRequest, invoke_constitutional_pipeline, constitutional_pipeline_result_json, format_constitutional_pipeline_result, explain_constitutional_pipeline_provenance
from seed_runtime.constitutional_pipeline_diagnostic import build_constitutional_pipeline_diagnostic, constitutional_pipeline_diagnostic_json
from tests.constitutional_pipeline_test_support import bounded_question


def test_pipeline_diagnostic_helper_consumes_existing_question_without_raw_ingress():
    supplied = bounded_question(bounded_question_id="bounded-question:diagnostic-supplied")
    request = ConstitutionalPipelineRequest(bounded_question=supplied)
    diagnostic = build_constitutional_pipeline_diagnostic(request)

    assert diagnostic.pipeline_request.bounded_question is supplied
    assert diagnostic.pipeline_result.bounded_question is supplied
    assert diagnostic.stages[0].artifact_identity == "bounded-question:diagnostic-supplied"
    assert diagnostic.pipeline_read_only is True
    assert diagnostic.writes_event_ledger is False
    assert diagnostic.mutates_cluster is False
    assert constitutional_pipeline_diagnostic_json(diagnostic)["pipeline_result"]["bounded_question"]["bounded_question_id"] == "bounded-question:diagnostic-supplied"


def test_provenance_and_renderers_preserve_supplied_identity_and_output_behavior():
    supplied = bounded_question(bounded_question_id="bounded-question:renderer-supplied")
    result = invoke_constitutional_pipeline(ConstitutionalPipelineRequest(bounded_question=supplied))
    explanation = explain_constitutional_pipeline_provenance(result)
    payload = constitutional_pipeline_result_json(result)
    rendered = format_constitutional_pipeline_result(result)

    assert result.bounded_question is supplied
    assert explanation.bounded_question_id == "bounded-question:renderer-supplied"
    assert explanation.read_only is True
    assert explanation.writes_event_ledger is False
    assert explanation.mutates_cluster is False
    assert payload["bounded_question"]["bounded_question_id"] == "bounded-question:renderer-supplied"
    assert payload["provenance_explanation"]["bounded_question_id"] == "bounded-question:renderer-supplied"
    assert "ID: bounded-question:renderer-supplied" in rendered
    assert "no event-ledger writes" in rendered
    assert "no cluster mutation" in rendered


def test_cli_raw_pipeline_ingress_is_removed():
    with pytest.raises(SystemExit):
        seed_local.main(["--constitutional-pipeline", "--operator-inquiry", "raw", "--inquiry-provenance", "raw", "--bounded-question", "raw", "--constitutional-intent", "raw", "--scope-status", "raw"])
    with pytest.raises(SystemExit):
        seed_local.main(["--constitutional-pipeline-diagnostic", "--operator-inquiry", "raw", "--inquiry-provenance", "raw", "--bounded-question", "raw", "--constitutional-intent", "raw", "--scope-status", "raw"])


def test_request_shape_rejects_raw_question_fields():
    with pytest.raises(TypeError):
        ConstitutionalPipelineRequest(operator_inquiry="raw", inquiry_provenance="raw", bounded_question="raw", constitutional_intent="raw", scope_status="raw")
