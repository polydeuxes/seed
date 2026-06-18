from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import StateProjector


def test_host_notes_records_and_lists_notes_in_seed_ledger():
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/generated/host_notes/toolkit.yaml")
    projector = StateProjector(ledger)
    executor = ToolExecutor(ledger, registry, projector)

    added = executor.execute("ws", "ses", "add_host_note", {"host": "example_host", "note": "SSH pending review"})
    listed = executor.execute("ws", "ses", "list_host_notes", {"host": "example_host"})

    assert added.kind == "tool_result"
    assert listed.payload["output"]["notes"] == [
        {"id": added.payload["output"]["note_id"], "note": "SSH pending review"}
    ]
    assert "host_note.added" in [event.kind for event in ledger.list_events("ws")]
