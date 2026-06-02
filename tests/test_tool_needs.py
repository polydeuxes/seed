from seed_runtime.events import EventLedger
from seed_runtime.models import Decision
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService


def test_creates_need_from_decision_and_deduplicates_open_need():
    ledger = EventLedger()
    service = ToolNeedService(ledger, StateProjector(ledger))
    decision = Decision(kind="request_tool", reason="missing", tool_need={"name": "Install SSH Server", "summary": "Install and start SSH server", "capability": "ssh_access"})

    first = service.create_from_decision("ws", decision, "evt_1")
    second = service.create_from_decision("ws", decision, "evt_2")

    assert first.id == second.id
    assert first.name == "install_ssh_server"
    assert [event.kind for event in ledger.list_events("ws")].count("tool_need.created") == 1
