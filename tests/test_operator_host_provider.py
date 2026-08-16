from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

import pytest

from scripts import operator_host_provider


class _PopenReached(Exception):
    pass


@pytest.mark.parametrize(
    ("command", "argv"),
    (
        (b"!ls\n", (b"/usr/bin/ls",)),
        (
            b"!cat path with spaces\r\n",
            (b"/usr/bin/cat", b"--", b"path with spaces"),
        ),
        (b"!ls\t\xff\n", (b"/usr/bin/ls", b"--", b"\xff")),
        (
            b"!pytest tests/exact.py::test_one\n",
            (
                *operator_host_provider._PYTEST_INVOCATION,
                b"tests/exact.py::test_one",
            ),
        ),
    ),
)
def test_host_provider_uses_only_fixed_argv_without_a_shell(
    monkeypatch, command, argv
):
    calls = []

    def reached(supplied_argv, **kwargs):
        calls.append((supplied_argv, kwargs))
        raise _PopenReached

    monkeypatch.setattr(subprocess, "Popen", reached)
    with pytest.raises(_PopenReached):
        operator_host_provider.invoke_operator_host(command)

    assert calls[0][0] == argv
    assert calls[0][1]["shell"] is False
    assert calls[0][1]["stdin"] is subprocess.DEVNULL


def test_pytest_provider_has_one_exact_argument_and_a_clean_environment(
    monkeypatch,
):
    calls = []

    def reached(supplied_argv, **kwargs):
        calls.append((supplied_argv, kwargs))
        raise _PopenReached

    monkeypatch.setenv("PYTEST_ADDOPTS", "developer supplied")
    monkeypatch.setattr(subprocess, "Popen", reached)
    with pytest.raises(_PopenReached):
        operator_host_provider.invoke_operator_host(
            b"!pytest tests/path with spaces.py::test_one\n"
        )

    argv, coordinates = calls[0]
    assert argv == (
        *operator_host_provider._PYTEST_INVOCATION,
        b"tests/path with spaces.py::test_one",
    )
    assert coordinates["env"] == {
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "SEED_IMPLEMENTATION_FUNCTION_MEASUREMENT": coordinates["env"][
            "SEED_IMPLEMENTATION_FUNCTION_MEASUREMENT"
        ],
    }
    assert coordinates["cwd"] == operator_host_provider._ROOT
    assert "PYTEST_ADDOPTS" not in coordinates["env"]


@pytest.mark.parametrize(
    "command",
    (b"!sh\n", b"!cat a\x00b\n", b"!pytest a\x00b\n", b"ls\n"),
)
def test_unknown_or_unrepresentable_host_invocation_is_refused_before_process(
    monkeypatch, command
):
    monkeypatch.setattr(
        subprocess,
        "Popen",
        lambda *args, **kwargs: pytest.fail((args, kwargs)),
    )
    with pytest.raises(operator_host_provider.OperatorHostProviderError):
        operator_host_provider.invoke_operator_host(command)


def test_cat_preserves_exact_posix_path_and_material(tmp_path):
    directory = os.fsencode(tmp_path)
    path = directory + b"/material-\xff"
    exact = b"\x00\xffexact material\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(descriptor, exact)
    finally:
        os.close(descriptor)

    supplied = operator_host_provider.invoke_operator_host(
        b"!cat " + path + b"\n"
    )

    assert tuple(occurrence.exact_bytes for occurrence in supplied.occurrences) == (
        exact,
        b"",
        b"",
    )
    assert len(
        {occurrence.source_boundary for occurrence in supplied.occurrences}
    ) == 3
    assert supplied.egress_occurrence_positions == (0, 1)


def test_ls_preserves_a_non_utf8_posix_path(tmp_path):
    directory = os.fsencode(tmp_path)
    name = b"entry-\xff"
    path = directory + b"/" + name
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(descriptor)

    supplied = operator_host_provider.invoke_operator_host(
        b"!ls " + directory + b"\n"
    )

    assert tuple(occurrence.exact_bytes for occurrence in supplied.occurrences) == (
        name + b"\n",
        b"",
        b"",
    )


