"""RuntimeLoop decision validation service.

DEPRECATED / EXPERIMENTAL: Runtime is the only canonical Seed runtime path.
This RuntimeLoop module is quarantined for historical/experimental tests and
must not be wired into CLI, API, default production paths, or canonical tests.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from seed_runtime.runtime_loop import Decision


class RuntimeLoopDecisionValidator:
    """Validate decisions returned to RuntimeLoop without routing them."""

    def validate_decision(self, proposed: object) -> tuple["Decision | None", str | None]:
        from seed_runtime.runtime_loop import Decision

        if not isinstance(proposed, Decision):
            return None, "decision provider must return a runtime_loop.Decision"
        if proposed.kind not in {"answer", "call_tool", "request_tool"}:
            return None, "decision kind must be 'answer', 'call_tool', or 'request_tool'"
        if not isinstance(proposed.reason, str):
            return None, "decision reason must be a string"
        if proposed.kind == "answer":
            if not isinstance(proposed.text, str) or proposed.text == "":
                return None, "answer decisions require non-empty text"
            if proposed.tool_name is not None or proposed.tool_args:
                return None, "answer decisions may not include tool output fields"
            if proposed.tool_need is not None:
                return None, "answer decisions may not include tool_need"
        if proposed.kind == "call_tool":
            if not isinstance(proposed.tool_name, str) or proposed.tool_name == "":
                return None, "tool decisions require a non-empty tool_name"
            if not isinstance(proposed.tool_args, dict):
                return None, "tool decisions require tool_args to be a dict"
            if proposed.text is not None:
                return None, "tool decisions may not include answer text"
            if proposed.tool_need is not None:
                return None, "tool decisions may not include tool_need"
        if proposed.kind == "request_tool":
            if not isinstance(proposed.tool_need, dict):
                return None, "request_tool decisions require tool_need dict"
            for field_name in ("name", "summary", "capability"):
                value = proposed.tool_need.get(field_name)
                if not isinstance(value, str) or value.strip() == "":
                    return None, f"request_tool decisions require non-empty {field_name}"
            if proposed.tool_name is not None or proposed.tool_args or proposed.text is not None:
                return None, "request_tool decisions may not include tool_name, tool_args, or text"
        return proposed, None
