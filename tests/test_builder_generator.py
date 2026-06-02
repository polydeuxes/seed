from pathlib import Path

from seed_builder.generator import CandidateStore, ToolkitGenerator
from seed_runtime.models import ToolNeed


def test_generator_writes_candidate_file_set(tmp_path):
    need = ToolNeed(id="need_1", workspace_id="ws", name="host_notes", summary="Record notes about hosts", capability="host_notes", reason="safe demo", desired_inputs=["host", "note"], desired_outputs=["stored"])
    candidate = ToolkitGenerator(CandidateStore(tmp_path)).generate(need)
    path = Path(candidate.artifact_path)

    assert (path / "toolkit.yaml").exists()
    assert (path / "operations.py").exists()
    assert (path / "tests/test_operation.py").exists()
    assert (path / "docs.md").read_text().startswith("# host_notes")
