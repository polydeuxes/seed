from __future__ import annotations

from io import BytesIO, StringIO
from pathlib import Path
import subprocess
import sys

import pytest

from seed_runtime import process_entry
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.operator_material_source import (
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
)
from scripts.primordial_host_escape import primordial_host_input


def _acquired_material(database: Path) -> list[bytes]:
    ledger = SQLiteEventLedger(database)
    try:
        return [
            event.exact_material
            for event in ledger.list()
            if event.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
        ]
    finally:
        ledger.close()


def _event_kinds(database: Path) -> list[str]:
    ledger = SQLiteEventLedger(database)
    try:
        return [event.kind for event in ledger.list()]
    finally:
        ledger.close()


def _skip_unrelated_measurement_work(monkeypatch):
    class _AlreadyMeasured(set):
        def __contains__(self, _item):
            return True

    monkeypatch.setattr(
        "seed_runtime.operator_console._recorded_byte_measurement_material_references",
        lambda _ledger: _AlreadyMeasured(),
    )


def test_project_script_uses_the_live_process_entry():
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")

    assert 'seed = "seed_runtime.process_entry:main"' in pyproject
    assert 'seed = "scripts.seed_local:main"' not in pyproject


def test_live_entry_accepts_the_database_coordinate(monkeypatch, tmp_path):
    database = tmp_path / "seed.db"
    monkeypatch.setattr("sys.stdin", BytesIO())

    assert process_entry.main(["--db", str(database)]) == 0

    ledger = SQLiteEventLedger(database)
    try:
        assert ledger.list()
    finally:
        ledger.close()


def test_live_entry_calls_the_current_console_boundary(monkeypatch):
    calls = []

    def console(
        *,
        ledger,
        locality_identity,
        input_stream,
        command_handlers=None,
        operator_invocation_provider=None,
    ):
        calls.append(
            (
                ledger,
                locality_identity,
                input_stream,
                command_handlers,
                operator_invocation_provider,
            )
        )

    monkeypatch.setattr(process_entry, "run_persistent_operator_console", console)
    monkeypatch.setattr("sys.stdin", BytesIO(b""))

    assert process_entry.main([]) == 0
    assert len(calls) == 1
    assert calls[0][3] is None
    assert calls[0][4] is process_entry.invoke_operator_host


@pytest.mark.parametrize("frame", (b"/", b"/\n", b"/\r\n"))
def test_primordial_slash_frame_is_the_existing_eof_boundary(
    monkeypatch, tmp_path, frame
):
    escape_database = tmp_path / "escape.db"
    eof_database = tmp_path / "eof.db"
    provider_calls = []

    def provider(material, _supply):
        provider_calls.append(material)
        raise AssertionError("primordial slash reached the host provider")

    monkeypatch.setattr(process_entry, "invoke_operator_host", provider)
    monkeypatch.setattr("sys.stdin", BytesIO(frame))
    assert process_entry.main(["--db", str(escape_database)]) == 0
    monkeypatch.setattr("sys.stdin", BytesIO(b""))
    assert process_entry.main(["--db", str(eof_database)]) == 0

    assert provider_calls == []
    assert _acquired_material(escape_database) == []
    assert _event_kinds(escape_database) == _event_kinds(eof_database)


def test_primordial_slash_preserves_prior_occurrences_and_ends_input(
    monkeypatch, tmp_path
):
    _skip_unrelated_measurement_work(monkeypatch)
    database = tmp_path / "seed.db"
    monkeypatch.setattr("sys.stdin", BytesIO(b"prior \xff\x00\n/\nnot acquired\n"))

    assert process_entry.main(["--db", str(database)]) == 0

    assert _acquired_material(database) == [b"prior \xff\x00\n"]


def test_other_slash_material_remains_exact_operator_material(monkeypatch, tmp_path):
    _skip_unrelated_measurement_work(monkeypatch)
    database = tmp_path / "seed.db"
    material = b"/exit\n/quit\r\n/\xff\x00 material\n"
    monkeypatch.setattr("sys.stdin", BytesIO(material))

    assert process_entry.main(["--db", str(database)]) == 0

    assert _acquired_material(database) == [
        b"/exit\n",
        b"/quit\r\n",
        b"/\xff\x00 material\n",
    ]


def test_host_escape_preserves_non_bytes_and_bytes_subclass_boundaries():
    class EqualSlash(bytes):
        pass

    exact_subclass = EqualSlash(b"/\n")

    class Boundary:
        def __init__(self):
            self.material = iter((exact_subclass, b"after\n"))

        def readline(self):
            return next(self.material)

    boundary = primordial_host_input(Boundary())
    text_boundary = primordial_host_input(StringIO("/\n"))

    assert boundary.readline() is exact_subclass
    assert boundary.readline() == b"after\n"
    assert text_boundary.readline() == "/\n"


@pytest.mark.parametrize(
    "material",
    (
        b"",
        b"//\n",
        b"/exit\n",
        b"/quit\r\n",
        b"/\r",
        b"/\xff\x00\n",
        b" /\n",
    ),
)
def test_host_escape_does_not_decode_or_reframe_other_bytes(material):
    boundary = primordial_host_input(BytesIO(material))

    assert boundary.readline() == material


def test_host_escape_latches_without_consuming_later_buffered_material():
    source = BytesIO(b"/\nafter\n")
    boundary = primordial_host_input(source)

    assert boundary.readline() == b""
    assert boundary.readline() == b""
    assert source.readline() == b"after\n"


def test_reopened_live_process_allocates_a_new_locality(tmp_path):
    database = tmp_path / "seed.db"
    command = [
        sys.executable,
        "-m",
        "seed_runtime.process_entry",
        "--db",
        str(database),
    ]

    for _invocation in range(2):
        result = subprocess.run(
            command,
            input="",
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


def test_live_entry_has_only_help_and_database_flags():
    parser = process_entry.build_parser()

    assert [tuple(action.option_strings) for action in parser._actions] == [
        ("-h", "--help"),
        ("--db",),
    ]
