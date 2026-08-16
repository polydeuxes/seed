from __future__ import annotations

from io import BytesIO, StringIO
from pathlib import Path
import os
import subprocess
import sys

import pytest

from seed_runtime import process_entry
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND
from seed_runtime.operator_material_acquisition import (
    OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
)
from scripts.primordial_host_escape import primordial_host_input


class _LiveOutput(StringIO):
    def __init__(self) -> None:
        super().__init__()
        self.buffer = BytesIO()


def _acquired_material(database: Path) -> list[bytes]:
    ledger = SQLiteEventLedger(database)
    try:
        return [
            event.exact_material
            for event in ledger.list()
            if event.kind == OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
        ]
    finally:
        ledger.close()


def _event_kinds(database: Path) -> list[str]:
    ledger = SQLiteEventLedger(database)
    try:
        return [event.kind for event in ledger.list()]
    finally:
        ledger.close()


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


def test_live_entry_does_not_emit_operator_material_back_to_stdout(
    monkeypatch, tmp_path
):
    output = _LiveOutput()
    monkeypatch.setattr("sys.stdin", BytesIO(b"hello\n"))
    monkeypatch.setattr("sys.stdout", output)

    assert process_entry.main(["--db", str(tmp_path / "seed.db")]) == 0

    assert output.buffer.getvalue() == b""
    assert output.getvalue() == ""


@pytest.mark.parametrize("frame", (b"/", b"/\n", b"/\r\n"))
def test_primordial_slash_frame_is_the_existing_eof_boundary(
    monkeypatch, tmp_path, frame
):
    escape_database = tmp_path / "escape.db"
    eof_database = tmp_path / "eof.db"
    provider_calls = []

    def provider(material):
        provider_calls.append(material)
        raise AssertionError("primordial slash reached the host provider")

    monkeypatch.setattr(process_entry, "invoke_operator_host", provider)
    monkeypatch.setattr("sys.stdout", _LiveOutput())
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
    database = tmp_path / "seed.db"
    monkeypatch.setattr("sys.stdin", BytesIO(b"prior \xff\x00\n/\nnot acquired\n"))
    monkeypatch.setattr("sys.stdout", StringIO())

    assert process_entry.main(["--db", str(database)]) == 0

    assert _acquired_material(database) == [b"prior \xff\x00\n"]


def test_other_slash_material_remains_exact_operator_material(monkeypatch, tmp_path):
    database = tmp_path / "seed.db"
    material = b"/exit\n/quit\r\n/\xff\x00 material\n"
    monkeypatch.setattr("sys.stdin", BytesIO(material))
    monkeypatch.setattr("sys.stdout", StringIO())

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


@pytest.mark.parametrize("name", ("ls", "cat"))
def test_live_process_composes_the_bounded_host_provider(tmp_path, name):
    directory = tmp_path / "source"
    directory.mkdir()
    material = b"\x00\xffhost material\n"
    path = directory / "one"
    path.write_bytes(material)
    addressed = directory if name == "ls" else path
    expected = b"one\n" if name == "ls" else material

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "seed_runtime.process_entry",
            "--db",
            str(tmp_path / f"{name}.db"),
        ],
        input=b"!" + name.encode("ascii") + b" " + os.fsencode(addressed) + b"\n",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        cwd=str(Path(__file__).resolve().parent.parent),
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout == expected


def test_live_process_ingests_pytest_measurement_without_egressing_it(tmp_path):
    database = tmp_path / "pytest.db"
    nodeid = (
        b"tests/test_implementation_function_measurement.py::"
        b"test_compiled_code_supplies_identities_without_ast_taxonomy"
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "seed_runtime.process_entry",
            "--db",
            str(database),
        ],
        input=b"!pytest " + nodeid + b"\n",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        cwd=str(Path(__file__).resolve().parent.parent),
    )

    assert result.returncode == 0, result.stderr
    ledger = SQLiteEventLedger(database)
    try:
        ingests = [
            event
            for event in ledger.list()
            if event.kind == MATERIAL_INGEST_OCCURRED_KIND
        ]
    finally:
        ledger.close()
    assert len(ingests) == 6
    assert [event.material["source_boundary"] for event in ingests[-5:]] == [
        "invocation output",
        "invocation error",
        "implementation function catalog",
        "implementation function measurement",
        "invocation end",
    ]
    assert [
        event.material["provenance_occurrence_references"]
        for event in ingests[-5:]
    ] == [[ingests[0].identity]] * 5
    assert result.stdout == (
        ingests[-5].exact_material + ingests[-4].exact_material
    )
    assert result.stderr == b""
    assert ingests[-3].exact_material
    assert ingests[-3].exact_material not in result.stdout
    assert ingests[-2].exact_material
    assert ingests[-2].exact_material not in result.stdout
    assert ingests[-1].exact_material == b""


def test_live_entry_has_only_help_and_database_flags():
    parser = process_entry.build_parser()

    assert [tuple(action.option_strings) for action in parser._actions] == [
        ("-h", "--help"),
        ("--db",),
    ]
