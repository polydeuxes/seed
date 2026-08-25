from __future__ import annotations

import os
import subprocess
import time

import pytest

from scripts import operator_host_provider
from seed_runtime.supplied_invocation_material import (
    SuppliedWitnessMaterialOccurrence,
)


class _PopenReached(Exception):
    pass


def _invoke(command):
    supplied = []
    result = operator_host_provider.invoke_operator_host(
        command, supplied.append
    )
    assert result is None
    return tuple(supplied)


@pytest.mark.parametrize(
    ("command", "argv"),
    (
        (b"!ls\n", (b"/usr/bin/ls",)),
        (
            b"!calculator 2+2\n",
            (b"/usr/bin/gnome-calculator", b"--solve=2+2"),
        ),
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
        operator_host_provider.invoke_operator_host(command, lambda _item: None)

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
            b"!pytest tests/path with spaces.py::test_one\n",
            lambda _item: None,
        )

    argv, coordinates = calls[0]
    assert argv == (
        *operator_host_provider._PYTEST_INVOCATION,
        b"tests/path with spaces.py::test_one",
    )
    assert coordinates["env"] == {
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    assert coordinates["cwd"] == operator_host_provider._ROOT
    assert "PYTEST_ADDOPTS" not in coordinates["env"]


@pytest.mark.parametrize(
    "command",
    (
        b"!sh\n",
        b"!cat a\x00b\n",
        b"!pytest a\x00b\n",
        b"!calculator\n",
        b"!calculator 2+\x002\n",
        b"ls\n",
    ),
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
        operator_host_provider.invoke_operator_host(command, lambda _item: None)


def test_calculator_provider_preserves_supplied_material_and_completion(
    monkeypatch,
):
    def bounded(
        argv,
        *,
        supply,
        time_boundary_second_count,
        material_byte_count_boundary,
    ):
        assert argv == (
            b"/usr/bin/gnome-calculator",
            b"--solve=2+2",
        )
        assert (
            time_boundary_second_count
            == operator_host_provider.TIME_BOUNDARY_SECOND_COUNT
        )
        assert (
            material_byte_count_boundary
            == operator_host_provider.MATERIAL_BYTE_COUNT_BOUNDARY
        )
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"exact output material",
                "invocation output occurrence 0",
            )
        )
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"exact error material",
                "invocation error occurrence 0",
            )
        )
        return False, False, False

    monkeypatch.setattr(operator_host_provider, "_bounded_invocation", bounded)

    supplied = _invoke(b"!calculator 2+2\n")

    assert supplied == (
        SuppliedWitnessMaterialOccurrence(
            b"exact output material",
            "invocation output occurrence 0",
        ),
        SuppliedWitnessMaterialOccurrence(
            b"exact error material",
            "invocation error occurrence 0",
        ),
        SuppliedWitnessMaterialOccurrence(
            b"",
            "invocation completion",
        ),
    )


def test_cat_preserves_exact_posix_path_and_material(tmp_path):
    directory = os.fsencode(tmp_path)
    path = directory + b"/material-\xff"
    exact = b"\x00\xffexact material\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(descriptor, exact)
    finally:
        os.close(descriptor)

    supplied = _invoke(b"!cat " + path + b"\n")

    assert tuple(occurrence.exact_bytes for occurrence in supplied) == (
        exact,
        b"",
        b"",
    )
    assert len({occurrence.source_boundary for occurrence in supplied}) == 3


def test_ls_preserves_a_non_utf8_posix_path(tmp_path):
    directory = os.fsencode(tmp_path)
    name = b"entry-\xff"
    path = directory + b"/" + name
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(descriptor)

    supplied = _invoke(b"!ls " + directory + b"\n")

    assert tuple(occurrence.exact_bytes for occurrence in supplied) == (
        name + b"\n",
        b"",
        b"",
    )


def test_host_material_boundary_is_one_mebibyte():
    assert operator_host_provider.MATERIAL_BYTE_COUNT_BOUNDARY == 1_048_576


def test_cat_preserves_finite_material_across_multiple_pipe_reads(tmp_path):
    exact = (bytes(range(256)) * 851) + bytes(range(256))[:202]
    assert len(exact) == 218_058
    path = tmp_path / "multiple-pipe-reads"
    path.write_bytes(exact)

    supplied = _invoke(b"!cat " + bytes(path) + b"\n")
    output = next(
        occurrence
        for occurrence in supplied
        if occurrence.source_boundary == "invocation output"
    )

    assert output.exact_bytes == exact
    assert tuple(
        len(occurrence.exact_bytes)
        for occurrence in output.read_occurrences
    ) == (
        65_536,
        65_536,
        65_536,
        21_450,
    )
    assert b"".join(
        occurrence.exact_bytes for occurrence in output.read_occurrences
    ) == exact
    assert tuple(
        occurrence.invocation_position
        for occurrence in output.read_occurrences
    ) == tuple(sorted(
        occurrence.invocation_position
        for occurrence in output.read_occurrences
    ))
    assert all(occurrence.known_loss == () for occurrence in supplied)


def test_host_output_is_bounded_without_returncode_material():
    supplied = _invoke(b"!cat /dev/zero\n")

    output = next(
        occurrence
        for occurrence in supplied
        if occurrence.source_boundary == "invocation output"
    )
    assert len(output.exact_bytes) == (
        operator_host_provider.MATERIAL_BYTE_COUNT_BOUNDARY
    )
    assert tuple(
        occurrence.source_boundary for occurrence in output.read_occurrences
    ) == tuple(
        f"invocation output read {position}"
        for position in range(len(output.read_occurrences))
    )
    assert output.known_loss
    assert supplied[-1].exact_bytes == b""
    assert supplied[-1].known_loss


