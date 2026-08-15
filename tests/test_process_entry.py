from __future__ import annotations

from io import BytesIO, StringIO
from pathlib import Path
import subprocess
import sys

import pytest

from seed_runtime import process_entry
from seed_runtime.events import SQLiteEventLedger


def test_project_script_uses_the_live_process_entry():
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")

    assert 'seed = "seed_runtime.process_entry:main"' in pyproject
    assert 'seed = "scripts.seed_local:main"' not in pyproject


def test_importing_the_live_entry_does_not_wake_dormant_modules():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import sys; import seed_runtime.process_entry; "
                "assert 'scripts.seed_local' not in sys.modules; "
                "assert 'seed_runtime.observations' not in sys.modules; "
                "assert 'seed_runtime.state' not in sys.modules; "
                "assert 'seed_runtime.diagnostic_inventory' not in sys.modules; "
                "assert 'seed_runtime.diagnostic_shape_audit' not in sys.modules"
            ),
        ],
        check=False,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_live_entry_accepts_the_database_coordinate(monkeypatch, tmp_path):
    database = tmp_path / "seed.db"
    monkeypatch.setattr("sys.stdin", BytesIO(b"material\n"))
    monkeypatch.setattr("sys.stdout", StringIO())

    assert process_entry.main(["--db", str(database)]) == 0

    ledger = SQLiteEventLedger(database)
    try:
        assert ledger.list()
    finally:
        ledger.close()


def test_reopened_live_process_allocates_a_new_locality(tmp_path):
    database = tmp_path / "seed.db"
    command = [
        sys.executable,
        "-m",
        "seed_runtime.process_entry",
        "--db",
        str(database),
    ]

    for material in ("first\n", "second\n"):
        result = subprocess.run(
            command,
            input=material,
            check=False,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True,
        )
        assert result.returncode == 0, result.stderr

    ledger = SQLiteEventLedger(database)
    try:
        Localities = {event.locality_identity for event in ledger.list()}
    finally:
        ledger.close()
    assert None not in Localities
    assert len(Localities) == 2


@pytest.mark.parametrize(
    "flag",
    [
        "--diagnostic-inventory",
        "--diagnostic-shape-audit",
        "--json",
        "--status",
        "--mismatches",
    ],
)
def test_historical_operational_flag_is_not_on_the_live_entry(flag):
    with pytest.raises(SystemExit, match="2"):
        process_entry.main([flag])


def test_historical_ingestion_flag_is_not_on_the_live_entry():
    with pytest.raises(SystemExit, match="2"):
        process_entry.main(["--observe", "host", "status", "healthy"])
