from seed_builder.generator import CandidateStore, ToolkitGenerator
from seed_builder.validator import ToolkitValidator
from seed_runtime.models import ToolNeed


def test_validator_accepts_generated_stub_candidate(tmp_path):
    need = ToolNeed(id="need_1", workspace_id="ws", name="host_notes", summary="Record notes about hosts", capability="host_notes", reason="safe demo", desired_inputs=["host"], desired_outputs=["stored"])
    candidate = ToolkitGenerator(CandidateStore(tmp_path)).generate(need)

    report = ToolkitValidator().validate(candidate.id, candidate.artifact_path)

    assert report.ok, report.checks
    assert [check.name for check in report.checks] == ["manifest", "schemas", "implementation_refs", "forbidden_imports", "tests"]
