"""Registration service for validated toolkit candidates."""

from __future__ import annotations

from pathlib import Path

from seed_builder.validator import ValidationReport
from seed_runtime.events import EventLedger
from seed_runtime.registry import ToolRegistry, load_toolkit_manifest
from seed_runtime.serialization import to_plain


class ToolkitRegistrationService:
    def __init__(self, ledger: EventLedger, registry: ToolRegistry) -> None:
        self.ledger = ledger
        self.registry = registry

    def register(self, workspace_id: str, artifact_path: str | Path, report: ValidationReport, *, causation_id: str | None = None) -> list[str]:
        if not report.ok:
            raise ValueError("cannot register candidate with failed validation report")
        toolkit = load_toolkit_manifest(Path(artifact_path) / "toolkit.yaml")
        self.registry.register_toolkit(toolkit)
        registered = []
        for tool in toolkit.tools:
            registered.append(tool.name)
            self.ledger.append(
                "tool.registered",
                workspace_id,
                {"tool": to_plain(tool), "candidate_id": report.candidate_id},
                actor="builder",
                causation_id=causation_id,
            )
        return registered
