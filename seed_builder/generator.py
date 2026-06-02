"""Toolkit candidate generation from Tool Needs."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from seed_runtime.ids import new_id
from seed_runtime.models import ToolkitCandidate, ToolNeed


@dataclass(frozen=True)
class CandidateStore:
    root: Path

    def write(self, candidate_id: str, files: dict[str, str]) -> Path:
        candidate_path = self.root / candidate_id
        candidate_path.mkdir(parents=True, exist_ok=True)
        for relative, content in files.items():
            target = candidate_path / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        return candidate_path


class ToolkitGenerator:
    def __init__(self, store: CandidateStore | None = None) -> None:
        self.store = store or CandidateStore(Path("builder_out"))

    def generate(self, need: ToolNeed) -> ToolkitCandidate:
        candidate_id = new_id("cand")
        files = self._render_files(need)
        path = self.store.write(candidate_id, files)
        return ToolkitCandidate(
            id=candidate_id,
            tool_need_id=need.id,
            workspace_id=need.workspace_id,
            artifact_path=str(path),
        )

    def _render_files(self, need: ToolNeed) -> dict[str, str]:
        toolkit_id = f"tk_generated_{need.name}"
        input_properties = {name: {"type": "string"} for name in (need.desired_inputs or ["input"])}
        output_properties = {"ok": {"type": "boolean"}, "summary": {"type": "string"}}
        for name in need.desired_outputs:
            output_properties[name] = {"type": "string"}
        manifest = {
            "id": toolkit_id,
            "name": need.name,
            "summary": need.summary,
            "source": "generated",
            "tools": [
                {
                    "name": need.name,
                    "summary": need.summary,
                    "input_schema": {
                        "type": "object",
                        "required": list(input_properties),
                        "properties": input_properties,
                        "additionalProperties": False,
                    },
                    "output_schema": {
                        "type": "object",
                        "required": ["ok", "summary"],
                        "properties": output_properties,
                        "additionalProperties": False,
                    },
                    "policy_action": f"generated.{need.name}",
                    "implementation": "operations:run",
                    "risk_class": "L3" if need.risk_hint == "mutating" else "L1",
                    "visibility": "model_visible",
                }
            ],
        }
        return {
            "toolkit.yaml": json.dumps(manifest, indent=2),
            "operations.py": self._operation_stub(need),
            "tests/test_operation.py": self._test_stub(need),
            "docs.md": f"# {need.name}\n\n{need.summary}\n\nReason: {need.reason}\n",
            "generation_notes.md": "Generated as an untrusted candidate. Validate before registration.\n",
        }

    def _operation_stub(self, need: ToolNeed) -> str:
        args = ", ".join(need.desired_inputs or ["input"])
        return f'''"""Generated candidate operation for {need.name}."""

from __future__ import annotations


def run(ctx, {args}):
    """Candidate stub; replace with reviewed implementation before registration."""
    return {{"ok": True, "summary": "Stubbed candidate for {need.name}."}}
'''

    def _test_stub(self, need: ToolNeed) -> str:
        kwargs = ", ".join(f"{name}='example'" for name in (need.desired_inputs or ["input"]))
        return f'''from operations import run


class Ctx:
    workspace_id = "ws_test"


def test_run_stub():
    result = run(Ctx(), {kwargs})
    assert result["ok"] is True
    assert "{need.name}" in result["summary"]
'''
