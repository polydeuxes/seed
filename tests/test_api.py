from seed_runtime.api import SeedAPI
from seed_runtime.context import ContextComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.models import Decision
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import FakeDecisionModel, Runtime
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService


def test_api_shell_exposes_message_state_and_tools():
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    projector = StateProjector(ledger)
    runtime = Runtime(
        ledger,
        projector,
        ContextComposer(registry),
        DecisionValidator(registry),
        ToolExecutor(ledger, registry, projector),
        ToolNeedService(ledger, projector),
        FakeDecisionModel(Decision(kind="answer", reason="ok", answer="done")),
    )
    api = SeedAPI(runtime, projector, registry)

    assert api.post_user_message("ws", "ses", "hello").message == "done"
    assert api.get_state("ws")["workspace_id"] == "ws"
    assert api.get_tools()[0]["name"] == "echo"
