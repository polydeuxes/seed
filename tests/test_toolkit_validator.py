from seed_builder.generator import CandidateStore, ToolkitGenerator
from seed_builder.validator import ToolkitValidator
from seed_runtime.models import ToolNeed


def test_validator_accepts_generated_stub_candidate(tmp_path):
    need = ToolNeed(id="need_1", workspace_id="ws", name="host_notes", summary="Record notes about hosts", capability="host_notes", reason="safe demo", desired_inputs=["host"], desired_outputs=["stored"])
    candidate = ToolkitGenerator(CandidateStore(tmp_path)).generate(need)

    report = ToolkitValidator().validate(candidate.id, candidate.artifact_path)

    assert report.ok, report.checks
    assert [check.name for check in report.checks] == ["manifest", "schemas", "implementation_refs", "forbidden_imports", "tests"]


def test_validator_fails_candidate_tests_that_exceed_timeout(tmp_path):
    need = ToolNeed(
        id="need_slow",
        workspace_id="ws",
        name="slow_tool",
        summary="Slow candidate",
        capability="slow",
        reason="prove validation timeout",
    )
    candidate = ToolkitGenerator(CandidateStore(tmp_path)).generate(need)
    test_path = tmp_path / candidate.id / "tests" / "test_operation.py"
    test_path.write_text(
        "import time\n\n"
        "def test_slow_candidate():\n"
        "    time.sleep(1)\n"
    )

    report = ToolkitValidator(test_timeout_seconds=0.01).validate(candidate.id, candidate.artifact_path)

    tests_check = next(check for check in report.checks if check.name == "tests")
    assert not tests_check.ok
    assert "timed out" in tests_check.message
