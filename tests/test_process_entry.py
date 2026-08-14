from __future__ import annotations

from io import StringIO
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
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_live_entry_accepts_only_console_coordinates(monkeypatch, tmp_path):
    database = tmp_path / "seed.db"
    monkeypatch.setattr("sys.stdin", StringIO("material\nexit\n"))
    monkeypatch.setattr("sys.stdout", StringIO())

    assert process_entry.main(["--db", str(database), "--workspace", "w"]) == 0

    ledger = SQLiteEventLedger(database)
    try:
        assert ledger.list("w")
    finally:
        ledger.close()


def test_reopened_live_process_allocates_a_new_session(tmp_path):
    database = tmp_path / "seed.db"
    command = [
        sys.executable,
        "-m",
        "seed_runtime.process_entry",
        "--db",
        str(database),
    ]

    for material in ("first\nexit\n", "second\nexit\n"):
        result = subprocess.run(
            command,
            input=material,
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr

    ledger = SQLiteEventLedger(database)
    try:
        sessions = {event.session_id for event in ledger.list("local")}
    finally:
        ledger.close()
    assert None not in sessions
    assert len(sessions) == 2


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
