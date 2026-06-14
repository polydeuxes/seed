import json

from seed_runtime.candidate_requests import inspect_candidate_requests

from test_seed_local_script import load_seed_local_module


def test_state_summary_input_preserves_high_confidence_state_summary_candidate():
    inspection = inspect_candidate_requests("show me state summary")

    assert inspection.ambiguity is False
    assert [candidate.label for candidate in inspection.candidates] == ["state summary"]
    assert inspection.candidates[0].confidence == "high"
    assert inspection.boundary == "candidate_request_preservation_only"


def test_generic_summary_input_preserves_multiple_summary_candidates():
    inspection = inspect_candidate_requests("show me summary")

    assert inspection.ambiguity is True
    assert [candidate.label for candidate in inspection.candidates] == [
        "state summary",
        "integrity summary",
        "impact summary",
    ]
    assert {candidate.confidence for candidate in inspection.candidates} == {"medium"}


def test_ambiguous_summary_preserves_ambiguity_instead_of_selecting_one():
    inspection = inspect_candidate_requests("show me summary")

    assert inspection.ambiguity is True
    assert len(inspection.candidates) > 1
    assert "ambiguity_preserved_not_failure" in inspection.notes


def test_candidate_request_inspection_does_not_perform_downstream_authority_steps():
    inspection = inspect_candidate_requests("show me summary")

    assert "no_capability_selection" in inspection.notes
    assert "no_policy_execution" in inspection.notes
    assert "no_tool_execution" in inspection.notes
    assert all("capability" not in candidate.__dict__ for candidate in inspection.candidates)


def test_candidate_requests_cli_is_read_only_and_does_not_build_runtime(capsys, monkeypatch):
    seed_local = load_seed_local_module()

    def fail_build_local_app(*args, **kwargs):  # pragma: no cover - guard callback
        raise AssertionError("candidate request inspection must not build runtime")

    def fail_tool_executor(*args, **kwargs):  # pragma: no cover - guard callback
        raise AssertionError("candidate request inspection must not create ToolExecutor")

    monkeypatch.setattr(seed_local, "build_local_app", fail_build_local_app)
    monkeypatch.setattr(seed_local, "ToolExecutor", fail_tool_executor)

    assert seed_local.main(["--candidate-requests", "show me summary"]) == 0

    output = json.loads(capsys.readouterr().out)
    assert output["boundary"] == "candidate_request_preservation_only"
    assert output["ambiguity"] is True
    assert [candidate["label"] for candidate in output["candidates"]] == [
        "state summary",
        "integrity summary",
        "impact summary",
    ]
    assert "no_capability_selection" in output["notes"]
    assert "no_policy_execution" in output["notes"]
    assert "no_tool_execution" in output["notes"]
