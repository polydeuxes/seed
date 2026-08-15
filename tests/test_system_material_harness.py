from __future__ import annotations

from scripts import system_material_harness
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.material_ingest import ingested_material_bytes


def test_file_material_crosses_the_live_system_ingest_signature(tmp_path, capsys):
    database = tmp_path / "seed.db"
    supplied = tmp_path / "supplied.bin"
    supplied.write_bytes(b"\x00exact\xff")

    assert system_material_harness.main(
        [
            "--db",
            str(database),
            "--locality",
            "locality_000001",
            "--file",
            str(supplied),
        ]
    ) == 0

    ledger = SQLiteEventLedger(database)
    try:
        events = ledger.list_locality("locality_000001")
        result = events[-1]
        assert ingested_material_bytes(result) == b"\x00exact\xff"
    finally:
        ledger.close()

    assert "locality_000001" in capsys.readouterr().out
