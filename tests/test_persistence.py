from seed_runtime.events import SQLiteEventLedger
from seed_runtime.models import Entity
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


def test_sqlite_ledger_persists_events(tmp_path):
    db = tmp_path / "events.db"
    ledger = SQLiteEventLedger(str(db))
    ledger.append("entity.upserted", "ws", {"entity": to_plain(Entity(id="ent_1", kind="host", name="node-1"))})
    ledger.close()

    reopened = SQLiteEventLedger(str(db))
    state = StateProjector(reopened).project("ws")

    assert state.entities["ent_1"].name == "node-1"
    reopened.close()
