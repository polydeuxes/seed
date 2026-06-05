"""RuntimeLoop context composition service.

This module owns the read-only construction of RuntimeContext for RuntimeLoop.
It does not read ledgers, append events, evaluate policy, execute tools, call
providers, mutate State, or change Runtime's legacy ContextComposer boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from seed_runtime.context_views import build_decision_context_view
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import State

if TYPE_CHECKING:
    from seed_runtime.runtime_loop import RuntimeContext, RuntimeInput


@dataclass(frozen=True)
class RuntimeLoopContextComposer:
    """Compose the RuntimeLoop provider context from explicit inputs."""

    tool_registry: ToolRegistry

    def compose(
        self,
        *,
        workspace_id: str,
        run_id: str,
        runtime_input: RuntimeInput,
        state: State,
    ) -> RuntimeContext:
        """Return the exact RuntimeContext shape RuntimeLoop providers receive."""

        from seed_runtime.runtime_loop import RuntimeContext

        tools = [
            {
                "name": tool.name,
                "summary": tool.summary,
                "policy_action": tool.policy_action,
                "risk_class": tool.risk_class,
            }
            for tool in self.tool_registry.list_tools(visible_only=True)
        ]
        decision_context = build_decision_context_view(state)
        return RuntimeContext(
            workspace_id=workspace_id,
            run_id=run_id,
            state=state,
            current_input={
                "text": runtime_input.user_text,
                "metadata": dict(runtime_input.metadata),
            },
            tools=tools,
            decision_context=decision_context,
        )
