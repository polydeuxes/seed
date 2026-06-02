"""Safe echo toolkit operations."""

from __future__ import annotations

from seed_runtime.execution import ToolContext


def echo(ctx: ToolContext, message: str) -> dict[str, object]:
    return {"ok": True, "message": message, "workspace_id": ctx.workspace_id}
