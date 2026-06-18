from seed_runtime.context import ContextComposer
from seed_runtime.events import EventLedger
from seed_runtime.models import Entity, Goal, ToolNeed
from seed_runtime.registry import ToolRegistry
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


def test_context_packet_shape_is_deterministic():
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    ledger.append("entity.upserted", "ws", {"entity": to_plain(Entity(id="ent_1", kind="host", name="example_host"))})
    ledger.append("goal.created", "ws", {"goal": to_plain(Goal(id="goal_1", workspace_id="ws", summary="Make SSH work"))})
    ledger.append("tool_need.created", "ws", {"tool_need": to_plain(ToolNeed(id="need_1", workspace_id="ws", name="install_ssh_server", summary="Install SSH", capability="ssh_access", reason="missing"))})
    input_event = ledger.append("input.user_message", "ws", {"text": "hello"}, actor="user", session_id="ses")
    state = StateProjector(ledger).project("ws")

    packet = ContextComposer(registry).compose("ws", "ses", input_event, state)

    assert packet.current_input["text"] == "hello"
    assert packet.active_goal["summary"] == "Make SSH work"
    assert [tool["name"] for tool in packet.tools] == ["echo"]
    assert [need["name"] for need in packet.open_tool_needs] == ["install_ssh_server"]
