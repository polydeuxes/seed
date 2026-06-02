"""Toolkit manifest loading and runtime tool registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from seed_runtime.models import ToolSpec, Toolkit


class ManifestError(ValueError):
    """Raised when a toolkit manifest is invalid."""


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}
        self._toolkits: dict[str, Toolkit] = {}

    def register_toolkit(self, toolkit: Toolkit) -> None:
        if toolkit.id in self._toolkits:
            raise ManifestError(f"toolkit {toolkit.id!r} is already registered")
        for tool in toolkit.tools:
            if tool.name in self._tools:
                raise ManifestError(f"tool {tool.name!r} is already registered")
        self._toolkits[toolkit.id] = toolkit
        for tool in toolkit.tools:
            self._tools[tool.name] = tool

    def get(self, name: str) -> ToolSpec | None:
        return self._tools.get(name)

    def require(self, name: str) -> ToolSpec:
        tool = self.get(name)
        if tool is None:
            raise KeyError(f"unknown tool {name!r}")
        return tool

    def list_tools(self, *, visible_only: bool = False) -> list[ToolSpec]:
        tools = list(self._tools.values())
        if visible_only:
            tools = [tool for tool in tools if tool.visibility == "model_visible" and tool.status == "registered"]
        return sorted(tools, key=lambda tool: tool.name)

    def list_toolkits(self) -> list[Toolkit]:
        return sorted(self._toolkits.values(), key=lambda toolkit: toolkit.name)

    def load_manifest(self, path: str | Path) -> Toolkit:
        toolkit = load_toolkit_manifest(path)
        self.register_toolkit(toolkit)
        return toolkit


def load_toolkit_manifest(path: str | Path) -> Toolkit:
    manifest_path = Path(path)
    data = json.loads(manifest_path.read_text())
    return toolkit_from_manifest(data)


def toolkit_from_manifest(data: dict[str, Any]) -> Toolkit:
    for key in ("id", "name", "summary", "tools"):
        if key not in data:
            raise ManifestError(f"manifest missing {key!r}")
    if not isinstance(data["tools"], list) or not data["tools"]:
        raise ManifestError("manifest must define at least one tool")
    tools: list[ToolSpec] = []
    for tool_data in data["tools"]:
        for key in ("name", "summary", "input_schema", "output_schema", "policy_action", "implementation"):
            if key not in tool_data:
                raise ManifestError(f"tool missing {key!r}")
        tools.append(
            ToolSpec(
                toolkit_id=data["id"],
                name=tool_data["name"],
                summary=tool_data["summary"],
                input_schema=tool_data["input_schema"],
                output_schema=tool_data["output_schema"],
                policy_action=tool_data["policy_action"],
                implementation=tool_data["implementation"],
                status=tool_data.get("status", "registered"),
                visibility=tool_data.get("visibility", "model_visible"),
                risk_class=tool_data.get("risk_class", "L1"),
                examples=tool_data.get("examples", []),
            )
        )
    return Toolkit(
        id=data["id"],
        name=data["name"],
        summary=data["summary"],
        tools=tools,
        status=data.get("status", "registered"),
        source=data.get("source", "core"),
    )
