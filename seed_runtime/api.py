"""Dependency-light API shell around Seed services.

This module intentionally avoids binding the architecture to a web framework.
A FastAPI/Flask adapter can call these methods directly when selected.
"""

from __future__ import annotations

from seed_runtime.models import RuntimeResponse
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import Runtime
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


class SeedAPI:
    def __init__(self, runtime: Runtime, projector: StateProjector, registry: ToolRegistry) -> None:
        self.runtime = runtime
        self.projector = projector
        self.registry = registry

    def post_user_message(self, workspace_id: str, session_id: str, text: str) -> RuntimeResponse:
        return self.runtime.handle_user_message(workspace_id, session_id, text)

    def get_state(self, workspace_id: str) -> dict[str, object]:
        return to_plain(self.projector.project(workspace_id))

    def get_toolkits(self) -> list[dict[str, object]]:
        return [to_plain(toolkit) for toolkit in self.registry.list_toolkits()]

    def get_tools(self) -> list[dict[str, object]]:
        return [to_plain(tool) for tool in self.registry.list_tools()]

    def get_tool_needs(self, workspace_id: str) -> list[dict[str, object]]:
        return [to_plain(need) for need in self.projector.project(workspace_id).tool_needs.values()]
