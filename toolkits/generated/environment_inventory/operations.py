"""Safe read-only environment inventory operations.

The functions in this generated toolkit only inspect in-memory Seed runtime
objects and the projected event-ledger state for the active workspace. They do
not run shell commands, open network connections, or scan the filesystem.
"""

from __future__ import annotations

from seed_runtime.execution import ToolContext
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


def _project_state(ctx: ToolContext):
    return StateProjector(ctx.ledger).project(ctx.workspace_id)


def list_registered_tools(ctx: ToolContext) -> dict[str, object]:
    """Return model-visible registered tools known to the current executor."""

    if ctx.registry is not None:
        tool_specs = ctx.registry.list_tools(visible_only=True)
    else:
        state = _project_state(ctx)
        tool_specs = sorted(
            [
                tool
                for tool in state.tools.values()
                if tool.visibility == "model_visible" and tool.status == "registered"
            ],
            key=lambda tool: tool.name,
        )
    tools = [
        {
            "name": tool.name,
            "summary": tool.summary,
            "risk_class": tool.risk_class,
        }
        for tool in tool_specs
    ]
    return {"ok": True, "tools": tools}


def list_open_tool_needs(ctx: ToolContext) -> dict[str, object]:
    """Return open ToolNeeds from the current projected state."""

    state = _project_state(ctx)
    needs = [
        to_plain(need)
        for need in sorted(state.open_tool_needs, key=lambda need: need.id)
    ]
    return {"ok": True, "tool_needs": needs}


def list_known_entities(ctx: ToolContext) -> dict[str, object]:
    """Return known entities from the current projected state."""

    state = _project_state(ctx)
    entities = [
        to_plain(entity)
        for entity in sorted(state.entities.values(), key=lambda entity: entity.id)
    ]
    return {"ok": True, "entities": entities}


def list_known_facts(ctx: ToolContext) -> dict[str, object]:
    """Return current facts from the current projected state."""

    state = _project_state(ctx)
    facts = [
        to_plain(fact)
        for fact in sorted(state.facts.values(), key=lambda fact: fact.id)
    ]
    return {"ok": True, "facts": facts}