def test_host_output_is_bounded_without_returncode_material():
    supplied = operator_host_provider.invoke_operator_host(b"!cat /dev/zero\n")

    assert len(supplied.occurrences[0].exact_bytes) == (
        operator_host_provider.MATERIAL_BYTE_LIMIT
    )
    assert supplied.occurrences[0].known_loss
    assert supplied.occurrences[-1].exact_bytes == b""


def test_pytest_provider_supplies_a_distinct_exact_measurement_artifact():
    nodeid = (
        b"tests/test_implementation_function_measurement.py::"
        b"test_compiled_code_supplies_identities_without_ast_taxonomy"
    )

    supplied = operator_host_provider.invoke_operator_host(
        b"!pytest " + nodeid + b"\n"
    )

    assert supplied.egress_occurrence_positions == (0, 1)
    assert tuple(
        occurrence.source_boundary for occurrence in supplied.occurrences
    ) == (
        "invocation output",
        "invocation error",
        "implementation function measurement",
        "invocation end",
    )
    assert supplied.occurrences[0].exact_bytes
    assert supplied.occurrences[1].exact_bytes == b""
    artifact = json.loads(supplied.occurrences[2].exact_bytes)
    assert [occurrence["pytest_identity"] for occurrence in artifact["pytest"]] == [
        nodeid.decode("ascii")
    ]
    implementation_positions = {
        coordinate["implementation_function_position"]
        for coordinate in artifact["pytest"][0]["python"]
    }
    assert implementation_positions
    assert all(
        position < len(artifact["python"])
        for position in implementation_positions
    )
    assert supplied.occurrences[2].known_loss == ()
    assert supplied.occurrences[3].exact_bytes == b""


def test_missing_pytest_measurement_artifact_is_refused(monkeypatch):
    monkeypatch.setattr(
        operator_host_provider,
        "_bounded_invocation",
        lambda *args, **kwargs: (b"out", b"error", False, False, False),
    )

    with pytest.raises(
        operator_host_provider.OperatorHostProviderError,
        match="exact implementation measurement material required",
    ):
        operator_host_provider.invoke_operator_host(b"!pytest tests/exact.py\n")


@pytest.mark.parametrize(
    ("timed_out", "output_limited", "error_limited"),
    (
        (True, False, False),
        (False, True, False),
        (False, False, True),
    ),
)
def test_bounded_pytest_preserves_partial_results_and_known_artifact_loss(
    monkeypatch, timed_out, output_limited, error_limited
):
    monkeypatch.setattr(
        operator_host_provider,
        "_bounded_invocation",
        lambda *args, **kwargs: (
            b"partial out",
            b"partial error",
            timed_out,
            output_limited,
            error_limited,
        ),
    )

    supplied = operator_host_provider.invoke_operator_host(
        b"!pytest tests/exact.py\n"
    )

    assert tuple(occurrence.exact_bytes for occurrence in supplied.occurrences) == (
        b"partial out",
        b"partial error",
        b"",
        b"",
    )
    assert all(
        supplied.occurrences[position].known_loss for position in (0, 1, 2)
    )
    assert supplied.occurrences[3].known_loss == ()


def test_pytest_measurement_artifact_is_bounded(tmp_path):
    path = tmp_path / "measurement"
    exact = b"x" * (operator_host_provider.IMPLEMENTATION_MEASUREMENT_BYTE_LIMIT + 1)
    path.write_bytes(exact)

    material, limited = operator_host_provider._bounded_artifact(path)

    assert material == exact[:-1]
    assert limited is True


def test_pytest_provider_death_is_not_replaced_by_supplied_results(monkeypatch):
    def die(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(operator_host_provider, "_bounded_invocation", die)

    with pytest.raises(KeyboardInterrupt):
        operator_host_provider.invoke_operator_host(b"!pytest tests/exact.py\n")
