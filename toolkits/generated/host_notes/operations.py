"""Generated-style host note operations.

These tools intentionally mutate only Seed's ledger. They are a safe first demo
for generated toolkit registration because they do not contact or change hosts.
"""

from __future__ import annotations

from seed_runtime.execution import ToolContext
from seed_runtime.ids import new_id


def add_host_note(ctx: ToolContext, host: str, note: str) -> dict[str, object]:
    note_id = new_id("note")
    ctx.ledger.append(
        "host_note.added",
        ctx.workspace_id,
        {"id": note_id, "host": host, "note": note},
        actor="tool",
        session_id=ctx.session_id,
        causation_id=ctx.call_event_id,
    )
    return {
        "ok": True,
        "host": host,
        "note_id": note_id,
        "summary": f"Recorded note for {host}.",
    }


def list_host_notes(ctx: ToolContext, host: str) -> dict[str, object]:
    notes = []
    for event in ctx.ledger.list_events(ctx.workspace_id):
        if event.kind != "host_note.added":
            continue
        if event.payload.get("host") != host:
            continue
        notes.append({"id": event.payload["id"], "note": event.payload["note"]})
    return {"ok": True, "host": host, "notes": notes}