def test_bounded_invocation_uses_its_exact_material_byte_count_boundary():
    supplied = []

    timed_out, output_truncated, error_truncated = (
        operator_host_provider._bounded_invocation(
            (b"/usr/bin/printf", b"abcdef"),
            supply=supplied.append,
            time_boundary_second_count=1.0,
            material_byte_count_boundary=3,
        )
    )

    assert not timed_out
    assert output_truncated
    assert not error_truncated
    assert tuple(occurrence.exact_bytes for occurrence in supplied) == (
        b"abc",
        b"",
    )


@pytest.mark.parametrize(
    ("time_boundary_second_count", "material_byte_count_boundary"),
    (
        (0.0, 3),
        (1, 3),
        (1.0, 0),
        (1.0, 3.0),
    ),
)
def test_bounded_invocation_refuses_invalid_exact_boundaries_before_process(
    monkeypatch,
    time_boundary_second_count,
    material_byte_count_boundary,
):
    monkeypatch.setattr(
        subprocess,
        "Popen",
        lambda *args, **kwargs: pytest.fail((args, kwargs)),
    )

    with pytest.raises(TypeError):
        operator_host_provider._bounded_invocation(
            (b"/usr/bin/printf", b"exact"),
            supply=lambda _occurrence: None,
            time_boundary_second_count=time_boundary_second_count,
            material_byte_count_boundary=material_byte_count_boundary,
        )


def test_completed_invocation_is_not_recast_as_timed_out_by_a_slow_consumer(
    monkeypatch,
):
    supplied = []

    def slow_consumer(occurrence):
        supplied.append(occurrence)
        if len(supplied) == 1:
            time.sleep(0.03)

    timed_out, output_truncated, error_truncated = (
        operator_host_provider._bounded_invocation(
            (b"/usr/bin/printf", b"exact"),
            supply=slow_consumer,
            time_boundary_second_count=0.01,
            material_byte_count_boundary=64,
        )
    )

    assert not timed_out
    assert not output_truncated
    assert not error_truncated
    assert tuple(occurrence.exact_bytes for occurrence in supplied) == (
        b"exact",
        b"",
    )


def test_inherited_open_pipe_is_bounded_without_recasting_parent_as_timed_out(
    monkeypatch,
):
    supplied = []
    program = (
        b"import os,time\n"
        b"if os.fork() == 0:\n"
        b" time.sleep(0.5)\n"
        b" os._exit(0)\n"
        b"os.write(1,b'exact')\n"
        b"os._exit(0)\n"
    )

    timed_out, output_truncated, error_truncated = (
        operator_host_provider._bounded_invocation(
            (operator_host_provider._PYTEST_INVOCATION[0], b"-c", program),
            supply=supplied.append,
            time_boundary_second_count=0.05,
            material_byte_count_boundary=64,
        )
    )

    assert not timed_out
    assert output_truncated
    assert error_truncated
    assert tuple(occurrence.exact_bytes for occurrence in supplied) == (
        b"exact",
        b"",
    )


def test_pytest_provider_supplies_process_material_and_completion():
    nodeid = (
        b"tests/test_book_material_acquisition.py::"
        b"test_book_material_witness_has_one_admitted_subject"
    )
    supplied = _invoke(b"!pytest " + nodeid + b"\n")

    process_material = tuple(
        occurrence
        for occurrence in supplied
        if occurrence.source_boundary in ("invocation output", "invocation error")
    )
    completion = supplied[-1]
    assert process_material
    assert all(
        occurrence.source_boundary in ("invocation output", "invocation error")
        for occurrence in process_material
    )
    assert any(
        occurrence.exact_bytes
        for occurrence in process_material
        if occurrence.source_boundary == "invocation output"
    )
    assert completion.source_boundary == "invocation completion"
    assert completion.exact_bytes == b""
    assert completion.known_loss == ()


@pytest.mark.parametrize(
    ("timed_out", "output_truncated", "error_truncated"),
    (
        (True, False, False),
        (False, True, False),
        (False, False, True),
    ),
)
def test_bounded_pytest_preserves_partial_results_and_known_completion_loss(
    monkeypatch, timed_out, output_truncated, error_truncated
):
    def bounded(*args, supply, **kwargs):
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"partial out",
                "invocation output occurrence 0",
            )
        )
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"partial error",
                "invocation error occurrence 0",
            )
        )
        return timed_out, output_truncated, error_truncated

    monkeypatch.setattr(
        operator_host_provider,
        "_bounded_invocation",
        bounded,
    )

    supplied = _invoke(b"!pytest tests/exact.py\n")

    assert tuple(occurrence.exact_bytes for occurrence in supplied) == (
        b"partial out",
        b"partial error",
        b"",
    )
    assert supplied[0].known_loss == ()
    assert supplied[1].known_loss == ()
    assert supplied[2].known_loss


def test_pytest_provider_death_is_not_replaced_by_supplied_results(monkeypatch):
    def die(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(operator_host_provider, "_bounded_invocation", die)

    with pytest.raises(KeyboardInterrupt):
        _invoke(b"!pytest tests/exact.py\n")
